"""Explain why independently verified Fact relations do not match parsed Claims.

Strictly diagnostic. Never upgrades UNKNOWN/PARTIAL/MISSING, and never decides
WRONG, Fatal, passing status or the A/B/C score.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Mapping
from typing import Any

from grading.evidence.canonical_grading_evidence import (
    validate_canonical_grading_evidence,
)
from grading.evidence.claim_alignment_contract import (
    canonical_relation, validate_alignment_result,
)

VERSION = "claim_alignment_gap_diagnostics.v1"

# Priority matters: a compatible triple that still needs claim scope/condition
# verification must never be called an approved scoring relation.
_CATEGORIES = (
    "NO_ASSERTED_CLAIMS_FOR_TOPIC",
    "NO_SUBJECT_MATCH",
    "SUBJECT_ONLY",
    "SUBJECT_PREDICATE_ONLY",
    "TRIPLE_POLARITY_DIFFERS",
    "TRIPLE_CONDITIONS_INCOMPLETE",
    "TRIPLE_COMPATIBLE_AUDIT_ONLY",
)


def diagnose_claim_fact_relation_gap(
    *, question_text: str, answer_text: str,
    canonical_evidence: Mapping[str, Any],
    alignment: Mapping[str, Any],
) -> dict[str, Any]:
    """Return counts only; no answer text, claim text or inferred equivalence."""
    document = validate_canonical_grading_evidence(
        dict(canonical_evidence), answer_text=answer_text,
    )
    checked = validate_alignment_result(dict(alignment), answer_text=answer_text)
    fingerprints = document.get("input_fingerprint") or {}
    if document.get("source", {}).get("mode") != "deterministic_parser":
        raise ValueError("diagnosis requires independently deterministic Claims")
    if (fingerprints.get("question_sha256")
            != hashlib.sha256(question_text.encode("utf-8")).hexdigest()
            or fingerprints.get("answer_sha256") != checked["answer_sha256"]):
        raise ValueError("foreign question or answer in diagnosis")
    claims = document["claims"]
    asserted = [row for row in claims if row["assertion_context"] == "asserted"]
    mentioned_only_count = sum(
        row["predicate"] == "mentioned" for row in asserted
    )
    fact_categories: Counter[str] = Counter()
    verified_count = 0
    machine_different = 0
    for fact in checked["fact_projection"]:
        if (fact.get("projection_status") != "VERIFIED_REGISTRY_RELATION"
                or not fact.get("source_fact_id")):
            continue
        verified_count += 1
        machine_different += bool(fact.get("machine_relation_differs"))
        relation = fact.get("relation")
        if not isinstance(relation, Mapping):
            fact_categories["VERIFIED_RELATION_MISSING"] += 1
            continue
        expected = canonical_relation(relation)
        topic = fact["owner_topic_id"]
        scoped = [
            claim for claim in asserted
            if not (claim.get("qualifiers") or {}).get("owner_topic_id")
            or (claim.get("qualifiers") or {}).get("owner_topic_id") == topic
        ]
        if not scoped:
            category = "NO_ASSERTED_CLAIMS_FOR_TOPIC"
        else:
            subjects = [
                canonical_relation(row) for row in scoped
                if row["subject"] == expected["subject"]
            ]
            if not subjects:
                category = "NO_SUBJECT_MATCH"
            else:
                predicates = [
                    row for row in subjects
                    if row["predicate"] == expected["predicate"]
                ]
                if not predicates:
                    category = "SUBJECT_ONLY"
                else:
                    triples = [
                        row for row in predicates
                        if row["object"] == expected["object"]
                    ]
                    if not triples:
                        category = "SUBJECT_PREDICATE_ONLY"
                    elif all(row["polarity"] != expected["polarity"] for row in triples):
                        category = "TRIPLE_POLARITY_DIFFERS"
                    elif not any(
                        set(expected["conditions"]).issubset(row["conditions"])
                        for row in triples
                        if row["polarity"] == expected["polarity"]
                    ):
                        category = "TRIPLE_CONDITIONS_INCOMPLETE"
                    else:
                        # Compatibility does not verify assertion scope,
                        # universal-quantifier correctness or approved meaning.
                        category = "TRIPLE_COMPATIBLE_AUDIT_ONLY"
        fact_categories[category] += 1
    if sum(fact_categories.values()) != verified_count:
        raise ValueError("diagnostic accounting mismatch")
    return {
        "schema_version": VERSION,
        "status": "DIAGNOSTIC_ONLY",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "final_grade_allowed": False,
        "claim_count": len(claims),
        "asserted_claim_count": len(asserted),
        "mentioned_only_claim_count": mentioned_only_count,
        "verified_fact_count": verified_count,
        "verified_machine_relation_differs_count": machine_different,
        "fact_relation_gap_counts": dict(sorted(fact_categories.items())),
        "full_fact_coverage_not_established": True,
    }
