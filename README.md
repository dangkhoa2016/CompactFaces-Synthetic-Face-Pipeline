# CompactFaces — Synthetic Face Dataset & Engineering Toolkit

[![CI](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline/actions/workflows/ci.yml)
![Dataset version](https://img.shields.io/badge/dataset-v1.0.0-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-green)](LICENSE)

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

**CompactFaces** is a reproducible *engineering case study* built around synthetic face portraits. Each identity has one neutral SOURCE, two pose variations (P1/P2) and two expression variations (E1/E2). The repository provides CPU validators, a Kaggle notebook, a static gallery builder, bilingual documentation and an optional GPU example.

**Useful for:** learning dataset integrity and provenance workflows, exploring controlled pose/expression collections, and testing data-processing pipelines. This is **not** a biometric identity benchmark or evidence of visual identity consistency.

**The source repository works without downloading the CompactFaces image dataset.** The released data and model weights are separate resources; the GitHub repository is intentionally code-only.

## At a glance

| Dataset 1.0.0 | Coverage |
|---|---|
| **187 synthetic identities** | 120 Core + 67 Additional Optional |
| **935 original PNGs** | 1024 × 1024; one SOURCE plus four pose/expression variants per identity |
| **SOURCE · P1 · P2 · E1 · E2** | Front/neutral · left turn · right turn · smile · annoyed |
| **935 final-step provenance records** | Machine-readable prompt, seed and generation/editing settings |
| **187 SOURCE lineage records** | SOURCE consistency references; not full step-by-step regeneration instructions |
| **935 Builder JPEG previews** | Distribution preview checks; not substitutes for original PNGs |

The validator checks **five-view structure, file integrity, SHA256 and metadata consistency**. It does **not** establish biometric uniqueness, visual identity similarity or independent legal clearance.

## Five-view preview — CORE:0002

| SOURCE · Neutral | P1 · Left turn | P2 · Right turn | E1 · Smile | E2 · Annoyed |
| :---: | :---: | :---: | :---: | :---: |
| ![Synthetic face preview SOURCE](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_SOURCE.webp) | ![Synthetic face preview P1](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_P1.webp) | ![Synthetic face preview P2](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_P2.webp) | ![Synthetic face preview E1](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_E1.webp) | ![Synthetic face preview E2](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/assets/thumb/images/core/identity_0002_E2.webp) |

These public 400px WebP thumbnails depict **one synthetic identity**. They are visual examples only: they do not verify the original PNG SHA256, visual quality or identity consistency. [Open the interactive gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/).

**Five-view visual example:** [Explore SOURCE, P1, P2, E1 and E2 in the web gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) (lossy WebP previews, not an integrity check) · [Kaggle CPU Integrity Lab](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) · [Notebook source](notebooks/compactfaces_kaggle_cpu_validation.ipynb) · [Kaggle Dataset Version 1](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) · [Hugging Face ImageFolder](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset).

To check downloaded data independently, follow [ImageFolder validation](docs/validation.md) or the [cross-platform verification guide](docs/platform-integrity.md). Do not infer image integrity from a dataset description or checksum quoted on a webpage.

## Quickstart — no image dataset or GPU required

Install **Git and Python 3.10+**, clone the repository, and run the included 10-row example. These CPU commands need neither the image dataset nor a GPU:

```bash
git clone https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline.git
cd CompactFaces-Synthetic-Face-Pipeline
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
```

The notebook validator executes the self-contained demo in both languages. **`DEMO_ONLY` is expected**: it checks example metadata, not published PNG bytes. These initial commands use only the Python standard library. See [Quickstart](docs/QUICKSTART.md) for optional Pillow, JavaScript and regression checks.

## Validate all 935 published images on Kaggle

1. Open the [CPU Integrity Lab](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) and choose **Copy & Edit**.
2. Attach dataset **`dangkhoa2016/compactfaces-synthetic-face-dataset`**, **Version 1**, from **Input → Add Input → Datasets**.
3. Set **Accelerator = None**, `MODE = "full"`, `DATASET_DIR = ""`, and run all cells.
4. Inspect `FULL_PASS` and the JSON report: **935 PNG SHA256**, **935 PNG IHDR dimensions**, **935 decoded Builder JPEG previews**, **935 embedded provenance entries**, **187 SOURCE lineages**.

**Release content binding:** FULL additionally checks the SHA256 of the mounted `metadata.csv` against the official Version 1 fingerprint. This confirms the expected metadata bytes, **not** the Kaggle-hosted version identifier or source Git commit.

**Scope:** `FULL_PASS` verifies file integrity and metadata consistency, **not** biometric uniqueness, visual quality or the similarity of five faces. The CI FULL regression uses generated test fixtures; it does not establish that the hosted Kaggle Dataset Version 1 has been independently checked.

**Important:** The notebook defaults to `MODE = "auto"`, which runs `DEMO_ONLY` when no dataset is attached. Use `MODE = "full"` for release verification so missing inputs fail explicitly.

Kaggle serves the dataset as *extracted directories*. Whole-ZIP checksum and CRC checks are therefore reported `SKIPPED_KAGGLE_EXTRACTED`; they are not falsely marked PASS. If data access is missing, explicitly choosing FULL produces an error rather than a misleading demo result. The notebook is **read-only** for input files and writes only an optional summary report to `/kaggle/working/`.

For an authorized local Hugging Face ImageFolder copy:

```bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
```

This local command verifies the five-slot structure and PNG SHA256; use the Kaggle notebook for Builder and embedded provenance checks. See [Validation](docs/validation.md), [Cross-platform integrity](docs/platform-integrity.md) and [Reproducibility](docs/reproducibility.md).

## Tools in this repository

| Path | Responsibility |
|---|---|
| `scripts/verify_dataset.py` | CPU metadata, five-view and SHA256 verification |
| `notebooks/compactfaces_kaggle_cpu_validation.ipynb` | One notebook, paired EN/VI explanations and shared Python code; DEMO / FULL / PARTIAL |
| `scripts/test_notebook_full_fixture.py` | Offline synthetic regression fixtures and negative cases |
| `scripts/build_static_gallery.py` | 400px and 768px WebP previews and static catalog from authorized ImageFolder inputs |
| `website_src/` | Responsive bilingual gallery, Core/Additional filters, five-view browsing |
| `modal_app.py` and `scripts/reproduce_source_pose_example.sh` | Optional new SOURCE/P2 generation/editing examples; prepared models and GPU needed |
| `scripts/model_assets.py` | Five model checkpoint SHA256 fingerprints; no bundled weights |

**Optional GPU example:** [Model setup](docs/MODEL_SETUP.md) → [Modal deployment](docs/MODAL_DEPLOYMENT.md). The example generates a **new** SOURCE/P2 pair using compatible checkpoints. It does not recreate the distributed 935-image dataset. Inspect output quality independently.

To generate local previews from your **authorized** ImageFolder, follow [Gallery guide](docs/gallery.md). The WebP output is lossy, and original PNGs are neither committed nor altered.

## Documentation

[Documentation index](docs/README.md) · [Quickstart](docs/QUICKSTART.md) · [Dataset/platform layout](docs/platforms.md) · [Architecture](docs/architecture.md) · [Validation](docs/validation.md) · [Reproducibility](docs/reproducibility.md) · [Model provenance](docs/MODEL_PROVENANCE.md) · [Release policy](docs/RELEASE_POLICY.md) · [Cross-platform verification](docs/platform-integrity.md)

## Provenance, scope and licenses

CompactFaces provides synthetic portraits and machine-readable metadata for dataset inspection. Hashes verify file content but cannot guarantee pixel-identical regeneration or non-resemblance to real people.

**License boundaries:** the repository-owned software and documentation are [MIT](LICENSE). Separately distributed dataset images, derived gallery WebPs and eligible metadata are [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) only where the rights holder can license them. Model weights and user-supplied inputs have their own terms. The code license does not grant commercial image rights. See [license scope](LICENSE-NOTES.md).

For privacy, image review or removal requests: **[i.am@dangkhoa.dev](mailto:i.am@dangkhoa.dev)**.

**Maintainer:** Đăng Khoa.
