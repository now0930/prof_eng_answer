"""Fail-closed, score-neutral judgement over already verified answer evidence.

This is an offline shadow projection. It cannot replace the A/B/C/D/E scorer,
declare an answer wrong, or assign a final grade. An unproved relation remains
unresolved even when a matching keyword occurs in the answer.
"""

from __future__ import annotations

from typing import Any

from .fact_grounded_contracts import (
    FactGroundedContractError,
    fingerprint,
    validate_fact,
    validate_question_contract,
)
from .fact_candidate_resolver import resolve_answer_candidates


def judge_candidates(
    *, question_text: str, answer_text: str, facts: list[dict[str, Any]],
    question_contract: dict[str, Any], candidates: list[dict[str, Any]],
    independently_verified_candidate_ids: set[str] | None = None,
    resolver_failed: bool = False,
) -> dict[str, Any]:
    """Use the existing resolver; raw LLM candidates never become evidence."""
    resolution = resolve_answer_candidates(
        question_text=question_text, answer_text=answer_text,
        facts=facts, question_contract=question_contract, candidates=candidates,
        independently_verified_candidate_ids=independently_verified_candidate_ids,
        resolver_failed=resolver_failed,
    )
    return judge_verified_evidence(
        question_text=question_text, facts=facts,
        question_contract=question_contract, resolution=resolution,
    )


def judge_verified_evidence(
    *, question_text: str, facts: list[dict[str, Any]],
    question_contract: dict[str, Any], resolution: dict[str, Any],
) -> dict[str, Any]:
    """Report proved and unresolved demands; never infer failure from absence."""
    fact_by_id: dict[str, dict[str, Any]] = {}
    for fact in facts:
        validate_fact(fact)
        if fact["fact_id"] in fact_by_id:
            raise FactGroundedContractError("duplicate fact_id")
        fact_by_id[fact["fact_id"]] = fact
    approved = {key for key, value in fact_by_id.items() if value["review_status"] == "approved"}
    if question_contract.get("knowledge_snapshot_sha256") != fingerprint(sorted(facts, key=lambda row: row["fact_id"])):
        raise FactGroundedContractError("question knowledge snapshot mismatch")
    validate_question_contract(question_contract, question_text, approved)
    if not isinstance(resolution, dict) or set(resolution) != {
        "accepted", "ignored_candidate_ids", "unresolved_spans", "scope_resolved",
        "extraction_complete", "score_effect",
    } or resolution["score_effect"] != "none":
        raise FactGroundedContractError("invalid evidence resolution")
    accepted = resolution["accepted"]
    if not isinstance(accepted, list) or not isinstance(resolution["unresolved_spans"], list):
        raise FactGroundedContractError("invalid evidence collection")
    observed: set[str] = set()
    candidate_ids: set[str] = set()
    scoped = {fid for row in question_contract["requirements"] for fid in row["fact_refs"]}
    for row in accepted:
        if not isinstance(row, dict) or set(row) != {"candidate_id", "fact_id", "source_span", "score_effect"} or row["score_effect"] != "none":
            raise FactGroundedContractError("invalid accepted evidence")
        if row["fact_id"] not in approved or row["fact_id"] not in scoped:
            raise FactGroundedContractError("unapproved or out-of-scope evidence")
        if row["candidate_id"] in candidate_ids:
            raise FactGroundedContractError("duplicate accepted candidate")
        candidate_ids.add(row["candidate_id"])
        observed.add(row["fact_id"])
    complete = (
        resolution["scope_resolved"] is True
        and resolution["extraction_complete"] is True
        and not resolution["unresolved_spans"]
    )
    rows = []
    for requirement in question_contract["requirements"]:
        refs = requirement["fact_refs"]
        proved = requirement["resolution"] == "resolved" and bool(refs) and set(refs) <= observed
        rows.append({
            "requirement_id": requirement["requirement_id"],
            "state": "proved" if proved else "unresolved",
            "fact_refs": refs,
        })
    return {
        "requirements": rows,
        "complete": complete,
        "final_grade_allowed": False,
        "score_effect": "none",
    }
