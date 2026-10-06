"""Proposal-first source update interface for future WordPress sync."""

from __future__ import annotations

import copy
from datetime import datetime
from typing import Any
from uuid import uuid4

from .master_topic_pack import (
    MasterTopicPackError,
    validate_master_topic_pack,
    validate_source_reference,
)


class SourceUpdateError(ValueError):
    pass


def find_topics_for_source(masters: list[dict[str, Any]], source_id: str) -> list[str]:
    """Return topic IDs that currently reference a source identifier."""
    topic_ids = []
    for master in masters:
        try:
            validate_master_topic_pack(master)
        except MasterTopicPackError as exc:
            raise SourceUpdateError(str(exc)) from exc
        if any(source.get("source_id") == source_id for source in master["sources"]):
            topic_ids.append(master["topic_id"])
    return sorted(set(topic_ids))


def propose_source_update(
    master: dict[str, Any],
    source_reference: dict[str, Any],
    *,
    proposed_at: str,
) -> dict[str, Any]:
    """Create a pending proposal; this function never mutates the Master."""
    validate_master_topic_pack(master)
    try:
        validate_source_reference(source_reference)
    except MasterTopicPackError as exc:
        raise SourceUpdateError(str(exc)) from exc
    try:
        timestamp = datetime.fromisoformat(proposed_at.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise SourceUpdateError("proposed_at must be ISO-8601") from exc
    if timestamp.tzinfo is None:
        raise SourceUpdateError("proposed_at must include a timezone")
    return {
        "proposal_id": str(uuid4()),
        "topic_id": master["topic_id"],
        "source_id": source_reference["source_id"],
        "base_revision": master["revision"],
        "proposed_at": timestamp.isoformat(),
        "source_reference": copy.deepcopy(source_reference),
        "status": "pending_approval",
        "approval_required": True,
    }


def apply_approved_source_update(
    master: dict[str, Any],
    proposal: dict[str, Any],
    *,
    approved_by: str | None,
) -> dict[str, Any]:
    """Apply a proposal only when an explicit approval identity is supplied."""
    if not approved_by or not approved_by.strip():
        raise SourceUpdateError("an explicit approver identity is required")
    return preview_source_update(master, proposal)


def preview_source_update(master: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
    """Validate a pending source-reference change and return its Master preview."""
    validate_master_topic_pack(master)
    if proposal.get("status") != "pending_approval" or proposal.get("approval_required") is not True:
        raise SourceUpdateError("proposal is not awaiting approval")
    if proposal.get("topic_id") != master["topic_id"] or proposal.get("base_revision") != master["revision"]:
        raise SourceUpdateError("proposal does not match the current Master revision")
    reference = proposal.get("source_reference")
    try:
        validate_source_reference(reference)
    except MasterTopicPackError as exc:
        raise SourceUpdateError(str(exc)) from exc
    if reference.get("source_id") != proposal.get("source_id"):
        raise SourceUpdateError("proposal source_id mismatch")

    updated = copy.deepcopy(master)
    matched = False
    for index, existing in enumerate(updated["sources"]):
        if existing["source_id"] == proposal["source_id"]:
            replacement = copy.deepcopy(reference)
            # Training scope is a Master-owned editorial policy, not WordPress
            # source metadata. A routine version refresh must not silently
            # broaden learner-visible material.
            if "training_scope" in existing and "training_scope" not in replacement:
                replacement["training_scope"] = copy.deepcopy(existing["training_scope"])
            updated["sources"][index] = replacement
            matched = True
            break
    if not matched:
        updated["sources"].append(copy.deepcopy(reference))
    updated["revision"] += 1
    validate_master_topic_pack(updated)
    return updated
