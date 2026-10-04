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


def validate_content_update_against_master(master: dict[str, Any], proposal: dict[str, Any]) -> None:
    try:
        validate_master_topic_pack(master)
    except MasterTopicPackError as exc:
        raise ContentUpdateError(str(exc)) from exc
    if proposal["topic_id"] != master["topic_id"] or proposal["base_revision"] != master["revision"]:
        raise ContentUpdateError("proposal does not match the current Master revision")
    target = proposal["target"]
    source_key = target["source_key"]
    if source_key not in master["legacy_topic_pack"]["source_files"]:
        raise ContentUpdateError("target source_key is not part of this Topic Pack")
    if proposal["affected_views"] != _affected_views(master, source_key):
        raise ContentUpdateError("affected_views do not match current Master projections")
    linked_sources = {source["source_id"]: source for source in master["sources"]}
    for item in proposal["evidence"]:
        source = linked_sources.get(item["source_id"])
        if source is None:
            raise ContentUpdateError("proposal evidence is no longer linked to this Topic")
        allowed_urls = {source.get("wordpress_url"), source.get("source_url", source.get("wordpress_url"))}
        if item["source_url"] not in allowed_urls:
            raise ContentUpdateError("proposal evidence URL does not match the linked source")


def validate_content_update_proposal(value: Any) -> dict[str, Any]:
    """Validate a proposal lifecycle record without applying its diff."""
    _expect(isinstance(value, dict), "content update proposal must be an object")
    required = {
        "schema_version", "proposal_id", "topic_id", "base_revision", "proposed_at",
        "target", "before_value", "proposed_value", "change_reason", "evidence",
        "affected_views", "status", "approval_required",
    }
    optional = {
        "approved_by", "approved_at", "rejected_by", "rejected_at",
        "candidate_ready_at", "candidate_revision", "applied_by", "applied_at",
    }
    _expect(required <= set(value) <= required | optional, "content update proposal fields do not match the contract")
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
    status = value["status"]
    _expect(status in {"pending_approval", "approved", "rejected", "candidate_ready", "applied"}, "content proposal status is invalid")
    _expect(value["approval_required"] is True, "content proposals require explicit approval")
    if status in {"approved", "candidate_ready", "applied"}:
        _expect(isinstance(value.get("approved_by"), str) and bool(value["approved_by"].strip()), "approved_by is required")
        _validate_timestamp(value.get("approved_at"), "approved_at")
    if status == "rejected":
        _expect(isinstance(value.get("rejected_by"), str) and bool(value["rejected_by"].strip()), "rejected_by is required")
        _validate_timestamp(value.get("rejected_at"), "rejected_at")
    if status in {"candidate_ready", "applied"}:
        _validate_timestamp(value.get("candidate_ready_at"), "candidate_ready_at")
        _expect(isinstance(value.get("candidate_revision"), int) and value["candidate_revision"] >= 2, "candidate_revision is invalid")
    if status == "applied":
        _expect(isinstance(value.get("applied_by"), str) and bool(value["applied_by"].strip()), "applied_by is required")
        _validate_timestamp(value.get("applied_at"), "applied_at")
    expected_optional = {
        "pending_approval": set(),
        "approved": {"approved_by", "approved_at"},
        "rejected": {"rejected_by", "rejected_at"},
        "candidate_ready": {"approved_by", "approved_at", "candidate_ready_at", "candidate_revision"},
        "applied": {"approved_by", "approved_at", "candidate_ready_at", "candidate_revision", "applied_by", "applied_at"},
    }[status]
    _expect(set(value) == required | expected_optional, "proposal lifecycle fields do not match its status")
    return value


def _validate_timestamp(value: Any, field: str) -> None:
    _expect(isinstance(value, str), f"{field} must be ISO-8601")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContentUpdateError(f"{field} must be ISO-8601") from exc
    _expect(parsed.tzinfo is not None, f"{field} must include a timezone")


def approve_content_update(
    master: dict[str, Any],
    proposal: dict[str, Any],
    *,
    approved_by: str | None,
    approved_at: str,
) -> dict[str, Any]:
    """Record explicit approval without applying the proposed field change."""
    validate_content_update_proposal(proposal)
    validate_content_update_against_master(master, proposal)
    if proposal["status"] != "pending_approval":
        raise ContentUpdateError("proposal is not awaiting approval")
    _expect(isinstance(approved_by, str) and bool(approved_by.strip()), "an explicit approver identity is required")
    _validate_timestamp(approved_at, "approved_at")
    approved = copy.deepcopy(proposal)
    approved.update(status="approved", approved_by=approved_by.strip(), approved_at=approved_at)
    return validate_content_update_proposal(approved)


def reject_content_update(
    proposal: dict[str, Any], *, rejected_by: str | None, rejected_at: str
) -> dict[str, Any]:
    """Record explicit rejection without changing Topic content."""
    validate_content_update_proposal(proposal)
    if proposal["status"] != "pending_approval":
        raise ContentUpdateError("proposal is not awaiting approval")
    _expect(isinstance(rejected_by, str) and bool(rejected_by.strip()), "an explicit reviewer identity is required")
    _validate_timestamp(rejected_at, "rejected_at")
    rejected = copy.deepcopy(proposal)
    rejected.update(status="rejected", rejected_by=rejected_by.strip(), rejected_at=rejected_at)
    return validate_content_update_proposal(rejected)


def mark_content_update_applied(
    proposal: dict[str, Any], *, applied_by: str | None, applied_at: str
) -> dict[str, Any]:
    """Record the final canonical-apply identity after a successful write."""
    validate_content_update_proposal(proposal)
    if proposal["status"] != "candidate_ready":
        raise ContentUpdateError("only a ready candidate can be marked applied")
    _expect(isinstance(applied_by, str) and bool(applied_by.strip()), "an explicit apply identity is required")
    _validate_timestamp(applied_at, "applied_at")
    applied = copy.deepcopy(proposal)
    applied.update(status="applied", applied_by=applied_by.strip(), applied_at=applied_at)
    return validate_content_update_proposal(applied)


def _find_target_record(value: Any, record_id: str, matches: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if any(value.get(key) == record_id for key in ("id", "anchor_id", "check_id", "pattern_id", "point_id")):
            matches.append(value)
        for child in value.values():
            _find_target_record(child, record_id, matches)
    elif isinstance(value, list):
        for child in value:
            _find_target_record(child, record_id, matches)


def apply_approved_content_update(
    master: dict[str, Any],
    source_payloads: dict[str, dict[str, Any]],
    proposal: dict[str, Any],
    *,
    candidate_ready_at: str,
) -> dict[str, Any]:
    """Return a candidate transformation; never writes files or the Master."""
    validate_content_update_against_master(master, proposal)
    validate_content_update_proposal(proposal)
    if proposal["status"] != "approved":
        raise ContentUpdateError("content proposal must be explicitly approved before apply")
    _validate_timestamp(candidate_ready_at, "candidate_ready_at")
    target = proposal["target"]
    key = target["source_key"]
    if key not in source_payloads or not isinstance(source_payloads[key], dict):
        raise ContentUpdateError("target source payload is unavailable")
    current_source = source_payloads[key]
    if current_source.get("topic_id") != master["topic_id"]:
        raise ContentUpdateError("target source payload belongs to another Topic")
    records: list[dict[str, Any]] = []
    _find_target_record(current_source, target["record_id"], records)
    if len(records) != 1:
        raise ContentUpdateError("target record must resolve to exactly one source record")
    record = records[0]
    field_path = target["field_path"]
    parent: Any = record
    for part in field_path[:-1]:
        if not isinstance(parent, dict) or part not in parent:
            raise ContentUpdateError("target field path does not exist")
        parent = parent[part]
    field = field_path[-1]
    if not isinstance(parent, dict) or field not in parent:
        raise ContentUpdateError("target field path does not exist")
    if parent[field] != proposal["before_value"]:
        raise ContentUpdateError("target before_value no longer matches current content")

    updated_master = copy.deepcopy(master)
    updated_master["revision"] += 1
    updated_sources = copy.deepcopy(source_payloads)
    updated_sources[key]["topic_id"] = master["topic_id"]
    updated_record_matches: list[dict[str, Any]] = []
    _find_target_record(updated_sources[key], target["record_id"], updated_record_matches)
    updated_parent: Any = updated_record_matches[0]
    for part in field_path[:-1]:
        updated_parent = updated_parent[part]
    updated_parent[field] = proposal["proposed_value"]
    applied = copy.deepcopy(proposal)
    applied.update(
        status="candidate_ready",
        candidate_ready_at=candidate_ready_at,
        candidate_revision=updated_master["revision"],
    )
    validate_content_update_proposal(applied)
    return {
        "master": updated_master,
        "source_payloads": updated_sources,
        "proposal": applied,
    }


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
