# Operation Runbook

이 문서는 `prof_eng_answer` Telegram 채점 Bot의 운영 점검, 재시작, 장애 대응 절차를 정리한다. Compose 세부 사용법은 `docker_compose_usage.md`를 함께 본다.

## 1. 현재 운영 기준

| 항목 | 기준 |
|---|---|
| Repository | `~/hermes/workspace/prof_eng_answer` |
| 컨테이너 내부 경로 | `/workspace/prof_eng_answer` |
| Compose 위치 | `~/hermes` |
| Bot 컨테이너 | `prof_eng_answer_bot` |
| Compose 서비스명 | 보통 `prof-eng-answer-bot` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 nohup 실행 | 사용하지 않음 |
| 로그 | `logs/prof_eng_answer.log`, `docker logs prof_eng_answer_bot` |

## 2. 빠른 상태 점검

```bash
cd ~/hermes

docker compose ps
docker logs --tail=120 prof_eng_answer_bot
```

정상 기준:

```text
prof_eng_answer_bot Up
bot started. ollama=..., model=...
```

Telegram `/grade` 요청 시 정상 흐름:

```text
채점을 시작합니다.
[agent] ...
[agent] Gemini semantic grader applied.   # provider에 따라 다를 수 있음
[agent] phase2 layered scoring applied: ...
채점 완료: .../25
[Question Type Coverage]
```

## 3. Git 최신 상태 확인

```bash
cd ~/hermes/workspace/prof_eng_answer

git fetch origin main
printf '[local HEAD] '; git rev-parse --short HEAD
printf '[origin/main] '; git rev-parse --short origin/main
git status --short
git log --oneline --decorate -5
```

정상 기준:

```text
local HEAD == origin/main
git status --short 출력 없음
```

## 4. Bot 재시작

일반 재시작:

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
sleep 5
docker compose ps prof-eng-answer-bot
docker logs --tail=80 prof_eng_answer_bot
```

완전 재기동:

```bash
cd ~/hermes
docker compose stop prof-eng-answer-bot
sleep 3
docker compose up -d prof-eng-answer-bot
sleep 8
docker compose ps prof-eng-answer-bot
docker logs --tail=120 prof_eng_answer_bot
```

완전 재기동 권장 상황:

- `bot.py` 실행 흐름 수정
- formatter 또는 `send_message()` boundary 수정
- Telegram 출력이 이전 코드처럼 보임
- polling 충돌 의심
- provider 설정 변경 후 live process 상태가 의심됨

## 5. 중복 polling 확인

Telegram Bot은 같은 token으로 여러 프로세스가 polling하면 응답이 꼬일 수 있다.

```bash
cd ~/hermes

echo '[containers]'
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Command}}' \
  | grep -E 'prof|hermes|bot|agent' || true

echo '[host python bot processes]'
ps -ef | grep -E 'prof_eng|run_prof_eng_bot|bot.py|telegram' | grep -v grep || true

echo '[prof_eng_answer_bot processes]'
docker exec prof_eng_answer_bot bash -lc '
  ps -ef | grep -E "python|bot.py|run_prof_eng_bot|telegram" | grep -v grep || true
'

echo '[hermes_agent processes]'
docker exec hermes_agent bash -lc '
  ps -ef | grep -E "prof_eng|bot.py|run_prof_eng_bot|telegram" | grep -v grep || true
' 2>/dev/null || true
```

정상 기준:

- `prof_eng_answer_bot` 내부에 `python -u bot.py` 1개
- `hermes_agent` 내부에는 `prof_eng_answer`용 `bot.py` 없음
- 같은 Telegram token을 쓰는 다른 bot 컨테이너 없음

## 6. 실행 명령 확인

```bash
cd ~/hermes

docker inspect prof_eng_answer_bot \
  --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'

docker compose config | sed -n '/prof-eng-answer-bot:/,/^[^ ]/p'
```

정상 기준:

- `prof_eng_answer_bot`이 `bot.py` 실행
- 수동 `nohup python bot.py` 실행 없음

## 7. 컨테이너 내부 코드 확인

```bash
cd ~/hermes

docker exec prof_eng_answer_bot bash -lc '
  cd /workspace/prof_eng_answer 2>/dev/null || cd /app 2>/dev/null || exit 1
  pwd
  echo
  git log --oneline --decorate -5 2>/dev/null || true
  git status --short 2>/dev/null || true
  echo
  grep -nE "def send_message|def format_result|difficulty_ceiling_evaluation|cap_applied|if __name__|main\(|while True" bot.py | sed -n "1,220p"
'
```

확인 포인트:

- `send_message()`가 최종 cleanup boundary 역할을 함
- `format_result()`가 ceiling 전/후 점수를 구분해 출력함
- `main()` 아래에 추가한 wrapper 코드는 실행되지 않음

## 8. Provider 점검

Telegram 명령:

```text
/provider
/provider auto
/provider gemini
/provider clova
/provider reset
```

운영 권장 기본값:

```text
LLM_PROVIDER=auto
LLM_PRIMARY=gemini
LLM_FALLBACK=clova
```

## 9. 환경변수 점검

환경변수는 상위 `.env`에서 관리한다.

```bash
cd ~/hermes
ls -la .env
```

확인할 항목:

- `TELEGRAM_BOT_TOKEN` 또는 `BOT_TOKEN`
- `OLLAMA_URL`
- `OLLAMA_MODEL`
- `GEMINI_API_KEY`
- `CLOVA_API_KEY`
- `LLM_PROVIDER`
- `LLM_PRIMARY`
- `LLM_FALLBACK`
- `DIFFICULTY_CEILING_MODE`
- `QUESTION_TYPE_COVERAGE_SCORE_MODE`

민감 정보 값을 직접 출력하거나 commit하지 않는다.

## 10. 대표 smoke test

Telegram에서 다음을 보낸다.

```text
/grade
문제: 차압전송기의 교정회로와 교정절차를 설명하시오.
답안: 차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.
```

정상 확인:

- 채점을 시작합니다 메시지 출력
- 채점 완료 메시지 출력
- `[Question Type Coverage]` 출력
- 문제 유형 lens가 `IMPLEMENTATION_EVALUATION` 계열로 표시
- legacy `GENERAL(일반 설명형)` 문구가 나오지 않음
- `C항목 보완: 문제 유형 lens에 맞는 핵심 fact...` 문구가 나옴

## 11. Theory-core ceiling smoke test

2차 시스템처럼 `THEORY_CORE` 문항에서 핵심 이론 오류가 있는 답안을 보내면 다음이 구분되어야 한다.

- `채점 완료: 10.0/25`처럼 최종 cap 점수
- `예상 점수대: 10~10`
- 3인 요약에서 ceiling 적용 전 평균/가중 점수
- difficulty ceiling 적용 후 최종 점수
- 약점에 구체적 이론 오류

예시 약점:

```text
감쇠비 관계식 오류
부족감쇠 해석 오류
감쇠비 구간 구분 부족
```

## 12. 코드 검증

```bash
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
  semantic_question_type_postprocess.py

python3 scripts/rubric_manager.py validate-all
```

정상 기준:

```text
ALL VALID
```

## 13. Rubric audit

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 scripts/rubric_audit/run_rubric_audit.py
```

정상 기준:

```text
status: PASS
Fact Anchor: MAJOR=0
Model Answer relationship: MAJOR=0
priority MINOR: 0
validate-all: OK
```

## 14. 자주 보는 증상과 원인

| 증상 | 가능 원인 | 조치 |
|---|---|---|
| Telegram 응답 없음 | Bot down, token 문제, polling 충돌 | `docker logs`, 중복 polling 확인 |
| 예전 문구가 계속 나옴 | live process가 이전 코드 import 상태 | 완전 재기동 |
| `/provider`와 실제 채점 provider가 다름 | chat별 provider 설정 또는 환경변수 혼선 | `/provider reset`, 로그 확인 |
| `phase2 postprocess failed` | Python 후처리 예외 | traceback 확인 후 해당 module 수정 |
| `모델 분석 JSON 파싱 실패` | Ollama 1차 분석 JSON malformed | 최종 phase2 결과가 교체됐는지 확인, parser 보강 |
| 점수대와 최종 점수 불일치 | ceiling 후 display field 동기화 누락 | `score_range`, `rater_summary`, `difficulty_ceiling_evaluation` 확인 |
| `GENERAL(일반 설명형)` 문구 출력 | legacy cleanup 누락 | `send_message()` boundary 확인 |

## 15. 문서 변경 반영

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 scripts/rubric_manager.py validate-all
git diff --check
git status --short
git add README.md docs scripts/rubrics
git commit -m "Update documentation"
git push origin main
```

문서만 바꾼 경우 Bot 재시작은 필수는 아니다. 단, 운영 문서가 live 동작을 설명하는 경우 smoke test를 권장한다.
