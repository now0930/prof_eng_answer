#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
OUT_CSV = ROOT / "reports/fact_anchor_removed_term_overlap.csv"

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

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    data = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    topics = load_topics(data)

    removed = []

    for topic in topics:
        topic_id = str(topic.get("topic_id", "")).strip()
        anchors = topic.get("anchors", [])
        if not isinstance(anchors, list):
            continue

        for anchor in anchors:
            if not isinstance(anchor, dict):
                continue

            anchor_id = str(anchor.get("id", "")).strip()
            core_terms = anchor.get("core_terms", [])
            support_terms = anchor.get("support_terms", [])

            if not isinstance(core_terms, list) or not isinstance(support_terms, list):
                continue

            core_set = {str(x).strip() for x in core_terms if str(x).strip()}
            new_support = []

            for raw in support_terms:
                term = str(raw).strip()
                if term and term in core_set:
                    removed.append({
                        "topic_id": topic_id,
                        "anchor_id": anchor_id,
                        "term": term,
                    })
                    continue
                new_support.append(raw)

            anchor["support_terms"] = new_support

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["topic_id", "anchor_id", "term"])
        writer.writeheader()
        writer.writerows(removed)

    print("removed overlap terms:", len(removed))
    print("wrote:", OUT_CSV)
    for r in removed[:80]:
        print(f"- {r['topic_id']} / {r['anchor_id']} :: {r['term']}")

    if args.write:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = backup_dir / f"industrial_instrumentation_control.fact_anchors.before_overlap_cleanup.{ts}.json"
        shutil.copy2(FACT_PATH, backup)
        save_json(FACT_PATH, data)
        print("backup:", backup)
        print("written:", FACT_PATH)
    else:
        print("DRY RUN only. Re-run with --write to apply.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
