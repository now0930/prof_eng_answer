from __future__ import annotations

from typing import Any, Dict, Iterable, List


COVERAGE_REVIEW_REPORT_VERSION = (
    "coverage_review_candidate_report_v1"
)


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _candidate_rows(
    aggregate: Any,
) -> Iterable[Dict[str, Any]]:
    if not isinstance(aggregate, dict):
        return []

    rows: List[Dict[str, Any]] = []
    for raw in aggregate.get("gaps") or []:
        if not isinstance(raw, dict):
            continue

        fingerprint = _clean_text(
            raw.get("gap_fingerprint")
        )
        if not fingerprint:
            continue

        count = int(raw.get("occurrence_count") or 0)
        action = _clean_text(
            raw.get("promotion_action")
        )
        human_review = (
            raw.get("human_review_candidate") is True
        )

        if human_review:
            action = "HUMAN_REVIEW"
        elif action != "HUMAN_REVIEW":
            action = "OBSERVE"

        rows.append(
            {
                "gap_fingerprint": fingerprint,
                "occurrence_count": count,
                "review_status": action,
                "human_review_candidate": human_review,
                "sample_demand_texts": list(
                    raw.get("sample_demand_texts") or []
                )[:5],
                "session_ids": list(
                    raw.get("session_ids") or []
                ),
                "routing_modes": list(
                    raw.get("routing_modes") or []
                ),
                "primary_topic_ids": list(
                    raw.get("primary_topic_ids") or []
                ),
                "recommended_action": (
                    "Review whether this recurring uncovered "
                    "demand justifies a new or expanded Topic Pack."
                    if human_review
                    else
                    "Keep observing recurrence; do not change Topic Packs."
                ),
            }
        )

    rows.sort(
        key=lambda row: (
            0
            if row["human_review_candidate"]
            else 1,
            -int(row["occurrence_count"]),
            row["gap_fingerprint"],
        )
    )
    return rows


def build_coverage_review_report(
    aggregate: Any,
) -> Dict[str, Any]:
    if not isinstance(aggregate, dict):
        aggregate = {}

    candidates = list(_candidate_rows(aggregate))
    review_count = sum(
        1
        for row in candidates
        if row["human_review_candidate"]
    )

    return {
        "version": COVERAGE_REVIEW_REPORT_VERSION,
        "source_aggregate_version": aggregate.get(
            "version"
        ),
        "valid_event_count": int(
            aggregate.get("valid_event_count") or 0
        ),
        "unique_gap_count": int(
            aggregate.get("unique_gap_count") or 0
        ),
        "human_review_threshold": int(
            aggregate.get("human_review_threshold") or 0
        ),
        "human_review_candidate_count": review_count,
        "candidates": candidates,
        "policy": {
            "report_only": True,
            "current_question_effect": "none",
            "score_effect": "none",
            "routing_effect": "none",
            "student_answer_used": False,
            "auto_topic_pack_creation": False,
            "auto_topic_pack_update": False,
            "human_review_required": True,
        },
    }


def render_coverage_review_markdown(
    report: Any,
) -> str:
    if not isinstance(report, dict):
        report = {}

    lines = [
        "# Coverage Feedback Review",
        "",
        (
            f"- Valid events: "
            f"{int(report.get('valid_event_count') or 0)}"
        ),
        (
            f"- Unique gaps: "
            f"{int(report.get('unique_gap_count') or 0)}"
        ),
        (
            f"- Human-review candidates: "
            f"{int(report.get('human_review_candidate_count') or 0)}"
        ),
        "",
    ]

    candidates = report.get("candidates") or []
    if not candidates:
        lines.extend(
            [
                "No coverage-gap observations are available.",
                "",
            ]
        )
        return "\n".join(lines)

    for index, row in enumerate(candidates, 1):
        status = _clean_text(
            row.get("review_status")
        ) or "OBSERVE"
        count = int(
            row.get("occurrence_count") or 0
        )
        lines.extend(
            [
                f"## {index}. {status}",
                "",
                f"- Occurrences: {count}",
                (
                    "- Gap fingerprint: "
                    + _clean_text(
                        row.get("gap_fingerprint")
                    )
                ),
            ]
        )

        texts = [
            _clean_text(value)
            for value in (
                row.get("sample_demand_texts") or []
            )
            if _clean_text(value)
        ]
        if texts:
            lines.append(
                "- Sample demand: " + texts[0]
            )

        topics = [
            _clean_text(value)
            for value in (
                row.get("primary_topic_ids") or []
            )
            if _clean_text(value)
        ]
        lines.append(
            "- Related primary Topics: "
            + (
                ", ".join(topics)
                if topics
                else "(none)"
            )
        )

        lines.append(
            "- Recommended action: "
            + _clean_text(
                row.get("recommended_action")
            )
        )
        lines.append("")

    lines.extend(
        [
            "## Governance",
            "",
            (
                "This report is advisory only. "
                "It does not change routing, scoring, "
                "or Topic Packs automatically."
            ),
            "",
        ]
    )
    return "\n".join(lines)
