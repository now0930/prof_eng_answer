"""Score-neutral deterministic grading shadow for production comparison."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

from local_semantic_resolver import resolve_with_optional_local_semantics
from engineering_invariant_evaluator import evaluate_engineering_invariants
from deterministic_requirement_evaluator import evaluate_deterministic_requirements
from deterministic_score_engine import calculate_deterministic_score
from fact_anchor_evidence_adapter import (
    augment_requirement_evaluation,
    evaluate_fact_anchor_requirements,
    requirement_scope_by_topic,
)
from quantity_dimension_evaluator import evaluate_quantity_dimension_consistency
from topic_machine_contract import extract_fatal_rule_ids, validate_topic_machine_contract


VERSION = "deterministic_grading_shadow_v1"
MARKER = "DETERMINISTIC_GRADING_SHADOW_V1"
ROOT = Path(__file__).resolve().parent


def _topic_id(grade: Mapping[str, Any]) -> str:
    for key in ("logic_check_topic_id", "topic_id", "inferred_topic_id"):
        value = str(grade.get(key) or "").strip()
        if value:
            return value
    return ""


def _machine_contract(topic_id: str) -> dict[str, Any] | None:
    if not topic_id:
        return None
    path = ROOT / "rubrics" / "topic_packs" / topic_id / "logic_check.json"
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    contract = payload.get("machine_contract")
    if not isinstance(contract, dict):
        return None
    known_rule_ids = extract_fatal_rule_ids(
        payload.get("llm_profile", {}).get("fatal_conditions", [])
    )
    return validate_topic_machine_contract(
        contract,
        topic_id=topic_id,
        known_rule_ids=known_rule_ids,
    )


def _claim_key(claim: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return tuple(
        str(claim.get(key) or "").strip().casefold()
        for key in ("subject", "predicate", "object", "polarity")
    )


def _requirement_results(
    contract: Mapping[str, Any] | None,
    claims: list[dict[str, Any]],
    violated_requirement_ids: set[str],
) -> list[dict[str, Any]]:
    if not contract:
        return []
    facts = {row["fact_id"]: row for row in contract["facts"]}
    claim_keys = {_claim_key(row) for row in claims}
    results: list[dict[str, Any]] = []
    for rule in contract["requirement_rules"]:
        required_ids = rule["required_fact_ids"]
        matched = [
            fact_id for fact_id in required_ids
            if _claim_key(facts[fact_id]) in claim_keys
        ]
        contradicted = [
            fact_id for fact_id in required_ids
            if any(
                key[:3] == _claim_key(facts[fact_id])[:3]
                and key[3] != _claim_key(facts[fact_id])[3]
                for key in claim_keys
            )
        ]
        requirement_id = rule["requirement_id"]
        if requirement_id in violated_requirement_ids or contradicted:
            status = "WRONG"
        elif len(matched) >= rule["minimum_match_count"]:
            status = "SATISFIED"
        elif matched:
            status = "PARTIAL"
        else:
            status = "MISSING"
        results.append({
            "requirement_id": requirement_id,
            "status": status,
            "matched_fact_ids": matched,
            "contradicted_fact_ids": contradicted,
        })
    return results


def build_deterministic_grading_shadow(
    *,
    grade: Mapping[str, Any],
    question_text: str,
    answer_text: str,
    semantic_call=None,
) -> dict[str, Any]:
    """Calculate deterministic findings without changing the legacy grade."""
    topic_id = _topic_id(grade)
    resolver = resolve_with_optional_local_semantics(
        question_text=question_text,
        answer_text=answer_text,
        semantic_call=semantic_call,
        topic_ids=[topic_id] if topic_id else None,
    )
    evidence_documents = resolver["evidence_documents"]
    claims = [
        copy.deepcopy(claim)
        for document in evidence_documents
        for claim in document.get("claims", [])
    ]
    dimension = evaluate_quantity_dimension_consistency({"claims": claims})
    engineering = evaluate_engineering_invariants(answer_text)
    contract = _machine_contract(topic_id)
    findings: list[dict[str, Any]] = []
    violated_requirements: set[str] = set()
    for violation in dimension["violations"] + engineering["violations"]:
        bindings = (
            [row for row in contract["invariant_bindings"]
             if row["invariant_code"] == violation["code"]]
            if contract else []
        )
        if not bindings:
            findings.append({
                "finding_id": violation["code"].casefold(),
                "classification": "technical_error",
                "invariant_code": violation["code"],
                "requirement_refs": [],
            })
            continue
        for binding in bindings:
            violated_requirements.update(binding["requirement_refs"])
            findings.append({
                "finding_id": binding["rule_id"],
                "classification": binding["classification"],
                "invariant_code": violation["code"],
                "requirement_refs": list(binding["requirement_refs"]),
                "recommended_ceiling": binding["recommended_ceiling"],
            })
    fact_anchors = evaluate_fact_anchor_requirements(
        answer_text=answer_text,
        topic_ids=[topic_id] if topic_id else [],
        question_text=question_text,
    )
    requirement_evaluation = evaluate_deterministic_requirements(
        claims=claims,
        invariant_codes=[
            row["code"] for row in dimension["violations"] + engineering["violations"]
        ],
        topic_ids=[topic_id] if topic_id else None,
        extraction_complete=True,
        requirement_scope_by_topic=requirement_scope_by_topic(fact_anchors),
    )
    requirement_evaluation = augment_requirement_evaluation(
        requirement_evaluation,
        fact_anchors,
    )
    if requirement_evaluation["requirements"]:
        requirements = requirement_evaluation["requirements"]
        findings = requirement_evaluation["findings"] or findings
    else:
        requirements = _requirement_results(contract, claims, violated_requirements)
    deterministic_score = calculate_deterministic_score(
        requirement_evaluation, answer_text=answer_text,
    )
    return {
        "version": VERSION,
        "marker": MARKER,
        "mode": "shadow",
        "topic_id": topic_id or None,
        "score_effect": "none",
        "production_score_changed": False,
        "production_verdict_changed": False,
        "llm_verdict_authority": 0,
        "provider_calls": resolver["provider_calls"],
        "resolver_status": resolver["status"],
        "evidence_fingerprint": [
            row["evidence_sha256"] for row in evidence_documents
        ],
        "findings": findings,
        "requirements": requirements,
        "fatal_or_core_error": any(
            row["classification"] in {"fatal", "core_error"}
            for row in findings
        ),
        "requirement_full_credit_allowed": requirement_evaluation[
            "requirement_full_credit_allowed"
        ],
        "perfect_theory_comment_allowed": requirement_evaluation[
            "perfect_theory_comment_allowed"
        ],
        "deterministic_score_candidate": deterministic_score,
    }


def attach_deterministic_grading_shadow(
    value: Any,
    *,
    question_text: str,
    answer_text: str,
    is_grade_dict,
) -> Any:
    """Recursively attach a score-neutral shadow to grade dictionaries."""
    if is_grade_dict(value):
        output = dict(value)
        output["deterministic_grading_shadow"] = build_deterministic_grading_shadow(
            grade=output,
            question_text=question_text,
            answer_text=answer_text,
        )
        return output
    if isinstance(value, list):
        return [
            attach_deterministic_grading_shadow(
                item, question_text=question_text, answer_text=answer_text,
                is_grade_dict=is_grade_dict,
            ) for item in value
        ]
    if isinstance(value, tuple):
        return tuple(
            attach_deterministic_grading_shadow(
                item, question_text=question_text, answer_text=answer_text,
                is_grade_dict=is_grade_dict,
            ) for item in value
        )
    if isinstance(value, dict):
        return {
            key: attach_deterministic_grading_shadow(
                item, question_text=question_text, answer_text=answer_text,
                is_grade_dict=is_grade_dict,
            ) for key, item in value.items()
        }
    return value
