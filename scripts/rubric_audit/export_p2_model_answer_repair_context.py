#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
MINOR_CSV = ROOT / "reports/model_answer_relationship_minor_analysis.csv"

OUT_CSV = ROOT / "reports/model_answer_p2_repair_context.csv"
OUT_MD = ROOT / "reports/model_answer_p2_repair_context.md"


def load_answers(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    if isinstance(data, dict):
        for key in ["answers", "model_answers", "items", "data"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]

        if "answer_id" in data:
            return [data]

    raise SystemExit("ERROR: unsupported model answer json structure")


def get_answer_id(answer: dict[str, Any]) -> str:
    for key in ["answer_id", "id", "model_answer_id"]:
        if answer.get(key):
            return str(answer[key]).strip()
    return ""


def as_lines(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return [value.strip()] if value.strip() else []

    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str):
                if item.strip():
                    out.append(item.strip())
            elif isinstance(item, dict):
                # dict 항목이면 주요 필드를 사람이 보이게 펼친다.
                parts = []
                for key in ["section", "title", "name", "point", "description", "content"]:
                    if item.get(key):
                        parts.append(f"{key}={item[key]}")
                if parts:
                    out.append(" | ".join(parts))
                else:
                    out.append(json.dumps(item, ensure_ascii=False))
            else:
                out.append(str(item))
        return out

    if isinstance(value, dict):
        out = []
        for k, v in value.items():
            if isinstance(v, list):
                joined = " / ".join(str(x) for x in v)
                out.append(f"{k}: {joined}")
            else:
                out.append(f"{k}: {v}")
        return out

    return [str(value)]


def main() -> int:
    if not MODEL_PATH.exists():
        raise SystemExit(f"ERROR: missing {MODEL_PATH}")

    if not MINOR_CSV.exists():
        raise SystemExit(
            f"ERROR: missing {MINOR_CSV}\n"
            "Run first: python3 scripts/analyze_model_answer_relationship_minors.py"
        )

    model_data = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    answers = load_answers(model_data)
    by_id = {get_answer_id(a): a for a in answers}

    with MINOR_CSV.open(encoding="utf-8-sig", newline="") as f:
        minor_rows = list(csv.DictReader(f))

    p2_rows = [r for r in minor_rows if r.get("priority") == "P2"]

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in p2_rows:
        grouped[r["answer_id"]].append(r)

    out_rows = []

    lines = []
    lines.append("# P2 Model Answer Repair Context")
    lines.append("")
    lines.append(f"- P2 issues: {len(p2_rows)}")
    lines.append(f"- affected answers: {len(grouped)}")
    lines.append("")
    lines.append("## Repair items")
    lines.append("")

    for answer_id, issues in sorted(grouped.items()):
        answer = by_id.get(answer_id)

        if not answer:
            lines.append(f"## {answer_id}")
            lines.append("")
            lines.append("- ERROR: answer_id not found in model answer bank")
            lines.append("")
            continue

        topic_id = str(answer.get("topic_id", "")).strip()
        qtype = str(answer.get("question_type", "")).strip()
        title = str(answer.get("title", answer.get("name", ""))).strip()

        expected = as_lines(answer.get("expected_structure"))
        high = as_lines(answer.get("high_score_features"))
        outline = as_lines(answer.get("model_answer_outline"))

        lines.append(f"## {answer_id}")
        lines.append("")
        lines.append(f"- topic_id: `{topic_id}`")
        lines.append(f"- question_type: `{qtype}`")
        lines.append(f"- title: {title}")
        lines.append("")

        lines.append("### Issues")
        lines.append("")
        for issue in issues:
            lines.append(
                f"- `{issue.get('action', '')}` / score `{issue.get('score', '')}`: "
                f"{issue.get('message', '')}"
            )
        lines.append("")

        lines.append("### expected_structure")
        lines.append("")
        for i, item in enumerate(expected, 1):
            lines.append(f"{i}. {item}")
        lines.append("")

        lines.append("### high_score_features")
        lines.append("")
        for i, item in enumerate(high, 1):
            lines.append(f"{i}. {item}")
        lines.append("")

        lines.append("### model_answer_outline")
        lines.append("")
        for i, item in enumerate(outline, 1):
            lines.append(f"{i}. {item}")
        lines.append("")

        lines.append("### repair_note")
        lines.append("")
        lines.append("- TODO: expected/high_score에 있는데 outline에 약한 핵심어를 outline에 추가하거나 기존 항목을 구체화한다.")
        lines.append("- TODO: order_fix는 outline 순서를 expected_structure 순서에 맞춘다.")
        lines.append("")

        out_rows.append(
            {
                "answer_id": answer_id,
                "topic_id": topic_id,
                "question_type": qtype,
                "title": title,
                "issue_count": str(len(issues)),
                "actions": " | ".join(i.get("action", "") for i in issues),
                "scores": " | ".join(i.get("score", "") for i in issues),
                "messages": " | ".join(i.get("message", "") for i in issues),
                "expected_structure": " || ".join(expected),
                "high_score_features": " || ".join(high),
                "model_answer_outline": " || ".join(outline),
                "repair_plan": "",
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "answer_id",
                "topic_id",
                "question_type",
                "title",
                "issue_count",
                "actions",
                "scores",
                "messages",
                "expected_structure",
                "high_score_features",
                "model_answer_outline",
                "repair_plan",
            ],
        )
        writer.writeheader()
        writer.writerows(out_rows)

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("P2 issues:", len(p2_rows))
    print("affected answers:", len(grouped))
    print("wrote:", OUT_CSV)
    print("wrote:", OUT_MD)

    print()
    print("[affected answers]")
    for r in out_rows:
        print(f"- {r['issue_count']} | {r['answer_id']} | {r['actions']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
