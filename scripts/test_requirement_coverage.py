#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bot
from question_type_coverage_adapter import (
    attach_question_type_coverage_feedback,
)


class RequirementCoverageRegressionTest(unittest.TestCase):
    def test_layer_points_are_3_6_8_6_2(self) -> None:
        path = ROOT / "rubrics/scoring_model/default.json"
        data = json.loads(path.read_text(encoding="utf-8"))

        points = {
            row["id"]: row["points"]
            for row in data["layers"]
        }

        self.assertEqual(
            points,
            {
                "A": 3,
                "B": 6,
                "C": 8,
                "D": 6,
                "E": 2,
            },
        )
        self.assertEqual(sum(points.values()), 25)

        names = {
            row["id"]: row["name"]
            for row in data["layers"]
        }

        self.assertEqual(
            names["A"],
            "문제 진입·답안 구조",
        )
        self.assertEqual(
            names["B"],
            "문제 요구 해석·완전성",
        )

    def test_weighted_requirement_coverage(self) -> None:
        grade = {
            "total_score": 15.0,
            "question_type_coverage": {
                "coverage_source": "semantic_grader",
                "question_type": "COMPARE_SELECTION",
                "name_ko": "비교·선정형",
                "overall_coverage": "weak",
                "sub_criteria_coverage": [
                    {
                        "criterion": "비교 대상",
                        "status": "present",
                        "evidence": "두 방식을 제시함",
                    },
                    {
                        "criterion": "비교축",
                        "status": "present",
                        "evidence": "정확도와 비용을 비교함",
                    },
                    {
                        "criterion": "적용 조건",
                        "status": "partial",
                        "evidence": "조건을 일부만 언급함",
                    },
                    {
                        "criterion": "선정 기준",
                        "status": "missing",
                        "evidence": "최종 선정 판단 없음",
                    },
                ],
                "missing_sub_criteria": ["선정 기준"],
                "c_fact_focus_coverage": {
                    "covered": ["비교 대상"],
                    "missing": ["trade-off"],
                },
                "d_field_judgement_focus_coverage": {
                    "covered": [],
                    "missing": ["현장 선정 기준"],
                },
                "scoring_hint": (
                    "B 요구사항 완전성과 C/D를 보수적으로 평가"
                ),
            },
        }

        result = attach_question_type_coverage_feedback(grade)
        summary = result["question_type_coverage_summary"]

        self.assertEqual(summary["sub_criteria_total"], 4)
        self.assertEqual(summary["sub_criteria_present"], 2)
        self.assertEqual(summary["sub_criteria_partial"], 1)
        self.assertEqual(summary["sub_criteria_missing"], 1)
        self.assertEqual(summary["weighted_coverage_score"], 2.5)
        self.assertEqual(summary["weighted_coverage_percent"], 62.5)
        self.assertEqual(
            summary["partial_criteria"],
            ["적용 조건"],
        )
        self.assertEqual(
            summary["missing_criteria"],
            ["선정 기준"],
        )

        text = bot._format_question_type_coverage_display(result)

        self.assertIn("[요구사항 충족도]", text)
        self.assertIn("요구사항 충족률: 62.5%", text)
        self.assertIn("가중 2.5/4", text)
        self.assertIn("충족 2 · 부분 1 · 오답 0 · 누락 1", text)
        self.assertIn("부분 충족: 적용 조건", text)
        self.assertIn("누락: 선정 기준", text)

class IncorrectRequirementCoverageRegressionTests(
    unittest.TestCase
):
    def test_incorrect_coverage_is_separate_from_missing(
        self,
    ) -> None:
        import bot
        from question_type_coverage_adapter import (
            attach_question_type_coverage_feedback,
        )

        grade = {
            "total_score": 1.02,
            "question_type": (
                "PRINCIPLE_INTERPRETATION"
            ),
            "question_type_v2": {
                "question_type": (
                    "PRINCIPLE_INTERPRETATION"
                ),
                "name_ko": "원리·해석형",
            },
            "question_type_coverage": {
                "coverage_source": "semantic_grader",
                "question_type": (
                    "PRINCIPLE_INTERPRETATION"
                ),
                "name_ko": "원리·해석형",
                "overall_coverage": "poor",
                "sub_criteria_coverage": [
                    {
                        "criterion": "배경",
                        "status": "present",
                        "evidence": "배경을 제시함",
                    },
                    {
                        "criterion": "구성",
                        "status": "partial",
                        "evidence": "일부만 설명함",
                    },
                    {
                        "criterion": "감쇠비 원리",
                        "status": "incorrect",
                        "evidence": (
                            "요구를 직접 설명했으나 "
                            "안정성 부호가 반대임"
                        ),
                    },
                    {
                        "criterion": "표준 수식",
                        "status": "missing",
                        "evidence": "수식 없음",
                    },
                ],
            },
            "explicit_requirement_cap_evaluation": {
                "eligible": True,
                "triggered": False,
                "incorrect_requirements": [
                    "감쇠비별 과도응답 특성 설명"
                ],
                "missing_requirements": [],
            },
        }

        result = (
            attach_question_type_coverage_feedback(
                grade
            )
        )

        summary = result[
            "question_type_coverage_summary"
        ]

        self.assertEqual(
            summary["sub_criteria_total"],
            4,
        )
        self.assertEqual(
            summary["sub_criteria_present"],
            1,
        )
        self.assertEqual(
            summary["sub_criteria_partial"],
            1,
        )
        self.assertEqual(
            summary["sub_criteria_incorrect"],
            1,
        )
        self.assertEqual(
            summary["sub_criteria_missing"],
            1,
        )
        self.assertEqual(
            summary["weighted_coverage_score"],
            1.5,
        )
        self.assertEqual(
            summary["weighted_coverage_percent"],
            37.5,
        )
        self.assertEqual(
            summary["incorrect_criteria"],
            ["감쇠비 원리"],
        )
        self.assertEqual(
            summary["missing_criteria"],
            ["표준 수식"],
        )

        text = (
            bot._format_question_type_coverage_display(
                result
            )
        )

        self.assertIn(
            (
                "충족 1 · 부분 1 · "
                "오답 1 · 누락 1"
            ),
            text,
        )
        self.assertIn(
            "오답 응답: 감쇠비 원리",
            text,
        )
        self.assertIn(
            "누락: 표준 수식",
            text,
        )
        self.assertIn(
            (
                "명시적 핵심 요구 오답 응답: "
                "감쇠비별 과도응답 특성 설명"
            ),
            text,
        )
        self.assertNotIn(
            "명시적 핵심 요구 누락",
            text,
        )

    def test_final_question_type_name_matches_v2(
        self,
    ) -> None:
        from question_type_output_adapter import (
            attach_question_type_v2_to_grade,
        )

        grade = {
            "question_type": "GENERAL",
            "question_type_name": "일반 설명형",
        }

        result = attach_question_type_v2_to_grade(
            grade,
            existing_question_type=(
                "PRINCIPLE_INTERPRETATION"
            ),
        )

        self.assertEqual(
            result["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertEqual(
            result["question_type_name"],
            "원리·해석형",
        )
        self.assertEqual(
            result["question_type_v2"]["name_ko"],
            "원리·해석형",
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
