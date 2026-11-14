"""Research-only literal surface probes for approved Registry Fact relations.

This is NOT a canonical claim parser or a semantic equivalence resolver.
Lexical subject/predicate/object co-occurrence is insufficient for credit.
The existing grader, parser, Fact registry and scoring exclusions are untouched.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Any, Mapping

from grading.evidence.canonical_claim_extractor import (
    _SENTENCE, _assertion_context, _find_alias, _find_subject_alias,
    _load_aliases, _load_predicates, _object_before_subject_allowed,
    _polarity, _same_clause,
)
from grading.evidence.claim_alignment_contract import validate_alignment_result

VERSION = "registry_surface_recall_audit.v1"
REVIEW = "REVIEW_LITERAL_TRIPLET_ONLY"
_HOLDS = frozenset({
    "HOLD_NONASSERTED_CONTEXT",
    "HOLD_NEGATED_RELATION",
    "HOLD_ABSOLUTE_QUANTIFIER",
    "HOLD_REQUIRED_CONDITIONS",
    "HOLD_AMBIGUOUS_WORD_ORDER",
})
_UNIVERSALS = ("항상", "무조건", "언제나", "always", "never", "unconditionally")


def _fingerprint(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def audit_registry_surface_recall(
    *, question_text: str, answer_text: str, alignment: Mapping[str, Any],
) -> dict[str, Any]:
    """Identify literal review targets using independently verified Fact projections.

    Subject, predicate and object must be visible in a *single sentence*.
    Even those review targets remain unverified: owner, scope, negation,
    corrections and technical meaning still require independent adjudication.
    """
    if not isinstance(question_text, str) or not isinstance(answer_text, str):
        raise ValueError("invalid input text")
    checked = validate_alignment_result(dict(alignment), answer_text=answer_text)
    aliases, predicates = _load_aliases(), _load_predicates()
    question_sha = hashlib.sha256(question_text.encode("utf-8")).hexdigest()
    answer_sha = checked["answer_sha256"]
    verified_facts = [
        row for row in checked["fact_projection"]
        if (row.get("projection_status") == "VERIFIED_REGISTRY_RELATION"
            and row.get("source_fact_id")
            and row.get("relation_source") == "verified_registry"
            and isinstance(row.get("relation"), dict))
    ]
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    seen: set[tuple[str, str, int, int]] = set()
    for fact in verified_facts:
        relation = fact["relation"]
        subject_id, predicate_id, object_id = (
            relation["subject"], relation["predicate"], relation["object"]
        )
        subject_aliases = aliases.get(subject_id, [])
        predicate_aliases = predicates.get(predicate_id, [])
        object_aliases = aliases.get(object_id, [])
        if not (subject_aliases and predicate_aliases and object_aliases):
            counts["ALIAS_INVENTORY_INCOMPLETE"] += 1
            continue
        matched_literal = False
        for sentence_match in _SENTENCE.finditer(answer_text):
            sentence = sentence_match.group()
            subject = _find_subject_alias(sentence, subject_aliases, predicate_id)
            predicate = (
                _find_alias(sentence, predicate_aliases, start_at=subject[1])
                if subject is not None else None
            )
            obj = _find_alias(sentence, object_aliases)
            if subject is None or predicate is None or obj is None:
                continue
            if not _same_clause(sentence, subject, obj):
                continue
            matched_literal = True
            if (
                obj[0] < subject[0]
                and not _object_before_subject_allowed(
                    sentence, subject, obj, predicate_id
                )
            ):
                disposition = "HOLD_AMBIGUOUS_WORD_ORDER"
            elif _assertion_context(sentence, max(subject[1], obj[1])) != "asserted":
                disposition = "HOLD_NONASSERTED_CONTEXT"
            elif _polarity(sentence, obj, predicate, predicate_id) != relation["polarity"]:
                disposition = "HOLD_NEGATED_RELATION"
            elif any(token in sentence.casefold() for token in _UNIVERSALS):
                disposition = "HOLD_ABSOLUTE_QUANTIFIER"
            elif relation["conditions"]:
                # The existing concept alias extraction of conditions is not
                # strong enough to certify their scope. Always hold conditional
                # Registry facts pending expert review, even if words overlap.
                disposition = "HOLD_REQUIRED_CONDITIONS"
            else:
                disposition = REVIEW
            if disposition != REVIEW and disposition not in _HOLDS:
                raise ValueError("unexpected shadow review disposition")
            span = {"start": sentence_match.start(), "end": sentence_match.end()}
            identity = (
                fact["owner_topic_id"], fact["fact_id"], span["start"], span["end"]
            )
            if identity in seen:
                continue
            seen.add(identity)
            counts[disposition] += 1
            candidate_identity = {
                "question_sha256": question_sha,
                "answer_sha256": answer_sha,
                "owner_topic_id": fact["owner_topic_id"],
                "fact_id": fact["fact_id"],
                "source_fact_id": fact["source_fact_id"],
                "source_span": span,
                "relation": relation,
                "disposition": disposition,
            }
            rows.append({
                "candidate_id": _fingerprint(candidate_identity),
                "owner_topic_id": fact["owner_topic_id"],
                "fact_id": fact["fact_id"],
                "source_fact_id": fact["source_fact_id"],
                "source_span": span,
                "review_disposition": disposition,
                "score_effect": "none",
            })
        if not matched_literal:
            counts["NO_LITERAL_TRIPLET"] += 1
    if len(rows) != len({row["candidate_id"] for row in rows}):
        raise ValueError("duplicate literal probe identity")
    rows.sort(key=lambda row: (
        row["owner_topic_id"], row["fact_id"],
        row["source_span"]["start"], row["source_span"]["end"],
    ))
    return {
        "schema_version": VERSION,
        "status": "LITERAL_SURFACE_AUDIT_ONLY",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "final_grade_allowed": False,
        "question_sha256": question_sha,
        "answer_sha256": answer_sha,
        "verified_fact_projection_count": len(verified_facts),
        "review_literal_candidate_count": counts[REVIEW],
        "hold_candidate_count": sum(counts[key] for key in _HOLDS),
        "disposition_counts": dict(sorted(counts.items())),
        "rows": rows,
        "limitations": [
            "Literal surface matches are not independent technical validation",
            "Neither a matched relation nor a zero count establishes grading correctness",
            "Conditional facts, negation and nonasserted context never receive credit",
        ],
    }
