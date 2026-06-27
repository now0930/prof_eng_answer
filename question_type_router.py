import json
from pathlib import Path


DEFAULT_PROFILE_PATH = Path("rubrics/question_types/default.json")


def load_question_type_profile(path=None):
    candidates = []

    if path:
        candidates.append(Path(path))

    candidates.extend([
        DEFAULT_PROFILE_PATH,
        Path(__file__).resolve().parent / "rubrics" / "question_types" / "default.json",
    ])

    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

    return {"types": [], "policy": {}}


def _norm(text):
    return (text or "").lower().replace(" ", "").replace("_", "").replace("-", "")


def _hits(text, terms):
    raw = text or ""
    nraw = _norm(raw)

    found = []
    for t in terms or []:
        t = str(t)
        nt = _norm(t)
        if not t:
            continue
        if t in raw or t.lower() in raw.lower() or nt in nraw:
            found.append(t)
    return found


def detect_question_type(question_text, answer_text="", profile=None):
    profile = profile or load_question_type_profile()

    q = question_text or ""
    a = answer_text or ""
    combined = q + "\n" + a

    candidates = []
    for qt in profile.get("types", []):
        trigger_hits = _hits(q, qt.get("triggers", []))
        answer_hits = _hits(a, qt.get("triggers", []))

        score = len(trigger_hits) * 10 + len(answer_hits) * 2

        # 문제문에 명시된 표현을 더 신뢰한다.
        if trigger_hits:
            score += 5

        if score <= 0:
            continue

        candidates.append({
            "id": qt.get("id"),
            "name": qt.get("name"),
            "score": score,
            "trigger_hits": trigger_hits,
            "answer_hits": answer_hits,
            "c_lens": qt.get("c_lens"),
            "c_required_elements": qt.get("c_required_elements", []),
            "weak_answer_pattern": qt.get("weak_answer_pattern"),
            "high_score_pattern": qt.get("high_score_pattern")
        })

    if not candidates:
        # 기본값은 DEFINE이 아니라, 범용 CONTENT 렌즈로 둔다.
        primary = {
            "id": "GENERAL",
            "name": "일반 설명형",
            "score": 0,
            "trigger_hits": [],
            "answer_hits": [],
            "c_lens": "문제 요구에 맞는 핵심 fact, 적용 범위, 한계, 실무 의미를 설명했는가",
            "c_required_elements": ["핵심 fact", "적용 범위", "한계", "실무 의미"],
            "weak_answer_pattern": "키워드만 나열하고 설명 구조와 현장 의미가 부족함",
            "high_score_pattern": "핵심 fact를 구조적으로 설명하고 현실 적용 의미까지 연결함"
        }
        candidates = [primary]
    else:
        candidates.sort(key=lambda x: x["score"], reverse=True)
        primary = candidates[0]

    confidence = "low"
    if primary.get("score", 0) >= 20:
        confidence = "high"
    elif primary.get("score", 0) >= 10:
        confidence = "medium"

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
        )
    }
