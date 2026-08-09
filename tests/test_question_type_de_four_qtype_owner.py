#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading_agents import _phase4_apply_rater_weighted_scoring


class FourQuestionTypeDEScoreOwnerRegression(unittest.TestCase):
    QTYPE_SCORES = {
        "PRINCIPLE_INTERPRETATION": (4.25, 1.50),
        "DIAGNOSIS_ACTION": (5.10, 1.70),
        "COMPARE_SELECTION": (4.80, 1.60),
        "IMPLEMENTATION_EVALUATION": (5.40, 1.80),
    }

    def _grade(self, qtype: str, d_score: float, e_score: float):
        return {
            "max_score": 25.0,
            "question_type": qtype,
            "question_type_id": qtype,
            "breakdown": [
                {"layer_id": "A", "item": "A", "score": 1.0, "max": 3.0, "reason": "A"},
                {"layer_id": "B", "item": "B", "score": 2.0, "max": 6.0, "reason": "B"},
                {"layer_id": "C", "item": "C", "score": 6.5, "max": 8.0, "reason": "C"},
                {"layer_id": "D", "item": "D", "score": d_score, "max": 6.0, "reason": f"{qtype} D authoritative"},
                {"layer_id": "E", "item": "E", "score": e_score, "max": 2.0, "reason": f"{qtype} E authoritative"},
            ],
            "answer_text_stats": {"char_count": 1000},
            "weaknesses": ["비용 고려", "시간 고려"],
        }

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

    def test_all_four_question_types_preserve_authoritative_de(self):
        self.assertEqual(
            set(self.QTYPE_SCORES),
            {
                "PRINCIPLE_INTERPRETATION",
                "DIAGNOSIS_ACTION",
                "COMPARE_SELECTION",
                "IMPLEMENTATION_EVALUATION",
            },
        )

        for qtype, (d_score, e_score) in self.QTYPE_SCORES.items():
            with self.subTest(question_type=qtype):
                grade = _phase4_apply_rater_weighted_scoring(
                    self._grade(qtype, d_score, e_score),
                    self._scoring_model(),
                    self._rater_profile(),
                )
                by_id = {row["layer_id"]: row for row in grade["breakdown"]}

                self.assertEqual(by_id["D"]["score"], round(d_score, 2))
                self.assertEqual(by_id["E"]["score"], round(e_score, 2))
                self.assertTrue(by_id["D"]["rater_weighted_diagnostic_only"])
                self.assertTrue(by_id["E"]["rater_weighted_diagnostic_only"])
                self.assertFalse(by_id["D"]["rater_weighted"])
                self.assertFalse(by_id["E"]["rater_weighted"])

                # Deliberately selected raters would change D/E if legacy
                # numeric overwrite were restored.
                self.assertNotEqual(
                    by_id["D"]["rater_weighted_candidate_score"],
                    by_id["D"]["score"],
                )
                self.assertNotEqual(
                    by_id["E"]["rater_weighted_candidate_score"],
                    by_id["E"]["score"],
                )

                self.assertEqual(
                    by_id["D"]["score_before_rater_weight"],
                    d_score,
                )
                self.assertEqual(
                    by_id["E"]["score_before_rater_weight"],
                    e_score,
                )

                expected_total = round(
                    sum(float(row["score"]) for row in grade["breakdown"]),
                    2,
                )
                self.assertEqual(grade["total_score"], expected_total)


if __name__ == "__main__":
    unittest.main(verbosity=1)
