"""Score-neutral question scope compiler over approved facts and grounded proposals."""

from __future__ import annotations

import hashlib
from typing import Any
import unicodedata

from grading.evidence.fact_grounded_contracts import (
    VERSION,
    FactGroundedContractError,
    fingerprint,
    validate_fact,
    validate_interpretation_candidate,
    validate_question_contract,
)


def compile_question_contract(
    question_text: str,
    facts: list[dict[str, Any]],
    requirement_candidates: list[dict[str, Any]],
    *, concept_aliases: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """Pin question requirements without reading any answer or assigning points.

    A unique approved fact is resolved. Multiple eligible facts are ambiguous,
    not silently all required; zero eligible facts are a knowledge gap.
    """
    if not isinstance(question_text, str) or not question_text.strip():
        raise FactGroundedContractError("question text is empty")
    fact_ids: set[str] = set()
    for fact in facts:
        validate_fact(fact)
        if fact["fact_id"] in fact_ids:
            raise FactGroundedContractError("duplicate fact_id")
        fact_ids.add(fact["fact_id"])
    approved = [fact for fact in facts if fact["review_status"] == "approved"]
    aliases = concept_aliases or {}
    seen_spans: set[tuple[int, int]] = set()
    requirements = []
    for candidate in requirement_candidates:
        validate_interpretation_candidate(candidate, question_text, "")
        if candidate["kind"] != "question_requirement":
            raise FactGroundedContractError("answer claim cannot define question scope")
        span = candidate["source_span"]
        span_key = (span["start"], span["end"])
        if span_key in seen_spans:
            raise FactGroundedContractError("duplicate question span")
        seen_spans.add(span_key)
        proposal = candidate["proposal"]
        targets = set(proposal["target_concepts"])
        conditions = set(proposal["conditions"])
        normalized_source = unicodedata.normalize("NFKC", candidate["source_text"]).casefold()
        concept_grounded = all(
            any(
                isinstance(alias, str) and alias.strip()
                and unicodedata.normalize("NFKC", alias).casefold() in normalized_source
                for alias in aliases.get(concept_id, [])
            ) for concept_id in targets
        )
        eligible = []
        for fact in approved:
            relation = fact["relation"]
            concepts = {relation["subject"], relation["object"]}
            if targets <= concepts and conditions == set(relation["conditions"]):
                eligible.append(fact["fact_id"])
        needs_richer_contract = proposal["task"] in {"compare", "calculate", "design", "evaluate", "apply"}
        resolution = (
            "knowledge_gap" if not eligible else
            "ambiguous" if len(eligible) != 1 or needs_richer_contract or not concept_grounded
            or candidate["producer"]["mode"] == "semantic_resolver" else
            "resolved"
        )
        requirements.append({
            "requirement_id": candidate["candidate_id"],
            "source_span": dict(span), "source_text": candidate["source_text"],
            "task": proposal["task"],
            "fact_refs": eligible if resolution == "resolved" else [],
            "resolution": resolution,
        })
    contract = {
        "schema_version": VERSION,
        "question_sha256": hashlib.sha256(question_text.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint(sorted(facts, key=lambda row: row["fact_id"])),
        "requirements": sorted(requirements, key=lambda row: (row["source_span"]["start"], row["requirement_id"])),
        "score_effect": "none",
    }
    return validate_question_contract(contract, question_text, {fact["fact_id"] for fact in approved})
