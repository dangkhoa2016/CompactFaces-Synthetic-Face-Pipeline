# Cross-platform file verification — CompactFaces 1.0.0

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](platform-integrity.vi.md)

CompactFaces uses the dataset identifier `dangkhoa2016/compactfaces-synthetic-face-dataset` on [Hugging Face](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) and [Kaggle](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset). The dataset specification describes **187 five-view synthetic identities** (120 Core and 67 Additional Optional), or **935 original PNGs** at 1024 × 1024. Builder JPEGs and gallery WebPs are derivative previews, not additional originals.

## Compare the files you actually downloaded

Hugging Face ImageFolder uses `data/train/metadata.csv` and relative image paths under `data/train/images/`. The Kaggle distribution uses a root `metadata.csv` and the directories `core_600png/images/` and `additional_optional_335png/images/`.

Download each platform's current CSV through its official dataset page, then run:

```bash
sha256sum /path/to/hf/metadata.csv /path/to/kaggle/metadata.csv
python3 scripts/compare_platform_metadata.py /path/to/hf/metadata.csv /path/to/kaggle/metadata.csv
```

The first command calculates each complete CSV's SHA256, so equal digests support byte-for-byte CSV equality. The second validates the 187-family/935-slot inventory, identity/slot keys, collection assignments and SOURCE bindings, and compares the **recorded PNG SHA256 fields**. It does **not** compare every arbitrary metadata column (such as review flags, prompts or file paths) for value equality; use the whole-CSV digest when exact CSV equality is required. **Neither check reads PNG bytes from both hosts.**

## Verify original PNGs

For a local Hugging Face ImageFolder copy, run:

```bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
```

For Kaggle's extracted layout, attach the dataset to the [CPU validation notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation), set `MODE = "full"`, and inspect every check in the resulting report. See [Validation](validation.md).

The checks compare files and metadata. They cannot establish biometric uniqueness, lack of resemblance to real people, or pixel-identical image generation.

[Download options](platforms.md) · [Dataset structure](DATASET_STRUCTURE.md) · [Reproducibility limits](reproducibility.md)
