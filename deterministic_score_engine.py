"""Deterministic score/verdict owner with explicit abstention on coverage gaps."""

from __future__ import annotations

from typing import Any, Mapping


VERSION = "deterministic_score_engine_v1"
MARKER = "DETERMINISTIC_SCORE_ENGINE_V1"
_CREDIT = {"SATISFIED": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "MISSING": 0.0}


def calculate_deterministic_score(
    requirement_evaluation: Mapping[str, Any],
    *,
    max_score: float = 25.0,
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

    raw_score = float(max_score) * sum(
        _CREDIT[row["status"]] for row in requirements
    ) / len(requirements)
    ceilings = [
        float(row["recommended_ceiling"])
        for row in requirement_evaluation.get("findings", [])
        if row.get("classification") in {"fatal", "core_error"}
        and isinstance(row.get("recommended_ceiling"), (int, float))
    ]
    total = min([raw_score, *ceilings]) if ceilings else raw_score
    total = round(total, 2)
    fatal = bool(requirement_evaluation.get("fatal_or_core_error"))
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
        "applied_ceiling": min(ceilings) if ceilings else None,
        "verdict": verdict,
        "external_llm_required_for_verdict": False,
        "official_pass_met": bool(not fatal and total >= max_score * 0.6),
        "high_score_met": bool(not fatal and total >= max_score * 0.8),
    }
