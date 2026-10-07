from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "process_control_loop_architecture_cascade_ratio_feedforward_override_split_range"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class ProcessControlLoopArchitecturePatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")
        cls.readme = (PACK / "README.md").read_text(encoding="utf-8")
        cls.sheet = (ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md").read_text(encoding="utf-8")

    def test_all_eight_patterns_have_intents_and_anchor_trace(self) -> None:
        patterns = self.model["expected_question_patterns"]
        self.assertEqual(len(patterns), 8)
        self.assertTrue(all(row.get("intent") and row.get("required_anchor_ids") for row in patterns))

        anchor_ids = {row.get("id", row.get("anchor_id")) for row in self.fact["anchors"]}
        required = {anchor for row in patterns for anchor in row["required_anchor_ids"]}
        outline = {anchor for row in self.model["recommended_outline"] for anchor in row["anchor_refs"]}
        self.assertEqual(required, anchor_ids)
        self.assertEqual(outline, anchor_ids)

    def test_scoring_guidance_is_question_scoped(self) -> None:
        high = "\n".join(self.model["high_score_points"])
        missing = "\n".join(self.model["common_missing_points"])
        importance = "\n".join(self.importance["high_band_unlock_conditions"])
        for n in range(1, 9):
            self.assertIn(f"Pattern {n}", high)
            self.assertIn(f"Pattern {n}", missing)
            self.assertIn(f"Pattern {n}", importance)

        self.assertIn("Pattern 1 and Pattern 8", high)
        self.assertIn("Pattern 5 and Pattern 7", missing)
        self.assertIn("요청되지 않은", high)

    def test_internal_mapping_is_not_misrepresented_as_official(self) -> None:
        combined = self.readme + "\n" + self.sheet + "\n" + json.dumps(self.model, ensure_ascii=False)
        self.assertIn("repository-local", combined)
        self.assertIn("not official exam classifications", combined)
        self.assertNotIn("Official criteria:", self.sheet)

    def test_existing_grading_type_and_neighbor_ownership_are_unchanged(self) -> None:
        self.assertEqual(self.model["question_type"], "COMPARE_SELECTION")
        self.assertEqual(self.importance["question_type"], "COMPARE_SELECTION")
        self.assertEqual(self.importance["difficulty"], "THEORY_CORE")
        for topic_id in (
            "pid_controller_tuning_sequence_gain_effects",
            "feedback_system_closed_loop_sensitivity_steady_state_error",
            "control_valve_authority_rangeability_gain_installed_performance",
        ):
            self.assertIn(topic_id, self.readme)


if __name__ == "__main__":
    unittest.main(verbosity=2)
