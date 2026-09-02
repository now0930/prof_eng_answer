from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation_ledger import attach_canonical_evaluation_ledger
from evidence_calibration import apply_evidence_based_calibration
from question_demand_contract import build_question_demand_contract


CASES = (
    (
        "PID 제어의 동작 원리를 설명하고 현장 튜닝 절차를 제시하시오.",
        2,
        "PRINCIPLE_INTERPRETATION",
    ),
    (
        "열전대와 RTD의 특성을 비교하고 적용 조건에 따른 선정 기준을 설명하시오.",
        2,
        "COMPARE_SELECTION",
    ),
    (
        "제어밸브 캐비테이션의 원인을 진단하고 방지 대책을 제시하시오.",
        2,
        "DIAGNOSIS_ACTION",
    ),
    (
        "스마트 MCC 적용 방법과 도입 효과를 평가하시오.",
        1,
        "IMPLEMENTATION_EVALUATION",
    ),
)


def _grade(question: str, statuses: list[str]) -> dict:
    contract = build_question_demand_contract(question)
    rows = [
        {
            "requirement_id": requirement["requirement_id"],
            "requirement": requirement["requirement_text"],
            "status": status,
        }
        for requirement, status in zip(contract["requirements"], statuses)
    ]
    grade = {
        "total_score": 17.0,
        "confidence": "high",
        "verdict": "strong",
        "question_demand_contract": contract,
        "explicit_requirement_projection_validation": {"valid": True},
        "question_type_coverage": {
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {"requirements": rows},
        },
    }
    return apply_evidence_based_calibration(
        attach_canonical_evaluation_ledger(grade)
    )


def test_four_question_types_share_one_atomic_contract() -> None:
    for question, expected_count, expected_lens in CASES:
        contract = build_question_demand_contract(question)
        assert len(contract["requirements"]) == expected_count
        assert contract["primary_lens"] == expected_lens
        assert len({row["requirement_id"] for row in contract["requirements"]}) == expected_count


def test_partial_or_missing_blocks_strong_for_every_question_type() -> None:
    for question, expected_count, _lens in CASES:
        statuses = ["correct"] * expected_count
        statuses[-1] = "partial" if expected_count > 1 else "missing"
        result = _grade(question, statuses)
        assert result["strong_verdict_allowed"] is False
        assert result["verdict"] == "needs_correction"


def test_all_correct_exact_projection_can_keep_high_for_every_type() -> None:
    for question, expected_count, _lens in CASES:
        result = _grade(question, ["correct"] * expected_count)
        assert result["strong_verdict_allowed"] is True
        assert result["confidence"] == "high"


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"CROSS_TOPIC_ACCURACY_CONTRACT_TESTS={len(tests)}_PASS")
