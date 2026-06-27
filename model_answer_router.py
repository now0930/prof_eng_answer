from __future__ import annotations

from typing import Any, Dict

from rubric_registry import (
    collect_topic_ids,
    load_model_answer_bank,
    normalize_text,
    text_hits,
)


def _compact_reference(answer: Dict[str, Any] | None) -> Dict[str, Any] | None:
    if not answer:
        return None

    return {
        "id": answer.get("id"),
        "topic_id": answer.get("topic_id"),
        "question_type": answer.get("question_type"),
        "title": answer.get("title"),
        "question_examples": answer.get("question_examples", []),
        "topic_aliases": answer.get("topic_aliases", []),
        "expected_structure": answer.get("expected_structure", []),
        "model_answer_outline": answer.get("model_answer_outline", []),
        "high_score_features": answer.get("high_score_features", []),
        "low_score_patterns": answer.get("low_score_patterns", []),
        "field_connection_points": answer.get("field_connection_points", []),
        "revision_notes": answer.get("revision_notes", []),
    }


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
    primary_type = (qte.get("primary_type") or {}).get("id") or "GENERAL"

    topic_ids_from_fact = collect_topic_ids(fact_eval or {})

    question = question_text or ""
    answer = answer_text or ""
    combined = question + "\n" + answer
    normalized_combined = normalize_text(combined)

    scored = []

    for item in answers:
        if not isinstance(item, dict):
            continue

        score = 0
        reasons = []
        content_hit = False
        strong_content_hit = False

        item_qtype = item.get("question_type")
        item_topic = item.get("topic_id")

        qtype_matched = primary_type != "GENERAL" and item_qtype == primary_type

        question_hits = text_hits(question, item.get("question_examples", []))
        alias_hits = text_hits(combined, item.get("topic_aliases", []))
        field_hits = text_hits(combined, item.get("field_connection_points", []))

        topic_from_fact_matched = item_topic in topic_ids_from_fact
        topic_text_matched = bool(item_topic and normalize_text(item_topic) in normalized_combined)

        if qtype_matched:
            score += 60
            reasons.append(f"question_type matched: {primary_type}")

        if topic_from_fact_matched:
            score += 60
            reasons.append(f"topic_id matched from fact_eval: {item_topic}")
            content_hit = True
            strong_content_hit = True

        if topic_text_matched:
            score += 25
            reasons.append(f"topic_id text matched: {item_topic}")
            content_hit = True
            strong_content_hit = True

        if question_hits:
            score += 50 * len(question_hits)
            reasons.append(f"question example matched: {question_hits}")
            content_hit = True
            strong_content_hit = True

        if alias_hits:
            score += 12 * len(alias_hits)
            reasons.append(f"topic_alias matched: {alias_hits}")
            content_hit = True

        if field_hits:
            score += 3 * len(field_hits)
            reasons.append(f"field connection matched: {field_hits}")
            content_hit = True

        # 핵심 방어:
        # question_type이 다르면 alias(Cv 등)만으로 다른 유형의 모범답안을 참조하지 않는다.
        if primary_type != "GENERAL" and item_qtype != primary_type and not strong_content_hit:
            continue

        if score > 0 and content_hit:
            scored.append({
                "score": score,
                "match_reasons": reasons,
                "answer": _compact_reference(item),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)

    if not scored:
        return {
            "version": "model_answer_reference_v1",
            "matched": False,
            "primary_reference": None,
            "candidates": [],
            "policy": bank.get("policy", {}),
            "reason": "topic_id, question_type, question example이 충분히 맞는 모범 답안을 찾지 못해 참조하지 않음.",
            "usage": "모범 답안은 정답 매칭용이 아니라 구조·깊이·현장 적용성 참고용이다.",
        }

    best = scored[0]
    best_score = float(best.get("score", 0) or 0)

    if best_score >= 80:
        confidence = "high"
    elif best_score >= 45:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "version": "model_answer_reference_v1",
        "matched": True,
        "confidence": confidence,
        "primary_reference": best["answer"],
        "match_reasons": best["match_reasons"],
        "candidates": scored[:3],
        "policy": bank.get("policy", {}),
        "usage": "모범 답안은 정답 문장 매칭용이 아니라 답안 구조, 전개 깊이, 현장 적용성 기준으로만 사용한다.",
    }
