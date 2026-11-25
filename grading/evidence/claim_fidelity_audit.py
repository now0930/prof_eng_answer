"""Non-scoring checks for source-to-claim fidelity in P2 diagnostics.

This module does not determine technical correctness.  It only blocks a
relation comparison when the extracted relation is contradicted by explicit
source structure or when its evidence cannot be grounded.
"""

from __future__ import annotations

import re
from typing import Any


_ARITHMETIC = {
    "addition": re.compile(r"(?:의\s*합(?:이다|으로|으로?\s*계산)?|더한|더해|더하여|더하면|더하는|plus|sum(?:\s+of)?|added\s+to)", re.I),
    "multiplication": re.compile(r"(?:곱(?:이다|한다|으로|을|은|이)?|곱하|곱한|times|multipl(?:y|ied)|product\s+of)", re.I),
    "division": re.compile(r"(?:나누(?:다|면|어|어야|는|ㄴ)|분의|divid(?:e|ed)\s+by|over)", re.I),
}


def relation_operation(text: str) -> str | None:
    """Return an explicitly stated arithmetic operation, if unambiguous."""
    found = [name for name, pattern in _ARITHMETIC.items() if pattern.search(text)]
    return found[0] if len(found) == 1 else None


def assess_claim_fidelity(
    *, answer_text: str, claim: dict[str, Any], topic_id: str,
    expected_claim: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assess whether a parser claim is grounded in its answer span.

    ``expected_claim`` is optional research-fixture metadata.  A PASS means
    only that the extracted representation matches that proposed relation
    and passes the local grounding checks; it is not an independent semantic
    label or a score decision.
    """
    span = claim.get("source_span") or {}
    start, end = span.get("start"), span.get("end")
    if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(answer_text):
        return {"status": "FAIL", "reason": "INVALID_SOURCE_SPAN", "score_effect": "none"}
    source = answer_text[start:end]
    if source != claim.get("source_text"):
        return {"status": "FAIL", "reason": "SOURCE_TEXT_MISMATCH", "score_effect": "none"}
    qualifiers = claim.get("qualifiers", {})
    if qualifiers.get("owner_topic_id", topic_id) != topic_id:
        return {"status": "FAIL", "reason": "OWNER_MISMATCH", "score_effect": "none"}
    if claim.get("assertion_context") not in {"asserted", "corrected"}:
        return {"status": "NOT_ESTABLISHED", "reason": "NOT_ADOPTED_ASSERTION", "score_effect": "none"}
    if qualifiers.get("context_inferred_subject") not in {None, False, "False"}:
        return {"status": "NOT_ESTABLISHED", "reason": "INFERRED_SUBJECT", "score_effect": "none"}

    operation = relation_operation(source)
    # Arithmetic words are stronger evidence than the extractor's generic
    # copula alias.  A sum/division cannot be normalized as a generic equality.
    if operation and claim.get("predicate") == "equivalent_to":
        expected_object = (expected_claim or {}).get("object")
        if operation == "addition":
            return {"status": "FAIL", "reason": "OPERATION_NOT_EQUIVALENCE", "observed_operation": operation, "score_effect": "none"}
        if operation == "division" and expected_object not in {"residual_tolerable_frequency_ratio"}:
            return {"status": "FAIL", "reason": "OPERATION_TARGET_MISMATCH", "observed_operation": operation, "score_effect": "none"}
    if expected_claim is None:
        return {"status": "NOT_ESTABLISHED", "reason": "NO_GROUNDED_TARGET_RELATION", "score_effect": "none"}

    # Polarity is intentionally not compared with the Fact here: opposite
    # polarity can be a faithful, technically contradictory Claim.  The
    # caller's relation comparator handles that after source fidelity passes.
    fields = ("subject", "predicate", "object")
    mismatched = [key for key in fields if claim.get(key) != expected_claim.get(key)]
    expected_conditions = set(expected_claim.get("conditions", []))
    actual_conditions = set(claim.get("conditions", []))
    if not expected_conditions <= actual_conditions:
        mismatched.append("conditions")
    if mismatched:
        return {"status": "FAIL", "reason": "CLAIM_TARGET_MISMATCH", "mismatched_fields": mismatched, "score_effect": "none"}
    if operation == "addition":
        return {"status": "FAIL", "reason": "OPERATION_NOT_EQUIVALENCE", "observed_operation": operation, "score_effect": "none"}
    return {
        "status": "NOT_ESTABLISHED",
        "reason": "SURFACE_SCHEMA_MATCH_NOT_SEMANTIC_PROOF",
        "observed_operation": operation,
        "score_effect": "none",
    }
