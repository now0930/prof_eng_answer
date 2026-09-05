from __future__ import annotations

import grading_agents as grading


def _semantic(*ids: str) -> dict:
    return {
        "parsed": {
            "question_demand_contract": {
                "requirements": [
                    {"requirement_id": demand_id} for demand_id in ids
                ],
            },
        },
    }


def _evidence(*ids: str) -> dict:
    return {
        "demands": [{"demand_id": demand_id} for demand_id in ids],
        "summary": {
            "covered_ratio": 1.0,
            "verified_ratio": 1.0,
            "mean_demand_level": 1.0,
        },
    }


def test_exact_native_scope_is_score_eligible() -> None:
    result = grading._stage7_native_projection_scope_validation(
        _evidence("D1", "D2"), _semantic("D1", "D2")
    )
    assert result["valid"] is True
    assert result["score_effect"] == "enabled"


def test_expanded_native_scope_is_diagnostic_only() -> None:
    result = grading._stage7_native_projection_scope_validation(
        _evidence("D1", "D2", "D3"), _semantic("D1", "D2")
    )
    assert result["valid"] is False
    assert result["score_effect"] == "diagnostic_only"


def test_out_of_scope_native_demands_cannot_overwrite_semantic_b() -> None:
    layers = [{"layer_id": "B", "score": 5.5}]
    result = grading._phase3_apply_question_demand_evidence_to_layer_scores(
        layers,
        _evidence("D1", "D2", "D3"),
        semantic_evaluation=_semantic("D1", "D2"),
    )
    assert result[0]["score"] == 5.5
    assert result[0]["native_projection_scope_validation"]["valid"] is False


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"NATIVE_PROJECTION_SCOPE_GUARD_TESTS={len(tests)}_PASS")
