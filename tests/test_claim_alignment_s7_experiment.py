"""Exercise the offline S7 harness without calling a provider or scoring claims."""
from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from grading.evidence.claim_alignment_contract import build_alignment_result
from scripts.evaluate_claim_alignment_s7 import _source_case, evaluate_cases

TOPIC = "pid_controller_tuning_sequence_gain_effects"
QUESTION = "PID I 동작을 설명하시오."
ANSWER = "I 동작으로 정상상태 오차를 줄인다."
FACT_ID = "i_action_effect"


def _gold(status="reviewed"):
    return {
        "version": "expert_accuracy_case_v1",
        "case_id": "s7_fixture",
        "review_status": status,
        "review": {
            "reviewer": "expert",
            "method": "expert_review",
            "reviewed_at": "2026-11-14T12:00:00+09:00",
            "evidence_path": "calibration/reviews/s7_test.md",
        },
        "source": {"kind": "regression_fixture", "path": "calibration/s7_fixture.json"},
        "topic_ids": [TOPIC],
        "labels": {
            "demands": [{
                "demand_id": "composite_pid_demand",
                "requirement": "적분 제어의 원리 및 정상상태 오차",
                "core": True, "status": "PARTIAL",
            }],
            "findings": [],
            "score_range": {"min": 0.0, "max": 20.0},
            "flags": {
                "passing_score_allowed": False,
                "strong_verdict_allowed": False,
                "confidence_ceiling": "high",
            },
        },
    }


def _alignment():
    return build_alignment_result(
        answer_text=ANSWER, topic_ids=[TOPIC],
        fact_projection=[{
            "owner_topic_id": TOPIC,
            "fact_id": FACT_ID, "parent_anchor_id": FACT_ID,
            "source_fact_id": "approved_i_fact",
            "projection_status": "VERIFIED_REGISTRY_RELATION",
            "relation_source": "verified_registry",
            "relation": {
                "subject": "integral_action", "predicate": "reduces",
                "object": "steady_state_error", "polarity": "positive",
                "conditions": [],
            },
        }],
        logic_projection=[],
        alignments=[{
            "owner_topic_id": TOPIC, "fact_id": FACT_ID,
            "answer_claim_id": "parsed_1",
            "source_span": {"start": 0, "end": len(ANSWER)},
            "reason": "canonical_relation_matches",
            "relation": "EXACT_RELATION",
        }],
        unresolved=[],
    )


def test_s7_experiment_has_gold_baseline_but_no_fake_fact_labels():
    def fake_grader(*, question_text, answer_text, qualitative_de_mode):
        assert os.environ["CLAIM_ALIGNMENT_MODE"] == "off"
        assert os.environ["QUALITATIVE_DE_MODE"] == "off"
        assert os.environ["VALIDATION_LIVE_API"] == "0"
        assert question_text == QUESTION and answer_text == ANSWER
        assert qualitative_de_mode == "off"
        return {
            "topic_ids": [TOPIC],
            "requirements": [{
                "owner_topic_id": TOPIC,
                "requirement_id": FACT_ID,
                "status": "MISSING",
            }],
            "resolution_review": {"required": False},
            "logic_check_evaluation": {"fatal_error_detected": False},
        }

    with patch(
        "scripts.evaluate_claim_alignment_s7._source_case",
        return_value=(QUESTION, ANSWER),
    ), patch(
        "scripts.evaluate_claim_alignment_s7.grade_deterministically",
        side_effect=fake_grader,
    ), patch(
        "scripts.evaluate_claim_alignment_s7.analyze_claim_alignment",
        return_value=_alignment(),
    ), patch(
        "scripts.evaluate_claim_alignment_s7.prediction_from_grade",
        return_value={"case_id": "s7_fixture", "passing_score_allowed": False},
    ), patch(
        "scripts.evaluate_claim_alignment_s7.measure_accuracy",
        return_value={"evaluated_case_count": 1},
    ):
        result = evaluate_cases([_gold()])
    assert result["status"] == "RESEARCH_ONLY"
    assert result["expert_accuracy_baseline"]["evaluated_case_count"] == 1
    assert result["expert_gold_mapped_to_fact_ids"] is False
    assert result["s7_independent_review"]["candidate_count"] == 1
    assert result["golden_coverage"]["no_candidate_reason_counts"] == {
        "HAS_REVIEW_CANDIDATES": 1,
    }
    assert result["golden_coverage"]["routing_expected_topic_missing_case_count"] == 0
    assert result["golden_coverage"]["case_diagnostics"][0]["verified_fact_projection_count"] == 1
    assert result["golden_coverage"]["alignment_relation_counts"] == {
        "CONDITION_GAP": 0,
        "CONTRADICTION_CANDIDATE": 0,
        "EXACT_RELATION": 1,
        "UNRESOLVED": 0,
    }
    assert result["golden_coverage"]["recall_disposition_counts"] == {
        "REVIEW_POTENTIAL_RECALL_MISS": 1,
    }
    assert result["baseline_false_pass_case_ids"] == []
    assert result["baseline_false_official_pass_case_ids"] == []
    assert result["s7_independent_review"]["reviewed_candidate_count"] == 0
    assert result["score_admission"] == "DISABLED"
    assert ANSWER not in json.dumps(result, ensure_ascii=False)


def test_source_fixture_loader_rejects_escape_and_reads_nested_case(tmp_path):
    import scripts.evaluate_claim_alignment_s7 as harness

    root = tmp_path
    folder = root / "calibration"
    folder.mkdir()
    fixture = folder / "cases.json"
    fixture.write_text(json.dumps({
        "cases": [
            {"case_id": "safe",
             "question": QUESTION,
             "answer": ANSWER},
        ],
    }, ensure_ascii=False), encoding="utf-8")
    with patch.object(harness, "ROOT", root):
        assert _source_case({
            "source": {
                "path": "calibration/cases.json",
                "source_case_id": "safe",
            },
        }) == (QUESTION, ANSWER)
        for bad_path in (
            "../private/secret.json",
            "/tmp/private.json",
            "reports/cases.json",
        ):
            with pytest.raises(ValueError):
                _source_case({"source": {"path": bad_path}})


def test_case_source_error_is_reported_without_answer_or_fake_pass():
    with patch(
        "scripts.evaluate_claim_alignment_s7._source_case",
        side_effect=ValueError("private answer must not leak"),
    ):
        report = evaluate_cases([_gold()])
    assert report["status"] == "INCOMPLETE_BASELINE"
    assert report["graded_case_count"] == 0
    assert report["failures"] == [{
        "case_id": "s7_fixture", "stage": "fixture",
        "error_type": "ValueError",
    }]
    assert "private answer" not in str(report)


def test_draft_labels_are_not_included_in_official_s7_evaluation():
    with patch(
        "scripts.evaluate_claim_alignment_s7._source_case",
        side_effect=AssertionError("draft should never be graded"),
    ):
        report = evaluate_cases([_gold("draft")])
    assert report["eligible_case_count"] == 0
    assert report["baseline_false_official_pass_case_ids"] == []
    assert report["s7_independent_review"]["candidate_count"] == 0
    assert report["expert_accuracy_baseline"]["status"] == "NO_ELIGIBLE_CASES"


def test_alignment_failure_is_diagnosed_without_private_answer_leak():
    baseline = {
        "topic_ids": [TOPIC],
        "requirements": [{
            "owner_topic_id": TOPIC, "requirement_id": FACT_ID,
            "status": "MISSING",
        }],
        "resolution_review": {"required": False},
        "logic_check_evaluation": {"fatal_error_detected": False},
        "official_pass_met": False,
    }
    with patch(
        "scripts.evaluate_claim_alignment_s7._source_case",
        return_value=(QUESTION, ANSWER),
    ), patch(
        "scripts.evaluate_claim_alignment_s7.grade_deterministically",
        return_value=baseline,
    ), patch(
        "scripts.evaluate_claim_alignment_s7.prediction_from_grade",
        return_value={"case_id": "s7_fixture", "passing_score_allowed": False},
    ), patch(
        "scripts.evaluate_claim_alignment_s7.analyze_claim_alignment",
        side_effect=ValueError("PRIVATE ANSWER CONTENT MUST NOT LEAK"),
    ), patch(
        "scripts.evaluate_claim_alignment_s7.measure_accuracy",
        return_value={"evaluated_case_count": 1, "false_pass_count": 0},
    ):
        result = evaluate_cases([_gold()])
    assert result["status"] == "INCOMPLETE_ALIGNMENT"
    assert result["baseline_failure_count"] == 0
    assert result["alignment_failure_count"] == 1
    assert result["graded_case_count"] == 1
    assert result["alignment_snapshot_count"] == 0
    assert result["failures"] == [{
        "case_id": "s7_fixture",
        "stage": "canonical_claim_alignment",
        "error_type": "ValueError",
    }]
    assert "PRIVATE ANSWER" not in str(result)


def test_zero_candidates_diagnose_no_exact_relation_not_false_perfection():
    answer = ANSWER
    condition_gap = build_alignment_result(
        answer_text=answer, topic_ids=[TOPIC],
        fact_projection=[{
            "owner_topic_id": TOPIC,
            "fact_id": FACT_ID, "parent_anchor_id": FACT_ID,
            "source_fact_id": "approved_i_fact",
            "projection_status": "VERIFIED_REGISTRY_RELATION",
            "relation_source": "verified_registry",
            "relation": {
                "subject": "integral_action", "predicate": "reduces",
                "object": "steady_state_error", "polarity": "positive",
                "conditions": ["closed_loop"],
            },
        }],
        logic_projection=[],
        alignments=[{
            "owner_topic_id": TOPIC, "fact_id": FACT_ID,
            "answer_claim_id": "parsed_1",
            "source_span": {"start": 0, "end": len(answer)},
            "reason": "fact_conditions_not_asserted",
            "relation": "CONDITION_GAP",
        }],
        unresolved=[],
    )
    baseline = {
        "topic_ids": [TOPIC],
        "requirements": [{
            "owner_topic_id": TOPIC, "requirement_id": FACT_ID,
            "status": "MISSING",
        }],
        "canonical_claim_extraction": {"claim_count": 1},
    }
    with patch(
        "scripts.evaluate_claim_alignment_s7._source_case",
        return_value=(QUESTION, ANSWER),
    ), patch(
        "scripts.evaluate_claim_alignment_s7.grade_deterministically",
        return_value=baseline,
    ), patch(
        "scripts.evaluate_claim_alignment_s7.prediction_from_grade",
        return_value={"case_id": "s7_fixture", "passing_score_allowed": False},
    ), patch(
        "scripts.evaluate_claim_alignment_s7.analyze_claim_alignment",
        return_value=condition_gap,
    ), patch(
        "scripts.evaluate_claim_alignment_s7.measure_accuracy",
        return_value={"evaluated_case_count": 1},
    ):
        result = evaluate_cases([_gold()])
    assert result["status"] == "RESEARCH_ONLY"
    assert result["s7_independent_review"]["candidate_count"] == 0
    assert result["golden_coverage"]["no_candidate_reason_counts"] == {
        "NO_EXACT_RELATION": 1,
    }
    assert result["golden_coverage"]["case_diagnostics"][0]["canonical_claim_count"] == 1
    assert result["score_admission"] == "DISABLED"


def test_missing_expert_expected_topic_is_reported_without_score_override():
    actual_topic = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    no_match = build_alignment_result(
        answer_text=ANSWER, topic_ids=[actual_topic],
        fact_projection=[], logic_projection=[], alignments=[], unresolved=[],
    )
    baseline = {
        "topic_ids": [actual_topic],
        "requirements": [],
    }
    with patch(
        "scripts.evaluate_claim_alignment_s7._source_case",
        return_value=(QUESTION, ANSWER),
    ), patch(
        "scripts.evaluate_claim_alignment_s7.grade_deterministically",
        return_value=baseline,
    ), patch(
        "scripts.evaluate_claim_alignment_s7.prediction_from_grade",
        return_value={"case_id": "s7_fixture", "passing_score_allowed": False},
    ), patch(
        "scripts.evaluate_claim_alignment_s7.analyze_claim_alignment",
        return_value=no_match,
    ), patch(
        "scripts.evaluate_claim_alignment_s7.measure_accuracy",
        return_value={"evaluated_case_count": 1},
    ):
        result = evaluate_cases([_gold()])
    coverage = result["golden_coverage"]
    assert coverage["routing_expected_topic_missing_case_count"] == 1
    assert coverage["routing_case_diagnostics"] == [{
        "case_id": "s7_fixture",
        "missing_expected_topic_ids": [TOPIC],
        "extra_routed_topic_ids": [actual_topic],
        "route_contains_expected_topics": False,
    }]
    assert coverage["no_candidate_reason_counts"] == {
        "NO_SELECTED_REQUIREMENTS": 1,
    }
    assert result["score_admission"] == "DISABLED"
