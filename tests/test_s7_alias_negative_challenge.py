"""Guardrails for S7 draft negative-answer replay; score-neutral and non-admitting."""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from scripts.evaluate_s7_alias_negative_challenge import evaluate_negative_probe


def _source():
    return {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_admission": "DISABLED",
        "rows": [{
            "owner_topic_id": "topic_x",
            "fact_id": "fact_x",
            "source_fact_id": "verified_x",
            "review_decision": "HOLD",
            "relation": {
                "subject": "a", "predicate": "equals",
                "object": "b", "polarity": "positive",
                "conditions": ["same_basis"],
            },
        }],
    }


def _fixture():
    return {
        "schema_version": "s7_negative_claim_challenge.v1",
        "score_admission": "DISABLED",
        "adjudication_status": "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED",
        "cases": [{
            "case_id": "x1",
            "owner_topic_id": "topic_x",
            "fact_id": "fact_x",
            "relation_subject_id": "a",
            "positive_answer": "correct a=b under same basis",
            "adversarial_answer": "wrong a=b under different basis",
            "adversarial_type": "MISSING_CONDITION",
            "positive_label": "SOURCE_CONSISTENT_DRAFT",
            "adversarial_label": "SOURCE_INCONSISTENT_DRAFT",
            "score_effect": "none",
        }],
    }


def _matcher_factory(*, positive=(), negative=(), score_effect="none"):
    def matcher(*, question_text, answer_text, topic_ids, required_by_topic):
        assert question_text
        assert topic_ids == ["topic_x"]
        assert required_by_topic == {"topic_x": {"fact_x"}}
        labels = positive if answer_text.startswith("correct") else negative
        return {
            "authority": "audit_only",
            "score_effect": score_effect,
            "fact_projection": [{
                "owner_topic_id": "topic_x",
                "fact_id": "fact_x",
                "source_fact_id": "verified_x",
                "projection_status": "VERIFIED_REGISTRY_RELATION",
                "relation": _source()["rows"][0]["relation"],
            }],
            "alignments": [{
                "owner_topic_id": "topic_x", "fact_id": "fact_x",
                "relation": label,
            } for label in labels],
            "unresolved": [],
        }
    return matcher


def test_zero_positive_coverage_never_looks_like_perfect_precision():
    result = evaluate_negative_probe(
        _source(), _fixture(), matcher=_matcher_factory(), strict=False,
    )
    assert result["status"] == "NO_POSITIVE_COVERAGE_INCONCLUSIVE"
    assert result["fact_pair_count"] == 1
    assert result["draft_answer_case_count"] == 2
    assert result["positive_exact_count"] == 0
    assert result["adversarial_exact_count_needs_review"] == 0
    assert result["measured_accuracy"] is None
    assert result["measured_precision"] is None
    assert result["measured_recall"] is None
    assert result["accuracy_claim"] == "NOT_ESTABLISHED"
    assert result["score_admission"] == "DISABLED"
    report = json.dumps(result)
    assert "correct a=b" not in report
    assert "wrong a=b" not in report


def test_adversarial_exact_match_is_a_blocker_even_when_positive_matches():
    result = evaluate_negative_probe(
        _source(), _fixture(),
        matcher=_matcher_factory(
            positive=("EXACT_RELATION",), negative=("EXACT_RELATION",),
        ),
        strict=False,
    )
    assert result["status"] == "NEGATIVE_EXACT_REVIEW_REQUIRED"
    assert result["positive_exact_count"] == 1
    assert result["adversarial_exact_count_needs_review"] == 1
    assert result["automatic_alias_admission"] is False
    assert result["all_candidate_decisions"] == "HOLD"


def test_positive_coverage_does_not_override_draft_label_limit():
    result = evaluate_negative_probe(
        _source(), _fixture(),
        matcher=_matcher_factory(positive=("EXACT_RELATION",)),
        strict=False,
    )
    assert result["status"] == "RESEARCH_ONLY_SHADOW_COMPARISON"
    assert result["positive_exact_count"] == 1
    assert result["adversarial_exact_count_needs_review"] == 0
    assert result["measured_precision"] is None
    assert result["accuracy_claim"] == "NOT_ESTABLISHED"


def test_reject_mismatched_subject_unreviewed_fact_or_preapproved_alias():
    variants = [
        ("relation_subject_id", "different"),
        ("fact_id", "not_in_source_review"),
        ("score_effect", "credit"),
    ]
    for key, value in variants:
        bad = _fixture()
        bad["cases"][0][key] = value
        with pytest.raises(ValueError):
            evaluate_negative_probe(
                _source(), bad, matcher=_matcher_factory(),
                strict=False,
            )
    bad_source = _source()
    bad_source["rows"][0]["review_decision"] = "ACCEPT"
    with pytest.raises(ValueError, match="pre-approved"):
        evaluate_negative_probe(
            bad_source, _fixture(), matcher=_matcher_factory(),
            strict=False,
        )


def test_duplicate_fixture_or_non_neutral_matcher_fail_closed():
    case = _fixture()["cases"][0]
    dup = _fixture()
    dup["cases"].append(deepcopy(case))
    with pytest.raises(ValueError, match="duplicate"):
        evaluate_negative_probe(
            _source(), dup, matcher=_matcher_factory(),
            strict=False,
        )
    with pytest.raises(ValueError, match="grading authority"):
        evaluate_negative_probe(
            _source(), _fixture(),
            matcher=_matcher_factory(score_effect="changes_grade"),
            strict=False,
        )


def test_source_review_baseline_and_20_119_gate_cannot_be_bypassed():
    for field, value in (
        ("status", "SOURCE_JOIN_HOLD"),
        ("score_admission", "ENABLED"),
    ):
        bad = _source()
        bad[field] = value
        with pytest.raises(ValueError):
            evaluate_negative_probe(
                bad, _fixture(), matcher=_matcher_factory(),
                strict=False,
            )
    with pytest.raises(ValueError, match="119-source / 20-challenge gate"):
        evaluate_negative_probe(
            _source(), _fixture(), matcher=_matcher_factory(),
        )
