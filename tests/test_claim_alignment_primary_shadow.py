"""Production grade must be identical with claim alignment off vs shadow."""
from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from grading.scoring.deterministic_primary_grader import (
    DeterministicPrimaryError, grade_deterministically,
)


# Existing primary-grade regression already verifies this exact route.
QUESTION = "열전대 온도센서의 측정 원리를 설명하시오."
ANSWER = "열전대는 제벡 효과로 온도차에 따른 열기전력을 측정한다."


def _run(mode):
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": mode}):
        return grade_deterministically(
            question_text=QUESTION, answer_text=ANSWER,
            qualitative_de_mode="off",
        )


def test_shadow_never_changes_abc_de_or_verdict():
    off = _run("off")
    shadow = _run("shadow")
    assert "claim_alignment_audit" not in off
    assert shadow["claim_alignment_audit"]["score_effect"] == "none"
    assert shadow["claim_alignment_audit"]["status"] == "SHADOW"
    recall = shadow["claim_alignment_audit"]["recall_review"]
    assert recall["score_effect"] == "none"
    assert type(recall["candidate_count"]) is int
    assert isinstance(recall["disposition_counts"], dict)
    for field in (
        "total_score", "deterministic_score", "requirement_summary",
        "requirements", "verdict", "passing_score_allowed",
        "logic_check_evaluation", "official_pass_met",
    ):
        assert off[field] == shadow[field], field


def test_shadow_failure_does_not_change_grade():
    baseline = _run("off")
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": "shadow"}), patch(
        "grading.evidence.claim_alignment_engine.analyze_claim_alignment",
        side_effect=RuntimeError("private answer secret must not leak"),
    ):
        failure = grade_deterministically(
            question_text=QUESTION, answer_text=ANSWER,
            qualitative_de_mode="off",
        )
    assert failure["claim_alignment_audit"] == {
        "status": "ERROR", "score_effect": "none", "error_type": "RuntimeError",
    }
    assert failure["total_score"] == baseline["total_score"]


def test_invalid_alignment_mode_fails_closed():
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": "admit_unverified"}):
        with pytest.raises(DeterministicPrimaryError, match="claim alignment"):
            grade_deterministically(
                question_text=QUESTION, answer_text=ANSWER,
                qualitative_de_mode="off",
            )


@pytest.mark.parametrize("question,answer", [
    (
        "PID 제어기의 P, I, D 동작 및 튜닝 순서를 설명하시오.",
        "P 동작으로 응답 특성을 조정하고, I 동작은 정상상태 오차를 줄인다. "
        "D 동작은 필요할 때 감쇠를 보완하고 노이즈와 적분 windup을 고려한다.",
    ),
    (
        "차압식 유량계의 측정 원리와 설치상 주의점을 설명하시오.",
        "차압식 유량계는 베르누이 원리에 의해 발생하는 차압을 이용하며 "
        "유량은 차압의 제곱근에 비례한다. 직관부를 확보하고 유체 밀도를 고려한다.",
    ),
    (
        "SIL 결정 방법을 설명하시오.",
        "lambda_SIS 비율이 PFD 비율보다 작도록 설계한다.",
    ),
])
def test_cross_topic_primary_shadow_is_score_invariant(question, answer):
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": "off"}):
        baseline = grade_deterministically(
            question_text=question, answer_text=answer, qualitative_de_mode="off",
        )
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": "shadow"}):
        candidate = grade_deterministically(
            question_text=question, answer_text=answer, qualitative_de_mode="off",
        )
    audit = candidate["claim_alignment_audit"]
    assert audit["status"] == "SHADOW"
    assert audit["score_effect"] == "none"
    assert audit["recall_review"]["score_effect"] == "none"
    for key in (
        "total_score", "deterministic_score", "score_breakdown",
        "requirements", "requirement_summary", "logic_check_evaluation",
        "passing_score_allowed", "official_pass_met", "high_score_met",
        "verdict",
    ):
        assert baseline.get(key) == candidate.get(key), key
