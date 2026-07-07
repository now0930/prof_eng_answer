#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

from grade_score_reconciler import _apply_numeric_flags
from grading_agents import (
    _phase8_normalize_originality_evaluation,
)


class OriginalityConsistencyRegressionTest(unittest.TestCase):
    def test_inflated_raw_score_is_limited_by_anchor_evidence(self):
        parsed = {
            "average_level": 0.34,
            "raw_originality_score": 3.4,
            "anchors": [
                {"id": "O1", "level": 0.3},
                {"id": "O2", "level": 0.3},
                {"id": "O3", "level": 0.5},
                {"id": "O4", "level": 0.3},
                {"id": "O5", "level": 0.3},
            ],
        }

        result = _phase8_normalize_originality_evaluation(parsed)

        self.assertEqual(
            result["reported_raw_originality_score"],
            3.4,
        )
        self.assertEqual(
            result["bounded_reported_raw_originality_score"],
            2.0,
        )
        self.assertEqual(
            result["anchor_derived_originality_score"],
            0.68,
        )
        self.assertEqual(result["raw_originality_score"], 0.68)
        self.assertEqual(
            result["originality_score_source"],
            "anchor_upper_bound",
        )
        self.assertTrue(
            result["originality_score_consistency_adjustment"][
                "applied"
            ]
        )

    def test_normalization_is_idempotent(self):
        parsed = {
            "average_level": 0.34,
            "raw_originality_score": 3.4,
            "anchors": [
                {"id": "O1", "level": 0.3},
                {"id": "O2", "level": 0.3},
                {"id": "O3", "level": 0.5},
                {"id": "O4", "level": 0.3},
                {"id": "O5", "level": 0.3},
            ],
        }

        first = _phase8_normalize_originality_evaluation(parsed)
        second = _phase8_normalize_originality_evaluation(first)

        self.assertEqual(
            second["reported_raw_originality_score"],
            3.4,
        )
        self.assertEqual(
            second["bounded_reported_raw_originality_score"],
            2.0,
        )
        self.assertEqual(second["raw_originality_score"], 0.68)
        self.assertEqual(
            second["originality_score_source"],
            "anchor_upper_bound",
        )

    def test_average_level_caps_raw_score_without_anchors(self):
        parsed = {
            "average_level": 0.25,
            "raw_originality_score": 1.8,
            "anchors": [],
        }

        result = _phase8_normalize_originality_evaluation(parsed)

        self.assertEqual(
            result["anchor_derived_originality_score"],
            0.5,
        )
        self.assertEqual(result["raw_originality_score"], 0.5)
        self.assertEqual(
            result["originality_score_source"],
            "average_level_upper_bound",
        )
        self.assertTrue(
            result["originality_score_consistency_adjustment"][
                "applied"
            ]
        )

    def test_raw_score_without_structured_evidence_gives_no_bonus(self):
        parsed = {
            "raw_originality_score": 1.8,
            "anchors": [],
        }

        result = _phase8_normalize_originality_evaluation(parsed)

        self.assertEqual(result["average_level"], 0.0)
        self.assertEqual(
            result["anchor_derived_originality_score"],
            0.0,
        )
        self.assertEqual(result["raw_originality_score"], 0.0)
        self.assertEqual(
            result["originality_score_source"],
            "no_structured_evidence",
        )
        self.assertTrue(
            result["originality_score_consistency_adjustment"][
                "applied"
            ]
        )

    def test_conservative_reported_score_is_not_raised(self):
        parsed = {
            "average_level": 0.24,
            "raw_originality_score": 0.2,
            "anchors": [
                {"id": "O1", "level": 0.3},
                {"id": "O2", "level": 0.3},
                {"id": "O3", "level": 0.3},
                {"id": "O4", "level": 0.3},
                {"id": "O5", "level": 0.0},
            ],
        }

        result = _phase8_normalize_originality_evaluation(parsed)

        self.assertEqual(
            result["anchor_derived_originality_score"],
            0.48,
        )
        self.assertEqual(result["raw_originality_score"], 0.2)
        self.assertEqual(
            result["originality_score_source"],
            "reported_raw",
        )
        self.assertFalse(
            result["originality_score_consistency_adjustment"][
                "applied"
            ]
        )


class FinalScoreMetadataRegressionTest(unittest.TestCase):
    def base_grade(self):
        return {
            "total_score": 12.39,
            "max_score": 25.0,
            "score_range": "12~12",
            "official_pass_score": 15.0,
            "practical_target_score": 17.5,
            "high_score_target": 20.0,
        }

    def test_ordinary_score_is_fully_synchronized(self):
        result = _apply_numeric_flags(self.base_grade())

        self.assertEqual(result["total_score"], 12.39)
        self.assertEqual(result["final_total_score"], 12.39)
        self.assertEqual(result["score_range"], "11.9~12.9")

    def test_triggered_but_not_applied_cap_uses_normal_range(self):
        grade = self.base_grade()
        grade["total_score"] = 9.84
        grade["explicit_requirement_cap_evaluation"] = {
            "triggered": True,
            "applied": False,
            "total_cap": 17.0,
            "adjusted_score": 9.84,
        }

        result = _apply_numeric_flags(grade)

        self.assertEqual(result["final_total_score"], 9.84)
        self.assertEqual(result["score_range"], "9.3~10.3")
        self.assertNotIn("cap 적용", result["score_range"])

    def test_binding_explicit_requirement_cap_is_displayed(self):
        grade = self.base_grade()
        grade["total_score"] = 17.0
        grade["explicit_requirement_cap_evaluation"] = {
            "triggered": True,
            "applied": True,
            "total_cap": 17.0,
            "adjusted_score": 17.0,
        }

        result = _apply_numeric_flags(grade)

        self.assertEqual(result["final_total_score"], 17.0)
        self.assertEqual(result["score_range"], "17점 cap 적용")

    def test_non_binding_applied_cap_only_limits_range_upper_bound(self):
        grade = self.base_grade()
        grade["total_score"] = 16.8
        grade["explicit_requirement_cap_evaluation"] = {
            "triggered": True,
            "applied": True,
            "total_cap": 17.0,
            "adjusted_score": 16.8,
        }

        result = _apply_numeric_flags(grade)

        self.assertEqual(result["score_range"], "16.3~17.0")
        self.assertNotIn("cap 적용", result["score_range"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
