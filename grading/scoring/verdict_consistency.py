"""Structured verdict and recommendation consistency policy."""

from __future__ import annotations

import copy
import re
from typing import Any

VERDICT_CONSISTENCY_SCHEMA_VERSION = "1.0"
VERDICT_CONSISTENCY_MARKER = "STRUCTURED_VERDICT_CONSISTENCY_V1"

_HARD_SEVERITIES = {"major", "fatal"}
_UNRESOLVED_REQUIREMENT_STATUSES = {
    "missing",
    "partial",
    "incorrect",
    "weak",
}

_FALSE_HARD_ERROR_REPLACEMENTS = (
    (
        "THEORY_CORE 핵심 이론 오류 cap 적용",
        "핵심 내용은 성립하나 상세 해석 보완 필요",
    ),
    (
        "THEORY_CORE 핵심 이론 오류",
        "핵심 내용은 성립하나 상세 해석 보완 필요",
    ),
    (
        "핵심 이론 오류가 확인되어 최종 cap이 적용되었습니다.",
        "확인된 근거에 따라 세부 해석 보완이 필요합니다.",
    ),
    (
        "핵심 이론 오류가 확인되었습니다.",
        "세부 해석과 근거 보완이 필요합니다.",
    ),
    (
        "핵심 이론 오류",
        "상세 해석 보완 사항",
    ),
    (
        "명백한 기술 오류",
        "기술 정확성 확인 사항",
    ),
    (
        "명백한 오류",
        "확인이 필요한 내용",
    ),
    (
        "fatal 오류",
        "핵심 보완 사항",
    ),
)


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any, limit: int = 420) -> str:
    text = str(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def _contract(
    payload: Any,
    key: str,
) -> dict[str, Any]:
    root = _dict(payload)
    value = root.get(key)

    if isinstance(value, dict):
        return value

    parsed = root.get("parsed")

    if isinstance(parsed, dict):
        value = parsed.get(key)

        if isinstance(value, dict):
            return value

    return {}


def has_structured_grading_contract(
    payload: Any,
) -> bool:
    return bool(
        _contract(
            payload,
            "general_evidence_contract",
        )
    )


def _logic_fatal(payload: Any) -> bool:
    root = _dict(payload)
    logic = _dict(
        root.get("logic_check_evaluation")
        or root.get("logic_check_result")
        or root.get("logic_check")
    )

    if logic.get("fatal") is True:
        return True

    if logic.get("fatal_error_detected") is True:
        return True

    for finding in _list(logic.get("findings")):
        if (
            isinstance(finding, dict)
            and _text(
                finding.get("severity")
            ).lower()
            == "fatal"
        ):
            return True

    return False


def _logic_findings(payload: Any) -> list[dict[str, Any]]:
    root = _dict(payload)
    logic = _dict(
        root.get("logic_check_evaluation")
        or root.get("logic_check_result")
        or root.get("logic_check")
    )
    return [
        row
        for row in _list(logic.get("findings"))
        if isinstance(row, dict)
    ]


def _defects(payload: Any) -> list[dict[str, Any]]:
    contract = _contract(
        payload,
        "general_evidence_contract",
    )
    return [
        row
        for row in _list(contract.get("defects"))
        if isinstance(row, dict)
    ]


def _requirements(payload: Any) -> list[dict[str, Any]]:
    coverage = _contract(
        payload,
        "question_type_coverage",
    )
    explicit = _dict(
        coverage.get(
            "explicit_requirement_coverage"
        )
    )
    return [
        row
        for row in _list(explicit.get("requirements"))
        if isinstance(row, dict)
    ]


def _question_requirement_labels(
    payload: Any,
) -> dict[str, str]:
    contract = _contract(
        payload,
        "question_demand_contract",
    )
    labels = {}

    for row in _list(contract.get("requirements")):
        if not isinstance(row, dict):
            continue

        requirement_id = _text(
            row.get("requirement_id"),
            180,
        )
        label = _text(
            row.get("demand_label")
            or row.get("requirement_text"),
            220,
        )

        if requirement_id and label:
            labels[requirement_id] = label

    return labels


def _defect_type(row: dict[str, Any]) -> str:
    value = _text(
        row.get("defect_type")
        or row.get("issue_type")
        or row.get("type"),
        80,
    ).lower()

    aliases = {
        "depth_gap": "core_depth_gap",
        "advanced_missing": "advanced_detail_missing",
        "formula_integrity_warning": "presentation_issue",
        "operator_missing": "presentation_issue",
    }
    return aliases.get(value, value)


def _severity(row: dict[str, Any]) -> str:
    return _text(
        row.get("severity"),
        60,
    ).lower()


def _explanation(row: dict[str, Any]) -> str:
    return _text(
        row.get("explanation")
        or row.get("reason")
        or row.get("description")
        or row.get("evidence_text")
        or row.get("evidence"),
        280,
    )


def _collect_base_signals(payload: Any) -> dict[str, Any]:
    defects = _defects(payload)
    correctness = []
    hard_correctness = []
    depth = []
    advanced = []
    presentation = []

    for row in defects:
        defect_type = _defect_type(row)

        if defect_type == "correctness_error":
            correctness.append(row)

            if (
                _severity(row) in _HARD_SEVERITIES
                or row.get(
                    "invalidates_core_conclusion"
                )
                is True
            ):
                hard_correctness.append(row)
        elif defect_type == "core_depth_gap":
            depth.append(row)
        elif defect_type == "advanced_detail_missing":
            advanced.append(row)
        elif defect_type == "presentation_issue":
            presentation.append(row)

    unresolved_requirements = []

    for row in _requirements(payload):
        status = _text(
            row.get("status"),
            80,
        ).lower()

        if status in _UNRESOLVED_REQUIREMENT_STATUSES:
            unresolved_requirements.append(row)

    return {
        "logic_fatal": _logic_fatal(payload),
        "correctness": correctness,
        "hard_correctness": hard_correctness,
        "depth": depth,
        "advanced": advanced,
        "presentation": presentation,
        "unresolved_requirements": unresolved_requirements,
    }


def _dedupe_text(
    values: list[str],
    limit: int = 4,
) -> list[str]:
    result = []
    seen = set()

    for value in values:
        text = _text(value, 320)

        if not text or text in seen:
            continue

        seen.add(text)
        result.append(text)

        if len(result) >= limit:
            break

    return result


def _sanitize_false_hard_error(
    value: Any,
    *,
    allow_hard_error: bool,
) -> Any:
    if allow_hard_error:
        return value

    if isinstance(value, str):
        result = value

        for source, target in _FALSE_HARD_ERROR_REPLACEMENTS:
            result = result.replace(source, target)

        return result

    if isinstance(value, list):
        return [
            _sanitize_false_hard_error(
                item,
                allow_hard_error=allow_hard_error,
            )
            for item in value
        ]

    if isinstance(value, tuple):
        return tuple(
            _sanitize_false_hard_error(
                item,
                allow_hard_error=allow_hard_error,
            )
            for item in value
        )

    if isinstance(value, dict):
        return {
            key: _sanitize_false_hard_error(
                item,
                allow_hard_error=allow_hard_error,
            )
            for key, item in value.items()
        }

    return value


def _requirement_improvements(
    payload: Any,
    rows: list[dict[str, Any]],
) -> list[str]:
    labels = _question_requirement_labels(payload)
    result = []

    for row in rows:
        status = _text(
            row.get("status"),
            80,
        ).lower()
        requirement_id = _text(
            row.get("requirement_id")
            or row.get("id"),
            180,
        )
        label = (
            labels.get(requirement_id)
            or _text(
                row.get("requirement")
                or row.get("requirement_text")
                or row.get("label"),
                220,
            )
            or "문제 요구"
        )

        status_text = {
            "missing": "누락된 요구를 직접 보완",
            "partial": "부분 충족 내용을 완결",
            "incorrect": "요구 대응 내용을 정확하게 수정",
            "weak": "요구 대응 근거를 강화",
        }.get(status, "요구 대응을 보완")

        result.append(
            f"{label}: {status_text}"
        )

    return result


def _base_structured_improvements(
    payload: Any,
    signals: dict[str, Any],
) -> list[str]:
    values = []

    for row in signals["correctness"]:
        explanation = _explanation(row)

        if explanation:
            values.append(
                f"기술 정확성: {explanation}"
            )

    for row in signals["depth"]:
        explanation = _explanation(row)

        if explanation:
            values.append(
                f"핵심 해석·설계 깊이: {explanation}"
            )

    for row in signals["advanced"]:
        explanation = _explanation(row)

        if explanation:
            values.append(
                f"고득점 세부사항: {explanation}"
            )

    for row in signals["presentation"]:
        explanation = _explanation(row)

        if explanation:
            values.append(
                f"수식·표현 무결성: {explanation}"
            )

    values.extend(
        _requirement_improvements(
            payload,
            signals["unresolved_requirements"],
        )
    )
    return _dedupe_text(values, limit=4)


def _base_structured_key_reasons(
    signals: dict[str, Any],
) -> list[str]:
    values = []

    for category in (
        "hard_correctness",
        "correctness",
        "depth",
        "presentation",
        "advanced",
    ):
        for row in signals[category]:
            explanation = _explanation(row)

            if explanation:
                values.append(explanation)

    return _dedupe_text(values, limit=4)


def _deterministic_verdict(
    signals: dict[str, Any],
) -> tuple[str, str]:
    if signals["logic_fatal"]:
        return "", ""

    if signals["hard_correctness"]:
        return (
            "검증된 핵심 기술 오류 보완 필요",
            (
                "구조화된 근거에서 중대 기술 오류가 확인되었습니다. "
                "해당 오류를 먼저 수정한 뒤 설계·현장 판단을 보완해야 합니다."
            ),
        )

    if signals["correctness"]:
        return (
            "기술 정확성 일부 보완 필요",
            (
                "답안의 기본 전개는 유지할 수 있으나, "
                "구조화된 근거에서 기술 정확성 보완 항목이 확인되었습니다."
            ),
        )

    if signals["depth"]:
        return (
            "핵심 내용은 성립하나 상세 해석 보완 필요",
            (
                "핵심 결론은 유지되지만 해석·설계·검증의 깊이를 "
                "보완해야 고득점 답안이 됩니다."
            ),
        )

    if signals["presentation"]:
        return (
            "핵심 내용은 유지되며 수식·표현 확인 필요",
            (
                "기술적 정오를 단정할 근거는 없으며, "
                "수식 연산자·변수 정의·표현 무결성을 확인해야 합니다."
            ),
        )

    if signals["advanced"]:
        return (
            "핵심 요구 충족, 고득점 세부사항 보완 필요",
            (
                "핵심 답안은 성립하며 예외 조건과 정량 근거 등 "
                "고득점 세부사항을 보완할 수 있습니다."
            ),
        )

    if signals["unresolved_requirements"]:
        return (
            "문제 요구 일부 보완 필요",
            (
                "핵심 기술 판정과 별개로 질문의 명시 요구 중 "
                "미충족 또는 부분 충족 항목이 남아 있습니다."
            ),
        )

    return "", ""


def _reconcile_base_summary(
    summary: Any,
    payload: Any,
) -> Any:
    if not isinstance(summary, dict):
        return summary

    if not has_structured_grading_contract(payload):
        return summary

    signals = _collect_signals(payload)
    allow_hard_error = bool(
        signals["logic_fatal"]
        or signals["hard_correctness"]
    )
    updated = copy.deepcopy(summary)
    updated = _sanitize_false_hard_error(
        updated,
        allow_hard_error=allow_hard_error,
    )

    if signals["logic_fatal"]:
        findings = _logic_findings(payload)
        reasons = _dedupe_text(
            [
                _text(
                    row.get("message")
                    or row.get("evidence"),
                    320,
                )
                for row in findings
                if _text(
                    row.get("message")
                    or row.get("evidence"),
                    320,
                )
            ],
            limit=4,
        )
        corrections = _dedupe_text(
            [
                _text(row.get("correct_rule"), 360)
                for row in findings
                if _text(row.get("correct_rule"), 360)
            ],
            limit=4,
        )
        updated["headline"] = (
            "검증된 핵심 기술 오류 보완 필요"
        )
        updated["overall"] = (
            "검증된 핵심 기술 오류가 확인되었습니다. "
            "현장 적용이나 답안 구조의 장점과 별개로 "
            "해당 오류를 먼저 교정해야 합니다."
        )
        if reasons:
            updated["key_reasons"] = reasons
        if corrections:
            updated["improvements"] = corrections
        updated["verdict_consistency"] = {
            "schema_version": VERDICT_CONSISTENCY_SCHEMA_VERSION,
            "marker": VERDICT_CONSISTENCY_MARKER,
            "mode": "preserve_verified_logic_fatal",
        }
        return updated

    headline, overall = _deterministic_verdict(
        signals
    )

    if headline:
        updated["headline"] = headline

    if overall:
        updated["overall"] = overall

    key_reasons = _structured_key_reasons(
        signals
    )
    improvements = _structured_improvements(
        payload,
        signals,
    )

    if key_reasons:
        updated["key_reasons"] = key_reasons

    if improvements:
        updated["improvements"] = improvements
    else:
        updated["improvements"] = []

    if "section_basis" in updated:
        updated["section_basis"] = (
            _sanitize_false_hard_error(
                updated["section_basis"],
                allow_hard_error=allow_hard_error,
            )
        )

    updated["verdict_consistency"] = {
        "schema_version": VERDICT_CONSISTENCY_SCHEMA_VERSION,
        "marker": VERDICT_CONSISTENCY_MARKER,
        "mode": "structured_evidence",
        "hard_error_wording_allowed": allow_hard_error,
        "structured_improvement_count": len(
            improvements
        ),
        "unresolved_requirement_count": len(
            signals["unresolved_requirements"]
        ),
    }
    return updated

_CONTRADICTORY_TECHNICAL_PRAISE = (
    re.compile(
        r"핵심\s*(?:개념|기술|이론)"
        r".{0,30}(?:정확|우수|충실)"
    ),
    re.compile(
        r"기술적\s*(?:개념|내용|관계)"
        r".{0,30}(?:정확|우수)"
    ),
    re.compile(
        r"(?:fact|기술)\s*기반"
        r".{0,30}(?:정확|우수)",
        re.IGNORECASE,
    ),
)
_STRONG_VALUES = {
    "strong",
    "excellent",
    "high",
    "full",
    "우수",
    "강함",
}
_PUBLIC_TEXT_KEYS = {
    "summary",
    "overall_comment",
    "overall_summary",
    "comment",
    "rater_summary",
    "headline",
    "verdict",
    "overall_verdict",
    "strengths",
    "weaknesses",
    "rewrite_advice",
    "improvement_points",
    "improvements",
    "next_practice_focus",
    "next_practice_points",
}


def _has_contradictory_technical_praise(
    value: str,
) -> bool:
    return any(
        pattern.search(value)
        for pattern in (
            _CONTRADICTORY_TECHNICAL_PRAISE
        )
    )


def _sanitize_public_feedback_value(
    value: Any,
) -> Any:
    replacement = (
        "답안 구조의 장점은 있으나 검증된 "
        "기술 오류를 먼저 수정해야 합니다."
    )

    if isinstance(value, str):
        if _has_contradictory_technical_praise(
            value
        ):
            return replacement
        return value

    if isinstance(value, list):
        return [
            _sanitize_public_feedback_value(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return tuple(
            _sanitize_public_feedback_value(item)
            for item in value
        )

    if isinstance(value, dict):
        return {
            key: _sanitize_public_feedback_value(item)
            for key, item in value.items()
        }

    return value


def _sanitize_public_feedback(
    payload: dict[str, Any],
) -> None:
    for key in _PUBLIC_TEXT_KEYS:
        if key in payload:
            payload[key] = (
                _sanitize_public_feedback_value(
                    payload[key]
                )
            )

    breakdown = payload.get("breakdown")
    if isinstance(breakdown, list):
        for row in breakdown:
            if not isinstance(row, dict):
                continue
            for key in (
                "reason",
                "comment",
                "summary",
            ):
                if key in row:
                    row[key] = (
                        _sanitize_public_feedback_value(
                            row[key]
                        )
                    )


def _verified_error_levels(
    signals: dict[str, Any],
) -> tuple[bool, bool]:
    hard_correctness = signals[
        "hard_correctness"
    ]
    fatal_correctness = any(
        _severity(row) == "fatal"
        or row.get(
            "invalidates_core_conclusion"
        )
        is True
        for row in hard_correctness
    )
    fatal_error = bool(
        signals["logic_fatal"]
        or fatal_correctness
    )
    major_or_fatal = bool(
        fatal_error
        or hard_correctness
    )
    return major_or_fatal, fatal_error


def _restrict_coverage_full_credit(
    payload: dict[str, Any],
) -> None:
    candidates = []

    for key in (
        "question_type_coverage",
        "question_type_coverage_summary",
    ):
        value = payload.get(key)
        if isinstance(value, dict):
            candidates.append(value)

    parsed = payload.get("parsed")
    if isinstance(parsed, dict):
        for key in (
            "question_type_coverage",
            "question_type_coverage_summary",
        ):
            value = parsed.get(key)
            if isinstance(value, dict):
                candidates.append(value)

    for coverage in candidates:
        for key in (
            "overall_coverage",
            "coverage",
            "verdict",
            "status",
        ):
            value = coverage.get(key)
            if (
                isinstance(value, str)
                and value.strip().casefold()
                in _STRONG_VALUES
            ):
                coverage[key] = "needs_correction"

        coverage["full_credit_allowed"] = False
        coverage[
            "verified_hard_error_present"
        ] = True

        for key in (
            "correctness_coverage_percent",
            "weighted_coverage_percent",
        ):
            value = coverage.get(key)
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                continue
            if numeric >= 100.0:
                coverage[key] = None
                coverage[
                    "verified_percentage_invalidated"
                ] = True


def _enforce_base_final_decision(
    payload: Any,
) -> Any:
    # This function discovers no new facts, changes no
    # question type, and adds no score penalty. It only
    # reconciles already-verified major/fatal errors with
    # public verdict, pass flags, and full-credit claims.
    if not isinstance(payload, dict):
        return payload

    signals = _collect_signals(payload)
    major_or_fatal, fatal_error = (
        _verified_error_levels(signals)
    )

    if not major_or_fatal:
        return payload

    updated = copy.deepcopy(payload)
    _sanitize_public_feedback(updated)
    _restrict_coverage_full_credit(updated)

    updated["strong_verdict_allowed"] = False
    updated[
        "requirements_full_credit_allowed"
    ] = False

    replacement = (
        "검증된 핵심 기술 오류 보완 필요"
        if fatal_error
        else "검증된 주요 기술 오류 보완 필요"
    )

    for key in (
        "verdict",
        "overall_verdict",
        "headline",
        "answer_level",
        "overall_level",
    ):
        value = updated.get(key)

        if not isinstance(value, str):
            continue

        if (
            value.strip().casefold()
            in _STRONG_VALUES
            or _has_contradictory_technical_praise(
                value
            )
        ):
            updated[key] = replacement

    if fatal_error:
        updated["passing_score_allowed"] = False
        updated["confidence_ceiling"] = "medium"

        confidence_rank = {
            "low": 0,
            "medium": 1,
            "high": 2,
        }
        for key in (
            "confidence",
            "grade_confidence",
            "confidence_level",
        ):
            value = updated.get(key)
            normalized = _text(value, 40).lower()
            if normalized not in confidence_rank:
                continue
            if confidence_rank[normalized] > confidence_rank["medium"]:
                updated[key] = "medium"

        fatal_summary = (
            "검증된 핵심 기술 오류가 확인되었습니다. "
            "현장 적용과 답안 구조의 장점과 별개로 "
            "해당 오류를 먼저 교정해야 합니다."
        )
        for key in (
            "summary",
            "overall_comment",
            "overall_summary",
            "comment",
            "rater_summary",
        ):
            if isinstance(updated.get(key), str):
                updated[key] = fatal_summary

        updated["verdict"] = (
            "검증된 핵심 기술 오류 보완 필요"
        )

        for key in (
            "official_pass_met",
            "practical_target_met",
            "high_score_met",
            "passing",
            "passed",
        ):
            if key in updated:
                updated[key] = False

    updated[
        "final_decision_consistency"
    ] = {
        "schema_version": (
            VERDICT_CONSISTENCY_SCHEMA_VERSION
        ),
        "marker": VERDICT_CONSISTENCY_MARKER,
        "mode": (
            "verified_error_invariants"
        ),
        "major_or_fatal_error": True,
        "fatal_error": fatal_error,
        "logic_fatal": bool(
            signals["logic_fatal"]
        ),
        "hard_correctness_count": len(
            signals["hard_correctness"]
        ),
        "passing_score_allowed": (
            False if fatal_error else None
        ),
        "strong_verdict_allowed": False,
        "requirements_full_credit_allowed": (
            False
        ),
        "numeric_score_changed": False,
    }
    return updated

# Structured defect priority helpers.
def _verified_reconciliation(
    payload: Any,
) -> dict[str, Any]:
    root = _dict(payload)
    direct = root.get(
        "verified_defect_reconciliation"
    )

    if isinstance(direct, dict):
        return direct

    parsed = root.get("parsed")

    if isinstance(parsed, dict):
        nested = parsed.get(
            "verified_defect_reconciliation"
        )

        if isinstance(nested, dict):
            return nested

    coverage = _contract(
        payload,
        "question_type_coverage",
    )
    explicit = _dict(
        coverage.get(
            "explicit_requirement_coverage"
        )
    )
    nested = explicit.get(
        "verified_defect_reconciliation"
    )

    return (
        nested
        if isinstance(nested, dict)
        else {}
    )


def _verified_defect_ids(
    payload: Any,
) -> set[str]:
    reconciliation = (
        _verified_reconciliation(
            payload
        )
    )
    result = {
        _text(value, 180)
        for value in _list(
            reconciliation.get(
                "applied_defect_ids"
            )
        )
        if _text(value, 180)
    }

    coverage = _contract(
        payload,
        "question_type_coverage",
    )
    explicit = _dict(
        coverage.get(
            "explicit_requirement_coverage"
        )
    )

    for row in _list(
        explicit.get("requirements")
    ):
        if not isinstance(row, dict):
            continue

        for value in _list(
            row.get("verified_defect_ids")
        ):
            defect_id = _text(
                value,
                180,
            )

            if defect_id:
                result.add(defect_id)

    return result


def _defect_id(
    row: dict[str, Any],
) -> str:
    return _text(
        row.get("defect_id")
        or row.get("id"),
        180,
    )


def _structured_priority_metadata(
    payload: Any,
    signals: dict[str, Any],
) -> dict[str, Any]:
    reconciliation = (
        _verified_reconciliation(
            payload
        )
    )
    applied_ids = sorted(
        _verified_defect_ids(
            payload
        )
    )
    unresolved_ids = [
        _text(value, 180)
        for value in _list(
            reconciliation.get(
                "unresolved_defect_ids"
            )
        )
        if _text(value, 180)
    ]

    return {
        "marker": (
            "STAGE18B3_STRUCTURED_DEFECT_OUTPUT_PRIORITY_V1"
        ),
        "source": (
            "existing_verified_defect_reconciliation"
        ),
        "output_priority": (
            "verified_defect_before_generic_feedback"
        ),
        "generic_feedback_can_override": False,
        "new_defect_owner_created": False,
        "score_effect": "none",
        "numeric_score_changed": False,
        "primary_score_owner": (
            reconciliation.get(
                "primary_score_owner"
            )
            or "C"
        ),
        "b_completeness_double_deduction": (
            reconciliation.get(
                "b_completeness_double_deduction"
            )
            is True
        ),
        "applied_defect_ids": applied_ids,
        "unresolved_defect_ids": (
            unresolved_ids
        ),
        "verified_correctness_count": len(
            signals.get(
                "verified_correctness"
            )
            or []
        ),
        "verified_hard_correctness_count": len(
            signals.get(
                "verified_hard_correctness"
            )
            or []
        ),
    }


def _collect_signals(
    payload: Any,
) -> dict[str, Any]:
    signals = _collect_base_signals(
        payload
    )
    verified_ids = (
        _verified_defect_ids(
            payload
        )
    )

    verified_correctness = [
        row
        for row in signals.get(
            "correctness",
            [],
        )
        if _defect_id(row)
        in verified_ids
    ]
    verified_hard = [
        row
        for row in signals.get(
            "hard_correctness",
            [],
        )
        if _defect_id(row)
        in verified_ids
    ]

    signals[
        "verified_defect_ids"
    ] = verified_ids
    signals[
        "verified_correctness"
    ] = verified_correctness
    signals[
        "verified_hard_correctness"
    ] = verified_hard
    return signals


def _prioritized_text(
    verified_rows: list[dict[str, Any]],
    fallback: list[str],
    *,
    label: str,
    limit: int = 4,
) -> list[str]:
    result = []
    explanations = []

    for row in verified_rows:
        explanation = _explanation(row)

        if not explanation:
            continue

        explanations.append(explanation)
        candidate = (
            f"{label}: {explanation}"
            if label
            else explanation
        )

        if candidate not in result:
            result.append(candidate)

        if len(result) >= limit:
            return result

    for value in fallback:
        text = _text(value, 320)

        if not text:
            continue

        if any(
            explanation in text
            for explanation in explanations
        ):
            continue

        if text not in result:
            result.append(text)

        if len(result) >= limit:
            break

    return result


def _structured_improvements(
    payload: Any,
    signals: dict[str, Any],
) -> list[str]:
    fallback = (
        _base_structured_improvements(
            payload,
            signals,
        )
    )
    verified = list(
        signals.get(
            "verified_hard_correctness"
        )
        or []
    )

    for row in (
        signals.get(
            "verified_correctness"
        )
        or []
    ):
        if row not in verified:
            verified.append(row)

    if not verified:
        return fallback

    return _prioritized_text(
        verified,
        fallback,
        label="검증된 기술 오류",
        limit=4,
    )


def _structured_key_reasons(
    signals: dict[str, Any],
) -> list[str]:
    fallback = (
        _base_structured_key_reasons(
            signals
        )
    )
    verified = list(
        signals.get(
            "verified_hard_correctness"
        )
        or []
    )

    for row in (
        signals.get(
            "verified_correctness"
        )
        or []
    ):
        if row not in verified:
            verified.append(row)

    if not verified:
        return fallback

    return _prioritized_text(
        verified,
        fallback,
        label="",
        limit=4,
    )


def reconcile_verdict_summary(
    summary: Any,
    payload: Any,
) -> Any:
    updated = (
        _reconcile_base_summary(
            summary,
            payload,
        )
    )

    if not isinstance(updated, dict):
        return updated

    signals = _collect_signals(payload)
    verified_ids = signals.get(
        "verified_defect_ids"
    ) or set()

    if not verified_ids:
        return updated

    updated[
        "structured_defect_output_priority"
    ] = _structured_priority_metadata(
        payload,
        signals,
    )
    return updated


def _enforce_structured_final_decision(
    payload: Any,
) -> Any:
    updated = (
        _enforce_base_final_decision(
            payload
        )
    )

    if not isinstance(updated, dict):
        return updated

    signals = _collect_signals(updated)
    verified_ids = signals.get(
        "verified_defect_ids"
    ) or set()

    if not verified_ids:
        return updated

    updated[
        "structured_defect_output_priority"
    ] = _structured_priority_metadata(
        updated,
        signals,
    )
    return updated

# Final score, status, and narrative consistency.


_POSITIVE_ACCURACY_MARKERS = (
    "정확한 Fact",
    "정확한 fact",
    "Fact가 정확",
    "fact가 정확",
    "사실관계가 정확",
    "오답이 없",
    "모든 Fact가 정확",
    "100% 정확",
    "완전히 정확",
    "정확성이 매우 높",
    "핵심 사실이 정확",
    "요구사항에 정확히 응답",
    "요구한 모든 핵심 항목에 직접 답",
    "정확한 설명이 우수",
    "핵심 개념 인지와 정확",
    "충실히 다루",
    "충실히",
    "구조적으로 잘 서술",
    "잘 서술",
    "잘 설명",
    "대체로 충족",
    "정확하게 설명",
)

_NARRATIVE_FIELDS = (
    "summary",
    "one_line_summary",
    "overall_comment",
    "rater_summary",
    "final_comment",
    "overall_assessment",
)

_ACCURACY_CAUTION_TEXT = (
    "구조화 검증에서 오답 또는 충돌 항목이 확인되어 "
    "정확성 보완이 필요합니다."
)


def _number(value):
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _nonempty_list(value):
    return isinstance(value, list) and bool(value)


def _collect_accuracy_conflicts(value):
    sources = []

    def add(source):
        source = str(source or "").strip()
        if source and source not in sources:
            sources.append(source)

    def walk(node, path="$"):
        if isinstance(node, dict):
            for key, child in node.items():
                child_path = f"{path}.{key}"
                key_lower = str(key).strip().lower()

                if key_lower in {
                    "wrong_count",
                    "contradicted_count",
                    "fatal_count",
                }:
                    number = _number(child)
                    if number is not None and number > 0:
                        add(child_path)

                if key_lower in {
                    "wrong",
                    "wrong_criteria",
                    "contradicted",
                    "contradictions",
                } and _nonempty_list(child):
                    add(child_path)

                if key_lower in {
                    "status",
                    "alignment_status",
                }:
                    status = str(child or "").strip().upper()
                    if status in {
                        "WRONG",
                        "CONTRADICTED",
                        "FATAL_CONTRADICTION",
                        "CANONICAL_RELATION_CONTRADICTION",
                    }:
                        add(child_path)

                if key_lower == "severity":
                    severity = str(child or "").strip().lower()
                    if severity in {"major", "fatal"}:
                        add(child_path)

                walk(child, child_path)
            return

        if isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")

    for root_key in (
        "question_type_coverage",
        "question_type_coverage_summary",
        "question_demand_evidence",
        "question_demand_evidence_for_score",
        "logic_check_evaluation",
        "logic_check_result",
        "generic_claim_relation_evaluation",
    ):
        if root_key in value:
            walk(value.get(root_key), root_key)

    # A canonical ledger with unresolved atomic requirements cannot support a
    # public claim that the answer as a whole is factually accurate.  This is
    # intentionally independent of topic, model, and scoring rubric.
    ledger = value.get("canonical_evaluation_ledger")
    if isinstance(ledger, dict):
        summary = ledger.get("summary")
        counts = summary.get("status_counts") if isinstance(summary, dict) else {}
        if isinstance(counts, dict) and any(
            (_number(counts.get(status)) or 0) > 0
            for status in ("partial", "incorrect", "missing", "unknown")
        ):
            add("canonical_evaluation_ledger.summary.status_counts")

    return sources


def _positive_accuracy_claim(value):
    if not isinstance(value, str):
        return False
    return any(
        marker in value
        for marker in _POSITIVE_ACCURACY_MARKERS
    )


def _rewrite_conflicting_narratives(output, conflict_sources):
    rewritten = []

    if not conflict_sources:
        return rewritten

    for field in _NARRATIVE_FIELDS:
        value = output.get(field)
        if _positive_accuracy_claim(value):
            output[field] = _ACCURACY_CAUTION_TEXT
            rewritten.append(field)

    strengths = output.get("strengths")
    if isinstance(strengths, list):
        prepared = []
        changed = False
        for item in strengths:
            if _positive_accuracy_claim(item):
                prepared.append(_ACCURACY_CAUTION_TEXT)
                changed = True
            else:
                prepared.append(item)
        if changed:
            output["strengths"] = prepared
            rewritten.append("strengths")

    return rewritten


def _status_from_score(
    total,
    official,
    practical,
    high,
):
    if total >= high:
        return "HIGH_SCORE"
    if total >= practical:
        return "PRACTICAL_TARGET"
    if total >= official:
        return "OFFICIAL_PASS"
    return "BELOW_PASS"


def enforce_final_score_status_narrative_consistency(
    parsed,
):
    if not isinstance(parsed, dict):
        return parsed

    output = dict(parsed)

    total = _number(
        output.get("total_score")
    )
    final_total = _number(
        output.get("final_total_score")
    )

    if total is not None:
        canonical_total = total
        score_source = "total_score"
    elif final_total is not None:
        canonical_total = final_total
        score_source = "final_total_score"
    else:
        canonical_total = None
        score_source = "none"

    score_fields_synchronized = []
    threshold_flags_synchronized = []

    if canonical_total is not None:
        max_score = _number(
            output.get("max_score")
        )
        if max_score is None or max_score <= 0:
            max_score = 25.0

        canonical_total = round(
            max(0.0, min(canonical_total, max_score)),
            2,
        )
        if output.get("total_score") != canonical_total:
            score_fields_synchronized.append(
                "total_score"
            )
        if (
            output.get("final_total_score")
            != canonical_total
        ):
            score_fields_synchronized.append(
                "final_total_score"
            )

        output["total_score"] = canonical_total
        output["final_total_score"] = canonical_total

        official = _number(
            output.get("official_pass_score")
        )
        practical = _number(
            output.get("practical_target_score")
        )
        high = _number(
            output.get("high_score_target")
        )

        if official is None:
            official = round(max_score * 0.60, 2)
        if practical is None:
            practical = round(max_score * 0.70, 2)
        if high is None:
            high = round(max_score * 0.80, 2)

        output["official_pass_score"] = official
        output["practical_target_score"] = practical
        output["high_score_target"] = high

        expected_flags = {
            "official_pass_met": canonical_total >= official,
            "practical_target_met": (
                canonical_total >= practical
            ),
            "average_target_met": (
                canonical_total >= practical
            ),
            "high_score_met": canonical_total >= high,
        }
        for key, expected in expected_flags.items():
            if output.get(key) is not expected:
                threshold_flags_synchronized.append(key)
            output[key] = expected

        canonical_status = (
            _status_from_score(
                canonical_total,
                official,
                practical,
                high,
            )
        )
        output["final_score_status"] = canonical_status
        output["score_status"] = canonical_status
    else:
        canonical_status = str(
            output.get("final_score_status")
            or output.get("score_status")
            or "UNKNOWN"
        ).strip() or "UNKNOWN"

    conflict_sources = (
        _collect_accuracy_conflicts(output)
    )
    rewritten_fields = _rewrite_conflicting_narratives(
        output,
        conflict_sources,
    )

    output["final_consistency_evaluation"] = {
        "version": "final_score_status_narrative_consistency_v1",
        "canonical_score": canonical_total,
        "canonical_status": canonical_status,
        "score_source": score_source,
        "score_fields_synchronized": (
            score_fields_synchronized
        ),
        "threshold_flags_synchronized": (
            threshold_flags_synchronized
        ),
        "structured_accuracy_conflict": bool(
            conflict_sources
        ),
        "conflict_sources": conflict_sources,
        "narrative_fields_checked": list(
            _NARRATIVE_FIELDS
        ) + ["strengths"],
        "narrative_fields_rewritten": (
            rewritten_fields
        ),
        "positive_accuracy_claim_allowed": not bool(
            conflict_sources
        ),
        "consistent": True,
        "direct_score_application": False,
    }
    return output


def enforce_generic_contract_consistency(parsed):
    """Public Stage23 generic score/status/narrative consistency gate."""
    return enforce_final_score_status_narrative_consistency(
        parsed
    )


def _should_apply_score_consistency(value):
    if not isinstance(value, dict):
        return False

    if any(
        key in value
        for key in (
            "generic_claim_relation_evaluation",
            "generic_de_policy_evaluation",
            "final_consistency_evaluation",
        )
    ):
        return True

    total = _number(
        value.get("total_score")
    )
    final_total = _number(
        value.get("final_total_score")
    )
    if (
        total is not None
        and final_total is not None
        and abs(total - final_total) > 0.001
    ):
        return True

    if _collect_accuracy_conflicts(value):
        return True

    coverage = value.get("question_type_coverage")
    if isinstance(coverage, dict) and any(
        key in coverage
        for key in (
            "wrong_count",
            "wrong_criteria",
            "correctness_coverage",
        )
    ):
        return True

    return False


def enforce_final_decision_consistency(payload: Any) -> Any:
    """Apply the complete public verdict-consistency pipeline once."""
    result = _enforce_structured_final_decision(payload)
    if _should_apply_score_consistency(result):
        return enforce_generic_contract_consistency(result)
    return result
