# How the five-view dataset pipeline works

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](pipeline.vi.md)

The source collection was produced with text-to-image generation followed by image editing and human selection. **The public repository supplies validators and a representative two-image GPU script, not a one-click 935-image generator.**

| Step | Inputs | Output | What to check |
|---|---|---|---|
| SOURCE | Text prompt, seed, Mage-Flow-Turbo | Neutral portrait candidate | single adult face, usable framing |
| P1/P2 | Selected SOURCE, Mage-Flow-Edit-Turbo | left/right-facing candidates | pose direction and identity consistency |
| E1/E2 | Selected SOURCE, editing model | smiling/annoyed candidates | expression and identity consistency |
| Selection | candidate images | one approved image per slot | visual issues, duplicates, cross-view consistency |
| Distribution | selected PNG + metadata | Hugging Face ImageFolder; Kaggle PNG folders | 187 families, 935 PNG, 5 slots, hashes |
| Web gallery | validated ImageFolder | 400/768px WebP | user experience, no original PNG copied |

## Try the supplied tools

- **No GPU:** `python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2`
- **With authorized images:** follow [Validation](validation.md) or [Kaggle Input setup](platforms.md).
- **Optional GPU:** configure five model files and a compatible `sd-cli` using [Model provenance](MODEL_PROVENANCE.md), then run `bash scripts/reproduce_source_pose_example.sh`.

Do not treat a checksum match as proof of biological identity, face non-resemblance, or upstream model equivalence. [Read the reproducibility limits](reproducibility.md).
