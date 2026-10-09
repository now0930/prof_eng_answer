#!/usr/bin/env python3
from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.scoring.deterministic_primary_grader import grade_deterministically


TOPIC_ID = "flow_measurement_meter_principles_velocity_selection"


class FlowMeasurementOntologyContractTests(unittest.TestCase):
    def grade(self, question: str, answer: str) -> dict:
        result = grade_deterministically(question_text=question, answer_text=answer)
        self.assertEqual(result["topic_id"], TOPIC_ID)
        self.assertEqual(result["grading_engine"], "deterministic_primary")
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["llm_verdict_authority"], 0)
        self.assertFalse(result["external_llm_required_for_verdict"])
        return result

    def test_meter_comparison_is_routed_and_graded_without_provider(self) -> None:
        question = "유량계 종류별 원리와 적용 조건을 설명하시오."
        answer = (
            "체적유량은 단면적과 단면 평균유속의 곱이다. "
            "밀도가 균일한 경우 질량유량은 밀도와 체적유량의 곱이다. "
            "피토관은 전압과 정압의 차로 국소 유속을 측정한다. "
            "가변면적식 유량계는 float 평형위치를 측정하여 유량을 지시한다. "
            "용적식 유량계는 측정실의 반복 체적을 계수한다. "
            "터빈 유량계는 rotor 회전 주파수로 측정한다. "
            "와류 유량계는 와류 방출 주파수로 측정한다. "
            "전자기 유량계는 도전성 유체에 적용한다. "
            "초음파 transit-time 유량계는 흐름 방향과 역방향의 전파시간 차로 측정한다. "
            "초음파 Doppler 유량계는 반사체의 도플러 주파수 이동으로 측정한다. "
            "코리올리스 유량계는 진동 튜브 위상 응답을 측정한다. "
            "열식 유량계는 유동에 따른 열전달을 측정한다. "
            "차압식 유량계 primary element는 오리피스 플레이트, 유량 노즐, 벤투리관으로 구성된다. "
            "유체 물성, 유량범위, 압력손실, 설치와 유지보수 조건으로 유량계를 선정한다. "
            "유동 profile은 상류 배관 교란과 swirl 영향을 받으므로 직관부 설치조건을 확인한다."
        )

        result = self.grade(question, answer)

        self.assertEqual(
            result["routing_evaluation"]["primary_topic_id"],
            TOPIC_ID,
        )
        self.assertEqual(result["requirement_summary"]["WRONG"], 0)
        self.assertEqual(result["requirement_summary"]["MISSING"], 0)
        self.assertFalse(result["logic_check_evaluation"]["fatal_error_detected"])

    def test_nonconductive_magnetic_meter_claim_is_fatal(self) -> None:
        result = self.grade(
            "전자기 유량계 적용 조건을 설명하시오.",
            "전자기 유량계는 비전도성 유체에 적용한다.",
        )

        self.assertTrue(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertIn(
            "flow_magnetic_meter_nonconductive_fatal",
            {
                row["finding_id"]
                for row in result["logic_check_evaluation"]["findings"]
            },
        )

    def test_density_qualified_mass_flow_relation_is_accepted(self) -> None:
        result = self.grade(
            "체적유량과 질량유량의 관계를 설명하시오.",
            "밀도가 균일한 경우 질량유량은 밀도와 체적유량의 곱이다.",
        )

        self.assertFalse(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertEqual(result["requirement_summary"]["WRONG"], 0)

    def test_conflating_mass_and_volume_flow_is_fatal(self) -> None:
        result = self.grade(
            "체적유량과 질량유량의 관계를 설명하시오.",
            "질량유량은 체적유량과 같은 물리량이다.",
        )

        self.assertTrue(result["logic_check_evaluation"]["fatal_error_detected"])
        self.assertIn(
            "flow_mass_volume_rate_conflation",
            {
                row["finding_id"]
                for row in result["logic_check_evaluation"]["findings"]
            },
        )


if __name__ == "__main__":
    unittest.main()
