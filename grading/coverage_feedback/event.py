from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, List, Optional


COVERAGE_FEEDBACK_EVENT_VERSION = "coverage_gap_event_v1"
COVERAGE_FEEDBACK_EVENT_TYPE = "TOPIC_COVERAGE_GAP"


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _stable_text(value: Any) -> str:
    text = _clean_text(value).lower()
    return re.sub(r"\s+", " ", text).strip()


def _sha256_text(value: Any) -> str:
    return hashlib.sha256(
        _stable_text(value).encode("utf-8")
    ).hexdigest()


def _demand_rows(
    question_demand_result: Any,
) -> Dict[str, Dict[str, str]]:
    if not isinstance(question_demand_result, dict):
        return {}
    if question_demand_result.get("ok") is not True:
        return {}

    rows: Dict[str, Dict[str, str]] = {}
    for raw in question_demand_result.get("demands") or []:
        if not isinstance(raw, dict):
            continue

        demand_id = _clean_text(
            raw.get("demand_id") or raw.get("id")
        )
        if not demand_id:
            continue

        demand_text = _clean_text(
            raw.get("text")
            or raw.get("demand")
            or raw.get("description")
        )
        rows[demand_id] = {
            "demand_id": demand_id,
            "demand_text": demand_text,
        }
    return rows


def build_coverage_feedback_event(
    semantic_result: Any,
    question_demand_result: Any,
) -> Optional[Dict[str, Any]]:
    """
    Build a non-scoring, downstream-only coverage observation.

    This function intentionally accepts no student-answer argument.
    It never changes routing and never promotes a Topic Pack.
    """
    if not isinstance(semantic_result, dict):
        return None
    if semantic_result.get("ok") is not True:
        return None

    routing_mode = _clean_text(
        semantic_result.get("routing_mode")
    )
    if routing_mode not in {
        "GENERAL",
        "SINGLE_TOPIC",
        "MULTI_TOPIC",
    }:
        # AMBIGUOUS is uncertainty, not evidence of a missing Topic.
        return None

    demand_rows = _demand_rows(question_demand_result)
    if not demand_rows:
        return None

    uncovered_ids: List[str] = []
    seen = set()
    for raw in semantic_result.get("uncovered_demand_ids") or []:
        demand_id = _clean_text(raw)
        if not demand_id or demand_id in seen:
            continue
        if demand_id not in demand_rows:
            # Never invent or persist unknown demand ids.
            continue
        seen.add(demand_id)
        uncovered_ids.append(demand_id)

    if not uncovered_ids:
        return None

    gaps = []
    for demand_id in uncovered_ids:
        row = demand_rows[demand_id]
        demand_text = row["demand_text"]
        gaps.append(
            {
                "demand_id": demand_id,
                "demand_text": demand_text,
                "gap_fingerprint": _sha256_text(demand_text),
            }
        )

    primary_topic_ids = sorted(
        {
            _clean_text(value)
            for value in (
                semantic_result.get("primary_topic_ids") or []
            )
            if _clean_text(value)
        }
    )
    supporting_topic_ids = sorted(
        {
            _clean_text(value)
            for value in (
                semantic_result.get("supporting_topic_ids") or []
            )
            if _clean_text(value)
        }
    )

    identity_payload = {
        "routing_mode": routing_mode,
        "primary_topic_ids": primary_topic_ids,
        "supporting_topic_ids": supporting_topic_ids,
        "gaps": [
            {
                "demand_id": row["demand_id"],
                "gap_fingerprint": row["gap_fingerprint"],
            }
            for row in gaps
        ],
    }
    event_fingerprint = hashlib.sha256(
        json.dumps(
            identity_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    return {
        "version": COVERAGE_FEEDBACK_EVENT_VERSION,
        "event_type": COVERAGE_FEEDBACK_EVENT_TYPE,
        "event_fingerprint": event_fingerprint,
        "routing_mode": routing_mode,
        "primary_topic_ids": primary_topic_ids,
        "supporting_topic_ids": supporting_topic_ids,
        "uncovered_demand_ids": uncovered_ids,
        "gaps": gaps,
        "policy": {
            "downstream_observation_only": True,
            "score_effect": "none",
            "routing_effect": "none",
            "student_answer_used": False,
            "auto_topic_pack_creation": False,
            "human_review_required_for_promotion": True,
            "ambiguous_mode_is_coverage_gap": False,
        },
    }
