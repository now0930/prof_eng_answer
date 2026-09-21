import unittest

from deterministic_topic_router import route_question_topics


class Chapter8And19TopicRoutingTests(unittest.TestCase):
    def assert_primary(self, question: str, expected: str) -> None:
        route = route_question_topics(question)
        self.assertEqual(route["status"], "ROUTED")
        self.assertEqual(route["primary_topic_id"], expected)
        self.assertEqual(route["provider_calls"], 0)
        self.assertFalse(route["answer_text_used"])

    def test_new_atomic_topics_own_their_questions(self):
        cases = {
            "계장 고속신호에서 전송선로 효과, 반사 원인과 종단 대책을 설명하시오.":
                "instrument_signal_transmission_line_reflection_termination",
            "광원·power meter와 OTDR 시험의 목적, 원리와 한계를 비교하시오.":
                "fiber_optic_link_modes_dispersion_loss_otdr_diagnostics",
            "Force-balance 압력변환기의 pneumatic 및 electronic 동작원리를 설명하시오.":
                "pressure_transmitter_force_balance_null_detection",
            "DP transmitter 3-valve manifold의 정상·격리·복귀 조작절차와 안전상 유의점을 설명하시오.":
                "dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation",
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                self.assert_primary(question, expected)

    def test_existing_chapter7_13_and_pressure_owners_are_preserved(self):
        cases = {
            "PFD, P&ID, Loop Diagram과 Functional Diagram의 역할과 관계를 설명하시오.":
                "pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative",
            "4–20 mA current loop의 live zero와 2-wire transmitter를 설명하시오.":
                "analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting",
            "압력센서의 Bourdon tube, diaphragm과 piezoresistive 원리를 비교하시오.":
                "pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error",
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                self.assert_primary(question, expected)


if __name__ == "__main__":
    unittest.main()
