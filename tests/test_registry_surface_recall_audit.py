"""Audit-only registry literal probing; no independent correctness claims."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from grading.evidence.claim_alignment_contract import build_alignment_result
from grading.evidence.registry_surface_recall_audit import (
    REVIEW, audit_registry_surface_recall,
)

TOPIC = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
FACT = "fsrm_low_demand_pfdavg"
QUESTION = "PFDavg의 적용 대상을 설명하시오."


def _alignment(answer, *, verified=True, conditions=None):
    fact = {
        "owner_topic_id": TOPIC,
        "fact_id": FACT,
        "parent_anchor_id": FACT,
        "source_fact_id": "approved_fact_pfdavg" if verified else None,
        "projection_status": (
            "VERIFIED_REGISTRY_RELATION" if verified
            else "STRUCTURED_MACHINE_RELATION"
        ),
        "relation_source": "verified_registry" if verified else "machine_contract",
        "relation": {
            "subject": "pfdavg", "predicate": "applies_to",
            "object": "low_demand", "polarity": "positive",
            "conditions": conditions or [],
        },
    }
    return build_alignment_result(
        answer_text=answer, topic_ids=[TOPIC], fact_projection=[fact],
        logic_projection=[], alignments=[], unresolved=[],
    )


def _audit(answer, **kwargs):
    return audit_registry_surface_recall(
        question_text=QUESTION,
        answer_text=answer, alignment=_alignment(answer, **kwargs),
    )


@pytest.mark.parametrize("answer", [
    "PFDavg는 저수요 모드에 적용한다.",
    "저수요 모드에서는 PFDavg를 사용한다.",
])
def test_explicit_literal_relation_is_a_review_candidate_not_credit(answer):
    result = _audit(answer)
    assert result["review_literal_candidate_count"] == 1
    assert result["disposition_counts"][REVIEW] == 1
    assert result["score_admission"] == "DISABLED"
    assert result["final_grade_allowed"] is False
    assert result["score_effect"] == "none"
    assert "SATISFIED" not in str(result)
    assert answer not in str(result)
    assert result["rows"][0]["source_span"] == {
        "start": 0, "end": len(answer),
    }


@pytest.mark.parametrize(("answer", "disposition"), [
    ("PFDavg는 저수요 모드에 적용하지 않는다.", "HOLD_NEGATED_RELATION"),
    ('"PFDavg는 저수요 모드에 적용한다"라고 주장한다.', "HOLD_NONASSERTED_CONTEXT"),
    ("잘못된 주장: PFDavg는 저수요 모드에 적용한다.", "HOLD_NONASSERTED_CONTEXT"),
    ("PFDavg는 항상 저수요 모드에 적용한다.", "HOLD_ABSOLUTE_QUANTIFIER"),
])
def test_negative_quoted_rejected_and_universal_claims_are_held(answer, disposition):
    result = _audit(answer)
    assert result["review_literal_candidate_count"] == 0
    assert result["disposition_counts"][disposition] == 1
    assert result["hold_candidate_count"] == 1
    assert result["rows"][0]["review_disposition"] == disposition


def test_conditionally_verified_fact_is_held_even_with_literal_cooccurrence():
    result = _audit(
        "PFDavg는 저수요 모드에 적용한다.", conditions=["sif_requirement"]
    )
    assert result["review_literal_candidate_count"] == 0
    assert result["disposition_counts"] == {"HOLD_REQUIRED_CONDITIONS": 1}


@pytest.mark.parametrize("answer", [
    "PFDavg는 고수요 모드에 적용한다.",
    "PFH는 저수요 모드에 적용한다.",
    "PFDavg 저수요 모드",
    "PFDavg는 저수요 모드를 보완한다.",
])
def test_wrong_or_keyword_only_answer_is_not_a_literal_candidate(answer):
    result = _audit(answer)
    assert result["review_literal_candidate_count"] == 0
    assert result["hold_candidate_count"] == 0
    assert result["disposition_counts"] == {"NO_LITERAL_TRIPLET": 1}


def test_unverified_fact_never_becomes_registry_candidate():
    result = _audit("PFDavg는 저수요 모드에 적용한다.", verified=False)
    assert result["verified_fact_projection_count"] == 0
    assert result["review_literal_candidate_count"] == 0
    assert result["rows"] == []


def test_tampered_or_foreign_answer_alignment_fails_closed():
    answer = "PFDavg는 저수요 모드에 적용한다."
    with pytest.raises(ValueError):
        audit_registry_surface_recall(
            question_text=QUESTION, answer_text=answer + "!",
            alignment=_alignment(answer),
        )


def test_same_answer_and_registry_fact_produce_reproducible_audit():
    answer = "PFDavg는 저수요 모드에 적용한다."
    result = _audit(answer)
    for _ in range(5):
        assert _audit(answer) == result


def test_reviewed_demand_mode_golden_cannot_recombine_wrong_subject_and_object():
    """Real reviewed source sentences; the Fact projection is synthetic-only."""
    path = (Path(__file__).resolve().parents[1]
            / "calibration/risk_golden/functional_safety_demand_mode_cases.json")
    cases = {
        item["case_id"]: item["answer"]
        for item in json.loads(path.read_text(encoding="utf-8"))["cases"]
    }
    normal = _audit(cases["risk_fsrm_demand_mode_normal_01"])
    fatal = _audit(cases["risk_fsrm_demand_mode_fatal_01"])
    assert normal["review_literal_candidate_count"] >= 1
    # "PFDavg ... 고수요 ...이고 PFH는 저수요..." is an intentionally
    # wrong cross-subject explanation. Word co-occurrence cannot credit it.
    assert fatal["review_literal_candidate_count"] == 0
    assert fatal["disposition_counts"]["HOLD_COMPOSITE_CLAUSE"] >= 1
    assert normal["score_admission"] == fatal["score_admission"] == "DISABLED"


def test_cross_clause_explicitly_stays_held():
    answer = (
        "PFDavg는 고수요에서 사용하는 값이고 "
        "PFH는 저수요 모드에서 요구 시 실패확률이다."
    )
    result = _audit(answer)
    assert result["review_literal_candidate_count"] == 0
    assert result["disposition_counts"] == {"HOLD_COMPOSITE_CLAUSE": 1}
