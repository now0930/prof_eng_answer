#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path
from typing import Any, Callable
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_llm_verifier import (
    extract_logic_evidence_candidates,
    verify_logic_with_llm,
)
from model_answer_router import find_model_answer_reference

TOPIC = "final_control_element_sil_sis_esd_valve_partial_stroke_test"
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
TOPIC_12 = "smart_positioner_diagnostics_valve_signature_predictive_maintenance"
TOPIC_13 = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
TOPIC_14 = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['final_element_role_in_sif', 'system_sif_sil_context_boundary', 'safe_state_process_hazard_basis', 'deenergize_to_trip_energy_philosophy', 'final_element_subsystem_boundary', 'valve_actuator_solenoid_architecture', 'utility_supply_and_shared_dependencies', 'trip_signal_and_output_chain', 'dangerous_failure_modes', 'safe_failure_and_spurious_trip', 'hidden_stuck_failure', 'seat_leakage_as_safety_requirement', 'actuator_force_margin_handoff', 'fail_action_vs_safe_state', 'failure_rate_partition_dd_du_sd_su', 'low_demand_pfdavg_contribution', 'high_continuous_demand_pfh_contribution', 'series_subsystem_pfd', 'final_element_budget_allocation', 'diagnostic_coverage_definition', 'proof_test_coverage_definition', 'pst_coverage_definition', 'pst_detectable_failure_set', 'pst_not_full_proof_test', 'full_stroke_proof_test_scope', 'test_interval_and_repair_time', 'imperfect_test_residual_risk', 'proof_test_procedure_repeatability', 'response_time_process_safety_time', 'component_response_time_sum', 'worst_case_trip_time', 'deenergized_energized_test_condition', 'bypass_override_inhibit_controls', 'impairment_alarm_and_permit', 'restoration_independent_verification', 'common_cause_beta_factor_context', 'redundancy_independence_boundary', 'shared_air_power_environment', 'partial_stroke_test_risk_controls', 'pst_interval_and_online_demand_exposure', 'diagnostic_credit_validation', 'valve_signature_pst_handoff', 'proof_test_records_traceability', 'fmeca_fmeda_vendor_data_assumptions', 'systematic_capability_software_procedure', 'maintenance_moc_spares', 'acceptance_criteria_and_srs_traceability', 'lifecycle_closed_loop_reverification']
EXPECTED_FATAL_IDS = ['sil_is_device_rating_only', 'esd_valve_alone_equals_sif', 'fail_close_always_safe', 'deenergize_always_safe_without_hazard_analysis', 'pst_equals_full_proof_test', 'pst_detects_all_dangerous_failures', 'diagnostic_coverage_equals_proof_test_coverage', 'pfdavg_equals_failure_probability_any_time', 'pfh_used_for_all_low_demand_cases', 'series_pfd_simple_sum_always_exact', 'test_interval_longer_always_safe', 'proof_test_coverage_100_by_procedure_name', 'response_time_equals_valve_stroke_only', 'bypass_has_no_sil_effect', 'override_restoration_without_independent_check', 'redundancy_removes_common_cause', 'shared_air_independence_assumed', 'seat_leakage_never_safety_relevant', 'vendor_sil_certificate_guarantees_application', 'fmda_data_without_mission_profile', 'pst_no_process_risk', 'online_test_no_spurious_trip_risk', 'maintenance_resets_as_good_as_new', 'diagnostics_replace_proof_test']
EXPECTED_MAJOR_IDS = ['fixed_pst_coverage', 'fixed_proof_interval', 'fixed_response_time', 'fixed_sil_allocation', 'fixed_beta_factor', 'fixed_repair_time', 'fixed_spurious_trip_limit', 'fixed_air_pressure', 'fixed_leakage_class', 'fixed_partial_stroke_percent', 'fixed_test_success_threshold', 'fixed_revalidation_interval']

ANCHOR_PROJECTION_KEYS = (
    "id",
    "anchor_id",
    "statement",
    "keywords",
    "core_terms",
    "accepted_explanations",
    "rejected_explanations",
    "grading_notes",
    "source_basis",
    "claim",
)

BROAD_ALIASES = {
    "sil", "sis", "sif", "safety", "valve", "test", "pst",
    "esd", "actuator", "solenoid", "proof",
}

NEGATIVE_RULE_IDS = (
    "sil_is_device_rating_only",
    "fail_close_always_safe",
    "pst_equals_full_proof_test",
    "diagnostic_coverage_equals_proof_test_coverage",
    "redundancy_removes_common_cause",
    "vendor_sil_certificate_guarantees_application",
)

POSITIVE_ANSWER = """
SIF final element subsystem valve actuator solenoid architecture를 정의한다.
Safety Instrumented Function final element safe state verification은 SRS에서 시작한다.
Low demand PFDavg high demand PFH final element를 demand mode에 따라 구분한다.
Diagnostic coverage proof test coverage final element의 detectable failure set을 구분한다.
Partial stroke test full stroke proof test comparison으로 residual hidden failure를 설명한다.
Shutdown valve response time process safety time margin을 worst-case condition에서 확인한다.
SIF bypass override impairment restoration management를 permit와 independent check로 관리한다.
Redundant shutdown valves common cause beta factor와 shared utility를 평가한다.
Final element proof-test record as-found as-left를 MOC와 revalidation에 연결한다.
"""

SAFE_ANSWER = """
SIF final element subsystem valve actuator solenoid architecture는 logic solver output부터
process safe state 달성까지 정의한다. Safety Instrumented Function final element safe state
verification은 hazard analysis와 SRS를 기준으로 한다. Low demand PFDavg high demand PFH
final element를 구분하고 Diagnostic coverage proof test coverage final element의 detectable failure
set을 명시한다. Partial stroke test full stroke proof test comparison에서 PST가 complete
travel, isolation과 seat leakage를 자동으로 대체하지 않는다고 설명한다. Shutdown valve
response time process safety time margin은 minimum utility와 maximum process load에서
측정한다. SIF bypass override impairment restoration management를 permit와 independent check로
관리하고 Redundant shutdown valves common cause beta factor를 관리한다. Final element proof-test record as-found
as-left를 maintenance, MOC와 lifecycle revalidation에 연결한다.
"""

SEMANTIC_CLUSTERS = {
    "context": (
        "Safety Instrumented Function",
        "final element",
        "safe state",
        "SRS",
    ),
    "architecture": (
        "valve",
        "actuator",
        "solenoid",
        "utility",
    ),
    "reliability": (
        "low demand",
        "PFDavg",
        "high demand",
        "PFH",
    ),
    "coverage": (
        "Diagnostic coverage",
        "proof test coverage",
        "detectable failure set",
    ),
    "testing": (
        "Partial stroke test",
        "full stroke proof test",
        "residual hidden failure",
    ),
    "response": (
        "response time",
        "process safety time",
        "worst-case condition",
    ),
    "governance": (
        "bypass",
        "override",
        "impairment",
        "restoration",
    ),
    "lifecycle": (
        "common cause",
        "shared utility",
        "as-found",
        "as-left",
        "MOC",
        "revalidation",
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def target_entry(filename: str, list_key: str) -> dict[str, Any]:
    rows = load_json(GENERATED_DIR / filename).get(list_key, [])
    matches = [
        row for row in rows
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
    answer_by_topic = {row["topic_id"]: row for row in bank["answers"]}
    return find_model_answer_reference(
        question_text=question,
        answer_text=answer_text,
        fact_eval={
            "topic_id": topic_id,
            "matched": True,
            "confidence": "high",
        },
        question_type_eval={
            "primary_type": {
                "id": answer_by_topic[topic_id]["question_type"],
                "confidence": "high",
            }
        },
        bank=bank,
    )


def matched_profile_key_terms(
    text: str,
    profile: dict[str, Any],
) -> list[str]:
    normalized = " ".join(text.casefold().split())
    terms = (
        profile.get("candidate_extraction") or {}
    ).get("key_terms") or []
    return [
        str(term) for term in terms
        if " ".join(str(term).casefold().split()) in normalized
    ]


def negative_samples() -> dict[str, str]:
    source = load_json(SOURCE_DIR / "fact_anchor.json")
    by_id = {
        row["id"]: row
        for row in source["fatal_wrong_claims"]
    }
    result: dict[str, str] = {}
    for rule_id in NEGATIVE_RULE_IDS:
        row = by_id[rule_id]
        wrong = str(row.get("wrong_claim") or row.get("claim") or "")
        correction = str(
            row.get("correction") or row.get("correct_rule") or ""
        )
        result[rule_id] = f"{wrong} {correction}"
    return result


def cluster_coverage(text: str) -> dict[str, bool]:
    normalized = " ".join(text.casefold().split())
    return {
        group: all(
            " ".join(marker.casefold().split()) in normalized
            for marker in markers
        )
        for group, markers in SEMANTIC_CLUSTERS.items()
    }


def assert_markers(
    testcase: unittest.TestCase,
    statement: str,
    markers: tuple[str, ...],
) -> None:
    normalized = " ".join(statement.casefold().split())
    for marker in markers:
        testcase.assertIn(
            " ".join(marker.casefold().split()),
            normalized,
        )


def pfdavg(rate: float, interval: float) -> float:
    if rate < 0.0 or interval < 0.0:
        raise ValueError
    return rate * interval / 2.0


def pfh(rate: float) -> float:
    if rate < 0.0:
        raise ValueError
    return rate


def pfd_series(values: list[float]) -> float:
    if any(value < 0.0 or value > 1.0 for value in values):
        raise ValueError
    product = 1.0
    for value in values:
        product *= 1.0 - value
    return 1.0 - product


def pfd_series_small(values: list[float]) -> float:
    if any(value < 0.0 or value > 1.0 for value in values):
        raise ValueError
    return sum(values)


def diagnostic_coverage(dd: float, du: float) -> float:
    if dd < 0.0 or du < 0.0 or dd + du <= 0.0:
        raise ValueError
    return dd / (dd + du)


def proof_test_coverage(detected: float, total: float) -> float:
    if detected < 0.0 or total <= 0.0 or detected > total:
        raise ValueError
    return detected / total


def pst_residual(rate: float, coverage: float) -> float:
    if rate < 0.0 or coverage < 0.0 or coverage > 1.0:
        raise ValueError
    return rate * (1.0 - coverage)


def common_cause_rate(beta: float, dangerous_rate: float) -> float:
    if beta < 0.0 or beta > 1.0 or dangerous_rate < 0.0:
        raise ValueError
    return beta * dangerous_rate


def final_element_response_time(
    solenoid: float,
    actuator: float,
    valve: float,
) -> float:
    if min(solenoid, actuator, valve) < 0.0:
        raise ValueError
    return solenoid + actuator + valve


def response_margin(allowed: float, measured: float) -> float:
    if allowed <= 0.0:
        raise ValueError
    return (allowed - measured) / allowed


def test_interval_margin(required: float, actual: float) -> float:
    if required <= 0.0:
        raise ValueError
    return (required - actual) / required


def safe_failure_fraction(
    safe: float,
    dangerous_detected: float,
    dangerous_undetected: float,
) -> float:
    total = safe + dangerous_detected + dangerous_undetected
    if min(safe, dangerous_detected, dangerous_undetected) < 0.0:
        raise ValueError
    if total <= 0.0:
        raise ValueError
    return (safe + dangerous_detected) / total


class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.importance = load_json(
            SOURCE_DIR / "topic_importance.json"
        )
        cls.gfact = target_entry(
            "fact_anchors.generated.json", "topics"
        )
        cls.profile = target_entry(
            "logic_check_profiles.generated.json", "profiles"
        )
        cls.glogic = target_entry(
            "logic_checks.generated.json", "topic_logic_checks"
        )
        cls.gmodel = target_entry(
            "model_answers.generated.json", "answers"
        )
        cls.gimportance = target_entry(
            "topic_importance.generated.json", "topics"
        )
        cls.by_id = {
            row["id"]: row["statement"]
            for row in cls.fact["anchors"]
        }

    def test_manifest_alignment(self) -> None:
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

    def test_exact_contract_ids(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.fact["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.gfact["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [
                row["id"]
                for row in self.fact["fatal_wrong_claims"]
            ],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.profile["major_checks"]],
            EXPECTED_MAJOR_IDS,
        )

    def test_anchor_projection_alignment(self) -> None:
        source_by = {
            row["id"]: row for row in self.fact["anchors"]
        }
        generated_by = {
            row["id"]: row for row in self.gfact["anchors"]
        }
        for anchor_id in EXPECTED_ANCHOR_IDS:
            for key in ANCHOR_PROJECTION_KEYS:
                self.assertEqual(
                    generated_by[anchor_id][key],
                    source_by[anchor_id][key],
                )

    def test_anchor_schema_projection_boundary(self) -> None:
        source_fields = set().union(
            *(set(row) for row in self.fact["anchors"])
        )
        generated_fields = set().union(
            *(set(row) for row in self.gfact["anchors"])
        )
        self.assertEqual(
            source_fields
            - generated_fields
            - set(ANCHOR_PROJECTION_KEYS),
            set(),
        )
        self.assertEqual(
            generated_fields
            - source_fields
            - set(ANCHOR_PROJECTION_KEYS),
            {"expected", "name", "support_terms"},
        )

    def test_fatal_major_alignment(self) -> None:
        self.assertEqual(
            self.gfact["fatal_wrong_claims"],
            self.fact["fatal_wrong_claims"],
        )
        self.assertEqual(
            self.profile["fatal_conditions"],
            self.fact["fatal_wrong_claims"],
        )
        self.assertEqual(
            self.profile["major_checks"],
            self.logic["llm_profile"]["major_checks"],
        )

    def test_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(self.glogic["fatal_checks"], [])
        self.assertEqual(self.glogic["major_checks"], [])
        self.assertEqual(self.glogic["question_type_checks"], [])
        candidate = self.profile["candidate_extraction"]
        self.assertEqual(candidate["rules"], [])
        self.assertEqual(len(candidate["key_terms"]), 567)
        policy = self.profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")
        self.assertEqual(policy["affected_layers"], ["C"])

    def test_model_importance(self) -> None:
        self.assertEqual(
            len(self.model["expected_question_patterns"]),
            10,
        )
        self.assertEqual(
            len(self.model["recommended_outline"]),
            8,
        )
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        self.assertEqual(
            set().union(
                *(
                    set(row["anchor_refs"])
                    for row in self.model["recommended_outline"]
                )
            ),
            anchor_set,
        )
        aliases = {
            str(alias).casefold()
            for alias in self.model["routing_aliases"]
        }
        self.assertFalse(BROAD_ALIASES & aliases)
        self.assertGreaterEqual(len(aliases), 20)
        self.assertEqual(
            self.gmodel["routing_aliases"],
            self.model["routing_aliases"],
        )
        self.assertEqual(self.gimportance, self.importance)
        self.assertEqual(
            self.importance["difficulty"],
            "FIELD_APPLICATION",
        )
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.importance["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )

    def test_explicit_boundaries(self) -> None:
        combined = (
            json.dumps(
                {
                    "fact": self.fact,
                    "logic": self.logic,
                    "model": self.model,
                },
                ensure_ascii=False,
            )
            + TOPIC_SHEET.read_text(encoding="utf-8")
        ).casefold()
        for marker in (
            "topic 1",
            "topic 3",
            "topic 4",
            "topic 8",
            "topic 10",
            "topic 11",
            "topic 12",
            "topic 13",
            "topic 14",
            "topic 16",
        ):
            self.assertIn(marker, combined)


ANCHOR_MARKER_CASES: dict[str, tuple[str, ...]] = {
    "final_element_role_in_sif": (
        "Final Element",
        "Safety Instrumented Function",
        "logic solver",
        "안전 상태",
        "solenoid valve",
        "actuator",
        "utility",
    ),
    "safe_state_process_hazard_basis": (
        "Safe State",
        "fail-close",
        "fail-open",
        "Hazard analysis",
        "Safety Requirement Specification",
    ),
    "valve_actuator_solenoid_architecture": (
        "ESD valve package",
        "valve body",
        "actuator",
        "solenoid-operated valve",
        "utility interface",
    ),
    "dangerous_failure_modes": (
        "demand",
        "요구 시간 초과",
        "required isolation",
        "solenoid sticking",
        "actuator leakage",
    ),
    "low_demand_pfdavg_contribution": (
        "Low-demand SIF",
        "PFDavg",
        "constant failure rate",
        "proof-test interval",
        "coverage",
    ),
    "proof_test_coverage_definition": (
        "Proof Test Coverage",
        "otherwise undetected",
        "failure-mode-to-test-step",
    ),
    "pst_not_full_proof_test": (
        "PST",
        "full travel",
        "full isolation",
        "seat leakage",
        "Full Stroke Proof Test",
    ),
    "response_time_process_safety_time": (
        "Process Safety Time",
        "allowable time",
        "worst-case supply",
        "process load",
        "friction",
    ),
    "bypass_override_inhibit_controls": (
        "Bypass",
        "override",
        "inhibit",
        "Authorization",
        "compensating measure",
        "removal criterion",
    ),
    "fmeca_fmeda_vendor_data_assumptions": (
        "FMECA",
        "FMEDA",
        "device type",
        "service",
        "environment",
        "useful life",
        "proof-test coverage",
        "diagnostic configuration",
        "repair assumption",
        "Certificate",
    ),
}


def _make_anchor_marker_test(
    anchor_id: str,
    markers: tuple[str, ...],
) -> Callable[[GeneratedContractRegressionTests], None]:
    def test(
        self: GeneratedContractRegressionTests,
    ) -> None:
        assert_markers(
            self,
            self.by_id[anchor_id],
            markers,
        )
    return test


for _anchor_id, _markers in ANCHOR_MARKER_CASES.items():
    setattr(
        GeneratedContractRegressionTests,
        f"test_anchor_markers_{_anchor_id}",
        _make_anchor_marker_test(_anchor_id, _markers),
    )


class RouterRegressionTests(unittest.TestCase):
    def assert_route(
        self,
        question: str,
        expected: str,
        answer_text: str = "",
    ) -> None:
        result = route_reference(
            question,
            expected,
            answer_text,
        )
        self.assertTrue(result.get("matched"), msg=result)
        self.assertEqual(
            selected_topic(result),
            expected,
            msg=result,
        )


ROUTER_CASES = (
    (
        "final_element_architecture",
        "SIF final element subsystem valve actuator solenoid utility architecture를 설명하시오.",
        TOPIC,
    ),
    (
        "safe_state",
        "Safety Instrumented Function final element safe state verification과 de-energize-to-trip을 평가하시오.",
        TOPIC,
    ),
    (
        "pfdavg_pfh",
        "Final element PFDavg PFH contribution과 SIL budget을 계산하시오.",
        TOPIC,
    ),
    (
        "coverage",
        "Diagnostic coverage proof test coverage final element의 차이를 설명하시오.",
        TOPIC,
    ),
    (
        "pst_full_test",
        "Partial stroke test full stroke proof test comparison과 residual dangerous failure를 설명하시오.",
        TOPIC,
    ),
    (
        "response",
        "Shutdown valve response time process safety time margin을 worst-case에서 평가하시오.",
        TOPIC,
    ),
    (
        "bypass",
        "SIF bypass override impairment restoration management 기준을 제시하시오.",
        TOPIC,
    ),
    (
        "common_cause",
        "Redundant shutdown valves common cause beta factor와 shared utility independence를 설명하시오.",
        TOPIC,
    ),
    (
        "records_moc",
        "Final element proof-test record as-found as-left와 MOC revalidation을 설명하시오.",
        TOPIC,
    ),
    (
        "fmeda",
        "ESD valve FMEDA failure-rate application assumptions와 SIL certificate 한계를 평가하시오.",
        TOPIC,
    ),
    (
        "topic1",
        "Unbalanced force actuator thrust packing friction fail-safe spring sizing을 계산하시오.",
        TOPIC_1,
    ),
    (
        "topic3",
        "Deadband stiction hysteresis response time을 동적으로 시험하시오.",
        TOPIC_3,
    ),
    (
        "topic4",
        "Globe ball butterfly body와 pneumatic electric hydraulic actuator를 비교하시오.",
        TOPIC_4,
    ),
    (
        "topic8",
        "Cavitation flashing liquid choked flow anti-cavitation trim을 설명하시오.",
        TOPIC_8,
    ),
    (
        "topic10",
        "Balanced trim unbalanced trim sealing structure와 actuator force를 비교하시오.",
        TOPIC_10,
    ),
    (
        "topic11",
        "Positioner I/P converter booster accessory calibration을 설명하시오.",
        TOPIC_11,
    ),
    (
        "topic12",
        "Smart positioner valve signature diagnostics predictive maintenance를 설명하시오.",
        TOPIC_12,
    ),
    (
        "topic13",
        "Seat leakage shutoff class packing fugitive emission as-found as-left를 설명하시오.",
        TOPIC_13,
    ),
    (
        "topic14",
        "High-flow low-flow high-temperature cryogenic particle slurry severe service를 평가하시오.",
        TOPIC_14,
    ),
    (
        "topic6",
        "Liquid Cv Kv Reynolds correction과 piping factor를 계산하시오.",
        TOPIC_6,
    ),
    (
        "question_only",
        "SIF final element safe state ESD valve PST proof-test PFDavg PFH를 평가하시오.",
        TOPIC,
        "Cv sizing cavitation noise seat leakage positioner calibration severe service actuator spring",
    ),
)


def _make_router_test(
    case: tuple[Any, ...],
) -> Callable[[RouterRegressionTests], None]:
    name, question, expected, *rest = case
    answer_text = str(rest[0]) if rest else ""

    def test(self: RouterRegressionTests) -> None:
        self.assert_route(
            str(question),
            str(expected),
            answer_text,
        )

    return test


for _case in ROUTER_CASES:
    setattr(
        RouterRegressionTests,
        f"test_route_{_case[0]}",
        _make_router_test(_case),
    )


class FinalElementSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.fact = load_json(
            SOURCE_DIR / "fact_anchor.json"
        )

    def test_contextual_negative_candidate_extraction(self) -> None:
        samples = negative_samples()
        self.assertEqual(
            set(samples),
            set(NEGATIVE_RULE_IDS),
        )
        for rule_id, answer_text in samples.items():
            matched = matched_profile_key_terms(
                answer_text,
                self.profile,
            )
            self.assertGreaterEqual(
                len(matched),
                2,
                msg=(rule_id, matched),
            )
            self.assertTrue(
                extract_logic_evidence_candidates(
                    answer_text,
                    self.profile,
                ),
                msg=rule_id,
            )

    def test_mocked_fatal_verifier(self) -> None:
        rule_id = "pst_equals_full_proof_test"
        answer_text = negative_samples()[rule_id]
        candidates = extract_logic_evidence_candidates(
            answer_text,
            self.profile,
        )
        self.assertTrue(candidates)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value={
                "verdict": "fatal",
                "confidence": 0.99,
                "reason": (
                    "PST와 Full Stroke Proof Test의 "
                    "detectable failure set을 동일시한다."
                ),
                "findings": [{
                    "candidate_id": candidates[0]["id"],
                    "rule_id": rule_id,
                    "severity": "fatal",
                    "message": "PST equals full proof test",
                    "correct_rule": (
                        "PST coverage와 Full Stroke Proof Test "
                        "coverage를 분리한다."
                    ),
                }],
            },
        ):
            result = verify_logic_with_llm(
                answer_text,
                TOPIC,
            )
        self.assertTrue(
            result["fatal_error_detected"],
            msg=result,
        )
        self.assertEqual(result["mode"], "fatal")
        self.assertEqual(
            result["findings"][0]["affected_layers"],
            ["C"],
        )

    def test_mocked_safe_verifier(self) -> None:
        candidates = extract_logic_evidence_candidates(
            SAFE_ANSWER,
            self.profile,
        )
        self.assertTrue(candidates)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value={
                "verdict": "pass",
                "confidence": 1.0,
                "reason": (
                    "SRS, demand mode, coverage와 "
                    "restoration boundary를 유지한다."
                ),
                "findings": [],
            },
        ):
            result = verify_logic_with_llm(
                SAFE_ANSWER,
                TOPIC,
            )
        self.assertFalse(
            result["fatal_error_detected"],
            msg=result,
        )
        self.assertEqual(result["mode"], "pass")
        self.assertIsNone(result["recommended_ceiling"])

    def test_positive_semantic_clusters(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(
            set(rows),
            set(SEMANTIC_CLUSTERS),
        )
        self.assertTrue(
            all(rows.values()),
            msg=rows,
        )

    def test_formula_source_markers(self) -> None:
        combined = json.dumps(
            {
                "fact": self.fact,
                "profile": self.profile,
            },
            ensure_ascii=False,
        ).casefold()
        for marker in (
            "pfdavg simple low demand",
            "pfh simple high demand",
            "series pfd exact",
            "series pfd small approximation",
            "diagnostic coverage",
            "proof test coverage",
            "pst residual dangerous rate",
            "beta common cause rate",
            "final element response time",
            "response time margin",
            "test interval margin",
            "safe failure fraction screening",
        ):
            self.assertIn(marker, combined)

    def test_safe_answer_markers(self) -> None:
        normalized = " ".join(
            SAFE_ANSWER.casefold().split()
        )
        for marker in (
            "logic solver output",
            "hazard analysis",
            "low demand pfdavg",
            "high demand pfh",
            "detectable failure set",
            "complete travel",
            "minimum utility",
            "independent check",
            "common cause beta factor",
            "as-found as-left",
            "lifecycle revalidation",
        ):
            self.assertIn(
                " ".join(marker.casefold().split()),
                normalized,
            )


def _formula_pfdavg(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            pfdavg(2.0e-6, 1000.0),
            0.001,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        pfdavg(-1.0, 1.0)


def _formula_pfh(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            pfh(2.0e-6),
            2.0e-6,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        pfh(-1.0)


def _formula_series_exact(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            pfd_series([0.01, 0.02]),
            0.0298,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        pfd_series([1.2])


def _formula_series_small(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            pfd_series_small([0.01, 0.02]),
            0.03,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        pfd_series_small([-0.1])


def _formula_diagnostic_coverage(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            diagnostic_coverage(3.0, 1.0),
            0.75,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        diagnostic_coverage(0.0, 0.0)


def _formula_proof_test_coverage(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            proof_test_coverage(8.0, 10.0),
            0.8,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        proof_test_coverage(2.0, 1.0)


def _formula_pst_residual(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            pst_residual(10.0, 0.6),
            4.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        pst_residual(1.0, 1.2)


def _formula_common_cause(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            common_cause_rate(0.1, 5.0),
            0.5,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        common_cause_rate(1.2, 1.0)


def _formula_response_time(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            final_element_response_time(0.2, 0.8, 2.0),
            3.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        final_element_response_time(-1.0, 1.0, 1.0)


def _formula_response_margin(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            response_margin(5.0, 4.0),
            0.2,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        response_margin(0.0, 1.0)


def _formula_test_interval_margin(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            test_interval_margin(10.0, 8.0),
            0.2,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        test_interval_margin(0.0, 1.0)


def _formula_sff(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            safe_failure_fraction(3.0, 1.0, 1.0),
            0.8,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        safe_failure_fraction(0.0, 0.0, 0.0)


FORMULA_CASES: dict[
    str,
    Callable[[unittest.TestCase], None],
] = {
    "pfdavg": _formula_pfdavg,
    "pfh": _formula_pfh,
    "series_exact": _formula_series_exact,
    "series_small": _formula_series_small,
    "diagnostic_coverage": _formula_diagnostic_coverage,
    "proof_test_coverage": _formula_proof_test_coverage,
    "pst_residual": _formula_pst_residual,
    "common_cause": _formula_common_cause,
    "response_time": _formula_response_time,
    "response_margin": _formula_response_margin,
    "test_interval_margin": _formula_test_interval_margin,
    "safe_failure_fraction": _formula_sff,
}


def _make_formula_test(
    function: Callable[[unittest.TestCase], None],
) -> Callable[[FinalElementSemanticRegressionTests], None]:
    def test(
        self: FinalElementSemanticRegressionTests,
    ) -> None:
        function(self)

    return test


for _name, _function in FORMULA_CASES.items():
    setattr(
        FinalElementSemanticRegressionTests,
        f"test_formula_{_name}",
        _make_formula_test(_function),
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
