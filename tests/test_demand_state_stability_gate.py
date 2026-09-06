import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.check_demand_state_stability_gate import evaluate


POLICY = {
    "version": "demand_state_stability_policy_v1",
    "minimum_runs": 2,
    "minimum_all_run_state_agreement": 0.9,
    "minimum_pairwise_state_agreement": 0.9,
    "maximum_material_transition_rate": 0.03,
    "maximum_case_score_spread": 4.0,
    "maximum_missing_cases_per_run": 0,
}


def _report(agreement=0.95, spread=2.0):
    return {
        "run_count": 2,
        "reviewed_demand_count": 100,
        "all_run_state_agreement": agreement,
        "materially_unstable_demand_count": 2,
        "maximum_case_score_spread": spread,
        "pairwise": [{"left": "a", "right": "b", "agreement": agreement}],
        "runs": [
            {"name": "a", "missing_case_count": 0},
            {"name": "b", "missing_case_count": 0},
        ],
    }


class DemandStateStabilityGateTests(unittest.TestCase):
    def test_stable_report_passes(self):
        self.assertEqual(evaluate(_report(), POLICY)["status"], "STABLE")

    def test_variance_fails_closed(self):
        result = evaluate(_report(agreement=0.82, spread=7.7), POLICY)
        self.assertEqual(result["status"], "HOLD")
        self.assertGreaterEqual(len(result["violations"]), 2)


if __name__ == "__main__":
    unittest.main()
