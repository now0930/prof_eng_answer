# LLM Provider 운영: Gemini + Naver CLOVA

이 문서는 기술사 답안 채점 Bot에서 Gemini와 Naver CLOVA를 함께 사용하는 방법을 정리한다.

기존 A/B/C/D/E 25점 채점 구조와 Python scoring rule은 유지한다. Gemini 또는 CLOVA는 답안 의미 평가를 보조하는 Provider로 사용한다.

## 1. 구조

    Telegram Bot
      ↓
    grading_agents.py
      ↓
    llm_provider_router.py
      ├─ gemini_grader.py
      └─ clova_grader.py

주요 파일 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| llm_provider_settings.py | 채팅방별 provider 설정 저장 및 조회 |
| llm_provider_router.py | Gemini, CLOVA, auto fallback 분기 |
| gemini_grader.py | Gemini 의미 평가 호출 |
| clova_grader.py | Naver CLOVA 의미 평가 호출 |
| bot.py | Telegram /provider 명령 처리 |
| grading_agents.py | 실제 채점 중 LLM router 호출 |

## 2. Provider 모드

| 모드 | 의미 |
|---|---|
| auto | Gemini 우선 사용, 실패 시 CLOVA fallback |
| gemini | Gemini만 사용 |
| clova | Naver CLOVA만 사용 |

Telegram에서 다음 명령으로 provider를 확인하거나 변경한다.

    /provider
    /provider auto
    /provider gemini
    /provider clova
    /provider reset

예시:

    /provider clova

응답 예:

    현재 채점 LLM Provider: Naver CLOVA

채팅방별 provider 설정은 다음 파일에 저장된다.

    data/user_settings/llm_provider_settings.json

이 파일은 실행 중 생성되는 사용자 설정 파일이므로 Git에 커밋하지 않는다.

## 3. 환경변수

.env에는 실제 API key를 넣고, .env.example에는 변수명과 예시만 남긴다.

    # LLM provider
    LLM_PROVIDER=auto
    LLM_PRIMARY=gemini
    LLM_FALLBACK=clova

    # Gemini
    GEMINI_API_KEY=
    GEMINI_MODEL=gemini-3.1-flash-lite

    # Naver CLOVA Studio
    CLOVA_API_KEY=
    CLOVA_APIGW_API_KEY=
    CLOVA_REQUEST_ID=prof-eng-answer-local
    CLOVA_MODEL=HCX-003
    CLOVA_HOST=https://clovastudio.stream.ntruss.com
    CLOVA_ENDPOINT=/v1/chat-completions/HCX-003

CLOVA_API_KEY에는 CLOVA Studio에서 발급받은 테스트 API 키 또는 서비스 API 키를 입력한다.

현재 구현은 다음 인증 방식을 사용한다.

    Authorization: Bearer {CLOVA_API_KEY}

CLOVA_APIGW_API_KEY는 Legacy 방식이 필요한 경우를 위해 남겨둔 항목이며, 현재 기본 구현에서는 비워두어도 된다.

## 4. CLOVA Compact Prompt

CLOVA는 긴 입력에 민감할 수 있으므로 clova_grader.py에서 Gemini용 긴 prompt를 그대로 사용하지 않고 compact prompt로 축약한다.

관련 환경변수는 다음과 같다.

    CLOVA_MAX_PROMPT_CHARS=16000
    CLOVA_MAX_TOKENS=2048
    CLOVA_TIMEOUT=120
    CLOVA_RETRIES=2

## 5. 실행 확인

Provider 확인:

    /provider

CLOVA 강제:

    /provider clova

짧은 답안 채점 테스트:

    /grade
    문제: Cv(Valve Flow Coefficient)를 설명하시오.
    배점: 25
    답안:
    Cv는 밸브의 유량계수로 밸브를 통과할 수 있는 유량의 크기를 나타낸다. Cv가 크면 유량이 많이 흐르고, 밸브 선정에 사용된다.

로그 확인:

    tail -n 200 logs/prof_eng_answer.log | grep -Ei "LLM|Gemini|CLOVA|semantic|provider|failed|error|fallback|applied" || true

세션 결과에서 실제 provider 확인:

    latest=$(ls -td data/sessions/* | head -1)
    grep -Rni "llm_provider\|llm_model\|fallback_from" "$latest" || true

정상 예:

    "llm_provider": "clova"
    "llm_model": "HCX-003"

주의: 기존 호환성 때문에 세션 파일명이 gemini_semantic_evaluation.json으로 남아 있을 수 있다. 파일명은 legacy 이름이며, 실제 사용 provider는 파일 내부의 llm_provider 값으로 판단한다.

## 6. 현재 구현 상태

완료된 항목은 다음과 같다.

- /provider 명령 추가
- auto, gemini, clova, reset 선택 가능
- 채팅방별 provider 설정 저장
- Gemini semantic grader 유지
- CLOVA semantic grader 추가
- LLM provider router 추가
- auto 모드에서 Gemini 우선, 실패 시 CLOVA fallback
- CLOVA compact prompt 적용
- 실제 채점 결과에 llm_provider, llm_model 기록

주의사항은 다음과 같다.

- .env는 Git에 커밋하지 않는다.
- API key와 Telegram token은 README, 코드, 로그에 직접 남기지 않는다.
- logs/, data/sessions/, data/user_settings/, backups/는 Git에 커밋하지 않는다.
- 기존 session 호환성을 위해 gemini_semantic_evaluation.json 파일명은 당분간 유지한다.
