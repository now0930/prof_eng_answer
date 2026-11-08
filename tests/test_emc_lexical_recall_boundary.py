"""EMC canonical-only boundary: unrelated words cannot recover positive credit."""

from unittest.mock import patch

from grading.evidence import fact_anchor_evidence_adapter as adapter
from grading.evidence.fact_anchor_evidence_adapter import (
    EMC_CANONICAL_ONLY_REQUIREMENTS,
    EMC_CANONICAL_ONLY_TOPIC,
    _lexical_recall_supported,
    augment_requirement_evaluation,
)


def _canonical(topic, requirement_id, status="MISSING"):
    return {
        "owner_topic_id": topic,
        "requirement_id": requirement_id,
        "status": status,
        "evidence_mode": "canonical_claim",
        "matched_fact_ids": ["proper_fact"] if status == "SATISFIED" else [],
    }


def _lexical(topic, requirement_id):
    return {
        "owner_topic_id": topic,
        "requirement_id": requirement_id,
        "status": "SATISFIED",
        "importance": "core",
        "source_span": {"start": 0, "end": 27},
        "evidence_text": "UPS를 사용하면 모든 EMC 문제가 해결된다.",
        "matched_terms": ["ground loop", "ups", "emc"],
        "concept_token_coverage": 0.05,
    }


def test_four_emc_canonical_only_requirements_never_get_false_lexical_credit():
    assert len(EMC_CANONICAL_ONLY_REQUIREMENTS) == 4
    for req in EMC_CANONICAL_ONLY_REQUIREMENTS:
        base = {"requirements": [_canonical(EMC_CANONICAL_ONLY_TOPIC, req)]}
        lexical = {"requirements": [_lexical(EMC_CANONICAL_ONLY_TOPIC, req)]}
        assert not _lexical_recall_supported(base["requirements"][0], lexical["requirements"][0])
        actual = augment_requirement_evaluation(base, lexical)
        row = actual["requirements"][0]
        assert row["status"] == "MISSING"
        assert row["evidence_mode"] == "canonical_claim"
        assert row["lexical_recall_floor_applied"] is False
        assert actual["canonical_promotion"]["lexical_recall_floor_count"] == 0


def test_emc_canonical_positive_fact_is_not_downgraded():
    req = "ipgse_emi_coupling_paths"
    base = {"requirements": [_canonical(EMC_CANONICAL_ONLY_TOPIC, req, "SATISFIED")]}
    lexical = {"requirements": [_lexical(EMC_CANONICAL_ONLY_TOPIC, req)]}
    result = augment_requirement_evaluation(base, lexical)["requirements"][0]
    assert result["status"] == "SATISFIED"
    assert result["matched_fact_ids"] == ["proper_fact"]
    assert result["lexical_recall_floor_applied"] is False


def test_emc_canonical_wrong_is_not_overridden_by_lexical_words():
    req = "ipgse_final_verification"
    base = {"requirements": [_canonical(EMC_CANONICAL_ONLY_TOPIC, req, "WRONG")]}
    lexical = {"requirements": [_lexical(EMC_CANONICAL_ONLY_TOPIC, req)]}
    result = augment_requirement_evaluation(base, lexical)["requirements"][0]
    assert result["status"] == "WRONG"
    assert result["lexical_recall_floor_applied"] is False


def test_unrelated_topic_preserves_existing_lexical_recall_behavior():
    topic = "some_other_topic"
    req = "scope_chain"
    base = {"requirements": [_canonical(topic, req)]}
    lexical = {"requirements": [_lexical(topic, req)]}
    assert _lexical_recall_supported(base["requirements"][0], lexical["requirements"][0])
    result = augment_requirement_evaluation(base, lexical)
    row = result["requirements"][0]
    assert row["status"] == "PARTIAL"
    assert row["evidence_mode"] == "canonical_claim+lexical_recall_floor"
    assert result["canonical_promotion"]["lexical_recall_floor_count"] == 1


def test_other_emc_requirements_preserve_lexical_recall_policy():
    req = "ipgse_shield_not_pe"
    base = {"requirements": [_canonical(EMC_CANONICAL_ONLY_TOPIC, req)]}
    lexical = {"requirements": [_lexical(EMC_CANONICAL_ONLY_TOPIC, req)]}
    result = augment_requirement_evaluation(base, lexical)
    assert result["requirements"][0]["status"] == "PARTIAL"



def test_actual_generic_terms_overmatch_wrong_ups_sentence_but_no_credit():
    answer = "Ground loop를 점검한다. UPS를 사용하면 모든 EMC 문제가 해결된다."
    with patch.object(adapter, "excluded_from_scoring", return_value=False):
        lexical = adapter.evaluate_fact_anchor_requirements(
            answer_text=answer, topic_ids=[EMC_CANONICAL_ONLY_TOPIC],
        )
    matched = {row["requirement_id"]: row for row in lexical["requirements"]}
    assert matched["ipgse_scope_chain"]["status"] == "SATISFIED"
    result = augment_requirement_evaluation(
        {"requirements": [_canonical(EMC_CANONICAL_ONLY_TOPIC, "ipgse_scope_chain")]},
        {"requirements": [matched["ipgse_scope_chain"]]},
    )
    assert result["requirements"][0]["status"] == "MISSING"
    assert not result["requirements"][0]["lexical_recall_floor_applied"]
