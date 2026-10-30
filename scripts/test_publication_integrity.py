#!/usr/bin/env python3
"""Offline negative tests for release sample and platform metadata comparison."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.compare_platform_metadata import compare
from scripts.validate_release_manifest_sample import ROOT, validate
from scripts.validate_repository import check_ci_badge


class READMEWorkflowBadgeTest(unittest.TestCase):
    def test_ci_is_rendered_as_image_in_both_readmes(self):
        url = "https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline/actions/workflows/ci.yml"
        badge = f"[![CI]({url}/badge.svg?branch=main)]({url})"
        for name in ("README.md", "README.vi.md"):
            with self.subTest(readme=name):
                content = (ROOT / name).read_text(encoding="utf-8")
                check_ci_badge(content, name)
                plain_link_only = content.replace(badge, f"[CI workflow]({url})", 1)
                with self.assertRaises(AssertionError):
                    check_ci_badge(plain_link_only, name)


class ReleaseManifestTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "examples/release_manifest_sample.json").read_text())

    def test_valid_sample(self):
        validate(self.manifest)

    def test_incorrect_release_collection_counts_rejected(self):
        data = deepcopy(self.manifest)
        data["collections"]["additional_optional"]["families"] = 73
        data["collections"]["additional_optional"]["images"] = 365
        with self.assertRaises(ValueError):
            validate(data)

    def test_incomplete_five_slot_sample_rejected(self):
        data = deepcopy(self.manifest)
        data["images"].pop()
        data["sample_count"] -= 1
        with self.assertRaises(ValueError):
            validate(data)

    def test_source_binding_rejected(self):
        data = deepcopy(self.manifest)
        data["images"][1]["source_sha256"] = "f" * 64
        with self.assertRaises(ValueError):
            validate(data)


class PlatformMetadataTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.hf = Path(self.temp.name) / "hf.csv"
        self.kaggle = Path(self.temp.name) / "kaggle.csv"
        self.fields = ["identity_key", "collection", "slot", "sha256", "source_sha256"]
        self.rows = []
        for collection, count, prefix in (("CORE", 120, "CORE"), ("ADDITIONAL_OPTIONAL", 67, "AD")):
            for idx in range(count):
                identity = f"CORE:{idx:04d}" if prefix == "CORE" else f"AD:AD{idx:04d}"
                source_sha = f"{idx + (0 if prefix == 'CORE' else 1000):064x}"
                for slot in ("SOURCE", "P1", "P2", "E1", "E2"):
                    self.rows.append({
                        "identity_key": identity, "collection": collection, "slot": slot,
                        "sha256": source_sha,
                        "source_sha256": source_sha,
                    })
        self.write(self.hf, self.rows)
        self.write(self.kaggle, self.rows)

    def write(self, path, rows):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_equal_snapshots(self):
        report = compare(self.hf, self.kaggle)
        self.assertEqual(report["png_sha256_matching"], 935)
        self.assertEqual(report["png_sha256_differing"], 0)
        self.assertEqual(report["decoded_pixel_equivalence"], "NOT_CHECKED")

    def test_changed_source_is_metadata_difference_not_pixel_proof(self):
        altered = deepcopy(self.rows)
        altered[0]["sha256"] = "f" * 64
        for row in altered[:5]:
            row["source_sha256"] = "f" * 64
        self.write(self.kaggle, altered)
        report = compare(self.hf, self.kaggle)
        self.assertEqual(report["png_sha256_differing"], 1)
        self.assertEqual(report["differing_slots"], ["SOURCE"])
        self.assertEqual(report["decoded_pixel_equivalence"], "NOT_CHECKED")

    def test_missing_slot_rejected(self):
        self.write(self.kaggle, self.rows[:-1])
        with self.assertRaises(ValueError):
            compare(self.hf, self.kaggle)

    def test_duplicate_slot_rejected(self):
        self.write(self.kaggle, self.rows + [self.rows[0]])
        with self.assertRaises(ValueError):
            compare(self.hf, self.kaggle)


if __name__ == "__main__":
    unittest.main()
