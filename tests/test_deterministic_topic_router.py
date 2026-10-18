import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_primary_grader import grade_deterministically


class DeterministicTopicRouterTests(unittest.TestCase):
    def test_thermistor_subject_is_not_overridden_by_generic_flow_pattern(self):
        for subject in ("Thermistor", "서미스터"):
            with self.subTest(subject=subject):
                result = route_question_topics(
                    f"{subject} 온도센서의 측정원리와 NTC·PTC 특성 및 적용조건을 설명하시오."
                )
                self.assertEqual(
                    result["primary_topic_id"],
                    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
                )
                self.assertNotIn(
                    "flow_measurement_meter_principles_velocity_selection", result["topic_ids"]
                )

    def test_real_flow_question_retains_exclusive_routing(self):
        for question in (
            "유량계의 종류별 측정원리와 적용조건을 비교하시오.",
            "유량계의 종류별 측정 원리 및 적용 조건을 설명하시오.",
        ):
            with self.subTest(question=question):
                result = route_question_topics(question)
                self.assertEqual(
                    result["primary_topic_id"],
                    "flow_measurement_meter_principles_velocity_selection",
                )
                self.assertEqual(result["source"], "exclusive_question_contract")

    def test_other_explicit_subjects_survive_unrelated_fuzzy_exclusivity(self):
        cases = (
            (
                "공정 조건에 적합한 유량계 선정 기준과 현장 오차 대책을 설명하시오.",
                "flow_measurement_meter_principles_velocity_selection",
            ),
            (
                "압전센서용 전하증폭기의 원리와 설계요소를 설명하시오.",
                "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
            ),
            (
                "압전식 힘센서의 원리와 오차요인을 설명하시오.",
                "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
            ),
            (
                "압전식 압력센서의 동압 측정원리와 설치조건을 설명하시오.",
                "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
            ),
            (
                "로드셀 신호용 계측증폭기와 ADC 설계 시 고려사항을 설명하시오.",
                "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error",
            ),
        )
        for question, owner in cases:
            with self.subTest(question=question):
                self.assertEqual(route_question_topics(question)["primary_topic_id"], owner)

    def test_thermistor_grade_uses_temperature_requirements(self):
        result = grade_deterministically(
            question_text="Thermistor 온도센서의 측정원리와 NTC·PTC 특성 및 적용조건을 설명하시오.",
            answer_text=(
                "서미스터는 온도에 따라 저항이 변하는 온도센서이다. "
                "NTC는 온도가 상승하면 저항이 감소하고, PTC는 저항이 증가한다. "
                "저항과 온도의 관계는 비선형이므로 보정이 필요하다."
            ),
        )
        self.assertEqual(
            result["topic_id"],
            "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
        )
        self.assertEqual(result["topic_ids"], [result["topic_id"]])
        self.assertTrue(result["requirements"])
        self.assertEqual(
            {row["owner_topic_id"] for row in result["requirements"]},
            {result["topic_id"]},
        )
        self.assertEqual(result["provider_calls"], 0)

    def test_question_only_route_is_repeatable(self):
        question = "열전대 온도센서의 측정 원리와 기준접점 보상이 필요한 이유를 설명하시오."
        first = route_question_topics(question)
        self.assertEqual(first, route_question_topics(question))
        self.assertEqual(first["provider_calls"], 0)
        self.assertFalse(first["answer_text_used"])
        self.assertEqual(
            first["primary_topic_id"],
            "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
        )

    def test_multi_concept_question_retains_exact_alias_secondary(self):
        result = route_question_topics(
            "높은 차압에서 닫힘에 실패하고 스템 마찰과 불연속적인 움직임이 관찰된 제어밸브의 원인과 조치를 설명하시오."
        )
        self.assertIn(
            "control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe",
            result["topic_ids"],
        )
        self.assertIn(
            "control_valve_deadband_stiction_response_time_positioner_dynamic_performance",
            result["topic_ids"],
        )

    def test_specific_v_model_question_uses_exclusive_contract(self):
        result = route_question_topics(
            "제어 소프트웨어 개발 수명 주기(V-Model)의 단위 시험, 통합 시험, "
            "시스템 시험과 SIL 달성을 위한 검증 방안을 설명하시오."
        )
        self.assertEqual(result["source"], "exclusive_question_contract")
        self.assertEqual(
            result["primary_topic_id"],
            "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation",
        )
        self.assertEqual(result["topic_ids"], [result["primary_topic_id"]])

    def test_control_architecture_question_is_not_captured_by_power_electronics(self):
        result = route_question_topics(
            "PLC, DCS, SCADA의 제어 아키텍처별 역할을 비교하시오."
        )
        self.assertEqual(
            result["primary_topic_id"],
            "plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability",
        )


if __name__ == "__main__":
    unittest.main()
