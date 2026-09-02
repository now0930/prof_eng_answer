from __future__ import annotations

import copy

import gemini_grader
from question_demand_contract import (
    build_question_demand_contract,
    extract_explicit_question_scope,
)
from question_type_router import detect_question_type


QUESTION = (
    "화학 플랜트 반응기 압력 위험 존재, 기존 보호장치로 불충분 SIS 도입 검토 "
    "1) 반응기 과압력 시나리오의 SIL 결정과정 "
    "2) 이를 만족하기 위한 SIS 아키텍처 설명"
)
SUBMISSION_A = "문제: " + QUESTION + "=" * 80 + "1. 배경 정의 계산 공식 중심 답안"
SUBMISSION_B = (
    "[화학 플랜트] 반응기 과압력 위험 대응 SIS 도입 검토\n"
    "📌 문제 정의\n"
    "화학 플랜트 반응기에 과압력 위험이 존재하나 기존 보호장치만으로는 불충분함.\n"
    "* 반응기 과압력 시나리오에 대한 요구 SIL 결정 과정 설명\n"
    "* 이를 만족하기 위한 SIS 아키텍처 설명\n"
    "🔹 1. 배경 (Background)\n"
    "적용 평가 검사 효과를 반복한 답안 본문"
)
EXPECTED_IDS = [
    "scenario_definition_and_cause",
    "existing_ipl_qualification",
    "required_rrf_and_target_sil",
    "demand_mode_and_sil_metric",
    "complete_sif_architecture",
    "quantitative_verification_dimension",
    "independence_ccf_hft_tradeoff",
    "proof_test_and_lifecycle",
]


def valid_result():
    rows = [
        {
            "requirement_id": requirement_id,
            "requirement": requirement_id,
            "status": "present",
            "mentioned": True,
            "evidence": "fixture",
            "is_core": True,
        }
        for requirement_id in EXPECTED_IDS
    ]
    return {
        "parsed": {
            "question_type": "PRINCIPLE_INTERPRETATION",
            "question_type_coverage": {
                "question_type": "PRINCIPLE_INTERPRETATION",
                "explicit_requirement_coverage": {"requirements": rows},
            },
        }
    }


def invalid_result():
    return {
        "parsed": {
            "question_type_coverage": {
                "explicit_requirement_coverage": {
                    "requirements": [
                        {"requirement": "SIL 결정", "status": "present"},
                        {"requirement": "SIS 아키텍처", "status": "present"},
                    ]
                }
            }
        }
    }


def test_question_scope_excludes_answer_body():
    scoped_a = extract_explicit_question_scope(SUBMISSION_A)
    scoped_b = extract_explicit_question_scope(SUBMISSION_B)
    assert "배경 정의 계산" not in scoped_a
    assert "적용 평가 검사" not in scoped_b
    assert "SIL" in scoped_a and "SIS" in scoped_a
    assert "SIL" in scoped_b and "SIS" in scoped_b


def test_topic_contract_owns_eight_axes_and_canonical_lens():
    for submission in (SUBMISSION_A, SUBMISSION_B):
        contract = build_question_demand_contract(submission)
        assert [row["requirement_id"] for row in contract["requirements"]] == EXPECTED_IDS
        assert contract["primary_lens"] == "IMPLEMENTATION_EVALUATION"
        assert contract["primary_lens_source"] == "topic_pack_canonical_primary_lens"


def test_router_is_answer_independent_for_same_topic():
    result_a = detect_question_type(SUBMISSION_A)
    result_b = detect_question_type(SUBMISSION_B)
    assert result_a["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert result_b["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert result_a["canonical_owner"] == "topic_pack_question_demand_axes"
    assert result_b["canonical_owner"] == "topic_pack_question_demand_axes"


def test_projection_validator_rejects_two_freeform_rows():
    contract = build_question_demand_contract(SUBMISSION_A)
    assert not gemini_grader._stage35e2_projection_matches_contract(
        invalid_result(), contract
    )
    assert gemini_grader._stage35e2_projection_matches_contract(
        valid_result(), contract
    )


def test_projection_state_normalizer_repairs_schema_only_fields():
    contract = build_question_demand_contract(SUBMISSION_A)
    result = valid_result()
    rows = result["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    rows[0].pop("mentioned")
    rows[1]["status"] = "incorrect"
    rows[1]["mentioned"] = False
    assert not gemini_grader._stage35e2_projection_matches_contract(
        result, contract
    )
    normalized = gemini_grader._stage35e2_normalize_projection_state_fields(
        result
    )
    assert gemini_grader._stage35e2_projection_matches_contract(
        normalized, contract
    )
    normalized_rows = normalized["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    assert normalized_rows[0]["mentioned"] is True
    assert normalized_rows[1]["status"] == "wrong"
    assert normalized_rows[1]["mentioned"] is True


def test_projection_normalizer_restores_id_from_exact_contract_text_only():
    contract = build_question_demand_contract(SUBMISSION_A)
    result = valid_result()
    rows = result["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    for row, requirement in zip(rows, contract["requirements"]):
        row.pop("requirement_id")
        row["requirement"] = requirement["requirement_text"]
    normalized = gemini_grader._stage35e2_normalize_projection_state_fields(
        result,
        contract,
    )
    assert gemini_grader._stage35e2_projection_matches_contract(
        normalized, contract
    )
    rows[0]["requirement"] += " 임의 변경"
    unsafe = gemini_grader._stage35e2_normalize_projection_state_fields(
        result,
        contract,
    )
    unsafe_ids = unsafe["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    assert not unsafe_ids[0].get("requirement_id")

    id_in_requirement = valid_result()
    id_rows = id_in_requirement["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    for row in id_rows:
        row.pop("requirement_id")
    id_normalized = gemini_grader._stage35e2_normalize_projection_state_fields(
        id_in_requirement,
        contract,
    )
    assert gemini_grader._stage35e2_projection_matches_contract(
        id_normalized,
        contract,
    )

    with_generic_duplicates = valid_result()
    duplicate_rows = with_generic_duplicates["parsed"][
        "question_type_coverage"
    ]["explicit_requirement_coverage"]["requirements"]
    duplicate_rows[:0] = [
        {
            "requirement": "SIL 결정과정",
            "status": "partial",
            "mentioned": True,
        },
        {
            "requirement": "SIS 아키텍처",
            "status": "partial",
            "mentioned": True,
        },
    ]
    deduped = gemini_grader._stage35e2_normalize_projection_state_fields(
        with_generic_duplicates,
        contract,
    )
    assert gemini_grader._stage35e2_projection_matches_contract(
        deduped,
        contract,
    )

    label_result = valid_result()
    label_rows = label_result["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    for row, requirement in zip(label_rows, contract["requirements"]):
        row.pop("requirement_id")
        row["requirement"] = requirement["demand_label"]
    label_normalized = gemini_grader._stage35e2_normalize_projection_state_fields(
        label_result,
        contract,
    )
    assert gemini_grader._stage35e2_projection_matches_contract(
        label_normalized,
        contract,
    )


def test_semantic_wrapper_retries_once_and_accepts_exact_projection():
    original = gemini_grader._question_demand_previous_gemini_semantic_grade
    calls = []

    def fake(question_text, *args, **kwargs):
        calls.append(gemini_grader._stage35e2_projection_retry_contract.get())
        return invalid_result() if len(calls) == 1 else valid_result()

    gemini_grader._question_demand_previous_gemini_semantic_grade = fake
    try:
        result = gemini_grader.gemini_semantic_grade(SUBMISSION_A)
    finally:
        gemini_grader._question_demand_previous_gemini_semantic_grade = original
    assert len(calls) == 2
    assert calls[0] is None
    assert isinstance(calls[1], dict)
    validation = result["explicit_requirement_projection_validation"]
    assert validation["valid"] is True
    assert validation["provider_attempts"] == 2
    assert result["question_demand_contract"]["primary_lens"] == "IMPLEMENTATION_EVALUATION"


def test_semantic_wrapper_fails_closed_after_invalid_retry():
    original = gemini_grader._question_demand_previous_gemini_semantic_grade

    def fake(question_text, *args, **kwargs):
        return invalid_result()

    gemini_grader._question_demand_previous_gemini_semantic_grade = fake
    try:
        result = gemini_grader.gemini_semantic_grade(SUBMISSION_A)
    finally:
        gemini_grader._question_demand_previous_gemini_semantic_grade = original
    validation = result["explicit_requirement_projection_validation"]
    assert validation["valid"] is False
    assert validation["fail_closed"] is True
    assert validation["provider_attempts"] == 2
    rows = result["parsed"]["question_type_coverage"][
        "explicit_requirement_coverage"
    ]["requirements"]
    assert rows == []
    assert result["question_demand_contract"]["requirements"]


def main():
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    assert len(tests) == 8
    for name, test in tests:
        test()
        print(f"PASS {name}")
    print("STAGE35E2_FOCUSED_TEST_RESULT=PASS")
    print(f"STAGE35E2_FOCUSED_TEST_COUNT={len(tests)}")


if __name__ == "__main__":
    main()
