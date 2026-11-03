# Modal GPU deployment for the optional CompactFaces example

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](MODAL_DEPLOYMENT.vi.md)

This guide runs an optional **new SOURCE portrait and P2 edit** on Modal A10G, not a reconstruction of the 935 published images. Modal builds, storage and GPU usage **may incur costs**. Users must verify runtime compatibility and inspect their own output quality.

## 1. Components

~~~text
Local machine: five checkpoints + Modal CLI
   │ upload (private)
   ▼
Modal Volume: compactfaces-example-models-v1
   │ mount read-only
   ├──► CPU remote SHA256 verification
   │          └── PASS required
   ▼
Modal A10G: pinned stable-diffusion.cpp CUDA build
   │ SOURCE + P2 output
   ▼
Modal Volume: compactfaces-example-results-v1
   └── per-run SOURCE.png, P2.png, report.json
~~~

Requirements: Modal workspace with appropriate permissions and GPU quota; Python 3.11+ on the client; Internet to fetch/build tools; local space for the five model files; rights to use the model weights.

## 2. Install and authenticate Modal

~~~bash
python3 -m pip install "modal==1.6.3"
modal --version
modal setup
modal profile current
~~~

The setup process may open a browser to authorize this machine. **Never paste tokens into files committed to Git.** Confirm the active workspace belongs to you. Modal references: [CLI](https://modal.com/docs/cli/latest) and [Volume](https://modal.com/docs/cli/latest/volume).

## 3. Download and verify checkpoints on your machine

Use [Model setup](MODEL_SETUP.md) to obtain the precise variants. Keep the two different Safetensors files in separate directories:

~~~text
~/compactfaces-models/
  turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
  edit/diffusion_pytorch_model.safetensors
  qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
  qwen/mmproj-BF16.gguf
  vae/diffusion_pytorch_model.safetensors
~~~

~~~bash
cd CompactFaces-Synthetic-Face-Pipeline
python3 scripts/model_assets.py --root "$HOME/compactfaces-models" --json
~~~

Continue only when the model verification verdict and all five file hashes are `PASS`. A missing file, checksum mismatch or presence-only check is insufficient.

## 4. Create two NEW Volumes

~~~bash
modal volume create compactfaces-example-models-v1
modal volume create compactfaces-example-results-v1
~~~

The commands create two Volumes for this example. Keep them separate from production resources. If you choose different names, configure `COMPACTFACES_MODEL_VOLUME` and `COMPACTFACES_OUTPUT_VOLUME` before running the app.

## 5. Upload model artifacts to the private model Volume

~~~bash
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf" \
  turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/edit/diffusion_pytorch_model.safetensors" \
  edit/diffusion_pytorch_model.safetensors
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf" \
  qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/qwen/mmproj-BF16.gguf" \
  qwen/mmproj-BF16.gguf
modal volume put compactfaces-example-models-v1 \
  "$HOME/compactfaces-models/vae/diffusion_pytorch_model.safetensors" \
  vae/diffusion_pytorch_model.safetensors
modal volume ls compactfaces-example-models-v1 /
~~~

Transfers may be large; expect storage charges. Never use the --force option unless you explicitly intend to replace an artifact. Avoid publishing checkpoint files outside their license terms.

## 6. Verify the REMOTE bytes on CPU before GPU

~~~bash
modal run modal_app.py::verify_models
~~~

This invokes a CPU Modal function using a **read-only** model Volume. It streams SHA256 across all five files. Expected: MODEL_PREFLIGHT_PASS and JSON verdict PASS. It does not prove that the inference binary is compatible, and can incur CPU/storage costs.

## 7. Pinned CUDA build details

The GPU Modal image uses CUDA 12.8.1 devel on Ubuntu 22.04, checks out upstream stable-diffusion.cpp revision **77b72a2efed78f55de26892c7e909cee001e8b83**, updates its submodules, then builds with SD_CUDA=ON and CUDA architecture 86 (A10G). The binary is /opt/sd-source/build/bin/sd-cli.

This configuration specifies the pinned inference-engine revision and A10G CUDA target. Verify compatibility on your actual hardware. Do not silently substitute a newer upstream revision. See [upstream build](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/build.md) and [Mage-Flow guide](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/mage_flow.md).

## 8. Explicitly invoke the A10G GPU test (paid)

Review Modal billing/quota, then run:

~~~bash
modal run modal_app.py::generate_pair
~~~

The function rechecks model checksums, builds/starts the pinned CLI environment, writes SOURCE.png then P2.png in a unique run folder, validates 1024×1024 PNG headers, and commits a report and files to the output Volume. If any step fails, it raises an error rather than declaring PASS.

Get the actual run ID from the returned result, then download:

~~~bash
modal volume ls compactfaces-example-results-v1 /
modal volume get compactfaces-example-results-v1 YOUR_RUN_ID/SOURCE.png ./SOURCE.png
modal volume get compactfaces-example-results-v1 YOUR_RUN_ID/P2.png ./P2.png
modal volume get compactfaces-example-results-v1 YOUR_RUN_ID/report.json ./report.json
~~~

Replace YOUR_RUN_ID with your actual result. Inspect both images visually before approving identity and pose quality. PNG checksum PASS is not the same as visual acceptance.

## 9. Verify your own GPU output

Check the result of `modal_app.py::generate_pair`: the run folder should include `SOURCE.png`, `P2.png`, and `report.json`. Confirm output dimensions and SHA256, then inspect visual pose and identity consistency. Correct file hashes do not establish image quality.

This optional two-image example does not regenerate the distributed dataset.

## 10. Troubleshooting and reporting

| Symptom | What to do |
|---|---|
| No authorized Modal profile | Run modal setup and confirm the workspace |
| Model Volume missing | Check the selected environment/Volume name |
| MODEL_PREFLIGHT_FAILED | Compare SHA256 and filenames; never bypass validation |
| Image build failed | Save build logs and report the failure; do not claim inference succeeded |
| sd-cli unsupported option | Review upstream CLI flags and pinned build compatibility |
| OOM/timeout on A10G | Save error/runtime information; do not claim successful inference |
| Images exist but pose is wrong | Retain evidence, mark visual review FAIL |

Record Git commit, model fingerprints, Modal SDK, GPU, pinned sd.cpp revision, prompts, seeds, duration, output SHA256, image review and every skipped check. Do not publish credentials, private Volume content or user data.

**No automated deletion, external endpoints or long-running deployments are created by this example.** GPU and storage billing are your responsibility. This repository remains a verification toolkit and a **two-image** optional GPU demonstration.

[Model setup](MODEL_SETUP.md) · [Model provenance](MODEL_PROVENANCE.md) · [Reproducibility](reproducibility.md)
