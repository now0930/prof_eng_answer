# Docker Compose 운영 방식

이 문서는 `prof_eng_answer` Telegram Bot의 Docker 실행 구조를 설명한다.

운영 환경에서는 상위 `~/hermes/docker-compose.yml`을 사용한다.  
Repo 내부의 `docker-compose.yaml`은 단독 실행 또는 예시용이다.

---

## 1. 운영 구조

운영 환경은 두 컨테이너로 분리한다.

| 서비스 | 컨테이너 | 역할 |
|---|---|---|
| `hermes` | `hermes_agent` | Hermes agent 기본 컨테이너 |
| `prof-eng-answer-bot` | `prof_eng_answer_bot` | Telegram 채점 Bot 자동 실행 |

`hermes` 서비스는 Telegram Bot용 `.env`를 직접 사용하지 않는다.  
Telegram token, Gemini, CLOVA, difficulty ceiling 설정은 `prof-eng-answer-bot` 서비스에서 사용한다.

---

## 2. 운영 compose 위치

운영 compose 파일 위치:

```text
~/hermes/docker-compose.yml
```

프로젝트 mount 위치:

```text
/home/now0930/hermes/workspace:/workspace
```

Bot 실행 경로:

```text
/workspace/prof_eng_answer
```

---

## 3. Bot 자동 실행

`prof-eng-answer-bot`은 Docker 시작 시 다음 스크립트를 실행한다.

```text
scripts/run_prof_eng_bot.sh
```

스크립트 역할:

- `/workspace/prof_eng_answer`로 이동
- `logs/prof_eng_answer.log` 생성
- `TELEGRAM_BOT_TOKEN`, `BOT_TOKEN`, `TELEGRAM_TOKEN` 호환 처리
- `DIFFICULTY_CEILING_MODE` 로그 출력
- `python -u bot.py` 실행

수동으로 `hermes_agent` 안에서 `nohup python bot.py`를 실행하지 않는다.  
수동 실행하면 Telegram polling이 중복될 수 있다.

---

## 4. 실행 명령

전체 실행:

```bash
cd ~/hermes
docker compose up -d
```

상태 확인:

```bash
cd ~/hermes
docker compose ps
```

정상 예:

```text
hermes_agent          Up
prof_eng_answer_bot   Up
```

Bot만 재시작:

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
```

전체 재생성:

```bash
cd ~/hermes
docker compose up -d --force-recreate hermes prof-eng-answer-bot
```

---

## 5. 로그 확인

Host 로그:

```bash
tail -n 120 ~/hermes/workspace/prof_eng_answer/logs/prof_eng_answer.log
```

Docker 로그:

```bash
docker logs --tail=120 prof_eng_answer_bot
```

컨테이너 상태:

```bash
docker inspect prof_eng_answer_bot --format 'Status={{{{.State.Status}}}} Restarting={{{{.State.Restarting}}}} ExitCode={{{{.State.ExitCode}}}}'
```

---

## 6. 중복 실행 확인

정상 상태에서는 `bot.py`가 `prof_eng_answer_bot`에만 있어야 한다.

```bash
docker exec prof_eng_answer_bot bash -lc 'pgrep -af "python.*bot.py" || true'
docker exec hermes_agent bash -lc 'pgrep -af "python.*bot.py" || true'
```

정상 기준:

| 컨테이너 | 기대 상태 |
|---|---|
| `prof_eng_answer_bot` | `python -u bot.py` 1개 |
| `hermes_agent` | 없음 |

`hermes_agent`에 bot.py가 떠 있으면 중지한다.

```bash
docker exec hermes_agent bash -lc 'pkill -f "python.*bot.py" || true'
```

---

## 7. 환경변수

운영 환경변수는 상위 `.env`에서 관리한다.

```text
~/hermes/.env
```

Repo 단독 실행 시에는 repo 루트의 `.env`를 사용할 수 있다.

```text
./.env
```

중요 변수:

| 변수 | 설명 |
|---|---|
| `TELEGRAM_BOT_TOKEN` 또는 `BOT_TOKEN` | Telegram Bot token |
| `OLLAMA_URL` | Ollama API URL |
| `OLLAMA_MODEL` | 로컬 분석 모델 |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Gemini 채점 모델 |
| `LLM_PROVIDER` | `auto`, `gemini`, `clova` |
| `CLOVA_API_KEY` | CLOVA Studio API key |
| `DIFFICULTY_CEILING_MODE` | `warn` 또는 `strict` |

`.env`는 Git에 올리지 않는다.

---

## 8. Repo compose 파일

Repo 내부 compose 파일:

```text
docker-compose.yaml
docker-compose.example.yml
```

Repo compose는 단독 실행 또는 예시용이다.

```bash
cd ~/hermes/workspace/prof_eng_answer
docker compose -f docker-compose.yaml config
docker compose -f docker-compose.yaml up -d
```

운영에서는 상위 `~/hermes/docker-compose.yml`을 우선 사용한다.
