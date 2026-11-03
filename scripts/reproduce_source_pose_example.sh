#!/usr/bin/env bash
# CompactFaces release 1.0.0: representative SOURCE + P2 smoke test.
# This does not regenerate the exact published 935 images.
set -euo pipefail
MODEL_DIR="${MODEL_DIR:-$HOME/compactfaces-models}"
SD="${SD_CLI:-/path/to/compatible/sd-cli}"
LLM="${QWEN_GGUF:-$MODEL_DIR/qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf}"
TURBO="${TURBO_GGUF:-$MODEL_DIR/turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf}"
VAE="${MAGE_VAE:-$MODEL_DIR/vae/diffusion_pytorch_model.safetensors}"
EDIT="${EDIT_SAFETENSORS:-$MODEL_DIR/edit/diffusion_pytorch_model.safetensors}"
MM="${VISION_PROJECTOR:-$MODEL_DIR/qwen/mmproj-BF16.gguf}"
OUT="${OUTPUT_DIR:-./compactfaces_example}"
mkdir -p "$OUT"
for f in "$SD" "$LLM" "$TURBO" "$VAE" "$EDIT" "$MM"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing model or binary: $f" >&2
    echo "Follow docs/MODEL_SETUP.md to download and verify the matching checkpoint." >&2
    exit 2
  fi
done
check_sha() {
  local expected="$1" path="$2" actual
  actual="$(sha256sum "$path" | awk '{print $1}')"
  if [[ "$actual" != "$expected" ]]; then
    echo "SHA256 MISMATCH: $path (actual $actual)" >&2
    exit 3
  fi
  echo "SHA256 PASS: $path"
}
check_sha 4c3dafc143ee64121692b6b63563a4f5288bf6183c4870e1d65f1566519ba7f0 "$TURBO"
check_sha 66358cb18bb6b3b1b6675aa412c7a88ef01d228f481184d13668e5201c730a0a "$LLM"
check_sha 34e076dc1e8a15321e1e07be5111d59cf16dd10b804b7c7e20b4de29013427e0 "$VAE"
# Compare local files with the recorded artifact fingerprints; this
# does not prove equivalence to an unpinned upstream revision.
check_sha 29c3726ecd64afe149eef28af3e27b6b40de52646bfd16757a37da4b6fbcf288 "$EDIT"
check_sha 364ef9a7502b7e9a834b9c013b953670f6ba2550b4a26fc043c317fa484eb53e "$MM"
"$SD" --llm "$LLM" --diffusion-model "$TURBO" --vae "$VAE" \
  --backend cuda0 --offload-to-cpu --diffusion-fa \
  -p "Photorealistic adult identification portrait, neutral expression, centered head, plain light-gray background." \
  -W 1024 -H 1024 --steps 4 --cfg-scale 1.0 -s 202610150001 \
  -o "$OUT/SOURCE.png"
"$SD" --llm "$LLM" --llm_vision "$MM" --diffusion-model "$EDIT" --vae "$VAE" \
  --backend cuda0 --offload-to-cpu --diffusion-fa \
  -p "Keep the same identity. Rotate the head clearly to the right, true three-quarter pose, neutral mouth and plain studio background." \
  -W 1024 -H 1024 --steps 4 --cfg-scale 1.0 --img-cfg-scale 1.12 \
  -s 202610150002 -r "$OUT/SOURCE.png" -o "$OUT/P2.png"
echo "Example output files at: $OUT"
