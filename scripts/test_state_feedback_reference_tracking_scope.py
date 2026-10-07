#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "state_feedback_reference_tracking_prefilter_integral_action"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class StateFeedbackPatternScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")
        cls.anchors = {item["anchor_id"] for item in cls.fact["anchors"]}

    def test_representative_patterns_and_references_are_complete(self) -> None:
        self.assertEqual(len(self.model["expected_question_patterns"]), 5)
        self.assertEqual(len(self.anchors), 14)
        required = {
            anchor_id
            for pattern in self.model["expected_question_patterns"]
            for anchor_id in pattern["required_anchor_ids"]
        }
        outline = {
            anchor_id
            for section in self.model["recommended_outline"]
            for anchor_id in section["anchor_refs"]
        }
        self.assertEqual(len(required), 14)
        self.assertEqual(outline, self.anchors)

    def test_missing_anchors_are_attached_to_the_question_that_needs_them(self) -> None:
        first = self.model["expected_question_patterns"][0]["required_anchor_ids"]
        fifth = self.model["expected_question_patterns"][4]["required_anchor_ids"]
        self.assertIn("state_tracking_pole_placement_tracking_distinction", first)
        self.assertIn("state_tracking_robustness_noise_gain_tradeoff", fifth)

    def test_score_guidance_is_pattern_scoped(self) -> None:
        for key in ("high_score_points", "common_missing_points"):
            with self.subTest(key=key):
                for item in self.model[key]:
                    self.assertIn("패턴", item, f"unscoped {key} item: {item}")
        for item in self.importance["high_band_unlock_conditions"]:
            self.assertIn("패턴", item, item)


if __name__ == "__main__":
    unittest.main()
