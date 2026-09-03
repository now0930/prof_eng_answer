"""Non-mutating replay support for grades corrupted by retired score policy."""

from __future__ import annotations

import copy
from typing import Any


LEGACY_MARKER = "VERIFIED_EVIDENCE_SCORE_CALIBRATION_V1"


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _restore_rows(rows: Any, target: float) -> None:
    """Recover a legacy artifact copy only; never used in live grading."""

    if not isinstance(rows, list):
        return
    scored = [row for row in rows if isinstance(row, dict) and _number(row.get("score")) is not None]
    current = sum(float(row["score"]) for row in scored)
    if current <= 0:
        return
    factor = target / current
    for row in scored:
        row["score"] = round(float(row["score"]) * factor, 2)
    residual = round(target - sum(float(row["score"]) for row in scored), 2)
    if residual:
        scored[-1]["score"] = round(float(scored[-1]["score"]) + residual, 2)


def restore_retired_volume_policy_for_replay(grade: Any) -> Any:
    """Reverse only the explicitly recorded V1 volume-calibration artifact."""

    if not isinstance(grade, dict):
        return grade
    output = copy.deepcopy(grade)
    record = output.get("verified_evidence_score_calibration")
    original = _number(record.get("original_score")) if isinstance(record, dict) else None
    eligible = bool(
        isinstance(record, dict)
        and record.get("marker") == LEGACY_MARKER
        and record.get("score_effect") == "verified_evidence_calibration"
        and record.get("applied") is True
        and original is not None
    )
    if not eligible:
        output["legacy_volume_policy_replay"] = {
            "applied": False,
            "score_effect": "none",
            "reason": "no_retired_volume_calibration_artifact",
        }
        return output
    for rows in (output.get("breakdown"), output.get("layer_scores")):
        _restore_rows(rows, original)
    weighted = output.get("rater_weighted_evaluation")
    if isinstance(weighted, dict):
        _restore_rows(weighted.get("weighted_layers"), original)
        for key in ("total_score", "weighted_total", "final_score", "score", "total"):
            if key in weighted:
                weighted[key] = original
    for key in ("total_score", "final_total_score", "final_score", "score", "total", "adjusted_total_score"):
        if key in output or key in {"total_score", "final_total_score"}:
            output[key] = original
    output["legacy_volume_policy_replay"] = {
        "applied": True,
        "score_effect": "replay_only_legacy_policy_reversal",
        "restored_base_score": round(original, 2),
        "source_marker": LEGACY_MARKER,
    }
    return output
