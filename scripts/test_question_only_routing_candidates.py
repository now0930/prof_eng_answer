from __future__ import annotations

import ast
import inspect
import json
from pathlib import Path
import unittest

import grading_agents
from semantic_router_shadow import (
    augment_rule_candidates_for_shadow,
    build_question_demand_aware_rule_candidates,
)

ROOT=Path(__file__).resolve().parents[1]

FORCES=(
    "control_valve_fluid_forces_unbalance_friction_"
    "actuator_sizing_fail_safe"
)
STICTION=(
    "control_valve_deadband_stiction_response_time_"
    "positioner_dynamic_performance"
)
SELECTION=(
    "control_valve_selection_process_pressure_"
    "temperature_flow_media_lifecycle"
)
CANONICAL=(
    ROOT
    / "calibration/question_demand_contracts/"
    "28219962740fca5e0750a26176750717da6d7beb2ea11bd46c02da6e2013edd2.json"
)


class QuestionOnlyRoutingCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        golden=json.loads(
            (
                ROOT
                / "calibration/qtype_golden/cases/"
                "diagnosis_action.json"
            ).read_text(encoding="utf-8")
        )
        cases=golden.get("cases") or []
        cls.question=str(cases[0]["question"])

        canonical=json.loads(
            CANONICAL.read_text(encoding="utf-8")
        )
        cls.qd={
            "status":"ok",
            "demands":canonical.get("demands") or [],
        }

    def test_demand_aware_candidates_are_exact_two_owners(self):
        result=build_question_demand_aware_rule_candidates(
            self.question,
            self.qd,
        )

        topics=[
            row["answer"]["topic_id"]
            for row in result["candidates"]
        ]
        self.assertEqual(
            topics,
            [FORCES,STICTION],
        )
        self.assertNotIn(SELECTION,topics)
        self.assertTrue(
            result[
                "question_demand_aware_authoritative"
            ]
        )
        self.assertFalse(result["student_answer_used"])
        self.assertFalse(result["fact_eval_used"])

        winners={
            row["demand_id"]:row["topic_id"]
            for row in result[
                "question_demand_aware_candidate_result"
            ]["demand_winners"]
        }
        self.assertEqual(
            {
                did
                for did,topic in winners.items()
                if topic==FORCES
            },
            {f"D{i}" for i in range(1,6)},
        )
        self.assertEqual(
            {
                did
                for did,topic in winners.items()
                if topic==STICTION
            },
            {f"D{i}" for i in range(6,11)},
        )

    def test_qd_unavailable_uses_neutral_rule_plus_augment(self):
        question=(
            "RTD와 열전대의 측정 원리, 오차 특성 및 "
            "적용성을 비교하시오."
        )
        result=build_question_demand_aware_rule_candidates(
            question,
            None,
        )
        topics=[
            row["answer"]["topic_id"]
            for row in result["candidates"]
        ]
        self.assertIn(
            "rtd_temperature_sensor_principle_pt100_wiring_compensation",
            topics,
        )
        self.assertIn(
            "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
            topics,
        )
        self.assertEqual(
            topics[:2],
            [
                "rtd_temperature_sensor_principle_pt100_wiring_compensation",
                "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
            ],
        )
        self.assertEqual(
            result[
                "question_demand_aware_candidate_result"
            ]["strategy"],
            "neutral_question_only_rule_plus_augment_fallback",
        )
        self.assertTrue(
            result[
                "question_demand_aware_authoritative"
            ]
        )
        self.assertTrue(result["question_only"])
        self.assertFalse(result["student_answer_used"])
        self.assertFalse(result["fact_eval_used"])
        for row in result["candidates"]:
            self.assertEqual(row.get("fact_score"),0)
            self.assertEqual(row.get("answer_score"),0)

    def test_qd_unavailable_single_topic_keeps_assisted_candidate(self):
        question=(
            "제어밸브의 캐비테이션과 플래싱의 발생 원리, "
            "차이점 및 방지대책을 설명하시오."
        )
        expected=(
            "control_valve_cavitation_flashing_choked_flow_"
            "damage_prevention"
        )
        result=build_question_demand_aware_rule_candidates(
            question,
            None,
        )
        topics=[
            row["answer"]["topic_id"]
            for row in result["candidates"]
        ]
        self.assertIn(expected,topics)
        self.assertTrue(
            result[
                "question_demand_aware_authoritative"
            ]
        )
        for row in result["candidates"]:
            self.assertEqual(row.get("fact_score"),0)
            self.assertEqual(row.get("answer_score"),0)

    def test_authoritative_candidates_do_not_broaden(self):
        result=build_question_demand_aware_rule_candidates(
            self.question,
            self.qd,
        )
        augmented=augment_rule_candidates_for_shadow(
            self.question,
            result,
        )
        topics=[
            row["answer"]["topic_id"]
            for row in augmented["candidates"]
        ]
        self.assertEqual(
            topics,
            [FORCES,STICTION],
        )
        self.assertTrue(
            augmented[
                "shadow_candidate_recall_adapter"
            ][
                "authoritative_question_demand_aware"
            ]
        )

    def test_phase10_never_feeds_legacy_result_to_routing(self):
        source=inspect.getsource(
            grading_agents._phase10_run_model_answer_reference
        )
        tree=ast.parse(source)
        legacy=[]
        question_only=[]
        for node in ast.walk(tree):
            if not isinstance(node,ast.keyword):
                continue
            if node.arg!="rule_result":
                continue
            if (
                isinstance(node.value,ast.Name)
                and node.value.id=="result"
            ):
                legacy.append(node.lineno)
            if (
                isinstance(node.value,ast.Name)
                and node.value.id=="semantic_rule_result"
            ):
                question_only.append(node.lineno)

        self.assertFalse(legacy)
        self.assertGreaterEqual(len(question_only),2)
        self.assertIn(
            "build_question_demand_aware_rule_candidates",
            source,
        )


if __name__ == "__main__":
    unittest.main()
