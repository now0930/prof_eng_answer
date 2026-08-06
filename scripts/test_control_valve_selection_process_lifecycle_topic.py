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

TOPIC = 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'
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
TOPIC_11 = 'control_valve_positioner_ip_converter_booster_accessories_calibration'
TOPIC_12 = 'smart_positioner_diagnostics_valve_signature_predictive_maintenance'
TOPIC_13 = 'control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions'
TOPIC_14 = 'control_valve_severe_service_high_low_flow_temperature_cryogenic_particles'
TOPIC_15 = 'final_control_element_sil_sis_esd_valve_partial_stroke_test'

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"
REQUIREMENTS = (
    ROOT
    / "gemini_script"
    / "20260806_topic16_control_valve_selection_process_lifecycle_requirements.md"
)

EXPECTED_ANCHOR_IDS = ['selection_process_ownership', 'governing_document_hierarchy', 'process_design_basis_traceability', 'tag_service_boundary', 'stakeholder_requirement_integration', 'requirement_classification_mandatory_preferred', 'operating_case_matrix', 'minimum_normal_maximum_cases', 'startup_shutdown_upset_cleaning_cases', 'pressure_reference_consistency', 'temperature_envelope_and_thermal_transient', 'flow_basis_and_uncertainty', 'fluid_phase_composition_properties', 'solids_fouling_corrosion_contaminant', 'control_objective_and_loop_dynamics', 'rangeability_turndown_travel_distribution', 'shutoff_leakage_fail_action', 'safety_environmental_regulatory_requirements', 'response_time_and_availability_requirement', 'specialist_calculation_handoff', 'liquid_gas_sizing_cross_check', 'authority_installed_characteristic_cross_check', 'cavitation_flashing_noise_velocity_cross_check', 'severe_service_and_material_cross_check', 'final_element_sis_esd_cross_check', 'selection_matrix_tradeoff', 'uncertainty_margin_and_double_margin', 'valve_body_flow_path_selection', 'trim_characteristic_and_flow_direction', 'pressure_temperature_rating_and_class', 'material_compatibility_and_corrosion', 'seat_packing_gasket_emissions', 'actuator_thrust_torque_supply_minimum', 'fail_action_spring_and_stored_energy', 'positioner_solenoid_booster_accessory_package', 'installation_orientation_piping_load_accessibility', 'datasheet_completeness_and_units', 'requisition_scope_and_guarantees', 'vendor_bid_technical_comparison', 'deviation_exception_risk_register', 'vendor_sizing_assumption_validation', 'document_and_configuration_control', 'inspection_test_plan_and_hold_points', 'material_certification_nde_traceability', 'fat_functional_performance_acceptance', 'sat_loop_stroke_response_leakage', 'commissioning_installed_performance_verification', 'as_built_baseline_and_handover', 'reliability_availability_maintainability', 'spare_parts_interchangeability_obsolescence', 'lifecycle_cost_energy_downtime', 'field_feedback_moc_revalidation']
EXPECTED_FATAL_IDS = ['single_normal_case_sufficient', 'datasheet_optional_after_vendor_selection', 'vendor_sizing_accepted_without_independent_check', 'line_size_equals_valve_size', 'largest_cv_is_safest', 'more_margin_always_better', 'catalog_rangeability_equals_installed_turndown', 'inherent_characteristic_alone_determines_control', 'pressure_class_from_normal_pressure_only', 'material_by_fluid_name_only', 'liquid_and_gas_same_sizing_method', 'phase_change_can_be_ignored', 'minimum_flow_not_selection_case', 'transient_cases_never_govern', 'piping_loss_and_authority_irrelevant', 'body_type_selected_by_company_habit', 'actuator_nameplate_force_is_enough', 'nominal_air_supply_is_only_case', 'fail_close_is_universally_safe', 'accessories_are_not_selection_boundary', 'higher_leakage_class_always_better', 'sil_certificate_alone_completes_selection', 'lowest_purchase_price_is_best_value', 'technical_deviation_can_close_verbally', 'fat_replaces_sat_and_commissioning', 'field_feedback_not_selection_input']
EXPECTED_MAJOR_IDS = ['fixed_capacity_margin', 'fixed_preferred_travel_band', 'fixed_valve_authority_target', 'fixed_velocity_limit', 'fixed_noise_limit', 'fixed_leakage_class', 'fixed_corrosion_allowance', 'fixed_actuator_safety_factor', 'fixed_air_supply', 'fixed_spare_ratio', 'fixed_fat_acceptance', 'fixed_commissioning_period', 'fixed_discount_rate', 'fixed_weighted_score']

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
    "selection",
    "valve",
    "process",
    "lifecycle",
    "vendor",
    "test",
    "datasheet",
    "actuator",
    "material",
    "cost",
}

NEGATIVE_RULE_IDS = ['single_normal_case_sufficient', 'largest_cv_is_safest', 'vendor_sizing_accepted_without_independent_check', 'catalog_rangeability_equals_installed_turndown', 'fat_replaces_sat_and_commissioning', 'lowest_purchase_price_is_best_value']
SEMANTIC_CLUSTERS = {'governing': ('Process Design Basis', 'PFD', 'P&ID', 'SRS', 'requirement traceability'), 'operating_cases': ('minimum', 'normal', 'maximum', 'startup', 'shutdown', 'upset', 'cleaning'), 'process_data': ('pressure reference', 'temperature envelope', 'flow basis', 'phase', 'composition', 'vapor pressure'), 'specialist': ('liquid sizing', 'gas sizing', 'valve authority', 'cavitation', 'flashing', 'noise', 'severe service'), 'package': ('valve body', 'trim', 'material compatibility', 'actuator', 'positioner', 'solenoid'), 'procurement': ('datasheet', 'requisition', 'vendor bid', 'deviation', 'configuration control'), 'acceptance': ('inspection test plan', 'FAT', 'SAT', 'commissioning', 'as-built'), 'lifecycle': ('reliability', 'availability', 'maintainability', 'spare parts', 'lifecycle cost', 'MOC', 'revalidation')}
POSITIVE_ANSWER = 'Process Design Basis, PFD, P&ID, SRS와 requirement traceability를 확정한다.\nMinimum normal maximum startup shutdown upset cleaning operating case를 분리한다.\nPressure reference, temperature envelope, flow basis, phase, composition과\nvapor pressure를 확인한다. Topic 6 liquid sizing, Topic 7 gas sizing,\nTopic 5 valve authority, Topic 8 cavitation flashing, Topic 9 noise와\nTopic 14 severe service 결과를 hand-off한다. Valve body, trim,\nmaterial compatibility, actuator, positioner와 solenoid를 package로 선정한다.\nDatasheet, requisition, vendor bid, deviation과 configuration control을 수행한다.\nInspection Test Plan, FAT, SAT, commissioning과 as-built를 acceptance evidence로\n관리한다. Reliability, availability, maintainability, spare parts,\nlifecycle cost, MOC와 revalidation을 폐루프로 연결한다.'
SAFE_ANSWER = 'Control valve integrated selection process는 Process Design Basis와\noperating case matrix에서 시작한다. Pressure reference와 flow basis를 명시한다.\nTopic 1 hand-off부터 Topic 15 hand-off까지 assumption, margin과 limitation을\n검토한다. Mandatory gate를 통과한 후보만 weighted score로 비교한다.\nDatasheet, vendor bid와 deviation을 추적한다. FAT SAT commissioning으로\ninstalled performance를 인수한다. Reliability availability maintainability와\nlifecycle cost를 평가하고 field feedback을 MOC revalidation에 반영한다.'
FORMULA_SOURCE_IDS = ['capacity_utilization', 'capacity_margin', 'installed_range_requirement', 'range_margin', 'valve_authority_handoff', 'hydraulic_energy_loss_power', 'availability', 'expected_downtime_cost', 'discounted_lifecycle_cost', 'weighted_selection_score', 'requirement_coverage', 'deviation_closure_rate']


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
        raise AssertionError(
            f"{filename} target count={len(matches)}"
        )
    return matches[0]


def selected_topic(result: dict[str, Any]) -> str | None:
    primary = result.get("primary_reference") or {}
    return (
        primary.get("topic_id")
        if isinstance(primary, dict)
        else None
    )


def route_reference(
    question: str,
    topic_id: str,
    answer_text: str = "",
) -> dict[str, Any]:
    bank = load_json(
        GENERATED_DIR / "model_answers.generated.json"
    )
    answer_by_topic = {
        row["topic_id"]: row for row in bank["answers"]
    }
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
        str(term)
        for term in terms
        if " ".join(str(term).casefold().split())
        in normalized
    ]


def negative_samples() -> dict[str, str]:
    source = load_json(SOURCE_DIR / "fact_anchor.json")
    by_id = {
        row["id"]: row
        for row in source["fatal_wrong_claims"]
    }
    result: dict[str, str] = {}
    context = (
        "control valve integrated selection process "
        "operating case lifecycle "
    )
    for rule_id in NEGATIVE_RULE_IDS:
        row = by_id[rule_id]
        wrong = str(
            row.get("wrong_claim")
            or row.get("claim")
            or ""
        )
        correction = str(
            row.get("correction")
            or row.get("correct_rule")
            or ""
        )
        result[rule_id] = (
            context + wrong + " " + correction
        )
    return result


def cluster_coverage(text: str) -> dict[str, bool]:
    normalized = " ".join(text.casefold().split())
    return {
        group: all(
            " ".join(marker.casefold().split())
            in normalized
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


def capacity_utilization(
    required: float,
    rated: float,
) -> float:
    if required < 0.0 or rated <= 0.0:
        raise ValueError
    return required / rated


def capacity_margin(
    rated: float,
    required: float,
) -> float:
    if required <= 0.0 or rated < 0.0:
        raise ValueError
    return (rated - required) / required


def installed_range_requirement(
    qmax: float,
    qmin: float,
) -> float:
    if qmax < 0.0 or qmin <= 0.0:
        raise ValueError
    return qmax / qmin


def range_margin(
    available: float,
    required: float,
) -> float:
    if available < 0.0 or required <= 0.0:
        raise ValueError
    return (available - required) / required


def valve_authority(
    valve_dp: float,
    other_dp: float,
) -> float:
    if valve_dp < 0.0 or other_dp < 0.0:
        raise ValueError
    total = valve_dp + other_dp
    if total <= 0.0:
        raise ValueError
    return valve_dp / total


def hydraulic_power(
    delta_p: float,
    flow: float,
) -> float:
    if delta_p < 0.0 or flow < 0.0:
        raise ValueError
    return delta_p * flow


def availability(
    mtbf: float,
    mttr: float,
) -> float:
    if mtbf <= 0.0 or mttr < 0.0:
        raise ValueError
    return mtbf / (mtbf + mttr)


def downtime_cost(
    frequency: float,
    downtime: float,
    cost_rate: float,
) -> float:
    if min(frequency, downtime, cost_rate) < 0.0:
        raise ValueError
    return frequency * downtime * cost_rate


def discounted_cost(
    costs: list[float],
    rate: float,
) -> float:
    if rate <= -1.0:
        raise ValueError
    if any(cost < 0.0 for cost in costs):
        raise ValueError
    return sum(
        cost / ((1.0 + rate) ** index)
        for index, cost in enumerate(costs)
    )


def weighted_score(
    weights: list[float],
    scores: list[float],
) -> float:
    if len(weights) != len(scores) or not weights:
        raise ValueError
    if any(weight < 0.0 for weight in weights):
        raise ValueError
    if not math.isclose(
        sum(weights),
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise ValueError
    return sum(
        weight * score
        for weight, score in zip(weights, scores)
    )


def requirement_coverage(
    verified: float,
    applicable: float,
) -> float:
    if applicable <= 0.0:
        raise ValueError
    if verified < 0.0 or verified > applicable:
        raise ValueError
    return verified / applicable


def deviation_closure_rate(
    closed: float,
    total: float,
) -> float:
    if total <= 0.0:
        raise ValueError
    if closed < 0.0 or closed > total:
        raise ValueError
    return closed / total


class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(
            SOURCE_DIR / "fact_anchor.json"
        )
        cls.logic = load_json(
            SOURCE_DIR / "logic_check.json"
        )
        cls.model = load_json(
            SOURCE_DIR / "model_answer.json"
        )
        cls.importance = load_json(
            SOURCE_DIR / "topic_importance.json"
        )
        cls.gfact = target_entry(
            "fact_anchors.generated.json",
            "topics",
        )
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.glogic = target_entry(
            "logic_checks.generated.json",
            "topic_logic_checks",
        )
        cls.gmodel = target_entry(
            "model_answers.generated.json",
            "answers",
        )
        cls.gimportance = target_entry(
            "topic_importance.generated.json",
            "topics",
        )
        cls.by_id = {
            row["id"]: row["statement"]
            for row in cls.fact["anchors"]
        }

    def test_manifest_alignment(self) -> None:
        source_ids = sorted(
            path.name
            for path in (
                ROOT / "rubrics" / "topic_packs"
            ).iterdir()
            if path.is_dir()
            and not path.name.startswith(".")
        )
        manifest_ids = [
            row["topic_id"]
            for row in load_json(
                GENERATED_DIR
                / "topic_pack_manifest.generated.json"
            )["topics"]
        ]
        self.assertEqual(manifest_ids, source_ids)
        self.assertEqual(len(manifest_ids), 39)
        self.assertEqual(manifest_ids.count(TOPIC), 1)
        self.assertEqual(manifest_ids.index(TOPIC), 11)

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
                for row in self.fact[
                    "fatal_wrong_claims"
                ]
            ],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [
                row["id"]
                for row in self.profile["major_checks"]
            ],
            EXPECTED_MAJOR_IDS,
        )

    def test_anchor_projection_alignment(self) -> None:
        source_by = {
            row["id"]: row
            for row in self.fact["anchors"]
        }
        generated_by = {
            row["id"]: row
            for row in self.gfact["anchors"]
        }
        for anchor_id in EXPECTED_ANCHOR_IDS:
            for key in ANCHOR_PROJECTION_KEYS:
                self.assertEqual(
                    generated_by[anchor_id][key],
                    source_by[anchor_id][key],
                )

    def test_anchor_schema_projection_boundary(self) -> None:
        source_fields = set().union(
            *(
                set(row)
                for row in self.fact["anchors"]
            )
        )
        generated_fields = set().union(
            *(
                set(row)
                for row in self.gfact["anchors"]
            )
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
            {
                "expected",
                "name",
                "support_terms",
            },
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
            self.logic["llm_profile"][
                "major_checks"
            ],
        )

    def test_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(
            self.glogic["fatal_checks"],
            [],
        )
        self.assertEqual(
            self.glogic["major_checks"],
            [],
        )
        self.assertEqual(
            self.glogic["question_type_checks"],
            [],
        )
        candidate = self.profile[
            "candidate_extraction"
        ]
        self.assertEqual(candidate["rules"], [])
        self.assertEqual(
            len(candidate["key_terms"]),
            891,
        )
        policy = self.profile["score_policy"]
        self.assertFalse(
            policy["direct_score_application"]
        )
        self.assertIsNone(
            policy["recommended_ceiling"]
        )
        self.assertEqual(
            policy["direct_d_e_effect"],
            "none",
        )
        self.assertEqual(
            policy["affected_layers"],
            ["C"],
        )
        self.assertEqual(
            self.profile["output_contract"][
                "excluded_score_layers"
            ],
            ["D", "E"],
        )

    def test_model_importance(self) -> None:
        self.assertEqual(
            len(
                self.model[
                    "expected_question_patterns"
                ]
            ),
            12,
        )
        self.assertEqual(
            len(
                self.model[
                    "recommended_outline"
                ]
            ),
            9,
        )
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        self.assertEqual(
            set().union(
                *(
                    set(row["anchor_refs"])
                    for row in self.model[
                        "recommended_outline"
                    ]
                )
            ),
            anchor_set,
        )
        aliases = {
            str(alias).casefold()
            for alias in self.model[
                "routing_aliases"
            ]
        }
        self.assertFalse(
            BROAD_ALIASES & aliases
        )
        self.assertGreaterEqual(
            len(aliases),
            20,
        )
        self.assertEqual(
            self.gmodel["routing_aliases"],
            self.model["routing_aliases"],
        )
        self.assertEqual(
            self.gimportance,
            self.importance,
        )
        self.assertEqual(
            self.importance["difficulty"],
            "FIELD_APPLICATION",
        )
        self.assertEqual(
            self.importance[
                "selection_importance"
            ],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.importance["question_type"],
            "COMPARE_SELECTION",
        )

    def test_explicit_handoff_registry(self) -> None:
        points = self.model[
            "routing_field_points"
        ]
        generated_points = self.gmodel[
            "routing_field_points"
        ]
        self.assertEqual(
            generated_points,
            points,
        )
        for number in range(1, 16):
            prefix = f"Topic {number} hand-off:"
            source_matches = [
                point
                for point in points
                if str(point).startswith(prefix)
            ]
            generated_matches = [
                point
                for point in generated_points
                if str(point).startswith(prefix)
            ]
            self.assertEqual(
                len(source_matches),
                1,
            )
            self.assertEqual(
                len(generated_matches),
                1,
            )

    def test_semantic_groups(self) -> None:
        combined = (
            json.dumps(
                {
                    "fact": self.fact,
                    "profile": self.profile,
                    "model": self.model,
                    "importance": self.importance,
                },
                ensure_ascii=False,
            )
            + TOPIC_SHEET.read_text(
                encoding="utf-8"
            )
        ).casefold()
        for markers in SEMANTIC_CLUSTERS.values():
            for marker in markers:
                self.assertIn(
                    marker.casefold(),
                    combined,
                )


ANCHOR_MARKER_CASES = {'selection_process_ownership': ('Topic 16', 'Topic 1~15', '수명주기', '선정 의사결정'), 'operating_case_matrix': ('upstream·downstream pressure', 'temperature', 'phase', 'composition', 'property source'), 'pressure_reference_consistency': ('absolute', 'gauge', 'static head', 'line-loss', 'pressure-rating'), 'fluid_phase_composition_properties': ('two-phase', 'density', 'viscosity', 'vapor pressure', 'compressibility'), 'specialist_calculation_handoff': ('Topic 1~15', 'margin', 'limitation', 'reviewer', 'hand-off record'), 'selection_matrix_tradeoff': ('capacity', 'controllability', 'maintainability', 'evidence quality', '가중점수'), 'valve_body_flow_path_selection': ('Globe', 'ball', 'butterfly', 'pressure recovery', 'maintenance access'), 'actuator_thrust_torque_supply_minimum': ('worst-case thrust·torque', 'friction', 'minimum credible supply', 'spring range', 'required speed'), 'datasheet_completeness_and_units': ('governing case', 'units', 'reference condition', 'property source', 'documentation'), 'vendor_bid_technical_comparison': ('datasheet revision', 'case basis', 'actuator', 'delivery', 'lifecycle support'), 'fat_functional_performance_acceptance': ('FAT', 'seat leakage', 'fail action', 'response', 'acceptance criterion'), 'field_feedback_moc_revalidation': ('as-found·as-left', 'vendor notice', 'failure database', 'MOC', 'periodic revalidation')}


def _make_anchor_marker_test(
    anchor_id: str,
    markers: tuple[str, ...],
) -> Callable[
    [GeneratedContractRegressionTests],
    None,
]:
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
        _make_anchor_marker_test(
            _anchor_id,
            _markers,
        ),
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
        self.assertTrue(
            result.get("matched"),
            msg=result,
        )
        self.assertEqual(
            selected_topic(result),
            expected,
            msg=result,
        )


ROUTER_CASES = (('integrated_process', 'control valve integrated selection process operating case lifecycle', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('design_basis_vendor', 'control valve process design basis datasheet vendor evaluation', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('process_envelope', 'control valve pressure temperature flow fluid selection workflow', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('operating_cases', 'minimum normal maximum startup shutdown upset valve selection', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('package_selection', 'control valve body trim characteristic actuator material package selection', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('specialist_integration', 'control valve sizing authority cavitation noise result integration', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('vendor_deviation', 'control valve datasheet requisition vendor bid deviation comparison', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('acceptance', 'control valve FAT SAT commissioning acceptance workflow', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('lifecycle', 'control valve reliability maintainability spares lifecycle cost', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('moc_feedback', 'control valve field feedback MOC revalidation selection criteria', 'control_valve_selection_process_pressure_temperature_flow_media_lifecycle'), ('topic1', 'Unbalanced force actuator thrust packing friction fail-safe spring sizing을 계산하시오.', 'control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe'), ('topic2', 'Equal percentage linear quick opening inherent installed characteristic을 비교하시오.', 'control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening'), ('topic3', 'Deadband stiction hysteresis response time을 동적으로 시험하시오.', 'control_valve_deadband_stiction_response_time_positioner_dynamic_performance'), ('topic4', 'Globe ball butterfly body와 pneumatic electric hydraulic actuator를 비교하시오.', 'control_valve_types_globe_rotary_body_actuator_selection'), ('topic5', 'Valve authority rangeability installed gain과 turndown을 설명하시오.', 'control_valve_authority_rangeability_gain_installed_performance'), ('topic6', 'Liquid Cv Kv Reynolds correction과 piping factor를 계산하시오.', 'control_valve_sizing_cv_kv_reynolds_liquid_selection'), ('topic7', 'Gas sizing expansion factor critical pressure ratio choked flow를 계산하시오.', 'control_valve_gas_sizing_choked_flow_critical_pressure_ratio'), ('topic8', 'Cavitation flashing liquid choked flow anti-cavitation trim을 설명하시오.', 'control_valve_cavitation_flashing_choked_flow_damage_prevention'), ('topic9', 'Aerodynamic hydrodynamic noise와 low-noise trim을 설명하시오.', 'control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim'), ('topic10', 'Balanced trim unbalanced trim sealing structure와 actuator force를 비교하시오.', 'balanced_trim_unbalanced_trim_structure_sealing_applications'), ('topic11', 'Positioner I/P converter booster accessory calibration을 설명하시오.', 'control_valve_positioner_ip_converter_booster_accessories_calibration'), ('topic12', 'Smart positioner valve signature diagnostics predictive maintenance를 설명하시오.', 'smart_positioner_diagnostics_valve_signature_predictive_maintenance'), ('topic13', 'Seat leakage shutoff class packing fugitive emission을 설명하시오.', 'control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions'), ('topic14', 'High-flow low-flow high-temperature cryogenic particle severe service를 평가하시오.', 'control_valve_severe_service_high_low_flow_temperature_cryogenic_particles'), ('topic15', 'SIF final element safe state ESD valve PST proof-test PFDavg PFH를 평가하시오.', 'final_control_element_sil_sis_esd_valve_partial_stroke_test'))


def _make_router_test(
    case: tuple[Any, ...],
) -> Callable[
    [RouterRegressionTests],
    None,
]:
    name, question, expected, *rest = case
    answer_text = (
        str(rest[0])
        if rest
        else ""
    )

    def test(
        self: RouterRegressionTests,
    ) -> None:
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


class SelectionLifecycleSemanticRegressionTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.fact = load_json(
            SOURCE_DIR / "fact_anchor.json"
        )
        cls.model = load_json(
            SOURCE_DIR / "model_answer.json"
        )

    def test_contextual_negative_candidate_extraction(
        self,
    ) -> None:
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
        rule_id = (
            "vendor_sizing_accepted_without_"
            "independent_check"
        )
        answer_text = negative_samples()[rule_id]
        candidates = (
            extract_logic_evidence_candidates(
                answer_text,
                self.profile,
            )
        )
        self.assertTrue(candidates)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value={
                "verdict": "fatal",
                "confidence": 0.99,
                "reason": (
                    "Vendor sizing을 독립 검토 없이 "
                    "승인하는 오류다."
                ),
                "findings": [{
                    "candidate_id":
                        candidates[0]["id"],
                    "rule_id": rule_id,
                    "severity": "fatal",
                    "message":
                        "vendor sizing accepted directly",
                    "correct_rule": (
                        "입력, units, correction, warning과 "
                        "guarantee basis를 독립 검토한다."
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
        self.assertEqual(
            result["mode"],
            "fatal",
        )
        self.assertEqual(
            result["findings"][0][
                "affected_layers"
            ],
            ["C"],
        )

    def test_mocked_safe_verifier(self) -> None:
        candidates = (
            extract_logic_evidence_candidates(
                SAFE_ANSWER,
                self.profile,
            )
        )
        self.assertTrue(candidates)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value={
                "verdict": "pass",
                "confidence": 1.0,
                "reason": (
                    "Operating case, specialist hand-off, "
                    "acceptance와 lifecycle boundary를 "
                    "유지한다."
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
        self.assertEqual(
            result["mode"],
            "pass",
        )
        self.assertIsNone(
            result["recommended_ceiling"]
        )

    def test_positive_semantic_clusters(self) -> None:
        rows = cluster_coverage(
            POSITIVE_ANSWER
        )
        self.assertEqual(
            set(rows),
            set(SEMANTIC_CLUSTERS),
        )
        self.assertTrue(
            all(rows.values()),
            msg=rows,
        )

    def test_formula_source_markers(self) -> None:
        combined = (
            REQUIREMENTS.read_text(
                encoding="utf-8"
            )
            + TOPIC_SHEET.read_text(
                encoding="utf-8"
            )
        ).casefold()
        for marker in FORMULA_SOURCE_IDS:
            self.assertIn(
                marker.casefold(),
                combined,
            )

    def test_safe_answer_markers(self) -> None:
        normalized = " ".join(
            SAFE_ANSWER.casefold().split()
        )
        for marker in (
            "process design basis",
            "operating case matrix",
            "pressure reference",
            "topic 1 hand-off",
            "topic 15 hand-off",
            "mandatory gate",
            "vendor bid",
            "deviation",
            "fat sat commissioning",
            "reliability availability maintainability",
            "lifecycle cost",
            "moc revalidation",
        ):
            self.assertIn(
                " ".join(
                    marker.casefold().split()
                ),
                normalized,
            )

    def test_all_handoff_answer_markers(self) -> None:
        points = self.model[
            "routing_field_points"
        ]
        for number in range(1, 16):
            prefix = f"Topic {number} hand-off:"
            self.assertEqual(
                sum(
                    str(point).startswith(prefix)
                    for point in points
                ),
                1,
            )


def _formula_capacity_utilization(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            capacity_utilization(
                80.0,
                100.0,
            ),
            0.8,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        capacity_utilization(1.0, 0.0)


def _formula_capacity_margin(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            capacity_margin(
                100.0,
                80.0,
            ),
            0.25,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        capacity_margin(1.0, 0.0)


def _formula_installed_range_requirement(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            installed_range_requirement(
                100.0,
                5.0,
            ),
            20.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        installed_range_requirement(1.0, 0.0)


def _formula_range_margin(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            range_margin(
                30.0,
                20.0,
            ),
            0.5,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        range_margin(1.0, 0.0)


def _formula_valve_authority(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            valve_authority(
                40.0,
                60.0,
            ),
            0.4,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        valve_authority(0.0, 0.0)


def _formula_hydraulic_power(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            hydraulic_power(
                200000.0,
                0.01,
            ),
            2000.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        hydraulic_power(-1.0, 1.0)


def _formula_availability(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            availability(
                990.0,
                10.0,
            ),
            0.99,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        availability(0.0, 1.0)


def _formula_downtime_cost(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            downtime_cost(
                2.0,
                5.0,
                1000.0,
            ),
            10000.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        downtime_cost(-1.0, 1.0, 1.0)


def _formula_discounted_cost(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            discounted_cost(
                [1000.0, 110.0],
                0.1,
            ),
            1100.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        discounted_cost([1.0], -1.0)


def _formula_weighted_score(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            weighted_score(
                [0.6, 0.4],
                [80.0, 90.0],
            ),
            84.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        weighted_score(
            [0.5, 0.4],
            [1.0, 1.0],
        )


def _formula_requirement_coverage(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            requirement_coverage(
                45.0,
                50.0,
            ),
            0.9,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        requirement_coverage(2.0, 1.0)


def _formula_deviation_closure_rate(
    testcase: unittest.TestCase,
) -> None:
    testcase.assertTrue(
        math.isclose(
            deviation_closure_rate(
                18.0,
                20.0,
            ),
            0.9,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    with testcase.assertRaises(ValueError):
        deviation_closure_rate(2.0, 1.0)


FORMULA_CASES = {
    "capacity_utilization":
        _formula_capacity_utilization,
    "capacity_margin":
        _formula_capacity_margin,
    "installed_range_requirement":
        _formula_installed_range_requirement,
    "range_margin":
        _formula_range_margin,
    "valve_authority":
        _formula_valve_authority,
    "hydraulic_power":
        _formula_hydraulic_power,
    "availability":
        _formula_availability,
    "downtime_cost":
        _formula_downtime_cost,
    "discounted_cost":
        _formula_discounted_cost,
    "weighted_score":
        _formula_weighted_score,
    "requirement_coverage":
        _formula_requirement_coverage,
    "deviation_closure_rate":
        _formula_deviation_closure_rate,
}


def _make_formula_test(
    function: Callable[
        [unittest.TestCase],
        None,
    ],
) -> Callable[
    [SelectionLifecycleSemanticRegressionTests],
    None,
]:
    def test(
        self:
            SelectionLifecycleSemanticRegressionTests,
    ) -> None:
        function(self)

    return test


for _formula_id, _formula_function in FORMULA_CASES.items():
    setattr(
        SelectionLifecycleSemanticRegressionTests,
        f"test_formula_{_formula_id}",
        _make_formula_test(
            _formula_function
        ),
    )


if __name__ == "__main__":
    loader = unittest.defaultTestLoader
    suite = loader.loadTestsFromModule(
        sys.modules[__name__]
    )
    test_count = suite.countTestCases()
    print(
        "TOPIC16_FOCUSED_TEST_INVENTORY "
        f"classes=3 tests={test_count}"
    )
    if test_count != 65:
        raise RuntimeError(
            "Expected 65 focused tests, "
            f"discovered {test_count}"
        )
    result = unittest.TextTestRunner(
        verbosity=2
    ).run(suite)
    print(
        "TOPIC16_FOCUSED_RESULT "
        f"run={result.testsRun} "
        f"failures={len(result.failures)} "
        f"errors={len(result.errors)}"
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
