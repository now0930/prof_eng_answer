# LLM Provider

이 문서는 Gemini와 Naver CLOVA provider 사용 방식을 설명한다.

---

## 1. 지원 Provider

| Provider | 역할 |
|---|---|
| `gemini` | Gemini semantic grader |
| `clova` | Naver CLOVA semantic grader |
| `auto` | Gemini 우선, 실패 시 CLOVA fallback |

Telegram 명령:

```text
/provider
/provider auto
/provider gemini
/provider clova
/provider reset
```

---

## 2. 사용자별 설정

Provider 선택은 사용자별로 저장된다.

```text
data/user_settings/llm_provider_settings.json
```

기본값은 `auto`이다.

---

## 3. 환경변수

운영 환경변수는 상위 `.env`에서 관리한다.

```text
~/hermes/.env
```

주요 변수:

| 변수 | 설명 |
|---|---|
| `LLM_PROVIDER` | 기본 provider |
| `LLM_PRIMARY` | auto 모드 primary |
| `LLM_FALLBACK` | auto 모드 fallback |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Gemini model |
| `CLOVA_API_KEY` | CLOVA Studio API key |
| `CLOVA_MODEL` | CLOVA model |
| `CLOVA_HOST` | CLOVA host |
| `CLOVA_ENDPOINT` | CLOVA endpoint |

`.env`는 Git에 올리지 않는다.

---

## 4. Auto Mode

`auto` 모드는 다음 순서로 동작한다.

```text
1. Gemini semantic grader 시도
2. Gemini 실패 시 CLOVA fallback
3. 결과 JSON에 llm_provider 기록
```

로그 예:

```text
[agent] Gemini semantic grader applied.
```

CLOVA 사용 시 session JSON 내부에 다음과 같은 값이 기록된다.

```json
{
  "llm_provider": "clova",
  "llm_model": "HCX-003"
}
```

---

## 5. 주의사항

- API key는 로그나 Git에 출력하지 않는다.
- `.env`는 commit하지 않는다.
- Provider 실패는 전체 채점 실패가 아닐 수 있다.
- 파일명이 `gemini_semantic_evaluation.json`이어도 내부 `llm_provider`가 실제 provider 기준이다.
---

## Question Type Coverage

Gemini와 CLOVA semantic grader는 A/B/C/D/E 평가와 함께 `question_type_coverage`를 출력하도록 요청받는다.

`question_type_coverage`는 다음을 평가한다.

- question_type v2 대분류
- sub_criteria 충족 여부
- C항목 Fact 설명의 부족 관점
- D항목 현장 판단의 부족 관점
- 보수적으로 볼 점수 항목에 대한 scoring hint

이 결과는 기본적으로 점수를 직접 바꾸지 않는다.  
`QUESTION_TYPE_COVERAGE_SCORE_MODE=warn`에서는 보정 후보만 표시한다.

실제 약한 보정을 적용하려면 다음을 사용한다.

```env
QUESTION_TYPE_COVERAGE_SCORE_MODE=strict
```

strict 모드에서도 최대 보정은 0.75점으로 제한한다.

