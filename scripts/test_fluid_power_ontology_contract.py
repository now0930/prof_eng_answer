#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_primary_grader import grade_deterministically


TOPIC_ID = "fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection"


class FluidPowerOntologyContractTests(unittest.TestCase):
    def grade(self, question: str, answer: str) -> dict:
        result = grade_deterministically(question_text=question, answer_text=answer)
        self.assertEqual(result["topic_id"], TOPIC_ID)
        self.assertEqual(result["grading_engine"], "deterministic_primary")
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["llm_verdict_authority"], 0)
        self.assertFalse(result["external_llm_required_for_verdict"])
        return result

    def test_representative_questions_route_exclusively_to_fluid_power(self) -> None:
        questions = [
            "유압 시스템과 공압 시스템의 작동유체와 기본 구성을 비교하시오.",
            "유압 펌프, 제어밸브 및 액추에이터의 기능과 압력·유량·힘·속도의 관계를 설명하시오.",
            "유압의 방향·압력·유량 제어밸브 종류와 회로상 기능을 설명하시오.",
            "유압 regenerative circuit, unloading circuit 및 accumulator의 기능과 적용조건을 설명하시오.",
            "공기압축기, air receiver, dryer 및 FRL의 기능과 공압 운전 시 고려사항을 설명하시오.",
            "전기-유압 서보밸브의 구성과 전기 입력에서 유압 유량 출력까지의 원리를 설명하시오.",
            "제시된 부하와 운전 조건에 적합한 유공압 회로 구성을 선정하고 검토사항을 설명하시오.",
        ]

        for question in questions:
            with self.subTest(question=question):
                route = route_question_topics(question)
                self.assertEqual(route["primary_topic_id"], TOPIC_ID)
                self.assertEqual(route["source"], "exclusive_question_contract")

    def test_process_control_valve_calibration_is_handed_off(self) -> None:
        route = route_question_topics(
            "공정 제어밸브 actuator의 positioner와 I/P converter 교정 절차를 설명하시오."
        )

        self.assertNotEqual(route["primary_topic_id"], TOPIC_ID)

    def test_correct_working_fluid_distinction_is_accepted_without_provider(self) -> None:
        result = self.grade(
            "유압 시스템과 공압 시스템의 작동유체를 구분하시오.",
            "유압 시스템의 작동유체는 액체이다. 공압 시스템의 작동유체는 기체이다.",
        )

        self.assertEqual(result["requirement_summary"]["WRONG"], 0)
        requirement_statuses = {
            row["requirement_id"]: row["status"]
            for row in result["requirements"]
            if row.get("owner_topic_id") == TOPIC_ID
        }
        self.assertEqual(
            requirement_statuses["hydraulic_working_fluid"],
            "SATISFIED",
        )
        self.assertEqual(
            requirement_statuses["pneumatic_working_fluid"],
            "SATISFIED",
        )
        self.assertFalse(result["logic_check_evaluation"]["fatal_error_detected"])

    def test_reversed_hydraulic_working_fluid_is_fatal(self) -> None:
        result = self.grade(
            "유압 시스템의 작동유체를 설명하시오.",
            "유압 시스템의 작동유체는 기체이다.",
        )

        self.assertTrue(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertIn(
            "fluid_power_hydraulic_working_fluid_fatal",
            {
                row["finding_id"]
                for row in result["logic_check_evaluation"]["findings"]
            },
        )

    def test_reversed_pneumatic_working_fluid_is_fatal(self) -> None:
        result = self.grade(
            "공압 시스템의 작동유체를 설명하시오.",
            "공압 시스템의 작동유체는 액체이다.",
        )

        self.assertTrue(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertIn(
            "fluid_power_pneumatic_working_fluid_fatal",
            {
                row["finding_id"]
                for row in result["logic_check_evaluation"]["findings"]
            },
        )


if __name__ == "__main__":
    unittest.main()
