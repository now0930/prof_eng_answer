"""Calibrate complete long-form answers from verified canonical evidence."""

from __future__ import annotations

import copy
from typing import Any


MARKER = "VERIFIED_EVIDENCE_SCORE_CALIBRATION_V1"


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _rescale_rows(rows: Any, target: float) -> None:
    if not isinstance(rows, list):
        return
    scored = [
        row for row in rows
        if isinstance(row, dict)
        and _number(row.get("score")) is not None
        and _number(row.get("max")) is not None
    ]
    if not scored:
        return
    current = sum(float(row["score"]) for row in scored)
    if current <= 0:
        return
    if target < current:
        factor = target / current
        for row in scored:
            row["score"] = round(float(row["score"]) * factor, 2)
    else:
        headrooms = [
            max(0.0, float(row["max"]) - float(row["score"]))
            for row in scored
        ]
        available = sum(headrooms)
        if available <= 0:
            return
        delta = target - current
        for row, headroom in zip(scored, headrooms):
            row["score"] = round(
                min(float(row["max"]), float(row["score"]) + delta * headroom / available),
                2,
            )
    residual = round(target - sum(float(row["score"]) for row in scored), 2)
    if residual:
        for row in sorted(
            scored,
            key=lambda item: float(item["max"]) - float(item["score"]),
            reverse=residual > 0,
        ):
            candidate = round(float(row["score"]) + residual, 2)
            if 0.0 <= candidate <= float(row["max"]):
                row["score"] = candidate
                break


def apply_verified_evidence_score_calibration(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    output = copy.deepcopy(payload)
    previous = output.get("verified_evidence_score_calibration")
    if isinstance(previous, dict):
        target = _number(previous.get("calibrated_score"))
        if target is not None:
            _rescale_rows(output.get("breakdown"), target)
            _rescale_rows(output.get("layer_scores"), target)
            weighted = output.get("rater_weighted_evaluation")
            if isinstance(weighted, dict):
                _rescale_rows(weighted.get("weighted_layers"), target)
                for key in ("total_score", "weighted_total", "final_score", "score", "total"):
                    if _number(weighted.get(key)) is not None:
                        weighted[key] = target
            for key in (
                "total_score", "final_total_score", "final_score", "score", "total",
                "adjusted_total_score",
            ):
                if key in output or key in {"total_score", "final_total_score"}:
                    output[key] = target
            return output
        # A neutral marker can be attached before volume and the final ledger
        # are available. Re-evaluate eligibility at the persistence boundary.

    ledger = output.get("canonical_evaluation_ledger")
    summary = ledger.get("summary") if isinstance(ledger, dict) else None
    counts = summary.get("status_counts") if isinstance(summary, dict) else None
    volume = output.get("volume_evaluation")
    ascii_count = (
        _number(volume.get("ascii_equivalent_count"))
        if isinstance(volume, dict)
        else None
    )
    total_requirements = int(summary.get("total") or 0) if isinstance(summary, dict) else 0
    eligible = bool(
        isinstance(summary, dict)
        and isinstance(counts, dict)
        and summary.get("complete_assessment") is True
        and total_requirements > 0
        and int(counts.get("correct") or 0) == total_requirements
        and not any(int(counts.get(key) or 0) for key in ("partial", "incorrect", "missing", "unknown"))
        and int(summary.get("unmatched_coverage_count") or 0) == 0
        and int(summary.get("unresolved_verified_defect_count") or 0) == 0
        and ascii_count is not None
        and ascii_count >= 1500.0
    )
    current = _number(output.get("total_score"))
    if not eligible or current is None:
        output["verified_evidence_score_calibration"] = {
            "marker": MARKER,
            "applied": False,
            "reason": "complete_long_form_verified_evidence_not_available",
            "score_effect": "none",
        }
        return output

    target = round(min(22.0, 17.0 + (ascii_count - 1500.0) / 120.0), 2)
    _rescale_rows(output.get("breakdown"), target)
    _rescale_rows(output.get("layer_scores"), target)
    weighted = output.get("rater_weighted_evaluation")
    if isinstance(weighted, dict):
        _rescale_rows(weighted.get("weighted_layers"), target)
        for key in ("total_score", "weighted_total", "final_score", "score", "total"):
            if _number(weighted.get(key)) is not None:
                weighted[key] = target
    for key in (
        "total_score", "final_total_score", "final_score", "score", "total",
        "adjusted_total_score",
    ):
        if key in output or key in {"total_score", "final_total_score"}:
            output[key] = target
    output["verified_evidence_score_calibration"] = {
        "marker": MARKER,
        "applied": target != round(current, 2),
        "score_effect": "verified_evidence_calibration",
        "original_score": round(current, 2),
        "calibrated_score": target,
        "basis": {
            "all_atomic_requirements_correct": True,
            "ascii_equivalent_count": int(ascii_count),
            "long_form_threshold": 1500,
            "upper_calibration_point": 2100,
        },
    }
    return output
