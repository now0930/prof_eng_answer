"""Independent, score-neutral S7 review of Claim Alignment recall candidates.

Golden demand labels are NOT automatically mapped to Fact Anchor IDs: they can
describe composite requirements. A reviewer must explicitly adjudicate each
source-bound candidate. This module never authorizes or changes grading.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime
import hashlib
import json
from typing import Any, Mapping

from grading.evidence.claim_alignment_contract import validate_alignment_result
from grading.evidence.claim_alignment_recall_audit import (
    summarize_recall_review_candidates,
)

VERSION = "claim_alignment_s7_benchmark.v1"
REVIEW_VERSION = "claim_alignment_s7_adjudication.v1"
DECISIONS = frozenset({"CREDITABLE", "NOT_CREDITABLE", "UNRESOLVED"})
REVIEW_METHODS = frozenset({"expert_review", "user_approval", "adjudication"})


class ClaimS7BenchmarkError(ValueError):
    """Invalid or ambiguous expert evidence; never infer a decision."""


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def build_s7_case_snapshot(
    *, case_id: str, question_text: str, answer_text: str,
    alignment: Mapping[str, Any], requirement_evaluation: Mapping[str, Any],
    provisional: bool, fatal_or_core_error: bool,
) -> dict[str, Any]:
    """Build a review queue from an independently validated shadow alignment.

    Snapshot contains case hashes and source offsets, NEVER answer sentences.
    A present EXACT relation remains only a candidate, not a proof of credit.
    """
    if (not isinstance(case_id, str) or not case_id.strip()
            or not isinstance(question_text, str) or not question_text.strip()
            or not isinstance(answer_text, str) or not isinstance(provisional, bool)
            or not isinstance(fatal_or_core_error, bool)):
        raise ClaimS7BenchmarkError("invalid case identity or flags")
    checked = validate_alignment_result(dict(alignment), answer_text=answer_text)
    review = summarize_recall_review_candidates(
        alignment=checked, answer_text=answer_text,
        requirement_evaluation=requirement_evaluation,
    )
    question_sha = hashlib.sha256(question_text.encode("utf-8")).hexdigest()
    candidates = []
    for row in review["rows"]:
        if row["review_disposition"] != "REVIEW_POTENTIAL_RECALL_MISS":
            continue
        identity = {
            "case_id": case_id,
            "question_sha256": question_sha,
            "answer_sha256": checked["answer_sha256"],
            "alignment_fingerprint": checked["fingerprint"],
            "owner_topic_id": row["owner_topic_id"],
            "requirement_id": row["requirement_id"],
            "source_fact_id": row["source_fact_id"],
            "answer_claim_id": row["answer_claim_id"],
            "source_span": row["source_span"],
        }
        candidates.append({
            "candidate_id": _sha(identity),
            "owner_topic_id": row["owner_topic_id"],
            "requirement_id": row["requirement_id"],
            "source_fact_id": row["source_fact_id"],
            "answer_claim_id": row["answer_claim_id"],
            "source_span": row["source_span"],
            "current_requirement_status": row["current_requirement_status"],
            "case_blockers": (
                (["provisional_scope_or_meaning"] if provisional else [])
                + (["fatal_or_core_error"] if fatal_or_core_error else [])
            ),
        })
    if len({row["candidate_id"] for row in candidates}) != len(candidates):
        raise ClaimS7BenchmarkError("duplicate candidate identity")
    return {
        "schema_version": VERSION,
        "case_id": case_id,
        "question_sha256": question_sha,
        "answer_sha256": checked["answer_sha256"],
        "alignment_fingerprint": checked["fingerprint"],
        "score_effect": "none",
        "final_grade_allowed": False,
        "provisional": provisional,
        "fatal_or_core_error": fatal_or_core_error,
        "candidate_count": len(candidates),
        "candidate_dispositions": review["disposition_counts"],
        "review_candidates": candidates,
    }


def _validate_adjudication(row: Any) -> dict[str, Any]:
    if not isinstance(row, dict) or row.get("schema_version") != REVIEW_VERSION:
        raise ClaimS7BenchmarkError("invalid adjudication schema")
    if row.get("review_status") not in {"reviewed", "adjudicated"}:
        raise ClaimS7BenchmarkError("unreviewed/draft label is not evidence")
    for field in ("case_id", "candidate_id", "answer_sha256"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ClaimS7BenchmarkError(f"invalid {field}")
    if row["decision"] not in DECISIONS:
        raise ClaimS7BenchmarkError("invalid independent decision")
    review = row.get("review")
    if not isinstance(review, dict):
        raise ClaimS7BenchmarkError("independent review provenance missing")
    if (not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip()
            or review.get("method") not in REVIEW_METHODS
            or not isinstance(review.get("evidence_path"), str)
            or not review["evidence_path"].strip()):
        raise ClaimS7BenchmarkError("independent review provenance incomplete")
    try:
        timestamp = datetime.fromisoformat(review["reviewed_at"])
    except (KeyError, TypeError, ValueError) as error:
        raise ClaimS7BenchmarkError("invalid independent review timestamp") from error
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ClaimS7BenchmarkError("independent review requires timezone")
    return row


def evaluate_s7_adjudications(
    snapshots: list[dict[str, Any]],
    adjudications: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calculate research metrics only; NEVER treat labels as grading rules."""
    index: dict[tuple[str, str], dict[str, Any]] = {}
    case_hashes: dict[str, str] = {}
    cases_with_candidates: set[str] = set()
    for snapshot in snapshots:
        if (not isinstance(snapshot, dict)
                or snapshot.get("schema_version") != VERSION
                or snapshot.get("score_effect") != "none"
                or snapshot.get("final_grade_allowed") is not False
                or not isinstance(snapshot.get("review_candidates"), list)):
            raise ClaimS7BenchmarkError("invalid or score-bearing snapshot")
        case_id = snapshot.get("case_id")
        answer_sha = snapshot.get("answer_sha256")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ClaimS7BenchmarkError("invalid case ID")
        if case_id in case_hashes:
            raise ClaimS7BenchmarkError("duplicate case ID")
        if not isinstance(answer_sha, str) or len(answer_sha) != 64:
            raise ClaimS7BenchmarkError("invalid answer fingerprint")
        case_hashes[case_id] = answer_sha
        for candidate in snapshot["review_candidates"]:
            if not isinstance(candidate, dict):
                raise ClaimS7BenchmarkError("invalid candidate")
            key = (case_id, candidate.get("candidate_id"))
            if not isinstance(key[1], str) or not key[1] or key in index:
                raise ClaimS7BenchmarkError("duplicate/invalid candidate identity")
            if candidate.get("current_requirement_status") not in {
                "MISSING", "PARTIAL", "UNKNOWN",
            }:
                raise ClaimS7BenchmarkError("non-recall candidate cannot be reviewed")
            if (not isinstance(candidate.get("source_fact_id"), str)
                    or not candidate["source_fact_id"]):
                raise ClaimS7BenchmarkError("unverified candidate")
            index[key] = candidate
            cases_with_candidates.add(case_id)
        if snapshot.get("candidate_count") != len(snapshot["review_candidates"]):
            raise ClaimS7BenchmarkError("candidate count mismatch")

    decisions: dict[tuple[str, str], str] = {}
    for row in adjudications:
        item = _validate_adjudication(row)
        key = (item["case_id"], item["candidate_id"])
        if key not in index:
            raise ClaimS7BenchmarkError("adjudication refers to stale/foreign candidate")
        if item["answer_sha256"] != case_hashes[item["case_id"]]:
            raise ClaimS7BenchmarkError("adjudication answer fingerprint mismatch")
        if key in decisions:
            raise ClaimS7BenchmarkError("duplicate independent adjudication")
        decisions[key] = item["decision"]

    tally = Counter(decisions.values())
    reviewed = tally["CREDITABLE"] + tally["NOT_CREDITABLE"]
    unlabeled = len(index) - len(decisions)
    # Observed precision is selection-biased when some candidates are unlabeled.
    # Never call it full-system precision or a release approval.
    return {
        "schema_version": VERSION,
        "status": "RESEARCH_ONLY",
        "score_effect": "none",
        "final_grade_allowed": False,
        "score_admission": "DISABLED",
        "case_count": len(snapshots),
        "cases_with_candidates": len(cases_with_candidates),
        "candidate_count": len(index),
        "reviewed_candidate_count": len(decisions),
        "unlabeled_candidate_count": unlabeled,
        "creditable_count": tally["CREDITABLE"],
        "not_creditable_count": tally["NOT_CREDITABLE"],
        "unresolved_review_count": tally["UNRESOLVED"],
        "observed_precision_labeled_only": (
            round(tally["CREDITABLE"] / reviewed, 4) if reviewed else None
        ),
        "evidence_state": (
            "NO_DECISIVE_REVIEWS" if not reviewed
            else "FALSE_ACCEPTANCE_RISK_FOUND" if tally["NOT_CREDITABLE"]
            else "INCOMPLETE_REVIEW" if unlabeled or tally["UNRESOLVED"]
            else "ALL_CANDIDATES_REVIEWED_NO_REJECTION"
        ),
        "limitations": [
            "existing expert demand IDs are not automatically Fact Anchor IDs",
            "case-level golden score labels do not adjudicate individual claims",
            "precision of manually selected reviewed candidates may be biased",
            "no reviewed label or audit hash grants A/B/C credit",
        ],
    }
