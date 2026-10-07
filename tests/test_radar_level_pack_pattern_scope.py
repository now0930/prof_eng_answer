from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class RadarLevelPackPatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")
        cls.readme = (PACK / "README.md").read_text(encoding="utf-8")
        cls.sheet = (ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md").read_text(encoding="utf-8")

    def test_14_patterns_and_questions_have_anchor_scope(self) -> None:
        patterns = self.model["expected_question_patterns"]
        examples = self.model["question_examples"]
        self.assertEqual(len(patterns), 14)
        self.assertEqual(len(examples), 14)
        self.assertTrue(all(row.get("intent") and row.get("required_anchor_ids") for row in patterns))

        anchor_ids = {row.get("id", row.get("anchor_id")) for row in self.fact["anchors"]}
        required = {anchor for row in patterns for anchor in row["required_anchor_ids"]}
        self.assertEqual(len(anchor_ids), 28)
        self.assertEqual(len(required), 20)

    def test_unlinked_nuance_and_gwr_anchors_are_optional(self) -> None:
        patterns = self.model["expected_question_patterns"]
        required = {anchor for row in patterns for anchor in row["required_anchor_ids"]}
        by_id = {row.get("id", row.get("anchor_id")): row for row in self.fact["anchors"]}
        optional = set(by_id) - required
        expected = {
            "radar_point_target_equation_scope",
            "radar_echo_polarity_sign_convention",
            "radar_adaptive_threshold_echo_tracking",
            "radar_upper_null_zone_overfill_coordination",
            "gwr_tdr_guided_wave_principle",
            "gwr_effective_permittivity_propagation_path",
            "gwr_quasi_tem_return_path",
            "gwr_interface_and_process_limitations",
        }
        self.assertEqual(optional, expected)
        self.assertTrue(all(by_id[anchor]["importance"] == "optional" for anchor in optional))

    def test_all_scoring_views_are_pattern_scoped_and_gwr_is_not_mandatory(self) -> None:
        high = "\n".join(self.model["high_score_points"])
        missing = "\n".join(self.model["common_missing_points"])
        importance = "\n".join(self.importance["high_band_unlock_conditions"])
        for n in range(1, 15):
            self.assertIn(f"Pattern {n}", high)
            self.assertIn(f"Pattern {n}", missing)
            self.assertIn(f"Pattern {n}", importance)

        self.assertIn("GWR", self.model["expected_question_patterns"][-1]["intent"])
        self.assertIn("필수 점수요건으로 쓰지 않는다", high)
        self.assertIn("Detailed guided-wave TDR", self.sheet)
        self.assertIn("remaining 8 anchors", self.sheet)
        self.assertIn("are `optional`", self.sheet)

    def test_existing_semantic_and_routing_authorities_remain(self) -> None:
        logic = load("logic_check.json")
        self.assertEqual(self.model["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertFalse(logic["deterministic_checks"]["enabled"])
        self.assertEqual(logic["deterministic_checks"]["fatal_checks"], [])
        self.assertIn("draft / human_review_required", self.readme)
        self.assertIn("alias와 routing을 계속 보유한다", self.readme)


if __name__ == "__main__":
    unittest.main(verbosity=2)
