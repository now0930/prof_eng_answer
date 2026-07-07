#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from explicit_requirement_cap import (
    apply_explicit_requirement_hard_cap,
)
from grade_score_reconciler import _apply_numeric_flags
from question_type_coverage_score_adjuster import (
    evaluate_question_type_coverage_score_adjustment,
)


def make_grade(
    requirements: list[dict],
    *,
    score: float = 20.0,
    confidence: str = "high",
    source: str = "question_text",
) -> dict:
    return {
        "total_score": score,
        "max_score": 25.0,
        "official_pass_score": 15.0,
        "practical_target_score": 17.5,
        "high_score_target": 20.0,
        "breakdown": [
            {
                "layer_id": "A",
                "item": "A. 문제 진입·답안 구조",
                "score": 2.5,
                "max": 3.0,
            },
            {
                "layer_id": "B",
                "item": "B. 문제 요구 해석·완전성",
                "score": 5.0,
                "max": 6.0,
            },
            {
                "layer_id": "C",
                "item": "C. 유형별 Fact 기반 내용 설명",
                "score": 6.0,
                "max": 8.0,
            },
            {
                "layer_id": "D",
                "item": "D. 현장 적용·설계 판단·제언",
                "score": 5.0,
                "max": 6.0,
            },
            {
                "layer_id": "E",
                "item": "E. 연결성·면접 방어 가능성",
                "score": 1.5,
                "max": 2.0,
            },
        ],
        "question_type_coverage": {
            "coverage_source": "semantic_grader",
            "question_type": "COMPARE_SELECTION",
            "name_ko": "비교·선정형",
            "overall_coverage": "weak",
            "sub_criteria_coverage": [
                {
                    "criterion": "background_need",
                    "status": "missing",
                },
                {
                    "criterion": "field_judgement",
                    "status": "missing",
                },
            ],
            "explicit_requirement_coverage": {
                "source": source,
                "extraction_confidence": confidence,
                "requirements": requirements,
            },
        },
    }


class ExplicitRequirementPipelineTest(unittest.TestCase):
    def test_actual_pipeline_applies_hard_cap_before_weak_adjustment(
        self,
    ) -> None:
        path = ROOT / "difficulty_output_adapter.py"
        source = path.read_text(encoding="utf-8")

        function_start = source.index(
            "def attach_difficulty_strategy_to_grade("
        )
        function_source = source[function_start:]

        feedback_pos = function_source.index(
            "attach_question_type_coverage_feedback"
        )
        hard_cap_pos = function_source.index(
            "apply_explicit_requirement_hard_cap"
        )
        weak_adjustment_pos = function_source.index(
            "apply_question_type_coverage_score_adjustment"
        )

        self.assertLess(feedback_pos, hard_cap_pos)
        self.assertLess(hard_cap_pos, weak_adjustment_pos)


class ExplicitRequirementCapTest(unittest.TestCase):
    def test_subcriteria_missing_alone_does_not_cap(self) -> None:
        grade = make_grade([])

        result = apply_explicit_requirement_hard_cap(grade)
        decision = result["explicit_requirement_cap_evaluation"]

        self.assertFalse(decision["triggered"])
        self.assertEqual(result["total_score"], 20.0)

    def test_partial_does_not_trigger_hard_cap(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "특성을 비교",
                    "status": "partial",
                    "evidence": "일부 비교함",
                    "is_core": True,
                }
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)
        decision = result["explicit_requirement_cap_evaluation"]

        self.assertFalse(decision["triggered"])
        self.assertEqual(result["total_score"], 20.0)

    def test_one_missing_caps_b_and_total(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "감쇠비별 구분",
                    "status": "present",
                    "evidence": "구간을 제시함",
                    "is_core": True,
                },
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "비교축 없음",
                    "is_core": True,
                },
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)
        decision = result["explicit_requirement_cap_evaluation"]

        self.assertTrue(decision["triggered"])
        self.assertEqual(decision["b_cap"], 3.5)
        self.assertEqual(decision["total_cap"], 17.0)
        self.assertEqual(result["total_score"], 17.0)

        b_row = next(
            row
            for row in result["breakdown"]
            if row["layer_id"] == "B"
        )
        self.assertEqual(b_row["score"], 3.5)

    def test_two_missing_caps_b_and_total(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "원리 설명",
                    "status": "present",
                    "evidence": "원리 있음",
                    "is_core": True,
                },
                {
                    "requirement": "문제점 설명",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
                {
                    "requirement": "개선방안 제시",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)
        decision = result["explicit_requirement_cap_evaluation"]

        self.assertEqual(decision["b_cap"], 2.0)
        self.assertEqual(decision["total_cap"], 14.0)
        self.assertEqual(result["total_score"], 14.0)

    def test_all_missing_uses_off_demand_level_cap(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "원리 설명",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)
        decision = result["explicit_requirement_cap_evaluation"]

        self.assertEqual(decision["b_cap"], 1.5)
        self.assertEqual(decision["total_cap"], 12.5)
        self.assertEqual(result["total_score"], 12.5)

    def test_medium_confidence_does_not_cap(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                }
            ],
            confidence="medium",
        )

        result = apply_explicit_requirement_hard_cap(grade)

        self.assertFalse(
            result["explicit_requirement_cap_evaluation"]["triggered"]
        )
        self.assertEqual(result["total_score"], 20.0)

    def test_hard_cap_suppresses_weak_penalty(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
                {
                    "requirement": "분류",
                    "status": "present",
                    "evidence": "있음",
                    "is_core": True,
                },
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)
        adjustment = (
            evaluate_question_type_coverage_score_adjustment(result)
        )

        self.assertEqual(adjustment["recommended_penalty"], 0.0)
        self.assertTrue(
            adjustment["hard_cap_supersedes_weak_penalty"]
        )

    def test_reconciliation_cannot_raise_above_requirement_cap(
        self,
    ) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
                {
                    "requirement": "분류",
                    "status": "present",
                    "evidence": "있음",
                    "is_core": True,
                },
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)
        self.assertEqual(result["total_score"], 17.0)

        # Simulate a later LLM cap reconciliation attempting to raise it.
        result["total_score"] = 19.0
        result["final_total_score"] = 19.0

        result = _apply_numeric_flags(result)

        self.assertEqual(result["total_score"], 17.0)
        self.assertTrue(
            result["explicit_requirement_cap_evaluation"][
                "reapplied_after_reconciliation"
            ]
        )


    def test_untrusted_coverage_source_does_not_cap(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "없음",
                    "is_core": True,
                },
                {
                    "requirement": "분류",
                    "status": "present",
                    "evidence": "있음",
                    "is_core": True,
                },
            ]
        )

        grade["question_type_coverage"][
            "coverage_source"
        ] = "manual"

        result = apply_explicit_requirement_hard_cap(grade)
        decision = result["explicit_requirement_cap_evaluation"]

        self.assertFalse(decision["triggered"])
        self.assertEqual(result["total_score"], 20.0)
        self.assertIn(
            "semantic_grader",
            decision["reason"],
        )

    def test_score_range_does_not_exceed_hard_cap(self) -> None:
        grade = make_grade(
            [
                {
                    "requirement": "감쇠비별 구분",
                    "status": "present",
                    "evidence": "구간을 제시함",
                    "is_core": True,
                },
                {
                    "requirement": "특성 비교",
                    "status": "missing",
                    "evidence": "비교축 없음",
                    "is_core": True,
                },
            ]
        )

        result = apply_explicit_requirement_hard_cap(grade)

        self.assertEqual(result["total_score"], 17.0)
        self.assertEqual(
            result["score_range"],
            "17점 cap 적용",
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
