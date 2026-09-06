"""Fail-closed gate for removal of LLM grading authority."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping


VERSION = "deterministic_authority_policy_v1"
MARKER = "DETERMINISTIC_AUTHORITY_GATE_V1"
ROOT = Path(__file__).resolve().parent
DEFAULT_POLICY = ROOT / "calibration" / "deterministic_authority_policy.json"


class GradingAuthorityError(RuntimeError):
    pass


def load_authority_policy(path: Path = DEFAULT_POLICY) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    if policy.get("version") != VERSION:
        raise GradingAuthorityError("deterministic authority policy version mismatch")
    return policy


def evaluate_authority_removal_gate(
    replay_report: Mapping[str, Any],
    *,
    known_overgrading_regression_pass: bool = False,
    normal_answer_regression_pass: bool = False,
    score_verdict_consistency_pass: bool = False,
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    selected = dict(policy or load_authority_policy())
    blockers: list[dict[str, Any]] = []

    def minimum(code: str, actual: Any, required: float) -> None:
        if isinstance(actual, bool) or not isinstance(actual, (int, float)) or actual < required:
            blockers.append({"code": code, "actual": actual, "required": required})

    def maximum(code: str, actual: Any, required: float) -> None:
        if isinstance(actual, bool) or not isinstance(actual, (int, float)) or actual > required:
            blockers.append({"code": code, "actual": actual, "required": required})

    def required_true(code: str, actual: bool) -> None:
        if actual is not True:
            blockers.append({"code": code, "actual": actual, "required": True})

    minimum(
        "KNOWN_FATAL_RECALL", replay_report.get("known_fatal_recall"),
        selected["minimum_known_fatal_recall"],
    )
    maximum(
        "FATAL_FALSE_POSITIVE_COUNT",
        replay_report.get("fatal_false_positive_count"),
        selected["maximum_fatal_false_positive_count"],
    )
    minimum(
        "DETERMINISTIC_REPEATABILITY",
        replay_report.get("deterministic_repeatability"),
        selected["minimum_deterministic_repeatability"],
    )
    maximum(
        "UNEXPLAINED_VERDICT_DIFF_COUNT",
        replay_report.get("unexplained_verdict_diff_count"),
        selected["maximum_unexplained_verdict_diff_count"],
    )
    if selected["require_known_overgrading_regression_pass"]:
        required_true("KNOWN_OVERGRADING_REGRESSION", known_overgrading_regression_pass)
    if selected["require_normal_answer_regression_pass"]:
        required_true("NORMAL_ANSWER_REGRESSION", normal_answer_regression_pass)
    if selected["require_score_verdict_consistency_pass"]:
        required_true("SCORE_VERDICT_CONSISTENCY", score_verdict_consistency_pass)
    if selected["require_external_llm_not_required"]:
        required_true(
            "EXTERNAL_LLM_REQUIRED_FOR_VERDICT",
            replay_report.get("external_llm_required_for_verdict") is False,
        )
    ready = not blockers
    return {
        "version": VERSION,
        "marker": MARKER,
        "decision": "READY" if ready else "HOLD",
        "ready": ready,
        "requested_target": {
            "EXTERNAL_LLM_REQUIRED_FOR_VERDICT": 0,
            "LLM_VERDICT_AUTHORITY": 0,
            "DETERMINISTIC_GRADING_PRIMARY": True,
        },
        "blockers": blockers,
        "policy": selected,
    }


def enforce_requested_authority_mode(
    *,
    environ: Mapping[str, str] | None = None,
    gate_report: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Reject premature deterministic-primary activation."""
    env = environ if environ is not None else os.environ
    requested = str(env.get("DETERMINISTIC_GRADING_PRIMARY") or "").casefold() in {
        "1", "true", "yes", "on",
    }
    if not requested:
        return {
            "mode": "legacy_primary_with_deterministic_shadow",
            "DETERMINISTIC_GRADING_PRIMARY": False,
            "LLM_VERDICT_AUTHORITY": 1,
            "EXTERNAL_LLM_REQUIRED_FOR_VERDICT": 1,
        }
    if not isinstance(gate_report, Mapping) or gate_report.get("ready") is not True:
        raise GradingAuthorityError(
            "deterministic primary activation rejected: authority gate is not READY"
        )
    raise GradingAuthorityError(
        "deterministic primary activation rejected: primary score engine is not connected"
    )
