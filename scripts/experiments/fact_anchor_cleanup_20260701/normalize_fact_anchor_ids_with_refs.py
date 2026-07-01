#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
OUT_CSV = ROOT / "reports/fact_anchor_id_normalization_with_refs.csv"

SEARCH_DIRS = [
    ROOT / "rubrics",
    ROOT / "scripts",
]

TEXT_SUFFIXES = {".json", ".py", ".md", ".yml", ".yaml"}

def load_topics(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ["topics", "fact_anchors", "items", "data"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        if "topic_id" in data and "anchors" in data:
            return [data]
    raise SystemExit("ERROR: unsupported fact anchor json structure")

def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def token_replace(text: str, old: str, new: str) -> tuple[str, int]:
    # id가 긴 snake_case인 경우도, F1 같은 짧은 id도 독립 token일 때만 교체한다.
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])")
    return pattern.subn(new, text)

def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for base in SEARCH_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.resolve() == FACT_PATH.resolve():
                continue
            if path.suffix not in TEXT_SUFFIXES:
                continue
            files.append(path)
    return sorted(files)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    data = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    topics = load_topics(data)

    mappings: list[dict[str, str]] = []

    for topic in topics:
        topic_id = str(topic.get("topic_id", "")).strip()
        anchors = topic.get("anchors", [])
        if not isinstance(anchors, list):
            continue

        for idx, anchor in enumerate(anchors, 1):
            if not isinstance(anchor, dict):
                continue

            old_id = str(anchor.get("id", "")).strip()
            new_id = f"F{idx}"

            if old_id and old_id != new_id:
                mappings.append({
                    "topic_id": topic_id,
                    "index": str(idx),
                    "old_id": old_id,
                    "new_id": new_id,
                    "name": str(anchor.get("name", "")),
                    "external_files": "",
                    "external_replacements": "0",
                })

    print("id mappings:", len(mappings))

    text_files = iter_text_files()
    file_updates: dict[Path, str] = {}
    ref_counts: dict[str, list[str]] = {}

    for path in text_files:
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = original
        file_changed = False

        for m in mappings:
            old = m["old_id"]
            new = m["new_id"]

            updated2, count = token_replace(updated, old, new)
            if count:
                file_changed = True
                updated = updated2
                ref_counts.setdefault(old, []).append(f"{path.relative_to(ROOT)}:{count}")

        if file_changed:
            file_updates[path] = updated

    for m in mappings:
        refs = ref_counts.get(m["old_id"], [])
        m["external_files"] = "; ".join(refs)
        m["external_replacements"] = str(sum(int(x.rsplit(":", 1)[1]) for x in refs) if refs else 0)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "topic_id",
                "index",
                "old_id",
                "new_id",
                "name",
                "external_files",
                "external_replacements",
            ],
        )
        writer.writeheader()
        writer.writerows(mappings)

    print("external files to update:", len(file_updates))
    for path in sorted(file_updates):
        print("-", path.relative_to(ROOT))

    print("wrote:", OUT_CSV)

    for m in mappings[:120]:
        suffix = f" | refs={m['external_files']}" if m["external_files"] else ""
        print(f"- {m['topic_id']} / {m['old_id']} -> {m['new_id']}{suffix}")

    if not args.write:
        print("DRY RUN only. Re-run with --write to apply.")
        return 0

    backup_dir = ROOT / "backups"
    backup_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    fact_backup = backup_dir / f"industrial_instrumentation_control.fact_anchors.before_id_normalization_with_refs.{ts}.json"
    shutil.copy2(FACT_PATH, fact_backup)

    for path in sorted(file_updates):
        backup = backup_dir / f"{path.name}.before_fact_anchor_id_refs.{ts}.bak"
        shutil.copy2(path, backup)
        path.write_text(file_updates[path], encoding="utf-8")
        print("updated ref file:", path.relative_to(ROOT), "| backup:", backup.relative_to(ROOT))

    # main fact anchor id 변경
    for topic in topics:
        anchors = topic.get("anchors", [])
        if not isinstance(anchors, list):
            continue
        for idx, anchor in enumerate(anchors, 1):
            if isinstance(anchor, dict):
                anchor["id"] = f"F{idx}"

    save_json(FACT_PATH, data)
    print("backup:", fact_backup)
    print("written:", FACT_PATH)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
