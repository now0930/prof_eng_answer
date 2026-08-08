from __future__ import annotations

import copy
from typing import Any, Dict, Optional


HYBRID_GENERAL_SUBJECT_EVIDENCE_VERSION = (
    "hybrid_general_subject_evidence_v1"
)
HYBRID_GENERAL_QUESTION_SUMMARY_VERSION = (
    "hybrid_general_question_summary_v1"
)


def _valid_context(
    model_answer_ref: Any,
) -> Optional[Dict[str, Any]]:
    if not isinstance(model_answer_ref, dict):
        return None

    context = model_answer_ref.get(
        "hybrid_general_grading_context"
    )
    if not isinstance(context, dict):
        return None
    if context.get("applicable") is not True:
        return None

    coverage_kind = str(
        context.get("coverage_kind") or ""
    ).strip()
    routing_mode = str(
        context.get("routing_mode") or ""
    ).strip()

    if coverage_kind == "PURE_GENERAL":
        if routing_mode != "GENERAL":
            return None
    elif coverage_kind == "HYBRID_TOPIC_GENERAL":
        if routing_mode not in {
            "SINGLE_TOPIC",
            "MULTI_TOPIC",
        }:
            return None
    else:
        return None

    general = context.get(
        "general_engineering_evidence"
    )
    if not isinstance(general, dict):
        return None
    if general.get("score_component") is not False:
        return None

    return context


def build_hybrid_general_subject_evidence(
    model_answer_ref: Any,
) -> Optional[Dict[str, Any]]:
    context = _valid_context(model_answer_ref)
    if context is None:
        return None

    topics = []
    for row in context.get("topic_evidence") or []:
        if not isinstance(row, dict):
            continue
        topic_id = str(row.get("topic_id") or "").strip()
        if not topic_id:
            continue
        topics.append(
            {
                "topic_id": topic_id,
                "title": copy.deepcopy(row.get("title")),
                "model_answer": copy.deepcopy(
                    row.get("model_answer")
                ),
                "fact_anchor": copy.deepcopy(
                    row.get("fact_anchor")
                ),
            }
        )

    return {
        "version": HYBRID_GENERAL_SUBJECT_EVIDENCE_VERSION,
        "routing_mode": context.get("routing_mode"),
        "coverage_kind": context.get("coverage_kind"),
        "primary_topic_ids": copy.deepcopy(
            context.get("primary_topic_ids") or []
        ),
        "topics": topics,
        "general_engineering_evidence": copy.deepcopy(
            context.get("general_engineering_evidence")
        ),
        "demand_mappings": copy.deepcopy(
            context.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            context.get("uncovered_demand_ids") or []
        ),
        "policy": {
            "one_question_one_score": True,
            "topic_general_score_summing": False,
            "topic_general_score_averaging": False,
            "partial_scores_created": False,
            "logic_check_general_aggregation": False,
            "topic_importance_general_aggregation": False,
        },
    }


def attach_hybrid_general_evidence_to_subject_rubric(
    subject_rubric: Any,
    model_answer_ref: Any,
) -> Any:
    evidence = build_hybrid_general_subject_evidence(
        model_answer_ref
    )
    if evidence is None or not isinstance(subject_rubric, dict):
        return subject_rubric

    result = copy.deepcopy(subject_rubric)
    result["hybrid_general_grading_evidence"] = evidence
    return result


def build_hybrid_general_question_contract_summary(
    model_answer_ref: Any,
) -> Optional[Dict[str, Any]]:
    context = _valid_context(model_answer_ref)
    if context is None:
        return None

    return {
        "version": HYBRID_GENERAL_QUESTION_SUMMARY_VERSION,
        "routing_mode": context.get("routing_mode"),
        "coverage_kind": context.get("coverage_kind"),
        "primary_topic_ids": copy.deepcopy(
            context.get("primary_topic_ids") or []
        ),
        "demand_mappings": copy.deepcopy(
            context.get("demand_mappings") or []
        ),
        "uncovered_demand_ids": copy.deepcopy(
            context.get("uncovered_demand_ids") or []
        ),
        "general_demand_count": len(
            (
                context.get("general_engineering_evidence")
                or {}
            ).get("demands")
            or []
        ),
        "policy": {
            "one_question_one_score": True,
            "primary_reference_overloaded": False,
            "new_runtime_mode_added": False,
        },
    }


def attach_hybrid_general_summary_to_question_contract(
    contract: Any,
    model_answer_ref: Any,
) -> Any:
    summary = build_hybrid_general_question_contract_summary(
        model_answer_ref
    )
    if summary is None or not isinstance(contract, dict):
        return contract

    result = copy.deepcopy(contract)
    result["hybrid_general_grading_context_summary"] = summary

    if str(result.get("contract_hash") or "").strip():
        from question_contract import rehash_question_contract

        return rehash_question_contract(result)

    return result


def enrich_hybrid_general_model_reference_with_contract(
    model_answer_ref: Any,
    contract: Any,
) -> Any:
    context = _valid_context(model_answer_ref)
    if context is None:
        return model_answer_ref
    if not isinstance(model_answer_ref, dict):
        return model_answer_ref
    if not isinstance(contract, dict):
        return model_answer_ref

    summary = contract.get(
        "hybrid_general_grading_context_summary"
    )
    if not isinstance(summary, dict):
        return model_answer_ref

    result = copy.deepcopy(model_answer_ref)
    result_context = copy.deepcopy(
        result["hybrid_general_grading_context"]
    )
    result_context["question_contract_summary"] = (
        copy.deepcopy(summary)
    )
    result["hybrid_general_grading_context"] = result_context
    return result
