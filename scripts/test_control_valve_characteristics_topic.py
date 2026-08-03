#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_llm_verifier import (  # noqa: E402
    extract_logic_evidence_candidates,
    verify_logic_with_llm,
)
from model_answer_router import find_model_answer_reference  # noqa: E402


TOPIC = (
    "control_valve_characteristics_inherent_installed_"
    "equal_percentage_linear_quick_opening"
)
TOPIC_1 = (
    "control_valve_fluid_forces_unbalance_friction_"
    "actuator_sizing_fail_safe"
)
PID_TOPIC = "pid_controller_tuning_sequence_gain_effects"

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"

EXPECTED_ANCHOR_IDS = [
    "control_valve_inherent_characteristic_definition",
    "control_valve_installed_characteristic_definition",
    "control_valve_inherent_installed_distinction",
    "control_valve_normalized_travel_relative_capacity",
    "control_valve_flow_valve_dp_dependency_boundary",
    "control_valve_linear_characteristic_definition",
    "control_valve_equal_percentage_characteristic_definition",
    "control_valve_equal_percentage_exponential_relation",
    "control_valve_equal_percentage_absolute_increment",
    "control_valve_quick_opening_characteristic_definition",
    "control_valve_inherent_constant_pressure_drop_condition",
    "control_valve_installed_pressure_drop_redistribution",
    "control_valve_system_resistance_flow_squared_relation",
    "control_valve_pump_curve_installed_characteristic_effect",
    "control_valve_static_head_installed_characteristic_effect",
    "control_valve_linear_installed_distortion",
    "control_valve_equal_percentage_partial_compensation",
    "control_valve_characteristic_selection_criteria",
    "control_valve_application_mapping_is_conditional",
    "control_valve_installed_local_slope_topic_boundary",
    "control_valve_manufacturer_curve_system_model_verification",
    "control_valve_commissioning_characteristic_verification",
]

EXPECTED_FATAL_IDS = [
    "control_valve_inherent_installed_same_concept",
    "control_valve_inherent_includes_system_resistance",
    "control_valve_installed_is_constant_dp_bench_curve",
    "control_valve_equal_percentage_equal_absolute_increment",
    "control_valve_equal_percentage_linear_with_travel",
    "control_valve_equal_percentage_largest_low_travel_increment",
    "control_valve_linear_always_installed_linear",
    "control_valve_quick_opening_precision_control_default",
    "control_valve_system_pressure_distribution_no_effect",
    "control_valve_variable_dp_no_installed_distortion",
    "control_valve_trim_only_determines_installed_curve",
    "control_valve_linear_guarantees_constant_process_gain",
]

EXPECTED_MAJOR_IDS = [
    "control_valve_equal_percentage_always_best",
    "control_valve_heat_exchanger_unconditional_mapping",
    "control_valve_quick_opening_never_modulates",
]

BROAD_ALIASES = {
    "control valve",
    "제어밸브",
    "valve",
    "flow",
    "유량",
    "linear",
    "installed",
    "gain",
    "performance",
    "authority",
    "rangeability",
    "Cv",
    "Kv",
    "sizing",
    "balanced trim",
    "unbalanced trim",
    "stiction",
    "deadband",
}

POSITIVE_ANSWER = """
제어밸브의 Inherent Flow Characteristic는 일정한 밸브 차압에서
normalized travel과 relative Cv의 관계이다. Installed Flow
Characteristic는 실제 배관계에서 travel과 actual flow의 관계이다.
Linear는 같은 travel 증가마다 Cv가 같은 절대량 증가한다.
Equal Percentage는 현재 Cv에 대해 같은 비율 증가하므로 저개도에서는
절대 증가량이 작고 고개도에서는 커진다. Quick Opening은 초기 travel에서
큰 capacity를 만들고 이후 평탄해져 On-Off 또는 bypass에 일반적으로 적합하다.
비압축성·비초크 조건에서 Q는 Cv와 valve differential pressure의 제곱근에
의존한다. 유량 증가 시 system pressure loss는 KQ² 형태로 증가하여 valve
차압이 재분배된다. centrifugal pump curve와 static head도 운전점에 영향을 준다.
따라서 minimum, normal, maximum flow와 제어 목적을 함께 보며, 열교환기라는
이유만으로 Equal Percentage를 무조건 선정하지 않는다. manufacturer curve와
hydraulic system model로 예상 installed curve를 검토하고 commissioning에서
command, travel, pressure와 flow response를 확인한다.
""".strip()

PARTIAL_ANSWER = """
Inherent Flow Characteristic는 일정한 밸브 차압에서 travel과 Cv의 관계이다.
Linear는 같은 절대량, Equal Percentage는 같은 비율로 증가한다.
Quick Opening은 초기 travel에서 큰 capacity를 만든다.
""".strip()

SAFE_CONTRAST_ANSWER = (
    "Equal Percentage는 같은 절대량이 아니라 같은 비율로 증가한다. "
    "Linear inherent trim이라도 실제 installed flow가 항상 선형인 것은 아니다."
)

NEGATIVE_ANSWER = (
    "Inherent Characteristic와 Installed Characteristic는 동일한 개념이다. "
    "Equal Percentage는 동일 travel마다 Cv가 같은 절대량 증가한다."
)

REQUIREMENT_MARKERS = {
    "inherent_definition": ("Inherent Flow Characteristic", "일정한 밸브 차압"),
    "installed_definition": ("Installed Flow", "실제 배관계"),
    "linear_definition": ("Linear", "같은 절대량"),
    "equal_percentage_definition": ("Equal Percentage", "같은 비율"),
    "quick_opening_definition": ("Quick Opening", "초기 travel"),
    "pressure_drop_redistribution": ("valve", "차압이 재분배"),
    "system_resistance": ("KQ²",),
    "pump_static_head": ("pump curve", "static head"),
    "selection_range": ("minimum", "normal", "maximum"),
    "conditional_application": ("무조건 선정하지 않는다",),
    "manufacturer_verification": ("manufacturer curve", "system model"),
    "commissioning_verification": ("commissioning", "flow response"),
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
            f"{filename}: expected one {TOPIC} entry, found {len(matches)}"
        )
    return matches[0]


def selected_topic(result: dict[str, Any]) -> str | None:
    primary = result.get("primary_reference") or {}
    if isinstance(primary, dict):
        value = primary.get("topic_id")
        if isinstance(value, str):
            return value
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
    return {
        requirement: all(marker in text for marker in markers)
        for requirement, markers in REQUIREMENT_MARKERS.items()
    }


class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.source_logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.source_model = load_json(SOURCE_DIR / "model_answer.json")
        cls.source_importance = load_json(SOURCE_DIR / "topic_importance.json")
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
        self.assertEqual(len(set(source_ids)), 22)
        self.assertEqual(
            self.source_fact["core_facts"],
            [item["statement"] for item in self.source_fact["anchors"]],
        )

    def test_logic_contract_has_fatal_major_safe_and_no_deterministic_verdicts(
        self,
    ) -> None:
        fatal_ids = [
            item["id"]
            for item in self.source_fact["fatal_wrong_claims"]
        ]
        major_ids = sorted(
            item["id"]
            for item in self.generated_profile["major_checks"]
        )
        self.assertEqual(fatal_ids, EXPECTED_FATAL_IDS)
        self.assertEqual(major_ids, EXPECTED_MAJOR_IDS)
        self.assertEqual(len(self.generated_profile["fatal_conditions"]), 12)
        self.assertGreaterEqual(len(self.generated_profile["safe_conditions"]), 8)
        self.assertGreaterEqual(
            len(self.generated_profile["false_positive_cautions"]),
            8,
        )
        self.assertFalse(self.generated_logic["enabled"])
        self.assertEqual(self.generated_logic["fatal_checks"], [])
        self.assertEqual(self.generated_logic["major_checks"], [])
        self.assertEqual(
            self.generated_profile["candidate_extraction"]["rules"],
            [],
        )
        self.assertEqual(
            self.generated_profile["output_contract"]["excluded_score_layers"],
            ["D", "E"],
        )
        self.assertFalse(
            self.generated_profile["score_policy"]["direct_score_application"]
        )

    def test_model_patterns_and_outline_cover_every_anchor(self) -> None:
        referenced: set[str] = set()
        patterns = self.source_model["expected_question_patterns"]
        outlines = self.source_model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 7)
        for pattern in patterns:
            referenced.update(pattern["required_anchor_ids"])
        for outline in outlines:
            referenced.update(outline["anchor_refs"])
        self.assertEqual(referenced, set(EXPECTED_ANCHOR_IDS))

    def test_routing_aliases_are_specific_and_generated_identically(self) -> None:
        aliases = self.source_model["routing_aliases"]
        self.assertEqual(
            self.generated_model["topic_aliases"],
            aliases,
        )
        self.assertFalse(BROAD_ALIASES & set(aliases))
        self.assertIn("inherent flow characteristic", aliases)
        self.assertIn("installed flow characteristic", aliases)
        self.assertIn("equal percentage valve characteristic", aliases)
        self.assertIn("quick opening valve characteristic", aliases)

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
            "NORMAL",
        )
        self.assertEqual(
            self.generated_importance["question_type"],
            "COMPARE_SELECTION",
        )
        self.assertEqual(
            self.generated_manifest["files"],
            [
                "fact_anchor.json",
                "model_answer.json",
                "topic_importance.json",
                "logic_check.json",
                "README.md",
            ],
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
        for topic_id in (TOPIC, TOPIC_1, PID_TOPIC):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(f"required Topic missing: {topic_id}")

    @classmethod
    def question_type_eval(cls, topic_id: str) -> dict[str, Any]:
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

    def test_inherent_installed_comparison_routes_to_topic2(self) -> None:
        result = self.route(
            "제어밸브의 inherent flow characteristic와 "
            "installed flow characteristic를 비교하시오.",
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_three_characteristics_comparison_routes_to_topic2(self) -> None:
        result = self.route(
            "제어밸브의 linear valve characteristic, "
            "equal percentage valve characteristic와 "
            "quick opening valve characteristic를 비교하고 "
            "선정기준을 설명하시오.",
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_installed_distortion_routes_with_pipeline_context(self) -> None:
        result = self.route(
            "밸브 고유 유량특성이 실제 배관에서 system resistance, "
            "pump curve와 static head에 의해 installed flow curve로 "
            "변형되는 원인을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_equal_percentage_selection_routes_with_pipeline_context(
        self,
    ) -> None:
        result = self.route(
            "넓은 부하범위에서 equal percentage valve characteristic를 "
            "선정하는 이유와 적용 제한을 설명하시오.",
            fact_topic=TOPIC,
            question_type_topic=TOPIC,
        )
        self.assert_primary(result, TOPIC)

    def test_topic1_actuator_question_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "공압식 제어밸브의 불평형력과 마찰력 및 "
            "Fail-Safe 스프링 선정기준을 설명하시오.",
            answer_text=(
                "부가 설명으로 equal percentage valve characteristic와 "
                "installed flow characteristic를 언급한다."
            ),
            fact_topic=TOPIC_1,
            question_type_topic=TOPIC_1,
        )
        self.assert_primary(result, TOPIC_1)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)

    def test_topic1_balanced_trim_question_is_not_absorbed(self) -> None:
        result = self.route(
            "Balanced trim과 unbalanced trim의 불평형력과 "
            "요구추력 차이를 설명하시오.",
            fact_topic=TOPIC_1,
            question_type_topic=TOPIC_1,
        )
        self.assert_primary(result, TOPIC_1)
        self.assertNotIn(TOPIC, candidate_topics(result), msg=result)

    def test_authority_rangeability_question_is_not_topic2(self) -> None:
        result = self.route(
            "Valve Authority, Rangeability와 Installed Gain이 "
            "제어성능에 미치는 영향을 설명하시오.",
        )
        self.assert_not_target(result)

    def test_cv_kv_sizing_question_is_not_topic2(self) -> None:
        result = self.route(
            "액체 제어밸브의 Cv와 Kv 변환, Reynolds 수 보정과 "
            "밸브 sizing 절차를 설명하시오.",
        )
        self.assert_not_target(result)

    def test_generic_linear_system_question_is_not_topic2(self) -> None:
        result = self.route(
            "선형시스템의 상태방정식과 중첩의 원리를 설명하시오.",
            question_type_topic=PID_TOPIC,
        )
        self.assert_not_target(result)

    def test_answer_only_characteristic_terms_cannot_select_topic2(
        self,
    ) -> None:
        result = self.route(
            "제어시스템의 안정도 판별법을 설명하시오.",
            answer_text=(
                "Inherent flow characteristic, installed flow characteristic, "
                "equal percentage valve characteristic를 길게 설명하였다."
            ),
        )
        self.assert_not_target(result)


class SemanticContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.source_fact = load_json(SOURCE_DIR / "fact_anchor.json")

    def test_positive_sample_covers_all_explicit_requirement_rows(self) -> None:
        rows = coverage_rows(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(REQUIREMENT_MARKERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_partial_sample_preserves_definitions_but_misses_system_rows(
        self,
    ) -> None:
        rows = coverage_rows(PARTIAL_ANSWER)
        self.assertTrue(rows["inherent_definition"])
        self.assertTrue(rows["linear_definition"])
        self.assertTrue(rows["equal_percentage_definition"])
        self.assertTrue(rows["quick_opening_definition"])
        for requirement in (
            "installed_definition",
            "pressure_drop_redistribution",
            "system_resistance",
            "pump_static_head",
            "selection_range",
            "conditional_application",
            "manufacturer_verification",
            "commissioning_verification",
        ):
            self.assertFalse(rows[requirement], msg=rows)

    def test_negative_samples_map_to_fatal_contracts_and_candidates(
        self,
    ) -> None:
        fatal_map = {
            item["id"]: item["claim"]
            for item in self.source_fact["fatal_wrong_claims"]
        }
        self.assertEqual(
            fatal_map["control_valve_inherent_installed_same_concept"],
            "Inherent Characteristic와 Installed Characteristic는 동일한 개념이다.",
        )
        self.assertEqual(
            fatal_map[
                "control_valve_equal_percentage_equal_absolute_increment"
            ],
            "Equal Percentage는 동일 travel마다 유량 또는 Cv가 같은 절대량만큼 증가한다.",
        )
        candidates = extract_logic_evidence_candidates(
            NEGATIVE_ANSWER,
            self.profile,
        )
        self.assertTrue(candidates)
        evidence = " ".join(item["text"] for item in candidates)
        self.assertIn("동일한 개념", evidence)
        self.assertIn("같은 절대량", evidence)

    def test_safe_contrast_is_registered_and_extracted_without_regex_verdict(
        self,
    ) -> None:
        safe_conditions = self.profile["safe_conditions"]
        self.assertIn(
            "Equal Percentage는 같은 절대량이 아니라 같은 비율로 증가한다.",
            safe_conditions,
        )
        self.assertEqual(
            self.profile["candidate_extraction"]["rules"],
            [],
        )
        candidates = extract_logic_evidence_candidates(
            SAFE_CONTRAST_ANSWER,
            self.profile,
        )
        self.assertTrue(candidates)
        evidence = " ".join(item["text"] for item in candidates)
        self.assertIn("같은 절대량이 아니라 같은 비율", evidence)
        self.assertIn("항상 선형인 것은 아니다", evidence)

    def test_mocked_semantic_fatal_verdict_is_c_owned(self) -> None:
        candidates = extract_logic_evidence_candidates(
            NEGATIVE_ANSWER,
            self.profile,
        )
        self.assertTrue(candidates)
        candidate_id = candidates[0]["id"]
        mocked = {
            "verdict": "fatal",
            "confidence": 0.95,
            "reason": "대표 오개념이 직접 주장되었다.",
            "findings": [
                {
                    "candidate_id": candidate_id,
                    "rule_id": (
                        "control_valve_inherent_installed_same_concept"
                    ),
                    "severity": "fatal",
                    "message": "Inherent와 Installed를 동일시하였다.",
                    "correct_rule": "두 특성의 기준조건과 system boundary를 구분한다.",
                }
            ],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked,
        ):
            result = verify_logic_with_llm(NEGATIVE_ANSWER, TOPIC)
        self.assertTrue(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "fatal")
        self.assertEqual(result["findings"][0]["affected_layers"], ["C"])
        self.assertEqual(result["findings"][0]["engine"], "llm_verifier_profile_v1")

    def test_mocked_safe_verdict_has_no_fatal_or_ceiling(self) -> None:
        mocked = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "오답을 반박한 올바른 설명이다.",
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
