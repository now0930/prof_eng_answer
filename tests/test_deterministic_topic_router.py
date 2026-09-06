import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_topic_router import route_question_topics


class DeterministicTopicRouterTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
