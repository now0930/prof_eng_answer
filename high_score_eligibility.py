"""Evidence-gated high-score eligibility.

This policy is a one-way hard cap. It can prevent an unsupported score from
crossing 20/25, but it never raises A/B/C/D/E evidence-owned scores.
"""

from __future__ import annotations

import copy
from typing import Any


POLICY_VERSION = "high_score_eligibility_v1"
HIGH_SCORE_THRESHOLD = 20.0
HIGH_SCORE_CAP_WHEN_INELIGIBLE = 19.99
MINIMUM_C_RATIO = 0.75
MINIMUM_D_RATIO = 0.70


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _layer_rows(value: Any) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in value if isinstance(value, list) else []:
        if not isinstance(row, dict):
            continue
        layer = str(row.get("layer_id") or row.get("layer") or "").upper()
        if layer in {"A", "B", "C", "D", "E"} and layer not in output:
            output[layer] = row
    return output


def _base_score(grade: dict[str, Any]) -> float | None:
    rows = _layer_rows(grade.get("breakdown"))
    if set(rows) != {"A", "B", "C", "D", "E"}:
        rows = _layer_rows(grade.get("layer_scores"))
    if set(rows) != {"A", "B", "C", "D", "E"}:
        return None
    scores = [_number(rows[layer].get("score")) for layer in "ABCDE"]
    if any(score is None for score in scores):
        return None
    return round(sum(score for score in scores if score is not None), 2)


def _layer_ratio(grade: dict[str, Any], layer: str) -> float | None:
    rows = _layer_rows(grade.get("breakdown"))
    if layer not in rows:
        rows = _layer_rows(grade.get("layer_scores"))
    row = rows.get(layer)
    if not isinstance(row, dict):
        return None
    score = _number(row.get("score"))
    maximum = _number(row.get("max") or row.get("max_score"))
    if score is None or maximum is None or maximum <= 0:
        return None
    return score / maximum


def _hard_defect_present(grade: dict[str, Any]) -> bool:
    for container_key, row_key in (
        ("logic_check_evaluation", "findings"),
        ("general_evidence_contract", "defects"),
    ):
        container = grade.get(container_key)
        rows = container.get(row_key) if isinstance(container, dict) else []
        if any(
            isinstance(row, dict)
            and str(row.get("severity") or "").casefold() in {"major", "fatal"}
            and (
                container_key == "logic_check_evaluation"
                or str(row.get("defect_type") or "").casefold() == "correctness_error"
            )
            for row in rows if isinstance(rows, list)
        ):
            return True
    return False


def _field_judgement_evidence(grade: dict[str, Any]) -> bool:
    """Require structured condition -> judgment -> verification evidence for D."""

    candidates = (
        grade.get("field_application_evidence")
        or grade.get("engineering_judgement_evidence")
        or []
    )
    for row in candidates if isinstance(candidates, list) else []:
        if isinstance(row, dict) and all(
            str(row.get(key) or "").strip()
            for key in ("field_condition", "engineering_judgement", "verification_method")
        ):
            return True
    return False


def _core_row_has_high_band_evidence(row: dict[str, Any], *, projection_valid: bool) -> bool:
    for item in row.get("evidence", []):
        if not isinstance(item, dict):
            continue
        if any(str(item.get(key) or "").strip() for key in (
            "quote_span", "answer_span", "source_span",
        )):
            return True
        if (
            projection_valid
            and item.get("exact_requirement_id") is True
            and str(item.get("status") or "") == "correct"
        ):
            return True
    return False


def evaluate_high_score_eligibility(grade: Any) -> dict[str, Any]:
    if not isinstance(grade, dict):
        return {"eligible": False, "reasons": ["grade_not_mapping"]}
    ledger = grade.get("canonical_evaluation_ledger")
    rows = ledger.get("rows") if isinstance(ledger, dict) else []
    core_rows = [row for row in rows if isinstance(row, dict) and row.get("is_core", True)]
    projection = grade.get("explicit_requirement_projection_validation")
    projection_valid = isinstance(projection, dict) and projection.get("valid") is True
    core_evidence_complete = bool(core_rows) and all(
        row.get("correctness_status", row.get("status")) == "correct"
        and _core_row_has_high_band_evidence(
            row, projection_valid=projection_valid,
        )
        for row in core_rows
    )
    base_score = _base_score(grade)
    c_ratio = _layer_ratio(grade, "C")
    d_ratio = _layer_ratio(grade, "D")
    reasons = []
    if base_score is None or base_score < HIGH_SCORE_THRESHOLD:
        reasons.append("base_score_below_high_band")
    if not core_evidence_complete:
        reasons.append("core_requirement_evidence_incomplete")
    if _hard_defect_present(grade):
        reasons.append("major_or_fatal_correctness_defect")
    if c_ratio is None or c_ratio < MINIMUM_C_RATIO:
        reasons.append("C_evidence_ratio_below_minimum")
    if d_ratio is None or d_ratio < MINIMUM_D_RATIO:
        reasons.append("D_evidence_ratio_below_minimum")
    if not _field_judgement_evidence(grade):
        reasons.append("D_field_condition_judgement_verification_evidence_missing")
    return {
        "version": POLICY_VERSION,
        "base_score": base_score,
        "C_ratio": round(c_ratio, 4) if c_ratio is not None else None,
        "D_ratio": round(d_ratio, 4) if d_ratio is not None else None,
        "core_requirement_evidence_complete": core_evidence_complete,
        "field_judgement_evidence_present": _field_judgement_evidence(grade),
        "eligible": not reasons,
        "reasons": reasons,
    }


def apply_high_score_eligibility_cap(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    output = copy.deepcopy(payload)
    total = _number(output.get("total_score"))
    decision = evaluate_high_score_eligibility(output)
    cap_applied = bool(total is not None and total >= HIGH_SCORE_THRESHOLD and not decision["eligible"])
    if cap_applied:
        cap = min(
            HIGH_SCORE_CAP_WHEN_INELIGIBLE,
            decision["base_score"] if decision["base_score"] is not None else HIGH_SCORE_CAP_WHEN_INELIGIBLE,
        )
        for key in ("total_score", "final_total_score", "final_score", "score", "total"):
            if key in output or key in {"total_score", "final_total_score"}:
                output[key] = cap
        caps = output.get("applied_caps")
        caps = list(caps) if isinstance(caps, list) else []
        caps.append({
            "type": "high_score_evidence_eligibility",
            "cap": cap,
            "reason_codes": decision["reasons"],
            "score_effect": "hard_cap",
        })
        output["applied_caps"] = caps
    decision["cap_applied"] = cap_applied
    decision["cap"] = (
        min(
            HIGH_SCORE_CAP_WHEN_INELIGIBLE,
            decision["base_score"] if decision["base_score"] is not None else HIGH_SCORE_CAP_WHEN_INELIGIBLE,
        )
        if cap_applied else None
    )
    decision["score_effect"] = "hard_cap" if cap_applied else "none"
    output["high_score_eligibility"] = decision
    return output
