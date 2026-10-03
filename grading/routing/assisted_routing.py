from __future__ import annotations

import copy
import os
from typing import Any, Dict, Iterable, Optional


ASSISTED_ROUTING_VERSION = "assisted_routing_v1"
ASSISTED_ROUTING_ENV = "ASSISTED_ROUTING_ENABLED"


def _env_flag_enabled(value: Optional[str]) -> bool:
    return str(value or "").strip().casefold() in {
        "1",
        "true",
        "yes",
        "on",
    }


def assisted_routing_enabled() -> bool:
    """Return the Stage 5 assisted-routing feature flag.

    Default is deliberately OFF.  Stage 5 only prepares a safe SINGLE_TOPIC
    overlay; production activation is a separate integration step.
    """

    return _env_flag_enabled(
        os.getenv(ASSISTED_ROUTING_ENV)
    )


def _topic_id_from_reference(value: Any) -> Optional[str]:
    if not isinstance(value, dict):
        return None
    topic_id = str(value.get("topic_id") or "").strip()
    return topic_id or None


def _distinct_topic_ids(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []

    out: list[str] = []
    seen: set[str] = set()

    for value in values:
        topic_id = str(value or "").strip()
        if not topic_id or topic_id in seen:
            continue
        seen.add(topic_id)
        out.append(topic_id)

    return out


def _candidate_reference_by_topic_id(
    shadow_candidate_result: Dict[str, Any],
    topic_id: str,
) -> Optional[Dict[str, Any]]:
    candidates = shadow_candidate_result.get("candidates") or []
    if not isinstance(candidates, list):
        return None

    for row in candidates:
        if not isinstance(row, dict):
            continue

        answer = row.get("answer")
        if not isinstance(answer, dict):
            continue

        answer_topic_id = str(
            answer.get("topic_id") or ""
        ).strip()

        if answer_topic_id == topic_id:
            return copy.deepcopy(answer)

    return None


def _fallback_reason(
    semantic_result: Dict[str, Any],
    shadow_candidate_result: Dict[str, Any],
) -> tuple[str, Optional[str], Optional[Dict[str, Any]]]:
    if semantic_result.get("ok") is not True:
        return "semantic_not_ok", None, None

    mode = str(
        semantic_result.get("routing_mode") or ""
    ).strip()

    if mode != "SINGLE_TOPIC":
        if mode == "MULTI_TOPIC":
            return "multi_topic_deferred_stage_6", None, None
        if mode == "GENERAL":
            return "general_deferred_stage_7", None, None
        if mode == "AMBIGUOUS":
            return "ambiguous_legacy_fallback", None, None
        return "unsupported_semantic_mode", None, None

    primary_topic_ids = _distinct_topic_ids(
        semantic_result.get("primary_topic_ids")
    )

    if len(primary_topic_ids) != 1:
        return "invalid_primary_topic_count", None, None

    topic_id = primary_topic_ids[0]
    reference = _candidate_reference_by_topic_id(
        shadow_candidate_result,
        topic_id,
    )

    if reference is None:
        return "primary_topic_missing_from_candidates", topic_id, None

    return "", topic_id, reference


def build_assisted_model_answer_reference(
    *,
    legacy_result: Dict[str, Any],
    semantic_result: Dict[str, Any],
    shadow_candidate_result: Dict[str, Any],
    enabled: Optional[bool] = None,
) -> Dict[str, Any]:
    """Build a Stage 5 SINGLE_TOPIC assisted-routing overlay.

    The three input objects are treated as immutable audit inputs.
    Existing legacy score/candidate/diagnostic fields are preserved.
    Only a valid semantic SINGLE_TOPIC route may overlay `matched` and
    `primary_reference`.

    MULTI_TOPIC is intentionally deferred to Stage 6.
    GENERAL is intentionally deferred to Stage 7.
    """

    if not isinstance(legacy_result, dict):
        raise TypeError("legacy_result must be a dict")
    if not isinstance(semantic_result, dict):
        raise TypeError("semantic_result must be a dict")
    if not isinstance(shadow_candidate_result, dict):
        raise TypeError("shadow_candidate_result must be a dict")

    result = copy.deepcopy(legacy_result)

    flag_enabled = (
        assisted_routing_enabled()
        if enabled is None
        else bool(enabled)
    )

    legacy_topic_id = _topic_id_from_reference(
        legacy_result.get("primary_reference")
    )

    metadata: Dict[str, Any] = {
        "version": ASSISTED_ROUTING_VERSION,
        "enabled": flag_enabled,
        "applied": False,
        "source": "legacy",
        "legacy_selected_topic_id": legacy_topic_id,
        "semantic_selected_topic_id": None,
        "selected_topic_id": legacy_topic_id,
        "fallback_reason": "",
        "student_answer_used": False,
        "multi_topic_enabled": False,
        "general_enabled": False,
        "score_policy_changed": False,
        "legacy_router_mutated": False,
    }

    if not flag_enabled:
        metadata["fallback_reason"] = "feature_flag_off"
        result["assisted_routing"] = metadata
        return result

    reason, semantic_topic_id, canonical_reference = _fallback_reason(
        semantic_result,
        shadow_candidate_result,
    )

    metadata["semantic_selected_topic_id"] = semantic_topic_id

    if reason:
        metadata["fallback_reason"] = reason
        result["assisted_routing"] = metadata
        return result

    assert semantic_topic_id is not None
    assert canonical_reference is not None

    # Stage 5 overlay boundary: only these two existing legacy contract
    # fields are changed.  Score-family and candidate diagnostics remain
    # untouched until later stages explicitly redefine those contracts.
    result["matched"] = True
    result["primary_reference"] = canonical_reference

    metadata.update(
        {
            "applied": True,
            "source": "semantic_single_topic",
            "selected_topic_id": semantic_topic_id,
            "fallback_reason": "",
        }
    )
    result["assisted_routing"] = metadata
    return result
