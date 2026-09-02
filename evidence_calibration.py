"""Evidence-based confidence and strong-verdict calibration.

This final gate discovers no facts and changes no numeric score.  It derives
public confidence and verdict ceilings only from the canonical ledger and
already-persisted validation evidence.
"""

from __future__ import annotations

import copy
from typing import Any


EVIDENCE_CALIBRATION_VERSION = "evidence_calibration_v1"
EVIDENCE_CALIBRATION_MARKER = "EVIDENCE_BASED_CALIBRATION_V1"

_CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}
_STRONG_VALUES = {
    "strong",
    "excellent",
    "high",
    "full",
    "우수",
    "강함",
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


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _score_snapshot(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value.get(key))
        for key in _SCORE_FIELDS
        if key in value
    }


def _contract(value: dict[str, Any], key: str) -> dict[str, Any]:
    direct = value.get(key)
    if isinstance(direct, dict):
        return direct
    parsed = value.get("parsed")
    if isinstance(parsed, dict):
        nested = parsed.get(key)
        if isinstance(nested, dict):
            return nested
    return {}


def _hard_defect_present(value: dict[str, Any]) -> bool:
    contract = _contract(value, "general_evidence_contract")
    defects = contract.get("defects")
    if not isinstance(defects, list):
        return False
    return any(
        isinstance(row, dict)
        and str(row.get("defect_type") or "").casefold() == "correctness_error"
        and str(row.get("severity") or "").casefold() in {"major", "fatal"}
        for row in defects
    )


def _fatal_present(value: dict[str, Any]) -> bool:
    logic = _dict(
        value.get("logic_check_evaluation")
        or value.get("logic_check_result")
        or value.get("logic_check")
    )
    if logic.get("fatal") is True or logic.get("fatal_error_detected") is True:
        return True
    findings = logic.get("findings")
    if isinstance(findings, list) and any(
        isinstance(row, dict)
        and str(row.get("severity") or "").casefold() == "fatal"
        for row in findings
    ):
        return True
    contract = _contract(value, "general_evidence_contract")
    defects = contract.get("defects")
    return isinstance(defects, list) and any(
        isinstance(row, dict)
        and str(row.get("defect_type") or "").casefold() == "correctness_error"
        and str(row.get("severity") or "").casefold() == "fatal"
        for row in defects
    )


def _projection_valid(value: dict[str, Any]) -> bool:
    validation = _contract(
        value,
        "explicit_requirement_projection_validation",
    )
    return validation.get("valid") is True


def _boundary_manual_review(value: dict[str, Any]) -> bool:
    boundary = _contract(value, "grading_boundary_evaluation")
    return boundary.get("manual_review_required") is True


def _ledger_signals(value: dict[str, Any]) -> dict[str, Any]:
    ledger = _contract(value, "canonical_evaluation_ledger")
    summary = _dict(ledger.get("summary"))
    counts = _dict(summary.get("status_counts"))
    rows = ledger.get("rows")
    rows = rows if isinstance(rows, list) else []
    semantic_evidence_present = any(
        isinstance(row, dict)
        and row.get("status_owner") == "semantic_coverage"
        for row in rows
    )
    return {
        "available": ledger.get("marker") == "CANONICAL_EVALUATION_LEDGER_V1"
        and ledger.get("status") != "unavailable",
        "complete": summary.get("complete_assessment") is True,
        "correct": int(counts.get("correct") or 0),
        "partial": int(counts.get("partial") or 0),
        "incorrect": int(counts.get("incorrect") or 0),
        "missing": int(counts.get("missing") or 0),
        "unknown": int(counts.get("unknown") or 0),
        "total": int(summary.get("total") or 0),
        "conflicts": int(summary.get("conflict_count") or 0),
        "unmatched": int(summary.get("unmatched_coverage_count") or 0),
        "unresolved_defects": int(
            summary.get("unresolved_verified_defect_count") or 0
        ),
        "semantic_evidence_present": semantic_evidence_present,
    }


def _confidence_ceiling(
    signals: dict[str, Any],
    *,
    projection_valid: bool,
    manual_review: bool,
    fatal: bool,
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    ceiling = "high"
    if not signals["available"]:
        return "low", ["canonical_ledger_unavailable"]
    if not signals["complete"] or signals["unknown"]:
        return "low", ["atomic_requirement_assessment_incomplete"]
    if signals["unresolved_defects"]:
        return "low", ["verified_defect_unresolved"]
    if signals["unmatched"]:
        ceiling = "medium"
        reasons.append("coverage_not_exactly_mapped")
    if signals["conflicts"]:
        ceiling = "medium"
        reasons.append("evidence_conflict_resolved_by_precedence")
    if signals["semantic_evidence_present"] and not projection_valid:
        ceiling = "medium"
        reasons.append("semantic_evidence_without_exact_projection_validation")
    if manual_review:
        ceiling = "medium"
        reasons.append("question_answer_boundary_manual_review")
    if fatal:
        ceiling = "medium"
        reasons.append("verified_fatal_confidence_cap")
    return ceiling, list(dict.fromkeys(reasons))


def _cap_confidence(container: dict[str, Any], ceiling: str) -> list[str]:
    changed = []
    for key in ("confidence", "grade_confidence", "confidence_level"):
        current = str(container.get(key) or "").strip().casefold()
        if current not in _CONFIDENCE_RANK:
            continue
        if _CONFIDENCE_RANK[current] > _CONFIDENCE_RANK[ceiling]:
            container[key] = ceiling
            changed.append(key)
    return changed


def _restrict_strong_values(container: dict[str, Any], replacement: str) -> list[str]:
    changed = []
    for key in (
        "verdict",
        "overall_verdict",
        "headline",
        "answer_level",
        "overall_level",
    ):
        value = container.get(key)
        if isinstance(value, str) and value.strip().casefold() in _STRONG_VALUES:
            container[key] = replacement
            changed.append(key)
    for key in ("question_type_coverage", "question_type_coverage_summary"):
        coverage = container.get(key)
        if not isinstance(coverage, dict):
            continue
        for field in ("overall_coverage", "coverage", "verdict", "status"):
            value = coverage.get(field)
            if isinstance(value, str) and value.strip().casefold() in _STRONG_VALUES:
                coverage[field] = replacement
                changed.append(f"{key}.{field}")
    return changed


def apply_evidence_based_calibration(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    output = copy.deepcopy(payload)
    before = _score_snapshot(output)
    previous = _dict(output.get("evidence_based_calibration"))
    signals = _ledger_signals(output)
    fatal = _fatal_present(output)
    hard_defect = _hard_defect_present(output) or fatal
    projection_valid = _projection_valid(output)
    manual_review = _boundary_manual_review(output)
    ceiling, reasons = _confidence_ceiling(
        signals,
        projection_valid=projection_valid,
        manual_review=manual_review,
        fatal=fatal,
    )
    confidence_fields = _cap_confidence(output, ceiling)
    parsed = output.get("parsed")
    if isinstance(parsed, dict):
        confidence_fields.extend(
            f"parsed.{key}" for key in _cap_confidence(parsed, ceiling)
        )
    confidence_fields = list(dict.fromkeys(
        [
            str(value)
            for value in previous.get("confidence_fields_changed", [])
            if str(value)
        ]
        + confidence_fields
    ))

    strong_allowed = bool(
        signals["available"]
        and signals["complete"]
        and signals["total"] > 0
        and signals["correct"] == signals["total"]
        and not signals["partial"]
        and not signals["incorrect"]
        and not signals["missing"]
        and not signals["unknown"]
        and not signals["unmatched"]
        and not signals["unresolved_defects"]
        and not hard_defect
        and projection_valid
    )
    verdict_fields: list[str] = []
    output["strong_verdict_allowed"] = strong_allowed
    if not strong_allowed:
        replacement = (
            "unknown"
            if not signals["available"] or not signals["complete"]
            else "needs_correction"
        )
        verdict_fields.extend(_restrict_strong_values(output, replacement))
        if isinstance(parsed, dict):
            verdict_fields.extend(
                f"parsed.{key}"
                for key in _restrict_strong_values(parsed, replacement)
            )
    verdict_fields = list(dict.fromkeys(
        [
            str(value)
            for value in previous.get("strong_fields_changed", [])
            if str(value)
        ]
        + verdict_fields
    ))

    output["confidence_ceiling"] = ceiling
    output["evidence_based_calibration"] = {
        "version": EVIDENCE_CALIBRATION_VERSION,
        "marker": EVIDENCE_CALIBRATION_MARKER,
        "score_effect": "none",
        "confidence_ceiling": ceiling,
        "confidence_reasons": reasons,
        "confidence_fields_changed": confidence_fields,
        "strong_verdict_allowed": strong_allowed,
        "strong_fields_changed": verdict_fields,
        "projection_validation_present": projection_valid,
        "manual_boundary_review": manual_review,
        "fatal_error": fatal,
        "hard_correctness_error": hard_defect,
        "ledger_signals": signals,
    }
    if before != _score_snapshot(output):
        raise RuntimeError("Evidence calibration changed numeric score state")
    return output
