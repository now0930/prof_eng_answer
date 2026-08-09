from __future__ import annotations

from copy import deepcopy
import unittest

import grading_agents as ga


RATERS = [
    {
        "rater_id": "professor",
        "rater_name": "Professor",
        "total_score": 17.0,
        "perspective": "이론 정확성과 논리 전개 관점에서 평가했습니다.",
    },
    {
        "rater_id": "professional_engineer",
        "rater_name": "Professional Engineer",
        "total_score": 17.5,
        "perspective": "실무 타당성 관점에서 평가했습니다.",
    },
    {
        "rater_id": "executive",
        "rater_name": "Executive",
        "total_score": 16.5,
        "perspective": (
            "비용, 시간, 적용 가능성, 기존 설비 영향, "
            "운영 리스크 관점에서 평가했습니다."
        ),
    },
]


def base_grade() -> dict:
    return {
        "question_type_evaluation": {},
        "total_score": 17.0,
        "difficulty_strategy": {
            "difficulty": "FIELD_APPLICATION",
        },
        "rater_results": deepcopy(RATERS),
        "rater_weighted_evaluation": {
            "version": "phase4_rater_weighted_v1",
            "diagnostic": "preserve",
        },
        "rater_summary": "legacy rater summary",
        "rewrite_advice": [
            "교수 관점에서 이론 정의를 반드시 추가하세요.",
            "임원 관점에서 비용과 기존 설비 영향을 반드시 검토하세요.",
            "문제에서 요구한 핵심 원리의 변수 관계를 명확히 설명하세요.",
        ],
        "improvement_points": [
            "Professional Engineer perspective: 현장 적용성을 보강하세요.",
            "명시 요구의 누락 항목을 보완하세요.",
        ],
        "next_practice_focus": [
            "기술사 관점에서 실무 판단을 제시하세요.",
            "문제 요구 해석·완전성",
        ],
        "weaknesses": [
            "Executive perspective: 운영 리스크 검토가 부족합니다.",
            "핵심 변수 설명이 부족합니다.",
        ],
    }


def run(qid: str, question: str, grade: dict | None = None) -> dict:
    return ga._phase9_apply_type_aware_de_feedback_policy(
        grade=deepcopy(grade or base_grade()),
        question_type_eval={
            "question_type": qid,
        },
        input_text=question,
    )


def public_text(grade: dict) -> str:
    rows = []

    for key in (
        "rewrite_advice",
        "improvement_points",
        "next_practice_focus",
        "weaknesses",
    ):
        rows.extend(str(x) for x in grade.get(key) or [])

    return "\n".join(rows)


class RaterPublicFeedbackBoundaryTest(unittest.TestCase):
    def test_persona_owned_public_messages_are_removed(self) -> None:
        actual = run(
            "DEFINE",
            "스마트 센서의 정의와 구성요소를 설명하시오.",
        )
        text = public_text(actual)

        for token in (
            "교수 관점",
            "임원 관점",
            "Professional Engineer perspective",
            "기술사 관점",
            "Executive perspective",
        ):
            self.assertNotIn(token, text)

        self.assertIn(
            "핵심 원리의 변수 관계를 명확히 설명하세요.",
            text,
        )
        self.assertIn(
            "문제 요구 해석·완전성",
            text,
        )

    def test_internal_rater_results_are_preserved_exactly(self) -> None:
        original = base_grade()
        expected_raters = deepcopy(original["rater_results"])
        expected_weighted = deepcopy(
            original["rater_weighted_evaluation"]
        )

        actual = run(
            "PRINCIPLE_INTERPRETATION",
            "2차 시스템의 감쇠비와 과도응답 특성을 설명하시오.",
            original,
        )

        self.assertEqual(
            actual["rater_results"],
            expected_raters,
        )
        self.assertEqual(
            actual["rater_weighted_evaluation"],
            expected_weighted,
        )
        self.assertIn(
            "비용, 시간, 적용 가능성",
            actual["rater_results"][2]["perspective"],
        )

    def test_public_rater_summary_is_neutral_boundary_text(self) -> None:
        actual = run(
            "COMPARE_SELECTION",
            "A 방식과 B 방식을 비교하고 선정 기준을 설명하시오.",
        )

        self.assertIn(
            "내부 채점·감사",
            actual["rater_summary"],
        )
        self.assertIn(
            "Question Type과 명시 Question Demand",
            actual["rater_summary"],
        )
        self.assertNotIn(
            "비용, 시간, 적용 가능성",
            actual["rater_summary"],
        )

    def test_explicit_cost_demand_does_not_make_rater_persona_owner(self) -> None:
        grade = base_grade()
        grade["rewrite_advice"].append(
            "비용 대비 성능(Cost-Benefit)을 비교하세요."
        )

        actual = run(
            "COMPARE_SELECTION",
            (
                "두 방식을 비용과 유지보수성을 포함하여 비교하고 "
                "선정 기준을 제시하시오."
            ),
            grade,
        )
        text = public_text(actual)

        self.assertIn(
            "비용 대비 성능(Cost-Benefit)을 비교하세요.",
            text,
        )
        self.assertNotIn(
            "임원 관점에서 비용과 기존 설비 영향을 반드시 검토하세요.",
            text,
        )

    def test_score_and_difficulty_axes_are_unchanged(self) -> None:
        original = base_grade()
        expected_score = original["total_score"]
        expected_difficulty = deepcopy(
            original["difficulty_strategy"]
        )

        actual = run(
            "DEFINE",
            "스마트 센서의 정의를 설명하시오.",
            original,
        )

        self.assertEqual(
            actual["total_score"],
            expected_score,
        )
        self.assertEqual(
            actual["difficulty_strategy"],
            expected_difficulty,
        )

        boundary = actual[
            "rater_public_feedback_boundary"
        ]
        self.assertTrue(
            boundary["rater_results_internal_diagnostic_only"]
        )
        self.assertTrue(
            boundary[
                "rater_weighted_evaluation_internal_diagnostic_only"
            ]
        )
        self.assertTrue(
            boundary["rater_results_preserved"]
        )
        self.assertFalse(
            boundary["score_axis_changed"]
        )
        self.assertFalse(
            boundary["difficulty_axis_changed"]
        )

    def test_all_three_rater_identities_remain_internal(self) -> None:
        actual = run(
            "PROBLEM_SOLVE",
            "문제점을 분석하고 개선방안을 설명하시오.",
        )

        ids = set(
            actual[
                "rater_public_feedback_boundary"
            ]["internal_rater_ids"]
        )

        self.assertEqual(
            ids,
            {
                "professor",
                "professional_engineer",
                "executive",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
