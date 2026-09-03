"""Record evidence-calibration diagnostics without changing grades.

This compatibility hook used to turn answer volume into a score floor. It is
now deliberately diagnostic-only: A/B/C/D/E own the base score and only
verified hard caps may reduce it.
"""

from __future__ import annotations

import copy
from typing import Any


MARKER = "VERIFIED_EVIDENCE_SCORE_CALIBRATION_V2"


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def apply_verified_evidence_score_calibration(payload: Any) -> Any:
    """Attach non-authoritative diagnostics and preserve every score field."""

    if not isinstance(payload, dict):
        return payload
    output = copy.deepcopy(payload)
    ledger = output.get("canonical_evaluation_ledger")
    summary = ledger.get("summary") if isinstance(ledger, dict) else None
    volume = output.get("volume_evaluation")
    ascii_count = (
        _number(volume.get("ascii_equivalent_count"))
        if isinstance(volume, dict)
        else None
    )
    current = _number(output.get("total_score"))
    output["verified_evidence_score_calibration"] = {
        "marker": MARKER,
        "applied": False,
        "score_effect": "none",
        "reason": "volume_and_ledger_evidence_are_diagnostic_only",
        "observed_score": round(current, 2) if current is not None else None,
        "observed_ascii_equivalent_count": (
            int(ascii_count) if ascii_count is not None else None
        ),
        "assessment_complete": (
            summary.get("complete_assessment") is True
            if isinstance(summary, dict)
            else False
        ),
        "policy": (
            "base_score=A+B+C+D+E; final_score=min(base_score, verified_hard_caps). "
            "Answer volume never raises or lowers a score."
        ),
    }
    return output
