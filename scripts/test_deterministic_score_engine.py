from __future__ import annotations

import unittest

from deterministic_score_engine import calculate_deterministic_score


def _evaluation(statuses: list[str], *, fatal: bool = False) -> dict:
    return {
        "requirements": [{"status": status} for status in statuses],
        "findings": [],
        "fatal_or_core_error": fatal,
    }


class DeterministicScoreCeilingTests(unittest.TestCase):
    def test_partial_only_nonfatal_answer_cannot_reach_mid_band(self) -> None:
        result = calculate_deterministic_score(
            _evaluation(["PARTIAL", "PARTIAL"]),
        )
        self.assertEqual(result["total_score"], 11.0)
        self.assertTrue(result["no_satisfied_nonfatal_ceiling_applied"])

    def test_one_satisfied_requirement_removes_partial_only_ceiling(self) -> None:
        result = calculate_deterministic_score(
            _evaluation(["SATISFIED", "MISSING"]),
        )
        self.assertEqual(result["total_score"], 12.5)
        self.assertFalse(result["no_satisfied_nonfatal_ceiling_applied"])

    def test_fatal_policy_keeps_its_independent_score_boundary(self) -> None:
        result = calculate_deterministic_score(
            _evaluation(["PARTIAL", "PARTIAL"], fatal=True),
        )
        self.assertEqual(result["total_score"], 12.5)
        self.assertFalse(result["no_satisfied_nonfatal_ceiling_applied"])


if __name__ == "__main__":
    unittest.main()
