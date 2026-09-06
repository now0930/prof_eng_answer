import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_score_engine import calculate_deterministic_score


class DeterministicScoreEngineTests(unittest.TestCase):
    def test_unknown_requirement_abstains_without_inventing_score(self):
        result = calculate_deterministic_score({
            "requirements": [{"status": "UNKNOWN"}], "findings": []
        })
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertIsNone(result["total_score"])
        self.assertTrue(result["external_llm_required_for_verdict"])

    def test_complete_requirements_produce_repeatable_score(self):
        evaluation = {
            "requirements": [
                {"status": "SATISFIED"}, {"status": "SATISFIED"},
                {"status": "PARTIAL"}, {"status": "MISSING"},
            ],
            "findings": [], "fatal_or_core_error": False,
        }
        first = calculate_deterministic_score(evaluation)
        self.assertEqual(first, calculate_deterministic_score(evaluation))
        self.assertEqual(first["total_score"], 15.62)
        self.assertEqual(first["verdict"], "PASS")

    def test_fatal_ceiling_and_verdict_override_threshold(self):
        evaluation = {
            "requirements": [{"status": "SATISFIED"}] * 3 + [{"status": "WRONG"}],
            "findings": [{"classification": "fatal", "recommended_ceiling": 13.0}],
            "fatal_or_core_error": True,
        }
        result = calculate_deterministic_score(evaluation)
        self.assertEqual(result["total_score"], 13.0)
        self.assertEqual(result["verdict"], "NEEDS_CORRECTION")
        self.assertFalse(result["official_pass_met"])
        self.assertFalse(result["high_score_met"])

    def test_answer_evidence_produces_a_to_e_breakdown_and_volume_cap(self):
        evaluation = {
            "requirements": [{"status": "SATISFIED"}] * 4,
            "findings": [], "fatal_or_core_error": False,
        }
        result = calculate_deterministic_score(
            evaluation, answer_text="1. 원리\n- 현장 조건을 확인한다.\n2. 결론",
        )
        self.assertEqual(set(result["score_breakdown"]), {
            "A_structure", "B_requirement_completeness", "C_fact_correctness",
            "D_engineering_judgment", "E_linkage",
        })
        self.assertLessEqual(result["total_score"], 19.0)
        self.assertFalse(result["high_score_met"])


if __name__ == "__main__":
    unittest.main()
