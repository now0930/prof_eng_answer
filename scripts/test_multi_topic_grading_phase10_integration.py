from __future__ import annotations

import copy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import grading_agents as ga


QUESTION_MULTI = (
    "RTD와 열전대의 측정 원리, 오차 특성 및 "
    "적용성을 비교하시오."
)
QUESTION_SINGLE = (
    "제어밸브의 캐비테이션과 플래싱의 발생 원리, "
    "차이점 및 방지대책을 설명하시오."
)

RTD_TOPIC = (
    "rtd_temperature_sensor_principle_pt100_wiring_compensation"
)
TC_TOPIC = (
    "thermocouple_temperature_sensor_seebeck_"
    "reference_junction_compensation"
)
CAVITATION_TOPIC = (
    "control_valve_cavitation_flashing_choked_flow_"
    "damage_prevention"
)


def semantic_multi() -> dict:
    return {
        "version": "semantic_router_shadow_v1",
        "shadow": True,
        "enabled": True,
        "status": "ok",
        "ok": True,
        "routing_mode": "MULTI_TOPIC",
        "primary_topic_ids": [RTD_TOPIC, TC_TOPIC],
        "supporting_topic_ids": [],
        "demand_mappings": [
            {
                "demand_id": "D1",
                "topic_id": RTD_TOPIC,
                "role": "PRIMARY",
            },
            {
                "demand_id": "D1",
                "topic_id": TC_TOPIC,
                "role": "PRIMARY",
            },
        ],
        "uncovered_demand_ids": [],
        "student_answer_used": False,
        "routing_effect": "none",
        "score_effect": "none",
        "llm_called": False,
    }


def semantic_single() -> dict:
    return {
        "version": "semantic_router_shadow_v1",
        "shadow": True,
        "enabled": True,
        "status": "ok",
        "ok": True,
        "routing_mode": "SINGLE_TOPIC",
        "primary_topic_ids": [CAVITATION_TOPIC],
        "supporting_topic_ids": [],
        "demand_mappings": [],
        "uncovered_demand_ids": [],
        "student_answer_used": False,
        "routing_effect": "none",
        "score_effect": "none",
        "llm_called": False,
    }


class MultiTopicPhase10IntegrationTest(unittest.TestCase):
    def _call(
        self,
        *,
        question: str,
        semantic: dict,
        multi_enabled: bool,
        assisted_enabled: bool,
    ) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(
                os.environ,
                {
                    "MULTI_TOPIC_GRADING_ENABLED": (
                        "1" if multi_enabled else "0"
                    ),
                    "ASSISTED_ROUTING_ENABLED": (
                        "1" if assisted_enabled else "0"
                    ),
                    "QUESTION_DEMAND_SHADOW_ENABLED": "0",
                    "SEMANTIC_ROUTER_SHADOW_ENABLED": "0",
                },
                clear=False,
            ):
                with patch.object(
                    ga,
                    "_phase10_run_semantic_router_shadow",
                    return_value=copy.deepcopy(semantic),
                ):
                    return ga._phase10_run_model_answer_reference(
                        input_text=question,
                        answer_text="",
                        question_type_eval={},
                        fact_eval={},
                        subject_rubric={},
                        session_dir=Path(tmp),
                    )

    def test_flags_off_preserve_existing_result_shape(self):
        result = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=False,
            assisted_enabled=False,
        )
        self.assertNotIn(
            "multi_topic_grading_context",
            result,
        )
        self.assertNotIn(
            "assisted_routing",
            result,
        )

    def test_multi_only_adds_parallel_context(self):
        off = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=False,
            assisted_enabled=False,
        )
        on = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=True,
            assisted_enabled=False,
        )

        context = on.get("multi_topic_grading_context")
        self.assertIsInstance(context, dict)
        self.assertTrue(context.get("applicable"))
        self.assertEqual(
            context.get("routing_mode"),
            "MULTI_TOPIC",
        )
        self.assertEqual(
            context.get("primary_topic_ids"),
            [RTD_TOPIC, TC_TOPIC],
        )
        self.assertEqual(
            [
                row.get("topic_id")
                for row in context.get("topic_evidence") or []
            ],
            [RTD_TOPIC, TC_TOPIC],
        )

        on_core = dict(on)
        on_core.pop("multi_topic_grading_context")
        self.assertEqual(on_core, off)

    def test_multi_and_assisted_preserve_context(self):
        off = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=False,
            assisted_enabled=False,
        )
        result = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=True,
            assisted_enabled=True,
        )

        context = result.get("multi_topic_grading_context")
        self.assertIsInstance(context, dict)
        self.assertTrue(context.get("applicable"))

        assisted = result.get("assisted_routing") or {}
        self.assertFalse(assisted.get("applied"))
        self.assertEqual(
            assisted.get("fallback_reason"),
            "multi_topic_deferred_stage_6",
        )

        self.assertEqual(
            result.get("matched"),
            off.get("matched"),
        )
        self.assertEqual(
            result.get("primary_reference"),
            off.get("primary_reference"),
        )

    def test_single_topic_multi_flag_adds_no_context(self):
        result = self._call(
            question=QUESTION_SINGLE,
            semantic=semantic_single(),
            multi_enabled=True,
            assisted_enabled=False,
        )
        self.assertNotIn(
            "multi_topic_grading_context",
            result,
        )

    def test_single_topic_assisted_behavior_is_preserved(self):
        result = self._call(
            question=QUESTION_SINGLE,
            semantic=semantic_single(),
            multi_enabled=True,
            assisted_enabled=True,
        )
        self.assertNotIn(
            "multi_topic_grading_context",
            result,
        )
        self.assertTrue(result.get("matched"))
        self.assertEqual(
            (result.get("primary_reference") or {}).get("topic_id"),
            CAVITATION_TOPIC,
        )
        self.assertTrue(
            (result.get("assisted_routing") or {}).get("applied")
        )

    def test_score_family_is_unchanged(self):
        off = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=False,
            assisted_enabled=False,
        )
        on = self._call(
            question=QUESTION_MULTI,
            semantic=semantic_multi(),
            multi_enabled=True,
            assisted_enabled=False,
        )

        for key in (
            "score",
            "top_score",
            "second_score",
            "score_margin",
            "question_score",
            "fact_score",
            "answer_score",
            "score_breakdown",
        ):
            with self.subTest(key=key):
                self.assertEqual(
                    on.get(key),
                    off.get(key),
                )


if __name__ == "__main__":
    unittest.main()
