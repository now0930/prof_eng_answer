#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
CANDIDATES = ROOT / "reports/fact_anchor_support_term_rewrite_candidates_strict.csv"
OUT_CSV = ROOT / "reports/fact_anchor_support_term_rewrite_applied.csv"

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

    with CANDIDATES.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    safe = [r for r in rows if r.get("action") == "safe_rewrite"]

    mapping = defaultdict(dict)
    for r in safe:
        topic_id = r["topic_id"].strip()
        anchor_id = r["anchor_id"].strip()
        old = r["old_term"].strip()
        new = r["suggested_terms"].strip()
        if old and new and old != new:
            mapping[(topic_id, anchor_id)][old] = new

    data = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    topics = load_topics(data)

    applied = []

    for topic in topics:
        topic_id = str(topic.get("topic_id", "")).strip()
        for anchor in topic.get("anchors", []):
            if not isinstance(anchor, dict):
                continue

            anchor_id = str(anchor.get("id", "")).strip()
            repl = mapping.get((topic_id, anchor_id), {})
            if not repl:
                continue

            terms = anchor.get("support_terms", [])
            if not isinstance(terms, list):
                continue

            new_terms = []
            seen = set()

            for raw in terms:
                old = str(raw).strip()
                new = repl.get(old, old)

                if new in seen:
                    # rewrite 후 중복이 되면 하나만 유지
                    applied.append({
                        "topic_id": topic_id,
                        "anchor_id": anchor_id,
                        "old_term": old,
                        "new_term": new,
                        "action": "dedupe_after_rewrite",
                    })
                    continue

                seen.add(new)
                new_terms.append(new)

                if old != new:
                    applied.append({
                        "topic_id": topic_id,
                        "anchor_id": anchor_id,
                        "old_term": old,
                        "new_term": new,
                        "action": "rewrite",
                    })

            anchor["support_terms"] = new_terms

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["topic_id", "anchor_id", "old_term", "new_term", "action"],
        )
        writer.writeheader()
        writer.writerows(applied)

    print("safe candidates:", len(safe))
    print("applied:", len(applied))
    print("wrote:", OUT_CSV)

    for r in applied[:120]:
        print(f"- {r['topic_id']} / {r['anchor_id']} :: {r['old_term']} -> {r['new_term']} [{r['action']}]")

    if args.write:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = backup_dir / f"industrial_instrumentation_control.fact_anchors.before_safe_support_rewrite.{ts}.json"
        shutil.copy2(FACT_PATH, backup)
        save_json(FACT_PATH, data)
        print("backup:", backup)
        print("written:", FACT_PATH)
    else:
        print("DRY RUN only. Re-run with --write to apply.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
