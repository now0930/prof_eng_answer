"""Hard cap for explicitly requested but missing question requirements.

Important distinction
---------------------
- question_type sub_criteria:
  high-score development lens; not every item is explicitly requested.
- explicit_requirement_coverage:
  requirements directly extracted from the question text.

Only explicit, core, high-confidence missing requirements may trigger this
hard cap.
"""

from __future__ import annotations

from typing import Any


ONE_MISSING_B_CAP = 3.5
ONE_MISSING_TOTAL_CAP = 17.0

MULTI_MISSING_B_CAP = 2.0
MULTI_MISSING_TOTAL_CAP = 14.0

ALL_MISSING_B_CAP = 1.5
ALL_MISSING_TOTAL_CAP = 12.5


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _to_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _walk_find_question_type_coverage(
    obj: Any,
) -> dict[str, Any] | None:
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


def _explicit_requirement_block(
    coverage: dict[str, Any],
) -> dict[str, Any] | None:
    block = coverage.get("explicit_requirement_coverage")

    if isinstance(block, dict):
        return block

    return None


def _normalise_requirement_rows(
    block: dict[str, Any],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []

    for row in _as_list(block.get("requirements")):
        if not isinstance(row, dict):
            continue

        requirement = str(
            row.get("requirement") or row.get("criterion") or ""
        ).strip()

        status = str(row.get("status") or "").strip().lower()
        evidence = str(row.get("evidence") or "").strip()

        # Hard cap requires the semantic grader to explicitly certify that
        # this is a core requirement directly present in the question.
        is_core = row.get("is_core") is True

        if not requirement:
            continue

        if status not in {"present", "partial", "missing"}:
            continue

        result.append(
            {
                "requirement": requirement,
                "status": status,
                "evidence": evidence,
                "is_core": is_core,
            }
        )

    return result


def evaluate_explicit_requirement_hard_cap(
    grade: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate hard-cap eligibility without mutating the grade."""
    score = _to_float(grade.get("total_score"), None)
    coverage = _walk_find_question_type_coverage(grade)

    decision: dict[str, Any] = {
        "eligible": False,
        "triggered": False,
        "applied": False,
        "reason": "",
        "original_score": score,
        "adjusted_score": score,
        "b_cap": None,
        "total_cap": None,
        "explicit_requirement_total": 0,
        "present_core_count": 0,
        "partial_core_count": 0,
        "missing_core_count": 0,
        "present_requirements": [],
        "partial_requirements": [],
        "missing_requirements": [],
        "source": None,
        "extraction_confidence": None,
    }

    if not isinstance(coverage, dict):
        decision["reason"] = (
            "question_type_coverage가 없어 명시적 요구사항 cap을 "
            "판단하지 않습니다."
        )
        return decision

    coverage_source = str(
        coverage.get("coverage_source") or ""
    ).strip().lower()

    if coverage_source != "semantic_grader":
        decision["reason"] = (
            "검증된 semantic_grader coverage가 아니므로 "
            "명시적 요구사항 hard cap을 적용하지 않습니다."
        )
        return decision

    block = _explicit_requirement_block(coverage)

    if not isinstance(block, dict):
        decision["reason"] = (
            "명시적 요구사항 평가 결과가 없어 hard cap을 "
            "적용하지 않습니다."
        )
        return decision

    source = str(block.get("source") or "").strip().lower()
    confidence = str(
        block.get("extraction_confidence") or ""
    ).strip().lower()

    decision["source"] = source or None
    decision["extraction_confidence"] = confidence or None

    if source != "question_text":
        decision["reason"] = (
            "명시적 요구사항 source가 question_text가 아니므로 "
            "hard cap을 적용하지 않습니다."
        )
        return decision

    if confidence != "high":
        decision["reason"] = (
            "명시적 요구사항 추출 신뢰도가 high가 아니므로 "
            "hard cap을 적용하지 않습니다."
        )
        return decision

    rows = [
        row
        for row in _normalise_requirement_rows(block)
        if row["is_core"]
    ]

    if not rows:
        decision["reason"] = (
            "문제문에서 직접 확인된 핵심 요구사항이 없어 "
            "hard cap을 적용하지 않습니다."
        )
        return decision

    present = [
        row["requirement"]
        for row in rows
        if row["status"] == "present"
    ]
    partial = [
        row["requirement"]
        for row in rows
        if row["status"] == "partial"
    ]
    missing = [
        row["requirement"]
        for row in rows
        if row["status"] == "missing"
    ]

    decision.update(
        {
            "eligible": True,
            "explicit_requirement_total": len(rows),
            "present_core_count": len(present),
            "partial_core_count": len(partial),
            "missing_core_count": len(missing),
            "present_requirements": present,
            "partial_requirements": partial,
            "missing_requirements": missing,
        }
    )

    # partial은 기존 weak coverage 조정 대상으로만 보고 hard cap에는
    # 포함하지 않는다.
    if not missing:
        decision["reason"] = (
            "명시적 핵심 요구사항의 완전 누락이 없어 "
            "hard cap을 적용하지 않습니다."
        )
        return decision

    decision["triggered"] = True

    if len(missing) == len(rows):
        decision["b_cap"] = ALL_MISSING_B_CAP
        decision["total_cap"] = ALL_MISSING_TOTAL_CAP
        decision["rule"] = "all_core_requirements_missing"
    elif len(missing) >= 2:
        decision["b_cap"] = MULTI_MISSING_B_CAP
        decision["total_cap"] = MULTI_MISSING_TOTAL_CAP
        decision["rule"] = "multiple_core_requirements_missing"
    else:
        decision["b_cap"] = ONE_MISSING_B_CAP
        decision["total_cap"] = ONE_MISSING_TOTAL_CAP
        decision["rule"] = "one_core_requirement_missing"

    decision["reason"] = (
        f"문제문이 직접 요구한 핵심 항목 {len(missing)}개가 "
        f"완전히 누락되어 B 최대 {decision['b_cap']}/6, "
        f"총점 최대 {decision['total_cap']}/25 규칙을 적용합니다."
    )

    return decision


def _cap_b_rows(
    rows: Any,
    b_cap: float,
) -> float:
    """Cap B rows and return score reduction."""
    if not isinstance(rows, list):
        return 0.0

    reduction = 0.0

    for row in rows:
        if not isinstance(row, dict):
            continue

        layer_id = str(
            row.get("layer_id") or row.get("id") or ""
        ).strip().upper()

        item = str(row.get("item") or "").strip()

        if layer_id != "B" and not item.startswith("B."):
            continue

        before = _to_float(row.get("score"), None)

        if before is None or before <= b_cap:
            continue

        row.setdefault(
            "score_before_explicit_requirement_cap",
            round(before, 2),
        )
        row["score"] = round(b_cap, 2)
        row["explicit_requirement_cap_applied"] = True
        row["explicit_requirement_b_cap"] = round(b_cap, 2)

        reason = str(row.get("reason") or "").strip()
        cap_reason = (
            f"명시적 핵심 요구사항 누락으로 "
            f"B 점수를 {b_cap:g}/6으로 제한함."
        )

        if cap_reason not in reason:
            row["reason"] = (
                f"{reason} / {cap_reason}"
                if reason
                else cap_reason
            )

        reduction += before - b_cap

    return round(reduction, 2)


def _update_score_flags(grade: dict[str, Any]) -> None:
    total = _to_float(grade.get("total_score"), 0.0) or 0.0
    max_score = _to_float(grade.get("max_score"), 25.0) or 25.0

    targets = (
        ("official_pass_score", "official_pass_met", 0.60),
        ("practical_target_score", "practical_target_met", 0.70),
        ("high_score_target", "high_score_met", 0.80),
    )

    for score_key, met_key, ratio in targets:
        target = _to_float(
            grade.get(score_key),
            round(max_score * ratio, 2),
        )
        if target is None:
            continue

        grade[score_key] = target
        grade[met_key] = total >= target

    grade["average_target_met"] = grade.get(
        "practical_target_met",
        False,
    )


def _cap_rater_results(
    grade: dict[str, Any],
    b_cap: float,
) -> None:
    raters = grade.get("rater_results") or grade.get("raters")

    if not isinstance(raters, list):
        return

    for rater in raters:
        if not isinstance(rater, dict):
            continue

        reduction = 0.0

        for key in ("layer_scores", "breakdown"):
            reduction = max(
                reduction,
                _cap_b_rows(rater.get(key), b_cap),
            )

        if reduction <= 0:
            continue

        old_total = _to_float(rater.get("total_score"), None)

        if old_total is None:
            continue

        rater.setdefault(
            "total_score_before_explicit_requirement_cap",
            round(old_total, 2),
        )
        rater["total_score"] = round(
            max(0.0, old_total - reduction),
            2,
        )


def _apply_decision_caps(
    grade: dict[str, Any],
    decision: dict[str, Any],
    *,
    reconciliation_guard: bool = False,
) -> dict[str, Any]:
    if not decision.get("triggered"):
        return grade

    b_cap = _to_float(decision.get("b_cap"), None)
    total_cap = _to_float(decision.get("total_cap"), None)

    if b_cap is None or total_cap is None:
        return grade

    original_score = _to_float(grade.get("total_score"), None)

    if original_score is None:
        return grade

    primary_reduction = _cap_b_rows(
        grade.get("breakdown"),
        b_cap,
    )

    # Keep alternate breakdown structures consistent, but only the primary
    # breakdown reduction changes grade.total_score.
    for key in (
        "average_breakdown",
        "layer_breakdown",
        "scoring_breakdown",
        "final_breakdown",
    ):
        _cap_b_rows(grade.get(key), b_cap)

    _cap_rater_results(grade, b_cap)

    score_after_b = max(
        0.0,
        original_score - primary_reduction,
    )

    final_score = round(
        min(score_after_b, total_cap),
        2,
    )

    if final_score < original_score:
        grade.setdefault(
            "pre_explicit_requirement_cap_total_score",
            round(original_score, 2),
        )

        grade["total_score"] = final_score
        grade["final_total_score"] = final_score

        if final_score >= total_cap:
            grade["score_range"] = (
                f"{final_score:g}점 cap 적용"
            )
        else:
            lower = max(0.0, final_score - 0.5)
            upper = min(
                25.0,
                total_cap,
                final_score + 0.5,
            )
            grade["score_range"] = (
                f"{lower:.1f}~{upper:.1f}"
            )

    decision["applied"] = (
        primary_reduction > 0
        or final_score < original_score
    )
    decision["b_cap_applied"] = primary_reduction > 0
    decision["b_score_reduction"] = primary_reduction
    decision["original_score"] = round(original_score, 2)
    decision["adjusted_score"] = final_score

    if reconciliation_guard and final_score < original_score:
        decision["reapplied_after_reconciliation"] = True

    applied_caps = grade.get("applied_caps")

    if not isinstance(applied_caps, list):
        applied_caps = []
        grade["applied_caps"] = applied_caps

    cap_record = {
        "id": "explicit_requirement_missing_cap",
        "b_cap": b_cap,
        "total_cap": total_cap,
        "missing_requirements": decision.get(
            "missing_requirements",
            [],
        ),
        "reason": decision.get("reason"),
    }

    if cap_record not in applied_caps:
        applied_caps.append(cap_record)

    warnings = grade.get("strategy_warnings")

    if not isinstance(warnings, list):
        warnings = []
        grade["strategy_warnings"] = warnings

    warning = (
        f"명시적 요구사항 누락 cap: "
        f"B≤{b_cap:g}/6, 총점≤{total_cap:g}/25"
    )

    if warning not in warnings:
        warnings.append(warning)

    _update_score_flags(grade)

    return grade


def apply_explicit_requirement_hard_cap(
    grade: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate and apply explicit requirement hard cap."""
    if not isinstance(grade, dict):
        return grade

    decision = evaluate_explicit_requirement_hard_cap(grade)
    grade["explicit_requirement_cap_evaluation"] = decision

    return _apply_decision_caps(
        grade,
        decision,
        reconciliation_guard=False,
    )


def enforce_existing_explicit_requirement_cap(
    grade: dict[str, Any],
) -> dict[str, Any]:
    """Prevent later score reconciliation from exceeding an existing cap."""
    if not isinstance(grade, dict):
        return grade

    decision = grade.get("explicit_requirement_cap_evaluation")

    if not isinstance(decision, dict):
        return grade

    return _apply_decision_caps(
        grade,
        decision,
        reconciliation_guard=True,
    )
