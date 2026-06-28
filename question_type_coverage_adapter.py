"""Reflect question_type_coverage in grade feedback.

This adapter does not change score. It only adds C/D feedback based on
semantic grader's question_type_coverage result.
"""

from __future__ import annotations

from typing import Any


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


def _append_unique(items: list[Any], value: Any) -> None:
    if value and value not in items:
        items.append(value)


def _criteria_counts(coverage: dict[str, Any]) -> dict[str, int]:
    rows = _as_list(coverage.get("sub_criteria_coverage"))
    counts = {"present": 0, "partial": 0, "missing": 0, "total": 0}

    for row in rows:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status", "")).strip().lower()
        if status in counts:
            counts[status] += 1
        counts["total"] += 1

    return counts


def _missing_criteria_text(coverage: dict[str, Any], limit: int = 5) -> str:
    missing = _as_list(coverage.get("missing_sub_criteria"))

    if not missing:
        rows = _as_list(coverage.get("sub_criteria_coverage"))
        for row in rows:
            if not isinstance(row, dict):
                continue
            status = str(row.get("status", "")).strip().lower()
            if status in {"missing", "partial"}:
                criterion = row.get("criterion")
                if criterion:
                    missing.append(criterion)

    missing = [str(x) for x in missing if x]
    if not missing:
        return ""

    shown = missing[:limit]
    suffix = ""
    if len(missing) > limit:
        suffix = f" 외 {len(missing) - limit}개"

    return ", ".join(shown) + suffix


def _focus_missing_text(focus: dict[str, Any], limit: int = 4) -> str:
    if not isinstance(focus, dict):
        return ""

    missing = [str(x) for x in _as_list(focus.get("missing")) if x]
    if not missing:
        return ""

    shown = missing[:limit]
    suffix = ""
    if len(missing) > limit:
        suffix = f" 외 {len(missing) - limit}개"

    return ", ".join(shown) + suffix


def attach_question_type_coverage_feedback(grade: dict[str, Any]) -> dict[str, Any]:
    """Attach readable C/D feedback from question_type_coverage.

    This function is intentionally non-scoring.
    """
    if not isinstance(grade, dict):
        return grade

    coverage = _walk_find_question_type_coverage(grade)
    if not isinstance(coverage, dict):
        return grade

    question_type = coverage.get("question_type") or grade.get("question_type")
    name_ko = coverage.get("name_ko")
    overall = str(coverage.get("overall_coverage", "")).strip().lower()

    counts = _criteria_counts(coverage)
    missing_text = _missing_criteria_text(coverage)

    c_missing = _focus_missing_text(
        coverage.get("c_fact_focus_coverage", {})
    )
    d_missing = _focus_missing_text(
        coverage.get("d_field_judgement_focus_coverage", {})
    )

    summary = {
        "question_type": question_type,
        "name_ko": name_ko,
        "overall_coverage": overall or None,
        "sub_criteria_total": counts["total"],
        "sub_criteria_present": counts["present"],
        "sub_criteria_partial": counts["partial"],
        "sub_criteria_missing": counts["missing"],
        "missing_sub_criteria_text": missing_text,
        "c_fact_focus_missing_text": c_missing,
        "d_field_judgement_focus_missing_text": d_missing,
        "note": (
            "이 평가는 점수를 직접 변경하지 않고, C항목 Fact 설명과 "
            "D항목 현장 판단 피드백을 보강합니다."
        ),
    }

    grade["question_type_coverage_summary"] = summary

    improvement_points = grade.get("improvement_points")
    if not isinstance(improvement_points, list):
        improvement_points = []
        grade["improvement_points"] = improvement_points

    strategy_warnings = grade.get("strategy_warnings")
    if not isinstance(strategy_warnings, list):
        strategy_warnings = []
        grade["strategy_warnings"] = strategy_warnings

    if overall in {"weak", "poor"}:
        _append_unique(
            improvement_points,
            (
                f"question_type 세부 요구 충족도가 낮습니다"
                f"({name_ko or question_type}). "
                "단답식 키워드보다 C항목 Fact 설명과 D항목 현장 판단을 보강해야 합니다."
            ),
        )

    if missing_text:
        _append_unique(
            improvement_points,
            f"누락 또는 부족한 세부 범주: {missing_text}",
        )

    if c_missing:
        _append_unique(
            improvement_points,
            f"C항목 Fact 기반 설명에서 부족한 관점: {c_missing}",
        )

    if d_missing:
        _append_unique(
            improvement_points,
            f"D항목 현장 적용·판단·제언에서 부족한 관점: {d_missing}",
        )

    scoring_hint = coverage.get("scoring_hint")
    if scoring_hint:
        _append_unique(
            strategy_warnings,
            f"question_type coverage 판단: {scoring_hint}",
        )

    # summary 문자열이 있는 경우 너무 길게 덮어쓰지 않고 뒤에 한 문장만 추가한다.
    old_summary = grade.get("summary")
    if isinstance(old_summary, str) and old_summary.strip():
        if "question_type 세부 요구" not in old_summary:
            if overall in {"weak", "poor"}:
                grade["summary"] = (
                    old_summary.rstrip()
                    + " question_type 세부 요구 충족도가 낮아 C/D항목 보완이 필요합니다."
                )
            elif overall in {"strong", "adequate"}:
                grade["summary"] = (
                    old_summary.rstrip()
                    + " question_type 세부 요구는 대체로 충족된 것으로 판단됩니다."
                )

    return grade
