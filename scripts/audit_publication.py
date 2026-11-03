#!/usr/bin/env python3
"""Prevent accidentally publishing local runtime paths, internal campaign identifiers, and credential shapes.

This scans the CURRENT repository tree only. It does not rewrite Git commit history.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {".md", ".py", ".sh", ".json", ".ipynb", ".js", ".html", ".yml", ".yaml", ".toml"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
RULES = {
    "dated internal workflow identifier": re.compile(
        r"(?i)(?:mage-flow-stage-[a-z0-9]+-20[0-9]{6}|"
        r"stage-[a-z]-edit-turbo-20[0-9]{6})"
    ),
    "internal workspace or model mount": re.compile(
        r"(?i)/(?:vol/(?:runtime|models)|mnt/(?:workspace|systemDisk))/"
    ),
    "private release staging reference": re.compile(
        r"(?i)(?:private_distribution_staging|compact600-recovery-authority|"
        r"mage_flow_edit_turbo_stage_d_model_binding)"
    ),
    "embedded access key shape": re.compile(
        r"(?i)(?:ghp_[a-z0-9]{30,}|github_pat_[a-z0-9_]{40,}|"
        r"hf_[a-z0-9]{28,}|sk-[a-z0-9]{32,})"
    ),
}


def scan() -> int:
    findings = []
    examined = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(x in SKIP_DIRS for x in path.relative_to(ROOT).parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        examined += 1
        content = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(content.splitlines(), 1):
            for category, pattern in RULES.items():
                if pattern.search(line):
                    findings.append((path.relative_to(ROOT), line_no, category))
    if findings:
        for path, line_no, category in findings:
            print(f"FAIL {category}: {path}:{line_no}")
        return 1
    print(f"PASS: {examined} repository source/documentation files checked for publication-risk patterns.")
    print("Note: Git history and remote platform copies require a separate audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(scan())
