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

from logic_llm_verifier import (
    extract_logic_evidence_candidates,
    verify_logic_with_llm,
)
from model_answer_router import find_model_answer_reference


TOPIC = (
    "control_valve_deadband_stiction_response_time_"
    "positioner_dynamic_performance"
)
TOPIC_1 = (
    "control_valve_fluid_forces_unbalance_friction_"
    "actuator_sizing_fail_safe"
)
TOPIC_2 = (
    "control_valve_characteristics_inherent_installed_"
    "equal_percentage_linear_quick_opening"
)
SECOND_ORDER_TOPIC = "second_order_system_resonance_frequency_response"

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"

EXPECTED_ANCHOR_IDS = [
    "final_control_element_variability_path",
    "deadband_definition_direction_reversal",
    "deadband_not_dead_time",
    "backlash_mechanical_clearance",
    "hysteresis_direction_dependent_output",
    "static_friction_starting_force",
    "stiction_stick_then_jump",
    "stick_slip_repeated_motion",
    "stiction_limit_cycle_path",
    "oscillation_requires_differential_diagnosis",
    "response_time_dead_dynamic_separation",
    "opening_closing_response_asymmetry",
    "small_step_test_control_resolution",
    "large_step_test_pneumatic_capacity",
    "reversal_test_deadband_hysteresis",
    "step_sensitivity_not_resolution_only",
    "positioner_closed_loop_position_feedback",
    "positioner_cannot_remove_mechanical_backlash",
    "positioner_cannot_replace_actuator_thrust",
    "positioner_gain_speed_stability_tradeoff",
    "pneumatic_supply_tubing_spool_capacity",
    "volume_booster_flow_capacity_feedback_condition",
    "hunting_multicausal_diagnosis",
    "improvement_verify_same_test_and_process_result",
]

EXPECTED_FATAL_IDS = [
    "control_valve_deadband_same_as_dead_time",
    "control_valve_stiction_same_as_slow_response",
    "control_valve_hysteresis_same_as_deadband",
    "control_valve_resolution_same_as_step_sensitivity",
    "control_valve_all_oscillation_caused_by_stiction",
    "control_valve_positioner_removes_mechanical_backlash",
    "control_valve_positioner_replaces_insufficient_actuator_thrust",
    "control_valve_high_positioner_gain_always_better",
    "control_valve_volume_booster_always_improves_stability",
    "control_valve_volume_booster_eliminates_deadband",
    "control_valve_response_time_only_dead_time",
    "control_valve_response_time_only_stroke_time",
    "control_valve_small_step_test_same_as_large_step_test",
    "control_valve_pid_tuning_eliminates_mechanical_stiction",
]

EXPECTED_MAJOR_IDS = [
    "control_valve_positioner_always_creates_second_order_system",
    "control_valve_integral_positioner_always_disable",
    "control_valve_loop_gain_universal_target_range",
    "control_valve_response_problem_eighty_percent_universal",
    "control_valve_specific_packing_universal_solution",
]

BROAD_ALIASES = {
    "control valve",
    "제어밸브",
    "valve",
    "response",
    "time",
    "friction",
    "positioner",
    "gain",
    "dead time",
    "hysteresis",
    "resolution",
    "hunting",
    "booster",
    "dynamic",
    "performance",
}

REQUIREMENT_MARKERS = {
    "final_control_element_variability_path": (
        "controller output",
        "valve travel",
        "process variability",
    ),
    "deadband_definition_direction_reversal": (
        "direction reversal deadband",
        "불감 구간",
    ),
    "deadband_not_dead_time": ("input range", "time delay"),
    "backlash_mechanical_clearance": (
        "linkage backlash",
        "mechanical clearance",
    ),
    "hysteresis_direction_dependent_output": (
        "hysteresis",
        "접근 방향",
        "output 차이",
    ),
    "static_friction_starting_force": (
        "static friction",
        "starting force",
    ),
    "stiction_stick_then_jump": (
        "stiction",
        "stick then jump",
        "travel jump",
    ),
    "stick_slip_repeated_motion": (
        "stick-slip",
        "repeated motion",
    ),
    "stiction_limit_cycle_path": (
        "controller output 누적",
        "PV limit cycle",
    ),
    "oscillation_requires_differential_diagnosis": (
        "differential diagnosis",
        "sensor noise",
        "process disturbance",
    ),
    "response_time_dead_dynamic_separation": (
        "response time",
        "dead time",
        "dynamic time",
    ),
    "opening_closing_response_asymmetry": (
        "opening response",
        "closing response",
        "asymmetry",
    ),
    "small_step_test_control_resolution": (
        "small-step test",
        "minimum movement",
        "repeatability",
    ),
    "large_step_test_pneumatic_capacity": (
        "large-step test",
        "stroke time",
        "pneumatic capacity",
    ),
    "reversal_test_deadband_hysteresis": (
        "reversal test",
        "deadband",
        "hysteresis",
    ),
    "step_sensitivity_not_resolution_only": (
        "step sensitivity",
        "minimum command",
        "minimum travel",
    ),
    "positioner_closed_loop_position_feedback": (
        "position feedback",
        "stem position",
        "actuator pressure",
    ),
    "positioner_cannot_remove_mechanical_backlash": (
        "positioner limitation",
        "mechanical backlash",
        "linkage repair",
    ),
    "positioner_cannot_replace_actuator_thrust": (
        "actuator thrust",
        "sizing",
        "supply pressure",
    ),
    "positioner_gain_speed_stability_tradeoff": (
        "positioner gain",
        "response speed",
        "overshoot",
        "hunting",
    ),
    "pneumatic_supply_tubing_spool_capacity": (
        "supply pressure",
        "tubing",
        "spool capacity",
        "relay capacity",
    ),
    "volume_booster_flow_capacity_feedback_condition": (
        "volume booster",
        "feedback",
        "bypass",
    ),
    "hunting_multicausal_diagnosis": (
        "booster gain",
        "feedback noise",
        "loop interaction",
    ),
    "improvement_verify_same_test_and_process_result": (
        "same test",
        "PV variability",
        "air consumption",
    ),
}

POSITIVE_ANSWER = """
Final control element에서 controller output은 positioner와 actuator pressure를
거쳐 valve travel, flow와 process variability로 연결된다. Direction reversal
deadband는 input range의 불감 구간이고 dead time의 time delay와 구분한다.
Linkage backlash와 mechanical clearance는 hysteresis를 만들며 동일 입력의
접근 방향에 따라 output 차이가 생긴다. Packing의 static friction과 starting
force를 넘으면 stiction 상태에서 stem이 stick then jump하고 travel jump와
stick-slip repeated motion이 나타난다. Controller output 누적과 sudden
movement는 PV limit cycle로 이어질 수 있으므로 oscillation은 differential
diagnosis로 positioner gain, sensor noise와 process disturbance를 구분한다.
Valve response time은 dead time과 dynamic time으로 구분한다. Opening response와
closing response는 공압 경로와 spring force에 의해 asymmetry를 가질 수 있다.
Small-step test는 minimum movement와 repeatability를 확인한다. Large-step test는
stroke time과 pneumatic capacity를 확인한다. Reversal test는 deadband와
hysteresis를 확인한다. Step sensitivity는 minimum command와 minimum travel을
resolution과 구분한다. Positioner의 position feedback은 command와 stem position
오차에 따라 actuator pressure를 조절한다. Positioner limitation 때문에
mechanical backlash에는 linkage repair가 필요하다. 부족한 actuator thrust,
sizing과 supply pressure 문제도 positioner가 대신하지 못한다. Positioner gain은
response speed, overshoot와 hunting의 trade-off를 가진다. Supply pressure,
tubing, spool capacity와 relay capacity를 확인한다. Volume booster는 feedback과
bypass 조건에서 적용한다. Booster gain, feedback noise와 loop interaction도
hunting 원인으로 진단한다. 개선 후에는 same test로 PV variability, quality와
air consumption을 비교한다.
""".strip()

PARTIAL_ANSWER = """
Direction reversal deadband에서 valve travel이 정지하는 불감 구간이 발생한다.
Deadband의 input range는 dead time의 time delay와 다르다. Packing static
friction과 starting force 때문에 stiction이 생기면 stem은 stick then jump하고
travel jump가 발생한다. Stick-slip repeated motion과 controller output 누적은
PV limit cycle로 이어질 수 있다.
""".strip()

SAFE_CONTRAST_ANSWER = (
    "Deadband는 dead time과 다르다. Positioner는 mechanical backlash 자체를 "
    "제거하지 못한다. Volume booster가 항상 안정성을 높이는 것은 아니다."
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


def candidate_topics(result: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for candidate in result.get("candidates") or []:
        if not isinstance(candidate, dict):
            continue
        answer = candidate.get("answer") or {}
        topic_id = answer.get("topic_id") or candidate.get("topic_id")
        if isinstance(topic_id, str) and topic_id not in found:
            found.append(topic_id)
    return found


def coverage_rows(text: str) -> dict[str, bool]:
    normalized_text = " ".join(text.casefold().split())
    return {
        requirement: all(
            " ".join(marker.casefold().split()) in normalized_text
            for marker in markers
        )
        for requirement, markers in REQUIREMENT_MARKERS.items()
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
        self.assertEqual(self.source_fact["topic_id"], TOPIC)
        self.assertEqual(self.generated_fact["topic_id"], TOPIC)
        self.assertEqual(self.generated_logic["topic_id"], TOPIC)
        self.assertEqual(self.generated_profile["topic_id"], TOPIC)
        self.assertEqual(self.generated_model["topic_id"], TOPIC)
        self.assertEqual(self.generated_importance["topic_id"], TOPIC)
        self.assertEqual(self.generated_manifest["topic_id"], TOPIC)

        manifest = load_json(
            GENERATED_DIR / "topic_pack_manifest.generated.json"
        )
        self.assertEqual(len(manifest["topics"]), 26)
        self.assertEqual(
            [
                index
                for index, row in enumerate(manifest["topics"])
                if row.get("topic_id") == TOPIC
            ],
            [2],
        )

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
        self.assertEqual(len(set(source_ids)), 24)

    def test_logic_contract_has_fatal_major_safe_and_no_caps(
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
            14,
        )
        self.assertGreaterEqual(
            len(self.generated_profile["safe_conditions"]),
            14,
        )
        self.assertFalse(self.generated_logic["enabled"])
        self.assertEqual(self.generated_logic["fatal_checks"], [])
        self.assertEqual(self.generated_logic["major_checks"], [])
        self.assertEqual(
            self.generated_profile["candidate_extraction"]["rules"],
            [],
        )
        self.assertFalse(
            self.generated_profile["score_policy"][
                "direct_score_application"
            ]
        )
        self.assertIsNone(
            self.generated_profile["score_policy"][
                "recommended_ceiling"
            ]
        )
        self.assertEqual(
            self.generated_profile["score_policy"][
                "direct_d_e_effect"
            ],
            "none",
        )

    def test_model_patterns_and_outline_cover_every_anchor(
        self,
    ) -> None:
        referenced: set[str] = set()
        patterns = self.source_model["expected_question_patterns"]
        outlines = self.source_model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        for pattern in patterns:
            referenced.update(pattern["required_anchor_ids"])
        for outline in outlines:
            referenced.update(outline["anchor_refs"])
        self.assertEqual(referenced, set(EXPECTED_ANCHOR_IDS))

    def test_routing_aliases_are_specific_and_generated_identically(
        self,
    ) -> None:
        aliases = self.source_model["routing_aliases"]
        self.assertEqual(
            self.generated_model["topic_aliases"],
            aliases,
        )
        self.assertFalse(BROAD_ALIASES & set(aliases))
        self.assertIn("control valve deadband stiction", aliases)
        self.assertIn("valve response time", aliases)
        self.assertIn("positioner dynamic performance", aliases)
        self.assertIn("volume booster response", aliases)

    def test_importance_and_manifest_contract(self) -> None:
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
            "DIAGNOSIS_ACTION",
        )


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
            SECOND_ORDER_TOPIC,
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

    def assert_not_target(self, result: dict[str, Any]) -> None:
        self.assertNotEqual(selected_topic(result), TOPIC, msg=result)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)

    def test_deadband_stiction_routes_with_pipeline_context(
        self,
    ) -> None:
        result = self.route(
            "제어밸브의 데드밴드와 스틱션이 stick-slip 및 "
            "공정변동을 만드는 원인과 개선방안을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_stick_slip_limit_cycle_routes_with_pipeline_context(
        self,
    ) -> None:
        result = self.route(
            "Control valve stick-slip이 controller output 누적과 "
            "PV limit cycle을 만드는 과정을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_response_time_routes_with_pipeline_context(
        self,
    ) -> None:
        result = self.route(
            "제어밸브 응답시간을 dead time과 dynamic time으로 "
            "구분하고 opening과 closing 차이를 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_step_tests_route_with_pipeline_context(self) -> None:
        result = self.route(
            "제어밸브의 small-step, large-step 및 direction "
            "reversal test의 목적과 step sensitivity를 비교하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_positioner_dynamic_routes_with_pipeline_context(
        self,
    ) -> None:
        result = self.route(
            "Positioner의 position feedback과 gain이 제어밸브 "
            "응답속도, overshoot와 hunting에 미치는 영향을 "
            "설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_pneumatic_booster_routes_with_pipeline_context(
        self,
    ) -> None:
        result = self.route(
            "Supply pressure, tubing, spool capacity와 volume "
            "booster가 제어밸브 응답시간과 hunting에 미치는 "
            "영향을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_topic1_question_is_not_absorbed(self) -> None:
        result = self.route(
            "공압식 제어밸브의 불평형력, 마찰력, actuator "
            "thrust와 fail-safe spring sizing 기준을 설명하시오.",
            fact_topic=TOPIC_1,
            question_type_topic=TOPIC_1,
        )
        self.assert_primary(result, TOPIC_1)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)

    def test_topic2_question_is_not_absorbed(self) -> None:
        result = self.route(
            "제어밸브의 inherent와 installed characteristic을 "
            "비교하고 linear, equal percentage와 quick opening을 "
            "설명하시오.",
            fact_topic=TOPIC_2,
            question_type_topic=TOPIC_2,
        )
        self.assert_primary(result, TOPIC_2)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)

    def test_authority_rangeability_is_not_topic3(self) -> None:
        result = self.route(
            "Valve authority, rangeability와 quantitative "
            "installed gain이 제어 성능에 미치는 영향을 설명하시오.",
        )
        self.assert_not_target(result)

    def test_cv_kv_sizing_is_not_topic3(self) -> None:
        result = self.route(
            "액체 제어밸브의 Cv, Kv, Reynolds correction과 "
            "valve size selection 절차를 설명하시오.",
        )
        self.assert_not_target(result)

    def test_generic_second_order_is_not_topic3(self) -> None:
        result = self.route(
            "일반 2차 시스템의 damping ratio, natural frequency와 "
            "dead time이 step response에 미치는 영향을 설명하시오.",
            fact_topic=SECOND_ORDER_TOPIC,
            question_type_topic=SECOND_ORDER_TOPIC,
        )
        self.assert_primary(result, SECOND_ORDER_TOPIC)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)

    def test_question_only_routing_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "제어밸브의 inherent와 installed characteristic, "
            "equal percentage 선정 기준을 설명하시오.",
            answer_text=(
                "Deadband, stiction, response time, positioner gain, "
                "volume booster와 hunting을 상세히 설명한다."
            ),
            fact_topic=TOPIC_2,
            question_type_topic=TOPIC_2,
        )
        self.assert_primary(result, TOPIC_2)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)


class SemanticContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.source_fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_positive_sample_covers_all_explicit_requirement_rows(
        self,
    ) -> None:
        rows = coverage_rows(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(REQUIREMENT_MARKERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_partial_sample_preserves_definitions_but_misses_dynamic_rows(
        self,
    ) -> None:
        rows = coverage_rows(PARTIAL_ANSWER)
        for requirement in (
            "deadband_definition_direction_reversal",
            "deadband_not_dead_time",
            "static_friction_starting_force",
            "stiction_stick_then_jump",
            "stick_slip_repeated_motion",
            "stiction_limit_cycle_path",
        ):
            self.assertTrue(rows[requirement], msg=rows)

        for requirement in (
            "large_step_test_pneumatic_capacity",
            "positioner_closed_loop_position_feedback",
            "pneumatic_supply_tubing_spool_capacity",
            "volume_booster_flow_capacity_feedback_condition",
            "improvement_verify_same_test_and_process_result",
        ):
            self.assertFalse(rows[requirement], msg=rows)

    def test_negative_samples_map_to_fatal_contracts_and_candidates(
        self,
    ) -> None:
        fatal_ids = [
            item["id"]
            for item in self.source_fact["fatal_wrong_claims"]
        ]
        self.assertEqual(fatal_ids, EXPECTED_FATAL_IDS)

        for item in self.source_fact["fatal_wrong_claims"]:
            with self.subTest(rule_id=item["id"]):
                candidates = extract_logic_evidence_candidates(
                    item["claim"],
                    self.profile,
                )
                self.assertTrue(candidates, msg=item)

    def test_safe_contrast_is_registered_and_extracted_without_regex_verdict(
        self,
    ) -> None:
        self.assertIn(
            "Deadband는 dead time과 다르다.",
            self.profile["safe_conditions"],
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

    def test_conditional_major_claims_are_separate_from_fatal_contract(
        self,
    ) -> None:
        major_ids = {
            item["id"]
            for item in self.profile["major_checks"]
        }
        fatal_ids = {
            item["id"]
            for item in self.source_fact["fatal_wrong_claims"]
        }
        self.assertEqual(major_ids, set(EXPECTED_MAJOR_IDS))
        self.assertEqual(fatal_ids, set(EXPECTED_FATAL_IDS))
        self.assertTrue(major_ids.isdisjoint(fatal_ids))

    def test_mocked_semantic_fatal_verdict_is_c_owned(
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
            "confidence": 0.95,
            "reason": "Deadband와 dead time을 동일시하였다.",
            "findings": [
                {
                    "candidate_id": candidates[0]["id"],
                    "rule_id": (
                        "control_valve_deadband_same_as_dead_time"
                    ),
                    "severity": "fatal",
                    "message": "핵심 개념을 반대로 설명했다.",
                    "correct_rule": (
                        "Deadband는 입력 불감 영역이고 dead time은 "
                        "시간 지연이다."
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
        self.assertEqual(
            result["recommended_ceiling"],
            10.0,
        )

    def test_mocked_safe_verdict_has_no_fatal_or_ceiling(
        self,
    ) -> None:
        mocked = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "개념을 구분하고 조건부 개선을 제시했다.",
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
