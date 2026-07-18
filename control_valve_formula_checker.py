from __future__ import annotations

import copy
import re
import unicodedata
from typing import Any


TARGET_TOPIC_ID = (
    "control_valve_fluid_forces_"
    "unbalance_friction_actuator_"
    "sizing_fail_safe"
)
FORMULA_CHECK_VERSION = (
    "control_valve_formula_check_v1"
)

try:
    import sympy as _sympy
except Exception:
    _sympy = None


_SCORE_FIELDS = (
    "total_score",
    "final_total_score",
    "total_before_cap",
    "score_range",
    "breakdown",
    "applied_caps",
    "rater_results",
    "rater_weighted_evaluation",
)

_P1_PATTERN = (
    r"(?<![A-Za-z0-9_])"
    r"p\s*_?\s*1"
    r"(?![A-Za-z0-9_])"
)
_P2_PATTERN = (
    r"(?<![A-Za-z0-9_])"
    r"p\s*_?\s*2"
    r"(?![A-Za-z0-9_])"
)


def _normalize_text(
    value: str | None,
) -> str:
    text = unicodedata.normalize(
        "NFKC",
        str(value or ""),
    )

    for old, new in {
        "−": "-",
        "–": "-",
        "—": "-",
        "×": "*",
        "·": "*",
        "∙": "*",
        "÷": "/",
        "＝": "=",
        "₁": "1",
        "₂": "2",
    }.items():
        text = text.replace(old, new)

    return text


def _compact_expression(
    expression: str,
) -> str:
    value = _normalize_text(
        expression
    )

    replacements = [
        (r"\\left|\\right", ""),
        (r"\$", ""),
        (r"\\,", ""),
        (r"\\cdot|\\times", "*"),
        (
            r"(?<![A-Za-z0-9_])"
            r"P\s*_?\s*1"
            r"(?![A-Za-z0-9_])",
            "P1",
        ),
        (
            r"(?<![A-Za-z0-9_])"
            r"P\s*_?\s*2"
            r"(?![A-Za-z0-9_])",
            "P2",
        ),
        (
            r"(?<![A-Za-z0-9_])"
            r"(?:A_EFF|AEFF|A_E)"
            r"(?![A-Za-z0-9_])",
            "A",
        ),
    ]

    for pattern, replacement in replacements:
        value = re.sub(
            pattern,
            replacement,
            value,
            flags=re.IGNORECASE,
        )

    value = value.replace(
        "유효 면적",
        "A",
    )
    value = value.replace(
        "유효면적",
        "A",
    )
    value = re.sub(
        r"\s+",
        "",
        value,
    )

    value = re.sub(
        r"(P1|P2)(?=A(?:$|[^A-Za-z0-9_]))",
        r"\1*",
        value,
    )
    value = re.sub(
        r"\)(?=A(?:$|[^A-Za-z0-9_]))",
        ")*",
        value,
    )
    value = re.sub(
        r"(?<=A)(?=P1|P2|\()",
        "*",
        value,
    )

    return value


def _strip_outer_parentheses(
    expression: str,
) -> str:
    value = expression

    while (
        len(value) >= 2
        and value.startswith("(")
        and value.endswith(")")
    ):
        depth = 0
        enclosed = True

        for index, char in enumerate(value):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1

                if (
                    depth == 0
                    and index != len(value) - 1
                ):
                    enclosed = False
                    break

            if depth < 0:
                enclosed = False
                break

        if not enclosed or depth != 0:
            break

        value = value[1:-1]

    return value


def _extract_equations(
    answer_text: str,
) -> list[dict[str, Any]]:
    equations = []

    for line_number, line in enumerate(
        _normalize_text(
            answer_text
        ).splitlines(),
        start=1,
    ):
        if "=" not in line:
            continue

        parts = line.split("=")

        for index in range(
            len(parts) - 1
        ):
            left = parts[index].strip()
            right = parts[index + 1].strip()

            if not left or not right:
                continue

            equations.append(
                {
                    "line": line_number,
                    "text": (
                        left
                        + "="
                        + right
                    ),
                    "left": left,
                    "right": right,
                    "normalized_right": (
                        _compact_expression(
                            right
                        )
                    ),
                }
            )

    return equations


def _force_left_side(
    left: str,
) -> bool:
    compact = _compact_expression(
        left
    ).upper()

    return bool(
        any(
            token in compact
            for token in [
                "FU",
                "FB",
                "FP",
                "PRESSUREFORCE",
                "UNBALANCEFORCE",
            ]
        )
        or "불평형력" in left
        or "압력력" in left
        or "압력에 의한 힘" in left
    )


def _sympy_formula_sign(
    expression: str,
) -> str | None:
    if _sympy is None:
        return None

    if not re.fullmatch(
        r"[A-Za-z0-9_+\-*/().]+",
        expression,
    ):
        return None

    try:
        p1, p2, area = _sympy.symbols(
            "P1 P2 A"
        )
        parsed = _sympy.sympify(
            expression,
            locals={
                "P1": p1,
                "P2": p2,
                "A": area,
            },
            evaluate=False,
        )

        if (
            _sympy.simplify(
                parsed
                - (p1 - p2) * area
            )
            == 0
        ):
            return "p1_minus_p2"

        if (
            _sympy.simplify(
                parsed
                - (p2 - p1) * area
            )
            == 0
        ):
            return "p2_minus_p1"

        return "other"

    except Exception:
        return None


def _pattern_formula_sign(
    expression: str,
) -> str:
    compact = _strip_outer_parentheses(
        expression.upper()
    )

    if compact in {
        "(P1-P2)*A",
        "A*(P1-P2)",
        "P1*A-P2*A",
        "A*P1-A*P2",
    }:
        return "p1_minus_p2"

    if compact in {
        "(P2-P1)*A",
        "A*(P2-P1)",
        "P2*A-P1*A",
        "A*P2-A*P1",
    }:
        return "p2_minus_p1"

    return "other"


def _formula_sign(
    expression: str,
) -> tuple[str, str]:
    symbolic = _sympy_formula_sign(
        expression
    )

    if symbolic is not None:
        return symbolic, "sympy"

    return (
        _pattern_formula_sign(
            expression
        ),
        "deterministic_pattern",
    )


def _contains_direction(
    text: str,
    direction: str,
) -> bool:
    if direction == "open":
        return bool(
            re.search(
                r"열림|개방|open",
                text,
                flags=re.IGNORECASE,
            )
        )

    return bool(
        re.search(
            r"닫힘|폐쇄|close",
            text,
            flags=re.IGNORECASE,
        )
    )


def _pressure_direction(
    answer_text: str,
    pressure_pattern: str,
) -> str | None:
    directions = set()

    for line in _normalize_text(
        answer_text
    ).splitlines():
        if not re.search(
            pressure_pattern,
            line,
            flags=re.IGNORECASE,
        ):
            continue

        if _contains_direction(
            line,
            "open",
        ):
            directions.add("open")

        if _contains_direction(
            line,
            "close",
        ):
            directions.add("close")

    if len(directions) == 1:
        return next(iter(directions))

    return None


def _positive_direction(
    answer_text: str,
) -> str | None:
    text = _normalize_text(
        answer_text
    )

    positive = (
        r"(?:양(?:의)?(?:\(\+\))?"
        r"|양의\s*방향"
        r"|\+"
        r"|positive)"
    )

    open_pattern = (
        r"(?:열림|개방|open)"
    )
    close_pattern = (
        r"(?:닫힘|폐쇄|close)"
    )

    open_positive = bool(
        re.search(
            open_pattern
            + r".{0,32}"
            + positive,
            text,
            flags=(
                re.IGNORECASE
                | re.DOTALL
            ),
        )
        or re.search(
            positive
            + r".{0,32}"
            + open_pattern,
            text,
            flags=(
                re.IGNORECASE
                | re.DOTALL
            ),
        )
    )

    close_positive = bool(
        re.search(
            close_pattern
            + r".{0,32}"
            + positive,
            text,
            flags=(
                re.IGNORECASE
                | re.DOTALL
            ),
        )
        or re.search(
            positive
            + r".{0,32}"
            + close_pattern,
            text,
            flags=(
                re.IGNORECASE
                | re.DOTALL
            ),
        )
    )

    if open_positive and not close_positive:
        return "open"

    if close_positive and not open_positive:
        return "close"

    return None


def _direction_context(
    answer_text: str,
) -> dict[str, Any]:
    positive = _positive_direction(
        answer_text
    )
    p1_direction = _pressure_direction(
        answer_text,
        _P1_PATTERN,
    )
    p2_direction = _pressure_direction(
        answer_text,
        _P2_PATTERN,
    )

    expected = None

    if positive == "open":
        if (
            p1_direction == "open"
            and p2_direction == "close"
        ):
            expected = "p1_minus_p2"
        elif (
            p1_direction == "close"
            and p2_direction == "open"
        ):
            expected = "p2_minus_p1"

    elif positive == "close":
        if (
            p1_direction == "close"
            and p2_direction == "open"
        ):
            expected = "p1_minus_p2"
        elif (
            p1_direction == "open"
            and p2_direction == "close"
        ):
            expected = "p2_minus_p1"

    return {
        "positive_direction": positive,
        "p1_direction": p1_direction,
        "p2_direction": p2_direction,
        "expected_formula_sign": expected,
        "explicit_complete_premise": (
            expected is not None
        ),
    }


def _finding(
    *,
    finding_id: str,
    severity: str,
    message: str,
    correct_rule: str,
    evidence: str = "",
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "severity": severity,
        "message": message,
        "evidence": evidence,
        "correct_rule": correct_rule,
        "score_effect": (
            "diagnostic_only"
        ),
        "direct_score_application": False,
    }


def _pressure_findings(
    equations: list[dict[str, Any]],
    direction: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    findings = []
    formulas = []

    for equation in equations:
        right = equation[
            "normalized_right"
        ].upper()

        if not (
            _force_left_side(
                equation["left"]
            )
            and (
                "P1" in right
                or "P2" in right
            )
        ):
            continue

        formula = copy.deepcopy(
            equation
        )
        formula["has_p1"] = (
            "P1" in right
        )
        formula["has_p2"] = (
            "P2" in right
        )
        formula["has_area"] = bool(
            re.search(
                r"(?<![A-Za-z0-9_])"
                r"A"
                r"(?![A-Za-z0-9_])",
                right,
            )
        )

        if not formula["has_area"]:
            formula["classification"] = (
                "missing_area"
            )
            formula["engine"] = (
                "deterministic_structure"
            )
            formulas.append(formula)

            findings.append(
                _finding(
                    finding_id=(
                        "pressure_force_"
                        "missing_area"
                    ),
                    severity="major",
                    message=(
                        "명시한 압력력 수식에 "
                        "유효면적 항이 없습니다."
                    ),
                    evidence=equation["text"],
                    correct_rule=(
                        "압력력은 압력 또는 "
                        "차압과 유효면적의 "
                        "곱으로 표현해야 합니다."
                    ),
                )
            )
            continue

        if re.search(
            r"(?:P1|P2)\+A"
            r"|A\+(?:P1|P2)",
            right,
        ):
            formula["classification"] = (
                "invalid_pressure_area_operation"
            )
            formula["engine"] = (
                "deterministic_structure"
            )
            formulas.append(formula)

            findings.append(
                _finding(
                    finding_id=(
                        "pressure_area_"
                        "invalid_operation"
                    ),
                    severity="major",
                    message=(
                        "압력과 면적을 더하는 "
                        "수식이 명시되었습니다."
                    ),
                    evidence=equation["text"],
                    correct_rule=(
                        "압력력은 압력과 "
                        "유효면적의 곱입니다."
                    ),
                )
            )
            continue

        sign, engine = _formula_sign(
            equation[
                "normalized_right"
            ]
        )

        formula["classification"] = sign
        formula["engine"] = engine
        formulas.append(formula)

    if not formulas:
        findings.append(
            _finding(
                finding_id=(
                    "pressure_force_"
                    "formula_absent"
                ),
                severity="warning",
                message=(
                    "P1·P2와 유효면적을 "
                    "연결한 명시적 압력력 "
                    "수식을 확인하지 못했습니다."
                ),
                correct_rule=(
                    "불평형력 설명 시 "
                    "압력차, 유효면적과 "
                    "힘 방향을 함께 "
                    "정의하는 것이 좋습니다."
                ),
            )
        )

        return findings, formulas

    expected = direction.get(
        "expected_formula_sign"
    )

    for formula in formulas:
        sign = formula.get(
            "classification"
        )

        if sign not in {
            "p1_minus_p2",
            "p2_minus_p1",
        }:
            continue

        if expected is None:
            findings.append(
                _finding(
                    finding_id=(
                        "pressure_direction_"
                        "not_declared"
                    ),
                    severity="warning",
                    message=(
                        "압력차 수식은 있으나 "
                        "양의 힘 방향과 P1·P2의 "
                        "작용 방향이 완전하게 "
                        "정의되지 않았습니다."
                    ),
                    evidence=formula["text"],
                    correct_rule=(
                        "열림 또는 닫힘을 "
                        "양의 방향으로 정한 후 "
                        "P1·P2 작용 방향을 "
                        "명시해야 합니다."
                    ),
                )
            )
        elif sign != expected:
            findings.append(
                _finding(
                    finding_id=(
                        "pressure_difference_"
                        "direction_reversed"
                    ),
                    severity="major",
                    message=(
                        "답안이 정의한 양의 "
                        "방향과 P1·P2 작용 "
                        "방향에 비해 압력차 "
                        "수식의 부호가 "
                        "반대로 명시되었습니다."
                    ),
                    evidence=formula["text"],
                    correct_rule=(
                        "선언한 양의 방향에 "
                        "맞춰 P1-P2 또는 "
                        "P2-P1을 결정해야 합니다."
                    ),
                )
            )

    return findings, formulas


def _friction_findings(
    answer_text: str,
) -> list[dict[str, Any]]:
    text = _normalize_text(
        answer_text
    )
    lowered = text.lower()

    if not any(
        token in lowered
        for token in [
            "마찰",
            "friction",
            "stiction",
        ]
    ):
        return []

    wrong = bool(
        re.search(
            r"마찰력.{0,40}"
            r"(?:운동|이동|스트로크).{0,20}"
            r"(?:같은|동일한)\s*방향",
            lowered,
        )
        or re.search(
            r"friction.{0,40}"
            r"(?:same direction|assists motion)",
            lowered,
            flags=re.IGNORECASE,
        )
    )

    if wrong:
        return [
            _finding(
                finding_id=(
                    "friction_direction_"
                    "assists_motion"
                ),
                severity="major",
                message=(
                    "마찰력이 이동 방향과 "
                    "같은 방향으로 작용한다고 "
                    "명시했습니다."
                ),
                correct_rule=(
                    "마찰력은 실제 운동 "
                    "방향의 반대로 작용합니다."
                ),
            )
        ]

    correct = bool(
        re.search(
            r"마찰력.{0,40}"
            r"(?:운동|이동|스트로크).{0,20}"
            r"(?:반대|저항)",
            lowered,
        )
        or re.search(
            r"(?:운동|이동|스트로크).{0,20}"
            r"(?:반대|저항).{0,30}"
            r"마찰",
            lowered,
        )
        or "opposes motion" in lowered
    )

    actuator_only = bool(
        re.search(
            r"마찰력.{0,30}"
            r"(?:구동기|액추에이터|fa).{0,20}"
            r"반대",
            lowered,
        )
    )

    if actuator_only and not correct:
        return [
            _finding(
                finding_id=(
                    "friction_direction_"
                    "reference_ambiguous"
                ),
                severity="warning",
                message=(
                    "마찰 방향을 운동 방향이 "
                    "아니라 구동기 힘의 "
                    "반대로만 정의했습니다."
                ),
                correct_rule=(
                    "마찰력은 실제 이동 "
                    "방향의 반대로 정의해야 "
                    "합니다."
                ),
            )
        ]

    if not correct:
        return [
            _finding(
                finding_id=(
                    "friction_direction_"
                    "not_declared"
                ),
                severity="warning",
                message=(
                    "마찰을 언급했으나 "
                    "실제 이동 방향에 대한 "
                    "반대 작용을 명시하지 "
                    "않았습니다."
                ),
                correct_rule=(
                    "마찰력은 실제 운동 "
                    "방향의 반대로 작용합니다."
                ),
            )
        ]

    return []


def evaluate_control_valve_formula_check(
    *,
    answer_text: str,
    topic_id: str | None,
) -> dict[str, Any]:
    resolved_topic = str(
        topic_id or ""
    ).strip()

    result = {
        "version": FORMULA_CHECK_VERSION,
        "engine": (
            "optional_sympy_with_"
            "deterministic_fallback"
        ),
        "sympy_available": (
            _sympy is not None
        ),
        "scope": TARGET_TOPIC_ID,
        "topic_id": resolved_topic,
        "applicable": (
            resolved_topic
            == TARGET_TOPIC_ID
        ),
        "score_effect": (
            "diagnostic_only"
        ),
        "direct_score_application": False,
        "verdict": "not_applicable",
        "major_error_detected": False,
        "warning_detected": False,
        "findings": [],
        "formulas": [],
        "direction_context": {},
        "summary": (
            "대상 Topic이 아니므로 "
            "수식 검사를 적용하지 않았습니다."
        ),
    }

    if resolved_topic != TARGET_TOPIC_ID:
        return result

    direction = _direction_context(
        answer_text
    )
    findings, formulas = (
        _pressure_findings(
            _extract_equations(
                answer_text
            ),
            direction,
        )
    )
    findings.extend(
        _friction_findings(
            answer_text
        )
    )

    major = any(
        item.get("severity") == "major"
        for item in findings
    )
    warning = any(
        item.get("severity") == "warning"
        for item in findings
    )

    result.update(
        {
            "verdict": (
                "major"
                if major
                else "warn"
                if warning
                else "pass"
            ),
            "major_error_detected": major,
            "warning_detected": warning,
            "findings": findings,
            "formulas": formulas,
            "direction_context": direction,
            "summary": (
                "명시적 수식 또는 방향 "
                "자기모순을 확인했습니다."
                if major
                else "수식·방향 정의 보완 "
                "경고가 있습니다."
                if warning
                else "확인 가능한 수식과 "
                "방향 관계에 명시적 "
                "모순이 없습니다."
            ),
        }
    )

    return result


def _score_snapshot(
    grade: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: copy.deepcopy(
            grade.get(key)
        )
        for key in _SCORE_FIELDS
        if key in grade
    }


def attach_control_valve_formula_check(
    grade: dict[str, Any],
    answer_text: str,
) -> dict[str, Any]:
    if not isinstance(grade, dict):
        return grade

    output = copy.deepcopy(grade)
    before = _score_snapshot(output)

    topic_id = (
        output.get("topic_id")
        or output.get(
            "logic_check_topic_id"
        )
        or output.get(
            "inferred_topic_id"
        )
        or ""
    )

    output[
        "formula_check_evaluation"
    ] = (
        evaluate_control_valve_formula_check(
            answer_text=answer_text,
            topic_id=str(topic_id),
        )
    )

    if before != _score_snapshot(output):
        raise RuntimeError(
            "Formula checker changed "
            "numeric score state"
        )

    return output
