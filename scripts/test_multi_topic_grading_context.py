from __future__ import annotations

import copy
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from model_answer_router import find_model_answer_reference
from rubric_registry import load_model_answer_bank
from semantic_router_shadow import (
    augment_rule_candidates_for_shadow,
)

from multi_topic_grading_context import (
    MULTI_TOPIC_GRADING_CONTEXT_VERSION,
    MULTI_TOPIC_GRADING_ENV,
    build_multi_topic_grading_context,
    load_generated_multi_topic_sources,
    multi_topic_grading_enabled,
)


RTD_TOPIC = (
    "rtd_temperature_sensor_principle_pt100_wiring_compensation"
)
TC_TOPIC = (
    "thermocouple_temperature_sensor_seebeck_"
    "reference_junction_compensation"
)


def semantic_multi() -> dict:
    return {
        "version": "semantic_router_shadow_v1",
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
    }


def candidate_fixture() -> dict:
    return {
        "candidates": [
            {
                "answer": {
                    "topic_id": RTD_TOPIC,
                    "title": "RTD",
                }
            },
            {
                "answer": {
                    "topic_id": TC_TOPIC,
                    "title": "Thermocouple",
                }
            },
        ]
    }


def source_fixture() -> dict:
    return {
        "model_answer": {
            "items": [
                {
                    "topic_id": RTD_TOPIC,
                    "title": "RTD",
                    "high_score": ["rtd"],
                },
                {
                    "topic_id": TC_TOPIC,
                    "title": "Thermocouple",
                    "high_score": ["tc"],
                },
            ]
        },
        "fact_anchor": {
            "items": [
                {
                    "topic_id": RTD_TOPIC,
                    "core_terms": ["Pt100"],
                },
                {
                    "topic_id": TC_TOPIC,
                    "core_terms": ["Seebeck"],
                },
            ]
        },
        "logic_check": {
            "items": [
                {
                    "topic_id": RTD_TOPIC,
                    "checks": ["RTD logic"],
                },
                {
                    "topic_id": TC_TOPIC,
                    "checks": ["TC logic"],
                },
            ]
        },
        "topic_importance": {
            "items": [
                {
                    "topic_id": RTD_TOPIC,
                    "importance": "high",
                },
                {
                    "topic_id": TC_TOPIC,
                    "importance": "high",
                },
            ]
        },
    }


class MultiTopicFlagTest(unittest.TestCase):
    def test_default_flag_is_off(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(
                multi_topic_grading_enabled()
            )

    def test_truthy_values(self):
        for value in ("1", "true", "TRUE", "yes", "on"):
            with self.subTest(value=value):
                with patch.dict(
                    os.environ,
                    {MULTI_TOPIC_GRADING_ENV: value},
                    clear=True,
                ):
                    self.assertTrue(
                        multi_topic_grading_enabled()
                    )


class MultiTopicContextBuilderTest(unittest.TestCase):
    def test_valid_multi_topic_context_preserves_order_and_evidence(self):
        semantic = semantic_multi()
        candidates = candidate_fixture()
        sources = source_fixture()

        before = (
            copy.deepcopy(semantic),
            copy.deepcopy(candidates),
            copy.deepcopy(sources),
        )

        result = build_multi_topic_grading_context(
            semantic_result=semantic,
            shadow_candidate_result=candidates,
            generated_sources=sources,
            enabled=True,
        )

        self.assertEqual(
            result["version"],
            MULTI_TOPIC_GRADING_CONTEXT_VERSION,
        )
        self.assertTrue(result["applicable"])
        self.assertEqual(
            result["primary_topic_ids"],
            [RTD_TOPIC, TC_TOPIC],
        )
        self.assertEqual(
            [
                row["topic_id"]
                for row in result["topic_evidence"]
            ],
            [RTD_TOPIC, TC_TOPIC],
        )

        for row in result["topic_evidence"]:
            topic_id = row["topic_id"]
            self.assertEqual(
                row["candidate_reference"]["topic_id"],
                topic_id,
            )
            self.assertEqual(
                row["model_answer"]["topic_id"],
                topic_id,
            )
            self.assertEqual(
                row["fact_anchor"]["topic_id"],
                topic_id,
            )
            self.assertEqual(
                row["logic_check"]["topic_id"],
                topic_id,
            )
            self.assertEqual(
                row["topic_importance"]["topic_id"],
                topic_id,
            )

        policy = result["policy"]
        self.assertTrue(
            policy["one_question_one_score"]
        )
        self.assertFalse(
            policy["topic_score_summing"]
        )
        self.assertFalse(
            policy["topic_score_averaging"]
        )
        self.assertFalse(
            policy["duplicate_score_layers"]
        )
        self.assertFalse(
            policy["primary_reference_overloaded"]
        )
        self.assertFalse(
            policy["student_answer_used_for_routing"]
        )

        self.assertEqual(semantic, before[0])
        self.assertEqual(candidates, before[1])
        self.assertEqual(sources, before[2])

    def test_feature_off_is_not_applicable(self):
        result = build_multi_topic_grading_context(
            semantic_result=semantic_multi(),
            shadow_candidate_result=candidate_fixture(),
            generated_sources=source_fixture(),
            enabled=False,
        )

        self.assertFalse(result["applicable"])
        self.assertEqual(
            result["fallback_reason"],
            "feature_flag_off",
        )

    def test_single_topic_is_not_applicable(self):
        semantic = semantic_multi()
        semantic["routing_mode"] = "SINGLE_TOPIC"
        semantic["primary_topic_ids"] = [RTD_TOPIC]

        result = build_multi_topic_grading_context(
            semantic_result=semantic,
            shadow_candidate_result=candidate_fixture(),
            generated_sources=source_fixture(),
            enabled=True,
        )

        self.assertFalse(result["applicable"])
        self.assertEqual(
            result["fallback_reason"],
            "single_topic_not_applicable",
        )

    def test_general_is_deferred_stage_7(self):
        semantic = semantic_multi()
        semantic["routing_mode"] = "GENERAL"
        semantic["primary_topic_ids"] = []

        result = build_multi_topic_grading_context(
            semantic_result=semantic,
            shadow_candidate_result=candidate_fixture(),
            generated_sources=source_fixture(),
            enabled=True,
        )

        self.assertEqual(
            result["fallback_reason"],
            "general_deferred_stage_7",
        )

    def test_multi_topic_requires_two_primary_topics(self):
        semantic = semantic_multi()
        semantic["primary_topic_ids"] = [RTD_TOPIC]

        result = build_multi_topic_grading_context(
            semantic_result=semantic,
            shadow_candidate_result=candidate_fixture(),
            generated_sources=source_fixture(),
            enabled=True,
        )

        self.assertEqual(
            result["fallback_reason"],
            "insufficient_primary_topic_count",
        )

    def test_primary_topic_must_exist_in_candidates(self):
        candidates = candidate_fixture()
        candidates["candidates"] = candidates["candidates"][:1]

        result = build_multi_topic_grading_context(
            semantic_result=semantic_multi(),
            shadow_candidate_result=candidates,
            generated_sources=source_fixture(),
            enabled=True,
        )

        self.assertTrue(
            result["fallback_reason"].startswith(
                "primary_topic_missing_from_candidates:"
            )
        )

    def test_model_answer_is_mandatory(self):
        sources = source_fixture()
        sources["model_answer"]["items"] = [
            sources["model_answer"]["items"][0]
        ]

        result = build_multi_topic_grading_context(
            semantic_result=semantic_multi(),
            shadow_candidate_result=candidate_fixture(),
            generated_sources=sources,
            enabled=True,
        )

        self.assertTrue(
            result["fallback_reason"].startswith(
                "primary_topic_missing_model_answer:"
            )
        )

    def test_optional_sources_may_be_missing_but_provenance_is_retained(self):
        sources = source_fixture()
        sources["fact_anchor"]["items"] = []
        sources["logic_check"]["items"] = []
        sources["topic_importance"]["items"] = []

        result = build_multi_topic_grading_context(
            semantic_result=semantic_multi(),
            shadow_candidate_result=candidate_fixture(),
            generated_sources=sources,
            enabled=True,
        )

        self.assertTrue(result["applicable"])
        for row in result["topic_evidence"]:
            self.assertIsNone(row["fact_anchor"])
            self.assertIsNone(row["logic_check"])
            self.assertIsNone(row["topic_importance"])

    def test_duplicate_primary_topic_ids_are_collapsed(self):
        semantic = semantic_multi()
        semantic["primary_topic_ids"] = [
            RTD_TOPIC,
            RTD_TOPIC,
            TC_TOPIC,
        ]

        result = build_multi_topic_grading_context(
            semantic_result=semantic,
            shadow_candidate_result=candidate_fixture(),
            generated_sources=source_fixture(),
            enabled=True,
        )

        self.assertEqual(
            result["primary_topic_ids"],
            [RTD_TOPIC, TC_TOPIC],
        )

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            build_multi_topic_grading_context(
                semantic_result=None,  # type: ignore[arg-type]
                shadow_candidate_result={},
                generated_sources={},
                enabled=True,
            )


class MultiTopicRealGeneratedEvidenceTest(unittest.TestCase):
    def test_rtd_thermocouple_real_generated_sources(self):
        question = (
            "RTD와 열전대의 측정 원리, 오차 특성 및 "
            "적용성을 비교하시오."
        )

        bank = load_model_answer_bank()

        legacy = find_model_answer_reference(
            question_text=question,
            answer_text="",
            question_type_eval={},
            fact_eval={},
            bank=bank,
        )

        shadow = augment_rule_candidates_for_shadow(
            question_text=question,
            rule_result=legacy,
            bank=bank,
        )

        sources = load_generated_multi_topic_sources(
            repo_root=Path(".")
        )

        result = build_multi_topic_grading_context(
            semantic_result=semantic_multi(),
            shadow_candidate_result=shadow,
            generated_sources=sources,
            enabled=True,
        )

        self.assertTrue(result["applicable"])
        self.assertEqual(
            result["primary_topic_ids"],
            [RTD_TOPIC, TC_TOPIC],
        )

        self.assertEqual(
            len(result["topic_evidence"]),
            2,
        )

        for row in result["topic_evidence"]:
            self.assertIsNotNone(row["model_answer"])
            self.assertIsNotNone(row["fact_anchor"])
            self.assertIsNotNone(row["logic_check"])
            self.assertIsNotNone(row["topic_importance"])


if __name__ == "__main__":
    unittest.main()
