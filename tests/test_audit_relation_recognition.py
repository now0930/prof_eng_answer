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
    assert result["reason"] == "UNRESOLVED_EXTRACTION_SPAN"
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
