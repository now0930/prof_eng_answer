from __future__ import annotations

from typing import Any, Dict, List

from rubric_registry import load_question_type_profile, normalize_text, text_hits


# 문제문에서 강하게 보아야 하는 유형별 trigger.
# 답안 본문보다 문제문 trigger를 우선한다.
STRONG_QUESTION_TRIGGERS: Dict[str, List[str]] = {
    "DEFINE": [
        "정의", "개념", "의미", "설명하시오", "설명하라", "무엇인가", "란", "이란"
    ],
    "PRINCIPLE": [
        "원리", "메커니즘", "동작 원리", "발생 원리", "작동 원리"
    ],
    "STRUCTURE": [
        "구성", "구조", "분류", "종류", "구성요소", "체계"
    ],
    "COMPARE": [
        "비교", "차이", "차이점", "장단점", "대비", "선정 기준", "적용 기준", "비교하고"
    ],
    "PROBLEM_SOLVE": [
        "문제점", "개선방안", "개선 방안", "개선", "해결방안", "해결 방안"
    ],
    "CAUSE_ACTION": [
        "원인과 대책", "원인 및 대책", "발생 원인", "대책", "방지대책", "조치"
    ],
    "PROCEDURE": [
        "절차", "방법", "순서", "수행 방법", "작성 방법", "시험 방법"
    ],
    "CALC_DESIGN": [
        "계산", "산정", "공식", "수식", "계산식", "설계", "사이징", "구하시오"
    ],
    "APPLICATION": [
        "적용 사례", "사례", "활용", "적용 방안", "적용 방법"
    ],
    "EVALUATION": [
        "평가", "효과", "효과 분석", "성과", "지표", "before/after", "전후 비교"
    ],
}


def _has_any(text: str, terms: List[str]) -> bool:
    ntext = normalize_text(text)
    for term in terms:
        if normalize_text(term) in ntext:
            return True
    return False


def _strong_hits(type_id: str, question_text: str) -> List[str]:
    return text_hits(question_text or "", STRONG_QUESTION_TRIGGERS.get(type_id, []))


def _has_non_define_strong_question_signal(question_text: str) -> bool:
    for type_id, terms in STRONG_QUESTION_TRIGGERS.items():
        if type_id == "DEFINE":
            continue
        if _has_any(question_text, terms):
            return True
    return False


def detect_question_type(
    question_text: str,
    answer_text: str = "",
    profile: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    profile = profile or load_question_type_profile()

    question = question_text or ""
    answer = answer_text or ""

    non_define_strong = _has_non_define_strong_question_signal(question)

    candidates = []

    for qt in profile.get("types", []):
        if not isinstance(qt, dict):
            continue

        type_id = str(qt.get("id", "")).strip()
        if not type_id:
            continue

        profile_question_hits = text_hits(question, qt.get("triggers", []))
        profile_answer_hits = text_hits(answer, qt.get("triggers", []))
        strong_question_hits = _strong_hits(type_id, question)

        score = 0

        # 문제문 강한 trigger가 가장 중요하다.
        score += len(strong_question_hits) * 30

        # profile trigger도 문제문에서는 비교적 강하게 본다.
        score += len(profile_question_hits) * 8

        # 답안 trigger는 보조 신호다. 답안의 "선정" 하나로 COMPARE가 되면 안 된다.
        score += min(len(profile_answer_hits), 3) * 1

        # DEFINE은 "설명하시오" 문제에서 기본값 역할을 한다.
        # 다만 비교/절차/계산/평가 등 강한 신호가 문제문에 있으면 DEFINE을 과대평가하지 않는다.
        if type_id == "DEFINE" and not non_define_strong:
            if _has_any(question, STRONG_QUESTION_TRIGGERS["DEFINE"]):
                score += 25

        # COMPARE는 문제문에 비교성 신호가 없으면 답안의 "선정"만으로 선택하지 않는다.
        if type_id == "COMPARE" and not _strong_hits("COMPARE", question):
            score = min(score, 5)

        if score <= 0:
            continue

        candidates.append({
            "id": type_id,
            "name": qt.get("name"),
            "score": score,
            "strong_question_hits": strong_question_hits,
            "trigger_hits": profile_question_hits,
            "answer_hits": profile_answer_hits,
            "c_lens": qt.get("c_lens"),
            "c_required_elements": qt.get("c_required_elements", []),
            "weak_answer_pattern": qt.get("weak_answer_pattern"),
            "high_score_pattern": qt.get("high_score_pattern"),
        })

    if candidates:
        candidates.sort(key=lambda x: x["score"], reverse=True)
        primary = candidates[0]
    else:
        primary = {
            "id": "GENERAL",
            "name": "일반 설명형",
            "score": 0,
            "strong_question_hits": [],
            "trigger_hits": [],
            "answer_hits": [],
            "c_lens": "문제 요구에 맞는 핵심 fact, 적용 범위, 한계, 실무 의미를 설명했는가",
            "c_required_elements": ["핵심 fact", "적용 범위", "한계", "실무 의미"],
            "weak_answer_pattern": "키워드만 나열하고 설명 구조와 현장 의미가 부족함",
            "high_score_pattern": "핵심 fact를 구조적으로 설명하고 현실 적용 의미까지 연결함",
        }
        candidates = [primary]

    score = float(primary.get("score", 0) or 0)
    if score >= 30:
        confidence = "high"
    elif score >= 12:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "version": "question_type_lens_v1",
        "policy": profile.get("policy", {}),
        "primary_type": primary,
        "candidates": candidates[:3],
        "confidence": confidence,
        "interpretation": "문제 유형은 별도 총점 체계가 아니라 C항목의 Fact 설명 방식을 결정하는 평가 렌즈로 사용한다.",
        "common_D_E_rule": profile.get("policy", {}).get(
            "common_D_E_rule",
            "모든 문제 유형은 D/E에서 현실 적용성, 문제 해결, 제언, 독창성을 공통 평가한다."
        ),
    }
