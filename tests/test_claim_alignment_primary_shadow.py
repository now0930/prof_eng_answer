"""Production grade must be identical with claim alignment off vs shadow."""
from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from grading.scoring.deterministic_primary_grader import (
    DeterministicPrimaryError, grade_deterministically,
)


QUESTION = "PID 제어기의 P, I, D 작용과 튜닝 시 고려사항을 설명하시오."
ANSWER = (
    "비례 동작은 현재 오차에 비례한다. "
    "적분 동작은 누적 오차에 작용하여 정상상태 오차를 제거한다. "
    "미분 동작은 오차 변화율에 따른 감쇠로 진동을 줄일 수 있다."
)


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
    assert shadow["claim_alignment_audit"]["status"] in {"SHADOW", "ERROR"}
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
