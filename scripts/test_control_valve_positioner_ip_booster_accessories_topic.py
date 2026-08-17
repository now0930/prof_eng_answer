#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_llm_verifier import extract_logic_evidence_candidates, verify_logic_with_llm
from model_answer_router import find_model_answer_reference

TOPIC = 'control_valve_positioner_ip_converter_booster_accessories_calibration'
TOPIC_1 = 'control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe'
TOPIC_2 = 'control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening'
TOPIC_3 = 'control_valve_deadband_stiction_response_time_positioner_dynamic_performance'
TOPIC_4 = 'control_valve_types_globe_rotary_body_actuator_selection'
TOPIC_5 = 'control_valve_authority_rangeability_gain_installed_performance'
TOPIC_6 = 'control_valve_sizing_cv_kv_reynolds_liquid_selection'
TOPIC_7 = 'control_valve_gas_sizing_choked_flow_critical_pressure_ratio'
TOPIC_8 = 'control_valve_cavitation_flashing_choked_flow_damage_prevention'
TOPIC_9 = 'control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim'
TOPIC_10 = 'balanced_trim_unbalanced_trim_structure_sealing_applications'

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['control_valve_positioner_accessory_scope', 'command_ip_positioner_actuator_feedback_chain', 'positioner_travel_feedback_controller', 'position_error_negative_feedback', 'pneumatic_positioner_force_balance_mechanism', 'electropneumatic_positioner_separate_ip_boundary', 'ip_converter_current_pressure_transduction', 'normalized_current_command', 'ip_linear_pressure_mapping', 'conventional_4_20ma_3_15psi_endpoints', 'ip_supply_air_dependency', 'positioner_direct_reverse_action', 'actuator_action_fail_action_separation', 'travel_feedback_linkage_cam_alignment', 'positioner_zero_span_travel_calibration', 'multipoint_upstroke_downstroke_verification', 'split_range_local_mapping', 'volume_booster_flow_capacity_function', 'booster_pressure_follower_boundary', 'booster_bypass_hunting_topic3_handoff', 'filter_regulator_supply_conditioning', 'lockup_relay_supply_failure_holding', 'quick_exhaust_rapid_vent_function', 'solenoid_on_off_pneumatic_switching', 'volume_tank_energy_storage_response_tradeoff', 'tubing_output_capacity_pressure_drop', 'bench_set_calibration_boundary', 'seat_endpoint_overtravel_mechanical_stop', 'command_pressure_travel_loop_test', 'hysteresis_deadband_stiction_topic3_handoff', 'air_quality_leakage_nozzle_restriction_failure', 'loss_signal_air_power_failure_response', 'operating_pressure_case_calibration_validity', 'maintenance_bypass_manual_operation_boundary', 'as_found_as_left_traceability', 'vendor_action_cam_relay_setting_crosscheck', 'smart_diagnostics_topic12_handoff', 'sis_esd_pst_topic15_handoff', 'package_workflow_topic16_handoff', 'final_signal_pressure_travel_fail_action_verification']
EXPECTED_FATAL_IDS = ['control_valve_positioner_equals_ip_converter', 'control_valve_ip_converter_measures_valve_travel', 'control_valve_positioner_open_loop_device', 'control_valve_positive_feedback_required', 'control_valve_direct_action_equals_fail_open', 'control_valve_reverse_action_equals_fail_close', 'control_valve_4ma_equals_zero_psi_conventional', 'control_valve_20ma_equals_twenty_psi_conventional', 'control_valve_booster_steady_pressure_amplifier', 'control_valve_booster_eliminates_all_hunting', 'control_valve_quick_exhaust_equals_volume_booster', 'control_valve_lockup_always_drives_fail_close', 'control_valve_solenoid_alone_determines_fail_action', 'control_valve_filter_regulator_increases_supply_pressure', 'control_valve_volume_tank_no_dynamic_effect', 'control_valve_bench_set_equals_positioner_calibration', 'control_valve_single_endpoint_calibration_sufficient', 'control_valve_upstroke_only_calibration_sufficient', 'control_valve_split_range_uses_global_full_range_mapping', 'control_valve_positioner_eliminates_all_stiction', 'control_valve_supply_loss_response_irrelevant', 'control_valve_universal_accessory_setting']
EXPECTED_MAJOR_IDS = ['control_valve_fixed_positioner_gain', 'control_valve_fixed_booster_bypass_opening', 'control_valve_fixed_stroke_time', 'control_valve_fixed_calibration_tolerance', 'control_valve_fixed_lockup_trip_pressure', 'control_valve_fixed_filter_grade', 'control_valve_fixed_solenoid_port_logic', 'control_valve_fixed_split_range_overlap', 'control_valve_fixed_tubing_size', 'control_valve_vendor_setting_without_manual_basis']

BROAD_ALIASES = {
    "positioner", "i/p", "ip", "booster", "accessory",
    "calibration", "signal", "pressure", "travel", "solenoid", "air",
}

POSITIVE_ANSWER = """
Command→I/P→positioner→actuator→travel feedback signal chain을 먼저 제시한다.
Positioner는 command와 actual travel을 비교하는 travel feedback controller이며
position error는 e=r-y이다. Output은 negative feedback 방향으로 error를 줄인다.
I/P converter는 current-to-pressure transducer이다. 4–20 mA와 3–15 psi에서
x=(I-Imin)/(Imax-Imin), P=Pmin+x(Pmax-Pmin)을 사용한다. 4·12·20 mA는
3·9·15 psi에 대응한다. Direct action과 reverse action을 actuator action,
spring action 및 fail action과 분리한다. Feedback linkage와 cam alignment를
확인한다. Zero span calibration 후 0·25·50·75·100% upstroke와 downstroke를
검증한다. Split-range는 own local current range로 normalization한다.
Volume booster는 pilot pressure follower이며 flow capacity를 높이고 steady-state
pressure amplifier가 아니다. Filter regulator, lock-up relay, quick-exhaust valve,
solenoid valve와 volume tank의 기능을 구분한다. Bench set과 positioner calibration을
구분한다. Loss of signal, loss of air와 loss of power를 시험한다. As-found와
as-left를 기록하고 vendor manual을 확인한다. Topic 1, Topic 3, Topic 4,
Topic 10, Topic 12, Topic 15와 Topic 16의 경계를 유지한다.
""".strip()

SAFE_ANSWER = """
Positioner는 command와 actual travel을 비교하는 local feedback controller이다.
I/P converter는 current-to-pressure transducer이다. Volume booster는 pilot
pressure follower이며 fill·vent flow capacity를 높인다. Direct·reverse action과
fail action을 구분하고 zero·span 및 upstroke·downstroke를 검증한다.
""".strip()

NEGATIVE_SAMPLES = {
    "control_valve_positioner_equals_ip_converter": (
        "travel feedback controller, command actual travel, local position loop, "
        "current to pressure, I/P 변환기와 포지셔너를 설명하지만 Positioner와 "
        "I/P converter는 같은 기능의 장치라고 주장한다."
    ),
    "control_valve_positive_feedback_required": (
        "position error, e equals r minus y, negative feedback, feedback polarity, "
        "error reduction을 설명하지만 positioner는 positive feedback가 필요하다고 주장한다."
    ),
    "control_valve_direct_action_equals_fail_open": (
        "direct reverse action, command increase, positioner action, actuator action "
        "fail action, fail open close를 설명하지만 direct action은 항상 fail-open이라고 주장한다."
    ),
    "control_valve_booster_steady_pressure_amplifier": (
        "volume booster, booster pressure follower, pilot pressure, not pressure "
        "amplifier, flow capacity를 설명하지만 booster는 steady-state pressure를 "
        "일정 비율로 증폭한다고 주장한다."
    ),
    "control_valve_bench_set_equals_positioner_calibration": (
        "bench set, spring range, positioner calibration, command travel relation, "
        "actuator adjustment를 설명하지만 bench set과 calibration은 같은 작업이라고 주장한다."
    ),
    "control_valve_single_endpoint_calibration_sufficient": (
        "zero span calibration, lower upper endpoint, iterative calibration, "
        "intermediate travel, positioner adjustment를 설명하지만 한 endpoint만 "
        "맞추면 calibration이 완료된다고 주장한다."
    ),
}

SEMANTIC_CLUSTERS = {
    "signal_chain": ("command→i/p→positioner→actuator→travel feedback", "travel feedback controller"),
    "feedback": ("e=r-y", "negative feedback"),
    "ip_mapping": ("current-to-pressure transducer", "4–20 ma", "3–15 psi", "3·9·15 psi"),
    "action": ("direct action", "reverse action", "fail action"),
    "calibration": ("zero span calibration", "0·25·50·75·100%", "upstroke", "downstroke"),
    "split_range": ("split-range", "local current range"),
    "booster": ("volume booster", "pilot pressure follower", "flow capacity", "pressure amplifier가 아니다"),
    "accessories": ("filter regulator", "lock-up relay", "quick-exhaust valve", "solenoid valve", "volume tank"),
    "records": ("as-found", "as-left", "vendor manual"),
    "handoffs": ("topic 1", "topic 3", "topic 4", "topic 10", "topic 12", "topic 15", "topic 16"),
}

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def target_entry(filename: str, list_key: str) -> dict[str, Any]:
    rows = load_json(GENERATED_DIR / filename).get(list_key, [])
    matches = [row for row in rows if isinstance(row, dict) and row.get("topic_id") == TOPIC]
    if len(matches) != 1:
        raise AssertionError(f"{filename} target count={len(matches)}")
    return matches[0]

def selected_topic(result: dict[str, Any]) -> str | None:
    primary = result.get("primary_reference") or {}
    return primary.get("topic_id") if isinstance(primary, dict) else None

def normalize_current(current: float, minimum: float, maximum: float) -> float:
    if maximum <= minimum:
        raise ValueError
    return (current - minimum) / (maximum - minimum)

def map_pressure(current: float, i_min: float, i_max: float, p_min: float, p_max: float) -> float:
    if p_max <= p_min:
        raise ValueError
    return p_min + normalize_current(current, i_min, i_max) * (p_max - p_min)

def inverse_current(pressure: float, i_min: float, i_max: float, p_min: float, p_max: float) -> float:
    if i_max <= i_min or p_max <= p_min:
        raise ValueError
    x = (pressure - p_min) / (p_max - p_min)
    return i_min + x * (i_max - i_min)

def direct_output(x: float) -> float:
    return x

def reverse_output(x: float) -> float:
    return 1.0 - x

def position_error(reference: float, actual: float) -> float:
    return reference - actual

def corrected_actual(reference: float, actual: float, gain: float) -> float:
    if not 0.0 < gain <= 1.0:
        raise ValueError
    return actual + gain * position_error(reference, actual)

def full_span_error(measured: float, command: float, y_min: float, y_max: float) -> float:
    if y_max <= y_min:
        raise ValueError
    return 100.0 * (measured - command) / (y_max - y_min)

def hysteresis(upstroke: float, downstroke: float) -> tuple[float, float]:
    signed = upstroke - downstroke
    return signed, abs(signed)

def booster_output_pressure(pilot_pressure: float, offset: float = 0.0) -> float:
    if pilot_pressure < 0:
        raise ValueError
    return pilot_pressure + offset

def cluster_coverage(text: str) -> dict[str, bool]:
    normalized = " ".join(text.casefold().split())
    return {
        group: all(" ".join(marker.casefold().split()) in normalized for marker in markers)
        for group, markers in SEMANTIC_CLUSTERS.items()
    }

def matched_profile_key_terms(text: str, profile: dict[str, Any]) -> list[str]:
    normalized = " ".join(text.casefold().split())
    terms = (profile.get("candidate_extraction") or {}).get("key_terms") or []
    return [
        str(term)
        for term in terms
        if " ".join(str(term).casefold().split()) in normalized
    ]

class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.importance = load_json(SOURCE_DIR / "topic_importance.json")
        cls.gfact = target_entry("fact_anchors.generated.json", "topics")
        cls.profile = target_entry("logic_check_profiles.generated.json", "profiles")
        cls.glogic = target_entry("logic_checks.generated.json", "topic_logic_checks")
        cls.gmodel = target_entry("model_answers.generated.json", "answers")
        cls.gimportance = target_entry("topic_importance.generated.json", "topics")
        cls.manifest = target_entry("topic_pack_manifest.generated.json", "topics")

    def test_source_generated_and_dynamic_manifest_alignment(self) -> None:
        for row in (self.fact, self.logic, self.model, self.importance, self.gfact, self.profile,
                    self.glogic, self.gmodel, self.gimportance, self.manifest):
            self.assertEqual(row["topic_id"], TOPIC)
        source_ids = sorted(
            path.name for path in (ROOT / "rubrics" / "topic_packs").iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        manifest_ids = [
            row["topic_id"]
            for row in load_json(GENERATED_DIR / "topic_pack_manifest.generated.json")["topics"]
        ]
        self.assertEqual(manifest_ids, source_ids)
        self.assertEqual(manifest_ids.count(TOPIC), 1)

    def test_exact_anchor_fatal_major_contract(self) -> None:
        self.assertEqual([row["id"] for row in self.fact["anchors"]], EXPECTED_ANCHOR_IDS)
        self.assertEqual([row["id"] for row in self.gfact["anchors"]], EXPECTED_ANCHOR_IDS)
        self.assertEqual([row["id"] for row in self.fact["fatal_wrong_claims"]], EXPECTED_FATAL_IDS)
        self.assertEqual([row["id"] for row in self.profile["major_checks"]], EXPECTED_MAJOR_IDS)
        self.assertEqual(len(self.profile["fatal_conditions"]), 22)

    def test_semantic_score_and_deterministic_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(self.glogic["fatal_checks"], [])
        self.assertEqual(self.glogic["major_checks"], [])
        self.assertEqual(self.profile["candidate_extraction"]["rules"], [])
        policy = self.profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")
        self.assertEqual(policy["affected_layers"], ["C"])
        self.assertEqual(self.profile["output_contract"]["excluded_score_layers"], ["D", "E"])

    def test_patterns_outline_aliases_and_importance(self) -> None:
        patterns = self.model["expected_question_patterns"]
        outlines = self.model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        pattern_anchor_set = set().union(
            *(
                set(row["required_anchor_ids"])
                for row in patterns
            )
        )
        outline_anchor_set = set().union(
            *(
                set(row["anchor_refs"])
                for row in outlines
            )
        )
        self.assertTrue(pattern_anchor_set <= anchor_set)
        self.assertTrue(outline_anchor_set <= anchor_set)
        sequence_anchor_set = {
            "bench_set_calibration_boundary",
            "actuator_action_fail_action_separation",
            "travel_feedback_linkage_cam_alignment",
            "positioner_direct_reverse_action",
            "positioner_zero_span_travel_calibration",
            "multipoint_upstroke_downstroke_verification",
            "seat_endpoint_overtravel_mechanical_stop",
            "command_pressure_travel_loop_test",
            "loss_signal_air_power_failure_response",
            "as_found_as_left_traceability",
            "vendor_action_cam_relay_setting_crosscheck",
        }
        self.assertTrue(
            sequence_anchor_set <= pattern_anchor_set
        )
        aliases = {str(alias).casefold() for alias in self.model["routing_aliases"]}
        self.assertFalse(BROAD_ALIASES & aliases)
        self.assertEqual(self.gmodel["topic_aliases"], self.model["routing_aliases"])
        self.assertEqual(self.gmodel["routing_aliases"], self.model["routing_aliases"])
        self.assertEqual(self.gimportance, self.importance)
        self.assertEqual(self.importance["difficulty"], "FIELD_APPLICATION")
        self.assertEqual(self.importance["question_type"], "PRINCIPLE_INTERPRETATION")

    def test_signal_chain_and_feedback_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("Command→I/P→positioner→actuator→travel feedback",
                      by_id["command_ip_positioner_actuator_feedback_chain"])
        self.assertIn("feedback controller", by_id["positioner_travel_feedback_controller"])
        self.assertIn("e=r-y", by_id["position_error_negative_feedback"])
        self.assertIn("negative-feedback", by_id["position_error_negative_feedback"])

    def test_current_pressure_mapping_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("current-to-pressure transducer",
                      by_id["ip_converter_current_pressure_transduction"])
        self.assertIn("x=(I-Imin)/(Imax-Imin)", by_id["normalized_current_command"])
        self.assertIn("Pcmd=Pmin+x(Pmax-Pmin)", by_id["ip_linear_pressure_mapping"])
        self.assertIn("3·9·15 psi", by_id["conventional_4_20ma_3_15psi_endpoints"])

    def test_action_and_calibration_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("Direct·reverse", by_id["positioner_direct_reverse_action"])
        self.assertIn("valve fail action", by_id["actuator_action_fail_action_separation"])
        self.assertIn("0·25·50·75·100%", by_id["multipoint_upstroke_downstroke_verification"])
        self.assertIn("local current range", by_id["split_range_local_mapping"])

    def test_booster_and_accessory_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("flow capacity", by_id["volume_booster_flow_capacity_function"])
        self.assertIn("pilot pressure follower", by_id["booster_pressure_follower_boundary"])
        self.assertIn("pressure amplifier가 아니다", by_id["booster_pressure_follower_boundary"])
        self.assertIn("pressure를 hold", by_id["lockup_relay_supply_failure_holding"])
        self.assertIn("빠르게 vent", by_id["quick_exhaust_rapid_vent_function"])

    def test_failure_records_and_vendor_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("Loss of signal·instrument air·electrical power",
                      by_id["loss_signal_air_power_failure_response"])
        self.assertIn("As-found·as-left", by_id["as_found_as_left_traceability"])
        self.assertIn("Vendor manual", by_id["vendor_action_cam_relay_setting_crosscheck"])

    def test_explicit_topic_handoff_boundaries(self) -> None:
        combined = json.dumps(
            {"fact": self.fact, "logic": self.logic, "model": self.model},
            ensure_ascii=False,
        ) + TOPIC_SHEET.read_text(encoding="utf-8")
        for marker in ("Topic 1", "Topic 3", "Topic 4", "Topic 10", "Topic 12", "Topic 15", "Topic 16"):
            self.assertIn(marker, combined)

    def test_section_aware_fatal_corrections(self) -> None:
        by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        checks = {
            "control_valve_positioner_equals_ip_converter": "travel-feedback controller",
            "control_valve_positive_feedback_required": "negative-feedback",
            "control_valve_direct_action_equals_fail_open": "독립적으로 확인",
            "control_valve_4ma_equals_zero_psi_conventional": "4 mA→3 psi",
            "control_valve_booster_steady_pressure_amplifier": "fill·vent flow capacity",
            "control_valve_quick_exhaust_equals_volume_booster": "rapid vent",
            "control_valve_bench_set_equals_positioner_calibration": "spring-force range",
            "control_valve_upstroke_only_calibration_sufficient": "Upstroke와 downstroke",
            "control_valve_split_range_uses_global_full_range_mapping": "own local Imin·Imax",
            "control_valve_universal_accessory_setting": "actuator volume",
        }
        for rule_id, marker in checks.items():
            correction = str(by_id[rule_id].get("correction") or by_id[rule_id].get("correct_rule") or "")
            self.assertIn(marker, correction)

class RouterRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(GENERATED_DIR / "model_answers.generated.json")
        cls.answer_by_topic = {row["topic_id"]: row for row in cls.bank["answers"]}
        for topic_id in (TOPIC, TOPIC_1, TOPIC_2, TOPIC_3, TOPIC_4, TOPIC_5,
                         TOPIC_6, TOPIC_7, TOPIC_8, TOPIC_9, TOPIC_10):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(f"missing topic {topic_id}")

    @classmethod
    def qtype(cls, topic_id: str) -> dict[str, Any]:
        return {"primary_type": {"id": cls.answer_by_topic[topic_id]["question_type"], "confidence": "high"}}

    @staticmethod
    def fact_eval(topic_id: str) -> dict[str, Any]:
        return {"topic_id": topic_id, "matched": True, "confidence": "high"}

    @classmethod
    def route(cls, question: str, topic_id: str, answer_text: str = "") -> dict[str, Any]:
        return find_model_answer_reference(
            question_text=question,
            answer_text=answer_text,
            fact_eval=cls.fact_eval(topic_id),
            question_type_eval=cls.qtype(topic_id),
            bank=cls.bank,
        )

    def assert_primary(self, result: dict[str, Any], expected: str) -> None:
        self.assertTrue(result.get("matched"), msg=result)
        self.assertEqual(selected_topic(result), expected, msg=result)

    def test_signal_chain_route(self) -> None:
        self.assert_primary(self.route(
            "Command→I/P→positioner→actuator→travel feedback signal chain과 negative feedback를 설명하시오.", TOPIC), TOPIC)

    def test_pneumatic_positioner_route(self) -> None:
        self.assert_primary(self.route(
            "Nozzle-flapper, force balance, range spring과 pneumatic relay를 이용한 positioner 원리를 설명하시오.", TOPIC), TOPIC)

    def test_ip_mapping_route(self) -> None:
        self.assert_primary(self.route(
            "I/P converter의 4–20 mA·3–15 psi mapping과 supply-air dependency를 설명하시오.", TOPIC), TOPIC)

    def test_action_chain_route(self) -> None:
        self.assert_primary(self.route(
            "Positioner direct·reverse action, actuator air action과 fail-open·fail-close를 구분하시오.", TOPIC), TOPIC)

    def test_zero_span_multipoint_route(self) -> None:
        self.assert_primary(self.route(
            "Positioner zero·span, feedback linkage와 0·25·50·75·100% upstroke·downstroke 교정 절차를 설명하시오.", TOPIC), TOPIC)

    def test_split_range_route(self) -> None:
        self.assert_primary(self.route(
            "Split-range segment local current mapping, gap·overlap과 action을 설명하시오.", TOPIC), TOPIC)

    def test_volume_booster_route(self) -> None:
        self.assert_primary(self.route(
            "Volume booster의 pilot-pressure following, fill·vent flow capacity와 bypass tradeoff를 설명하시오.", TOPIC), TOPIC)

    def test_pneumatic_accessory_route(self) -> None:
        self.assert_primary(self.route(
            "Filter regulator, lock-up relay, quick-exhaust, solenoid valve와 volume tank의 기능을 비교하시오.", TOPIC), TOPIC)

    def test_failure_chain_route(self) -> None:
        self.assert_primary(self.route(
            "Loss of signal·air·power와 I/P·positioner·booster·accessory failure를 signal chain으로 진단하시오.", TOPIC), TOPIC)

    def test_integrated_loop_test_route(self) -> None:
        self.assert_primary(self.route(
            "DCS command, loop current, I/P pressure, positioner output, actual travel, fail action과 as-found·as-left를 통합 검증하시오.",
            TOPIC), TOPIC)

    def test_topic1_actuator_force_boundary(self) -> None:
        self.assert_primary(self.route(
            "Worst-case unbalanced force, packing friction, seat load와 fail-safe spring으로 actuator thrust를 산정하시오.", TOPIC_1), TOPIC_1)

    def test_topic3_dynamic_boundary(self) -> None:
        self.assert_primary(self.route(
            "Deadband, stiction, response time, hunting과 booster bypass tuning을 진단하시오.", TOPIC_3), TOPIC_3)

    def test_topic4_actuator_type_boundary(self) -> None:
        self.assert_primary(self.route(
            "Pneumatic·electric·hydraulic actuator type과 globe·rotary body 구조를 비교 선정하시오.", TOPIC_4), TOPIC_4)

    def test_topic5_installed_performance_boundary(self) -> None:
        self.assert_primary(self.route(
            "Valve authority, installed characteristic, rangeability와 installed gain을 설명하시오.", TOPIC_5), TOPIC_5)

    def test_topic9_noise_boundary(self) -> None:
        self.assert_primary(self.route(
            "Aerodynamic·hydrodynamic noise, low-noise trim과 pipe transmission loss를 설명하시오.", TOPIC_9), TOPIC_9)

    def test_topic10_trim_friction_boundary(self) -> None:
        self.assert_primary(self.route(
            "Balanced·unbalanced trim, residual force, balance seal friction과 internal leakage를 비교하시오.", TOPIC_10), TOPIC_10)

    def test_question_only_routing_survives_answer_contamination(self) -> None:
        result = self.route(
            "Deadband, stiction, hysteresis와 hunting을 진단하고 booster bypass를 조정하시오.",
            TOPIC_3,
            answer_text="4–20 mA 3–15 psi I/P mapping, positioner zero span, lock-up relay와 volume tank를 상세히 서술한다.",
        )
        self.assert_primary(result, TOPIC_3)
        aliases = {str(alias).casefold() for alias in self.answer_by_topic[TOPIC]["routing_aliases"]}
        self.assertFalse(BROAD_ALIASES & aliases)

class PositionerAccessorySemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry("logic_check_profiles.generated.json", "profiles")
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_current_normalization_endpoints_and_domain(self) -> None:
        self.assertEqual(normalize_current(4.0, 4.0, 20.0), 0.0)
        self.assertEqual(normalize_current(12.0, 4.0, 20.0), 0.5)
        self.assertEqual(normalize_current(20.0, 4.0, 20.0), 1.0)
        with self.assertRaises(ValueError):
            normalize_current(4.0, 4.0, 4.0)

    def test_ip_pressure_mapping_endpoints_and_monotonicity(self) -> None:
        values = [map_pressure(current, 4.0, 20.0, 3.0, 15.0) for current in (4.0, 12.0, 20.0)]
        self.assertEqual(values, [3.0, 9.0, 15.0])
        self.assertLess(values[0], values[1])
        self.assertLess(values[1], values[2])
        with self.assertRaises(ValueError):
            map_pressure(12.0, 4.0, 20.0, 3.0, 3.0)

    def test_inverse_pressure_to_current_mapping(self) -> None:
        for current in (4.0, 8.0, 12.0, 16.0, 20.0):
            pressure = map_pressure(current, 4.0, 20.0, 3.0, 15.0)
            self.assertTrue(math.isclose(inverse_current(pressure, 4.0, 20.0, 3.0, 15.0), current))
        with self.assertRaises(ValueError):
            inverse_current(9.0, 4.0, 20.0, 3.0, 3.0)

    def test_direct_and_reverse_action_mapping(self) -> None:
        for x in (0.0, 0.25, 0.5, 0.75, 1.0):
            self.assertEqual(direct_output(x), x)
            self.assertEqual(reverse_output(x), 1.0 - x)
            self.assertEqual(direct_output(x) + reverse_output(x), 1.0)

    def test_negative_feedback_reduces_position_error(self) -> None:
        reference, actual = 0.8, 0.2
        initial = abs(position_error(reference, actual))
        updated = corrected_actual(reference, actual, 0.5)
        self.assertLess(abs(position_error(reference, updated)), initial)
        self.assertGreater(position_error(reference, actual), 0.0)
        self.assertLess(position_error(0.2, 0.8), 0.0)
        with self.assertRaises(ValueError):
            corrected_actual(reference, actual, 0.0)

    def test_split_range_local_normalization(self) -> None:
        self.assertEqual(normalize_current(4.0, 4.0, 12.0), 0.0)
        self.assertEqual(normalize_current(12.0, 4.0, 12.0), 1.0)
        self.assertEqual(normalize_current(12.0, 12.0, 20.0), 0.0)
        self.assertEqual(normalize_current(20.0, 12.0, 20.0), 1.0)

    def test_full_span_calibration_error(self) -> None:
        self.assertEqual(full_span_error(51.0, 50.0, 0.0, 100.0), 1.0)
        self.assertEqual(full_span_error(49.0, 50.0, 0.0, 100.0), -1.0)
        with self.assertRaises(ValueError):
            full_span_error(50.0, 50.0, 100.0, 100.0)

    def test_up_down_hysteresis_difference(self) -> None:
        self.assertEqual(hysteresis(51.0, 49.0), (2.0, 2.0))
        self.assertEqual(hysteresis(49.0, 51.0), (-2.0, 2.0))

    def test_booster_pressure_follower_not_gain_device(self) -> None:
        self.assertEqual(booster_output_pressure(10.0), 10.0)
        self.assertEqual(booster_output_pressure(10.0, 0.2), 10.2)
        self.assertNotEqual(booster_output_pressure(10.0), 20.0)
        with self.assertRaises(ValueError):
            booster_output_pressure(-1.0)

    def test_positive_sample_semantic_cluster_coverage(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(SEMANTIC_CLUSTERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_contextual_negative_candidate_extraction(self) -> None:
        fatal_set = {row["id"] for row in self.fact["fatal_wrong_claims"]}
        self.assertTrue(set(NEGATIVE_SAMPLES) <= fatal_set)
        for rule_id, answer_text in NEGATIVE_SAMPLES.items():
            with self.subTest(rule_id=rule_id):
                matched = matched_profile_key_terms(answer_text, self.profile)
                self.assertGreaterEqual(len(matched), 3, msg={"rule_id": rule_id, "matched": matched})
                candidates = extract_logic_evidence_candidates(answer_text, self.profile)
                self.assertTrue(candidates, msg={"rule_id": rule_id, "matched": matched})

    def test_mocked_fatal_and_safe_verifier_contracts(self) -> None:
        rule_id = "control_valve_booster_steady_pressure_amplifier"
        answer_text = NEGATIVE_SAMPLES[rule_id]
        candidates = extract_logic_evidence_candidates(answer_text, self.profile)
        self.assertTrue(candidates)
        mocked_fatal = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": "Volume booster를 steady-state pressure amplifier로 잘못 설명하였다.",
            "findings": [{
                "candidate_id": candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message": "Universal pressure-gain claim",
                "correct_rule": "Booster는 pilot pressure를 추종하면서 fill·vent flow capacity를 높이는 장치이다.",
            }],
        }
        with patch("logic_llm_verifier._call_ollama_json", return_value=mocked_fatal):
            fatal_result = verify_logic_with_llm(answer_text, TOPIC)
        self.assertTrue(fatal_result["fatal_error_detected"], msg=fatal_result)
        self.assertEqual(fatal_result["mode"], "fatal")
        self.assertEqual(fatal_result["findings"][0]["affected_layers"], ["C"])
        self.assertEqual(fatal_result["recommended_ceiling"], 10.0)

        safe_candidates = extract_logic_evidence_candidates(SAFE_ANSWER, self.profile)
        self.assertTrue(safe_candidates)
        mocked_safe = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "Positioner·I/P·booster 기능과 action·calibration 경계를 정확히 구분하였다.",
            "findings": [],
        }
        with patch("logic_llm_verifier._call_ollama_json", return_value=mocked_safe):
            safe_result = verify_logic_with_llm(SAFE_ANSWER, TOPIC)
        self.assertFalse(safe_result["fatal_error_detected"], msg=safe_result)
        self.assertEqual(safe_result["mode"], "pass")
        self.assertIsNone(safe_result["recommended_ceiling"])
        self.assertEqual(safe_result["findings"], [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
