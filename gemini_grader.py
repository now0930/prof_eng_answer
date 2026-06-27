import os
import re
import json
import urllib.request
import urllib.error
from pathlib import Path


def _extract_json(text):
    text = text or ""

    try:
        return json.loads(text)
    except Exception:
        pass

    m = re.search(r"```json\s*(.*?)\s*```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            pass

    raise ValueError("Gemini 응답에서 JSON을 파싱하지 못했습니다.")


def _compact(obj, max_chars=16000):
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    if len(s) > max_chars:
        return s[:max_chars] + "\n...[TRUNCATED]..."
    return s


def build_gemini_grading_prompt(
    question_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval,
):
    layers = scoring_model.get("layers", [])
    raters = rater_profile.get("raters", []) if rater_profile else []

    return f"""
너는 산업계측제어기술사 답안 채점위원이다.

너의 역할:
- 답안을 단순 키워드가 아니라 의미와 논리로 평가한다.
- 최종 cap 적용은 Python이 하므로, 너는 cap 적용 전 원점수(raw layer score)를 평가한다.
- 답안이 짧으면 짧다는 사실은 반영하되, Python의 volume cap과 중복으로 과도하게 깎지는 않는다.
- 하지만 키워드만 있고 설명이 없으면 높은 점수를 주면 안 된다.
- fact가 틀리면 대책 점수도 보수적으로 본다.
- 기술사 답안은 배경 → 문제점 → fact 설명 → 현실적 대책 → 연결성/면접 방어 가능성이 중요하다.

채점 철학:
1. 문제 의도 파악이 중요하다.
2. 문제점 정의가 정확해야 한다.
3. fact 기반 설명은 핵심 개념을 정확하고 간결하게 설명하는지 본다.
4. 대책은 현실적이어야 한다. 비용, 시간, 적용 가능성, 기존 설비 영향, 운전 리스크를 고려한다.
5. 개인 의견은 문제점과 fact에서 논리적으로 도출되어야 한다.
6. 기술사 답안지 25점 문항은 약 3쪽 전개가 평균이다.
7. 사진 3장과 OCR이 함께 들어오면 OCR 누락 가능성을 고려한다.

점수 항목:
{_compact(layers)}

채점자 역할:
{_compact(raters)}

현재 volume 판단:
{_compact(volume)}

현재 Python fact anchor 평가:
{_compact(fact_eval)}

현재 Python connection 평가:
{_compact(connection_eval)}

문제:
{question_text}

답안:
{answer_text}

반드시 아래 JSON만 출력하라. 설명 문장, markdown, 코드블록을 붙이지 마라.

{{
  "version": "gemini_semantic_grader_v1",
  "confidence": "low|medium|high",
  "overall_comment": "총평",
  "layers": [
    {{
      "layer_id": "A",
      "score": 0.0,
      "max": 4.0,
      "reason": "배경과 문제 진입 평가 사유",
      "evidence": ["답안에서 확인한 근거"]
    }},
    {{
      "layer_id": "B",
      "score": 0.0,
      "max": 5.0,
      "reason": "문제점 정의 평가 사유",
      "evidence": []
    }},
    {{
      "layer_id": "C",
      "score": 0.0,
      "max": 8.0,
      "reason": "fact 기반 설명 평가 사유",
      "evidence": []
    }},
    {{
      "layer_id": "D",
      "score": 0.0,
      "max": 6.0,
      "reason": "현실적 대책 평가 사유",
      "evidence": []
    }},
    {{
      "layer_id": "E",
      "score": 0.0,
      "max": 2.0,
      "reason": "연결성/면접 방어 가능성 평가 사유",
      "evidence": []
    }}
  ],
  "fact_anchor_review": [
    {{
      "id": "F1",
      "level": 0.0,
      "reason": "fact anchor 평가"
    }}
  ],
  "connection_review": {{
    "background_to_problem": "평가",
    "problem_to_fact": "평가",
    "fact_to_solution": "평가",
    "solution_to_problem": "평가"
  }},
  "rater_comments": [
    {{
      "rater_id": "professor",
      "comment": "교수 관점 평가"
    }},
    {{
      "rater_id": "professional_engineer",
      "comment": "기술사 관점 평가"
    }},
    {{
      "rater_id": "executive",
      "comment": "기업 임원 관점 평가"
    }}
  ],
  "risks": ["과대평가 또는 과소평가 위험"],
  "improvement_advice": ["보완 조언"]
}}
"""


def gemini_semantic_grade(
    question_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval,
    timeout=180,
):
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    )
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        return {
            "ok": False,
            "error": "GEMINI_API_KEY 환경변수가 없습니다.",
            "parsed": None,
            "raw_text": ""
        }

    prompt = build_gemini_grading_prompt(
        question_text=question_text,
        answer_text=answer_text,
        scoring_model=scoring_model,
        subject_rubric=subject_rubric,
        rater_profile=rater_profile,
        volume=volume,
        fact_eval=fact_eval,
        connection_eval=connection_eval,
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 8192
        }
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "error": f"Gemini HTTPError {e.code}: {body}",
            "parsed": None,
            "raw_text": ""
        }
    except Exception as e:
        return {
            "ok": False,
            "error": f"Gemini request failed: {e!r}",
            "parsed": None,
            "raw_text": ""
        }

    text_parts = []
    for cand in data.get("candidates", []):
        content = cand.get("content", {})
        for part in content.get("parts", []):
            if "text" in part:
                text_parts.append(part["text"])

    raw_text = "\n\n".join(text_parts).strip()

    try:
        parsed = _extract_json(raw_text)
    except Exception as e:
        return {
            "ok": False,
            "error": f"Gemini JSON parse failed: {e!r}",
            "parsed": None,
            "raw_text": raw_text,
            "raw_response": data
        }

    return {
        "ok": True,
        "error": "",
        "model": model,
        "parsed": parsed,
        "raw_text": raw_text,
        "raw_response": data
    }
