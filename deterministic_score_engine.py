"""Deterministic score/verdict owner with explicit abstention on coverage gaps."""

from __future__ import annotations

import math
from typing import Any, Mapping

from deterministic_score_evidence import evaluate_score_evidence


VERSION = "deterministic_score_engine_v1"
MARKER = "DETERMINISTIC_SCORE_ENGINE_V1"
_CREDIT = {"SATISFIED": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "MISSING": 0.0}
MINIMUM_SATISFIED_RATIO_FOR_PASS = 0.15
PASS_EVIDENCE_CEILING_RATIO = 0.58
NO_SATISFIED_NONFATAL_CEILING_RATIO = 0.44


def calculate_deterministic_score(
    requirement_evaluation: Mapping[str, Any],
    *,
    max_score: float = 25.0,
    answer_text: str | None = None,
) -> dict[str, Any]:
    requirements = requirement_evaluation.get("requirements")
    if not isinstance(requirements, list):
        requirements = []
    unknown = [row for row in requirements if row.get("status") not in _CREDIT]
    coverage_complete = bool(requirements) and not unknown
    base = {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "llm_verdict_authority": 0,
        "max_score": float(max_score),
        "coverage_complete": coverage_complete,
    }
    if not coverage_complete:
        return {
            **base,
            "decision": "ABSTAIN",
            "total_score": None,
            "verdict": "UNKNOWN",
            "external_llm_required_for_verdict": True,
            "reason": "deterministic_requirement_coverage_incomplete",
        }

    requirement_ratio = sum(
        _CREDIT[row["status"]] for row in requirements
    ) / len(requirements)
    satisfied_ratio = sum(
        row["status"] == "SATISFIED" for row in requirements
    ) / len(requirements)
    score_evidence = evaluate_score_evidence(answer_text) if answer_text is not None else None
    if score_evidence is None:
        raw_score = float(max_score) * requirement_ratio
        breakdown = None
    else:
        content_ratio = math.sqrt(requirement_ratio)
        breakdown = {
            "A_structure": score_evidence["structure"]["score"],
            "B_requirement_completeness": round(6.0 * content_ratio, 6),
            "C_fact_correctness": round(8.0 * content_ratio, 6),
            "D_engineering_judgment": score_evidence["engineering_judgment"]["score"],
            "E_linkage": score_evidence["linkage"]["score"],
        }
        raw_score = sum(breakdown.values())
    ceilings = [
        float(row["recommended_ceiling"])
        for row in requirement_evaluation.get("findings", [])
        if row.get("classification") in {"fatal", "core_error"}
        and isinstance(row.get("recommended_ceiling"), (int, float))
    ]
    all_ceilings = list(ceilings)
    minimum_satisfied_ratio_for_pass = MINIMUM_SATISFIED_RATIO_FOR_PASS
    pass_evidence_eligible = satisfied_ratio >= minimum_satisfied_ratio_for_pass
    if not pass_evidence_eligible:
        all_ceilings.append(float(max_score) * PASS_EVIDENCE_CEILING_RATIO)
    if (
        score_evidence is not None
        and not score_evidence["high_score_eligibility"]["eligible"]
    ):
        all_ceilings.append(
            float(score_evidence["high_score_eligibility"]["ceiling_when_ineligible"])
        )
    total = min([raw_score, *all_ceilings]) if all_ceilings else raw_score
    total = round(total, 2)
    fatal = bool(requirement_evaluation.get("fatal_or_core_error"))
    no_satisfied_nonfatal_ceiling_applied = bool(not fatal and satisfied_ratio == 0.0)
    if no_satisfied_nonfatal_ceiling_applied:
        # A collection of partial lexical matches must not become a mid-band
        # answer merely because an exact question contract has fewer anchors.
        # Fatal/core-error scores retain their separately reviewed ceilings.
        all_ceilings.append(float(max_score) * NO_SATISFIED_NONFATAL_CEILING_RATIO)
        total = min([raw_score, *all_ceilings])
        total = round(total, 2)
    if fatal:
        verdict = "NEEDS_CORRECTION"
    elif total >= max_score * 0.8:
        verdict = "HIGH_SCORE"
    elif total >= max_score * 0.7:
        verdict = "PRACTICAL_TARGET"
    elif total >= max_score * 0.6:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    return {
        **base,
        "decision": "SCORED",
        "total_score": total,
        "raw_score": round(raw_score, 2),
        "applied_ceiling": min(all_ceilings) if all_ceilings else None,
        "score_breakdown": breakdown,
        "score_evidence": score_evidence,
        "satisfied_requirement_ratio": round(satisfied_ratio, 6),
        "minimum_satisfied_ratio_for_pass": minimum_satisfied_ratio_for_pass,
        "pass_evidence_eligible": pass_evidence_eligible,
        "no_satisfied_nonfatal_ceiling_applied": no_satisfied_nonfatal_ceiling_applied,
        "verdict": verdict,
        "external_llm_required_for_verdict": False,
        "official_pass_met": bool(not fatal and total >= max_score * 0.6),
        "high_score_met": bool(not fatal and total >= max_score * 0.8),
    }
