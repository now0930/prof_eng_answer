"""Provider-free production grade builder for deterministic-primary mode."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deterministic_requirement_evaluator import evaluate_deterministic_requirements
from deterministic_score_engine import calculate_deterministic_score
from deterministic_topic_router import route_question_topics
from engineering_invariant_evaluator import evaluate_engineering_invariants
from fact_anchor_evidence_adapter import augment_requirement_evaluation, evaluate_fact_anchor_requirements
from canonical_claim_extractor import extract_canonical_claim_evidence
from quantity_dimension_evaluator import evaluate_quantity_dimension_consistency


VERSION = "deterministic_primary_grader_v1"
MARKER = "DETERMINISTIC_GRADING_PRIMARY_V1"


class DeterministicPrimaryError(RuntimeError):
    pass


def grade_deterministically(*, question_text: str, answer_text: str) -> dict[str, Any]:
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
    requirements = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=[row["code"] for row in violations],
        topic_ids=route["topic_ids"],
        extraction_complete=True,
    )
    requirements = augment_requirement_evaluation(
        requirements,
        evaluate_fact_anchor_requirements(
            question_text=question_text,
            answer_text=answer_text,
            topic_ids=route["topic_ids"],
        ),
    )
    score = calculate_deterministic_score(requirements, answer_text=answer_text)
    if score["decision"] != "SCORED":
        raise DeterministicPrimaryError("deterministic score engine abstained")
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
    else:
        summary = (
            f"외부 LLM 없이 Topic Pack과 공학 ontology의 결정론적 evidence로 "
            f"{total}/25.0점을 산정했습니다."
        )
    return {
        "version": VERSION,
        "marker": MARKER,
        "grading_engine": "deterministic_primary",
        "provider_calls": 0,
        "llm_verdict_authority": 0,
        "external_llm_required_for_verdict": False,
        "topic_id": route["primary_topic_id"],
        "topic_ids": route["topic_ids"],
        "routing_evaluation": route,
        "canonical_claim_extraction": {
            "marker": extraction["marker"],
            "claim_count": extraction["canonical_evidence"]["summary"]["claim_count"],
            "unresolved_span_count": len(extraction["unresolved_spans"]),
            "provider_calls": 0,
        },
        "requirements": requirements["requirements"],
        "requirement_summary": requirements["summary"],
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
        "verdict": score["verdict"],
        "official_pass_met": score["official_pass_met"],
        "high_score_met": score["high_score_met"],
        "confidence": (
            "high"
            if requirements["fatal_or_core_error"] or score["pass_evidence_eligible"]
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
    return raw
