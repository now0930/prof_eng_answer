"""S7 two-reviewer independent-label audit (local/private; no grade authority).

This checks *review forms*, not independence of human reviewers and not
correctness of labels. It NEVER determines benchmark readiness by itself.
No source/answer text, canonical aliases, or scores leave the local output.
"""
from __future__ import annotations

from collections import Counter
from datetime import date
import re
from typing import Any

PACKET_SCHEMA = "s7_independent_expert_packet.v1"
REPORT_SCHEMA = "s7_independent_reviewer_agreement.v1"
LABELS = frozenset({
    "RELATION_WITH_REQUIRED_CONDITIONS",
    "RELATION_BUT_CONDITIONS_MISSING",
    "CONTRADICTORY_RELATION",
    "UNDETERMINED_OR_OUT_OF_SCOPE",
})
CONFIDENCE = frozenset({"LOW", "MEDIUM", "HIGH"})
_REQUIRED = (
    "schema_version", "reviewer_id", "review_date", "reviewer_affiliation_or_domain",
    "evaluation_status", "source_inventory_execution_sha", "source_cards",
    "items_to_adjudicate", "independently_authored_challenge_requests",
)


def _field(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing or invalid reviewer field: " + name)
    return value.strip()


def _index(rows: Any, index_key: str) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError("review rows are not an array")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("review row must be a map")
        key = _field(row.get(index_key), index_key)
        if key in result:
            raise ValueError("duplicate review identity " + index_key)
        result[key] = row
    return result


def audit_two_reviewer_submissions(
    original_packet: dict[str, Any],
    review_a: dict[str, Any],
    review_b: dict[str, Any],
) -> dict[str, Any]:
    """Check original packet integrity, then measure reviewer agreement.

    No author-side sealed map is accepted: comparisons to author expectations
    or model outputs must never enter reviewer-label quality control.
    """
    if (
        original_packet.get("schema_version") != PACKET_SCHEMA
        or original_packet.get("evaluation_status") != "AWAITING_INDEPENDENT_REVIEW"
        or original_packet.get("score_admission") != "DISABLED"
        or original_packet.get("score_effect") != "none"
        or len(original_packet.get("source_cards", [])) != 5
        or len(original_packet.get("items_to_adjudicate", [])) != 10
        or len(original_packet.get("independently_authored_challenge_requests", [])) != 5
        or set(original_packet.get("allowed_expert_labels", [])) != LABELS
    ):
        raise ValueError("unverified review packet baseline")
    source = _index(original_packet["source_cards"], "fact_id")
    original = _index(original_packet["items_to_adjudicate"], "review_item_id")
    requested = _index(
        original_packet["independently_authored_challenge_requests"], "fact_id"
    )
    if len(source) != 5 or len(original) != 10 or set(source) != set(requested):
        raise ValueError("incomplete source cards or challenge requests")
    if any(v.get("expert_label") != "" for v in original.values()):
        raise ValueError("original packet must not contain author/expert labels")
    if any(x.get("score_admission") != "DISABLED" for x in (review_a, review_b)):
        raise ValueError("score admission enabled")
    summaries: list[dict[str, Any]] = []
    for doc in (review_a, review_b):
        if not isinstance(doc, dict):
            raise ValueError("invalid reviewer submission")
        if doc.get("schema_version") != PACKET_SCHEMA or any(k not in doc for k in _REQUIRED):
            raise ValueError("review document schema missing")
        if (
            doc.get("source_inventory_execution_sha")
            != original_packet.get("source_inventory_execution_sha")
            or doc.get("score_effect") != "none"
            or doc.get("evaluation_status") != "COMPLETE_BY_INDEPENDENT_REVIEWER"
            or doc.get("source_cards") != original_packet["source_cards"]
            or doc.get("allowed_expert_labels") != original_packet["allowed_expert_labels"]
        ):
            raise ValueError("source version/definition changed during review")
        pseudo = _field(doc.get("reviewer_id"), "reviewer_id")
        _field(doc.get("reviewer_affiliation_or_domain"),
               "reviewer_affiliation_or_domain")
        raw_date = _field(doc.get("review_date"), "review_date")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_date):
            raise ValueError("review_date must be ISO date")
        try:
            date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ValueError("invalid review date") from exc
        items = _index(doc["items_to_adjudicate"], "review_item_id")
        if set(items) != set(original):
            raise ValueError("reviewer may not add/delete/re-identify case")
        judgments = {}
        for item_id, row in items.items():
            base = original[item_id]
            # Forbid changing draft answer and its Fact ownership.
            if (
                row.get("fact_id") != base.get("fact_id")
                or row.get("authored_draft_text") != base.get("authored_draft_text")
                or set(row) != set(base)
            ):
                raise ValueError("reviewer altered authored text or review structure")
            label = row.get("expert_label")
            if label not in LABELS:
                raise ValueError("missing/unknown independent label")
            rationale = _field(row.get("expert_rationale"), "expert_rationale")
            _field(row.get("disputed_claim_or_scope_notes"),
                   "disputed_claim_or_scope_notes")
            confidence = row.get("reviewer_confidence")
            if confidence not in CONFIDENCE:
                raise ValueError("confidence must be LOW, MEDIUM or HIGH")
            supplied = row.get("condition_ids_explicitly_asserted")
            missing = row.get("condition_ids_missing_or_ambiguous")
            if not isinstance(supplied, list) or not isinstance(missing, list):
                raise ValueError("condition coverage requires lists")
            if (
                len(set(supplied)) != len(supplied)
                or len(set(missing)) != len(missing)
                or set(supplied) & set(missing)
            ):
                raise ValueError("duplicate/overlapping condition coverage")
            source_conditions = set(source[row["fact_id"]]["source_relation"]["conditions"])
            if (not set(supplied) <= source_conditions
                    or not set(missing) <= source_conditions):
                raise ValueError("invented condition ID")
            if label == "RELATION_WITH_REQUIRED_CONDITIONS" and (
                set(supplied) != source_conditions or missing
            ):
                raise ValueError("cannot assert complete relation with missing conditions")
            if label == "RELATION_BUT_CONDITIONS_MISSING" and not missing:
                raise ValueError("missing-condition label requires cited missing IDs")
            judgments[item_id] = {
                "fact_id": row["fact_id"],
                "label": label,
                "asserted": sorted(supplied),
                "missing": sorted(missing),
                "confidence": confidence,
                "rationale_present": len(rationale) > 0,
            }
        # Newly authored challenge prompts are voluntary here; report completeness.
        challenges = _index(doc["independently_authored_challenge_requests"], "fact_id")
        if set(challenges) != set(requested):
            raise ValueError("reviewer challenge Fact identity changed")
        authored_new = 0
        for fact_id, row in challenges.items():
            if set(row) != set(requested[fact_id]):
                raise ValueError("new challenge structure altered")
            fields = (
                "new_correct_paraphrase", "new_wrong_relation_or_direction",
                "new_missing_condition_case", "new_ambiguous_or_quoted_statement",
            )
            for key in fields:
                if not isinstance(row.get(key), str):
                    raise ValueError("invalid independently authored text")
                authored_new += bool(row[key].strip())
        summaries.append({"reviewer_id": pseudo, "judgments": judgments,
                          "new_case_field_count": authored_new})
    if summaries[0]["reviewer_id"] == summaries[1]["reviewer_id"]:
        raise ValueError("two different reviewer pseudonyms required")
    a, b = summaries
    disagreements = []
    label_match = 0
    condition_match = 0
    confusions: Counter[str] = Counter()
    for item_id in sorted(original):
        x, y = a["judgments"][item_id], b["judgments"][item_id]
        same_label = x["label"] == y["label"]
        same_condition = (
            x["asserted"] == y["asserted"] and x["missing"] == y["missing"]
        )
        label_match += same_label
        condition_match += same_condition
        if not (same_label and same_condition):
            disagreements.append({
                "review_item_id": item_id,
                "fact_id": x["fact_id"],
                "reviewer_label_disagreement": not same_label,
                "condition_coverage_disagreement": not same_condition,
                "requires_manual_reconciliation": True,
            })
        confusions["%s/%s" % (x["label"], y["label"])] += 1
    # Even complete agreement does not independently authenticate identities
    # or prove semantic truth, and provides NO parser performance numbers.
    return {
        "schema_version": REPORT_SCHEMA,
        "status": (
            "TWO_REVIEWER_DISAGREEMENT_MANUAL_RECONCILIATION"
            if disagreements else
            "TWO_REVIEWER_AGREEMENT_INDEPENDENCE_NOT_AUTHENTICATED"
        ),
        "source_inventory_execution_sha":
            original_packet["source_inventory_execution_sha"],
        "reviewed_draft_count": len(original),
        "reviewer_count_declared_not_authenticated": 2,
        "matching_relation_labels": label_match,
        "matching_condition_coverage": condition_match,
        "disagreement_count": len(disagreements),
        "new_independently_authored_field_counts_declared":
            [x["new_case_field_count"] for x in summaries],
        "disagreements": disagreements,
        "agreement_not_accuracy": True,
        "human_identity_independence_verified": False,
        "expert_benchmark_ready": False,
        "scorer_accuracy": None,
        "scorer_precision": None,
        "scorer_recall": None,
        "candidate_decision": "HOLD",
        "automatic_alias_admission": False,
        "score_effect": "none",
        "score_admission": "DISABLED",
        "limitations": [
            "Labels are self-declared; no independent reviewer authentication.",
            "Reviewer agreement is not an expert ground truth or model accuracy.",
            "Requires manual reconciliation, source-specific audit and holdout review.",
            "No author-side key, source statements or answer text in report.",
        ],
    }
