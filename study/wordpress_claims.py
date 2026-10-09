"""Validation contract for WordPress evidence claims before Topic promotion."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

CLAIM_SCHEMA_VERSION = "wordpress-claim-v1"
SOURCE_KEYS = {"fact_anchor", "logic_check", "model_answer", "topic_importance", "question_demand_axes"}
CLAIM_TYPES = {"definition", "formula", "condition", "classification", "causal", "application", "boundary", "fatal_claim"}
STATUSES = {"candidate", "human_review_required", "approved", "rejected"}
TOPIC_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")
CLAIM_RE = re.compile(r"^[A-Z][A-Z0-9_-]+$")
HASH_RE = re.compile(r"^[a-fA-F0-9]{64}$")


class WordPressClaimError(ValueError):
    """Raised when a WordPress claim cannot enter a Topic proposal."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise WordPressClaimError(message)


def validate_wordpress_claim(value: Any) -> dict[str, Any]:
    """Validate a claim without changing any source, Master, or Topic file."""
    _expect(isinstance(value, dict), "claim must be an object")
    required = {"schema_version", "claim_id", "topic_id", "claim_type", "claim_text", "evidence", "target", "review_status", "score_effect"}
    optional = {"conditions", "units"}
    _expect(required <= set(value) <= required | optional, "claim fields do not match wordpress-claim-v1")
    _expect(value["schema_version"] == CLAIM_SCHEMA_VERSION, "unsupported claim schema")
    _expect(isinstance(value["claim_id"], str) and CLAIM_RE.fullmatch(value["claim_id"] or "") is not None, "claim_id is invalid")
    _expect(isinstance(value["topic_id"], str) and TOPIC_RE.fullmatch(value["topic_id"] or "") is not None, "topic_id is invalid")
    _expect(value["claim_type"] in CLAIM_TYPES, "claim_type is invalid")
    _expect(isinstance(value["claim_text"], str) and bool(value["claim_text"].strip()), "claim_text is required")
    for field in ("conditions", "units"):
        if field in value:
            _expect(isinstance(value[field], list) and all(isinstance(item, str) for item in value[field]), f"{field} must be a string list")
    evidence = value["evidence"]
    _expect(isinstance(evidence, list) and len(evidence) >= 1, "at least one evidence item is required")
    for index, item in enumerate(evidence):
        _expect(isinstance(item, dict), f"evidence[{index}] must be an object")
        fields = {"source_id", "source_url", "source_version", "source_content_sha256", "locator", "excerpt"}
        _expect(set(item) == fields, f"evidence[{index}] fields are invalid")
        for field in ("source_id", "source_version", "locator", "excerpt"):
            _expect(isinstance(item[field], str) and bool(item[field].strip()), f"evidence[{index}].{field} is required")
        parsed = urlparse(item["source_url"])
        _expect(parsed.scheme in {"http", "https"} and bool(parsed.netloc), f"evidence[{index}].source_url is invalid")
        _expect(HASH_RE.fullmatch(item["source_content_sha256"] or "") is not None, f"evidence[{index}] hash is invalid")
    target = value["target"]
    _expect(isinstance(target, dict) and set(target) == {"source_key", "record_id"}, "target fields are invalid")
    _expect(target["source_key"] in SOURCE_KEYS, "target source_key is invalid")
    _expect(isinstance(target["record_id"], str) and bool(target["record_id"].strip()), "target record_id is required")
    _expect(value["review_status"] in STATUSES, "review_status is invalid")
    _expect(value["score_effect"] == "none", "WordPress claim cannot have score effect before canonical approval")
    return value
