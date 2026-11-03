# Download and use CompactFaces data

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](platforms.vi.md)

The GitHub source repository, original images, and gallery are **separate resources**. Source-only CPU smoke tests require no accounts or dataset files.

## Download options

| Resource | URL | Contents |
|---|---|---|
| GitHub | [Pipeline code](https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline) | scripts, example metadata, docs, notebook source |
| Hugging Face | [CompactFaces ImageFolder](https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) | original PNGs and metadata |
| Kaggle | [CompactFaces dataset](https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset) | Version 1: 187 identities, 935 PNGs and metadata |
| Kaggle notebook | [CPU validation notebook](https://www.kaggle.com/code/dangkhoa2016/compactfaces-synthetic-face-cpu-validation) | ready-to-run validation interface |
| Website | [Browse gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/) | WebP previews; not original PNGs |

## Kaggle notebook: attach the dataset

1. Open the **CPU validation notebook** above and click **Copy & Edit**, or import the repository's notebook.
2. On the right, open **Input → Add Input** (or **Add Data**) → **Datasets**.
3. Search for **compactfaces-synthetic-face-dataset**, confirm owner **dangkhoa2016** and choose **Version 1**, then **Add**.
4. Select **Accelerator: None**. Once attached, Kaggle provides `metadata.csv` and the directories `core_600png/images/`, `additional_optional_335png/images/`, and `collection_builder_187/WEB_COLLECTION_BUILDER/previews/` under `/kaggle/input/compactfaces-synthetic-face-dataset/`. **You do not need to prepare or extract ZIP files**; the notebook reads these files directly.
5. Set `MODE = "full"` to require the dataset, and run all cells. Leave `DATASET_DIR = ""` for automatic detection, or set the path printed in the notebook if ambiguous.
6. Check `FULL_PASS` and the actual verified PNG count. `DEMO_ONLY` validates only bundled example metadata, not original images.

## Run on your own computer

For a compatible ImageFolder with `metadata.csv`, run:

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
~~~

The ImageFolder code examples in the shared dataset card use Hugging Face's `data/train/` layout and **cannot be run unchanged against Kaggle's extracted folder layout**. For Kaggle Dataset Version 1, use the FULL notebook above; it resolves Kaggle's actual directories, checks original bytes and reports inapplicable archive-level checks as skipped. Read [Validation](validation.md) and [License notes](../LICENSE-NOTES.md).
