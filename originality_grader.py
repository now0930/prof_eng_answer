import json
import os
import re
import urllib.error
import urllib.request


def _extract_json(text: str) -> dict:
    text = str(text or "").strip()

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
        ).strip()
        text = re.sub(
            r"```$",
            "",
            text,
        ).strip()

    def parse_object(candidate: str):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed

    parsed = parse_object(text)
    if parsed is not None:
        return parsed

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        parsed = parse_object(
            text[start : end + 1]
        )

        if parsed is not None:
            return parsed

    raise ValueError(
        "JSON object not found in Gemini response"
    )


def build_originality_prompt(question_text, answer_text, layer_scores=None, volume=None, fact_eval=None, connection_eval=None):
    layer_scores = layer_scores or []
    volume = volume or {}
    fact_eval = fact_eval or {}
    connection_eval = connection_eval or {}

    return f"""
너는 산업계측제어기술사 답안을 평가하는 채점위원이다.

이번 평가는 '독창성'이라는 이름을 사용하지만, 창작적 표현이나 특이한 문장을 평가하지 않는다.
여기서 독창성은 '기술사적 판단성', 즉 정확한 fact를 바탕으로 문제를 실제 설비 조건으로 재해석하고,
제약 조건, 대안 비교, 적용 우선순위, 검증 방법을 제시하는 능력이다.

중요한 원칙:
- Fact 없는 독창성은 인정하지 않는다.
- 기술적으로 틀린 주장은 독창성이 아니라 오류다.
- 유행어, 추상적 표현, 과장된 표현은 가점하지 않는다.
- 현장 조건, 비용, 기존 설비 영향, 운전 리스크, 적용 순서, 검증 기준이 있을 때만 가점한다.
- 답안이 짧으면 높은 독창성 점수를 주지 않는다.

평가 항목:
O1. 문제 재해석 능력
- 문제를 단순 정의로 끝내지 않고 실제 설계·운전·유지보수 문제로 확장했는가

O2. 현장 조건 반영
- 기존 설비, 정상/최소/최대 운전 조건, 설치 조건, 유체 조건, 운전 데이터를 고려했는가

O3. 대안 비교와 trade-off
- 여러 대안을 비교하고 비용, 리스크, 공기, 효과 차이를 고려했는가

O4. 적용 우선순위 제시
- 진단 → 조정 → 부분 변경 → 설비 변경 등 현실적인 적용 순서를 제시했는가

O5. 검증 가능성
- 운전 trend, 계측값, 시험, 점검 항목, 판정 기준 등 확인 가능한 검증 방법을 제시했는가

점수 기준:
0.0 = 없음
0.3 = 키워드만 있음
0.5 = 일반론 수준
0.7 = 문제와 연결된 판단 있음
0.9 = 현장 조건과 trade-off가 구체적
1.0 = 대안, 제약, 검증, 우선순위가 모두 명확

점수 계산 규칙:
- average_level은 O1~O5 level의 산술평균이다.
- raw_originality_score는 average_level × 2.0이다.
- raw_originality_score의 허용 범위는 0.0~2.0이다.
- 총평과 anchor level이 부정적인데 높은 raw 점수를 부여하지 마라.

반드시 JSON만 출력하라. 설명문, markdown, 코드블록은 출력하지 마라.

JSON schema:
{{
  "version": "originality_evaluator_v1",
  "confidence": "low|medium|high",
  "overall_comment": "독창성 평가 총평",
  "anchors": [
    {{
      "id": "O1",
      "name": "문제 재해석 능력",
      "level": 0.0,
      "reason": "평가 이유",
      "evidence": ["답안에서 확인한 근거 문장 또는 표현"]
    }},
    {{
      "id": "O2",
      "name": "현장 조건 반영",
      "level": 0.0,
      "reason": "평가 이유",
      "evidence": []
    }},
    {{
      "id": "O3",
      "name": "대안 비교와 trade-off",
      "level": 0.0,
      "reason": "평가 이유",
      "evidence": []
    }},
    {{
      "id": "O4",
      "name": "적용 우선순위 제시",
      "level": 0.0,
      "reason": "평가 이유",
      "evidence": []
    }},
    {{
      "id": "O5",
      "name": "검증 가능성",
      "level": 0.0,
      "reason": "평가 이유",
      "evidence": []
    }}
  ],
  "average_level": 0.0,
  "raw_originality_score": 0.0,
  "technical_error_risk": false,
  "technical_error_reason": "",
  "false_originality_risk": false,
  "false_originality_reason": "",
  "improvement_advice": [
    "독창성 향상을 위한 구체적 조언"
  ]
}}

문제:
{question_text}

답안:
{answer_text}

현재 A/B/C/D/E 점수 참고:
{json.dumps(layer_scores, ensure_ascii=False, indent=2)}

답안 분량 평가 참고:
{json.dumps(volume, ensure_ascii=False, indent=2)}

Fact Anchor 평가 참고:
{json.dumps(fact_eval, ensure_ascii=False, indent=2)}

Connection 평가 참고:
{json.dumps(connection_eval, ensure_ascii=False, indent=2)}
""".strip()


def gemini_originality_evaluate(question_text, answer_text, layer_scores=None, volume=None, fact_eval=None, connection_eval=None):
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    )

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        return {
            "ok": False,
            "error": "GEMINI_API_KEY is missing",
            "model": model,
            "raw_text": "",
            "parsed": None
        }

    prompt = build_originality_prompt(
        question_text=question_text,
        answer_text=answer_text,
        layer_scores=layer_scores,
        volume=volume,
        fact_eval=fact_eval,
        connection_eval=connection_eval,
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 4096
        }
    }

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
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        raw_text = ""
        candidates = data.get("candidates") or []
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            raw_text = "".join(p.get("text", "") for p in parts)

        parsed = _extract_json(raw_text)

        return {
            "ok": True,
            "error": "",
            "model": model,
            "raw_text": raw_text,
            "parsed": parsed
        }

    except urllib.error.HTTPError as e:
        body = ""
        body_error = ""

        try:
            body = e.read().decode("utf-8")
        except Exception as read_error:
            body_error = repr(read_error)

        error_text = f"HTTPError {e.code}: {body[:1000]}"

        if body_error:
            error_text += (
                " (response body unavailable: "
                f"{body_error})"
            )

        return {
            "ok": False,
            "error": error_text,
            "model": model,
            "raw_text": "",
            "parsed": None
        }

    except Exception as e:
        return {
            "ok": False,
            "error": repr(e),
            "model": model,
            "raw_text": "",
            "parsed": None
        }
