#!/usr/bin/env python3
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from difficulty_strategy import (
    classify_question_difficulty,
    evaluate_exam_selection,
    load_difficulty_profiles,
    load_exam_selection_policy,
    load_topic_importance,
)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    profiles = load_difficulty_profiles()
    topics = load_topic_importance()
    exam = load_exam_selection_policy()

    assert_true("profiles" in profiles, "difficulty profiles missing profiles")
    assert_true("THEORY_CORE" in profiles["profiles"], "THEORY_CORE profile missing")
    assert_true("topics" in topics and topics["topics"], "topic importance topics missing")
    assert_true("difficulty_score_bands" in exam, "exam selection score bands missing")

    q1 = classify_question_difficulty("2차 시스템의 감쇠비에 따른 응답특성을 설명하시오.")
    assert_true(q1["difficulty"] == "THEORY_CORE", "2차 시스템 should be THEORY_CORE")
    assert_true(q1["selection_importance"] == "CORE_MUST_PREPARE", "2차 시스템 should be CORE_MUST_PREPARE")

    q2 = classify_question_difficulty("Cv(Valve Flow Coefficient)를 설명하시오.")
    assert_true(q2["difficulty"] == "FIELD_APPLICATION", "Cv should be FIELD_APPLICATION")

    questions = [
        "스마트팩토리의 개념과 구성요소를 설명하시오.",
        "2차 시스템의 감쇠비에 따른 응답특성을 설명하시오.",
        "RTD와 열전대를 비교하시오.",
        "밸브 Cv를 설명하시오.",
        "방폭 등급을 설명하시오.",
        "PLC와 DCS를 비교하시오."
    ]

    ev = evaluate_exam_selection(questions, [1, 3, 4, 6])
    assert_true(ev["omitted_core_must_prepare_count"] >= 1, "omitted core topic should be detected")
    assert_true(ev["strategy_grade"] in {"high_risk", "medium_risk"}, "strategy should have risk")

    ev2 = evaluate_exam_selection(questions, [2, 3, 4, 6], expected_scores={2: 8})
    assert_true(any(r["rule_id"] == "theory_selected_but_floor_not_met" for r in ev2["risks"]), "below-floor theory risk missing")

    print("VALID")
    print("profiles:", ", ".join(profiles["profiles"].keys()))
    print("topics:", len(topics["topics"]))
    print("sample_2nd_order:", json.dumps(q1, ensure_ascii=False))
    print("sample_exam_strategy:", ev["strategy_grade"])


if __name__ == "__main__":
    main()
