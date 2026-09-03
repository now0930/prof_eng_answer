from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verified_evidence_score_calibration import apply_verified_evidence_score_calibration


SCORE_FIELDS = (
    "total_score", "final_total_score", "breakdown", "layer_scores",
    "rater_weighted_evaluation",
)


def _grade(*, count: int, score: float, question_type: str) -> dict:
    breakdown = [
        {"layer_id": "A", "score": score * 3 / 25, "max": 3.0},
        {"layer_id": "B", "score": score * 6 / 25, "max": 6.0},
        {"layer_id": "C", "score": score * 8 / 25, "max": 8.0},
        {"layer_id": "D", "score": score * 6 / 25, "max": 6.0},
        {"layer_id": "E", "score": score * 2 / 25, "max": 2.0},
    ]
    return {
        "total_score": score,
        "final_total_score": score,
        "breakdown": breakdown,
        "layer_scores": [
            {"layer": name, "score": row["score"], "max": row["max"]}
            for name, row in zip("ABCDE", breakdown)
        ],
        "rater_weighted_evaluation": {
            "total_score": score,
            "weighted_total": score,
            "weighted_layers": [
                {"layer_id": row["layer_id"], "score": row["score"], "max": row["max"]}
                for row in breakdown
            ],
        },
        "question_type": question_type,
        "volume_evaluation": {"ascii_equivalent_count": count},
        "canonical_evaluation_ledger": {
            "summary": {"complete_assessment": True},
        },
    }


def _score_snapshot(grade: dict) -> dict:
    return {key: copy.deepcopy(grade.get(key)) for key in SCORE_FIELDS}


def test_volume_is_score_invariant_for_every_question_type() -> None:
    question_types = (
        "COMPARE_SELECTION", "DIAGNOSIS_ACTION",
        "IMPLEMENTATION_EVALUATION", "PRINCIPLE_INTERPRETATION",
    )
    for question_type in question_types:
        snapshots = []
        for count in (1500, 1800, 1928, 2100):
            grade = _grade(count=count, score=13.5, question_type=question_type)
            result = apply_verified_evidence_score_calibration(grade)
            assert _score_snapshot(result) == _score_snapshot(grade)
            assert result["verified_evidence_score_calibration"]["score_effect"] == "none"
            snapshots.append(result["total_score"])
        assert snapshots == [13.5] * 4


def test_calibration_never_raises_or_lowers_base_score() -> None:
    for score in (13.5, 24.0):
        grade = _grade(count=1928, score=score, question_type="IMPLEMENTATION_EVALUATION")
        result = apply_verified_evidence_score_calibration(grade)
        assert _score_snapshot(result) == _score_snapshot(grade)


def test_repeated_or_unrelated_padding_is_score_neutral() -> None:
    base = apply_verified_evidence_score_calibration(
        _grade(count=900, score=16.4, question_type="PRINCIPLE_INTERPRETATION")
    )
    padded = apply_verified_evidence_score_calibration(
        _grade(count=5000, score=16.4, question_type="PRINCIPLE_INTERPRETATION")
    )
    assert _score_snapshot(base) == _score_snapshot(padded)


def test_calibration_is_idempotent_without_reasserting_a_target() -> None:
    grade = _grade(count=1800, score=15.0, question_type="DIAGNOSIS_ACTION")
    once = apply_verified_evidence_score_calibration(grade)
    twice = apply_verified_evidence_score_calibration(once)
    assert _score_snapshot(twice) == _score_snapshot(grade)
    assert twice == once


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"VERIFIED_EVIDENCE_SCORE_CALIBRATION_TESTS={len(tests)}_PASS")
