#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading_agents import (
    _phase2_apply_caps,
    _phase4_apply_rater_weighted_scoring,
)


class QuestionTypeDEFactCapTerminalityTest(unittest.TestCase):
    def _layers(self, c_score, d_score=6.0, e_score=2.0):
        return [
            {"layer_id": "A", "item": "A", "score": 1.0, "max": 3.0, "reason": "A"},
            {"layer_id": "B", "item": "B", "score": 2.0, "max": 6.0, "reason": "B"},
            {"layer_id": "C", "item": "C", "score": c_score, "max": 8.0, "reason": "C"},
            {"layer_id": "D", "item": "D", "score": d_score, "max": 6.0, "reason": "D"},
            {"layer_id": "E", "item": "E", "score": e_score, "max": 2.0, "reason": "E"},
        ]

    def _scoring_model(self):
        return {
            "total_points": 25.0,
            "rater_weights_by_layer": {
                "A": {"professor": 1.0},
                "B": {"professor": 1.0},
                "C": {"professor": 1.0},
                "D": {"executive": 1.0},
                "E": {"professional_engineer": 1.0},
            },
        }

    def _rater_profile(self):
        return {
            "raters": [
                {"id": "professor", "name": "교수", "enabled": True},
                {"id": "professional_engineer", "name": "기술사", "enabled": True},
                {"id": "executive", "name": "임원", "enabled": True},
            ],
        }

    def _run_rater(self, layers):
        grade = {
            "max_score": 25.0,
            "breakdown": layers,
            "answer_text_stats": {"char_count": 1000},
            "weaknesses": ["비용 고려", "시간 고려"],
        }
        return _phase4_apply_rater_weighted_scoring(
            grade,
            self._scoring_model(),
            self._rater_profile(),
        )

    def test_hard_fact_caps_are_terminal_after_rater(self):
        cases = (
            (2.99, 2.0, 0.5),
            (4.99, 3.0, 1.0),
            (6.49, 4.5, 1.5),
        )

        for c_score, d_cap, e_cap in cases:
            with self.subTest(c_score=c_score):
                layers = self._layers(c_score)
                _, _, applied = _phase2_apply_caps(
                    layers,
                    {"cap": None},
                )

                by_id = {row["layer_id"]: row for row in layers}
                self.assertEqual(by_id["D"]["score"], d_cap)
                self.assertEqual(by_id["E"]["score"], e_cap)
                self.assertTrue(
                    any(
                        row.get("id")
                        == "fact_score_limits_solution_and_connection"
                        for row in applied
                    )
                )

                grade = self._run_rater(layers)
                final = {row["layer_id"]: row for row in grade["breakdown"]}

                self.assertLessEqual(final["D"]["score"], d_cap)
                self.assertLessEqual(final["E"]["score"], e_cap)
                self.assertEqual(final["D"]["score"], d_cap)
                self.assertEqual(final["E"]["score"], e_cap)
                self.assertTrue(final["D"]["rater_weighted_diagnostic_only"])
                self.assertTrue(final["E"]["rater_weighted_diagnostic_only"])
                self.assertGreaterEqual(
                    final["D"]["rater_weighted_candidate_score"],
                    final["D"]["score"],
                )
                self.assertGreaterEqual(
                    final["E"]["rater_weighted_candidate_score"],
                    final["E"]["score"],
                )

    def test_topic_aware_soft_fact_caps_are_terminal_after_rater(self):
        layers = self._layers(4.5)
        context = {
            "decision": {
                "mode": "soft",
                "reason": "test soft cap",
            },
            "semantic_calibration": {
                "semantic_c_ratio": 0.8,
                "semantic_c_score": 6.4,
                "semantic_c_max": 8.0,
            },
        }

        _, _, applied = _phase2_apply_caps(
            layers,
            {"cap": None},
            topic_cap_context=context,
        )

        by_id = {row["layer_id"]: row for row in layers}
        self.assertEqual(by_id["D"]["score"], 4.8)
        self.assertEqual(by_id["E"]["score"], 1.6)
        self.assertEqual(by_id["D"]["fact_dependency_cap_mode"], "topic_aware_soft")
        self.assertEqual(by_id["E"]["fact_dependency_cap_mode"], "topic_aware_soft")
        self.assertTrue(
            any(
                row.get("id")
                == "fact_topic_aware_soft_limits_solution_and_connection"
                and row.get("mode") == "soft"
                for row in applied
            )
        )

        grade = self._run_rater(layers)
        final = {row["layer_id"]: row for row in grade["breakdown"]}

        self.assertEqual(final["D"]["score"], 4.8)
        self.assertEqual(final["E"]["score"], 1.6)
        self.assertTrue(final["D"]["rater_weighted_diagnostic_only"])
        self.assertTrue(final["E"]["rater_weighted_diagnostic_only"])

    def test_no_fact_cap_when_c_reaches_threshold(self):
        layers = self._layers(6.5, d_score=5.25, e_score=1.75)
        _, _, applied = _phase2_apply_caps(
            layers,
            {"cap": None},
        )

        by_id = {row["layer_id"]: row for row in layers}
        self.assertEqual(by_id["D"]["score"], 5.25)
        self.assertEqual(by_id["E"]["score"], 1.75)
        self.assertFalse(
            any(
                str(row.get("id", "")).startswith("fact_")
                for row in applied
            )
        )

        grade = self._run_rater(layers)
        final = {row["layer_id"]: row for row in grade["breakdown"]}
        self.assertEqual(final["D"]["score"], 5.25)
        self.assertEqual(final["E"]["score"], 1.75)


if __name__ == "__main__":
    unittest.main(verbosity=1)
