# LLM Provider

## 1. 목적

이 문서는 `prof_eng_answer`의 LLM provider 구조를 설명한다.

현재 Bot은 Telegram으로 받은 답안을 semantic grader에 전달하고, 그 결과를 Python rule 기반 채점 파이프라인과 결합한다.

운영 기준은 다음과 같다.

| 항목 | 기준 |
|---|---|
| 기본 provider 모드 | `auto` |
| 우선 provider | `gemini` |
| fallback provider | `clova` |
| 로컬 보조 모델 | Ollama model |
| provider 변경 방법 | Telegram `/provider` 명령 |

## 2. Provider 종류

| provider | 역할 |
|---|---|
| `gemini` | 기본 semantic grader |
| `clova` | Naver CLOVA Studio 기반 fallback semantic grader |
| `auto` | Gemini 우선, 실패 시 CLOVA fallback |

## 3. 권장 운영 설정

운영 환경에서는 다음 조합을 권장한다.

    LLM_PROVIDER=auto
    LLM_PRIMARY=gemini
    LLM_FALLBACK=clova

의미는 다음과 같다.

| 변수 | 의미 |
|---|---|
| `LLM_PROVIDER=auto` | provider 자동 선택 |
| `LLM_PRIMARY=gemini` | 우선 Gemini 사용 |
| `LLM_FALLBACK=clova` | Gemini 실패 시 CLOVA 사용 |

## 4. 환경변수

환경변수는 상위 `.env`에서 관리한다.

    ~/hermes/.env

주요 변수:

| 변수 | 의미 |
|---|---|
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Gemini 모델명 |
| `CLOVA_API_KEY` | Naver CLOVA API key |
| `CLOVA_MODEL` | CLOVA 모델명 |
| `LLM_PROVIDER` | `auto`, `gemini`, `clova` |
| `LLM_PRIMARY` | 기본 provider |
| `LLM_FALLBACK` | fallback provider |
| `OLLAMA_URL` | Ollama API URL |
| `OLLAMA_MODEL` | 로컬 보조 분석 모델 |

주의:

- API key 값을 문서나 로그에 직접 남기지 않는다.
- `.env` 파일은 Git에 커밋하지 않는다.
- Telegram token도 문서에 기록하지 않는다.

## 5. Telegram provider 명령

현재 provider 확인:

    /provider

provider 자동 모드:

    /provider auto

Gemini만 사용:

    /provider gemini

CLOVA만 사용:

    /provider clova

기본값으로 복귀:

    /provider reset

## 6. auto 모드 동작

`auto` 모드는 다음 순서로 동작한다.

    1. LLM_PRIMARY provider로 semantic grading 시도
    2. 성공하면 해당 결과 사용
    3. 실패하면 LLM_FALLBACK provider로 재시도
    4. fallback도 실패하면 Python fallback 또는 오류 메시지 처리

운영 권장값은 다음이다.

    LLM_PRIMARY=gemini
    LLM_FALLBACK=clova

## 7. Semantic grader 역할

Semantic grader는 다음 정보를 평가한다.

- A/B/C/D/E 항목별 의미 평가
- 답안의 기술적 깊이
- 누락된 핵심 Fact
- 현장 적용성
- 기술사적 판단성
- Question Type v2 coverage
- 보완 방향

Semantic grader 결과는 그대로 최종 점수가 되지 않는다.
Python rule이 다음을 추가로 처리한다.

- 짧은 답안 cap
- 점수 범위 정규화
- Difficulty ceiling 후보
- Question Type coverage 보정 후보
- fallback coverage 처리
- Telegram 출력 정리

## 8. Question Type coverage contract

현재 semantic grader는 가능하면 `question_type_coverage`를 반환해야 한다.

핵심 요구:

    question_type
    name_ko
    coverage_source
    sub_criteria_coverage
    c_fact_focus_coverage
    d_field_judgement_focus_coverage
    missing_sub_criteria
    overall_coverage
    scoring_hint

정상 semantic coverage는 다음 값을 가진다.

    coverage_source: semantic_grader

semantic grader가 coverage를 반환하지 못하면 fallback coverage를 생성한다.

fallback coverage는 다음 특징을 가진다.

    coverage_source: fallback_missing_semantic_field 또는 fallback_missing_grade_field
    overall_coverage: unknown
    점수 보정에 사용하지 않음

## 9. provider 장애 대응

Gemini 장애가 의심될 때:

    /provider clova

CLOVA 장애가 의심될 때:

    /provider gemini

provider 설정을 기본으로 되돌릴 때:

    /provider reset

컨테이너 로그 확인:

    cd ~/hermes
    docker logs --tail=120 prof_eng_answer_bot

## 10. 운영 확인 smoke test

Telegram에서 다음을 보낸다.

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

정상 확인:

- 채점 엔진에 Gemini 또는 CLOVA semantic grader가 표시된다.
- 보조 모델이 표시된다.
- 채점 완료 메시지가 온다.
- `[Question Type Coverage]`가 출력된다.
- provider 장애 시 fallback 또는 오류 메시지가 로그에 남는다.

## 11. 관련 파일

| 파일 | 역할 |
|---|---|
| `gemini_grader.py` | Gemini semantic grader |
| `clova_grader.py` | CLOVA semantic grader |
| `grading_agents.py` | provider 선택과 채점 pipeline |
| `semantic_question_type_prompt.py` | Question Type coverage prompt contract |
| `semantic_question_type_postprocess.py` | coverage fallback/postprocess |
| `bot.py` | Telegram 명령 처리와 provider 명령 |
