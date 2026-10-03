"""Contracts for additive Master Topic Pack records.

The current Topic Pack remains the grading authority. This module validates
the versioned envelope and will expose read-only projections in later stages.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = "master-topic-pack-v1"
SOURCE_KEYS = {
    "fact_anchor",
    "logic_check",
    "model_answer",
    "topic_importance",
    "question_demand_axes",
}
_REQUIRED_SOURCE_KEYS = SOURCE_KEYS - {"question_demand_axes"}
_SOURCE_TYPES = {
    "wordpress_post",
    "wordpress_page",
    "pdf",
    "overleaf",
    "html",
    "other",
}
_VERIFICATION_STATUSES = {"unverified", "verified", "stale", "unavailable"}


class MasterTopicPackError(ValueError):
    """Raised when a Master Topic Pack violates its schema contract."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise MasterTopicPackError(message)


def _valid_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    parts = value.split("/")
    return not value.startswith("/") and all(part not in {"", ".", ".."} for part in parts)


def _valid_uri(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _validate_source_reference(source: Any, index: int) -> None:
    prefix = f"sources[{index}]"
    _expect(isinstance(source, dict), f"{prefix} must be an object")
    required = {
        "source_id", "source_type", "wordpress_url", "title", "version",
        "page", "section", "updated_at", "verification_status",
    }
    _expect(set(source) == required, f"{prefix} must contain exactly the source reference fields")
    _expect(isinstance(source["source_id"], str) and bool(source["source_id"].strip()), f"{prefix}.source_id is required")
    _expect(source["source_type"] in _SOURCE_TYPES, f"{prefix}.source_type is invalid")
    _expect(isinstance(source["title"], str) and bool(source["title"].strip()), f"{prefix}.title is required")
    _expect(isinstance(source["version"], (str, int)) and not isinstance(source["version"], bool), f"{prefix}.version is invalid")
    _expect(source["page"] is None or isinstance(source["page"], (str, int)), f"{prefix}.page is invalid")
    _expect(source["section"] is None or isinstance(source["section"], str), f"{prefix}.section is invalid")
    _expect(source["verification_status"] in _VERIFICATION_STATUSES, f"{prefix}.verification_status is invalid")
    url = source["wordpress_url"]
    _expect(url is None or _valid_uri(url), f"{prefix}.wordpress_url must be an HTTP(S) URL or null")
    if source["source_type"] in {"wordpress_post", "wordpress_page"}:
        _expect(_valid_uri(url), f"{prefix}.wordpress_url is required for WordPress sources")
    updated_at = source["updated_at"]
    _expect(updated_at is None or isinstance(updated_at, str), f"{prefix}.updated_at is invalid")
    if updated_at is not None:
        try:
            datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise MasterTopicPackError(f"{prefix}.updated_at must be ISO-8601") from exc


def validate_master_topic_pack(value: Any) -> dict[str, Any]:
    """Validate and return a Master Topic Pack mapping without mutating it."""
    _expect(isinstance(value, dict), "Master Topic Pack must be an object")
    required = {
        "schema_version", "topic_id", "title_ko", "revision", "legacy_topic_pack",
        "projections", "sources", "source_update_policy",
    }
    allowed = required | {"$schema"}
    _expect(required <= set(value) and set(value) <= allowed, "Master Topic Pack fields do not match the contract")
    _expect(value["schema_version"] == SCHEMA_VERSION, "unsupported Master Topic Pack schema_version")
    topic_id = value["topic_id"]
    _expect(isinstance(topic_id, str) and len(topic_id) >= 8 and topic_id == topic_id.lower(), "topic_id is invalid")
    _expect(all(part and part.isalnum() for part in topic_id.split("_")), "topic_id must use lowercase alphanumeric segments")
    _expect(isinstance(value["title_ko"], str) and bool(value["title_ko"].strip()), "title_ko is required")
    _expect(isinstance(value["revision"], int) and not isinstance(value["revision"], bool) and value["revision"] >= 1, "revision must be a positive integer")

    legacy = value["legacy_topic_pack"]
    _expect(isinstance(legacy, dict) and set(legacy) == {"source_root", "source_files"}, "legacy_topic_pack fields are invalid")
    _expect(_valid_relative_path(legacy["source_root"]), "legacy source_root must be a safe relative path")
    files = legacy["source_files"]
    _expect(isinstance(files, dict) and _REQUIRED_SOURCE_KEYS <= set(files) <= SOURCE_KEYS, "legacy source_files are incomplete or contain unknown keys")
    _expect(all(_valid_relative_path(path) for path in files.values()), "legacy source file paths must be safe relative paths")

    projections = value["projections"]
    _expect(isinstance(projections, dict) and set(projections) == {"grading", "training", "diagnosis"}, "all three projections are required")
    grading = projections["grading"]
    _expect(isinstance(grading, dict) and set(grading) == {"projection_id", "authority", "source_keys"}, "grading projection fields are invalid")
    _expect(grading["projection_id"] == "grading-projection-v1" and grading["authority"] == "existing_topic_pack", "grading projection must preserve existing grading authority")
    _expect(isinstance(grading["source_keys"], list) and len(grading["source_keys"]) >= 4 and len(set(grading["source_keys"])) == len(grading["source_keys"]), "grading source_keys are invalid")
    _expect(set(grading["source_keys"]) <= set(files), "grading projection references a missing legacy source")

    training = projections["training"]
    _expect(isinstance(training, dict) and set(training) == {"projection_id", "content_sources", "daily_target"}, "training projection fields are invalid")
    _expect(training["projection_id"] == "training-projection-v1", "unsupported training projection")
    _expect(isinstance(training["content_sources"], list) and len(training["content_sources"]) > 0, "training content_sources are required")
    _expect(set(training["content_sources"]) <= set(files), "training projection references a missing legacy source")
    _expect(isinstance(training["daily_target"], int) and not isinstance(training["daily_target"], bool) and training["daily_target"] >= 1, "daily_target must be positive")

    diagnosis = projections["diagnosis"]
    _expect(isinstance(diagnosis, dict) and set(diagnosis) == {"projection_id", "content_sources", "dimensions"}, "diagnosis projection fields are invalid")
    _expect(diagnosis["projection_id"] == "diagnosis-projection-v1", "unsupported diagnosis projection")
    _expect(isinstance(diagnosis["content_sources"], list) and len(diagnosis["content_sources"]) > 0, "diagnosis content_sources are required")
    _expect(set(diagnosis["content_sources"]) <= set(files), "diagnosis projection references a missing legacy source")
    valid_dimensions = {"format", "content", "reasoning", "application", "verification"}
    _expect(isinstance(diagnosis["dimensions"], list) and len(diagnosis["dimensions"]) >= 2 and set(diagnosis["dimensions"]) <= valid_dimensions, "diagnosis dimensions are invalid")

    _expect(isinstance(value["sources"], list), "sources must be an array")
    source_ids: set[str] = set()
    for index, source in enumerate(value["sources"]):
        _validate_source_reference(source, index)
        _expect(source["source_id"] not in source_ids, "source_id values must be unique within a Topic")
        source_ids.add(source["source_id"])

    policy = value["source_update_policy"]
    _expect(policy == {"mode": "proposal_only", "approval_required": True}, "source updates must require approval")
    return value
