# Using and validating CompactFaces

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](release-checklist.vi.md)

These commands help users check their downloaded source toolkit or dataset.

## Check the source toolkit

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 -m unittest -v scripts.test_dataset_validator scripts.test_gallery_cache
```

The examples exercise synthetic fixtures. **They do not verify the 935 distributed original PNGs.** The WebP cache tests require Pillow.

## Check downloaded data

Use the [Dataset validation guide](validation.md) for a local ImageFolder, or attach the Kaggle distribution to the [CPU notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) and set `MODE = "full"`. Inspect actual counts, hashes, per-check statuses and skipped checks. Use [cross-platform comparison](platform-integrity.md) when comparing downloads from Hugging Face and Kaggle.

For license terms, consult [MIT](../LICENSE), [image license notes](../LICENSE-NOTES.md), and upstream model licenses. Do not upload credentials, private personal images or identifying data when reporting problems.

[Quickstart](QUICKSTART.md) · [Troubleshooting](troubleshooting.md)
