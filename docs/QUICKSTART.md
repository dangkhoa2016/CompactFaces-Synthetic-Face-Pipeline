# Quickstart — CPU first

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](QUICKSTART.vi.md)

**Requirements:** Git and Python 3.10+. The initial CPU checks need no dataset, GPU, model downloads or third-party Python packages.

## 1. Clone and verify the included example

~~~bash
git clone https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline.git
cd CompactFaces-Synthetic-Face-Pipeline
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
python3 scripts/validate_notebooks.py
~~~

Expected: successful source checks and a **DEMO_ONLY** notebook report. This **does not** validate 935 original PNGs. Optional syntax checks: `python3 -m py_compile scripts/*.py`; `node --check website_src/app.js`; `bash -n scripts/reproduce_source_pose_example.sh`.

## 2. Verify the full dataset

For the complete collection, [attach CompactFaces Dataset Version 1 on Kaggle](platforms.md), set `MODE = "full"` in the CPU notebook and run all cells. Kaggle provides PNG images and metadata directly; no manual ZIP download or extraction is required.

Alternatively, if you downloaded the Hugging Face ImageFolder with permission, verify its local files:

~~~bash
python3 scripts/verify_dataset.py /path/to/data/train --expected-images 935 --expected-families 187 --verify-images
~~~

Full PNG byte verification requires the actual images. Follow [Validation](validation.md) for the supported ImageFolder or Kaggle workflow. Do not claim FULL_PASS from DEMO_ONLY.

## 3. Optional gallery and GPU example

~~~bash
python3 -m pip install Pillow
python3 scripts/build_static_gallery.py --train /path/to/data/train --output ./compactfaces_gallery
python3 -m http.server 8095 --bind 127.0.0.1 --directory ./compactfaces_gallery
~~~

The gallery creates lossy WebP previews and does not modify input PNGs. If you want to try a new SOURCE/P2 generation example, follow [model setup](MODEL_SETUP.md). Do not expect pixel-identical regeneration of the collection.

**Want to generate an example pair on Modal?** After the CPU checks, follow [Model setup](MODEL_SETUP.md) and [Modal deployment](MODAL_DEPLOYMENT.md). A GPU is not needed for the dataset verification above.

[Dataset platforms](platforms.md) · [Troubleshooting](troubleshooting.md)
