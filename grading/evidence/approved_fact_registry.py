"""Validated, explicitly reviewed Fact registry, separate from generated rubrics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .fact_grounded_contracts import FactGroundedContractError, validate_fact


REGISTRY_PATH = Path("grading/evidence/approved_fact_registry.json")


def load_approved_fact_registry(repository_root: str | Path) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    path = (root / REGISTRY_PATH).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise FactGroundedContractError("approved Fact registry is missing")
    registry = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(registry, dict) or set(registry) != {"registry_version", "approval_record", "facts"}:
        raise FactGroundedContractError("invalid approved Fact registry")
    if registry["registry_version"] != "approved-fact-registry-v1":
        raise FactGroundedContractError("unsupported approved Fact registry")
    approval = registry["approval_record"]
    required = {"reviewer_id", "delegated_by_user", "reviewed_at", "review_basis", "approval_scope"}
    if not isinstance(approval, dict) or set(approval) != required or approval["delegated_by_user"] is not True:
        raise FactGroundedContractError("approval provenance is incomplete")
    if not isinstance(approval["reviewer_id"], str) or not approval["reviewer_id"].strip():
        raise FactGroundedContractError("reviewer identity is missing")
    facts = registry["facts"]
    if not isinstance(facts, list) or not facts:
        raise FactGroundedContractError("approved Fact list is empty")
    seen: set[str] = set()
    for fact in facts:
        validate_fact(fact)
        if fact["review_status"] != "approved":
            raise FactGroundedContractError("registry contains a non-approved Fact")
        if fact.get("verification_status") != "verified":
            raise FactGroundedContractError("registry Fact is not independently verified")
        if fact["fact_id"] in seen:
            raise FactGroundedContractError("duplicate approved Fact ID")
        seen.add(fact["fact_id"])
        master_path = root / "master_topic_packs" / f"{fact['topic_id']}.json"
        if not master_path.is_file():
            raise FactGroundedContractError("Fact topic Master pack is missing")
        master = json.loads(master_path.read_text(encoding="utf-8"))
        if master.get("topic_id") != fact["topic_id"]:
            raise FactGroundedContractError("Fact topic does not match Master pack")
        # source_refs preserve WordPress provenance only. Their currentness is
        # audited separately and cannot override independent technical evidence.
    return registry
