from __future__ import annotations

from copy import deepcopy
import unittest

from grading_agents import (
    _phase8_build_question_type_originality_scope_contract,
    _phase8_project_question_type_originality_scope,
)
from originality_grader import build_originality_prompt


def qtype(qid: str) -> dict:
    return {
        "primary_type": {
            "id": qid,
            "confidence": "high",
        }
    }


def synthetic_eval() -> dict:
    return {
        "ok": True,
        "raw_text": "audit raw preserved",
        "parsed": {
            "anchors": [
                {
                    "id": "O1",
                    "name": "문제 재해석 능력",
                    "level": 0.5,
                    "reason": "핵심 관계를 재구성함.",
                    "evidence": ["원리 관계를 재구성함."],
                },
                {
                    "id": "O2",
                    "name": "현장 조건 반영",
                    "level": 0.8,
                    "reason": "설치·유지보수 조건을 제시함.",
                    "evidence": ["현장 설치 조건 제시"],
                },
                {
                    "id": "O3",
                    "name": "대안 비교와 trade-off",
                    "level": 0.7,
                    "reason": "대안 trade-off를 제시함.",
                    "evidence": ["대안 비교"],
                },
                {
                    "id": "O4",
                    "name": "적용 우선순위 제시",
                    "level": 0.6,
                    "reason": "적용 우선순위를 제시함.",
                    "evidence": ["우선순위 제시"],
                },
                {
                    "id": "O5",
                    "name": "검증 가능성",
                    "level": 0.5,
                    "reason": "결과 해석의 검증 근거를 제시함.",
                    "evidence": ["검증 근거"],
                },
            ],
            "improvement_advice": [
                "현장 설치조건과 유지보수 비용을 추가하세요.",
                "원리와 변수 관계를 더 명확히 연결하세요.",
            ],
        },
    }


class QuestionTypeOriginalityDemandScopeTest(unittest.TestCase):
    def test_principle_excludes_unasked_field_tradeoff_priority(self) -> None:
        contract = (
            _phase8_build_question_type_originality_scope_contract(
                "2차 시스템의 감쇠비와 과도응답 특성을 설명하시오.",
                qtype("PRINCIPLE_INTERPRETATION"),
            )
        )

        self.assertEqual(
            contract["allowed_anchor_ids"],
            ["O1", "O5"],
        )

        projected = _phase8_project_question_type_originality_scope(
            synthetic_eval(),
            contract,
        )

        anchors = {
            row["id"]: row
            for row in projected["parsed"]["anchors"]
        }

        self.assertEqual(anchors["O2"]["level"], 0.0)
        self.assertEqual(anchors["O3"]["level"], 0.0)
        self.assertEqual(anchors["O4"]["level"], 0.0)
        self.assertEqual(anchors["O1"]["level"], 0.5)
        self.assertEqual(anchors["O5"]["level"], 0.5)

        # Applicability denominator is only O1/O5, so a principle question
        # is not numerically punished because O2/O3/O4 are non-applicable.
        self.assertEqual(
            projected["parsed"]["average_level"],
            0.5,
        )
        self.assertEqual(
            projected["parsed"]["raw_originality_score"],
            1.0,
        )
        self.assertEqual(
            projected["parsed"]["improvement_advice"],
            ["원리와 변수 관계를 더 명확히 연결하세요."],
        )
        self.assertEqual(
            projected["raw_text"],
            "audit raw preserved",
        )

    def test_compare_selection_enables_tradeoff_and_priority(self) -> None:
        contract = (
            _phase8_build_question_type_originality_scope_contract(
                "두 센서를 비교하고 선정기준을 설명하시오.",
                qtype("COMPARE_SELECTION"),
            )
        )

        self.assertEqual(
            set(contract["allowed_anchor_ids"]),
            {"O1", "O3", "O4", "O5"},
        )

    def test_problem_solve_keeps_all_originality_axes(self) -> None:
        contract = (
            _phase8_build_question_type_originality_scope_contract(
                "문제점의 원인을 분석하고 개선방안을 제시하시오.",
                qtype("PROBLEM_SOLVE"),
            )
        )

        self.assertEqual(
            set(contract["allowed_anchor_ids"]),
            {"O1", "O2", "O3", "O4", "O5"},
        )

    def test_procedure_scope_is_not_field_content_checklist(self) -> None:
        contract = (
            _phase8_build_question_type_originality_scope_contract(
                "계측기 교정 절차와 방법을 설명하시오.",
                qtype("PROCEDURE"),
            )
        )

        self.assertEqual(
            set(contract["allowed_anchor_ids"]),
            {"O1", "O4", "O5"},
        )

    def test_explicit_field_demand_can_enable_o2(self) -> None:
        contract = (
            _phase8_build_question_type_originality_scope_contract(
                "원리를 설명하고 현장 적용 시 설치조건을 제시하시오.",
                qtype("PRINCIPLE_INTERPRETATION"),
            )
        )

        self.assertIn("O2", contract["allowed_anchor_ids"])

    def test_prompt_uses_generic_contract_marker(self) -> None:
        contract = (
            _phase8_build_question_type_originality_scope_contract(
                "2차 시스템의 감쇠비를 설명하시오.",
                qtype("PRINCIPLE_INTERPRETATION"),
            )
        )

        prompt = build_originality_prompt(
            question_text="2차 시스템의 감쇠비를 설명하시오.",
            answer_text="감쇠비와 극점 관계를 설명한다.",
            question_scope_contract=contract,
        )

        self.assertIn(
            "[QUESTION_TYPE_ORIGINALITY_DEMAND_SCOPE_V1]",
            prompt,
        )
        self.assertNotIn(
            "[HYBRID_ORIGINALITY_DEMAND_SCOPE_V1]",
            prompt,
        )
        self.assertIn(
            '"allowed_anchor_ids"',
            prompt,
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
