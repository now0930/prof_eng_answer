"""Candidate selection cannot make a verified relationship score-bearing."""
from __future__ import annotations

import copy

import pytest

from grading.evidence.claim_alignment_contract import (
    ClaimAlignmentError, build_alignment_result,
)
from grading.evidence.claim_alignment_recall_audit import (
    summarize_recall_review_candidates,
)

TOPIC = "pid_controller_tuning_sequence_gain_effects"
ANSWER = "I 제어로 정상상태 오차를 줄일 수 있다."
FACT_ID = "i_action_effect"


def _alignment(*, projection_status="VERIFIED_REGISTRY_RELATION",
               relation_conflict=False, relation="EXACT_RELATION"):
    fact = {
        "owner_topic_id": TOPIC, "fact_id": FACT_ID,
        "parent_anchor_id": FACT_ID,
        "projection_status": projection_status,
        "source_fact_id": (
            "registry_i_action" if projection_status == "VERIFIED_REGISTRY_RELATION"
            else None
        ),
        "relation_source": (
            "verified_registry" if projection_status == "VERIFIED_REGISTRY_RELATION"
            else "machine_contract"
        ),
        "machine_relation_differs": relation_conflict,
        "relation": {
            "subject": "integral_action", "predicate": "reduces",
            "object": "steady_state_error", "polarity": "positive",
            "conditions": [],
        },
    }
    return build_alignment_result(
        answer_text=ANSWER, topic_ids=[TOPIC],
        fact_projection=[fact], logic_projection=[],
        alignments=[{
            "answer_claim_id": "claim_i",
            "fact_id": FACT_ID, "owner_topic_id": TOPIC,
            "relation": relation, "reason": "synthetic",
            "source_span": {"start": 0, "end": len(ANSWER)},
        }],
        unresolved=[],
    )


def _requirements(status="MISSING"):
    return {"requirements": [{
        "owner_topic_id": TOPIC,
        "requirement_id": FACT_ID,
        "status": status,
        "score_group_id": "group_i",
    }]}


def _run(*, alignment=None, requirements=None):
    return summarize_recall_review_candidates(
        alignment=alignment if alignment is not None else _alignment(),
        answer_text=ANSWER,
        requirement_evaluation=(
            requirements if requirements is not None else _requirements()
        ),
    )


def test_missing_exact_claim_is_review_queue_only():
    result = _run()
    assert result["candidate_count"] == 1
    assert result["disposition_counts"] == {
        "REVIEW_POTENTIAL_RECALL_MISS": 1,
    }
    assert result["score_effect"] == "none"
    assert result["final_grade_allowed"] is False
    assert result["rows"][0]["current_requirement_status"] == "MISSING"
    assert ANSWER not in str(result)


@pytest.mark.parametrize("status,expected", [
    ("SATISFIED", "ALREADY_SATISFIED"),
    ("PARTIAL", "REVIEW_POTENTIAL_RECALL_MISS"),
    ("UNKNOWN", "REVIEW_POTENTIAL_RECALL_MISS"),
    ("WRONG", "BLOCKED_EXISTING_WRONG"),
])
def test_existing_requirement_authority_is_never_overridden(status, expected):
    result = _run(requirements=_requirements(status))
    assert result["rows"][0]["review_disposition"] == expected
    assert "new_requirement_status" not in str(result)


def test_unverified_projection_and_machine_contract_conflict_cannot_promote():
    unverified = _run(
        alignment=_alignment(projection_status="STRUCTURED_MACHINE_RELATION"),
    )
    assert unverified["disposition_counts"] == {"NOT_VERIFIED": 1}
    conflict = _run(alignment=_alignment(relation_conflict=True))
    assert conflict["disposition_counts"] == {
        "HOLD_SOURCE_CONTRACT_CONFLICT": 1,
    }


def test_condition_gap_and_unrelated_requirement_are_not_recall_candidates():
    partial = _run(alignment=_alignment(relation="CONDITION_GAP"))
    assert partial["candidate_count"] == 0
    scoped = _run(requirements={"requirements": [{
        "owner_topic_id": TOPIC, "requirement_id": "other_requirement",
        "status": "MISSING",
    }]})
    assert scoped["candidate_count"] == 0


def test_duplicate_requirement_identity_fails_closed():
    duplicate = _requirements()
    duplicate["requirements"].append(copy.deepcopy(duplicate["requirements"][0]))
    with pytest.raises(ValueError, match="duplicate requirement"):
        _run(requirements=duplicate)


def test_wrong_answer_hash_and_unapproved_status_fail_closed():
    with pytest.raises(ClaimAlignmentError, match="fingerprint"):
        summarize_recall_review_candidates(
            alignment=_alignment(), answer_text="다른 답안",
            requirement_evaluation=_requirements(),
        )
    with pytest.raises(ValueError, match="unsupported requirement status"):
        _run(requirements=_requirements("SCORED"))
