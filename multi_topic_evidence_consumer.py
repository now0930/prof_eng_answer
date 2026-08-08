from __future__ import annotations

import copy
from typing import Any, Dict, Optional


MULTI_TOPIC_SUBJECT_EVIDENCE_VERSION = (
    "multi_topic_subject_evidence_v1"
)
MULTI_TOPIC_QUESTION_CONTRACT_VERSION = (
    "multi_topic_question_contract_v1"
)


def _valid_context(
    model_answer_ref: Any,
) -> Optional[Dict[str, Any]]:
    if not isinstance(model_answer_ref, dict):
        return None

    context = model_answer_ref.get(
        "multi_topic_grading_context"
    )
    if not isinstance(context, dict):
        return None
    if context.get("applicable") is not True:
        return None
    if context.get("routing_mode") != "MULTI_TOPIC":
        return None

    primary_topic_ids = context.get(
        "primary_topic_ids"
    )
    topic_evidence = context.get("topic_evidence")

    if not isinstance(primary_topic_ids, list):
        return None
    if not isinstance(topic_evidence, list):
        return None

    distinct = []
    seen = set()
    for value in primary_topic_ids:
        topic_id = str(value or "").strip()
        if not topic_id or topic_id in seen:
            continue
        seen.add(topic_id)
        distinct.append(topic_id)

    if len(distinct) < 2:
        return None

    evidence_ids = [
        str(row.get("topic_id") or "").strip()
        for row in topic_evidence
        if isinstance(row, dict)
    ]

    if any(
        topic_id not in evidence_ids
        for topic_id in distinct
    ):
        return None

    return context


def build_multi_topic_subject_evidence(
    model_answer_ref: Any,
) -> Optional[Dict[str, Any]]:
    """Build non-scoring combined evidence for the subject rubric."""

    context = _valid_context(model_answer_ref)
    if context is None:
        return None

    primary_topic_ids = [
        str(value).strip()
        for value in context["primary_topic_ids"]
        if str(value or "").strip()
    ]

    topics = []
    by_topic = {
        str(row.get("topic_id") or "").strip(): row
        for row in context.get("topic_evidence") or []
        if isinstance(row, dict)
    }

    for topic_id in primary_topic_ids:
        row = by_topic[topic_id]
        topics.append(
            {
                "topic_id": topic_id,
                "title": copy.deepcopy(
                    row.get("title")
                ),
                "model_answer": copy.deepcopy(
                    row.get("model_answer")
                ),
                "fact_anchor": copy.deepcopy(
                    row.get("fact_anchor")
                ),
            }
        )

    return {
        "version": MULTI_TOPIC_SUBJECT_EVIDENCE_VERSION,
        "routing_mode": "MULTI_TOPIC",
        "primary_topic_ids": primary_topic_ids,
        "topics": topics,
        "demand_mappings": copy.deepcopy(
            context.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            context.get("uncovered_demand_ids") or []
        ),
        "policy": {
            "one_question_one_score": True,
            "topic_score_summing": False,
            "topic_score_averaging": False,
            "logic_topic_id_list_overload": False,
            "difficulty_aggregation": False,
        },
    }


def attach_multi_topic_evidence_to_subject_rubric(
    subject_rubric: Any,
    model_answer_ref: Any,
) -> Any:
    """Attach evidence without replacing legacy single-topic rubric fields."""

    evidence = build_multi_topic_subject_evidence(
        model_answer_ref
    )
    if evidence is None:
        return subject_rubric

    if not isinstance(subject_rubric, dict):
        return subject_rubric

    result = copy.deepcopy(subject_rubric)
    result["multi_topic_grading_evidence"] = evidence
    return result


def build_multi_topic_question_contract_summary(
    model_answer_ref: Any,
) -> Optional[Dict[str, Any]]:
    """Build a question-level multi-topic coverage summary."""

    context = _valid_context(model_answer_ref)
    if context is None:
        return None

    topics = []
    for row in context.get("topic_evidence") or []:
        if not isinstance(row, dict):
            continue

        topic_id = str(
            row.get("topic_id") or ""
        ).strip()
        if not topic_id:
            continue

        topics.append(
            {
                "topic_id": topic_id,
                "title": copy.deepcopy(
                    row.get("title")
                ),
            }
        )

    return {
        "version": MULTI_TOPIC_QUESTION_CONTRACT_VERSION,
        "routing_mode": "MULTI_TOPIC",
        "primary_topic_ids": copy.deepcopy(
            context.get("primary_topic_ids") or []
        ),
        "topics": topics,
        "demand_mappings": copy.deepcopy(
            context.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            context.get("uncovered_demand_ids") or []
        ),
        "coverage_policy": {
            "combined_primary_topic_coverage": True,
            "primary_reference_overloaded": False,
            "one_question_one_score": True,
        },
    }


def attach_multi_topic_summary_to_question_contract(
    contract: Any,
    model_answer_ref: Any,
) -> Any:
    """Attach a parallel summary to an existing question contract."""

    summary = build_multi_topic_question_contract_summary(
        model_answer_ref
    )
    if summary is None:
        return contract

    if not isinstance(contract, dict):
        return contract

    result = copy.deepcopy(contract)
    result["multi_topic_grading_context_summary"] = summary
    return result


def enrich_multi_topic_model_reference_with_contract(
    model_answer_ref: Any,
    contract: Any,
) -> Any:
    """Preserve parallel context and add only its contract summary."""

    context = _valid_context(model_answer_ref)
    if context is None:
        return model_answer_ref

    if not isinstance(model_answer_ref, dict):
        return model_answer_ref
    if not isinstance(contract, dict):
        return model_answer_ref

    summary = contract.get(
        "multi_topic_grading_context_summary"
    )
    if not isinstance(summary, dict):
        return model_answer_ref

    result = copy.deepcopy(model_answer_ref)
    result_context = copy.deepcopy(
        result["multi_topic_grading_context"]
    )
    result_context["question_contract_summary"] = (
        copy.deepcopy(summary)
    )
    result["multi_topic_grading_context"] = result_context
    return result
