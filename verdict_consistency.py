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
    logic = _dict(root.get("logic_check"))

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


def _signals(payload: Any) -> dict[str, Any]:
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


def _structured_improvements(
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


def _structured_key_reasons(
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


def reconcile_verdict_summary(
    summary: Any,
    payload: Any,
) -> Any:
    if not isinstance(summary, dict):
        return summary

    if not has_structured_grading_contract(payload):
        return summary

    signals = _signals(payload)
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
