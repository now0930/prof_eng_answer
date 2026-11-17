from __future__ import annotations

import pytest
import hashlib
import json

import grading.evidence.s7_b7_review_validation as validation

from grading.evidence.s7_b7_review_validation import (
    ReviewValidationError,
    _reviewer_disagreement,
    _validate_reviewed_case,
    _validate_span,
    validate_review_bundle,
)


def test_review_span_uses_exact_answer_slice_with_korean_and_english() -> None:
    answer = "Nyquist 경로는 열린 우반평면을 둘러싼다."
    _validate_span({"start": 0, "end": 7, "text": "Nyquist"}, answer)
    _validate_span({"start": 8, "end": 10, "text": "경로"}, answer)


@pytest.mark.parametrize(
    "span",
    [
        {"start": -1, "end": 2, "text": "x"},
        {"start": 0, "end": 99, "text": "x"},
        {"start": 0, "end": 1, "text": "n"},
        {"start": 0, "end": 1, "text": "N", "fact_id": "borrowed"},
        {"start": True, "end": 1, "text": "N"},
    ],
)
def test_invalid_or_fabricated_review_span_is_rejected(span: dict) -> None:
    with pytest.raises(ReviewValidationError):
        _validate_span(span, "Nyquist")


def _valid_review(answer: str = "V-model links design and test stages.") -> dict:
    return {
        "reviewer_identity": "independent-reviewer-1",
        "reviewed_at": "2026-11-17T12:00:00Z",
        "overall_answer_label": "FULLY_SUPPORTED_WITHIN_FACT_SCOPE",
        "claim_fact_assessments": [
            {
                "claim_id": "claim-1",
                "independent_reviewer_label": "EQUIVALENT_WITHIN_SCOPE",
                "rationale": "The stated relation is supported.",
                "evidence_span": {"start": 0, "end": len(answer), "text": answer},
            }
        ],
        "required_condition_assessment": [],
        "assertion_context_assessment": "ASSERTED",
        "reviewer_evidence": [
            {"document": "SEI V Models article", "locator": "Traditional V Model section", "reason": "Supports correspondence."}
        ],
        "rationale": "The relation is within the source Fact scope.",
    }


def test_v_model_zero_required_conditions_is_valid_without_invented_condition() -> None:
    answer = "V-model links design and test stages."
    _validate_reviewed_case(_valid_review(answer), {"answer_text": answer}, set())


@pytest.mark.parametrize(
    "mutation, expected_code",
    [
        (lambda value: value.update(reviewer_identity=None), "REVIEWER_IDENTITY_REQUIRED"),
        (lambda value: value.update(reviewed_at=None), "REVIEW_TIMESTAMP_REQUIRED"),
        (lambda value: value.update(reviewed_at="2026-11-17T12:00:00"), "REVIEW_TIMESTAMP_REQUIRED"),
        (lambda value: value.update(reviewer_evidence=[]), "REVIEW_SOURCE_EVIDENCE_REQUIRED"),
        (lambda value: value["reviewer_evidence"][0].update(locator=""), "REVIEW_SOURCE_LOCATOR_INVALID"),
        (lambda value: value["claim_fact_assessments"][0]["evidence_span"].update(text="wrong"), "REVIEW_CLAIM_SPAN_MISMATCH"),
        (lambda value: value["claim_fact_assessments"][0].update(independent_reviewer_label="AUTHOR_GUESS"), "CLAIM_LABEL_INVALID"),
    ],
)
def test_reviewed_record_requires_identity_evidence_and_answer_span(mutation, expected_code: str) -> None:
    answer = "V-model links design and test stages."
    record = _valid_review(answer)
    mutation(record)
    with pytest.raises(ReviewValidationError, match=expected_code):
        _validate_reviewed_case(record, {"answer_text": answer}, set())


def test_required_conditions_must_match_fact_exactly() -> None:
    answer = "V-model links design and test stages."
    record = _valid_review(answer)
    record["required_condition_assessment"] = [
        {"condition_id": "invented-condition", "status": "SATISFIED", "rationale": "invented"}
    ]
    with pytest.raises(ReviewValidationError, match="CONDITION_SCOPE_MISMATCH"):
        _validate_reviewed_case(record, {"answer_text": answer}, set())


def test_reviewer_disagreement_stays_pending_and_reviewed_conflict_is_rejected() -> None:
    decisions = [
        {"reviewer_identity": "reviewer-a", "overall_answer_label": "FULLY_SUPPORTED_WITHIN_FACT_SCOPE", "claim_fact_assessments": [], "required_condition_assessment": [], "assertion_context_assessment": "ASSERTED"},
        {"reviewer_identity": "reviewer-b", "overall_answer_label": "MIXED_OR_CONTRADICTED", "claim_fact_assessments": [], "required_condition_assessment": [], "assertion_context_assessment": "ASSERTED"},
    ]
    assert _reviewer_disagreement("PENDING", decisions) is True
    assert _reviewer_disagreement("CONFLICT", decisions) is True
    with pytest.raises(ReviewValidationError, match="REVIEWER_DISAGREEMENT_NOT_PENDING"):
        _reviewer_disagreement("REVIEWED", decisions)


def test_reviewed_status_requires_conflict_resolution_if_decisions_disagree() -> None:
    decisions = [
        {"reviewer_identity": "reviewer-a", "overall_answer_label": "FULLY_SUPPORTED_WITHIN_FACT_SCOPE", "claim_fact_assessments": [], "required_condition_assessment": [], "assertion_context_assessment": "ASSERTED"},
        {"reviewer_identity": "reviewer-b", "overall_answer_label": "MIXED_OR_CONTRADICTED", "claim_fact_assessments": [], "required_condition_assessment": [], "assertion_context_assessment": "ASSERTED"},
    ]
    with pytest.raises(ReviewValidationError, match="REVIEWER_DISAGREEMENT_NOT_PENDING"):
        _reviewer_disagreement("REVIEWED", decisions)


def test_duplicate_reviewer_identity_is_rejected() -> None:
    decisions = [
        {"reviewer_identity": "same", "overall_answer_label": "UNRESOLVED", "claim_fact_assessments": [], "required_condition_assessment": [], "assertion_context_assessment": "UNCLEAR"},
        {"reviewer_identity": "same", "overall_answer_label": "UNRESOLVED", "claim_fact_assessments": [], "required_condition_assessment": [], "assertion_context_assessment": "UNCLEAR"},
    ]
    with pytest.raises(ReviewValidationError, match="REVIEWER_DECISION_IDENTITY_INVALID"):
        _reviewer_disagreement("PENDING", decisions)


def _write_bundle(tmp_path, monkeypatch):
    source_cases = []
    facts = {}
    registry_facts = []
    blind_cases = []
    crosswalk = []
    audit_cases = []
    review_cases = []
    for index in range(5):
        topic, fact_id, case_id = f"topic-{index}", f"fact-{index}", f"source-{index}"
        answer = f"Unique answer {index}."
        relation = {"subject": "s", "predicate": "maps", "object": "o", "conditions": []}
        refs = [{"authority_id": f"auth-{index}", "locator": "section 1"}]
        source_cases.append({"case_id": case_id, "topic_id": topic, "comparison_fact_id": fact_id, "answer_text": answer, "data_origin": "AUTHOR_AUTHORED_PROBE_NOT_GOLD", "review_status": "PENDING", "independent_reviewer_label": None, "reviewer_id": None, "reviewer_evidence": None})
        fact = {"topic_id": topic, "fact_id": fact_id, "original_fact_statement": f"statement-{index}", "relation": relation, "required_conditions": [], "source_references": refs}
        facts[fact_id] = fact
        registry_facts.append({"topic_id": topic, "fact_id": fact_id, "statement": fact["original_fact_statement"], "relation": relation, "verification_refs": refs})
        blind_id = f"B7-{index:012X}"
        blind_cases.append({"blind_case_id": blind_id, "comparison_fact_id": fact_id, "topic_id": topic, "answer_text": answer, "review_task": "review"})
        crosswalk.append({"blind_case_id": blind_id, "original_case_id": case_id, "original_case_kind": "synthetic", "answer_sha256": hashlib.sha256(answer.encode()).hexdigest()})
        audit_cases.append({"original_case_id": case_id, "original_case_kind": "synthetic", "normalized_answer_sha256": hashlib.sha256(answer.casefold().encode()).hexdigest(), "exact_duplicate_omitted_from_blind_packet": False})
        review_cases.append({"blind_case_id": blind_id, "review_status": "PENDING", "reviewer_identity": None, "overall_answer_label": None, "claim_fact_assessments": [], "required_condition_assessment": None, "assertion_context_assessment": None, "reviewer_evidence": [], "rationale": None})

    source = {"schema_version": "s7_b7_expert_review_packet.v1", "policy": {"accuracy_status": "NOT_ESTABLISHED", "score_admission": "DISABLED", "score_effect": "none", "author_authored_cases_are_ground_truth": False, "registry_facts_changed": False}, "cases": source_cases}
    source_bytes = json.dumps(source, ensure_ascii=False).encode()
    source_path = tmp_path / "source.json"
    source_path.write_bytes(source_bytes)
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    blind = {"schema_version": "s7_b7_blinded_review_packet.v1", "source_packet_sha256": source_sha, "status": "PENDING_INDEPENDENT_REVIEW", "scoring_effect": "none", "case_count": 5, "cases": blind_cases, "facts": facts}
    results = {"schema_version": "s7_b7_blind_review_results.v1", "source_blind_packet_sha256": validation._canonical_sha256(blind), "accuracy_status": "NOT_ESTABLISHED", "reviewed_case_count": 0, "cases": review_cases}
    audit = {"schema_version": "s7_b7_probe_quality_audit.v1", "source_packet_sha256": source_sha, "source_case_count": 5, "exact_unique_answer_count": 5, "exact_duplicate_group_count": 0, "exact_duplicate_case_count": 0, "case_kind_mismatch_count": 0, "possible_semantic_overlap_groups": [], "blind_id_crosswalk": crosswalk, "case_audit": audit_cases}
    paths = []
    for name, value in (("blind.json", blind), ("results.json", results), ("audit.json", audit)):
        path = tmp_path / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        paths.append(path)
    monkeypatch.setattr(validation, "EXPECTED_SOURCE_PACKET_SHA256", source_sha)
    monkeypatch.setattr(validation, "EXPECTED_SOURCE_CASES", 5)
    monkeypatch.setattr(validation, "EXPECTED_UNIQUE_CASES", 5)
    monkeypatch.setattr(validation, "EXPECTED_DUPLICATE_GROUPS", 0)
    monkeypatch.setattr(validation, "EXPECTED_CASE_KIND_MISMATCHES", 0)
    monkeypatch.setattr(validation, "load_approved_fact_registry", lambda _: {"facts": registry_facts})
    return source_path, *paths


def test_synthetic_pending_bundle_integrity_passes_without_private_fixture_dependency(tmp_path, monkeypatch) -> None:
    source, blind, results, audit = _write_bundle(tmp_path, monkeypatch)
    report = validate_review_bundle(source, blind, results, audit, tmp_path)
    assert report["status"] == "REVIEW_PENDING"
    assert report["source_case_count"] == 5
    assert report["blind_unique_case_count"] == 5
    assert report["reviewed_case_count"] == 0
    assert report["false_acceptance_rate"] is None
    assert report["false_rejection_rate"] is None
    assert report["source_match_proven"] is False


@pytest.mark.parametrize(
    "mutate, code",
    [
        (lambda blind, results, audit: blind["cases"].pop(), "BLIND_CASE_COUNT_INVALID"),
        (lambda blind, results, audit: blind["cases"].append(blind["cases"][0]), "BLIND_CASE_COUNT_INVALID"),
        (lambda blind, results, audit: blind["cases"][0].update(topic_id="wrong-topic"), "BLIND_CASE_SCOPE_INVALID"),
        (lambda blind, results, audit: blind["cases"][0].update(blind_case_id=blind["cases"][1]["blind_case_id"]), "BLIND_CASE_ID_INVALID_OR_DUPLICATE"),
        (lambda blind, results, audit: blind["cases"][0].update(case_kind="leaked"), "BLIND_PACKET_LEAKED_AUTHOR_METADATA"),
        (lambda blind, results, audit: audit["blind_id_crosswalk"].pop(), "PRIVATE_CROSSWALK_COUNTS_INVALID"),
        (lambda blind, results, audit: results["cases"].pop(), "REVIEW_RESULT_COUNT_INVALID"),
        (lambda blind, results, audit: results["cases"][0].update(review_status="REVIEWED"), "REVIEWER_IDENTITY_REQUIRED"),
        (lambda blind, results, audit: results["cases"][0].update(review_status="PENDING", overall_answer_label="UNRESOLVED"), "PENDING_RESULT_CONTAINS_REVIEW_LABELS"),
    ],
)
def test_bundle_rejects_integrity_tampering(tmp_path, monkeypatch, mutate, code) -> None:
    source, blind_path, result_path, audit_path = _write_bundle(tmp_path, monkeypatch)
    blind, results, audit = (json.loads(path.read_text()) for path in (blind_path, result_path, audit_path))
    mutate(blind, results, audit)
    for path, value in ((blind_path, blind), (result_path, results), (audit_path, audit)):
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    # Result hash is deliberately left as-is where the blind packet was modified.
    with pytest.raises(ReviewValidationError, match=code):
        validate_review_bundle(source, blind_path, result_path, audit_path, tmp_path)
