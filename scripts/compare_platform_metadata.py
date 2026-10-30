#!/usr/bin/env python3
"""Compare authorized CompactFaces metadata snapshots without copying private image records.

A byte-SHA mismatch is NOT evidence of pixel equivalence. This program never
makes a decoded-pixel claim without the images and an independent image test.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SLOTS = {"SOURCE", "P1", "P2", "E1", "E2"}
COLLECTIONS = {"CORE": (120, 600), "ADDITIONAL_OPTIONAL": (67, 335)}
SHA = re.compile(r"[a-f0-9]{64}\Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for part in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest()


def read_snapshot(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"identity_key", "collection", "slot", "sha256", "source_sha256"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path.name}: missing required metadata columns")
        result = {}
        for row in reader:
            key = (row["identity_key"], row["slot"])
            if key in result:
                raise ValueError(f"{path.name}: duplicate identity/slot")
            if row["collection"] not in COLLECTIONS or row["slot"] not in SLOTS:
                raise ValueError(f"{path.name}: unknown collection or slot")
            if not SHA.fullmatch(row["sha256"]) or not SHA.fullmatch(row["source_sha256"]):
                raise ValueError(f"{path.name}: invalid SHA256")
            result[key] = row
    families = {}
    for (identity, slot), row in result.items():
        pattern = r"CORE:[0-9]{4}" if row["collection"] == "CORE" else r"AD:AD[0-9]{4}"
        if not re.fullmatch(pattern, identity):
            raise ValueError(f"{path.name}: invalid identity syntax")
        families.setdefault(identity, {})[slot] = row
    for identity, slots in families.items():
        if set(slots) != SLOTS:
            raise ValueError(f"{path.name}: identity has missing slots")
        source = slots["SOURCE"]["sha256"]
        if any(row["source_sha256"] != source for row in slots.values()):
            raise ValueError(f"{path.name}: inconsistent SOURCE binding")
        if len({row["collection"] for row in slots.values()}) != 1:
            raise ValueError(f"{path.name}: mixed collection within one identity")
    return result


def compare(hf_csv: Path, kaggle_csv: Path) -> dict:
    hf = read_snapshot(hf_csv)
    kaggle = read_snapshot(kaggle_csv)
    if set(hf) != set(kaggle):
        raise ValueError("Identity/slot sets differ between the platforms")
    if len(hf) != 935 or len({identity for identity, _ in hf}) != 187:
        raise ValueError("Unexpected canonical 187-family / 935-image inventory")
    families: dict[str, set[str]] = {}
    counts = Counter()
    for (identity, slot), row in hf.items():
        other = kaggle[(identity, slot)]
        if row["collection"] != other["collection"]:
            raise ValueError("Collection mismatch across platforms")
        families.setdefault(identity, set()).add(slot)
        counts[row["collection"]] += 1
    if any(slots != SLOTS for slots in families.values()):
        raise ValueError("Missing/duplicate five-view identity slot")
    for collection, (expected_families, expected_images) in COLLECTIONS.items():
        if counts[collection] != expected_images:
            raise ValueError("Canonical collection count mismatch")
        if sum(hf[(key, "SOURCE")]["collection"] == collection for key in families) != expected_families:
            raise ValueError("Canonical family count mismatch")
    matching = sum(hf[key]["sha256"] == kaggle[key]["sha256"] for key in hf)
    different = len(hf) - matching
    differing_slots = sorted({slot for key, slot in hf if hf[(key, slot)]["sha256"] != kaggle[(key, slot)]["sha256"]})
    return {
        "schema": "compactfaces_platform_metadata_comparison_v1",
        "records": len(hf),
        "identities": len(families),
        "collections": dict(sorted(counts.items())),
        "same_identity_slot_set": True,
        "png_sha256_matching": matching,
        "png_sha256_differing": different,
        "differing_slots": differing_slots,
        "hf_metadata_csv_sha256": sha256_file(hf_csv),
        "kaggle_metadata_csv_sha256": sha256_file(kaggle_csv),
        "decoded_pixel_equivalence": "NOT_CHECKED",
        "note": "A PNG byte difference does not prove matching decoded pixels.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hf_metadata_csv", type=Path)
    parser.add_argument("kaggle_metadata_csv", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON summary location (no identity-level data)")
    args = parser.parse_args()
    result = compare(args.hf_metadata_csv, args.kaggle_metadata_csv)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
