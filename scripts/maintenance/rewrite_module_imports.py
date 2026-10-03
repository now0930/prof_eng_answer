#!/usr/bin/env python3
"""Mechanical import and source-path rewrite for staged module moves.

Run after moving files with git mv. Arguments are old_name=new.dotted.module.
Only tracked Python files are changed; review the diff before committing.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAME = re.compile(r"[a-z][a-z0-9_]*\Z")
DOTTED = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\Z")


def rewrite(text: str, old: str, new: str) -> str:
    text = re.sub(
        rf"(?m)^(\s*)from {re.escape(old)}(?=\s+import\b)",
        rf"\1from {new}",
        text,
    )
    text = re.sub(
        rf"(?m)^(\s*)import {re.escape(old)}(?:\s+as\s+([A-Za-z_]\w*))?(?=\s*(?:#.*)?$)",
        lambda match: f"{match.group(1)}import {new} as {match.group(2) or old}",
        text,
    )
    for quote in ('"', "'"):
        text = text.replace(
            f"{quote}{old}.py{quote}",
            f"{quote}{new.replace('.', '/')}.py{quote}",
        )
        data_suffixes = "json|md|csv|txt|log|yaml|yml|sqlite3|db"
        text = re.sub(
            rf"{re.escape(quote)}{re.escape(old)}\.(?!({data_suffixes}){re.escape(quote)})",
            f"{quote}{new}.",
            text,
        )
    return text


def main(arguments: list[str]) -> int:
    if not arguments:
        raise SystemExit("usage: rewrite_module_imports.py old_name=new.module [...]")
    mappings: list[tuple[str, str]] = []
    for argument in arguments:
        old, separator, new = argument.partition("=")
        if not separator or not NAME.fullmatch(old) or not DOTTED.fullmatch(new):
            raise SystemExit(f"invalid module mapping: {argument}")
        mappings.append((old, new))

    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.py"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    changed: list[str] = []
    for raw_path in tracked.split(b"\0"):
        if not raw_path:
            continue
        relative = raw_path.decode("utf-8")
        path = ROOT / relative
        if not path.is_file():
            continue
        before = path.read_text(encoding="utf-8")
        after = before
        for old, new in mappings:
            after = rewrite(after, old, new)
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed.append(relative)
    print(f"REWRITTEN_FILES={len(changed)}")
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
