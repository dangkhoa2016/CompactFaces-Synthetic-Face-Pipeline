# Build and use the static WebP gallery

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](gallery.vi.md)

**Live example:** [CompactFaces gallery](https://compactfaces-synthetic-face-dataset.dangkhoa.dev/). The website shows WebP previews; original 1024×1024 PNGs are hosted separately.

## Requirements and build

A compatible five-view ImageFolder with `metadata.csv`, Python 3.10+ and Pillow:

~~~bash
python3 -m pip install Pillow
python3 scripts/build_static_gallery.py --train /path/to/data/train   --output ./compactfaces_gallery --workers 4
python3 -m http.server 8095 --bind 127.0.0.1 --directory ./compactfaces_gallery
~~~

For an explicit **Public-ready export**, use the same command with `--public` after `--workers 4`. This writes canonical Hugging Face/Kaggle links, enables the public index/robots profile, and leaves `website_src/` unchanged. **It does not deploy the output or verify remote accessibility.** Keep the default command for local preview.

Open http://127.0.0.1:8095/ in a browser. Do not open the HTML directly from disk: the gallery fetches a JSON catalog over HTTP.

## What the generated site provides

- 400px thumbnail and 768px preview WebPs for each accepted view (not source PNGs).
- Identity search, Core/Additional filters, five-slot view, light/dark appearance and EN/VI content.
- Browser-only About/Contact pages. The removal request flow **prepares a mail draft**; sending requires a working email client.
- Local/production configuration in `site-config.json`; verify all external links and search-engine indexing settings before publishing.

The builder verifies each PNG SHA256 before processing it. A previously generated WebP is reused **only when** its sidecar cache record matches the PNG SHA256, Pillow version, encoder settings and the actual WebP SHA256. Missing or corrupted markers trigger regeneration; `--force` always regenerates. The build report separates newly generated WebPs from verified cache hits.

Previews are lossy derivatives. Upload them only when distribution rights permit. Original PNGs are not modified. The local source template uses `noindex`; the explicit `--public` export enables indexing and official dataset links in the generated output.

[Architecture](architecture.md) · [Licensing](../LICENSE-NOTES.md)
