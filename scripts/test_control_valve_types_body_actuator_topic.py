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


TOPIC = "control_valve_types_globe_rotary_body_actuator_selection"
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

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"

EXPECTED_ANCHOR_IDS = [
    "sliding_stem_rotary_motion_classification",
    "single_port_globe_throttling_structure",
    "angle_valve_flow_direction_change",
    "post_guided_plug_alignment",
    "port_guided_plug_alignment",
    "cage_guided_alignment_and_flow_path",
    "double_port_capacity_force_balance_limit",
    "three_way_mixing_diverting_function",
    "sanitary_valve_cleanability_drainability",
    "butterfly_compact_high_capacity",
    "high_performance_butterfly_eccentric_sealing",
    "segmented_v_notch_ball_throttling",
    "eccentric_plug_noncontact_rotation",
    "full_port_ball_low_restriction_scope",
    "multiport_selector_flow_routing",
    "end_connection_threaded_flanged_welded",
    "standard_bonnet_pressure_boundary",
    "extension_bonnet_temperature_isolation",
    "bellows_seal_bonnet_emission_barrier",
    "plug_guiding_alignment_and_side_load",
    "reduced_capacity_trim_match_required_flow",
    "spring_diaphragm_actuator_force_and_fail_safe",
    "piston_actuator_high_force_and_speed",
    "rack_pinion_rotary_torque_conversion",
    "electric_actuator_motor_gear_control",
    "manual_actuator_local_operation_limit",
    "actuator_output_matches_valve_motion",
    "body_actuator_selection_multi_criteria",
]

EXPECTED_FATAL_IDS = [
    "control_valve_rotary_valve_onoff_only",
    "control_valve_globe_always_low_capacity",
    "control_valve_double_port_fully_balanced_zero_force",
    "control_valve_double_port_best_tight_shutoff",
    "control_valve_cage_guided_all_solids_service",
    "control_valve_butterfly_not_for_control",
    "control_valve_segmented_ball_same_full_port_ball",
    "control_valve_full_port_ball_always_best_throttling",
    "control_valve_three_way_mixing_diverting_unrestricted_interchange",
    "control_valve_bellows_eliminates_all_packing",
    "control_valve_extension_bonnet_universal_length",
    "control_valve_reduced_trim_replaces_sizing",
    "control_valve_actuator_independent_of_valve_motion",
    "control_valve_piston_actuator_inherently_fail_safe",
    "control_valve_electric_actuator_cannot_fail_safe",
    "control_valve_manual_actuator_automatic_modulating_control",
]

EXPECTED_MAJOR_IDS = [
    "control_valve_globe_universally_most_accurate",
    "control_valve_rotary_universally_highest_capacity_lowest_cost",
    "control_valve_pneumatic_always_better_than_electric",
    "control_valve_electric_always_lower_maintenance",
    "control_valve_sanitary_type_determined_by_industry_name_only",
    "control_valve_end_connection_selected_by_pressure_only",
]

BROAD_ALIASES = {
    "valve",
    "control valve",
    "제어밸브",
    "actuator",
    "액추에이터",
    "selection",
    "선정",
    "globe",
    "ball",
    "butterfly",
}

COVERAGE_MARKERS = {
    "classification": (
        "sliding-stem",
        "rotary valve",
        "linear force",
        "rotary torque",
    ),
    "globe_types": (
        "single-port globe",
        "cage-guided",
        "double-port",
        "three-way valve",
        "sanitary valve",
    ),
    "rotary_types": (
        "butterfly valve",
        "high-performance butterfly",
        "segmented ball",
        "eccentric plug",
        "full-port ball",
        "multiport selector",
    ),
    "body_components": (
        "threaded connection",
        "flanged connection",
        "welded connection",
        "extension bonnet",
        "bellows seal",
        "plug guiding",
        "reduced-capacity trim",
    ),
    "pneumatic_actuators": (
        "spring-diaphragm",
        "piston actuator",
        "rack-and-pinion",
    ),
    "electric_manual": (
        "electric actuator",
        "duty cycle",
        "manual actuator",
        "handwheel",
    ),
    "motion_matching": (
        "actuator output",
        "valve motion",
        "stroke",
        "rotation angle",
    ),
    "selection_criteria": (
        "process fluid",
        "pressure temperature",
        "fail-safe",
        "power source",
        "maintenance",
        "lifecycle cost",
    ),
}

POSITIVE_ANSWER = """
Control valve body는 sliding-stem과 rotary valve로 분류한다.
Sliding-stem에는 linear force가 필요하고 rotary valve에는 rotary torque가
필요하다. Globe 계열은 single-port globe, cage-guided, double-port,
three-way valve와 sanitary valve를 비교한다. Rotary 계열은 butterfly valve,
high-performance butterfly, segmented ball, eccentric plug, full-port ball과
multiport selector를 비교한다. Body component는 threaded connection, flanged
connection, welded connection, extension bonnet, bellows seal, plug guiding과
reduced-capacity trim을 검토한다. Pneumatic actuator는 spring-diaphragm,
piston actuator와 rack-and-pinion을 비교한다. Electric actuator는 duty cycle과
정전 동작을 확인하고 manual actuator와 handwheel은 현장 조작으로 한정한다.
Actuator output은 valve motion, stroke와 rotation angle에 일치시킨다. 최종 선정은
process fluid, pressure temperature, fail-safe, power source, maintenance와
lifecycle cost를 함께 검토한다.
""".strip()

PARTIAL_ANSWER = """
Sliding-stem과 rotary valve를 분류한다. Sliding-stem은 linear force를 사용하고
rotary valve는 rotary torque를 사용한다. Globe 계열에서는 single-port globe,
cage-guided, double-port, three-way valve와 sanitary valve를 비교한다.
Pneumatic actuator는 spring-diaphragm, piston actuator와 rack-and-pinion을
비교한다.
""".strip()

SAFE_CONTRAST_ANSWER = (
    "Rotary valve도 throttling에 사용할 수 있다. Double-port는 유체력 상쇄에 "
    "유리할 수 있으나 완전한 balance를 보장하지 않는다. Reduced-capacity trim은 "
    "sizing을 대신하지 않는다. Electric actuator도 stored energy를 이용해 "
    "정전 시 동작을 설계할 수 있다."
)


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
        self.assertGreaterEqual(len(aliases), 16)

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
            "COMPARE_SELECTION",
        )
        output = self.generated_profile["output_contract"]
        self.assertEqual(output["direct_score_layers"], ["C"])
        self.assertEqual(output["excluded_score_layers"], ["D", "E"])


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
        for topic_id in (TOPIC, TOPIC_1, TOPIC_2, TOPIC_3):
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

    def test_sliding_stem_rotary_selection_routes_to_topic4(self) -> None:
        result = self.route(
            "Sliding-stem과 rotary control valve의 구조와 장단점을 "
            "비교하고 actuator 선정 기준을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_globe_structure_comparison_routes_to_topic4(self) -> None:
        result = self.route(
            "Single-port, post-guided, port-guided, cage-guided와 "
            "double-port globe valve를 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_three_way_sanitary_routes_to_topic4(self) -> None:
        result = self.route(
            "Three-way mixing·diverting valve와 sanitary valve의 "
            "구조와 적용 조건을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_rotary_body_types_route_to_topic4(self) -> None:
        result = self.route(
            "Butterfly, segmented V-notch ball, eccentric plug와 "
            "full-port ball valve를 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_bonnet_guide_reduced_trim_routes_to_topic4(self) -> None:
        result = self.route(
            "Standard·extension·bellows-seal bonnet, plug guiding과 "
            "reduced-capacity trim의 선정 기준을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_pneumatic_actuator_types_route_to_topic4(self) -> None:
        result = self.route(
            "Spring-diaphragm, piston과 rack-and-pinion actuator의 "
            "force·torque, 속도와 fail-safe를 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_integrated_body_actuator_selection_routes_to_topic4(
        self,
    ) -> None:
        result = self.route(
            "Globe와 rotary body 및 pneumatic·electric·manual "
            "actuator를 비교하고 적합한 조합 선정 기준을 제시하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_topic1_force_sizing_is_not_absorbed(self) -> None:
        result = self.route(
            "제어밸브 불평형력, 마찰력, actuator thrust와 "
            "fail-safe spring sizing을 설명하시오.",
            fact_topic=TOPIC_1,
            question_type_topic=TOPIC_1,
        )
        self.assert_primary(result, TOPIC_1)

    def test_topic2_characteristics_is_not_absorbed(self) -> None:
        result = self.route(
            "Inherent와 installed characteristic 및 linear, "
            "equal percentage, quick opening을 비교하시오.",
            fact_topic=TOPIC_2,
            question_type_topic=TOPIC_2,
        )
        self.assert_primary(result, TOPIC_2)

    def test_topic3_dynamic_performance_is_not_absorbed(self) -> None:
        result = self.route(
            "제어밸브 deadband, stiction, response time과 "
            "positioner hunting의 원인과 개선방안을 설명하시오.",
            fact_topic=TOPIC_3,
            question_type_topic=TOPIC_3,
        )
        self.assert_primary(result, TOPIC_3)

    def test_authority_rangeability_future_topic_is_not_topic4(
        self,
    ) -> None:
        result = self.route(
            "Valve authority, rangeability와 installed valve gain이 "
            "process performance에 미치는 영향을 설명하시오."
        )
        self.assert_not_target(result)

    def test_cv_kv_sizing_future_topic_is_not_topic4(self) -> None:
        result = self.route(
            "액체 제어밸브의 Cv, Kv, Reynolds correction과 "
            "valve size selection 절차를 설명하시오."
        )
        self.assert_not_target(result)

    def test_question_only_routing_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "Inherent와 installed characteristic 및 equal percentage "
            "선정 기준을 설명하시오.",
            answer_text=(
                "Globe, butterfly, segmented ball, piston actuator, "
                "electric actuator와 bellows bonnet을 상세히 설명한다."
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
        self.assertTrue(rows["classification"], msg=rows)
        self.assertTrue(rows["globe_types"], msg=rows)
        self.assertTrue(rows["pneumatic_actuators"], msg=rows)

        for group in (
            "rotary_types",
            "body_components",
            "electric_manual",
            "motion_matching",
            "selection_criteria",
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

        representative_ids = {
            "control_valve_rotary_valve_onoff_only",
            "control_valve_double_port_fully_balanced_zero_force",
            "control_valve_reduced_trim_replaces_sizing",
            "control_valve_electric_actuator_cannot_fail_safe",
        }
        selected = [
            row
            for row in fatal_rows
            if row["id"] in representative_ids
        ]
        self.assertEqual(len(selected), 4)

        for row in selected:
            with self.subTest(rule_id=row["id"]):
                candidates = extract_logic_evidence_candidates(
                    row["claim"],
                    self.profile,
                )
                self.assertTrue(candidates, msg=row)

    def test_safe_contrast_is_registered_and_extracted(self) -> None:
        safe = set(self.profile["safe_conditions"])
        self.assertIn(
            "Reduced-capacity trim은 sizing을 대신하지 않는다.",
            safe,
        )
        self.assertIn(
            "Double-port는 유체력 상쇄에 유리할 수 있으나 "
            "완전한 balance를 보장하지 않는다.",
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
        claim = self.source_fact["fatal_wrong_claims"][0]["claim"]
        candidates = extract_logic_evidence_candidates(
            claim,
            self.profile,
        )
        self.assertTrue(candidates)

        mocked = {
            "verdict": "fatal",
            "confidence": 0.96,
            "reason": "Rotary valve의 throttling 적용을 부정하였다.",
            "findings": [
                {
                    "candidate_id": candidates[0]["id"],
                    "rule_id": "control_valve_rotary_valve_onoff_only",
                    "severity": "fatal",
                    "message": "Rotary valve 적용 범위를 반대로 설명했다.",
                    "correct_rule": (
                        "Rotary valve도 형식과 trim에 따라 "
                        "throttling에 사용할 수 있다."
                    ),
                }
            ],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked,
        ):
            result = verify_logic_with_llm(claim, TOPIC)

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
            "reason": "구조 차이와 조건부 선정 근거가 타당하다.",
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
