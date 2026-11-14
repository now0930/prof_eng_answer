"""Score-neutral shared claim alignment contract.

This is a projection/audit boundary, not a second grade engine. Facts, learner
claims and forbidden rules keep distinct ownership; no model may assign grades,
WRONG, fatal or score ceilings through this module.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

VERSION = "claim_alignment.v1"
_ALLOWED_CONTEXT = frozenset({"asserted", "quoted", "rejected", "corrected"})
_ALLOWED_POLARITY = frozenset({"positive", "negative"})
_RELATIONS = frozenset({
    "EXACT_RELATION", "CONDITION_GAP", "CONTRADICTION_CANDIDATE",
    "UNRESOLVED",
})


class ClaimAlignmentError(ValueError):
    pass


def _id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ClaimAlignmentError(f"{field}: nonempty identifier required")
    return value.strip().casefold()


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False,
                   separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def canonical_relation(value: Mapping[str, Any]) -> dict[str, Any]:
    """Keep only engineering relation fields. Reject invalid, never invent."""
    if not isinstance(value, Mapping):
        raise ClaimAlignmentError("relation must be a mapping")
    conditions = value.get("conditions") or []
    if not isinstance(conditions, list) or any(not isinstance(c, str) for c in conditions):
        raise ClaimAlignmentError("invalid condition list")
    polarity = value.get("polarity", "positive")
    if polarity not in _ALLOWED_POLARITY:
        raise ClaimAlignmentError("invalid polarity")
    return {
        "subject": _id(value.get("subject"), "subject"),
        "predicate": _id(value.get("predicate"), "predicate"),
        "object": _id(value.get("object"), "object"),
        "polarity": polarity,
        "conditions": sorted({_id(c, "condition") for c in conditions}),
    }


def validate_alignment_result(
    result: Any, *, answer_text: str, selected_fact_ids: set[str] | None = None
) -> dict[str, Any]:
    if not isinstance(result, dict) or set(result) != {
        "schema_version", "authority", "score_effect", "answer_sha256",
        "topic_ids", "fact_projection", "logic_projection", "alignments",
        "unresolved", "summary", "fingerprint",
    }:
        raise ClaimAlignmentError("alignment result fields mismatch")
    if result["schema_version"] != VERSION or result["authority"] != "audit_only":
        raise ClaimAlignmentError("alignment may not own grading authority")
    if result["score_effect"] != "none":
        raise ClaimAlignmentError("alignment cannot change scores")
    if result["answer_sha256"] != hashlib.sha256(answer_text.encode("utf-8")).hexdigest():
        raise ClaimAlignmentError("answer fingerprint mismatch")
    if not isinstance(result["topic_ids"], list) or not isinstance(result["fact_projection"], list):
        raise ClaimAlignmentError("invalid projection")
    if not isinstance(result["logic_projection"], list) or not isinstance(result["alignments"], list):
        raise ClaimAlignmentError("invalid alignments")
    if not isinstance(result["unresolved"], list):
        raise ClaimAlignmentError("invalid unresolved claims")
    if not isinstance(result["summary"], dict):
        raise ClaimAlignmentError("invalid summary")
    projected_facts = {
        (row.get("owner_topic_id"), row.get("fact_id"))
        for row in result["fact_projection"] if isinstance(row, dict)
    }
    selected_topics = set(result["topic_ids"])
    if any(topic not in selected_topics for topic, _ in projected_facts):
        raise ClaimAlignmentError("fact projection outside topic scope")
    for row in result["alignments"]:
        if not isinstance(row, dict) or set(row) != {
            "answer_claim_id", "fact_id", "owner_topic_id", "relation",
            "reason", "source_span",
        }:
            raise ClaimAlignmentError("invalid alignment row")
        if row["relation"] not in _RELATIONS:
            raise ClaimAlignmentError("invalid relation label")
        if (row["owner_topic_id"], row["fact_id"]) not in projected_facts:
            raise ClaimAlignmentError("alignment references non-projected fact")
        if selected_fact_ids is not None and row["fact_id"] not in selected_fact_ids:
            raise ClaimAlignmentError("out-of-scope fact")
        span = row["source_span"]
        if not isinstance(span, dict) or set(span) != {"start", "end"}:
            raise ClaimAlignmentError("invalid answer span")
        start, end = span["start"], span["end"]
        if (type(start) is not int or type(end) is not int
                or start < 0 or start >= end or end > len(answer_text)):
            raise ClaimAlignmentError("answer span out of bounds")
    copy = {key: value for key, value in result.items() if key != "fingerprint"}
    if result["fingerprint"] != _sha(copy):
        raise ClaimAlignmentError("alignment fingerprint mismatch")
    return result


def build_alignment_result(
    *, answer_text: str, topic_ids: list[str], fact_projection: list[dict[str, Any]],
    logic_projection: list[dict[str, Any]], alignments: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create stable, replayable audit metadata without copying answer text."""
    counts = {label: sum(row["relation"] == label for row in alignments)
              for label in sorted(_RELATIONS)}
    obj = {
        "schema_version": VERSION,
        "authority": "audit_only",
        "score_effect": "none",
        "answer_sha256": hashlib.sha256(answer_text.encode("utf-8")).hexdigest(),
        "topic_ids": sorted(set(topic_ids)),
        "fact_projection": sorted(fact_projection, key=lambda x: (x["owner_topic_id"], x["fact_id"])),
        "logic_projection": sorted(logic_projection, key=lambda x: (x["owner_topic_id"], x["rule_id"])),
        "alignments": sorted(alignments, key=lambda x: (
            x["source_span"]["start"], x["source_span"]["end"],
            x["answer_claim_id"], x["owner_topic_id"], x["fact_id"],
        )),
        "unresolved": sorted(unresolved, key=lambda x: (
            x["source_span"]["start"], x["source_span"]["end"],
        )),
        "summary": {
            "fact_count": len(fact_projection),
            "logic_rule_count": len(logic_projection),
            "alignment_count": len(alignments),
            "unresolved_count": len(unresolved),
            "relation_counts": counts,
        },
    }
    obj["fingerprint"] = _sha(obj)
    return validate_alignment_result(obj, answer_text=answer_text)
