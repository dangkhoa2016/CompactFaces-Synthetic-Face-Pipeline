#!/usr/bin/env python3
"""Offline tests for the optional Modal model manifest and basic source execution.

No credentials, model weights, GPUs, network calls or paid Modal resources.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import model_assets


class ModelAssetsTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.payloads = {
            "turbo": b"fake-model-turbo",
            "edit": b"fake-model-edit",
            "qwen": b"fake-model-qwen",
            "projector": b"fake-model-projector",
            "vae": b"fake-model-vae",
        }
        self.fixture_assets = {}
        for role, contents in self.payloads.items():
            self.fixture_assets[role] = (role + "/model.bin", hashlib.sha256(contents).hexdigest())
            path = self.root / role / "model.bin"
            path.parent.mkdir()
            path.write_bytes(contents)
        self.original_manifest = model_assets.ASSETS
        model_assets.ASSETS = self.fixture_assets
        self.addCleanup(setattr, model_assets, "ASSETS", self.original_manifest)

    def test_all_hashes_pass(self):
        result = model_assets.inspect(self.root)
        self.assertEqual("PASS", result["verdict"])
        self.assertTrue(all(v["status"] == "PASS" for v in result["models"].values()))

    def test_wrong_byte_is_mismatch(self):
        (self.root / "edit" / "model.bin").write_bytes(b"changed")
        result = model_assets.inspect(self.root)
        self.assertEqual("INCOMPLETE_OR_MISMATCH", result["verdict"])
        self.assertEqual("MISMATCH", result["models"]["edit"]["status"])

    def test_missing_file_is_failure(self):
        (self.root / "vae" / "model.bin").unlink()
        result = model_assets.inspect(self.root)
        self.assertEqual("MISSING", result["models"]["vae"]["status"])
        self.assertNotEqual("PASS", result["verdict"])

    def test_presence_only_cannot_pass(self):
        result = model_assets.inspect(self.root, verify_hashes=False)
        self.assertEqual("PRESENCE_ONLY", result["verdict"])
        self.assertFalse(result["sha256_verified"])

    def test_missing_root(self):
        result = model_assets.inspect(self.root / "missing")
        self.assertEqual("INCOMPLETE_OR_MISMATCH", result["verdict"])

    def test_manifest_all_real_entries_are_hex_sha(self):
        self.assertEqual(5, len(self.original_manifest))
        self.assertEqual(5, len({item[0] for item in self.original_manifest.values()}))
        for rel, checksum in self.original_manifest.values():
            self.assertEqual(64, len(checksum))
            self.assertTrue(all(c in "0123456789abcdef" for c in checksum))
            self.assertFalse(Path(rel).is_absolute())

    def test_python310_compatible_streaming_image_hash(self):
        script = (ROOT / "scripts" / "verify_dataset.py").read_text()
        self.assertNotIn("hashlib.file_digest", script)
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "images").mkdir()
            slots = ["SOURCE", "P1", "P2", "E1", "E2"]
            source_sha = hashlib.sha256(b"SOURCE-fake-image-data").hexdigest()
            lines = ["file_name,identity_key,collection,slot,sha256,source_sha256"]
            for slot in slots:
                name = "images/" + slot + ".png"
                contents = (slot + "-fake-image-data").encode()
                (d / name).write_bytes(contents)
                lines.append(",".join([name, "CORE:0001", "CORE", slot,
                                       hashlib.sha256(contents).hexdigest(), source_sha]))
            (d / "metadata.csv").write_text("\n".join(lines) + "\n")
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "verify_dataset.py"), str(d),
                 "--expected-images", "5", "--expected-families", "1", "--verify-images"],
                text=True, capture_output=True)
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn("PASS: 1 identity families / 5 images", run.stdout)

    def test_modal_runner_is_explicit_and_pinned(self):
        src = (ROOT / "modal_app.py").read_text()
        self.assertIn('gpu="A10G"', src)
        self.assertIn("read_only=True", src)
        self.assertIn("SDCPP_REF = ", src)
        self.assertIn("from_name(MODEL_VOLUME_NAME, create_if_missing=False)", src)
        self.assertNotIn("create_if_missing=True", src)
        self.assertIn("result_vol.commit()", src)
        self.assertIn("visual_quality_review", src)
        self.assertIn("PENDING_HUMAN_REVIEW", src)
        self.assertIn("Preserve this hairstyle verbatim", src)
        self.assertIn("202610150011", src)
        self.assertIn("202610150012", src)
        compile(src, str(ROOT / "modal_app.py"), "exec")


if __name__ == "__main__":
    unittest.main(verbosity=2)
