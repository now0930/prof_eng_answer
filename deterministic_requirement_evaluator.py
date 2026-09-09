"""Deterministic requirement states from evidence, contracts and invariants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from topic_machine_contract import extract_fatal_rule_ids, validate_topic_machine_contract


VERSION = "deterministic_requirement_evaluator_v1"
MARKER = "DETERMINISTIC_REQUIREMENT_EVALUATION_V1"
ROOT = Path(__file__).resolve().parent


def _topic_anchor_ids(topic_id: str) -> set[str]:
    path = ROOT / "rubrics" / "topic_packs" / topic_id / "fact_anchor.json"
    if not path.is_file():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        str(row.get("anchor_id") or row.get("id") or "").strip()
        for row in payload.get("anchors", [])
        if isinstance(row, dict)
    }


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


def _claim_id(row: Mapping[str, Any], index: int) -> str:
    return str(row.get("claim_id") or f"anonymous_claim_{index}")


def _adopted(row: Mapping[str, Any]) -> bool:
    return str(row.get("assertion_context") or "asserted").casefold() in {
        "asserted", "corrected",
    }


def _required_conditions(row: Mapping[str, Any]) -> set[str]:
    value = row.get("conditions") or []
    return {str(item).strip().casefold() for item in value if str(item).strip()}


def evaluate_deterministic_requirements(
    *,
    claims: list[dict[str, Any]],
    invariant_codes: Iterable[str],
    topic_ids: Iterable[str] | None = None,
    extraction_complete: bool = False,
    requirement_scope_by_topic: Mapping[str, Iterable[str]] | None = None,
) -> dict[str, Any]:
    """Apply fixed precedence; unresolved extraction never becomes MISSING."""
    codes = {str(row).strip() for row in invariant_codes if str(row).strip()}
    requested_topics = {
        str(row).strip() for row in (topic_ids or []) if str(row).strip()
    }
    selected_contracts = load_machine_contracts(requested_topics)
    if codes:
        # An invariant code is globally unique and its owner must remain active
        # when routing exposes a neighboring primary Topic.
        owners = [
            contract for contract in load_machine_contracts()
            if any(row["invariant_code"] in codes for row in contract["invariant_bindings"])
        ]
        selected_owner_ids = {row["owner_topic_id"] for row in selected_contracts}
        selected_contracts.extend(
            row for row in owners if row["owner_topic_id"] not in selected_owner_ids
        )
    adopted_claims = [
        (index, row) for index, row in enumerate(claims)
        if isinstance(row, Mapping) and _adopted(row)
    ]
    ignored_claim_ids = [
        _claim_id(row, index) for index, row in enumerate(claims)
        if isinstance(row, Mapping) and not _adopted(row)
    ]
    allocated_claim_ids: set[str] = set()
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
            requirement_id = rule["requirement_id"]
            scope = requirement_scope_by_topic or {}
            scoped_ids = {
                str(row).strip()
                for row in scope.get(contract["owner_topic_id"], [])
                if str(row).strip()
            }
            if (
                requirement_scope_by_topic is not None
                and requirement_id in _topic_anchor_ids(contract["owner_topic_id"])
                and requirement_id not in scoped_ids
                and requirement_id not in violated_refs
            ):
                continue
            matched: list[str] = []
            contradicted: list[str] = []
            related: list[str] = []
            evidence_claim_ids: list[str] = []
            required_fact_keys = {
                _key(facts[fact_id]) for fact_id in rule["required_fact_ids"]
            }
            allow_subject_mention_partial = bool(
                rule.get("allow_subject_mention_partial", False)
            )
            for fact_id in rule["required_fact_ids"]:
                fact = facts[fact_id]
                fact_key = _key(fact)
                fact_conditions = _required_conditions(fact)
                candidates = [
                    (index, claim) for index, claim in adopted_claims
                    if _claim_id(claim, index) not in allocated_claim_ids
                ]
                exact = [
                    (index, claim) for index, claim in candidates
                    if _key(claim) == fact_key
                    and fact_conditions <= _required_conditions(claim)
                ]
                opposite = [
                    (index, claim) for index, claim in candidates
                    if _key(claim)[:3] == fact_key[:3]
                    and _key(claim)[3] != fact_key[3]
                ]
                relation_conflict = [
                    (index, claim) for index, claim in candidates
                    if _key(claim)[:2] == fact_key[:2]
                    and _key(claim)[2] != fact_key[2]
                    and _key(claim)[3] == fact_key[3]
                    and _key(claim) not in required_fact_keys
                ]
                partial = [
                    (index, claim) for index, claim in candidates
                    if _key(claim)[0] == fact_key[0]
                    and _key(claim) not in required_fact_keys
                    and (
                        (
                            allow_subject_mention_partial
                            and _key(claim)[1] == "mentioned"
                        )
                        or sum(
                            left == right
                            for left, right in zip(_key(claim)[:3], fact_key[:3])
                        ) >= 2
                    )
                ]
                selected = opposite[:1] or exact[:1] or relation_conflict[:1] or partial[:1]
                if opposite:
                    contradicted.append(fact_id)
                elif exact:
                    matched.append(fact_id)
                elif relation_conflict:
                    contradicted.append(fact_id)
                elif partial:
                    related.append(fact_id)
                if selected:
                    index, claim = selected[0]
                    claim_id = _claim_id(claim, index)
                    allocated_claim_ids.add(claim_id)
                    evidence_claim_ids.append(claim_id)
            if requirement_id in violated_refs or contradicted:
                status = "WRONG"
            elif len(matched) >= rule["minimum_match_count"]:
                status = "SATISFIED"
            elif matched or related:
                status = "PARTIAL"
            elif extraction_complete:
                status = "MISSING"
            else:
                status = "UNKNOWN"
            results.append({
                "owner_topic_id": contract["owner_topic_id"],
                "requirement_id": requirement_id,
                "score_group_id": (
                    str(rule["score_group_id"])
                    if rule.get("score_group_id") else None
                ),
                "status": status,
                "evidence_mode": "canonical_claim",
                "matched_fact_ids": matched,
                "contradicted_fact_ids": contradicted,
                "related_fact_ids": related,
                "evidence_claim_ids": evidence_claim_ids,
            })
            if contradicted and rule.get("contradiction_classification"):
                findings.append({
                    "finding_id": rule["contradiction_rule_id"],
                    "classification": rule["contradiction_classification"],
                    "invariant_code": "MACHINE_CONTRACT_RELATION_CONTRADICTION",
                    "requirement_refs": [requirement_id],
                    "recommended_ceiling": rule[
                        "contradiction_recommended_ceiling"
                    ],
                    "owner_topic_id": contract["owner_topic_id"],
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
        "evidence_allocation": {
            "allocated_claim_ids": sorted(allocated_claim_ids),
            "ignored_nonasserted_claim_ids": sorted(ignored_claim_ids),
            "duplicate_credit_count": 0,
        },
    }
