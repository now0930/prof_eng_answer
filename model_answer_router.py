from __future__ import annotations

from typing import Any, Dict

from rubric_registry import (
    collect_topic_ids,
    load_model_answer_bank,
    normalize_text,
    text_hits,
)


# 질문은 topic 결정의 주 근거로 사용한다.
QUESTION_ALIAS_WEIGHT = 12
QUESTION_FIELD_WEIGHT = 3
QUESTION_FIELD_SCORE_CAP = 15

# 답안은 topic 결정의 약한 보조 근거로만 사용한다.
ANSWER_ALIAS_WEIGHT = 2
ANSWER_ALIAS_SCORE_CAP = 8
ANSWER_FIELD_WEIGHT = 1
ANSWER_FIELD_SCORE_CAP = 5

# 최종 선택 기준
MIN_MATCH_SCORE = 50
AMBIGUOUS_MARGIN = 10
HIGH_CONFIDENCE_SCORE = 80
HIGH_CONFIDENCE_MARGIN = 20


def _merge_unique_terms(*groups: Any) -> list[str]:
    """여러 alias 필드를 순서 유지 방식으로 병합한다."""
    merged: list[str] = []
    seen: set[str] = set()

    for group in groups:
        if not isinstance(group, (list, tuple, set)):
            continue

        for value in group:
            term = str(value or "").strip()
            if not term:
                continue

            normalized = normalize_text(term)
            if not normalized or normalized in seen:
                continue

            seen.add(normalized)
            merged.append(term)

    return merged


def _compact_reference(
    answer: Dict[str, Any] | None,
) -> Dict[str, Any] | None:
    if not answer:
        return None

    return {
        "id": answer.get("id"),
        "topic_id": answer.get("topic_id"),
        "question_type": answer.get("question_type"),
        "title": answer.get("title"),
        "question_examples": answer.get("question_examples", []),
        "topic_aliases": _merge_unique_terms(
            answer.get("topic_aliases"),
            answer.get("aliases"),
            answer.get("routing_aliases"),
        ),
        "expected_structure": answer.get("expected_structure", []),
        "model_answer_outline": answer.get("model_answer_outline", []),
        "high_score_features": answer.get("high_score_features", []),
        "low_score_patterns": answer.get("low_score_patterns", []),
        "field_connection_points": _merge_unique_terms(
            answer.get("field_connection_points"),
            answer.get("routing_field_points"),
        ),
        "revision_notes": answer.get("revision_notes", []),
    }


def _capped_hit_score(
    hit_count: int,
    weight: int,
    cap: int | None = None,
) -> int:
    score = max(0, int(hit_count)) * max(0, int(weight))

    if cap is not None:
        score = min(score, max(0, int(cap)))

    return score


def find_model_answer_reference(
    question_text: str,
    answer_text: str = "",
    question_type_eval: Dict[str, Any] | None = None,
    fact_eval: Dict[str, Any] | None = None,
    bank: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    bank = bank or load_model_answer_bank()
    answers = bank.get("answers", [])

    qte = question_type_eval or {}
    primary_type = (
        (qte.get("primary_type") or {}).get("id")
        or "GENERAL"
    )

    topic_ids_from_fact = collect_topic_ids(fact_eval or {})

    question = question_text or ""
    answer = answer_text or ""

    normalized_question = normalize_text(question)

    scored = []

    for item in answers:
        if not isinstance(item, dict):
            continue

        question_score = 0
        fact_score = 0
        answer_score = 0

        reasons = []

        question_content_hit = False
        answer_content_hit = False
        strong_question_hit = False

        item_qtype = item.get("question_type")
        item_topic = item.get("topic_id")

        qtype_matched = (
            primary_type != "GENERAL"
            and item_qtype == primary_type
        )

        # 현재 schema와 legacy schema의 alias를 모두 사용한다.
        # 중복 alias는 normalize_text 기준으로 한 번만 계산한다.
        aliases = _merge_unique_terms(
            item.get("topic_aliases"),
            item.get("aliases"),
            item.get("routing_aliases"),
        )

        field_points = _merge_unique_terms(
            item.get("field_connection_points"),
            item.get("routing_field_points"),
        )

        # 질문과 답안을 절대 합치지 않는다.
        question_example_hits = text_hits(
            question,
            item.get("question_examples", []),
        )
        question_alias_hits = text_hits(
            question,
            aliases,
        )
        answer_alias_hits = text_hits(
            answer,
            aliases,
        )
        question_field_hits = text_hits(
            question,
            field_points,
        )
        answer_field_hits = text_hits(
            answer,
            field_points,
        )

        topic_from_fact_matched = (
            item_topic in topic_ids_from_fact
        )

        topic_text_matched = bool(
            item_topic
            and normalize_text(item_topic)
            in normalized_question
        )

        if qtype_matched:
            question_score += 60
            reasons.append(
                f"question_type matched: {primary_type}"
            )

        if topic_from_fact_matched:
            fact_score += 60
            reasons.append(
                "topic_id matched from fact_eval: "
                f"{item_topic}"
            )

        if topic_text_matched:
            question_score += 25
            reasons.append(
                f"topic_id matched in question: {item_topic}"
            )
            question_content_hit = True
            strong_question_hit = True

        if question_example_hits:
            bonus = 50 * len(question_example_hits)
            question_score += bonus
            reasons.append(
                "question example matched in question: "
                f"{question_example_hits}"
            )
            question_content_hit = True
            strong_question_hit = True

        if question_alias_hits:
            bonus = _capped_hit_score(
                len(question_alias_hits),
                QUESTION_ALIAS_WEIGHT,
            )
            question_score += bonus
            reasons.append(
                "topic_alias matched in question: "
                f"{question_alias_hits}"
            )
            question_content_hit = True

        if question_field_hits:
            bonus = _capped_hit_score(
                len(question_field_hits),
                QUESTION_FIELD_WEIGHT,
                QUESTION_FIELD_SCORE_CAP,
            )
            question_score += bonus
            reasons.append(
                "field connection matched in question: "
                f"{question_field_hits}"
            )
            question_content_hit = True

        if answer_alias_hits:
            bonus = _capped_hit_score(
                len(answer_alias_hits),
                ANSWER_ALIAS_WEIGHT,
                ANSWER_ALIAS_SCORE_CAP,
            )
            answer_score += bonus
            reasons.append(
                "topic_alias matched in answer as weak support: "
                f"{answer_alias_hits} (+{bonus})"
            )
            answer_content_hit = True

        if answer_field_hits:
            bonus = _capped_hit_score(
                len(answer_field_hits),
                ANSWER_FIELD_WEIGHT,
                ANSWER_FIELD_SCORE_CAP,
            )
            answer_score += bonus
            reasons.append(
                "field connection matched in answer "
                "as weak support: "
                f"{answer_field_hits} (+{bonus})"
            )
            answer_content_hit = True

        # 기존 방어를 유지하되 strong 근거는
        # 질문 또는 fact_eval에서만 인정한다.
        if (
            primary_type != "GENERAL"
            and item_qtype != primary_type
            and not strong_question_hit
            and not topic_from_fact_matched
        ):
            continue

        total_score = (
            question_score
            + fact_score
            + answer_score
        )

        # 핵심 변경:
        # 답안에만 alias가 등장한 후보는 선택하지 않는다.
        # 질문 또는 fact_eval에 topic 근거가 있어야 한다.
        eligible = (
            question_content_hit
            or topic_from_fact_matched
        )

        if total_score > 0 and eligible:
            scored.append({
                "score": total_score,
                "question_score": question_score,
                "fact_score": fact_score,
                "answer_score": answer_score,
                "score_breakdown": {
                    "question": question_score,
                    "fact_eval": fact_score,
                    "answer_support": answer_score,
                },
                "question_content_hit": question_content_hit,
                "answer_content_hit": answer_content_hit,
                "match_reasons": reasons,
                "answer": _compact_reference(item),
            })

    scored.sort(
        key=lambda row: row["score"],
        reverse=True,
    )

    if not scored:
        return {
            "version": "model_answer_reference_v1",
            "matched": False,
            "ambiguous": False,
            "routing_status": "unmatched",
            "confidence": "low",
            "primary_reference": None,
            "top_score": None,
            "second_score": None,
            "score_margin": None,
            "candidates": [],
            "policy": bank.get("policy", {}),
            "reason": (
                "질문 또는 fact_eval에서 topic 근거가 충분한 "
                "모범 답안을 찾지 못해 참조하지 않음. "
                "답안에만 등장한 topic 용어는 라우팅 근거로 "
                "사용하지 않음."
            ),
            "usage": (
                "모범 답안은 정답 매칭용이 아니라 "
                "구조·깊이·현장 적용성 참고용이다."
            ),
        }

    best = scored[0]
    best_score = float(best.get("score", 0) or 0)

    second = scored[1] if len(scored) > 1 else None
    second_score = (
        float(second.get("score", 0) or 0)
        if second
        else None
    )
    score_margin = (
        best_score - second_score
        if second_score is not None
        else None
    )

    # 최소 점수에 미달하면 특정 topic을 확정하지 않는다.
    if best_score < MIN_MATCH_SCORE:
        return {
            "version": "model_answer_reference_v1",
            "matched": False,
            "ambiguous": False,
            "routing_status": "insufficient_score",
            "confidence": "low",
            "primary_reference": None,
            "top_score": best_score,
            "second_score": second_score,
            "score_margin": score_margin,
            "candidates": scored[:3],
            "policy": bank.get("policy", {}),
            "reason": (
                "최상위 후보 점수가 최소 선택 기준보다 낮아 "
                "특정 topic을 확정하지 않음."
            ),
            "usage": (
                "모범 답안은 정답 매칭용이 아니라 "
                "구조·깊이·현장 적용성 참고용이다."
            ),
        }

    # 1위와 2위의 차이가 작으면 오라우팅 방지를 위해
    # primary_reference를 확정하지 않는다.
    if (
        second_score is not None
        and score_margin is not None
        and score_margin < AMBIGUOUS_MARGIN
    ):
        return {
            "version": "model_answer_reference_v1",
            "matched": False,
            "ambiguous": True,
            "routing_status": "ambiguous",
            "confidence": "low",
            "primary_reference": None,
            "top_score": best_score,
            "second_score": second_score,
            "score_margin": score_margin,
            "candidates": scored[:3],
            "policy": bank.get("policy", {}),
            "reason": (
                "상위 topic 후보 간 점수 차이가 작아 "
                "특정 topic을 확정하지 않음."
            ),
            "usage": (
                "모호한 경우 모범 답안을 강제로 선택하지 않고 "
                "fact 및 logic check 결과를 우선한다."
            ),
        }

    if (
        best_score >= HIGH_CONFIDENCE_SCORE
        and (
            score_margin is None
            or score_margin >= HIGH_CONFIDENCE_MARGIN
        )
    ):
        confidence = "high"
    else:
        confidence = "medium"

    return {
        "version": "model_answer_reference_v1",
        "matched": True,
        "ambiguous": False,
        "routing_status": "matched",
        "confidence": confidence,
        "primary_reference": best["answer"],
        "match_reasons": best["match_reasons"],
        "score": best["score"],
        "top_score": best_score,
        "second_score": second_score,
        "score_margin": score_margin,
        "question_score": best["question_score"],
        "fact_score": best["fact_score"],
        "answer_score": best["answer_score"],
        "score_breakdown": best["score_breakdown"],
        "candidates": scored[:3],
        "policy": bank.get("policy", {}),
        "usage": (
            "모범 답안은 정답 문장 매칭용이 아니라 "
            "답안 구조, 전개 깊이, 현장 적용성 "
            "기준으로만 사용한다."
        ),
    }
