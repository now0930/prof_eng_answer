from __future__ import annotations

import unittest

from deterministic_score_engine import calculate_deterministic_score


def _evaluation(statuses: list[str], *, fatal: bool = False) -> dict:
    return {
        "requirements": [{"status": status} for status in statuses],
        "findings": [],
        "fatal_or_core_error": fatal,
    }


def _grouped_evaluation(rows: list[tuple[str, str]]) -> dict:
    return {
        "requirements": [
            {"requirement_id": f"r{index}", "status": status, "score_group_id": group}
            for index, (group, status) in enumerate(rows)
        ],
        "findings": [],
        "fatal_or_core_error": False,
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

    def test_duplicate_evidence_rows_count_as_one_scoring_demand(self) -> None:
        result = calculate_deterministic_score(_grouped_evaluation([
            ("unit_test", "WRONG"),
            ("unit_test", "WRONG"),
            ("system_test", "PARTIAL"),
        ]))
        self.assertEqual(result["raw_requirement_count"], 3)
        self.assertEqual(result["scoring_group_count"], 2)
        self.assertEqual(
            {row["score_group_id"]: row["status"] for row in result["scoring_groups"]},
            {"unit_test": "WRONG", "system_test": "PARTIAL"},
        )

    def test_wrong_dominates_other_evidence_in_same_group(self) -> None:
        result = calculate_deterministic_score(_grouped_evaluation([
            ("mcdc", "SATISFIED"),
            ("mcdc", "WRONG"),
            ("mcdc", "MISSING"),
        ]))
        self.assertEqual(result["scoring_groups"][0]["status"], "WRONG")

    def test_satisfied_dominates_noncontradictory_missing_evidence(self) -> None:
        result = calculate_deterministic_score(_grouped_evaluation([
            ("vmodel", "SATISFIED"),
            ("vmodel", "MISSING"),
        ]))
        self.assertEqual(result["scoring_groups"][0]["status"], "SATISFIED")

    def test_unscoped_same_name_requirements_remain_separate_by_owner(self) -> None:
        evaluation = {
            "requirements": [
                {"owner_topic_id": "topic_a", "requirement_id": "definition", "status": "SATISFIED"},
                {"owner_topic_id": "topic_b", "requirement_id": "definition", "status": "MISSING"},
            ],
            "findings": [],
            "fatal_or_core_error": False,
        }
        result = calculate_deterministic_score(evaluation)
        self.assertEqual(result["scoring_group_count"], 2)


if __name__ == "__main__":
    unittest.main()
