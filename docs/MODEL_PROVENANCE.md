# Model provenance and reference fingerprints

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](MODEL_PROVENANCE.vi.md)

This document is the **single human-readable reference** for the five model files used by the optional CompactFaces SOURCE → P2 GPU example: their roles, exact variants, source pages, and recorded checksums. For download directories, validation commands, and GPU execution steps, use [Model setup](MODEL_SETUP.md). Dataset verification on CPU does not require any model weights.

## Model inventory

| Role | File and format | Model source / reference |
|---|---|---|
| Text-to-image SOURCE | `Mage-Flow-Turbo-DiT-Q8_0.gguf` · GGUF Q8_0 | [Mage-Flow-Turbo](https://huggingface.co/mage-flow-community/Mage-Flow-Turbo) · [Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/mage-flow-community-mage-flow-turbo) |
| Image pose/expression editing | `diffusion_pytorch_model.safetensors` · Edit transformer | [Mage-Flow-Edit-Turbo](https://huggingface.co/mage-flow-community/Mage-Flow-Edit-Turbo) · [Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/mage-flow-community-mage-flow-edit-turbo) |
| Text/vision conditioning | `Qwen3VL-4B-Instruct-Q4_K_M.gguf` · GGUF Q4_K_M | [Qwen3-VL GGUF Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/qwen-qwen3-vl-4b-instruct-gguf) · [upstream model family](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) |
| Vision projector | `mmproj-BF16.gguf` · GGUF BF16 | [Revision-pinned projector file](https://huggingface.co/unsloth/Qwen3-VL-4B-Instruct-GGUF/blob/cc8371d67a57fc6ae05fc5a9c2df763914928539/mmproj-BF16.gguf) |
| Latent decoding | `diffusion_pytorch_model.safetensors` · VAE Safetensors | [Mage-Flow-Turbo Kaggle mirror](https://www.kaggle.com/models/dangkhoa2016/mage-flow-community-mage-flow-turbo) · **PyTorch / vae-only / Version 1** |

**Edit and VAE are different artifacts** despite sharing the basename `diffusion_pytorch_model.safetensors`. Use the distinct `edit/` and `vae/` paths in [Model setup](MODEL_SETUP.md). Do not infer byte identity from a matching display name or from a different quantization.

## Recorded SHA256 checksums

The full fingerprints are intentionally **outside the wide model table**. Expand the reference below to copy them. The authoritative values used by the repository's read-only verifier are defined in [`scripts/model_assets.py`](../scripts/model_assets.py); the reference below must match that script.

<details>
<summary>Show five full SHA256 values and relative paths</summary>

```text
4c3dafc143ee64121692b6b63563a4f5288bf6183c4870e1d65f1566519ba7f0  turbo/Mage-Flow-Turbo-DiT-Q8_0.gguf
29c3726ecd64afe149eef28af3e27b6b40de52646bfd16757a37da4b6fbcf288  edit/diffusion_pytorch_model.safetensors
66358cb18bb6b3b1b6675aa412c7a88ef01d228f481184d13668e5201c730a0a  qwen/Qwen3VL-4B-Instruct-Q4_K_M.gguf
364ef9a7502b7e9a834b9c013b953670f6ba2550b4a26fc043c317fa484eb53e  qwen/mmproj-BF16.gguf
34e076dc1e8a15321e1e07be5111d59cf16dd10b804b7c7e20b4de29013427e0  vae/diffusion_pytorch_model.safetensors
```

</details>

These are expected SHA256 fingerprints for the specified file variants, not universal hashes for every upstream model revision. Do not replace a fingerprint to accept a different artifact.

## What the provenance supports

The released dataset includes `generation_metadata.jsonl` (935 final-step image records), `source_lineage.jsonl` (187 SOURCE lineage records), and `generation_metadata_audit.json`. The PNGs also retain structured generation parameters where recorded. These describe the released files and their final processing records, not every intermediate inference artifact.

The project used Mage-Flow-Turbo for synthetic SOURCE generation and Mage-Flow-Edit-Turbo for pose/expression variants. The optional GPU runner is a demonstration that can create a **new** SOURCE and P2 pair; it is **not** a byte-for-byte reproduction of the 935 published images. Verify actual GPU output and visual consistency independently; checksum matching does not establish image quality. See [Modal deployment](MODAL_DEPLOYMENT.md) and [Reproducibility](reproducibility.md).

## Rights and further information

The project-owned code is [MIT-licensed](../LICENSE). Dataset image licensing is explained in [License notes](../LICENSE-NOTES.md), and third-party model weights retain their own licenses. Check the actual model source pages before use. Hash matching establishes file integrity against a recorded fingerprint, **not** a right to use or redistribute a model.

[Prepare and verify models](MODEL_SETUP.md) · [CUDA/Modal workflow](MODAL_DEPLOYMENT.md) · [Reproducibility](reproducibility.md)
