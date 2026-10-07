from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


TOPIC_ID = "sis_sil_safety_software_independence_systematic_failure_verification_validation"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class SisSilPatternScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")

    def test_pattern_corpus_composition_and_intents(self) -> None:
        patterns = self.model["expected_question_patterns"]
        examples = self.model["question_examples"]
        self.assertEqual(len(patterns), 15)
        self.assertEqual(len(examples), 10)
        self.assertEqual([row["pattern"] for row in patterns[:10]], examples)
        intents = [row.get("intent", "").strip() for row in patterns]
        self.assertTrue(all(intents))
        self.assertEqual(len(set(intents)), len(intents))

    def test_scoring_and_importance_text_is_scoped_to_patterns(self) -> None:
        text = "\n".join(
            self.model["high_score_points"]
            + self.model["common_missing_points"]
            + self.importance["high_band_unlock_conditions"]
        )
        numbers = {int(value) for value in re.findall(r"Pattern (\d+)", text)}
        self.assertEqual(numbers, set(range(1, 16)))

        model_patterns = self.model["expected_question_patterns"]
        self.assertEqual(
            model_patterns[10]["intent"].split(":", 1)[0], "Boundary guard"
        )
        self.assertEqual(
            model_patterns[11]["intent"].split(":", 1)[0], "Boundary guard"
        )
        self.assertEqual(
            model_patterns[12]["intent"].split(":", 1)[0], "Boundary guard"
        )

    def test_semantic_routing_and_evaluator_contracts_are_preserved(self) -> None:
        fact = load("fact_anchor.json")
        logic = load("logic_check.json")
        self.assertEqual(self.model["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.model["topic_aliases"], self.model["routing_aliases"])
        self.assertEqual(len(fact["anchors"]), 34)
        self.assertEqual(len(fact["fatal_wrong_claims"]), 18)
        self.assertFalse(logic["deterministic_checks"]["enabled"])
        self.assertEqual(len(logic["llm_profile"]["major_checks"]), 12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
