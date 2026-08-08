from __future__ import annotations

import ast
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import grading_agents as ga


QUESTION = (
    "제어밸브의 캐비테이션과 플래싱의 발생 원리, "
    "차이점 및 방지대책을 설명하시오."
)

EXPECTED_TOPIC = (
    "control_valve_cavitation_flashing_choked_flow_"
    "damage_prevention"
)


def semantic_single_topic() -> dict:
    return {
        "version": "semantic_router_shadow_v1",
        "shadow": True,
        "enabled": True,
        "status": "ok",
        "ok": True,
        "routing_mode": "SINGLE_TOPIC",
        "primary_topic_ids": [EXPECTED_TOPIC],
        "supporting_topic_ids": [],
        "uncovered_demand_ids": [],
        "student_answer_used": False,
        "routing_effect": "none",
        "score_effect": "none",
        "legacy_router_authoritative": True,
        "llm_called": False,
    }


def semantic_multi_topic() -> dict:
    return {
        **semantic_single_topic(),
        "routing_mode": "MULTI_TOPIC",
        "primary_topic_ids": [
            EXPECTED_TOPIC,
            "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim",
        ],
    }


class AssistedRoutingPhase10StaticContractTest(unittest.TestCase):
    def test_single_integration_point(self):
        grading = Path("grading_agents.py").read_text(
            encoding="utf-8"
        )
        legacy = Path("model_answer_router.py").read_text(
            encoding="utf-8"
        )

        self.assertEqual(
            grading.count(
                "semantic_router_shadow_result = "
                "_phase10_run_semantic_router_shadow("
            ),
            1,
        )
        self.assertEqual(
            grading.count(
                "build_assisted_model_answer_reference("
            ),
            1,
        )
        self.assertEqual(
            grading.count("if assisted_routing_enabled():"),
            1,
        )
        self.assertNotIn(
            "build_assisted_model_answer_reference",
            legacy,
        )


class AssistedRoutingPhase10RuntimeTest(unittest.TestCase):
    def _call(self) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            return ga._phase10_run_model_answer_reference(
                input_text=QUESTION,
                answer_text="",
                question_type_eval={},
                fact_eval={},
                subject_rubric={},
                session_dir=Path(tmp),
            )

    def test_flag_off_preserves_raw_legacy_return(self):
        with patch.dict(
            os.environ,
            {"ASSISTED_ROUTING_ENABLED": "0"},
            clear=False,
        ):
            with patch.object(
                ga,
                "_phase10_run_semantic_router_shadow",
                return_value=semantic_single_topic(),
            ):
                result = self._call()

        self.assertNotIn("assisted_routing", result)
        self.assertFalse(bool(result.get("matched")))
        self.assertIsNone(result.get("primary_reference"))

    def test_flag_on_single_topic_applies_overlay(self):
        with patch.dict(
            os.environ,
            {"ASSISTED_ROUTING_ENABLED": "1"},
            clear=False,
        ):
            with patch.object(
                ga,
                "_phase10_run_semantic_router_shadow",
                return_value=semantic_single_topic(),
            ):
                result = self._call()

        self.assertTrue(result.get("matched"))
        self.assertEqual(
            (result.get("primary_reference") or {}).get("topic_id"),
            EXPECTED_TOPIC,
        )

        meta = result.get("assisted_routing") or {}
        self.assertTrue(meta.get("applied"))
        self.assertEqual(
            meta.get("source"),
            "semantic_single_topic",
        )
        self.assertEqual(
            meta.get("selected_topic_id"),
            EXPECTED_TOPIC,
        )
        self.assertFalse(meta.get("student_answer_used"))
        self.assertFalse(meta.get("score_policy_changed"))
        self.assertFalse(meta.get("legacy_router_mutated"))

    def test_flag_on_multi_topic_stays_legacy(self):
        with patch.dict(
            os.environ,
            {"ASSISTED_ROUTING_ENABLED": "1"},
            clear=False,
        ):
            with patch.object(
                ga,
                "_phase10_run_semantic_router_shadow",
                return_value=semantic_multi_topic(),
            ):
                result = self._call()

        self.assertFalse(bool(result.get("matched")))
        self.assertIsNone(result.get("primary_reference"))

        meta = result.get("assisted_routing") or {}
        self.assertFalse(meta.get("applied"))
        self.assertEqual(
            meta.get("fallback_reason"),
            "multi_topic_deferred_stage_6",
        )


if __name__ == "__main__":
    unittest.main()
