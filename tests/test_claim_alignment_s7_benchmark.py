"""S7 independent adjudication is research-only, never a grading pathway."""
from __future__ import annotations

import copy
import hashlib

import pytest

from grading.evidence.claim_alignment_contract import build_alignment_result
from grading.quality.claim_alignment_s7_benchmark import (
    ClaimS7BenchmarkError, build_s7_case_snapshot, evaluate_s7_adjudications,
    REVIEW_VERSION,
)

TOPIC = "pid_controller_tuning_sequence_gain_effects"
CASE_ID = "synthetic_pid_1"
QUESTION = "PID의 I 동작을 설명하시오."
ANSWER = "적분 제어는 정상상태 오차를 줄인다."
FACT_ID = "i_action_effect"
FACT = {
    "owner_topic_id": TOPIC, "fact_id": FACT_ID,
    "parent_anchor_id": FACT_ID, "source_fact_id": "registry_i_action",
    "projection_status": "VERIFIED_REGISTRY_RELATION",
    "relation_source": "verified_registry",
    "relation": {
        "subject": "integral_action", "predicate": "reduces",
        "object": "steady_state_error", "polarity": "positive",
        "conditions": [],
    },
}


def _alignment(*, relation="EXACT_RELATION", verified=True):
    fact = copy.deepcopy(FACT)
    if not verified:
        fact["source_fact_id"] = None
        fact["projection_status"] = "STRUCTURED_MACHINE_RELATION"
        fact["relation_source"] = "machine_contract"
    return build_alignment_result(
        answer_text=ANSWER, topic_ids=[TOPIC], fact_projection=[fact],
        logic_projection=[], alignments=[{
            "owner_topic_id": TOPIC, "fact_id": FACT_ID,
            "answer_claim_id": "claim_i", "relation": relation,
            "reason": "synthetic",
            "source_span": {"start": 0, "end": len(ANSWER)},
        }], unresolved=[],
    )


def _snapshot(*, status="MISSING", relation="EXACT_RELATION",
              verified=True, provisional=False, fatal=False):
    return build_s7_case_snapshot(
        case_id=CASE_ID, question_text=QUESTION, answer_text=ANSWER,
        alignment=_alignment(relation=relation, verified=verified),
        requirement_evaluation={"requirements": [{
            "owner_topic_id": TOPIC, "requirement_id": FACT_ID,
            "status": status,
        }]},
        provisional=provisional, fatal_or_core_error=fatal,
    )


def _label(snapshot, *, decision="CREDITABLE",
           answer_sha=None, case_id=CASE_ID):
    return {
        "schema_version": REVIEW_VERSION,
        "case_id": case_id,
        "candidate_id": snapshot["review_candidates"][0]["candidate_id"],
        "answer_sha256": (
            answer_sha if answer_sha is not None
            else hashlib.sha256(ANSWER.encode()).hexdigest()
        ),
        "decision": decision,
        "review_status": "reviewed",
        "review": {
            "reviewer": "independent_expert",
            "method": "expert_review",
            "reviewed_at": "2026-11-14T12:00:00+09:00",
            "evidence_path": "calibration/reviews/synthetic_pid_review.md",
        },
    }


def test_unadjudicated_candidate_is_not_automatically_credited():
    snapshot = _snapshot()
    assert snapshot["candidate_count"] == 1
    assert snapshot["review_candidates"][0]["current_requirement_status"] == "MISSING"
    assert ANSWER not in str(snapshot)
    result = evaluate_s7_adjudications([snapshot], [])
    assert result["evidence_state"] == "NO_DECISIVE_REVIEWS"
    assert result["unlabeled_candidate_count"] == 1
    assert result["observed_precision_labeled_only"] is None
    assert result["score_admission"] == "DISABLED"
    assert result["score_effect"] == "none"


def test_independent_positive_review_still_cannot_award_a_b_c():
    snapshot = _snapshot()
    result = evaluate_s7_adjudications([snapshot], [_label(snapshot)])
    assert result["creditable_count"] == 1
    assert result["observed_precision_labeled_only"] == 1.0
    assert result["score_admission"] == "DISABLED"
    assert result["final_grade_allowed"] is False


def test_independent_negative_review_exposes_false_acceptance_risk():
    snapshot = _snapshot()
    result = evaluate_s7_adjudications(
        [snapshot], [_label(snapshot, decision="NOT_CREDITABLE")],
    )
    assert result["not_creditable_count"] == 1
    assert result["observed_precision_labeled_only"] == 0.0
    assert result["evidence_state"] == "FALSE_ACCEPTANCE_RISK_FOUND"
    assert result["score_admission"] == "DISABLED"


def test_excluded_sources_and_condition_gaps_are_not_candidates():
    for snapshot in (
        _snapshot(status="WRONG"),
        _snapshot(status="SATISFIED"),
        _snapshot(relation="CONDITION_GAP"),
        _snapshot(verified=False),
    ):
        assert snapshot["candidate_count"] == 0
        assert not snapshot["review_candidates"]


def test_fatal_and_provisional_case_blockers_are_recorded():
    snapshot = _snapshot(provisional=True, fatal=True)
    assert snapshot["review_candidates"][0]["case_blockers"] == [
        "provisional_scope_or_meaning", "fatal_or_core_error",
    ]
    assert snapshot["final_grade_allowed"] is False


def test_stale_foreign_duplicate_and_draft_labels_fail_closed():
    snapshot = _snapshot()
    label = _label(snapshot)
    with pytest.raises(ClaimS7BenchmarkError, match="fingerprint"):
        evaluate_s7_adjudications(
            [snapshot], [_label(snapshot, answer_sha="0" * 64)],
        )
    with pytest.raises(ClaimS7BenchmarkError, match="stale/foreign"):
        evaluate_s7_adjudications(
            [snapshot], [_label(snapshot, case_id="foreign")],
        )
    with pytest.raises(ClaimS7BenchmarkError, match="duplicate"):
        evaluate_s7_adjudications([snapshot], [label, label])
    draft = _label(snapshot)
    draft["review_status"] = "draft"
    with pytest.raises(ClaimS7BenchmarkError, match="unreviewed/draft"):
        evaluate_s7_adjudications([snapshot], [draft])


def test_missing_provenance_and_unresolved_review_do_not_fake_accuracy():
    snapshot = _snapshot()
    label = _label(snapshot, decision="UNRESOLVED")
    result = evaluate_s7_adjudications([snapshot], [label])
    assert result["unresolved_review_count"] == 1
    assert result["observed_precision_labeled_only"] is None
    invalid = _label(snapshot)
    invalid["review"]["reviewed_at"] = "2026-11-14T12:00:00"
    with pytest.raises(ClaimS7BenchmarkError, match="timezone"):
        evaluate_s7_adjudications([snapshot], [invalid])
    invalid = _label(snapshot)
    invalid["review"]["evidence_path"] = ""
    with pytest.raises(ClaimS7BenchmarkError, match="provenance"):
        evaluate_s7_adjudications([snapshot], [invalid])


def test_case_identity_and_snapshot_duplicate_are_rejected():
    snapshot = _snapshot()
    with pytest.raises(ClaimS7BenchmarkError, match="duplicate case"):
        evaluate_s7_adjudications([snapshot, copy.deepcopy(snapshot)], [])
    with pytest.raises(ClaimS7BenchmarkError, match="score-bearing snapshot"):
        evaluate_s7_adjudications([{**snapshot, "score_effect": "grant"}], [])


def test_snapshot_rejects_stale_answer_in_alignment():
    with pytest.raises(ValueError, match="answer fingerprint"):
        build_s7_case_snapshot(
            case_id=CASE_ID, question_text=QUESTION, answer_text=ANSWER + "!",
            alignment=_alignment(),
            requirement_evaluation={"requirements": []},
            provisional=False, fatal_or_core_error=False,
        )
