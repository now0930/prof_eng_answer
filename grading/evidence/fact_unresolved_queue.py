"""Bridge deterministic parser uncertainty to the score-neutral LLM assistant.

Question scope must already be fixed independently of the answer. This module
never creates a requirement or treats a model proposal as verified evidence.
"""
from __future__ import annotations

from typing import Any

from .canonical_claim_extractor import extract_canonical_claim_evidence
from .engineering_invariant_evaluator import evaluate_engineering_invariants
from .fact_grounded_contracts import (
    FactGroundedContractError, fingerprint, validate_fact, validate_question_contract,
)
from .unresolved_semantic_assist import assist_unresolved, build_assist_request


def screen_assist_proposals(*, excerpt: str, proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Block obvious contradictions; passing this screen does not prove meaning."""
    invariant_codes = sorted({row["code"] for row in
                              evaluate_engineering_invariants(excerpt)["violations"]})
    parsed = extract_canonical_claim_evidence(excerpt)
    unsafe_claim_context = any(
        claim.get("polarity") == "negative"
        or claim.get("assertion_context") in {"quoted", "rejected"}
        for claim in parsed["canonical_evidence"]["claims"]
    )
    screened = []
    for proposal in proposals:
        reasons = []
        if proposal["interpretation"] == "supported":
            if invariant_codes:
                reasons.append("engineering_invariant_violation")
            if unsafe_claim_context:
                reasons.append("negative_or_nonasserted_claim")
        screened.append({"fact_id": proposal["fact_id"],
                         "state": "blocked" if reasons else "pending_semantic_verification",
                         "reasons": reasons, "invariant_codes": invariant_codes})
    return screened


def build_unresolved_queue(*, question_text: str, answer_text: str,
                           facts: list[dict[str, Any]], question_contract: dict[str, Any],
                           extraction: dict[str, Any]) -> dict[str, Any]:
    """Create work only for parser-identified spans with a unique resolved scope."""
    by_id = {}
    for fact in facts:
        validate_fact(fact)
        if fact["fact_id"] in by_id:
            raise FactGroundedContractError("duplicate Fact ID")
        by_id[fact["fact_id"]] = fact
    if question_contract.get("knowledge_snapshot_sha256") != fingerprint(
        sorted(facts, key=lambda fact: fact["fact_id"])
    ):
        raise FactGroundedContractError("question knowledge snapshot mismatch")
    approved = {fid for fid, fact in by_id.items() if fact["review_status"] == "approved"}
    validate_question_contract(question_contract, question_text, approved)
    if not isinstance(extraction, dict) or extraction.get("provider_calls") != 0:
        raise FactGroundedContractError("only deterministic parser output is accepted")
    spans = extraction.get("unresolved_spans")
    if not isinstance(spans, list):
        raise FactGroundedContractError("parser unresolved spans missing")
    resolved = [row for row in question_contract["requirements"] if row["resolution"] == "resolved"]
    work_items = []
    skipped = []
    seen_spans = set()
    for span in spans:
        if not isinstance(span, dict) or set(span) != {"start", "end", "source_text", "concept_candidates"}:
            raise FactGroundedContractError("invalid parser span")
        start, end = span["start"], span["end"]
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(answer_text):
            raise FactGroundedContractError("parser span outside answer")
        if answer_text[start:end] != span["source_text"]:
            raise FactGroundedContractError("parser quote mismatch")
        if (start, end) in seen_spans:
            raise FactGroundedContractError("duplicate parser span")
        seen_spans.add((start, end))
        concepts = span["concept_candidates"]
        if not isinstance(concepts, list) or not all(isinstance(x, str) for x in concepts):
            raise FactGroundedContractError("invalid parser concepts")
        concept_ids = set(concepts)
        matching = []
        for requirement in resolved:
            matched_fact_ids = [fid for fid in requirement["fact_refs"]
                                if concept_ids & {by_id[fid]["relation"]["subject"],
                                                  by_id[fid]["relation"]["object"]}]
            if matched_fact_ids:
                matching.append((requirement, matched_fact_ids))
        if not matching and len(resolved) == 1:
            matching = [(resolved[0], list(resolved[0]["fact_refs"]))]
            # One possible demand; semantic verification is still required.
        if len(matching) != 1:
            skipped.append({"source_span": {"start": start, "end": end},
                            "reason": "ambiguous_or_unresolved_question_scope"})
            continue
        requirement, matched_fact_ids = matching[0]
        work_items.append({
            "requirement_id": requirement["requirement_id"],
            "fact_ids": matched_fact_ids,
            "source_span": {"start": start, "end": end},
            "reason": "deterministic_parser_unresolved",
        })
    return {"work_items": work_items, "skipped": skipped, "score_effect": "none"}


def assist_parser_unresolved(*, question_text: str, answer_text: str,
                             facts: list[dict[str, Any]], question_contract: dict[str, Any],
                             topic_ids: list[str], versions: dict[str, str],
                             provider, enabled: bool = False, cache=None,
                             reviewer_provider=None, reviewer_version: str = "", reviewer_cache=None,
                             max_items: int | None = None) -> dict[str, Any]:
    """Run the real parser, then request interpretations only for its unresolved spans."""
    extraction = extract_canonical_claim_evidence(
        answer_text, question_text=question_text, topic_ids=topic_ids,
    )
    queue = build_unresolved_queue(
        question_text=question_text, answer_text=answer_text, facts=facts,
        question_contract=question_contract, extraction=extraction,
    )
    if max_items is not None:
        if type(max_items) is not int or max_items < 0:
            raise FactGroundedContractError("invalid semantic assistance limit")
        deferred = queue["work_items"][max_items:]
        queue["work_items"] = queue["work_items"][:max_items]
        queue["skipped"].extend({"source_span": item["source_span"],
                                 "reason": "deferred_by_call_limit"} for item in deferred)
    assisted = assist_unresolved(
        question=question_text, answer=answer_text, facts=facts,
        work_items=queue["work_items"], versions=versions,
        provider=provider, enabled=enabled, cache=cache,
    )
    reviewer_calls = 0
    for item, work_item in zip(assisted["items"], queue["work_items"]):
        if item["state"] == "pending_verification":
            start, end = work_item["source_span"]["start"], work_item["source_span"]["end"]
            item["screening"] = screen_assist_proposals(
                excerpt=answer_text[start:end], proposals=item["proposals"],
            )
            if reviewer_provider is not None:
                # Local import avoids a module cycle: the review layer uses the
                # same deterministic screening function defined above.
                from .fact_semantic_review import review_assist_response

                request = build_assist_request(
                    question=question_text, answer=answer_text, facts=facts,
                    work_item=work_item, versions=versions,
                )
                review = review_assist_response(
                    request=request, response={"rows": item["proposals"]},
                    provider=reviewer_provider, reviewer_version=reviewer_version,
                    cache=reviewer_cache,
                )
                item["semantic_review"] = review
                reviewer_calls += review["reviewer_calls"]
    return {
        "parser_unresolved_count": len(extraction["unresolved_spans"]),
        "queued_count": len(queue["work_items"]), "skipped": queue["skipped"],
        "assistance": assisted, "reviewer_calls": reviewer_calls,
        "score_effect": "none", "final_grade_allowed": False,
    }
