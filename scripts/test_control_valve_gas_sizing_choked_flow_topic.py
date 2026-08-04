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

TOPIC = 'control_valve_gas_sizing_choked_flow_critical_pressure_ratio'
TOPIC_2 = 'control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening'
TOPIC_3 = 'control_valve_deadband_stiction_response_time_positioner_dynamic_performance'
TOPIC_4 = 'control_valve_types_globe_rotary_body_actuator_selection'
TOPIC_5 = 'control_valve_authority_rangeability_gain_installed_performance'
TOPIC_6 = 'control_valve_sizing_cv_kv_reynolds_liquid_selection'

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['compressible_control_valve_sizing_scope', 'flow_basis_standard_actual_mass_distinction', 'standard_condition_definition_required', 'absolute_pressure_required', 'absolute_temperature_required', 'pressure_drop_ratio_definition', 'pressure_ratio_direction', 'gas_property_input_selection', 'compressibility_factor_meaning', 'heat_capacity_ratio_factor', 'valve_pressure_drop_ratio_factor_meaning', 'xT_valve_style_trim_travel_dependency', 'piping_geometry_factor_gas_service', 'xTP_fitting_adjusted_factor', 'no_fitting_reference_condition', 'choked_pressure_ratio_limit', 'sizing_ratio_minimum_selection', 'expansion_factor_physical_meaning', 'expansion_factor_subcritical_relation', 'expansion_factor_bounds', 'subcritical_flow_behavior', 'choked_flow_physical_meaning', 'choked_flow_not_zero_flow', 'choked_flow_downstream_independence', 'standard_volume_formula_structure', 'mass_flow_formula_structure', 'unit_constant_equation_dependency', 'required_vs_rated_gas_coefficient', 'selected_travel_xT_iteration', 'minimum_normal_maximum_gas_cases', 'fail_open_maximum_flow_case', 'steam_vapor_property_boundary', 'aerodynamic_noise_handoff', 'vendor_hand_calculation_crosscheck_gas']
EXPECTED_FATAL_IDS = ['control_valve_gas_use_gauge_pressure_in_ratio', 'control_valve_gas_pressure_ratio_uses_p2_denominator', 'control_valve_standard_actual_mass_flow_identical', 'control_valve_gas_ignore_absolute_temperature', 'control_valve_gas_z_always_one', 'control_valve_gas_fgamma_always_one', 'control_valve_gas_xT_universal_constant', 'control_valve_gas_xT_independent_of_travel', 'control_valve_gas_xTP_always_equals_xT_with_fittings', 'control_valve_gas_use_max_pressure_ratio', 'control_valve_gas_y_increases_with_pressure_ratio', 'control_valve_gas_y_below_two_thirds_standard_relation', 'control_valve_gas_choked_means_zero_flow', 'control_valve_gas_choked_flow_increases_indefinitely', 'control_valve_gas_use_liquid_equation_unchanged', 'control_valve_gas_capacity_independent_of_inlet_pressure', 'control_valve_gas_required_equals_rated', 'control_valve_gas_single_operating_point_sufficient', 'control_valve_wet_steam_same_as_single_phase_gas']
EXPECTED_MAJOR_IDS = ['control_valve_fgamma_formula_without_standard', 'control_valve_fixed_compressibility_factor', 'control_valve_fixed_xT_by_valve_type', 'control_valve_fixed_normal_travel_gas', 'control_valve_exact_N_constant_without_units', 'control_valve_xTP_always_lower_than_xT', 'control_valve_choked_always_sonic_at_outlet', 'control_valve_steam_quality_optional']

BROAD_ALIASES = {
    "gas", "steam", "vapor", "choked flow", "pressure ratio",
    "expansion factor", "compressibility", "valve sizing",
    "sizing", "Cv", "xT", "Y",
}

POSITIVE_ANSWER = """
Standard volume, actual volume와 mass flow의 flow basis를 구분하고 base pressure와
base temperature를 정의한다. P1, P2는 absolute pressure이고 T1은 absolute
temperature이다. Molecular weight, gas specific gravity, inlet density,
specific heat ratio와 compressibility factor Z1을 선택한다. Pressure drop ratio
x=ΔP/P1, F gamma, xT와 choked pressure ratio를 계산한다. Reducer, expander,
FP와 xTP를 반영한다. Sizing ratio는 작은 값을 선택하고 expansion factor Y는
감소하며 2/3 이상 1 이하이다. Standard volume formula와 mass flow formula,
required Cv, rated trim capacity와 selected travel을 검토한다. Minimum, normal,
maximum과 fail-open maximum gas flow를 계산한다. Wet steam은 two-phase로
분리하고 aerodynamic noise는 Topic 9로 hand-off한다. Vendor sizing result를
hand calculation으로 검증한다.
""".strip()

SAFE_ANSWER = """
P1과 P2는 absolute pressure, T1은 absolute temperature이다. Actual x와
FγxT 또는 FγxTP 중 작은 값을 사용한다. Expansion factor Y는 common relation에서
2/3 이상 1 이하이다. Choked flow는 flow stop이 아니며 selected travel의 xT로
required Cv를 반복 계산한다.
""".strip()

NEGATIVE_SAMPLES = {
    "control_valve_gas_use_gauge_pressure_in_ratio": (
        "control valve gas sizing, absolute pressure, P1 absolute, P2 absolute, "
        "gauge conversion과 pressure drop ratio를 검토하지만 gauge pressure를 "
        "그대로 x=ΔP/P1의 P1과 P2로 사용한다고 주장한다."
    ),
    "control_valve_gas_use_max_pressure_ratio": (
        "sizing ratio, minimum selection, actual pressure ratio, choked limit, "
        "critical pressure ratio와 flow limit를 비교하면서 큰 값을 사용한다고 주장한다."
    ),
    "control_valve_gas_y_increases_with_pressure_ratio": (
        "expansion factor Y, subcritical expansion factor, pressure ratio, "
        "Y decrease, gas expansion과 density decrease를 설명하면서 Y가 증가한다고 주장한다."
    ),
    "control_valve_gas_choked_means_zero_flow": (
        "choked flow, compressible flow limit, maximum mass flow, flow continues, "
        "not blockage와 downstream pressure를 설명하면서 유량이 0이라고 주장한다."
    ),
}

SEMANTIC_CLUSTERS = {
    "basis": ("standard volume", "actual volume", "mass flow", "base pressure", "base temperature"),
    "absolute": ("absolute pressure", "absolute temperature", "p1", "p2", "t1"),
    "properties": ("molecular weight", "gas specific gravity", "inlet density", "specific heat ratio", "z1"),
    "ratio": ("pressure drop ratio", "δp/p1", "f gamma", "xt", "choked pressure ratio"),
    "fitting_y": ("reducer", "expander", "fp", "xtp", "expansion factor y"),
    "selection": ("standard volume formula", "mass flow formula", "required cv", "rated trim capacity", "selected travel"),
    "cases": ("minimum", "normal", "maximum", "fail-open", "maximum gas flow"),
    "boundaries": ("wet steam", "two-phase", "aerodynamic noise", "topic 9", "vendor sizing", "hand calculation"),
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


def pressure_ratio(p1: float, p2: float) -> float:
    if p1 <= 0 or p2 < 0 or p2 > p1:
        raise ValueError
    return (p1 - p2) / p1


def choked_limit(f_gamma: float, x_t: float) -> float:
    if f_gamma <= 0 or x_t <= 0:
        raise ValueError
    return f_gamma * x_t


def sizing_ratio(actual_x: float, limit: float) -> float:
    if actual_x < 0 or limit <= 0:
        raise ValueError
    return min(actual_x, limit)


def expansion_factor(x_sizing: float, f_gamma: float, x_t: float) -> float:
    if x_sizing < 0 or f_gamma <= 0 or x_t <= 0:
        raise ValueError
    raw = 1.0 - x_sizing / (3.0 * f_gamma * x_t)
    return max(2.0 / 3.0, min(1.0, raw))


def standard_term(c: float, p1: float, y: float, x: float, m: float, t1: float, z1: float) -> float:
    if any(value <= 0 for value in (c, p1, y, x, m, t1, z1)):
        raise ValueError
    return c * p1 * y * math.sqrt(x / (m * t1 * z1))


def mass_term(c: float, y: float, x: float, p1: float, rho1: float) -> float:
    if any(value <= 0 for value in (c, y, x, p1, rho1)):
        raise ValueError
    return c * y * math.sqrt(x * p1 * rho1)


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
        for row in (self.fact, self.logic, self.model, self.importance, self.gfact, self.profile, self.glogic, self.gmodel, self.gimportance, self.manifest):
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
        self.assertEqual(len(self.profile["fatal_conditions"]), 19)
        self.assertEqual(len(set(EXPECTED_ANCHOR_IDS)), 34)

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
        anchors = set(EXPECTED_ANCHOR_IDS)
        self.assertTrue(all(set(row["required_anchor_ids"]) <= anchors for row in patterns))
        self.assertEqual(set().union(*(set(row["anchor_refs"]) for row in outlines)), anchors)
        aliases = self.model["routing_aliases"]
        self.assertFalse(BROAD_ALIASES & set(aliases))
        self.assertEqual(self.gmodel["topic_aliases"], aliases)
        self.assertEqual(self.gimportance, self.importance)
        self.assertEqual(self.importance["difficulty"], "FIELD_APPLICATION")
        self.assertEqual(self.importance["question_type"], "CALC_DESIGN")

    def test_absolute_ratio_and_gas_property_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("absolute pressure", by_id["absolute_pressure_required"])
        self.assertIn("absolute temperature", by_id["absolute_temperature_required"])
        self.assertIn("x=(P1-P2)/P1", by_id["pressure_drop_ratio_definition"])
        self.assertIn("molecular weight", by_id["gas_property_input_selection"])
        self.assertIn("Z1", by_id["compressibility_factor_meaning"])

    def test_xt_xtp_y_choked_and_iteration_markers(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("travel", by_id["xT_valve_style_trim_travel_dependency"])
        self.assertIn("reducer", by_id["piping_geometry_factor_gas_service"])
        self.assertIn("FγxT", by_id["choked_pressure_ratio_limit"])
        self.assertIn("FγxTP", by_id["choked_pressure_ratio_limit"])
        self.assertIn("작은 값을 사용", by_id["sizing_ratio_minimum_selection"])
        self.assertIn("2/3", by_id["expansion_factor_bounds"])
        self.assertIn("반복 계산", by_id["selected_travel_xT_iteration"])

    def test_equation_operating_case_and_topic_boundaries(self) -> None:
        by_id = {row["id"]: row["statement"] for row in self.fact["anchors"]}
        self.assertIn("M·T1·Z1", by_id["standard_volume_formula_structure"])
        self.assertIn("P1·ρ1", by_id["mass_flow_formula_structure"])
        combined = json.dumps(
            {"fact": self.fact, "logic": self.logic, "model": self.model},
            ensure_ascii=False,
        ) + TOPIC_SHEET.read_text(encoding="utf-8")
        for marker in ("Minimum", "normal", "maximum", "Fail-open", "Topic 6", "Topic 8", "Topic 9", "aerodynamic noise"):
            self.assertIn(marker, combined)

    def test_section_aware_fatal_corrections(self) -> None:
        by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        checks = {
            "control_valve_gas_use_gauge_pressure_in_ratio": "absolute pressure",
            "control_valve_gas_use_max_pressure_ratio": "작은 값을 사용",
            "control_valve_gas_choked_means_zero_flow": "유량 정지가 아니다",
            "control_valve_gas_choked_flow_increases_indefinitely": "limit에 고정",
            "control_valve_gas_use_liquid_equation_unchanged": "압축성 유체 equation",
        }
        for rule_id, marker in checks.items():
            correction = str(by_id[rule_id].get("correction") or by_id[rule_id].get("correct_rule") or "")
            self.assertIn(marker, correction)


class RouterRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(GENERATED_DIR / "model_answers.generated.json")
        cls.answer_by_topic = {row["topic_id"]: row for row in cls.bank["answers"]}
        for topic_id in (TOPIC, TOPIC_2, TOPIC_3, TOPIC_4, TOPIC_5, TOPIC_6):
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

    def test_flow_basis_and_absolute_conditions_route(self) -> None:
        for question in (
            "Standard volume, actual volume와 mass flow를 구분한 gas valve sizing을 설명하시오.",
            "P1·P2 absolute pressure와 T1 absolute temperature를 사용하는 gas sizing을 설명하시오.",
        ):
            with self.subTest(question=question):
                self.assert_primary(self.route(question, TOPIC), TOPIC)

    def test_ratio_choked_expansion_and_formula_route(self) -> None:
        for question in (
            "Pressure ratio x, Fγ, xT와 choked limit를 계산하시오.",
            "Expansion factor Y의 감소 방향과 2/3 lower bound를 설명하시오.",
            "Standard volume, molecular weight, T1, Z1과 required Cv를 설명하시오.",
            "Mass flow, inlet density와 P1을 이용한 gas valve Cv를 설명하시오.",
        ):
            with self.subTest(question=question):
                self.assert_primary(self.route(question, TOPIC), TOPIC)

    def test_fitting_iteration_fail_open_and_integrated_route(self) -> None:
        for question in (
            "Reducer·expander가 연결된 gas valve의 FP와 xTP를 설명하시오.",
            "Selected travel의 xT와 xTP로 required Cv를 반복 계산하시오.",
            "Fail-open gas valve의 choked maximum flow를 검토하시오.",
            "Flow basis, absolute P·T, Z1, Fγ, xT, xTP, Y와 Cv로 steam valve를 선정하시오.",
        ):
            with self.subTest(question=question):
                self.assert_primary(self.route(question, TOPIC), TOPIC)

    def test_topic6_liquid_sizing_boundary(self) -> None:
        result = self.route(
            "비초크 액체 Cv·Kv, SG, Fp와 FR Reynolds correction을 설명하시오.",
            TOPIC_6,
        )
        self.assert_primary(result, TOPIC_6)

    def test_topic2_to_topic5_boundaries(self) -> None:
        cases = [
            ("Linear, equal-percentage와 quick-opening characteristic를 비교하시오.", TOPIC_2),
            ("Deadband, stiction, response time과 positioner hunting을 설명하시오.", TOPIC_3),
            ("Globe·rotary body와 pneumatic·electric actuator를 비교하시오.", TOPIC_4),
            ("Valve Authority, rangeability와 installed gain을 설명하시오.", TOPIC_5),
        ]
        for question, expected in cases:
            with self.subTest(expected=expected):
                self.assert_primary(self.route(question, expected), expected)

    def test_question_only_routing_survives_answer_contamination(self) -> None:
        result = self.route(
            "비초크 액체 Cv·Kv와 Reynolds correction을 설명하시오.",
            TOPIC_6,
            answer_text=(
                "Gas sizing의 absolute P1, Fγ, xT, xTP, expansion factor Y와 "
                "choked flow를 상세히 작성한다."
            ),
        )
        self.assert_primary(result, TOPIC_6)

    def test_generated_topic7_question_type_is_calc_design(self) -> None:
        self.assertEqual(self.answer_by_topic[TOPIC]["question_type"], "CALC_DESIGN")

    def test_topic7_aliases_do_not_claim_future_detail_topics(self) -> None:
        aliases = set(self.answer_by_topic[TOPIC]["routing_aliases"])
        self.assertNotIn("liquid cavitation", aliases)
        self.assertNotIn("aerodynamic noise prediction", aliases)
        self.assertNotIn("low-noise trim", aliases)


class FormulaSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry("logic_check_profiles.generated.json", "profiles")
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_pressure_ratio_numeric_direction_and_domain(self) -> None:
        self.assertTrue(math.isclose(pressure_ratio(10.0, 8.0), 0.2))
        self.assertGreater(pressure_ratio(10.0, 5.0), pressure_ratio(10.0, 8.0))
        self.assertTrue(math.isclose(pressure_ratio(10.0, 10.0), 0.0))
        for args in ((0.0, 0.0), (-1.0, 0.0), (10.0, -1.0), (10.0, 11.0)):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    pressure_ratio(*args)

    def test_choked_min_selection_and_expansion_bounds(self) -> None:
        limit = choked_limit(1.0, 0.7)
        self.assertTrue(math.isclose(sizing_ratio(0.4, limit), 0.4))
        self.assertTrue(math.isclose(sizing_ratio(0.9, limit), limit))
        y0 = expansion_factor(0.0, 1.0, 0.7)
        ym = expansion_factor(0.35, 1.0, 0.7)
        yc = expansion_factor(0.7, 1.0, 0.7)
        self.assertTrue(math.isclose(y0, 1.0))
        self.assertGreater(y0, ym)
        self.assertGreater(ym, yc)
        self.assertTrue(math.isclose(yc, 2.0 / 3.0))

    def test_choked_plateau(self) -> None:
        limit = 0.7
        values = []
        for actual_x in (0.7, 0.8, 0.95):
            limited = sizing_ratio(actual_x, limit)
            y = expansion_factor(limited, 1.0, 0.7)
            values.append(standard_term(10.0, 10.0, y, limited, 20.0, 300.0, 1.0))
        self.assertTrue(all(math.isclose(value, values[0]) for value in values))

    def test_standard_capacity_monotonicity(self) -> None:
        base = standard_term(10.0, 10.0, 0.9, 0.2, 20.0, 300.0, 1.0)
        self.assertGreater(standard_term(20.0, 10.0, 0.9, 0.2, 20.0, 300.0, 1.0), base)
        self.assertGreater(standard_term(10.0, 20.0, 0.9, 0.2, 20.0, 300.0, 1.0), base)
        self.assertLess(standard_term(10.0, 10.0, 0.8, 0.2, 20.0, 300.0, 1.0), base)
        self.assertLess(standard_term(10.0, 10.0, 0.9, 0.2, 40.0, 300.0, 1.0), base)
        self.assertLess(standard_term(10.0, 10.0, 0.9, 0.2, 20.0, 600.0, 1.0), base)
        self.assertLess(standard_term(10.0, 10.0, 0.9, 0.2, 20.0, 300.0, 2.0), base)

    def test_mass_capacity_monotonicity_and_domains(self) -> None:
        base = mass_term(10.0, 0.9, 0.2, 10.0, 2.0)
        self.assertGreater(mass_term(20.0, 0.9, 0.2, 10.0, 2.0), base)
        self.assertGreater(mass_term(10.0, 0.9, 0.4, 10.0, 2.0), base)
        self.assertGreater(mass_term(10.0, 0.9, 0.2, 20.0, 2.0), base)
        self.assertGreater(mass_term(10.0, 0.9, 0.2, 10.0, 4.0), base)
        self.assertLess(mass_term(10.0, 0.8, 0.2, 10.0, 2.0), base)
        with self.assertRaises(ValueError):
            standard_term(10.0, 0.0, 0.9, 0.2, 20.0, 300.0, 1.0)
        with self.assertRaises(ValueError):
            mass_term(10.0, 0.9, 0.2, 10.0, 0.0)

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
        rule_id = "control_valve_gas_choked_means_zero_flow"
        answer_text = NEGATIVE_SAMPLES[rule_id]
        candidates = extract_logic_evidence_candidates(answer_text, self.profile)
        self.assertTrue(candidates)
        mocked_fatal = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": "Choked flow를 zero flow로 설명하였다.",
            "findings": [{
                "candidate_id": candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message": "Choked-flow meaning error",
                "correct_rule": "Choked flow는 유량 정지가 아니라 mass-flow limit이다.",
            }],
        }
        with patch("logic_llm_verifier._call_ollama_json", return_value=mocked_fatal):
            fatal_result = verify_logic_with_llm(answer_text, TOPIC)
        self.assertTrue(fatal_result["fatal_error_detected"], msg=fatal_result)
        self.assertEqual(fatal_result["mode"], "fatal")
        self.assertEqual(fatal_result["findings"][0]["affected_layers"], ["C"])
        self.assertEqual(fatal_result["recommended_ceiling"], 10.0)

        mocked_safe = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "Absolute condition과 choked boundary가 정확하다.",
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
