"""Bounded plain-text source excerpts from the validated Training View only."""


def _pages(text, limit=3000):
    """Telegram counts UTF-16 units; preserve every character, including formulas."""
    pages, chars, size = [], [], 0
    for char in text:
        width = 2 if ord(char) > 0xffff else 1
        if size + width > limit:
            pages.append(''.join(chars))
            chars, size = [], 0
        chars.append(char)
        size += width
    if chars:
        pages.append(''.join(chars))
    return pages


def learning_review_messages(training):
    """Render validated synthesis in learning order; private drafts stay hidden."""
    synthesis = training.get('learning_synthesis')
    if synthesis is None:
        return []
    if not isinstance(synthesis, dict) or synthesis.get('status') != 'loaded' or synthesis.get('score_effect') != 'none':
        return ['학습 구성 자료를 현재 확인할 수 없습니다. 기존 복습 자료를 이용하세요.']
    doc = synthesis['document']
    path = doc['learning_path']
    allowed = set(synthesis['eligible_section_ids'])
    review_labels = {'human_verified': '사람 검토 완료',
                     'llm_verified': 'LLM 승인·사람 승인 아님',
                     'llm_reviewed_human_pending': 'LLM 검토·사람 검토 대기'}
    status = review_labels.get(path['review']['status'])
    if status is None:
        return ['학습 구성 초안은 검토 대기 상태입니다. 기존 복습 자료를 이용하세요.']
    evidence = {e['evidence_id']: e for e in doc['evidence']}
    knowledge = {k['knowledge_id']: k for k in doc['knowledge']}
    origins = {'source_excerpt': '원문 인용', 'synthesis': '여러 자료 종합', 'authored': '작성한 설명'}
    messages = _pages('\n'.join([
        '주제 학습: ' + path['title'],
        f"구성 버전: {doc['revision']} / {status} / 점수 영향 없음",
        '학습 목표:', *['- ' + value for value in path['objectives']],
    ]))
    for number, section in enumerate(path['sections'], 1):
        items = [knowledge[k] for k in section['knowledge_ids']]
        if section['section_id'] not in allowed or any(k['review']['status'] not in review_labels for k in items):
            messages.append(f'{number}. 학습 절 보류 — 초안·미해결 충돌 또는 출처 확인 필요')
            continue
        lines = [f"{number}. {section['title']} [{section['section_id']}]",
                 origins[section['origin']] + ' / ' + status, section['body']]
        refs = list(section['evidence_ids'])
        for item in items:
            lines.extend(['개념: ' + item['title'] + ' / ' + review_labels[item['review']['status']],
                          origins[item['origin']] + ': ' + item['statement']])
            for field, label in [('conditions','적용 조건'), ('units','단위'), ('exceptions','예외·한계')]:
                if item[field]:
                    lines.extend([label + ':', *['- ' + value for value in item[field]]])
            refs.extend(item['evidence_ids'])
        for check in section['self_check']:
            lines.extend(['자가 점검: ' + check['question'], '확인 답안: ' + check['answer']])
        for ref in dict.fromkeys(refs):
            source = evidence[ref]
            lines.append(f"출처: {source['source_url']} / {source['locator']} / 버전 {source['source_version']}")
        if section['material_ids']:
            lines.append('연결 학습자료: ' + ', '.join(section['material_ids']))
        messages.extend(_pages('\n'.join(lines)))
    return messages


def review_model_answer_messages(training, attempts=None):
    """Render a question-matched answer and score-neutral comparison of final grades."""
    answer = training.get("review_model_answer") if isinstance(training, dict) else None
    if not isinstance(answer, dict) or answer.get("score_effect") != "none":
        return []
    status = {"human_verified": "사람 검토 완료",
              "llm_reviewed_human_pending": "LLM 검토·사람 검토 대기"}.get(answer.get("review_status"))
    if status is None:
        return []
    lines = ["학습용 모범답안: " + answer["title"],
             "검토 상태: " + status + " / 점수 영향 없음",
             "문제: " + answer["question"]]
    output = _pages("\n".join(lines))
    for section in answer["sections"]:
        output.extend(_pages(section["title"] + "\n" + section["body"]))
    output.extend(_pages("자가 점검:\n" + "\n".join("- " + x for x in answer["self_check"])))
    output.extend(_pages("학습 자료 출처:\n" + "\n".join(
        "- " + s["url"] + " / " + s["locator"] for s in answer["sources"])))
    if attempts:
        messages = ["이 문항의 이전 확정 채점 (점수 변경 없음):"]
        ids = {rid for demand in answer["question_demands"] for rid in demand["requirement_ids"]}
        for index, attempt in enumerate(attempts, 1):
            statuses = {row["requirement_id"]: row["status"]
                        for row in attempt.get("requirement_statuses", [])
                        if isinstance(row, dict) and row.get("requirement_id") in ids}
            messages.append(f"{index}회: {attempt['score']:g}/25 ({attempt['attempted_at'][:10]})")
            dimensions = {row.get("layer_id"): row.get("score") for row in attempt.get("layer_scores", [])
                          if isinstance(row, dict) and row.get("layer_id") in {"D", "E"}
                          and isinstance(row.get("score"), (int, float))}
            if dimensions:
                messages.append("공학적 판단 D: " + str(dimensions.get("D", "기록 없음"))
                                + "/6 · 논리 연결 E: " + str(dimensions.get("E", "기록 없음")) + "/2")
            for demand in answer["question_demands"]:
                values = [statuses[rid] for rid in demand["requirement_ids"] if rid in statuses]
                if values:
                    messages.append("- " + demand["label"] + ": " + "/".join(values))
        messages.append("부분·누락 요구를 우선 복습하세요. 판정은 확정 당시 기록이며 표현 인식 누락 가능성이 있습니다. D/E는 근거·적용조건·결론의 연결을 점검하세요.")
        output.extend(_pages("\n".join(messages)))
    return output


def _short(value, limit):
    text = " ".join(value.split()) if isinstance(value, str) else ""
    return text if len(text) <= limit else text[:limit - 1] + "…"


def feedback_lesson_lines(feedback, training):
    """Historical navigation must match the currently loaded lesson revisions."""
    nav = feedback.get('learning_navigation') if isinstance(feedback, dict) else None
    if not isinstance(nav, dict) or nav.get('score_effect') != 'none' or not nav.get('recommendations'):
        return []
    current = training.get('learning_synthesis') or {}
    if (current.get('status') != 'loaded'
            or current.get('document', {}).get('topic_id') != nav.get('topic_id')
            or current.get('master_revision') != nav.get('master_revision')
            or current.get('document', {}).get('revision') != nav.get('synthesis_revision')):
        return ['이전 학습 절 안내는 현재 자료 버전과 달라 다시 확인해야 합니다.']
    allowed = set(current['eligible_section_ids'])
    lines, seen = [], set()
    for recommendation in nav['recommendations']:
        for lesson in recommendation['lessons']:
            sid = lesson['section_id']
            if sid in allowed and sid not in seen:
                lines.append('이전 진단에 따른 복습 절: ' + _short(lesson['title'], 100) + ' [' + _short(sid, 80) + ']')
                seen.add(sid)
    return lines[:4]


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
