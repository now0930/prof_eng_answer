#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class PiezoelectricTopicPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.logic = load("logic_check.json")
        cls.importance = load("topic_importance.json")
        cls.anchors = {row["id"]: row for row in cls.fact["anchors"]}
        cls.patterns = cls.model["expected_question_patterns"]

    def test_topic_identity_and_existing_question_type_are_preserved(self) -> None:
        for payload in (self.fact, self.model, self.logic, self.importance):
            self.assertEqual(payload["topic_id"], TOPIC_ID)
        self.assertEqual(self.model["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.importance["question_type"], "PRINCIPLE_INTERPRETATION")

    def test_each_expected_question_has_a_distinct_intent_and_example(self) -> None:
        patterns = [row["pattern"] for row in self.patterns]
        intents = [row["intent"] for row in self.patterns]
        self.assertEqual(self.model["question_examples"], patterns)
        self.assertEqual(len(intents), len(set(intents)))
        self.assertTrue(all(len(intent) >= 20 for intent in intents))

    def test_anchor_references_cover_the_defined_fact_inventory(self) -> None:
        anchor_ids = set(self.anchors)
        required_union: set[str] = set()
        for row in self.patterns:
            required = set(row["required_anchor_ids"])
            self.assertTrue(required)
            self.assertTrue(required <= anchor_ids)
            required_union |= required
        self.assertEqual(required_union, anchor_ids)

    def test_global_feedback_text_is_scoped_to_question_patterns(self) -> None:
        model_text = self.model["high_score_points"] + self.model["common_missing_points"]
        importance_text = self.importance["high_band_unlock_conditions"]
        self.assertTrue(all("문항" in row for row in model_text))
        self.assertTrue(all("문항" in row for row in importance_text))

    def test_direct_inverse_effect_and_sensitivity_unit_boundary(self) -> None:
        direct = self.anchors["piezoelectric_direct_inverse_effect_distinction"]["statement"]
        units = self.anchors["piezoelectric_charge_voltage_sensitivity_units"]["statement"]
        self.assertIn("기계적 입력을 전하", direct)
        self.assertIn("전기장을 변형", direct)
        self.assertIn("pC/N", units)
        self.assertIn("mV/N", units)
        self.assertIn("전하감도", units)
        self.assertIn("전압감도", units)

    def test_custom_candidate_rules_are_empty_but_key_term_extraction_is_configured(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        extraction = self.logic["llm_profile"]["candidate_extraction"]
        self.assertFalse(deterministic["enabled"])
        self.assertEqual(extraction["rules"], [])
        self.assertTrue(extraction["key_terms"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
