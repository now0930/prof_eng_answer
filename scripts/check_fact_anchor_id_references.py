#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"

SEARCH_DIRS = [
    ROOT / "rubrics",
    ROOT / "scripts",
]

SKIP_PATHS = {
    FACT_PATH.resolve(),
}

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

def main() -> int:
    data = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    topics = load_topics(data)

    old_ids = []
    for topic in topics:
        for anchor in topic.get("anchors", []):
            if not isinstance(anchor, dict):
                continue
            aid = str(anchor.get("id", "")).strip()
            if aid and aid not in {"F1", "F2", "F3", "F4", "F5"}:
                old_ids.append((topic.get("topic_id", ""), aid))

    print("non-standard anchor ids:", len(old_ids))
    print()

    refs = []
    for base in SEARCH_DIRS:
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.resolve() in SKIP_PATHS:
                continue
            if path.suffix not in {".json", ".py", ".md", ".yml", ".yaml"}:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for topic_id, aid in old_ids:
                if aid in text:
                    refs.append((str(path.relative_to(ROOT)), topic_id, aid))

    print("external references:", len(refs))
    for path, topic_id, aid in refs[:200]:
        print(f"- {path} :: {topic_id} :: {aid}")

    if refs:
        print()
        print("WARNING: external references found. Do not rename ids until references are handled.")
        return 1

    print("OK: no external references found")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
