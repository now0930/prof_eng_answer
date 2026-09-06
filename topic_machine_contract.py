"""Validation for optional, additive Topic Pack machine contracts."""

from __future__ import annotations

import copy
import re
from typing import Any


VERSION = "topic_machine_contract_v1"
_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_CLASSIFICATIONS = {"fatal", "core_error", "major", "minor"}


class TopicMachineContractError(ValueError):
    pass


def _identifier(value: Any, field: str) -> str:
    result = str(value or "").strip()
    if not _ID.fullmatch(result):
        raise TopicMachineContractError(f"{field} must be a canonical id")
    return result


def validate_topic_machine_contract(
    value: Any,
    *,
    topic_id: str,
    known_rule_ids: set[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TopicMachineContractError("machine_contract must be an object")
    required = {
        "schema_version", "owner_topic_id", "authority", "score_effect",
        "facts", "requirement_rules", "invariant_bindings",
    }
    if set(value) != required:
        raise TopicMachineContractError("machine_contract fields mismatch")
    if value.get("schema_version") != VERSION:
        raise TopicMachineContractError("machine_contract version mismatch")
    if value.get("owner_topic_id") != topic_id:
        raise TopicMachineContractError("machine_contract owner mismatch")
    if value.get("authority") != "deterministic_topic_contract":
        raise TopicMachineContractError("machine_contract authority mismatch")
    if value.get("score_effect") != "downstream_deterministic_only":
        raise TopicMachineContractError("machine_contract cannot directly score")

    facts = value.get("facts")
    if not isinstance(facts, list) or not facts:
        raise TopicMachineContractError("machine_contract facts must not be empty")
    fact_ids: set[str] = set()
    for index, fact in enumerate(facts):
        if not isinstance(fact, dict) or set(fact) != {
            "fact_id", "subject", "predicate", "object", "polarity",
        }:
            raise TopicMachineContractError(f"facts[{index}] fields mismatch")
        fact_id = _identifier(fact.get("fact_id"), f"facts[{index}].fact_id")
        if fact_id in fact_ids:
            raise TopicMachineContractError(f"duplicate fact_id: {fact_id}")
        fact_ids.add(fact_id)
        for key in ("subject", "predicate", "object"):
            _identifier(fact.get(key), f"facts[{index}].{key}")
        if fact.get("polarity") not in {"positive", "negative"}:
            raise TopicMachineContractError(f"facts[{index}].polarity invalid")

    requirement_ids: set[str] = set()
    rules = value.get("requirement_rules")
    if not isinstance(rules, list) or not rules:
        raise TopicMachineContractError("requirement_rules must not be empty")
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict) or set(rule) != {
            "requirement_id", "required_fact_ids", "minimum_match_count",
        }:
            raise TopicMachineContractError(
                f"requirement_rules[{index}] fields mismatch"
            )
        requirement_id = _identifier(
            rule.get("requirement_id"),
            f"requirement_rules[{index}].requirement_id",
        )
        if requirement_id in requirement_ids:
            raise TopicMachineContractError(
                f"duplicate requirement_id: {requirement_id}"
            )
        requirement_ids.add(requirement_id)
        refs = rule.get("required_fact_ids")
        if not isinstance(refs, list) or not refs or not set(refs) <= fact_ids:
            raise TopicMachineContractError(
                f"requirement_rules[{index}] has unknown fact refs"
            )
        minimum = rule.get("minimum_match_count")
        if (
            isinstance(minimum, bool)
            or not isinstance(minimum, int)
            or not 1 <= minimum <= len(refs)
        ):
            raise TopicMachineContractError(
                f"requirement_rules[{index}].minimum_match_count invalid"
            )

    bindings = value.get("invariant_bindings")
    if not isinstance(bindings, list):
        raise TopicMachineContractError("invariant_bindings must be an array")
    known = known_rule_ids or set()
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict) or set(binding) != {
            "invariant_code", "rule_id", "classification",
            "requirement_refs", "recommended_ceiling",
        }:
            raise TopicMachineContractError(
                f"invariant_bindings[{index}] fields mismatch"
            )
        _identifier(
            str(binding.get("invariant_code") or "").casefold(),
            "invariant_code",
        )
        rule_id = _identifier(binding.get("rule_id"), "rule_id")
        if known and rule_id not in known:
            raise TopicMachineContractError(f"unknown rule_id: {rule_id}")
        if binding.get("classification") not in _CLASSIFICATIONS:
            raise TopicMachineContractError("invalid invariant classification")
        refs = binding.get("requirement_refs")
        if not isinstance(refs, list) or not refs or not set(refs) <= requirement_ids:
            raise TopicMachineContractError("unknown invariant requirement ref")
        ceiling = binding.get("recommended_ceiling")
        if (
            isinstance(ceiling, bool)
            or not isinstance(ceiling, (int, float))
            or not 0 <= float(ceiling) <= 25
        ):
            raise TopicMachineContractError("invalid recommended_ceiling")
    return copy.deepcopy(value)
