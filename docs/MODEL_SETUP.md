# Model setup for the optional GPU example

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](MODEL_SETUP.vi.md)

Use this guide to prepare and verify five local model files for the optional **SOURCE → P2** GPU example. The Kaggle CPU dataset validator does **not** need these files, CUDA, Modal, or model downloads. The GitHub repository distributes no model weights.

**Before downloading:** consult the **single [model inventory and source links](MODEL_PROVENANCE.md#model-inventory)** for the five exact model variants and their upstream/Kaggle sources. This setup page intentionally does not repeat the source table or 64-character hashes.

## 1. Prepare the local layout

Create the directories, then place each authorized model file in its matching location:

```bash
mkdir -p "$HOME/compactfaces-models"/{turbo,edit,qwen,vae}
```

```text
~/compactfaces-models/
├── turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
├── edit/diffusion_pytorch_model.safetensors
├── qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
├── qwen/mmproj-BF16.gguf
└── vae/diffusion_pytorch_model.safetensors
```

**Important:** The Edit transformer and VAE are **different files** with the same basename, `diffusion_pytorch_model.safetensors`. Do not overwrite one with the other. Select the exact GGUF quantization and the `vae-only` variant described in [Model provenance](MODEL_PROVENANCE.md).

## 2. Download from the documented sources

Open the linked source for each component in [Model provenance](MODEL_PROVENANCE.md#model-inventory). Check the model page's license and permissions, then select the indicated GGUF/Safetensors file and quantization. Use the provider's documented UI or CLI; do not assume that similar model names or revisions are byte-equivalent.

The full recorded SHA256 values appear once, in the [expandable checksum reference](MODEL_PROVENANCE.md#recorded-sha256-checksums). They are also encoded in `scripts/model_assets.py`, which the validation command uses. Hashes characterize recorded files, **not** every upstream revision.

## 3. Verify all five local files (CPU only)

Run these commands from the GitHub repository root:

```bash
python3 scripts/model_assets.py --root "$HOME/compactfaces-models"
python3 scripts/model_assets.py --root "$HOME/compactfaces-models" --json
```

The read-only verifier streams each file, checks its SHA256 against the five recorded fingerprints, and reports `PASS`, `MISSING`, or `MISMATCH`. **Only five matching SHA256 values produce verdict `PASS` and exit code 0**. A missing or mismatched file produces exit code 2.

The `--presence-only` option checks paths only: its result is **not** an integrity PASS. Never change expected hashes merely to make a downloaded file pass.

## 4. Run the optional example

After local verification passes, follow the [Modal deployment guide](MODAL_DEPLOYMENT.md) to upload the models to private Volumes, verify remote SHA256 on CPU, and separately launch the paid GPU run.

Alternatively, with a compatible NVIDIA/CUDA `sd-cli` binary installed:

```bash
export SD_CLI=/path/to/compatible/sd-cli
export MODEL_DIR="$HOME/compactfaces-models"
export OUTPUT_DIR=./compactfaces_example
bash scripts/reproduce_source_pose_example.sh
```

The example creates a new SOURCE and P2, not byte-identical copies of the 935 published portraits. Runtime compatibility and visual quality must be checked separately from SHA256.

## Troubleshooting

| Symptom | What to check |
|---|---|
| `MISSING` | Relative path, case-sensitive filename, and completed download |
| `MISMATCH` | Quantization, file variant, source revision, and downloaded bytes |
| Edit file used as VAE | Keep the two Safetensors files in their respective directories |
| Access denied | Read the source model license and request authorized access |
| CUDA error after SHA256 PASS | Validate `sd-cli`, GPU, CUDA build, and model compatibility |

See [Model provenance](MODEL_PROVENANCE.md) for the original file fingerprints, source references, licensing boundaries, and reproducibility limitations; see [Reproducibility](reproducibility.md) for what the example does not prove.
