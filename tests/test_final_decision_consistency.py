from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from grade_output_summarizer import _build_payload
from verdict_consistency import (
    enforce_final_decision_consistency,
)


def fatal_grade() -> dict:
    return {
        "total_score": 16.0,
        "max_score": 25.0,
        "official_pass_score": 15.0,
        "practical_target_score": 17.5,
        "high_score_target": 20.0,
        "confidence": "high",
        "summary": (
            "핵심 개념 설명은 정확하고 "
            "우수합니다."
        ),
        "strengths": [
            "기술적 개념의 정확성이 "
            "우수합니다.",
            "표의 구조가 명확합니다.",
        ],
        "question_type_coverage": {
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {
                "requirements": [
                    {
                        "requirement_id": "R1",
                        "status": "incorrect",
                    }
                ]
            },
        },
        "logic_check_evaluation": {
            "fatal_error_detected": True,
            "findings": [
                {
                    "severity": "fatal",
                    "message": "핵심 범주 오류",
                }
            ],
        },
        "general_evidence_contract": {
            "defects": [],
        },
    }


class FinalDecisionConsistencyTest(
    unittest.TestCase
):
    def test_fatal_blocks_pass_and_strong(
        self,
    ) -> None:
        result = (
            enforce_final_decision_consistency(
                fatal_grade()
            )
        )

        self.assertFalse(
            result["passing_score_allowed"]
        )
        self.assertFalse(
            result["strong_verdict_allowed"]
        )
        self.assertFalse(
            result[
                "requirements_full_credit_allowed"
            ]
        )
        self.assertEqual(
            result["confidence_ceiling"],
            "medium",
        )
        self.assertEqual(
            result["confidence"],
            "medium",
        )
        self.assertEqual(
            result["question_type_coverage"][
                "overall_coverage"
            ],
            "needs_correction",
        )
        self.assertNotIn(
            "정확하고 우수",
            result["summary"],
        )

        payload = _build_payload(result)
        self.assertFalse(
            payload["score"]["official_pass_met"]
        )
        self.assertFalse(
            payload["score"][
                "practical_target_met"
            ]
        )
        self.assertFalse(
            payload["score"]["high_score_met"]
        )

    def test_major_nonfatal_blocks_strong_only(
        self,
    ) -> None:
        grade = {
            "total_score": 15.5,
            "summary": (
                "핵심 기술관계가 모두 "
                "정확합니다."
            ),
            "general_evidence_contract": {
                "defects": [
                    {
                        "defect_type": (
                            "correctness_error"
                        ),
                        "severity": "major",
                        "explanation": (
                            "주요 정의 오류"
                        ),
                    }
                ]
            },
        }

        result = (
            enforce_final_decision_consistency(
                grade
            )
        )

        self.assertFalse(
            result["strong_verdict_allowed"]
        )
        self.assertNotIn(
            "passing_score_allowed",
            result,
        )
        self.assertNotIn(
            "모두 정확",
            result["summary"],
        )

    def test_nonfatal_is_unchanged(
        self,
    ) -> None:
        grade = {
            "total_score": 13.0,
            "summary": "구조가 명확합니다.",
            "general_evidence_contract": {
                "defects": [
                    {
                        "defect_type": (
                            "core_depth_gap"
                        ),
                        "severity": "minor",
                    }
                ]
            },
        }
        before = copy.deepcopy(grade)
        after = (
            enforce_final_decision_consistency(
                grade
            )
        )
        self.assertEqual(after, before)


# STAGE18B2_CANONICAL_QTYPE_AND_SCORE_SOURCE_V2
class CanonicalQuestionTypeAndScoreSourceV2Test(
    unittest.TestCase
):
    def test_final_attach_reuses_canonical_question_type(
        self,
    ) -> None:
        from question_demand_contract import (
            attach_question_demand_contract,
        )

        result = {
            "question_type_evaluation": {
                "primary_type": {
                    "id": (
                        "PRINCIPLE_INTERPRETATION"
                    ),
                },
            },
        }

        updated = attach_question_demand_contract(
            result,
            "두 방식을 비교하고 선정 기준을 설명하시오.",
            canonical_primary_lens=result,
        )
        contract = updated[
            "question_demand_contract"
        ]

        self.assertEqual(
            contract[
                "detected_primary_lens"
            ],
            "COMPARE_SELECTION",
        )
        self.assertEqual(
            contract["primary_lens"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertEqual(
            contract[
                "primary_lens_source"
            ],
            "canonical_question_type_router",
        )
        self.assertTrue(
            contract[
                "canonical_primary_lens_applied"
            ]
        )
        self.assertEqual(
            contract[
                "final_primary_lens_owner"
            ],
            "canonical_question_type_router",
        )

    def test_pregrade_contract_remains_question_only_fallback(
        self,
    ) -> None:
        from question_demand_contract import (
            build_question_demand_contract,
        )

        contract = build_question_demand_contract(
            "원리와 동작 특성을 설명하시오."
        )

        self.assertEqual(
            contract[
                "primary_lens_source"
            ],
            "question_text_pregrade_fallback",
        )
        self.assertFalse(
            contract[
                "canonical_primary_lens_applied"
            ]
        )
        self.assertEqual(
            contract[
                "answer_text_dependency"
            ],
            "none",
        )
        self.assertTrue(
            all(
                item["source"]
                == "question_text_only"
                and item[
                    "answer_text_dependency"
                ]
                == "none"
                for item in contract[
                    "requirements"
                ]
            )
        )

    def test_complete_abcde_breakdown_is_authoritative(
        self,
    ) -> None:
        from grade_score_reconciler import (
            authoritative_abcde_breakdown_score,
            best_uncapped_numeric_score,
        )

        grade = {
            "max_score": 25.0,
            "weighted_total_score": 22.0,
            "committee_total_score": 21.0,
            "breakdown": [
                {
                    "layer_id": "A",
                    "score": 2.0,
                },
                {
                    "layer_id": "B",
                    "score": 3.0,
                },
                {
                    "layer_id": "C",
                    "score": 4.0,
                },
                {
                    "layer_id": "D",
                    "score": 4.0,
                },
                {
                    "layer_id": "E",
                    "score": 1.0,
                },
            ],
        }

        self.assertEqual(
            authoritative_abcde_breakdown_score(
                grade
            ),
            14.0,
        )
        self.assertEqual(
            best_uncapped_numeric_score(
                grade
            ),
            14.0,
        )

    def test_incomplete_breakdown_uses_legacy_fallback(
        self,
    ) -> None:
        from grade_score_reconciler import (
            authoritative_abcde_breakdown_score,
            best_uncapped_numeric_score,
        )

        grade = {
            "max_score": 25.0,
            "weighted_total_score": 18.0,
            "breakdown": [
                {
                    "layer_id": "A",
                    "score": 2.0,
                },
                {
                    "layer_id": "B",
                    "score": 3.0,
                },
            ],
        }

        self.assertIsNone(
            authoritative_abcde_breakdown_score(
                grade
            )
        )
        self.assertEqual(
            best_uncapped_numeric_score(
                grade
            ),
            18.0,
        )


if __name__ == "__main__":
    unittest.main()
