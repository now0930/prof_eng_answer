"""Fail-closed shadow resolver for answer-claim interpretation candidates."""

from __future__ import annotations

from typing import Any

from .fact_grounded_contracts import (
    FactGroundedContractError,
    fingerprint,
    validate_fact,
    validate_interpretation_candidate,
    validate_question_contract,
)


def resolve_answer_candidates(
    *, question_text: str, answer_text: str,
    facts: list[dict[str, Any]], question_contract: dict[str, Any],
    candidates: list[dict[str, Any]], resolver_failed: bool = False,
    independently_verified_candidate_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Accept only uniquely grounded positive claims; never classify or score."""
    seen_facts: set[str] = set()
    for fact in facts:
        validate_fact(fact)
        if fact["fact_id"] in seen_facts:
            raise FactGroundedContractError("duplicate fact_id")
        seen_facts.add(fact["fact_id"])
    if question_contract.get("knowledge_snapshot_sha256") != fingerprint(sorted(facts, key=lambda row: row["fact_id"])):
        raise FactGroundedContractError("question knowledge snapshot does not match facts")
    approved = {fact["fact_id"]: fact for fact in facts if fact["review_status"] == "approved"}
    independently_verified = independently_verified_candidate_ids or set()
    validate_question_contract(question_contract, question_text, set(approved))
    scoped_fact_ids = {
        fact_id
        for requirement in question_contract["requirements"]
        if requirement["resolution"] == "resolved"
        for fact_id in requirement["fact_refs"]
    }
    scope_resolved = bool(question_contract["requirements"]) and all(
        requirement["resolution"] == "resolved"
        for requirement in question_contract["requirements"]
    )
    seen_candidates: set[str] = set()
    spans: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for candidate in candidates:
        validate_interpretation_candidate(candidate, question_text, answer_text)
        if candidate["kind"] != "answer_claim":
            raise FactGroundedContractError("question proposal cannot resolve an answer")
        if candidate["candidate_id"] in seen_candidates:
            raise FactGroundedContractError("duplicate candidate_id")
        seen_candidates.add(candidate["candidate_id"])
        span = candidate["source_span"]
        spans.setdefault((span["start"], span["end"]), []).append(candidate)
    overlap_spans = {
        left for left in spans for right in spans
        if left != right and left[0] < right[1] and right[0] < left[1]
    }
    accepted = []
    unresolved = []
    ignored = []
    covered = [False] * len(answer_text)
    for (start, end), proposals in sorted(spans.items()):
        covered[start:end] = [True] * (end - start)
        if len(proposals) != 1 or resolver_failed or (start, end) in overlap_spans:
            unresolved.append({"start": start, "end": end, "reason": "conflicting_or_failed_resolution"})
            continue
        candidate = proposals[0]
        proposal = candidate["proposal"]
        if proposal["assertion_context"] in {"quoted", "rejected"}:
            if candidate["candidate_id"] in independently_verified:
                ignored.append(candidate["candidate_id"])
            else:
                unresolved.append({"start": start, "end": end, "reason": "unverified_assertion_context"})
            continue
        matches = [fact_id for fact_id, fact in approved.items() if fact_id in scoped_fact_ids and (
            proposal["subject"] == fact["relation"]["subject"]
            and proposal["predicate"] == fact["relation"]["predicate"]
            and proposal["object"] == fact["relation"]["object"]
            and set(proposal["conditions"]) == set(fact["relation"]["conditions"])
            and proposal["polarity"] == "positive"
        )]
        if len(matches) != 1 or candidate["candidate_id"] not in independently_verified:
            unresolved.append({"start": start, "end": end, "reason": "not_uniquely_grounded"})
            continue
        accepted.append({
            "candidate_id": candidate["candidate_id"], "fact_id": matches[0],
            "source_span": {"start": start, "end": end}, "score_effect": "none",
        })
    for index, character in enumerate(answer_text):
        if not character.isspace() and not covered[index]:
            unresolved.append({"start": index, "end": index + 1, "reason": "uninterpreted_answer_text"})
    if resolver_failed and not unresolved:
        unresolved.append({"start": 0, "end": len(answer_text), "reason": "resolver_failed"})
    return {
        "accepted": accepted,
        "ignored_candidate_ids": ignored,
        "unresolved_spans": unresolved,
        "scope_resolved": scope_resolved,
        "extraction_complete": scope_resolved and not unresolved,
        "score_effect": "none",
    }
