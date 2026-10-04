"""Bounded plain-text source excerpts from the validated Training View only."""


def _short(value, limit):
    text = " ".join(value.split()) if isinstance(value, str) else ""
    return text if len(text) <= limit else text[:limit - 1] + "…"


def source_review_lines(training):
    """Display source text and pending comments without deciding correctness."""
    lines = []
    sources = training.get("source_materials", [])
    sources = sources if isinstance(sources, list) else []
    for source in [s for s in sources if isinstance(s, dict) and s.get("text")][:2]:
        lines.append(
            "   출처 원문 발췌 (참고자료·채점 기준 아님): "
            + _short(source.get("title"), 80) + " — " + _short(source.get("text"), 220)
        )
        url = source.get("source_url")
        if isinstance(url, str) and url.startswith(("https://", "http://")):
            lines.append("   출처: " + _short(url, 240))
    annotations = training.get("source_review_annotations", [])
    annotations = annotations if isinstance(annotations, list) else []
    pending = [a for a in annotations if isinstance(a, dict)
               and a.get("status") == "pending_review" and a.get("score_effect") == "none"]
    states = {"matching": "현재 원문 일치", "stale": "이전 원문 기준", "text_unavailable": "원문 확인 불가"}
    for note in pending[:2]:
        state = states.get(note.get("source_state"), "원문 상태 미확인")
        lines.append("   검토 대기 (점수 영향 없음·" + state + "): "
                     + _short(note.get("locator"), 70) + " / 인용: "
                     + _short(note.get("quote"), 80) + " / 의견: "
                     + _short(note.get("review_note"), 160))
    if len(pending) > 2:
        lines.append(f"   검토 대기 주석 {len(pending) - 2}건 추가 (원문·전체 주석은 별도 보존)")
    return lines
