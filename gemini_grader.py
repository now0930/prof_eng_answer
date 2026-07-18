from semantic_question_type_prompt import (
    build_question_type_json_contract,
    build_question_type_semantic_guidance,
)

import os
import re
import json
import urllib.request
import urllib.error
from pathlib import Path


def _extract_json(text: str) -> dict:
    normalized = str(text or "").strip()

    if not normalized:
        raise ValueError(
            "Gemini 응답에서 JSON 객체를 찾지 못했습니다."
        )

    def parse_object(candidate: str):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            raise ValueError(
                "Gemini 응답 JSON root는 object여야 합니다."
            )

        return parsed

    direct_result = parse_object(normalized)

    if direct_result is not None:
        return direct_result

    fence_match = re.fullmatch(
        r"\s*```(?:json)?\s*(.*?)\s*```\s*",
        normalized,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if fence_match:
        fenced_result = parse_object(
            fence_match.group(1).strip()
        )

        if fenced_result is not None:
            return fenced_result

    decoder = json.JSONDecoder()
    search_index = 0

    while True:
        object_start = normalized.find(
            "{",
            search_index,
        )

        if object_start < 0:
            break

        try:
            parsed, _end = decoder.raw_decode(
                normalized[object_start:]
            )
        except json.JSONDecodeError:
            search_index = object_start + 1
            continue

        if isinstance(parsed, dict):
            return parsed

        search_index = object_start + 1

    raise ValueError(
        "Gemini 응답에서 JSON 객체를 찾지 못했습니다."
    )


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
- 기술사 답안은 배경 → 문제점 → fact 설명 → 현장 적용·제언 → 연결성/면접 방어 가능성이 중요하다.

채점 철학:
1. 문제 의도 파악이 중요하다.
2. 문제 요구 파악이 정확해야 한다.
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
      "max": 3.0,
      "reason": "문제 진입·답안 구조 평가 사유",
      "evidence": ["답안에서 확인한 근거"]
    }},
    {{
      "layer_id": "B",
      "score": 0.0,
      "max": 6.0,
      "reason": "문제 요구 해석·완전성 평가 사유",
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
      "reason": "현장 적용·제언 평가 사유",
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
            "temperature": 0.0,
            "topP": 1.0,
            "candidateCount": 1,
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


# ============================================================
# PHASE9_QUESTION_TYPE_LENS_PROMPT_WRAPPER
# question_type은 C항목의 Fact 설명 방식 렌즈로만 사용한다.
# ============================================================

_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT = build_gemini_grading_prompt


def build_gemini_grading_prompt(
    question_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval
):
    base_prompt = _ORIGINAL_BUILD_GEMINI_GRADING_PROMPT(
        question_text,
        answer_text,
        scoring_model,
        subject_rubric,
        rater_profile,
        volume,
        fact_eval,
        connection_eval
    )

    qte = {}
    if isinstance(subject_rubric, dict):
        qte = subject_rubric.get("question_type_evaluation") or {}

    if not qte:
        return base_prompt

    primary = qte.get("primary_type") or {}
    policy = qte.get("policy") or {}

    lens_text = f"""

[문제 유형 기반 C항목 평가 렌즈]

중요 원칙:
- 문제 유형은 별도 채점 체계가 아니다.
- 기존 A/B/C/D/E 25점 구조는 유지한다.
- question_type은 C항목의 Fact 기반 설명 방식을 결정하는 렌즈로만 사용한다.
- A/B/D/E는 모든 문제 유형에 공통 적용한다.
- 특히 D/E에서는 모든 유형에 대해 현실 적용성, 현장 문제 연결, 개선 제언, 기술사적 판단성을 평가한다.

선택된 문제 유형:
- ID: {primary.get("id")}
- 이름: {primary.get("name")}
- 신뢰도: {qte.get("confidence")}

C항목 평가 렌즈:
{primary.get("c_lens")}

C항목에서 확인할 필수 요소:
{primary.get("c_required_elements")}

낮은 답안 패턴:
{primary.get("weak_answer_pattern")}

높은 답안 패턴:
{primary.get("high_score_pattern")}

채점 지시:
- C항목은 위 문제 유형 렌즈에 따라 평가하라.
- 단순 키워드 나열은 낮게 평가하라.
- 유형별 Fact 설명이 충분하더라도 D/E에서 현실 적용성, 해결 제언, 기술사적 판단이 부족하면 고득점으로 보지 마라.
- 계산·설계형도 별도 예외가 아니라 C항목 렌즈 중 하나로만 본다.
- 평가형, 절차형, 비교형도 마찬가지로 C항목의 설명 방식 차이로만 본다.
""".strip()

    return base_prompt + "\n\n" + lens_text


# ============================================================
# PHASE10_MODEL_ANSWER_REFERENCE_PROMPT_WRAPPER
# 모범 답안은 정답 매칭용이 아니라 구조·깊이·현장 적용성 기준으로만 사용
# ============================================================

_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_PHASE10 = build_gemini_grading_prompt


def build_gemini_grading_prompt(
    question_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval
):
    base_prompt = _ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_PHASE10(
        question_text,
        answer_text,
        scoring_model,
        subject_rubric,
        rater_profile,
        volume,
        fact_eval,
        connection_eval
    )

    model_ref = {}
    if isinstance(subject_rubric, dict):
        model_ref = subject_rubric.get("model_answer_reference") or {}

    if not model_ref or not model_ref.get("matched"):
        return base_prompt

    ref = model_ref.get("primary_reference") or {}
    policy = model_ref.get("policy") or {}

    ref_text = f"""

[모범 답안 Bank 참조 기준]

중요 원칙:
- 모범 답안은 정답 문장 매칭용이 아니다.
- 동일 문장을 요구하지 마라.
- 표현이나 순서가 달라도 핵심 fact, 논리, 구조, 현장 적용성, 제언이 충분하면 인정하라.
- 모범 답안보다 더 나은 현장 판단, 적용 조건, 비용·운전·안전 고려가 있으면 긍정적으로 평가하라.
- 모범 답안은 부족 요소 탐지와 보완 방향 제시를 위한 기준 답안이다.
- 기존 A/B/C/D/E 25점 구조와 답안 분량 cap을 유지하라.

선택된 모범 답안:
- ID: {ref.get("id")}
- topic_id: {ref.get("topic_id")}
- question_type: {ref.get("question_type")}
- title: {ref.get("title")}
- match_confidence: {model_ref.get("confidence")}
- match_reasons: {model_ref.get("match_reasons")}

모범 답안 사용 정책:
{policy}

기대 답안 구조:
{ref.get("expected_structure")}

모범 답안 outline:
{ref.get("model_answer_outline")}

고득점 특징:
{ref.get("high_score_features")}

저득점 패턴:
{ref.get("low_score_patterns")}

현장 연결 포인트:
{ref.get("field_connection_points")}

채점 지시:
- C항목에서는 위 모범 답안을 참고하여 Fact 설명의 구조와 깊이를 평가하라.
- D/E항목에서는 현장 적용성, 문제 해결, 제언, 기술사적 판단성을 평가하라.
- 모범 답안에 없는 문장이라도 기술적으로 타당하고 현장성이 높으면 인정하라.
- 모범 답안과 문장이 비슷하더라도 현장 적용성이나 논리 연결이 부족하면 고득점으로 보지 마라.
- 피드백에는 모범 답안 기준에서 부족한 구조, fact, 현장 연결 포인트를 구체적으로 제시하라.
""".strip()

    return base_prompt + "\n\n" + ref_text


# ============================================================
# PHASE11_REQUIREMENT_AND_TYPE_FACT_PROMPT_WRAPPER
# B/C 항목 의미 정리:
# B = 문제 요구 해석·완전성
# C = 유형별 Fact 기반 내용 설명
# ============================================================

_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_PHASE11 = build_gemini_grading_prompt


def build_gemini_grading_prompt(
    question_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval
):
    base_prompt = _ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_PHASE11(
        question_text,
        answer_text,
        scoring_model,
        subject_rubric,
        rater_profile,
        volume,
        fact_eval,
        connection_eval
    )

    phase11_text = """

[B/C 항목 평가 의미 정리]

중요:
- B항목은 '문제점 정의'가 아니라 '문제 요구 해석·완전성'이다.
- C항목은 'Fact 기반 문제점 설명'이 아니라 '유형별 Fact 기반 내용 설명'이다.
- DEFINE, PRINCIPLE, STRUCTURE, COMPARE, PROCEDURE, CALC_DESIGN, APPLICATION, EVALUATION 문제에서 억지로 문제점을 찾지 마라.
- 문제 유형에 따라 C항목의 Fact 전개 방식이 달라진다.
- 다만 모든 기술사 답안은 D/E에서 현실 적용성, 현장 문제 연결, 제언, 기술사적 판단성을 평가한다.

B. 문제 요구 해석·완전성 평가 기준:
- 답안자가 문제에서 요구한 설명 방향을 정확히 잡았는가?
- 문제문의 요구동사와 세부 요구항목을 모두 식별했는가?
- 각 요구항목에 답안의 목차 또는 본문이 1:1로 대응하는가?
- 핵심 요구항목을 누락하거나 일부만 답하지 않았는가?
- DEFINE이면 정의와 개념 설명 요구를 파악했는가?
- COMPARE이면 비교 대상과 선정 기준 요구를 파악했는가?
- PROCEDURE이면 절차와 판정 기준 요구를 파악했는가?
- CALC_DESIGN이면 공식, 변수, 계산 과정, 설계 기준 설명 요구를 파악했는가?
- EVALUATION이면 평가 지표, 효과 분석, 한계 분석 요구를 파악했는가?

C. 유형별 Fact 기반 내용 설명 평가 기준:
- 선택된 question_type lens에 맞게 Fact를 전개했는가?
- 단순 키워드 나열이 아니라 구조, 인과관계, 절차, 비교축, 계산 의미, 평가 지표 등을 설명했는가?
- Fact Anchor와 Model Answer Bank가 제공된 경우, 동일 문장을 요구하지 말고 구조·깊이·현장 적용성 기준으로 참고하라.

채점 표현 지시:
- DEFINE 문제에서 '문제점 정의가 부족하다'라고 쓰지 말고 '문제 요구에 따른 표준 정의 조건과 실무 의미 설명이 부족하다'라고 써라.
- STRUCTURE 문제에서 '문제점 정의가 없다'라고 쓰지 말고 '구성요소, 분류 기준, 역할 관계 설명이 부족하다'라고 써라.
- COMPARE 문제에서 '문제점 정의가 없다'라고 쓰지 말고 '비교축, 적용 조건, 선정 기준 설명이 부족하다'라고 써라.
- PROCEDURE 문제에서 '문제점 정의가 없다'라고 쓰지 말고 '절차 순서, 입력 자료, 판정 기준, 산출물 설명이 부족하다'라고 써라.
- CALC_DESIGN 문제에서 '문제점 정의가 없다'라고 쓰지 말고 '공식, 변수, 단위, 계산 결과 해석, 설계 기준 설명이 부족하다'라고 써라.
- EVALUATION 문제에서 '문제점 정의가 없다'라고 쓰지 말고 '평가 지표, 전후 비교, 정량·정성 효과, 한계 분석이 부족하다'라고 써라.
""".strip()

    return base_prompt + "\n\n" + phase11_text


# ============================================================
# PHASE12_FIELD_APPLICATION_LABEL_PROMPT_WRAPPER
# D항목을 '대책' 중심이 아니라 현장 적용·설계 판단·제언으로 표현
# ============================================================

_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_PHASE12 = build_gemini_grading_prompt


def build_gemini_grading_prompt(
    question_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval
):
    base_prompt = _ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_PHASE12(
        question_text,
        answer_text,
        scoring_model,
        subject_rubric,
        rater_profile,
        volume,
        fact_eval,
        connection_eval
    )

    phase12_text = """

[D/E 항목 표현 원칙]

- D항목은 '현실적 대책'만을 의미하지 않는다.
- D항목은 모든 문제 유형에서 '현장 적용성, 설계 판단, 운영 조건, 비용·안전·유지보수 고려, 제언'을 평가한다.
- DEFINE 문제에서는 대책이 없다고 쓰기보다 '정의가 현장 적용 의미, 선정 기준, 운전 리스크, 제언으로 확장되지 않았다'라고 평가하라.
- COMPARE 문제에서는 '선정 기준과 적용 조건이 부족하다'라고 평가하라.
- PROCEDURE 문제에서는 '절차의 판정 기준, 산출물, 기록·검증이 부족하다'라고 평가하라.
- CALC_DESIGN 문제에서는 '계산 결과 해석과 설계 기준, 현장 적용 의미가 부족하다'라고 평가하라.
- EVALUATION 문제에서는 '평가 지표, 전후 비교, 효과와 한계, 후속 조치가 부족하다'라고 평가하라.

연결성 표현:
- 배경→문제 요구
- 문제 요구→유형별 Fact 설명
- Fact→현장 적용·제언
- 제언→문제 요구 충족
""".strip()

    return base_prompt + "\n\n" + phase12_text



# ============================================================


# ============================================================

# P0_C_DETERMINISTIC_SAMPLING_WRAPPER
_ORIGINAL_GEMINI_SEMANTIC_GRADE_SAMPLING_V1 = (
    gemini_semantic_grade
)


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

    result = (
        _ORIGINAL_GEMINI_SEMANTIC_GRADE_SAMPLING_V1(
            question_text=question_text,
            answer_text=answer_text,
            scoring_model=scoring_model,
            subject_rubric=subject_rubric,
            rater_profile=rater_profile,
            volume=volume,
            fact_eval=fact_eval,
            connection_eval=connection_eval,
            timeout=timeout,
        )
    )

    from llm_sampling import (
        build_llm_request_contract,
    )

    sampling_contract = (
        build_llm_request_contract(
            provider="gemini",
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-2.5-flash",
            ),
            prompt=prompt,
            requested_sampling={
                "temperature": 0.0,
                "top_p": 1.0,
                "candidate_count": 1,
            },
            applied_sampling={
                "temperature": 0.0,
                "top_p": 1.0,
                "candidate_count": 1,
                "max_output_tokens": 8192,
            },
            unsupported_settings=[
                "top_k",
                "seed",
            ],
        )
    )

    if isinstance(result, dict):
        result["llm_request"] = (
            sampling_contract
        )

    return result


# PHASE18_GEMINI_SEMANTIC_RETRY_WRAPPER
# Gemini 503, timeout, connection reset 등 일시 장애 시 재시도
# 점수 계산 로직은 바꾸지 않고 Gemini 호출 안정성만 높인다.
# ============================================================

_ORIGINAL_GEMINI_SEMANTIC_GRADE_PHASE18 = gemini_semantic_grade


def _phase18_is_retryable_gemini_error(err_text):
    text = str(err_text or "").lower()
    retryable_markers = [
        "503",
        "service unavailable",
        "temporarily unavailable",
        "timeout",
        "timed out",
        "connection reset",
        "connectionreseterror",
        "ssl",
        "handshake",
        "rate limit",
        "resource exhausted",
        "deadline",
        "unavailable",
    ]
    return any(m in text for m in retryable_markers)


def gemini_semantic_grade(*args, **kwargs):
    import json
    import time

    delays = [2, 5, 10]
    last_result = None
    last_error = None

    total_attempts = len(delays) + 1

    for attempt_idx, delay in enumerate([0] + delays, start=1):
        if delay:
            time.sleep(delay)

        try:
            result = _ORIGINAL_GEMINI_SEMANTIC_GRADE_PHASE18(*args, **kwargs)
            last_result = result

            # dict가 아니면 기존 동작 유지
            if not isinstance(result, dict):
                return result

            # ok가 없거나 ok=True이면 성공으로 간주
            if result.get("ok", True) is not False:
                if attempt_idx > 1:
                    result.setdefault("retry_info", {})
                    result["retry_info"].update({
                        "retried": True,
                        "attempts": attempt_idx
                    })
                return result

            # ok=False인 경우 retry 가능한 에러인지 확인
            err_text = json.dumps(result, ensure_ascii=False)
            last_error = err_text

            if _phase18_is_retryable_gemini_error(err_text) and attempt_idx < total_attempts:
                print(f"[agent] Gemini semantic grader retry {attempt_idx}/{total_attempts}: {err_text[:300]}")
                continue

            return result

        except Exception as e:
            last_error = repr(e)

            if _phase18_is_retryable_gemini_error(last_error) and attempt_idx < total_attempts:
                print(f"[agent] Gemini semantic grader retry {attempt_idx}/{total_attempts}: {last_error[:300]}")
                continue

            raise

    # 재시도 후에도 실패한 경우 기존 pipeline fallback을 타도록 ok=False 반환
    if isinstance(last_result, dict):
        last_result.setdefault("retry_info", {})
        last_result["retry_info"].update({
            "retried": True,
            "attempts": total_attempts,
            "final_error": last_error,
            "exhausted": True
        })
        return last_result

    return {
        "ok": False,
        "error": f"Gemini semantic grader failed after retries: {last_error}",
        "retry_info": {
            "retried": True,
            "attempts": total_attempts,
            "exhausted": True
        }
    }


# === qtype semantic result postprocess wrapper v2 ===
_ORIGINAL_GEMINI_SEMANTIC_GRADE_QTYPE_V2 = gemini_semantic_grade

def gemini_semantic_grade(*args, **kwargs):
    from semantic_question_type_postprocess import ensure_question_type_coverage

    result = _ORIGINAL_GEMINI_SEMANTIC_GRADE_QTYPE_V2(*args, **kwargs)

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

# === final qtype semantic prompt wrapper v4 EOF ===
# This wrapper must stay near the end of this file because build_gemini_grading_prompt
# is redefined multiple times by phase wrappers.
from semantic_question_type_prompt import (
    build_question_type_json_contract,
    build_question_type_semantic_guidance,
)

_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_QTYPE_V4_EOF = build_gemini_grading_prompt

def build_gemini_grading_prompt(question_text, answer_text, *args, **kwargs):
    base_prompt = _ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_QTYPE_V4_EOF(
        question_text,
        answer_text,
        *args,
        **kwargs,
    )

    if not isinstance(base_prompt, str):
        return base_prompt

    if (
        "Question Type v2 평가 지침" in base_prompt
        and "MANDATORY QUESTION_TYPE_COVERAGE OUTPUT CONTRACT" in base_prompt
        and "QTYPE_HARD_JSON_TEMPLATE_V4" in base_prompt
    ):
        return base_prompt

    existing_question_type = (
        kwargs.get("question_type")
        or kwargs.get("detected_question_type")
        or kwargs.get("legacy_question_type")
    )

    try:
        qtype_guidance = build_question_type_semantic_guidance(
            question_text,
            existing_question_type=existing_question_type,
        )
        qtype_contract = build_question_type_json_contract(
            question_text,
            existing_question_type=existing_question_type,
        )
    except Exception as exc:
        qtype_guidance = (
            "[Question Type v2 평가 지침]\n"
                "question_type 세부 평가 지침 생성에 실패했습니다. "
                f"기존 A/B/C/D/E 기준으로 평가하세요. error={exc}"
        )
        qtype_contract = (
            "[MANDATORY QUESTION_TYPE_COVERAGE OUTPUT CONTRACT]\n"
                "최종 JSON root object에 question_type_coverage 필드를 반드시 포함하세요."
        )

    qtype_template = """
[QTYPE_HARD_JSON_TEMPLATE_V4]

너는 반드시 JSON object 하나만 반환해야 한다.
최상위 JSON에는 반드시 다음 key가 있어야 한다.

- version
- confidence
- overall_comment
- layers
- fact_anchor_review
- connection_review
- rater_comments
- risks
- improvement_advice
- question_type_coverage

question_type_coverage는 절대 생략하지 마라.
question_type_coverage는 raw_text 문자열 내부가 아니라 최상위 JSON field여야 한다.
coverage_source는 반드시 "semantic_grader"로 둔다.
overall_coverage에는 unknown, fallback, not_evaluated를 쓰지 마라.

반드시 다음 구조를 포함하라.

"question_type_coverage": {
  "question_type": "문제 유형",
  "name_ko": "한글 유형명",
  "coverage_source": "semantic_grader",
  "sub_criteria_coverage": [
    {
      "criterion": "sub_criteria 이름",
      "status": "present | partial | incorrect | missing",
      "evidence": "답안 근거 또는 누락 설명",
      "impact": "C 또는 D 점수 판단 영향"
    }
  ],
  "c_fact_focus_coverage": {
    "covered": [],
    "missing": []
  },
  "d_field_judgement_focus_coverage": {
    "covered": [],
    "missing": []
  },
  "missing_sub_criteria": [],
  "overall_coverage": "strong | adequate | weak | poor",
  "scoring_hint": "C/D 항목을 어떻게 보수적으로 볼지 설명"
}

금지:
- question_type_coverage 생략 금지
- coverage_source를 fallback으로 쓰기 금지
- overall_coverage를 unknown으로 쓰기 금지
- markdown 코드블록 출력 금지
"""

    return (
        qtype_template
        + "\n\n"
        + base_prompt
        + "\n\n"
        + qtype_guidance
        + "\n\n"
        + qtype_contract
        + "\n\n"
        + qtype_template
    )



# === explicit question requirement final prompt wrapper v1 ===
_ORIGINAL_BUILD_GEMINI_PROMPT_EXPLICIT_REQ_V1 = (
    build_gemini_grading_prompt
)

def build_gemini_grading_prompt(*args, **kwargs):
    base = _ORIGINAL_BUILD_GEMINI_PROMPT_EXPLICIT_REQ_V1(
        *args,
        **kwargs,
    )

    question_text = (
        args[0]
        if args
        else kwargs.get("question_text")
    )

    explicit_contract = f"""
[FINAL MANDATORY EXPLICIT REQUIREMENT CONTRACT]

문제문:
{question_text or ""}

최종 JSON의 question_type_coverage 내부에 반드시
explicit_requirement_coverage를 포함하라.

"explicit_requirement_coverage": {{
  "source": "question_text",
  "extraction_confidence": "high | medium | low",
  "requirements": [
    {{
      "requirement": "문제문이 직접 요구한 독립 항목",
      "status": "present | partial | incorrect | missing",
      "evidence": "답안 근거 또는 누락 설명",
      "is_core": true
    }}
  ]
}}

유형별 권장 전개와 문제문 직접 요구를 혼동하지 마라.
문제문에 직접 없는 background, 현장 판단, trade-off를
명시적 요구사항으로 만들지 마라.
답안이 요구 항목을 직접 다뤘지만 핵심 사실이 틀리면
incorrect로 평가하라.
답안이 해당 요구 항목을 전혀 다루지 않았을 때만
missing으로 평가하라.
""".strip()

    return base + "\n\n" + explicit_contract
# === PLAN_B_GENERAL_LAYER_OWNERSHIP_PROMPT_V1 ===
_PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1 = build_gemini_grading_prompt


def _plan_b_general_layer_ownership_prompt_v1():
    return """
[PLAN_B_GENERAL_LAYER_OWNERSHIP_V1]

A/B/C/D/E 계층의 역할과 감점 소유권을 다음과 같이 고정한다.

1. A는 문제 진입과 답안 구조만 평가한다. 기술 Fact 정확성, 현장 설계 깊이, 독창성을 A에서 다시 감점하지 않는다.
2. B는 문제문이 명시적으로 요구한 항목에 직접 응답했는지 평가한다.
   - missing: 요구항목을 전혀 다루지 않음
   - partial/shallow: 요구항목을 다뤘으나 일부 범위나 조건이 빠짐
   - addressed: 요구항목에 직접 대응함
   Fact 정확성, 공식, 부호, 방향, 물리적 타당성, 기술 깊이는 C의 주된 책임이다.
   명시적 요구를 다뤘다면 기술 오류나 깊이 부족만으로 B를 누락처럼 감점하지 않는다.
   explicit_requirement_coverage의 incorrect 진단은 유지할 수 있으나 그 기술 오류의 주된 점수 감점은 C에 한 번만 귀속한다.
3. C는 기술 Fact, 공식, 부호와 방향, 전제조건, 물리 모델의 정확성을 평가한다.
   핵심 원리가 틀리면 incorrect, 결론을 반대로 만들거나 안전을 훼손하면 fatal로 본다.
4. D는 실제 선정·설계·운전 판단을 평가한다. 적용 조건, worst-case, 검증 절차, 비용, 안전, 유지보수, 기존 설비 영향, 실행 가능성과 trade-off를 본다.
   C의 Fact 부족만을 이유로 D를 다시 감점하지 않는다. C 오류가 D의 현장 결론을 무효화하면 보조 영향으로 기록하되 같은 오류의 전체 감점을 반복하지 않는다.
5. E는 배경→요구→Fact→판단→결론의 논리 연결, 우선순위, 주장 일관성과 면접 방어 가능성을 평가한다.
   C의 Fact 누락 또는 D의 현장 깊이 부족을 그대로 반복 감점하지 않는다. E 감점은 연결 단절, 모순, 근거 없는 결론처럼 E 자체 결함이 있을 때만 적용한다.
6. 동일한 기술 issue는 하나의 primary_owner_layer에만 점수 감점을 귀속한다. 다른 계층은 secondary_context_layers로만 기록하며 deduction_applied=false로 둔다.
7. 점수 목표, 특정 Topic, 특정 세션, 특정 답안 문자열에 따른 보정을 금지한다.

최종 JSON root에 다음 진단 필드를 포함하라.

"layer_issue_ownership": [
  {
    "issue_id": "일반화 가능한 snake_case 식별자",
    "severity": "missing | partial | incorrect | fatal",
    "primary_owner_layer": "A | B | C | D | E",
    "secondary_context_layers": [],
    "deduction_applied_layers": ["대표 감점 계층 하나"],
    "reason": "대표 계층과 보조 영향의 구분"
  }
]

layer_issue_ownership는 별도 점수체계가 아니라 같은 issue의 중복 감점을 방지하는 진단 계약이다.
""".strip()


def build_gemini_grading_prompt(*args, **kwargs):
    base_prompt = _PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1(*args, **kwargs)
    marker = "[PLAN_B_GENERAL_LAYER_OWNERSHIP_V1]"
    if marker in base_prompt:
        return base_prompt
    return base_prompt + "\n\n" + _plan_b_general_layer_ownership_prompt_v1()
