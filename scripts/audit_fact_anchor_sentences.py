#!/usr/bin/env python3
"""Read-only Fact Anchor style inventory: single sentence vs review candidates.

This tool does NOT shorten technical facts, change Topic IDs, mutate source,
write to generated banks, approve Facts, or alter grading. A one-sentence
Anchor may still contain multiple independently assessable engineering claims.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.fact_anchor_sentence_view import (
    project_fact_anchor_sentences,
)


def inventory() -> dict:
    view = project_fact_anchor_sentences()
    by_topic: dict[str, dict] = {}
    for row in view["rows"]:
        topic = row["owner_topic_id"]
        topic_row = by_topic.setdefault(topic, {
            "anchor_count": 0,
            "multi_sentence_count": 0,
            "long_statement_count": 0,
            "general_scoring_excluded_count": 0,
            "review_anchor_ids": [],
        })
        topic_row["anchor_count"] += 1
        if row["style_status"] == "MANUAL_SIMPLIFICATION_REQUIRED":
            topic_row["multi_sentence_count"] += 1
            topic_row["review_anchor_ids"].append(row["fact_id"])
        if len(row["statement"]) > 180:
            topic_row["long_statement_count"] += 1
        if row["general_scoring_excluded"]:
            topic_row["general_scoring_excluded_count"] += 1
    return {
        "schema_version": "fact_anchor_style_inventory.v1",
        "status": "AUDIT_ONLY",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "topic_count": len(by_topic),
        "anchor_count": view["anchor_count"],
        "multi_sentence_count": view["multi_sentence_count"],
        "long_statement_count": sum(
            item["long_statement_count"] for item in by_topic.values()
        ),
        "topic_breakdown": dict(sorted(by_topic.items())),
        "limitations": [
            "Sentence count uses punctuation heuristics, not semantic atomicity.",
            "A single sentence can include independently falsifiable claims.",
            "Necessary conditions, units, applicability and source evidence require individual review.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summary-only", action="store_true",
        help="Only show global counts; omit per-Topic review IDs.",
    )
    args = parser.parse_args(argv)
    result = inventory()
    if args.summary_only:
        result.pop("topic_breakdown", None)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
