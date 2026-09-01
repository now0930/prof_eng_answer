"""Deterministic relation and dimensional checks for target-SIL answers.

This module owns only explicit SIL risk-reduction equations.  It does not
penalize missing equations and it does not infer a wrong claim from keywords.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any


SIL_RELATION_INTEGRITY_VERSION = "sil_relation_integrity_v1"
SIL_RELATION_INTEGRITY_MARKER = "SIL_RELATION_INTEGRITY_V1"
SIL_TARGET_TOPIC_ID = (
    "sil_target_determination_risk_reduction_and_lifecycle"
)

_PFD = r"pfd(?:avg|average)?(?:target)?"
_RRF = r"rrf(?:required)?"
_TARGET_FREQUENCY = (
    r"(?:ftarget|ftolerable|fhmax|rmax|fallowed|fallowable)"
)
_RESIDUAL_FREQUENCY = (
    r"(?:fresidual|fd|finitiating|finit|fsource)"
)
_RELATION = r"(?:<=|>=|=|<|>)"

_CORRECTION_CONTEXT = re.compile(
    r"(?:"
    r"잘못(?:된|이다|이며|으로)"
    r"|틀린\s*(?:식|관계|표현)"
    r"|오류\s*(?:식|관계|표현|예시)?"
    r"|성립하지\s*않"
    r"|사용하면\s*안"
    r"|적용하면\s*안"
    r"|올바른\s*(?:식|관계)"
    r"|correct(?:ed|ion)?"
    r"|wrong\s*(?:formula|relation|example)"
    r")",
    flags=re.IGNORECASE,
)


def _canonical(value: Any) -> str:
    text = unicodedata.normalize(
        "NFKC",
        str(value or ""),
    ).casefold()
    replacements = (
        ("≤", "<="),
        ("≥", ">="),
        ("≦", "<="),
        ("≧", ">="),
        ("×", "*"),
        ("·", "*"),
        ("÷", "/"),
        ("\\times", "*"),
        ("\\cdot", "*"),
        ("\\leq", "<="),
        ("\\le", "<="),
        ("\\geq", ">="),
        ("\\ge", ">="),
    )
    for old, new in replacements:
        text = text.replace(old, new)

    # Formula identifiers are compared independent of OCR/LaTeX subscript
    # punctuation. Operators and parentheses remain intact.
    text = re.sub(r"[\s_{}\[\],$`]", "", text)
    return text


def _answer_lines(answer_text: Any) -> list[tuple[int, str, str]]:
    rows: list[tuple[int, str, str]] = []
    for line_number, raw_line in enumerate(
        str(answer_text or "").replace("\r", "").splitlines(),
        start=1,
    ):
        raw = raw_line.strip()
        if not raw:
            continue
        rows.append((line_number, raw, _canonical(raw)))
    return rows


def _is_corrective_context(raw_line: str) -> bool:
    return _CORRECTION_CONTEXT.search(raw_line) is not None


def _stable_finding_id(
    rule_id: str,
    line_number: int,
    evidence: str,
) -> str:
    payload = f"{rule_id}\n{line_number}\n{evidence}".encode("utf-8")
    suffix = hashlib.sha256(payload).hexdigest()[:12]
    return f"{rule_id}_{suffix}"


def _finding(
    *,
    rule_id: str,
    line_number: int,
    evidence: str,
    message: str,
    correct_rule: str,
    error_class: str,
    claim_signature: str,
    anchor_refs: list[str],
    demand_refs: list[str],
) -> dict[str, Any]:
    return {
        "id": _stable_finding_id(
            rule_id,
            line_number,
            evidence,
        ),
        "rule_id": rule_id,
        "source_rule_id": rule_id,
        "severity": "fatal",
        "message": message,
        "correct_rule": correct_rule,
        "affected_layers": ["C"],
        "recommended_ceiling": 14.5,
        "evidence": evidence[:500],
        "line_number": line_number,
        "engine": SIL_RELATION_INTEGRITY_MARKER,
        "evidence_trust_tier": "DETERMINISTIC",
        "error_class": error_class,
        "claim_signature": claim_signature,
        "anchor_refs": list(anchor_refs),
        "demand_refs": list(demand_refs),
        "diagnostic_only": False,
    }


def _contains_frequency_product_pfd(compact: str) -> bool:
    prefix = rf"{_PFD}{_RELATION}"
    target_then_source = rf"{prefix}[^/]{{0,80}}{_TARGET_FREQUENCY}[^/]{{0,40}}\*[^/]{{0,40}}{_RESIDUAL_FREQUENCY}"
    source_then_target = rf"{prefix}[^/]{{0,80}}{_RESIDUAL_FREQUENCY}[^/]{{0,40}}\*[^/]{{0,40}}{_TARGET_FREQUENCY}"
    return bool(
        re.search(target_then_source, compact)
        or re.search(source_then_target, compact)
    )


def _contains_inverse_pfd_ratio(compact: str) -> bool:
    return re.search(
        rf"{_PFD}(?:<=|=|<).{{0,60}}"
        rf"{_RESIDUAL_FREQUENCY}/(?:\()?{_TARGET_FREQUENCY}",
        compact,
    ) is not None


def _contains_inverse_rrf_ratio(compact: str) -> bool:
    return re.search(
        rf"{_RRF}=.{{0,60}}"
        rf"{_TARGET_FREQUENCY}/(?:\()?{_RESIDUAL_FREQUENCY}",
        compact,
    ) is not None


def _contains_wrong_pfd_inequality(compact: str) -> bool:
    return re.search(
        rf"{_PFD}(?:>=|>).{{0,60}}"
        rf"{_TARGET_FREQUENCY}/(?:\()?{_RESIDUAL_FREQUENCY}",
        compact,
    ) is not None


def _recognized_correct_relations(compact: str) -> list[str]:
    relations: list[str] = []
    if re.search(
        rf"{_RRF}=.{{0,60}}"
        rf"{_RESIDUAL_FREQUENCY}/(?:\()?{_TARGET_FREQUENCY}",
        compact,
    ):
        relations.append("required_rrf_residual_over_tolerable")
    if re.search(
        rf"{_PFD}(?:<=|=|<).{{0,60}}"
        rf"{_TARGET_FREQUENCY}/(?:\()?{_RESIDUAL_FREQUENCY}",
        compact,
    ):
        relations.append("target_pfd_tolerable_over_residual")
    if re.search(rf"{_PFD}(?:<=|=|<).{{0,30}}1/{_RRF}", compact):
        relations.append("target_pfd_inverse_rrf")
    return relations


def evaluate_sil_relation_integrity(
    answer_text: Any,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    recognized: list[dict[str, Any]] = []
    corrective_examples: list[dict[str, Any]] = []

    for line_number, raw_line, compact in _answer_lines(answer_text):
        checks = (
            (
                "fatal_target_pfd_frequency_product",
                _contains_frequency_product_pfd(compact),
                "목표 PFDavg를 두 빈도의 곱으로 산정하여 차원과 위험감소 관계가 틀렸습니다.",
                "저요구 모드에서는 PFDavg_target <= F_tolerable/F_residual = 1/RRF_required입니다.",
                "DIMENSION_AND_RELATION_DIRECTION",
                "target_pfd_equals_frequency_product",
                ["required_rrf_relation", "target_pfd_relation"],
                ["required_rrf_and_target_sil", "quantitative_verification_dimension"],
            ),
            (
                "fatal_target_pfd_inverse_ratio",
                _contains_inverse_pfd_ratio(compact),
                "목표 PFDavg의 잔여빈도/허용빈도 비가 역전되었습니다.",
                "PFDavg_target <= F_tolerable/F_residual이며 그 역수는 RRF_required입니다.",
                "RELATION_DIRECTION",
                "target_pfd_uses_residual_over_tolerable",
                ["required_rrf_relation", "target_pfd_relation"],
                ["required_rrf_and_target_sil", "quantitative_verification_dimension"],
            ),
            (
                "fatal_required_rrf_inverse_ratio",
                _contains_inverse_rrf_ratio(compact),
                "요구 RRF의 허용빈도/잔여빈도 비가 역전되었습니다.",
                "RRF_required = F_residual/F_tolerable입니다.",
                "RELATION_DIRECTION",
                "required_rrf_uses_tolerable_over_residual",
                ["required_rrf_relation"],
                ["required_rrf_and_target_sil"],
            ),
            (
                "fatal_target_pfd_wrong_inequality",
                _contains_wrong_pfd_inequality(compact),
                "목표 PFDavg의 허용 부등호 방향이 반대입니다.",
                "요구 위험감소를 만족하려면 PFDavg가 목표 상한 이하이어야 합니다.",
                "RELATION_DIRECTION",
                "target_pfd_uses_lower_bound",
                ["target_pfd_relation"],
                ["required_rrf_and_target_sil", "quantitative_verification_dimension"],
            ),
        )

        matched_wrong = [row for row in checks if row[1]]
        if matched_wrong and _is_corrective_context(raw_line):
            corrective_examples.append(
                {
                    "line_number": line_number,
                    "evidence": raw_line[:500],
                    "suppressed_rule_ids": [row[0] for row in matched_wrong],
                }
            )
        else:
            for (
                rule_id,
                matched,
                message,
                correct_rule,
                error_class,
                claim_signature,
                anchor_refs,
                demand_refs,
            ) in checks:
                if not matched:
                    continue
                findings.append(
                    _finding(
                        rule_id=rule_id,
                        line_number=line_number,
                        evidence=raw_line,
                        message=message,
                        correct_rule=correct_rule,
                        error_class=error_class,
                        claim_signature=claim_signature,
                        anchor_refs=anchor_refs,
                        demand_refs=demand_refs,
                    )
                )

        for relation_id in _recognized_correct_relations(compact):
            recognized.append(
                {
                    "relation_id": relation_id,
                    "line_number": line_number,
                    "evidence": raw_line[:500],
                }
            )

    deduped_findings: list[dict[str, Any]] = []
    seen_rules: set[str] = set()
    for finding in findings:
        rule_id = str(finding.get("rule_id") or "")
        if rule_id in seen_rules:
            continue
        seen_rules.add(rule_id)
        deduped_findings.append(finding)

    if deduped_findings:
        status = "fatal"
    elif recognized:
        status = "valid"
    else:
        status = "not_evaluated"

    return {
        "version": SIL_RELATION_INTEGRITY_VERSION,
        "marker": SIL_RELATION_INTEGRITY_MARKER,
        "topic_id": SIL_TARGET_TOPIC_ID,
        "applicable": True,
        "status": status,
        "fatal_error_detected": bool(deduped_findings),
        "findings": deduped_findings,
        "recognized_correct_relations": recognized,
        "corrective_examples_suppressed": corrective_examples,
        "score_policy": {
            "score_effect": "verified_fatal_ceiling",
            "recommended_ceiling": (
                14.5 if deduped_findings else None
            ),
            "affected_layers": ["C"],
            "direct_d_e_effect": "none",
            "missing_formula_penalty": False,
        },
    }
