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


def _criteria_details(
    coverage: dict[str, Any],
) -> dict[str, Any]:
    rows = _as_list(coverage.get("sub_criteria_coverage"))

    status_rows: list[dict[str, str]] = []
    present: list[str] = []
    partial: list[str] = []
    missing: list[str] = []

    weighted_score = 0.0

    for row in rows:
        if not isinstance(row, dict):
            continue

        criterion = str(row.get("criterion") or "").strip()
        status = str(row.get("status") or "").strip().lower()
        evidence = str(row.get("evidence") or "").strip()

        if not criterion:
            continue

        if status not in {"present", "partial", "missing"}:
            status = "missing"

        status_rows.append({
            "criterion": criterion,
            "status": status,
            "evidence": evidence,
        })

        if status == "present":
            present.append(criterion)
            weighted_score += 1.0
        elif status == "partial":
            partial.append(criterion)
            weighted_score += 0.5
        else:
            missing.append(criterion)

    total = len(status_rows)

    if total:
        ratio = round(weighted_score / total, 4)
        percent = round(ratio * 100, 1)
    else:
        ratio = None
        percent = None

    return {
        "status_rows": status_rows,
        "present_criteria": present,
        "partial_criteria": partial,
        "missing_criteria": missing,
        "weighted_score": round(weighted_score, 2),
        "weighted_ratio": ratio,
        "weighted_percent": percent,
        "total": total,
    }


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
    details = _criteria_details(coverage)
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
        "weighted_coverage_score": details["weighted_score"],
        "weighted_coverage_ratio": details["weighted_ratio"],
        "weighted_coverage_percent": details["weighted_percent"],
        "criteria_status_rows": details["status_rows"],
        "present_criteria": details["present_criteria"],
        "partial_criteria": details["partial_criteria"],
        "missing_criteria": details["missing_criteria"],
        "missing_sub_criteria_text": missing_text,
        "c_fact_focus_missing_text": c_missing,
        "d_field_judgement_focus_missing_text": d_missing,
        "note": (
            "이 평가는 B항목 요구사항 완전성과 C항목 Fact 설명, "
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

def ensure_grade_question_type_coverage(
    grade: dict[str, Any],
    question_text: str | None = None,
) -> dict[str, Any]:
    """Ensure grade has question_type_coverage.

    If semantic grader coverage is missing after merge, create fallback coverage.
    This fallback is for display/checking and does not pretend Gemini/CLOVA
    actually evaluated every sub_criteria.
    """
    if not isinstance(grade, dict):
        return grade

    existing = _walk_find_question_type_coverage(grade)
    if isinstance(existing, dict):
        return grade

    try:
        from semantic_question_type_prompt import empty_question_type_coverage

        qtype_v2 = grade.get("question_type_v2")
        existing_question_type = None

        if isinstance(qtype_v2, dict):
            existing_question_type = qtype_v2.get("question_type")

        existing_question_type = (
            existing_question_type
            or grade.get("question_type")
            or grade.get("legacy_question_type")
        )

        coverage = empty_question_type_coverage(
            question_text=question_text,
            existing_question_type=existing_question_type,
        )

        coverage["overall_coverage"] = "unknown"
        coverage["coverage_source"] = "fallback_missing_grade_field"
        coverage["sub_criteria_coverage"] = []
        coverage["missing_sub_criteria"] = []
        coverage["c_fact_focus_coverage"] = {
            "covered": [],
            "missing": [],
        }
        coverage["d_field_judgement_focus_coverage"] = {
            "covered": [],
            "missing": [],
        }
        coverage["scoring_hint"] = (
            "semantic grader의 question_type_coverage가 결과에서 확인되지 않아 "
            "fallback coverage를 생성했습니다. 이 값은 점수 보정에 사용하지 않습니다."
        )

        grade["question_type_coverage"] = coverage
        return grade

    except Exception as exc:
        grade["question_type_coverage_error"] = f"fallback coverage generation failed: {exc}"
        return grade


# === qtype coverage root promotion wrapper v1 EOF ===
# Keep this near the end of the file. It promotes nested semantic coverage
# to grade root so grade.json remains self-contained and consistent.
try:
    from question_type_taxonomy import (
        get_question_type_profile,
        normalize_question_type,
        question_type_c_focus,
        question_type_d_focus,
        question_type_sub_criteria,
    )

    def _promote_question_type_coverage_to_root_v1(grade: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(grade, dict):
            return grade

        coverage = _walk_find_question_type_coverage(grade)
        if not isinstance(coverage, dict):
            return grade

        grade["question_type_coverage"] = coverage

        coverage_qtype = coverage.get("question_type")
        if coverage_qtype:
            qtype = normalize_question_type(coverage_qtype)
            profile = get_question_type_profile(qtype)

            grade["question_type"] = qtype
            grade["question_type_v2"] = {
                "question_type": qtype,
                "name_ko": coverage.get("name_ko") or profile.get("name_ko"),
                "sub_criteria": question_type_sub_criteria(qtype),
                "c_fact_focus": question_type_c_focus(qtype),
                "d_field_judgement_focus": question_type_d_focus(qtype),
                "note": (
                    "question_type_v2는 B항목 요구사항 완전성과 C항목 Fact 전개, "
                    "D항목 현장 판단을 보완하는 평가 lens입니다."
                ),
            }

        return grade


    _ORIGINAL_ATTACH_QTYPE_COVERAGE_FEEDBACK_PROMOTE_ROOT_V1 = attach_question_type_coverage_feedback

    def attach_question_type_coverage_feedback(grade: dict[str, Any]) -> dict[str, Any]:
        grade = _ORIGINAL_ATTACH_QTYPE_COVERAGE_FEEDBACK_PROMOTE_ROOT_V1(grade)
        return _promote_question_type_coverage_to_root_v1(grade)


    if "ensure_grade_question_type_coverage" in globals():
        _ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_PROMOTE_ROOT_V1 = ensure_grade_question_type_coverage

        def ensure_grade_question_type_coverage(
            grade: dict[str, Any],
            question_text: str | None = None,
        ) -> dict[str, Any]:
            grade = _ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_PROMOTE_ROOT_V1(
                grade,
                question_text=question_text,
            )
            return _promote_question_type_coverage_to_root_v1(grade)

except Exception:
    pass

# === qtype legacy GENERAL cleanup wrapper v2 EOF ===
# Remove old GENERAL(일반 설명형) phrases after question_type_v2 is resolved.
# This wrapper captures original functions via default arguments to avoid recursion
# if the file is patched more than once.
try:
    import re as _qtype_cleanup_re_v2

    def _cleanup_legacy_general_text_v2(grade):
        if not isinstance(grade, dict):
            return grade

        qtype = grade.get("question_type")
        qv2 = grade.get("question_type_v2") or {}

        if not isinstance(qv2, dict):
            qv2 = {}

        name_ko = qv2.get("name_ko") or ""
        c_focus = qv2.get("c_fact_focus") or []

        legacy_sentence_patterns = [
            r"\s*문제 유형은\s*GENERAL\(일반 설명형\)로 판단하고,\s*C항목은 해당 유형의 Fact 설명 렌즈로 평가했습니\s*다\.?",
            r"\s*문제 유형은\s*GENERAL\(일반 설명형\)로 판단했습니다\.?",
            r"\s*문제 유형은\s*GENERAL\(일반 설명형\)로 판단하고[^.]*평가했습니\s*다\.?",
        ]

        for key in ["summary", "overall_comment"]:
            value = grade.get(key)
            if not isinstance(value, str):
                continue

            text = value
            for pattern in legacy_sentence_patterns:
                text = _qtype_cleanup_re_v2.sub(pattern, "", text)

            text = _qtype_cleanup_re_v2.sub(r"\s{2,}", " ", text).strip()
            grade[key] = text

        replacement_c = None
        if qtype and name_ko and c_focus:
            replacement_c = (
                f"C항목 보완: {name_ko} 유형에서는 "
                f"{', '.join(c_focus)}를 문제 요구에 맞게 구조적으로 설명하도록 답안을 전개하세요."
            )

        for key in ["improvement_points", "weaknesses", "strategy_warnings"]:
            values = grade.get(key)
            if not isinstance(values, list):
                continue

            cleaned = []
            for item in values:
                if (
                    isinstance(item, str)
                    and "일반 설명형 유형에서는" in item
                    and "C항목 보완" in item
                    and replacement_c
                ):
                    cleaned.append(replacement_c)
                else:
                    cleaned.append(item)

            grade[key] = cleaned

        return grade


    if "_QTYPE_CLEAN_GENERAL_V2_INSTALLED" not in globals():
        _QTYPE_CLEAN_GENERAL_V2_INSTALLED = True

        _ORIGINAL_ATTACH_QTYPE_COVERAGE_FEEDBACK_CLEAN_GENERAL_V2 = attach_question_type_coverage_feedback

        def attach_question_type_coverage_feedback(
            grade,
            _orig=_ORIGINAL_ATTACH_QTYPE_COVERAGE_FEEDBACK_CLEAN_GENERAL_V2,
        ):
            grade = _orig(grade)
            return _cleanup_legacy_general_text_v2(grade)


        if "ensure_grade_question_type_coverage" in globals():
            _ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_CLEAN_GENERAL_V2 = ensure_grade_question_type_coverage

            def ensure_grade_question_type_coverage(
                grade,
                question_text=None,
                _orig=_ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_CLEAN_GENERAL_V2,
            ):
                grade = _orig(
                    grade,
                    question_text=question_text,
                )
                return _cleanup_legacy_general_text_v2(grade)

except Exception:
    pass
