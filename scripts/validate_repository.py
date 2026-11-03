#!/usr/bin/env python3
"""CPU-only source, bilingual documentation and publication-boundary audit."""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
SWITCH="Language / Ngôn ngữ:"
BINARY_SUFFIX={".png",".jpg",".jpeg",".webp",".zip",".gguf",".safetensors",".pth",".pt",".ckpt"}
SKIP_EXTERNAL=("http://","https://","mailto:","data:","#","javascript:")
LINK_PATTERN=re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CANONICAL_DATASET_SLUG="compactfaces-synthetic-face-dataset"
# Split the retired slug so the validation script itself is not a false positive.
LEGACY_DATASET_SLUG="compactfaces-synthetic-face-" + "187-identities"
CANONICAL_DATASET_URL=("https://www.kaggle.com/datasets/dangkhoa2016/" + CANONICAL_DATASET_SLUG)
TEXT_SUFFIXES={".md", ".ipynb", ".json", ".py", ".js", ".html", ".yml", ".yaml", ".sh", ".txt"}

def check_dataset_slug_text(path, content):
    assert LEGACY_DATASET_SLUG not in content, f"Retired Kaggle dataset slug in {path}: use {CANONICAL_DATASET_SLUG}"

def verify_dataset_slug_consistency():
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in {".git", "__pycache__", ".venv", ".ipynb_checkpoints"} for part in p.parts):
            continue
        check_dataset_slug_text(p.relative_to(ROOT), p.read_text(encoding="utf8"))
    canonical_pages=("README.md", "README.vi.md", "docs/platforms.md", "docs/platforms.vi.md",
                     "docs/RELEASE_POLICY.md", "docs/RELEASE_POLICY.vi.md",
                     "docs/RELEASE_SYNC.md", "docs/RELEASE_SYNC.vi.md")
    for name in canonical_pages:
        assert CANONICAL_DATASET_URL in (ROOT/name).read_text(encoding="utf8"), (
            f"Missing canonical Kaggle URL in {name}: {CANONICAL_DATASET_URL}")

def verify_gallery_public_links():
    """Catch missing GitHub navigation and stale unpublished-link copy in website source."""
    website = ROOT / "website_src"
    github_url = "https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline"
    html = {name: (website / name).read_text(encoding="utf8")
            for name in ("index.html", "about.html", "contact.html")}
    for name, content in html.items():
        assert github_url in content, f"Missing GitHub repository link in {name}"
        assert 'target="_blank"' in content and 'rel="noopener noreferrer"' in content, name
        assert '<div class="footer-right">' in content and 'GitHub</a>' in content, name
        assert "No external link configured" not in content, f"Stale deployment copy in {name}"
        assert "after publication" not in content, f"Stale publication copy in {name}"
    assert 'id="githubLink"' in html["index.html"], "Missing GitHub source card on Index"
    assert 'id="sourceRepoLink"' in html["about.html"], "Missing GitHub source button on About"
    assert 'id="contactSourceLink"' in html["contact.html"], "Missing GitHub source block on Contact"
    dataset_targets = {
        "HuggingFace": "https://huggingface.co/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset",
        "Kaggle": "https://www.kaggle.com/datasets/dangkhoa2016/compactfaces-synthetic-face-dataset",
    }
    for page in ("about", "contact"):
        for platform, url in dataset_targets.items():
            assert f'id="{page}{platform}Link"' in html[page + ".html"], (page, platform)
            assert url in html[page + ".html"], (page, platform, "wrong dataset URL")
    app = (website / "app.js").read_text(encoding="utf8")
    pages = (website / "pages.js").read_text(encoding="utf8")
    for key in ('openRepository:"View source code"', 'openRepository:"Xem mã nguồn GitHub"'):
        assert key in app, f"Missing gallery bilingual source label: {key}"
    for key in ('openRepository:"View source on GitHub"', 'openRepository:"Xem mã nguồn trên GitHub"'):
        assert key in pages, f"Missing About/Contact bilingual source label: {key}"
    for name in ("about.html", "contact.html"):
        assert '<span data-i18n="openRepository">View source on GitHub</span>' in html[name], (
            f"Missing readable HTML fallback label in {name}")
        assert '<span data-i18n="openRepository">openRepository</span>' not in html[name], (
            f"Untranslated key exposed in {name}")
    for key in ('openHuggingFace:"View dataset on Hugging Face"','openHuggingFace:"Xem dataset trên Hugging Face"','openKaggle:"View dataset on Kaggle"','openKaggle:"Xem dataset trên Kaggle"'):
        assert key in pages, f"Missing About/Contact dataset translation: {key}"
    assert '["PUBLIC", "PUBLIC_GALLERY_PREVIEW"].includes(state.config.publication_status)' in app
    for text in ("Chưa cấu hình liên kết ngoài",
                 "Nút tải ngoài chỉ hoạt động",
                 "External download buttons are enabled only"):
        assert text not in app, f"Stale staging message: {text}"


def verify_gallery_translation_coverage():
    """Check every static HTML translation key against both EN and VI dictionaries."""
    website = ROOT / "website_src"
    for script_name, page_names in (
        ("app.js", ("index.html",)),
        ("pages.js", ("about.html", "contact.html")),
    ):
        js = (website / script_name).read_text(encoding="utf8")
        start = js.index("  en: {")
        middle = js.index("  vi: {", start)
        end = js.index("\n  }\n};", middle)
        key_pattern = re.compile(r'(?<![\w])([A-Za-z][\w]*):"')
        en_keys = set(key_pattern.findall(js[start:middle]))
        vi_keys = set(key_pattern.findall(js[middle:end]))
        for page_name in page_names:
            html = (website / page_name).read_text(encoding="utf8")
            keys = set(re.findall(r'data-i18n(?:-placeholder)?="([A-Za-z][\w]*)"', html))
            assert keys, f"No translation labels found in {page_name}"
            assert keys <= en_keys, f"Missing English translation in {page_name}: {keys - en_keys}"
            assert keys <= vi_keys, f"Missing Vietnamese translation in {page_name}: {keys - vi_keys}"
            leaked = re.search(
                r'data-i18n="([A-Za-z][\w]*)"[^>]*>\s*\1\s*<', html)
            assert not leaked, f"Literal i18n key appears in {page_name}: {leaked.group(1)}"


def verify_reader_facing_copy():
    """Block known provisional/ambiguous copy across all published docs and pages.

    Review notes about licensing, accurate test scope, and troubleshooting access
    are deliberately retained: those constraints are materially different.
    """
    retired = (
        ("request access if it is ", "private"),
        ("xin quyền nếu đang ở ", "chế độ riêng tư"),
        ("Cloning a private repository ", "requires GitHub access"),
        ("để clone repository Private ", "vẫn cần quyền truy cập GitHub"),
        ("Access depends on ", "dataset permissions"),
        ("Quyền truy cập tùy theo ", "từng nền tảng"),
        ("Quyền truy cập tùy theo ", "trạng thái chia sẻ"),
        ("Access depends on the service's ", "current sharing settings"),
        ("Private datasets require ", "access permission"),
        ("Dataset Private ", "cần có quyền"),
        ("<span data-i18n=\"openRepository\">", "openRepository</span>"),
    )
    candidates = (p for p in ROOT.rglob("*")
                  if p.is_file() and p.suffix.lower() in {".md", ".html", ".js", ".ipynb"})
    scanned = 0
    for path in candidates:
        if any(part in {".git", "__pycache__", ".venv", ".ipynb_checkpoints"} for part in path.parts):
            continue
        content = path.read_text(encoding="utf8")
        for first, second in retired:
            phrase = first + second
            assert phrase not in content, f"Retired or untranslated text in {path.relative_to(ROOT)}"
        scanned += 1
    print(f"PASS: {scanned} reader-facing Markdown/HTML/JS/notebook files checked for retired access and translation copy.")



def verify_public_document_copy():
    """Block internal development chronology in public-facing Markdown.

    Data lineage, model versioning and ordinary reproducibility notes are
    permitted; internal dates, release gates and development status are not.
    """
    patterns = {
        "internal execution date": re.compile(r"\b2026-(?:10|11)-[0-9]{2}\b|(?:29/10|01/11)/2026"),
        "internal chronology": re.compile(
            r"(?i)\b(?:development history|project evolution|historical snapshot|"
            r"historical fingerprint|historical binary|release gate|prepublication)\b"
        ),
        "internal Vietnamese status": re.compile(
            r"lịch sử (?:Git|phát triển|commit)|nghiệm thu nội bộ|"
            r"fingerprint lịch sử|bản ghi đồng bộ ngày|đã ghi nhận ngày|nghiệm thu|"
            r"bắt buộc trước khi công bố"
        ),
        "private-dataset instructions": re.compile(
            r"A private dataset requires access permission|Dataset private|"
            r"An unavailable dataset cannot be attached without permission|"
            r"(?:a private gallery|gallery private)", re.I
        ),
        "internal publication configuration": re.compile(
            r"PRIVATE_STAGING_ONLY|required for public release", re.I
        ),
    }
    count = 0
    for page in ROOT.rglob("*.md"):
        if any(part in {".git", "__pycache__", ".venv"} for part in page.parts):
            continue
        text = page.read_text(encoding="utf8")
        for name, pattern in patterns.items():
            match = pattern.search(text)
            assert match is None, (
                f"Public-document copy violation ({name}): {page.relative_to(ROOT)}"
                f" (near {match.group(0)!r})"
            )
        count += 1
    notebook_file = ROOT / "notebooks/compactfaces_kaggle_cpu_validation.ipynb"
    notebook = json.loads(notebook_file.read_text(encoding="utf8"))
    for cell_index, cell in enumerate(notebook["cells"]):
        source = "".join(cell["source"])
        for name, pattern in patterns.items():
            match = pattern.search(source)
            assert match is None, (
                f"Public notebook copy violation ({name}): "
                f"{notebook_file.relative_to(ROOT)}:cell{cell_index} "
                f"({match.group(0)!r})"
            )
    print(f"PASS: {count} Markdown documents and {len(notebook['cells'])} notebook cells checked for internal copy.")


def check_ci_badge(markdown: str, source: str) -> None:
    """Require the CI image badge rather than only a workflow text link."""
    url = "https://github.com/dangkhoa2016/CompactFaces-Synthetic-Face-Pipeline/actions/workflows/ci.yml"
    expected = f"[![CI]({url}/badge.svg?branch=main)]({url})"
    assert markdown.count(expected) == 1, f"Missing or duplicated CI image badge: {source}"


def verify():
    assert (ROOT/"LICENSE").is_file(), "Missing LICENSE"
    license_text=(ROOT/"LICENSE").read_text(encoding="utf8")
    assert "MIT License" in license_text
    assert "Đăng Khoa <i.am@dangkhoa.dev>" in license_text
    verify_dataset_slug_consistency()
    verify_gallery_public_links()
    verify_gallery_translation_coverage()
    verify_reader_facing_copy()
    verify_public_document_copy()

    docs=sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts and "__pycache__" not in p.parts)
    checked=set(docs)
    assert docs
    for p in docs:
        filename=p.name
        is_vi=filename.endswith(".vi.md")
        english=(p.with_name(filename[:-6]+".md") if is_vi else p)
        vietnamese=(p if is_vi else p.with_name(filename[:-3]+".vi.md"))
        counterpart=english if is_vi else vietnamese
        assert counterpart.is_file(), f"Missing bilingual partner: {p.relative_to(ROOT)} -> {counterpart}"
        content=p.read_text(encoding="utf8")
        assert SWITCH in "\n".join(content.splitlines()[:18]), f"Missing language switch: {p.relative_to(ROOT)}"
        assert counterpart.name in content, f"Language switch not linked: {p.relative_to(ROOT)}"
        for target in LINK_PATTERN.findall(content):
            target=target.strip().split(" ",1)[0]
            if not target or target.startswith(SKIP_EXTERNAL) or target.startswith("<"):
                continue
            path=target.split("#",1)[0].split("?",1)[0]
            if not path or path.startswith("/"):
                continue
            resolved=(p.parent/path).resolve()
            assert resolved.is_relative_to(ROOT), f"Markdown links outside repository: {p}: {target}"
            assert resolved.exists(), f"Broken doc link: {p.relative_to(ROOT)} -> {target}"
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or "__pycache__" in p.parts:
            continue
        assert p.suffix.lower() not in BINARY_SUFFIX, f"Disallowed model/image/archive: {p}"
    for script in ("verify_dataset.py","build_static_gallery.py","validate_repository.py", "validate_notebooks.py","audit_publication.py","model_assets.py","test_modal_workflow.py", "test_notebook_full_fixture.py"):
        assert (ROOT/"scripts"/script).is_file()
    for name in ("index.html","about.html","contact.html","app.js","pages.js"):
        assert (ROOT/"website_src"/name).is_file()
    config=json.loads((ROOT/"website_src/site-config.json").read_text(encoding="utf8"))
    assert config["publication_status"]=="LOCAL_PREVIEW"
    assert not any(config.get("downloads",{}).values())
    for name in ("index.html","about.html","contact.html"):
        assert "noindex" in (ROOT/"website_src"/name).read_text(encoding="utf8").lower()
    workflow=(ROOT/".github/workflows/ci.yml").read_text(encoding="utf8")
    assert "validate_repository.py" in workflow
    assert "audit_publication.py" in workflow
    assert "test_modal_workflow.py" in workflow
    assert "contents: read" in workflow
    assert (ROOT/".github/CODEOWNERS").is_file()
    for p in (ROOT/"README.md",ROOT/"README.vi.md"):
        s=p.read_text(encoding="utf8")
        check_ci_badge(s, p.name)
        assert "LICENSE" in s
        assert "prepublication" not in s.lower() and "pending" not in s.lower()
        assert "not uploaded" not in s.lower() and "future dataset" not in s.lower()
    assert "works without downloading" in (ROOT/"README.md").read_text(encoding="utf8")
    assert "không cần tải" in (ROOT/"README.vi.md").read_text(encoding="utf8").lower()
    print(f"PASS: {len(docs)} paired Markdown pages; verified relative links, code-only MIT, CI, local-preview config.")

if __name__=="__main__":
    verify()
