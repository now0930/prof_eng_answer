from grading.evidence.s7_answer_claim_shadow import (
    compare_claim_to_registry, extract_answer_claims, evaluate_answer_shadow,
)


def test_stage_a_needs_only_answer_and_does_not_emit_registry_ids():
    result = extract_answer_claims("제어밸브 데드밴드는 입력 방향을 반전할 때 출력 변화가 없는 범위다.")
    assert result["claims"][0]["extraction_status"] == "SURFACE_CLAIM_REVIEW_ONLY"
    assert "subject_id" not in result["claims"][0]
    assert "fact_id" not in result["claims"][0]
    assert result["score_admission"] == "DISABLED"


def test_stage_a_abstains_on_negation_quote_and_unrecognized_text():
    assert extract_answer_claims('"입력 방향을 반전하면 출력 변화가 없다"는 틀린 주장이다.') ["claims"][0]["extraction_status"] == "ABSTAIN"
    assert extract_answer_claims("관계없는 설명이다.")["claims"] == []


def test_conditions_are_never_inferred():
    claim = extract_answer_claims("개발 단계는 시험 단계에 대응한다.")["claims"]
    assert claim and claim[0]["conditions"] == []
    assert claim[0]["condition_status"] == "NOT_EXTRACTED"


def test_registry_ids_are_not_copied_and_match_is_not_asserted():
    claim = {"extraction_status": "SURFACE_CLAIM_REVIEW_ONLY", "surface_subject": "S"}
    registry = {"fact_id": "F", "review_status": "approved", "verification_status": "verified",
                "relation": {"subject": "registry-subject", "predicate": "maps", "object": "registry-object"}}
    result = compare_claim_to_registry(claim, registry)
    assert result["status"] == "NOT_ESTABLISHED"
    assert result["source_match_proven"] is False


def test_shadow_never_admits_score_without_expert_accuracy_labels():
    result = evaluate_answer_shadow("개발 단계는 시험 단계에 대응한다.", [])
    assert result["score_admission"] == "DISABLED"
    assert result["score_effect"] == "none"
    assert result["accuracy"] is None


def test_five_fact_surface_scope_and_fail_closed():
    examples = [
        "제어밸브 데드밴드는 입력 방향을 반전할 때 출력 변화가 없는 범위다.",
        "승인된 기준선은 변경 관리의 기준으로 사용한다.",
        "실효 불평형 면적은 압력 작용면과 밸브 구조에 따라 결정된다.",
        "개발 단계는 시험 단계에 대응한다.",
        "Nyquist 경로는 우반평면을 둘러싸며 L(s)는 복소평면에 사상된다.",
    ]
    for text in examples:
        result = extract_answer_claims(text)
        assert result["claims"]
        assert all(row["evidence_span"]["end"] <= len(text) for row in result["claims"])
        assert result["score_effect"] == "none"


def test_wrong_direction_and_partial_statement_are_not_promoted():
    partial = extract_answer_claims("개발 단계만 설명한다.")
    assert partial["claims"] == []
    wrong = extract_answer_claims("개발 단계는 시험 단계와 무관하다.")
    # Unsupported/negated surface patterns do not create a positive match.
    assert wrong["claims"][0]["extraction_status"] == "ABSTAIN"
