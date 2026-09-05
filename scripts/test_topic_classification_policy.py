#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"

ALLOWED_DIFFICULTIES = {
    "THEORY_CORE",
    "FIELD_APPLICATION",
    "DESIGN_EVALUATION",
}
ALLOWED_SELECTION_IMPORTANCE = {
    "CORE_MUST_PREPARE",
    "HIGH",
    "NORMAL",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    topic_dirs = sorted(path for path in PACK_ROOT.iterdir() if path.is_dir())
    assert topic_dirs, "no Topic Packs found"

    topics_by_difficulty: dict[str, set[str]] = {
        value: set() for value in ALLOWED_DIFFICULTIES
    }
    importance_counts: Counter[str] = Counter()

    for topic_dir in topic_dirs:
        path = topic_dir / "topic_importance.json"
        assert path.is_file(), f"missing classification source: {path}"
        importance = load_json(path)
        difficulty = importance.get("difficulty")
        selection_importance = importance.get("selection_importance")

        assert difficulty in ALLOWED_DIFFICULTIES, (
            topic_dir.name,
            difficulty,
        )
        assert selection_importance in ALLOWED_SELECTION_IMPORTANCE, (
            topic_dir.name,
            selection_importance,
        )
        topics_by_difficulty[difficulty].add(topic_dir.name)
        importance_counts[selection_importance] += 1

    classified = set().union(*topics_by_difficulty.values())
    actual = {path.name for path in topic_dirs}
    assert classified == actual
    assert sum(len(values) for values in topics_by_difficulty.values()) == len(actual)

    print(f"theory_topic_count={len(topics_by_difficulty['THEORY_CORE'])}")
    print(f"application_topic_count={len(topics_by_difficulty['FIELD_APPLICATION'])}")
    print(f"design_topic_count={len(topics_by_difficulty['DESIGN_EVALUATION'])}")
    print(f"classified_topic_count={len(classified)}")
    print(
        "selection_importance_values="
        + ",".join(sorted(importance_counts))
    )


if __name__ == "__main__":
    main()
