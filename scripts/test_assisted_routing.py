from __future__ import annotations

import copy
import os
import unittest
from unittest.mock import patch

from assisted_routing import (
    ASSISTED_ROUTING_ENV,
    ASSISTED_ROUTING_VERSION,
    assisted_routing_enabled,
    build_assisted_model_answer_reference,
)


def legacy_result() -> dict:
    return {
        "version": "model_answer_reference_v1",
        "matched": False,
        "ambiguous": False,
        "routing_status": "unmatched",
        "confidence": "low",
        "primary_reference": None,
        "match_reasons": [],
        "score": 0,
        "top_score": 0,
        "second_score": 0,
        "score_margin": 0,
        "question_score": 0,
        "fact_score": 0,
        "answer_score": 0,
        "score_breakdown": {"question": 0},
        "candidates": [],
        "policy": {"threshold": 50},
        "usage": "legacy",
        "reason": "below threshold",
    }


def candidate_result() -> dict:
    return {
        "candidates": [
            {
                "answer": {
                    "topic_id": "topic_a",
                    "title": "Topic A",
                },
                "score": 18,
                "question_score": 18,
                "fact_score": 0,
                "answer_score": 0,
                "match_reasons": ["shadow recall"],
                "shadow_recall_adapter": True,
            },
            {
                "answer": {
                    "topic_id": "topic_b",
                    "title": "Topic B",
                },
                "score": 16,
                "question_score": 16,
                "fact_score": 0,
                "answer_score": 0,
                "match_reasons": ["shadow recall"],
                "shadow_recall_adapter": True,
            },
        ]
    }


def semantic(
    mode: str = "SINGLE_TOPIC",
    *,
    ok: bool = True,
    primary: list[str] | None = None,
) -> dict:
    return {
        "ok": ok,
        "routing_mode": mode,
        "primary_topic_ids": (
            ["topic_a"] if primary is None else primary
        ),
        "supporting_topic_ids": [],
        "student_answer_used": False,
        "routing_effect": "none",
        "score_effect": "none",
    }


class AssistedRoutingFlagTest(unittest.TestCase):
    def test_default_flag_is_off(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(assisted_routing_enabled())

    def test_truthy_flag_values(self):
        for value in ("1", "true", "TRUE", "yes", "on"):
            with self.subTest(value=value):
                with patch.dict(
                    os.environ,
                    {ASSISTED_ROUTING_ENV: value},
                    clear=True,
                ):
                    self.assertTrue(assisted_routing_enabled())


class AssistedRoutingBuilderTest(unittest.TestCase):
    def test_feature_off_returns_legacy_copy(self):
        legacy = legacy_result()
        semantic_result = semantic()
        candidates = candidate_result()

        before_legacy = copy.deepcopy(legacy)
        before_semantic = copy.deepcopy(semantic_result)
        before_candidates = copy.deepcopy(candidates)

        result = build_assisted_model_answer_reference(
            legacy_result=legacy,
            semantic_result=semantic_result,
            shadow_candidate_result=candidates,
            enabled=False,
        )

        for key, value in legacy.items():
            self.assertEqual(result[key], value)

        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "feature_flag_off",
        )
        self.assertFalse(
            result["assisted_routing"]["applied"]
        )
        self.assertEqual(legacy, before_legacy)
        self.assertEqual(semantic_result, before_semantic)
        self.assertEqual(candidates, before_candidates)

    def test_valid_single_topic_overlays_reference_and_matched_only(self):
        legacy = legacy_result()
        semantic_result = semantic()
        candidates = candidate_result()

        result = build_assisted_model_answer_reference(
            legacy_result=legacy,
            semantic_result=semantic_result,
            shadow_candidate_result=candidates,
            enabled=True,
        )

        self.assertTrue(result["matched"])
        self.assertEqual(
            result["primary_reference"],
            {
                "topic_id": "topic_a",
                "title": "Topic A",
            },
        )

        preserved = [
            "ambiguous",
            "routing_status",
            "confidence",
            "match_reasons",
            "score",
            "top_score",
            "second_score",
            "score_margin",
            "question_score",
            "fact_score",
            "answer_score",
            "score_breakdown",
            "candidates",
            "policy",
            "usage",
            "reason",
        ]
        for key in preserved:
            with self.subTest(key=key):
                self.assertEqual(result[key], legacy[key])

        meta = result["assisted_routing"]
        self.assertEqual(meta["version"], ASSISTED_ROUTING_VERSION)
        self.assertTrue(meta["applied"])
        self.assertEqual(
            meta["source"],
            "semantic_single_topic",
        )
        self.assertEqual(
            meta["semantic_selected_topic_id"],
            "topic_a",
        )
        self.assertEqual(
            meta["selected_topic_id"],
            "topic_a",
        )
        self.assertFalse(meta["student_answer_used"])
        self.assertFalse(meta["multi_topic_enabled"])
        self.assertFalse(meta["general_enabled"])
        self.assertFalse(meta["score_policy_changed"])
        self.assertFalse(meta["legacy_router_mutated"])

    def test_overlay_uses_candidate_answer_copy(self):
        candidates = candidate_result()

        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(),
            shadow_candidate_result=candidates,
            enabled=True,
        )

        result["primary_reference"]["title"] = "changed"

        self.assertEqual(
            candidates["candidates"][0]["answer"]["title"],
            "Topic A",
        )

    def test_multi_topic_falls_back_to_legacy(self):
        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(
                "MULTI_TOPIC",
                primary=["topic_a", "topic_b"],
            ),
            shadow_candidate_result=candidate_result(),
            enabled=True,
        )

        self.assertFalse(result["matched"])
        self.assertIsNone(result["primary_reference"])
        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "multi_topic_deferred_stage_6",
        )

    def test_general_falls_back_to_legacy(self):
        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(
                "GENERAL",
                primary=[],
            ),
            shadow_candidate_result=candidate_result(),
            enabled=True,
        )

        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "general_deferred_stage_7",
        )

    def test_ambiguous_falls_back_to_legacy(self):
        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(
                "AMBIGUOUS",
                primary=[],
            ),
            shadow_candidate_result=candidate_result(),
            enabled=True,
        )

        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "ambiguous_legacy_fallback",
        )

    def test_semantic_error_falls_back_to_legacy(self):
        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(ok=False),
            shadow_candidate_result=candidate_result(),
            enabled=True,
        )

        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "semantic_not_ok",
        )

    def test_multiple_primary_topics_are_rejected_for_single_mode(self):
        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(
                primary=["topic_a", "topic_b"],
            ),
            shadow_candidate_result=candidate_result(),
            enabled=True,
        )

        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "invalid_primary_topic_count",
        )

    def test_primary_topic_must_exist_in_supplied_candidates(self):
        result = build_assisted_model_answer_reference(
            legacy_result=legacy_result(),
            semantic_result=semantic(
                primary=["missing_topic"],
            ),
            shadow_candidate_result=candidate_result(),
            enabled=True,
        )

        self.assertEqual(
            result["assisted_routing"]["semantic_selected_topic_id"],
            "missing_topic",
        )
        self.assertEqual(
            result["assisted_routing"]["fallback_reason"],
            "primary_topic_missing_from_candidates",
        )

    def test_raw_inputs_are_never_mutated(self):
        legacy = legacy_result()
        semantic_result = semantic()
        candidates = candidate_result()

        expected = (
            copy.deepcopy(legacy),
            copy.deepcopy(semantic_result),
            copy.deepcopy(candidates),
        )

        build_assisted_model_answer_reference(
            legacy_result=legacy,
            semantic_result=semantic_result,
            shadow_candidate_result=candidates,
            enabled=True,
        )

        self.assertEqual(legacy, expected[0])
        self.assertEqual(semantic_result, expected[1])
        self.assertEqual(candidates, expected[2])

    def test_non_dict_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            build_assisted_model_answer_reference(
                legacy_result=None,  # type: ignore[arg-type]
                semantic_result={},
                shadow_candidate_result={},
                enabled=True,
            )


if __name__ == "__main__":
    unittest.main()
