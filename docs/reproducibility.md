# Reproducibility and independent verification of CompactFaces 1.0.0

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](reproducibility.vi.md)

This guide distinguishes **verification of published files** from **generating new images**. Anyone can run the CPU demo without downloading the dataset, but a full audit requires authorized access to the original PNGs. The optional Modal workflow produces a NEW example pair, not the exact 935 curated portraits.

## 1. What you can reproduce

| Level | Goal | Inputs | Expected evidence |
|---|---|---|---|
| A | Source-code/demo checks | Git, Python 3.10+, no dataset | 2 example families, 10 metadata rows, DEMO_ONLY |
| B | ImageFolder byte verification | 935 PNGs + metadata.csv | 187 five-view families, 935 file SHA256 matches |
| C | Kaggle FULL and provenance | Kaggle Dataset Version 1, CPU + Pillow | 935 PNG, 935 previews, 935 final-step records, 187 SOURCE lineages |
| D | New GPU smoke test | Five model artifacts + compatible sd-cli on CUDA | NEW SOURCE.png / P2.png + report.json, not release reconstruction |

The dataset contains 120 Core identity families and 67 Additional Optional families. Each contains SOURCE (neutral), P1 (left), P2 (right), E1 (smile) and E2 (annoyed), totaling 187 × 5 = 935 original 1024×1024 PNGs.

**Integrity** means the current file bytes match recorded SHA256; **provenance** means metadata from an output's final step agrees with stored records; **generation method reproduction** means a new image is produced using a comparable pipeline. These are distinct claims: passing Level B or C does not demonstrate Level D, and pixel-identical recreation of all release images is NOT supported.

## 2. Level A — CPU checks without downloading data

~~~bash
git clone https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline.git
cd CompactFaces-Synthetic-Face-Pipeline
python3 --version
git rev-parse HEAD
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
python3 scripts/audit_publication.py
python3 -m unittest -v scripts/test_modal_workflow.py
~~~

Successful example output includes PASS: 2 identity families / 10 images. The notebook checker performs a bilingual DEMO: verified_png_sha256_count = 0 is **expected**. No release PNG has been checked. The source scanner checks defined token patterns; it does not replace a security review.

## 3. Level B — verify the ImageFolder PNGs

Download the [Hugging Face dataset](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) if you have access. Point to the directory that actually contains metadata.csv and the relative image paths:

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train \
  --expected-images 935 --expected-families 187 --verify-images
~~~

Expected success: PASS: 187 identity families / 935 images. The script validates counts and slot inventory, then reads each PNG in chunks to compare SHA256 to the corresponding CSV field. It does **not** inspect embedded PNG prompts or full source ancestry. On missing files or mismatches, retain inputs and stop; never change a checksum merely to obtain PASS.

## 4. Level C — full CPU notebook on Kaggle

Open [the notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation). Click Copy & Edit, then Input → Add Input → Datasets. Find compactfaces-synthetic-face-dataset by dangkhoa2016, select **Dataset Version 1**, and Add. Use Accelerator = None.

Set the notebook configuration to:

~~~python
MODE = "full"
DATASET_DIR = ""
VERIFY_PNG_SHA256 = True
VERIFY_BUILDER = True
EXPORT_REPORT = True
~~~

CompactFaces Kaggle Dataset Version 1 provides `metadata.csv` and **Core, Additional and Builder folders** under `/kaggle/input/compactfaces-synthetic-face-dataset/`. The notebook reads these files directly. For ambiguous inputs, inspect the sidebar and set DATASET_DIR. With EXPORT_REPORT enabled, it writes compactfaces_cpu_validation_report.json to /kaggle/working.

Inspect **all** fields: mode FULL; verdict FULL_PASS; 187 identities; 935 records; verified_png_sha256_count 935; builder_jpeg_previews 935; generation_provenance_verified 935; source_lineage_verified 187; metadata/png_sha256/builder/provenance checks PASS.

**Reporting scope:** The notebook retains the `builder_crc` and `zip_files` fields for report compatibility. For Kaggle Dataset Version 1, both report `SKIPPED_KAGGLE_EXTRACTED` because archive-file checks do not apply to its folder layout. This is **expected**, not an error or a request for additional files, and does not prevent `FULL_PASS` when image, Builder-preview and provenance checks pass.

Provenance verification compares generation_metadata.jsonl (935 records), source_lineage.jsonl (187 records), generation_metadata_audit.json, and embedded PNG SDCpp parameters using Pillow. It checks image hash, identity/slot, prompt, seed and diffusion step counts recorded for the **last** generation/edit step. It does not recover discarded attempts or every ancestor of an edited SOURCE.

## 5. Level D — optional new GPU pair on Modal

First follow [Model setup](MODEL_SETUP.md), then [Modal deployment](MODAL_DEPLOYMENT.md). Download exactly five model files and obtain matching SHA256 for each. The Modal example uses access-controlled model/output Volumes, CPU verification and an explicitly invoked GPU function.

~~~bash
python3 scripts/model_assets.py --root "$HOME/compactfaces-models"
modal run modal_app.py::verify_models
# Review costs and quota before the paid GPU step:
modal run modal_app.py::generate_pair
~~~

The GPU runner pins a stable-diffusion.cpp source revision and records two prompts/seeds, model hashes, image hashes and timings. The GPU example requires checking the generated output and its actual hashes; see [Modal deployment](MODAL_DEPLOYMENT.md). It does not establish quality across all identities.

If two output PNGs exist and their hashes match, this proves **new example artifacts were produced**, not the curatorial consistency of all 187 identities. Review SOURCE/P2 visual similarity and pose direction separately.

## 6. Why pixel-identical regeneration is not supported

The dataset includes final-step metadata and SOURCE links for checking files, not a guarantee of pixel-identical image generation. Identical prompt and seed values may produce different pixels across model builds and runtimes.

The gallery's 400/768px WebP images are **lossy previews** and cannot substitute for original PNG SHA256 verification. Synthetic portraits may coincidentally resemble real people; a passing checksum is not a biometric uniqueness, consent or licensing review.

## 7. Minimum evidence for your own report

Keep repository commit SHA, dataset URL/version, input layout (Kaggle folders or Hugging Face ImageFolder), command, Python and Modal SDK versions, CPU/GPU device, model SHA256 and revision, prompts/seeds, output hashes, elapsed times, visual review and every skipped or failed check. Do not include tokens, private storage addresses, or personal data in published logs.

Use precise language: “DEMO metadata test PASS” for Level A; “935 original PNG SHA256 verified against metadata” only after a true Level B/C execution; “`builder_crc` and `zip_files` skipped because they do not apply to folder input” for the current Kaggle release; “new SOURCE/P2 pair created on GPU” only after live Level D evidence. Do not combine these into an unsupported claim of exact dataset regeneration.

[Troubleshooting](troubleshooting.md) · [Dataset platforms](platforms.md) · [Model provenance](MODEL_PROVENANCE.md) · [Licensing](../LICENSE-NOTES.md)

## Notebook execution metadata

For an independently reviewable FULL report, retain the notebook source revision, Kaggle Dataset Version 1, the SHA256 of `metadata.csv`, UTC execution time, Python/Pillow versions, input layout and enabled checks. `COMPACTFACES_GIT_SHA` is an optional user-provided source revision. The report records the CPU device class without a unique device identifier. Verify the actual Kaggle dataset version separately; never infer it from the mount path or expose host secrets. All 935 PNG IHDR dimensions are checked against 1024 × 1024; this header test does not replace SHA256 verification.
