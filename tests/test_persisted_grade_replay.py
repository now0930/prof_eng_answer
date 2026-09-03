from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from persisted_grade_replay import restore_retired_volume_policy_for_replay


def test_legacy_volume_replay_recovers_recorded_base_score_only_from_metadata() -> None:
    stored = {
        "total_score": 20.57,
        "final_total_score": 20.57,
        "breakdown": [
            {"layer_id": "A", "score": 2.59}, {"layer_id": "B", "score": 5.03},
            {"layer_id": "C", "score": 6.19}, {"layer_id": "D", "score": 5.07},
            {"layer_id": "E", "score": 1.69},
        ],
        "verified_evidence_score_calibration": {
            "marker": "VERIFIED_EVIDENCE_SCORE_CALIBRATION_V1",
            "applied": True,
            "score_effect": "verified_evidence_calibration",
            "original_score": 14.3,
        },
    }
    replay = restore_retired_volume_policy_for_replay(stored)
    assert stored["total_score"] == 20.57
    assert replay["total_score"] == 14.3
    assert round(sum(row["score"] for row in replay["breakdown"]), 2) == 14.3
    assert replay["legacy_volume_policy_replay"]["applied"] is True


def test_current_or_unrelated_artifact_is_not_changed() -> None:
    stored = {"total_score": 11.97, "verified_evidence_score_calibration": {"marker": "V2"}}
    replay = restore_retired_volume_policy_for_replay(stored)
    assert replay["total_score"] == 11.97
    assert replay["legacy_volume_policy_replay"]["applied"] is False


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"PERSISTED_GRADE_REPLAY_TESTS={len(tests)}_PASS")
