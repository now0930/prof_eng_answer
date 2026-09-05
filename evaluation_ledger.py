"""Canonical, topic-neutral evaluation ledger.

The ledger is a projection, not another grader.  It combines the immutable
question-demand contract, semantic coverage, and verified defects into one
row per atomic requirement.  It never changes numeric scores.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any


EVALUATION_LEDGER_SCHEMA_VERSION = "1.0"
EVALUATION_LEDGER_MARKER = "CANONICAL_EVALUATION_LEDGER_V1"

_STATUSES = {
    # Provider coverage contracts define ``present`` as directly addressed,
    # technically correct, and sufficiently complete.  The ledger still
    # requires exact requirement identity plus evidence before preserving it
    # as ``correct`` (see ``_evidence_from_coverage``).
    "present": "correct",
    "correct": "correct",
    "partial": "partial",
    "incorrect": "incorrect",
    "wrong": "incorrect",
    "contradicted": "incorrect",
    "missing": "missing",
    "absent": "missing",
}
_STATUS_ORDER = {
    "unknown": 0,
    "correct": 1,
    "partial": 2,
    "missing": 3,
    "incorrect": 4,
}
_SCORE_FIELDS = (
    "score",
    "total_score",
    "final_total_score",
    "final_score",
    "raw_total_score",
    "adjusted_total_score",
    "uncapped_total_score",
    "score_range",
    "layer_scores",
    "breakdown",
    "applied_caps",
)

_DEMAND_LINK_STOPWORDS = {
    "관점", "관련", "대한", "방안", "설명", "제시", "정의", "적용",
    "검토", "평가", "수행", "올바른", "그리고", "또는", "으로",
    "한다", "하다", "있게", "전체", "요구", "결정", "목표",
    "the", "and", "for", "with", "from", "into",
}
_DEMAND_ACTION_SUFFIXES = (
    "설명하시오", "제시하시오", "비교하시오", "해석하시오",
    "설명", "제시", "비교", "정의", "적용", "검토", "평가", "방안",
)


def _score_snapshot(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value.get(key))
        for key in _SCORE_FIELDS
        if key in value
    }


def _nested(value: dict[str, Any], key: str) -> dict[str, Any]:
    direct = value.get(key)
    if isinstance(direct, dict):
        return direct
    parsed = value.get("parsed")
    if isinstance(parsed, dict):
        nested = parsed.get(key)
        if isinstance(nested, dict):
            return nested
    return {}


def _normalise_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def _compact_link_text(value: Any) -> str:
    return re.sub(
        r"[^0-9a-zA-Z가-힣λ]+",
        "",
        str(value or "").casefold(),
    )


def _demand_link_tokens(value: Any) -> set[str]:
    return {
        token
        for token in re.findall(
            r"[0-9a-zA-Z가-힣λ]+",
            str(value or "").casefold(),
        )
        if (
            token not in _DEMAND_LINK_STOPWORDS
            and (len(token) >= 2 or token == "λ")
        )
    }


def _demand_link_phrase(requirement: dict[str, Any]) -> str:
    raw = str(
        requirement.get("object_text")
        or requirement.get("requirement_text")
        or ""
    ).strip()
    for suffix in _DEMAND_ACTION_SUFFIXES:
        raw = re.sub(rf"\s*{re.escape(suffix)}\s*$", "", raw).strip()
    compact = _compact_link_text(raw)
    return compact if len(compact) >= 4 else ""


def _infer_defect_requirement_links(
    defects: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Link unreferenced verified defects only on unique lexical evidence.

    Explicit source-owned requirement IDs always win.  This fallback is
    diagnostic and score-neutral; ambiguity leaves the defect unresolved.
    """

    output: list[dict[str, Any]] = []
    valid_requirements = [row for row in requirements if isinstance(row, dict)]
    for raw_defect in defects:
        defect = copy.deepcopy(raw_defect)
        if str(defect.get("requirement_id") or "").strip():
            output.append(defect)
            continue

        primary_evidence = " ".join(
            str(defect.get(key) or "")
            for key in ("evidence", "evidence_text")
        )
        explanation = " ".join(
            str(defect.get(key) or "")
            for key in ("explanation", "correct_rule")
        )
        evidence = f"{primary_evidence} {explanation}".strip()
        compact_primary = _compact_link_text(primary_evidence)
        compact_explanation = _compact_link_text(explanation)
        evidence_tokens = _demand_link_tokens(evidence)
        candidates: list[tuple[int, str, str, list[str]]] = []
        for requirement in valid_requirements:
            requirement_id = str(
                requirement.get("requirement_id") or ""
            ).strip()
            if not requirement_id:
                continue
            phrase = _demand_link_phrase(requirement)
            overlap = sorted(
                evidence_tokens
                & _demand_link_tokens(
                    " ".join(
                        str(requirement.get(key) or "")
                        for key in ("object_text", "requirement_text")
                    )
                )
            )
            exact_primary = bool(phrase and phrase in compact_primary)
            exact_explanation = bool(phrase and phrase in compact_explanation)
            exact_phrase = exact_primary or exact_explanation
            if not exact_phrase and len(overlap) < 2:
                continue
            score = 200 if exact_primary else (100 if exact_explanation else len(overlap))
            candidates.append((score, requirement_id, "exact_phrase" if exact_phrase else "token_overlap", overlap))

        candidates.sort(key=lambda row: (-row[0], row[1]))
        if candidates and (
            len(candidates) == 1 or candidates[0][0] > candidates[1][0]
        ):
            _, requirement_id, method, overlap = candidates[0]
            defect["requirement_id"] = requirement_id
            defect["requirement_link"] = {
                "method": method,
                "matched_tokens": overlap,
                "score_effect": "none",
            }
        output.append(defect)
    return output


def _status(value: Any) -> str:
    return _STATUSES.get(str(value or "").strip().casefold(), "unknown")


def _stable_id(prefix: str, value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"{prefix}_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:12]}"


def _coverage_rows(grade: dict[str, Any]) -> list[dict[str, Any]]:
    coverage = _nested(grade, "question_type_coverage")
    explicit = coverage.get("explicit_requirement_coverage")
    rows = explicit.get("requirements") if isinstance(explicit, dict) else None
    output = (
        [copy.deepcopy(row) for row in rows if isinstance(row, dict)]
        if isinstance(rows, list)
        else []
    )
    if output:
        return output

    projection = _nested(grade, "native_question_demand_projection_v1")
    states = projection.get("states")
    if not isinstance(states, list):
        return []
    state_status = {
        0: "missing",
        1: "partial",
        2: "partial",
        3: "correct",
    }
    for row in states:
        if not isinstance(row, dict):
            continue
        state = row.get("state")
        if isinstance(state, bool) or state not in state_status:
            continue
        output.append({
            "requirement_id": row.get("demand_id"),
            "requirement_text": row.get("text"),
            "status": state_status[state],
            "evidence": "",
            "coverage_source": "native_question_demand_projection_v1",
        })
    return output


def _verified_defects(grade: dict[str, Any]) -> list[dict[str, Any]]:
    contract = _nested(grade, "general_evidence_contract")
    rows = contract.get("defects")
    defects = [
        copy.deepcopy(row)
        for row in (rows if isinstance(rows, list) else [])
        if isinstance(row, dict)
        and str(row.get("defect_type") or "").casefold() == "correctness_error"
        and str(row.get("severity") or "").casefold() in {"major", "fatal"}
        and str(row.get("owner_layer") or "C").upper() == "C"
    ]
    logic = _nested(grade, "logic_check_evaluation")
    demand_contract = _nested(grade, "question_demand_contract")
    requirements = [
        row for row in (demand_contract.get("requirements") or [])
        if isinstance(row, dict)
    ]
    findings = logic.get("findings")
    for finding in findings if isinstance(findings, list) else []:
        if not isinstance(finding, dict):
            continue
        severity = str(finding.get("severity") or "").casefold()
        if severity not in {"major", "fatal"}:
            continue
        finding_id = str(
            finding.get("rule_id")
            or finding.get("source_rule_id")
            or finding.get("finding_id")
            or finding.get("id")
            or ""
        ).strip()
        demand_refs = finding.get("demand_refs")
        resolved_refs = [
            str(value).strip() for value in demand_refs
            if str(value).strip()
        ] if isinstance(demand_refs, list) else []
        for raw_term in (
            finding.get("demand_ref_terms")
            if isinstance(finding.get("demand_ref_terms"), list)
            else []
        ):
            term = _compact_link_text(raw_term)
            if not term:
                continue
            matches = [
                str(requirement.get("requirement_id") or "").strip()
                for requirement in requirements
                if str(requirement.get("requirement_id") or "").strip()
                and term in _compact_link_text(
                    " ".join(str(requirement.get(key) or "") for key in (
                        "object_text", "requirement_text",
                    ))
                )
            ]
            if len(matches) == 1 and matches[0] not in resolved_refs:
                resolved_refs.append(matches[0])
        requirement_ids = (
            resolved_refs
            if resolved_refs
            else [""]
        )
        for requirement_id in requirement_ids:
            requirement_id = str(requirement_id or "").strip()
            projected = {
                "defect_id": finding_id,
                "source_finding_id": finding_id,
                "requirement_id": requirement_id,
                "defect_type": "correctness_error",
                "severity": severity,
                "owner_layer": "C",
                "evidence": str(finding.get("evidence") or "").strip(),
                "explanation": str(
                    finding.get("message") or finding.get("correct_rule") or ""
                ).strip(),
                "correct_rule": str(finding.get("correct_rule") or "").strip(),
                "trust_tier": str(
                    finding.get("evidence_trust_tier") or "DETERMINISTIC"
                ),
            }
            identity = (finding_id, requirement_id)
            if any(
                (
                    str(row.get("defect_id") or row.get("source_finding_id") or ""),
                    str(row.get("requirement_id") or ""),
                ) == identity
                for row in defects
            ):
                continue
            defects.append(projected)
    return defects


def _coverage_match(
    requirement: dict[str, Any],
    rows: list[dict[str, Any]],
    consumed: set[int],
) -> int | None:
    requirement_id = str(requirement.get("requirement_id") or "").strip()
    if requirement_id:
        exact = [
            index for index, row in enumerate(rows)
            if index not in consumed
            and str(row.get("requirement_id") or "").strip() == requirement_id
        ]
        if len(exact) == 1:
            return exact[0]

    text = _normalise_text(requirement.get("requirement_text"))
    if text:
        exact_text = [
            index for index, row in enumerate(rows)
            if index not in consumed
            and _normalise_text(
                row.get("requirement_text")
                or row.get("requirement")
                or row.get("criterion")
            ) == text
        ]
        if len(exact_text) == 1:
            return exact_text[0]

    # Generic semantic providers may omit generated requirement IDs and the
    # trailing action word (for example, "설명").  A normalized demand phrase
    # is still a canonical identity only when it selects exactly one row.
    phrase = _demand_link_phrase(requirement)
    if phrase:
        phrase_matches = [
            index for index, row in enumerate(rows)
            if index not in consumed
            and _demand_link_phrase({
                "requirement_text": (
                    row.get("requirement_text")
                    or row.get("requirement")
                    or row.get("criterion")
                )
            }) == phrase
        ]
        if len(phrase_matches) == 1:
            return phrase_matches[0]

    # Provider coverage often omits the action suffix ("설명", "제시") or
    # qualifies a short object (for example "특징").  Accept only a unique
    # object/containment match so this fallback cannot guess ambiguously.
    object_text = _compact_link_text(requirement.get("object_text"))
    if object_text:
        candidates = []
        for index, row in enumerate(rows):
            if index in consumed:
                continue
            row_text = _compact_link_text(
                row.get("requirement_text")
                or row.get("requirement")
                or row.get("criterion")
            )
            if row_text and (object_text == row_text or object_text in row_text):
                candidates.append(index)
        if len(candidates) == 1:
            return candidates[0]
    return None


def _semantic_score_ratio(grade: dict[str, Any]) -> float | None:
    evaluation = _nested(grade, "gemini_semantic_evaluation")
    parsed = evaluation.get("parsed")
    if not isinstance(parsed, dict):
        return None
    layers = parsed.get("layers")
    if isinstance(layers, list) and layers:
        score = 0.0
        maximum = 0.0
        for row in layers:
            if not isinstance(row, dict):
                continue
            row_score = row.get("score")
            row_max = row.get("max")
            if (
                isinstance(row_score, (int, float))
                and not isinstance(row_score, bool)
                and isinstance(row_max, (int, float))
                and not isinstance(row_max, bool)
                and row_max > 0
            ):
                score += float(row_score)
                maximum += float(row_max)
        return score / maximum if maximum > 0 else None
    score = parsed.get("score")
    maximum = parsed.get("max")
    if (
        isinstance(score, (int, float))
        and not isinstance(score, bool)
        and isinstance(maximum, (int, float))
        and not isinstance(maximum, bool)
        and maximum > 0
    ):
        return float(score) / float(maximum)
    return None


def _reconcile_high_confidence_long_form_states(
    grade: dict[str, Any],
    rows: list[dict[str, Any]],
    defects: list[dict[str, Any]],
) -> dict[str, Any]:
    # Whole-answer length and aggregate semantic scores are not evidence for a
    # particular atomic requirement. Retain the old marker for auditability,
    # but never mutate requirement state.
    _ = grade, rows, defects
    return {
        "marker": "HIGH_CONFIDENCE_SEMANTIC_LONG_FORM_RECONCILIATION_V1",
        "applied": False,
        "score_effect": "none",
        "reason": "whole_answer_signals_cannot_upgrade_atomic_requirement_state",
        "upgraded_requirement_ids": [],
    }


def _evidence_from_coverage(
    row: dict[str, Any],
    *,
    canonical_requirement_id: str,
    canonical_identity_verified: bool = False,
) -> dict[str, Any]:
    verified_ids = sorted({
        str(value).strip()
        for value in row.get("verified_defect_ids", [])
        if str(value).strip()
    }) if isinstance(row.get("verified_defect_ids"), list) else []
    raw_status = str(row.get("status") or "").strip().casefold()
    evidence_text = str(row.get("evidence") or "").strip()
    provided_requirement_id = str(row.get("requirement_id") or "").strip()
    exact_requirement_id = bool(
        provided_requirement_id
        and provided_requirement_id == canonical_requirement_id
    ) or canonical_identity_verified
    if verified_ids:
        status = "incorrect"
    elif raw_status == "correct" and (evidence_text or exact_requirement_id):
        status = "correct"
    elif raw_status == "present" and exact_requirement_id and evidence_text:
        status = "correct"
    elif raw_status == "partial":
        status = "partial"
    elif raw_status in {"present", "correct"} and evidence_text:
        status = "partial"
    elif raw_status in {"missing", "absent"}:
        status = "missing"
    else:
        status = "unknown"
    source_kind = "verified_defect_reconciliation" if verified_ids else "semantic_coverage"
    trust_tier = "verified_structured" if verified_ids else "semantic_inferred"
    payload = {
        "source_kind": source_kind,
        "source_id": verified_ids or canonical_requirement_id,
        "trust_tier": trust_tier,
        "status": status,
        "evidence": evidence_text,
        "provided_requirement_id": provided_requirement_id,
        "canonical_requirement_id": canonical_requirement_id,
        "exact_requirement_id": exact_requirement_id,
    }
    payload["evidence_id"] = _stable_id("evidence", payload)
    return payload


def _defects_by_requirement(defects: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for defect in defects:
        requirement_id = str(defect.get("requirement_id") or "").strip()
        if requirement_id:
            result.setdefault(requirement_id, []).append(defect)
    return result


def _defect_evidence(defect: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "source_kind": "verified_defect",
        "source_id": str(defect.get("defect_id") or defect.get("source_finding_id") or "").strip(),
        "trust_tier": "verified_structured",
        "status": "incorrect",
        "severity": str(defect.get("severity") or "").strip().casefold(),
        "evidence": str(defect.get("explanation") or defect.get("evidence") or "").strip(),
    }
    payload["evidence_id"] = _stable_id("evidence", payload)
    return payload


def build_canonical_evaluation_ledger(grade: Any) -> dict[str, Any]:
    if not isinstance(grade, dict):
        return {
            "schema_version": EVALUATION_LEDGER_SCHEMA_VERSION,
            "marker": EVALUATION_LEDGER_MARKER,
            "status": "unavailable",
            "reason": "grade_not_mapping",
            "score_effect": "none",
            "rows": [],
        }

    contract = _nested(grade, "question_demand_contract")
    requirements = contract.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        return {
            "schema_version": EVALUATION_LEDGER_SCHEMA_VERSION,
            "marker": EVALUATION_LEDGER_MARKER,
            "status": "unavailable",
            "reason": "question_demand_contract_missing",
            "score_effect": "none",
            "rows": [],
        }

    coverage_rows = _coverage_rows(grade)
    canonical_ids = [
        str(row.get("requirement_id") or "").strip()
        for row in requirements if isinstance(row, dict)
    ]
    provider_ids = [
        str(row.get("requirement_id") or "").strip()
        for row in coverage_rows if str(row.get("requirement_id") or "").strip()
    ]
    provider_positions = [
        canonical_ids.index(requirement_id)
        for requirement_id in provider_ids
        if requirement_id in canonical_ids
    ]
    coverage_mapping_valid = bool(
        not provider_ids
        or (
            len(provider_positions) == len(provider_ids)
            and len(provider_ids) == len(set(provider_ids))
            and provider_positions == sorted(provider_positions)
        )
    )
    active_coverage_rows = coverage_rows if coverage_mapping_valid else []
    defects = _infer_defect_requirement_links(
        _verified_defects(grade),
        requirements,
    )
    defects_by_requirement = _defects_by_requirement(defects)
    consumed: set[int] = set()
    rows: list[dict[str, Any]] = []

    for index, requirement in enumerate(requirements, start=1):
        if not isinstance(requirement, dict):
            continue
        requirement_id = str(requirement.get("requirement_id") or "").strip()
        if not requirement_id:
            requirement_id = _stable_id("requirement", {
                "index": index,
                "text": requirement.get("requirement_text"),
            })
        evidence: list[dict[str, Any]] = []
        coverage_index = _coverage_match(requirement, active_coverage_rows, consumed)
        if coverage_index is not None:
            consumed.add(coverage_index)
            coverage_row = active_coverage_rows[coverage_index]
            provided_requirement_id = str(
                coverage_row.get("requirement_id") or ""
            ).strip()
            canonical_identity_verified = bool(
                provided_requirement_id == requirement_id
                or (
                    not provided_requirement_id
                    and _demand_link_phrase(requirement)
                    and _demand_link_phrase(requirement)
                    == _demand_link_phrase({
                        "requirement_text": (
                            coverage_row.get("requirement_text")
                            or coverage_row.get("requirement")
                            or coverage_row.get("criterion")
                        )
                    })
                )
            )
            evidence.append(_evidence_from_coverage(
                coverage_row,
                canonical_requirement_id=requirement_id,
                canonical_identity_verified=canonical_identity_verified,
            ))
        evidence.extend(
            _defect_evidence(defect)
            for defect in defects_by_requirement.get(requirement_id, [])
        )
        statuses = [item["status"] for item in evidence if item["status"] != "unknown"]
        resolved = max(statuses, key=lambda value: _STATUS_ORDER[value]) if statuses else "unknown"
        unique_statuses = sorted(set(statuses), key=lambda value: _STATUS_ORDER[value])
        correctness_status = resolved
        addressing_status = (
            "missing" if correctness_status == "missing"
            else "substantive" if any(item.get("evidence") for item in evidence)
            else "mentioned" if evidence
            else "missing"
        )
        evidence_quality = (
            "deterministic" if any(item["trust_tier"] == "verified_structured" for item in evidence)
            else "semantic_inferred" if any(item.get("evidence") for item in evidence)
            else "none"
        )
        rows.append({
            "requirement_id": requirement_id,
            "requirement_index": index,
            "requirement_text": str(requirement.get("requirement_text") or "").strip(),
            "demand_kind": str(requirement.get("demand_kind") or "").strip(),
            "is_core": bool(requirement.get("is_core", True)),
            "status": correctness_status,
            "addressing_status": addressing_status,
            "correctness_status": correctness_status,
            "evidence_quality": evidence_quality,
            "depth_level": addressing_status,
            "mentioned": addressing_status in {"mentioned", "substantive"},
            "status_owner": (
                "verified_defect" if any(item["trust_tier"] == "verified_structured" for item in evidence)
                else ("semantic_coverage" if evidence else "unassessed")
            ),
            "score_ownership": {
                "completeness": "B",
                "correctness": "C",
                "double_deduction_allowed": False,
            },
            "conflict": len(unique_statuses) > 1,
            "observed_statuses": unique_statuses,
            "evidence": evidence,
        })

    state_reconciliation = _reconcile_high_confidence_long_form_states(
        grade,
        rows,
        defects,
    )

    counts = {name: 0 for name in _STATUS_ORDER}
    for row in rows:
        counts[row["status"]] += 1
    total = len(rows)
    assessed = total - counts["unknown"]
    unmatched_coverage = [
        copy.deepcopy(row)
        for index, row in enumerate(coverage_rows)
        if not coverage_mapping_valid or index not in consumed
    ]
    referenced_defect_ids: set[str] = set()
    for row in rows:
        for item in row["evidence"]:
            if item.get("source_kind") not in {
                "verified_defect",
                "verified_defect_reconciliation",
            }:
                continue
            source_id = item.get("source_id")
            values = source_id if isinstance(source_id, list) else [source_id]
            referenced_defect_ids.update(
                str(value).strip() for value in values if str(value).strip()
            )
    unresolved_defects = [
        copy.deepcopy(defect)
        for defect in defects
        if str(defect.get("defect_id") or defect.get("source_finding_id") or "")
        not in referenced_defect_ids
    ]
    complete = bool(
        total
        and counts["unknown"] == 0
        and not unresolved_defects
    )
    exact_ratio = round(counts["correct"] / total, 4) if complete else None
    return {
        "schema_version": EVALUATION_LEDGER_SCHEMA_VERSION,
        "marker": EVALUATION_LEDGER_MARKER,
        "status": "complete" if complete else "incomplete",
        "canonical_owner": "canonical_evaluation_ledger",
        "question_hash": str(contract.get("question_hash") or ""),
        "question_demand_contract_marker": str(contract.get("contract_marker") or ""),
        "score_effect": "none",
        "rows": rows,
        "summary": {
            "total": total,
            "assessed": assessed,
            "complete_assessment": complete,
            "status_counts": counts,
            "exact_requirement_fulfillment_ratio": exact_ratio,
            "exact_requirement_fulfillment_percent": (
                round(exact_ratio * 100.0, 1) if exact_ratio is not None else None
            ),
            "conflict_count": sum(1 for row in rows if row["conflict"]),
            "unmatched_coverage_count": len(unmatched_coverage),
            "unresolved_verified_defect_count": len(unresolved_defects),
            "coverage_mapping_valid": coverage_mapping_valid,
        },
        "unmatched_coverage": unmatched_coverage,
        "coverage_mapping_validation": {
            "valid": coverage_mapping_valid,
            "canonical_requirement_ids": canonical_ids,
            "provider_requirement_ids": provider_ids,
            "mode": "fail_closed" if not coverage_mapping_valid else "exact_or_unique_text",
        },
        "unresolved_verified_defects": unresolved_defects,
        "state_reconciliation": state_reconciliation,
        "ownership_policy": {
            "question_demands": "question_demand_contract",
            "demand_status": "canonical_evaluation_ledger",
            "completeness_score": "B",
            "correctness_score": "C",
            "numeric_score": "A_B_C_D_E_layers",
        },
    }


def attach_canonical_evaluation_ledger(
    grade: Any,
    *,
    question_text: str = "",
) -> Any:
    if not isinstance(grade, dict):
        return grade
    output = copy.deepcopy(grade)
    before = _score_snapshot(output)
    if not _nested(output, "question_demand_contract") and question_text.strip():
        from question_demand_contract import build_question_demand_contract

        contract = build_question_demand_contract(question_text)
        output["question_demand_contract"] = contract
        parsed = output.get("parsed")
        if isinstance(parsed, dict):
            parsed["question_demand_contract"] = copy.deepcopy(contract)
    ledger = build_canonical_evaluation_ledger(output)
    output["canonical_evaluation_ledger"] = ledger
    parsed = output.get("parsed")
    if isinstance(parsed, dict):
        parsed["canonical_evaluation_ledger"] = copy.deepcopy(ledger)
    if before != _score_snapshot(output):
        raise RuntimeError("Canonical evaluation ledger changed numeric score state")
    return output
