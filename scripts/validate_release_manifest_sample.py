#!/usr/bin/env python3
"""Validate that the *illustrative* release manifest is internally consistent."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLOTS = {"SOURCE", "P1", "P2", "E1", "E2"}
EXPECTED = {"core": (120, 600), "additional_optional": (67, 335)}
SHA = re.compile(r"[0-9a-f]{64}\Z")


def validate(manifest: dict) -> None:
    if manifest.get("schema") != "compactfaces_release_manifest_v1" or manifest.get("example_only") is not True:
        raise ValueError("Must be an illustrative CompactFaces release manifest")
    if manifest.get("identity_families") != 187 or manifest.get("image_count") != 935:
        raise ValueError("Canonical release inventory is not 187 families / 935 PNG")
    collection_counts = manifest["collections"]
    if set(collection_counts) != set(EXPECTED):
        raise ValueError("Unexpected collection")
    if any((collection_counts[k]["families"], collection_counts[k]["images"]) != pair
           for k, pair in EXPECTED.items()):
        raise ValueError("Collection counts differ from canonical release")
    if sum(v["families"] for v in collection_counts.values()) != manifest["identity_families"]:
        raise ValueError("Family totals differ")
    if sum(v["images"] for v in collection_counts.values()) != manifest["image_count"]:
        raise ValueError("Image totals differ")
    if set(manifest["slots"]) != SLOTS or len(manifest["slots"]) != 5:
        raise ValueError("Five slots required")
    images = manifest["images"]
    if len(images) != manifest["sample_count"] or len(images) % 5:
        raise ValueError("Example sample count must include complete five-slot families")
    groups = defaultdict(dict)
    for row in images:
        if row["slot"] not in SLOTS or row["slot"] in groups[row["identity_key"]]:
            raise ValueError("Duplicate/invalid sample slot")
        if row["collection"] not in {"CORE", "ADDITIONAL_OPTIONAL"}:
            raise ValueError("Invalid collection in sample")
        if not SHA.fullmatch(row["sha256"]) or not SHA.fullmatch(row["source_sha256"]):
            raise ValueError("Invalid sample SHA")
        groups[row["identity_key"]][row["slot"]] = row
    for identity, items in groups.items():
        if set(items) != SLOTS:
            raise ValueError("Each sampled identity must have all five slots")
        source = items["SOURCE"]["sha256"]
        if any(row["source_sha256"] != source for row in items.values()):
            raise ValueError("Inconsistent sampled SOURCE binding")
        if len({row["collection"] for row in items.values()}) != 1:
            raise ValueError("Mixed collection in sampled identity")


if __name__ == "__main__":
    validate(json.loads((ROOT / "examples/release_manifest_sample.json").read_text(encoding="utf-8")))
    print("PASS: illustrative release manifest counts, sample families, slots and hashes.")
