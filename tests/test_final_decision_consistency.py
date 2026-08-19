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


if __name__ == "__main__":
    unittest.main()
