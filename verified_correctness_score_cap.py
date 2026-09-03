"""One-way score caps for verified core-correctness failures.

This policy is deliberately topic- and question-type-neutral.  It operates
only on deterministic logic findings or reconciled structured defects; an LLM
opinion, a missing enrichment hint, or a stylistic weakness never triggers it.
"""

from __future__ import annotations

import copy
from typing import Any


VERIFIED_CORRECTNESS_SCORE_CAP_VERSION = "verified_correctness_score_cap_v2"
VERIFIED_CORRECTNESS_SCORE_CAP_MARKER = "VERIFIED_CORRECTNESS_SCORE_CAP_V2"
FATAL_TOTAL_CAP = 14.5
MAJOR_CORE_TOTAL_CAP = 17.4
_SCORE_FIELDS = (
    "score",
    "total_score",
    "final_total_score",
    "final_score",
    "adjusted_total_score",
)


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _contract(value: dict[str, Any], key: str) -> dict[str, Any]:
    direct = value.get(key)
    if isinstance(direct, dict):
        return direct
    parsed = value.get("parsed")
    if isinstance(parsed, dict) and isinstance(parsed.get(key), dict):
        return parsed[key]
    return {}


def _identifiers(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value.strip()} if value.strip() else set()
    if not isinstance(value, (list, tuple, set)):
        return set()
    return {
        str(item).strip()
        for item in value
        if str(item).strip()
    }


def _core_requirement_ids(value: dict[str, Any]) -> set[str]:
    ledger = _contract(value, "canonical_evaluation_ledger")
    rows = ledger.get("rows")
    if not isinstance(rows, list):
        return set()
    return {
        str(row.get("requirement_id") or "").strip()
        for row in rows
        if isinstance(row, dict)
        and row.get("is_core") is True
        and str(row.get("requirement_id") or "").strip()
    }


def _is_core_related(row: dict[str, Any], core_ids: set[str]) -> bool:
    if row.get("invalidates_core_conclusion") is True:
        return True
    references = _identifiers(row.get("requirement_id"))
    references.update(_identifiers(row.get("requirement_ids")))
    references.update(_identifiers(row.get("demand_refs")))
    references.update(_identifiers(row.get("requirement_refs")))
    return bool(references.intersection(core_ids))


def _logic_events(value: dict[str, Any], core_ids: set[str]) -> list[dict[str, Any]]:
    logic = _mapping(
        value.get("logic_check_evaluation")
        or value.get("logic_check_result")
        or value.get("logic_check")
    )
    if not logic:
        return []

    events: list[dict[str, Any]] = []
    findings = logic.get("findings")
    if isinstance(findings, list):
        for index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                continue
            severity = str(finding.get("severity") or "").strip().casefold()
            if severity not in {"fatal", "major"}:
                continue
            events.append({
                "source": "logic_check_evaluation.findings",
                "id": str(
                    finding.get("rule_id")
                    or finding.get("id")
                    or f"logic-{index}"
                ),
                "severity": severity,
                "core_related": (
                    True if severity == "fatal"
                    else _is_core_related(finding, core_ids)
                ),
            })

    if logic.get("fatal_error_detected") is True or logic.get("fatal") is True:
        if not any(event["severity"] == "fatal" for event in events):
            events.append({
                "source": "logic_check_evaluation.fatal_error_detected",
                "id": "logic-fatal-flag",
                "severity": "fatal",
                "core_related": True,
            })
    return events


def _structured_defect_events(
    value: dict[str, Any], core_ids: set[str]
) -> list[dict[str, Any]]:
    contract = _contract(value, "general_evidence_contract")
    defects = contract.get("defects")
    if not isinstance(defects, list):
        return []
    events: list[dict[str, Any]] = []
    for index, defect in enumerate(defects):
        if not isinstance(defect, dict):
            continue
        if str(defect.get("defect_type") or "").casefold() != "correctness_error":
            continue
        severity = str(defect.get("severity") or "").strip().casefold()
        if severity not in {"fatal", "major"}:
            continue
        events.append({
            "source": "general_evidence_contract.defects",
            "id": str(defect.get("id") or defect.get("defect_id") or f"defect-{index}"),
            "severity": severity,
            "core_related": (
                True if severity == "fatal"
                else _is_core_related(defect, core_ids)
            ),
        })
    return events


def evaluate_verified_correctness_score_cap(payload: Any) -> dict[str, Any]:
    """Return the policy decision without mutating a grade payload."""
    value = _mapping(payload)
    core_ids = _core_requirement_ids(value)
    events = _logic_events(value, core_ids)
    events.extend(_structured_defect_events(value, core_ids))
    fatal = [event for event in events if event["severity"] == "fatal"]
    major_core = [
        event for event in events
        if event["severity"] == "major" and event["core_related"]
    ]
    if fatal:
        cap = FATAL_TOTAL_CAP
        reason_codes = ["verified_fatal_correctness_error"]
    elif major_core:
        cap = MAJOR_CORE_TOTAL_CAP
        reason_codes = ["verified_major_core_correctness_error"]
    else:
        cap = None
        reason_codes = []
    source_ids = [
        f"{event['source']}:{event['id']}"
        for event in events
    ]
    return {
        "version": VERIFIED_CORRECTNESS_SCORE_CAP_VERSION,
        "marker": VERIFIED_CORRECTNESS_SCORE_CAP_MARKER,
        "policy_applicable": cap is not None,
        "cap": cap,
        "reason_codes": reason_codes,
        "source_ids": source_ids,
        "fatal_count": len(fatal),
        "major_core_count": len(major_core),
        "events": events,
    }


def apply_verified_correctness_score_cap(payload: Any) -> Any:
    """Apply a monotonic final-score cap from verified correctness evidence."""
    if not isinstance(payload, dict):
        return payload
    output = copy.deepcopy(payload)
    decision = evaluate_verified_correctness_score_cap(output)
    previous = _mapping(output.get("verified_correctness_score_cap"))
    if (
        previous.get("version") == decision["version"]
        and previous.get("cap") == decision["cap"]
        and previous.get("source_ids") == decision["source_ids"]
    ):
        return output

    current = _number(
        output.get("total_score", output.get("final_total_score"))
    )
    cap = decision["cap"]
    previous_cap = _number(previous.get("cap"))
    previously_applied = bool(
        cap is not None
        and previous.get("score_effect") == "hard_cap"
        and previous_cap == cap
        and previous.get("source_ids") == decision["source_ids"]
    )
    changed_fields: list[str] = []
    if current is not None and cap is not None and current > cap:
        for field in _SCORE_FIELDS:
            numeric = _number(output.get(field))
            if numeric is not None and numeric > cap:
                output[field] = cap
                changed_fields.append(field)

    applied_caps = output.get("applied_caps")
    caps = [
        row for row in applied_caps
        if not (
            isinstance(row, dict)
            and row.get("type") == "verified_correctness_score_cap"
        )
    ] if isinstance(applied_caps, list) else []
    cap_applied = bool(changed_fields) or previously_applied
    if cap_applied:
        caps.append({
            "type": "verified_correctness_score_cap",
            "cap": cap,
            "reason_codes": decision["reason_codes"],
            "source_ids": decision["source_ids"],
            "score_effect": "hard_cap",
        })
        output["applied_caps"] = caps
    elif isinstance(applied_caps, list):
        # `applied_caps` is public evidence of an actual numeric reduction,
        # not a list of merely applicable policies.
        output["applied_caps"] = caps

    decision.update({
        "score_effect": "hard_cap" if cap_applied else "none",
        "original_total_score": (
            previous.get("original_total_score")
            if previously_applied else current
        ),
        "applied_total_score": (
            min(current, cap) if current is not None and cap is not None else current
        ),
        "changed_fields": changed_fields,
        "preserved_prior_application": previously_applied,
    })
    output["verified_correctness_score_cap"] = decision
    return output
