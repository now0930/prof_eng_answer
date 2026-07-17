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
    """
    Detect the grading lens from question demand only.

    answer_text remains in the signature for compatibility, but it must never
    affect lens selection.
    """
    del answer_text

    profile = (
        profile
        or load_question_type_profile()
    )

    question = question_text or ""

    raw_types = profile.get(
        "types",
        [],
    )

    if isinstance(raw_types, dict):
        normalized_types = []

        for mapped_id, mapped_value in (
            raw_types.items()
        ):
            if not isinstance(
                mapped_value,
                dict,
            ):
                continue

            normalized_item = dict(
                mapped_value
            )
            normalized_item.setdefault(
                "id",
                str(mapped_id),
            )
            normalized_types.append(
                normalized_item
            )

    elif isinstance(raw_types, list):
        normalized_types = [
            dict(item)
            for item in raw_types
            if isinstance(item, dict)
        ]

    else:
        normalized_types = []

    v2_trigger_groups = {
        "PRINCIPLE_INTERPRETATION": [
            "DEFINE",
            "PRINCIPLE",
            "CALC_DESIGN",
        ],
        "DIAGNOSIS_ACTION": [
            "PROBLEM_SOLVE",
            "CAUSE_ACTION",
        ],
        "COMPARE_SELECTION": [
            "COMPARE",
            "STRUCTURE",
        ],
        "IMPLEMENTATION_EVALUATION": [
            "PROCEDURE",
            "APPLICATION",
            "EVALUATION",
        ],
    }

    explicit_demand_terms = {
        "PRINCIPLE_INTERPRETATION": [
            "개념 설명",
            "개념을 설명",
            "원리 설명",
            "원리를 설명",
            "설계 기준",
            "설계기준",
            "기준 제시",
            "기준을 제시",
            "수식을 유도",
            "공식을 유도",
            "계산하시오",
            "구하시오",
            "해석하시오",
            "유도하시오",
        ],
        "DIAGNOSIS_ACTION": [
            "원인과 대책",
            "발생원인과 대책",
            "발생 원인과 대책",
            "문제점과 개선",
            "문제점",
            "개선방안",
            "개선 방안",
            "대책을 제시",
        ],
        "COMPARE_SELECTION": [
            "비교",
            "차이점",
            "장단점",
            "대비",
            "선정하시오",
            "선정하여",
            "선정하고",
            "선택하시오",
            "선택하여",
        ],
        "IMPLEMENTATION_EVALUATION": [
            "절차를 설명",
            "시험 방법",
            "평가 방법",
            "적용 사례",
            "구현 방법",
            "검증 방법",
        ],
    }

    deterministic_priority = {
        "DIAGNOSIS_ACTION": 0,
        "COMPARE_SELECTION": 1,
        "IMPLEMENTATION_EVALUATION": 2,
        "PRINCIPLE_INTERPRETATION": 3,
    }

    candidates = []

    for question_type in normalized_types:
        type_id = str(
            question_type.get("id", "")
        ).strip()

        if not type_id:
            continue

        trigger_terms = (
            question_type.get("triggers")
            or question_type.get(
                "selection_signals"
            )
            or []
        )

        profile_question_hits = text_hits(
            question,
            trigger_terms,
        )

        trigger_group_ids = (
            v2_trigger_groups.get(type_id)
            or [type_id]
        )

        strong_question_hits = []

        for trigger_group_id in (
            trigger_group_ids
        ):
            for hit in _strong_hits(
                trigger_group_id,
                question,
            ):
                if (
                    hit
                    not in strong_question_hits
                ):
                    strong_question_hits.append(
                        hit
                    )

        explicit_hits = text_hits(
            question,
            explicit_demand_terms.get(
                type_id,
                [],
            ),
        )

        score = 0
        score += (
            len(strong_question_hits)
            * 30
        )
        score += (
            len(profile_question_hits)
            * 8
        )
        score += (
            len(explicit_hits)
            * 40
        )

        compare_strong_hits = _strong_hits(
            "COMPARE",
            question,
        )

        if (
            type_id
            in {
                "COMPARE",
                "COMPARE_SELECTION",
            }
            and not compare_strong_hits
            and not explicit_hits
        ):
            score = min(
                score,
                5,
            )

        if score <= 0:
            continue

        matched_rules = []

        for hit in explicit_hits:
            matched_rules.append(
                f"explicit_demand:{hit}"
            )

        for hit in strong_question_hits:
            matched_rules.append(
                f"strong_question:{hit}"
            )

        for hit in profile_question_hits:
            matched_rules.append(
                f"profile_question:{hit}"
            )

        candidates.append(
            {
                "id": type_id,
                "name": (
                    question_type.get("name")
                    or question_type.get(
                        "name_ko"
                    )
                ),
                "score": score,
                "strong_question_hits": (
                    strong_question_hits
                ),
                "trigger_hits": (
                    profile_question_hits
                ),
                "explicit_demand_hits": (
                    explicit_hits
                ),
                "answer_hits": [],
                "matched_rules": (
                    matched_rules
                ),
                "c_lens": (
                    question_type.get(
                        "c_lens"
                    )
                    or question_type.get(
                        "evaluation_lens"
                    )
                ),
                "c_required_elements": (
                    question_type.get(
                        "c_required_elements",
                        [],
                    )
                    or question_type.get(
                        "required_elements",
                        [],
                    )
                ),
                "weak_answer_pattern": (
                    question_type.get(
                        "weak_answer_pattern"
                    )
                ),
                "high_score_pattern": (
                    question_type.get(
                        "high_score_pattern"
                    )
                ),
            }
        )

    if candidates:
        candidates.sort(
            key=lambda candidate: (
                -float(
                    candidate.get(
                        "score",
                        0,
                    )
                    or 0
                ),
                deterministic_priority.get(
                    str(
                        candidate.get("id")
                        or ""
                    ),
                    99,
                ),
                str(
                    candidate.get("id")
                    or ""
                ),
            )
        )
        primary = candidates[0]

    else:
        primary = {
            "id": "GENERAL",
            "name": "일반 설명형",
            "score": 0,
            "strong_question_hits": [],
            "trigger_hits": [],
            "explicit_demand_hits": [],
            "answer_hits": [],
            "matched_rules": [],
            "c_lens": (
                "문제 요구에 맞는 핵심 fact, "
                "적용 범위, 한계, 실무 의미를 "
                "설명했는가"
            ),
            "c_required_elements": [
                "핵심 fact",
                "적용 범위",
                "한계",
                "실무 의미",
            ],
            "weak_answer_pattern": (
                "키워드만 나열하고 설명 구조와 "
                "현장 의미가 부족함"
            ),
            "high_score_pattern": (
                "핵심 fact를 구조적으로 설명하고 "
                "현실 적용 의미까지 연결함"
            ),
        }
        candidates = [primary]

    top_score = float(
        primary.get("score", 0)
        or 0
    )

    second_score = 0.0

    if len(candidates) >= 2:
        second_score = float(
            candidates[1].get(
                "score",
                0,
            )
            or 0
        )

    margin = top_score - second_score

    explicit_primary_hits = (
        primary.get(
            "explicit_demand_hits"
        )
        or []
    )
    strong_primary_hits = (
        primary.get(
            "strong_question_hits"
        )
        or []
    )

    if (
        explicit_primary_hits
        and top_score >= 40
        and margin >= 15
    ):
        confidence = "high"

    elif (
        (
            strong_primary_hits
            or top_score >= 12
        )
        and margin >= 5
    ):
        confidence = "medium"

    else:
        confidence = "low"

    question_type_locked = (
        confidence == "high"
    )

    if question_type_locked:
        status = "locked"
        warning = ""
    else:
        status = "provisional"
        warning = (
            "⚠ 이 문제의 유형 분류는 잠정 상태이며 "
            "확인이 필요합니다"
        )

    policy = profile.get("policy")

    if not isinstance(policy, dict):
        policy = {}

    return {
        "version": (
            "question_type_lens_v2_"
            "deterministic"
        ),
        "policy": policy,
        "question_type": (
            primary.get("id")
        ),
        "primary_type": primary,
        "candidates": candidates[:3],
        "confidence": confidence,
        "status": status,
        "question_type_locked": (
            question_type_locked
        ),
        "source": "deterministic_rule",
        "matched_rules": (
            primary.get("matched_rules")
            or []
        ),
        "warning": warning,
        "top_score": top_score,
        "second_score": second_score,
        "margin": margin,
        "interpretation": (
            "문제 유형은 답안과 무관하게 문제의 "
            "요구 동사와 명시적 요구만으로 결정한다. "
            "high confidence만 현재 실행에서 "
            "잠금 처리한다."
        ),
        "common_D_E_rule": policy.get(
            "common_D_E_rule",
            (
                "모든 문제 유형은 D/E에서 현실 적용성, "
                "문제 해결, 제언, 독창성을 공통 평가한다."
            ),
        ),
    }
