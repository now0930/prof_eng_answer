# Docker Compose Usage

## 1. 목적

이 문서는 `prof_eng_answer` Telegram 채점 Bot의 Docker Compose 운영 방식을 설명한다.

현재 운영 기준은 다음과 같다.

| 항목 | 기준 |
|---|---|
| Compose 위치 | `~/hermes/docker-compose.yml` |
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| Bot 전용 컨테이너 | `prof_eng_answer_bot` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 nohup 실행 | 사용하지 않음 |
| 중복 polling 방지 | 필수 |

## 2. 운영 구조

운영은 상위 `~/hermes` 디렉터리에서 수행한다.

    cd ~/hermes
    docker compose ps

주요 컨테이너:

| 컨테이너 | 역할 |
|---|---|
| `hermes_agent` | Hermes agent 기본 컨테이너 |
| `prof_eng_answer_bot` | 기술사 답안 채점 Telegram Bot 전용 컨테이너 |

`prof_eng_answer_bot`이 Telegram Bot의 유일한 실행 주체여야 한다.

`hermes_agent` 내부에서 `nohup python bot.py`를 수동 실행하지 않는다.

## 3. 시작

전체 compose 시작:

    cd ~/hermes
    docker compose up -d
    docker compose ps

Bot 컨테이너만 시작:

    cd ~/hermes
    docker compose up -d prof-eng-answer-bot

## 4. 재시작

일반 재시작:

    cd ~/hermes
    docker compose restart prof-eng-answer-bot

완전 재기동:

    cd ~/hermes
    docker compose stop prof-eng-answer-bot
    sleep 3
    docker compose up -d prof-eng-answer-bot

코드 import 상태가 꼬였거나, `bot.py` 실행 흐름을 수정한 뒤에는 완전 재기동을 권장한다.

## 5. 상태 확인

    cd ~/hermes
    docker compose ps prof-eng-answer-bot

로그 확인:

    docker logs --tail=120 prof_eng_answer_bot

실시간 로그:

    docker logs -f --tail=80 prof_eng_answer_bot

## 6. 컨테이너 내부 코드 위치

일반 운영 경로:

    /workspace/prof_eng_answer

확인 명령:

    docker exec prof_eng_answer_bot bash -lc '
    cd /workspace/prof_eng_answer 2>/dev/null || cd /app 2>/dev/null || exit 1
    pwd
    ls -la
    '

## 7. Git 최신 상태 확인

로컬 repository 기준:

    cd ~/hermes/workspace/prof_eng_answer

    git fetch origin main

    echo "[HEAD]"
    git rev-parse --short HEAD

    echo "[origin/main]"
    git rev-parse --short origin/main

    git status --short
    git log --oneline --decorate -5

정상 기준:

    HEAD == origin/main
    git status --short 출력 없음

컨테이너 내부 확인:

    docker exec prof_eng_answer_bot bash -lc '
    cd /workspace/prof_eng_answer 2>/dev/null || cd /app 2>/dev/null || exit 1
    git log --oneline --decorate -5 2>/dev/null || true
    git status --short 2>/dev/null || true
    '

## 8. 중복 polling 확인

Telegram Bot은 동일 token으로 여러 프로세스가 polling하면 응답 충돌이 발생할 수 있다.

Host와 컨테이너 전체 확인:

    cd ~/hermes

    echo "[containers]"
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Command}}' \
      | grep -E 'prof|hermes|bot|agent' || true

    echo
    echo "[host python bot processes]"
    ps -ef \
      | grep -E 'prof_eng|run_prof_eng_bot|bot.py|telegram' \
      | grep -v grep || true

    echo
    echo "[prof_eng_answer_bot processes]"
    docker exec prof_eng_answer_bot bash -lc '
    ps -ef | grep -E "python|bot.py|run_prof_eng_bot|telegram" | grep -v grep || true
    '

    echo
    echo "[hermes_agent processes]"
    docker exec hermes_agent bash -lc '
    ps -ef | grep -E "prof_eng|bot.py|run_prof_eng_bot|telegram" | grep -v grep || true
    ' 2>/dev/null || true

정상 기준:

    prof_eng_answer_bot 내부에 python -u bot.py 1개
    hermes_agent 내부에는 prof_eng_answer bot.py 없음
    host에서 보이는 python -u bot.py는 컨테이너 프로세스일 수 있음

주의사항:

- `hermes_agent` 내부에서 `nohup python bot.py &`를 실행하지 않는다.
- 같은 Telegram token을 쓰는 다른 Bot 컨테이너가 있는지 확인한다.
- `telegram_bot_prod` 같은 별도 컨테이너가 있으면 같은 token 사용 여부를 점검한다.

## 9. 실행 명령 확인

컨테이너가 어떤 명령으로 실행되는지 확인한다.

    cd ~/hermes

    docker inspect prof_eng_answer_bot \
      --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'

    docker compose config | sed -n '/prof-eng-answer-bot:/,/^[^ ]/p'

정상 기준:

    prof_eng_answer_bot이 bot.py를 실행
    수동 nohup 실행 없음

## 10. bot.py 실행 흐름 주의

운영 시 `bot.py`는 다음 방식으로 실행된다.

    python -u bot.py

그리고 파일 내부에서 다음 흐름으로 진입한다.

    if __name__ == "__main__":
        main()

`main()` 내부에는 polling loop가 있다.

    while True:
        ...

따라서 `if __name__ == "__main__": main()` 아래쪽에 append한 wrapper 코드는 실행되지 않는다.

잘못된 방식:

    if __name__ == "__main__":
        main()

    # 이 아래 wrapper는 실행형 bot.py에서는 실행되지 않음
    def format_result(...):
        ...

올바른 방식:

    main()보다 위에 함수 정의
    또는 send_message() 경계에서 최종 출력 정리

현재 legacy `GENERAL(일반 설명형)` 문구 정리는 `send_message()` 내부의 send boundary cleanup에서 처리한다.

## 11. send boundary cleanup 확인

현재 Bot은 Telegram 송신 직전에 legacy 문구를 정리한다.

확인 명령:

    cd ~/hermes

    docker exec prof_eng_answer_bot bash -lc '
    cd /workspace/prof_eng_answer 2>/dev/null || cd /app 2>/dev/null || exit 1

    grep -nE "send boundary legacy GENERAL|final Telegram legacy GENERAL cleanup wrapper|_cleanup_legacy_general_text_for_send|def send_message|if __name__|main\(|while True" bot.py | sed -n "1,220p"
    '

정상 기준:

    send boundary legacy GENERAL cleanup v1 있음
    _cleanup_legacy_general_text_for_send 있음
    def send_message 내부에서 cleanup 호출함
    final Telegram legacy GENERAL cleanup wrapper 없음

예상 형태:

    110:# === send boundary legacy GENERAL cleanup v1 ===
    111:def _cleanup_legacy_general_text_for_send(text):
    150:def send_message(chat_id, text):
    151:    text = _cleanup_legacy_general_text_for_send(text)
    886:def main():
    896:    while True:
    924:if __name__ == "__main__":
    925:    main()

## 12. 환경변수

환경변수는 상위 `~/hermes/.env`에서 관리한다.

    ~/hermes/.env

주요 변수:

| 변수 | 의미 |
|---|---|
| `TELEGRAM_BOT_TOKEN` 또는 `BOT_TOKEN` | Telegram Bot token |
| `OLLAMA_URL` | Ollama API URL |
| `OLLAMA_MODEL` | 로컬 보조 모델 |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Gemini 모델명 |
| `CLOVA_API_KEY` | Naver CLOVA API key |
| `CLOVA_MODEL` | CLOVA 모델명 |
| `LLM_PROVIDER` | `auto`, `gemini`, `clova` |
| `LLM_PRIMARY` | 기본 provider |
| `LLM_FALLBACK` | fallback provider |
| `DIFFICULTY_CEILING_MODE` | `warn`, `strict`, `off` |
| `QUESTION_TYPE_COVERAGE_SCORE_MODE` | `warn`, `strict`, `off` |

주의:

    .env
    API key
    Telegram token

위 항목은 Git에 커밋하지 않는다.

## 13. 대표 smoke test

Telegram에서 다음을 보낸다.

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

정상 확인:

- 채점 완료 메시지가 온다.
- `[Question Type Coverage]`가 출력된다.
- 문제 유형 lens가 `적용·평가형(IMPLEMENTATION_EVALUATION)`로 표시된다.
- `[보완 방향]`에 `C항목 보완: 일반 설명형 유형에서는 ...` 문구가 없어야 한다.
- 대신 `C항목 보완: 문제 유형 lens에 맞는 핵심 fact...` 문구가 나와야 한다.

## 14. 코드 검증

Bot 관련 Python 문법 확인:

    cd ~/hermes/workspace/prof_eng_answer

    python3 -m py_compile \
      bot.py \
      grading_agents.py \
      gemini_grader.py \
      clova_grader.py \
      difficulty_strategy.py \
      difficulty_output_adapter.py \
      difficulty_score_ceiling.py \
      question_type_taxonomy.py \
      question_type_coverage_adapter.py \
      question_type_coverage_score_adjuster.py \
      semantic_question_type_prompt.py \
      semantic_question_type_postprocess.py \
      scripts/validate_model_answer_bank.py

Rubric 전체 검증:

    python3 scripts/rubric_manager.py validate-all

## 15. 문서 변경 후 반영 절차

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

    git add docs/docker_compose_usage.md
    git commit -m "Update Docker Compose operation documentation"
    git push origin main

문서 변경 후 Bot 컨테이너 재시작은 필수는 아니다.
단, 운영 문서와 실제 컨테이너 상태가 맞는지 smoke test는 수행하는 것이 좋다.
