#!/usr/bin/env python3
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from rubric_registry import load_topic_importance_bank


DIFFICULTY_PROFILE_PATH = Path("rubrics/difficulty_profiles/default.json")
TOPIC_IMPORTANCE_PATH = None  # deprecated: use load_topic_importance_bank()
EXAM_SELECTION_PATH = Path("rubrics/exam_selection/default.json")


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize(text: str) -> str:
    text = str(text or "").lower()
    text = text.replace("ζ", "zeta")
    text = text.replace("ω", "omega")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_difficulty_profiles() -> Dict[str, Any]:
    return _load_topic_importance_bank()


def load_topic_importance() -> Dict[str, Any]:
    return _load_topic_importance_bank()


def load_exam_selection_policy() -> Dict[str, Any]:
    return _load_topic_importance_bank()


def classify_question_difficulty(question_text: str) -> Dict[str, Any]:
    topic_data = load_topic_importance()
    q = _normalize(question_text)

    best = None
    best_score = 0

    for topic in topic_data.get("topics", []):
        score = 0
        hits = []

        for alias in topic.get("aliases", []):
            a = _normalize(alias)
            if not a:
                continue
            if a in q:
                score += max(1, len(a))
                hits.append(alias)

        if score > best_score:
            best = dict(topic)
            best["matched_aliases"] = hits
            best_score = score

    if best:
        best["matched"] = True
        best["match_score"] = best_score
        return best

    default_policy = dict(topic_data.get("default_topic_policy", {}))
    default_policy.update({
        "topic_id": "unknown",
        "label": "미분류 주제",
        "matched": False,
        "matched_aliases": [],
        "match_score": 0
    })
    return default_policy


def get_profile_policy(difficulty: str) -> Dict[str, Any]:
    profiles = load_difficulty_profiles().get("profiles", {})
    return profiles.get(difficulty, profiles.get("FIELD_APPLICATION", {}))


def summarize_question_strategy(question_text: str) -> Dict[str, Any]:
    topic = classify_question_difficulty(question_text)
    profile = get_profile_policy(topic.get("difficulty"))

    return {
        "question": question_text,
        "topic_id": topic.get("topic_id"),
        "topic_label": topic.get("label"),
        "matched": topic.get("matched"),
        "matched_aliases": topic.get("matched_aliases", []),
        "difficulty": topic.get("difficulty"),
        "difficulty_label": profile.get("label"),
        "selection_importance": topic.get("selection_importance"),
        "selection_policy": topic.get("selection_policy"),
        "minimum_attempt_floor": topic.get("minimum_attempt_floor"),
        "target_score": topic.get("target_score"),
        "excellent_score_band": topic.get("excellent_score_band"),
        "default_score_ceiling": profile.get("default_score_ceiling"),
        "requires_band_unlock": profile.get("scoring_policy", {}).get("requires_band_unlock", False),
        "omission_risk": topic.get("omission_risk"),
        "fatal_error_risk": topic.get("fatal_error_risk"),
        "score_ceiling_policy": topic.get("score_ceiling_policy")
    }


def evaluate_exam_selection(
    questions: List[str],
    selected_numbers: List[int],
    expected_scores: Optional[Dict[int, float]] = None
) -> Dict[str, Any]:
    expected_scores = expected_scores or {}
    selected_set = set(int(x) for x in selected_numbers)

    analyzed = []
    risks = []
    positives = []

    for idx, question in enumerate(questions, start=1):
        item = summarize_question_strategy(question)
        item["number"] = idx
        item["selected"] = idx in selected_set
        item["expected_score"] = expected_scores.get(idx)
        analyzed.append(item)

    offered_core = [
        x for x in analyzed
        if x.get("selection_importance") == "CORE_MUST_PREPARE"
    ]
    selected_core = [x for x in offered_core if x.get("selected")]
    omitted_core = [x for x in offered_core if not x.get("selected")]

    if omitted_core:
        risks.append({
            "rule_id": "core_must_prepare_omitted",
            "severity": "high",
            "message": "반복 출제되는 핵심 변별 문항을 회피한 선택입니다. 직접 감점은 아니지만 고득점 안정성이 낮아질 수 있습니다.",
            "questions": [
                {
                    "number": x["number"],
                    "topic_id": x.get("topic_id"),
                    "topic_label": x.get("topic_label"),
                    "difficulty": x.get("difficulty")
                }
                for x in omitted_core
            ]
        })

    selected_items = [x for x in analyzed if x.get("selected")]
    low_ceiling_count = sum(
        1 for x in selected_items
        if x.get("difficulty") in {"BASIC_CONCEPT", "FIELD_APPLICATION"}
    )
    theory_selected = [x for x in selected_items if x.get("difficulty") == "THEORY_CORE"]

    if len(selected_items) >= 4 and low_ceiling_count >= 4:
        risks.append({
            "rule_id": "all_safe_low_ceiling",
            "severity": "medium",
            "message": "선택한 4문제가 안정형 주제 위주입니다. 평균 통과는 가능하나 고득점 ceiling은 낮을 수 있습니다."
        })

    for item in theory_selected:
        score = item.get("expected_score")
        floor = item.get("minimum_attempt_floor")
        if score is not None and floor is not None and score < floor:
            risks.append({
                "rule_id": "theory_selected_but_floor_not_met",
                "severity": "high",
                "message": "THEORY_CORE 문항을 선택했지만 예상 점수가 최소 선택 floor보다 낮습니다. 선택 방향은 타당할 수 있으나 답안 실행력이 부족합니다.",
                "question": {
                    "number": item["number"],
                    "topic_id": item.get("topic_id"),
                    "expected_score": score,
                    "minimum_attempt_floor": floor
                }
            })

    if selected_core:
        positives.append({
            "rule_id": "core_topic_selected",
            "message": "반복 핵심 변별 문항을 선택했습니다. 단, 실제 점수는 수식·개념 정확도에 따라 결정됩니다.",
            "questions": [
                {
                    "number": x["number"],
                    "topic_id": x.get("topic_id"),
                    "topic_label": x.get("topic_label")
                }
                for x in selected_core
            ]
        })

    if theory_selected and len(selected_items) >= 4 and low_ceiling_count <= 3:
        positives.append({
            "rule_id": "balanced_high_reward_selection",
            "message": "고득점 가능성이 있는 THEORY_CORE 문항과 안정형 문항을 함께 선택한 균형형 전략입니다."
        })

    if any(r["severity"] == "high" for r in risks):
        strategy_grade = "high_risk"
    elif risks:
        strategy_grade = "medium_risk"
    elif positives:
        strategy_grade = "balanced_or_positive"
    else:
        strategy_grade = "neutral"

    return {
        "schema_version": "exam_selection_evaluation_v1",
        "questions": analyzed,
        "selected_numbers": sorted(selected_set),
        "offered_core_must_prepare_count": len(offered_core),
        "selected_core_must_prepare_count": len(selected_core),
        "omitted_core_must_prepare_count": len(omitted_core),
        "risks": risks,
        "positives": positives,
        "strategy_grade": strategy_grade,
        "note": "개별 답안 점수와 문항 선택 전략 평가는 분리한다. 제어이론 선택 자체는 가산점이 아니며, 정확히 풀었을 때만 고득점 band가 열린다."
    }


if __name__ == "__main__":
    examples = [
        "스마트팩토리의 개념과 구성요소를 설명하시오.",
        "2차 시스템의 감쇠비에 따른 응답특성을 설명하시오.",
        "RTD와 열전대를 비교하시오.",
        "밸브 Cv를 설명하시오."
    ]

    for q in examples:
        print(json.dumps(summarize_question_strategy(q), ensure_ascii=False, indent=2))
