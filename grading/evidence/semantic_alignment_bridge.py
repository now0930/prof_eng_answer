"""Join private, independently reviewed semantic suggestions with Claim Alignment.

This is a score-neutral, source-bound audit. The LLM's interpretation can
highlight misses of the deterministic parser, but cannot award B/C credit,
trigger Fatal, revise Fact verification, or override a Logic Check.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Mapping
from typing import Any

from grading.evidence.claim_alignment_contract import (
    ClaimAlignmentError, canonical_relation, validate_alignment_result,
)
from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.canonical_grading_evidence import validate_canonical_grading_evidence
from grading.evidence.claim_alignment_engine import _compare
from grading.evidence.semantic_admission import evaluate_semantic_admission
from grading.evidence.fact_grounded_contracts import fingerprint


class SemanticAlignmentBridgeError(ValueError):
    pass


def _fresh_confirmed_relations(
    *, question: str, answer: str, alignment: Mapping[str, Any],
) -> set[tuple[str, str, str, int, int]]:
    """Recheck purported EXACT rows against freshly extracted answer claims.

    An audit digest only detects mutation; an attacker can mint a fresh digest
    for a fabricated EXACT row. Never elevate that row to even a confirmed
    diagnostic state without independently recreating its parsed relation.
    """
    try:
        parsed = extract_canonical_claim_evidence(
            answer, question_text=question, topic_ids=alignment["topic_ids"],
        )
        document = validate_canonical_grading_evidence(
            parsed["canonical_evidence"], answer_text=answer,
        )
    except Exception:
        # Auditing is advisory. Parser failure makes every purported EXACT
        # relation pending, never a false confirmation or grading failure.
        return set()
    expected = document.get("input_fingerprint") or {}
    if (expected.get("question_sha256") != hashlib.sha256(question.encode()).hexdigest()
            or expected.get("answer_sha256") != hashlib.sha256(answer.encode()).hexdigest()
            or (document.get("source") or {}).get("mode") != "deterministic_parser"):
        return set()
    claims = {
        row.get("claim_id"): row
        for row in document["claims"]
        if isinstance(row, Mapping)
    }
    projected = {
        (row.get("owner_topic_id"), row.get("fact_id")): row
        for row in alignment["fact_projection"]
        if isinstance(row, Mapping)
        and row.get("projection_status") == "VERIFIED_REGISTRY_RELATION"
        and row.get("source_fact_id")
    }
    confirmed: set[tuple[str, str, str, int, int]] = set()
    for row in alignment["alignments"]:
        if row.get("relation") != "EXACT_RELATION":
            continue
        fact = projected.get((row["owner_topic_id"], row["fact_id"]))
        claim = claims.get(row["answer_claim_id"])
        if not fact or not claim or claim.get("source_span") != row["source_span"]:
            continue
        start, end = row["source_span"]["start"], row["source_span"]["end"]
        if claim.get("source_text") != answer[start:end]:
            continue
        if _compare(fact, claim) != ("EXACT_RELATION", "canonical_relation_matches"):
            continue
        confirmed.add((
            row["owner_topic_id"], row["fact_id"],
            row["answer_claim_id"], start, end,
        ))
    return confirmed


def link_private_semantic_report(
    *, question: str, answer: str, report: Mapping[str, Any],
    alignment: Mapping[str, Any], approved_facts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Join only exact source spans, verified fact IDs and reviewed interpretations."""
    if (report.get("schema_version") != "semantic-assist-private-run-v1"
            or report.get("question_sha256") != hashlib.sha256(question.encode()).hexdigest()
            or report.get("answer_sha256") != hashlib.sha256(answer.encode()).hexdigest()
            or report.get("score_effect") != "none"
            or report.get("final_grade_allowed") is not False):
        raise SemanticAlignmentBridgeError("untrusted_or_stale_semantic_report")
    result = report.get("result")
    if (not isinstance(result, Mapping)
            or result.get("score_effect") != "none"
            or result.get("final_grade_allowed") is not False):
        raise SemanticAlignmentBridgeError("semantic_result_has_authority")
    assistance = result.get("assistance") or {}
    items = assistance.get("items")
    if not isinstance(items, list):
        raise SemanticAlignmentBridgeError("semantic_items_missing")
    if (alignment.get("score_effect") != "none"
            or alignment.get("answer_sha256") != report.get("answer_sha256")):
        raise SemanticAlignmentBridgeError("alignment_source_mismatch")
    try:
        validate_alignment_result(dict(alignment), answer_text=answer)
    except ClaimAlignmentError as error:
        raise SemanticAlignmentBridgeError("invalid_alignment_contract") from error
    if report.get("facts_sha256") != fingerprint(
        sorted(approved_facts, key=lambda fact: fact["fact_id"])
    ):
        raise SemanticAlignmentBridgeError("stale_or_foreign_fact_registry_snapshot")
    registry = {}
    for fact in approved_facts:
        if fact.get("review_status") != "approved" or fact.get("verification_status") != "verified":
            continue
        registry[fact["fact_id"]] = fact
    projection = {
        (row.get("owner_topic_id"), row.get("source_fact_id")): row
        for row in alignment.get("fact_projection", [])
        if isinstance(row, Mapping)
        and row.get("projection_status") == "VERIFIED_REGISTRY_RELATION"
    }

    # Use a fresh deterministic parse, not caller-supplied EXACT labels, to
    # justify the diagnostic ALIGNED_WITH_DETERMINISTIC_EVIDENCE state.
    fresh_exact = _fresh_confirmed_relations(
        question=question, answer=answer, alignment=alignment,
    )
    summaries: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for item in items:
        if not isinstance(item, Mapping):
            raise SemanticAlignmentBridgeError("invalid_item")
        span = item.get("source_span")
        if (not isinstance(span, Mapping) or set(span) != {"start", "end"}
                or type(span["start"]) is not int or type(span["end"]) is not int
                or not 0 <= span["start"] < span["end"] <= len(answer)):
            raise SemanticAlignmentBridgeError("missing_or_invalid_parser_span")
        proposals = item.get("proposals") or []
        if not isinstance(proposals, list):
            raise SemanticAlignmentBridgeError("invalid_proposals")
        review_doc = item.get("semantic_review") or {}
        reviews = {
            row.get("fact_id"): row
            for row in review_doc.get("rows", [])
            if isinstance(row, Mapping)
        }
        for proposal in proposals:
            if not isinstance(proposal, Mapping):
                raise SemanticAlignmentBridgeError("invalid_proposal")
            source_fact_id = proposal.get("fact_id")
            source_fact = registry.get(source_fact_id)
            if source_fact is None:
                raise SemanticAlignmentBridgeError("unapproved_fact_in_proposal")
            projected = projection.get((source_fact["topic_id"], source_fact_id))
            if projected is None:
                state = "PENDING"
                reasons = ["fact_outside_verified_question_scope"]
                legacy_anchor_id = str(source_fact.get("legacy_anchor_id") or "")
            elif (
                not isinstance(source_fact.get("relation"), Mapping)
                or projected.get("owner_topic_id") != source_fact["topic_id"]
                or projected.get("fact_id") != str(
                    source_fact.get("legacy_anchor_id") or source_fact_id
                )
                or projected.get("parent_anchor_id") != projected.get("fact_id")
                or projected.get("relation_source") != "verified_registry"
                or projected.get("relation") != canonical_relation({
                    **source_fact["relation"], "polarity": "positive",
                })
            ):
                # The approved source Fact, not a caller-supplied audit label,
                # determines whether a relation is independently verified.
                state = "PENDING"
                reasons = ["source_relation_mismatch"]
                legacy_anchor_id = str(source_fact.get("legacy_anchor_id") or "")
            else:
                legacy_anchor_id = projected["fact_id"]
                review = reviews.get(source_fact_id)
                mapped_review = ({
                    "fact_id": legacy_anchor_id,
                    "state": review.get("state"),
                } if review else None)
                mapped_proposal = {
                    "fact_id": legacy_anchor_id,
                    "interpretation": proposal.get("interpretation"),
                    "quote": proposal.get("quote"),
                    "missing_conditions": proposal.get("missing_conditions"),
                }
                disposition = evaluate_semantic_admission(
                    suggestion=mapped_proposal, review=mapped_review,
                    alignment=alignment, valid_fact_ids={legacy_anchor_id},
                    source_span=span, answer_text=answer,
                )
                state = disposition["state"]
                reasons = disposition["reason_codes"]
                if state == "ALIGNED_WITH_DETERMINISTIC_EVIDENCE":
                    exact_rows = (
                        row for row in alignment["alignments"]
                        if row.get("owner_topic_id") == source_fact["topic_id"]
                        and row.get("fact_id") == legacy_anchor_id
                        and row.get("relation") == "EXACT_RELATION"
                        and row.get("source_span") == dict(span)
                    )
                    if not any(
                        (row["owner_topic_id"], row["fact_id"],
                         row["answer_claim_id"], span["start"], span["end"])
                        in fresh_exact
                        for row in exact_rows
                    ):
                        state = "PENDING"
                        reasons = ["fresh_canonical_relation_not_confirmed"]
            counts[state] += 1
            summaries.append({
                "source_fact_id": source_fact_id,
                "legacy_anchor_id": legacy_anchor_id,
                "requirement_id": item.get("requirement_id"),
                "source_span": dict(span),
                "proposed_interpretation": proposal.get("interpretation"),
                "state": state,
                "reason_codes": reasons,
                "score_effect": "none",
            })
    return {
        "schema_version": "semantic_alignment_bridge.v1",
        "status": "AUDIT_ONLY",
        "score_effect": "none",
        "final_grade_allowed": False,
        "question_sha256": report["question_sha256"],
        "answer_sha256": report["answer_sha256"],
        "review_count": len(summaries),
        "disposition_counts": dict(sorted(counts.items())),
        "rows": summaries,
    }
