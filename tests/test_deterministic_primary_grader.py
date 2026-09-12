import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_primary_grader import grade_deterministically, persist_deterministic_grade
from grading_agents import finalize_grade_after_score_reconciliation, run_agent_pipeline


class DeterministicPrimaryGraderTests(unittest.TestCase):
    def test_provider_free_grade_has_public_score_and_fatal_consistency(self):
        grade = grade_deterministically(
            question_text="SIL 결정 방법을 설명하시오.",
            answer_text="lambda_SIS 비율이 PFD 비율보다 작도록 설계한다.",
        )
        self.assertEqual(grade["provider_calls"], 0)
        self.assertEqual(grade["llm_verdict_authority"], 0)
        self.assertTrue(grade["logic_check_evaluation"]["fatal_error_detected"])
        self.assertFalse(grade["official_pass_met"])

    def test_persistence_is_provider_neutral_json(self):
        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대는 제벡 효과로 온도차에 따른 열기전력을 측정한다.",
        )
        with tempfile.TemporaryDirectory() as directory:
            raw = persist_deterministic_grade(directory, grade)
            self.assertIn("DETERMINISTIC_GRADING_PRIMARY_V1", raw)
            self.assertTrue((Path(directory) / "deterministic_grade.json").is_file())

    def test_production_entrypoint_bypasses_llm_callable(self):
        calls = []

        def forbidden_call(prompt):
            calls.append(prompt)
            raise AssertionError("external LLM must not be called")

        with tempfile.TemporaryDirectory() as directory, patch.dict(
            "os.environ", {"DETERMINISTIC_GRADING_PRIMARY": "true"}, clear=False,
        ):
            _, grade = run_agent_pipeline(
                call_ollama_fn=forbidden_call,
                raw_text=(
                    "[문제] 열전대 온도센서의 측정 원리를 설명하시오.\n"
                    "[답안]\n열전대는 제벡 효과에 따른 열기전력을 측정한다."
                ),
                rubric={}, sid="deterministic-primary-test", image_count=0,
                session_dir=directory,
            )
        self.assertEqual(calls, [])
        self.assertEqual(grade["marker"], "DETERMINISTIC_GRADING_PRIMARY_V1")
        self.assertGreater(grade["total_score"], 0.0)

    def test_reconciler_cannot_call_llm_or_change_deterministic_grade(self):
        from grade_score_reconciler import reconcile_grade_score

        grade = {
            "marker": "DETERMINISTIC_GRADING_PRIMARY_V1",
            "total_score": 14.5,
            "max_score": 25.0,
            "verdict": "FAIL",
            "deterministic_score": {
                "total_score": 14.5,
                "raw_score": 16.37,
                "applied_ceiling": 14.5,
            },
        }
        result = reconcile_grade_score(
            parsed=grade,
            raw_text="unused",
            call_llm_fn=lambda _: (_ for _ in ()).throw(AssertionError("LLM called")),
        )
        self.assertIs(result, grade)

    def test_legacy_finalizers_cannot_change_deterministic_grade(self):
        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대는 제벡 효과에 따른 열기전력을 측정한다.",
        )
        result = finalize_grade_after_score_reconciliation(grade)
        self.assertIs(result, grade)
        self.assertEqual(result["total_score"], grade["deterministic_score"]["total_score"])

    def test_telegram_formatting_does_not_call_llm(self):
        import bot

        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대는 제벡 효과에 따른 열기전력을 측정한다.",
        )
        with patch.object(
            bot,
            "call_ollama",
            side_effect=AssertionError("LLM called"),
        ):
            rendered = bot.format_result(grade)
        self.assertIn("채점 완료:", rendered)
        self.assertIn("[결정론적 요구 판정]", rendered)
        self.assertEqual(grade["verdict"], grade["deterministic_score"]["verdict"])

    def test_telegram_breakdown_rounds_display_only_and_lists_missing_ids(self):
        import bot

        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대를 언급한다.",
        )
        grade["breakdown"][1]["score"] = 4.434783
        rendered = bot.format_result(grade)
        self.assertIn("4.43/6", rendered)
        self.assertNotIn("4.434783/6", rendered)
        self.assertIn("누락 요구:", rendered)
        self.assertEqual(grade["breakdown"][1]["score"], 4.434783)

    def test_partial_mentions_alone_cannot_reach_passing_score(self):
        grade = grade_deterministically(
            question_text=(
                "제어 소프트웨어 개발 수명 주기(V-Model)의 단위 시험, 통합 시험, "
                "시스템 시험과 SIL 달성을 위한 검증 방안을 설명하시오."
            ),
            answer_text=(
                "V-Model과 검증, 시험, 시스템, 요구사항, 인터페이스, 모델, "
                "복잡도, 변경관리의 필요성을 언급한다."
            ),
        )
        score = grade["deterministic_score"]
        self.assertFalse(score["pass_evidence_eligible"])
        self.assertLess(grade["total_score"], 15.0)


if __name__ == "__main__":
    unittest.main()
