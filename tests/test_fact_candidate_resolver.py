"""Stage 4 shadow resolver never turns an unverified claim into a score."""

from __future__ import annotations

import copy
import hashlib

from grading.evidence.fact_candidate_resolver import resolve_answer_candidates
from grading.evidence.fact_grounded_contracts import VERSION, fingerprint


QUESTION = "LOPA의 위험감소를 설명하라."
ANSWER = "LOPA는 위험감소를 결정한다."
TOPIC = "sil_target_determination_risk_reduction_and_lifecycle"


def fact(status: str = "approved") -> dict:
    return {
        "schema_version": VERSION, "fact_id": "risk_reduction", "topic_id": TOPIC,
        "statement": "합성 사실", "relation": {
            "subject": "lopa", "predicate": "determines", "object": "risk_reduction", "conditions": [],
        },
        "source_refs": [{
            "source_id": "fixture:post:1", "source_version": "1",
            "source_sha256": "a" * 64, "locator": "section:body",
        }],
        "review_status": status, "revision": 1, "score_effect": "none",
    }


def question_contract(facts: list[dict], resolved: bool = True) -> dict:
    return {
        "schema_version": VERSION,
        "question_sha256": hashlib.sha256(QUESTION.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint(facts),
        "requirements": [{
            "requirement_id": "explain_risk_reduction",
            "source_span": {"start": 0, "end": len(QUESTION)},
            "source_text": QUESTION, "task": "explain",
            "fact_refs": ["risk_reduction"] if resolved else [],
            "resolution": "resolved" if resolved else "knowledge_gap",
        }],
        "score_effect": "none",
    }


def candidate(text: str = ANSWER) -> dict:
    return {
        "schema_version": VERSION, "candidate_id": "answer_1", "kind": "answer_claim",
        "source_span": {"start": 0, "end": len(text)}, "source_text": text,
        "proposal": {
            "subject": "lopa", "predicate": "determines", "object": "risk_reduction",
            "conditions": [], "polarity": "positive", "assertion_context": "asserted",
        },
        "producer": {"mode": "semantic_resolver", "resolver_id": "fixture", "resolver_version": "1"},
        "score_effect": "none",
    }


def resolve(*, text: str = ANSWER, facts: list[dict] | None = None,
            contract: dict | None = None, candidates: list[dict] | None = None,
            failed: bool = False, verified: set[str] | None = None) -> dict:
    rows = facts if facts is not None else [fact()]
    return resolve_answer_candidates(
        question_text=QUESTION, answer_text=text, facts=rows,
        question_contract=contract if contract is not None else question_contract(rows),
        candidates=candidates if candidates is not None else [candidate()], resolver_failed=failed,
        independently_verified_candidate_ids=verified,
    )


def test_exact_scoped_claim_is_only_score_neutral_evidence() -> None:
    result = resolve(verified={"answer_1"})
    assert result["extraction_complete"] is True
    assert result["accepted"][0]["fact_id"] == "risk_reduction"
    assert result["score_effect"] == "none"
    assert "score" not in result and "verdict" not in result


def test_negative_claim_and_unapproved_fact_are_unresolved() -> None:
    negative = candidate()
    negative["proposal"]["polarity"] = "negative"
    assert resolve(candidates=[negative])["extraction_complete"] is False
    rows = [fact("candidate")]
    assert resolve(facts=rows, contract=question_contract(rows, resolved=False))["accepted"] == []


def test_llm_proposal_alone_cannot_be_accepted() -> None:
    result = resolve()
    assert result["accepted"] == []
    assert result["extraction_complete"] is False


def test_unscoped_claim_is_not_accepted() -> None:
    result = resolve(contract=question_contract([fact()], resolved=False))
    assert not result["accepted"]
    assert result["unresolved_spans"]
    assert result["scope_resolved"] is False
    assert result["extraction_complete"] is False


def test_quoted_claim_is_ignored_and_unprocessed_tail_blocks_completion() -> None:
    quoted = candidate()
    quoted["proposal"]["assertion_context"] = "quoted"
    result = resolve(candidates=[quoted], verified={"answer_1"})
    assert result["ignored_candidate_ids"] == ["answer_1"]
    assert result["accepted"] == []
    assert result["extraction_complete"] is True
    assert resolve(candidates=[quoted])["extraction_complete"] is False
    result = resolve(text=ANSWER + " 추가 설명", candidates=[candidate()])
    assert result["extraction_complete"] is False
    assert any(row["reason"] == "uninterpreted_answer_text" for row in result["unresolved_spans"])


def test_conflicting_candidates_or_resolver_failure_abstain() -> None:
    second = copy.deepcopy(candidate())
    second["candidate_id"] = "answer_2"
    second["proposal"]["object"] = "sil_target"
    assert resolve(candidates=[candidate(), second])["accepted"] == []
    assert resolve(failed=True)["extraction_complete"] is False


def test_overlapping_spans_do_not_double_accept() -> None:
    shorter = copy.deepcopy(candidate())
    shorter["candidate_id"] = "answer_2"
    shorter["source_span"]["end"] -= 1
    shorter["source_text"] = ANSWER[:-1]
    assert resolve(candidates=[candidate(), shorter])["accepted"] == []
