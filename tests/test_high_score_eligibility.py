from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from high_score_eligibility import apply_high_score_eligibility_cap
from grading_agents import finalize_grade_after_score_reconciliation


def _grade(*, total: float, complete: bool, field_evidence: bool) -> dict:
    layers = [
        {"layer_id": "A", "score": 2.7, "max": 3.0},
        {"layer_id": "B", "score": 5.5, "max": 6.0},
        {"layer_id": "C", "score": 7.0, "max": 8.0},
        {"layer_id": "D", "score": 5.2, "max": 6.0},
        {"layer_id": "E", "score": 1.6, "max": 2.0},
    ]
    rows = [{
        "is_core": True,
        "status": "correct" if complete else "partial",
        "correctness_status": "correct" if complete else "partial",
        "evidence": [{"quote_span": "quoted answer span"}] if complete else [],
    }]
    return {
        "total_score": total,
        "final_total_score": total,
        "breakdown": layers,
        "canonical_evaluation_ledger": {"rows": rows},
        "field_application_evidence": ([{
            "field_condition": "load changes", "engineering_judgement": "select margin",
            "verification_method": "site acceptance test",
        }] if field_evidence else []),
    }


def test_ineligible_high_score_is_capped_but_never_raised() -> None:
    result = apply_high_score_eligibility_cap(_grade(total=22.0, complete=False, field_evidence=False))
    assert result["total_score"] == 19.99
    assert result["final_total_score"] == 19.99
    assert result["high_score_eligibility"]["cap_applied"] is True


def test_complete_structured_evidence_does_not_change_high_score() -> None:
    result = apply_high_score_eligibility_cap(_grade(total=22.0, complete=True, field_evidence=True))
    assert result["total_score"] == 22.0
    assert result["high_score_eligibility"]["eligible"] is True


def test_sub_high_score_is_not_changed_by_eligibility_policy() -> None:
    result = apply_high_score_eligibility_cap(_grade(total=13.5, complete=False, field_evidence=False))
    assert result["total_score"] == 13.5
    assert result["high_score_eligibility"]["cap_applied"] is False


def test_cap_never_leaves_final_score_above_abcd_e_base_score() -> None:
    result = apply_high_score_eligibility_cap(_grade(total=22.0, complete=False, field_evidence=False))
    result["breakdown"] = [
        {"layer_id": "A", "score": 2.0, "max": 3.0},
        {"layer_id": "B", "score": 2.0, "max": 6.0},
        {"layer_id": "C", "score": 3.0, "max": 8.0},
        {"layer_id": "D", "score": 3.0, "max": 6.0},
        {"layer_id": "E", "score": 1.0, "max": 2.0},
    ]
    result["total_score"] = 22.0
    result = apply_high_score_eligibility_cap(result)
    assert result["total_score"] == 11.0
    assert result["total_score"] <= sum(row["score"] for row in result["breakdown"])


def test_post_reconciliation_boundary_reasserts_high_score_cap() -> None:
    grade = _grade(total=22.0, complete=False, field_evidence=False)
    result = finalize_grade_after_score_reconciliation(grade)
    assert result["total_score"] == 19.99
    assert result["final_total_score"] == 19.99
    assert result["high_score_eligibility"]["cap_applied"] is True


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"HIGH_SCORE_ELIGIBILITY_TESTS={len(tests)}_PASS")
