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

from logic_llm_verifier import (
    extract_logic_evidence_candidates,
    verify_logic_with_llm,
)
from model_answer_router import find_model_answer_reference

TOPIC = 'smart_positioner_diagnostics_valve_signature_predictive_maintenance'
TOPIC_1 = "control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe"
TOPIC_2 = "control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening"
TOPIC_3 = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
TOPIC_4 = "control_valve_types_globe_rotary_body_actuator_selection"
TOPIC_5 = "control_valve_authority_rangeability_gain_installed_performance"
TOPIC_6 = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
TOPIC_7 = "control_valve_gas_sizing_choked_flow_critical_pressure_ratio"
TOPIC_8 = "control_valve_cavitation_flashing_choked_flow_damage_prevention"
TOPIC_9 = "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim"
TOPIC_10 = "balanced_trim_unbalanced_trim_structure_sealing_applications"
TOPIC_11 = "control_valve_positioner_ip_converter_booster_accessories_calibration"

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['smart_positioner_diagnostic_scope', 'diagnostic_signal_data_chain', 'online_monitoring_offline_test_boundary', 'static_dynamic_signature_boundary', 'device_status_event_configuration_history', 'data_quality_time_sync_units', 'vendor_variable_dictionary_verification', 'as_left_reference_signature', 'comparable_context_baseline', 'command_travel_error_signed', 'full_span_travel_error', 'up_down_hysteresis_signature', 'actuator_pressure_open_close_band', 'pressure_band_friction_proxy', 'process_force_confounding', 'supply_pressure_regulator_droop', 'ip_zero_span_drift_trend', 'relay_pilot_fill_vent_health', 'pneumatic_air_consumption_leakage', 'feedback_sensor_drift_noise_dropout', 'cycle_count_definition', 'accumulated_travel_direction_reversal', 'stroke_time_response_trend', 'endpoint_seat_contact_mechanical_stop', 'packing_stem_shaft_resistance_trend', 'trim_balance_seal_friction_handoff', 'baseline_residual_context', 'percent_change_domain', 'rate_of_change_time_domain', 'threshold_persistence_deadband', 'multi_evidence_failure_isolation', 'diagnostic_confidence_data_quality', 'false_positive_negative_context', 'detection_confirmation_boundary', 'detect_verify_diagnose_priority_workflow', 'time_condition_predictive_maintenance_compare', 'degradation_trend_lead_time', 'maintenance_priority_consequence', 'hart_fieldbus_asset_integration', 'offline_test_process_risk', 'as_found_as_left_work_order_feedback', 'topic1_topic3_topic11_boundary', 'topic13_topic15_topic16_boundary', 'final_closed_loop_diagnostic_verification']
EXPECTED_FATAL_IDS = ['smart_diagnostic_guarantees_root_cause', 'valve_signature_alone_proves_seat_leakage', 'static_dynamic_signature_identical', 'baseline_context_irrelevant', 'travel_error_sign_can_change', 'ip_drift_is_only_zero_span', 'pressure_band_equals_friction_universally', 'pressure_signature_ignores_process_force', 'air_consumption_alone_proves_leakage', 'stroke_time_alone_proves_stiction', 'cycle_count_universal_definition', 'accumulated_travel_without_sampling_basis', 'single_threshold_is_sufficient', 'universal_health_index_weights', 'alarm_requires_immediate_repair', 'data_quality_flag_unnecessary', 'offline_signature_always_safe', 'predictive_maintenance_exact_failure_date', 'correlation_proves_causation', 'pst_data_automatic_proof_test_credit', 'friction_source_uniquely_identifiable', 'smart_positioner_replaces_inspection', 'as_left_only_record_sufficient', 'hart_fieldbus_is_realtime_unlimited']
EXPECTED_MAJOR_IDS = ['fixed_travel_error_threshold', 'fixed_pressure_band_threshold', 'fixed_air_leakage_threshold', 'fixed_stroke_time_threshold', 'fixed_alarm_persistence', 'fixed_health_index_weights', 'fixed_degradation_window', 'fixed_rul_lead_time', 'fixed_sampling_update_rate', 'fixed_offline_test_interval', 'fixed_maintenance_priority', 'fixed_data_quality_acceptance']

BROAD_ALIASES = {
    "smart",
    "diagnostic",
    "signature",
    "trend",
    "alarm",
    "health",
    "maintenance",
    "hart",
    "positioner",
    "valve",
}

NEGATIVE_RULE_IDS = (
    "valve_signature_alone_proves_seat_leakage",
    "pressure_band_equals_friction_universally",
    "cycle_count_universal_definition",
    "offline_signature_always_safe",
    "pst_data_automatic_proof_test_credit",
    "hart_fieldbus_is_realtime_unlimited",
)

SEMANTIC_CLUSTERS = {
    "architecture": (
        "smart positioner diagnostic data chain",
        "actual travel",
        "actuator pressure",
        "device status",
    ),
    "signature": (
        "online monitoring",
        "offline diagnostic test",
        "static valve signature",
        "dynamic operating signature",
        "as-left reference signature",
    ),
    "features": (
        "travel error",
        "hysteresis",
        "pressure band",
        "friction proxy",
        "process ΔP",
    ),
    "pneumatic_sensor": (
        "supply regulator",
        "I/P",
        "relay",
        "air consumption",
        "feedback sensor",
    ),
    "usage_trend": (
        "cycle count",
        "accumulated travel",
        "stroke time",
        "baseline residual",
        "rate of change",
    ),
    "alarm_quality": (
        "persistence",
        "deadband",
        "diagnostic confidence",
        "data quality",
        "multi-evidence",
    ),
    "maintenance": (
        "time-based",
        "condition-based",
        "predictive maintenance",
        "actionable lead time",
    ),
    "workflow": (
        "detect verify diagnose prioritize plan repair as-left",
        "HART",
        "Fieldbus",
        "work-order feedback",
    ),
}

POSITIVE_ANSWER = """
Smart positioner diagnostic data chain은 command, actual travel, supply pressure,
actuator pressure와 device status를 timestamp와 data quality로 연결한다.
Online monitoring과 offline diagnostic test를 분리하고 static valve signature,
dynamic operating signature와 as-left reference signature를 동일 operating context에서 비교한다.
Travel error, hysteresis, opening-closing pressure band와 conditional friction proxy를
process ΔP와 함께 해석한다. Supply regulator, I/P, relay, air consumption과
feedback sensor의 drift·noise·dropout을 구분한다. Cycle count, accumulated travel,
stroke time, baseline residual, percentage change와 rate of change를 추적한다.
Alarm은 persistence, deadband, diagnostic confidence, data quality와 multi-evidence를 사용한다.
Time-based, condition-based와 predictive maintenance를 비교하고 actionable lead time을 제시한다.
Detect verify diagnose prioritize plan repair as-left workflow를 HART, Fieldbus,
asset management와 work-order feedback으로 폐루프 검증한다.
"""

SAFE_ANSWER = """
Smart-positioner alarm은 root-cause 후보이다. Comparable as-left baseline과 operating
context를 확인한 뒤 travel, pressure, supply, air usage, timing, status와 data quality를
multi-evidence로 검토한다. Physical inspection과 functional test로 원인을 확인한다.
Predictive maintenance는 degradation trend와 lead time을 제공하지만 exact failure date를
보장하지 않는다. Repair 후 as-left signature와 work-order result를 기록한다.
"""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def target_entry(filename: str, list_key: str) -> dict[str, Any]:
    rows = load_json(GENERATED_DIR / filename).get(list_key, [])
    matches = [
        row
        for row in rows
        if isinstance(row, dict) and row.get("topic_id") == TOPIC
    ]
    if len(matches) != 1:
        raise AssertionError(f"{filename} target count={len(matches)}")
    return matches[0]


def selected_topic(result: dict[str, Any]) -> str | None:
    primary = result.get("primary_reference") or {}
    return primary.get("topic_id") if isinstance(primary, dict) else None


def route_reference(
    question: str,
    topic_id: str,
    answer_text: str = "",
) -> dict[str, Any]:
    bank = load_json(GENERATED_DIR / "model_answers.generated.json")
    answer_by_topic = {
        row["topic_id"]: row
        for row in bank["answers"]
    }
    qtype = {
        "primary_type": {
            "id": answer_by_topic[topic_id]["question_type"],
            "confidence": "high",
        }
    }
    fact_eval = {
        "topic_id": topic_id,
        "matched": True,
        "confidence": "high",
    }
    return find_model_answer_reference(
        question_text=question,
        answer_text=answer_text,
        fact_eval=fact_eval,
        question_type_eval=qtype,
        bank=bank,
    )


def travel_error(command: float, measured: float) -> float:
    return command - measured


def full_span_error(
    command: float,
    measured: float,
    minimum: float,
    maximum: float,
) -> float:
    if maximum <= minimum:
        raise ValueError
    return 100.0 * (command - measured) / (maximum - minimum)


def hysteresis(upstroke: float, downstroke: float) -> float:
    return abs(upstroke - downstroke)


def pressure_band(opening: float, closing: float) -> float:
    return abs(opening - closing)


def friction_proxy(effective_area: float, band: float) -> float:
    if effective_area <= 0.0 or band < 0.0:
        raise ValueError
    return effective_area * band / 2.0


def baseline_residual(current: float, baseline: float) -> float:
    return current - baseline


def percent_change(current: float, baseline: float) -> float:
    if baseline == 0.0:
        raise ValueError
    return 100.0 * (current - baseline) / abs(baseline)


def rate_of_change(
    first: float,
    second: float,
    t1: float,
    t2: float,
) -> float:
    if t2 <= t1:
        raise ValueError
    return (second - first) / (t2 - t1)


def baseline_delta(current: float, baseline: float) -> float:
    return current - baseline


def accumulated_travel(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError
    return sum(
        abs(values[index] - values[index - 1])
        for index in range(1, len(values))
    )


def weighted_health(
    features: list[float],
    weights: list[float],
) -> float:
    if len(features) != len(weights) or not features:
        raise ValueError
    if any(not 0.0 <= value <= 1.0 for value in features):
        raise ValueError
    if any(weight < 0.0 for weight in weights):
        raise ValueError
    total = sum(weights)
    if total <= 0.0:
        raise ValueError
    return sum(
        feature * weight
        for feature, weight in zip(features, weights)
    ) / total


def cluster_coverage(text: str) -> dict[str, bool]:
    normalized = " ".join(text.casefold().split())
    return {
        group: all(
            " ".join(marker.casefold().split()) in normalized
            for marker in markers
        )
        for group, markers in SEMANTIC_CLUSTERS.items()
    }


def matched_profile_key_terms(
    text: str,
    profile: dict[str, Any],
) -> list[str]:
    normalized = " ".join(text.casefold().split())
    terms = (
        profile.get("candidate_extraction") or {}
    ).get("key_terms") or []
    return [
        str(term)
        for term in terms
        if " ".join(str(term).casefold().split()) in normalized
    ]


def negative_samples() -> dict[str, str]:
    fact = load_json(SOURCE_DIR / "fact_anchor.json")
    by_id = {
        row["id"]: row
        for row in fact["fatal_wrong_claims"]
    }
    samples: dict[str, str] = {}
    for rule_id in NEGATIVE_RULE_IDS:
        row = by_id[rule_id]
        wrong = str(row.get("wrong_claim") or row.get("claim") or "")
        correction = str(
            row.get("correction")
            or row.get("correct_rule")
            or ""
        )
        samples[rule_id] = f"{wrong} {correction}"
    return samples


class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.importance = load_json(SOURCE_DIR / "topic_importance.json")
        cls.gfact = target_entry("fact_anchors.generated.json", "topics")
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.glogic = target_entry(
            "logic_checks.generated.json",
            "topic_logic_checks",
        )
        cls.gmodel = target_entry("model_answers.generated.json", "answers")
        cls.gimportance = target_entry(
            "topic_importance.generated.json",
            "topics",
        )
        cls.manifest = target_entry(
            "topic_pack_manifest.generated.json",
            "topics",
        )

    def test_source_generated_and_dynamic_manifest_alignment(self) -> None:
        for row in (
            self.fact,
            self.logic,
            self.model,
            self.importance,
            self.gfact,
            self.profile,
            self.glogic,
            self.gmodel,
            self.gimportance,
            self.manifest,
        ):
            self.assertEqual(row["topic_id"], TOPIC)
        source_ids = sorted(
            path.name
            for path in (ROOT / "rubrics" / "topic_packs").iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        manifest_ids = [
            row["topic_id"]
            for row in load_json(
                GENERATED_DIR / "topic_pack_manifest.generated.json"
            )["topics"]
        ]
        self.assertEqual(manifest_ids, source_ids)
        self.assertEqual(manifest_ids.count(TOPIC), 1)

    def test_exact_anchor_fatal_major_contract(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.fact["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.gfact["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.fact["fatal_wrong_claims"]],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.gfact["fatal_wrong_claims"]],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.profile["major_checks"]],
            EXPECTED_MAJOR_IDS,
        )
        self.assertEqual(len(self.profile["fatal_conditions"]), 24)

    def test_fatal_corrections_exact_source_generated_alignment(self) -> None:
        source_by = {
            row["id"]: row
            for row in self.fact["fatal_wrong_claims"]
        }
        generated_by = {
            row["id"]: row
            for row in self.gfact["fatal_wrong_claims"]
        }
        for rule_id in EXPECTED_FATAL_IDS:
            self.assertEqual(generated_by[rule_id], source_by[rule_id])

    def test_semantic_score_and_deterministic_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(self.glogic["fatal_checks"], [])
        self.assertEqual(self.glogic["major_checks"], [])
        self.assertEqual(self.glogic["question_type_checks"], [])
        self.assertEqual(
            self.profile["candidate_extraction"]["rules"],
            [],
        )
        self.assertGreaterEqual(
            len(self.profile["candidate_extraction"]["key_terms"]),
            300,
        )
        policy = self.profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")
        self.assertEqual(policy["affected_layers"], ["C"])
        self.assertEqual(
            self.profile["output_contract"]["excluded_score_layers"],
            ["D", "E"],
        )

    def test_patterns_outline_aliases_and_importance(self) -> None:
        patterns = self.model["expected_question_patterns"]
        outlines = self.model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        self.assertTrue(
            all(
                set(row["required_anchor_ids"]) <= anchor_set
                for row in patterns
            )
        )
        self.assertEqual(
            set().union(
                *(set(row["anchor_refs"]) for row in outlines)
            ),
            anchor_set,
        )
        aliases = {
            str(alias).casefold()
            for alias in self.model["routing_aliases"]
        }
        self.assertFalse(BROAD_ALIASES & aliases)
        self.assertEqual(
            self.gmodel["topic_aliases"],
            self.model["routing_aliases"],
        )
        self.assertEqual(
            self.gmodel["routing_aliases"],
            self.model["routing_aliases"],
        )
        self.assertEqual(self.gimportance, self.importance)
        self.assertEqual(self.importance["difficulty"], "FIELD_APPLICATION")
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(self.importance["question_type"], "DIAGNOSIS_ACTION")

    def test_diagnostic_chain_and_data_quality_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "Command, actual travel, supply pressure",
            by_id["diagnostic_signal_data_chain"],
        )
        self.assertIn("device status", by_id["diagnostic_signal_data_chain"])
        self.assertIn("quality flag", by_id["data_quality_time_sync_units"])
        self.assertIn(
            "vendor dictionary",
            by_id["vendor_variable_dictionary_verification"],
        )

    def test_online_offline_static_dynamic_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "Online monitoring",
            by_id["online_monitoring_offline_test_boundary"],
        )
        self.assertIn(
            "offline diagnostic test",
            by_id["online_monitoring_offline_test_boundary"],
        )
        self.assertIn(
            "Static valve signature",
            by_id["static_dynamic_signature_boundary"],
        )
        self.assertIn(
            "dynamic operating signature",
            by_id["static_dynamic_signature_boundary"],
        )

    def test_baseline_and_travel_error_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("as-left", by_id["as_left_reference_signature"])
        self.assertIn(
            "reference signature",
            by_id["as_left_reference_signature"],
        )
        self.assertIn("process ΔP", by_id["comparable_context_baseline"])
        self.assertIn(
            "ex=xcmd-xmeas",
            by_id["command_travel_error_signed"],
        )
        self.assertIn(
            "EFS=100(xcmd-xmeas)/(xmax-xmin)",
            by_id["full_span_travel_error"],
        )

    def test_pressure_friction_and_process_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "H(u)=|xup(u)-xdown(u)|",
            by_id["up_down_hysteresis_signature"],
        )
        self.assertIn(
            "ΔPsig(x)=|Popen(x)-Pclose(x)|",
            by_id["actuator_pressure_open_close_band"],
        )
        self.assertIn(
            "Fproxy≈Aeff·ΔPsig/2",
            by_id["pressure_band_friction_proxy"],
        )
        self.assertIn(
            "confounding factor",
            by_id["process_force_confounding"],
        )

    def test_pneumatic_sensor_and_usage_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        for anchor_id, marker in (
            ("supply_pressure_regulator_droop", "regulator droop"),
            ("ip_zero_span_drift_trend", "zero·span drift"),
            ("relay_pilot_fill_vent_health", "fill·vent"),
            ("pneumatic_air_consumption_leakage", "Air-consumption"),
            ("feedback_sensor_drift_noise_dropout", "dropout"),
            ("cycle_count_definition", "partial cycle"),
        ):
            self.assertIn(marker, by_id[anchor_id])

    def test_usage_response_endpoint_and_resistance_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "TAT=Σ|xk-xk-1|",
            by_id["accumulated_travel_direction_reversal"],
        )
        self.assertIn(
            "Stroke-time trend",
            by_id["stroke_time_response_trend"],
        )
        self.assertIn(
            "Seat contact",
            by_id["endpoint_seat_contact_mechanical_stop"],
        )
        self.assertIn(
            "Packing",
            by_id["packing_stem_shaft_resistance_trend"],
        )
        self.assertIn(
            "Topic 10",
            by_id["trim_balance_seal_friction_handoff"],
        )

    def test_trend_alarm_confidence_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "rz=zcurrent-zbaseline(context)",
            by_id["baseline_residual_context"],
        )
        self.assertIn("nonzero baseline", by_id["percent_change_domain"])
        self.assertIn("t2>t1", by_id["rate_of_change_time_domain"])
        self.assertIn(
            "persistence",
            by_id["threshold_persistence_deadband"],
        )
        self.assertIn(
            "multi-evidence",
            by_id["multi_evidence_failure_isolation"],
        )
        self.assertIn(
            "confidence",
            by_id["diagnostic_confidence_data_quality"],
        )

    def test_detection_maintenance_and_workflow_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "Anomaly detection",
            by_id["detection_confirmation_boundary"],
        )
        self.assertIn(
            "detect→verify→diagnose→prioritize→plan→repair→as-left",
            by_id["detect_verify_diagnose_priority_workflow"],
        )
        self.assertIn(
            "Time-based",
            by_id["time_condition_predictive_maintenance_compare"],
        )
        self.assertIn(
            "actionable lead time",
            by_id["degradation_trend_lead_time"],
        )
        self.assertIn(
            "production, safety, quality",
            by_id["maintenance_priority_consequence"],
        )

    def test_integration_offline_risk_and_feedback_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn(
            "HART·Fieldbus",
            by_id["hart_fieldbus_asset_integration"],
        )
        self.assertIn(
            "safety authorization",
            by_id["offline_test_process_risk"],
        )
        feedback_statement = by_id[
            "as_found_as_left_work_order_feedback"
        ].casefold()
        for marker in (
            "as-found",
            "as-left",
            "work-order result",
        ):
            self.assertIn(marker, feedback_statement)

    def test_explicit_topic_handoff_boundaries(self) -> None:
        combined = json.dumps(
            {
                "fact": self.fact,
                "logic": self.logic,
                "model": self.model,
            },
            ensure_ascii=False,
        ) + TOPIC_SHEET.read_text(encoding="utf-8")
        for marker in (
            "Topic 1",
            "Topic 3",
            "Topic 10",
            "Topic 11",
            "Topic 13",
            "Topic 15",
            "Topic 16",
        ):
            self.assertIn(marker, combined)

    def test_section_aware_fatal_corrections(self) -> None:
        by_id = {
            row["id"]: row
            for row in self.fact["fatal_wrong_claims"]
        }
        checks: dict[str, tuple[str, ...]] = {
            "smart_diagnostic_guarantees_root_cause": (
                "physical inspection",
                "functional test",
            ),
            "valve_signature_alone_proves_seat_leakage": (
                "Topic 13",
                "shutoff test",
            ),
            "pressure_band_equals_friction_universally": (
                "friction proxy",
                "process-force",
            ),
            "single_threshold_is_sufficient": (
                "persistence",
                "multi-evidence",
            ),
            "universal_health_index_weights": (
                "feature",
                "normalization",
                "weight",
                "threshold",
                "valve·service별로",
            ),
            "offline_signature_always_safe": (
                "process interruption",
                "safety authorization",
            ),
            "predictive_maintenance_exact_failure_date": (
                "degradation trend",
                "exact failure date를 보장하지 않는다",
            ),
            "pst_data_automatic_proof_test_credit": (
                "Topic 15",
                "validation",
            ),
            "smart_positioner_replaces_inspection": (
                "보완하며 대체하지 않는다",
            ),
            "hart_fieldbus_is_realtime_unlimited": (
                "update rate",
                "communication quality",
            ),
        }
        for rule_id, markers in checks.items():
            correction = str(
                by_id[rule_id].get("correction")
                or by_id[rule_id].get("correct_rule")
                or ""
            )
            for marker in markers:
                self.assertIn(marker, correction)


class RouterRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(GENERATED_DIR / "model_answers.generated.json")
        cls.answer_by_topic = {
            row["topic_id"]: row
            for row in cls.bank["answers"]
        }
        for topic_id in (
            TOPIC,
            TOPIC_1,
            TOPIC_2,
            TOPIC_3,
            TOPIC_4,
            TOPIC_5,
            TOPIC_6,
            TOPIC_7,
            TOPIC_8,
            TOPIC_9,
            TOPIC_10,
            TOPIC_11,
        ):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(f"missing topic {topic_id}")

    @classmethod
    def qtype(cls, topic_id: str) -> dict[str, Any]:
        return {
            "primary_type": {
                "id": cls.answer_by_topic[topic_id]["question_type"],
                "confidence": "high",
            }
        }

    @staticmethod
    def fact_eval(topic_id: str) -> dict[str, Any]:
        return {
            "topic_id": topic_id,
            "matched": True,
            "confidence": "high",
        }

    @classmethod
    def route(
        cls,
        question: str,
        topic_id: str,
        answer_text: str = "",
    ) -> dict[str, Any]:
        return find_model_answer_reference(
            question_text=question,
            answer_text=answer_text,
            fact_eval=cls.fact_eval(topic_id),
            question_type_eval=cls.qtype(topic_id),
            bank=cls.bank,
        )

    def assert_primary(
        self,
        result: dict[str, Any],
        expected: str,
    ) -> None:
        self.assertTrue(result.get("matched"), msg=result)
        self.assertEqual(selected_topic(result), expected, msg=result)

    def test_diagnostic_data_chain_route(self) -> None:
        self.assert_primary(
            self.route(
                "Smart positioner diagnostic data chain에서 command, actual travel, "
                "supply pressure, actuator pressure와 device status를 연결해 진단하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_online_offline_route(self) -> None:
        self.assert_primary(
            self.route(
                "Online monitoring과 offline valve signature test의 목적, "
                "stroke risk와 적용 조건을 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_static_dynamic_signature_route(self) -> None:
        self.assert_primary(
            self.route(
                "Static valve signature와 dynamic operating signature의 excitation, "
                "sampling과 해석 목적을 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_as_left_baseline_route(self) -> None:
        self.assert_primary(
            self.route(
                "As-left reference signature와 process ΔP, supply, temperature, "
                "stroke direction을 이용해 comparable baseline을 설정하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_travel_hysteresis_route(self) -> None:
        self.assert_primary(
            self.route(
                "Command actual travel deviation, full-span travel error와 "
                "upstroke downstroke hysteresis signature를 계산하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_pressure_band_friction_route(self) -> None:
        self.assert_primary(
            self.route(
                "Opening closing actuator pressure band와 effective area로 "
                "conditional friction proxy를 계산하고 process-force 한계를 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_supply_ip_relay_route(self) -> None:
        self.assert_primary(
            self.route(
                "Supply regulator droop, I/P zero span drift, relay pilot와 "
                "fill vent response 이상을 진단하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_air_feedback_sensor_route(self) -> None:
        self.assert_primary(
            self.route(
                "Air consumption pneumatic leakage trend와 travel feedback sensor "
                "drift noise dropout을 구분하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_usage_stroke_time_route(self) -> None:
        self.assert_primary(
            self.route(
                "Cycle count, accumulated travel, direction reversal와 stroke time "
                "response degradation trend를 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_alarm_confidence_route(self) -> None:
        self.assert_primary(
            self.route(
                "Baseline residual, percentage rate of change, alarm persistence, "
                "deadband, diagnostic confidence와 data quality를 설계하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_maintenance_strategy_route(self) -> None:
        self.assert_primary(
            self.route(
                "Time based, condition based와 predictive valve maintenance를 "
                "degradation trend와 actionable lead time 기준으로 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_closed_loop_integration_route(self) -> None:
        self.assert_primary(
            self.route(
                "Detect verify diagnose prioritize plan repair as-left workflow와 "
                "HART Fieldbus asset diagnostic work-order feedback을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_topic1_force_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Worst-case unbalanced force, packing friction, seat load와 "
                "fail-safe spring으로 actuator thrust를 산정하시오.",
                TOPIC_1,
            ),
            TOPIC_1,
        )

    def test_topic3_dynamic_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Deadband, stiction, hysteresis, response time와 hunting을 "
                "시험하고 booster bypass를 tuning하시오.",
                TOPIC_3,
            ),
            TOPIC_3,
        )

    def test_topic4_body_actuator_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Globe, butterfly, ball valve body와 pneumatic, electric, "
                "hydraulic actuator type을 비교 선정하시오.",
                TOPIC_4,
            ),
            TOPIC_4,
        )

    def test_topic10_trim_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Balanced trim과 unbalanced trim의 residual force, balance seal "
                "friction과 internal leakage를 비교하시오.",
                TOPIC_10,
            ),
            TOPIC_10,
        )

    def test_topic11_positioner_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Positioner, I/P converter, volume booster, lock-up relay의 원리와 "
                "zero span multipoint calibration을 설명하시오.",
                TOPIC_11,
            ),
            TOPIC_11,
        )

    def test_question_only_routing_survives_answer_contamination(self) -> None:
        result = self.route(
            "Valve signature baseline, travel-pressure trend와 multi-evidence "
            "predictive maintenance를 설계하시오.",
            TOPIC,
            answer_text=(
                "Deadband stiction tuning, 4-20 mA 3-15 psi I/P calibration, "
                "balanced trim과 actuator thrust를 상세히 서술한다."
            ),
        )
        self.assert_primary(result, TOPIC)
        aliases = {
            str(alias).casefold()
            for alias in self.answer_by_topic[TOPIC]["routing_aliases"]
        }
        self.assertFalse(BROAD_ALIASES & aliases)


class SmartPositionerDiagnosticSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )

    def test_signed_travel_error(self) -> None:
        self.assertTrue(
            math.isclose(
                travel_error(0.8, 0.5),
                0.3,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )
        self.assertTrue(
            math.isclose(
                travel_error(0.5, 0.8),
                -0.3,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )

    def test_full_span_error_and_domain(self) -> None:
        self.assertTrue(
            math.isclose(
                full_span_error(51.0, 49.0, 0.0, 100.0),
                2.0,
            )
        )
        with self.assertRaises(ValueError):
            full_span_error(50.0, 50.0, 100.0, 100.0)

    def test_hysteresis_symmetry(self) -> None:
        self.assertEqual(hysteresis(51.0, 49.0), 2.0)
        self.assertEqual(hysteresis(49.0, 51.0), 2.0)

    def test_pressure_band_and_conditional_friction_proxy(self) -> None:
        self.assertEqual(pressure_band(8.0, 12.0), 4.0)
        self.assertEqual(friction_proxy(2.0, 4.0), 4.0)
        with self.assertRaises(ValueError):
            friction_proxy(0.0, 4.0)
        with self.assertRaises(ValueError):
            friction_proxy(2.0, -1.0)

    def test_baseline_residual_percent_and_rate(self) -> None:
        self.assertEqual(baseline_residual(12.0, 10.0), 2.0)
        self.assertEqual(percent_change(12.0, 10.0), 20.0)
        self.assertEqual(rate_of_change(10.0, 14.0, 2.0, 4.0), 2.0)
        with self.assertRaises(ValueError):
            percent_change(1.0, 0.0)
        with self.assertRaises(ValueError):
            rate_of_change(1.0, 2.0, 5.0, 5.0)

    def test_air_usage_and_stroke_time_baseline_delta(self) -> None:
        self.assertEqual(baseline_delta(7.0, 5.0), 2.0)
        self.assertEqual(baseline_delta(5.0, 7.0), -2.0)

    def test_accumulated_travel_and_domain(self) -> None:
        self.assertTrue(
            math.isclose(
                accumulated_travel([0.0, 0.5, 0.2, 1.0]),
                1.6,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )
        with self.assertRaises(ValueError):
            accumulated_travel([1.0])

    def test_conditional_weighted_health_index(self) -> None:
        self.assertTrue(
            math.isclose(
                weighted_health([0.2, 0.8], [1.0, 3.0]),
                0.65,
            )
        )
        for features, weights in (
            ([0.2], [0.0]),
            ([1.2], [1.0]),
            ([0.2, 0.3], [1.0]),
        ):
            with self.subTest(features=features, weights=weights):
                with self.assertRaises(ValueError):
                    weighted_health(features, weights)

    def test_positive_sample_semantic_cluster_coverage(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(SEMANTIC_CLUSTERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_contextual_negative_candidate_extraction(self) -> None:
        samples = negative_samples()
        self.assertEqual(set(samples), set(NEGATIVE_RULE_IDS))
        for rule_id, answer_text in samples.items():
            with self.subTest(rule_id=rule_id):
                matched = matched_profile_key_terms(
                    answer_text,
                    self.profile,
                )
                self.assertGreaterEqual(
                    len(matched),
                    3,
                    msg={"rule_id": rule_id, "matched": matched},
                )
                candidates = extract_logic_evidence_candidates(
                    answer_text,
                    self.profile,
                )
                self.assertTrue(
                    candidates,
                    msg={"rule_id": rule_id, "matched": matched},
                )

    def test_mocked_fatal_verifier_contract(self) -> None:
        rule_id = "pressure_band_equals_friction_universally"
        answer_text = negative_samples()[rule_id]
        candidates = extract_logic_evidence_candidates(
            answer_text,
            self.profile,
        )
        self.assertTrue(candidates)
        mocked_fatal = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": "Pressure band를 조건 없는 friction force로 단정한다.",
            "findings": [{
                "candidate_id": candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message": "Universal pressure-band friction claim",
                "correct_rule": (
                    "Pressure band는 effective area와 process-force 가정이 "
                    "성립할 때만 friction proxy로 해석한다."
                ),
            }],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_fatal,
        ):
            result = verify_logic_with_llm(answer_text, TOPIC)
        self.assertTrue(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "fatal")
        self.assertEqual(
            result["findings"][0]["affected_layers"],
            ["C"],
        )

    def test_mocked_safe_verifier_contract(self) -> None:
        candidates = extract_logic_evidence_candidates(
            SAFE_ANSWER,
            self.profile,
        )
        self.assertTrue(candidates)
        mocked_safe = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": (
                "Comparable baseline, multi-evidence와 field verification을 "
                "사용하고 Topic 경계를 유지한다."
            ),
            "findings": [],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_safe,
        ):
            result = verify_logic_with_llm(SAFE_ANSWER, TOPIC)
        self.assertFalse(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "pass")
        self.assertIsNone(result["recommended_ceiling"])
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
