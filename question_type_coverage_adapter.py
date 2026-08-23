"""Reflect question_type_coverage in grade feedback.

This adapter does not change score. It only adds C/D feedback based on
semantic grader's question_type_coverage result.
"""

from __future__ import annotations

from typing import Any

from generic_grading_contract import (
    DemandAssessment,
    DemandState,
    demand_matrix_summary,
    normalize_demand_state,
)


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


_LEGACY_COVERAGE_STATUS_TO_DEMAND_STATE = {
    "present": DemandState.CORRECT,
    "correct": DemandState.CORRECT,
    "partial": DemandState.PARTIAL,
    "wrong": DemandState.WRONG,
    "incorrect": DemandState.WRONG,
    "contradicted": DemandState.WRONG,
    "missing": DemandState.MISSING,
    "absent": DemandState.MISSING,
}


def _coverage_demand_state(value: Any) -> DemandState:
    normalized = str(value or "").strip().lower()
    if normalized in _LEGACY_COVERAGE_STATUS_TO_DEMAND_STATE:
        return _LEGACY_COVERAGE_STATUS_TO_DEMAND_STATE[normalized]
    return normalize_demand_state(value)



def _criteria_counts(coverage: dict[str, Any]) -> dict[str, int]:
    rows = _as_list(coverage.get("sub_criteria_coverage"))
    counts = {
        "present": 0,
        "correct": 0,
        "partial": 0,
        "wrong": 0,
        "missing": 0,
        "total": 0,
    }

    for row in rows:
        if not isinstance(row, dict):
            continue

        state = _coverage_demand_state(
            row.get("demand_state")
            or row.get("status")
        )

        if state is DemandState.CORRECT:
            counts["present"] += 1
            counts["correct"] += 1
        elif state is DemandState.PARTIAL:
            counts["partial"] += 1
        elif state is DemandState.WRONG:
            counts["wrong"] += 1
        else:
            counts["missing"] += 1

        counts["total"] += 1

    return counts



def _criteria_details(
    coverage: dict[str, Any],
) -> dict[str, Any]:
    rows = _as_list(coverage.get("sub_criteria_coverage"))

    status_rows: list[dict[str, Any]] = []
    present: list[str] = []
    partial: list[str] = []
    wrong: list[str] = []
    missing: list[str] = []
    assessments: list[DemandAssessment] = []

    for row in rows:
        if not isinstance(row, dict):
            continue

        criterion = str(
            row.get("criterion")
            or row.get("demand_id")
            or ""
        ).strip()
        evidence = str(row.get("evidence") or "").strip()

        if not criterion:
            continue

        state = _coverage_demand_state(
            row.get("demand_state")
            or row.get("status")
        )
        mentioned_raw = row.get("mentioned")
        mentioned = (
            bool(mentioned_raw)
            if mentioned_raw is not None
            else state is not DemandState.MISSING
        )

        legacy_status = {
            DemandState.CORRECT: "present",
            DemandState.PARTIAL: "partial",
            DemandState.WRONG: "wrong",
            DemandState.MISSING: "missing",
        }[state]

        status_rows.append(
            {
                "criterion": criterion,
                "status": legacy_status,
                "demand_state": state.value,
                "mentioned": mentioned,
                "evidence": evidence,
            }
        )

        assessments.append(
            DemandAssessment(
                demand_id=criterion,
                status=state,
                mentioned=mentioned,
                evidence=evidence,
                rationale=str(
                    row.get("rationale")
                    or row.get("reason")
                    or ""
                ).strip(),
            )
        )

        if state is DemandState.CORRECT:
            present.append(criterion)
        elif state is DemandState.PARTIAL:
            partial.append(criterion)
        elif state is DemandState.WRONG:
            wrong.append(criterion)
        else:
            missing.append(criterion)

    matrix = demand_matrix_summary(assessments)

    return {
        "status_rows": status_rows,
        "present_criteria": present,
        "correct_criteria": list(present),
        "partial_criteria": partial,
        "wrong_criteria": wrong,
        "missing_criteria": missing,
        "present": len(present),
        "correct": len(present),
        "partial": len(partial),
        "wrong": len(wrong),
        "missing": len(missing),
        "weighted_score": matrix["correctness_credit"],
        "weighted_ratio": matrix["correctness_coverage_ratio"],
        "weighted_percent": matrix[
            "correctness_coverage_percent"
        ],
        "mention_coverage_ratio": matrix[
            "mention_coverage_ratio"
        ],
        "mention_coverage_percent": matrix[
            "mention_coverage_percent"
        ],
        "correctness_coverage_ratio": matrix[
            "correctness_coverage_ratio"
        ],
        "correctness_coverage_percent": matrix[
            "correctness_coverage_percent"
        ],
        "full_correct_coverage": matrix[
            "full_correct_coverage"
        ],
        "state_counts": matrix["state_counts"],
        "total": matrix["total"],
    }


def _missing_criteria_text(coverage: dict[str, Any], limit: int = 5) -> str:
    missing = _as_list(coverage.get("missing_sub_criteria"))

    if not missing:
        rows = _as_list(coverage.get("sub_criteria_coverage"))
        for row in rows:
            if not isinstance(row, dict):
                continue
            state = _coverage_demand_state(
                row.get("demand_state")
                or row.get("status")
            )
            if state in {
                DemandState.PARTIAL,
                DemandState.WRONG,
                DemandState.MISSING,
            }:
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
        "sub_criteria_correct": counts["correct"],
        "sub_criteria_partial": counts["partial"],
        "sub_criteria_wrong": counts["wrong"],
        "sub_criteria_missing": counts["missing"],
        "mention_coverage_ratio": details[
            "mention_coverage_ratio"
        ],
        "mention_coverage_percent": details[
            "mention_coverage_percent"
        ],
        "correctness_coverage_ratio": details[
            "correctness_coverage_ratio"
        ],
        "correctness_coverage_percent": details[
            "correctness_coverage_percent"
        ],
        "full_correct_coverage": details[
            "full_correct_coverage"
        ],
        "weighted_coverage_score": details["weighted_score"],
        "weighted_coverage_ratio": details["weighted_ratio"],
        "weighted_coverage_percent": details["weighted_percent"],
        "criteria_status_rows": details["status_rows"],
        "present_criteria": details["present_criteria"],
        "correct_criteria": details["correct_criteria"],
        "partial_criteria": details["partial_criteria"],
        "wrong_criteria": details["wrong_criteria"],
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

    root_qtype = grade.get("question_type")
    coverage_qtype = coverage.get("question_type")
    canonical_source = root_qtype or coverage_qtype

    if not canonical_source:
        grade["question_type_coverage"] = coverage
        return grade

    qtype = normalize_question_type(canonical_source)
    profile = get_question_type_profile(qtype)
    coverage_normalized = (
        normalize_question_type(coverage_qtype)
        if coverage_qtype
        else None
    )
    type_mismatch = bool(
        root_qtype
        and coverage_normalized
        and coverage_normalized != qtype
    )

    coverage = dict(coverage)

    if type_mismatch:
        # Coverage built for a stale semantic lens cannot replace the
        # question-only canonical type. Explicit requirement evidence is
        # topic-neutral and remains preserved.
        resolved_name = profile.get("name_ko")
        coverage["question_type"] = qtype
        coverage["name_ko"] = resolved_name
        coverage["overall_coverage"] = "unknown"
        coverage["coverage_source"] = (
            "question_only_type_owner_mismatch_guard"
        )
        coverage["sub_criteria_coverage"] = []
        coverage["missing_sub_criteria"] = []
        coverage["partial_sub_criteria"] = []
        coverage["c_fact_focus_coverage"] = {
            "covered": [],
            "missing": [],
        }
        coverage["d_field_judgement_focus_coverage"] = {
            "covered": [],
            "missing": [],
        }
        coverage["scoring_hint"] = (
            "semantic question_type coverage가 question-only "
            "deterministic router와 불일치하여 유형별 coverage를 "
            "점수 및 충족 판정에서 제외했습니다."
        )
        coverage["question_type_owner_reconciliation"] = {
            "canonical_owner": (
                "question_only_deterministic_router"
            ),
            "canonical_question_type": qtype,
            "discarded_coverage_question_type": (
                coverage_normalized
            ),
            "type_specific_coverage_invalidated": True,
            "explicit_requirement_coverage_preserved": (
                isinstance(
                    coverage.get(
                        "explicit_requirement_coverage"
                    ),
                    dict,
                )
            ),
        }

        summary = grade.get(
            "question_type_coverage_summary"
        )
        if not isinstance(summary, dict):
            summary = {}
        summary.update(
            {
                "question_type": qtype,
                "name_ko": resolved_name,
                "overall_coverage": "unknown",
                "sub_criteria_total": 0,
                "sub_criteria_present": 0,
                "sub_criteria_correct": 0,
                "sub_criteria_partial": 0,
                "sub_criteria_wrong": 0,
                "sub_criteria_incorrect": 0,
                "sub_criteria_missing": 0,
                "mention_coverage_ratio": None,
                "mention_coverage_percent": None,
                "correctness_coverage_ratio": None,
                "correctness_coverage_percent": None,
                "full_correct_coverage": False,
                "weighted_coverage_score": 0.0,
                "weighted_coverage_ratio": None,
                "weighted_coverage_percent": None,
                "criteria_status_rows": [],
                "present_criteria": [],
                "correct_criteria": [],
                "partial_criteria": [],
                "wrong_criteria": [],
                "incorrect_criteria": [],
                "missing_criteria": [],
            }
        )
        grade[
            "question_type_coverage_summary"
        ] = summary
    else:
        resolved_name = (
            coverage.get("name_ko")
            or profile.get("name_ko")
        )
        coverage["question_type"] = qtype
        coverage["name_ko"] = resolved_name

    grade["question_type_coverage"] = coverage
    grade["question_type"] = qtype
    grade["question_type_name"] = resolved_name

    # Preserve the locked question_type_v2 serialization contract.
    grade["question_type_v2"] = {
        "question_type": qtype,
        "name_ko": resolved_name,
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

# === qtype legacy GENERAL cleanup wrapper v2 EOF ===
# Remove old GENERAL(일반 설명형) phrases after question_type_v2 is resolved.
# This wrapper captures original functions via default arguments to avoid recursion
# if the file is patched more than once.
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

# INCORRECT_REQUIREMENT_STATUS_CONTRACT_V3
def _apply_incorrect_requirement_status_contract_v3(grade):
    if not isinstance(grade, dict):
        return grade

    qtype_v2 = grade.get("question_type_v2")

    if isinstance(qtype_v2, dict):
        root_type = str(
            grade.get("question_type") or ""
        ).strip()
        qtype_v2_type = str(
            qtype_v2.get("question_type") or ""
        ).strip()
        final_type = root_type or qtype_v2_type
        final_name = ""

        if final_type:
            final_type = normalize_question_type(
                final_type
            )
            profile = get_question_type_profile(
                final_type
            )
            final_name = str(
                grade.get("question_type_name")
                or (
                    qtype_v2.get("name_ko")
                    if qtype_v2_type == final_type
                    else None
                )
                or profile.get("name_ko")
                or ""
            ).strip()

            grade["question_type"] = final_type
            grade["question_type_name"] = final_name
            qtype_v2["question_type"] = final_type
            qtype_v2["name_ko"] = final_name
            qtype_v2["sub_criteria"] = (
                question_type_sub_criteria(
                    final_type
                )
            )
            qtype_v2["c_fact_focus"] = (
                question_type_c_focus(
                    final_type
                )
            )
            qtype_v2[
                "d_field_judgement_focus"
            ] = question_type_d_focus(
                final_type
            )

        coverage_summary = grade.get(
            "question_type_coverage_summary"
        )

        if isinstance(coverage_summary, dict):
            if final_type:
                coverage_summary["question_type"] = final_type

            if final_name:
                coverage_summary["name_ko"] = final_name

        legacy_eval = grade.get(
            "question_type_evaluation"
        )

        if isinstance(legacy_eval, dict):
            primary = legacy_eval.get(
                "primary_type"
            )

            if isinstance(primary, dict):
                old_type = str(
                    primary.get("id") or ""
                ).strip()
                old_name = str(
                    primary.get("name") or ""
                ).strip()

                if (
                    old_type
                    and old_name
                    and final_type
                    and final_name
                ):
                    old_label = (
                        f"{old_type}({old_name})"
                    )
                    new_label = (
                        f"{final_type}({final_name})"
                    )

                    for field in (
                        "summary",
                        "overall_summary",
                    ):
                        value = grade.get(field)

                        if isinstance(value, str):
                            grade[field] = value.replace(
                                old_label,
                                new_label,
                            )

    coverage = grade.get(
        "question_type_coverage"
    )

    if not isinstance(coverage, dict):
        return grade

    rows = coverage.get(
        "sub_criteria_coverage"
    )

    if not isinstance(rows, list):
        return grade

    normalised_rows = []

    aliases = {
        "wrong": "incorrect",
        "invalid": "incorrect",
        "factually_incorrect": "incorrect",
        "factually-incorrect": "incorrect",
    }

    for row in rows:
        if not isinstance(row, dict):
            continue

        criterion = str(
            row.get("criterion")
            or row.get("requirement")
            or ""
        ).strip()

        status = str(
            row.get("status") or ""
        ).strip().lower()

        status = aliases.get(
            status,
            status,
        )

        if (
            not criterion
            or status
            not in {
                "present",
                "partial",
                "incorrect",
                "missing",
            }
        ):
            continue

        normalised = dict(row)
        normalised["criterion"] = criterion
        normalised["status"] = status
        normalised_rows.append(
            normalised
        )

    if not normalised_rows:
        return grade

    present = [
        row["criterion"]
        for row in normalised_rows
        if row["status"] == "present"
    ]

    partial = [
        row["criterion"]
        for row in normalised_rows
        if row["status"] == "partial"
    ]

    incorrect = [
        row["criterion"]
        for row in normalised_rows
        if row["status"] == "incorrect"
    ]

    missing = [
        row["criterion"]
        for row in normalised_rows
        if row["status"] == "missing"
    ]

    total = len(normalised_rows)
    weighted_score = (
        len(present)
        + 0.5 * len(partial)
    )
    weighted_ratio = (
        weighted_score / total
        if total
        else 0.0
    )

    summary = grade.get(
        "question_type_coverage_summary"
    )

    if not isinstance(summary, dict):
        summary = {}

    qtype_v2 = grade.get(
        "question_type_v2"
    )

    final_type = ""
    final_name = ""

    if isinstance(qtype_v2, dict):
        final_type = str(
            qtype_v2.get("question_type") or ""
        ).strip()
        final_name = str(
            qtype_v2.get("name_ko") or ""
        ).strip()

    summary.update(
        {
            "question_type": (
                final_type
                or coverage.get("question_type")
                or grade.get("question_type")
            ),
            "name_ko": (
                final_name
                or coverage.get("name_ko")
                or grade.get("question_type_name")
            ),
            "overall_coverage": coverage.get(
                "overall_coverage"
            ),
            "sub_criteria_total": total,
            "sub_criteria_present": len(present),
            "sub_criteria_partial": len(partial),
            "sub_criteria_incorrect": len(incorrect),
            "sub_criteria_missing": len(missing),
            "weighted_coverage_score": round(
                weighted_score,
                2,
            ),
            "weighted_coverage_ratio": round(
                weighted_ratio,
                4,
            ),
            "weighted_coverage_percent": round(
                weighted_ratio * 100.0,
                1,
            ),
            "partial_criteria": partial,
            "incorrect_criteria": incorrect,
            "missing_criteria": missing,
            "criteria_status_rows": [
                {
                    "criterion": row["criterion"],
                    "status": row["status"],
                    "evidence": str(
                        row.get("evidence") or ""
                    ).strip(),
                }
                for row in normalised_rows
            ],
        }
    )

    grade[
        "question_type_coverage_summary"
    ] = summary

    return grade


_ORIGINAL_ATTACH_QTYPE_COVERAGE_INCORRECT_V3 = (
    attach_question_type_coverage_feedback
)


def attach_question_type_coverage_feedback(
    *args,
    **kwargs,
):
    result = (
        _ORIGINAL_ATTACH_QTYPE_COVERAGE_INCORRECT_V3(
            *args,
            **kwargs,
        )
    )

    return (
        _apply_incorrect_requirement_status_contract_v3(
            result
        )
    )


_ORIGINAL_ENSURE_QTYPE_COVERAGE_INCORRECT_V3 = (
    ensure_grade_question_type_coverage
)


def ensure_grade_question_type_coverage(
    *args,
    **kwargs,
):
    result = (
        _ORIGINAL_ENSURE_QTYPE_COVERAGE_INCORRECT_V3(
            *args,
            **kwargs,
        )
    )

    return (
        _apply_incorrect_requirement_status_contract_v3(
            result
        )
    )

# PLAN_A_DESIGN_CRITERIA_COVERAGE_CONSISTENCY_V1
#
# Final deterministic trust boundary for semantic coverage. A design-
# criteria question without an explicit numeric demand must not retain a
# calculation_or_interpretation=missing contradiction when formula/model
# evidence and result or field interpretation are already non-missing.
import re as _plan_a_re


_PLAN_A_EXPLICIT_NUMERIC_DEMAND_RE_V1 = _plan_a_re.compile(
    r"("
    r"계산\s*하시오|계산하시오|"
    r"산정\s*하시오|산정하시오|"
    r"구\s*하시오|구하시오|"
    r"수치(?:를|값을)?\s*(?:계산|산정|도출)|"
    r"계산\s*결과"
    r")",
    _plan_a_re.IGNORECASE,
)

_PLAN_A_DESIGN_CRITERIA_DEMAND_RE_V1 = _plan_a_re.compile(
    r"("
    r"설계\s*기준(?:을)?\s*(?:제시|설명)|"
    r"선정\s*기준(?:을)?\s*(?:제시|설명)"
    r")",
    _plan_a_re.IGNORECASE,
)

_PLAN_A_NON_MISSING_STATUSES_V1 = {
    "present",
    "partial",
}


def _plan_a_question_text_v1(
    grade,
    args,
    kwargs,
):
    explicit = kwargs.get("question_text")

    if isinstance(explicit, str) and explicit.strip():
        return explicit

    if isinstance(grade, dict):
        for key in (
            "question_text",
            "question",
            "problem_text",
            "prompt",
        ):
            value = grade.get(key)

            if isinstance(value, str) and value.strip():
                return value

    for value in args:
        if isinstance(value, str) and value.strip():
            return value

    return ""


def _plan_a_coverage_blocks_v1(value):
    seen = set()
    stack = [value]

    while stack:
        current = stack.pop()
        current_id = id(current)

        if current_id in seen:
            continue

        seen.add(current_id)

        if isinstance(current, dict):
            rows = current.get("sub_criteria_coverage")

            if (
                isinstance(rows, list)
                and any(
                    isinstance(row, dict)
                    and row.get("criterion")
                    == "calculation_or_interpretation"
                    for row in rows
                )
            ):
                yield current

            stack.extend(current.values())

        elif isinstance(current, list):
            stack.extend(current)


def _plan_a_repair_design_criteria_coverage_v1(
    grade,
    question_text,
):
    if not isinstance(grade, dict):
        return grade

    question = str(question_text or "")

    if _PLAN_A_EXPLICIT_NUMERIC_DEMAND_RE_V1.search(
        question
    ):
        return grade

    if not _PLAN_A_DESIGN_CRITERIA_DEMAND_RE_V1.search(
        question
    ):
        return grade

    repaired = False

    for coverage in _plan_a_coverage_blocks_v1(grade):
        rows = coverage.get("sub_criteria_coverage") or []
        by_name = {
            str(row.get("criterion")): row
            for row in rows
            if isinstance(row, dict)
        }

        target = by_name.get(
            "calculation_or_interpretation"
        )

        if not isinstance(target, dict):
            continue

        target_status = str(
            target.get("status") or ""
        ).strip().lower()

        if target_status != "missing":
            continue

        formula_status = str(
            (
                by_name.get("formula_model_variables")
                or {}
            ).get("status")
            or ""
        ).strip().lower()

        result_status = str(
            (
                by_name.get("result_meaning")
                or {}
            ).get("status")
            or ""
        ).strip().lower()

        field_status = str(
            (
                by_name.get("field_judgement")
                or {}
            ).get("status")
            or ""
        ).strip().lower()

        if (
            formula_status
            not in _PLAN_A_NON_MISSING_STATUSES_V1
        ):
            continue

        if (
            result_status
            not in _PLAN_A_NON_MISSING_STATUSES_V1
            and field_status
            not in _PLAN_A_NON_MISSING_STATUSES_V1
        ):
            continue

        target["status"] = "partial"
        target["evidence"] = (
            "관련 식·모델과 설계 방향은 제시했으나 "
            "계산 조건, 최악 조건 또는 전 범위 검증이 부족함"
        )
        target["impact"] = (
            "명시적 요구의 완전 누락이 아니라 C/D항목의 "
            "기술적 깊이 부족으로 평가"
        )

        coverage["missing_sub_criteria"] = [
            str(row.get("criterion"))
            for row in rows
            if (
                isinstance(row, dict)
                and str(
                    row.get("status") or ""
                ).strip().lower()
                == "missing"
                and row.get("criterion")
            )
        ]

        coverage["partial_sub_criteria"] = [
            str(row.get("criterion"))
            for row in rows
            if (
                isinstance(row, dict)
                and str(
                    row.get("status") or ""
                ).strip().lower()
                == "partial"
                and row.get("criterion")
            )
        ]

        repaired = True

    if repaired:
        grade = (
            _apply_incorrect_requirement_status_contract_v3(
                grade
            )
        )

    return grade


_ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_PLAN_A_V1 = (
    ensure_grade_question_type_coverage
)


def ensure_grade_question_type_coverage(
    *args,
    **kwargs,
):
    result = (
        _ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_PLAN_A_V1(
            *args,
            **kwargs,
        )
    )
    question_text = _plan_a_question_text_v1(
        result,
        args,
        kwargs,
    )

    return _plan_a_repair_design_criteria_coverage_v1(
        result,
        question_text,
    )


_ORIGINAL_ATTACH_QTYPE_COVERAGE_PLAN_A_V1 = (
    attach_question_type_coverage_feedback
)


# PLAN_A_ATTACH_QUESTION_TEXT_COMPATIBILITY_V1
def attach_question_type_coverage_feedback(
    *args,
    **kwargs,
):
    forwarded_kwargs = dict(kwargs)
    explicit_question_text = forwarded_kwargs.pop(
        "question_text",
        None,
    )

    result = (
        _ORIGINAL_ATTACH_QTYPE_COVERAGE_PLAN_A_V1(
            *args,
            **forwarded_kwargs,
        )
    )

    question_text = _plan_a_question_text_v1(
        result,
        args,
        {
            "question_text": explicit_question_text,
        },
    )

    return _plan_a_repair_design_criteria_coverage_v1(
        result,
        question_text,
    )

# === STAGE25G3G_FATAL_COVERAGE_CONSISTENCY_V1 ===
# Reclassify only coverage rows that semantically overlap fatal logic
# findings. This adapter remains non-scoring.
import re as _stage25g3g_re

_STAGE25G3G_PREVIOUS_ATTACH_QUESTION_TYPE_COVERAGE_FEEDBACK = (
    attach_question_type_coverage_feedback
)

_STAGE25G3G_TOKEN_PATTERN = _stage25g3g_re.compile(
    r"[A-Za-z][A-Za-z0-9]{1,}|[가-힣]{2,}"
)
_STAGE25G3G_STOP_TOKENS = {
    "and",
    "answer",
    "claim",
    "condition",
    "detected",
    "error",
    "fatal",
    "finding",
    "logic",
    "mapped",
    "mapping",
    "profile",
    "rule",
    "software",
    "test",
    "testing",
    "validation",
    "verification",
    "wrong",
    "검증",
    "답안",
    "오류",
    "조건",
    "항목",
}


def _stage25g3g_string_values(value: Any) -> list[str]:
    values: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, str):
            prepared = node.strip()
            if prepared:
                values.append(prepared)
            return
        if isinstance(node, dict):
            for key, child in node.items():
                key_text = str(key or "").strip()
                if key_text:
                    values.append(key_text)
                walk(child)
            return
        if isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return values


def _stage25g3g_tokens(value: Any) -> set[str]:
    tokens: set[str] = set()
    for raw in _stage25g3g_string_values(value):
        prepared = _stage25g3g_re.sub(
            r"[_/.:+\-]+",
            " ",
            raw,
        )
        for token in _STAGE25G3G_TOKEN_PATTERN.findall(
            prepared
        ):
            normalized = token.casefold()
            if normalized in _STAGE25G3G_STOP_TOKENS:
                continue
            if len(normalized) < 2:
                continue
            tokens.add(normalized)
    return tokens


def _stage25g3g_logic_evaluations(
    grade: dict[str, Any],
) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    seen: set[int] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            identity = id(node)
            if identity in seen:
                return
            seen.add(identity)

            findings = node.get("findings")
            if (
                isinstance(findings, list)
                and (
                    "fatal_error_detected" in node
                    or "score_policy" in node
                    or "deduction_elements" in node
                )
            ):
                found.append(node)

            for key, child in node.items():
                if key in {
                    "logic_check_evaluation",
                    "logic_check_result",
                    "secondary_logic_evaluations",
                    "selected_secondary_evaluations",
                }:
                    walk(child)
                elif isinstance(child, (dict, list)):
                    walk(child)
            return

        if isinstance(node, list):
            for child in node:
                walk(child)

    for key in (
        "logic_check_evaluation",
        "logic_check_result",
    ):
        walk(grade.get(key))

    return found


def _stage25g3g_fatal_findings(
    grade: dict[str, Any],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for evaluation in _stage25g3g_logic_evaluations(
        grade
    ):
        raw_findings = evaluation.get("findings")
        if not isinstance(raw_findings, list):
            continue
        for row in raw_findings:
            if not isinstance(row, dict):
                continue
            if str(
                row.get("severity") or ""
            ).strip().lower() != "fatal":
                continue

            finding_id = str(
                row.get("id") or ""
            ).strip()
            identity = (
                finding_id
                or repr(sorted(row.items()))
            )
            if identity in seen_ids:
                continue
            seen_ids.add(identity)
            findings.append(row)

    return findings


def _stage25g3g_row_text(
    row: dict[str, Any],
) -> str:
    values = []
    for key in (
        "criterion",
        "demand_id",
        "evidence",
        "reason",
        "rationale",
        "requirement_text",
        "description",
        "label",
        "name",
    ):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
    return " ".join(values)


# === STAGE25G3G1_FATAL_COVERAGE_PRECISION_V1 ===
_STAGE25G3G1_GENERIC_RELATION_TOKENS = {
    "answer",
    "claim",
    "condition",
    "error",
    "fatal",
    "finding",
    "integrity",
    "integration",
    "unit",
    "logic",
    "mapping",
    "model",
    "profile",
    "rule",
    "safety",
    "sil",
    "software",
    "stage",
    "system",
    "test",
    "testing",
    "validation",
    "verification",
    "vmodel",
    "wrong",
}


def _stage25g3g1_normalize_anchor(
    value: Any,
) -> str:
    return " ".join(
        str(value or "")
        .replace("_", " ")
        .replace("-", " ")
        .replace("/", " ")
        .split()
    ).casefold()


def _stage25g3g1_finding_direct_anchors(
    finding: dict[str, Any],
) -> list[str]:
    anchors: list[str] = []

    def add(value: Any) -> None:
        prepared = (
            _stage25g3g1_normalize_anchor(
                value
            )
        )
        if not prepared:
            return
        if prepared in (
            _STAGE25G3G1_GENERIC_RELATION_TOKENS
        ):
            return
        if prepared not in anchors:
            anchors.append(prepared)

    for key in (
        "coverage_anchor_terms",
        "anchor_terms",
        "evidence_terms",
    ):
        raw = finding.get(key)
        if isinstance(raw, list):
            for value in raw:
                add(value)
        elif isinstance(raw, str):
            add(raw)

    finding_id = str(
        finding.get("id") or ""
    ).strip().casefold()
    if finding_id:
        relation = finding_id
        if "_fatal_" in relation:
            relation = relation.split(
                "_fatal_",
                1,
            )[1]

        relation_sides = []
        for separator in (
            "_is_",
            "_mapped_to_",
            "_maps_to_",
            "_as_",
            "_means_",
            "_to_",
        ):
            if separator in relation:
                left, right = relation.split(
                    separator,
                    1,
                )
                relation_sides.extend(
                    [left, right]
                )
                break
        if not relation_sides:
            relation_sides.append(relation)

        for side in relation_sides:
            raw_tokens = [
                token
                for token in side.split("_")
                if token
                and not token.startswith("sw")
                and not token.isdigit()
            ]
            significant_tokens = [
                token
                for token in raw_tokens
                if token
                not in (
                    _STAGE25G3G1_GENERIC_RELATION_TOKENS
                )
            ]
            if not significant_tokens:
                continue

            if len(raw_tokens) >= 2:
                # Preserve the complete multi-token technical relation,
                # even when one component such as "integrity" is generic.
                # Examples:
                #   random_hardware_integrity
                # Reject generic stage relations because they have no
                # significant token after filtering:
                #   software_test, integration_test
                add(" ".join(raw_tokens))
            elif (
                len(significant_tokens) == 1
                and len(significant_tokens[0]) >= 3
                and significant_tokens[0]
                not in {
                    "random",
                    "hardware",
                }
            ):
                add(significant_tokens[0])

    # Do not scan every string nested in the finding for acronyms.
    # Shared profile/context text may contain another relation's anchor.
    # Only explicit anchor fields and the finding-ID relation axis are used.
    return sorted(
        anchors,
        key=lambda value: (
            -len(value.split()),
            -len(value),
            value,
        ),
    )


def _stage25g3g1_anchor_in_text(
    anchor: str,
    row_text: str,
) -> bool:
    prepared_anchor = (
        _stage25g3g1_normalize_anchor(
            anchor
        )
    )
    prepared_row = (
        _stage25g3g1_normalize_anchor(
            row_text
        )
    )
    if not prepared_anchor or not prepared_row:
        return False

    if prepared_anchor.isascii():
        pattern = (
            r"(?<![a-z0-9])"
            + _stage25g3g_re.escape(
                prepared_anchor
            ).replace(
                r"\ ",
                r"\s+",
            )
            + r"(?![a-z0-9])"
        )
        return bool(
            _stage25g3g_re.search(
                pattern,
                prepared_row,
            )
        )

    return prepared_anchor in prepared_row


def _stage25g3g_row_match(
    row: dict[str, Any],
    finding: dict[str, Any],
    token_frequency: dict[str, int],
) -> tuple[bool, list[str]]:
    del token_frequency

    row_text = _stage25g3g_row_text(row)
    anchors = (
        _stage25g3g1_finding_direct_anchors(
            finding
        )
    )
    matched = [
        anchor
        for anchor in anchors
        if _stage25g3g1_anchor_in_text(
            anchor,
            row_text,
        )
    ]
    return bool(matched), matched


def _stage25g3g1_unique_reclassification_keys(
    grade: dict[str, Any],
) -> set[tuple[str, tuple[str, ...]]]:
    keys: set[
        tuple[str, tuple[str, ...]]
    ] = set()

    for container_name, row_key in (
        (
            "question_type_coverage",
            "sub_criteria_coverage",
        ),
        (
            "question_type_coverage_summary",
            "criteria_status_rows",
        ),
    ):
        container = grade.get(
            container_name
        )
        if not isinstance(container, dict):
            continue
        rows = container.get(row_key)
        if not isinstance(rows, list):
            continue

        for row in rows:
            if not isinstance(row, dict):
                continue
            metadata = row.get(
                "fatal_logic_reclassification"
            )
            if not isinstance(metadata, dict):
                continue

            criterion = str(
                row.get("criterion")
                or row.get("demand_id")
                or row.get(
                    "requirement_text"
                )
                or ""
            ).strip().casefold()
            finding_ids = tuple(
                sorted(
                    str(value)
                    for value in (
                        metadata.get(
                            "finding_ids"
                        )
                        or []
                    )
                    if str(value).strip()
                )
            )
            if criterion and finding_ids:
                keys.add(
                    (
                        criterion,
                        finding_ids,
                    )
                )

    return keys


def _stage25g3g1_physical_reclassification_count(
    grade: dict[str, Any],
) -> int:
    count = 0
    for container_name, row_key in (
        (
            "question_type_coverage",
            "sub_criteria_coverage",
        ),
        (
            "question_type_coverage_summary",
            "criteria_status_rows",
        ),
    ):
        container = grade.get(
            container_name
        )
        if not isinstance(container, dict):
            continue
        rows = container.get(row_key)
        if not isinstance(rows, list):
            continue
        count += sum(
            isinstance(row, dict)
            and isinstance(
                row.get(
                    "fatal_logic_reclassification"
                ),
                dict,
            )
            for row in rows
        )
    return count



def _stage25g3g_refresh_summary_counts(
    coverage: dict[str, Any],
) -> None:
    rows = coverage.get("criteria_status_rows")
    if not isinstance(rows, list):
        return

    counts = {
        "present": 0,
        "correct": 0,
        "partial": 0,
        "wrong": 0,
        "missing": 0,
    }
    total = 0
    correctness_credit = 0.0
    mentioned_count = 0

    for row in rows:
        if not isinstance(row, dict):
            continue
        status = str(
            row.get("status")
            or row.get("demand_state")
            or ""
        ).strip().lower()
        if status in {"present", "correct"}:
            counts["present"] += 1
            counts["correct"] += 1
            correctness_credit += 1.0
            mentioned_count += 1
        elif status == "partial":
            counts["partial"] += 1
            correctness_credit += 0.5
            mentioned_count += 1
        elif status in {
            "wrong",
            "incorrect",
            "contradicted",
        }:
            counts["wrong"] += 1
            mentioned_count += 1
        else:
            counts["missing"] += 1
        total += 1

    coverage["sub_criteria_total"] = total
    coverage["sub_criteria_present"] = (
        counts["present"]
    )
    coverage["sub_criteria_correct"] = (
        counts["correct"]
    )
    coverage["sub_criteria_partial"] = (
        counts["partial"]
    )
    coverage["sub_criteria_wrong"] = (
        counts["wrong"]
    )
    coverage["sub_criteria_missing"] = (
        counts["missing"]
    )
    coverage["state_counts"] = dict(counts)

    if total > 0:
        correctness_ratio = (
            correctness_credit / total
        )
        mention_ratio = mentioned_count / total
    else:
        correctness_ratio = 0.0
        mention_ratio = 0.0

    coverage["weighted_coverage_score"] = round(
        correctness_credit,
        4,
    )
    coverage["weighted_coverage_ratio"] = round(
        correctness_ratio,
        6,
    )
    coverage["weighted_coverage_percent"] = round(
        correctness_ratio * 100.0,
        1,
    )
    coverage["correctness_coverage_ratio"] = round(
        correctness_ratio,
        6,
    )
    coverage[
        "correctness_coverage_percent"
    ] = round(
        correctness_ratio * 100.0,
        1,
    )
    coverage["mention_coverage_ratio"] = round(
        mention_ratio,
        6,
    )
    coverage["mention_coverage_percent"] = round(
        mention_ratio * 100.0,
        1,
    )
    coverage["full_correct_coverage"] = bool(
        total > 0
        and counts["correct"] == total
    )


def _stage25g3g_reconcile_coverage_dict(
    coverage: dict[str, Any],
    fatal_findings: list[dict[str, Any]],
) -> int:
    row_keys = (
        "sub_criteria_coverage",
        "criteria_status_rows",
        "requirements",
        "rows",
    )
    candidate_rows: list[dict[str, Any]] = []
    for key in row_keys:
        rows = coverage.get(key)
        if not isinstance(rows, list):
            continue
        candidate_rows.extend(
            row
            for row in rows
            if isinstance(row, dict)
        )

    if not candidate_rows or not fatal_findings:
        return 0

    token_frequency: dict[str, int] = {}
    for row in candidate_rows:
        for token in _stage25g3g_tokens(
            _stage25g3g_row_text(row)
        ):
            token_frequency[token] = (
                token_frequency.get(token, 0)
                + 1
            )

    changed = 0
    for row in candidate_rows:
        matched_ids: list[str] = []
        matched_tokens: list[str] = []

        for finding in fatal_findings:
            matched, tokens = _stage25g3g_row_match(
                row,
                finding,
                token_frequency,
            )
            if not matched:
                continue
            finding_id = str(
                finding.get("id") or ""
            ).strip()
            if (
                finding_id
                and finding_id not in matched_ids
            ):
                matched_ids.append(finding_id)
            for token in tokens:
                if token not in matched_tokens:
                    matched_tokens.append(token)

        if not matched_ids:
            continue

        current_status = str(
            row.get("status")
            or row.get("demand_state")
            or ""
        ).strip().lower()
        metadata = row.get(
            "fatal_logic_reclassification"
        )
        if not isinstance(metadata, dict):
            metadata = {}

        previous_ids = metadata.get("finding_ids")
        if not isinstance(previous_ids, list):
            previous_ids = []

        merged_ids = [
            str(value)
            for value in previous_ids
            if str(value).strip()
        ]
        for finding_id in matched_ids:
            if finding_id not in merged_ids:
                merged_ids.append(finding_id)

        if (
            current_status != "wrong"
            or set(previous_ids) != set(merged_ids)
        ):
            changed += 1

        row["status"] = "wrong"
        row["demand_state"] = "WRONG"
        row["mentioned"] = True
        row["fatal_logic_reclassification"] = {
            "version": (
                "stage25g3g_fatal_coverage_"
                "consistency_v1"
            ),
            "original_status": (
                metadata.get("original_status")
                or current_status
                or "unspecified"
            ),
            "finding_ids": merged_ids,
            "matched_tokens": sorted(
                set(matched_tokens)
            ),
            "score_effect": "none",
        }

        caution = (
            "구조화 검증에서 관련 핵심 이론 오답이 "
            "확인되어 WRONG으로 재분류됨"
        )
        evidence = str(
            row.get("evidence") or ""
        ).strip()
        if caution not in evidence:
            row["evidence"] = (
                evidence + " " + caution
            ).strip()

    _stage25g3g_refresh_summary_counts(
        coverage
    )
    return changed


def _stage25g3g_reconcile_fatal_coverage(
    grade: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(grade, dict):
        return grade

    fatal_findings = _stage25g3g_fatal_findings(
        grade
    )
    if not fatal_findings:
        return grade

    changed = 0
    visited: set[int] = set()

    def walk(node: Any) -> None:
        nonlocal changed
        if isinstance(node, dict):
            identity = id(node)
            if identity in visited:
                return
            visited.add(identity)

            if any(
                isinstance(node.get(key), list)
                for key in (
                    "sub_criteria_coverage",
                    "criteria_status_rows",
                    "requirements",
                    "rows",
                )
            ):
                changed += (
                    _stage25g3g_reconcile_coverage_dict(
                        node,
                        fatal_findings,
                    )
                )

            for child in node.values():
                if isinstance(child, (dict, list)):
                    walk(child)
            return

        if isinstance(node, list):
            for child in node:
                walk(child)

    for key in (
        "question_type_coverage",
        "question_type_coverage_summary",
    ):
        walk(grade.get(key))

    grade["fatal_coverage_consistency"] = {
        "version": (
            "stage25g3g_fatal_coverage_"
            "consistency_v1"
        ),
        "fatal_finding_ids": [
            str(row.get("id") or "")
            for row in fatal_findings
            if str(row.get("id") or "").strip()
        ],
        "reclassified_row_count": len(
            _stage25g3g1_unique_reclassification_keys(
                grade
            )
        ),
        "reclassified_physical_row_count": (
            _stage25g3g1_physical_reclassification_count(
                grade
            )
        ),
        "changed_row_count_this_pass": changed,
        "match_strategy": (
            "stage25g3g1_direct_relation_anchor_v1"
        ),
        "score_effect": "none",
    }
    return grade


def attach_question_type_coverage_feedback(
    *args: Any,
    **kwargs: Any,
) -> dict[str, Any]:
    grade = None
    if args and isinstance(args[0], dict):
        grade = args[0]
    elif isinstance(kwargs.get("grade"), dict):
        grade = kwargs.get("grade")

    if isinstance(grade, dict):
        _stage25g3g_reconcile_fatal_coverage(
            grade
        )

    result = (
        _STAGE25G3G_PREVIOUS_ATTACH_QUESTION_TYPE_COVERAGE_FEEDBACK(
            *args,
            **kwargs,
        )
    )
    output = (
        result
        if isinstance(result, dict)
        else grade
    )
    if isinstance(output, dict):
        _stage25g3g_reconcile_fatal_coverage(
            output
        )
    return result
