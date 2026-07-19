"""Diagnostic general evidence and defect contract.

The contract normalizes semantic evidence metadata. It does not modify
scores, caps, totals, pass/fail decisions, or layer ownership by itself.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

GENERAL_EVIDENCE_CONTRACT_SCHEMA_VERSION = "1.0"
GENERAL_EVIDENCE_CONTRACT_MARKER = "GENERAL_EVIDENCE_CONTRACT_V1"

_ALLOWED_DEFECT_TYPES = {
    "correctness_error",
    "core_depth_gap",
    "advanced_detail_missing",
    "presentation_issue",
}
_ALLOWED_LAYERS = {"A", "B", "C", "D", "E"}
_ALLOWED_SEVERITIES = {"fatal", "major", "partial", "minor", "warning"}
_ALLOWED_STATUSES = {
    "supported",
    "partial",
    "unsupported",
    "contradicted",
    "unclear",
}
_ALLOWED_EVIDENCE_TYPES = {
    "definition",
    "principle",
    "mechanism",
    "formula",
    "condition",
    "assumption",
    "field_judgement",
    "verification",
    "tradeoff",
    "example",
    "other",
}

_DEFECT_ALIASES = {
    "correctness": "correctness_error",
    "error": "correctness_error",
    "incorrect": "correctness_error",
    "wrong": "correctness_error",
    "technical_error": "correctness_error",
    "depth_gap": "core_depth_gap",
    "core_gap": "core_depth_gap",
    "missing_core_depth": "core_depth_gap",
    "insufficient_depth": "core_depth_gap",
    "advanced_missing": "advanced_detail_missing",
    "minor_detail_missing": "advanced_detail_missing",
    "presentation": "presentation_issue",
    "formatting": "presentation_issue",
    "formula_integrity_warning": "presentation_issue",
    "operator_missing": "presentation_issue",
}
_STATUS_ALIASES = {
    "present": "supported",
    "satisfied": "supported",
    "adequate": "supported",
    "incomplete": "partial",
    "missing": "unsupported",
    "incorrect": "contradicted",
    "unknown": "unclear",
}
_SEVERITY_ALIASES = {
    "critical": "fatal",
    "high": "major",
    "medium": "partial",
    "low": "minor",
    "info": "warning",
}


def _text(value: Any, limit: int = 2400) -> str:
    if value is None:
        return ""
    text = value if isinstance(value, str) else str(value)
    return re.sub(r"\s+", " ", text).strip()[:limit]


def _token(value: Any) -> str:
    text = _text(value, 200).lower()
    return re.sub(r"[^a-z0-9가-힣]+", "_", text).strip("_")


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if value is None:
        return []
    return [value]


def _layer(value: Any, fallback: str = "") -> str:
    token = _text(value, 8).upper()
    if token in _ALLOWED_LAYERS:
        return token
    return fallback if fallback in _ALLOWED_LAYERS else ""


def _status(value: Any) -> str:
    token = _STATUS_ALIASES.get(_token(value), _token(value))
    return token if token in _ALLOWED_STATUSES else "unclear"


def _defect_type(value: Any) -> str:
    token = _DEFECT_ALIASES.get(_token(value), _token(value))
    return token if token in _ALLOWED_DEFECT_TYPES else "presentation_issue"


def _severity(value: Any, defect_type: str) -> str:
    token = _SEVERITY_ALIASES.get(_token(value), _token(value))

    if token not in _ALLOWED_SEVERITIES:
        return "partial" if defect_type == "correctness_error" else "minor"

    if defect_type != "correctness_error" and token in {"fatal", "major"}:
        return "partial"

    return token


def _stable_id(prefix: str, value: dict[str, Any]) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _normalize_variables(value: Any) -> list[dict[str, str]]:
    if isinstance(value, dict):
        items = [
            {"name": key, "meaning": meaning}
            for key, meaning in value.items()
        ]
    else:
        items = _as_list(value)

    rows = []

    for item in items:
        if isinstance(item, dict):
            name = _text(item.get("name") or item.get("symbol"), 120)
            meaning = _text(
                item.get("meaning")
                or item.get("definition")
                or item.get("description"),
                500,
            )
            unit = _text(item.get("unit"), 120)
        else:
            name = _text(item, 120)
            meaning = ""
            unit = ""

        if name:
            rows.append(
                {
                    "name": name,
                    "meaning": meaning,
                    "unit": unit,
                }
            )

    return rows


def _normalize_claim(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        raw = {"claim_text": _text(raw)}

    claim_text = _text(
        raw.get("claim_text") or raw.get("claim") or raw.get("text")
    )
    evidence_text = _text(
        raw.get("evidence_text")
        or raw.get("evidence")
        or raw.get("support")
    )

    if not claim_text and not evidence_text:
        return None

    evidence_type = _token(
        raw.get("evidence_type") or raw.get("type")
    )
    if evidence_type not in _ALLOWED_EVIDENCE_TYPES:
        evidence_type = "other"

    row = {
        "requirement_id": _text(
            raw.get("requirement_id") or raw.get("requirement"),
            160,
        ),
        "claim_text": claim_text,
        "evidence_text": evidence_text,
        "evidence_type": evidence_type,
        "status": _status(raw.get("status")),
        "owner_layer": _layer(raw.get("owner_layer")),
        "conditions": [
            _text(item, 500)
            for item in _as_list(raw.get("conditions"))
            if _text(item, 500)
        ],
    }
    row["claim_id"] = _text(
        raw.get("claim_id") or raw.get("id"),
        160,
    ) or _stable_id("claim", row)
    return row


def _normalize_formula(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        raw = {"formula_text": _text(raw)}

    formula_text = _text(
        raw.get("formula_text")
        or raw.get("formula")
        or raw.get("expression")
    )
    if not formula_text:
        return None

    integrity = _token(
        raw.get("integrity_status") or raw.get("status")
    )
    if integrity not in {
        "valid",
        "warning",
        "invalid",
        "not_evaluated",
        "not_applicable",
    }:
        integrity = "not_evaluated"

    row = {
        "requirement_id": _text(
            raw.get("requirement_id") or raw.get("requirement"),
            160,
        ),
        "formula_text": formula_text,
        "variables": _normalize_variables(raw.get("variables")),
        "conditions": [
            _text(item, 500)
            for item in _as_list(raw.get("conditions"))
            if _text(item, 500)
        ],
        "interpretation": _text(
            raw.get("interpretation") or raw.get("meaning")
        ),
        "integrity_status": integrity,
        "integrity_notes": [
            _text(item, 700)
            for item in _as_list(
                raw.get("integrity_notes")
                or raw.get("warnings")
                or raw.get("issues")
            )
            if _text(item, 700)
        ],
        "owner_layer": _layer(raw.get("owner_layer"), "C"),
    }
    row["formula_id"] = _text(
        raw.get("formula_id") or raw.get("id"),
        160,
    ) or _stable_id("formula", row)
    return row


def _normalize_defect(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        raw = {
            "explanation": _text(raw),
            "defect_type": "presentation_issue",
        }

    defect_type = _defect_type(
        raw.get("defect_type")
        or raw.get("issue_type")
        or raw.get("type")
    )
    explanation = _text(
        raw.get("explanation")
        or raw.get("reason")
        or raw.get("description")
    )
    evidence_text = _text(
        raw.get("evidence_text")
        or raw.get("evidence")
        or raw.get("quote")
    )

    if not explanation and not evidence_text:
        return None

    row = {
        "defect_type": defect_type,
        "severity": _severity(raw.get("severity"), defect_type),
        "owner_layer": _layer(
            raw.get("owner_layer")
            or raw.get("primary_owner_layer"),
            "C",
        ),
        "requirement_id": _text(
            raw.get("requirement_id") or raw.get("requirement"),
            160,
        ),
        "evidence_text": evidence_text,
        "explanation": explanation,
        "affected_claim_ids": [
            _text(item, 160)
            for item in _as_list(raw.get("affected_claim_ids"))
            if _text(item, 160)
        ],
        "diagnostic_only": True,
    }
    row["defect_id"] = _text(
        raw.get("defect_id")
        or raw.get("issue_id")
        or raw.get("id"),
        160,
    ) or _stable_id("defect", row)
    return row


def _dedupe(
    rows: list[dict[str, Any]],
    id_key: str,
) -> list[dict[str, Any]]:
    result = []
    seen = set()

    for row in rows:
        identifier = _text(row.get(id_key), 200)
        fingerprint = json.dumps(
            row,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        key = (
            identifier,
            hashlib.sha256(fingerprint.encode("utf-8")).hexdigest(),
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(row)

    return result


def empty_general_evidence_contract() -> dict[str, Any]:
    return {
        "schema_version": GENERAL_EVIDENCE_CONTRACT_SCHEMA_VERSION,
        "contract_marker": GENERAL_EVIDENCE_CONTRACT_MARKER,
        "mode": "diagnostic_only",
        "score_effect": "none",
        "claims": [],
        "formulas": [],
        "defects": [],
        "field_judgements": [],
        "summary": {
            "claim_count": 0,
            "supported_claim_count": 0,
            "formula_count": 0,
            "defect_count": 0,
            "defect_type_counts": {
                "correctness_error": 0,
                "core_depth_gap": 0,
                "advanced_detail_missing": 0,
                "presentation_issue": 0,
            },
            "owner_layer_counts": {
                "A": 0,
                "B": 0,
                "C": 0,
                "D": 0,
                "E": 0,
            },
        },
    }


def normalize_general_evidence_contract(
    value: Any,
) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}

    claims = _dedupe(
        [
            row
            for raw in _as_list(source.get("claims"))
            if (row := _normalize_claim(raw)) is not None
        ],
        "claim_id",
    )
    formulas = _dedupe(
        [
            row
            for raw in _as_list(source.get("formulas"))
            if (row := _normalize_formula(raw)) is not None
        ],
        "formula_id",
    )
    defects = _dedupe(
        [
            row
            for raw in _as_list(
                source.get("defects") or source.get("issues")
            )
            if (row := _normalize_defect(raw)) is not None
        ],
        "defect_id",
    )

    field_judgements = []

    for raw in _as_list(source.get("field_judgements")):
        if isinstance(raw, dict):
            judgement = {
                "judgement_text": _text(
                    raw.get("judgement_text")
                    or raw.get("judgement")
                    or raw.get("text")
                ),
                "evidence_text": _text(
                    raw.get("evidence_text")
                    or raw.get("evidence")
                ),
                "status": _status(raw.get("status")),
                "owner_layer": _layer(
                    raw.get("owner_layer"),
                    "D",
                ),
            }
        else:
            judgement = {
                "judgement_text": _text(raw),
                "evidence_text": "",
                "status": "unclear",
                "owner_layer": "D",
            }

        if judgement["judgement_text"] or judgement["evidence_text"]:
            field_judgements.append(judgement)

    defect_type_counts = {
        key: 0
        for key in sorted(_ALLOWED_DEFECT_TYPES)
    }
    owner_layer_counts = {
        key: 0
        for key in sorted(_ALLOWED_LAYERS)
    }

    for defect in defects:
        defect_type_counts[defect["defect_type"]] += 1
        owner_layer_counts[defect["owner_layer"]] += 1

    normalized = empty_general_evidence_contract()
    normalized.update(
        {
            "claims": claims,
            "formulas": formulas,
            "defects": defects,
            "field_judgements": field_judgements,
            "summary": {
                "claim_count": len(claims),
                "supported_claim_count": sum(
                    claim["status"] == "supported"
                    for claim in claims
                ),
                "formula_count": len(formulas),
                "defect_count": len(defects),
                "defect_type_counts": defect_type_counts,
                "owner_layer_counts": owner_layer_counts,
            },
        }
    )
    return normalized


def attach_general_evidence_contract(
    result: Any,
) -> Any:
    if not isinstance(result, dict):
        return result

    updated = copy.deepcopy(result)
    raw_contract = updated.get("general_evidence_contract")
    parsed = updated.get("parsed")

    if raw_contract is None and isinstance(parsed, dict):
        raw_contract = parsed.get("general_evidence_contract")

    normalized = normalize_general_evidence_contract(raw_contract)
    updated["general_evidence_contract"] = normalized

    if isinstance(parsed, dict):
        parsed["general_evidence_contract"] = copy.deepcopy(normalized)

    return updated

# GENERIC_FORMULA_INTEGRITY_INTEGRATION_V1
_formula_integrity_previous_attach_general_evidence_contract = (
    attach_general_evidence_contract
)


def attach_general_evidence_contract(result: Any) -> Any:
    normalized = (
        _formula_integrity_previous_attach_general_evidence_contract(
            result
        )
    )

    from generic_formula_integrity import (
        apply_formula_integrity_to_result,
    )

    return apply_formula_integrity_to_result(normalized)
