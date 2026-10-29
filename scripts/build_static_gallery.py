#!/usr/bin/env python3
"""Build a read-only CompactFaces 1.0.0 static preview from validated PNGs.

No public deployment, destructive cleanup, or mutation of source images.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
from PIL import Image, ImageOps, __version__ as pillow_version

SLOTS = ("SOURCE", "P1", "P2", "E1", "E2")
PUBLIC_DOWNLOADS = {
    "huggingface": "https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset",
    "kaggle": "https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset",
}


def image_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for piece in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(piece)
    return digest.hexdigest()


def safe_write_webp(
    im: Image.Image, output: Path, side: int, quality: int,
    force: bool, source_sha256: str,
) -> tuple[int, bool]:
    """Reuse a derivative only when source, encoder settings and output hash match.

    A same-size WebP without its matching marker is NEVER accepted as a cache hit.
    Cache markers live beside derivatives and do not attest to public deployment.
    """
    marker = output.with_name(output.name + ".cache.json")
    identity = {
        "schema": "compactfaces-webp-cache-v1",
        "source_png_sha256": source_sha256,
        "side": side,
        "quality": quality,
        "pillow_version": pillow_version,
    }
    if output.is_file() and marker.is_file() and not force:
        try:
            previous = json.loads(marker.read_text(encoding="utf-8"))
            if all(previous.get(key) == value for key, value in identity.items()):
                with Image.open(output) as webp:
                    valid = webp.format == "WEBP" and webp.size == (side, side)
                    if valid:
                        webp.load()
                if valid and previous.get("output_sha256") == image_sha(output):
                    return output.stat().st_size, True
        except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError):
            pass

    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.name + f".{os.getpid()}.tmp")
    marker_temp = marker.with_name(marker.name + f".{os.getpid()}.tmp")
    try:
        preview = im.resize((side, side), Image.Resampling.LANCZOS)
        preview.save(temp, format="WEBP", quality=quality, method=5)
        with Image.open(temp) as check:
            if check.format != "WEBP" or check.size != (side, side):
                raise ValueError(f"Invalid derivative output: {temp}")
            check.load()
        derivative_sha = image_sha(temp)
        os.replace(temp, output)
        marker_temp.write_text(json.dumps({
            **identity, "output_sha256": derivative_sha,
        }, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(marker_temp, marker)
    finally:
        if temp.exists():
            temp.unlink()
        if marker_temp.exists():
            marker_temp.unlink()
    return output.stat().st_size, False


def parse_and_validate(train: Path):
    with (train / "metadata.csv").open(newline="", encoding="utf-8") as inp:
        rows = list(csv.DictReader(inp))
    if len(rows) != 935:
        raise ValueError(f"Expected 935 source images; found {len(rows)} rows")
    identities = collections.defaultdict(dict)
    for row in rows:
        key, slot, collection = row["identity_key"], row["slot"], row["collection"]
        if slot not in SLOTS or slot in identities[key]:
            raise ValueError(f"Invalid identity or slot: {key}/{slot}")
        if collection not in ("CORE", "ADDITIONAL_OPTIONAL"):
            raise ValueError(f"Unexpected collection label: {key}/{slot}")
        if key.startswith("CORE:") != (collection == "CORE"):
            raise ValueError(f"Collection/identity mismatch: {key}")
        rel = Path(row["file_name"])
        if rel.is_absolute() or ".." in rel.parts or rel.parts[0] != "images" or rel.suffix.lower() != ".png":
            raise ValueError(f"Unsafe file_name: {rel}")
        if len(row["sha256"]) != 64:
            raise ValueError(f"Bad source checksum: {key}/{slot}")
        row["source_path"] = train / rel
        if not row["source_path"].is_file():
            raise FileNotFoundError(row["source_path"])
        identities[key][slot] = row
    if len(identities) != 187 or any(set(imgs) != set(SLOTS) for imgs in identities.values()):
        raise ValueError("Not exactly 187 complete five-slot families")
    if sum(key.startswith("CORE:") for key in identities) != 120:
        raise ValueError("Expected 120 Core identities")
    if sum(key.startswith("AD:") for key in identities) != 67:
        raise ValueError("Expected 67 Additional Optional identities")
    all_checksums = [record["sha256"] for group in identities.values() for record in group.values()]
    if len(all_checksums) != len(set(all_checksums)):
        raise ValueError("Duplicate image SHA256 in dataset inventory")
    for key, group in identities.items():
        source_sha = group["SOURCE"]["sha256"]
        if any(record.get("source_sha256") != source_sha for record in group.values()):
            raise ValueError(f"Invalid SOURCE lineage: {key}")
    return identities


def build_one(task):
    row, output, force = task
    rel = Path(row["file_name"]).with_suffix(".webp")
    preview_path = output / "assets" / "preview" / rel
    thumb_path = output / "assets" / "thumb" / rel
    png_path = row["source_path"]
    actual_sha = image_sha(png_path)
    if actual_sha != row["sha256"]:
        raise ValueError(f"Source SHA mismatch: {row['identity_key']}/{row['slot']}")
    with Image.open(png_path) as im:
        im.load()
        if im.size != (1024, 1024):
            raise ValueError(f"Expected 1024x1024 PNG: {png_path}")
        rgb = ImageOps.exif_transpose(im).convert("RGB")
        b1, reused_thumb = safe_write_webp(rgb, thumb_path, 400, 76, force, actual_sha)
        b2, reused_preview = safe_write_webp(rgb, preview_path, 768, 82, force, actual_sha)
    return {
        "thumb": thumb_path.relative_to(output).as_posix(),
        "preview": preview_path.relative_to(output).as_posix(),
        "sha256": actual_sha,
        "thumb_bytes": b1,
        "preview_bytes": b2,
        "reused_webp_files": int(reused_thumb) + int(reused_preview),
    }


def configure_public_output(output: Path) -> None:
    """Make only the GENERATED site public-ready; source remains staging-safe.

    This changes markup/links and does not prove that remote hosts are public or
    that the site has been deployed. Those checks are separate release gates.
    """
    config_path = output / "site-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("brand") != "CompactFaces" or config.get("release") != "1.0.0":
        raise ValueError("Unexpected gallery site config")
    config["publication_status"] = "PUBLIC"
    config["downloads"] = dict(PUBLIC_DOWNLOADS)
    config["allow_indexing"] = True
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    retired = '<meta name="robots" content="noindex,nofollow,noarchive">'
    public_origin = "https://compactfaces-synthetic-face-dataset.dangkhoa.dev"
    canonical_paths = {"index.html": "/", "about.html": "/about", "contact.html": "/contact"}
    for filename, path in canonical_paths.items():
        page = output / filename
        content = page.read_text(encoding="utf-8")
        if content.count(retired) != 1:
            raise ValueError(f"Expected exactly one staging robots meta in {filename}")
        replacement = ('<meta name="robots" content="index,follow">\n'
                       f'  <link rel="canonical" href="{public_origin}{path}">')
        page.write_text(content.replace(retired, replacement), encoding="utf-8")
    site_map = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "".join(f'  <url><loc>{public_origin}{path}</loc></url>\n'
                          for path in canonical_paths.values())
                + '</urlset>\n')
    (output / "sitemap.xml").write_text(site_map, encoding="utf-8")
    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {public_origin}/sitemap.xml\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path, required=True, help="HF ImageFolder data/train directory")
    parser.add_argument("--output", type=Path, required=True, help="Static gallery staging destination")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent / "website_src")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--force", action="store_true", help="Regenerate derivatives even when valid files exist")
    parser.add_argument("--public", action="store_true", help="Generate an indexable PUBLIC site with canonical HF/Kaggle download URLs; hosting not verified")
    args = parser.parse_args()
    train, output = args.train.resolve(), args.output.resolve()
    if train == output or train in output.parents or output in train.parents:
        raise ValueError("Gallery output and immutable input cannot be nested into each other")
    groups = parse_and_validate(train)
    if not (args.source / "index.html").exists():
        raise FileNotFoundError(args.source / "index.html")
    jobs = [(group[slot], output, args.force) for _, group in sorted(groups.items()) for slot in SLOTS]
    print(f"Starting derivative build: {len(groups)} identities, {len(jobs)} PNG, workers={args.workers}", flush=True)
    begin = time.monotonic()
    results = {}
    completed = 0
    thumb_bytes = 0
    preview_bytes = 0
    reused_webp_files = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(8, args.workers))) as pool:
        future_lookup = {pool.submit(build_one, job): (job[0]["identity_key"], job[0]["slot"]) for job in jobs}
        for future in concurrent.futures.as_completed(future_lookup):
            identity, slot = future_lookup[future]
            info = future.result()
            results[(identity, slot)] = info
            thumb_bytes += info["thumb_bytes"]
            preview_bytes += info["preview_bytes"]
            reused_webp_files += info["reused_webp_files"]
            completed += 1
            if completed % 100 == 0 or completed == len(jobs):
                print(f"  completed {completed}/{len(jobs)} (elapsed {time.monotonic()-begin:.0f}s)", flush=True)

    records = []
    for key, entries in sorted(groups.items(), key=lambda kv: (not kv[0].startswith("CORE:"), kv[0])):
        collection = "core" if key.startswith("CORE:") else "additional_optional"
        images = {}
        for slot in SLOTS:
            info = results[(key, slot)]
            images[slot] = {"thumb": info["thumb"], "preview": info["preview"], "sha256": info["sha256"]}
        records.append({"id": key, "collection": collection, "images": images})
    catalog = {
        "brand": "CompactFaces",
        "release": "1.0.0",
        "images": 935,
        "families": len(records),
        "variants": {"thumb": 400, "preview": 768, "format": "webp"},
        "items": records,
    }
    output.mkdir(parents=True, exist_ok=True)
    for filename in ("index.html", "about.html", "contact.html", "styles.css", "app.js", "pages.js", "site-config.json", "robots.txt"):
        shutil.copyfile(args.source / filename, output / filename)
    if args.public:
        configure_public_output(output)
    data = output / "data"
    data.mkdir(exist_ok=True)
    temp = data / "catalog.json.tmp"
    temp.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    os.replace(temp, data / "catalog.json")
    summary = {
        "release": "1.0.0",
        "identities": 187,
        "images": 935,
        "thumb_px": 400,
        "preview_px": 768,
        "thumb_bytes": thumb_bytes,
        "preview_bytes": preview_bytes,
        "generated_webp_files": len(jobs) * 2 - reused_webp_files,
        "reused_webp_files": reused_webp_files,
        "source_png_modified": False,
        "hosting_visibility_verified": False,
        "publication_status": json.loads((output / "site-config.json").read_text(encoding="utf-8"))["publication_status"],
    }
    (data / "build-report.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
