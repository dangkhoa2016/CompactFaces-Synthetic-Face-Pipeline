# Static identity gallery source

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

`website_src/` is a **standalone, bilingual HTML/CSS/JavaScript frontend** used by the CompactFaces technical project. It implements Explore, About, Contact, search, collection and slot filters, pagination, deep links, keyboard/swipe controls and a five-image viewer. No backend or analytics provider is required.

The repository contains the website **source**, not generated images. To display a collection, provide an authorized local ImageFolder with `metadata.csv` and the five-slot PNG files. The reference builder validates all image hashes and produces 400px WebP thumbnails plus 768px WebP previews:

```bash
python3 -m pip install Pillow
python3 scripts/build_static_gallery.py   --train /path/to/compatible/data/train   --output /path/to/gallery
python3 -m http.server 8095 --bind 127.0.0.1 --directory /path/to/gallery
```

Add `--public` to the builder only when preparing the public site export; it enables canonical external download URLs, per-page canonical tags, a sitemap and an indexable robots profile **in the generated output only**. Re-deploy the generated export (including `robots.txt` and `sitemap.xml`) for search engines to see these settings; updating the source alone does not modify an already hosted site. Public hosting and link availability must still be independently checked.

The builder is configured for the **CompactFaces 1.0.0 case-study inventory** (187 five-view families), with per-file SHA256 and SOURCE lineage checks. This is an optional export example; the repository's CPU tests work independently using `examples/` without input PNGs.

## Asset and link policy

- The static site contains **WebP derivatives only**; original 1024px PNGs remain with their owner.
- The source `site-config.json` is a **local preview configuration** with external download URLs unset. Use the builder's `--public` option to generate a site with dataset links and public indexing in the output directory. Source HTML has `noindex` for local previews.
- Hugging Face and Kaggle links are resolved from the deployment configuration. The viewer serves WebP previews, not the original PNG downloads.
- About explains the source toolkit. Contact creates a `mailto:` draft including selected identity/slot; it never submits a server request, uploads selfies or claims automatic deletion.
- Source PNGs, curation logs, credentials and runtime model weights are excluded from Git.

The website can be served offline using a local HTTP server after the user supplies a compatible catalog. The CI source checks require neither this catalog nor any remote dataset.
