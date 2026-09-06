"""Deterministic requirement states from evidence, contracts and invariants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from topic_machine_contract import extract_fatal_rule_ids, validate_topic_machine_contract


VERSION = "deterministic_requirement_evaluator_v1"
MARKER = "DETERMINISTIC_REQUIREMENT_EVALUATION_V1"
ROOT = Path(__file__).resolve().parent


def load_machine_contracts(topic_ids: Iterable[str] | None = None) -> list[dict[str, Any]]:
    selected = {str(row).strip() for row in (topic_ids or []) if str(row).strip()}
    contracts: list[dict[str, Any]] = []
    for path in sorted((ROOT / "rubrics" / "topic_packs").glob("*/logic_check.json")):
        if selected and path.parent.name not in selected:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        contract = payload.get("machine_contract")
        if not isinstance(contract, dict):
            continue
        contracts.append(validate_topic_machine_contract(
            contract,
            topic_id=path.parent.name,
            known_rule_ids=extract_fatal_rule_ids(
                payload.get("llm_profile", {}).get("fatal_conditions", [])
            ),
        ))
    return contracts


def _key(row: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return tuple(
        str(row.get(field) or "").strip().casefold()
        for field in ("subject", "predicate", "object", "polarity")
    )


def evaluate_deterministic_requirements(
    *,
    claims: list[dict[str, Any]],
    invariant_codes: Iterable[str],
    topic_ids: Iterable[str] | None = None,
    extraction_complete: bool = False,
) -> dict[str, Any]:
    """Apply fixed precedence; unresolved extraction never becomes MISSING."""
    codes = {str(row).strip() for row in invariant_codes if str(row).strip()}
    requested_topics = {
        str(row).strip() for row in (topic_ids or []) if str(row).strip()
    }
    selected_contracts = load_machine_contracts(requested_topics)
    if not requested_topics and codes:
        # An invariant code is globally unique and may safely resolve its owner
        # even when legacy routing exposed only the neighboring primary topic.
        selected_contracts = [
            contract for contract in load_machine_contracts()
            if any(row["invariant_code"] in codes for row in contract["invariant_bindings"])
        ]
    claim_keys = {_key(row) for row in claims}
    results: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for contract in selected_contracts:
        facts = {row["fact_id"]: row for row in contract["facts"]}
        violated_refs: set[str] = set()
        for binding in contract["invariant_bindings"]:
            if binding["invariant_code"] not in codes:
                continue
            violated_refs.update(binding["requirement_refs"])
            findings.append({
                "finding_id": binding["rule_id"],
                "classification": binding["classification"],
                "invariant_code": binding["invariant_code"],
                "requirement_refs": list(binding["requirement_refs"]),
                "recommended_ceiling": binding["recommended_ceiling"],
                "owner_topic_id": contract["owner_topic_id"],
            })
        for rule in contract["requirement_rules"]:
            matched = [
                fact_id for fact_id in rule["required_fact_ids"]
                if _key(facts[fact_id]) in claim_keys
            ]
            contradicted = [
                fact_id for fact_id in rule["required_fact_ids"]
                if any(
                    candidate[:3] == _key(facts[fact_id])[:3]
                    and candidate[3] != _key(facts[fact_id])[3]
                    for candidate in claim_keys
                )
            ]
            requirement_id = rule["requirement_id"]
            if requirement_id in violated_refs or contradicted:
                status = "WRONG"
            elif len(matched) >= rule["minimum_match_count"]:
                status = "SATISFIED"
            elif matched:
                status = "PARTIAL"
            elif extraction_complete:
                status = "MISSING"
            else:
                status = "UNKNOWN"
            results.append({
                "owner_topic_id": contract["owner_topic_id"],
                "requirement_id": requirement_id,
                "status": status,
                "matched_fact_ids": matched,
                "contradicted_fact_ids": contradicted,
            })
    fatal = any(row["classification"] in {"fatal", "core_error"} for row in findings)
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "llm_verdict_authority": 0,
        "score_effect": "none",
        "requirements": results,
        "findings": findings,
        "fatal_or_core_error": fatal,
        "requirement_full_credit_allowed": not fatal,
        "perfect_theory_comment_allowed": not fatal,
        "summary": {
            status: sum(row["status"] == status for row in results)
            for status in ("SATISFIED", "PARTIAL", "WRONG", "MISSING", "UNKNOWN")
        },
    }
