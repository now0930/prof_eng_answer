from __future__ import annotations

import copy
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
FIXTURE = (
    REPO
    / "scripts"
    / "fixtures"
    / "plan_a_control_valve_coverage_case.json"
)
sys.path.insert(0, str(REPO))

from explicit_requirement_cap import (
    evaluate_explicit_requirement_hard_cap,
)
from question_type_coverage_adapter import (
    attach_question_type_coverage_feedback,
    ensure_grade_question_type_coverage,
)
from question_type_coverage_score_adjuster import (
    apply_question_type_coverage_score_adjustment,
)
from semantic_question_type_prompt import (
    build_question_type_semantic_guidance,
)


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def make_grade(
    *,
    question: str | None = None,
    calculation_status: str = "missing",
    formula_status: str = "partial",
    result_status: str = "partial",
    field_status: str = "partial",
) -> dict:
    case = load_fixture()
    coverage = copy.deepcopy(case["question_type_coverage"])

    status_overrides = {
        "calculation_or_interpretation": calculation_status,
        "formula_model_variables": formula_status,
        "result_meaning": result_status,
        "field_judgement": field_status,
    }

    for row in coverage["sub_criteria_coverage"]:
        criterion = row.get("criterion")
        if criterion in status_overrides:
            row["status"] = status_overrides[criterion]

    envelope = copy.deepcopy(
        case.get("verified_semantic_envelope") or {}
    )
    coverage.update(
        envelope.get("coverage_metadata") or {}
    )

    parsed = {
        "question_type": case["question_type"],
        "question_type_coverage": copy.deepcopy(coverage),
    }
    parsed.update(
        envelope.get("semantic_parsed_metadata") or {}
    )

    semantic_evaluation = {"parsed": parsed}
    semantic_evaluation.update(
        envelope.get("semantic_evaluation_metadata") or {}
    )

    grade = {
        "total_score": 9.49,
        "question_text": question or case["question"],
        "question_type": case["question_type"],
        "question_type_coverage": copy.deepcopy(coverage),
        "gemini_semantic_evaluation": semantic_evaluation,
    }
    grade.update(envelope.get("grade_metadata") or {})
    return grade


def criterion_status(coverage: dict, criterion: str) -> str | None:
    for row in coverage.get("sub_criteria_coverage") or []:
        if isinstance(row, dict) and row.get("criterion") == criterion:
            return row.get("status")
    return None


class PlanARequirementCoverageRegressionTest(unittest.TestCase):
    def test_design_criteria_repairs_missing_calculation_to_partial(self) -> None:
        grade = make_grade()
        result = ensure_grade_question_type_coverage(
            grade,
            question_text=grade["question_text"],
        )

        root_status = criterion_status(
            result["question_type_coverage"],
            "calculation_or_interpretation",
        )
        nested_status = criterion_status(
            result["gemini_semantic_evaluation"]["parsed"][
                "question_type_coverage"
            ],
            "calculation_or_interpretation",
        )

        self.assertEqual("partial", root_status)
        self.assertEqual("partial", nested_status)

    def test_prompt_distinguishes_design_criteria_from_numeric_calculation(self) -> None:
        guidance = build_question_type_semantic_guidance(
            load_fixture()["question"],
            "PRINCIPLE_INTERPRETATION",
        )

        self.assertIn("설계 기준을 제시", guidance)
        self.assertIn("수치 계산 요구로 자동 변환하지", guidance)
        self.assertIn("계산하시오", guidance)
        self.assertIn("산정하시오", guidance)
        self.assertIn("구하시오", guidance)

    def test_prompt_separates_b_completeness_from_c_fact_accuracy(self) -> None:
        guidance = build_question_type_semantic_guidance(
            load_fixture()["question"],
            "PRINCIPLE_INTERPRETATION",
        )

        self.assertIn("B항목", guidance)
        self.assertIn("명시적 요구사항의 언급·충족", guidance)
        self.assertIn("C항목", guidance)
        self.assertIn("기술적 정확성·Fact 깊이", guidance)
        self.assertIn("같은 기술적 약점을 B와 C에서 중복 감점하지", guidance)

    def test_attach_accepts_question_text_without_forwarding_unknown_kwarg(
        self,
    ) -> None:
        grade = make_grade()
        result = attach_question_type_coverage_feedback(
            grade,
            question_text=grade["question_text"],
        )

        self.assertEqual(
            "partial",
            criterion_status(
                result["question_type_coverage"],
                "calculation_or_interpretation",
            ),
        )
        self.assertEqual(
            "partial",
            criterion_status(
                result["gemini_semantic_evaluation"]["parsed"][
                    "question_type_coverage"
                ],
                "calculation_or_interpretation",
            ),
        )

    def test_explicit_numeric_calculation_can_remain_missing(self) -> None:
        grade = make_grade(
            question=(
                "최대 차압과 유효 면적을 이용해 필요한 Spring 힘을 "
                "계산하시오."
            )
        )
        result = ensure_grade_question_type_coverage(
            grade,
            question_text=grade["question_text"],
        )

        self.assertEqual(
            "missing",
            criterion_status(
                result["question_type_coverage"],
                "calculation_or_interpretation",
            ),
        )

    def test_absent_formula_and_interpretation_can_remain_missing(self) -> None:
        grade = make_grade(
            formula_status="missing",
            result_status="missing",
            field_status="missing",
        )
        result = ensure_grade_question_type_coverage(
            grade,
            question_text=grade["question_text"],
        )

        self.assertEqual(
            "missing",
            criterion_status(
                result["question_type_coverage"],
                "calculation_or_interpretation",
            ),
        )

    def test_incorrect_status_is_not_repaired(self) -> None:
        grade = make_grade(calculation_status="incorrect")
        result = ensure_grade_question_type_coverage(
            grade,
            question_text=grade["question_text"],
        )

        self.assertEqual(
            "incorrect",
            criterion_status(
                result["question_type_coverage"],
                "calculation_or_interpretation",
            ),
        )

    def test_warn_adjustment_does_not_change_total_score(self) -> None:
        grade = make_grade(calculation_status="partial")

        with patch.dict(
            os.environ,
            {"QUESTION_TYPE_COVERAGE_SCORE_MODE": "warn"},
            clear=False,
        ):
            result = apply_question_type_coverage_score_adjustment(grade)

        decision = result["question_type_coverage_score_adjustment"]
        self.assertFalse(decision["applied"])
        self.assertEqual(9.49, result["total_score"])
        self.assertEqual(0, decision["coverage_counts"]["missing"])
        self.assertEqual(5, decision["coverage_counts"]["partial"])
        self.assertGreater(decision["recommended_penalty"], 0.0)
        self.assertLessEqual(
            decision["recommended_penalty"],
            decision["max_total_penalty"],
        )
        self.assertAlmostEqual(
            decision["recommended_penalty"],
            sum(decision["suggested_layer_penalties"].values()),
            places=2,
        )

    def test_explicit_core_requirements_present_do_not_trigger_b_cap(self) -> None:
        grade = make_grade()
        decision = evaluate_explicit_requirement_hard_cap(grade)

        self.assertTrue(decision["eligible"])
        self.assertFalse(decision["triggered"])
        self.assertIsNone(decision["b_cap"])
        self.assertEqual(3, decision["present_core_count"])
        self.assertEqual(0, decision["missing_core_count"])


if __name__ == "__main__":
    unittest.main()
