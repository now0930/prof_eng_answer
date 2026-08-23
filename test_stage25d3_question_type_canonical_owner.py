from __future__ import annotations

import copy
import unittest

from question_type_coverage_adapter import (
    _apply_incorrect_requirement_status_contract_v3,
    _promote_question_type_coverage_to_root_v1,
    attach_question_type_coverage_feedback,
)
from question_type_output_adapter import (
    attach_question_type_v2_to_grade,
)
from question_type_taxonomy import (
    detect_question_type_from_text,
)


QUESTION = (
    "제어 소프트웨어의 V-model 개발 절차를 설명하고 "
    "단위 시험, 통합 시험, 시스템 시험 및 SIL 검증 방안을 "
    "설명하시오."
)
EXPECTED = "IMPLEMENTATION_EVALUATION"
STALE = "COMPARE_SELECTION"


class QuestionTypeCanonicalOwnerTest(unittest.TestCase):
    def test_fixture_routes_to_implementation_evaluation(self):
        self.assertEqual(
            detect_question_type_from_text(QUESTION),
            EXPECTED,
        )

    def test_question_text_overrides_root_semantic_type(self):
        result = attach_question_type_v2_to_grade(
            {"question_type": STALE},
            question_text=QUESTION,
        )
        self.assertEqual(
            result["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            result["question_type_v2"]["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            result["question_type_v2"]["legacy_question_type"],
            STALE,
        )

    def test_question_text_overrides_nested_semantic_type(self):
        result = attach_question_type_v2_to_grade(
            {
                "semantic_evaluation": {
                    "question_type": STALE,
                },
            },
            question_text=QUESTION,
        )
        self.assertEqual(
            result["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            result["question_type_v2"]["question_type"],
            EXPECTED,
        )

    def test_existing_type_is_fallback_without_question_text(self):
        result = attach_question_type_v2_to_grade(
            {"question_type": STALE},
            question_text=None,
        )
        self.assertEqual(
            result["question_type"],
            STALE,
        )

    def test_locked_promotion_serialization_is_unchanged(self):
        grade = {
            "question_type": "EXISTING_ROOT_TYPE",
            "question_type_coverage": {
                "question_type": "NESTED_TYPE",
                "name_ko": "중첩 이름",
            },
        }
        result = (
            _promote_question_type_coverage_to_root_v1(
                grade
            )
        )
        self.assertEqual(
            set(result["question_type_v2"]),
            {
                "question_type",
                "name_ko",
                "sub_criteria",
                "c_fact_focus",
                "d_field_judgement_focus",
                "note",
            },
        )
        self.assertEqual(
            result["question_type_v2"]["name_ko"],
            "중첩 이름",
        )

    def test_mismatched_semantic_coverage_is_invalidated(self):
        grade = attach_question_type_v2_to_grade(
            {
                "question_type_coverage": {
                    "question_type": STALE,
                    "name_ko": "비교·선정형",
                    "coverage_source": "semantic_grader",
                    "overall_coverage": "strong",
                    "sub_criteria_coverage": [
                        {
                            "criterion": "comparison_axis",
                            "status": "present",
                            "evidence": "비교축",
                        }
                    ],
                    "missing_sub_criteria": [],
                    "c_fact_focus_coverage": {
                        "covered": ["comparison_axis"],
                        "missing": [],
                    },
                    "d_field_judgement_focus_coverage": {
                        "covered": ["selection_judgement"],
                        "missing": [],
                    },
                    "explicit_requirement_coverage": {
                        "requirements": [
                            {
                                "requirement_id": "R1",
                                "status": "present",
                            }
                        ]
                    },
                }
            },
            question_text=QUESTION,
        )

        result = attach_question_type_coverage_feedback(
            grade,
            question_text=QUESTION,
        )
        coverage = result["question_type_coverage"]
        summary = result[
            "question_type_coverage_summary"
        ]

        self.assertEqual(
            result["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            result["question_type_v2"]["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            coverage["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            coverage["overall_coverage"],
            "unknown",
        )
        self.assertEqual(
            coverage["sub_criteria_coverage"],
            [],
        )
        self.assertEqual(
            coverage["coverage_source"],
            "question_only_type_owner_mismatch_guard",
        )
        self.assertTrue(
            coverage[
                "question_type_owner_reconciliation"
            ][
                "type_specific_coverage_invalidated"
            ]
        )
        self.assertEqual(
            coverage[
                "explicit_requirement_coverage"
            ]["requirements"][0]["requirement_id"],
            "R1",
        )
        self.assertEqual(
            summary["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            summary["overall_coverage"],
            "unknown",
        )
        self.assertFalse(
            summary["full_correct_coverage"],
        )

    def test_matching_coverage_is_preserved(self):
        grade = attach_question_type_v2_to_grade(
            {
                "question_type_coverage": {
                    "question_type": EXPECTED,
                    "name_ko": "적용·평가형",
                    "coverage_source": "semantic_grader",
                    "overall_coverage": "adequate",
                    "sub_criteria_coverage": [
                        {
                            "criterion": "procedure_method",
                            "status": "partial",
                            "evidence": "절차 일부",
                        }
                    ],
                }
            },
            question_text=QUESTION,
        )
        result = attach_question_type_coverage_feedback(
            grade,
            question_text=QUESTION,
        )
        coverage = result["question_type_coverage"]
        self.assertEqual(
            coverage["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            len(coverage["sub_criteria_coverage"]),
            1,
        )
        self.assertEqual(
            coverage["overall_coverage"],
            "adequate",
        )

    def test_final_status_contract_cannot_repromote_stale_qtype_v2(self):
        grade = {
            "question_type": EXPECTED,
            "question_type_name": "적용·평가형",
            "question_type_v2": {
                "question_type": STALE,
                "name_ko": "비교·선정형",
                "note": "sentinel",
            },
        }
        result = (
            _apply_incorrect_requirement_status_contract_v3(
                copy.deepcopy(grade)
            )
        )
        self.assertEqual(
            result["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            result["question_type_v2"]["question_type"],
            EXPECTED,
        )
        self.assertEqual(
            result["question_type_name"],
            "적용·평가형",
        )
        self.assertEqual(
            result["question_type_v2"]["note"],
            "sentinel",
        )


if __name__ == "__main__":
    unittest.main()
