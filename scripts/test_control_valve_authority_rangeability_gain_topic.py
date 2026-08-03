#!/usr/bin/env python3
from __future__ import annotations

import json
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


TOPIC = "control_valve_authority_rangeability_gain_installed_performance"
TOPIC_1 = (
    "control_valve_fluid_forces_unbalance_friction_"
    "actuator_sizing_fail_safe"
)
TOPIC_2 = (
    "control_valve_characteristics_inherent_installed_"
    "equal_percentage_linear_quick_opening"
)
TOPIC_3 = (
    "control_valve_deadband_stiction_response_time_"
    "positioner_dynamic_performance"
)
TOPIC_4 = "control_valve_types_globe_rotary_body_actuator_selection"
FEEDBACK_TOPIC = (
    "feedback_system_closed_loop_sensitivity_steady_state_error"
)

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = (
    ROOT
    / "docs"
    / "topic_sheets"
    / f"{TOPIC}.md"
)

EXPECTED_ANCHOR_IDS = [
    "valve_authority_physical_meaning",
    "authority_simple_series_formula",
    "authority_system_boundary_definition",
    "pressure_drop_redistribution_with_flow",
    "low_authority_installed_characteristic_distortion",
    "authority_not_fixed_universal_target",
    "oversizing_low_normal_travel",
    "oversizing_reduces_effective_valve_drop",
    "oversizing_increases_local_gain_sensitivity",
    "inherent_gain_constant_pressure_drop",
    "installed_gain_actual_system_slope",
    "installed_gain_operating_point_dependency",
    "installed_gain_differs_from_inherent_gain",
    "process_gain_operating_point_dependency",
    "loop_gain_component_product",
    "valve_process_gain_compensation",
    "equal_percentage_compensation_is_conditional",
    "gain_variation_affects_control_performance",
    "control_range_gain_acceptance_concept",
    "rangeability_controllable_cv_ratio",
    "rangeability_not_travel_ratio",
    "installed_rangeability_flow_ratio",
    "installed_rangeability_differs_from_rated",
    "process_turndown_distinct_from_rangeability",
    "minimum_controllable_flow_limits",
    "seat_leakage_not_minimum_control_flow",
    "min_normal_max_operating_point_validation",
    "gain_curve_installed_curve_final_verification",
]

EXPECTED_FATAL_IDS = [
    "control_valve_authority_total_pressure_without_boundary",
    "control_valve_authority_is_valve_opening",
    "control_valve_authority_always_one_target",
    "control_valve_low_authority_no_characteristic_effect",
    "control_valve_oversizing_improves_control_range",
    "control_valve_installed_gain_equals_inherent_gain",
    "control_valve_installed_gain_constant_all_travel",
    "control_valve_equal_percentage_constant_loop_gain_always",
    "control_valve_loop_gain_valve_gain_only",
    "control_valve_rangeability_is_travel_ratio",
    "control_valve_rangeability_is_rated_cv_only",
    "control_valve_rated_equals_installed_rangeability",
    "control_valve_rangeability_equals_process_turndown",
    "control_valve_zero_leakage_zero_minimum_flow",
    "control_valve_controller_tuning_fixes_bad_authority",
    "control_valve_single_design_point_proves_full_performance",
]

EXPECTED_MAJOR_IDS = [
    "control_valve_authority_fixed_recommended_value",
    "control_valve_equal_percentage_always_best",
    "control_valve_high_authority_always_best",
    "control_valve_catalog_rangeability_guarantees_process_turndown",
    "control_valve_gain_band_universal_standard",
    "control_valve_oversizing_body_size_only",
]

BROAD_ALIASES = {
    "authority",
    "gain",
    "range",
    "rangeability",
    "valve",
    "control valve",
    "제어밸브",
    "performance",
    "성능",
    "turndown",
}

COVERAGE_MARKERS = {
    "authority": (
        "design point",
        "system boundary",
        "valve pressure drop",
    ),
    "redistribution": (
        "pressure-drop redistribution",
        "system resistance",
        "installed characteristic",
    ),
    "oversizing": (
        "oversized valve",
        "low normal travel",
        "local installed gain",
    ),
    "gain_definition": (
        "inherent valve gain",
        "installed valve gain",
        "operating point",
    ),
    "loop_gain": (
        "controller gain",
        "process gain",
        "measurement gain",
        "loop gain",
    ),
    "rangeability": (
        "rated rangeability",
        "installed rangeability",
        "process turndown",
    ),
    "minimum_flow": (
        "minimum controllable flow",
        "seat leakage",
        "deadband",
        "measurement noise",
    ),
    "validation": (
        "minimum flow",
        "normal flow",
        "maximum flow",
        "installed flow curve",
        "gain curve",
    ),
}

POSITIVE_ANSWER = """
Valve Authority는 design point와 system boundary를 정한 뒤 valve pressure drop의
비중으로 계산한다. 유량 변화에 따른 pressure-drop redistribution과 system
resistance는 installed characteristic를 왜곡할 수 있다. Oversized valve는
low normal travel과 높은 local installed gain을 만들 수 있다. Inherent valve
gain은 일정 차압의 기울기이고 installed valve gain은 실제 operating point의
기울기이다. Controller gain, installed valve gain, process gain과 measurement
gain을 결합하여 loop gain을 평가한다. Rated rangeability, installed
rangeability와 process turndown을 구분한다. Minimum controllable flow는 seat
leakage뿐 아니라 deadband와 measurement noise의 영향을 받는다. Minimum flow,
normal flow와 maximum flow를 installed flow curve와 gain curve에서 검증한다.
""".strip()

PARTIAL_ANSWER = """
Valve Authority는 design point와 system boundary에서 valve pressure drop의
비중으로 계산한다. Pressure-drop redistribution과 system resistance가
installed characteristic를 바꿀 수 있다. Inherent valve gain과 installed
valve gain은 operating point 조건이 다르다.
""".strip()

SAFE_CONTRAST_ANSWER = (
    "Authority는 design point와 system boundary에서 계산한다. "
    "Equal-percentage는 특정 process gain 변화에서 보상에 유리할 수 있으나 "
    "모든 공정에서 loop gain을 일정하게 만들지는 않는다. Installed "
    "rangeability와 process turndown은 구분한다. Seat leakage와 minimum "
    "controllable flow는 다른 성능 항목이다."
)


NEGATIVE_SAMPLES = {
    "control_valve_authority_is_valve_opening": (
        "Valve Authority는 design point와 system boundary에서의 valve "
        "pressure drop share가 아니라 밸브 개도율 또는 travel 비율이다."
    ),
    "control_valve_installed_gain_equals_inherent_gain": (
        "Installed valve gain은 모든 operating point에서 inherent valve "
        "gain과 동일하며 valve pressure drop과 system resistance 변화의 "
        "영향을 받지 않는다."
    ),
    "control_valve_rangeability_is_travel_ratio": (
        "Rated rangeability는 maximum travel과 minimum travel의 비이며 "
        "maximum controllable flow와 minimum controllable flow capacity는 "
        "고려하지 않는다."
    ),
    "control_valve_zero_leakage_zero_minimum_flow": (
        "Seat leakage가 zero인 control valve는 deadband, stiction과 "
        "measurement noise에 관계없이 minimum controllable flow도 zero이다."
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
        topic_id = primary.get("topic_id")
        if isinstance(topic_id, str):
            return topic_id
    return None


def coverage_rows(text: str) -> dict[str, bool]:
    normalized = " ".join(text.casefold().split())
    return {
        group: all(
            " ".join(marker.casefold().split()) in normalized
            for marker in markers
        )
        for group, markers in COVERAGE_MARKERS.items()
    }


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
        cls.generated_logic = target_entry(
            "logic_checks.generated.json",
            "topic_logic_checks",
        )
        cls.generated_profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
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
            self.generated_logic,
            self.generated_profile,
            self.generated_model,
            self.generated_importance,
            self.generated_manifest,
        ):
            self.assertEqual(row["topic_id"], TOPIC)

        manifest = load_json(
            GENERATED_DIR / "topic_pack_manifest.generated.json"
        )
        source_topic_ids = sorted(
            path.name
            for path in (
                ROOT / "rubrics" / "topic_packs"
            ).iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        generated_topic_ids = [
            row["topic_id"]
            for row in manifest["topics"]
        ]
        self.assertEqual(generated_topic_ids, source_topic_ids)
        self.assertEqual(generated_topic_ids.count(TOPIC), 1)

    def test_anchor_contract_is_exact_and_unique(self) -> None:
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
        self.assertEqual(len(set(source_ids)), 28)
        self.assertEqual(
            self.source_fact["core_facts"],
            [
                item["statement"]
                for item in self.source_fact["anchors"]
            ],
        )

    def test_logic_contract_has_fatal_major_safe_and_no_direct_score(
        self,
    ) -> None:
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
            16,
        )
        self.assertGreaterEqual(
            len(self.generated_profile["safe_conditions"]),
            16,
        )
        self.assertFalse(self.generated_logic["enabled"])
        self.assertEqual(self.generated_logic["fatal_checks"], [])
        self.assertEqual(self.generated_logic["major_checks"], [])
        self.assertEqual(
            self.generated_profile["candidate_extraction"]["rules"],
            [],
        )
        policy = self.generated_profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")

    def test_model_patterns_and_outline_cover_all_anchors(self) -> None:
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
        self.assertGreaterEqual(len(aliases), 18)

    def test_importance_and_output_ownership_contract(self) -> None:
        self.assertEqual(
            self.generated_importance,
            self.source_importance,
        )
        self.assertEqual(
            self.generated_importance["difficulty"],
            "THEORY_CORE",
        )
        self.assertEqual(
            self.generated_importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.generated_importance["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )
        output = self.generated_profile["output_contract"]
        self.assertEqual(output["direct_score_layers"], ["C"])
        self.assertEqual(output["excluded_score_layers"], ["D", "E"])

    def test_authority_formula_and_system_boundary_contract(self) -> None:
        by_id = {
            item["id"]: item
            for item in self.source_fact["anchors"]
        }
        formula = by_id["authority_simple_series_formula"]
        boundary = by_id["authority_system_boundary_definition"]
        target = by_id["authority_not_fixed_universal_target"]

        self.assertIn("밸브 압력강하", formula["statement"])
        self.assertIn("가변 시스템 저항", formula["statement"])
        self.assertIn("pump curve", boundary["statement"])
        self.assertIn("static head", boundary["statement"])
        self.assertIn("parallel branch", boundary["statement"])
        self.assertIn("고정 숫자", target["statement"])

    def test_rangeability_and_turndown_boundary_contract(self) -> None:
        by_id = {
            item["id"]: item
            for item in self.source_fact["anchors"]
        }
        rated = by_id["rangeability_controllable_cv_ratio"]["statement"]
        travel = by_id["rangeability_not_travel_ratio"]["statement"]
        installed = by_id["installed_rangeability_flow_ratio"]["statement"]
        turndown = by_id[
            "process_turndown_distinct_from_rangeability"
        ]["statement"]

        self.assertIn("최대 제어 가능 Cv", rated)
        self.assertIn("최소 제어 가능 Cv", rated)
        self.assertIn("travel", travel)
        self.assertIn("실제 계통", installed)
        self.assertIn("동일 개념이 아니다", turndown)

    def test_topic_sheet_formula_markers_and_no_universal_numeric_target(
        self,
    ) -> None:
        text = TOPIC_SHEET.read_text(encoding="utf-8")
        for marker in (
            "a_v =",
            r"K_{v,\mathrm{inh}}",
            r"K_{v,\mathrm{inst}}",
            r"K_{\mathrm{loop}}",
            "R_v =",
            r"R_{\mathrm{inst}}",
        ):
            self.assertIn(marker, text)

        combined = json.dumps(
            {
                "fact": self.source_fact,
                "logic": self.source_logic,
                "model": self.source_model,
                "importance": self.source_importance,
            },
            ensure_ascii=False,
        ) + text
        for prohibited in (
            "Authority는 반드시 0.5",
            "Authority는 항상 0.5",
            "모든 계통에서 0.5",
            "4:1은 국제 표준",
            "gain variation은 반드시 4:1",
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
            TOPIC_1,
            TOPIC_2,
            TOPIC_3,
            TOPIC_4,
            FEEDBACK_TOPIC,
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

    def test_authority_definition_routes_to_topic5(self) -> None:
        result = self.route(
            "Valve Authority의 정의, 설계점 차압 식과 system boundary를 "
            "설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_low_authority_distortion_routes_to_topic5(self) -> None:
        result = self.route(
            "낮은 Valve Authority가 installed characteristic와 "
            "installed valve gain을 왜곡하는 원리를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_oversizing_performance_routes_to_topic5(self) -> None:
        result = self.route(
            "Oversized control valve의 low normal travel, Authority와 "
            "local installed gain 문제를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_inherent_installed_gain_routes_to_topic5(self) -> None:
        result = self.route(
            "Inherent valve gain과 installed valve gain의 차이와 "
            "operating point 의존성을 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_loop_gain_compensation_routes_to_topic5(self) -> None:
        result = self.route(
            "Installed valve gain, process gain과 loop gain의 관계 및 "
            "gain compensation을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_equal_percentage_compensation_routes_to_topic5(self) -> None:
        result = self.route(
            "Equal-percentage characteristic가 process gain 변화를 "
            "보상하는 원리와 한계를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_rangeability_turndown_routes_to_topic5(self) -> None:
        result = self.route(
            "Rated rangeability, installed rangeability와 process "
            "turndown을 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_minimum_controllable_flow_routes_to_topic5(self) -> None:
        result = self.route(
            "Minimum controllable flow에 미치는 seat leakage, deadband, "
            "stiction과 measurement noise의 영향을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_integrated_performance_routes_to_topic5(self) -> None:
        result = self.route(
            "Authority, installed gain, rangeability와 process gain을 "
            "이용한 installed performance 평가 절차를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_topic1_force_sizing_is_not_absorbed(self) -> None:
        result = self.route(
            "제어밸브 불평형력, 마찰력, actuator thrust와 fail-safe "
            "spring sizing을 설명하시오.",
            fact_topic=TOPIC_1,
            question_type_topic=TOPIC_1,
        )
        self.assert_primary(result, TOPIC_1)

    def test_topic2_characteristic_shapes_are_not_absorbed(self) -> None:
        result = self.route(
            "Inherent와 installed flow characteristic 및 linear, "
            "equal percentage, quick opening 형상을 비교하시오.",
            fact_topic=TOPIC_2,
            question_type_topic=TOPIC_2,
        )
        self.assert_primary(result, TOPIC_2)

    def test_topic3_dynamic_performance_is_not_absorbed(self) -> None:
        result = self.route(
            "제어밸브 deadband, stiction, response time과 positioner "
            "hunting의 원인과 개선방안을 설명하시오.",
            fact_topic=TOPIC_3,
            question_type_topic=TOPIC_3,
        )
        self.assert_primary(result, TOPIC_3)

    def test_topic4_body_actuator_selection_is_not_absorbed(self) -> None:
        result = self.route(
            "Globe와 rotary valve body 및 pneumatic·electric actuator "
            "형식을 비교하고 선정 기준을 설명하시오.",
            fact_topic=TOPIC_4,
            question_type_topic=TOPIC_4,
        )
        self.assert_primary(result, TOPIC_4)

    def test_cv_kv_sizing_future_topic_is_not_topic5(self) -> None:
        result = self.route(
            "액체 제어밸브의 Cv, Kv, Reynolds correction과 valve size "
            "계산 절차를 설명하시오."
        )
        self.assert_not_target(result)

    def test_generic_feedback_loop_gain_is_not_absorbed(self) -> None:
        result = self.route(
            "폐루프 feedback system의 sensitivity와 steady-state error 및 "
            "loop gain 관계를 설명하시오.",
            fact_topic=FEEDBACK_TOPIC,
            question_type_topic=FEEDBACK_TOPIC,
        )
        self.assert_primary(result, FEEDBACK_TOPIC)

    def test_question_only_routing_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "Linear, equal percentage와 quick opening valve "
            "characteristic를 비교하시오.",
            answer_text=(
                "Authority, installed valve gain, rangeability, process "
                "turndown과 gain curve를 상세히 설명한다."
            ),
            fact_topic=TOPIC_2,
            question_type_topic=TOPIC_2,
        )
        self.assert_primary(result, TOPIC_2)


class SemanticContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.source_fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_positive_sample_covers_all_semantic_clusters(
        self,
    ) -> None:
        rows = coverage_rows(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(COVERAGE_MARKERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_partial_sample_preserves_core_but_misses_other_clusters(
        self,
    ) -> None:
        rows = coverage_rows(PARTIAL_ANSWER)
        self.assertTrue(rows["authority"], msg=rows)
        self.assertTrue(rows["redistribution"], msg=rows)
        self.assertTrue(rows["gain_definition"], msg=rows)

        for group in (
            "oversizing",
            "loop_gain",
            "rangeability",
            "minimum_flow",
            "validation",
        ):
            self.assertFalse(rows[group], msg=rows)

    def test_fatal_contract_ids_and_representative_candidates(
        self,
    ) -> None:
        fatal_rows = self.source_fact["fatal_wrong_claims"]
        self.assertEqual(
            [row["id"] for row in fatal_rows],
            EXPECTED_FATAL_IDS,
        )

        fatal_by_id = {
            row["id"]: row
            for row in fatal_rows
        }
        self.assertEqual(
            set(NEGATIVE_SAMPLES),
            {
                "control_valve_authority_is_valve_opening",
                "control_valve_installed_gain_equals_inherent_gain",
                "control_valve_rangeability_is_travel_ratio",
                "control_valve_zero_leakage_zero_minimum_flow",
            },
        )

        for rule_id, sample in NEGATIVE_SAMPLES.items():
            with self.subTest(rule_id=rule_id):
                self.assertIn(rule_id, fatal_by_id)
                candidates = extract_logic_evidence_candidates(
                    sample,
                    self.profile,
                )
                self.assertTrue(
                    candidates,
                    msg={
                        "rule_id": rule_id,
                        "sample": sample,
                        "source_claim": fatal_by_id[rule_id]["claim"],
                    },
                )

    def test_safe_contrast_is_registered_and_extracted(self) -> None:
        safe = set(self.profile["safe_conditions"])
        self.assertIn(
            "Authority는 정의한 설계점과 시스템 경계에서 계산한다.",
            safe,
        )
        self.assertIn(
            "Installed rangeability는 실제 루프의 제어 가능 유량비이다.",
            safe,
        )
        self.assertIn(
            "Seat leakage와 minimum controllable flow는 다른 성능 항목이다.",
            safe,
        )
        self.assertEqual(
            self.profile["candidate_extraction"]["rules"],
            [],
        )
        self.assertTrue(
            extract_logic_evidence_candidates(
                SAFE_CONTRAST_ANSWER,
                self.profile,
            )
        )

    def test_major_claims_are_separate_from_fatal_contract(
        self,
    ) -> None:
        major_ids = {
            row["id"]
            for row in self.profile["major_checks"]
        }
        fatal_ids = {
            row["id"]
            for row in self.source_fact["fatal_wrong_claims"]
        }
        self.assertEqual(major_ids, set(EXPECTED_MAJOR_IDS))
        self.assertEqual(fatal_ids, set(EXPECTED_FATAL_IDS))
        self.assertTrue(major_ids.isdisjoint(fatal_ids))

    def test_mocked_fatal_verdict_is_c_owned_with_production_ceiling(
        self,
    ) -> None:
        rule_id = "control_valve_authority_is_valve_opening"
        answer_text = NEGATIVE_SAMPLES[rule_id]
        candidates = extract_logic_evidence_candidates(
            answer_text,
            self.profile,
        )
        self.assertTrue(candidates)

        mocked = {
            "verdict": "fatal",
            "confidence": 0.97,
            "reason": "Authority를 valve opening으로 잘못 정의하였다.",
            "findings": [
                {
                    "candidate_id": candidates[0]["id"],
                    "rule_id": rule_id,
                    "severity": "fatal",
                    "message": "Authority의 물리적 정의를 반대로 설명했다.",
                    "correct_rule": (
                        "Authority는 정의한 system boundary에서 "
                        "valve pressure-drop share이다."
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

    def test_mocked_safe_verdict_has_no_fatal_or_ceiling(
        self,
    ) -> None:
        mocked = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "Authority와 rangeability 경계를 조건부로 정확히 설명했다.",
            "findings": [],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked,
        ):
            result = verify_logic_with_llm(
                SAFE_CONTRAST_ANSWER,
                TOPIC,
            )

        self.assertFalse(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "pass")
        self.assertIsNone(result["recommended_ceiling"])
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
