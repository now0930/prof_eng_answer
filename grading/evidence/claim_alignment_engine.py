"""Relational alignment audit across existing source-owned Fact/Logic/Answer layers.

The existing deterministic requirement evaluator is STILL the authority for
SATISFIED/PARTIAL/WRONG and all scores. This module does not infer correctness
from keyword overlap and never evaluates free-form Logic Check regex as fatal.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any, Iterable

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.claim_alignment_contract import (
    build_alignment_result, canonical_relation,
)
from grading.evidence.fact_claim_adapter import project_fact_claims
from grading.evidence.logic_rule_adapter import project_logic_rules

ASSERTED = "asserted"
_UNQUALIFIED_UNIVERSAL = re.compile(
    r"(?<![a-z])(?:always|never|unconditionally)(?![a-z])|항상|무조건|언제나",
    re.IGNORECASE,
)


def _compare(fact: dict[str, Any], claim: dict[str, Any]) -> tuple[str, str] | None:
    """Compare only canonicalized, asserted relations; uncertainty stays explicit."""
    f = fact.get("relation")
    if f is None:
        return None
    if claim.get("assertion_context") != ASSERTED:
        return None
    a = canonical_relation(claim)
    if any(a[key] != f[key] for key in ("subject", "predicate", "object")):
        return None
    if (fact.get("projection_status") != "VERIFIED_REGISTRY_RELATION"
            or not fact.get("source_fact_id")):
        return ("UNRESOLVED", "source_relation_not_independently_verified")
    if a["polarity"] != f["polarity"]:
        return ("CONTRADICTION_CANDIDATE", "opposite_relation_polarity")
    # Canonical triplets alone do not establish the truth of a universal claim.
    # Use the existing Logic Check/invariant owner for such assertions.
    if _UNQUALIFIED_UNIVERSAL.search(str(claim.get("source_text") or "")):
        return ("UNRESOLVED", "absolute_quantifier_requires_logic_verification")
    # The question may supply conditions, but this audit never invents them.
    if not set(f["conditions"]).issubset(a["conditions"]):
        return ("CONDITION_GAP", "fact_conditions_not_asserted")
    return ("EXACT_RELATION", "canonical_relation_matches")


def analyze_claim_alignment(
    *, question_text: str, answer_text: str, topic_ids: Iterable[str],
    parser_output: Mapping[str, Any] | None = None,
    required_by_topic: dict[str, set[str]] | None = None,
) -> dict[str, Any]:
    """Read-only snapshot; no model calls, no grade changes, no raw answer copying."""
    topics = sorted(set(str(t) for t in topic_ids if str(t)))
    if parser_output is None:
        parser_output = extract_canonical_claim_evidence(
            answer_text, question_text=question_text, topic_ids=topics,
        )
    document = parser_output.get("canonical_evidence") or {}
    expected_sha = document.get("input_fingerprint", {}).get("answer_sha256")
    if expected_sha is None:
        raise ValueError("missing canonical answer fingerprint")
    import hashlib
    if expected_sha != hashlib.sha256(answer_text.encode("utf-8")).hexdigest():
        raise ValueError("stale or foreign canonical answer document")
    claims = document.get("claims")
    if not isinstance(claims, list):
        raise ValueError("canonical claims missing")
    facts = project_fact_claims(topics, required_by_topic=required_by_topic)
    logic = project_logic_rules(topics)
    aligned = []
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        span = claim.get("source_span")
        if not isinstance(span, dict):
            continue
        start, end = span.get("start"), span.get("end")
        if (type(start) is not int or type(end) is not int or start < 0
                or end <= start or end > len(answer_text)
                or answer_text[start:end] != claim.get("source_text")):
            raise ValueError("canonical claim span mismatch")
        for fact in facts:
            candidate = _compare(fact, claim)
            if candidate is None:
                continue
            relation, reason = candidate
            aligned.append({
                "answer_claim_id": str(claim["claim_id"]),
                "fact_id": fact["fact_id"],
                "owner_topic_id": fact["owner_topic_id"],
                "relation": relation,
                "reason": reason,
                "source_span": {"start": start, "end": end},
            })
    unresolved = []
    for span in parser_output.get("unresolved_spans") or []:
        if not isinstance(span, dict):
            continue
        start, end = span.get("start"), span.get("end")
        if (type(start) is not int or type(end) is not int or start < 0
                or end <= start or end > len(answer_text)
                or answer_text[start:end] != span.get("source_text")):
            raise ValueError("unresolved span mismatch")
        unresolved.append({
            "source_span": {"start": start, "end": end},
            "reason": "deterministic_parser_unresolved",
            "concept_count": len(span.get("concept_candidates") or []),
        })
    # Do not persist the original Fact statements or answer fragments in audit metadata.
    return build_alignment_result(
        answer_text=answer_text,
        topic_ids=topics,
        fact_projection=facts,
        logic_projection=logic,
        alignments=aligned,
        unresolved=unresolved,
    )
