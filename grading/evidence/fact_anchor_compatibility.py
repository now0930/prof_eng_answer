"""Opt-in preservation of an already reviewed Fact's prior scoring reference.

This is a representation adapter, not a Fact admission decision. Existing
exclusion/hold and source-approval checks remain authoritative. An unmarked
Anchor is returned unchanged.
"""
from __future__ import annotations

import hashlib
from typing import Any


COMPATIBILITY_VERSION = "fact_anchor_sentence_compat_v1"


def validate_sentence_compatibility(anchor: dict[str, Any]) -> str | None:
    """Validate an optional representation contract, never Fact eligibility."""
    if "sentence_compatibility" not in anchor:
        return None
    marker = anchor["sentence_compatibility"]
    if not isinstance(marker, dict) or set(marker) != {"version", "reference_sha256"}:
        raise ValueError("invalid Fact sentence compatibility metadata")
    if marker["version"] != COMPATIBILITY_VERSION:
        raise ValueError("unsupported Fact sentence compatibility version")
    statement = anchor.get("statement")
    expected = anchor.get("expected")
    accepted = anchor.get("accepted_explanations")
    if (
        not isinstance(statement, str) or not statement.strip()
        or not isinstance(expected, str) or not isinstance(accepted, list)
        or not accepted or accepted[0] != expected
        or not expected.startswith(statement + " ")
        or not statement.endswith((".", "!", "?", "。"))
        or any(key in anchor and anchor[key] != statement for key in ("claim", "description"))
        or hashlib.sha256(expected.encode("utf-8")).hexdigest() != marker["reference_sha256"]
    ):
        raise ValueError("Fact sentence compatibility reference mismatch")
    return expected


def scoring_anchor_view(anchor: dict[str, Any]) -> dict[str, Any]:
    """Use the pinned prior reference only for a valid, explicitly marked view.

    Invalid metadata is ignored here and rejected by existing Topic Pack
    validation. It cannot suppress an axis or grant a Fact scoring authority.
    """
    try:
        expected = validate_sentence_compatibility(anchor)
    except ValueError:
        return anchor
    if expected is None:
        return anchor
    result = dict(anchor)
    result.pop("sentence_compatibility")
    result["statement"] = expected
    for key in ("claim", "description"):
        if key in result:
            result[key] = expected
    return result


def scoring_topic_view(topic: dict[str, Any]) -> dict[str, Any]:
    """Restore baseline Anchor and mirrored core-fact text for scoring context."""
    anchors = topic.get("anchors")
    if not isinstance(anchors, list) or not any(
        isinstance(anchor, dict) and "sentence_compatibility" in anchor
        for anchor in anchors
    ):
        return topic
    # A mirrored core_fact has no ID: a repeated short sentence cannot be
    # attributed safely to just one Anchor. Leave the runtime view untouched.
    for anchor in anchors:
        if not isinstance(anchor, dict) or "sentence_compatibility" not in anchor:
            continue
        if sum(isinstance(other, dict) and other.get("statement") == anchor.get("statement")
               for other in anchors) > 1:
            return topic
    result = dict(topic)
    references: dict[str, str] = {}
    converted = []
    for anchor in anchors:
        if not isinstance(anchor, dict):
            converted.append(anchor)
            continue
        view = scoring_anchor_view(anchor)
        if view is not anchor:
            short = anchor["statement"]
            reference = view["statement"]
            references[short] = reference
        converted.append(view)
    result["anchors"] = converted
    core_facts = topic.get("core_facts")
    if isinstance(core_facts, list):
        result["core_facts"] = [references.get(value, value) if isinstance(value, str) else value
                                for value in core_facts]
    return result
