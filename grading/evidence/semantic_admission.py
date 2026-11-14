"""Fail-closed audit of semantic suggestions; not a model scoring gateway.

Two agreeing models are insufficient proof of technical truth. The canonical
deterministic relation must ALREADY be validated for a semantic suggestion to
be marked 'ALIGNED_WITH_DETERMINISTIC_EVIDENCE'. This module never changes A-E.
"""
from __future__ import annotations

from typing import Any, Mapping


class SemanticAdmissionError(ValueError):
    pass


def evaluate_semantic_admission(
    *, suggestion: Mapping[str, Any], review: Mapping[str, Any] | None,
    alignment: Mapping[str, Any], valid_fact_ids: set[str],
    source_span: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Return score-neutral disposition with safe reason codes."""
    fact_id = suggestion.get("fact_id")
    interpretation = suggestion.get("interpretation")
    if not isinstance(fact_id, str) or fact_id not in valid_fact_ids:
        raise SemanticAdmissionError("unscoped_fact")
    if interpretation not in {"supported", "partial", "contradicted", "unknown"}:
        raise SemanticAdmissionError("invalid_interpretation")
    if not isinstance(alignment, Mapping) or alignment.get("score_effect") != "none":
        raise SemanticAdmissionError("invalid_alignment_audit")

    status = "PENDING"
    reasons: list[str] = []
    valid_span = (
        isinstance(source_span, Mapping)
        and set(source_span) == {"start", "end"}
        and type(source_span["start"]) is int
        and type(source_span["end"]) is int
        and 0 <= source_span["start"] < source_span["end"]
    )
    if interpretation == "unknown":
        reasons.append("semantic_unknown")
    elif not isinstance(review, Mapping) or review.get("state") != "semantic_agreement":
        reasons.append("independent_review_not_agreed")
    elif review.get("fact_id") not in (None, fact_id):
        reasons.append("review_fact_mismatch")
    elif suggestion.get("missing_conditions"):
        reasons.append("missing_conditions")
    elif not valid_span:
        reasons.append("unbound_answer_span")
    else:
        matched = [
            row for row in alignment.get("alignments") or []
            if row.get("fact_id") == fact_id
            and row.get("source_span") == dict(source_span)
            and row.get("relation") == "EXACT_RELATION"
        ]
        if interpretation == "supported" and matched:
            status = "ALIGNED_WITH_DETERMINISTIC_EVIDENCE"
            reasons.append("canonical_relation_confirmed")
        else:
            reasons.append("semantic_proposal_not_deterministically_confirmed")
    return {
        "fact_id": fact_id,
        "proposed_interpretation": interpretation,
        "state": status,
        "reason_codes": reasons,
        "score_effect": "none",
        "final_grade_allowed": False,
    }
