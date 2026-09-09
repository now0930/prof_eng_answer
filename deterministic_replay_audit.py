"""Gemini-off replay audit for deterministic correctness coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from expert_accuracy_benchmark import load_jsonl, validate_gold_case
from engineering_invariant_evaluator import evaluate_engineering_invariants
from deterministic_requirement_evaluator import evaluate_deterministic_requirements
from deterministic_score_engine import calculate_deterministic_score
from deterministic_topic_router import route_question_topics
from fact_anchor_evidence_adapter import (
    augment_requirement_evaluation,
    evaluate_fact_anchor_requirements,
    requirement_scope_by_topic,
)
from canonical_claim_extractor import extract_canonical_claim_evidence
from quantity_dimension_evaluator import evaluate_quantity_dimension_consistency
from topic_machine_contract import extract_fatal_rule_ids, validate_topic_machine_contract


VERSION = "deterministic_replay_audit_v1"
MARKER = "DETERMINISTIC_REPLAY_AUDIT_V1"


def _fixture(root: Path, case: dict[str, Any]) -> tuple[str, str]:
    source = case.get("source") or {}
    payload = json.loads((root / str(source.get("path") or "")).read_text(encoding="utf-8"))
    source_case_id = str(source.get("source_case_id") or "").strip()
    if source_case_id:
        payload = next(
            row for row in payload.get("cases", [])
            if isinstance(row, dict) and row.get("case_id") == source_case_id
        )
    question = str(payload.get("question") or "").strip()
    answer = str(payload.get("answer") or payload.get("original_answer") or "").strip()
    if not question or not answer:
        raise ValueError(f"fixture input missing: {case.get('case_id')}")
    return question, answer


def _invariant_bindings(root: Path) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for path in sorted((root / "rubrics/topic_packs").glob("*/logic_check.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        contract = payload.get("machine_contract")
        if not isinstance(contract, dict):
            continue
        fatal_ids = extract_fatal_rule_ids(
            payload.get("llm_profile", {}).get("fatal_conditions", [])
        )
        validated = validate_topic_machine_contract(
            contract,
            topic_id=path.parent.name,
            known_rule_ids=fatal_ids,
        )
        for binding in validated["invariant_bindings"]:
            result.setdefault(binding["invariant_code"], []).append(binding)
    return result


def run_deterministic_replay_audit(
    *,
    root: Path,
    golden_path: Path,
) -> dict[str, Any]:
    cases = load_jsonl(golden_path, validate_gold_case)
    bindings = _invariant_bindings(root)
    rows: list[dict[str, Any]] = []
    known_fatal_count = 0
    true_positive = 0
    false_positive = 0
    repeatability_failures = 0
    scored_case_count = 0
    score_consistency_failures = 0
    score_distances: list[float] = []
    score_in_range_count = 0
    overgrading_violations: list[dict[str, Any]] = []
    routing_true_positive = 0
    routing_expected_count = 0
    routing_false_positive = 0
    unexplained: list[dict[str, Any]] = []

    def analyze(question: str, answer: str, topic_ids: list[str]) -> dict[str, Any]:
        extraction = extract_canonical_claim_evidence(
            answer, question_text=question, topic_ids=topic_ids,
        )
        quantity = evaluate_quantity_dimension_consistency(
            extraction["canonical_evidence"]
        )
        engineering = evaluate_engineering_invariants(answer)
        return {
            "violations": quantity["violations"] + engineering["violations"],
            "claims": extraction["canonical_evidence"]["claims"],
            "provider_calls": engineering["provider_calls"],
        }

    for case in cases:
        question, answer = _fixture(root, case)
        routed = route_question_topics(question)
        expected_topics = set(case.get("topic_ids", []))
        routed_topics = set(routed["topic_ids"])
        routing_true_positive += len(expected_topics & routed_topics)
        routing_expected_count += len(expected_topics)
        routing_false_positive += len(routed_topics - expected_topics)
        first = analyze(question, answer, routed["topic_ids"])
        second = analyze(question, answer, routed["topic_ids"])
        repeatable = first == second
        if not repeatable:
            repeatability_failures += 1
        detected_ids = {
            binding["rule_id"]
            for violation in first["violations"]
            for binding in bindings.get(violation["code"], [])
            if binding["classification"] == "fatal"
        }
        invariant_codes = {row["code"] for row in first["violations"]}
        fact_anchors = evaluate_fact_anchor_requirements(
            answer_text=answer,
            topic_ids=routed["topic_ids"],
            question_text=question,
        )
        requirement_evaluation = evaluate_deterministic_requirements(
            claims=first["claims"],
            invariant_codes=invariant_codes,
            topic_ids=routed["topic_ids"],
            extraction_complete=True,
            requirement_scope_by_topic=requirement_scope_by_topic(fact_anchors),
        )
        requirement_evaluation = augment_requirement_evaluation(
            requirement_evaluation,
            fact_anchors,
        )
        detected_ids.update(
            finding["finding_id"]
            for finding in requirement_evaluation.get("findings", [])
            if finding.get("classification") == "fatal"
        )
        gold_ids = {
            finding["finding_id"]
            for finding in case["labels"]["findings"]
            if finding["severity"] == "fatal"
        }
        known_fatal_count += len(gold_ids)
        true_positive += len(gold_ids & detected_ids)
        false_positive += len(detected_ids - gold_ids)
        score = calculate_deterministic_score(requirement_evaluation, answer_text=answer)
        repeated_requirements = evaluate_deterministic_requirements(
            claims=second["claims"],
            invariant_codes={row["code"] for row in second["violations"]},
            topic_ids=routed["topic_ids"],
            extraction_complete=True,
            requirement_scope_by_topic=requirement_scope_by_topic(fact_anchors),
        )
        repeated_requirements = augment_requirement_evaluation(
            repeated_requirements,
            fact_anchors,
        )
        repeated_score = calculate_deterministic_score(repeated_requirements, answer_text=answer)
        if score != repeated_score:
            score_consistency_failures += 1
        if score["decision"] == "SCORED":
            scored_case_count += 1
            score_range = case.get("labels", {}).get("score_range", {})
            minimum = float(score_range.get("min", 0.0))
            maximum = float(score_range.get("max", 25.0))
            value = float(score["total_score"])
            distance = minimum - value if value < minimum else value - maximum if value > maximum else 0.0
            score_distances.append(distance)
            if distance == 0.0:
                score_in_range_count += 1
            flags = case.get("labels", {}).get("flags", {})
            if flags.get("passing_score_allowed") is False and score.get("official_pass_met"):
                overgrading_violations.append({
                    "case_id": case["case_id"], "code": "FALSE_PASS",
                })
            if flags.get("strong_verdict_allowed") is False and score.get("high_score_met"):
                overgrading_violations.append({
                    "case_id": case["case_id"], "code": "FALSE_HIGH_SCORE",
                })
        for finding_id in sorted(gold_ids - detected_ids):
            unexplained.append({
                "case_id": case["case_id"],
                "finding_id": finding_id,
                "reason": "no_deterministic_invariant_owner",
            })
        rows.append({
            "case_id": case["case_id"],
            "gold_fatal_ids": sorted(gold_ids),
            "detected_fatal_ids": sorted(detected_ids),
            "deterministic_violation_codes": sorted({
                violation["code"] for violation in first["violations"]
            }),
            "repeatable": repeatable,
            "deterministic_score_decision": score["decision"],
            "deterministic_score": score["total_score"],
            "deterministic_raw_score": score.get("raw_score"),
            "deterministic_applied_ceiling": score.get("applied_ceiling"),
            "deterministic_score_breakdown": score.get("score_breakdown"),
            "deterministic_score_evidence": score.get("score_evidence"),
            "gold_score_range": case.get("labels", {}).get("score_range"),
            "deterministic_routed_topic_ids": routed["topic_ids"],
            "gold_topic_ids": sorted(expected_topics),
        })

    recall = true_positive / known_fatal_count if known_fatal_count else 1.0
    fatal_invariants_ready = bool(
        recall == 1.0
        and false_positive == 0
        and repeatability_failures == 0
        and not unexplained
    )
    score_coverage = scored_case_count / len(cases) if cases else 0.0
    score_consistent = score_consistency_failures == 0
    mean_score_distance = (
        sum(score_distances) / len(score_distances) if score_distances else None
    )
    score_in_range_rate = (
        score_in_range_count / len(score_distances) if score_distances else 0.0
    )
    routing_recall = (
        routing_true_positive / routing_expected_count if routing_expected_count else 0.0
    )
    score_accuracy_ready = bool(
        score_coverage == 1.0
        and score_consistent
        and not overgrading_violations
        and mean_score_distance is not None
        and mean_score_distance <= 1.0
        and score_in_range_rate >= 0.85
    )
    ready = bool(
        fatal_invariants_ready
        and score_accuracy_ready
        and routing_recall == 1.0
        and routing_false_positive == 0
    )
    return {
        "version": VERSION,
        "marker": MARKER,
        "provider_calls": 0,
        "case_count": len(cases),
        "known_fatal_count": known_fatal_count,
        "known_fatal_true_positive": true_positive,
        "known_fatal_recall": round(recall, 6),
        "fatal_false_positive_count": false_positive,
        "fatal_invariants_ready": fatal_invariants_ready,
        "deterministic_repeatability": (
            1.0 if not repeatability_failures else round(
                (len(cases) - repeatability_failures) / len(cases), 6
            )
        ),
        "unexplained_verdict_diff_count": len(unexplained),
        "deterministic_scored_case_count": scored_case_count,
        "deterministic_score_coverage": round(score_coverage, 6),
        "score_verdict_consistency_pass": score_consistent,
        "deterministic_score_mean_out_of_range_distance": (
            round(mean_score_distance, 6) if mean_score_distance is not None else None
        ),
        "deterministic_score_in_range_rate": round(score_in_range_rate, 6),
        "deterministic_score_accuracy_ready": score_accuracy_ready,
        "deterministic_topic_routing_recall": round(routing_recall, 6),
        "deterministic_topic_routing_false_positive_count": routing_false_positive,
        "known_overgrading_regression_pass": not overgrading_violations,
        "known_overgrading_violation_count": len(overgrading_violations),
        "known_overgrading_violations": overgrading_violations,
        "normal_answer_regression_pass": bool(false_positive == 0),
        "external_llm_required_for_verdict": not ready,
        "llm_verdict_authority_removal_ready": ready,
        "decision": "READY" if ready else "HOLD",
        "unexplained_differences": unexplained,
        "cases": rows,
    }
