"""Fail-closed comparison of independently reviewed semantic proposals.

No LLM output may assign a grade. Even identical conclusions from two models
are not technical proof; the same answer span and verified source-owned Fact
relation must also have been confirmed by the deterministic canonical parser.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class SemanticAdmissionError(ValueError):
    pass


def evaluate_semantic_admission(
    *, suggestion: Mapping[str, Any], review: Mapping[str, Any] | None,
    alignment: Mapping[str, Any], valid_fact_ids: set[str],
    source_span: Mapping[str, int] | None = None,
    answer_text: str | None = None,
) -> dict[str, Any]:
    """Diagnostic only: ALIGNED_WITH_DETERMINISTIC_EVIDENCE is NOT score approval."""
    fact_id = suggestion.get("fact_id")
    interpretation = suggestion.get("interpretation")
    if not isinstance(fact_id, str) or fact_id not in valid_fact_ids:
        raise SemanticAdmissionError("unscoped_or_unapproved_fact")
    if interpretation not in {"supported", "partial", "contradicted", "unknown"}:
        raise SemanticAdmissionError("invalid_interpretation")
    if not isinstance(alignment, Mapping) or alignment.get("score_effect") != "none":
        raise SemanticAdmissionError("invalid_alignment_audit")

    span_ok = (
        isinstance(source_span, Mapping)
        and set(source_span) == {"start", "end"}
        and type(source_span["start"]) is int
        and type(source_span["end"]) is int
        and source_span["start"] >= 0
        and source_span["end"] > source_span["start"]
    )
    quote = suggestion.get("quote")
    quote_ok = (
        span_ok and isinstance(answer_text, str)
        and isinstance(quote, str) and bool(quote.strip())
        and source_span["end"] <= len(answer_text)
        and quote in answer_text[source_span["start"]:source_span["end"]]
    )
    verified_projection = [
        f for f in alignment.get("fact_projection", [])
        if isinstance(f, Mapping) and f.get("fact_id") == fact_id
        and f.get("projection_status") == "VERIFIED_REGISTRY_RELATION"
        and f.get("source_fact_id")
    ]
    status = "PENDING"
    reason: str
    if interpretation == "unknown":
        reason = "semantic_unknown"
    elif not span_ok:
        reason = "unbound_answer_span"
    elif not quote_ok:
        reason = "unbound_or_foreign_quote"
    elif suggestion.get("missing_conditions"):
        reason = "missing_conditions"
    elif not isinstance(review, Mapping) or review.get("state") != "semantic_agreement":
        reason = "independent_review_not_agreed"
    elif review.get("fact_id") not in (None, fact_id):
        reason = "review_fact_mismatch"
    elif not verified_projection:
        reason = "unverified_fact_projection"
    else:
        matched = [
            row for row in alignment.get("alignments") or []
            if isinstance(row, Mapping)
            and row.get("fact_id") == fact_id
            and row.get("source_span") == dict(source_span)
            and row.get("relation") == "EXACT_RELATION"
        ]
        if interpretation == "supported" and matched:
            status = "ALIGNED_WITH_DETERMINISTIC_EVIDENCE"
            reason = "canonical_relation_confirmed"
        else:
            reason = "semantic_proposal_not_deterministically_confirmed"
    return {
        "fact_id": fact_id,
        "proposed_interpretation": interpretation,
        "state": status,
        "reason_codes": [reason],
        "score_effect": "none",
        "final_grade_allowed": False,
    }
