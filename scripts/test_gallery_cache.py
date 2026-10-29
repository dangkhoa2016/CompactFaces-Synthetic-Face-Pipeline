#!/usr/bin/env python3
"""Test conservative WebP reuse against the original image's SHA256."""
from __future__ import annotations

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from scripts.build_static_gallery import safe_write_webp, configure_public_output


class GalleryCacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name) / "thumb.webp"
        self.image = Image.new("RGB", (16, 16), (20, 80, 160))
        self.sha = hashlib.sha256(b"source-png-A").hexdigest()

    def build(self, force=False, sha=None, quality=76):
        return safe_write_webp(self.image, self.output, 12, quality, force, sha or self.sha)

    def test_cache_hit_only_when_all_inputs_match(self):
        self.assertFalse(self.build()[1])
        self.assertTrue(self.build()[1])

    def test_missing_marker_forces_rebuild(self):
        self.build()
        self.output.with_name(self.output.name + ".cache.json").unlink()
        self.assertFalse(self.build()[1])

    def test_changed_png_hash_forces_rebuild(self):
        self.build()
        another = hashlib.sha256(b"source-png-B").hexdigest()
        self.assertFalse(self.build(sha=another)[1])
        self.assertTrue(self.build(sha=another)[1])

    def test_corrupt_output_forces_rebuild(self):
        self.build()
        self.output.write_bytes(b"not a webp")
        self.assertFalse(self.build()[1])
        with Image.open(self.output) as check:
            self.assertEqual(check.format, "WEBP")

    def test_changed_encoder_quality_forces_rebuild(self):
        self.build()
        self.assertFalse(self.build(quality=82)[1])

    def test_force_regenerates(self):
        self.build()
        self.assertFalse(self.build(force=True)[1])


class PublicOutputTests(unittest.TestCase):
    def test_explicit_public_profile_does_not_edit_staging_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "published"
            output.mkdir()
            source = Path(__file__).resolve().parent.parent / "website_src"
            names = ("index.html", "about.html", "contact.html", "site-config.json", "robots.txt")
            for name in names:
                shutil.copyfile(source / name, output / name)
            original = (source / "site-config.json").read_bytes()
            configure_public_output(output)
            import json
            config = json.loads((output / "site-config.json").read_text())
            self.assertEqual(config["publication_status"], "PUBLIC")
            self.assertTrue(config["allow_indexing"])
            self.assertEqual(set(config["downloads"]), {"huggingface", "kaggle"})
            self.assertTrue(all(url.startswith("https://") for url in config["downloads"].values()))
            for name in ("index.html", "about.html", "contact.html"):
                html = (output / name).read_text()
                self.assertIn('content="index,follow"', html)
                self.assertNotIn('content="noindex,nofollow,noarchive"', html)
                self.assertIn('rel="canonical"', html)
            robots = (output / "robots.txt").read_text()
            self.assertIn("Allow: /", robots)
            self.assertIn("Sitemap: https://compactfaces-synthetic-face-dataset.dangkhoa.dev/sitemap.xml", robots)
            sitemap = (output / "sitemap.xml").read_text()
            self.assertIn("https://compactfaces-synthetic-face-dataset.dangkhoa.dev/about", sitemap)
            self.assertIn("https://compactfaces-synthetic-face-dataset.dangkhoa.dev/contact", sitemap)
            self.assertNotIn("<script", sitemap)
            self.assertEqual((source / "site-config.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
