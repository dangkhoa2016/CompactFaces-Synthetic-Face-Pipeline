"""Optional Modal GPU smoke test for CompactFaces. Run explicitly; no public endpoint.

Commands:
  modal run modal_app.py::verify_models  # CPU, hashes 5 model artifacts
  modal run modal_app.py::generate_pair  # paid A10G GPU, outputs to separate Volume

NOT a deterministic reconstruction of 935 curated images.
"""
from __future__ import annotations

import os
from pathlib import Path

import modal

SDCPP_REF = "77b72a2efed78f55de26892c7e909cee001e8b83"
MODEL_VOLUME_NAME = os.environ.get("COMPACTFACES_MODEL_VOLUME", "compactfaces-example-models-v1")
OUTPUT_VOLUME_NAME = os.environ.get("COMPACTFACES_OUTPUT_VOLUME", "compactfaces-example-results-v1")

app = modal.App("compactfaces-gpu-smoke-example")
model_vol = modal.Volume.from_name(MODEL_VOLUME_NAME, create_if_missing=False)
result_vol = modal.Volume.from_name(OUTPUT_VOLUME_NAME, create_if_missing=False)
manifest_file = Path(__file__).resolve().parent / "scripts" / "model_assets.py"

cpu_image = (
    modal.Image.debian_slim(python_version="3.11")
    .add_local_file(str(manifest_file), remote_path="/app/model_assets.py")
)

# This is an independently pinned candidate source revision, not the
# historical runtime build. Building may require further compatibility fixes.
gpu_image = (
    modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu22.04", add_python="3.11")
    .apt_install("build-essential", "cmake", "ninja-build", "git", "libgomp1",
                 "libstdc++6", "ca-certificates", "pkg-config", "libcurl4-openssl-dev")
    .run_commands(
        "git clone --recursive https://github.com/leejet/stable-diffusion.cpp /opt/sd-source",
        f"git -C /opt/sd-source checkout --detach {SDCPP_REF}",
        "git -C /opt/sd-source submodule update --init --recursive",
        "cmake -S /opt/sd-source -B /opt/sd-source/build -G Ninja "
        "-DCMAKE_BUILD_TYPE=Release -DSD_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86 "
        "-DSD_WEBP=OFF -DSD_WEBM=OFF",
        "cmake --build /opt/sd-source/build --config Release --parallel 8",
        "test -x /opt/sd-source/build/bin/sd-cli",
    )
    .add_local_file(str(manifest_file), remote_path="/app/model_assets.py")
)


@app.function(
    image=cpu_image,
    volumes={"/models": model_vol.with_mount_options(read_only=True)},
    timeout=1500,
)
def verify_models() -> dict:
    """CPU-only SHA256 verification; this can incur storage/CPU charges."""
    import sys
    sys.path.insert(0, "/app")
    from model_assets import inspect
    result = inspect(Path("/models"), verify_hashes=True)
    if result["verdict"] != "PASS":
        raise ValueError("MODEL_PREFLIGHT_FAILED: " +
                         ", ".join(f"{k}={v['status']}" for k, v in result["models"].items()))
    import json
    print("MODEL_PREFLIGHT_PASS: five recorded fingerprints")
    print(json.dumps({"verdict": result["verdict"],
                      "model_count": result["model_count"],
                      "sha256_verified": result["sha256_verified"]}))
    return result


@app.function(
    image=gpu_image,
    gpu="A10G",
    volumes={"/models": model_vol.with_mount_options(read_only=True), "/output": result_vol},
    timeout=3000,
    cpu=6,
    memory=32768,
)
def generate_pair() -> dict:
    """Explicit A10G invocation. Builds SOURCE and P2, validates PNG and commits results."""
    import hashlib
    import json
    import struct
    import subprocess
    import sys
    import time
    import uuid
    from datetime import datetime, timezone

    sys.path.insert(0, "/app")
    from model_assets import ASSETS, inspect

    checked = inspect(Path("/models"), verify_hashes=True)
    if checked["verdict"] != "PASS":
        raise ValueError("MODEL_PREFLIGHT_FAILED: do not generate with incorrect weights")
    paths = {role: str(Path("/models") / spec[0]) for role, spec in ASSETS.items()}
    binary = "/opt/sd-source/build/bin/sd-cli"
    if not Path(binary).is_file():
        raise FileNotFoundError("Pinned sd-cli build missing")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    directory = Path("/output") / run_id
    directory.mkdir(parents=True, exist_ok=False)
    source = directory / "SOURCE.png"
    pose = directory / "P2.png"
    # Describe the same concrete hairstyle in BOTH prompts. This improves
    # consistency for the documented example; not a general identity guarantee.
    hairstyle = ("distinct dark black swept-up medium short quiff with volume above forehead, "
                 "clean very short tapered sides, visible clean hairline, ")
    prompt_source = (
        "Photorealistic adult man, natural face, 1024px head and shoulders portrait, "
        + hairstyle
        + "straight-facing neutral expression, no smile, "
          "dark navy crew-neck shirt, plain light gray seamless studio backdrop."
    )
    prompt_pose = (
        "Edit the attached SOURCE as the SAME individual. Head turned 45 degrees "
        "to his right, a three-quarter profile with the nose pointing right. "
        "Preserve this hairstyle verbatim: "
        + hairstyle
        + "Preserve identical facial bone structure, forehead, eyebrows, nose, "
          "ear shape, skin tone, age, dark navy crew-neck shirt and studio lighting. "
          "Do not restyle hair, shorten, lengthen, shift hairline, or remodel face. Neutral expression."
    )
    common = ["--backend", "cuda0", "--offload-to-cpu", "--diffusion-fa",
              "-W", "1024", "-H", "1024", "--steps", "4", "--cfg-scale", "1.0"]
    commands = [
        [binary, "--llm", paths["qwen"], "--diffusion-model", paths["turbo"],
         "--vae", paths["vae"], *common, "-p", prompt_source,
         "-s", "202610150011", "-o", str(source)],
        [binary, "--llm", paths["qwen"], "--llm_vision", paths["projector"],
         "--diffusion-model", paths["edit"], "--vae", paths["vae"], *common,
         "--img-cfg-scale", "1.12", "-p", prompt_pose, "-s", "202610150012",
         "-r", str(source), "-o", str(pose)]
    ]
    started = time.monotonic()
    run_steps = []
    for label, cmd in zip(("SOURCE", "P2"), commands):
        stamp = time.monotonic()
        try:
            completed = subprocess.run(cmd, text=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, timeout=1250, check=False)
            returncode, logs = completed.returncode, completed.stdout
        except subprocess.TimeoutExpired as exc:
            returncode = -1
            logs = ((exc.stdout or b"").decode("utf-8", "replace")
                    if isinstance(exc.stdout, bytes) else (exc.stdout or ""))
            logs += "\nINFERENCE_TIMEOUT"
        (directory / (label + ".log")).write_text(logs[-262144:], encoding="utf-8")
        run_steps.append({"slot": label, "elapsed_seconds": round(time.monotonic() - stamp, 2),
                          "returncode": returncode})
        if returncode:
            failure = {"status": "FAIL", "slot": label, "run_id": run_id,
                       "steps_report": run_steps, "sdcpp_source_commit": SDCPP_REF,
                       "scope": "generation_failed_do_not_claim_pass"}
            (directory / "report.json").write_text(json.dumps(failure, indent=2) + "\n")
            result_vol.commit()
            raise RuntimeError(f"{label} inference exit={returncode}; "
                               f"run_id={run_id}; last 1600 log characters: {logs[-1600:]}")
    images = {}
    for label, file in (("SOURCE", source), ("P2", pose)):
        with file.open("rb") as f:
            header = f.read(24)
        if len(header) < 24 or header[:8] != bytes.fromhex("89504e470d0a1a0a") or header[12:16] != b"IHDR":
            raise ValueError(f"Output is not a valid PNG header: {label}")
        width, height = struct.unpack(">II", header[16:24])
        if (width, height) != (1024, 1024):
            raise ValueError(f"Wrong PNG dimensions for {label}: {width}x{height}")
        hasher = hashlib.sha256()
        with file.open("rb") as fp:
            for chunk in iter(lambda: fp.read(1024 * 1024), b""):
                hasher.update(chunk)
        images[label] = {"path_in_output_volume": f"{run_id}/{label}.png",
                         "sha256": hasher.hexdigest(), "bytes": file.stat().st_size,
                         "width": width, "height": height}
    try:
        smi = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,uuid,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10, check=False)
        gpu_description = smi.stdout.strip() if smi.returncode == 0 else "unavailable"
    except (OSError, subprocess.TimeoutExpired):
        gpu_description = "unavailable"
    binary_sha256 = hashlib.sha256(Path(binary).read_bytes()).hexdigest()
    result = {
        "status": "PASS", "scope": "new_source_plus_right_pose_only_not_release_recreation",
        "run_id": run_id, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gpu_requested": "A10G", "gpu_device": gpu_description,
        "parallel_gpu_instances": 1,
        "sdcpp_source_commit": SDCPP_REF, "sdcpp_binary_sha256": binary_sha256,
        "model_fingerprints": {k: v[1] for k, v in ASSETS.items()},
        "prompts": {"SOURCE": prompt_source, "P2": prompt_pose},
        "seeds": {"SOURCE": 202610150011, "P2": 202610150012},
        "visual_quality_review": "PENDING_HUMAN_REVIEW",
        "example_subject_style": "explicit_consistent_short_swept_up_quiff",
        "resolution": [1024, 1024], "steps": 4,
        "commands": commands, "steps_report": run_steps,
        "runtime_seconds": round(time.monotonic() - started, 2),
        "images": images,
    }
    (directory / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    result_vol.commit()
    print("GPU_PAIR_PASS", run_id)
    print(json.dumps({"status": "PASS", "run_id": run_id,
                      "runtime_seconds": result["runtime_seconds"],
                      "output_images": list(images)}, ensure_ascii=False))
    return {"status": result["status"], "run_id": run_id, "images": images,
            "runtime_seconds": result["runtime_seconds"],
            "note": "Download the two PNGs and report.json from the output Volume."}
