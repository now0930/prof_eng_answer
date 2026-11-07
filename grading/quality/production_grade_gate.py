"""Fail-closed evidence checks for the current production grading path.

This validates an *existing* grade. It never assigns points, retries a provider,
replaces a fallback, or changes grading/fatal/Topic Pack policy.
"""

from __future__ import annotations

import math
from typing import Any, Mapping


class ProductionGradeFailure(RuntimeError):
    """A reviewed benchmark case did not finish the required production path."""


_LIMITS = {
    "A_structure": 3.0,
    "B_requirement_completeness": 6.0,
    "C_fact_correctness": 8.0,
    "D_engineering_judgment": 6.0,
    "E_linkage": 2.0,
}


def _fail(case_id: str, reason: str) -> None:
    # No raw learner answer, provider response or credentials in this message.
    raise ProductionGradeFailure(f"production grading incomplete: case={case_id}, reason={reason}")


def _score(value: Any, maximum: float, case_id: str, field: str) -> float:
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or not 0 <= value <= maximum):
        _fail(case_id, f"invalid_{field}")
    return float(value)


def require_production_grade_success(grade: Mapping[str, Any], case_id: str) -> None:
    """Require actual deterministic A/B/C and applied Argon D/E evidence.

    Validates the active production artifact. Provider failure, provider-not-
    configured, invalid proposal and deterministic fallback MUST fail this gate
    even if the runtime legitimately retained a low-score fallback grade.
    The original scoring algorithm itself is not changed.
    """
    if not isinstance(grade, Mapping):
        _fail(case_id, "missing_grade")
    if grade.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
        _fail(case_id, "not_deterministic_primary")
    if grade.get("llm_verdict_authority") != 0 or grade.get("external_llm_required_for_verdict") is not False:
        _fail(case_id, "invalid_verdict_authority")
    if grade.get("llm_score_authority") != "D_E_ONLY":
        _fail(case_id, "argon_de_not_authoritative")
    if grade.get("grading_engine") != "deterministic_abc_argon_de":
        _fail(case_id, "production_engine_mismatch")

    deterministic = grade.get("deterministic_score")
    if not isinstance(deterministic, Mapping) or deterministic.get("decision") != "SCORED":
        _fail(case_id, "deterministic_score_not_completed")
    if deterministic.get("marker") != "DETERMINISTIC_SCORE_ENGINE_V1":
        _fail(case_id, "deterministic_score_marker_mismatch")
    if deterministic.get("llm_verdict_authority") != 0:
        _fail(case_id, "deterministic_authority_mismatch")
    if (grade.get("resolution_review") or {}).get("required") is True:
        _fail(case_id, "unresolved_requirement")
    if (grade.get("resolution_review") or {}).get("score_status") != "final":
        _fail(case_id, "nonfinal_score_status")
    if not isinstance(grade.get("requirements"), list) or not grade["requirements"]:
        _fail(case_id, "missing_requirements")

    scores = deterministic.get("score_breakdown")
    if not isinstance(scores, Mapping) or set(scores) != set(_LIMITS):
        _fail(case_id, "incomplete_score_breakdown")
    for key, maximum in _LIMITS.items():
        _score(scores[key], maximum, case_id, key)
    total = _score(grade.get("total_score"), 25.0, case_id, "total_score")
    deterministic_total = _score(deterministic.get("total_score"), 25.0, case_id, "deterministic_total")
    if abs(total - deterministic_total) > 0.000001:
        _fail(case_id, "deterministic_total_mismatch")

    de = grade.get("qualitative_de_evaluation")
    if not isinstance(de, Mapping) or de.get("mode") != "argon" or de.get("provider") != "argon":
        _fail(case_id, "argon_mode_missing")
    if de.get("status") != "APPLIED":
        _fail(case_id, "argon_de_not_applied")
    if de.get("score_effect") != "replace_de" or deterministic.get("qualitative_de_score_effect") != "replace_de":
        _fail(case_id, "argon_de_score_effect_missing")
    if de.get("provider_calls") != 1:
        _fail(case_id, "argon_provider_call_missing")
    if not isinstance(de.get("request_hash"), str) or len(de["request_hash"]) != 64:
        _fail(case_id, "argon_request_evidence_missing")
    if not isinstance(de.get("input_hash"), str) or len(de["input_hash"]) != 64:
        _fail(case_id, "argon_input_evidence_missing")
    criteria = de.get("criteria")
    if (not isinstance(criteria, list) or len(criteria) != 5
            or {row.get("criterion_id") for row in criteria if isinstance(row, Mapping)}
            != {"D1", "D2", "D3", "E1", "E2"}):
        _fail(case_id, "argon_criteria_incomplete")
    proposed, effective = de.get("proposed_scores"), de.get("effective_scores")
    if not isinstance(proposed, Mapping) or not isinstance(effective, Mapping):
        _fail(case_id, "argon_score_evidence_missing")
    for key in ("D_engineering_judgment", "E_linkage"):
        _score(proposed.get(key), _LIMITS[key], case_id, f"proposed_{key}")
        value = _score(effective.get(key), _LIMITS[key], case_id, f"effective_{key}")
        if abs(value - scores[key]) > 0.000001:
            _fail(case_id, f"argon_{key}_score_mismatch")
