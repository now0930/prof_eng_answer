from __future__ import annotations

import copy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import grading_agents as ga
import hybrid_general_grading_context as hg
import semantic_router_shadow as srs
from hybrid_general_grading_context import (
    HYBRID_GENERAL_GRADING_ENV,
    build_hybrid_general_grading_context,
    hybrid_general_grading_enabled,
)


TOPIC = (
    "control_valve_cavitation_flashing_choked_flow_"
    "damage_prevention"
)


def demands() -> dict:
    return {
        "ok": True,
        "demands": [
            {"id": "D1", "text": "발생 원리를 설명하시오."},
            {"id": "D2", "text": "현장 적용 대책을 설명하시오."},
        ],
    }


def candidates() -> dict:
    return {
        "candidates": [
            {"answer": {"topic_id": TOPIC, "title": "Cavitation"}}
        ]
    }


def sources() -> dict:
    return {
        "model_answer": {
            "topics": [{"topic_id": TOPIC, "title": "Cavitation"}]
        },
        "fact_anchor": {
            "topics": [{"topic_id": TOPIC, "anchors": []}]
        },
    }


def semantic_general() -> dict:
    return {
        "ok": True,
        "routing_mode": "GENERAL",
        "primary_topic_ids": [],
        "demand_mappings": [],
        "uncovered_demand_ids": ["D1", "D2"],
    }


def semantic_hybrid() -> dict:
    return {
        "ok": True,
        "routing_mode": "SINGLE_TOPIC",
        "primary_topic_ids": [TOPIC],
        "demand_mappings": [
            {"demand_id": "D1", "topic_id": TOPIC, "role": "PRIMARY"}
        ],
        "uncovered_demand_ids": ["D2"],
    }


class HybridGeneralContextUnitTest(unittest.TestCase):
    def test_default_flag_is_off(self):
        with patch.dict(
            os.environ,
            {HYBRID_GENERAL_GRADING_ENV: ""},
            clear=False,
        ):
            self.assertFalse(hybrid_general_grading_enabled())

    def test_pure_general(self):
        result = build_hybrid_general_grading_context(
            semantic_result=semantic_general(),
            question_demand_result=demands(),
            shadow_candidate_result={},
            generated_sources={},
            enabled=True,
        )
        self.assertTrue(result["applicable"])
        self.assertEqual(result["coverage_kind"], "PURE_GENERAL")
        self.assertEqual(result["primary_topic_ids"], [])
        self.assertFalse(
            result["general_engineering_evidence"]["score_component"]
        )

    def test_single_topic_plus_general(self):
        result = build_hybrid_general_grading_context(
            semantic_result=semantic_hybrid(),
            question_demand_result=demands(),
            shadow_candidate_result=candidates(),
            generated_sources=sources(),
            enabled=True,
        )
        self.assertTrue(result["applicable"])
        self.assertEqual(
            result["coverage_kind"],
            "HYBRID_TOPIC_GENERAL",
        )
        row = result["topic_evidence"][0]
        self.assertIn("model_answer", row)
        self.assertIn("fact_anchor", row)
        self.assertNotIn("logic_check", row)
        self.assertNotIn("topic_importance", row)

    def test_no_uncovered_is_not_hybrid(self):
        semantic = semantic_hybrid()
        semantic["uncovered_demand_ids"] = []
        result = build_hybrid_general_grading_context(
            semantic_result=semantic,
            question_demand_result=demands(),
            shadow_candidate_result=candidates(),
            generated_sources=sources(),
            enabled=True,
        )
        self.assertFalse(result["applicable"])

    def test_ambiguous_is_not_general(self):
        semantic = semantic_general()
        semantic["routing_mode"] = "AMBIGUOUS"
        result = build_hybrid_general_grading_context(
            semantic_result=semantic,
            question_demand_result=demands(),
            shadow_candidate_result={},
            generated_sources={},
            enabled=True,
        )
        self.assertFalse(result["applicable"])


class HybridGeneralPhase10IntegrationTest(unittest.TestCase):
    def _call(
        self,
        *,
        question: str,
        semantic: dict,
        demand_result: dict,
        enabled: bool,
    ) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(
                os.environ,
                {
                    HYBRID_GENERAL_GRADING_ENV: (
                        "1" if enabled else "0"
                    ),
                    "MULTI_TOPIC_GRADING_ENABLED": "0",
                    "ASSISTED_ROUTING_ENABLED": "0",
                    "QUESTION_DEMAND_SHADOW_ENABLED": "0",
                    "SEMANTIC_ROUTER_SHADOW_ENABLED": "0",
                },
                clear=False,
            ):
                with patch.object(
                    ga,
                    "_phase10_run_question_demand_shadow",
                    return_value=copy.deepcopy(demand_result),
                ), patch.object(
                    ga,
                    "_phase10_run_semantic_router_shadow",
                    return_value=copy.deepcopy(semantic),
                ), patch.object(
                    srs,
                    "augment_rule_candidates_for_shadow",
                    return_value=copy.deepcopy(candidates()),
                ), patch.object(
                    hg,
                    "load_generated_hybrid_general_sources",
                    return_value=copy.deepcopy(sources()),
                ):
                    return ga._phase10_run_model_answer_reference(
                        input_text=question,
                        answer_text="",
                        question_type_eval={},
                        fact_eval={},
                        subject_rubric={},
                        session_dir=Path(tmp),
                    )

    def test_pure_general_parallel_only(self):
        question = "일반 계측시스템의 신뢰성 확보 방안을 설명하시오."
        off = self._call(
            question=question,
            semantic=semantic_general(),
            demand_result=demands(),
            enabled=False,
        )
        on = self._call(
            question=question,
            semantic=semantic_general(),
            demand_result=demands(),
            enabled=True,
        )
        context = on.get("hybrid_general_grading_context")
        self.assertIsInstance(context, dict)
        self.assertEqual(context.get("coverage_kind"), "PURE_GENERAL")
        on_core = dict(on)
        on_core.pop("hybrid_general_grading_context")
        self.assertEqual(on_core, off)

    def test_hybrid_preserves_primary_reference_and_scores(self):
        question = (
            "제어밸브 캐비테이션의 발생 원리와 "
            "현장 적용 대책을 설명하시오."
        )
        off = self._call(
            question=question,
            semantic=semantic_hybrid(),
            demand_result=demands(),
            enabled=False,
        )
        on = self._call(
            question=question,
            semantic=semantic_hybrid(),
            demand_result=demands(),
            enabled=True,
        )

        context = on.get("hybrid_general_grading_context")
        self.assertIsInstance(context, dict)
        self.assertEqual(
            context.get("coverage_kind"),
            "HYBRID_TOPIC_GENERAL",
        )
        self.assertEqual(
            on.get("primary_reference"),
            off.get("primary_reference"),
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
            self.assertEqual(on.get(key), off.get(key))


if __name__ == "__main__":
    unittest.main()
