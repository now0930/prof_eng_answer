import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "speed_rotation_measurement_encoder_proximity_tachometer_selection_error": (10, 22, "PRINCIPLE_INTERPRETATION"),
    "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error": (13, 14, "PRINCIPLE_INTERPRETATION"),
    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization": (3, 14, "PRINCIPLE_INTERPRETATION"),
    "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response": (10, 40, "PROBLEM_SOLVE"),
}
SCOPE = re.compile(r"^\[(?:P\d+(?:-P\d+)?)(?:,P\d+(?:-P\d+)?)*\]")


class RemainingScreenTopicScopeTest(unittest.TestCase):
    def test_question_intents_and_anchor_unions(self):
        for topic_id, (pattern_count, anchor_count, _) in CASES.items():
            with self.subTest(topic=topic_id):
                base = ROOT / "rubrics" / "topic_packs" / topic_id
                model = json.loads((base / "model_answer.json").read_text(encoding="utf-8"))
                anchors = json.loads((base / "fact_anchor.json").read_text(encoding="utf-8"))["anchors"]
                patterns = model["expected_question_patterns"]
                self.assertEqual(len(patterns), pattern_count)
                self.assertTrue(all(row.get("intent", "").strip() for row in patterns))
                required = set().union(*(set(row["required_anchor_ids"]) for row in patterns))
                self.assertEqual(len(required), anchor_count)
                self.assertEqual(required, {row["id"] for row in anchors})

    def test_question_scoped_scoring_and_importance(self):
        for topic_id, (pattern_count, _, expected_type) in CASES.items():
            with self.subTest(topic=topic_id):
                base = ROOT / "rubrics" / "topic_packs" / topic_id
                model = json.loads((base / "model_answer.json").read_text(encoding="utf-8"))
                importance = json.loads((base / "topic_importance.json").read_text(encoding="utf-8"))
                self.assertEqual(model["question_type"], expected_type)
                self.assertEqual(importance["question_type"], expected_type)
                points = model.get("high_score_points", []) + model.get("common_missing_points", [])
                points += importance.get("high_band_unlock_conditions", [])
                self.assertTrue(points)
                for point in points:
                    match = SCOPE.match(point)
                    self.assertIsNotNone(match, point)
                    for number in map(int, re.findall(r"P(\d+)", match.group(0))):
                        self.assertLessEqual(number, pattern_count, point)


if __name__ == "__main__":
    unittest.main()
