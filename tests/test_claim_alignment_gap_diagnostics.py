"""S7 relation-gap diagnostics explain missing matches but cannot grade."""
from __future__ import annotations

import copy

import pytest

from grading.evidence.canonical_grading_evidence import (
    build_canonical_grading_evidence,
)
from grading.evidence.claim_alignment_contract import (
    build_alignment_result, canonical_relation,
)
from grading.evidence.claim_alignment_gap_diagnostics import (
    diagnose_claim_fact_relation_gap,
)

QUESTION = "차압식 유량계 원리를 설명하시오."
ANSWER = "유량은 차압의 제곱근에 비례한다."
TOPIC = "differential_pressure_flow_measurement_orifice_venturi_nozzle"
FACT_ID = "flow_dp_sqrt"


def _fixture(*, claim_relation=None, fact_relation=None, assertion="asserted",
             claim_owner=None, verified=True, differs=False, claim=True):
    base = {
        "subject": "flow_rate", "predicate": "proportional_to",
        "object": "square_root_dp", "polarity": "positive", "conditions": [],
    }
    assertion_relation = base | (claim_relation or {})
    expected_relation = base | (fact_relation or {})
    parsed = build_canonical_grading_evidence(
        question_text=QUESTION, answer_text=ANSWER,
        source={
            "mode": "deterministic_parser",
            "resolver_id": "canonical_claim_extractor",
            "resolver_version": "1",
        },
        claims=([{
            **assertion_relation,
            "assertion_context": assertion,
            "source_span": {"start": 0, "end": len(ANSWER)},
            "source_text": ANSWER,
            "qualifiers": {"owner_topic_id": claim_owner or TOPIC},
        }] if claim else []),
    )
    fact = {
        "owner_topic_id": TOPIC, "fact_id": FACT_ID,
        "parent_anchor_id": FACT_ID,
        "projection_status": (
            "VERIFIED_REGISTRY_RELATION" if verified
            else "STRUCTURED_MACHINE_RELATION"
        ),
        "source_fact_id": "registry_dp_flow" if verified else None,
        "relation_source": "verified_registry" if verified else "machine_contract",
        "machine_relation_differs": differs,
        "relation": canonical_relation(expected_relation),
    }
    aligned = build_alignment_result(
        answer_text=ANSWER, topic_ids=[TOPIC],
        fact_projection=[fact], logic_projection=[], alignments=[],
        unresolved=[],
    )
    return parsed, aligned


def _audit(**kwargs):
    parsed, aligned = _fixture(**kwargs)
    return diagnose_claim_fact_relation_gap(
        question_text=QUESTION, answer_text=ANSWER,
        canonical_evidence=parsed, alignment=aligned,
    )


@pytest.mark.parametrize(("kwargs", "category"), [
    ({}, "TRIPLE_COMPATIBLE_AUDIT_ONLY"),
    ({"claim": False}, "NO_ASSERTED_CLAIMS_FOR_TOPIC"),
    ({"assertion": "quoted"}, "NO_ASSERTED_CLAIMS_FOR_TOPIC"),
    ({"claim_owner": "foreign_topic_id"}, "NO_ASSERTED_CLAIMS_FOR_TOPIC"),
    ({"claim_relation": {"subject": "pressure"}}, "NO_SUBJECT_MATCH"),
    ({"claim_relation": {"predicate": "increases"}}, "SUBJECT_ONLY"),
    ({"claim_relation": {"object": "pressure"}}, "SUBJECT_PREDICATE_ONLY"),
    ({"claim_relation": {"polarity": "negative"}}, "TRIPLE_POLARITY_DIFFERS"),
    ({"fact_relation": {"conditions": ["incompressible"]}},
     "TRIPLE_CONDITIONS_INCOMPLETE"),
])
def test_relation_gap_classification_is_read_only(kwargs, category):
    result = _audit(**kwargs)
    assert result["fact_relation_gap_counts"] == {category: 1}
    assert result["score_admission"] == "DISABLED"
    assert result["final_grade_allowed"] is False
    assert result["score_effect"] == "none"
    assert ANSWER not in str(result)
    assert "total_score" not in result


def test_registry_missing_is_not_an_approved_relation():
    result = _audit(verified=False)
    assert result["verified_fact_count"] == 0
    assert result["fact_relation_gap_counts"] == {}
    assert result["score_admission"] == "DISABLED"


def test_verified_and_machine_relation_disagreement_is_exposed_not_overridden():
    result = _audit(differs=True)
    assert result["verified_machine_relation_differs_count"] == 1
    assert result["verified_fact_count"] == 1


def test_foreign_answer_or_tampered_canonical_document_is_rejected():
    parsed, alignment = _fixture()
    with pytest.raises(ValueError, match="foreign question or answer"):
        diagnose_claim_fact_relation_gap(
            question_text=QUESTION + " 변경", answer_text=ANSWER,
            canonical_evidence=parsed, alignment=alignment,
        )
    forged = copy.deepcopy(parsed)
    forged["claims"][0]["predicate"] = "arbitrary"
    with pytest.raises(ValueError):
        diagnose_claim_fact_relation_gap(
            question_text=QUESTION, answer_text=ANSWER,
            canonical_evidence=forged, alignment=alignment,
        )
