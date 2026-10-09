from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "second_order_system_resonance_frequency_response"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class SecondOrderResonancePatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")

    def test_four_representative_patterns_have_intent_and_examples(self) -> None:
        patterns = self.model["expected_question_patterns"]
        examples = self.model["question_examples"]
        self.assertEqual(len(patterns), 4)
        self.assertEqual(len(examples), 4)
        self.assertTrue(all(pattern.get("intent") for pattern in patterns))

    def test_all_five_anchors_are_traced_by_patterns_and_outline(self) -> None:
        anchor_ids = {f"F{i}" for i in range(1, len(self.fact["anchors"]) + 1)}
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
        self.assertEqual(len(anchor_ids), 5)
        self.assertEqual(pattern_union, anchor_ids)
        self.assertEqual(outline_union, anchor_ids)

    def test_high_score_and_missing_points_are_question_scoped(self) -> None:
        high = "\n".join(self.model["high_score_points"])
        missing = "\n".join(self.model["common_missing_points"])
        importance = "\n".join(self.importance["high_band_unlock_conditions"])
        for number in range(1, 5):
            self.assertIn(f"Pattern {number}", high)
            self.assertIn(f"Pattern {number}", missing)
            self.assertIn(f"Pattern {number}", importance)

        # Field/plant application is required only for Pattern 4, not for the
        # concept-difference question in Pattern 3.
        self.assertIn('"F5"', json.dumps(self.model["expected_question_patterns"][3]))
        self.assertNotIn('"F5"', json.dumps(self.model["expected_question_patterns"][2]))

    def test_existing_semantic_and_fatal_authority_is_unchanged(self) -> None:
        logic = load("logic_check.json")
        self.assertEqual(self.model["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.importance["question_type"], self.model["question_type"])
        self.assertTrue(logic["deterministic_checks"]["enabled"])
        self.assertEqual(len(logic["deterministic_checks"]["fatal_checks"]), 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
