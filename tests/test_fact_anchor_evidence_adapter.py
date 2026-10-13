import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.evidence.fact_anchor_evidence_adapter import (
    augment_requirement_evaluation,
    evaluate_fact_anchor_requirements,
)


TOPIC = "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration"
SW04 = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"


class FactAnchorEvidenceAdapterTests(unittest.TestCase):
    def test_model_reference_yields_deterministic_anchor_states(self):
        payload = json.loads(
            (REPO / "calibration/expert_accuracy_model_answer_cases.json")
            .read_text(encoding="utf-8")
        )
        case = next(row for row in payload["cases"] if row["topic_id"] == TOPIC)
        result = evaluate_fact_anchor_requirements(
            answer_text=case["answer"], topic_ids=[TOPIC]
        )
        self.assertTrue(result["requirements"])
        self.assertGreater(result["summary"]["SATISFIED"], 0)
        self.assertEqual(result["provider_calls"], 0)

    def test_sparse_answer_is_partial_or_missing_not_satisfied(self):
        result = evaluate_fact_anchor_requirements(
            answer_text="압전 센서는 전하를 측정한다.", topic_ids=[TOPIC]
        )
        self.assertNotEqual(
            {row["status"] for row in result["requirements"]}, {"SATISFIED"}
        )

    def test_unknown_topic_has_no_invented_requirements(self):
        result = evaluate_fact_anchor_requirements(
            answer_text="내용", topic_ids=["not_a_topic"]
        )
        self.assertEqual(result["requirements"], [])

    def test_anchor_id_identity_mention_is_partial_not_satisfied(self):
        result = evaluate_fact_anchor_requirements(
            question_text="Sliding-stem valve와 rotary valve의 구조, 장단점과 적용 조건을 비교하시오.",
            answer_text="Butterfly 형식도 있다.",
            topic_ids=["control_valve_types_globe_rotary_body_actuator_selection"],
        )
        row = next(
            item for item in result["requirements"]
            if item["requirement_id"] == "butterfly_compact_high_capacity"
        )
        self.assertEqual(row["status"], "PARTIAL")
        self.assertIn("butterfly", row["matched_identity_tokens"])

    def test_augmentation_preserves_wrong_machine_requirement(self):
        base = {
            "requirements": [{
                "owner_topic_id": TOPIC, "requirement_id": "fatal_relation",
                "status": "WRONG",
            }],
            "findings": [{"classification": "fatal"}],
            "fatal_or_core_error": True,
        }
        anchors = evaluate_fact_anchor_requirements(
            answer_text="압전 센서는 전하를 측정한다.", topic_ids=[TOPIC]
        )
        result = augment_requirement_evaluation(base, anchors)
        self.assertEqual(result["requirements"][0]["status"], "WRONG")
        self.assertTrue(result["fatal_or_core_error"])

    def test_explicit_question_contract_limits_requirements_to_owned_anchor_ids(self):
        result = evaluate_fact_anchor_requirements(
            question_text="SIF에서 Final Element의 역할과 구성, subsystem boundary를 설명하시오.",
            answer_text="Final Element는 SIF의 출력으로 valve, actuator, solenoid로 구성된다.",
            topic_ids=["final_control_element_sil_sis_esd_valve_partial_stroke_test"],
        )
        self.assertEqual(
            result["question_contract_selections"][0]["mode"],
            "explicit_question_contract",
        )
        self.assertEqual(
            {row["requirement_id"] for row in result["requirements"]},
            {
                "final_element_role_in_sif",
                "system_sif_sil_context_boundary",
                "safe_state_process_hazard_basis",
                "deenergize_to_trip_energy_philosophy",
                "final_element_subsystem_boundary",
                "valve_actuator_solenoid_architecture",
                "utility_supply_and_shared_dependencies",
                "trip_signal_and_output_chain",
                "seat_leakage_as_safety_requirement",
            },
        )

    def test_spacing_variant_matches_authored_identity_term(self):
        result = evaluate_fact_anchor_requirements(
            answer_text="단위 시험은 모듈의 요구사항을 검증한다.",
            topic_ids=[SW04],
        )
        row = next(
            item for item in result["requirements"]
            if item["requirement_id"] == "sw04_unit_test"
        )
        self.assertTrue(row["identity_term_matched"])
        self.assertEqual(row["status"], "PARTIAL")

    def test_low_similarity_question_fails_closed_without_all_anchors(self):
        result = evaluate_fact_anchor_requirements(
            question_text="완전히 관계없는 질문 문장",
            answer_text="많은 용어를 적어도 범위를 추측하지 않는다.",
            topic_ids=[SW04],
        )
        self.assertEqual(
            result["question_contract_selections"][0]["mode"],
            "scope_unresolved",
        )
        self.assertEqual(len(result["requirements"]), 1)
        self.assertEqual(result["requirements"][0]["requirement_id"], "__question_scope__")

    def test_composite_valve_diagnosis_uses_explicit_owner_scopes(self):
        payload = json.loads(
            (REPO / "calibration/qtype_golden/cases/diagnosis_action.json")
            .read_text(encoding="utf-8")
        )
        case = next(row for row in payload["cases"] if row["case_id"] == "QG-DA-PASS-01")
        topics = case["expected"]["expected_topic_ids"]
        result = evaluate_fact_anchor_requirements(
            answer_text=case["answer"],
            topic_ids=topics,
            question_text=case["question"],
        )
        self.assertEqual(
            {row["mode"] for row in result["question_contract_selections"]},
            {"explicit_question_contract"},
        )
        selected_by_topic = {
            topic: {
                row["requirement_id"] for row in result["requirements"]
                if row["owner_topic_id"] == topic
            }
            for topic in topics
        }
        self.assertEqual(
            selected_by_topic["control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe"],
            {
                "control_valve_unbalance_force_effective_area_approximation",
                "control_valve_actuator_sizing_worst_case_conditions",
                "control_valve_packing_friction",
                "control_valve_guide_friction_side_load",
                "control_valve_stiction_deadband_diagnostics",
                "control_valve_seat_load_shutoff_class",
            },
        )
        self.assertEqual(
            selected_by_topic["control_valve_deadband_stiction_response_time_positioner_dynamic_performance"],
            {
                "stiction_stick_then_jump",
                "stiction_limit_cycle_path",
                "oscillation_requires_differential_diagnosis",
                "improvement_verify_same_test_and_process_result",
            },
        )

    def test_same_condition_retest_is_partial_not_full_verification(self):
        payload = json.loads(
            (REPO / "calibration/expert_accuracy_model_answer_cases.json")
            .read_text(encoding="utf-8")
        )
        case = next(
            row for row in payload["cases"]
            if row["case_id"] == "model_reference_08_instrumentation_power_grounding_shielding_ups_ground_loop_emc"
        )
        result = evaluate_fact_anchor_requirements(
            answer_text=case["answer"],
            topic_ids=[case["topic_id"]],
            question_text=case["question"],
        )
        row = next(
            item for item in result["requirements"]
            if item["requirement_id"] == "ipgse_final_verification"
        )
        self.assertEqual(row["status"], "PARTIAL")
        self.assertNotEqual(row["status"], "SATISFIED")
        self.assertIn("동일 조건에서 재검증", row["matched_terms"])

    def test_generic_configuration_change_does_not_require_conditional_psm_fact(self):
        result = evaluate_fact_anchor_requirements(
            question_text="산업용 제어시스템의 형상관리와 변경관리 절차를 설명하시오.",
            answer_text="승인된 기준선에 따라 변경을 검토한다.",
            topic_ids=["configuration_change_release_backup_rollback_migration_obsolescence_management"],
        )
        self.assertEqual(
            result["question_contract_selections"][0]["mode"],
            "explicit_question_contract",
        )
        self.assertNotIn(
            "sw06_documentation_training_knowledge_retention",
            {row["requirement_id"] for row in result["requirements"]},
        )


if __name__ == "__main__":
    unittest.main()
