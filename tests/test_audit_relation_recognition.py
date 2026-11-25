import pytest

from scripts.audit_relation_recognition import audit_relation_recognition


TOPIC = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
QUESTION = "Verification과 Validation의 차이와 적용방법을 설명하시오."
REQUIREMENT = "sw04_verification_definition"
ASSERTION = "Verification은 명세와 설계기준을 확인한다."
DENIAL = "Verification은 명세와 설계기준을 확인하지 않는다."


@pytest.mark.parametrize(("answer", "status"), [
    (ASSERTION, "CONFIRMED_RELATION"),
    (DENIAL, "CONFIRMED_CONTRADICTION"),
    ("Verification, 명세 적합, 확인.", "RECOGNITION_UNCERTAIN"),
    (f"“{ASSERTION}”", "RECOGNITION_UNCERTAIN"),
    (f"{ASSERTION} {DENIAL}", "RECOGNITION_UNCERTAIN"),
    (f"전제가 맞는 경우 {ASSERTION}", "RECOGNITION_UNCERTAIN"),
    ("  ", "CONTENT_INSUFFICIENT"),
])
def test_existing_machine_contract_audit(answer, status):
    result = audit_relation_recognition(
        question_text=QUESTION, answer_text=answer, topic_id=TOPIC, requirement_id=REQUIREMENT,
    )
    assert result["status"] == status
    assert result["score_effect"] == "none"
    if status == "CONFIRMED_RELATION":
        assert result["evidence_spans"] == [{"start": 0, "end": len(answer)}]
    if answer in {"  ", "Verification, 명세 적합, 확인."}:
        assert result["evidence_spans"] == []


def test_audit_uses_existing_scope_for_other_requirement_in_topic():
    result = audit_relation_recognition(
        question_text=QUESTION, answer_text=ASSERTION, topic_id=TOPIC, requirement_id="sw04_unit_test",
    )
    assert result["status"] == "RECOGNITION_UNCERTAIN"
    assert result["reason"] == "OUTSIDE_QUESTION_SCOPE"


def test_unresolved_contradictory_span_blocks_positive_audit_candidate():
    topic = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
    result = audit_relation_recognition(
        question_text="MC/DC의 개념, 목적과 충족조건을 설명하시오.",
        answer_text=(
            "100% MC/DC는 전체 SIL 달성을 단독으로 보장하지 않는다.\n"
            "100% MC/DC는 전체 SIL 달성을 단독으로 보장한다."
        ),
        topic_id=topic,
        requirement_id="mcdc_one_hundred_percent_limit",
    )
    assert result["status"] == "RECOGNITION_UNCERTAIN"
    assert result["reason"] == "CONDITIONAL_OR_MIXED_EVIDENCE"
    assert result["score_effect"] == "none"


def test_later_corrected_relation_supersedes_matching_unresolved_span():
    topic = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
    result = audit_relation_recognition(
        question_text="MC/DC의 개념, 목적과 충족조건을 설명하시오.",
        answer_text=(
            "100% MC/DC는 전체 SIL 달성을 단독으로 보장한다."
            "라는 설명은 잘못이다. 실제로는 100% MC/DC는 전체 SIL 달성을 "
            "단독으로 보장하지 않는다."
        ),
        topic_id=topic,
        requirement_id="mcdc_one_hundred_percent_limit",
    )
    assert result["status"] == "CONFIRMED_RELATION"
    assert result["score_effect"] == "none"


def test_unresolved_unrecognized_second_assertion_blocks_first_relation():
    result = audit_relation_recognition(
        question_text=QUESTION,
        answer_text=(
            f"{ASSERTION}\n"
            "명세 적합성 확인은 Verification의 목적이 아니다."
        ),
        topic_id=TOPIC,
        requirement_id=REQUIREMENT,
    )
    assert result["status"] == "RECOGNITION_UNCERTAIN"
    assert result["reason"] == "UNRESOLVED_EXTRACTION_SPAN"
    assert result["score_effect"] == "none"


def test_explicitly_rejected_relation_followed_by_same_fact_correction_is_supported():
    result = audit_relation_recognition(
        question_text="유량과 유속의 정의 및 단면 평균유속, 체적유량 관계를 설명하시오.",
        answer_text=(
            "체적유량은 단면적과 단면 평균유속의 곱이 아니다.라는 설명은 잘못이다. "
            "실제로는 체적유량은 단면적과 단면 평균유속의 곱이다."
        ),
        topic_id="flow_measurement_meter_principles_velocity_selection",
        requirement_id="flow_volumetric_rate_area_integral",
    )
    assert result["status"] == "CONFIRMED_RELATION"
    assert result["evidence_spans"] == [{"start": 39, "end": 69}]


def test_unrejected_opposite_relation_remains_mixed_and_uncertain():
    result = audit_relation_recognition(
        question_text="유량과 유속의 정의 및 단면 평균유속, 체적유량 관계를 설명하시오.",
        answer_text=(
            "체적유량은 단면적과 단면 평균유속의 곱이다.\n"
            "체적유량은 단면적과 단면 평균유속의 곱이 아니다."
        ),
        topic_id="flow_measurement_meter_principles_velocity_selection",
        requirement_id="flow_volumetric_rate_area_integral",
    )
    assert result["status"] == "RECOGNITION_UNCERTAIN"


def test_required_uniform_density_condition_must_be_present_and_bound():
    question = "체적유량과 질량유량의 관계 및 밀도 영향을 설명하시오."
    common = {
        "question_text": question,
        "topic_id": "flow_measurement_meter_principles_velocity_selection",
        "requirement_id": "flow_mass_rate_density_relation",
    }
    correct = audit_relation_recognition(
        **common,
        answer_text="밀도가 균일한 조건에서 질량유량은 밀도와 체적유량의 곱이다.",
    )
    omitted = audit_relation_recognition(
        **common,
        answer_text="질량유량은 밀도와 체적유량의 곱이다.",
    )
    assert correct["status"] == "CONFIRMED_RELATION"
    assert omitted["status"] == "RECOGNITION_UNCERTAIN"


def test_rrf_relation_does_not_require_repeating_scenario_scope_in_answer():
    result = audit_relation_recognition(
        question_text="LOPA의 계산 절차와 residual frequency 및 RRF 산정방법을 설명하시오.",
        answer_text="요구 RRF는 residual frequency를 tolerable frequency로 나눈 값이다.",
        topic_id="hazop_lopa_ipl_risk_reduction_sil_target_allocation",
        requirement_id="hazop_lopa_required_rrf",
    )
    assert result["status"] == "CONFIRMED_RELATION"
    assert result["score_effect"] == "none"


def test_corrected_followup_can_inherit_only_the_explicit_rejected_claim_subject():
    answer = (
        "Verification이 명세 적합성을 확인하지 않는다는 주장은 틀리다. "
        "실제로 명세 적합성을 확인한다."
    )
    result = audit_relation_recognition(
        question_text=QUESTION,
        answer_text=answer,
        topic_id=TOPIC,
        requirement_id=REQUIREMENT,
    )
    assert result["status"] == "CONFIRMED_RELATION"
    assert result["evidence_spans"] == [{"start": 40, "end": len(answer)}]


def test_structured_claim_condition_not_present_in_source_is_unresolved():
    import json
    from pathlib import Path

    from reports.run_p2b_relation_diagnostic_20261125 import compare_structured

    cases = json.loads(
        (Path(__file__).resolve().parents[1] / "reports/p2b_relation_cases_20261125.json")
        .read_text(encoding="utf-8")
    )
    row = next(
        item for item in cases["structured"]
        if item["case_id"] == "hazop_lopa_required_rrf/condition_other"
    )
    result = compare_structured(row)
    assert result["observed"] == "RECOGNITION_UNCERTAIN"
    assert result["ungrounded_claim_conditions"] == ["different_condition"]


def test_generalization_probe_never_supports_a_non_support_provisional_case():
    import json
    from pathlib import Path

    probe = json.loads(
        (Path(__file__).resolve().parents[1] / "reports/p2b_generalization_cases_20261125.json")
        .read_text(encoding="utf-8")
    )
    assert len(probe["cases"]) == 36
    for case in probe["cases"]:
        result = audit_relation_recognition(
            question_text=case["question"],
            answer_text=case["answer"],
            topic_id=case["topic_id"],
            requirement_id=case["requirement_id"],
        )
        assert result["status"] != "EXECUTION_ERROR"
        if case["expected_technical_subrelation"] != "CONFIRMED_RELATION":
            assert result["status"] != "CONFIRMED_RELATION", case["case_id"]
        if case["expected_technical_subrelation"] == "CONFIRMED_RELATION":
            assert result["status"] != "CONFIRMED_CONTRADICTION", case["case_id"]
