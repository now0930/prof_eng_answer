from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "pressure_transmitter_force_balance_null_detection"
ROOT = Path(__file__).resolve().parents[1]
# Proposed scope wording is reviewable without replacing the approved source.
PACK = ROOT / "rubrics" / "topic_pack_candidates" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class ForceBalancePressureTransmitterTopicPackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")
        cls.sheet = (PACK / "proposed_topic_sheet.md").read_text(encoding="utf-8")

    def test_identity_and_pattern_contract(self) -> None:
        self.assertEqual(len(self.model["expected_question_patterns"]), 2)
        self.assertIn("pneumatic/electronic feedback", self.model["expected_question_patterns"][0]["intent"])
        self.assertIn("trade-off", self.model["expected_question_patterns"][1]["intent"])

        anchors = {row["anchor_id"] for row in self.fact["anchors"]}
        required = {
            anchor_id
            for pattern in self.model["expected_question_patterns"]
            for anchor_id in pattern["required_anchor_ids"]
        }
        self.assertEqual(required, anchors)
        outline = {
            anchor_id
            for section in self.model["recommended_outline"]
            for anchor_id in section["anchor_refs"]
        }
        self.assertEqual(outline, anchors)

    def test_cross_pattern_scoring_requirements_are_limited(self) -> None:
        high = "\n".join(self.model["high_score_points"])
        missing = "\n".join(self.model["common_missing_points"])
        importance = "\n".join(self.importance["high_band_unlock_conditions"])

        self.assertIn("Pattern 1에서만", high)
        self.assertIn("Pattern 2에서만", high)
        self.assertIn("Pattern 1에서만", missing)
        self.assertIn("Pattern 2에서만", missing)
        self.assertIn("Pattern 1(동작원리 비교)에서만", importance)
        self.assertIn("Pattern 2(특징·장단점·적용)에서만", importance)
        self.assertIn("Pattern-specific grading boundary", self.sheet)
        self.assertIn("intrinsic-safety", self.sheet)

    def test_core_mechanism_and_ownership_are_preserved(self) -> None:
        serialized = json.dumps(self.fact, ensure_ascii=False) + json.dumps(self.model, ensure_ascii=False)
        for term in ("Fsensed=ΔP·A", "position error", "baffle-nozzle", "force coil"):
            self.assertIn(term, serialized)
        self.assertIn("pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error", self.sheet)
        self.assertIn("dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation", self.sheet)


if __name__ == "__main__":
    unittest.main(verbosity=2)
