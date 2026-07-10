#!/usr/bin/env python3
import os
import re
from typing import Any, Dict, List, Optional

from difficulty_strategy import summarize_question_strategy


def _to_float(value, default=None):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _normalize(text: str) -> str:
    text = str(text or "").lower()
    text = text.replace("ζ", "zeta")
    text = text.replace("ω", "omega")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return "\n".join(_as_text(x) for x in value)
    if isinstance(value, dict):
        return "\n".join(f"{k}: {_as_text(v)}" for k, v in value.items())
    return str(value)


def _extract_score(grade: Dict[str, Any]) -> Optional[float]:
    for key in ["total_score", "final_score", "score", "weighted_score"]:
        score = _to_float(grade.get(key))
        if score is not None:
            return score
    return None


def _set_score(grade: Dict[str, Any], score: float) -> None:
    for key in ["total_score", "final_score", "score", "weighted_score"]:
        if key in grade:
            grade[key] = round(float(score), 2)
            return
    grade["total_score"] = round(float(score), 2)


def _append_unique(items: List[str], text: str) -> List[str]:
    text = str(text or "").strip()
    if text and text not in items:
        items.append(text)
    return items


def _get_list(grade: Dict[str, Any], key: str) -> List[str]:
    value = grade.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value if str(x).strip()]
    text = str(value).strip()
    return [text] if text else []


def _theory_core_evidence(answer_text: str, grade: Dict[str, Any]) -> Dict[str, Any]:
    """
    THEORY_CORE 고득점 band unlock 판단용 evidence.

    여기서는 최종 정답성을 판정하지 않는다.
    이미 계산된 LLM/휴리스틱 채점 결과와 답안 내용을 참고하여,
    21~25점 band를 열 수 있는 최소 근거가 있는지만 보수적으로 본다.
    """
    combined = "\n".join([
        answer_text or "",
        _as_text(grade.get("summary")),
        _as_text(grade.get("improvement_points")),
        _as_text(grade.get("weaknesses")),
        _as_text(grade.get("difficulty_strategy")),
    ])

    t = _normalize(combined)

    groups = {
        "core_model_or_equation": [
            "전달함수",
            "특성방정식",
            "s^2",
            "s²",
            "분모",
            "표준 2차",
            "omega",
            "omega_n",
            "wn",
            "고유진동수",
            "자연진동수"
        ],
        "damping_ratio": [
            "감쇠비",
            "zeta",
            "제타"
        ],
        "pole_or_root_interpretation": [
            "극점",
            "pole",
            "근",
            "중근",
            "실근",
            "복소근",
            "판별식",
            "root"
        ],
        "response_characteristics": [
            "오버슈트",
            "overshoot",
            "정착시간",
            "settling",
            "상승시간",
            "rise time",
            "진동",
            "과도응답",
            "응답특성"
        ],
        "field_judgement": [
            "튜닝",
            "tuning",
            "pid",
            "loop",
            "루프",
            "공정",
            "안정성",
            "제어기",
            "현장",
            "운전",
            "품질"
        ]
    }

    hits = {}
    for group, keywords in groups.items():
        hits[group] = [kw for kw in keywords if _normalize(kw) in t]

    hit_count = sum(1 for v in hits.values() if v)

    fatal_patterns = [
        r"zeta\s*=\s*1.{0,20}중근.{0,10}아니",
        r"감쇠비.{0,20}반대",
        r"안정.{0,10}불안정.{0,10}반대",
        r"underdamped.{0,20}overdamped.{0,20}혼동",
        r"오버슈트.{0,20}반대",
        r"극점.{0,20}반대"
    ]

    fatal_detected = any(re.search(p, t) for p in fatal_patterns)

    return {
        "groups": hits,
        "hit_count": hit_count,
        "fatal_error_suspected": fatal_detected,
        "unlock_high_band": hit_count >= 4 and not fatal_detected
    }


def _build_ceiling_decision(
    score: float,
    strategy: Dict[str, Any],
    answer_text: str,
    grade: Dict[str, Any]
) -> Dict[str, Any]:
    difficulty = strategy.get("difficulty")
    ceiling = _to_float(strategy.get("default_score_ceiling"))

    decision = {
        "mode": os.getenv("DIFFICULTY_CEILING_MODE", "warn").strip().lower(),
        "difficulty": difficulty,
        "topic_id": strategy.get("topic_id"),
        "selection_importance": strategy.get("selection_importance"),
        "original_score": round(score, 2),
        "cap_applied": False,
        "recommended_cap": None,
        "capped_score": round(score, 2),
        "reason": "",
        "note": (
            "선택 자체 가산점은 없으며, 난이도별 ceiling과 "
            "THEORY_CORE high band unlock 조건만 평가한다."
        )
    }

    if difficulty == "THEORY_CORE":
        evidence = _theory_core_evidence(answer_text, grade)

        # Topic-specific Logic Check is more reliable than broad text heuristics.
        # If it was applied, use its fatal flag as the authoritative signal.
        logic_eval = grade.get("logic_check_evaluation") or {}
        if isinstance(logic_eval, dict) and logic_eval.get("applicable"):
            evidence["logic_check_override"] = True
            evidence["logic_check_mode"] = logic_eval.get("mode")
            evidence["logic_check_fatal_error_detected"] = bool(
                logic_eval.get("fatal_error_detected")
            )

            evidence["fatal_error_suspected"] = bool(
                logic_eval.get("fatal_error_detected")
            )

            if not evidence["fatal_error_suspected"]:
                evidence["unlock_high_band"] = True
                evidence["fatal_error_reason"] = ""
                evidence["fatal_evidence"] = []

        decision["theory_core_evidence"] = evidence

        theory_cap = ceiling if ceiling is not None else 17.5
        no_unlock_cap = min(16.5, theory_cap)
        fatal_cap = min(10.0, no_unlock_cap)

        if evidence["fatal_error_suspected"]:
            decision["recommended_cap"] = fatal_cap
            decision["reason"] = (
                "THEORY_CORE 핵심 이론 오류가 의심되어 "
                f"{fatal_cap:g}점 cap 후보를 적용합니다."
            )
        elif not evidence["unlock_high_band"] and score > no_unlock_cap:
            decision["recommended_cap"] = no_unlock_cap
            decision["reason"] = (
                "THEORY_CORE 고득점 band unlock 근거가 부족하여 "
                f"{no_unlock_cap:g}점 cap 후보를 적용합니다."
            )
        elif score > theory_cap:
            decision["recommended_cap"] = theory_cap
            decision["reason"] = (
                "THEORY_CORE 현실적 ceiling을 초과하여 "
                f"{theory_cap:g}점 cap 후보를 적용합니다."
            )
        else:
            decision["reason"] = (
                "THEORY_CORE 현실적 ceiling 범위 안에 있거나 "
                "고득점 band unlock 조건을 충족한 상태입니다."
            )

        if decision["recommended_cap"] is not None:
            decision["capped_score"] = min(score, float(decision["recommended_cap"]))

        return decision

    if ceiling is not None and score > ceiling:
        decision["recommended_cap"] = ceiling
        decision["capped_score"] = min(score, ceiling)
        decision["reason"] = (
            f"{difficulty} 문제는 안정 득점형 또는 현장 적용형으로 판단되어 "
            f"고득점 ceiling {ceiling:g}점 후보를 적용합니다."
        )
    else:
        decision["reason"] = (
            f"{difficulty} 문제의 현재 점수는 ceiling 적용 대상이 아닙니다."
        )

    return decision




def _append_unique_messages(grade: Dict[str, Any], key: str, messages: list[str]) -> None:
    current = grade.get(key)

    if isinstance(current, list):
        items = [str(x) for x in current if str(x).strip()]
    elif isinstance(current, str) and current.strip():
        items = [current.strip()]
    else:
        items = []

    for msg in messages:
        msg = str(msg).strip()
        if msg and msg not in items:
            items.append(msg)

    grade[key] = items


def _attach_theory_core_fatal_feedback(
    grade: Dict[str, Any],
    decision: Dict[str, Any],
) -> None:
    """
    THEORY_CORE에서 fatal_error_suspected가 true이면,
    단순히 '핵심 이론 오류 의심'이라고만 쓰지 않고
    약점/보완 방향에 구체적인 이론 오류 후보를 명시한다.
    """
    if decision.get("difficulty") != "THEORY_CORE":
        return

    evidence = decision.get("theory_core_evidence") or {}

    if not evidence.get("fatal_error_suspected"):
        return

    strategy = grade.get("difficulty_strategy") or {}
    topic_id = (
        decision.get("topic_id")
        or strategy.get("topic_id")
        or ""
    )

    if topic_id == "second_order_system":
        weaknesses = [
            "감쇠비 관계식 오류: ζ는 sin^-1(ωd/ωn)로 표현하지 않으며, 부족감쇠 영역에서는 ωd = ωn√(1-ζ²) 관계로 설명해야 한다.",
            "부족감쇠 해석 오류: 0 < ζ < 1은 일반적으로 안정한 감쇠진동 응답이며, 이를 단순히 발산으로 표현하면 안정/불안정 구분이 흐려진다.",
            "감쇠비 구간 구분 부족: ζ = 0, 0 < ζ < 1, ζ = 1, ζ > 1 및 우반평면 극점에 의한 불안정 조건을 구분해야 한다.",
        ]

        advice = [
            "2차 표준형 s² + 2ζωn s + ωn² = 0에서 극점, 감쇠비 ζ, 고유진동수 ωn, 감쇠진동수 ωd의 관계를 정확히 정리하세요.",
            "감쇠비별 응답을 무감쇠(ζ=0), 부족감쇠(0<ζ<1), 임계감쇠(ζ=1), 과감쇠(ζ>1), 불안정 영역으로 구분해 표로 비교하세요.",
            "부족감쇠는 오버슈트와 진동이 발생하지만 안정한 경우가 많으므로, 발산 조건과 분리해서 설명하세요.",
        ]
    else:
        weaknesses = [
            "THEORY_CORE 문항에서 핵심 수식·변수 관계·응답 해석 중 중대한 오류 가능성이 감지되었다.",
        ]

        advice = [
            "핵심 이론 문항은 표준 모델, 핵심 변수, 수식 관계, 물리적 의미, 현장 판단을 순서대로 검증해 재작성하세요.",
        ]

    _append_unique_messages(grade, "weaknesses", weaknesses)
    _append_unique_messages(grade, "rewrite_advice", advice)



def _prefer_question_type_adjusted_score(
    grade,
    fallback_score,
):
    try:
        fallback = float(
            fallback_score
        )
    except (
        TypeError,
        ValueError,
        OverflowError,
    ):
        fallback = 0.0

    adjustment = grade.get(
        "question_type_coverage_score_adjustment"
    ) or {}

    if not isinstance(
        adjustment,
        dict,
    ):
        return round(
            fallback,
            2,
        ), False

    if (
        adjustment.get("mode") != "strict"
        or adjustment.get("applied") is not True
    ):
        return round(
            fallback,
            2,
        ), False

    try:
        adjusted = float(
            adjustment.get(
                "adjusted_score"
            )
        )
    except (
        TypeError,
        ValueError,
        OverflowError,
    ):
        return round(
            fallback,
            2,
        ), False

    adjusted = max(
        0.0,
        adjusted,
    )

    if adjusted < fallback:
        return round(
            adjusted,
            2,
        ), True

    return round(
        fallback,
        2,
    ), False

def apply_difficulty_score_ceiling(
    grade: Dict[str, Any],
    question_text: Optional[str] = None,
    answer_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    난이도별 score ceiling 적용 함수.

    기본값:
      DIFFICULTY_CEILING_MODE=warn

    warn:
      recommended_cap만 계산하고 점수는 그대로 둔다.

    strict:
      recommended_cap이 있고 현재 점수가 cap보다 높으면 실제 점수를 제한한다.
    """
    if not isinstance(grade, dict):
        return grade

    score = _extract_score(grade)

    if score is None:
        grade["difficulty_ceiling_evaluation"] = {
            "cap_applied": False,
            "reason": "score not found"
        }
        return grade

    strategy = grade.get("difficulty_strategy")

    if not isinstance(strategy, dict) or not strategy.get("difficulty"):
        if not question_text:
            grade["difficulty_ceiling_evaluation"] = {
                "cap_applied": False,
                "reason": "difficulty strategy not found and question text unavailable"
            }
            return grade

        strategy = summarize_question_strategy(question_text)
        grade["difficulty_strategy"] = strategy

    decision = _build_ceiling_decision(
        score=score,
        strategy=strategy,
        answer_text=answer_text or "",
        grade=grade
    )

    _attach_theory_core_fatal_feedback(grade, decision)

    mode = decision.get("mode")
    recommended_cap = decision.get("recommended_cap")

    if (
        mode == "strict"
        and recommended_cap is not None
        and decision["capped_score"] < score
    ):
        # Preserve pre-ceiling score for explanation, but keep user-facing
        # final score fields consistent with the capped score.
        score, coverage_score_applied = (
            _prefer_question_type_adjusted_score(
                grade,
                score,
            )
        )

        if coverage_score_applied:
            grade["total_score"] = score
            grade[
                "coverage_adjusted_score_applied_to_ceiling"
            ] = True

            adjustment = grade.get(
                "question_type_coverage_score_adjustment"
            )
            if isinstance(adjustment, dict):
                adjustment[
                    "score_flow_applied_before_ceiling"
                ] = True

        grade["pre_ceiling_total_score"] = round(float(score), 2)

        _set_score(grade, decision["capped_score"])

        capped_score = round(float(decision["capped_score"]), 2)
        capped_int = int(capped_score)
        grade["score_range"] = f"{capped_int}~{capped_int}"

        # If the grade object has committee summary fields based on the
        # pre-ceiling score, keep the raw values but expose explicit labels.
        grade["final_total_score"] = capped_score

        capped_int = int(float(decision["capped_score"]))
        grade["score_range"] = f"{capped_int}~{capped_int}"
        decision["cap_applied"] = True

        summary = str(grade.get("summary") or "").strip()
        cap_text = (
            f" 난이도 ceiling 정책에 따라 최종 점수를 "
            f"{decision['original_score']}/25에서 {decision['capped_score']}/25로 제한했습니다. "
            f"사유: {decision['reason']}"
        )

        if cap_text.strip() not in summary:
            grade["summary"] = summary + cap_text if summary else cap_text.strip()

    warnings = _get_list(grade, "strategy_warnings")

    if recommended_cap is not None:
        if mode == "strict":
            warnings = _append_unique(
                warnings,
                f"난이도 ceiling strict 모드: 권장 cap {recommended_cap}점, "
                f"적용 여부={decision['cap_applied']}."
            )
        else:
            warnings = _append_unique(
                warnings,
                f"난이도 ceiling warn 모드: 권장 cap {recommended_cap}점 후보가 "
                "계산되었으나 실제 점수에는 반영하지 않았습니다."
            )

    grade["strategy_warnings"] = warnings
    grade["difficulty_ceiling_evaluation"] = decision

    return grade
