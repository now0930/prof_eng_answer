from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from expert_accuracy_benchmark import (
    GOLD_VERSION,
    PREDICTION_VERSION,
    load_jsonl,
    measure_accuracy,
    prediction_from_grade,
    validate_gold_case,
)


def _gold(status: str = "reviewed") -> dict:
    result = {
        "version": GOLD_VERSION,
        "case_id": "case-1",
        "review_status": status,
        "labels": {
            "demands": [
                {"demand_id": "D1", "requirement": "정의", "core": True, "status": "CORRECT"},
                {"demand_id": "D2", "requirement": "검증", "core": True, "status": "WRONG"},
            ],
            "findings": [{"finding_id": "F1", "severity": "fatal"}],
            "score_range": {"min": 10.0, "max": 12.0},
            "flags": {
                "passing_score_allowed": False,
                "strong_verdict_allowed": False,
                "confidence_ceiling": "medium",
            },
        },
    }
    if status in {"reviewed", "adjudicated"}:
        result["review"] = {
            "reviewer": "test-reviewer",
            "method": "expert_review",
            "reviewed_at": "2026-09-02T05:24:26+09:00",
            "evidence_path": "tests/fixture-review.md",
        }
    return result


def _prediction() -> dict:
    return {
        "version": PREDICTION_VERSION,
        "case_id": "case-1",
        "demands": [
            {"demand_id": "D1", "status": "CORRECT"},
            {"demand_id": "D2", "status": "WRONG"},
        ],
        "findings": [{"finding_id": "F1", "severity": "fatal"}],
        "total_score": 11.0,
        "passing_score_allowed": False,
        "strong_verdict_allowed": False,
        "confidence": "medium",
    }


def test_perfect_prediction_has_perfect_metrics() -> None:
    report = measure_accuracy([_gold()], [_prediction()])
    assert report["status"] == "OK"
    assert report["demand_extraction"]["f1"] == 1.0
    assert report["demand_state_accuracy"] == 1.0
    assert report["major_finding_detection"]["f1"] == 1.0
    assert report["score_range_mae"] == 0.0
    assert report["false_pass_count"] == 0
    assert report["false_strong_count"] == 0
    assert report["confidence_ceiling_violation_count"] == 0


def test_draft_is_excluded_unless_explicitly_requested() -> None:
    excluded = measure_accuracy([_gold("draft")], [_prediction()])
    assert excluded["status"] == "NO_ELIGIBLE_CASES"
    assert excluded["demand_extraction"]["f1"] is None
    report = measure_accuracy([_gold("draft")], [_prediction()], include_draft=True)
    assert report["evaluated_case_count"] == 1


def test_false_positive_and_score_distance_are_reported() -> None:
    prediction = _prediction()
    prediction["demands"] = [{"demand_id": "D1", "status": "WRONG"}]
    prediction["findings"] = [{"finding_id": "F2", "severity": "major"}]
    prediction["total_score"] = 15.0
    prediction["passing_score_allowed"] = True
    prediction["strong_verdict_allowed"] = True
    prediction["confidence"] = "high"
    report = measure_accuracy([_gold()], [prediction])
    assert report["demand_extraction"]["recall"] == 0.5
    assert report["demand_state_accuracy"] == 0.0
    assert report["major_finding_detection"]["f1"] == 0.0
    assert report["score_range_mae"] == 3.0
    assert report["false_pass_count"] == 1
    assert report["false_strong_count"] == 1
    assert report["confidence_ceiling_violation_count"] == 1


def test_grade_adapter_preserves_claimed_present_as_prediction() -> None:
    grade = {
        "total_score": 14.0,
        "confidence": "high",
        "official_pass_met": False,
        "question_type_coverage": {
            "explicit_requirement_coverage": {
                "requirements": [
                    {"requirement_id": "D1", "status": "present"},
                    {"requirement_id": "D2", "status": "incorrect"},
                ]
            }
        },
        "question_type_coverage_summary": {"overall_coverage": "strong"},
        "logic_check_evaluation": {
            "findings": [{"rule_id": "F1", "severity": "fatal"}]
        },
    }
    prediction = prediction_from_grade("case-1", grade)
    assert prediction["demands"] == [
        {"demand_id": "D1", "requirement": "", "status": "CORRECT"},
        {"demand_id": "D2", "requirement": "", "status": "WRONG"},
    ]
    assert prediction["findings"] == [{"finding_id": "F1", "severity": "fatal"}]
    assert prediction["strong_verdict_allowed"] is True


def test_grade_adapter_prefers_canonical_ledger_over_legacy_coverage() -> None:
    grade = {
        "total_score": 12.0,
        "confidence": "medium",
        "strong_verdict_allowed": False,
        "canonical_evaluation_ledger": {
            "marker": "CANONICAL_EVALUATION_LEDGER_V1",
            "rows": [
                {"requirement_id": "D1", "status": "incorrect"},
                {"requirement_id": "D2", "status": "partial"},
            ],
        },
        "question_type_coverage": {
            "explicit_requirement_coverage": {
                "requirements": [
                    {"requirement_id": "D1", "status": "present"},
                    {"requirement_id": "D2", "status": "present"},
                ]
            }
        },
    }
    prediction = prediction_from_grade("case-1", grade)
    assert prediction["demands"] == [
        {"demand_id": "D1", "requirement": "", "status": "WRONG"},
        {"demand_id": "D2", "requirement": "", "status": "PARTIAL"},
    ]


def test_grade_adapter_keeps_unassessed_ledger_rows_as_unknown() -> None:
    grade = {
        "total_score": 12.0,
        "confidence": "low",
        "canonical_evaluation_ledger": {
            "marker": "CANONICAL_EVALUATION_LEDGER_V1",
            "rows": [
                {"requirement_id": "D1", "status": "unknown"},
                {"requirement_id": "D2", "status": "missing"},
            ],
        },
    }
    prediction = prediction_from_grade("case-1", grade)
    assert prediction["demands"] == [
        {"demand_id": "D1", "requirement": "", "status": "UNKNOWN"},
        {"demand_id": "D2", "requirement": "", "status": "MISSING"},
    ]


def test_semantically_equal_demand_text_matches_when_ids_differ() -> None:
    gold = _gold()
    gold["labels"]["demands"] = [{
        "demand_id": "EXPERT-D1",
        "requirement": "승인된 Baseline과 변경 영향분석을 제시한다.",
        "core": True,
        "status": "PARTIAL",
    }]
    prediction = _prediction()
    prediction["demands"] = [{
        "demand_id": "requirement_hash",
        "requirement": "변경 영향분석과 승인된 Baseline 제시",
        "status": "PARTIAL",
    }]
    prediction["findings"] = []
    gold["labels"]["findings"] = []
    report = measure_accuracy([gold], [prediction])
    assert report["demand_extraction"]["f1"] == 1.0
    assert report["demand_state_accuracy"] == 1.0


def test_committed_golden_seed_is_fully_reviewed() -> None:
    path = REPO / "calibration" / "expert_accuracy_golden.jsonl"
    rows = load_jsonl(path, validate_gold_case)
    assert len(rows) == 30
    assert {row["review_status"] for row in rows} == {"reviewed"}
    assert sum(row["review_status"] == "reviewed" for row in rows) == 30
    assert len({row["case_id"] for row in rows}) == len(rows)


def test_reviewed_status_requires_auditable_review_evidence() -> None:
    value = _gold()
    value.pop("review")
    try:
        validate_gold_case(value)
    except Exception as error:
        assert "review evidence" in str(error)
    else:
        raise AssertionError("reviewed case without evidence must fail")


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} expert accuracy benchmark checks")


if __name__ == "__main__":
    main()
