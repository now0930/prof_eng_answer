from question_type_output_adapter import attach_question_type_v2_to_grade

#!/usr/bin/env python3
from typing import Any, Dict, List, Optional

from difficulty_strategy import summarize_question_strategy, get_profile_policy


def _as_list(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value if str(x).strip()]
    if isinstance(value, tuple):
        return [str(x) for x in value if str(x).strip()]
    text = str(value).strip()
    return [text] if text else []


def _append_unique(items: List[str], text: str) -> List[str]:
    text = str(text or "").strip()
    if not text:
        return items
    if text not in items:
        items.append(text)
    return items


def _extract_question_from_grade(grade: Dict[str, Any]) -> str:
    candidates = [
        "question",
        "question_text",
        "problem",
        "problem_text",
        "exam_question",
        "prompt",
    ]

    for key in candidates:
        value = grade.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    for value in grade.values():
        if isinstance(value, dict):
            for key in candidates:
                nested = value.get(key)
                if isinstance(nested, str) and nested.strip():
                    return nested.strip()

    return ""


def _strategy_summary_text(strategy: Dict[str, Any]) -> str:
    difficulty = strategy.get("difficulty")
    difficulty_label = strategy.get("difficulty_label") or difficulty
    importance = strategy.get("selection_importance")
    policy = strategy.get("selection_policy")
    ceiling = strategy.get("default_score_ceiling")
    excellent = strategy.get("excellent_score_band")
    topic_label = strategy.get("topic_label") or strategy.get("topic_id")

    if difficulty == "THEORY_CORE":
        return (
            f"본 문항은 '{topic_label}' 계열의 핵심 이론 변별형 문제로 판단했습니다. "
            f"난이도 Profile은 {difficulty}({difficulty_label})이며, 선택 중요도는 {importance}, "
            f"선택 정책은 {policy}입니다. 제어이론 계열 문제는 선택했다는 사실만으로 가산점을 주지 않고, "
            f"표준 모델·핵심 변수·수식 관계·응답특성·현장 판단이 정확히 연결될 때 "
            f"{excellent[0]}~{excellent[1]}점 고득점 band가 열리는 고위험·고보상형 문항으로 평가합니다."
        )

    if difficulty == "BASIC_CONCEPT":
        return (
            f"본 문항은 기본 개념형 문제로 판단했습니다. 난이도 Profile은 {difficulty}({difficulty_label})이며, "
            f"정의·개념·구성·적용 범위를 폭넓게 설명하는 것이 핵심입니다. "
            f"안정적인 득점은 가능하지만 고득점 ceiling은 약 {ceiling}점 수준으로 보았습니다."
        )

    if difficulty == "FIELD_APPLICATION":
        return (
            f"본 문항은 현장 적용형 문제로 판단했습니다. 난이도 Profile은 {difficulty}({difficulty_label})이며, "
            f"정의나 원리뿐 아니라 선정 기준, 현장 조건, 문제점, 개선방안, 비용·유지보수·기존 설비 영향을 연결해야 합니다. "
            f"우수 답안의 ceiling은 약 {ceiling}점 수준으로 보았습니다."
        )

    if difficulty == "DESIGN_EVALUATION":
        return (
            f"본 문항은 설계·평가형 문제로 판단했습니다. 난이도 Profile은 {difficulty}({difficulty_label})이며, "
            f"평가 기준, 지표, 대안 비교, 효과 분석, 검증 방법을 포함해야 고득점이 가능합니다. "
            f"우수 답안의 ceiling은 약 {ceiling}점 수준으로 보았습니다."
        )

    return (
        f"본 문항의 난이도 Profile은 {difficulty}({difficulty_label})로 판단했습니다. "
        f"선택 중요도는 {importance}, 선택 정책은 {policy}입니다."
    )


def _theory_core_improvement_points(strategy: Dict[str, Any]) -> List[str]:
    points = [
        "THEORY_CORE 보완: 표준 모델 또는 특성방정식을 먼저 제시하세요.",
        "THEORY_CORE 보완: 핵심 변수의 의미를 명확히 설명하세요. 예: 감쇠비 ζ, 고유진동수 ωn.",
        "THEORY_CORE 보완: 수식 → 극점/조건 → 응답특성 → 현장 판단 순서로 연결하세요.",
        "THEORY_CORE 보완: 감쇠, 오버슈트, 진동성, 안정성 관계를 반대로 설명하지 않도록 주의하세요.",
        "THEORY_CORE 고득점 조건: 핵심 이론이 정확할 때만 21~25점 band가 열립니다."
    ]

    return points


def _non_theory_improvement_points(strategy: Dict[str, Any]) -> List[str]:
    difficulty = strategy.get("difficulty")

    if difficulty == "BASIC_CONCEPT":
        return [
            "BASIC_CONCEPT 보완: 정의, 구성요소, 적용 범위, 한계, 실무 의미를 빠짐없이 전개하세요.",
            "BASIC_CONCEPT 주의: 안정적인 득점은 가능하지만 고득점 ceiling이 낮을 수 있으므로 현장 적용까지 연결하세요."
        ]

    if difficulty == "FIELD_APPLICATION":
        return [
            "FIELD_APPLICATION 보완: 선정 기준, 현장 조건, 문제점, 개선방안, 비용·유지보수 영향을 함께 쓰세요.",
            "FIELD_APPLICATION 고득점 조건: 단순 개념 설명을 넘어 실제 설비 적용 판단까지 연결하세요."
        ]

    if difficulty == "DESIGN_EVALUATION":
        return [
            "DESIGN_EVALUATION 보완: 평가 기준, 정량·정성 지표, 대안 비교, 효과 분석, 검증 방법을 포함하세요."
        ]

    return []


def attach_difficulty_strategy_to_grade(
    grade: Dict[str, Any],
    question_text: Optional[str] = None
) -> Dict[str, Any]:
    grade = attach_question_type_v2_to_grade(grade, question_text=question_text)
    if not isinstance(grade, dict):
        return grade

    question = (question_text or "").strip() or _extract_question_from_grade(grade)

    if not question:
        grade.setdefault("difficulty_strategy", {
            "matched": False,
            "note": "question text not available"
        })
        return grade

    try:
        strategy = summarize_question_strategy(question)
    except Exception as e:
        grade.setdefault("difficulty_strategy", {
            "matched": False,
            "error": str(e)
        })
        return grade

    grade["difficulty_strategy"] = strategy

    summary = str(grade.get("summary") or "").strip()
    strategy_text = _strategy_summary_text(strategy)

    if strategy_text and strategy_text not in summary:
        if summary:
            grade["summary"] = summary + " " + strategy_text
        else:
            grade["summary"] = strategy_text

    improvement_points = _as_list(
        grade.get("improvement_points")
        or grade.get("improvements")
        or grade.get("보완 방향")
    )

    if strategy.get("difficulty") == "THEORY_CORE":
        for p in _theory_core_improvement_points(strategy):
            improvement_points = _append_unique(improvement_points, p)
    else:
        for p in _non_theory_improvement_points(strategy):
            improvement_points = _append_unique(improvement_points, p)

    if improvement_points:
        grade["improvement_points"] = improvement_points

    warnings = _as_list(grade.get("strategy_warnings"))

    if strategy.get("selection_importance") == "CORE_MUST_PREPARE":
        warnings = _append_unique(
            warnings,
            "반복 출제되는 핵심 변별 주제입니다. 한 문제 채점에서는 직접 가산점이 없지만, 6문제 중 4문제 선택 전략에서는 회피 시 고득점 안정성이 낮아질 수 있습니다."
        )

    if strategy.get("difficulty") == "THEORY_CORE":
        warnings = _append_unique(
            warnings,
            "THEORY_CORE 문항은 선택 자체가 가산점이 아니며, 핵심 이론 정확성이 충족될 때만 고득점 band가 열립니다."
        )

    if warnings:
        grade["strategy_warnings"] = warnings

    return grade
