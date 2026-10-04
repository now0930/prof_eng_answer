from __future__ import annotations

import json
from typing import Any


HYBRID_GENERAL_PROMPT_MARKER = (
    "[HYBRID_GENERAL_GRADING_EVIDENCE_V1]"
)


def _compact(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def build_hybrid_general_prompt_section(
    subject_rubric: Any,
) -> str:
    if not isinstance(subject_rubric, dict):
        return ""

    evidence = subject_rubric.get(
        "hybrid_general_grading_evidence"
    )
    if not isinstance(evidence, dict):
        return ""

    coverage_kind = str(
        evidence.get("coverage_kind") or ""
    ).strip()
    routing_mode = str(
        evidence.get("routing_mode") or ""
    ).strip()

    if coverage_kind not in {
        "PURE_GENERAL",
        "HYBRID_TOPIC_GENERAL",
    }:
        return ""

    general = evidence.get(
        "general_engineering_evidence"
    )
    if not isinstance(general, dict):
        return ""
    if general.get("score_component") is not False:
        return ""

    topics = evidence.get("topics") or []
    if not isinstance(topics, list):
        topics = []

    topic_payload = []
    for row in topics:
        if not isinstance(row, dict):
            continue
        topic_id = str(row.get("topic_id") or "").strip()
        if not topic_id:
            continue
        topic_payload.append(
            {
                "topic_id": topic_id,
                "title": row.get("title"),
                "model_answer": row.get("model_answer"),
                "fact_anchor": row.get("fact_anchor"),
            }
        )

    demands = general.get("demands") or []
    if not isinstance(demands, list):
        demands = []

    payload = {
        "routing_mode": routing_mode,
        "coverage_kind": coverage_kind,
        "primary_topic_ids": evidence.get(
            "primary_topic_ids"
        )
        or [],
        "topic_evidence": topic_payload,
        "demand_mappings": evidence.get(
            "demand_mappings"
        )
        or [],
        "general_engineering_demands": demands,
        "uncovered_demand_ids": evidence.get(
            "uncovered_demand_ids"
        )
        or [],
    }

    return f"""
{HYBRID_GENERAL_PROMPT_MARKER}

이 블록은 Topic Router v2 Stage 7의 채점 근거다.

규칙:
1. 전체 문제와 학생 답안을 한 번만 평가한다.
2. Topic evidence와 General Engineering evidence를 하나의 holistic evidence로 사용한다.
3. Topic 점수와 General 점수를 따로 만들거나 합산·평균하지 않는다.
4. 기존 A/B/C/D/E 계층과 총점 25점 산식을 변경하지 않는다.
5. GENERAL evidence는 supplied Topic Pack으로 충분히 소유되지 않은 question demand에만 사용한다.
6. Topic evidence의 model_answer와 fact_anchor는 해당 Topic demand의 기준으로만 사용한다.
7. GENERAL이라는 이유만으로 감점하거나 가점하지 않는다.
8. AMBIGUOUS를 GENERAL로 해석하지 않는다.
9. 학생 답안으로 routing_mode, coverage_kind, uncovered demand를 다시 판정하지 않는다.
10. 기존 general_evidence_contract는 별도의 post-grading diagnostic contract이므로 이 routing evidence와 혼동하지 않는다.

HYBRID_GENERAL_CONTEXT={_compact(payload)}
""".strip()
