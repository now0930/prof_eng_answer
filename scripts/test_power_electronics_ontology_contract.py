#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.scoring.deterministic_primary_grader import grade_deterministically
from grading.routing.deterministic_topic_router import route_question_topics


TOPIC_ID = "power_electronics_converters_motor_drive_control"


class PowerElectronicsOntologyContractTests(unittest.TestCase):
    def grade(self, question: str, answer: str) -> dict:
        result = grade_deterministically(question_text=question, answer_text=answer)
        self.assertEqual(result["topic_id"], TOPIC_ID)
        self.assertEqual(result["grading_engine"], "deterministic_primary")
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["llm_verdict_authority"], 0)
        self.assertFalse(result["external_llm_required_for_verdict"])
        return result

    def test_representative_questions_route_exclusively_to_this_topic(self) -> None:
        questions = [
            "정류기와 인버터의 변환 방향을 비교하시오.",
            "전력변환기의 AC-DC, DC-DC, DC-AC 및 AC-AC 변환 원리와 적용을 설명하시오.",
            "다이오드, SCR, IGBT 및 MOSFET의 제어 특성과 전력변환기 내 역할을 비교하시오.",
            "정류기의 위상제어와 PWM DC-DC 변환의 출력제어 원리 및 파형·손실 특성을 설명하시오.",
            "전압원 인버터와 전류원 인버터의 차이, PWM의 기능 및 주요 설계 고려사항을 설명하시오.",
            "유도전동기의 가변속 구동에서 V/f 제어와 자속기준 벡터제어의 목적·원리·적용상 차이를 설명하시오.",
            "전력변환기 및 전동기 구동설비의 고조파, 효율, 열, EMC·보호와 시운전 고려사항을 설명하시오.",
        ]

        for question in questions:
            with self.subTest(question=question):
                route = route_question_topics(question)
                self.assertEqual(route["primary_topic_id"], TOPIC_ID)
                self.assertEqual(route["source"], "exclusive_question_contract")

    def test_shaft_speed_sensor_selection_is_handed_off(self) -> None:
        route = route_question_topics(
            "전동기 회전속도 센서의 encoder 선정과 계측오차를 설명하시오."
        )

        self.assertNotEqual(route["primary_topic_id"], TOPIC_ID)

    def test_rectifier_and_inverter_direction_is_checked_without_provider(self) -> None:
        result = self.grade(
            "정류기와 인버터의 변환 방향을 비교하시오.",
            "정류기의 출력은 직류이다. 인버터의 출력은 교류이다.",
        )

        self.assertEqual(result["requirement_summary"]["WRONG"], 0)
        self.assertEqual(result["requirement_summary"]["MISSING"], 0)
        self.assertEqual(result["requirement_summary"]["SATISFIED"], 2)
        self.assertFalse(result["logic_check_evaluation"]["fatal_error_detected"])

    def test_reversed_rectifier_direction_is_fatal(self) -> None:
        result = self.grade(
            "정류기의 변환 방향을 설명하시오.",
            "정류기의 출력은 교류이다.",
        )

        self.assertTrue(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertIn(
            "converter_rectifier_direction_fatal",
            {
                row["finding_id"]
                for row in result["logic_check_evaluation"]["findings"]
            },
        )

    def test_reversed_inverter_direction_is_fatal(self) -> None:
        result = self.grade(
            "인버터의 변환 방향을 설명하시오.",
            "인버터의 출력은 직류이다.",
        )

        self.assertTrue(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertIn(
            "converter_inverter_direction_fatal",
            {
                row["finding_id"]
                for row in result["logic_check_evaluation"]["findings"]
            },
        )


if __name__ == "__main__":
    unittest.main()
