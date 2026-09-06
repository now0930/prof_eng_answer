import unittest
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from demand_state_stability import analyze_stability


def _gold():
    return [{
        "version": "expert_accuracy_case_v1",
        "case_id": "case-1",
        "review_status": "reviewed",
        "review": {
            "reviewer": "expert",
            "method": "expert_review",
            "reviewed_at": "2026-09-06T00:00:00+00:00",
        },
        "labels": {
            "demands": [
                {"demand_id": "d1", "requirement": "first", "status": "CORRECT"},
                {"demand_id": "d2", "requirement": "second", "status": "PARTIAL"},
            ],
            "findings": [],
            "score_range": {"min": 10, "max": 15},
            "flags": {
                "passing_score_allowed": False,
                "strong_verdict_allowed": False,
                "confidence_ceiling": "medium",
            },
        },
    }]


def _prediction(score, demands):
    return [{
        "version": "expert_accuracy_prediction_v1",
        "case_id": "case-1",
        "demands": demands,
        "findings": [],
        "total_score": score,
        "passing_score_allowed": False,
        "strong_verdict_allowed": False,
        "confidence": "medium",
    }]


class DemandStateStabilityTests(unittest.TestCase):
    def test_stability_counts_omitted_demands_as_unknown(self):
        report = analyze_stability(_gold(), [
            ("run-a", _prediction(12, [
                {"demand_id": "d1", "requirement": "first", "status": "CORRECT"},
                {"demand_id": "d2", "requirement": "second", "status": "PARTIAL"},
            ])),
            ("run-b", _prediction(14, [
                {"demand_id": "d1", "requirement": "first", "status": "MISSING"},
            ])),
        ])

        self.assertEqual(report["reviewed_demand_count"], 2)
        self.assertEqual(report["all_run_state_agreement"], 0.0)
        self.assertEqual(report["unstable_demand_count"], 2)
        self.assertEqual(report["materially_unstable_demand_count"], 1)
        self.assertEqual(report["maximum_case_score_spread"], 2.0)
        self.assertEqual(report["runs"][1]["unresolved_demand_count"], 1)

    def test_stability_requires_two_distinct_runs(self):
        with self.assertRaisesRegex(ValueError, "at least two"):
            analyze_stability(_gold(), [("only", _prediction(12, []))])


if __name__ == "__main__":
    unittest.main()
