from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation_ledger import attach_canonical_evaluation_ledger
from evidence_calibration import apply_evidence_based_calibration
from question_demand_contract import build_question_demand_contract


QUESTION = "PID 제어의 동작 원리를 설명하고 현장 튜닝 절차를 제시하시오."


def _grade(statuses=("correct", "correct"), *, projection=False) -> dict:
    contract = build_question_demand_contract(QUESTION)
    rows = [
        {
            "requirement_id": requirement["requirement_id"],
            "requirement": requirement["requirement_text"],
            "status": status,
        }
        for requirement, status in zip(contract["requirements"], statuses)
    ]
    grade = {
        "total_score": 17.2,
        "final_total_score": 17.2,
        "layer_scores": [{"layer": "C", "score": 6.0}],
        "confidence": "high",
        "grade_confidence": "high",
        "verdict": "strong",
        "question_demand_contract": contract,
        "question_type_coverage": {
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {"requirements": rows},
        },
        "question_type_coverage_summary": {"overall_coverage": "strong"},
    }
    if projection:
        grade["explicit_requirement_projection_validation"] = {"valid": True}
    return attach_canonical_evaluation_ledger(grade)


def test_semantic_only_without_exact_projection_caps_high_to_medium() -> None:
    result = apply_evidence_based_calibration(_grade())
    assert result["confidence"] == "medium"
    assert result["grade_confidence"] == "medium"
    assert result["confidence_ceiling"] == "medium"
    assert result["strong_verdict_allowed"] is False
    assert result["verdict"] == "needs_correction"
    assert result["evidence_based_calibration"]["strong_verdict_allowed"] is False


def test_exact_projection_and_all_correct_can_keep_high_and_strong() -> None:
    result = apply_evidence_based_calibration(_grade(projection=True))
    assert result["confidence"] == "high"
    assert result["confidence_ceiling"] == "high"
    assert result["verdict"] == "strong"
    assert result["evidence_based_calibration"]["strong_verdict_allowed"] is True


def test_semantically_verified_presence_projects_to_correct() -> None:
    result = apply_evidence_based_calibration(
        _grade(("present", "present"), projection=True)
    )
    assert result["canonical_evaluation_ledger"]["summary"][
        "status_counts"
    ]["correct"] == 2
    assert result["strong_verdict_allowed"] is True


def test_partial_requirement_blocks_strong_without_changing_score() -> None:
    grade = _grade(("correct", "partial"), projection=True)
    before = copy.deepcopy((grade["total_score"], grade["layer_scores"]))
    result = apply_evidence_based_calibration(grade)
    assert result["strong_verdict_allowed"] is False
    assert result["verdict"] == "needs_correction"
    assert result["question_type_coverage"]["overall_coverage"] == "needs_correction"
    assert (result["total_score"], result["layer_scores"]) == before


def test_incomplete_ledger_is_low_and_never_strong() -> None:
    grade = _grade(("correct",), projection=True)
    result = apply_evidence_based_calibration(grade)
    assert result["confidence"] == "low"
    assert result["confidence_ceiling"] == "low"
    assert result["strong_verdict_allowed"] is False
    assert result["verdict"] == "unknown"


def test_verified_fatal_caps_confidence_and_blocks_strong() -> None:
    grade = _grade(projection=True)
    requirement_id = grade["question_demand_contract"]["requirements"][0]["requirement_id"]
    grade["general_evidence_contract"] = {
        "defects": [{
            "defect_id": "fatal-1",
            "defect_type": "correctness_error",
            "severity": "fatal",
            "owner_layer": "C",
            "requirement_id": requirement_id,
        }]
    }
    grade = attach_canonical_evaluation_ledger(grade)
    result = apply_evidence_based_calibration(grade)
    assert result["confidence"] == "medium"
    assert result["strong_verdict_allowed"] is False
    assert result["evidence_based_calibration"]["fatal_error"] is True


def test_calibration_is_idempotent() -> None:
    once = apply_evidence_based_calibration(_grade())
    twice = apply_evidence_based_calibration(once)
    assert once == twice


def test_common_final_boundary_runs_calibration_after_ledger() -> None:
    import grading_agents

    result = grading_agents._stage17e5_finalize_pipeline_result(
        _grade(),
        {"question_answer_boundary": {"manual_review_required": False}},
    )
    assert result["canonical_evaluation_ledger"]["marker"] == (
        "CANONICAL_EVALUATION_LEDGER_V1"
    )
    assert result["evidence_based_calibration"]["marker"] == (
        "EVIDENCE_BASED_CALIBRATION_V1"
    )


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"EVIDENCE_BASED_CALIBRATION_TESTS={len(tests)}_PASS")
