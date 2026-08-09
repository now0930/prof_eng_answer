from __future__ import annotations

from copy import deepcopy
import unittest

import grading_agents as ga


GENERIC_GRADE = {
    "question_type_evaluation": {},
    "summary": "기존 요약",
    "rewrite_advice": [
        (
            "배경 → 문제 요구 → 유형별 Fact 기반 내용 설명 → "
            "현장 적용·설계 판단·제언 순서로 답안을 확장하세요."
        ),
        (
            "대책은 비용, 시간, 적용 가능성, 기존 설비 영향, "
            "운전 리스크까지 연결하세요."
        ),
        "핵심 원리와 변수 관계를 더 명확히 설명하세요.",
    ],
    "improvement_points": [
        (
            "FIELD_APPLICATION 보완: 선정 기준, 현장 조건, 문제점, "
            "개선방안, 비용·유지보수 영향을 함께 쓰세요."
        ),
        "누락된 명시 요구를 보완하세요.",
    ],
    "next_practice_focus": [
        "현장 적용성, 제언, 기술사적 판단 제시",
        "문제 요구 해석·완전성",
    ],
    "weaknesses": [
        "비용 대비 성능(Cost-Benefit) 검토가 부족합니다.",
        "핵심 변수의 의미 설명이 부족합니다.",
    ],
}


def run_policy(
    qid: str,
    question: str,
    grade: dict | None = None,
) -> dict:
    return ga._phase9_apply_type_aware_de_feedback_policy(
        grade=deepcopy(grade or GENERIC_GRADE),
        question_type_eval={
            "question_type": qid,
        },
        input_text=question,
    )


def joined(grade: dict) -> str:
    values = []

    for key in (
        "rewrite_advice",
        "improvement_points",
        "next_practice_focus",
        "weaknesses",
    ):
        values.extend(
            str(item)
            for item in grade.get(key) or []
        )

    return "\n".join(values)


class GenericFeedbackFinalProjectionTest(unittest.TestCase):
    def test_define_removes_unasked_field_cost_lifecycle(self) -> None:
        actual = run_policy(
            "DEFINE",
            "스마트 센서의 정의와 구성요소를 설명하시오.",
        )
        text = joined(actual)

        for token in (
            "현장 적용·설계 판단·제언 순서로",
            "비용, 시간, 적용 가능성",
            "FIELD_APPLICATION 보완:",
            "현장 적용성, 제언, 기술사적 판단 제시",
            "Cost-Benefit",
        ):
            self.assertNotIn(token, text)

        self.assertIn(
            "핵심 원리와 변수 관계를 더 명확히 설명하세요.",
            text,
        )
        self.assertIn(
            "문제 요구 해석·완전성",
            text,
        )

    def test_principle_baseline_remains_preserved(self) -> None:
        actual = run_policy(
            "PRINCIPLE_INTERPRETATION",
            "2차 시스템의 감쇠비와 과도응답 특성을 설명하시오.",
        )
        text = joined(actual)

        self.assertNotIn("Cost-Benefit", text)
        self.assertNotIn("FIELD_APPLICATION 보완:", text)
        self.assertIn("원리·해석형 D/E", text)
        self.assertIn(
            "원리·수식·변수 의미·결과 해석의 연결",
            actual["next_practice_focus"],
        )

    def test_compare_selection_keeps_tradeoff_but_not_unasked_cost(self) -> None:
        grade = {
            "question_type_evaluation": {},
            "rewrite_advice": [
                "대안 비교와 trade-off를 명확히 쓰세요.",
                "비용 대비 성능(Cost-Benefit)을 추가하세요.",
            ],
            "improvement_points": [],
            "next_practice_focus": [],
            "weaknesses": [],
        }

        actual = run_policy(
            "COMPARE_SELECTION",
            "A 방식과 B 방식을 비교하고 선정 기준을 설명하시오.",
            grade,
        )
        text = joined(actual)

        self.assertIn(
            "대안 비교와 trade-off를 명확히 쓰세요.",
            text,
        )
        self.assertNotIn("Cost-Benefit", text)

    def test_problem_solve_does_not_imply_cost_or_maintenance(self) -> None:
        grade = {
            "question_type_evaluation": {},
            "rewrite_advice": [
                "문제점과 개선방안의 인과관계를 연결하세요.",
                "비용·유지보수·기존 설비 영향을 함께 쓰세요.",
            ],
            "improvement_points": [],
            "next_practice_focus": [],
            "weaknesses": [],
        }

        actual = run_policy(
            "PROBLEM_SOLVE",
            "제어계의 문제점을 분석하고 개선방안을 설명하시오.",
            grade,
        )
        text = joined(actual)

        self.assertIn(
            "문제점과 개선방안의 인과관계를 연결하세요.",
            text,
        )
        self.assertNotIn(
            "비용·유지보수·기존 설비",
            text,
        )

    def test_explicit_cost_demand_is_preserved(self) -> None:
        grade = {
            "question_type_evaluation": {},
            "rewrite_advice": [
                "비용 대비 성능(Cost-Benefit)을 비교하세요.",
            ],
            "improvement_points": [],
            "next_practice_focus": [],
            "weaknesses": [],
        }

        actual = run_policy(
            "COMPARE_SELECTION",
            (
                "두 방식을 비교하고 비용과 유지보수성을 포함하여 "
                "선정 기준을 제시하시오."
            ),
            grade,
        )

        self.assertIn(
            "비용 대비 성능(Cost-Benefit)을 비교하세요.",
            actual["rewrite_advice"],
        )
        projection = actual[
            "public_feedback_question_demand_projection"
        ]
        self.assertTrue(
            projection[
                "explicit_cost_or_lifecycle_demand"
            ]
        )

    def test_projection_is_feedback_only(self) -> None:
        grade = deepcopy(GENERIC_GRADE)
        grade.update({
            "total_score": 17.25,
            "breakdown": [
                {
                    "layer_id": "D",
                    "score": 4.0,
                    "max": 6.0,
                },
                {
                    "layer_id": "E",
                    "score": 1.0,
                    "max": 2.0,
                },
            ],
            "difficulty_strategy": {
                "difficulty": "FIELD_APPLICATION",
            },
        })

        actual = run_policy(
            "DEFINE",
            "스마트 센서의 정의를 설명하시오.",
            grade,
        )

        self.assertEqual(actual["total_score"], 17.25)
        self.assertEqual(
            actual["breakdown"],
            grade["breakdown"],
        )
        self.assertEqual(
            actual["difficulty_strategy"],
            grade["difficulty_strategy"],
        )
        projection = actual[
            "public_feedback_question_demand_projection"
        ]
        self.assertFalse(
            projection["score_axis_changed"]
        )
        self.assertFalse(
            projection["difficulty_axis_changed"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
