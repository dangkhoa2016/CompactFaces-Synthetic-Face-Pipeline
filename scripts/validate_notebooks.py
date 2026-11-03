#!/usr/bin/env python3
"""Check ONE production-style Kaggle CPU notebook with EN/VI Markdown cells, shared Python and an honest DEMO."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks"
NOTEBOOK_NAME = "compactfaces_kaggle_cpu_validation.ipynb"
NOTEBOOK = NOTEBOOK_DIR / NOTEBOOK_NAME
SECTIONS = (
    "intro", "contract", "setup", "inputs", "inventory",
    "integrity", "builder", "gallery", "provenance", "report", "scope",
)
SECTION_CODE_AFTER = {
    "setup", "inputs", "inventory", "integrity", "builder", "gallery", "provenance", "report",
}


def audit() -> list[str]:
    paths = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    assert paths == [NOTEBOOK], f"Only one Jupyter notebook is allowed; found: {paths}"
    obj = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert obj["nbformat"] == 4
    metadata = obj["metadata"].get("compactfaces", {})
    assert metadata.get("locale") == "en-vi"
    assert metadata.get("markdown_language_policy") == "separate_adjacent_cells"
    assert metadata.get("accelerator") == "none"
    cells = obj["cells"]
    assert len(cells) == 30, f"Expected 22 separate Markdown and 8 shared Python cells; got {len(cells)}"
    ids = [c.get("id") for c in cells]
    assert len(set(ids)) == len(ids), "Duplicate notebook cell IDs"

    executable = []
    position = 0
    for section in SECTIONS:
        for lang in ("en", "vi"):
            c = cells[position]
            assert c["cell_type"] == "markdown", (position, c["cell_type"])
            assert c["metadata"]["compactfaces"] == {"language": lang, "section": section}
            assert c["id"] == f"{section}-{lang}"
            text = "".join(c["source"])
            assert len(text.strip()) > 20
            assert ".vi.ipynb" not in text, "Stale second notebook link"
            assert (
                "**English**" in text if lang == "en" else "**Tiếng Việt**" in text
            ), (section, lang)
            assert re.search(r"(?m)^# ", text) if section == "intro" else re.search(r"(?m)^## ", text)
            position += 1
        if section in SECTION_CODE_AFTER:
            c = cells[position]
            assert c["cell_type"] == "code" and c["metadata"]["compactfaces"]["shared"] is True
            assert c.get("outputs", []) == [] and c.get("execution_count") is None
            source = "".join(c["source"])
            compile(source, f"{NOTEBOOK_NAME}:cell{position}", "exec")
            executable.append(source)
            position += 1
    assert position == len(cells)
    vi_intro = "".join(cells[1]["source"])
    for anchor in ("setup-vi","inventory-vi","integrity-vi","builder-vi","gallery-vi","report-vi"):
        assert f"(#{anchor})" in vi_intro, f"VI navigation incorrectly targets EN: {anchor}"
    assert "verified_png_dimensions_count" in executable[-1]
    for locale_id in ("intro-en", "intro-vi", "contract-en", "contract-vi", "report-en", "report-vi"):
        content = "".join(next(c["source"] for c in cells if c["id"] == locale_id))
        assert "FULL_PASS" in content or "FULL PASS" in content, f"Missing FULL scope explanation: {locale_id}"
    assert "verify_png_header_and_hash" in "\n".join(executable)
    assert len(executable) == 8
    print(f"PASS: one notebook, {len(SECTIONS)} paired Markdown sections, {len(executable)} shared Python cells.")
    return executable


def run_demo(sources: list[str], lang: str) -> dict:
    ns = {"__name__": "__main__"}
    for code in sources:
        code = code.replace('MODE = "auto"', 'MODE = "demo"').replace('MODE = "full"', 'MODE = "demo"')
        code = code.replace("EXPORT_REPORT = True", "EXPORT_REPORT = False")
        code = code.replace('LANGUAGE = "en"', f'LANGUAGE = "{lang}"')
        exec(compile(code, f"{NOTEBOOK_NAME}:demo:{lang}", "exec"), ns)
    assert ns["LANGUAGE"] == lang, "DEMO output locale mismatch"
    result = ns["report"]
    assert result["verdict"] == "DEMO_ONLY"
    assert result["mode"] == "DEMO"
    assert result["identities"] == 2 and result["records"] == 10
    assert result["verified_png_sha256_count"] == 0
    assert result["verified_png_dimensions_count"] == 0
    assert result["checks"]["png_dimensions"] == "SKIPPED_DEMO"
    assert result["checks"]["png_sha256"] == "SKIPPED_DEMO"
    assert result["checks"]["builder"] == "SKIPPED_DEMO"
    assert result["checks"]["provenance"] == "SKIPPED_DEMO"
    assert result["generation_provenance_verified"] == 0
    assert result["source_lineage_verified"] == 0
    assert all({"file_name", "identity_key", "collection", "slot", "sha256", "source_sha256", "archive_name", "archive_file_name"} <= set(row) for row in ns["rows"])
    assert result["device_class"] == "CPU" and "device_id" not in result
    assert result["dataset_version"] is None and result["dataset_version_verification"] == "NOT_CHECKED"
    assert result["validation_scope"] == "FILE_INTEGRITY_AND_METADATA_ONLY"
    assert result["visual_quality_assessed"] is False
    print(f"PASS {lang}: no-data CPU DEMO, zero PNGs claimed verified.")
    return ns


def test_negative_cases(ns: dict) -> None:
    from copy import deepcopy

    rows = []
    for identity,collection,base in (
        ("CORE:0002","CORE","identity_0002"),
        ("AD:AD0002","ADDITIONAL_OPTIONAL","AD0002"),
    ):
        source_sha = "a"*64 if collection == "CORE" else "b"*64
        for slot in ("SOURCE","P1","P2","E1","E2"):
            sha = source_sha if slot == "SOURCE" else (str(len(rows)+1)*64)[:64]
            rows.append({"identity_key":identity,"collection":collection,
                         "slot":slot,"sha256":sha,"source_sha256":source_sha,
                         "archive_file_name":f"images/{base}_{slot}.png"})
    expected = ns["expected_builder_paths"](rows)
    assert len(expected)==10
    assert "WEB_COLLECTION_BUILDER/previews/core_0002_SOURCE.jpg" in expected
    assert "WEB_COLLECTION_BUILDER/previews/additional_AD0002_E2.jpg" in expected
    entries=[]
    for identity,collection in (("CORE:0002","core"),("AD:AD0002","additional")):
        group={r["slot"]:r for r in rows if r["identity_key"]==identity}
        entries.append({"key":identity,"collection":collection,
                        "id":identity.split(":",1)[1],
                        "source_sha256":group["SOURCE"]["sha256"],
                        "slot_sha256":{k:v["sha256"] for k,v in group.items()},
                        "image_paths":{k:v["archive_file_name"] for k,v in group.items()}})
    catalog={"schema":"compactfaces_collection_builder_catalog_v1",
             "total_families":2,"total_images":10,"core_count":1,
             "additional_optional_count":1,"entries":entries}
    ns["verify_builder_catalog"](catalog,rows)
    def must_reject(fn,case):
        try:
            fn()
        except (ValueError,KeyError,AssertionError):
            return
        raise AssertionError(f"Accepted malformed fixture: {case}")
    wrong=deepcopy(catalog)
    wrong["entries"][0]["slot_sha256"]["P1"]="0"*64
    must_reject(lambda:ns["verify_builder_catalog"](wrong,rows),"tampered SHA")
    wrong=deepcopy(catalog)
    wrong["entries"][1]["image_paths"]["P2"]="images/wrong.png"
    must_reject(lambda:ns["verify_builder_catalog"](wrong,rows),"wrong preview original")
    wrong=deepcopy(catalog)
    wrong["entries"][1]["key"]="CORE:0002"
    must_reject(lambda:ns["verify_builder_catalog"](wrong,rows),"duplicate Builder identity")
    wrong=deepcopy(rows)
    wrong[1]["slot"]="SOURCE"
    must_reject(lambda:ns["expected_builder_paths"](wrong),"duplicate preview name")
    ns["verify_lineage_identity_keys"](
        [{"identity_key":"CORE:0002"},{"identity_key":"AD:AD0002"}],
        {"CORE:0002","AD:AD0002"})
    must_reject(lambda:ns["verify_lineage_identity_keys"](
        [{"identity_key":"CORE:0002"},{"identity_key":"CORE:0002"}],
        {"CORE:0002","AD:AD0002"}),"duplicate lineage")
    must_reject(lambda:ns["verify_lineage_identity_keys"](
        [{"identity_key":"CORE:0002"},{"identity_key":"AD:AD9999"}],
        {"CORE:0002","AD:AD0002"}),"wrong lineage identity")
    print("PASS: 6 negative Builder/lineage checks (hash, path, duplicate/mismatch).")


def test_input_detection_contract(sources: list[str]) -> None:
    """AUTO must ignore unrelated datasets but reject partial CompactFaces mounts."""
    import contextlib
    import io
    import os
    import tempfile
    from unittest.mock import patch

    with tempfile.TemporaryDirectory(prefix="compactfaces-auto-input-") as temp:
        input_root = Path(temp) / "kaggle_input"
        input_root.mkdir()
        def classify():
            namespace = {"__name__": "__main__"}
            with patch.dict(os.environ, {
                    "COMPACTFACES_KAGGLE_INPUT_ROOT": str(input_root),
                    "COMPACTFACES_DATASET_DIR": "",
                    "COMPACTFACES_NOTEBOOK_LANGUAGE": "en"}), contextlib.redirect_stdout(io.StringIO()):
                for code in sources[:2]:
                    exec(compile(code, "notebook:auto:input-detection", "exec"), namespace)
            return namespace["active_mode"]

        assert classify() == "demo", "No input must select DEMO"
        unrelated = input_root / "unrelated-dataset"
        unrelated.mkdir()
        (unrelated / "metadata.csv").write_text("other_column,value\n", encoding="utf-8")
        assert classify() == "demo", "Unrelated input must be ignored"

        partial = input_root / "compactfaces-synthetic-face-dataset"
        (partial / "core_600png/images").mkdir(parents=True)
        (partial / "additional_optional_335png/images").mkdir(parents=True)
        (partial / "metadata.csv").write_text("identity_key,collection,slot\n", encoding="utf-8")
        try:
            classify()
        except FileNotFoundError as exc:
            assert "Incomplete CompactFaces input" in str(exc), exc
        else:
            raise AssertionError("AUTO silently accepted a missing Builder directory")
        print("PASS: AUTO rejects partially mounted CompactFaces, not DEMO_ONLY")

        (partial / "collection_builder_187/WEB_COLLECTION_BUILDER/previews").mkdir(parents=True)
        assert classify() == "full", "Complete directory structure must select FULL"
        (partial / "metadata.csv").unlink()
        try:
            classify()
        except FileNotFoundError as exc:
            assert "Incomplete CompactFaces input" in str(exc), exc
        else:
            raise AssertionError("AUTO silently accepted missing CompactFaces metadata.csv")
        print("PASS: AUTO accepts complete layout and rejects missing metadata.csv")


def test_duplicate_imagefolder_file_name(sources: list[str]) -> None:
    """Two distinct slots cannot resolve to the same ImageFolder file_name."""
    import csv
    import tempfile

    with tempfile.TemporaryDirectory(prefix="compactfaces-duplicate-path-") as temp:
        path = Path(temp) / "metadata.csv"
        rows = []
        for slot, sha in (("SOURCE", "a" * 64), ("P1", "b" * 64)):
            rows.append({
                "file_name": "images/repeated.png", "identity_key": "CORE:0000",
                "collection": "CORE", "slot": slot, "sha256": sha,
                "source_sha256": "a" * 64, "archive_name": "core_600png.zip",
                "archive_file_name": f"images/unique_{slot}.png"})
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        namespace = {"__name__": "__main__"}
        exec(compile(sources[0].replace('MODE = "auto"', 'MODE = "demo"'),
                     "notebook:duplicate:setup", "exec"), namespace)
        exec(compile(sources[1], "notebook:duplicate:imports", "exec"), namespace)
        namespace["root"] = Path(temp)
        namespace["active_mode"] = "full"
        try:
            exec(compile(sources[2], "notebook:duplicate:metadata", "exec"), namespace)
        except ValueError as exc:
            assert "Duplicate ImageFolder path" in str(exc), exc
        else:
            raise AssertionError("Duplicate ImageFolder file_name unexpectedly accepted")
        print("PASS: duplicate ImageFolder file_name rejected independently of ZIP path")


if __name__ == "__main__":
    sources = audit()
    for locale in ("en", "vi"):
        namespace = run_demo(sources, locale)
        test_negative_cases(namespace)
    test_input_detection_contract(sources)
    test_duplicate_imagefolder_file_name(sources)
    print("PASS: integrated bilingual notebook and honest CPU validation.")
