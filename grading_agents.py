#!/usr/bin/env python3
import json
import re
from datetime import datetime
from pathlib import Path


def extract_json(text):
    if not text:
        return None

    text = str(text).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    if start < 0:
        return None

    in_string = False
    escape = False
    depth = 0

    for i in range(start, len(text)):
        ch = text[i]

        if escape:
            escape = False
            continue

        if ch == "\\":
            escape = True
            continue

        if ch == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start:i + 1]
                try:
                    return json.loads(candidate)
                except Exception:
                    return None

    return None


def write_json(path, data):
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def rubric_items(rubric):
    items = rubric.get("items", []) if isinstance(rubric, dict) else []
    clean = []
    for item in items:
        clean.append({
            "name": item.get("name", "항목"),
            "points": float(item.get("points", 0)),
            "criteria": item.get("criteria", [])
        })
    return clean


def rubric_total_points(rubric):
    if isinstance(rubric, dict):
        if "total_points" in rubric:
            return float(rubric["total_points"])
        items = rubric_items(rubric)
        if items:
            return sum(x["points"] for x in items)
    return 25.0


def short_list(values, limit=5):
    if not isinstance(values, list):
        return []
    result = []
    for v in values[:limit]:
        if isinstance(v, str):
            result.append(v[:120])
        else:
            result.append(str(v)[:120])
    return result


def clean_text(value, limit=300):
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\\rightarrow", "→")
    text = text.replace("$ightarrow$", "→")
    text = text.replace("$", "")
    text = text.replace("\\", "")
    return text[:limit]


def build_compact_prompt(raw_text, rubric, sid, image_count):
    items = rubric_items(rubric)
    item_names = [x["name"] for x in items]
    max_score = rubric_total_points(rubric)

    return f"""
너는 기술사 논술형 답안 분석 보조자다.
최종 채점표는 시스템이 만들 것이므로, 너는 간단한 JSON 분석값만 작성한다.

절대 규칙:
- JSON 하나만 출력한다.
- markdown code block을 쓰지 않는다.
- 모든 문자열은 짧게 쓴다.
- LaTeX, 역슬래시, 달러 기호를 쓰지 않는다.
- A, B, C 등급을 쓰지 않는다.
- 점수는 반드시 숫자로 쓴다.
- scores 배열에는 반드시 아래 rubric_items와 같은 항목명만 사용한다.
- scores 배열의 원소는 반드시 object만 사용한다.
- scores 배열 안에 문자열을 넣지 않는다.

세션 ID: {sid}
첨부 이미지 수: {image_count}
만점: {max_score}

rubric_items:
{json.dumps(item_names, ensure_ascii=False)}

rubric:
{json.dumps(rubric, ensure_ascii=False)}

사용자 원문:
{raw_text}

출력 JSON 형식:
{{
  "problem": "문제 원문",
  "subject": "추정 과목명 또는 unknown",
  "topic": "핵심 주제",
  "question_type": "explain|compare|discuss|countermeasure|procedure|cause_prevention|unknown",
  "demand_verbs": ["설명하시오"],
  "expected_structure": ["개요", "본론", "결론"],
  "required_perspectives": ["품질", "안전", "공정", "원가", "유지관리"],
  "expected_keywords": ["키워드1", "키워드2"],
  "detected_keywords": ["답안에 실제 있는 키워드"],
  "detected_perspectives": ["답안에 실제 있는 관점"],
  "evidence_quotes": ["답안에 실제 있는 짧은 근거 문장"],
  "missing_expected_parts": ["누락 항목"],
  "strengths": ["장점"],
  "weaknesses": ["약점"],
  "rewrite_advice": ["보완 방향"],
  "scores": [
    {{
      "item": "{item_names[0] if item_names else '종합 평가'}",
      "score": 0,
      "reason": "짧은 사유"
    }}
  ],
  "one_line_summary": "한 줄 총평",
  "grade_confidence": "high|medium|low"
}}
""".strip()


def fallback_analysis(raw_text, rubric):
    return {
        "problem": "",
        "subject": "unknown",
        "topic": "unknown",
        "question_type": "unknown",
        "demand_verbs": [],
        "expected_structure": [],
        "required_perspectives": [],
        "expected_keywords": [],
        "detected_keywords": [],
        "detected_perspectives": [],
        "evidence_quotes": [],
        "missing_expected_parts": [],
        "strengths": [],
        "weaknesses": ["모델 응답 JSON 파싱에 실패하여 보수적으로 채점함."],
        "rewrite_advice": ["문제 요구 구조에 맞춰 목차와 핵심 키워드를 보강할 것."],
        "scores": [],
        "one_line_summary": "모델 분석 실패로 보수적 기본 채점을 적용함.",
        "grade_confidence": "low"
    }


def build_question_analysis(analysis, rubric):
    return {
        "problem": clean_text(analysis.get("problem")),
        "point_allocated": rubric_total_points(rubric),
        "subject": clean_text(analysis.get("subject"), 80) or "unknown",
        "topic": clean_text(analysis.get("topic"), 80) or "unknown",
        "question_type": clean_text(analysis.get("question_type"), 40) or "unknown",
        "demand_verbs": short_list(analysis.get("demand_verbs"), 5),
        "expected_structure": short_list(analysis.get("expected_structure"), 5),
        "required_perspectives": short_list(analysis.get("required_perspectives"), 5),
        "expected_keywords": short_list(analysis.get("expected_keywords"), 8),
        "answer_text_detected": True,
        "analysis_confidence": clean_text(analysis.get("grade_confidence"), 20) or "medium",
        "notes": []
    }


def build_evidence(analysis):
    return {
        "detected_keywords": short_list(analysis.get("detected_keywords"), 10),
        "detected_structure": short_list(analysis.get("expected_structure"), 5),
        "detected_perspectives": short_list(analysis.get("detected_perspectives"), 5),
        "evidence_quotes": [
            {
                "quote": clean_text(q, 100),
                "supports": []
            }
            for q in short_list(analysis.get("evidence_quotes"), 3)
        ],
        "missing_expected_parts": short_list(analysis.get("missing_expected_parts"), 8),
        "missing_or_unclear": [],
        "answer_depth_assessment": "short",
        "evidence_confidence": clean_text(analysis.get("grade_confidence"), 20) or "medium"
    }


def score_from_analysis(analysis, rubric):
    items = rubric_items(rubric)
    max_total = rubric_total_points(rubric)
    raw_scores = analysis.get("scores", [])

    score_map = {}
    if isinstance(raw_scores, list):
        for row in raw_scores:
            if not isinstance(row, dict):
                continue
            name = str(row.get("item", "")).strip()
            try:
                score = float(row.get("score", 0))
            except Exception:
                score = 0.0
            reason = clean_text(row.get("reason"), 180)
            score_map[name] = {
                "score": score,
                "reason": reason
            }

    breakdown = []

    if items:
        for item in items:
            name = item["name"]
            max_item = item["points"]
            matched = score_map.get(name)

            if matched:
                score = max(0.0, min(float(matched["score"]), max_item))
                reason = matched["reason"] or "항목 기준에 따라 부분 점수 부여."
            else:
                # 모델이 항목 점수를 누락하면 중간 이하 기본값
                score = round(max_item * 0.52, 2)
                reason = "모델이 해당 항목 점수를 누락하여 보수적 기본 점수를 적용함."

            breakdown.append({
                "item": name,
                "score": round(score, 2),
                "max": max_item,
                "reason": reason,
                "evidence_used": []
            })
    else:
        breakdown.append({
            "item": "종합 평가",
            "score": round(max_total * 0.52, 2),
            "max": max_total,
            "reason": "채점 항목이 없어 보수적 종합 점수를 적용함.",
            "evidence_used": []
        })

    total = round(sum(float(x["score"]) for x in breakdown), 2)
    return total, breakdown


def build_grade(analysis, rubric, sid, question_analysis, evidence):
    max_total = rubric_total_points(rubric)
    total, breakdown = score_from_analysis(analysis, rubric)

    confidence = clean_text(analysis.get("grade_confidence"), 20) or "medium"
    if confidence not in ["high", "medium", "low"]:
        confidence = "medium"

    score_low = max(0, int(total) - 2)
    score_high = min(int(max_total), int(total) + 2)

    missing = short_list(analysis.get("missing_expected_parts"), 8)

    grade = {
        "session_id": sid,
        "rubric_type": "derived_public_source_rubric",
        "total_score": total,
        "max_score": max_total,
        "score_range": f"{score_low}~{score_high}",
        "grade_confidence": confidence,
        "one_line_summary": clean_text(analysis.get("one_line_summary"), 220) or "기준에 따라 부분 점수를 부여함.",
        "breakdown": breakdown,
        "strengths": short_list(analysis.get("strengths"), 5),
        "weaknesses": short_list(analysis.get("weaknesses"), 5),
        "missing_keywords": missing,
        "rewrite_advice": short_list(analysis.get("rewrite_advice"), 3),
        "model_answer_outline": question_analysis.get("expected_structure", []),
        "next_practice_focus": short_list(analysis.get("rewrite_advice"), 3),
        "audit_note": "모델은 compact analysis만 생성했고, 최종 grade.json은 Python이 rubric 기준으로 조립했습니다.",
        "question_analysis_summary": {
            "topic": question_analysis.get("topic"),
            "question_type": question_analysis.get("question_type"),
            "analysis_confidence": question_analysis.get("analysis_confidence")
        },
        "evidence_summary": {
            "detected_keywords": evidence.get("detected_keywords", []),
            "missing_expected_parts": evidence.get("missing_expected_parts", []),
            "evidence_confidence": evidence.get("evidence_confidence")
        },
        "agent_pipeline": {
            "version": "2026-06-27-agent-v3-python-assembled-grade",
            "logical_steps": [
                "question_analysis",
                "answer_evidence_extraction",
                "python_assembled_grading"
            ],
            "physical_llm_calls": 1,
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
    }

    return grade


def run_agent_pipeline(call_ollama_fn, raw_text, rubric, sid, image_count, session_dir, progress_fn=None):
    session_dir = Path(session_dir)
    session_dir.mkdir(parents=True, exist_ok=True)

    def progress(msg):
        print(f"[agent] {msg}", flush=True)
        if progress_fn:
            try:
                progress_fn(msg)
            except Exception:
                pass

    write_json(session_dir / "rubric_snapshot.json", rubric)

    progress("1/3 문제 분석, 2/3 답안 근거 추출, 3/3 Python 기준 채점을 수행합니다.")

    prompt = build_compact_prompt(raw_text, rubric, sid, image_count)

    (session_dir / "question_analysis_prompt.txt").write_text(prompt, encoding="utf-8")
    (session_dir / "evidence_prompt.txt").write_text(prompt, encoding="utf-8")
    (session_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    raw_result = call_ollama_fn(prompt)

    (session_dir / "question_analysis_raw.txt").write_text(raw_result, encoding="utf-8")
    (session_dir / "evidence_raw.txt").write_text(raw_result, encoding="utf-8")
    (session_dir / "grade_raw.txt").write_text(raw_result, encoding="utf-8")

    analysis = extract_json(raw_result)
    if not isinstance(analysis, dict):
        analysis = fallback_analysis(raw_text, rubric)
        progress("모델 분석 JSON 파싱에 실패하여 fallback 채점을 적용합니다.")

    question_analysis = build_question_analysis(analysis, rubric)
    evidence = build_evidence(analysis)
    grade = build_grade(analysis, rubric, sid, question_analysis, evidence)

    write_json(session_dir / "question_analysis.json", question_analysis)
    write_json(session_dir / "evidence.json", evidence)
    write_json(session_dir / "grade.json", grade)

    progress("채점 파이프라인이 완료되었습니다.")
    return raw_result, grade
