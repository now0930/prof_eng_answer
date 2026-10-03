"""Proposal-only contract for curated Topic content changes."""

from __future__ import annotations

import copy
from datetime import datetime
import re
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from .master_topic_pack import MasterTopicPackError, validate_master_topic_pack


CONTENT_UPDATE_SCHEMA_VERSION = "content-update-proposal-v1"
_SOURCE_KEYS = {
    "fact_anchor", "logic_check", "model_answer", "topic_importance",
    "question_demand_axes",
}
_HASH_RE = re.compile(r"^[a-fA-F0-9]{64}$")
_TOPIC_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


class ContentUpdateError(ValueError):
    """Raised when a curated-content proposal violates its contract."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise ContentUpdateError(message)


def _affected_views(master: dict[str, Any], source_key: str) -> list[str]:
    projection_sources = {
        "grading": master["projections"]["grading"]["source_keys"],
        "training": master["projections"]["training"]["content_sources"],
        "diagnosis": master["projections"]["diagnosis"]["content_sources"],
    }
    return [view for view, keys in projection_sources.items() if source_key in keys]


def validate_content_update_proposal(value: Any) -> dict[str, Any]:
    """Validate a pending proposal. This validator never applies its diff."""
    _expect(isinstance(value, dict), "content update proposal must be an object")
    required = {
        "schema_version", "proposal_id", "topic_id", "base_revision", "proposed_at",
        "target", "before_value", "proposed_value", "change_reason", "evidence",
        "affected_views", "status", "approval_required",
    }
    _expect(set(value) == required, "content update proposal fields do not match the contract")
    _expect(value["schema_version"] == CONTENT_UPDATE_SCHEMA_VERSION, "unsupported content update proposal schema")
    _expect(isinstance(value["proposal_id"], str) and bool(value["proposal_id"].strip()), "proposal_id is required")
    _expect(
        isinstance(value["topic_id"], str)
        and len(value["topic_id"]) >= 8
        and _TOPIC_ID_RE.fullmatch(value["topic_id"]) is not None,
        "topic_id is invalid",
    )
    _expect(isinstance(value["base_revision"], int) and not isinstance(value["base_revision"], bool) and value["base_revision"] >= 1, "base_revision must be positive")
    _expect(isinstance(value["proposed_at"], str), "proposed_at is required")
    try:
        timestamp = datetime.fromisoformat(value["proposed_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContentUpdateError("proposed_at must be ISO-8601") from exc
    _expect(timestamp.tzinfo is not None, "proposed_at must include a timezone")

    target = value["target"]
    _expect(isinstance(target, dict) and set(target) == {"source_key", "record_id", "field_path"}, "target fields are invalid")
    _expect(isinstance(target["source_key"], str) and target["source_key"] in _SOURCE_KEYS, "target source_key is invalid")
    _expect(isinstance(target["record_id"], str) and bool(target["record_id"].strip()), "target record_id is required")
    _expect(
        isinstance(target["field_path"], list)
        and 1 <= len(target["field_path"]) <= 5
        and all(isinstance(part, str) and part.strip() for part in target["field_path"]),
        "target field_path must contain one to five non-empty path parts",
    )
    _expect(value["before_value"] is None or isinstance(value["before_value"], str), "before_value must be a string or null")
    _expect(isinstance(value["proposed_value"], str) and bool(value["proposed_value"].strip()), "proposed_value is required")
    _expect(isinstance(value["change_reason"], str) and bool(value["change_reason"].strip()), "change_reason is required")

    evidence = value["evidence"]
    _expect(isinstance(evidence, list) and len(evidence) >= 1, "at least one source evidence item is required")
    for index, item in enumerate(evidence):
        prefix = f"evidence[{index}]"
        keys = {"source_id", "source_url", "source_version", "source_content_sha256", "locator", "excerpt"}
        _expect(isinstance(item, dict) and set(item) == keys, f"{prefix} fields are invalid")
        for key in ("source_id", "source_version", "locator", "excerpt"):
            _expect(isinstance(item[key], str) and bool(item[key].strip()), f"{prefix}.{key} is required")
        parsed = urlparse(item["source_url"])
        _expect(parsed.scheme in {"http", "https"} and bool(parsed.netloc), f"{prefix}.source_url must be HTTP(S)")
        _expect(isinstance(item["source_content_sha256"], str) and _HASH_RE.fullmatch(item["source_content_sha256"]) is not None, f"{prefix}.source_content_sha256 must be SHA-256 hex")

    impacts = value["affected_views"]
    _expect(
        isinstance(impacts, list)
        and len(impacts) >= 1
        and all(isinstance(view, str) for view in impacts)
        and len(impacts) == len(set(impacts))
        and set(impacts) <= {"grading", "training", "diagnosis"},
        "affected_views is invalid",
    )
    _expect(value["status"] == "pending_approval", "content proposals must remain pending approval")
    _expect(value["approval_required"] is True, "content proposals require explicit approval")
    return value


def propose_content_update(
    master: dict[str, Any],
    *,
    target: dict[str, Any],
    before_value: str | None,
    proposed_value: str,
    change_reason: str,
    evidence: list[dict[str, Any]],
    proposed_at: str,
) -> dict[str, Any]:
    """Create an evidence-linked pending diff without mutating the Master."""
    try:
        validate_master_topic_pack(master)
    except MasterTopicPackError as exc:
        raise ContentUpdateError(str(exc)) from exc
    source_key = target.get("source_key") if isinstance(target, dict) else None
    if not isinstance(source_key, str) or source_key not in _SOURCE_KEYS:
        raise ContentUpdateError("target source_key is invalid")
    impacts = _affected_views(master, source_key)
    if not impacts:
        raise ContentUpdateError("target source_key is not consumed by any Master View")
    linked_sources = {source["source_id"]: source for source in master["sources"]}
    if not isinstance(evidence, list):
        raise ContentUpdateError("evidence must be an array")
    for item in evidence:
        source = linked_sources.get(item.get("source_id")) if isinstance(item, dict) else None
        if source is None:
            raise ContentUpdateError("evidence source_id must already be linked to this Topic")
        allowed_urls = {source.get("wordpress_url"), source.get("source_url", source.get("wordpress_url"))}
        if item.get("source_url") not in allowed_urls:
            raise ContentUpdateError("evidence source_url does not match the linked source")

    proposal = {
        "schema_version": CONTENT_UPDATE_SCHEMA_VERSION,
        "proposal_id": str(uuid4()),
        "topic_id": master["topic_id"],
        "base_revision": master["revision"],
        "proposed_at": proposed_at,
        "target": copy.deepcopy(target),
        "before_value": before_value,
        "proposed_value": proposed_value,
        "change_reason": change_reason,
        "evidence": copy.deepcopy(evidence),
        "affected_views": impacts,
        "status": "pending_approval",
        "approval_required": True,
    }
    return validate_content_update_proposal(proposal)
