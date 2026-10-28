#!/usr/bin/env python3
"""Check CompactFaces ImageFolder metadata and, optionally, original PNG bytes.

This tool validates a local copy. It does not verify remote hosting, image
decoding, full creation history, or Kaggle's extracted folder layout.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import re
from pathlib import Path

SLOTS = {"SOURCE", "P1", "P2", "E1", "E2"}
REQUIRED = {"file_name", "identity_key", "collection", "slot", "sha256", "source_sha256"}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
CORE_ID = re.compile(r"CORE:[0-9]{4}\Z")
AD_ID = re.compile(r"AD:AD[0-9]{4}\Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(data_dir: Path, expected_images: int = 935,
             expected_families: int = 187, verify_images: bool = False) -> dict:
    root = data_dir.resolve()
    with (root / "metadata.csv").open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames is not None and REQUIRED <= set(reader.fieldnames),
                f"metadata.csv missing required columns: {sorted(REQUIRED - set(reader.fieldnames or []))}")
        rows = list(reader)
    require(len(rows) == expected_images,
            f"Expected {expected_images} image records, found {len(rows)}")

    groups = collections.defaultdict(dict)
    collections_count = collections.Counter()
    paths = set()
    image_hashes = set()
    for row in rows:
        identity = row["identity_key"]
        slot = row["slot"]
        collection = row["collection"]
        require(slot in SLOTS, f"Invalid slot: {identity}/{slot}")
        require(slot not in groups[identity], f"Duplicate slot: {identity}/{slot}")
        require(
            (collection == "CORE" and CORE_ID.fullmatch(identity) is not None) or
            (collection == "ADDITIONAL_OPTIONAL" and AD_ID.fullmatch(identity) is not None),
            f"Invalid identity/collection: {identity}/{collection}",
        )
        for field in ("sha256", "source_sha256"):
            require(SHA256.fullmatch(row[field]) is not None,
                    f"Invalid {field}: {identity}/{slot}")
        require(row["sha256"] not in image_hashes,
                f"Duplicate PNG SHA256 in inventory: {identity}/{slot}")
        image_hashes.add(row["sha256"])

        filename = row["file_name"]
        rel = Path(filename)
        require(filename == rel.as_posix() and not rel.is_absolute() and
                ".." not in rel.parts and len(rel.parts) >= 2 and
                rel.parts[0] == "images" and rel.suffix.lower() == ".png",
                f"Unsafe or invalid PNG path: {filename}")
        require(filename not in paths, f"Duplicate image path: {filename}")
        paths.add(filename)

        if verify_images:
            image = (root / rel).resolve()
            require(image.is_relative_to(root) and image.is_file(),
                    f"Missing or outside-root PNG: {filename}")
            digest = hashlib.sha256()
            with image.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            require(digest.hexdigest() == row["sha256"],
                    f"PNG SHA256 mismatch: {filename}")

        groups[identity][slot] = row
        collections_count[collection] += 1

    require(len(groups) == expected_families,
            f"Expected {expected_families} families, found {len(groups)}")
    for identity, slots in groups.items():
        require(set(slots) == SLOTS, f"Missing/extra view for {identity}")
        source_sha = slots["SOURCE"]["sha256"]
        require(all(row["source_sha256"] == source_sha for row in slots.values()),
                f"Incorrect SOURCE binding: {identity}")
        require(len({row["collection"] for row in slots.values()}) == 1,
                f"Mixed collections: {identity}")

    if expected_images == 935 and expected_families == 187:
        require(collections_count["CORE"] == 600 and
                collections_count["ADDITIONAL_OPTIONAL"] == 335,
                f"Wrong canonical collection counts: {dict(collections_count)}")
        require(sum(identity.startswith("CORE:") for identity in groups) == 120 and
                sum(identity.startswith("AD:") for identity in groups) == 67,
                "Wrong canonical identity distribution")
    return {
        "families": len(groups), "images": len(rows),
        "verified_png_sha256": len(rows) if verify_images else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", type=Path,
                        help="ImageFolder directory with metadata.csv and images/")
    parser.add_argument("--expected-images", type=int, default=935)
    parser.add_argument("--expected-families", type=int, default=187)
    parser.add_argument("--verify-images", action="store_true")
    args = parser.parse_args()
    result = validate(args.data_dir, args.expected_images,
                      args.expected_families, args.verify_images)
    print(f"PASS: {result['families']} identity families / {result['images']} images")
    if args.verify_images:
        print(f"PNG SHA256 verified: {result['verified_png_sha256']}/{result['images']}")
    else:
        print("PNG SHA256: NOT_CHECKED (omit --verify-images only for metadata checks)")


if __name__ == "__main__":
    main()
