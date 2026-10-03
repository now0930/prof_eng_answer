from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


MULTI_TOPIC_GRADING_CONTEXT_VERSION = (
    "multi_topic_grading_context_v1"
)
MULTI_TOPIC_GRADING_ENV = "MULTI_TOPIC_GRADING_ENABLED"

DEFAULT_GENERATED_SOURCES = {
    "model_answer": Path(
        "rubrics/generated/model_answers.generated.json"
    ),
    "fact_anchor": Path(
        "rubrics/generated/fact_anchors.generated.json"
    ),
    "logic_check": Path(
        "rubrics/generated/logic_checks.generated.json"
    ),
    "topic_importance": Path(
        "rubrics/generated/topic_importance.generated.json"
    ),
}


def _env_flag_enabled(value: Optional[str]) -> bool:
    return str(value or "").strip().casefold() in {
        "1",
        "true",
        "yes",
        "on",
    }


def multi_topic_grading_enabled() -> bool:
    """Return the Stage 6 multi-topic feature flag.

    The default remains OFF until integration and activation validation
    complete.
    """

    return _env_flag_enabled(
        os.getenv(MULTI_TOPIC_GRADING_ENV)
    )


def _distinct_topic_ids(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []

    out: list[str] = []
    seen: set[str] = set()

    for value in values:
        topic_id = str(value or "").strip()
        if not topic_id or topic_id in seen:
            continue
        seen.add(topic_id)
        out.append(topic_id)

    return out


def _candidate_reference_by_topic_id(
    shadow_candidate_result: Dict[str, Any],
    topic_id: str,
) -> Optional[Dict[str, Any]]:
    candidates = shadow_candidate_result.get("candidates") or []
    if not isinstance(candidates, list):
        return None

    for row in candidates:
        if not isinstance(row, dict):
            continue

        answer = row.get("answer")
        if not isinstance(answer, dict):
            continue

        answer_topic_id = str(
            answer.get("topic_id") or ""
        ).strip()

        if answer_topic_id == topic_id:
            return copy.deepcopy(answer)

    return None


def _find_topic_objects(
    value: Any,
    topic_id: str,
) -> list[Dict[str, Any]]:
    found: list[Dict[str, Any]] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            if str(node.get("topic_id") or "").strip() == topic_id:
                found.append(node)

            for child in node.values():
                visit(child)

        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return found


def _first_topic_object(
    value: Any,
    topic_id: str,
) -> Optional[Dict[str, Any]]:
    matches = _find_topic_objects(value, topic_id)
    if not matches:
        return None
    return copy.deepcopy(matches[0])


def load_generated_multi_topic_sources(
    *,
    repo_root: Path | str = ".",
) -> Dict[str, Any]:
    root = Path(repo_root)
    out: Dict[str, Any] = {}

    for label, rel_path in DEFAULT_GENERATED_SOURCES.items():
        path = root / rel_path
        out[label] = json.loads(
            path.read_text(encoding="utf-8")
        )

    return out


def _fallback_context(
    *,
    enabled: bool,
    reason: str,
    semantic_result: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "version": MULTI_TOPIC_GRADING_CONTEXT_VERSION,
        "enabled": enabled,
        "applicable": False,
        "routing_mode": str(
            semantic_result.get("routing_mode") or ""
        ).strip()
        or None,
        "primary_topic_ids": [],
        "topic_evidence": [],
        "demand_mappings": copy.deepcopy(
            semantic_result.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            semantic_result.get("uncovered_demand_ids") or []
        ),
        "fallback_reason": reason,
        "policy": {
            "one_question_one_score": True,
            "topic_score_summing": False,
            "topic_score_averaging": False,
            "duplicate_score_layers": False,
            "primary_reference_overloaded": False,
            "single_topic_behavior_changed": False,
            "general_behavior_changed": False,
            "student_answer_used_for_routing": False,
        },
        "provenance": {
            "semantic_primary_topics_preserved": True,
            "raw_semantic_preserved": True,
            "shadow_candidates_preserved": True,
            "generated_sources_preserved": True,
        },
    }


def build_multi_topic_grading_context(
    *,
    semantic_result: Dict[str, Any],
    shadow_candidate_result: Dict[str, Any],
    generated_sources: Dict[str, Any],
    enabled: Optional[bool] = None,
) -> Dict[str, Any]:
    """Build a MULTI_TOPIC evidence context without scoring.

    This function never sums, averages, or otherwise combines Topic-level
    scores. It prepares provenance-preserving evidence for one later grading
    pass over one student answer.
    """

    if not isinstance(semantic_result, dict):
        raise TypeError("semantic_result must be a dict")
    if not isinstance(shadow_candidate_result, dict):
        raise TypeError(
            "shadow_candidate_result must be a dict"
        )
    if not isinstance(generated_sources, dict):
        raise TypeError("generated_sources must be a dict")

    flag_enabled = (
        multi_topic_grading_enabled()
        if enabled is None
        else bool(enabled)
    )

    if not flag_enabled:
        return _fallback_context(
            enabled=False,
            reason="feature_flag_off",
            semantic_result=semantic_result,
        )

    if semantic_result.get("ok") is not True:
        return _fallback_context(
            enabled=True,
            reason="semantic_not_ok",
            semantic_result=semantic_result,
        )

    mode = str(
        semantic_result.get("routing_mode") or ""
    ).strip()

    if mode != "MULTI_TOPIC":
        reason = {
            "SINGLE_TOPIC": "single_topic_not_applicable",
            "GENERAL": "general_deferred_stage_7",
            "AMBIGUOUS": "ambiguous_not_applicable",
        }.get(mode, "unsupported_semantic_mode")

        return _fallback_context(
            enabled=True,
            reason=reason,
            semantic_result=semantic_result,
        )

    primary_topic_ids = _distinct_topic_ids(
        semantic_result.get("primary_topic_ids")
    )

    if len(primary_topic_ids) < 2:
        return _fallback_context(
            enabled=True,
            reason="insufficient_primary_topic_count",
            semantic_result=semantic_result,
        )

    model_answers = generated_sources.get("model_answer")
    if model_answers is None:
        return _fallback_context(
            enabled=True,
            reason="model_answer_source_missing",
            semantic_result=semantic_result,
        )

    topic_evidence: list[Dict[str, Any]] = []

    for topic_id in primary_topic_ids:
        candidate_reference = _candidate_reference_by_topic_id(
            shadow_candidate_result,
            topic_id,
        )

        if candidate_reference is None:
            return _fallback_context(
                enabled=True,
                reason=(
                    "primary_topic_missing_from_candidates:"
                    + topic_id
                ),
                semantic_result=semantic_result,
            )

        model_answer = _first_topic_object(
            model_answers,
            topic_id,
        )

        if model_answer is None:
            return _fallback_context(
                enabled=True,
                reason=(
                    "primary_topic_missing_model_answer:"
                    + topic_id
                ),
                semantic_result=semantic_result,
            )

        fact_anchor = _first_topic_object(
            generated_sources.get("fact_anchor"),
            topic_id,
        )
        logic_check = _first_topic_object(
            generated_sources.get("logic_check"),
            topic_id,
        )
        topic_importance = _first_topic_object(
            generated_sources.get("topic_importance"),
            topic_id,
        )

        title = str(
            model_answer.get("title")
            or candidate_reference.get("title")
            or ""
        ).strip()

        topic_evidence.append(
            {
                "topic_id": topic_id,
                "title": title,
                "candidate_reference": candidate_reference,
                "model_answer": model_answer,
                "fact_anchor": fact_anchor,
                "logic_check": logic_check,
                "topic_importance": topic_importance,
            }
        )

    return {
        "version": MULTI_TOPIC_GRADING_CONTEXT_VERSION,
        "enabled": True,
        "applicable": True,
        "routing_mode": "MULTI_TOPIC",
        "primary_topic_ids": primary_topic_ids,
        "topic_evidence": topic_evidence,
        "demand_mappings": copy.deepcopy(
            semantic_result.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            semantic_result.get("uncovered_demand_ids") or []
        ),
        "fallback_reason": "",
        "policy": {
            "one_question_one_score": True,
            "topic_score_summing": False,
            "topic_score_averaging": False,
            "duplicate_score_layers": False,
            "primary_reference_overloaded": False,
            "single_topic_behavior_changed": False,
            "general_behavior_changed": False,
            "student_answer_used_for_routing": False,
        },
        "provenance": {
            "semantic_primary_topics_preserved": True,
            "raw_semantic_preserved": True,
            "shadow_candidates_preserved": True,
            "generated_sources_preserved": True,
        },
    }
