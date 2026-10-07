import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
SCOPE = re.compile(r"^\[(?:P\d+(?:-P\d+)?)(?:,P\d+(?:-P\d+)?)*\]")


class SafetyCriticalSoftwarePatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
        cls.model = json.loads((cls.pack / "model_answer.json").read_text(encoding="utf-8"))
        cls.importance = json.loads((cls.pack / "topic_importance.json").read_text(encoding="utf-8"))
        cls.anchors = json.loads((cls.pack / "fact_anchor.json").read_text(encoding="utf-8"))["anchors"]

    def test_question_intent_example_and_anchor_contract(self):
        patterns = self.model["expected_question_patterns"]
        self.assertEqual(len(patterns), 12)
        self.assertEqual(self.model["question_examples"], [row["pattern"] for row in patterns])
        self.assertTrue(all(row.get("intent", "").strip() for row in patterns))
        required = set().union(*(set(row["required_anchor_ids"]) for row in patterns))
        self.assertEqual(required, {row["id"] for row in self.anchors})
        self.assertEqual(len(required), 33)

    def test_evaluation_points_are_pattern_scoped(self):
        points = self.model["high_score_points"] + self.model["common_missing_points"]
        points += self.importance["high_band_unlock_conditions"]
        for point in points:
            self.assertRegex(point, SCOPE)
            for number in map(int, re.findall(r"P(\d+)", SCOPE.match(point).group(0))):
                self.assertLessEqual(number, 12)

    def test_question_type_and_identity_unchanged(self):
        self.assertEqual(self.model["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.importance["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.model["topic_id"], TOPIC_ID)


if __name__ == "__main__":
    unittest.main()
