"""Deterministic authority boundary for semantic demand-state proposals."""

from __future__ import annotations

import copy
import re
from typing import Any

from demand_state_contract import normalize_internal_state


SCHEMA_VERSION = "demand_evidence_resolution_v1"


def _normalized(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def _exact_quote(quote: Any, answer_text: str) -> tuple[str, bool]:
    raw = str(quote or "").strip()
    normalized = _normalized(raw)
    return raw, bool(len(normalized) >= 4 and normalized in _normalized(answer_text))


def _coverage_lists(value: Any) -> list[list[dict[str, Any]]]:
    output: list[list[dict[str, Any]]] = []
    seen: set[int] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            explicit = node.get("explicit_requirement_coverage")
            rows = explicit.get("requirements") if isinstance(explicit, dict) else None
            if isinstance(rows, list) and id(rows) not in seen:
                seen.add(id(rows))
                output.append(rows)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return output


def _canonical_ids(value: Any) -> set[str]:
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            contract = node.get("question_demand_contract")
            requirements = contract.get("requirements") if isinstance(contract, dict) else None
            if isinstance(requirements, list):
                found.update(
                    str(row.get("requirement_id") or "").strip()
                    for row in requirements
                    if isinstance(row, dict) and str(row.get("requirement_id") or "").strip()
                )
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return found


def resolve_semantic_demand_evidence(value: Any, answer_text: str) -> Any:
    """Validate evidence and attach the only state the ledger may consume."""
    if not isinstance(value, dict):
        return value
    output = copy.deepcopy(value)
    canonical_ids = _canonical_ids(output)
    for rows in _coverage_lists(output):
        for row in rows:
            if not isinstance(row, dict):
                continue
            provider_status = normalize_internal_state(row.get("status"))
            requirement_id = str(row.get("requirement_id") or "").strip()
            identity_verified = bool(requirement_id and requirement_id in canonical_ids)
            candidate = row.get("evidence_quote")
            if candidate in (None, ""):
                candidate = row.get("evidence")
            quote, quote_verified = _exact_quote(candidate, answer_text)
            mentioned = row.get("mentioned") is True
            raw_confidence = str(row.get("state_confidence") or "").strip().lower()
            state_confidence = (
                raw_confidence if raw_confidence in {"high", "medium", "low"}
                else "legacy_unspecified"
            )

            if provider_status == "correct":
                resolved = "correct" if identity_verified and quote_verified else (
                    "partial" if mentioned else "unknown"
                )
            elif provider_status == "partial":
                resolved = "partial" if mentioned or quote_verified else "unknown"
            elif provider_status == "missing":
                resolved = "partial" if quote_verified else (
                    "missing"
                    if not mentioned and state_confidence in {"high", "legacy_unspecified"}
                    else "unknown"
                )
            elif provider_status == "incorrect":
                resolved = "incorrect"
            else:
                resolved = "unknown"

            row["provider_status"] = provider_status
            row["resolved_status"] = resolved
            row["evidence_quote"] = quote
            row["deterministic_evidence"] = {
                "schema_version": SCHEMA_VERSION,
                "canonical_identity_verified": identity_verified,
                "exact_answer_quote_verified": quote_verified,
                "provider_is_advisory": True,
                "wrong_requires_verified_defect": True,
                "state_confidence": state_confidence,
                "uncertainty_downgraded": bool(
                    resolved == "unknown" and provider_status != "unknown"
                ),
            }
    return output
