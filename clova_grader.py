from semantic_question_type_prompt import (
    build_question_type_json_contract,
    build_question_type_semantic_guidance,
)

#!/usr/bin/env python3
import json
import os
import re
import time
import uuid
import urllib.request
import urllib.error
from typing import Any, Dict


def _safe_json_loads(text: str) -> Dict[str, Any]:
    text = (text or "").strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text.strip(), flags=re.I).strip()
        text = re.sub(r"```$", "", text.strip()).strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start:end + 1])

    raise ValueError("CLOVA response does not contain valid JSON")


def _extract_clova_content(data: Dict[str, Any]) -> str:
    # CLOVA native response
    result = data.get("result")
    if isinstance(result, dict):
        message = result.get("message")
        if isinstance(message, dict) and message.get("content"):
            return str(message.get("content"))

        if result.get("text"):
            return str(result.get("text"))

    # OpenAI-compatible style fallback
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            msg = first.get("message")
            if isinstance(msg, dict) and msg.get("content"):
                return str(msg.get("content"))
            if first.get("text"):
                return str(first.get("text"))

    return json.dumps(data, ensure_ascii=False)


def _shorten_text(value, limit=3000):
    text = str(value or "")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]..."


def _safe_compact(value, limit=6000):
    try:
        text = json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        text = str(value)
    return _shorten_text(text, limit)


def _find_value(obj, key_names):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in key_names and v:
                return v
        for v in obj.values():
            found = _find_value(v, key_names)
            if found:
                return found
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            found = _find_value(v, key_names)
            if found:
                return found
    return None


def _build_prompt(*args, **kwargs) -> str:
    """
    CLOVA는 Gemini보다 입력 제한에 민감하므로,
    긴 Gemini용 prompt를 그대로 쓰지 않고 compact prompt로 축약한다.
    """
    max_chars = int(os.getenv("CLOVA_MAX_PROMPT_CHARS", "16000"))

    # 1) 먼저 기존 Gemini prompt를 만들어보고, 충분히 짧으면 그대로 사용
    try:
        from gemini_grader import build_gemini_grading_prompt
        prompt = build_gemini_grading_prompt(*args, **kwargs)
        if len(prompt) <= max_chars:
            return prompt
    except Exception:
        prompt = ""

    # 2) 길거나 실패하면 CLOVA용 compact prompt 생성
    all_input = {
        "args": args,
        "kwargs": kwargs,
    }

    question = (
        _find_value(all_input, {"question", "problem", "exam_question", "question_text"})
        or ""
    )
    answer = (
        _find_value(all_input, {"answer", "answer_text", "student_answer", "ocr_text", "response"})
        or ""
    )
    rubric = (
        _find_value(all_input, {"rubric", "rubrics", "scoring_model", "active_profile"})
        or ""
    )
    existing_grade = (
        _find_value(all_input, {"grade", "base_grade", "result", "grading_result"})
        or ""
    )

    compact_payload = {
        "question": _shorten_text(question, 2500),
        "student_answer": _shorten_text(answer, 6000),
        "rubric_or_context": _safe_compact(rubric, 2500),
        "existing_grade_or_context": _safe_compact(existing_grade, 3000),
        "input_summary": _safe_compact(all_input, 3000),
    }

    compact_prompt = (
        "당신은 산업계측제어기술사 답안 채점 보조 모델입니다.\n"
        "아래 입력을 바탕으로 답안의 의미 평가를 수행하십시오.\n"
        "반드시 JSON 객체만 출력하십시오. 설명 문장이나 Markdown은 출력하지 마십시오.\n\n"
        "평가 기준:\n"
        "- A. 배경과 문제 진입\n"
        "- B. 문제 요구 파악\n"
        "- C. 유형별 Fact 기반 내용 설명\n"
        "- D. 현장 적용·설계 판단·제언\n"
        "- E. 연결성·면접 방어 가능성\n\n"
        "출력 JSON 형식:\n"
        "{\n"
        '  "ok": true,\n'
        '  "semantic_scores": {\n'
        '    "A": 0.0,\n'
        '    "B": 0.0,\n'
        '    "C": 0.0,\n'
        '    "D": 0.0,\n'
        '    "E": 0.0\n'
        "  },\n"
        '  "comments": {\n'
        '    "A": "평가 의견",\n'
        '    "B": "평가 의견",\n'
        '    "C": "평가 의견",\n'
        '    "D": "평가 의견",\n'
        '    "E": "평가 의견"\n'
        "  },\n"
        '  "strengths": ["장점"],\n'
        '  "weaknesses": ["약점"],\n'
        '  "improvement_points": ["보완 방향"],\n'
        '  "adjustment_reason": "의미 평가 근거"\n'
        "}\n\n"
        "입력:\n"
        + json.dumps(compact_payload, ensure_ascii=False, default=str)
    )

    if len(compact_prompt) > max_chars:
        compact_prompt = compact_prompt[:max_chars] + "\n...[prompt truncated]..."

    return compact_prompt


def _clova_chat(prompt: str) -> str:
    api_key = os.getenv("CLOVA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("CLOVA_API_KEY is empty")

    model = os.getenv("CLOVA_MODEL", "HCX-003").strip() or "HCX-003"
    host = os.getenv("CLOVA_HOST", "https://clovastudio.stream.ntruss.com").rstrip("/")
    endpoint = os.getenv("CLOVA_ENDPOINT", f"/v1/chat-completions/{model}").strip()

    if "{model}" in endpoint:
        endpoint = endpoint.format(model=model)

    url = host + endpoint

    request_id = (
        os.getenv("CLOVA_REQUEST_ID", "").strip()
        or f"prof-eng-answer-{uuid.uuid4()}"
    )

    body = {
        "messages": [
            {
                "role": "system",
                "content": "You are a strict Korean professional engineer exam answer evaluator. Return JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": float(os.getenv("CLOVA_TEMPERATURE", "0.1")),
        "topP": float(os.getenv("CLOVA_TOP_P", "0.8")),
        "maxTokens": int(os.getenv("CLOVA_MAX_TOKENS", "2048")),
        "includeAiFilters": False,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-NCP-CLOVASTUDIO-REQUEST-ID": request_id,
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
    }

    # Legacy key를 쓰는 환경이면 선택적으로 같이 보낸다.
    apigw_key = os.getenv("CLOVA_APIGW_API_KEY", "").strip()
    if apigw_key:
        headers["X-NCP-CLOVASTUDIO-API-KEY"] = api_key
        headers["X-NCP-APIGW-API-KEY"] = apigw_key

    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=int(os.getenv("CLOVA_TIMEOUT", "120"))) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        raise RuntimeError(
            f"CLOVA HTTPError {e.code}: {body[:4000]} "
            f"| url={url} | model={model}"
        ) from e

    parsed = json.loads(raw)
    return _extract_clova_content(parsed)


def clova_semantic_grade(*args, **kwargs) -> Dict[str, Any]:
    retries = int(os.getenv("CLOVA_RETRIES", "2"))
    delays = [2, 5, 10]

    last_error = None

    for attempt in range(retries + 1):
        try:
            prompt = _build_prompt(*args, **kwargs)
            content = _clova_chat(prompt)
            result = _safe_json_loads(content)

            if isinstance(result, dict):
                result.setdefault("ok", True)
                result.setdefault("llm_provider", "clova")
                result.setdefault("llm_model", os.getenv("CLOVA_MODEL", "HCX-003"))
                result.setdefault("retry_info", {"attempt": attempt + 1})
                return result

            return {
                "ok": False,
                "llm_provider": "clova",
                "error": "CLOVA returned non-dict JSON",
                "raw": str(result)[:1000],
            }

        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(delays[min(attempt, len(delays) - 1)])
                continue

    return {
        "ok": False,
        "llm_provider": "clova",
        "error": str(last_error),
    }





# === qtype semantic result postprocess wrapper v2 ===
_ORIGINAL_CLOVA_SEMANTIC_GRADE_QTYPE_V2 = clova_semantic_grade

def clova_semantic_grade(*args, **kwargs):
    from semantic_question_type_postprocess import ensure_question_type_coverage

    result = _ORIGINAL_CLOVA_SEMANTIC_GRADE_QTYPE_V2(*args, **kwargs)

    question_text = (
        kwargs.get("question_text")
        or kwargs.get("question")
        or (args[0] if args else None)
    )
    existing_question_type = (
        kwargs.get("question_type")
        or kwargs.get("detected_question_type")
        or kwargs.get("legacy_question_type")
    )

    return ensure_question_type_coverage(
        result,
        question_text=question_text,
        existing_question_type=existing_question_type,
    )

if __name__ == "__main__":
    content = _clova_chat('{"test": true} 형태의 JSON만 출력해.')
    print(content[:1000])
