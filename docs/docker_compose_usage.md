# Docker Compose Usage

이 문서는 `prof_eng_answer` Telegram Bot의 Docker Compose 운영 방식만 설명한다. 장애 대응 전체 절차는 `operation_runbook.md`를 우선한다.

## 1. 운영 기준

| 항목 | 기준 |
|---|---|
| Compose 위치 | `~/hermes` |
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| 컨테이너 내부 경로 | `/workspace/prof_eng_answer` |
| Bot 컨테이너 | `prof_eng_answer_bot` |
| Compose 서비스명 | 보통 `prof-eng-answer-bot` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 nohup 실행 | 사용하지 않음 |

## 2. 상태 확인

```bash
cd ~/hermes

docker compose ps
docker compose ps prof-eng-answer-bot
docker logs --tail=120 prof_eng_answer_bot
```

## 3. 시작과 재시작

전체 compose 시작:

```bash
cd ~/hermes
docker compose up -d
docker compose ps
```

Bot만 시작:

```bash
cd ~/hermes
docker compose up -d prof-eng-answer-bot
```

일반 재시작:

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
```

완전 재기동:

```bash
cd ~/hermes
docker compose stop prof-eng-answer-bot
sleep 3
docker compose up -d prof-eng-answer-bot
```

`bot.py`, formatter, provider, `send_message()` boundary를 수정한 뒤에는 완전 재기동을 권장한다.

## 4. 로그 확인

```bash
docker logs --tail=120 prof_eng_answer_bot
docker logs -f --tail=80 prof_eng_answer_bot
```

정상 로그 예:

```text
prof_eng_answer_bot service started
cwd=/workspace/prof_eng_answer
bot started. ollama=http://ollama:11434, model=...
```

채점 중 정상 로그 예:

```text
[agent] phase2 wrapper entered.
[agent] Gemini semantic grader applied.
[agent] phase2 layered scoring applied: ...
[agent] phase21 final difficulty ceiling evaluated: ...
```

## 5. 컨테이너 내부 확인

```bash
cd ~/hermes

docker exec prof_eng_answer_bot bash -lc '
  cd /workspace/prof_eng_answer 2>/dev/null || cd /app 2>/dev/null || exit 1
  pwd
  git log --oneline --decorate -5 2>/dev/null || true
  git status --short 2>/dev/null || true
'
```

## 6. 실행 명령 확인

```bash
cd ~/hermes

docker inspect prof_eng_answer_bot \
  --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'

docker compose config | sed -n '/prof-eng-answer-bot:/,/^[^ ]/p'
```

정상 기준:

- `prof_eng_answer_bot`이 `python -u bot.py` 또는 동등한 명령으로 실행
- `hermes_agent` 내부에서 별도 `nohup python bot.py` 실행 없음

## 7. 중복 polling 방지

```bash
cd ~/hermes

docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Command}}' \
  | grep -E 'prof|hermes|bot|agent' || true

ps -ef | grep -E 'prof_eng|bot.py|telegram' | grep -v grep || true

docker exec prof_eng_answer_bot bash -lc '
  ps -ef | grep -E "python|bot.py|telegram" | grep -v grep || true
'
```

정상 기준:

- 같은 Telegram token으로 polling하는 Bot은 하나
- `prof_eng_answer_bot` 내부의 Python Bot process는 하나

## 8. 환경변수

환경변수는 상위 `.env`에서 관리한다.

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

민감 정보는 출력하거나 commit하지 않는다.

## 9. 코드 변경 후 최소 검증

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 -m py_compile bot.py grading_agents.py difficulty_score_ceiling.py
python3 scripts/rubric_manager.py validate-all

git diff --check
git status --short
```

Bot 실행 코드 변경 후:

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
docker logs --tail=120 prof_eng_answer_bot
```
