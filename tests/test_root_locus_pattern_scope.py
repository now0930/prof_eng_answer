from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "root_locus_stability_gain_design"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class RootLocusPatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")

    def test_five_question_patterns_have_intent_and_examples(self) -> None:
        patterns = self.model["expected_question_patterns"]
        examples = self.model["question_examples"]
        self.assertEqual(len(patterns), 5)
        self.assertEqual(len(examples), 5)
        self.assertTrue(all(row.get("intent") for row in patterns))

    def test_all_fact_anchors_are_required_and_present_in_outline(self) -> None:
        anchor_ids = {row["id"] for row in self.fact["anchors"]}
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
        self.assertEqual(len(anchor_ids), 14)
        self.assertEqual(pattern_union, anchor_ids)
        self.assertEqual(outline_union, anchor_ids)

    def test_scoring_and_importance_conditions_are_pattern_scoped(self) -> None:
        high = "\n".join(self.model["high_score_points"])
        missing = "\n".join(self.model["common_missing_points"])
        importance = "\n".join(self.importance["high_band_unlock_conditions"])
        for number in range(1, 6):
            self.assertIn(f"Pattern {number}", high)
            self.assertIn(f"Pattern {number}", missing)
            self.assertIn(f"Pattern {number}", importance)

    def test_existing_grading_and_routing_authorities_are_unchanged(self) -> None:
        logic = load("logic_check.json")
        self.assertEqual(self.model["question_type"], "CALC_DESIGN")
        self.assertFalse(logic["deterministic_checks"]["enabled"])
        self.assertEqual(logic["deterministic_checks"]["fatal_checks"], [])
        self.assertIn("lead compensator", self.model["routing_aliases"])
        self.assertIn("lag compensator", self.model["routing_aliases"])
        self.assertEqual(len(self.fact["fatal_wrong_claims"]), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
