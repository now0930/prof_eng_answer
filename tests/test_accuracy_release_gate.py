from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from accuracy_release_gate import evaluate_accuracy_release_gate
from expert_accuracy_benchmark import load_jsonl, validate_gold_case


def _policy() -> dict:
    return {
        "version": "expert_accuracy_release_policy_v1",
        "minimum_reviewed_cases": 4,
        "minimum_distinct_topics": 4,
        "required_question_types": [
            "PRINCIPLE_INTERPRETATION",
            "DIAGNOSIS_ACTION",
            "COMPARE_SELECTION",
            "IMPLEMENTATION_EVALUATION",
        ],
        "minimum_cases_per_question_type": 1,
        "minimum_major_finding_labels": 4,
        "minimum_demand_extraction_f1": 0.9,
        "minimum_demand_state_accuracy": 0.85,
        "minimum_major_finding_precision": 0.9,
        "minimum_major_finding_recall": 0.85,
        "maximum_score_range_mae": 1.0,
        "maximum_false_pass_count": 0,
        "maximum_false_strong_count": 0,
        "maximum_confidence_ceiling_violation_count": 0,
    }


def _gold(index: int, question_type: str) -> dict:
    return {
        "version": "expert_accuracy_case_v1",
        "case_id": f"case-{index}",
        "review_status": "reviewed",
        "review": {
            "reviewer": "test-reviewer",
            "method": "expert_review",
            "reviewed_at": "2026-09-02T05:24:26+09:00",
            "evidence_path": "tests/fixture-review.md",
        },
        "topic_ids": [f"topic-{index}"],
        "question_type": question_type,
        "labels": {
            "demands": [{
                "demand_id": f"D{index}",
                "requirement": "atomic demand",
                "core": True,
                "status": "WRONG",
            }],
            "findings": [{"finding_id": f"F{index}", "severity": "major"}],
            "score_range": {"min": 10.0, "max": 14.0},
            "flags": {
                "passing_score_allowed": False,
                "strong_verdict_allowed": False,
                "confidence_ceiling": "medium",
            },
        },
    }


def _report() -> dict:
    return {
        "evaluated_case_count": 4,
        "demand_extraction": {"f1": 0.95},
        "demand_state_accuracy": 0.9,
        "major_finding_detection": {"precision": 0.95, "recall": 0.9},
        "score_range_mae": 0.5,
        "false_pass_count": 0,
        "false_strong_count": 0,
        "confidence_ceiling_violation_count": 0,
    }


def _reviewed_cases() -> list[dict]:
    types = _policy()["required_question_types"]
    return [_gold(index, question_type) for index, question_type in enumerate(types, 1)]


def test_balanced_cross_topic_metrics_are_ready() -> None:
    result = evaluate_accuracy_release_gate(_report(), _reviewed_cases(), _policy())
    assert result["decision"] == "READY"
    assert result["blockers"] == []


def test_false_strong_and_low_recall_hold_release() -> None:
    report = _report()
    report["false_strong_count"] = 1
    report["major_finding_detection"]["recall"] = 0.5
    result = evaluate_accuracy_release_gate(report, _reviewed_cases(), _policy())
    codes = {row["code"] for row in result["blockers"]}
    assert result["decision"] == "HOLD"
    assert {"FALSE_STRONG_COUNT", "MAJOR_FINDING_RECALL"} <= codes


def test_complete_dataset_without_predictions_is_explicitly_hold() -> None:
    gold = load_jsonl(
        ROOT / "calibration" / "expert_accuracy_golden.jsonl",
        validate_gold_case,
    )
    policy = json.loads(
        (ROOT / "calibration" / "expert_accuracy_release_policy.json").read_text(
            encoding="utf-8"
        )
    )
    result = evaluate_accuracy_release_gate(
        {
            "evaluated_case_count": 0,
            "demand_extraction": {"f1": None},
            "demand_state_accuracy": None,
            "major_finding_detection": {"precision": None, "recall": None},
            "score_range_mae": None,
            "false_pass_count": 0,
            "false_strong_count": 0,
            "confidence_ceiling_violation_count": 0,
        },
        gold,
        policy,
    )
    assert result["decision"] == "HOLD"
    assert result["dataset"]["reviewed_case_count"] == 30
    assert any(row["code"] == "EVALUATED_CASE_COUNT" for row in result["blockers"])


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"ACCURACY_RELEASE_GATE_TESTS={len(tests)}_PASS")
