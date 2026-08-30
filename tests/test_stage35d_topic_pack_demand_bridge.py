from __future__ import annotations

from question_demand_contract import (
    attach_question_demand_contract,
    build_question_demand_contract,
)
from question_type_coverage_adapter import (
    _criteria_counts,
    _criteria_details,
)


QUESTION = (
    "화학 플랜트 반응기 압력 위험이 존재하고 기존 보호장치가 불충분하여 "
    "SIS 도입을 검토한다. 반응기 과압력 시나리오의 SIL 결정과정과 "
    "이를 만족하기 위한 SIS 아키텍처를 설명하시오."
)

EXPECTED_AXES = [
    "scenario_definition_and_cause",
    "existing_ipl_qualification",
    "required_rrf_and_target_sil",
    "demand_mode_and_sil_metric",
    "complete_sif_architecture",
    "quantitative_verification_dimension",
    "independence_ccf_hft_tradeoff",
    "proof_test_and_lifecycle",
]


def test_topic_pack_contract_exposes_exact_eight_axes() -> None:
    contract = build_question_demand_contract(QUESTION)
    assert contract["topic_pack_demand_axes_applied"] is True
    assert [row["requirement_id"] for row in contract["requirements"]] == EXPECTED_AXES
    assert contract["summary"]["requirement_count"] == 8
    assert contract["answer_text_dependency"] == "none"
    assert contract["score_effect"] == "semantic_guidance_only"


def test_unrelated_question_keeps_generic_contract() -> None:
    contract = build_question_demand_contract("PID 제어 원리를 설명하시오.")
    assert contract["topic_pack_demand_axes_applied"] is False
    assert contract["requirements"]
    assert contract["summary"]["requirement_count"] != 8


def test_attach_keeps_canonical_lens_and_eight_axes() -> None:
    result = {"parsed": {"question_type": "PRINCIPLE_INTERPRETATION"}}
    attached = attach_question_demand_contract(
        result,
        QUESTION,
        canonical_primary_lens="PRINCIPLE_INTERPRETATION",
    )
    contract = attached["question_demand_contract"]
    assert contract["primary_lens"] == "PRINCIPLE_INTERPRETATION"
    assert len(contract["requirements"]) == 8
    assert attached["parsed"]["question_demand_contract"] == contract


def _explicit_rows() -> list[dict[str, object]]:
    states = ["correct"] * 5 + ["wrong", "partial", "missing"]
    return [
        {
            "requirement_id": axis,
            "requirement_text": axis,
            "demand_state": state,
            "mentioned": state != "missing",
            "evidence": "fixture evidence" if state != "missing" else "",
        }
        for axis, state in zip(EXPECTED_AXES, states)
    ]


def test_summary_counts_prefer_explicit_eight_over_generic_seven() -> None:
    coverage = {
        "explicit_requirement_coverage": {"requirements": _explicit_rows()},
        "sub_criteria_coverage": [
            {"criterion": f"generic_{index}", "status": "present"}
            for index in range(7)
        ],
    }
    counts = _criteria_counts(coverage)
    assert counts == {
        "present": 5,
        "correct": 5,
        "partial": 1,
        "wrong": 1,
        "missing": 1,
        "total": 8,
    }


def test_summary_details_use_requirement_ids() -> None:
    coverage = {
        "explicit_requirement_coverage": {"requirements": _explicit_rows()},
        "sub_criteria_coverage": [],
    }
    details = _criteria_details(coverage)
    assert details["total"] == 8
    assert details["wrong_criteria"] == ["quantitative_verification_dimension"]
    assert details["partial_criteria"] == ["independence_ccf_hft_tradeoff"]
    assert details["missing_criteria"] == ["proof_test_and_lifecycle"]


def test_empty_explicit_falls_back_to_generic_rows() -> None:
    coverage = {
        "explicit_requirement_coverage": {"requirements": []},
        "sub_criteria_coverage": [
            {"criterion": "generic", "status": "present"}
        ],
    }
    counts = _criteria_counts(coverage)
    assert counts["total"] == 1
    assert counts["correct"] == 1


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    assert len(tests) == 6
    for name, test in tests:
        test()
        print(f"PASS {name}")
    print("STAGE35D_FOCUSED_TEST_RESULT=PASS")
    print(f"STAGE35D_FOCUSED_TEST_COUNT={len(tests)}")


if __name__ == "__main__":
    main()
