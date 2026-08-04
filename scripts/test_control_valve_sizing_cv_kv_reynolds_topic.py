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

from logic_llm_verifier import (  # noqa: E402
    extract_logic_evidence_candidates,
    verify_logic_with_llm,
)
from model_answer_router import find_model_answer_reference  # noqa: E402


TOPIC = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
TOPIC_2 = (
    "control_valve_characteristics_inherent_installed_"
    "equal_percentage_linear_quick_opening"
)
TOPIC_3 = (
    "control_valve_deadband_stiction_response_time_"
    "positioner_dynamic_performance"
)
TOPIC_4 = "control_valve_types_globe_rotary_body_actuator_selection"
TOPIC_5 = "control_valve_authority_rangeability_gain_installed_performance"

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = (
    ROOT
    / "docs"
    / "topic_sheets"
    / f"{TOPIC}.md"
)

EXPECTED_ANCHOR_IDS = [
    "cv_flow_capacity_physical_meaning",
    "cv_reference_definition_us_units",
    "kv_reference_definition_metric_units",
    "cv_kv_conversion_relation",
    "unit_system_consistency",
    "basic_nonchoked_liquid_flow_relation",
    "required_coefficient_inverse_pressure_root",
    "specific_gravity_direction",
    "basic_equation_applicability_boundary",
    "liquid_sizing_input_data",
    "sizing_pressure_drop_definition",
    "required_vs_rated_coefficient",
    "body_size_vs_trim_capacity",
    "minimum_normal_maximum_sizing_points",
    "selected_characteristic_travel_mapping",
    "normal_operating_travel_is_conditional",
    "piping_geometry_factor_meaning",
    "piping_factor_reduces_effective_capacity",
    "piping_factor_geometry_dependency",
    "viscosity_low_reynolds_trigger",
    "valve_reynolds_number_meaning",
    "valve_style_modifier_dependency",
    "reynolds_factor_correction_direction",
    "reynolds_correction_not_arbitrary_constant",
    "reynolds_correction_iteration",
    "small_flow_trim_special_review",
    "corrected_required_vs_available_trim",
    "oversized_valve_selection_consequence",
    "undersized_valve_selection_consequence",
    "cavitation_flashing_choked_screening",
    "complex_fluid_separate_method",
    "vendor_hand_calculation_crosscheck",
]

EXPECTED_FATAL_IDS = [
    "control_valve_cv_is_opening_or_line_size",
    "control_valve_cv_reference_condition_wrong",
    "control_valve_cv_kv_numerically_identical",
    "control_valve_cv_superior_to_kv",
    "control_valve_liquid_flow_linear_with_pressure_drop",
    "control_valve_required_coefficient_decreases_with_density",
    "control_valve_basic_liquid_equation_all_services",
    "control_valve_required_equals_rated_coefficient",
    "control_valve_body_size_equals_trim_capacity",
    "control_valve_single_flow_point_sufficient",
    "control_valve_ignore_attached_fittings",
    "control_valve_fp_below_one_reduces_required_capacity",
    "control_valve_viscosity_never_affects_cv",
    "control_valve_fr_below_one_reduces_required_capacity",
    "control_valve_fr_arbitrary_fixed_value",
    "control_valve_reynolds_iteration_unnecessary",
    "control_valve_catalog_capacity_proves_selection",
    "control_valve_clean_liquid_equation_for_complex_fluid",
]

EXPECTED_MAJOR_IDS = [
    "control_valve_kv_reference_temperature_universal_wording",
    "control_valve_fixed_normal_travel_band",
    "control_valve_fixed_capacity_margin",
    "control_valve_fp_always_one_or_always_required",
    "control_valve_universal_reynolds_threshold",
    "control_valve_universal_fr_correlation",
    "control_valve_cavitation_screening_optional",
]

BROAD_ALIASES = {
    "Cv",
    "Kv",
    "coefficient",
    "flow coefficient",
    "유량계수",
    "valve sizing",
    "sizing",
    "밸브 선정",
    "liquid",
    "Reynolds",
    "viscosity",
    "점도",
}

POSITIVE_ANSWER = """
Cv와 Kv는 control valve flow capacity를 나타내지만 reference condition과
unit system이 다르다. Cv는 60°F water, 1 psi와 US gpm 기준이며 Kv는
water, 1 bar와 m3/h 기준이다. Kv는 약 0.865 Cv이고 Cv는 약 1.156 Kv이다.
Single-phase non-choked turbulent liquid에서 required Cv는
Q times square root of SG divided by valve pressure drop로 계산한다.
Minimum, normal과 maximum flow에서 required coefficient를 각각 계산하고
rated trim capacity 및 operating travel과 비교한다. Reducer와 expander가
직결되면 piping geometry factor Fp를 검토한다. High viscosity와 small-flow
trim에서는 valve Reynolds number와 FR을 계산하고 corrected coefficient가
수렴할 때까지 iteration한다. 마지막으로 cavitation, flashing과 liquid
choked possibility를 screening하고 vendor sizing을 hand calculation과
unit basis로 교차 검증한다.
""".strip()

SAFE_ANSWER = """
Cv와 Kv는 서로 다른 unit system의 valve flow-capacity coefficient이다.
Non-choked turbulent liquid에서 flow는 pressure-drop square root에
비례한다. Fp와 FR이 1보다 작으면 동일 flow의 corrected required
coefficient는 증가할 수 있다. Minimum, normal과 maximum flow를 각각
계산하고 cavitation과 flashing 상세는 별도 Topic에서 검토한다.
""".strip()

NEGATIVE_SAMPLES = {
    "control_valve_cv_kv_numerically_identical": (
        "control valve Cv와 control valve Kv의 Cv Kv conversion 및 unit "
        "consistency를 검토할 때 60 F water, 1 psi, US gpm, 1 bar와 m3/h "
        "reference condition이 달라도 Cv와 Kv 숫자는 항상 동일하므로 "
        "conversion이 필요 없다고 주장한다."
    ),
    "control_valve_liquid_flow_linear_with_pressure_drop": (
        "non-choked liquid와 turbulent liquid의 flow capacity coefficient, "
        "square root pressure drop, specific gravity 및 required Cv 관계를 "
        "설명하면서도 control valve flow는 valve pressure drop에 선형 "
        "비례하고 square root는 사용하지 않는다고 주장한다."
    ),
    "control_valve_fr_below_one_reduces_required_capacity": (
        "viscosity, valve Reynolds number, Reynolds factor, FR, small flow "
        "trim, iterative calculation과 corrected required Cv를 검토하면서도 "
        "FR이 1보다 작아지면 corrected required Cv는 basic Cv보다 "
        "감소한다고 주장한다."
    ),
    "control_valve_basic_liquid_equation_all_services": (
        "non-choked liquid, cavitation screening, flashing, liquid choked, "
        "two phase, non-Newtonian, vendor sizing과 hand calculation의 적용 "
        "경계를 설명하면서도 basic clean-liquid Cv equation을 모든 service에 "
        "그대로 최종 적용할 수 있다고 주장한다."
    ),
}

SEMANTIC_CLUSTERS = {
    "definition_units": (
        "flow capacity",
        "60°f",
        "1 psi",
        "1 bar",
        "unit system",
    ),
    "conversion": (
        "0.865",
        "1.156",
    ),
    "basic_formula": (
        "non-choked",
        "turbulent liquid",
        "square root",
        "valve pressure drop",
    ),
    "operating_points": (
        "minimum",
        "normal",
        "maximum",
        "rated trim capacity",
        "operating travel",
    ),
    "piping": (
        "reducer",
        "expander",
        "piping geometry factor",
    ),
    "reynolds": (
        "viscosity",
        "valve reynolds number",
        "fr",
        "iteration",
    ),
    "service_limits": (
        "cavitation",
        "flashing",
        "liquid choked",
        "vendor sizing",
        "hand calculation",
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def target_entry(filename: str, list_key: str) -> dict[str, Any]:
    data = load_json(GENERATED_DIR / filename)
    matches = [
        item
        for item in data.get(list_key, [])
        if isinstance(item, dict) and item.get("topic_id") == TOPIC
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"{filename}: expected one target, found {len(matches)}"
        )
    return matches[0]


def selected_topic(result: dict[str, Any]) -> str | None:
    primary = result.get("primary_reference") or {}
    if isinstance(primary, dict):
        value = primary.get("topic_id")
        if isinstance(value, str):
            return value
    return None


def required_cv(
    flow: float,
    specific_gravity: float,
    pressure_drop: float,
) -> float:
    if flow < 0:
        raise ValueError("flow must be non-negative")
    if specific_gravity <= 0:
        raise ValueError("specific gravity must be positive")
    if pressure_drop <= 0:
        raise ValueError("pressure drop must be positive")
    return flow * math.sqrt(specific_gravity / pressure_drop)


def corrected_capacity(
    basic: float,
    fp: float,
    fr: float,
) -> float:
    if basic < 0:
        raise ValueError("basic capacity must be non-negative")
    if not 0 < fp <= 1:
        raise ValueError("Fp must be in (0, 1]")
    if not 0 < fr <= 1:
        raise ValueError("FR must be in (0, 1]")
    return basic / (fp * fr)


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
    candidate = profile.get("candidate_extraction") or {}
    key_terms = candidate.get("key_terms") or []
    return [
        term
        for term in key_terms
        if " ".join(str(term).casefold().split()) in normalized
    ]


class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.source_logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.source_model = load_json(SOURCE_DIR / "model_answer.json")
        cls.source_importance = load_json(
            SOURCE_DIR / "topic_importance.json"
        )
        cls.generated_fact = target_entry(
            "fact_anchors.generated.json",
            "topics",
        )
        cls.generated_profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.generated_logic = target_entry(
            "logic_checks.generated.json",
            "topic_logic_checks",
        )
        cls.generated_model = target_entry(
            "model_answers.generated.json",
            "answers",
        )
        cls.generated_importance = target_entry(
            "topic_importance.generated.json",
            "topics",
        )
        cls.generated_manifest = target_entry(
            "topic_pack_manifest.generated.json",
            "topics",
        )

    def test_source_and_generated_topic_contracts_exist(self) -> None:
        for row in (
            self.source_fact,
            self.source_logic,
            self.source_model,
            self.source_importance,
            self.generated_fact,
            self.generated_profile,
            self.generated_logic,
            self.generated_model,
            self.generated_importance,
            self.generated_manifest,
        ):
            self.assertEqual(row["topic_id"], TOPIC)

        source_ids = sorted(
            path.name
            for path in (
                ROOT / "rubrics" / "topic_packs"
            ).iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        manifest = load_json(
            GENERATED_DIR / "topic_pack_manifest.generated.json"
        )
        generated_ids = [
            row["topic_id"]
            for row in manifest["topics"]
        ]
        self.assertEqual(generated_ids, source_ids)
        self.assertEqual(generated_ids.count(TOPIC), 1)

    def test_anchor_contract_is_exact_unique_and_generated(self) -> None:
        source_ids = [
            item["id"]
            for item in self.source_fact["anchors"]
        ]
        generated_ids = [
            item["id"]
            for item in self.generated_fact["anchors"]
        ]
        self.assertEqual(source_ids, EXPECTED_ANCHOR_IDS)
        self.assertEqual(generated_ids, EXPECTED_ANCHOR_IDS)
        self.assertEqual(len(set(source_ids)), 32)
        self.assertEqual(
            self.source_fact["core_facts"],
            [
                item["statement"]
                for item in self.source_fact["anchors"]
            ],
        )

    def test_fatal_major_and_no_direct_score_contract(self) -> None:
        fatal_ids = [
            item["id"]
            for item in self.source_fact["fatal_wrong_claims"]
        ]
        major_ids = [
            item["id"]
            for item in self.generated_profile["major_checks"]
        ]
        self.assertEqual(fatal_ids, EXPECTED_FATAL_IDS)
        self.assertEqual(major_ids, EXPECTED_MAJOR_IDS)
        self.assertEqual(
            len(self.generated_profile["fatal_conditions"]),
            18,
        )
        self.assertGreaterEqual(
            len(self.generated_profile["safe_conditions"]),
            20,
        )
        self.assertFalse(self.generated_logic["enabled"])
        self.assertEqual(self.generated_logic["fatal_checks"], [])
        self.assertEqual(self.generated_logic["major_checks"], [])
        policy = self.generated_profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")

    def test_patterns_and_outline_cover_all_anchors(self) -> None:
        patterns = self.source_model["expected_question_patterns"]
        outlines = self.source_model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)

        anchor_set = set(EXPECTED_ANCHOR_IDS)
        for pattern in patterns:
            self.assertTrue(
                set(pattern["required_anchor_ids"]).issubset(anchor_set)
            )
        outline_refs = set().union(
            *(set(row["anchor_refs"]) for row in outlines)
        )
        self.assertEqual(outline_refs, anchor_set)

    def test_routing_aliases_are_specific_and_generated_identically(
        self,
    ) -> None:
        aliases = self.source_model["routing_aliases"]
        self.assertEqual(
            self.generated_model["topic_aliases"],
            aliases,
        )
        self.assertFalse(BROAD_ALIASES & set(aliases))
        self.assertEqual(len(aliases), len(set(aliases)))
        self.assertGreaterEqual(len(aliases), 20)

    def test_importance_and_output_ownership_contract(self) -> None:
        self.assertEqual(
            self.generated_importance,
            self.source_importance,
        )
        self.assertEqual(
            self.generated_importance["difficulty"],
            "FIELD_APPLICATION",
        )
        self.assertEqual(
            self.generated_importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.generated_importance["question_type"],
            "CALC_DESIGN",
        )
        output = self.generated_profile["output_contract"]
        self.assertEqual(output["direct_score_layers"], ["C"])
        self.assertEqual(output["excluded_score_layers"], ["D", "E"])

    def test_reference_definition_and_conversion_markers(self) -> None:
        by_id = {
            item["id"]: item["statement"]
            for item in self.source_fact["anchors"]
        }
        self.assertIn("60°F", by_id["cv_reference_definition_us_units"])
        self.assertIn("1 psi", by_id["cv_reference_definition_us_units"])
        self.assertIn("US gpm", by_id["cv_reference_definition_us_units"])
        self.assertIn("1 bar", by_id["kv_reference_definition_metric_units"])
        self.assertIn("m³/h", by_id["kv_reference_definition_metric_units"])
        self.assertIn("0.865", by_id["cv_kv_conversion_relation"])
        self.assertIn("1.156", by_id["cv_kv_conversion_relation"])

    def test_required_rated_body_trim_and_operating_points(self) -> None:
        by_id = {
            item["id"]: item["statement"]
            for item in self.source_fact["anchors"]
        }
        self.assertIn(
            "동일시하지 않는다",
            by_id["required_vs_rated_coefficient"],
        )
        self.assertIn(
            "다른 개념",
            by_id["body_size_vs_trim_capacity"],
        )
        self.assertIn(
            "Minimum, normal과 maximum",
            by_id["minimum_normal_maximum_sizing_points"],
        )
        self.assertIn(
            "operating travel",
            by_id["selected_characteristic_travel_mapping"],
        )

    def test_piping_reynolds_and_iteration_markers(self) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.source_fact["anchors"]
        }

        piping_meaning = by_id["piping_geometry_factor_meaning"]
        for marker in (
            "Fp",
            "reducer",
            "expander",
            "fitting",
            "effective flow capacity",
        ):
            self.assertIn(marker, piping_meaning)

        piping_direction = by_id[
            "piping_factor_reduces_effective_capacity"
        ]
        self.assertIn("Fp<1", piping_direction)
        self.assertIn("effective capacity", piping_direction)
        self.assertIn("작아진다", piping_direction)

        reynolds_meaning = by_id["valve_reynolds_number_meaning"]
        self.assertIn("Valve Reynolds number", reynolds_meaning)
        self.assertIn("관성력", reynolds_meaning)
        self.assertIn("점성력", reynolds_meaning)

        reynolds_direction = by_id[
            "reynolds_factor_correction_direction"
        ]
        self.assertIn("FR<1", reynolds_direction)
        self.assertIn("corrected required", reynolds_direction)
        self.assertIn("증가한다", reynolds_direction)

        iteration = by_id["reynolds_correction_iteration"]
        self.assertIn("상호 의존", iteration)
        self.assertIn("반복하여 수렴", iteration)

        small_flow = by_id["small_flow_trim_special_review"]
        self.assertIn("small-flow trim", small_flow)
        self.assertIn("Reynolds correlation", small_flow)

    def test_service_boundary_and_no_universal_numbers(self) -> None:
        combined = json.dumps(
            {
                "fact": self.source_fact,
                "logic": self.source_logic,
                "model": self.source_model,
                "importance": self.source_importance,
            },
            ensure_ascii=False,
        ) + TOPIC_SHEET.read_text(encoding="utf-8")

        for marker in (
            "cavitation",
            "flashing",
            "liquid choked",
            "Two-phase",
            "non-Newtonian",
            "Topic 8",
        ):
            self.assertIn(marker, combined)

        for prohibited in (
            "Kv는 반드시 20°C",
            "정상 개도는 반드시 50%",
            "항상 10% 여유",
            "Reynolds 5000이 모든 밸브의 절대 경계",
        ):
            self.assertNotIn(prohibited, combined)


class RouterRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(
            GENERATED_DIR / "model_answers.generated.json"
        )
        cls.answer_by_topic = {
            item["topic_id"]: item
            for item in cls.bank["answers"]
            if isinstance(item, dict)
        }
        for topic_id in (
            TOPIC,
            TOPIC_2,
            TOPIC_3,
            TOPIC_4,
            TOPIC_5,
        ):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(
                    f"required Topic missing: {topic_id}"
                )

    @classmethod
    def question_type_eval(
        cls,
        topic_id: str,
    ) -> dict[str, Any]:
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
        *,
        answer_text: str = "",
        fact_topic: str | None = None,
        question_type_topic: str | None = None,
    ) -> dict[str, Any]:
        return find_model_answer_reference(
            question_text=question,
            answer_text=answer_text,
            fact_eval=(
                cls.fact_eval(fact_topic)
                if fact_topic is not None
                else None
            ),
            question_type_eval=(
                cls.question_type_eval(question_type_topic)
                if question_type_topic is not None
                else None
            ),
            bank=cls.bank,
        )

    def assert_primary(
        self,
        result: dict[str, Any],
        expected: str,
    ) -> None:
        self.assertTrue(result.get("matched"), msg=result)
        self.assertEqual(selected_topic(result), expected, msg=result)

    def assert_not_target(
        self,
        result: dict[str, Any],
    ) -> None:
        self.assertNotEqual(selected_topic(result), TOPIC, msg=result)

    def test_cv_kv_definition_routes_to_topic6(self) -> None:
        result = self.route(
            "제어밸브 Cv와 Kv의 기준조건, 단위 및 상호 변환 관계를 "
            "설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_basic_liquid_calculation_routes_to_topic6(self) -> None:
        result = self.route(
            "비초크 난류 액체의 유량, 차압과 SG로 required Cv를 "
            "계산하고 적용조건을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_unit_and_input_audit_routes_to_topic6(self) -> None:
        result = self.route(
            "Cv·Kv liquid sizing의 unit consistency와 minimum, normal, "
            "maximum process data 검증 절차를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_min_normal_max_trim_selection_routes_to_topic6(self) -> None:
        result = self.route(
            "Minimum, normal과 maximum flow의 required coefficient를 "
            "rated trim Cv 및 operating travel과 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_piping_factor_routes_to_topic6(self) -> None:
        result = self.route(
            "Reducer와 expander가 연결된 control valve의 piping geometry "
            "factor Fp와 effective capacity 보정을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_reynolds_factor_routes_to_topic6(self) -> None:
        result = self.route(
            "고점도 액체의 valve Reynolds number, FR 보정과 iterative "
            "required Cv calculation을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_small_flow_trim_routes_to_topic6(self) -> None:
        result = self.route(
            "Small-flow trim의 low Reynolds correction과 corrected required "
            "Cv 선정 절차를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_over_under_sizing_routes_to_topic6(self) -> None:
        result = self.route(
            "Required Cv, rated trim capacity와 operating travel로 "
            "oversized 및 undersized valve를 진단하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_integrated_liquid_selection_routes_to_topic6(self) -> None:
        result = self.route(
            "Cv·Kv, Fp, FR, minimum·normal·maximum flow와 vendor data를 "
            "이용한 액체 제어밸브 선정 절차를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_topic2_characteristic_is_not_absorbed(self) -> None:
        result = self.route(
            "Linear, equal-percentage와 quick-opening inherent flow "
            "characteristic를 비교하시오.",
            fact_topic=TOPIC_2,
            question_type_topic=TOPIC_2,
        )
        self.assert_primary(result, TOPIC_2)

    def test_topic3_dynamic_performance_is_not_absorbed(self) -> None:
        result = self.route(
            "제어밸브 deadband, stiction, response time과 positioner "
            "hunting을 설명하시오.",
            fact_topic=TOPIC_3,
            question_type_topic=TOPIC_3,
        )
        self.assert_primary(result, TOPIC_3)

    def test_topic4_body_actuator_selection_is_not_absorbed(self) -> None:
        result = self.route(
            "Globe와 rotary valve body 및 pneumatic·electric actuator "
            "선정 기준을 설명하시오.",
            fact_topic=TOPIC_4,
            question_type_topic=TOPIC_4,
        )
        self.assert_primary(result, TOPIC_4)

    def test_topic5_authority_gain_is_not_absorbed(self) -> None:
        result = self.route(
            "Valve Authority, installed gain, rangeability와 process "
            "turndown의 관계를 설명하시오.",
            fact_topic=TOPIC_5,
            question_type_topic=TOPIC_5,
        )
        self.assert_primary(result, TOPIC_5)

    def test_future_gas_sizing_is_not_topic6(self) -> None:
        result = self.route(
            "Compressible gas control valve sizing의 expansion factor, "
            "critical pressure ratio와 choked flow를 설명하시오."
        )
        self.assert_not_target(result)

    def test_future_cavitation_detail_is_not_topic6(self) -> None:
        result = self.route(
            "Liquid pressure recovery factor, incipient cavitation, flashing, "
            "choked criterion과 anti-cavitation trim을 설명하시오."
        )
        self.assert_not_target(result)

    def test_question_only_routing_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "Valve Authority와 installed gain 및 rangeability를 "
            "설명하시오.",
            answer_text=(
                "Cv, Kv, Fp, FR, valve Reynolds number와 required trim "
                "capacity를 상세히 계산한다."
            ),
            fact_topic=TOPIC_5,
            question_type_topic=TOPIC_5,
        )
        self.assert_primary(result, TOPIC_5)


class FormulaSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.source_fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_cv_forward_square_root_relation(self) -> None:
        cv = 20.0
        sg = 1.0
        q1 = cv * math.sqrt(4.0 / sg)
        q2 = cv * math.sqrt(16.0 / sg)
        self.assertTrue(math.isclose(q1, 40.0))
        self.assertTrue(math.isclose(q2, 80.0))
        self.assertTrue(math.isclose(q2 / q1, 2.0))

    def test_required_cv_flow_sg_and_pressure_directions(self) -> None:
        base = required_cv(100.0, 1.0, 4.0)
        self.assertTrue(math.isclose(base, 50.0))
        self.assertGreater(required_cv(200.0, 1.0, 4.0), base)
        self.assertGreater(required_cv(100.0, 4.0, 4.0), base)
        self.assertLess(required_cv(100.0, 1.0, 16.0), base)

    def test_cv_kv_conversion_roundtrip(self) -> None:
        cv = 100.0
        kv = 0.865 * cv
        cv_roundtrip = 1.156 * kv
        self.assertLess(abs(cv_roundtrip - cv) / cv, 0.001)

    def test_fp_correction_direction(self) -> None:
        basic = 10.0
        self.assertGreater(
            corrected_capacity(basic, 0.8, 1.0),
            basic,
        )
        self.assertTrue(
            math.isclose(
                corrected_capacity(basic, 1.0, 1.0),
                basic,
            )
        )

    def test_fr_correction_direction(self) -> None:
        basic = 10.0
        self.assertGreater(
            corrected_capacity(basic, 1.0, 0.5),
            basic,
        )
        self.assertGreater(
            corrected_capacity(basic, 1.0, 0.4),
            corrected_capacity(basic, 1.0, 0.8),
        )

    def test_combined_fp_fr_monotonicity(self) -> None:
        basic = 10.0
        fp_only = corrected_capacity(basic, 0.8, 1.0)
        combined = corrected_capacity(basic, 0.8, 0.5)
        self.assertGreater(combined, fp_only)
        self.assertTrue(math.isclose(combined, 25.0))

    def test_formula_domain_guards(self) -> None:
        invalid_required = [
            (-1.0, 1.0, 1.0),
            (1.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
        ]
        for args in invalid_required:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    required_cv(*args)

        invalid_corrections = [
            (10.0, 0.0, 1.0),
            (10.0, 1.1, 1.0),
            (10.0, 1.0, 0.0),
            (10.0, 1.0, 1.1),
        ]
        for args in invalid_corrections:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    corrected_capacity(*args)

    def test_positive_sample_covers_all_semantic_clusters(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(SEMANTIC_CLUSTERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_contextual_negative_samples_extract_candidates(self) -> None:
        fatal_ids = {
            row["id"]
            for row in self.source_fact["fatal_wrong_claims"]
        }
        self.assertTrue(set(NEGATIVE_SAMPLES).issubset(fatal_ids))

        for rule_id, answer_text in NEGATIVE_SAMPLES.items():
            with self.subTest(rule_id=rule_id):
                matched_terms = matched_profile_key_terms(
                    answer_text,
                    self.profile,
                )
                self.assertGreaterEqual(
                    len(matched_terms),
                    3,
                    msg={
                        "rule_id": rule_id,
                        "matched_terms": matched_terms,
                        "answer": answer_text,
                    },
                )
                candidates = extract_logic_evidence_candidates(
                    answer_text,
                    self.profile,
                )
                self.assertTrue(
                    candidates,
                    msg={
                        "rule_id": rule_id,
                        "matched_terms": matched_terms,
                        "answer": answer_text,
                    },
                )

    def test_mocked_fatal_verdict_is_c_owned_with_ceiling(self) -> None:
        rule_id = "control_valve_fr_below_one_reduces_required_capacity"
        answer_text = NEGATIVE_SAMPLES[rule_id]
        candidates = extract_logic_evidence_candidates(
            answer_text,
            self.profile,
        )
        self.assertTrue(candidates)

        mocked = {
            "verdict": "fatal",
            "confidence": 0.98,
            "reason": "FR correction 방향을 반대로 설명하였다.",
            "findings": [
                {
                    "candidate_id": candidates[0]["id"],
                    "rule_id": rule_id,
                    "severity": "fatal",
                    "message": "FR<1에서 required capacity 방향 오류",
                    "correct_rule": (
                        "FR<1이면 동일 flow의 corrected required "
                        "coefficient는 증가한다."
                    ),
                }
            ],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked,
        ):
            result = verify_logic_with_llm(
                answer_text,
                TOPIC,
            )

        self.assertTrue(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "fatal")
        self.assertEqual(
            result["findings"][0]["affected_layers"],
            ["C"],
        )
        self.assertEqual(result["recommended_ceiling"], 10.0)

    def test_mocked_safe_verdict_has_no_fatal_or_ceiling(self) -> None:
        mocked = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "Cv·Kv와 Fp·FR 적용경계를 조건부로 정확히 설명했다.",
            "findings": [],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked,
        ):
            result = verify_logic_with_llm(
                SAFE_ANSWER,
                TOPIC,
            )

        self.assertFalse(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "pass")
        self.assertIsNone(result["recommended_ceiling"])
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
