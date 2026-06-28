# 기술사 답안 채점 Telegram Bot

산업계측제어기술사 답안을 Telegram으로 입력받아 기술사 답안지 기준에 맞춰 채점하는 프로젝트이다.

현재 채점 방식은 단순 키워드 매칭이 아니라 다음 요소를 결합한다.

- A/B/C/D/E 25점 채점 구조
- Fact Anchor 기반 핵심 개념 평가
- Question Type Lens 기반 유형별 C항목 평가
- Model Answer Bank 기반 답안 구조·깊이 참조
- 교수·기술사·기업 임원 관점의 3인 layer 가중 합성
- Gemini 또는 Naver CLOVA 기반 LLM 의미 평가
- Python rule 기반 volume cap, fallback, 후처리, Telegram 출력

## 1. 핵심 구조

25점 문항은 다음 5개 항목으로 평가한다.

| 항목 | 설명 | 배점 |
|---|---|---:|
| A | 배경과 문제 진입 | 4 |
| B | 문제 요구 파악 | 5 |
| C | 유형별 Fact 기반 내용 설명 | 8 |
| D | 현장 적용·설계 판단·제언 | 6 |
| E | 연결성·면접 방어 가능성 | 2 |
| 합계 |  | 25 |

기준선은 다음과 같다.

- 공식 합격선: 15점
- 실전 목표선: 17.5점
- 고득점 기준: 20점

상세 채점 구조는 `docs/grading_architecture.md`를 참고한다.

## 2. LLM Provider

의미 평가 LLM Provider는 Telegram 명령으로 선택할 수 있다.

    /provider
    /provider auto
    /provider gemini
    /provider clova
    /provider reset

Provider 모드는 다음과 같다.

| 모드 | 의미 |
|---|---|
| auto | Gemini 우선 사용, 실패 시 CLOVA fallback |
| gemini | Gemini만 사용 |
| clova | Naver CLOVA만 사용 |

상세 설정은 `docs/llm_provider.md`를 참고한다.

## 3. Telegram 사용법

짧은 답안 채점 예시는 다음과 같다.

    /grade
    문제: Cv(Valve Flow Coefficient)를 설명하시오.
    배점: 25
    답안:
    Cv는 밸브의 유량계수로 밸브를 통과할 수 있는 유량의 크기를 나타낸다. Cv가 크면 유량이 많이 흐르고, 밸브 선정에 사용된다.

새 세션 시작:

    /new

현재 상태 확인:

    /status

Rubric 정보 확인:

    /rubric

Provider 확인:

    /provider

## 4. 주요 문서

| 문서 | 내용 |
|---|---|
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조와 phase 흐름 |
| `docs/llm_provider.md` | Gemini + Naver CLOVA provider 설정 |
| `docs/rubric_authoring_guide.md` | 문제유형, Fact Anchor, Model Answer 작성 방법 |
| `docs/docker_compose_usage.md` | Docker Compose 실행 예시 |
| `docs/migration_plan.md` | 구조 변경 또는 마이그레이션 계획 |
| `docs/structure_review.md` | 과거 구조 검토 문서. 현재는 deprecated |

## 5. 주요 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram Bot 입출력 처리 |
| `grading_agents.py` | 채점 파이프라인 |
| `llm_provider_router.py` | Gemini, CLOVA, auto fallback 분기 |
| `gemini_grader.py` | Gemini 의미 평가 호출 |
| `clova_grader.py` | Naver CLOVA 의미 평가 호출 |
| `llm_provider_settings.py` | 채팅방별 provider 설정 저장 |
| `question_type_router.py` | 문제 유형 판정 |
| `model_answer_router.py` | 모범 답안 Bank 참조 |
| `rubric_registry.py` | Rubric JSON 로드·검증·관리 |
| `scripts/rubric_manager.py` | Rubric 관리 CLI |

## 6. 환경변수

실제 운영 환경에서는 `.env`에 API key와 token을 넣는다.

    GEMINI_API_KEY=
    GEMINI_MODEL=gemini-3.1-flash-lite

    CLOVA_API_KEY=
    CLOVA_MODEL=HCX-003
    CLOVA_HOST=https://clovastudio.stream.ntruss.com
    CLOVA_ENDPOINT=/v1/chat-completions/HCX-003

    TELEGRAM_TOKEN=
    OLLAMA_URL=http://ollama:11434
    OLLAMA_MODEL=gemma4:e4b

`.env`는 Git에 커밋하지 않는다.

## 7. 실행

Bot 재시작 예시는 다음과 같다.

    cd ~/hermes/workspace/prof_eng_answer

    docker exec hermes_agent bash -lc 'pkill -f "python.*bot.py" || true'

    mkdir -p logs
    : > logs/prof_eng_answer.log

    docker exec -d hermes_agent bash -lc '
    cd /workspace/prof_eng_answer &&
    mkdir -p logs &&
    nohup python bot.py >> logs/prof_eng_answer.log 2>&1 &
    '

로그 확인:

    tail -n 120 logs/prof_eng_answer.log

## 8. 검증

호스트 검증:

    python3 -m py_compile bot.py grading_agents.py gemini_grader.py clova_grader.py llm_provider_router.py llm_provider_settings.py
    python3 scripts/rubric_manager.py validate-all

컨테이너 검증:

    docker exec -it hermes_agent bash -lc '
    cd /workspace/prof_eng_answer &&
    python -m py_compile bot.py grading_agents.py gemini_grader.py clova_grader.py llm_provider_router.py llm_provider_settings.py &&
    python scripts/rubric_manager.py validate-all
    '

## 9. Git에 커밋하지 않는 항목

다음 항목은 Git에 커밋하지 않는다.

- `.env`
- API key
- Telegram token
- `logs/`
- `data/sessions/`
- `data/user_settings/`
- `backups/`
- `__pycache__/`
- 사용자 답안 이미지
- 사용자 답안 텍스트
