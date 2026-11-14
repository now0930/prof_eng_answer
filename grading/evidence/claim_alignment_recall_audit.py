"""Score-neutral review queue for exact Claim/Fact matches missed by grading.

This cannot produce a score-bearing admission, even when a verified Registry
relation and answer Claim match. Human-labelled false-positive/false-negative
regression and an explicit, separately gated scorer are required before any
B/C status change.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any

from grading.evidence.claim_alignment_contract import validate_alignment_result


def summarize_recall_review_candidates(
    *, alignment: Mapping[str, Any], answer_text: str,
    requirement_evaluation: Mapping[str, Any],
) -> dict[str, Any]:
    """Identify audit-only missed-recall candidates with source ownership."""
    validate_alignment_result(dict(alignment), answer_text=answer_text)
    rows = requirement_evaluation.get("requirements")
    if not isinstance(rows, list):
        raise ValueError("requirement rows are missing")
    requirements: dict[tuple[str, str], Mapping[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("invalid requirement row")
        topic, requirement_id = row.get("owner_topic_id"), row.get("requirement_id")
        if not isinstance(topic, str) or not isinstance(requirement_id, str):
            raise ValueError("invalid requirement identity")
        key = (topic, requirement_id)
        if key in requirements:
            # Ambiguous ownership must not silently choose one score state.
            raise ValueError("duplicate requirement identity")
        if row.get("status") not in {
            "SATISFIED", "PARTIAL", "MISSING", "UNKNOWN", "WRONG",
        }:
            raise ValueError("unsupported requirement status")
        requirements[key] = row

    projected = {
        (fact.get("owner_topic_id"), fact.get("fact_id")): fact
        for fact in alignment["fact_projection"]
        if isinstance(fact, Mapping)
    }
    events: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, int, int]] = set()
    for row in alignment["alignments"]:
        if row["relation"] != "EXACT_RELATION":
            continue
        topic, fact_id = row["owner_topic_id"], row["fact_id"]
        fact = projected.get((topic, fact_id))
        if fact is None:
            continue
        # Explicit ID equality is the only permitted mapping here. Neither
        # keywords nor an LLM may invent a requirement to link this Fact.
        req = requirements.get((topic, fact_id))
        if req is None or fact_id == "__question_scope__":
            continue
        span = row["source_span"]
        event_key = (
            topic, fact_id, row["answer_claim_id"], span["start"], span["end"],
        )
        if event_key in seen:
            continue
        seen.add(event_key)
        if (
            fact.get("projection_status") != "VERIFIED_REGISTRY_RELATION"
            or not fact.get("source_fact_id")
            or fact.get("relation_source") != "verified_registry"
        ):
            disposition = "NOT_VERIFIED"
        elif fact.get("machine_relation_differs"):
            disposition = "HOLD_SOURCE_CONTRACT_CONFLICT"
        elif req["status"] == "WRONG":
            disposition = "BLOCKED_EXISTING_WRONG"
        elif req["status"] == "SATISFIED":
            disposition = "ALREADY_SATISFIED"
        else:
            # A possible false rejection, not evidence that a status should
            # be upgraded. Review the actual sentence, scope and Logic first.
            disposition = "REVIEW_POTENTIAL_RECALL_MISS"
        events.append({
            "owner_topic_id": topic,
            "requirement_id": fact_id,
            "source_fact_id": fact.get("source_fact_id"),
            "answer_claim_id": row["answer_claim_id"],
            "source_span": dict(span),
            "current_requirement_status": req["status"],
            "review_disposition": disposition,
        })
    events.sort(key=lambda r: (
        r["owner_topic_id"], r["requirement_id"],
        r["source_span"]["start"], r["source_span"]["end"],
        r["answer_claim_id"],
    ))
    counts = Counter(row["review_disposition"] for row in events)
    return {
        "schema_version": "claim_alignment_recall_audit.v1",
        "status": "AUDIT_ONLY",
        "score_effect": "none",
        "final_grade_allowed": False,
        "candidate_count": len(events),
        "disposition_counts": dict(sorted(counts.items())),
        "rows": events,
    }
