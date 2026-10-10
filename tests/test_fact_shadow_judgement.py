import hashlib

import pytest

from grading.evidence.fact_grounded_contracts import VERSION, FactGroundedContractError, fingerprint
from grading.evidence.fact_shadow_judgement import judge_candidates, judge_verified_evidence


def fixture():
    question = "Explain SIL target."
    fact = {
        "schema_version": VERSION, "fact_id": "sil_ratio", "topic_id": "sil_target",
        "statement": "The low-demand target PFD is the tolerable-to-residual frequency ratio.",
        "relation": {"subject": "sil", "predicate": "has_target", "object": "pfd", "conditions": ["low_demand"]},
        "source_refs": [{"source_id": "wp-post:9398", "source_version": "1", "source_sha256": "a" * 64, "locator": "section 6"}],
        "review_status": "approved", "revision": 1, "score_effect": "none",
    }
    contract = {
        "schema_version": VERSION, "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint([fact]),
        "requirements": [{"requirement_id": "req_one", "source_span": {"start": 0, "end": len(question)},
                          "source_text": question, "task": "explain", "fact_refs": ["sil_ratio"], "resolution": "resolved"}],
        "score_effect": "none",
    }
    resolution = {
        "accepted": [{"candidate_id": "candidate_one", "fact_id": "sil_ratio", "source_span": {"start": 0, "end": 7}, "score_effect": "none"}],
        "ignored_candidate_ids": [], "unresolved_spans": [], "scope_resolved": True,
        "extraction_complete": True, "score_effect": "none",
    }
    return question, fact, contract, resolution


def test_verified_fact_is_proved_but_never_scores():
    question, fact, contract, resolution = fixture()
    result = judge_verified_evidence(question_text=question, facts=[fact], question_contract=contract, resolution=resolution)
    assert result["requirements"][0]["state"] == "proved"
    assert result["complete"] is True
    assert result["final_grade_allowed"] is False
    assert result["score_effect"] == "none"


def test_absence_and_partial_extraction_do_not_mean_wrong():
    question, fact, contract, resolution = fixture()
    resolution["accepted"] = []
    resolution["unresolved_spans"] = [{"start": 0, "end": 1, "reason": "uninterpreted_answer_text"}]
    resolution["extraction_complete"] = False
    result = judge_verified_evidence(question_text=question, facts=[fact], question_contract=contract, resolution=resolution)
    assert result["requirements"][0]["state"] == "unresolved"
    assert result["complete"] is False


def test_candidate_cannot_assign_score_or_use_unapproved_fact():
    question, fact, contract, resolution = fixture()
    resolution["accepted"][0]["score"] = 25
    with pytest.raises(FactGroundedContractError):
        judge_verified_evidence(question_text=question, facts=[fact], question_contract=contract, resolution=resolution)
    del resolution["accepted"][0]["score"]
    fact["review_status"] = "candidate"
    contract["knowledge_snapshot_sha256"] = fingerprint([fact])
    with pytest.raises(FactGroundedContractError):
        judge_verified_evidence(question_text=question, facts=[fact], question_contract=contract, resolution=resolution)


def test_unverified_semantic_candidate_cannot_be_proved():
    question, fact, contract, _ = fixture()
    answer = "SIL has target PFD."
    candidate = {
        "schema_version": VERSION, "candidate_id": "candidate_one", "kind": "answer_claim",
        "source_span": {"start": 0, "end": len(answer)}, "source_text": answer,
        "proposal": {"subject": "sil", "predicate": "has_target", "object": "pfd",
                     "conditions": ["low_demand"], "polarity": "positive", "assertion_context": "asserted"},
        "producer": {"mode": "semantic_resolver", "resolver_id": "test_resolver", "resolver_version": "1"},
        "score_effect": "none",
    }
    result = judge_candidates(question_text=question, answer_text=answer,
                              facts=[fact], question_contract=contract, candidates=[candidate])
    assert result["requirements"][0]["state"] == "unresolved"
