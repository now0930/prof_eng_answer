"""Project the existing deterministic grade into a scoped D/E shadow input."""

from __future__ import annotations

from typing import Any, Mapping


ABC_KEYS = ("A_structure", "B_requirement_completeness", "C_fact_correctness")


def project_deterministic_shadow_input(grade: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Use requirement owners, never all router candidates, as D/E topic scope.

    This adapter copies only the established A/B/C evidence. It cannot
    recalculate scores or promote LLM suggestions to deterministic findings.
    """
    if grade.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
        raise ValueError("non_deterministic_grade")
    routed = grade.get("topic_ids")
    rows = grade.get("requirements")
    scores = (grade.get("deterministic_score") or {}).get("score_breakdown")
    if not isinstance(routed, list) or not isinstance(rows, list) or not isinstance(scores, dict):
        raise ValueError("incomplete_deterministic_grade")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("invalid_requirement_rows")
    owners = {row.get("owner_topic_id") for row in rows}
    if not owners or any(not isinstance(owner, str) or not owner or owner not in routed for owner in owners):
        raise ValueError("unresolved_requirement_topic_scope")
    abc_result = {
        "score_breakdown": {key: scores[key] for key in ABC_KEYS},
        "requirements": [{key: row.get(key) for key in
                          ("requirement_id", "owner_topic_id", "status", "source_span", "source_spans", "evidence_text") if key in row}
                         for row in rows],
    }
    topic_context = {"topic_ids": [topic for topic in routed if topic in owners], "verified_facts": []}
    return abc_result, topic_context
