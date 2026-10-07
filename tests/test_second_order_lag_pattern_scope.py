from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "second_order_lag_response_by_damping_ratio"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class SecondOrderLagPatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")

    def test_five_patterns_have_intent_and_matching_examples(self) -> None:
        patterns = self.model["expected_question_patterns"]
        examples = self.model["question_examples"]
        self.assertEqual(len(patterns), 5)
        self.assertEqual(len(examples), 5)
        self.assertTrue(all(row.get("intent") for row in patterns))

    def test_split_damping_anchors_are_traced_by_patterns_and_outline(self) -> None:
        anchor_ids = {row["anchor_id"] for row in self.fact["anchors"]}
        pattern_union = {
            anchor
            for pattern in self.model["expected_question_patterns"]
            for anchor in pattern["required_anchor_ids"]
        }
        outline_union = {
            anchor
            for section in self.model["recommended_outline"]
            for anchor in section.get("anchor_refs", [])
        }
        self.assertEqual(len(anchor_ids), 9)
        self.assertTrue({"so2_zero_negative_damping", "so2_negative_damping_instability"} <= anchor_ids)
        self.assertEqual(pattern_union, anchor_ids)
        self.assertEqual(outline_union, anchor_ids)

    def test_nonpositive_damping_is_pass_required_only_when_requested(self) -> None:
        patterns = self.model["expected_question_patterns"]
        negative_damping = "so2_zero_negative_damping"
        for index, pattern in enumerate(patterns):
            if index in (0, 3):
                self.assertIn(negative_damping, pattern["pass_required_anchor_ids"])
            else:
                self.assertNotIn("pass_required_anchor_ids", pattern)
                self.assertNotIn(negative_damping, pattern["required_anchor_ids"])

    def test_feedback_criteria_are_pattern_scoped_without_contract_changes(self) -> None:
        high = "\n".join(self.model["high_score_points"])
        missing = "\n".join(self.model["common_missing_points"])
        importance = "\n".join(self.importance["high_band_unlock_conditions"])
        for number in range(1, 6):
            self.assertIn(f"Pattern {number}", high)
            self.assertIn(f"Pattern {number}", missing)
            self.assertIn(f"Pattern {number}", importance)

        logic = load("logic_check.json")
        self.assertEqual(self.model["question_type"], "COMPARE_SELECTION")
        self.assertTrue(logic["deterministic_checks"]["enabled"])
        self.assertGreater(len(logic["deterministic_checks"]["fatal_checks"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
