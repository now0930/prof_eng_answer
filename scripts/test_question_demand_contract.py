from __future__ import annotations

import copy
import unittest

import gemini_grader
from question_demand_contract import (
    QUESTION_DEMAND_CONTRACT_MARKER,
    attach_question_demand_contract,
    build_question_demand_contract,
    normalize_question_text,
)


# QUESTION_DEMAND_CONTRACT_REGRESSION_V1


class QuestionDemandContractTests(unittest.TestCase):
    def test_principle_and_design_question_uses_hybrid_contract(self):
        contract = build_question_demand_contract(
            "불평형력과 마찰력의 개념을 설명하시오. "
            "Fail-safe 스프링 설계 기준을 제시하시오."
        )

        self.assertEqual(
            contract["primary_lens"],
            "PRINCIPLE_INTERPRETATION",
        )
        secondary = {
            row["demand_kind"]
            for row in contract["secondary_demands"]
        }
        self.assertIn("DESIGN", secondary)
        self.assertTrue(contract["primary_lens_locked"])
        self.assertEqual(
            contract["answer_text_dependency"],
            "none",
        )

    def test_compare_selection_question_uses_compare_primary(self):
        contract = build_question_demand_contract(
            "열전대와 RTD를 비교하고 선정 기준을 설명하시오."
        )

        self.assertEqual(
            contract["primary_lens"],
            "COMPARE_SELECTION",
        )

    def test_cause_and_action_question_uses_diagnosis_primary(self):
        contract = build_question_demand_contract(
            "측정 오차의 원인을 분석하고 저감 대책을 제시하시오."
        )

        self.assertEqual(
            contract["primary_lens"],
            "DIAGNOSIS_ACTION",
        )

    def test_implementation_evaluation_question_uses_implementation_primary(self):
        contract = build_question_demand_contract(
            "스마트 MCC 적용 방법과 도입 효과를 평가하시오."
        )

        self.assertEqual(
            contract["primary_lens"],
            "IMPLEMENTATION_EVALUATION",
        )

    def test_contract_is_stable_across_symbol_variants(self):
        first = build_question_demand_contract(
            "▶️ PID 제어 원리를 설명하시오."
        )
        second = build_question_demand_contract(
            "▶ PID 제어 원리를 설명하시오."
        )

        self.assertEqual(
            first["normalized_question"],
            second["normalized_question"],
        )
        self.assertEqual(
            first["question_hash"],
            second["question_hash"],
        )
        self.assertEqual(
            first["requirements"],
            second["requirements"],
        )

    def test_requirement_ids_are_deterministic(self):
        question = (
            "원리를 설명하고 설계 기준과 검증 방법을 제시하시오."
        )

        first = build_question_demand_contract(question)
        second = build_question_demand_contract(question)

        self.assertEqual(
            first["requirements"],
            second["requirements"],
        )
        self.assertTrue(
            all(
                row["requirement_id"].startswith("requirement_")
                for row in first["requirements"]
            )
        )

    def test_result_attachment_preserves_score_fields(self):
        grade = {
            "score": 18.0,
            "total_score": 18.0,
            "layer_scores": [
                {"layer_id": "B", "score": 5.0},
                {"layer_id": "C", "score": 5.5},
            ],
            "parsed": {},
        }
        before = copy.deepcopy(grade)

        attached = attach_question_demand_contract(
            grade,
            "원리를 설명하고 설계 기준을 제시하시오.",
        )

        self.assertEqual(grade, before)
        self.assertEqual(attached["score"], before["score"])
        self.assertEqual(
            attached["total_score"],
            before["total_score"],
        )
        self.assertEqual(
            attached["layer_scores"],
            before["layer_scores"],
        )
        self.assertEqual(
            attached["question_demand_contract"],
            attached["parsed"]["question_demand_contract"],
        )

    def test_prompt_contains_locked_question_only_contract(self):
        prompt = gemini_grader.build_gemini_grading_prompt(
            question_text=(
                "원리를 설명하고 설계 기준을 제시하시오."
            ),
            answer_text=(
                "비교표를 중심으로 작성한 답안이다."
            ),
            scoring_model={},
            subject_rubric={},
            rater_profile={},
            volume={},
            fact_eval={},
            connection_eval={},
        )

        self.assertIn(
            QUESTION_DEMAND_CONTRACT_MARKER,
            prompt,
        )
        self.assertIn(
            '"primary_lens": "PRINCIPLE_INTERPRETATION"',
            prompt,
        )
        self.assertIn(
            '"demand_kind": "DESIGN"',
            prompt,
        )
        self.assertIn(
            "답안 내용으로 primary_lens를 변경하거나 재분류하지 않는다",
            prompt,
        )

    def test_normalization_does_not_accept_answer_text(self):
        self.assertEqual(
            normalize_question_text("  문제  "),
            "문제",
        )

        contract = build_question_demand_contract(
            "원리를 설명하시오."
        )

        self.assertNotIn("answer_text", contract)
        self.assertEqual(
            contract["answer_text_dependency"],
            "none",
        )


if __name__ == "__main__":
    unittest.main()
