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

TOPIC = 'control_valve_cavitation_flashing_choked_flow_damage_prevention'
TOPIC_2 = 'control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening'
TOPIC_3 = 'control_valve_deadband_stiction_response_time_positioner_dynamic_performance'
TOPIC_4 = 'control_valve_types_globe_rotary_body_actuator_selection'
TOPIC_5 = 'control_valve_authority_rangeability_gain_installed_performance'
TOPIC_6 = 'control_valve_sizing_cv_kv_reynolds_liquid_selection'
TOPIC_7 = 'control_valve_gas_sizing_choked_flow_critical_pressure_ratio'

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['liquid_pressure_profile_scope', 'absolute_pressure_basis_liquid_phase_change', 'vapor_pressure_operating_temperature', 'thermodynamic_critical_pressure_meaning', 'vena_contracta_minimum_pressure', 'vapor_formation_condition', 'downstream_pressure_recovery', 'pressure_recovery_factor_fl_meaning', 'fl_direction_and_cavitation_susceptibility', 'fl_style_trim_travel_dependency', 'critical_pressure_ratio_factor_ff', 'bare_valve_liquid_choked_limit', 'piping_geometry_factor_fp_liquid', 'combined_recovery_factor_flp', 'fitting_adjusted_liquid_choked_limit', 'effective_liquid_sizing_pressure_drop', 'liquid_choked_flow_capacity_limit', 'liquid_choked_flow_not_zero', 'cavitation_classification', 'flashing_classification', 'cavitation_flashing_commonality', 'cavitation_flashing_difference', 'cavitation_inception_development_damage_levels', 'cavitation_damage_mechanism', 'flashing_damage_mechanism', 'choked_vapor_damage_axes_separated', 'liquid_phase_change_operating_cases', 'increase_downstream_pressure_prevention', 'reduce_liquid_temperature_prevention', 'reduce_total_pressure_drop_prevention', 'pressure_drop_staging_prevention', 'higher_fl_low_recovery_selection', 'flashing_service_geometry_location', 'anti_cavitation_trim_not_flashing_cure', 'vendor_crosscheck_liquid_phase_change', 'topic9_topic14_handoff']
EXPECTED_FATAL_IDS = ['control_valve_liquid_use_gauge_pressure_for_phase_change', 'control_valve_vapor_pressure_independent_of_temperature', 'control_valve_critical_pressure_equals_vapor_pressure', 'control_valve_lower_fl_means_lower_pressure_recovery', 'control_valve_fl_universal_constant', 'control_valve_flp_always_equals_fl_with_fittings', 'control_valve_liquid_use_max_actual_choked_drop', 'control_valve_liquid_choked_means_zero_flow', 'control_valve_liquid_choked_flow_increases_indefinitely', 'control_valve_cavitation_defined_by_p2_below_pv', 'control_valve_flashing_means_bubble_collapse', 'control_valve_cavitation_flashing_identical', 'control_valve_all_cavitation_immediate_severe_damage', 'control_valve_all_liquid_choked_flow_is_damaging_cavitation', 'control_valve_flashing_always_collapses_downstream', 'control_valve_anti_cavitation_trim_recondenses_flashing', 'control_valve_larger_valve_always_solves_cavitation', 'control_valve_hard_material_alone_prevents_phase_change_damage', 'control_valve_use_gas_xt_y_formula_for_liquid_choke', 'control_valve_single_normal_case_sufficient_for_cavitation']
EXPECTED_MAJOR_IDS = ['control_valve_ff_formula_without_standard', 'control_valve_fixed_fl_by_valve_type', 'control_valve_pvc_inversion_universal_exact', 'control_valve_fixed_cavitation_index_threshold', 'control_valve_fixed_normal_travel_cavitation', 'control_valve_downstream_pressure_increase_always_available', 'control_valve_fixed_anti_cavitation_stage_count', 'control_valve_material_life_prediction_without_data']

BROAD_ALIASES = {
    "cavitation",
    "flashing",
    "choked flow",
    "vapor pressure",
    "pressure recovery",
    "FL",
    "FF",
    "valve damage",
    "erosion",
    "noise",
    "liquid sizing",
}

POSITIVE_ANSWER = """
P1, P2, Pvc, Pv와 Pc는 absolute pressure를 사용하고 operating temperature의
vapor pressure와 critical pressure를 확인한다. Vena contracta에서 minimum
local pressure가 형성되고 downstream pressure recovery가 발생한다. Pressure
recovery factor FL, low FL, high pressure recovery와 selected travel을 확인한다.
Liquid critical pressure ratio factor FF, piping geometry factor FP와 combined
recovery factor FLP를 계산한다. Bare valve choked limit와 fitting adjusted
choked limit를 비교하고 effective sizing pressure drop은 minimum selection을
적용한다. Cavitation classification은 bubble collapse, flashing classification은
persistent vapor와 two phase flow로 구분한다. Pressure drop staging과 multi
stage trim을 검토하고 flashing service geometry와 erosion path를 확인한다.
Minimum normal maximum, startup shutdown, vendor cavitation sizing과 hand
calculation을 수행한다. Topic 9 hydrodynamic noise와 Topic 14 material로
상세 검토를 hand-off한다.
""".strip()

SAFE_ANSWER = """
P1, P2, Pvc, Pv와 Pc는 absolute pressure이다. Operating temperature의 Pv를
사용한다. Actual pressure drop과 liquid choked limit 중 작은 값을 적용한다.
Pvc<Pv이고 P2>Pv이면 cavitation, P2≤Pv이면 flashing이다. Choked flow는
zero flow가 아니며 damage severity는 별도로 판정한다.
""".strip()

NEGATIVE_SAMPLES = {
    "control_valve_liquid_use_gauge_pressure_for_phase_change": (
        "absolute pressure, P1 P2 Pvc, vapor pressure, critical pressure와 "
        "unit consistency를 검토하지만 gauge pressure를 P1, P2, Pv와 Pc에 "
        "그대로 사용한다고 주장한다."
    ),
    "control_valve_lower_fl_means_lower_pressure_recovery": (
        "pressure recovery factor FL, low FL, high pressure recovery, lower Pvc와 "
        "cavitation susceptibility를 설명하면서 low FL은 lower pressure "
        "recovery라고 주장한다."
    ),
    "control_valve_liquid_use_max_actual_choked_drop": (
        "effective sizing pressure drop, minimum selection, actual pressure drop, "
        "choked limit와 delta P sizing을 비교하지만 두 값 중 큰 값을 "
        "사용한다고 주장한다."
    ),
    "control_valve_flashing_means_bubble_collapse": (
        "flashing classification, Pvc below Pv, P2 at or below Pv, persistent vapor와 "
        "two phase flow를 설명하면서 flashing의 핵심은 bubble collapse라고 "
        "주장한다."
    ),
    "control_valve_anti_cavitation_trim_recondenses_flashing": (
        "anti cavitation trim, pressure drop staging, not flashing cure, "
        "not recondensation과 persistent vapor를 검토하지만 flashing vapor를 "
        "재응축한다고 주장한다."
    ),
}

SEMANTIC_CLUSTERS = {
    "pressure_basis": (
        "absolute pressure",
        "operating temperature",
        "vapor pressure",
        "critical pressure",
    ),
    "pressure_profile": (
        "vena contracta",
        "minimum local pressure",
        "downstream pressure recovery",
    ),
    "recovery": (
        "pressure recovery factor fl",
        "low fl",
        "high pressure recovery",
        "selected travel",
    ),
    "factors": (
        "liquid critical pressure ratio factor ff",
        "piping geometry factor fp",
        "combined recovery factor flp",
    ),
    "choked": (
        "bare valve choked limit",
        "fitting adjusted choked limit",
        "effective sizing pressure drop",
        "minimum selection",
    ),
    "classification": (
        "cavitation classification",
        "bubble collapse",
        "flashing classification",
        "persistent vapor",
        "two phase flow",
    ),
    "mitigation": (
        "pressure drop staging",
        "multi stage trim",
        "flashing service geometry",
        "erosion path",
    ),
    "cases_handoff": (
        "minimum normal maximum",
        "startup shutdown",
        "vendor cavitation sizing",
        "hand calculation",
        "topic 9 hydrodynamic noise",
        "topic 14 material",
    ),
}


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


def liquid_ff(pv: float, pc: float) -> float:
    if pv < 0 or pc <= 0 or pv > pc:
        raise ValueError
    return 0.96 - 0.28 * math.sqrt(pv / pc)


def bare_choked_limit(
    p1: float,
    pv: float,
    ff_value: float,
    fl: float,
) -> float:
    if p1 <= 0 or pv < 0 or ff_value <= 0 or fl <= 0:
        raise ValueError
    pressure_term = p1 - ff_value * pv
    if pressure_term <= 0:
        raise ValueError
    return fl * fl * pressure_term


def fitting_choked_limit(
    p1: float,
    pv: float,
    ff_value: float,
    flp: float,
    fp: float,
) -> float:
    if p1 <= 0 or pv < 0 or ff_value <= 0 or flp <= 0 or fp <= 0:
        raise ValueError
    pressure_term = p1 - ff_value * pv
    if pressure_term <= 0:
        raise ValueError
    return (flp / fp) ** 2 * pressure_term


def effective_drop(actual: float, limit: float) -> float:
    if actual < 0 or limit <= 0:
        raise ValueError
    return min(actual, limit)


def vena_contracta_pressure(
    p1: float,
    actual_drop: float,
    fl: float,
) -> float:
    if p1 <= 0 or actual_drop < 0 or fl <= 0:
        raise ValueError
    return p1 - actual_drop / (fl * fl)


def classify_phase(
    pvc: float,
    pv: float,
    p2: float,
) -> str:
    if min(pvc, pv, p2) <= 0:
        raise ValueError
    if pvc >= pv:
        return "single_phase"
    if p2 > pv:
        return "cavitation"
    return "flashing"


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
        (profile.get("candidate_extraction") or {})
        .get("key_terms")
        or []
    )
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
            for path in (
                ROOT / "rubrics" / "topic_packs"
            ).iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        manifest_ids = [
            row["topic_id"]
            for row in load_json(
                GENERATED_DIR
                / "topic_pack_manifest.generated.json"
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
            [
                row["id"]
                for row in self.fact["fatal_wrong_claims"]
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
        self.assertEqual(
            len(self.profile["fatal_conditions"]),
            20,
        )
        self.assertEqual(len(set(EXPECTED_ANCHOR_IDS)), 36)

    def test_semantic_score_and_deterministic_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(self.glogic["fatal_checks"], [])
        self.assertEqual(self.glogic["major_checks"], [])
        self.assertEqual(
            self.profile["candidate_extraction"]["rules"],
            [],
        )
        policy = self.profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")
        self.assertEqual(policy["affected_layers"], ["C"])
        self.assertEqual(
            self.profile["output_contract"][
                "excluded_score_layers"
            ],
            ["D", "E"],
        )

    def test_patterns_outline_aliases_and_importance(self) -> None:
        patterns = self.model["expected_question_patterns"]
        outlines = self.model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        anchors = set(EXPECTED_ANCHOR_IDS)
        self.assertTrue(
            all(
                set(row["required_anchor_ids"]) <= anchors
                for row in patterns
            )
        )
        self.assertEqual(
            set().union(
                *(
                    set(row["anchor_refs"])
                    for row in outlines
                )
            ),
            anchors,
        )
        aliases = self.model["routing_aliases"]
        self.assertFalse(BROAD_ALIASES & set(aliases))
        self.assertEqual(
            self.gmodel["topic_aliases"],
            aliases,
        )
        self.assertEqual(
            self.gmodel["routing_aliases"],
            aliases,
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
            self.importance["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )

    def test_pressure_and_thermodynamic_property_markers(self) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        absolute = by_id[
            "absolute_pressure_basis_liquid_phase_change"
        ]
        for marker in (
            "absolute pressure",
            "P1",
            "P2",
            "Pvc",
            "Pv",
            "Pc",
        ):
            self.assertIn(marker, absolute)
        self.assertIn(
            "operating temperature",
            by_id["vapor_pressure_operating_temperature"],
        )
        self.assertIn(
            "thermodynamic critical pressure",
            by_id["thermodynamic_critical_pressure_meaning"],
        )
        self.assertIn(
            "Pvc",
            by_id["vena_contracta_minimum_pressure"],
        )

    def test_recovery_factor_and_choked_limit_markers(self) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "manufacturer coefficient",
            by_id["pressure_recovery_factor_fl_meaning"],
        )
        self.assertIn(
            "낮은 FL",
            by_id[
                "fl_direction_and_cavitation_susceptibility"
            ],
        )
        self.assertIn(
            "travel",
            by_id["fl_style_trim_travel_dependency"],
        )
        self.assertIn(
            "Pv/Pc",
            by_id["critical_pressure_ratio_factor_ff"],
        )
        self.assertIn(
            "FL²(P1-FF·Pv)",
            by_id["bare_valve_liquid_choked_limit"],
        )
        self.assertIn(
            "(FLP/FP)²(P1-FF·Pv)",
            by_id[
                "fitting_adjusted_liquid_choked_limit"
            ],
        )
        self.assertIn(
            "작은 값",
            by_id["effective_liquid_sizing_pressure_drop"],
        )

    def test_classification_damage_and_axis_markers(self) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        cavitation = by_id["cavitation_classification"]
        flashing = by_id["flashing_classification"]
        for marker in ("Pvc<Pv", "P2>Pv", "collapse"):
            self.assertIn(marker, cavitation)
        for marker in ("Pvc<Pv", "P2≤Pv", "downstream"):
            self.assertIn(marker, flashing)
        self.assertIn(
            "microjet",
            by_id["cavitation_damage_mechanism"],
        )
        self.assertIn(
            "two-phase",
            by_id["flashing_damage_mechanism"],
        )
        self.assertIn(
            "서로 다른 판정축",
            by_id["choked_vapor_damage_axes_separated"],
        )

    def test_prevention_operating_case_and_handoff_markers(self) -> None:
        combined = json.dumps(
            {
                "fact": self.fact,
                "logic": self.logic,
                "model": self.model,
            },
            ensure_ascii=False,
        ) + TOPIC_SHEET.read_text(encoding="utf-8")
        for marker in (
            "Minimum",
            "normal",
            "maximum",
            "startup",
            "shutdown",
            "pressure drop",
            "multi-stage",
            "Higher FL",
            "flashing service",
            "Topic 6",
            "Topic 7",
            "Topic 9",
            "Topic 14",
        ):
            self.assertIn(marker, combined)

    def test_section_aware_fatal_corrections(self) -> None:
        by_id = {
            row["id"]: row
            for row in self.fact["fatal_wrong_claims"]
        }
        checks = {
            "control_valve_liquid_use_gauge_pressure_for_phase_change":
                "absolute pressure",
            "control_valve_lower_fl_means_lower_pressure_recovery":
                "큰 pressure recovery",
            "control_valve_liquid_use_max_actual_choked_drop":
                "작은 값",
            "control_valve_liquid_choked_means_zero_flow":
                "유량 정지가 아니다",
            "control_valve_cavitation_defined_by_p2_below_pv":
                "Pvc<Pv",
            "control_valve_flashing_means_bubble_collapse":
                "persistent downstream vapor",
            "control_valve_anti_cavitation_trim_recondenses_flashing":
                "재응축 장치가 아니다",
            "control_valve_use_gas_xt_y_formula_for_liquid_choke":
                "Liquid choked flow는 FF",
        }
        for rule_id, marker in checks.items():
            correction = str(
                by_id[rule_id].get("correction")
                or by_id[rule_id].get("correct_rule")
                or ""
            )
            self.assertIn(marker, correction)


class RouterRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(
            GENERATED_DIR / "model_answers.generated.json"
        )
        cls.answer_by_topic = {
            row["topic_id"]: row
            for row in cls.bank["answers"]
        }
        for topic_id in (
            TOPIC,
            TOPIC_2,
            TOPIC_3,
            TOPIC_4,
            TOPIC_5,
            TOPIC_6,
            TOPIC_7,
        ):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(
                    f"missing topic {topic_id}"
                )

    @classmethod
    def qtype(cls, topic_id: str) -> dict[str, Any]:
        return {
            "primary_type": {
                "id": cls.answer_by_topic[topic_id][
                    "question_type"
                ],
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
        self.assertEqual(
            selected_topic(result),
            expected,
            msg=result,
        )

    def test_pressure_profile_and_property_routes(self) -> None:
        questions = (
            "Liquid control valve의 P1→Pvc→P2 pressure profile과 pressure recovery를 설명하시오.",
            "Operating temperature의 Pv와 thermodynamic critical pressure Pc를 사용하는 cavitation sizing을 설명하시오.",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assert_primary(
                    self.route(question, TOPIC),
                    TOPIC,
                )

    def test_factor_fitting_and_choked_limit_routes(self) -> None:
        questions = (
            "FL, FF, vapor pressure와 liquid choked pressure-drop limit의 관계를 설명하시오.",
            "Reducer·expander가 직접 연결된 valve의 FP, FLP와 fitting-adjusted choked limit를 설명하시오.",
            "Actual pressure drop과 choked limit 중 작은 값을 사용하는 liquid sizing을 설명하시오.",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assert_primary(
                    self.route(question, TOPIC),
                    TOPIC,
                )

    def test_cavitation_and_flashing_routes(self) -> None:
        questions = (
            "Pvc, Pv와 P2를 이용하여 cavitation과 flashing을 비교하시오.",
            "Pvc<Pv이고 P2>Pv인 cavitation과 P2≤Pv인 flashing을 구분하시오.",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assert_primary(
                    self.route(question, TOPIC),
                    TOPIC,
                )

    def test_damage_and_prevention_routes(self) -> None:
        questions = (
            "Cavitation의 inception·development·damage mechanism과 현장 징후를 설명하시오.",
            "Flashing의 persistent two-phase flow와 erosion mechanism 및 valve installation 대책을 설명하시오.",
            "Cavitation prevention을 위한 higher FL과 multi-stage anti-cavitation trim을 설명하시오.",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assert_primary(
                    self.route(question, TOPIC),
                    TOPIC,
                )

    def test_operating_case_and_integrated_routes(self) -> None:
        questions = (
            "Minimum·normal·maximum 및 startup·shutdown 조건에서 cavitation·flashing risk를 진단하시오.",
            "P1, P2, Pv, Pc, FF, FL, FP, FLP와 selected travel을 이용한 liquid severe-service valve 선정 절차를 설명하시오.",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assert_primary(
                    self.route(question, TOPIC),
                    TOPIC,
                )

    def test_topic6_nonchoked_liquid_boundary(self) -> None:
        result = self.route(
            "비초크 액체 Cv·Kv, SG, Fp와 FR Reynolds correction을 설명하시오.",
            TOPIC_6,
        )
        self.assert_primary(result, TOPIC_6)

    def test_topic7_gas_choked_boundary(self) -> None:
        result = self.route(
            "Gas standard volume, absolute P1, Fγ, xT, xTP와 expansion factor Y를 이용한 choked gas sizing을 설명하시오.",
            TOPIC_7,
        )
        self.assert_primary(result, TOPIC_7)

    def test_topic2_to_topic5_boundaries(self) -> None:
        cases = [
            (
                "Linear, equal-percentage와 quick-opening characteristic를 비교하시오.",
                TOPIC_2,
            ),
            (
                "Deadband, stiction, response time과 positioner hunting을 설명하시오.",
                TOPIC_3,
            ),
            (
                "Globe·rotary body와 pneumatic·electric actuator를 비교하시오.",
                TOPIC_4,
            ),
            (
                "Valve Authority, rangeability와 installed gain을 설명하시오.",
                TOPIC_5,
            ),
        ]
        for question, expected in cases:
            with self.subTest(expected=expected):
                self.assert_primary(
                    self.route(question, expected),
                    expected,
                )

    def test_question_only_routing_survives_answer_contamination(self) -> None:
        result = self.route(
            "비초크 액체 Cv·Kv와 Reynolds correction을 설명하시오.",
            TOPIC_6,
            answer_text=(
                "P1→Pvc→P2, Pv, Pc, FF, FL, FP, FLP, "
                "cavitation, flashing과 liquid choked flow를 "
                "상세히 작성한다."
            ),
        )
        self.assert_primary(result, TOPIC_6)
        self.assertEqual(
            self.answer_by_topic[TOPIC]["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )
        aliases = set(
            self.answer_by_topic[TOPIC]["routing_aliases"]
        )
        self.assertFalse(BROAD_ALIASES & aliases)


class FormulaSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.fact = load_json(
            SOURCE_DIR / "fact_anchor.json"
        )

    def test_ff_numeric_domain_and_direction(self) -> None:
        self.assertTrue(
            math.isclose(liquid_ff(0.0, 10.0), 0.96)
        )
        self.assertTrue(
            math.isclose(liquid_ff(10.0, 10.0), 0.68)
        )
        self.assertGreater(
            liquid_ff(1.0, 10.0),
            liquid_ff(4.0, 10.0),
        )
        for args in (
            (-1.0, 10.0),
            (1.0, 0.0),
            (11.0, 10.0),
        ):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    liquid_ff(*args)

    def test_bare_choked_limit_direction_and_domain(self) -> None:
        ff_value = liquid_ff(1.0, 10.0)
        base = bare_choked_limit(
            10.0,
            1.0,
            ff_value,
            0.8,
        )
        self.assertGreater(
            bare_choked_limit(
                10.0,
                1.0,
                ff_value,
                0.9,
            ),
            base,
        )
        self.assertGreater(
            bare_choked_limit(
                20.0,
                1.0,
                ff_value,
                0.8,
            ),
            base,
        )
        self.assertLess(
            bare_choked_limit(
                10.0,
                2.0,
                ff_value,
                0.8,
            ),
            base,
        )
        with self.assertRaises(ValueError):
            bare_choked_limit(
                0.0,
                1.0,
                ff_value,
                0.8,
            )

    def test_fitting_reference_identity_and_domain(self) -> None:
        ff_value = liquid_ff(1.0, 10.0)
        bare = bare_choked_limit(
            10.0,
            1.0,
            ff_value,
            0.8,
        )
        reference = fitting_choked_limit(
            10.0,
            1.0,
            ff_value,
            0.8,
            1.0,
        )
        self.assertTrue(math.isclose(bare, reference))
        self.assertGreater(
            fitting_choked_limit(
                10.0,
                1.0,
                ff_value,
                0.9,
                1.0,
            ),
            reference,
        )
        with self.assertRaises(ValueError):
            fitting_choked_limit(
                10.0,
                1.0,
                ff_value,
                0.8,
                0.0,
            )

    def test_effective_drop_minimum_and_choked_plateau(self) -> None:
        limit = 5.0
        self.assertTrue(
            math.isclose(effective_drop(3.0, limit), 3.0)
        )
        self.assertTrue(
            math.isclose(effective_drop(7.0, limit), limit)
        )
        values = [
            effective_drop(actual, limit)
            for actual in (5.0, 7.0, 10.0)
        ]
        self.assertTrue(
            all(
                math.isclose(value, limit)
                for value in values
            )
        )
        with self.assertRaises(ValueError):
            effective_drop(-1.0, limit)

    def test_vena_contracta_direction_and_domain(self) -> None:
        self.assertLess(
            vena_contracta_pressure(10.0, 4.0, 0.7),
            vena_contracta_pressure(10.0, 4.0, 0.9),
        )
        self.assertLess(
            vena_contracta_pressure(10.0, 6.0, 0.8),
            vena_contracta_pressure(10.0, 3.0, 0.8),
        )
        with self.assertRaises(ValueError):
            vena_contracta_pressure(10.0, 4.0, 0.0)

    def test_phase_classification_boundaries_and_domain(self) -> None:
        self.assertEqual(
            classify_phase(5.0, 4.0, 6.0),
            "single_phase",
        )
        self.assertEqual(
            classify_phase(3.0, 4.0, 5.0),
            "cavitation",
        )
        self.assertEqual(
            classify_phase(3.0, 4.0, 4.0),
            "flashing",
        )
        self.assertEqual(
            classify_phase(3.0, 4.0, 3.0),
            "flashing",
        )
        with self.assertRaises(ValueError):
            classify_phase(0.0, 4.0, 5.0)

    def test_positive_sample_semantic_cluster_coverage(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(
            set(rows),
            set(SEMANTIC_CLUSTERS),
        )
        self.assertTrue(
            all(rows.values()),
            msg=rows,
        )

    def test_contextual_negative_candidate_extraction(self) -> None:
        fatal_set = {
            row["id"]
            for row in self.fact["fatal_wrong_claims"]
        }
        self.assertTrue(
            set(NEGATIVE_SAMPLES) <= fatal_set
        )
        for rule_id, answer_text in NEGATIVE_SAMPLES.items():
            with self.subTest(rule_id=rule_id):
                matched = matched_profile_key_terms(
                    answer_text,
                    self.profile,
                )
                self.assertGreaterEqual(
                    len(matched),
                    3,
                    msg={
                        "rule_id": rule_id,
                        "matched": matched,
                    },
                )
                candidates = (
                    extract_logic_evidence_candidates(
                        answer_text,
                        self.profile,
                    )
                )
                self.assertTrue(
                    candidates,
                    msg={
                        "rule_id": rule_id,
                        "matched": matched,
                    },
                )

    def test_mocked_fatal_and_safe_verifier_contracts(self) -> None:
        rule_id = (
            "control_valve_liquid_choked_means_zero_flow"
        )
        answer_text = (
            "liquid choked flow, capacity limit, downstream pressure, "
            "flow saturation과 pressure drop limit를 설명하면서 "
            "유량이 0이라고 주장한다."
        )
        candidates = extract_logic_evidence_candidates(
            answer_text,
            self.profile,
        )
        self.assertTrue(candidates)
        mocked_fatal = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": (
                "Liquid choked flow를 zero flow로 설명하였다."
            ),
            "findings": [{
                "candidate_id": candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message": "Liquid choked-flow meaning error",
                "correct_rule": (
                    "Liquid choked flow는 capacity limit이며 "
                    "유량 정지가 아니다."
                ),
            }],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_fatal,
        ):
            fatal_result = verify_logic_with_llm(
                answer_text,
                TOPIC,
            )
        self.assertTrue(
            fatal_result["fatal_error_detected"],
            msg=fatal_result,
        )
        self.assertEqual(fatal_result["mode"], "fatal")
        self.assertEqual(
            fatal_result["findings"][0][
                "affected_layers"
            ],
            ["C"],
        )
        self.assertEqual(
            fatal_result["recommended_ceiling"],
            10.0,
        )

        mocked_safe = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": (
                "Absolute pressure, choked limit와 "
                "phase classification이 정확하다."
            ),
            "findings": [],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_safe,
        ):
            safe_result = verify_logic_with_llm(
                SAFE_ANSWER,
                TOPIC,
            )
        self.assertFalse(
            safe_result["fatal_error_detected"],
            msg=safe_result,
        )
        self.assertEqual(safe_result["mode"], "pass")
        self.assertIsNone(
            safe_result["recommended_ceiling"]
        )
        self.assertEqual(safe_result["findings"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
