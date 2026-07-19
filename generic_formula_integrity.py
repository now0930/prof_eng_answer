"""Generic, topic-independent formula integrity diagnostics.

The analyzer checks only representational integrity. It does not decide
whether a domain formula is scientifically correct and does not change scores.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

GENERIC_FORMULA_INTEGRITY_SCHEMA_VERSION = "1.0"
GENERIC_FORMULA_INTEGRITY_MARKER = "GENERIC_FORMULA_INTEGRITY_V1"

_RELATION_PATTERN = re.compile(r"(?:<=|>=|!=|==|=|<|>|≤|≥|≠)")
_TERM_PATTERN = re.compile(
    r"""
    (?:
        [A-Za-zΑ-Ωα-ω가-힣]
        [A-Za-z0-9_Α-Ωα-ω가-힣,]*
        (?:\s*\([^()\n]*\))?
    )
    |
    (?:
        \d+(?:\.\d+)?
    )
    """,
    re.VERBOSE,
)
_OPERATOR_ONLY_PATTERN = re.compile(r"^[+\-*/^=<>≤≥≠]+$")
_FUNCTION_NAMES = {
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "log",
    "ln",
    "exp",
    "sqrt",
    "max",
    "min",
    "abs",
}


def _text(value: Any, limit: int = 5000) -> str:
    if value is None:
        return ""
    text = value if isinstance(value, str) else str(value)
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()[:limit]


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _balanced_delimiters(text: str) -> list[dict[str, str]]:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[tuple[str, int]] = []
    issues: list[dict[str, str]] = []

    for index, char in enumerate(text):
        if char in "([{":
            stack.append((char, index))
        elif char in ")]}":
            if not stack or stack[-1][0] != pairs[char]:
                issues.append(
                    {
                        "code": "unbalanced_delimiter",
                        "severity": "partial",
                        "message": (
                            f"닫는 구분자 '{char}'의 짝이 맞지 않는다."
                        ),
                    }
                )
                continue
            stack.pop()

    for char, _index in stack:
        issues.append(
            {
                "code": "unbalanced_delimiter",
                "severity": "partial",
                "message": (
                    f"여는 구분자 '{char}'가 닫히지 않았다."
                ),
            }
        )

    return issues


def _line_starts_with_term(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped[0] in "+-*/^=<>≤≥≠,.;:)]}":
        return False
    return bool(_TERM_PATTERN.match(stripped))


def _line_ends_with_continuation(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return stripped[-1] in "+-*/^=<>≤≥≠([{,"


def _missing_multiline_operators(text: str) -> list[dict[str, str]]:
    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if len(lines) < 2:
        return []

    relation_index = None

    for index, line in enumerate(lines):
        if _RELATION_PATTERN.search(line):
            relation_index = index
            break

    if relation_index is None:
        return []

    issues: list[dict[str, str]] = []

    for index in range(relation_index + 1, len(lines)):
        current = lines[index]
        previous = lines[index - 1]

        if _OPERATOR_ONLY_PATTERN.fullmatch(current):
            continue

        if (
            _line_starts_with_term(current)
            and not _line_ends_with_continuation(previous)
        ):
            issues.append(
                {
                    "code": "missing_term_operator",
                    "severity": "warning",
                    "message": (
                        f"{index + 1}번째 수식 줄 앞에 항 연결 연산자가 "
                        "누락됐을 가능성이 있다."
                    ),
                }
            )

    return issues


def _adjacent_terms_without_operator(
    text: str,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for line_number, line in enumerate(text.split("\n"), start=1):
        stripped = line.strip()

        if not stripped:
            continue

        matches = list(_TERM_PATTERN.finditer(stripped))

        for left, right in zip(matches, matches[1:]):
            between = stripped[left.end():right.start()]

            if not between or not between.strip():
                left_token = left.group(0).strip().lower()

                if left_token in _FUNCTION_NAMES:
                    continue

                issues.append(
                    {
                        "code": "adjacent_terms_without_operator",
                        "severity": "warning",
                        "message": (
                            f"{line_number}번째 수식 줄에서 두 항 사이의 "
                            "연산자가 보이지 않는다."
                        ),
                    }
                )
                break

    return issues


def _dedupe_issues(
    issues: list[dict[str, str]],
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for issue in issues:
        key = (
            str(issue.get("code") or ""),
            str(issue.get("message") or ""),
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(issue)

    return result


def analyze_formula_text(
    formula_text: Any,
) -> dict[str, Any]:
    text = _text(formula_text)

    if not text:
        return {
            "schema_version": GENERIC_FORMULA_INTEGRITY_SCHEMA_VERSION,
            "marker": GENERIC_FORMULA_INTEGRITY_MARKER,
            "status": "not_applicable",
            "issues": [],
        }

    issues = []
    issues.extend(_balanced_delimiters(text))
    issues.extend(_missing_multiline_operators(text))
    issues.extend(_adjacent_terms_without_operator(text))
    issues = _dedupe_issues(issues)

    if any(
        issue.get("severity") == "partial"
        for issue in issues
    ):
        status = "invalid"
    elif issues:
        status = "warning"
    else:
        status = "valid"

    return {
        "schema_version": GENERIC_FORMULA_INTEGRITY_SCHEMA_VERSION,
        "marker": GENERIC_FORMULA_INTEGRITY_MARKER,
        "status": status,
        "issues": issues,
    }


def _merge_notes(
    existing: Any,
    analysis: dict[str, Any],
) -> list[str]:
    notes = []

    if isinstance(existing, list):
        notes.extend(
            str(item).strip()
            for item in existing
            if str(item).strip()
        )
    elif existing:
        notes.append(str(existing).strip())

    notes.extend(
        str(issue.get("message") or "").strip()
        for issue in analysis.get("issues", [])
        if str(issue.get("message") or "").strip()
    )

    result = []
    seen = set()

    for note in notes:
        if note in seen:
            continue
        seen.add(note)
        result.append(note)

    return result


def _formula_defect(
    formula: dict[str, Any],
    issue: dict[str, str],
) -> dict[str, Any]:
    payload = {
        "defect_type": "presentation_issue",
        "severity": (
            "partial"
            if issue.get("severity") == "partial"
            else "warning"
        ),
        "owner_layer": "C",
        "requirement_id": str(
            formula.get("requirement_id") or ""
        ).strip(),
        "evidence_text": str(
            formula.get("formula_text") or ""
        ).strip(),
        "explanation": str(
            issue.get("message") or ""
        ).strip(),
        "affected_claim_ids": [],
        "diagnostic_only": True,
        "formula_issue_code": str(
            issue.get("code") or ""
        ).strip(),
        "formula_id": str(
            formula.get("formula_id") or ""
        ).strip(),
    }
    payload["defect_id"] = _stable_id(
        "formula_integrity",
        payload,
    )
    return payload


def _dedupe_defects(
    defects: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result = []
    seen = set()

    for defect in defects:
        identifier = str(
            defect.get("defect_id") or ""
        ).strip()

        if not identifier:
            identifier = _stable_id(
                "defect",
                defect,
            )
            defect["defect_id"] = identifier

        if identifier in seen:
            continue

        seen.add(identifier)
        result.append(defect)

    return result


def _refresh_summary(
    contract: dict[str, Any],
) -> None:
    defects = contract.get("defects")
    formulas = contract.get("formulas")

    if not isinstance(defects, list):
        defects = []
    if not isinstance(formulas, list):
        formulas = []

    summary = contract.get("summary")

    if not isinstance(summary, dict):
        summary = {}
        contract["summary"] = summary

    type_counts = {
        "correctness_error": 0,
        "core_depth_gap": 0,
        "advanced_detail_missing": 0,
        "presentation_issue": 0,
    }
    owner_counts = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
    }

    for defect in defects:
        if not isinstance(defect, dict):
            continue

        defect_type = str(
            defect.get("defect_type") or ""
        ).strip()
        owner_layer = str(
            defect.get("owner_layer") or ""
        ).strip().upper()

        if defect_type in type_counts:
            type_counts[defect_type] += 1

        if owner_layer in owner_counts:
            owner_counts[owner_layer] += 1

    summary["formula_count"] = len(formulas)
    summary["defect_count"] = len(defects)
    summary["defect_type_counts"] = type_counts
    summary["owner_layer_counts"] = owner_counts
    summary["formula_integrity_warning_count"] = sum(
        isinstance(formula, dict)
        and formula.get("integrity_status") == "warning"
        for formula in formulas
    )
    summary["formula_integrity_invalid_count"] = sum(
        isinstance(formula, dict)
        and formula.get("integrity_status") == "invalid"
        for formula in formulas
    )


def apply_formula_integrity_to_contract(
    value: Any,
) -> Any:
    if not isinstance(value, dict):
        return value

    contract = copy.deepcopy(value)
    formulas = contract.get("formulas")

    if not isinstance(formulas, list):
        return contract

    defects = contract.get("defects")

    if not isinstance(defects, list):
        defects = []

    updated_formulas = []
    generated_defects = []

    for raw_formula in formulas:
        if not isinstance(raw_formula, dict):
            updated_formulas.append(raw_formula)
            continue

        formula = copy.deepcopy(raw_formula)
        analysis = analyze_formula_text(
            formula.get("formula_text")
        )
        existing_status = str(
            formula.get("integrity_status") or ""
        ).strip()

        deterministic_status = analysis["status"]

        if existing_status == "invalid":
            final_status = "invalid"
        elif deterministic_status in {"invalid", "warning"}:
            final_status = deterministic_status
        elif existing_status in {
            "valid",
            "warning",
            "not_evaluated",
            "not_applicable",
        }:
            final_status = existing_status
        else:
            final_status = deterministic_status

        formula["integrity_status"] = final_status
        formula["integrity_notes"] = _merge_notes(
            formula.get("integrity_notes"),
            analysis,
        )
        formula["generic_integrity"] = analysis
        updated_formulas.append(formula)

        for issue in analysis.get("issues", []):
            generated_defects.append(
                _formula_defect(
                    formula,
                    issue,
                )
            )

    contract["formulas"] = updated_formulas
    contract["defects"] = _dedupe_defects(
        [
            defect
            for defect in defects
            if isinstance(defect, dict)
        ]
        + generated_defects
    )
    contract["formula_integrity"] = {
        "schema_version": GENERIC_FORMULA_INTEGRITY_SCHEMA_VERSION,
        "marker": GENERIC_FORMULA_INTEGRITY_MARKER,
        "mode": "diagnostic_only",
        "score_effect": "none",
    }
    _refresh_summary(contract)
    return contract


def apply_formula_integrity_to_result(
    result: Any,
) -> Any:
    if not isinstance(result, dict):
        return result

    updated = copy.deepcopy(result)
    root_contract = updated.get("general_evidence_contract")
    parsed = updated.get("parsed")

    if isinstance(root_contract, dict):
        root_contract = apply_formula_integrity_to_contract(
            root_contract
        )
        updated["general_evidence_contract"] = root_contract

    if isinstance(parsed, dict):
        parsed_contract = parsed.get(
            "general_evidence_contract"
        )

        if isinstance(parsed_contract, dict):
            parsed_contract = apply_formula_integrity_to_contract(
                parsed_contract
            )
            parsed["general_evidence_contract"] = parsed_contract

            if not isinstance(root_contract, dict):
                updated["general_evidence_contract"] = copy.deepcopy(
                    parsed_contract
                )

    return updated
