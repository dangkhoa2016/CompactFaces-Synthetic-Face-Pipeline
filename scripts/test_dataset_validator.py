#!/usr/bin/env python3
"""Negative regressions for the local ImageFolder metadata validator."""
from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.verify_dataset import validate

SLOTS = ("SOURCE", "P1", "P2", "E1", "E2")
FIELDS = ("file_name", "identity_key", "collection", "slot", "sha256", "source_sha256")


class DatasetValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.rows = []
        for identity, collection in (
            ("CORE:0001", "CORE"),
            ("AD:AD0001", "ADDITIONAL_OPTIONAL"),
        ):
            source = hashlib.sha256(f"{identity}/SOURCE".encode()).hexdigest()
            for slot in SLOTS:
                data = f"{identity}/{slot}".encode()
                filename = f"images/{identity.replace(':', '_')}_{slot}.png"
                dest = self.root / filename
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                self.rows.append({
                    "file_name": filename, "identity_key": identity,
                    "collection": collection, "slot": slot,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "source_sha256": source,
                })
        self.write()

    def write(self):
        with (self.root / "metadata.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(self.rows)

    def validate(self, verify_images=False):
        self.write()
        return validate(self.root, 10, 2, verify_images)

    def test_good_schema_and_actual_png_sha256(self):
        result = self.validate(True)
        self.assertEqual(result["verified_png_sha256"], 10)

    def test_wrong_source_binding_rejected(self):
        self.rows[1]["source_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "SOURCE binding"):
            self.validate()

    def test_mixed_collections_rejected(self):
        self.rows[1]["collection"] = "ADDITIONAL_OPTIONAL"
        with self.assertRaisesRegex(ValueError, "identity/collection"):
            self.validate()

    def test_duplicate_image_hash_rejected(self):
        self.rows[1]["sha256"] = self.rows[0]["sha256"]
        with self.assertRaisesRegex(ValueError, "Duplicate PNG SHA256"):
            self.validate()

    def test_unsafe_path_rejected_without_opening(self):
        self.rows[0]["file_name"] = "../outside.png"
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            self.validate()

    def test_broken_png_hash_detected(self):
        path = self.root / self.rows[0]["file_name"]
        path.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "PNG SHA256 mismatch"):
            self.validate(True)

    def test_bad_slot_rejected(self):
        self.rows[0]["slot"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "Invalid slot"):
            self.validate()

    def test_duplicate_slot_rejected(self):
        self.rows[1]["slot"] = "SOURCE"
        with self.assertRaisesRegex(ValueError, "Duplicate slot"):
            self.validate()

    def test_bogus_collection_rejected(self):
        self.rows[0]["collection"] = "NOT_A_COLLECTION"
        with self.assertRaisesRegex(ValueError, "identity/collection"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
