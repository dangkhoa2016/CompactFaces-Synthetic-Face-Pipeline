#!/usr/bin/env python3
"""Shared, CPU-only checkpoint manifest for the optional CompactFaces GPU demo.

Recorded local fingerprints from the 1.0.0 case study. This utility NEVER downloads
weights, never changes source files and does not assert upstream revision identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ASSETS = {
    "turbo": ("turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf", "4c3dafc143ee64121692b6b63563a4f5288bf6183c4870e1d65f1566519ba7f0"),
    "edit": ("edit/diffusion_pytorch_model.safetensors", "29c3726ecd64afe149eef28af3e27b6b40de52646bfd16757a37da4b6fbcf288"),
    "qwen": ("qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf", "66358cb18bb6b3b1b6675aa412c7a88ef01d228f481184d13668e5201c730a0a"),
    "projector": ("qwen/mmproj-BF16.gguf", "364ef9a7502b7e9a834b9c013b953670f6ba2550b4a26fc043c317fa484eb53e"),
    "vae": ("vae/diffusion_pytorch_model.safetensors", "34e076dc1e8a15321e1e07be5111d59cf16dd10b804b7c7e20b4de29013427e0"),
}


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fp:
        for block in iter(lambda: fp.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect(root: Path, verify_hashes: bool = True) -> dict:
    root = Path(root).expanduser().resolve()
    results = {}
    for role, (name, expected) in ASSETS.items():
        path = root / name
        entry = {"relative_path": name, "expected_sha256": expected, "present": path.is_file()}
        if path.is_file():
            entry["bytes"] = path.stat().st_size
            if verify_hashes:
                actual = digest_file(path)
                entry["actual_sha256"] = actual
                entry["status"] = "PASS" if actual == expected else "MISMATCH"
            else:
                entry["status"] = "NOT_CHECKED"
        else:
            entry["status"] = "MISSING"
        results[role] = entry
    outcome = ("PASS" if all(v["status"] == "PASS" for v in results.values()) else
               "INCOMPLETE_OR_MISMATCH" if verify_hashes else
               "PRESENCE_ONLY" if all(v["present"] for v in results.values()) else "MISSING")
    return {"root": str(root), "verdict": outcome, "model_count": len(ASSETS),
            "sha256_verified": verify_hashes, "models": results,
            "scope": "recorded_local_file_fingerprints_not_upstream_revision_attestation"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True,
                        help="directory containing turbo/, edit/, qwen/ and vae/")
    parser.add_argument("--presence-only", action="store_true",
                        help="check paths only; NOT a checksum or acceptance test")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = inspect(args.root, verify_hashes=not args.presence_only)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for name, entry in result["models"].items():
            print(f"{name:10} {entry['status']:12} {entry['relative_path']}")
        print("VERDICT:", result["verdict"])
    return 0 if result["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
