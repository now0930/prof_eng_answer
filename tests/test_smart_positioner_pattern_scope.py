import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "smart_positioner_diagnostics_valve_signature_predictive_maintenance"


class SmartPositionerPatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
        cls.model = json.loads((cls.pack / "model_answer.json").read_text(encoding="utf-8"))
        cls.importance = json.loads((cls.pack / "topic_importance.json").read_text(encoding="utf-8"))
        cls.anchors = json.loads((cls.pack / "fact_anchor.json").read_text(encoding="utf-8"))["anchors"]

    def test_question_patterns_cover_pack_and_have_intents(self):
        patterns = self.model["expected_question_patterns"]
        self.assertEqual(len(patterns), 10)
        self.assertTrue(all(row.get("intent", "").strip() for row in patterns))
        required = set().union(*(set(row["required_anchor_ids"]) for row in patterns))
        self.assertEqual(required, {row["id"] for row in self.anchors})

    def test_scoring_and_importance_criteria_name_their_pattern_scope(self):
        count = len(self.model["expected_question_patterns"])
        scoped = re.compile(r"^\[(?:P(?:[1-9]|10)(?:-P(?:[1-9]|10))?)(?:,P(?:[1-9]|10)(?:-P(?:[1-9]|10))?)*\]")
        for field in ("high_score_points", "common_missing_points"):
            for point in self.model[field]:
                self.assertRegex(point, scoped)
        for point in self.importance["high_band_unlock_conditions"]:
            self.assertRegex(point, scoped)
        for match in re.finditer(r"P(\d+)", " ".join(
            self.model["high_score_points"]
            + self.model["common_missing_points"]
            + self.importance["high_band_unlock_conditions"]
        )):
            self.assertLessEqual(int(match.group(1)), count)

    def test_routing_and_question_type_contract_unchanged(self):
        self.assertEqual(self.model["question_type"], "DIAGNOSIS_ACTION")
        self.assertEqual(self.importance["question_type"], "DIAGNOSIS_ACTION")
        self.assertEqual(self.model["topic_id"], TOPIC_ID)


if __name__ == "__main__":
    unittest.main()
