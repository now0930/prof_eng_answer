from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from grading.scoring import difficulty_strategy
from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_primary_grader import grade_deterministically
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

    def test_runtime_route_and_provider_free_grade_use_approved_topic(self) -> None:
        question = (
            "전기계(RLC)와 기계계(질량-스프링-댐퍼)의 "
            "2차 시스템 유사관계를 설명하시오."
        )
        answer = (
            "기계계는 m x¨ + D x˙ + kx = f(t)로 나타낸다. "
            "직렬 RLC계는 L q¨ + R q˙ + (1/C)q = E(t)이다. "
            "Force–Voltage analogy에서 f와 E, m과 L, D와 R, "
            "k와 1/C, x와 q, 속도와 전류를 대응시킨다. "
            "이 대응은 두 방정식 구조의 모델 유사성이다. "
            "L q¨ 항의 차원이 입력 전압과 일치하는지 확인한다."
        )

        route = route_question_topics(question)
        grade = grade_deterministically(
            question_text=question,
            answer_text=answer,
        )

        self.assertEqual(route.get("primary_topic_id"), TOPIC_ID)
        self.assertEqual(grade.get("topic_id"), TOPIC_ID)
        self.assertEqual(grade.get("provider_calls"), 0)
        self.assertFalse(
            grade.get("logic_check_evaluation", {}).get("fatal_error_detected")
        )
        self.assertEqual(grade.get("logic_check_evaluation", {}).get("findings"), [])


if __name__ == "__main__":
    unittest.main()
