# Troubleshooting and common questions

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](troubleshooting.vi.md)

| Symptom | What to do |
|---|---|
| The CPU example works but 935 PNGs are not checked | Expected: the repository bundles only ten sample metadata rows. Download the authorized dataset or use Kaggle FULL. |
| Cannot find the dataset in Kaggle | Open **Input → Add Input → Datasets**, search **compactfaces-synthetic-face-dataset**, confirm owner dangkhoa2016, select Version 1; check access permissions. |
| Kaggle reports DEMO_ONLY | No dataset was selected. Set `MODE = "full"` to require it and reveal missing inputs. |
| Images not found after attaching the dataset | Open the Input panel and check for `metadata.csv`, `core_600png/images/` and `additional_optional_335png/images/`. The notebook reads the extracted directories directly. |
| FULL says multiple dataset roots | Set `DATASET_DIR` to the exact /kaggle/input/... folder shown in the Input panel. |
| SHA256 mismatch / missing view | Stop and inspect the actual bytes, metadata and slot assignments. Do not overwrite the curated originals. |
| GPU model cannot load | Verify the exact variant, SHA256, Safetensors file role and compatible `sd-cli` build in [Model setup](MODEL_SETUP.md). |
| Gallery has empty image slots | Serve it over HTTP with `python3 -m http.server`; check the generated catalog and relative paths. |
| Contact button does not send an email | It opens a mail draft; configure a local mail client or manually send the message. |
| GitHub Action has no steps or result | Inspect hosted runner permissions/billing and the target commit; a missing job is not a successful test. |

For privacy or image-removal questions, contact **i.am@dangkhoa.dev** with a specific identity/slot. Do not post credentials, personal photos or sensitive files in public issues.

**Modal errors:** see [Modal deployment](MODAL_DEPLOYMENT.md) to distinguish model SHA256 mismatch, CUDA build failures and inference failures.

[Quickstart](QUICKSTART.md) · [Validation](validation.md)
