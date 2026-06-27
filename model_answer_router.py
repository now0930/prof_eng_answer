import json
import re
from pathlib import Path


DEFAULT_BANK_PATH = Path("rubrics/model_answers/industrial_instrumentation_control.json")


def load_model_answer_bank(path=None):
    candidates = []

    if path:
        candidates.append(Path(path))

    candidates.extend([
        DEFAULT_BANK_PATH,
        Path(__file__).resolve().parent / "rubrics" / "model_answers" / "industrial_instrumentation_control.json",
    ])

    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

    return {
        "version": "model_answer_bank_empty",
        "policy": {},
        "answers": []
    }


def _norm(text):
    text = text or ""
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = text.replace("_", "").replace("-", "")
    return text


def _contains_any(text, terms):
    raw = text or ""
    nraw = _norm(raw)

    found = []
    for t in terms or []:
        t = str(t).strip()
        if not t:
            continue
        nt = _norm(t)
        if t in raw or t.lower() in raw.lower() or nt in nraw:
            found.append(t)
    return found


def _collect_topic_ids(obj):
    found = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                lk = str(k).lower()
                if "topic" in lk and isinstance(v, str) and v.strip():
                    found.add(v.strip())
                walk(v)
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(obj)
    return found


def _compact_reference(answer):
    if not answer:
        return None

    return {
        "id": answer.get("id"),
        "topic_id": answer.get("topic_id"),
        "question_type": answer.get("question_type"),
        "title": answer.get("title"),
        "question_examples": answer.get("question_examples", []),
        "expected_structure": answer.get("expected_structure", []),
        "model_answer_outline": answer.get("model_answer_outline", []),
        "high_score_features": answer.get("high_score_features", []),
        "low_score_patterns": answer.get("low_score_patterns", []),
        "field_connection_points": answer.get("field_connection_points", []),
        "revision_notes": answer.get("revision_notes", [])
    }


def find_model_answer_reference(
    question_text,
    answer_text="",
    question_type_eval=None,
    fact_eval=None,
    bank=None
):
    bank = bank or load_model_answer_bank()
    answers = bank.get("answers", [])

    qte = question_type_eval or {}
    primary_type = (qte.get("primary_type") or {}).get("id") or "GENERAL"

    topic_ids_from_fact = _collect_topic_ids(fact_eval or {})

    q = question_text or ""
    a = answer_text or ""
    combined = q + "\n" + a

    scored = []

    for item in answers:
        score = 0
        reasons = []
        content_hit = False

        item_qtype = item.get("question_type")
        item_topic = item.get("topic_id")

        if primary_type != "GENERAL" and item_qtype == primary_type:
            score += 40
            reasons.append(f"question_type matched: {primary_type}")

        if item_topic in topic_ids_from_fact:
            score += 50
            reasons.append(f"topic_id matched from fact_eval: {item_topic}")
            content_hit = True

        # topic_id 자체가 문제/답안에 직접 등장하는 경우
        if item_topic and _norm(item_topic) in _norm(combined):
            score += 20
            reasons.append(f"topic_id text matched: {item_topic}")
            content_hit = True

        q_examples = item.get("question_examples", [])
        q_hits = _contains_any(q, q_examples)
        if q_hits:
            score += 35 * len(q_hits)
            reasons.append(f"question example matched: {q_hits}")
            content_hit = True

        field_hits = _contains_any(combined, item.get("field_connection_points", []))
        if field_hits:
            score += 5 * len(field_hits)
            reasons.append(f"field connection matched: {field_hits}")
            content_hit = True

        title_hits = _contains_any(combined, [item.get("title", "")])
        if title_hits:
            score += 10
            reasons.append("title matched")
            content_hit = True

        # question_type만 맞는 것으로는 선택하지 않는다.
        # 모범 답안은 topic까지 어느 정도 맞을 때만 참조한다.
        if score > 0 and content_hit:
            scored.append({
                "score": score,
                "match_reasons": reasons,
                "answer": _compact_reference(item)
            })

    scored.sort(key=lambda x: x["score"], reverse=True)

    if not scored:
        return {
            "version": "model_answer_reference_v1",
            "matched": False,
            "primary_reference": None,
            "candidates": [],
            "policy": bank.get("policy", {}),
            "reason": "topic_id 또는 question example이 충분히 맞는 모범 답안을 찾지 못해 참조하지 않음.",
            "usage": "모범 답안은 정답 매칭용이 아니라 구조·깊이·현장 적용성 참고용이다."
        }

    best = scored[0]

    confidence = "low"
    if best["score"] >= 80:
        confidence = "high"
    elif best["score"] >= 45:
        confidence = "medium"

    return {
        "version": "model_answer_reference_v1",
        "matched": True,
        "confidence": confidence,
        "primary_reference": best["answer"],
        "match_reasons": best["match_reasons"],
        "candidates": scored[:3],
        "policy": bank.get("policy", {}),
        "usage": "모범 답안은 정답 문장 매칭용이 아니라 답안 구조, 전개 깊이, 현장 적용성 기준으로만 사용한다."
    }
