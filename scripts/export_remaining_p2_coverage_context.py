#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
MINOR_CSV = ROOT / "reports/model_answer_relationship_minor_analysis.csv"

OUT_MD = ROOT / "reports/model_answer_remaining_p2_coverage_context.md"
OUT_CSV = ROOT / "reports/model_answer_remaining_p2_coverage_context.csv"


def load_answers(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    if isinstance(data, dict):
        for key in ["answers", "model_answers", "items", "data"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]

        if "answer_id" in data or "id" in data:
            return [data]

    raise SystemExit("ERROR: unsupported model answer json structure")


def get_answer_id(answer: dict[str, Any]) -> str:
    for key in ["answer_id", "id", "model_answer_id"]:
        if answer.get(key):
            return str(answer[key]).strip()
    return ""


def lines_of(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return [value.strip()] if value.strip() else []

    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]

    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]

    return [str(value)]


def main() -> int:
    model_data = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    answers = load_answers(model_data)
    by_id = {get_answer_id(a): a for a in answers}

    with MINOR_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    targets = [
        r for r in rows
        if r.get("priority") == "P2"
        and r.get("action") in {
            "add_expected_terms_to_outline",
            "add_high_score_terms_to_outline",
        }
    ]

    answer_ids = []
    for r in targets:
        aid = r["answer_id"]
        if aid not in answer_ids:
            answer_ids.append(aid)

    md = []
    md.append("# Remaining P2 Coverage Context")
    md.append("")
    md.append(f"- issues: {len(targets)}")
    md.append(f"- answers: {len(answer_ids)}")
    md.append("")

    out_rows = []

    for aid in answer_ids:
        a = by_id.get(aid)
        if not a:
            continue

        issues = [r for r in targets if r["answer_id"] == aid]

        expected = lines_of(a.get("expected_structure"))
        high = lines_of(a.get("high_score_features"))
        outline = lines_of(a.get("model_answer_outline"))

        md.append(f"## {aid}")
        md.append("")
        md.append(f"- topic_id: `{a.get('topic_id', '')}`")
        md.append(f"- question_type: `{a.get('question_type', '')}`")
        md.append(f"- title: {a.get('title', a.get('name', ''))}")
        md.append("")
        md.append("### issues")
        md.append("")
        for r in issues:
            md.append(f"- `{r['action']}` / `{r['score']}`: {r['message']}")
        md.append("")
        md.append("### expected_structure")
        md.append("")
        for i, x in enumerate(expected, 1):
            md.append(f"{i}. {x}")
        md.append("")
        md.append("### high_score_features")
        md.append("")
        for i, x in enumerate(high, 1):
            md.append(f"{i}. {x}")
        md.append("")
        md.append("### model_answer_outline")
        md.append("")
        for i, x in enumerate(outline, 1):
            md.append(f"{i}. {x}")
        md.append("")

        out_rows.append({
            "answer_id": aid,
            "topic_id": str(a.get("topic_id", "")),
            "question_type": str(a.get("question_type", "")),
            "issues": " | ".join(f"{r['action']}:{r['score']}" for r in issues),
            "expected_structure": " || ".join(expected),
            "high_score_features": " || ".join(high),
            "model_answer_outline": " || ".join(outline),
        })

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "answer_id",
                "topic_id",
                "question_type",
                "issues",
                "expected_structure",
                "high_score_features",
                "model_answer_outline",
            ],
        )
        writer.writeheader()
        writer.writerows(out_rows)

    print("issues:", len(targets))
    print("answers:", len(answer_ids))
    print("wrote:", OUT_MD)
    print("wrote:", OUT_CSV)

    for aid in answer_ids:
        print("-", aid)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
