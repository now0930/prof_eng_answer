"""Provider-free production grade builder for deterministic-primary mode."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

from grading.scoring.deterministic_requirement_evaluator import (
    evaluate_deterministic_requirements, load_machine_contracts,
)
from grading.scoring.deterministic_score_engine import calculate_deterministic_score
from grading.routing.deterministic_topic_router import route_question_topics
from grading.evidence.engineering_invariant_evaluator import evaluate_engineering_invariants
from grading.evidence.fact_anchor_evidence_adapter import (
    augment_requirement_evaluation,
    evaluate_fact_anchor_requirements,
    requirement_scope_by_topic,
)
from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.quantity_dimension_evaluator import evaluate_quantity_dimension_consistency
from grading.evidence.cross_topic_question_contract import evaluate_cross_topic_question


VERSION = "deterministic_primary_grader_v1"
MARKER = "DETERMINISTIC_GRADING_PRIMARY_V1"


class DeterministicPrimaryError(RuntimeError):
    pass


def _unresolved_requirement_ids(
    spans: list[dict[str, Any]], requirement_rows: list[dict[str, Any]],
    topic_ids: list[str],
) -> list[str]:
    """Only flag unresolved text tied to a still-missing machine-contract demand."""
    missing = {
        (str(row.get("owner_topic_id")), str(row.get("requirement_id")))
        for row in requirement_rows if row.get("status") == "MISSING"
    }
    if not spans or not missing:
        return []
    concepts = {
        str(concept)
        for span in spans for concept in span.get("concept_candidates", [])
    }
    affected: set[str] = set()
    for contract in load_machine_contracts(topic_ids):
        owner = str(contract["owner_topic_id"])
        facts = {row["fact_id"]: row for row in contract["facts"]}
        for rule in contract["requirement_rules"]:
            requirement_id = str(rule["requirement_id"])
            if (owner, requirement_id) not in missing:
                continue
            if any(
                str(facts[fact_id].get(field)) in concepts
                for fact_id in rule["required_fact_ids"]
                for field in ("subject", "object")
            ):
                affected.add(requirement_id)
    return sorted(affected)


def grade_deterministically(
    *, question_text: str, answer_text: str,
    llm_evidence_fn: Callable[[str], str] | None = None,
    qualitative_de_mode: str | None = None,
    qualitative_de_llm_fn: Callable[[str], str] | None = None,
) -> dict[str, Any]:
    de_mode = (qualitative_de_mode if qualitative_de_mode is not None
               else os.getenv("QUALITATIVE_DE_MODE", "off")).strip().casefold()
    if de_mode not in {"off", "argon"}:
        raise DeterministicPrimaryError("unsupported qualitative D/E mode")
    route = route_question_topics(question_text)
    if route["status"] != "ROUTED":
        raise DeterministicPrimaryError("deterministic topic routing abstained")
    extraction = extract_canonical_claim_evidence(
        answer_text,
        question_text=question_text,
        topic_ids=route["topic_ids"],
    )
    quantity = evaluate_quantity_dimension_consistency(
        extraction["canonical_evidence"]
    )
    engineering = evaluate_engineering_invariants(answer_text)
    violations = quantity["violations"] + engineering["violations"]
    cross_topic = evaluate_cross_topic_question(
        question_text=question_text,
        answer_text=answer_text,
        topic_ids=route["topic_ids"],
        llm_evidence_fn=llm_evidence_fn,
    )
    fact_anchors = cross_topic or evaluate_fact_anchor_requirements(
        question_text=question_text,
        answer_text=answer_text,
        topic_ids=route["topic_ids"],
    )
    requirements = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=[row["code"] for row in violations],
        topic_ids=route["topic_ids"],
        extraction_complete=True,
        requirement_scope_by_topic=requirement_scope_by_topic(fact_anchors),
    )
    requirements = augment_requirement_evaluation(
        requirements,
        fact_anchors,
    )
    unresolved_requirement_ids = _unresolved_requirement_ids(
        extraction["unresolved_spans"], requirements["requirements"], route["topic_ids"],
    )
    missing_count = int(requirements.get("summary", {}).get("MISSING", 0))
    recall_floor_ids = [
        str(row.get("requirement_id") or "")
        for row in requirements.get("requirements", [])
        if row.get("lexical_recall_floor_applied")
    ]
    low_evidence_recall = bool(
        missing_count >= 4
        and (
            recall_floor_ids
            or extraction.get("unresolved_spans")
        )
    )
    scope_selections = fact_anchors.get("question_contract_selections", [])
    scope_resolved = bool(scope_selections) and all(
        row.get("mode") in {"explicit_question_contract", "derived_question_contract", "cross_topic_question_contract"}
        for row in scope_selections
    )
    scope_exact = scope_resolved and all(
        row.get("mode") in {"explicit_question_contract", "cross_topic_question_contract"}
        for row in scope_selections
    )
    score = calculate_deterministic_score(requirements, answer_text=answer_text)
    if score["decision"] != "SCORED":
        raise DeterministicPrimaryError("deterministic score engine abstained")
    de_evaluation: dict[str, Any] = {
        "mode": de_mode, "status": "OFF" if de_mode == "off" else "FALLBACK",
        "score_effect": "none", "provider": "argon" if de_mode == "argon" else None,
        "provider_calls": 0,
    }
    if de_mode == "argon":
        from grading.qualitative.de_shadow import evaluate_qualitative_de
        from grading.qualitative.provider_transport import argon_call

        provider = qualitative_de_llm_fn
        api_key = os.getenv("GEMINI_API_KEY", "")
        if provider is None and api_key:
            provider = argon_call(api_key)
        owners = {row.get("owner_topic_id") for row in requirements["requirements"]}
        abc_result = {
            "score_breakdown": {key: score["score_breakdown"][key] for key in
                                ("A_structure", "B_requirement_completeness", "C_fact_correctness")},
            "requirements": requirements["requirements"],
        }
        shadow = evaluate_qualitative_de(
            question_text, answer_text, abc_result,
            {"topic_ids": [topic for topic in route["topic_ids"] if topic in owners],
             "verified_facts": []},
            llm_call=provider,
            model_metadata={"provider": "argon", "model_id": "gemini-4-argon",
                            "prompt_version": "qualitative_de_shadow_v3_examples"},
        )
        de_evaluation.update({
            "provider_calls": shadow["provider_calls"],
            "reason_code": shadow.get("reason_code"),
            "input_hash": shadow["input_hash"],
            "request_hash": shadow.get("request_hash"),
            "semantic_truth_verified": shadow["semantic_truth_verified"],
        })
        if shadow["status"] == "SHADOW_VALIDATED":
            proposed = {"D_engineering_judgment": shadow["proposed_d"],
                        "E_linkage": shadow["proposed_e"]}
            score = calculate_deterministic_score(
                requirements, answer_text=answer_text, de_override=proposed,
            )
            de_evaluation.update({
                "status": "APPLIED", "score_effect": "replace_de",
                "proposed_scores": proposed,
                "effective_scores": {key: score["score_breakdown"][key] for key in proposed},
                "criteria": shadow["criteria"],
                "interview_questions": shadow["interview_questions"],
            })
        else:
            de_evaluation["status"] = "FALLBACK"
    breakdown = [
        {"layer_id": key[0], "item": key, "score": value, "max_score": maximum}
        for key, value, maximum in (
            ("A_structure", score["score_breakdown"]["A_structure"], 3.0),
            ("B_requirement_completeness", score["score_breakdown"]["B_requirement_completeness"], 6.0),
            ("C_fact_correctness", score["score_breakdown"]["C_fact_correctness"], 8.0),
            ("D_engineering_judgment", score["score_breakdown"]["D_engineering_judgment"], 6.0),
            ("E_linkage", score["score_breakdown"]["E_linkage"], 2.0),
        )
    ]
    findings = [
        {
            **row,
            "severity": "fatal" if row["classification"] == "fatal" else row["classification"],
            "message": f"{row['invariant_code']} 결정론 규칙이 검출되었습니다.",
        }
        for row in requirements.get("findings", [])
    ]
    total = score["total_score"]
    score_range = (
        f"{max(0.0, total - 0.5):.1f}~{min(25.0, total + 0.5):.1f}"
    )
    if requirements["fatal_or_core_error"]:
        summary = (
            "검증된 핵심 기술 오류가 확인되었습니다. 현장 적용과 답안 구조의 "
            "장점과 별개로 해당 오류를 먼저 교정해야 합니다."
        )
    elif cross_topic and cross_topic["llm_evidence_audit"]["provider_calls"]:
        if cross_topic["llm_evidence_audit"]["accepted_count"]:
            summary = (
                "LLM의 근거 제안은 검토 후보로만 보관하고, 교차 Topic의 결정론적 "
                f"근거만으로 {total}/25.0점을 산정했습니다."
            )
        else:
            summary = (
                "LLM의 근거 제안이 채택되지 않아 교차 Topic의 결정론적 근거만으로 "
                f"{total}/25.0점을 산정했습니다."
            )
    else:
        summary = (
            f"외부 LLM 없이 Topic Pack과 공학 ontology의 결정론적 evidence로 "
            f"{total}/25.0점을 산정했습니다."
            if de_evaluation["status"] != "APPLIED" else
            f"Topic Pack과 공학 ontology의 결정론적 A/B/C evidence로 "
            f"{total}/25.0점을 산정했습니다."
        )
    if de_evaluation["status"] == "APPLIED":
        summary += " A/B/C는 결정론적으로 유지하고, Argon의 근거 검증된 D/E 제안을 반영했습니다."
    elif de_evaluation["status"] == "FALLBACK":
        summary += " Argon D/E 평가가 유효하지 않아 기존 결정론적 D/E를 사용했습니다."
    if unresolved_requirement_ids:
        summary += " 관련 문장의 의미 해석이 미해결되어 점수는 잠정값이며 합격 판정은 보류합니다."
    return {
        "version": VERSION,
        "marker": MARKER,
        "grading_engine": (
            "deterministic_abc_argon_de" if de_evaluation["status"] == "APPLIED"
            else "deterministic_primary"
        ),
        "provider_calls": (
            cross_topic["llm_evidence_audit"]["provider_calls"] if cross_topic else 0
        ) + de_evaluation["provider_calls"],
        "llm_verdict_authority": 0,
        "llm_score_authority": (
            "D_E_ONLY" if de_evaluation["status"] == "APPLIED" else "none"
        ),
        "external_llm_required_for_verdict": False,
        "qualitative_de_evaluation": de_evaluation,
        "topic_id": route["primary_topic_id"],
        "topic_ids": route["topic_ids"],
        "routing_evaluation": route,
        "question_scope_evaluation": {
            "resolved": scope_resolved,
            "exact": scope_exact,
            "selections": scope_selections,
        },
        "cross_topic_evidence": (
            {"contract_id": cross_topic["contract_id"],
             "llm_evidence_audit": cross_topic["llm_evidence_audit"],
             "llm_evidence_suggestions": cross_topic["llm_evidence_suggestions"]}
            if cross_topic else None
        ),
        "canonical_claim_extraction": {
            "marker": extraction["marker"],
            "claim_count": extraction["canonical_evidence"]["summary"]["claim_count"],
            "unresolved_span_count": len(extraction["unresolved_spans"]),
            "provider_calls": 0,
        },
        "requirements": requirements["requirements"],
        "requirement_summary": requirements["summary"],
        "canonical_promotion": requirements.get("canonical_promotion", {}),
        "evidence_recall_diagnostic": {
            "code": "LOW_EVIDENCE_RECALL" if low_evidence_recall else "OK",
            "warning": low_evidence_recall,
            "missing_requirement_count": missing_count,
            "lexical_recall_floor_requirement_ids": recall_floor_ids,
            "unresolved_span_count": len(extraction["unresolved_spans"]),
            "score_effect": "none",
        },
        "resolution_review": {
            "required": bool(unresolved_requirement_ids),
            "requirement_ids": unresolved_requirement_ids,
            "reason": "related_unresolved_claim" if unresolved_requirement_ids else None,
            "score_status": "provisional" if unresolved_requirement_ids else "final",
        },
        "passing_score_allowed": not bool(unresolved_requirement_ids),
        "logic_check_evaluation": {
            "fatal_error_detected": requirements["fatal_or_core_error"],
            "mode": "fatal" if requirements["fatal_or_core_error"] else "normal",
            "findings": findings,
        },
        "deterministic_score": score,
        "total_score": total,
        "max_score": 25.0,
        "score_range": score_range,
        "breakdown": breakdown,
        "verdict": "REVIEW_REQUIRED" if unresolved_requirement_ids else score["verdict"],
        "official_pass_met": bool(score["official_pass_met"] and not unresolved_requirement_ids),
        "high_score_met": bool(score["high_score_met"] and not unresolved_requirement_ids),
        "confidence": (
            "low" if unresolved_requirement_ids else
            "medium" if de_evaluation["status"] == "APPLIED"
            else "low" if de_evaluation["status"] == "FALLBACK"
            else
            "low"
            if cross_topic and cross_topic["llm_evidence_audit"]["error_type"]
            else "high"
            if requirements["fatal_or_core_error"] or (
                scope_exact and score["pass_evidence_eligible"]
            )
            else "medium"
        ),
        "summary": summary,
        "overall_comment": summary,
    }


def persist_deterministic_grade(session_dir: str | Path, grade: dict[str, Any]) -> str:
    if session_dir is None:
        raise DeterministicPrimaryError("deterministic grade persistence requires session_dir")
    path = Path(session_dir)
    path.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(grade, ensure_ascii=False, indent=2)
    (path / "deterministic_grade.json").write_text(raw, encoding="utf-8")
    (path / "grade_raw.txt").write_text(raw, encoding="utf-8")
    try:
        from grading.quality.operational_checksheet import (
            build_quality_checksheet, save_quality_checksheet,
        )
        save_quality_checksheet(path, build_quality_checksheet(grade))
    except Exception as error:
        # Quality tracking must never change or prevent the authoritative grade.
        # The class name is safe to log; the exception text could contain private data.
        print(f"[quality] checksheet_persistence_failed exception_type={type(error).__name__}")
    return raw
