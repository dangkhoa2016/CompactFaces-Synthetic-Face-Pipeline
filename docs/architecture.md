# Architecture — an independent dataset toolkit

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](architecture.vi.md)

CompactFaces separates **data creation**, **read-only validation** and **public presentation**. A user can run the validators without installing the GPU inference engine or downloading the original collection.

## System diagram

~~~text
Optional GPU generator (Mage-Flow-Turbo / Edit, Qwen, VAE)
       │ new SOURCE / P1 / P2 / E1 / E2 candidates
       ▼
Human selection and quality control (not automated by this repository)
       │ selected 1024×1024 PNGs + metadata + SHA256
       ├──────────► ImageFolder distribution (Hugging Face)
       ├──────────► PNG folders + CPU notebook (Kaggle)
       └──────────► read-only gallery builder ► 400/768px WebP website

Metadata / PNG folders ──► CPU verifiers ──► counts, slot consistency, hashes, errors
~~~

## Main repository components

| Component | Responsibility | Input → output |
|---|---|---|
| `scripts/verify_dataset.py` | Check identity/slot schema, accepted rows and optional PNG SHA256 | local ImageFolder → terminal report |
| `scripts/build_static_gallery.py` | Verify the source before deriving previews | compatible ImageFolder → static WebP site |
| `notebooks/compactfaces_kaggle_cpu_validation.ipynb` | Guide users through Kaggle CPU checks | attached dataset → visible report |
| `website_src/` | Site template, search, five-view UI, contact email draft | generated catalog → browser |
| `scripts/reproduce_source_pose_example.sh` | Demonstrate optional GPU inference | compatible models → two new PNG examples |

## Operational boundaries

- Validators **read** inputs; a failed checksum is a hard error, not an automatic repair.
- Original images and model weights are **not committed to GitHub**. Repository tests use bundled synthetic example metadata.
- Gallery WebPs are lossy derivatives, not replacements for the original PNGs.
- The Contact form prepares an email in the user's mail client; it does not upload files or guarantee delivery.
- SHA256 confirms byte equality, **not** biometric uniqueness, consent, or pixel-identical image regeneration.

[Get started](QUICKSTART.md) · [Dataset structure](DATASET_STRUCTURE.md) · [Model files](MODEL_PROVENANCE.md)
