import pytest

from grading.evidence.fact_shadow_comparison import summarize_shadow_cases


def shadow(complete=True, state="proved"):
    return {"requirements": [{"requirement_id": "r", "state": state, "fact_refs": ["f"]}],
            "complete": complete, "final_grade_allowed": False, "score_effect": "none"}


def test_only_complete_cases_are_compared():
    cases = [
        {"case_id": "same", "shadow": shadow(), "reference_fact_ids": ["f"]},
        {"case_id": "held", "shadow": shadow(False, "unresolved"), "reference_fact_ids": ["f"]},
        {"case_id": "different", "shadow": shadow(), "reference_fact_ids": ["g"]},
    ]
    result = summarize_shadow_cases(cases)
    assert (result["cases"], result["comparable"], result["agreements"], result["disagreements"]) == (3, 2, 1, 1)
    assert result["incomplete"] == 1


def test_shadow_cannot_carry_grade_authority():
    row = shadow()
    row["final_grade_allowed"] = True
    with pytest.raises(ValueError):
        summarize_shadow_cases([{"case_id": "x", "shadow": row, "reference_fact_ids": ["f"]}])
