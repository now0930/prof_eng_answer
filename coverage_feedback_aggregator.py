from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


COVERAGE_FEEDBACK_EVENT_FILENAME = "coverage_feedback_event.json"
COVERAGE_FEEDBACK_AGGREGATE_VERSION = (
    "coverage_feedback_aggregate_v1"
)
DEFAULT_HUMAN_REVIEW_THRESHOLD = 3


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _load_event(path: Path) -> Dict[str, Any] | None:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        return None

    if not isinstance(payload, dict):
        return None
    if payload.get("event_type") != "TOPIC_COVERAGE_GAP":
        return None

    policy = payload.get("policy")
    if not isinstance(policy, dict):
        return None
    if policy.get("score_effect") != "none":
        return None
    if policy.get("routing_effect") != "none":
        return None
    if policy.get("student_answer_used") is not False:
        return None
    if policy.get("auto_topic_pack_creation") is not False:
        return None

    return payload


def iter_session_coverage_events(
    sessions_root: str | Path,
) -> Iterable[Dict[str, Any]]:
    root = Path(sessions_root)
    if not root.is_dir():
        return

    for session_dir in sorted(root.iterdir()):
        if not session_dir.is_dir():
            continue

        event_path = (
            session_dir / COVERAGE_FEEDBACK_EVENT_FILENAME
        )
        if not event_path.is_file():
            continue

        payload = _load_event(event_path)
        if payload is None:
            continue

        yield {
            "session_id": session_dir.name,
            "event_path": str(event_path),
            "event": payload,
        }


def aggregate_coverage_feedback(
    sessions_root: str | Path,
    *,
    human_review_threshold: int = (
        DEFAULT_HUMAN_REVIEW_THRESHOLD
    ),
) -> Dict[str, Any]:
    threshold = max(2, int(human_review_threshold))

    groups: Dict[str, Dict[str, Any]] = {}
    seen_event_fingerprints = set()
    scanned_sessions = 0
    valid_events = 0

    for row in iter_session_coverage_events(
        sessions_root
    ):
        scanned_sessions += 1
        session_id = row["session_id"]
        event = row["event"]

        event_fingerprint = _clean_text(
            event.get("event_fingerprint")
        )
        if not event_fingerprint:
            continue
        if event_fingerprint in seen_event_fingerprints:
            # Avoid duplicate copies of an identical event.
            continue
        seen_event_fingerprints.add(event_fingerprint)
        valid_events += 1

        routing_mode = _clean_text(
            event.get("routing_mode")
        )
        primary_topic_ids = sorted(
            {
                _clean_text(value)
                for value in (
                    event.get("primary_topic_ids") or []
                )
                if _clean_text(value)
            }
        )

        for gap in event.get("gaps") or []:
            if not isinstance(gap, dict):
                continue

            fingerprint = _clean_text(
                gap.get("gap_fingerprint")
            )
            demand_text = _clean_text(
                gap.get("demand_text")
            )
            demand_id = _clean_text(
                gap.get("demand_id")
            )
            if not fingerprint or not demand_text:
                continue

            item = groups.setdefault(
                fingerprint,
                {
                    "gap_fingerprint": fingerprint,
                    "occurrence_count": 0,
                    "session_ids": [],
                    "sample_demand_texts": [],
                    "demand_ids": [],
                    "routing_modes": [],
                    "primary_topic_ids": [],
                },
            )

            if session_id not in item["session_ids"]:
                item["session_ids"].append(session_id)
                item["occurrence_count"] += 1

            if (
                demand_text
                not in item["sample_demand_texts"]
            ):
                item["sample_demand_texts"].append(
                    demand_text
                )

            if (
                demand_id
                and demand_id not in item["demand_ids"]
            ):
                item["demand_ids"].append(demand_id)

            if (
                routing_mode
                and routing_mode
                not in item["routing_modes"]
            ):
                item["routing_modes"].append(
                    routing_mode
                )

            for topic_id in primary_topic_ids:
                if (
                    topic_id
                    not in item["primary_topic_ids"]
                ):
                    item["primary_topic_ids"].append(
                        topic_id
                    )

    aggregates: List[Dict[str, Any]] = []
    for item in groups.values():
        item["session_ids"].sort()
        item["sample_demand_texts"].sort()
        item["demand_ids"].sort()
        item["routing_modes"].sort()
        item["primary_topic_ids"].sort()

        count = int(item["occurrence_count"])
        item["human_review_candidate"] = (
            count >= threshold
        )
        item["promotion_action"] = (
            "HUMAN_REVIEW"
            if count >= threshold
            else "OBSERVE"
        )
        item["auto_topic_pack_creation"] = False
        aggregates.append(item)

    aggregates.sort(
        key=lambda item: (
            -int(item["occurrence_count"]),
            item["gap_fingerprint"],
        )
    )

    review_candidates = sum(
        1
        for item in aggregates
        if item["human_review_candidate"]
    )

    return {
        "version": COVERAGE_FEEDBACK_AGGREGATE_VERSION,
        "sessions_root": str(Path(sessions_root)),
        "valid_event_count": valid_events,
        "unique_gap_count": len(aggregates),
        "human_review_threshold": threshold,
        "human_review_candidate_count": (
            review_candidates
        ),
        "gaps": aggregates,
        "policy": {
            "read_only_source_scan": True,
            "score_effect": "none",
            "routing_effect": "none",
            "student_answer_used": False,
            "semantic_clustering_performed": False,
            "auto_topic_pack_creation": False,
            "human_review_required": True,
            "current_question_effect": "none",
        },
    }
