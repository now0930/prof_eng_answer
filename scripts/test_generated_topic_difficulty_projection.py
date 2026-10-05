from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from grading.scoring import difficulty_strategy
from scripts.build_generated_rubrics import build_topic_importance


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "second_order_system_modeling_electromechanical_analogy"


class GeneratedTopicDifficultyProjectionTest(unittest.TestCase):
    def test_approved_question_pattern_maps_to_topic_difficulty(self) -> None:
        source = json.loads(
            (
                ROOT
                / "rubrics"
                / "topic_packs"
                / TOPIC_ID
                / "topic_importance.json"
            ).read_text(encoding="utf-8")
        )
        projected = build_topic_importance(
            [{"topic_importance": source}], "test-version"
        )
        question = (
            "전기계(RLC)와 기계계(질량-스프링-댐퍼)의 "
            "2차 시스템 유사관계를 설명하시오."
        )

        with mock.patch.object(
            difficulty_strategy,
            "load_topic_importance",
            return_value=projected,
        ):
            result = difficulty_strategy.classify_question_difficulty(question)

        self.assertEqual(result.get("topic_id"), TOPIC_ID)
        self.assertEqual(result.get("difficulty"), "THEORY_CORE")
        self.assertEqual(result.get("selection_importance"), "HIGH")
        self.assertIn(question, result.get("matched_aliases", []))


if __name__ == "__main__":
    unittest.main()
