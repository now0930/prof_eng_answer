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

TOPIC = 'control_valve_severe_service_high_low_flow_temperature_cryogenic_particles'
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

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['severe_service_combined_risk_definition', 'operating_case_envelope', 'process_fluid_geometry_consequence_chain', 'high_flow_velocity_area_relation', 'high_flow_kinetic_energy_density', 'high_flow_hydraulic_power', 'downstream_piping_outlet_effect', 'staged_pressure_reduction_distribution', 'high_flow_erosion_vibration', 'low_flow_minimum_controllable_flow', 'installed_rangeability_handoff', 'microflow_trim_geometry', 'low_reynolds_laminar_correction', 'low_flow_plugging_sensitivity', 'high_temperature_material_strength_oxidation', 'thermal_expansion_clearance', 'differential_growth_binding_leakage', 'packing_gasket_seat_coating_temperature', 'thermal_cycling_heat_soak', 'actuator_positioner_heat_isolation', 'low_temperature_toughness_brittle_fracture', 'cryogenic_thermal_contraction', 'extended_bonnet_packing_isolation', 'cryogenic_vaporization_two_phase', 'trapped_liquid_cavity_pressure', 'icing_condensation_insulation_interface', 'particle_characterization', 'slurry_erosion_impingement', 'fibrous_sticky_polymerizing_plugging', 'valve_geometry_solids_passage', 'cage_multihole_particle_sensitivity', 'hardfacing_coating_ceramic', 'purge_flushing_cleanout', 'orientation_flow_direction_self_cleaning', 'corrosion_erosion_corrosion', 'high_viscosity_non_newtonian_sizing', 'multiphase_entrained_gas_uncertainty', 'seat_packing_material_tradeoff', 'actuator_breakaway_thermal_friction_handoff', 'cavitation_flashing_noise_handoff', 'min_normal_max_transient_cases', 'fouling_wear_clearance_trend', 'inspection_monitoring_trim_replacement', 'specification_material_sizing_workflow', 'vendor_qualification_purchaser_acceptance', 'maintainability_spares_turnaround', 'lifecycle_cost_energy_service_life', 'repair_reverification_worst_case']
EXPECTED_FATAL_IDS = ['severe_service_single_threshold', 'high_flow_velocity_irrelevant', 'hydraulic_power_universal_damage_law', 'staging_always_prevents_damage', 'catalog_rangeability_equals_min_flow', 'microflow_trim_never_plugs', 'laminar_correction_unnecessary', 'material_strength_temperature_independent', 'thermal_expansion_constraint_irrelevant', 'packing_limit_independent_of_heat', 'low_temperature_only_viscosity_issue', 'extended_bonnet_always_optional', 'trapped_liquid_pressure_impossible', 'icing_condensation_harmless', 'particle_size_alone_sufficient', 'hardfacing_always_solves_erosion', 'multihole_trim_universally_best_for_slurry', 'full_port_always_self_cleaning', 'unlimited_purge_is_safe', 'corrosion_erosion_identical', 'stokes_settling_universal', 'multiphase_equals_single_phase', 'diagnostics_replace_inspection', 'vendor_label_guarantees_lifecycle']
EXPECTED_MAJOR_IDS = ['fixed_velocity_limit', 'fixed_hydraulic_power_limit', 'fixed_minimum_flow_ratio', 'fixed_micro_orifice', 'fixed_material_temperature_limit', 'fixed_extended_bonnet_length', 'fixed_particle_size_limit', 'fixed_slurry_velocity', 'fixed_purge_rate', 'fixed_hardness_requirement', 'fixed_inspection_interval', 'fixed_wear_limit']

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
    "severe", "service", "flow", "temperature", "cryogenic",
    "particle", "slurry", "erosion", "valve", "trim",
}
NEGATIVE_RULE_IDS = (
    "severe_service_single_threshold",
    "hydraulic_power_universal_damage_law",
    "catalog_rangeability_equals_min_flow",
    "material_strength_temperature_independent",
    "stokes_settling_universal",
    "vendor_label_guarantees_lifecycle",
)

POSITIVE_ANSWER = """
Severe service는 operating envelope와 failure consequence로 정의한다.
High-flow에서는 local velocity, hydraulic power와 pressure staging을 검토한다.
Low-flow에서는 minimum controllable flow, micro-flow trim과 plugging을 검토한다.
High-temperature에서는 thermal expansion, differential growth와 heat soak를 확인한다.
Cryogenic service에서는 extended bonnet, thermal contraction과 cavity pressure를 확인한다.
Particle, slurry와 fibrous service에서는 hardfacing, ceramic, purge와 clean-out access를
비교한다. Inspection, spare trim, vendor qualification과 repair verification을
lifecycle에 연결한다.
"""

SAFE_ANSWER = """
Severe service는 pressure, flow, temperature, phase, particle, geometry, material와
consequence가 결합된 operating envelope이다. Hydraulic power와 erosive severity는
screening proxy이며 universal damage law가 아니다. Catalog rangeability와 installed
minimum controllable flow를 구분한다. High-temperature service는 pressure derating,
thermal expansion와 differential growth를 확인한다. Cryogenic service는 material
toughness, extended bonnet, thermal contraction와 cavity-pressure relief를 검토한다.
Particle service는 size distribution, concentration, hardness와 shape를 정의한다.
Stokes settling은 creeping-flow·dilute·spherical-particle domain에서만 사용한다.
Diagnostics는 inspection을 대체하지 않는다. Vendor qualification은 purchaser
operating envelope, reference installation와 acceptance test로 검증한다.
"""

SEMANTIC_CLUSTERS = {
    "framework": ("severe service", "operating envelope", "failure consequence"),
    "high_flow": ("high-flow", "local velocity", "hydraulic power", "pressure staging"),
    "low_flow": ("low-flow", "minimum controllable flow", "micro-flow trim", "plugging"),
    "thermal": ("high-temperature", "thermal expansion", "differential growth", "heat soak"),
    "cryogenic": ("cryogenic", "extended bonnet", "thermal contraction", "cavity pressure"),
    "particles": ("particle", "slurry", "fibrous"),
    "materials": ("hardfacing", "ceramic", "purge", "clean-out"),
    "lifecycle": ("inspection", "spare trim", "vendor qualification", "repair verification"),
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


def flow_velocity(flow: float, area: float) -> float:
    if flow < 0.0 or area <= 0.0:
        raise ValueError
    return flow / area


def specific_kinetic_energy(velocity: float) -> float:
    return velocity * velocity / 2.0


def hydraulic_power(delta_p: float, flow: float) -> float:
    if delta_p < 0.0 or flow < 0.0:
        raise ValueError
    return delta_p * flow


def erosive_severity(density: float, velocity: float, area: float) -> float:
    if density < 0.0 or velocity < 0.0 or area <= 0.0:
        raise ValueError
    return density * velocity**3 * area


def installed_turndown(maximum_flow: float, minimum_flow: float) -> float:
    if minimum_flow <= 0.0 or maximum_flow < minimum_flow:
        raise ValueError
    return maximum_flow / minimum_flow


def minimum_flow_margin(available: float, required: float) -> float:
    if required <= 0.0:
        raise ValueError
    return (available - required) / required


def thermal_expansion(alpha: float, length: float, delta_t: float) -> float:
    if length < 0.0:
        raise ValueError
    return alpha * length * delta_t


def differential_growth(
    alpha_1: float,
    alpha_2: float,
    length: float,
    delta_t: float,
) -> float:
    if length < 0.0:
        raise ValueError
    return (alpha_1 - alpha_2) * length * delta_t


def heat_leak(u_value: float, area: float, delta_t: float) -> float:
    if u_value < 0.0 or area < 0.0:
        raise ValueError
    return u_value * area * delta_t


def vaporization_fraction(
    heat_input: float,
    mass_flow: float,
    latent_heat: float,
) -> float:
    if heat_input < 0.0 or mass_flow <= 0.0 or latent_heat <= 0.0:
        raise ValueError
    return heat_input / (mass_flow * latent_heat)


def stokes_settling(
    particle_density: float,
    fluid_density: float,
    gravity: float,
    diameter: float,
    viscosity: float,
) -> float:
    if gravity < 0.0 or diameter < 0.0 or viscosity <= 0.0:
        raise ValueError
    return (
        (particle_density - fluid_density)
        * gravity
        * diameter**2
        / (18.0 * viscosity)
    )


def wear_delta(current: float, baseline: float) -> float:
    return current - baseline


def wear_rate(first: float, second: float, t1: float, t2: float) -> float:
    if t2 <= t1:
        raise ValueError
    return (second - first) / (t2 - t1)


def matched_profile_key_terms(text: str, profile: dict[str, Any]) -> list[str]:
    normalized = " ".join(text.casefold().split())
    terms = (profile.get("candidate_extraction") or {}).get("key_terms") or []
    return [
        str(term) for term in terms
        if " ".join(str(term).casefold().split()) in normalized
    ]


def negative_samples() -> dict[str, str]:
    source = load_json(SOURCE_DIR / "fact_anchor.json")
    by_id = {row["id"]: row for row in source["fatal_wrong_claims"]}
    result: dict[str, str] = {}
    for rule_id in NEGATIVE_RULE_IDS:
        row = by_id[rule_id]
        wrong = str(row.get("wrong_claim") or row.get("claim") or "")
        correction = str(row.get("correction") or row.get("correct_rule") or "")
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
        testcase.assertIn(" ".join(marker.casefold().split()), normalized)


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
        cls.by_id = {row["id"]: row["statement"] for row in cls.fact["anchors"]}

    def test_manifest_alignment(self) -> None:
        source_ids = sorted(
            path.name for path in (ROOT / "rubrics" / "topic_packs").iterdir()
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
        self.assertEqual([row["id"] for row in self.fact["anchors"]], EXPECTED_ANCHOR_IDS)
        self.assertEqual([row["id"] for row in self.gfact["anchors"]], EXPECTED_ANCHOR_IDS)
        self.assertEqual(
            [row["id"] for row in self.fact["fatal_wrong_claims"]],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.profile["major_checks"]],
            EXPECTED_MAJOR_IDS,
        )

    def test_anchor_projection_alignment(self) -> None:
        source_by = {row["id"]: row for row in self.fact["anchors"]}
        generated_by = {row["id"]: row for row in self.gfact["anchors"]}
        for anchor_id in EXPECTED_ANCHOR_IDS:
            for key in ANCHOR_PROJECTION_KEYS:
                self.assertEqual(
                    generated_by[anchor_id][key],
                    source_by[anchor_id][key],
                )

    def test_anchor_schema_projection_boundary(self) -> None:
        source_fields = set().union(*(set(row) for row in self.fact["anchors"]))
        generated_fields = set().union(*(set(row) for row in self.gfact["anchors"]))
        self.assertEqual(
            source_fields - generated_fields - set(ANCHOR_PROJECTION_KEYS),
            set(),
        )
        self.assertEqual(
            generated_fields - source_fields - set(ANCHOR_PROJECTION_KEYS),
            {"expected", "name", "support_terms"},
        )

    def test_fatal_major_alignment(self) -> None:
        self.assertEqual(self.gfact["fatal_wrong_claims"], self.fact["fatal_wrong_claims"])
        self.assertEqual(self.profile["fatal_conditions"], self.fact["fatal_wrong_claims"])
        self.assertEqual(
            self.profile["major_checks"],
            self.logic["llm_profile"]["major_checks"],
        )

    def test_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(self.glogic["fatal_checks"], [])
        self.assertEqual(self.glogic["major_checks"], [])
        self.assertEqual(self.glogic["question_type_checks"], [])
        self.assertEqual(self.profile["candidate_extraction"]["rules"], [])
        self.assertEqual(len(self.profile["candidate_extraction"]["key_terms"]), 657)
        policy = self.profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")
        self.assertEqual(policy["affected_layers"], ["C"])

    def test_model_importance(self) -> None:
        self.assertEqual(len(self.model["expected_question_patterns"]), 10)
        self.assertEqual(len(self.model["recommended_outline"]), 8)
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        self.assertEqual(
            set().union(
                *(set(row["anchor_refs"]) for row in self.model["recommended_outline"])
            ),
            anchor_set,
        )
        aliases = {str(alias).casefold() for alias in self.model["routing_aliases"]}
        self.assertFalse(BROAD_ALIASES & aliases)
        self.assertEqual(self.gmodel["routing_aliases"], self.model["routing_aliases"])
        self.assertEqual(self.gimportance, self.importance)
        self.assertEqual(self.importance["difficulty"], "FIELD_APPLICATION")
        self.assertEqual(self.importance["selection_importance"], "CORE_MUST_PREPARE")
        self.assertEqual(self.importance["question_type"], "COMPARE_SELECTION")

    def test_explicit_boundaries(self) -> None:
        combined = (
            json.dumps(
                {"fact": self.fact, "logic": self.logic, "model": self.model},
                ensure_ascii=False,
            )
            + TOPIC_SHEET.read_text(encoding="utf-8")
        ).casefold()
        for marker in (
            "topic 1", "topic 3", "topic 4", "topic 5", "topic 6",
            "topic 7", "topic 8", "topic 9", "topic 10", "topic 12",
            "topic 13", "topic 15", "topic 16",
        ):
            self.assertIn(marker, combined)


ANCHOR_MARKER_CASES: dict[str, tuple[str, ...]] = {
    "severe_service_combined_risk_definition": (
        "severe service", "process condition", "fluid property",
        "valve geometry", "failure consequence",
    ),
    "operating_case_envelope": (
        "minimum", "normal", "maximum", "startup", "shutdown",
        "cleaning", "upset condition", "operating envelope",
    ),
    "high_flow_hydraulic_power": (
        "hydraulic power", "pressure drop", "screening",
        "pressure staging", "cavitation", "flashing",
    ),
    "microflow_trim_geometry": (
        "small orifice", "needle", "multi-hole", "long-path geometry",
        "resolution", "repeatability", "plugging",
    ),
    "high_temperature_material_strength_oxidation": (
        "allowable strength", "pressure derating", "oxidation", "scaling", "creep",
    ),
    "extended_bonnet_packing_isolation": (
        "cryogenic extended bonnet", "packing", "cold zone",
        "vapor space", "required length", "orientation",
    ),
    "particle_characterization": (
        "size distribution", "concentration", "hardness",
        "shape", "density", "settling tendency",
    ),
    "fibrous_sticky_polymerizing_plugging": (
        "fibrous", "sticky", "polymerizing fluid", "dead zone",
        "bridging", "deposit", "plugging",
    ),
    "hardfacing_coating_ceramic": (
        "hardfacing", "hard coating", "ceramic",
        "thermal shock", "repairability",
    ),
    "specification_material_sizing_workflow": (
        "specification", "operating envelope", "material review",
        "sizing", "geometry selection", "vendor review",
        "commissioning", "maintenance",
    ),
}


def _make_anchor_marker_test(
    anchor_id: str,
    markers: tuple[str, ...],
) -> Callable[[GeneratedContractRegressionTests], None]:
    def test(self: GeneratedContractRegressionTests) -> None:
        assert_markers(self, self.by_id[anchor_id], markers)
    return test


for _anchor_id, _markers in ANCHOR_MARKER_CASES.items():
    setattr(
        GeneratedContractRegressionTests,
        f"test_anchor_markers_{_anchor_id}",
        _make_anchor_marker_test(_anchor_id, _markers),
    )


class RouterRegressionTests(unittest.TestCase):
    def assert_route(self, question: str, expected: str, answer_text: str = "") -> None:
        result = route_reference(question, expected, answer_text)
        self.assertTrue(result.get("matched"), msg=result)
        self.assertEqual(selected_topic(result), expected, msg=result)


ROUTER_CASES = (
    ("framework", "Control valve severe service operating envelope와 failure consequence를 설명하시오.", TOPIC),
    ("high_flow", "High-flow local velocity hydraulic power pressure staging downstream erosion을 비교하시오.", TOPIC),
    ("low_flow", "Low-flow minimum controllable flow installed rangeability를 설명하시오.", TOPIC),
    ("microflow", "Micro-flow small-orifice needle multi-hole trim plugging을 비교하시오.", TOPIC),
    ("high_temperature", "High-temperature material strength pressure derating thermal expansion heat soak를 평가하시오.", TOPIC),
    ("cryogenic", "Cryogenic toughness thermal contraction extended bonnet cavity pressure를 설명하시오.", TOPIC),
    ("particle", "Particle size distribution concentration hardness shape로 valve를 선정하시오.", TOPIC),
    ("slurry_fibrous", "Slurry erosion fibrous sticky polymerizing plugging을 진단하시오.", TOPIC),
    ("material_purge", "Hardfacing ceramic purge flushing clean-out을 비교하시오.", TOPIC),
    ("multiphase_lifecycle", "Multiphase uncertainty inspection spare trim vendor qualification repair verification을 설명하시오.", TOPIC),
    ("topic1", "Unbalanced force actuator thrust packing friction fail-safe spring sizing을 계산하시오.", TOPIC_1),
    ("topic3", "Deadband stiction hysteresis response time을 동적으로 시험하시오.", TOPIC_3),
    ("topic4", "Globe ball butterfly body와 pneumatic electric hydraulic actuator를 비교하시오.", TOPIC_4),
    ("topic5", "Valve authority installed gain rangeability turndown 이론을 설명하시오.", TOPIC_5),
    ("topic6", "Liquid Cv Kv Reynolds correction과 piping factor를 계산하시오.", TOPIC_6),
    ("topic7", "Gas sizing expansion factor critical pressure ratio choked flow를 계산하시오.", TOPIC_7),
    ("topic8", "Cavitation flashing liquid choked flow anti-cavitation trim을 설명하시오.", TOPIC_8),
    ("topic9", "Aerodynamic hydrodynamic noise prediction과 low-noise trim을 설명하시오.", TOPIC_9),
    ("topic13", "Seat leakage shutoff class packing fugitive emission as-found as-left를 설명하시오.", TOPIC_13),
    (
        "question_only",
        "High-flow low-flow high-temperature cryogenic particle slurry severe-service valve를 비교 선정하시오.",
        TOPIC,
        "Cv sizing cavitation noise seat leakage positioner calibration valve signature actuator spring",
    ),
)


def _make_router_test(case: tuple[Any, ...]) -> Callable[[RouterRegressionTests], None]:
    name, question, expected, *rest = case
    answer_text = str(rest[0]) if rest else ""
    def test(self: RouterRegressionTests) -> None:
        self.assert_route(str(question), str(expected), answer_text)
    return test


for _case in ROUTER_CASES:
    setattr(
        RouterRegressionTests,
        f"test_route_{_case[0]}",
        _make_router_test(_case),
    )


class SevereServiceSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry("logic_check_profiles.generated.json", "profiles")
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_contextual_negative_candidate_extraction(self) -> None:
        samples = negative_samples()
        self.assertEqual(set(samples), set(NEGATIVE_RULE_IDS))
        for rule_id, answer_text in samples.items():
            matched = matched_profile_key_terms(answer_text, self.profile)
            self.assertGreaterEqual(len(matched), 2, msg=(rule_id, matched))
            self.assertTrue(
                extract_logic_evidence_candidates(answer_text, self.profile),
                msg=rule_id,
            )

    def test_mocked_fatal_verifier(self) -> None:
        rule_id = "severe_service_single_threshold"
        answer_text = negative_samples()[rule_id]
        candidates = extract_logic_evidence_candidates(answer_text, self.profile)
        self.assertTrue(candidates)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value={
                "verdict": "fatal",
                "confidence": 0.99,
                "reason": "Severe service를 단일 threshold로 단정한다.",
                "findings": [{
                    "candidate_id": candidates[0]["id"],
                    "rule_id": rule_id,
                    "severity": "fatal",
                    "message": "Single-threshold severe-service claim",
                    "correct_rule": "Combined operating envelope를 사용한다.",
                }],
            },
        ):
            result = verify_logic_with_llm(answer_text, TOPIC)
        self.assertTrue(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "fatal")
        self.assertEqual(result["findings"][0]["affected_layers"], ["C"])

    def test_mocked_safe_verifier(self) -> None:
        candidates = extract_logic_evidence_candidates(SAFE_ANSWER, self.profile)
        self.assertTrue(candidates)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value={
                "verdict": "pass",
                "confidence": 1.0,
                "reason": "Operating envelope와 domain boundary를 유지한다.",
                "findings": [],
            },
        ):
            result = verify_logic_with_llm(SAFE_ANSWER, TOPIC)
        self.assertFalse(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "pass")
        self.assertIsNone(result["recommended_ceiling"])

    def test_positive_semantic_clusters(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(SEMANTIC_CLUSTERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_formula_source_markers(self) -> None:
        combined = json.dumps(
            {"fact": self.fact, "profile": self.profile},
            ensure_ascii=False,
        ).casefold()
        for marker in (
            "flow velocity q over a",
            "specific kinetic energy velocity squared over two",
            "hydraulic power delta pressure times flow",
            "erosive severity rho v cubed area proxy",
            "ri qmax qmin installed turndown",
            "minimum flow margin available required",
            "thermal expansion alpha l delta t",
            "heat leak u a delta t",
            "vaporization fraction heat input mass flow latent heat",
            "stokes settling density difference diameter viscosity",
            "wear rate time ordered measurement",
        ):
            self.assertIn(marker, combined)

    def test_safe_answer_markers(self) -> None:
        normalized = " ".join(SAFE_ANSWER.casefold().split())
        for marker in (
            "screening proxy",
            "minimum controllable flow",
            "pressure derating",
            "extended bonnet",
            "cavity-pressure relief",
            "size distribution",
            "creeping-flow",
            "diagnostics는 inspection을 대체하지 않는다",
            "purchaser operating envelope",
        ):
            self.assertIn(" ".join(marker.casefold().split()), normalized)


def _formula_velocity(testcase: unittest.TestCase) -> None:
    testcase.assertEqual(flow_velocity(10.0, 2.0), 5.0)
    with testcase.assertRaises(ValueError):
        flow_velocity(1.0, 0.0)


def _formula_energy(testcase: unittest.TestCase) -> None:
    testcase.assertEqual(specific_kinetic_energy(4.0), 8.0)
    testcase.assertEqual(hydraulic_power(200.0, 0.5), 100.0)
    with testcase.assertRaises(ValueError):
        hydraulic_power(-1.0, 1.0)


def _formula_erosive(testcase: unittest.TestCase) -> None:
    testcase.assertEqual(erosive_severity(2.0, 3.0, 4.0), 216.0)
    with testcase.assertRaises(ValueError):
        erosive_severity(1.0, 1.0, 0.0)


def _formula_turndown(testcase: unittest.TestCase) -> None:
    testcase.assertEqual(installed_turndown(100.0, 5.0), 20.0)
    testcase.assertTrue(
        math.isclose(
            minimum_flow_margin(12.0, 10.0),
            0.2,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )


def _formula_thermal(testcase: unittest.TestCase) -> None:
    testcase.assertTrue(
        math.isclose(
            thermal_expansion(1.0e-5, 10.0, 100.0),
            0.01,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    testcase.assertTrue(
        math.isclose(
            differential_growth(2.0e-5, 1.0e-5, 10.0, 100.0),
            0.01,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )


def _formula_heat_vapor(testcase: unittest.TestCase) -> None:
    testcase.assertEqual(heat_leak(2.0, 3.0, 4.0), 24.0)
    testcase.assertEqual(vaporization_fraction(20.0, 2.0, 5.0), 2.0)


def _formula_settling(testcase: unittest.TestCase) -> None:
    testcase.assertTrue(
        math.isclose(
            stokes_settling(3.0, 1.0, 9.0, 0.1, 1.0),
            0.01,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )


def _formula_wear(testcase: unittest.TestCase) -> None:
    testcase.assertEqual(wear_delta(8.0, 5.0), 3.0)
    testcase.assertEqual(wear_rate(10.0, 14.0, 2.0, 4.0), 2.0)


FORMULA_CASES: dict[str, Callable[[unittest.TestCase], None]] = {
    "velocity": _formula_velocity,
    "energy": _formula_energy,
    "erosive": _formula_erosive,
    "turndown": _formula_turndown,
    "thermal": _formula_thermal,
    "heat_vapor": _formula_heat_vapor,
    "settling": _formula_settling,
    "wear": _formula_wear,
}


def _make_formula_test(
    function: Callable[[unittest.TestCase], None],
) -> Callable[[SevereServiceSemanticRegressionTests], None]:
    def test(self: SevereServiceSemanticRegressionTests) -> None:
        function(self)
    return test


for _name, _function in FORMULA_CASES.items():
    setattr(
        SevereServiceSemanticRegressionTests,
        f"test_formula_{_name}",
        _make_formula_test(_function),
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
