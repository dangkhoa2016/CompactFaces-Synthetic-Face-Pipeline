# CompactFaces 1.0.0 dataset structure

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](DATASET_STRUCTURE.vi.md)

The reference dataset has **187 synthetic identity families and 935 accepted 1024×1024 PNGs**. Each identity always has **five views**:

| Slot | Intended view |
|---|---|
| `SOURCE` | Neutral, front-facing reference portrait |
| `P1` | Left-facing pose |
| `P2` | Right-facing pose |
| `E1` | Smiling expression |
| `E2` | Annoyed expression |

**Core:** 120 families / 600 PNGs. **Additional Optional:** 67 families / 335 PNGs. Additional Optional is included in the 187-family total.

## Metadata

The Hugging Face ImageFolder uses `data/train/metadata.csv`; Kaggle Dataset Version 1 has `metadata.csv` at its root beside `core_600png/images/` and `additional_optional_335png/images/`. Each metadata row records `file_name`, `identity_key`, `collection`, `slot`, `sha256` and `source_sha256`. Legacy `archive_name` / `archive_file_name` fields describe the original distribution mapping; **they do not require ZIP files on Kaggle**.

- Each `identity_key` must occur exactly five times with different slots.
- All five rows of a family belong to the same collection and reference the same SOURCE SHA256.
- `sha256` identifies the **actual PNG bytes**, not a preview or inferred visual identity.
- Generation metadata and SOURCE lineage records are distributed with the dataset, not required by GitHub's CPU smoke test.

## Usage guidance

When preparing machine-learning train/validation/test splits, group by `identity_key` to prevent the same synthetic family from appearing in multiple splits. Check [verification instructions](validation.md) before trusting any local copy. Being synthetic does not guarantee all portraits are unique in biometric space, non-identifiable or free of incidental resemblance to real people.

[Download locations](platforms.md) · [Licenses](../LICENSE-NOTES.md)
