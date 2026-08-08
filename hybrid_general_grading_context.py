from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


HYBRID_GENERAL_GRADING_CONTEXT_VERSION = (
    "hybrid_general_grading_context_v1"
)
HYBRID_GENERAL_GRADING_ENV = "HYBRID_GENERAL_GRADING_ENABLED"

DEFAULT_GENERATED_SOURCES = {
    "model_answer": Path("rubrics/generated/model_answers.generated.json"),
    "fact_anchor": Path("rubrics/generated/fact_anchors.generated.json"),
}


def _env_flag_enabled(value: Optional[str]) -> bool:
    return str(value or "").strip().casefold() in {"1", "true", "yes", "on"}


def hybrid_general_grading_enabled() -> bool:
    return _env_flag_enabled(os.getenv(HYBRID_GENERAL_GRADING_ENV))


def load_generated_hybrid_general_sources(
    *,
    repo_root: Path | str = ".",
) -> Dict[str, Any]:
    root = Path(repo_root)
    out: Dict[str, Any] = {}
    for label, rel_path in DEFAULT_GENERATED_SOURCES.items():
        out[label] = json.loads(
            (root / rel_path).read_text(encoding="utf-8")
        )
    return out


def _distinct(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        token = str(value or "").strip()
        if token and token not in seen:
            seen.add(token)
            out.append(token)
    return out


def _primary_topic_ids(semantic_result: Dict[str, Any]) -> list[str]:
    direct = _distinct(semantic_result.get("primary_topic_ids"))
    if direct:
        return direct

    values = []
    rows = semantic_result.get("demand_mappings") or []
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            if str(row.get("role") or "").strip() == "PRIMARY":
                values.append(row.get("topic_id"))
    return _distinct(values)


def _candidate_topic_ids(
    shadow_candidate_result: Dict[str, Any],
) -> set[str]:
    out: set[str] = set()
    rows = shadow_candidate_result.get("candidates") or []
    if not isinstance(rows, list):
        return out
    for row in rows:
        if not isinstance(row, dict):
            continue
        answer = row.get("answer")
        if not isinstance(answer, dict):
            continue
        topic_id = str(answer.get("topic_id") or "").strip()
        if topic_id:
            out.add(topic_id)
    return out


def _find_topic_object(
    value: Any,
    topic_id: str,
) -> Optional[Dict[str, Any]]:
    found: Optional[Dict[str, Any]] = None

    def visit(node: Any) -> None:
        nonlocal found
        if found is not None:
            return
        if isinstance(node, dict):
            if str(node.get("topic_id") or "").strip() == topic_id:
                found = copy.deepcopy(node)
                return
            for child in node.values():
                visit(child)
                if found is not None:
                    return
        elif isinstance(node, list):
            for child in node:
                visit(child)
                if found is not None:
                    return

    visit(value)
    return found


def _demand_map(
    question_demand_result: Dict[str, Any],
) -> Dict[str, str]:
    rows = question_demand_result.get("demands") or []
    out: Dict[str, str] = {}
    if not isinstance(rows, list):
        return out

    for row in rows:
        if not isinstance(row, dict):
            continue
        demand_id = str(
            row.get("id") or row.get("demand_id") or ""
        ).strip()
        demand_text = str(
            row.get("text") or row.get("demand") or ""
        ).strip()
        if demand_id and demand_text and demand_id not in out:
            out[demand_id] = demand_text
    return out


def _fallback_context(
    *,
    enabled: bool,
    reason: str,
    semantic_result: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "version": HYBRID_GENERAL_GRADING_CONTEXT_VERSION,
        "enabled": enabled,
        "applicable": False,
        "routing_mode": str(
            semantic_result.get("routing_mode") or ""
        ).strip()
        or None,
        "coverage_kind": None,
        "primary_topic_ids": [],
        "topic_evidence": [],
        "demand_mappings": copy.deepcopy(
            semantic_result.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            semantic_result.get("uncovered_demand_ids") or []
        ),
        "general_engineering_evidence": None,
        "fallback_reason": reason,
        "policy": {
            "one_question_one_score": True,
            "topic_general_score_summing": False,
            "topic_general_score_averaging": False,
            "partial_scores_created": False,
            "primary_reference_overloaded": False,
            "new_runtime_mode_added": False,
            "student_answer_used_for_context": False,
            "logic_check_general_aggregation": False,
            "topic_importance_general_aggregation": False,
        },
    }


def build_hybrid_general_grading_context(
    *,
    semantic_result: Dict[str, Any],
    question_demand_result: Dict[str, Any],
    shadow_candidate_result: Dict[str, Any],
    generated_sources: Dict[str, Any],
    enabled: Optional[bool] = None,
) -> Dict[str, Any]:
    for label, value in (
        ("semantic_result", semantic_result),
        ("question_demand_result", question_demand_result),
        ("shadow_candidate_result", shadow_candidate_result),
        ("generated_sources", generated_sources),
    ):
        if not isinstance(value, dict):
            raise TypeError(f"{label} must be a dict")

    flag_enabled = (
        hybrid_general_grading_enabled()
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
    if question_demand_result.get("ok") is not True:
        return _fallback_context(
            enabled=True,
            reason="question_demand_not_ok",
            semantic_result=semantic_result,
        )

    mode = str(semantic_result.get("routing_mode") or "").strip()
    if mode == "AMBIGUOUS":
        return _fallback_context(
            enabled=True,
            reason="ambiguous_not_general",
            semantic_result=semantic_result,
        )
    if mode not in {"SINGLE_TOPIC", "MULTI_TOPIC", "GENERAL"}:
        return _fallback_context(
            enabled=True,
            reason="unsupported_semantic_mode",
            semantic_result=semantic_result,
        )

    demands = _demand_map(question_demand_result)
    if not demands:
        return _fallback_context(
            enabled=True,
            reason="no_question_demands",
            semantic_result=semantic_result,
        )

    primary_topic_ids = _primary_topic_ids(semantic_result)
    explicit_uncovered = _distinct(
        semantic_result.get("uncovered_demand_ids")
    )

    if mode == "GENERAL":
        if primary_topic_ids:
            return _fallback_context(
                enabled=True,
                reason="general_mode_has_primary_topics",
                semantic_result=semantic_result,
            )
        uncovered_demand_ids = explicit_uncovered or list(demands)
        coverage_kind = "PURE_GENERAL"
    else:
        if not primary_topic_ids:
            return _fallback_context(
                enabled=True,
                reason="topic_mode_has_no_primary_topics",
                semantic_result=semantic_result,
            )
        if not explicit_uncovered:
            return _fallback_context(
                enabled=True,
                reason="no_uncovered_demands",
                semantic_result=semantic_result,
            )
        uncovered_demand_ids = explicit_uncovered
        coverage_kind = "HYBRID_TOPIC_GENERAL"

    unknown_uncovered = [
        demand_id
        for demand_id in uncovered_demand_ids
        if demand_id not in demands
    ]
    if unknown_uncovered:
        return _fallback_context(
            enabled=True,
            reason="unknown_uncovered_demand:" + ",".join(unknown_uncovered),
            semantic_result=semantic_result,
        )

    topic_evidence: list[Dict[str, Any]] = []
    if primary_topic_ids:
        candidate_ids = _candidate_topic_ids(shadow_candidate_result)
        model_answers = generated_sources.get("model_answer")
        fact_anchors = generated_sources.get("fact_anchor")

        for topic_id in primary_topic_ids:
            if topic_id not in candidate_ids:
                return _fallback_context(
                    enabled=True,
                    reason="primary_topic_missing_from_candidates:" + topic_id,
                    semantic_result=semantic_result,
                )

            model_answer = _find_topic_object(model_answers, topic_id)
            fact_anchor = _find_topic_object(fact_anchors, topic_id)

            if model_answer is None:
                return _fallback_context(
                    enabled=True,
                    reason="primary_topic_missing_model_answer:" + topic_id,
                    semantic_result=semantic_result,
                )
            if fact_anchor is None:
                return _fallback_context(
                    enabled=True,
                    reason="primary_topic_missing_fact_anchor:" + topic_id,
                    semantic_result=semantic_result,
                )

            topic_evidence.append(
                {
                    "topic_id": topic_id,
                    "title": str(model_answer.get("title") or "").strip(),
                    "model_answer": model_answer,
                    "fact_anchor": fact_anchor,
                }
            )

    general_demands = [
        {
            "demand_id": demand_id,
            "demand_text": demands[demand_id],
            "source": "question_demand",
        }
        for demand_id in uncovered_demand_ids
    ]

    return {
        "version": HYBRID_GENERAL_GRADING_CONTEXT_VERSION,
        "enabled": True,
        "applicable": True,
        "routing_mode": mode,
        "coverage_kind": coverage_kind,
        "primary_topic_ids": primary_topic_ids,
        "topic_evidence": topic_evidence,
        "demand_mappings": copy.deepcopy(
            semantic_result.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": uncovered_demand_ids,
        "general_engineering_evidence": {
            "basis": "question_demands_only",
            "knowledge_scope": (
                "general_industrial_instrumentation_control_engineering"
            ),
            "demands": general_demands,
            "score_component": False,
        },
        "fallback_reason": "",
        "policy": {
            "one_question_one_score": True,
            "topic_general_score_summing": False,
            "topic_general_score_averaging": False,
            "partial_scores_created": False,
            "primary_reference_overloaded": False,
            "new_runtime_mode_added": False,
            "student_answer_used_for_context": False,
            "logic_check_general_aggregation": False,
            "topic_importance_general_aggregation": False,
        },
        "provenance": {
            "semantic_result_preserved": True,
            "question_demand_result_preserved": True,
            "generated_topic_evidence_model_fact_only": True,
        },
    }
