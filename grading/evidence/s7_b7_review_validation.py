"""Fail-closed validation for the local-only S7 B7 review packet.

This module validates review data integrity. It does not authenticate reviewers,
adjudicate engineering truth, approve a semantic crosswalk, or affect grading.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from .approved_fact_registry import load_approved_fact_registry


EXPECTED_SOURCE_PACKET_SHA256 = "f1271be031902768e67ba008053e7d35c81e35eb753d3e9adcb3d2a12d0bdf99"
EXPECTED_SOURCE_CASES = 40
EXPECTED_UNIQUE_CASES = 37
EXPECTED_DUPLICATE_GROUPS = 3
EXPECTED_CASE_KIND_MISMATCHES = 3
OVERALL_LABELS = {
    "FULLY_SUPPORTED_WITHIN_FACT_SCOPE",
    "PARTIALLY_SUPPORTED_OR_INCOMPLETE",
    "MIXED_OR_CONTRADICTED",
    "NO_ASSERTION",
    "UNRESOLVED",
}
CLAIM_LABELS = {
    "EQUIVALENT_WITHIN_SCOPE",
    "PARTIAL_OR_CONDITION_OMITTED",
    "CONTRADICTED",
    "NOT_ASSERTED_QUOTED_OR_REJECTED",
    "UNRESOLVED",
}
CONDITION_STATUSES = {"SATISFIED", "MISSING", "NOT_APPLICABLE", "UNRESOLVED"}
ASSERTION_CONTEXTS = {"ASSERTED", "QUOTED", "NEGATED", "RETRACTED", "MIXED", "UNCLEAR"}
FORBIDDEN_BLIND_KEYS = {
    "case_kind", "probe_note", "stage_a_extracted_claims",
    "stage_b_comparison_status", "original_case_id", "original_case_kind",
    "blind_id_crosswalk", "author_audit_and_key", "independent_reviewer_label",
}


class ReviewValidationError(ValueError):
    """A sanitized integrity error; messages never contain supplied answer text."""


def _fail(code: str) -> None:
    raise ReviewValidationError(code)


def _read_json(path: str | Path, code: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        _fail(code)


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _raw_sha256(path: str | Path) -> str:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except OSError:
        _fail("SOURCE_PACKET_UNREADABLE")


def _normalized_answer(text: str) -> str:
    return " ".join(text.casefold().split())


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _validate_blind_packet(packet: Any, source: dict[str, Any], registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not isinstance(packet, dict) or packet.get("schema_version") != "s7_b7_blinded_review_packet.v1":
        _fail("BLIND_PACKET_SCHEMA_INVALID")
    if packet.get("status") != "PENDING_INDEPENDENT_REVIEW" or packet.get("scoring_effect") != "none":
        _fail("BLIND_PACKET_POLICY_INVALID")
    if packet.get("source_packet_sha256") != EXPECTED_SOURCE_PACKET_SHA256:
        _fail("BLIND_PACKET_SOURCE_FINGERPRINT_MISMATCH")
    if FORBIDDEN_BLIND_KEYS.intersection(_walk_keys(packet)):
        _fail("BLIND_PACKET_LEAKED_AUTHOR_METADATA")
    cases = packet.get("cases")
    facts = packet.get("facts")
    if not isinstance(cases, list) or len(cases) != EXPECTED_UNIQUE_CASES or packet.get("case_count") != EXPECTED_UNIQUE_CASES:
        _fail("BLIND_CASE_COUNT_INVALID")
    if not isinstance(facts, dict) or len(facts) != 5:
        _fail("BLIND_FACT_SET_INVALID")

    source_pairs = {(c.get("topic_id"), c.get("comparison_fact_id")) for c in source["cases"]}
    approved = {f["fact_id"]: f for f in registry["facts"]}
    seen: dict[str, dict[str, Any]] = {}
    unique_public: set[tuple[str, str, str]] = set()
    for fact_id, fact in facts.items():
        if not isinstance(fact, dict) or fact.get("fact_id") != fact_id:
            _fail("BLIND_FACT_ID_INVALID")
        current = approved.get(fact_id)
        if current is None or fact.get("topic_id") != current["topic_id"]:
            _fail("BLIND_FACT_OWNERSHIP_MISMATCH")
        if fact.get("original_fact_statement") != current["statement"] or fact.get("relation") != current["relation"]:
            _fail("BLIND_FACT_CONTENT_MISMATCH")
        if fact.get("required_conditions") != current["relation"].get("conditions"):
            _fail("BLIND_FACT_CONDITIONS_MISMATCH")
        if fact.get("source_references") != current["verification_refs"]:
            _fail("BLIND_FACT_REFERENCES_MISMATCH")

    for case in cases:
        if not isinstance(case, dict) or set(case) != {"blind_case_id", "comparison_fact_id", "topic_id", "answer_text", "review_task"}:
            _fail("BLIND_CASE_SCHEMA_INVALID")
        blind_id, fact_id, topic_id, answer = (case.get("blind_case_id"), case.get("comparison_fact_id"), case.get("topic_id"), case.get("answer_text"))
        if not isinstance(blind_id, str) or not re.fullmatch(r"B7-[A-F0-9]{12}", blind_id) or blind_id in seen:
            _fail("BLIND_CASE_ID_INVALID_OR_DUPLICATE")
        if not isinstance(answer, str) or not answer.strip() or (topic_id, fact_id) not in source_pairs:
            _fail("BLIND_CASE_SCOPE_INVALID")
        if fact_id not in facts or facts[fact_id]["topic_id"] != topic_id:
            _fail("BLIND_CASE_FACT_OWNERSHIP_MISMATCH")
        public_key = (topic_id, fact_id, _normalized_answer(answer))
        if public_key in unique_public:
            _fail("BLIND_CASE_DUPLICATE_ANSWER")
        unique_public.add(public_key)
        seen[blind_id] = case
    if len(unique_public) != EXPECTED_UNIQUE_CASES or len({(c["topic_id"], c["comparison_fact_id"]) for c in cases}) != 5:
        _fail("BLIND_CASE_COVERAGE_INVALID")
    return seen


def _validate_span(span: Any, answer: str) -> None:
    if not isinstance(span, dict) or set(span) != {"start", "end", "text"}:
        _fail("REVIEW_CLAIM_SPAN_INVALID")
    start, end, text = span["start"], span["end"], span["text"]
    if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool):
        _fail("REVIEW_CLAIM_SPAN_INVALID")
    if start < 0 or end <= start or end > len(answer) or not isinstance(text, str) or answer[start:end] != text:
        _fail("REVIEW_CLAIM_SPAN_MISMATCH")


def _parse_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _validate_reviewed_case(result: dict[str, Any], case: dict[str, Any], expected_condition_ids: set[str]) -> None:
    if not isinstance(result.get("reviewer_identity"), str) or not result["reviewer_identity"].strip():
        _fail("REVIEWER_IDENTITY_REQUIRED")
    if not _parse_timestamp(result.get("reviewed_at")):
        _fail("REVIEW_TIMESTAMP_REQUIRED")
    if result.get("overall_answer_label") not in OVERALL_LABELS:
        _fail("OVERALL_LABEL_INVALID")
    if not isinstance(result.get("rationale"), str) or not result["rationale"].strip():
        _fail("REVIEW_RATIONALE_REQUIRED")
    if result.get("assertion_context_assessment") not in ASSERTION_CONTEXTS:
        _fail("ASSERTION_CONTEXT_INVALID")
    claims = result.get("claim_fact_assessments")
    if not isinstance(claims, list):
        _fail("CLAIM_ASSESSMENTS_REQUIRED")
    for claim in claims:
        if not isinstance(claim, dict) or claim.get("independent_reviewer_label") not in CLAIM_LABELS:
            _fail("CLAIM_LABEL_INVALID")
        if not isinstance(claim.get("rationale"), str) or not claim["rationale"].strip():
            _fail("CLAIM_RATIONALE_REQUIRED")
        _validate_span(claim.get("evidence_span"), case["answer_text"])
    claim_ids = [claim.get("claim_id") for claim in claims]
    if any(not isinstance(value, str) or not value.strip() for value in claim_ids) or len(set(claim_ids)) != len(claim_ids):
        _fail("CLAIM_ID_INVALID_OR_DUPLICATE")
    conditions = result.get("required_condition_assessment")
    if not isinstance(conditions, list):
        _fail("CONDITION_ASSESSMENTS_REQUIRED")
    fact_conditions = set()
    for condition in conditions:
        if not isinstance(condition, dict) or condition.get("status") not in CONDITION_STATUSES:
            _fail("CONDITION_ASSESSMENT_INVALID")
        cid = condition.get("condition_id")
        if not isinstance(cid, str) or cid in fact_conditions:
            _fail("CONDITION_ID_INVALID_OR_DUPLICATE")
        fact_conditions.add(cid)
        if not isinstance(condition.get("rationale"), str) or not condition["rationale"].strip():
            _fail("CONDITION_RATIONALE_REQUIRED")
    if fact_conditions != expected_condition_ids:
        _fail("CONDITION_SCOPE_MISMATCH")
    if not isinstance(result.get("reviewer_evidence"), list) or not result["reviewer_evidence"]:
        _fail("REVIEW_SOURCE_EVIDENCE_REQUIRED")
    for evidence in result["reviewer_evidence"]:
        if not isinstance(evidence, dict) or any(not isinstance(evidence.get(k), str) or not evidence[k].strip() for k in ("document", "locator", "reason")):
            _fail("REVIEW_SOURCE_LOCATOR_INVALID")


def _reviewer_disagreement(status: Any, decisions: Any) -> bool:
    if decisions is None:
        if status == "CONFLICT":
            _fail("CONFLICT_WITHOUT_REVIEWERS")
        return False
    if not isinstance(decisions, list) or not decisions:
        _fail("REVIEWER_DECISIONS_INVALID")
    identities = [d.get("reviewer_identity") for d in decisions if isinstance(d, dict)]
    if len(identities) != len(decisions) or any(not isinstance(v, str) or not v.strip() for v in identities) or len(set(identities)) != len(identities):
        _fail("REVIEWER_DECISION_IDENTITY_INVALID")
    labels = set()
    for decision in decisions:
        overall = decision.get("overall_answer_label")
        claims = decision.get("claim_fact_assessments", [])
        conditions = decision.get("required_condition_assessment", [])
        context = decision.get("assertion_context_assessment")
        if overall not in OVERALL_LABELS or not isinstance(claims, list) or not isinstance(conditions, list) or context not in ASSERTION_CONTEXTS:
            _fail("REVIEWER_DECISION_LABEL_INVALID")
        if any(not isinstance(c, dict) or c.get("independent_reviewer_label") not in CLAIM_LABELS for c in claims):
            _fail("REVIEWER_DECISION_CLAIM_LABEL_INVALID")
        if any(not isinstance(c, dict) or c.get("status") not in CONDITION_STATUSES for c in conditions):
            _fail("REVIEWER_DECISION_CONDITION_INVALID")
        labels.add((
            overall,
            context,
            _canonical_sha256(claims),
            _canonical_sha256(conditions),
        ))
    disagreement = len(labels) > 1
    if disagreement and status not in {"PENDING", "CONFLICT"}:
        _fail("REVIEWER_DISAGREEMENT_NOT_PENDING")
    if status == "CONFLICT" and not disagreement:
        _fail("CONFLICT_WITHOUT_DISAGREEMENT")
    return disagreement


def validate_review_bundle(
    source_packet_path: str | Path,
    blind_packet_path: str | Path,
    results_path: str | Path,
    audit_path: str | Path,
    repository_root: str | Path,
) -> dict[str, Any]:
    """Validate packets and declared reviewer output without exposing private data."""
    source_path = Path(source_packet_path)
    if _raw_sha256(source_path) != EXPECTED_SOURCE_PACKET_SHA256:
        _fail("SOURCE_PACKET_FINGERPRINT_MISMATCH")
    source = _read_json(source_path, "SOURCE_PACKET_INVALID")
    blind = _read_json(blind_packet_path, "BLIND_PACKET_INVALID")
    results = _read_json(results_path, "REVIEW_RESULTS_INVALID")
    audit = _read_json(audit_path, "PRIVATE_AUDIT_INVALID")
    if not isinstance(source, dict) or source.get("schema_version") != "s7_b7_expert_review_packet.v1":
        _fail("SOURCE_PACKET_SCHEMA_INVALID")
    policy = source.get("policy")
    if not isinstance(policy, dict) or policy.get("accuracy_status") != "NOT_ESTABLISHED" or policy.get("score_admission") != "DISABLED" or policy.get("score_effect") != "none" or policy.get("author_authored_cases_are_ground_truth") is not False or policy.get("registry_facts_changed") is not False:
        _fail("SOURCE_PACKET_POLICY_INVALID")
    source_cases = source.get("cases")
    if not isinstance(source_cases, list) or len(source_cases) != EXPECTED_SOURCE_CASES:
        _fail("SOURCE_CASE_COUNT_INVALID")
    if len({c.get("case_id") for c in source_cases}) != EXPECTED_SOURCE_CASES:
        _fail("SOURCE_CASE_ID_INVALID")
    if any(not isinstance(c, dict) or c.get("data_origin") != "AUTHOR_AUTHORED_PROBE_NOT_GOLD" or c.get("review_status") != "PENDING" or c.get("independent_reviewer_label") is not None or c.get("reviewer_id") is not None or c.get("reviewer_evidence") is not None for c in source_cases):
        _fail("SOURCE_CASE_HAS_UNTRUSTED_REVIEW_STATE")
    source_scope_counts = Counter((c.get("topic_id"), c.get("comparison_fact_id")) for c in source_cases if isinstance(c, dict))
    if len(source_scope_counts) != 5 or any(count != EXPECTED_SOURCE_CASES // 5 for count in source_scope_counts.values()):
        _fail("SOURCE_FACT_CASE_COVERAGE_INVALID")
    if audit.get("schema_version") != "s7_b7_probe_quality_audit.v1" or audit.get("source_packet_sha256") != EXPECTED_SOURCE_PACKET_SHA256:
        _fail("PRIVATE_AUDIT_SOURCE_MISMATCH")
    if audit.get("source_case_count") != EXPECTED_SOURCE_CASES or audit.get("exact_unique_answer_count") != EXPECTED_UNIQUE_CASES:
        _fail("PRIVATE_AUDIT_COUNTS_INVALID")
    if audit.get("exact_duplicate_group_count") != EXPECTED_DUPLICATE_GROUPS or audit.get("exact_duplicate_case_count") != EXPECTED_SOURCE_CASES - EXPECTED_UNIQUE_CASES:
        _fail("PRIVATE_DUPLICATE_AUDIT_INVALID")
    if audit.get("case_kind_mismatch_count") != EXPECTED_CASE_KIND_MISMATCHES:
        _fail("AUTHOR_CLASSIFICATION_AUDIT_COUNT_INVALID")
    registry = load_approved_fact_registry(repository_root)
    blind_by_id = _validate_blind_packet(blind, source, registry)

    crosswalk = audit.get("blind_id_crosswalk")
    audit_cases = audit.get("case_audit")
    if not isinstance(crosswalk, list) or len(crosswalk) != EXPECTED_UNIQUE_CASES or not isinstance(audit_cases, list) or len(audit_cases) != EXPECTED_SOURCE_CASES:
        _fail("PRIVATE_CROSSWALK_COUNTS_INVALID")
    source_by_id = {c["case_id"]: c for c in source_cases}
    audit_by_id = {c.get("original_case_id"): c for c in audit_cases}
    if set(audit_by_id) != set(source_by_id) or len(audit_by_id) != EXPECTED_SOURCE_CASES:
        _fail("PRIVATE_AUDIT_CASE_MAPPING_INVALID")
    cross_blind: set[str] = set()
    cross_original: set[str] = set()
    for entry in crosswalk:
        bid, oid = entry.get("blind_case_id"), entry.get("original_case_id")
        if bid not in blind_by_id or oid not in source_by_id or bid in cross_blind or oid in cross_original:
            _fail("PRIVATE_CROSSWALK_ID_INVALID")
        public, blind_case, audited = source_by_id[oid], blind_by_id[bid], audit_by_id[oid]
        digest = hashlib.sha256(public["answer_text"].encode("utf-8")).hexdigest()
        normalized_digest = hashlib.sha256(_normalized_answer(public["answer_text"]).encode("utf-8")).hexdigest()
        if (entry.get("answer_sha256") != digest or blind_case["answer_text"] != public["answer_text"]
                or blind_case["topic_id"] != public["topic_id"] or blind_case["comparison_fact_id"] != public["comparison_fact_id"]
                or audited.get("normalized_answer_sha256") != normalized_digest
                or entry.get("original_case_kind") != audited.get("original_case_kind")):
            _fail("PRIVATE_CROSSWALK_CONTENT_MISMATCH")
        cross_blind.add(bid)
        cross_original.add(oid)
    if cross_blind != set(blind_by_id):
        _fail("PRIVATE_CROSSWALK_NOT_ONE_TO_ONE")
    included_hashes = {
        (source_by_id[oid]["topic_id"], source_by_id[oid]["comparison_fact_id"], entry["answer_sha256"])
        for entry in crosswalk for oid in [entry["original_case_id"]]
    }
    omitted = [row for row in audit_cases if row.get("exact_duplicate_omitted_from_blind_packet") is True]
    if len(omitted) != EXPECTED_SOURCE_CASES - EXPECTED_UNIQUE_CASES:
        _fail("PRIVATE_DUPLICATE_OMISSION_COUNT_INVALID")
    for row in omitted:
        source_case = source_by_id[row["original_case_id"]]
        digest = hashlib.sha256(source_case["answer_text"].encode("utf-8")).hexdigest()
        if (source_case["topic_id"], source_case["comparison_fact_id"], digest) not in included_hashes:
            _fail("PRIVATE_OMITTED_CASE_NOT_EXACT_DUPLICATE")

    if not isinstance(results, dict) or results.get("schema_version") != "s7_b7_blind_review_results.v1":
        _fail("REVIEW_RESULTS_SCHEMA_INVALID")
    if results.get("source_blind_packet_sha256") != _canonical_sha256(blind):
        _fail("REVIEW_RESULTS_PACKET_FINGERPRINT_MISMATCH")
    result_cases = results.get("cases")
    if not isinstance(result_cases, list) or len(result_cases) != EXPECTED_UNIQUE_CASES:
        _fail("REVIEW_RESULT_COUNT_INVALID")
    result_by_id: dict[str, dict[str, Any]] = {}
    reviewed_count = 0
    pending_count = 0
    conflict_count = 0
    for item in result_cases:
        if not isinstance(item, dict):
            _fail("REVIEW_RESULT_SCHEMA_INVALID")
        bid = item.get("blind_case_id")
        if bid not in blind_by_id or bid in result_by_id:
            _fail("REVIEW_RESULT_ID_INVALID_OR_DUPLICATE")
        result_by_id[bid] = item
        status = item.get("review_status")
        decisions = item.get("reviewer_decisions")
        disagreement = _reviewer_disagreement(status, decisions)
        if disagreement:
            conflict_count += 1
            pending_count += 1
            continue
        if status == "PENDING":
            if any(item.get(k) not in (None, [], "") for k in ("reviewer_identity", "reviewed_at", "overall_answer_label", "claim_fact_assessments", "required_condition_assessment", "assertion_context_assessment", "reviewer_evidence", "rationale")):
                _fail("PENDING_RESULT_CONTAINS_REVIEW_LABELS")
            pending_count += 1
        elif status == "REVIEWED":
            if decisions is not None and len(decisions) > 1:
                _fail("MULTIPLE_REVIEWERS_REQUIRE_ADJUDICATION_RECORD")
            expected = set(blind["facts"][blind_by_id[bid]["comparison_fact_id"]]["required_conditions"])
            _validate_reviewed_case(item, blind_by_id[bid], expected)
            reviewed_count += 1
        elif status == "CONFLICT":
            pending_count += 1
            conflict_count += 1
        else:
            _fail("REVIEW_STATUS_INVALID")
    if set(result_by_id) != set(blind_by_id):
        _fail("REVIEW_RESULTS_SCOPE_MISMATCH")
    if results.get("reviewed_case_count") != reviewed_count:
        _fail("REVIEWED_COUNT_MISMATCH")
    accuracy = "NOT_ESTABLISHED" if reviewed_count == 0 else "NOT_ESTABLISHED"
    if results.get("accuracy_status") != accuracy:
        _fail("ACCURACY_STATUS_MUST_REMAIN_NOT_ESTABLISHED")
    if results.get("source_match_proven", False) is not False:
        _fail("SOURCE_MATCH_MUST_REMAIN_UNPROVEN")
    if results.get("score_admission", "DISABLED") != "DISABLED" or results.get("score_effect", "none") != "none":
        _fail("SCORING_POLICY_MUST_REMAIN_DISABLED")
    return {
        "status": "REVIEW_PENDING" if pending_count else "REVIEW_DATA_VALIDATED",
        "source_case_count": EXPECTED_SOURCE_CASES,
        "blind_unique_case_count": len(blind_by_id),
        "exact_duplicate_group_count": EXPECTED_DUPLICATE_GROUPS,
        "exact_duplicate_case_count": EXPECTED_SOURCE_CASES - EXPECTED_UNIQUE_CASES,
        "author_case_kind_mismatch_count": EXPECTED_CASE_KIND_MISMATCHES,
        "possible_semantic_overlap_group_count": len(audit.get("possible_semantic_overlap_groups", [])),
        "reviewed_case_count": reviewed_count,
        "pending_case_count": pending_count,
        "conflict_case_count": conflict_count,
        "unknown_or_unresolved_labels_are_not_accuracy": True,
        "accuracy_status": "NOT_ESTABLISHED",
        "false_acceptance_rate": None,
        "false_rejection_rate": None,
        "score_admission": "DISABLED",
        "score_effect": "none",
        "source_match_proven": False,
        "reviewer_identity_independently_authenticated": False,
    }
