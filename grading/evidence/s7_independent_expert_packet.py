"""Prepare private, source-referenced, label-hidden S7 expert review material.

Not part of CI. A reviewer must independently judge authored draft answers and
write NEW cases; generating this packet does not create expert labels.
Never automatically admit any outcome to canonical scoring or ontology.
"""
from __future__ import annotations

import hashlib
import json
import secrets
from typing import Any, Callable

from grading.evidence.s7_remaining_five_expert_queue import SCOPE, VERSION as QUEUE_VERSION


def _sha256_manifest(rows: list[dict[str, str]]) -> str:
    payload = json.dumps(
        sorted(rows, key=lambda r: r["review_item_id"]),
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def prepare_private_expert_review_packet(
    source_review: dict[str, Any],
    queue: dict[str, Any],
    challenge: dict[str, Any],
    *,
    token_factory: Callable[[], str] | None = None,
    shuffle: Callable[[list[Any]], None] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Create an unlabeled private packet and *separate*, sealed author-side map.

    The returned packet contains source statements and authored answer text; it
    must never be committed or uploaded as a GitHub Actions artifact.
    """
    if (
        source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
        or source_review.get("status") != "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
        or queue.get("schema_version") != QUEUE_VERSION
        or queue.get("status") != "FIVE_UNPROBED_FACTS_QUEUED_FOR_INDEPENDENT_REVIEW"
        or challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
        or challenge.get("adjudication_status") != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
        or source_review.get("score_admission") != "DISABLED"
        or source_review.get("score_effect") != "none"
        or queue.get("score_admission") != "DISABLED"
        or queue.get("score_effect") != "none"
        or queue.get("candidate_decision") != "HOLD"
        or queue.get("automatic_alias_admission") is not False
        or queue.get("source_inventory_execution_sha")
        != source_review.get("inventory_execution_sha")
        or queue.get("execution_commit_sha")
        != source_review.get("inventory_execution_sha")
        or queue.get("queued_fact_count") != 5
        or queue.get("authored_draft_answer_count") != 10
        or queue.get("independently_labeled_answer_count") != 0
    ):
        raise ValueError("cannot package expert material from unverified/success-claimed evidence")
    sr = source_review.get("rows")
    qr = queue.get("rows")
    cr = challenge.get("cases")
    if not (isinstance(sr, list) and isinstance(qr, list) and isinstance(cr, list)):
        raise ValueError("source/queue/challenge rows missing")
    source_map = {(r["owner_topic_id"], r["fact_id"]): r for r in sr}
    queued_map = {(r["owner_topic_id"], r["fact_id"]): r for r in qr}
    challenged_map = {(r["owner_topic_id"], r["fact_id"]): r for r in cr}
    if any(len(m) != len(v) for m, v in (
        (source_map, sr), (queued_map, qr), (challenged_map, cr)
    )):
        raise ValueError("duplicate Fact ownership in reviewer input")
    if len(qr) != 5 or set(queued_map) != {
        (sp["owner"], fid) for fid, sp in SCOPE.items()
    }:
        raise ValueError("unexpected reviewer Fact set")
    token_factory = token_factory or (lambda: secrets.token_urlsafe(18))
    shuffle = shuffle or secrets.SystemRandom().shuffle

    source_cards = []
    items = []
    secrets_map: list[dict[str, str]] = []
    manifest_rows: list[dict[str, str]] = []
    unique_tokens: set[str] = set()
    for fid, sp in sorted(SCOPE.items()):
        key = sp["owner"], fid
        s, q, c = source_map.get(key), queued_map.get(key), challenged_map.get(key)
        if not all(isinstance(v, dict) for v in (s, q, c)):
            raise ValueError("review source Fact is not represented in all inputs")
        relation = {
            "subject": sp["subject"], "predicate": sp["predicate"],
            "object": sp["object"], "conditions": sp["conditions"],
            "polarity": "positive",
        }
        if (s.get("relation") != relation
                or s.get("source_fact_id") != sp["source_fact_id"]
                or q.get("source_fact_id") != sp["source_fact_id"]
                or q.get("review_status") != "PENDING_INDEPENDENT_ADJUDICATION"
                or s.get("review_decision") != "HOLD"
                or s.get("registry_review_status") != "approved"
                or s.get("registry_verification_status") != "verified"
                or not s.get("registry_verification_refs")
                or s.get("candidate_alias") is not None
                or q.get("score_effect") != "none"
                or c.get("score_effect") != "none"
                or c.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
                or c.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"):
            raise ValueError("review packet authority, identity or label state drift")
        source_cards.append({
            "fact_id": fid,
            "source_fact_id": sp["source_fact_id"],
            "source_statement": s["source_statement"],
            "source_relation": relation,
            "verification_refs": [{
                "authority_id": r.get("authority_id"),
                "citation": r.get("citation"),
                "locator": r.get("locator"),
                "url": r.get("url"),
            } for r in s["registry_verification_refs"]],
            "review_scope": "Judge equivalence and explicit condition coverage only.",
        })
        for side, field in (("authored_positive", "positive_answer"),
                            ("authored_adversarial", "adversarial_answer")):
            raw = c.get(field)
            if not isinstance(raw, str) or not raw.strip():
                raise ValueError("missing author-draft text")
            token = token_factory()
            if not isinstance(token, str) or len(token) < 16 or token in unique_tokens:
                raise ValueError("duplicate or short private review token")
            unique_tokens.add(token)
            items.append({
                "review_item_id": token,
                "fact_id": fid,
                "authored_draft_text": raw,
                "expert_label": "",
                "condition_ids_explicitly_asserted": [],
                "condition_ids_missing_or_ambiguous": [],
                "disputed_claim_or_scope_notes": "",
                "expert_rationale": "",
                "reviewer_confidence": "",
            })
            secrets_map.append({
                "review_item_id": token,
                "case_id": c["case_id"],
                "author_side": side,
                "fact_id": fid,
            })
            manifest_rows.append({
                "review_item_id": token,
                "fact_id": fid,
                "authored_draft_text": raw,
            })
    if len(items) != 10 or len(secrets_map) != 10:
        raise ValueError("exactly 10 separate blinded drafts expected")
    shuffle(items)
    packet = {
        "schema_version": "s7_independent_expert_packet.v1",
        "reviewer_id": "",
        "review_date": "",
        "reviewer_affiliation_or_domain": "",
        "evaluation_status": "AWAITING_INDEPENDENT_REVIEW",
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "score_admission": "DISABLED",
        "score_effect": "none",
        "allowed_expert_labels": [
            "RELATION_WITH_REQUIRED_CONDITIONS",
            "RELATION_BUT_CONDITIONS_MISSING",
            "CONTRADICTORY_RELATION",
            "UNDETERMINED_OR_OUT_OF_SCOPE",
        ],
        "instruction": (
            "Independently classify each authored sentence with reference to the "
            "source Fact and explicit required conditions. Do not assume the "
            "source conditions from the question or from familiar context. "
            "Explain uncertain cases and note any draft assertion beyond the "
            "narrow Registry triplet. Preserve full reviewer reasoning. "
            "Do not infer author-provided labels."
        ),
        "source_cards": source_cards,
        "items_to_adjudicate": items,
        "independently_authored_challenge_requests": [
            {
                "fact_id": fid,
                "new_correct_paraphrase": "",
                "new_wrong_relation_or_direction": "",
                "new_missing_condition_case": "",
                "new_ambiguous_or_quoted_statement": "",
                "sources_or_assumptions": "",
            }
            for fid in sorted(SCOPE)
        ],
        "warning": (
            "Private file contains authored answers and source text. "
            "NEVER upload to GitHub Actions, public Issue, or PR."
        ),
    }
    sealed = {
        "schema_version": "s7_independent_expert_sealed_map.v1",
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "manifest_sha256": _sha256_manifest(manifest_rows),
        "secrecy": "EXTERNAL_PRIVATE_FILE_NOT_FOR_REVIEWER_OR_CI",
        "items": sorted(secrets_map, key=lambda x: x["review_item_id"]),
    }
    if any(k in json.dumps(packet, ensure_ascii=False)
           for k in ('"author_side"', '"positive_label"', '"adversarial_label"')):
        raise ValueError("predicted author labels accidentally exposed to reviewer")
    return packet, sealed
