# Validate available dataset images and metadata

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](validation.vi.md)

The tools distinguish **source smoke tests** from **full image verification**. Never equate DEMO_ONLY or a successful schema check with verifying the original 935 PNGs.

## A. CPU verification without a dataset

~~~bash
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
~~~

This validates the bundled sample schema and executable notebook DEMO. No original PNG byte is checked.

## B. Validate downloaded ImageFolder

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
~~~

Requires `metadata.csv` and its referenced files. The local validator checks identity syntax, five-slot completeness, Core/Additional consistency, unique image paths and SHA256 entries, and each family's `source_sha256` binding. With `--verify-images`, it also checks PNG file bytes against recorded SHA256. It **does not decode PNGs, check dimensions or verify embedded provenance**; use the Kaggle FULL notebook for those further checks. Without the flag, PNG bytes are **not checked**.

Run negative regression tests with `python3 -m unittest -v scripts.test_dataset_validator scripts.test_gallery_cache` (Pillow required for the cache tests).

## C. Kaggle CPU notebook

1. [Open the notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation).
2. Follow [Input → Add Input → Datasets](platforms.md) and select CompactFaces Dataset Version 1 from dangkhoa2016.
3. Set `MODE = "full"`, accelerator `None`, and Run all.
4. Read the final `verified_png_sha256_count`, `input_layout`, per-check status and `verdict`.

The FULL notebook reads attached Kaggle Dataset Version 1 **PNG directories and metadata directly**, without manual ZIP preparation. It checks 935 PNG SHA256 values, 935 Builder JPEG previews, 935 generation-provenance records, 187 SOURCE lineage records and embedded PNG SDCpp metadata via Pillow. FULL_PASS requires the corresponding provenance files; missing inputs stop verification.

The Builder check enforces all 935 preview filenames against identity/slot metadata, **fully decodes** each JPEG and cross-checks the Builder catalog's **original PNG SHA256/path entries**. It does not hash each JPEG against an independent JPEG checksum manifest, and a valid but visually different JPEG can pass. SOURCE lineage identities must be unique and cover the expected 187 source identities. These checks do not establish visual equivalence between JPEG and PNG. **`FULL_PASS` means file integrity and metadata consistency only**: no automated assessment of visual quality, cross-view face similarity or biometric uniqueness is performed. The repository CI FULL test uses synthetic fixtures, not the hosted Kaggle release.

**When a check fails:** retain the original files, inspect missing paths/duplicate slots/checksum values and obtain a correct authorized copy. Do not regenerate or overwrite accepted images simply to turn a failure green.

[Dataset structure](DATASET_STRUCTURE.md) · [Troubleshooting](troubleshooting.md)

## PNG geometry and machine-readable evidence

The CPU notebook checks PNG signature and IHDR width/height of **all 935 originals**, requiring 1024 × 1024, independently of the optional SHA256 switch. These header checks do not constitute full image decoding. For every `FULL_PASS`, all 935 original file hashes, Builder previews, embedded provenance and SOURCE lineage must also pass. The five-view preview checks the dimensions again for the selected family.

The JSON report includes `verified_png_dimensions_count`, `metadata_csv_sha256`, Python and Pillow versions, execution UTC timestamp, CPU architecture, and active verification options. `source_git_commit` can be supplied through `COMPACTFACES_GIT_SHA`; otherwise it remains null. Reports record only the CPU device class, not a device identifier. The notebook does not independently verify dataset owner or version: check these in the Kaggle Input panel or API.
