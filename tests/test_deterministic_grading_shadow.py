from __future__ import annotations

import unittest
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_grading_shadow import (
    attach_deterministic_grading_shadow,
    build_deterministic_grading_shadow,
)

TOPIC = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
QUESTION = "SIL 결정 방법을 설명하시오."


def _grade():
    return {"total_score": 20.0, "verdict": "strong", "topic_id": TOPIC}


class DeterministicGradingShadowTests(unittest.TestCase):
    def test_operational_dimension_error_becomes_bound_fatal_shadow(self):
        result = build_deterministic_grading_shadow(
            grade=_grade(), question_text=QUESTION,
            answer_text="lambda_SIS 비율이 PFD 비율보다 작도록 시스템을 설계한다.",
        )
        self.assertTrue(result["fatal_or_core_error"])
        self.assertEqual(
            result["findings"][0]["finding_id"],
            "failure_rate_compared_directly_to_pfd",
        )
        self.assertEqual(result["provider_calls"], 0)
        statuses = {
            row["requirement_id"]: row["status"] for row in result["requirements"]
        }
        self.assertEqual(statuses["quantitative_verification_dimension"], "WRONG")

    def test_corrected_statement_has_no_dimension_finding(self):
        result = build_deterministic_grading_shadow(
            grade=_grade(), question_text=QUESTION,
            answer_text="고장률은 시간당 고장률이고 PFDavg는 무차원이다.",
        )
        self.assertEqual(result["findings"], [])
        self.assertFalse(result["fatal_or_core_error"])

    def test_shadow_is_exactly_repeatable(self):
        kwargs = dict(
            grade=_grade(), question_text=QUESTION, answer_text="lambda < PFDavg"
        )
        self.assertEqual(
            build_deterministic_grading_shadow(**kwargs),
            build_deterministic_grading_shadow(**kwargs),
        )

    def test_attachment_does_not_change_score_or_verdict(self):
        original = _grade()
        attached = attach_deterministic_grading_shadow(
            original, question_text=QUESTION, answer_text="lambda < PFDavg",
            is_grade_dict=lambda row: isinstance(row, dict) and "total_score" in row,
        )
        self.assertEqual(original, _grade())
        self.assertEqual(attached["total_score"], original["total_score"])
        self.assertEqual(attached["verdict"], original["verdict"])
        self.assertEqual(attached["deterministic_grading_shadow"]["score_effect"], "none")

    def test_unrelated_topic_keeps_generic_invariant_without_fatal_binding(self):
        result = build_deterministic_grading_shadow(
            grade={"total_score": 10, "topic_id": "unrelated"},
            question_text="비교를 설명하시오.", answer_text="lambda < PFD",
        )
        self.assertEqual(result["findings"][0]["classification"], "technical_error")
        self.assertFalse(result["fatal_or_core_error"])


if __name__ == "__main__":
    unittest.main()
