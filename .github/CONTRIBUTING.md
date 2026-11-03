# Contributing to CompactFaces

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](CONTRIBUTING.vi.md)

Contributions are welcome for repository-owned code, validation tooling, translation and documentation. **Never contribute original dataset PNGs, real-person photos, model checkpoints or credentials.**

## Development

Use Python 3.10+ for CPU validation; Node.js for JavaScript syntax checks. GPU hardware is optional and only relevant to the representative SOURCE/P2 smoke test.

```bash
python3 scripts/verify_dataset.py examples --expected-images 10 --expected-families 2
python3 scripts/validate_repository.py
node --check website_src/app.js && node --check website_src/pages.js
bash -n scripts/reproduce_source_pose_example.sh
```

## Documentation and review

- All Markdown documents must have English and Vietnamese counterparts: `file.md` and `file.vi.md`.
- Update both sides together and include a working language switch at the top.
- Keep code changes focused, ideally no more than ~600 changed lines per commit; bilingual document pairs may exceed this.
- Explain what changed, why, how it was tested, and whether any provenance/publication claim changed.
- Do not represent generated previews as 1024px originals; the 935 original PNGs are not part of this repository.
- See [data integrity](../docs/validation.md) and the [software-quality checklist](../docs/release-checklist.md).

This repository's own code/docs use MIT. Image/data redistribution rights remain outside that grant. See [license scope](../LICENSE-NOTES.md).
