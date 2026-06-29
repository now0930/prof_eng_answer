"""Weak score adjustment from question_type_coverage.

Default mode is warn. In warn mode this module only records a recommended
penalty. In strict mode it applies a small total_score adjustment.

This is intentionally weak and conservative:
- max total penalty: 0.75 / 25
- max C-related penalty: 0.45
- max D-related penalty: 0.30
"""

from __future__ import annotations

import os
from typing import Any


DEFAULT_MODE = "warn"
MAX_TOTAL_PENALTY = 0.75
MAX_C_PENALTY = 0.45
MAX_D_PENALTY = 0.30


def _walk_find_question_type_coverage(obj: Any) -> dict[str, Any] | None:
    if isinstance(obj, dict):
        coverage = obj.get("question_type_coverage")
        if isinstance(coverage, dict):
            return coverage

        for value in obj.values():
            found = _walk_find_question_type_coverage(value)
            if found:
                return found

    elif isinstance(obj, list):
        for item in obj:
            found = _walk_find_question_type_coverage(item)
            if found:
                return found

    return None


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _to_float(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except Exception:
        return default


def _get_mode() -> str:
    mode = os.getenv("QUESTION_TYPE_COVERAGE_SCORE_MODE", DEFAULT_MODE)
    mode = str(mode).strip().lower()

    if mode not in {"warn", "strict", "off"}:
        return DEFAULT_MODE

    return mode


def _focus_missing_count(coverage: dict[str, Any], key: str) -> int:
    focus = coverage.get(key)
    if not isinstance(focus, dict):
        return 0

    return len([x for x in _as_list(focus.get("missing")) if x])


def _sub_criteria_penalty(coverage: dict[str, Any]) -> tuple[float, dict[str, int]]:
    rows = _as_list(coverage.get("sub_criteria_coverage"))

    counts = {
        "present": 0,
        "partial": 0,
        "missing": 0,
        "unknown": 0,
        "total": 0,
    }

    penalty = 0.0

    for row in rows:
        if not isinstance(row, dict):
            continue

        status = str(row.get("status", "")).strip().lower()
        counts["total"] += 1

        if status == "present":
            counts["present"] += 1
        elif status == "partial":
            counts["partial"] += 1
            penalty += 0.05
        elif status == "missing":
            counts["missing"] += 1
            penalty += 0.12
        else:
            counts["unknown"] += 1
            penalty += 0.03

    return penalty, counts


def evaluate_question_type_coverage_score_adjustment(
    grade: dict[str, Any],
) -> dict[str, Any]:
    """Return a weak score adjustment decision.

    Does not mutate grade.
    """
    mode = _get_mode()
    score = _to_float(grade.get("total_score"), None)
    coverage = _walk_find_question_type_coverage(grade)

    decision: dict[str, Any] = {
        "mode": mode,
        "applied": False,
        "reason": "",
        "question_type": None,
        "name_ko": None,
        "original_score": score,
        "recommended_penalty": 0.0,
        "adjusted_score": score,
        "max_total_penalty": MAX_TOTAL_PENALTY,
        "suggested_layer_penalties": {
            "C": 0.0,
            "D": 0.0,
        },
        "coverage_counts": {
            "present": 0,
            "partial": 0,
            "missing": 0,
            "unknown": 0,
            "total": 0,
        },
    }

    if mode == "off":
        decision["reason"] = "QUESTION_TYPE_COVERAGE_SCORE_MODE=off 이므로 보정하지 않습니다."
        return decision

    if score is None:
        decision["reason"] = "total_score가 없어 점수 보정을 계산하지 않습니다."
        return decision

    if not isinstance(coverage, dict):
        decision["reason"] = "question_type_coverage가 없어 점수 보정을 계산하지 않습니다."
        return decision

    question_type = coverage.get("question_type")
    name_ko = coverage.get("name_ko")
    overall = str(coverage.get("overall_coverage", "")).strip().lower()

    decision["question_type"] = question_type
    decision["name_ko"] = name_ko
    decision["overall_coverage"] = overall or None

    sub_penalty, counts = _sub_criteria_penalty(coverage)
    decision["coverage_counts"] = counts

    coverage_source = str(coverage.get("coverage_source", "")).strip().lower()
    if overall in {"unknown", "not_evaluated"} or coverage_source.startswith("fallback"):
        decision["recommended_penalty"] = 0.0
        decision["adjusted_score"] = score
        decision["suggested_layer_penalties"] = {
            "C": 0.0,
            "D": 0.0,
        }
        decision["reason"] = (
            "question_type_coverage가 fallback/unknown 상태이므로 "
            "점수 보정 후보를 계산하지 않습니다."
        )
        return decision

    c_missing_count = _focus_missing_count(coverage, "c_fact_focus_coverage")
    d_missing_count = _focus_missing_count(coverage, "d_field_judgement_focus_coverage")

    c_penalty = min(MAX_C_PENALTY, sub_penalty * 0.55 + c_missing_count * 0.06)
    d_penalty = min(MAX_D_PENALTY, sub_penalty * 0.45 + d_missing_count * 0.06)

    # overall_coverage가 weak/poor이면 최소 보수성만 확보한다.
    if overall == "weak":
        c_penalty = max(c_penalty, 0.20)
        d_penalty = max(d_penalty, 0.12)
    elif overall == "poor":
        c_penalty = max(c_penalty, 0.30)
        d_penalty = max(d_penalty, 0.20)

    total_penalty = min(MAX_TOTAL_PENALTY, c_penalty + d_penalty)
    total_penalty = round(total_penalty, 2)

    adjusted_score = max(0.0, round(score - total_penalty, 2))

    decision["coverage_counts"] = counts
    decision["suggested_layer_penalties"] = {
        "C": round(min(c_penalty, total_penalty), 2),
        "D": round(max(0.0, total_penalty - min(c_penalty, total_penalty)), 2),
    }
    decision["recommended_penalty"] = total_penalty
    decision["adjusted_score"] = adjusted_score

    if total_penalty <= 0:
        decision["reason"] = "question_type 세부 요구 충족도가 충분하여 점수 보정 후보가 없습니다."
    else:
        decision["reason"] = (
            f"{name_ko or question_type} 세부 요구 충족도가 부족하여 "
            f"C/D항목 기준 약한 보정 후보 {total_penalty:g}점을 계산했습니다."
        )

    return decision


def apply_question_type_coverage_score_adjustment(
    grade: dict[str, Any],
) -> dict[str, Any]:
    """Attach and optionally apply weak score adjustment.

    warn mode: attach decision only.
    strict mode: subtract recommended_penalty from total_score.
    """
    if not isinstance(grade, dict):
        return grade

    decision = evaluate_question_type_coverage_score_adjustment(grade)
    grade["question_type_coverage_score_adjustment"] = decision

    if (
        decision.get("mode") == "strict"
        and decision.get("recommended_penalty", 0) > 0
        and decision.get("adjusted_score") is not None
    ):
        old_score = _to_float(grade.get("total_score"), None)

        if old_score is not None:
            grade["total_score"] = decision["adjusted_score"]
            decision["applied"] = True
            decision["original_score"] = old_score
            decision["adjusted_score"] = grade["total_score"]

            warnings = grade.get("strategy_warnings")
            if not isinstance(warnings, list):
                warnings = []
                grade["strategy_warnings"] = warnings

            msg = (
                "question_type coverage strict 보정 적용: "
                f"{old_score:g} -> {grade['total_score']:g} "
                f"(-{decision['recommended_penalty']:g})"
            )
            if msg not in warnings:
                warnings.append(msg)

    return grade
