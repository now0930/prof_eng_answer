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
        self.assertLessEqual(result["total_score"], 18.5)
        self.assertFalse(result["high_score_met"])

    def test_generic_cues_cannot_award_exceptional_last_point(self):
        evaluation = {
            "requirements": [{"status": "SATISFIED"}] * 4,
            "findings": [], "fatal_or_core_error": False,
        }
        answer = (
            "1. 현장 선정 검증\n- 현장 설비 선정 조건과 시험 기록을 관리한다.\n"
            "2. 공학 판단\n- 비용 영향 위험 한계와 수식 경계를 검증한다.\n"
            "3. 결론\n- 조건에 따라 확인하면 결론으로 연결된다.\n" + "충분한 설명 " * 400
        )
        result = calculate_deterministic_score(evaluation, answer_text=answer)
        self.assertEqual(result["total_score"], 24.0)
        self.assertEqual(result["maximum_automatic_score"], 24.0)

    def test_ineligible_depth_uses_practical_band_upper_ceiling(self):
        evaluation = {
            "requirements": [{"status": "SATISFIED"}] * 4,
            "findings": [], "fatal_or_core_error": False,
        }
        result = calculate_deterministic_score(
            evaluation,
            answer_text=(
                "1. 현장 선정 검증\n- 현장 설비 선정 조건과 시험 기록을 관리한다.\n"
                "2. 결론\n- 위험과 비용 영향에 따라 확인한다."
            ),
        )
        self.assertLessEqual(result["total_score"], 18.5)
        self.assertEqual(result["high_score_ineligible_ceiling"], 18.5)


if __name__ == "__main__":
    unittest.main()
