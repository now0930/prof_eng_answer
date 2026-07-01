#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_CSV = ROOT / "reports/model_answer_relationship_validation.csv"
OUT_CSV = ROOT / "reports/model_answer_relationship_minor_analysis.csv"
OUT_MD = ROOT / "reports/model_answer_relationship_minor_analysis.md"


def pick(row: dict[str, str], *names: str) -> str:
    for name in names:
        if name in row and row[name] is not None:
            return str(row[name]).strip()
    return ""


def parse_score(row: dict[str, str]) -> float | None:
    raw = pick(row, "score", "coverage", "value")
    if raw:
        try:
            return float(raw)
        except ValueError:
            pass

    msg = pick(row, "message", "detail", "reason")

    m = re.search(r"score=([0-9.]+)", msg)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None

    m = re.search(r":\s*([0-9.]+)\s*$", msg)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None

    return None


def classify_action(check: str, message: str, score: float | None) -> tuple[str, str]:
    text = f"{check} {message}"

    if "전개 순서" in text:
        return "order_fix", "model_answer_outline 순서를 expected_structure 전개 순서에 맞춤"

    if "약하게 연결된 항목" in text:
        return "weak_outline_item_review", "model_answer_outline 항목 중 expected/high_score와 약한 항목을 삭제·이동·구체화"

    if "expected_structure 대비 model_answer_outline coverage 부족" in text:
        return "add_expected_terms_to_outline", "expected_structure 핵심 요구를 model_answer_outline에 반영"

    if "high_score_features 대비 model_answer_outline coverage 부족" in text:
        return "add_high_score_terms_to_outline", "high_score_features의 고득점 요소를 model_answer_outline에 반영"

    if "anchor" in text or "fact" in text:
        return "fact_alignment_review", "fact anchor와 model answer 연결성 검토"

    if score is not None and score <= 0.65:
        return "low_score_manual_review", "점수가 낮아 수동 검토 필요"

    return "advisory_review", "권고성 minor로 유지 가능성 있음"



# Reviewed after manual model_answer_outline repair.
# These are still MINOR in the relationship validator, but are no longer
# actionable P2 items because the outline already follows the expected
# answer structure or contains the requested high-score concepts.
REVIEWED_ADVISORY = {
    (
        "control_valve_positioner_ip_converter_PRINCIPLE_INTERPRETATION_v1",
        "add_expected_terms_to_outline",
    ),
    (
        "control_valve_body_trim_selection_COMPARE_SELECTION_v1",
        "add_high_score_terms_to_outline",
    ),
    (
        "adc_dac_signal_conversion_interface_PRINCIPLE_INTERPRETATION_v1",
        "order_fix",
    ),
    (
        "calibration_error_accuracy_precision_PROCEDURE_v1",
        "order_fix",
    ),
    (
        "cv_valve_flow_coefficient_CALC_DESIGN_v1",
        "order_fix",
    ),
}


def priority(action: str, score: float | None, message: str, answer_id: str = "") -> str:
    if (answer_id, action) in REVIEWED_ADVISORY:
        return "P3"

    if score is not None and score <= 0.60:
        return "P1"

    if action == "weak_outline_item_review":
        return "P2"

    if action == "order_fix":
        if score is not None and score <= 0.60:
            return "P1"
        return "P3"

    if score is not None and score < 0.70:
        return "P2"

    return "P3"


def main() -> int:
    if not IN_CSV.exists():
        raise SystemExit(
            f"ERROR: missing {IN_CSV}\n"
            "Run first: python3 scripts/validate_model_answer_relationships.py"
        )

    with IN_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    minors = []

    for r in rows:
        severity = pick(r, "severity", "level")

        if severity and severity.upper() != "MINOR":
            continue

        check = pick(r, "check", "check_name", "issue_type", "type", "category")
        answer_id = pick(r, "answer_id", "model_answer_id", "id")
        topic_id = pick(r, "topic_id", "topic")
        question_type = pick(r, "question_type", "type_profile")
        message = pick(r, "message", "detail", "reason")
        score = parse_score(r)

        action, action_reason = classify_action(check, message, score)
        prio = priority(action, score, message, answer_id)

        minors.append(
            {
                "priority": prio,
                "action": action,
                "topic_id": topic_id,
                "answer_id": answer_id,
                "question_type": question_type,
                "check": check,
                "score": "" if score is None else f"{score:.2f}",
                "message": message,
                "action_reason": action_reason,
            }
        )

    order = {"P1": 0, "P2": 1, "P3": 2}

    minors.sort(
        key=lambda r: (
            order.get(r["priority"], 9),
            r["action"],
            r["topic_id"],
            r["answer_id"],
        )
    )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "priority",
                "action",
                "topic_id",
                "answer_id",
                "question_type",
                "check",
                "score",
                "message",
                "action_reason",
            ],
        )
        writer.writeheader()
        writer.writerows(minors)

    by_priority = Counter(r["priority"] for r in minors)
    by_action = Counter(r["action"] for r in minors)
    by_check = Counter(r["check"] for r in minors)
    by_topic = Counter(r["topic_id"] for r in minors)

    lines = []
    lines.append("# Model Answer Relationship Minor Analysis")
    lines.append("")
    lines.append(f"- total minor: {len(minors)}")
    lines.append("")
    lines.append("## By priority")
    lines.append("")

    for k, v in by_priority.most_common():
        lines.append(f"- {k}: {v}")

    lines.append("")
    lines.append("## By action")
    lines.append("")

    for k, v in by_action.most_common():
        lines.append(f"- {k}: {v}")

    lines.append("")
    lines.append("## By check")
    lines.append("")

    for k, v in by_check.most_common():
        lines.append(f"- {k}: {v}")

    lines.append("")
    lines.append("## By topic")
    lines.append("")

    for k, v in by_topic.most_common():
        lines.append(f"- {k}: {v}")

    lines.append("")
    lines.append("## Items")
    lines.append("")

    for r in minors:
        lines.append(f"### {r['priority']} / {r['action']} / {r['answer_id']}")
        lines.append("")
        lines.append(f"- topic_id: `{r['topic_id']}`")
        lines.append(f"- question_type: `{r['question_type']}`")
        lines.append(f"- check: `{r['check']}`")
        lines.append(f"- score: `{r['score']}`")
        lines.append(f"- message: {r['message']}")
        lines.append(f"- suggested_action: {r['action_reason']}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("minor:", len(minors))
    print("wrote:", OUT_CSV)
    print("wrote:", OUT_MD)
    print()
    print("[by priority]")
    for k, v in by_priority.most_common():
        print(f"{k}: {v}")

    print()
    print("[by action]")
    for k, v in by_action.most_common():
        print(f"{k}: {v}")

    print()
    print("[by topic top]")
    for k, v in by_topic.most_common(20):
        print(f"{v:3} | {k}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
