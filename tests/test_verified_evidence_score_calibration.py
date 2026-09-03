from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verified_evidence_score_calibration import (
    apply_verified_evidence_score_calibration,
)


def _grade(*, count: int, statuses: dict[str, int], score: float) -> dict:
    total = sum(statuses.values())
    return {
        "total_score": score,
        "final_total_score": score,
        "breakdown": [
            {"layer_id": "A", "score": score * 3 / 25, "max": 3.0},
            {"layer_id": "B", "score": score * 6 / 25, "max": 6.0},
            {"layer_id": "C", "score": score * 8 / 25, "max": 8.0},
            {"layer_id": "D", "score": score * 6 / 25, "max": 6.0},
            {"layer_id": "E", "score": score * 2 / 25, "max": 2.0},
        ],
        "volume_evaluation": {"ascii_equivalent_count": count},
        "canonical_evaluation_ledger": {
            "summary": {
                "total": total,
                "complete_assessment": True,
                "status_counts": statuses,
                "unmatched_coverage_count": 0,
                "unresolved_verified_defect_count": 0,
            }
        },
    }


def test_complete_pass_depth_is_calibrated_inside_pass_band() -> None:
    result = apply_verified_evidence_score_calibration(_grade(
        count=1560,
        statuses={"correct": 4, "partial": 0, "incorrect": 0, "missing": 0, "unknown": 0},
        score=24.0,
    ))
    assert result["total_score"] == 17.5
    assert round(sum(row["score"] for row in result["breakdown"]), 2) == 17.5


def test_complete_high_depth_is_raised_into_high_band() -> None:
    result = apply_verified_evidence_score_calibration(_grade(
        count=1980,
        statuses={"correct": 4, "partial": 0, "incorrect": 0, "missing": 0, "unknown": 0},
        score=13.5,
    ))
    assert result["total_score"] == 21.0


def test_partial_or_short_answer_is_score_neutral() -> None:
    partial = apply_verified_evidence_score_calibration(_grade(
        count=1800,
        statuses={"correct": 3, "partial": 1, "incorrect": 0, "missing": 0, "unknown": 0},
        score=16.0,
    ))
    short = apply_verified_evidence_score_calibration(_grade(
        count=900,
        statuses={"correct": 4, "partial": 0, "incorrect": 0, "missing": 0, "unknown": 0},
        score=12.0,
    ))
    assert partial["total_score"] == 16.0
    assert short["total_score"] == 12.0


def test_calibration_is_idempotent() -> None:
    once = apply_verified_evidence_score_calibration(_grade(
        count=1800,
        statuses={"correct": 4, "partial": 0, "incorrect": 0, "missing": 0, "unknown": 0},
        score=15.0,
    ))
    assert apply_verified_evidence_score_calibration(once) == once


def test_calibration_reasserts_target_after_legacy_reconciliation() -> None:
    once = apply_verified_evidence_score_calibration(_grade(
        count=1800,
        statuses={"correct": 4, "partial": 0, "incorrect": 0, "missing": 0, "unknown": 0},
        score=24.0,
    ))
    once["total_score"] = 24.0
    once["final_total_score"] = 24.0
    twice = apply_verified_evidence_score_calibration(once)
    assert twice["total_score"] == 19.5
    assert twice["final_total_score"] == 19.5


def test_neutral_early_marker_is_rechecked_when_evidence_arrives() -> None:
    grade = _grade(
        count=1800,
        statuses={"correct": 4, "partial": 0, "incorrect": 0, "missing": 0, "unknown": 0},
        score=12.0,
    )
    grade["verified_evidence_score_calibration"] = {
        "marker": "VERIFIED_EVIDENCE_SCORE_CALIBRATION_V1",
        "applied": False,
        "score_effect": "none",
    }
    result = apply_verified_evidence_score_calibration(grade)
    assert result["total_score"] == 19.5
    assert result["verified_evidence_score_calibration"]["applied"] is True


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"VERIFIED_EVIDENCE_SCORE_CALIBRATION_TESTS={len(tests)}_PASS")
