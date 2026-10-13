"""The real parser's unresolved spans are the only answer text sent to assistance."""
from copy import deepcopy

import pytest

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.fact_grounded_contracts import FactGroundedContractError, fingerprint
from grading.evidence.fact_unresolved_queue import (
    assist_parser_unresolved, build_unresolved_queue, screen_assist_proposals,
)
from test_fact_candidate_resolver import fact


TOPIC = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
QUESTION = "요구모드별 PFDavg를 설명하시오."
ANSWER = "PFDavg는 계산하기 복잡한 지표이다."


def scoped_inputs():
    row = fact()
    row["topic_id"] = TOPIC
    row["relation"] = {"subject": "pfdavg", "predicate": "applies_to",
                       "object": "low_demand", "conditions": []}
    facts = [row]
    import hashlib
    contract = {
        "schema_version": row["schema_version"],
        "question_sha256": hashlib.sha256(QUESTION.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint(facts),
        "requirements": [{"requirement_id": "r1",
                          "source_span": {"start": 0, "end": len(QUESTION)},
                          "source_text": QUESTION, "task": "explain",
                          "fact_refs": [row["fact_id"]], "resolution": "resolved"}],
        "score_effect": "none",
    }
    versions = {k: "v1" for k in ("model", "prompt", "parser", "verifier", "policy")}
    return facts, contract, versions


def test_real_parser_routes_only_unresolved_excerpt():
    facts, contract, versions = scoped_inputs()
    requests = []
    def provider(request):
        requests.append(request)
        return {"rows": [{"fact_id": facts[0]["fact_id"],
                          "interpretation": "unknown", "quote": request["excerpt"],
                          "reason": "fixture", "missing_conditions": []}]}
    result = assist_parser_unresolved(
        question_text=QUESTION, answer_text=ANSWER, facts=facts,
        question_contract=contract, topic_ids=[TOPIC], versions=versions,
        provider=provider, enabled=True,
    )
    assert result["parser_unresolved_count"] == result["queued_count"] == 1
    assert requests[0]["excerpt"] == ANSWER
    assert result["assistance"]["provider_calls"] == 1
    assert result["assistance"]["items"][0]["state"] == "pending_verification"
    assert result["final_grade_allowed"] is False


def test_resolved_parser_claim_and_disabled_assist_use_no_provider():
    facts, contract, versions = scoped_inputs()
    def forbidden(_request):
        pytest.fail("unexpected provider call")
    for answer, enabled in [("PFDavg는 저수요 모드에 적용한다.", True), (ANSWER, False)]:
        result = assist_parser_unresolved(
            question_text=QUESTION, answer_text=answer, facts=facts,
            question_contract=contract, topic_ids=[TOPIC], versions=versions,
            provider=forbidden, enabled=enabled,
        )
        assert result["assistance"]["provider_calls"] == 0


def test_ambiguous_question_scope_skips_call():
    facts, contract, versions = scoped_inputs()
    other = deepcopy(facts[0])
    other["fact_id"] = "other"
    other["relation"] = {"subject": "unrelated", "predicate": "applies_to",
                         "object": "other_object", "conditions": []}
    facts.append(other)
    contract["requirements"].append({**contract["requirements"][0],
                                      "requirement_id": "r2", "fact_refs": ["other"]})
    contract["knowledge_snapshot_sha256"] = fingerprint(sorted(facts, key=lambda row: row["fact_id"]))
    extraction = extract_canonical_claim_evidence(ANSWER, question_text=QUESTION, topic_ids=[TOPIC])
    result = build_unresolved_queue(question_text=QUESTION, answer_text=ANSWER,
                                    facts=facts, question_contract=contract, extraction=extraction)
    assert len(result["work_items"]) == 1  # pfdavg concept uniquely scopes r1
    extraction["unresolved_spans"][0]["concept_candidates"] = []
    result = build_unresolved_queue(question_text=QUESTION, answer_text=ANSWER,
                                    facts=facts, question_contract=contract, extraction=extraction)
    assert not result["work_items"]
    assert result["skipped"][0]["reason"] == "ambiguous_or_unresolved_question_scope"


def test_stale_snapshot_and_forged_quote_rejected():
    facts, contract, _ = scoped_inputs()
    extraction = extract_canonical_claim_evidence(ANSWER, question_text=QUESTION, topic_ids=[TOPIC])
    stale = deepcopy(contract)
    stale["knowledge_snapshot_sha256"] = "0" * 64
    with pytest.raises(FactGroundedContractError):
        build_unresolved_queue(question_text=QUESTION, answer_text=ANSWER,
                               facts=facts, question_contract=stale, extraction=extraction)
    extraction["unresolved_spans"][0]["source_text"] = "invented"
    with pytest.raises(FactGroundedContractError):
        build_unresolved_queue(question_text=QUESTION, answer_text=ANSWER,
                               facts=facts, question_contract=contract, extraction=extraction)


@pytest.mark.parametrize("excerpt,reason", [
    ("PFD_avg <= F_H,max × F_D", "engineering_invariant_violation"),
    ("PFDavg는 저수요 모드에 적용하지 않는다.", "negative_or_nonasserted_claim"),
    ("잘못된 예시는 PFDavg를 고수요 모드에 적용하는 것이다.",
     "negative_or_nonasserted_claim"),
])
def test_obvious_false_support_is_blocked(excerpt, reason):
    screened = screen_assist_proposals(excerpt=excerpt, proposals=[{
        "fact_id": "risk_reduction", "interpretation": "supported",
    }])
    assert screened[0]["state"] == "blocked"
    assert reason in screened[0]["reasons"]


def test_clean_support_still_requires_semantic_verification():
    screened = screen_assist_proposals(excerpt="PFDavg는 저수요 모드에 적용한다.", proposals=[{
        "fact_id": "risk_reduction", "interpretation": "supported",
    }])
    assert screened[0]["state"] == "pending_semantic_verification"


def test_parser_path_can_collect_blind_second_review_without_score():
    facts, contract, versions = scoped_inputs()
    def first(request):
        return {"rows": [{"fact_id": facts[0]["fact_id"],
                          "interpretation": "supported", "quote": request["excerpt"],
                          "reason": "first reading", "missing_conditions": []}]}
    def reviewer(request):
        assert "first reading" not in str(request)
        return {"interpretation": "unknown", "quote": request["excerpt"],
                "reason": "source does not establish the relation", "missing_conditions": []}
    result = assist_parser_unresolved(
        question_text=QUESTION, answer_text=ANSWER, facts=facts,
        question_contract=contract, topic_ids=[TOPIC], versions=versions,
        provider=first, reviewer_provider=reviewer, reviewer_version="v1", enabled=True,
    )
    assert result["reviewer_calls"] == 1
    review = result["assistance"]["items"][0]["semantic_review"]
    assert review["rows"][0]["state"] == "disagreement"
    assert review["final_grade_allowed"] is False


def test_assistance_call_limit_defers_extra_parser_spans():
    facts, contract, versions = scoped_inputs()
    answer = ANSWER + "\n" + ANSWER
    result = assist_parser_unresolved(
        question_text=QUESTION, answer_text=answer, facts=facts,
        question_contract=contract, topic_ids=[TOPIC], versions=versions,
        provider=lambda request: pytest.fail("call limit should disable provider"),
        enabled=True, max_items=0,
    )
    assert result["queued_count"] == 0
    assert result["assistance"]["provider_calls"] == 0
    assert any(row["reason"] == "deferred_by_call_limit" for row in result["skipped"])
    with pytest.raises(FactGroundedContractError, match="limit"):
        assist_parser_unresolved(
            question_text=QUESTION, answer_text=answer, facts=facts,
            question_contract=contract, topic_ids=[TOPIC], versions=versions,
            provider=lambda request: None, enabled=True, max_items=-1,
        )


def test_multi_fact_requirement_sends_only_concept_matched_fact():
    facts, contract, _ = scoped_inputs()
    other = deepcopy(facts[0])
    other["fact_id"] = "unrelated_fact"
    other["relation"] = {"subject": "unrelated", "predicate": "applies_to",
                         "object": "other_object", "conditions": []}
    facts.append(other)
    contract["requirements"][0]["fact_refs"].append(other["fact_id"])
    contract["knowledge_snapshot_sha256"] = fingerprint(
        sorted(facts, key=lambda row: row["fact_id"])
    )
    extraction = extract_canonical_claim_evidence(
        ANSWER, question_text=QUESTION, topic_ids=[TOPIC],
    )
    queue = build_unresolved_queue(
        question_text=QUESTION, answer_text=ANSWER, facts=facts,
        question_contract=contract, extraction=extraction,
    )
    assert queue["work_items"][0]["fact_ids"] == [facts[0]["fact_id"]]
