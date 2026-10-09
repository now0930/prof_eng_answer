import json
import unittest
from pathlib import Path

from grading.scoring.deterministic_primary_grader import grade_deterministically


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/topic_atomicity_second_order_replay.json"
ZERO_ID = "so2_zero_negative_damping"
NEGATIVE_ID = "so2_negative_damping_instability"


class SecondOrderAnchorAtomicityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = {row["id"]: row for row in fixture["cases"]}

    def grade(self, case_id):
        case = self.cases[case_id]
        return grade_deterministically(
            question_text=case["question"], answer_text=case["answer"],
        )

    @staticmethod
    def statuses(grade):
        return {row["requirement_id"]: row["status"] for row in grade["requirements"]}

    def test_zero_and_negative_damping_are_independently_scored(self):
        zero = self.statuses(self.grade("zero_only"))
        negative = self.statuses(self.grade("negative_only"))
        self.assertEqual(zero[ZERO_ID], "SATISFIED")
        self.assertEqual(zero[NEGATIVE_ID], "MISSING")
        self.assertEqual(negative[ZERO_ID], "MISSING")
        self.assertEqual(negative[NEGATIVE_ID], "SATISFIED")

    def test_complete_comparison_satisfies_both_required_claims(self):
        grade = self.grade("complete_comparison")
        statuses = self.statuses(grade)
        self.assertEqual(statuses[ZERO_ID], "SATISFIED")
        self.assertEqual(statuses[NEGATIVE_ID], "SATISFIED")
        required = {
            row["requirement_id"]: row
            for row in grade["requirements"]
            if row["requirement_id"] in {ZERO_ID, NEGATIVE_ID}
        }
        self.assertTrue(all(row["pass_required"] for row in required.values()))


if __name__ == "__main__":
    unittest.main()
