#!/usr/bin/env python3
"""Regression-test real notebook FULL/PARTIAL contracts on generated local fixtures.

No released portraits, model weights, tokens, or external downloads are used.
Pillow is required; generated images and reports stay in a temporary directory.
"""
from __future__ import annotations
import contextlib
import csv
import hashlib
import io
import json
import os
import tempfile
from pathlib import Path
from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parent.parent
SLOTS = ("SOURCE", "P1", "P2", "E1", "E2")
COLUMNS = (
    "file_name", "identity_key", "collection", "slot", "sha256",
    "source_sha256", "archive_name", "archive_file_name",
)
def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def write_fixture(directory:Path)->Path:
    root=directory/"extracted"
    root.mkdir()
    preview=io.BytesIO()
    Image.new("RGB",(12,12),(80,90,100)).save(preview,format="JPEG")
    jpeg=preview.getvalue()
    rows=[]
    generation=[]
    lineages=[]
    catalog=[]
    for collection,n,prefix,archive in (
        ("CORE",120,"CORE","core_600png"),
        ("ADDITIONAL_OPTIONAL",67,"AD:AD","additional_optional_335png"),
    ):
        for number in range(n):
            identity=(f"CORE:{number:04d}" if collection=="CORE" else f"AD:AD{number:04d}")
            view={}
            source_hash=None
            source_meta=None
            for slot_index,slot in enumerate(SLOTS):
                filename=f"{prefix.replace(':','_')}_{number:04d}_{slot}.png"
                path=f"images/{filename}"
                file_name=f"images/{'core' if collection=='CORE' else 'additional_optional'}/{filename}"
                positive=f"synthetic fixture identity {identity} slot {slot}"
                negative="fixture only; not released"
                seed=number*10+slot_index
                raw={"prompt":{"positive":positive,"negative":negative},
                     "seed":seed,"sampling":{"steps":8}}
                embedded="Synthetic fixture metadata\nSDCPP: "+json.dumps(raw,ensure_ascii=False,sort_keys=True)
                image_path=root/archive/path
                image_path.parent.mkdir(parents=True,exist_ok=True)
                image_size=(12,12)  # synthetic fixture; production expects 1024px
                image=Image.new("RGB",image_size,(90,95,100))
                pnginfo=PngImagePlugin.PngInfo()
                pnginfo.add_text("parameters",embedded)
                image.save(image_path,format="PNG",pnginfo=pnginfo)
                image_sha=sha(image_path.read_bytes())
                if slot=="SOURCE":
                    source_hash=image_sha
                    source_meta=(sha(positive.encode()),seed)
                entry={"file_name":file_name,"identity_key":identity,
                       "collection":collection,"slot":slot,"sha256":image_sha,
                       "source_sha256":source_hash,
                       "archive_name":archive+".zip","archive_file_name":path}
                rows.append(entry)
                generation.append({
                    "identity_key":identity,"slot":slot,"file_name":file_name,
                    "png_sha256":image_sha,
                    "embedded_parameters_sha256":sha(embedded.encode()),
                    "sdcpp_parameters":raw,"positive_prompt":positive,
                    "negative_prompt":negative,"seed":seed,"steps":8,
                    "prompt_sha256":sha(positive.encode()),
                })
                view[slot]=entry
                preview_path=(root/"collection_builder_187"/"WEB_COLLECTION_BUILDER"/"previews"/
                              f"{'core' if collection=='CORE' else 'additional'}_{identity.split(':',1)[1]}_{slot}.jpg")
                preview_path.parent.mkdir(parents=True,exist_ok=True)
                preview_path.write_bytes(jpeg)
            lineages.append({"identity_key":identity,
                             "source_png_sha256":source_hash,
                             "final_step_prompt_sha256":source_meta[0],
                             "final_step_seed":source_meta[1]})
            catalog.append({"key":identity,
                            "collection":"core" if collection=="CORE" else "additional",
                            "id":identity.split(":",1)[1],
                            "source_sha256":source_hash,
                            "slot_sha256":{k:v["sha256"] for k,v in view.items()},
                            "image_paths":{k:v["archive_file_name"] for k,v in view.items()}})
    with (root/"metadata.csv").open("w",newline="",encoding="utf8") as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    files={}
    for name,records in (
        ("generation_metadata.jsonl",generation),
        ("source_lineage.jsonl",lineages),
    ):
        content="".join(json.dumps(rec,ensure_ascii=False,sort_keys=True)+"\n" for rec in records).encode()
        (root/name).write_bytes(content)
        files[name]=sha(content)
    (root/"generation_metadata_audit.json").write_text(
        json.dumps({"status":"PASS","artifacts_sha256":files}),encoding="utf8")
    (root/"collection_builder_187"/"COLLECTION_BUILDER_CATALOG.json").write_text(
        json.dumps({"schema":"compactfaces_collection_builder_catalog_v1",
                    "total_families":187,"total_images":935,
                    "core_count":120,"additional_optional_count":67,
                    "entries":catalog}),encoding="utf8")
    assert len(rows)==935 and len(generation)==935 and len(lineages)==187
    return root

def execute(root:Path,*,hash_png=True,builder=True,locale="en")->dict:
    notebook=json.loads((ROOT/"notebooks/compactfaces_kaggle_cpu_validation.ipynb").read_text(encoding="utf8"))
    namespace={"__name__":"__main__"}
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        for c in notebook["cells"]:
            if c["cell_type"]!="code":
                continue
            code="".join(c["source"])
            code=code.replace('MODE = "auto"','MODE = "full"')
            code=code.replace('EXPECTED_PNG_SIZE = 1024','EXPECTED_PNG_SIZE = 12')
            code=code.replace('assert EXPECTED_PNG_SIZE == 1024','assert EXPECTED_PNG_SIZE == 12')
            code=code.replace('DATASET_DIR = ""',f'DATASET_DIR = {str(root)!r}')
            code=code.replace('LANGUAGE = "en"',f'LANGUAGE = {locale!r}')
            code=code.replace('EXPORT_REPORT = True','EXPORT_REPORT = False')
            if not hash_png:
                code=code.replace('VERIFY_PNG_SHA256 = True','VERIFY_PNG_SHA256 = False')
            if not builder:
                code=code.replace('VERIFY_BUILDER = True','VERIFY_BUILDER = False')
            exec(compile(code,str(ROOT/"notebooks/compactfaces_kaggle_cpu_validation.ipynb"),"exec"),namespace)
    return namespace["report"]

def main()->None:
    with tempfile.TemporaryDirectory(prefix="compactfaces-fixture-") as temp:
        root=write_fixture(Path(temp))
        success=execute(root)
        assert success["verdict"]=="FULL_PASS",success
        assert success["verified_png_sha256_count"]==935,success
        assert success["verified_png_dimensions_count"]==935,success
        assert success["checks"]["png_dimensions"]=="PASS",success
        assert len(success["metadata_csv_sha256"])==64,success
        assert success["python_version"],success
        assert success["executed_at_utc"],success
        assert success["builder_jpeg_previews"]==935,success
        assert success["generation_provenance_verified"]==935,success
        assert success["source_lineage_verified"]==187,success
        print("PASS: FULL synthetic fixture (935 PNG hashes, 935 JPEG, 935 provenance, 187 lineages)")

        skipped=execute(root,hash_png=False,locale="vi")
        assert skipped["verdict"]=="PARTIAL",skipped
        assert skipped["verified_png_sha256_count"]==0,skipped
        assert skipped["checks"]["png_sha256"]=="SKIPPED_BY_OPTION",skipped
        assert "SKIPPED_BY_OPTION (0/935)" in skipped["note"],skipped
        print("PASS: PARTIAL without SHA256 reports exactly ZERO verified PNGs and honest VI note")

        no_builder=execute(root,builder=False)
        assert no_builder["verdict"]=="PARTIAL",no_builder
        assert no_builder["builder_jpeg_previews"]==0,no_builder
        assert "SKIPPED_BY_OPTION (0/935)" in no_builder["note"],no_builder
        print("PASS: PARTIAL without Builder reports exactly ZERO verified JPEGs and honest EN note")

        first=root/"core_600png/images/CORE_0000_SOURCE.png"
        original=first.read_bytes()
        Image.new("RGB",(13,12),(90,95,100)).save(first,format="PNG")
        try:
            execute(root)
        except ValueError as exc:
            assert "PNG dimensions mismatch" in str(exc),exc
        else:
            raise AssertionError("Wrong-size PNG unexpectedly accepted")
        print("PASS: invalid PNG IHDR dimensions rejected")
        first.write_bytes(original+b"tampered")
        try:
            execute(root)
        except ValueError as exc:
            assert "SHA256 mismatch" in str(exc),exc
        else:
            raise AssertionError("Tampered PNG unexpectedly accepted")
        print("PASS: tampered PNG rejected")
        # Restore a valid PNG from original fixture parameters for the required-column test.
        with (root/"metadata.csv").open(newline="",encoding="utf8") as f:
            metadata=list(csv.DictReader(f))
        for row in metadata:
            row.pop("file_name",None)
        with (root/"metadata.csv").open("w",newline="",encoding="utf8") as f:
            writer=csv.DictWriter(f,fieldnames=COLUMNS[1:])
            writer.writeheader()
            writer.writerows(metadata)
        try:
            execute(root)
        except ValueError as exc:
            assert "Missing metadata columns" in str(exc) and "file_name" in str(exc),exc
        else:
            raise AssertionError("Missing file_name column unexpectedly accepted")
        print("PASS: missing file_name fails early with actionable schema error")
    print("PASS: synthetic fixture regression suite; no released images accessed")

if __name__=="__main__":
    main()
