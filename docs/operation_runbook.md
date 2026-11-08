# Operation Runbook

이 문서는 `prof_eng_answer` Telegram 채점 Bot의 운영 점검, 재시작, 장애 대응 절차를 정리한다. Compose 세부 사용법은 `docker_compose_usage.md`를 함께 본다.

**2026-11-04 배포 확인:** 운영 checkout은 `codex/essay-boundary-calibration-20261028` 개발 브랜치를 사용하며, `main`과의 동일성만으로 배포 여부를 판단하지 않는다. Fact Anchor 2,092개 중 539개는 일반 채점 참조에서 차단되고 1,553개는 차단되지 않는다. 이는 전수 사실 검증 완료를 뜻하지 않는다. [배포·채점 smoke 기록](../reports/fact_anchor_1656_operational_deployment_20261104.md)을 참조한다.

## 2026-11-08 운영 우선 전환 결정

새 채점 후보의 48건 qualification이 `HOLD`인 동안에도 **기존 운영 봇은 변경 없이 유지**한다.
지원 근거가 없는 주제의 점수 또는 Argon `FALLBACK`을 정식 합격/채점으로 승인하지 않는다.
새 커밋의 Docker 배포는 기존 `READY` → endpoint smoke 조건을 그대로 적용한다.

실패 원인, 최소 운영 범위, 향후 제한 파일럿 조건, SIL·EMC·Nyquist 후속 작업은
[운영 우선 전환 결정 및 미완료 과제(2026-11-08)](operations_first_20261108.md)를 참조한다.
해당 문서의 운영 결론은 **새 버전 배포 승인이나 기존 Release Gate 예외를 뜻하지 않는다**.

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

Telegram `/grade` 요청 시 정상 흐름(설정에 따라 D/E Argon 보조 평가가 추가될 수 있음):

```text
채점을 시작합니다.
[agent] ...
결정론적 primary 점수·fatal 판정
D/E 보조 평가 상태 확인: QUALITATIVE_DE_MODE=argon이면 provider 호출 가능
채점 완료: .../25
```

## 3. Git 최신 상태 확인

```bash
cd ~/hermes/workspace/prof_eng_answer

git fetch origin
printf '[branch] '; git branch --show-current
printf '[local HEAD] '; git rev-parse --short HEAD
printf '[upstream] '; git rev-parse --short '@{upstream}'
git status --short
git log --oneline --decorate -5
```

정상 기준:

```text
local HEAD == 추적 중인 원격 브랜치의 HEAD
git status --short 출력 없음
```

현재 브랜치가 `main`인지 먼저 확인한다. 개발 브랜치에서 배포하는 경우 `origin/main`과의 차이는 그 자체로 장애가 아니다.

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
  grading/providers/gemini.py \
  grading/providers/clova.py \
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
git add README.md docs
git commit -m "Update documentation"
git push origin HEAD
```

`git branch --show-current`로 작업 브랜치를 확인하고 보호된 `main`에 직접 커밋하지 않는다. 문서만 바꾼 경우 Bot 재시작은 필수는 아니다. 단, 운영 문서가 live 동작을 설명하는 경우 smoke test를 권장한다.

결정론 전용 smoke는 D/E 보조 평가를 일시적으로 끄고 A~C·fatal·점수 확정 경로를 점검한다. 운영 설정이 `QUALITATIVE_DE_MODE=argon`이어도 이 smoke에는 외부 호출이 없어야 한다. 실제 운영 모드의 D/E 평가를 확인하려면 별도의 공개·합성 답안으로 채점하고 provider 호출 여부, D/E 상태, `llm_verdict_authority=0`을 따로 확인한다. 두 결과는 서로 다른 범위의 시험이며, 단일 답안의 점수로 채점 품질을 보증하지 않는다.

```bash
python3 -B scripts/run_deterministic_primary_smoke.py
```

## 16. Release validation과 GitHub Actions

Runtime 또는 Rubric 변경을 push하기 전에는 host release validation을 확인한다.

```bash
cd ~/hermes/workspace/prof_eng_answer

PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0 RUN_GRADING_REPRODUCIBILITY=0 scripts/validate_release.sh
```

`PROMOTE_GENERATED=0` 경로는 GitHub Actions에서 사용하는 non-promote 검증 경로와 같은 계약을 가져야 한다.

Bot의 저장소 기준 경로는 `PROF_ENG_BASE_DIR`로 재정의할 수 있다. 기본값은
컨테이너의 `/workspace/prof_eng_answer`이며, 호스트·CI에서 직접 P0를 실행할 때는
실제 checkout 경로를 지정한다. 이 설정은 rubric·session·Master 탐색 경로만
바꾸며 채점 규칙은 바꾸지 않는다.

```bash
PROF_ENG_BASE_DIR="$PWD" \
PYTHONPATH="$PWD" \
python3 -B scripts/test_grading_reproducibility.py \
  --runs 10 --output-json /tmp/grading_reproducibility.json \
  --output-md /tmp/grading_reproducibility.md
```

Committed regression은 hermetic해야 한다.

- 로컬 `data/sessions/<session_id>/...`에 의존하지 않는다.
- 필요한 입력은 `scripts/fixtures/<semantic_name>/`에 tracked fixture로 둔다.
- clean checkout에서도 같은 focused test와 release validation이 통과해야 한다.

Push 후 해당 commit의 Actions 결과를 확인한다.

```bash
COMMIT="$(git rev-parse HEAD)"

gh run list   --repo now0930/prof_eng_answer   --workflow validation   --commit "$COMMIT"   --limit 3
```

정상 기준:

```text
status=completed
conclusion=success
headSha == local HEAD
```

GitHub runner의 action runtime deprecation warning은 job failure와 구분한다. 실제 `conclusion`과 failed step을 기준으로 판단한다.

## 17. 채점 의미 drift 점검

Issue #1 계열 변경이나 배포 전에는 Topic·기술관계·최종 출력의 의미 기준선을 확인한다.

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 -B scripts/check_grading_integrity_drift.py \
  --report /tmp/grading_integrity_drift_report.json
python3 -B tests/test_sil_runtime_replay.py
```

정상 기준:

- `status`가 `PASS`
- `semantic_sha256`가 committed baseline과 일치
- SIL 원본은 fatal, 교정본은 valid
- HAZOP/LOPA·PST·MC/DC 이웃 문항에 Issue #1 Topic이 누출되지 않음
- Telegram 투영에서 `strong`, `100%`, 잘못된 정확성 칭찬이 없음

실패 해석과 기준선 변경 절차는 [`grading_integrity_drift_runbook.md`](grading_integrity_drift_runbook.md)를 따른다.

## 18. 전문가 정확도 배포 gate

코드 release validation과 별도로 전문가 검토 Golden Set 기반 정확도 gate를 확인한다.

```bash
python3 scripts/measure_expert_accuracy.py \
  --predictions calibration/expert_accuracy_predictions.jsonl \
  --require-cases \
  --output reports/expert_accuracy_report.json

python3 scripts/check_accuracy_release_gate.py \
  --report reports/expert_accuracy_report.json \
  --require-ready
```

`READY`일 때만 정확도 정책 변경을 운영 배포한다. `draft` label은 배포 판정에서 제외한다.

## 19. 통합 Release Candidate 실행

### 19.A 검증된 Displacer Fact 7개를 지속 운영할 때

운영 점수의 소유자는 기존 채점기와 승인된 Topic Pack Anchor이다. `approved_fact_registry.json`의
7개 Fact는 출처·기술적 검증의 증거이며 `score_effect=none`이다. 등록부만 바꾸거나
`score_effect`를 수정해 점수를 직접 바꾸지 않는다. 새 문구를 채점에 적용하려면 기존
Topic Pack 승인 절차와 생성 자료 재빌드를 먼저 거친다.

배포 후보 checkout에서 다음 읽기 전용 점검을 실행한다.

```bash
python3 -B scripts/check_displacer_operational_readiness.py
python3 scripts/rubric_manager.py validate-topic-pack-release --all
python3 scripts/rubric_manager.py validate-all
PROMOTE_GENERATED=0 scripts/validate_release.sh
```

첫 명령은 검증 Fact 7개, 사람 승인 Pack, 생성된 채점 은행, 세 문항의 라우팅·요구 Anchor가
일치할 때만 성공한다. 이후에도 §19.0의 clean checkout·비공개 자료 백업·manifest 및
운영 commit 확인 조건을 모두 지킨다. Telegram에서는 Displacer 원리/Float 비교,
밀도·계면, wet/dry 교정·정비 중 각 유형을 한 번씩 시험한다. 질문별 요구 Anchor만
평가되고 다른 유형의 Anchor를 일괄 요구하지 않는지 확인한다. 실제 점수 또는 피드백에
이상이 생기면 이전 배포본으로 되돌리고 답안·채점 결과는 비공개 이력에만 남긴다.

운영하면서 WordPress나 제조사 근거를 갱신하는 경우: 원문 보존 → Fact·Anchor 차이 검토
→ Topic Pack 승인 → 생성 자료 재빌드 → 위 점검과 전체 release gate → 새 배포본 전환
→ Telegram smoke 순서로 반복한다. 승인 전 후보나 새 Fact는 운영 점수에 반영하지 않는다.

### 19.0 WordPress 학습 계층 배포 사전조건

학습 계층을 포함한 커밋은 다음 조건을 모두 만족하기 전에는 운영 컨테이너를
재시작하지 않는다.

```bash
cd ~/hermes/workspace/prof_eng_answer
git fetch origin
git status --short
git rev-parse HEAD
python3 -m py_compile study/synthesis_mapping.py study/synthesis_authoring.py \
  study/synthesis_application.py scripts/author_topic_learning_synthesis.py
python3 scripts/rubric_manager.py validate-topic-pack-release --all
PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0 \
RUN_GRADING_REPRODUCIBILITY=0 scripts/validate_release.sh
```

운영 checkout의 HEAD가 배포할 커밋과 일치하고 worktree가 clean이어야 한다.
`data/`의 WordPress 원문·OCR·학습 후보·감사 자료는 Git 추적 대상이 아니므로
별도 백업을 확인한다. Master가 가리키는 학습 artifact는 Master의
`content_sha256`과 일치해야 하며, artifact가 없는 환경에서는 기존 Training
fallback만 사용한다.

현재 개발 checkout의 최신 학습 계층 커밋과 운영 checkout의 HEAD가 다르고,
운영 checkout에는 비추적 자료가 있으므로 이 조건은 아직 충족되지 않았다.
이 상태에서 `docker compose restart`, `up`, `release_candidate deploy`를
실행하지 않는다. 운영 반영은 clean checkout에 커밋을 배치하고 비공개 자료를
별도 복원한 뒤, manifest의 commit·runtime SHA·Master artifact 해시를 확인하고
진행한다. main 병합과 실제 Telegram smoke는 별도 승인·운영 작업이다.

저장소가 clean 상태이고 현재 provider credential과 `OLLAMA_URL`의 보조 model이
준비된 환경에서 후보를 생성한다. Orchestrator는 이를 먼저 사전점검하고 실패하면
나머지 검증과 provider 호출을 시작하지 않는다.
코드 release validation은 운영 credential·provider routing 변수를 제거한 CI 동등
환경에서 실행한다. 이후 30건 재채점과 안정성 반복 평가에도 운영 API 키를
사용하지 않고, 독립된 검증 전용 provider 키만 전달한다. 코드가 같은
운영 채점 경로를 실행하더라도 자격증명과 quota는 분리한다.

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 scripts/release_candidate.py qualify --workers 2
```

### 19.1 현행 운영 채점 계약 및 재현 가능한 검사 환경 (2026-11-07)

배포 후보는 운영의 **채점 로직과 설정** (`DETERMINISTIC_GRADING_PRIMARY=true`,
`QUALITATIVE_DE_MODE=argon`)을 그대로 검사한다. 단, 검증용 subprocess에는
`VALIDATION_GEMINI_API_KEY`를 Argon transport의 `GEMINI_API_KEY` 입력에만
임시 연결한다. 운영 `GEMINI_API_KEY`를 사용하는 것은 금지한다. 두 키는
서로 달라야 하며, `VALIDATION_LIVE_API=1`을 명시하지 않으면 API 검증은
실행되지 않는다. 키 값은 출력하거나 Git에 저장하지 않는다.

### 채점 API와 검증 API 분리

| 구분 | 환경변수 | 사용 경로 |
|---|---|---|
| 채점 | `GEMINI_API_KEY`, `CLOVA_API_KEY` | Telegram 운영 봇 |
| 검증 | `VALIDATION_GEMINI_API_KEY`, `VALIDATION_CLOVA_API_KEY` | 정확도·안정성·Argon D/E 반복성·비공개 의미 검증 |
| 검증 활성화 | `VALIDATION_LIVE_API=1` | 유료 검증을 명시적으로 허용할 때만 |
| 검증 채점 횟수 한도 | `VALIDATION_MAX_LIVE_GRADES=60` | Release qualification 기본 30건 × 2회 |

**평소에는** `PROMOTE_GENERATED=0 scripts/validate_release.sh`와
`python3 scripts/rubric_manager.py validate-all`처럼 무료 결정론 검증을 사용한다.
이 경로는 운영 키와 검증 키를 모두 제거한다.

**유료 검증이 필요할 때만**, 운영에 사용하지 않는 독립 계정/프로젝트의
검증 키를 비공개 환경에 설정하고 다음을 실행한다.

```bash
# 키 값은 쉘 히스토리 또는 Git에 직접 기록하지 않는다.
# 사전에 VALIDATION_GEMINI_API_KEY를 비공개 환경에서 설정한다.
VALIDATION_LIVE_API=1 VALIDATION_MAX_LIVE_GRADES=60 \\
  python3 scripts/release_candidate.py qualify --workers 1
```

현재 Golden Set에는 48건이 있으므로 기본 2회 반복은 **총 96건의 채점 실행**이다.
기본 한도 60건에서는 실행 전 `validation_grade_budget_exceeded_actual_worklist`으로
중단된다. 실제 유료 검증을 허용할 때만 검증 전용 quota를 확인하고
`VALIDATION_MAX_LIVE_GRADES=96` 이상으로 명시적으로 조정한다.

전체 Gate는 30건 × 최소 2회 검증을 요구하므로 무료 테스트로 대체하거나
사례 수를 줄여 READY를 선언해서는 안 된다. `VALIDATION_MAX_LIVE_GRADES`는
제출 채점 횟수만 제한하며 모델 내부 요청·재시도·실제 토큰 총량까지
제한하지 않는다. 제공자 콘솔에서 **검증 프로젝트의 별도 예산·일일 quota**도
설정해야 한다. 단지 API 키 문자열만 다르고 동일 프로젝트라면 quota가
공유될 수 있다. 운영 키가 없거나 소진되어도 검증 과정에서 자동 대체하지 않는다.
운영 서비스 배포와 실제 Telegram 재채점은 별도 단계다.

`qualify`는 A/B/C의 `DETERMINISTIC_GRADING_PRIMARY_V1` 및
`deterministic_score.decision=SCORED`, D/E의
`qualitative_de_evaluation.status=APPLIED`와 provider 호출 근거,
`llm_score_authority=D_E_ONLY`, `llm_verdict_authority=0`,
최종 점수 일치·미해결 상태 유무를 검사한다. 예전
`gemini_semantic_evaluation.parsed`는 현행 성공 증거가 아니다.
`FALLBACK`, 공급자 실패, 비정상 응답, 성공 증거 누락은 **HOLD**이며
저점수로 대신 계산하거나 검사만 건너뛸 수 없다.
`semantic_truth_verified=false`만으로는 실패가 아니다. 이 필드는
문자열·구조 검증과 독립적인 의미 검증 완료 여부를 뜻한다.

운영 bot 이미지에 pytest가 없더라도 운영 이미지/서비스를 수정하지 않고
별도 Python 3.11 + pytest 8.4.2 검증 컨테이너를 만들 수 있다. 운영
checkout은 clean commit이어야 하며, 스크립트는 **추적 중인 파일만**
임시 로컬 clone으로 복제한다. 따라서 ignored WordPress 원문,
개인 session, `.env`, DB를 검증 컨테이너로 복사하지 않는다.
Docker 이미지 빌드 단계는 네트워크가 필요하며, 검증 실행은
`--network none`으로 진행한다. 기본 이미지의 실제 image ID는 출력하여
실행 기록에 보관한다. 사용 후 임시 clone을 제거하고 운영 컨테이너는
재시작하지 않는다.

```bash
cd ~/hermes/workspace/prof_eng_answer
bash scripts/run_isolated_release_validation.sh
```

실제 30건 평가와 반복 안정성은 위의 오프라인 회귀검사로 대체할 수 없다.
운영 credential·Ollama·Golden input을 사용할 수 있는 **운영 환경에서만**
`qualify`를 실행한다. 민감한 `provider_predictions`와 `grade.json`은
운영 비공개 저장소 영역에서 유지한다.

새로운 전문가 재채점 진단 경로에서는 `qualify`가
`--require-production-success --collect-failures`를 사용하여 모든 검토
사례의 성공/실패를 먼저 수집한다. 실패가 하나라도 있으면
`provider_predictions/case_results.jsonl`에 공개 case ID, 실패 유형,
정제된 원인 코드만 기록한다. 실패한 `grade.json`은 운영 비공개 출력
디렉터리에 보관해 A~E, 해결되지 않은 요구사항을 개별 분석할 수 있지만
`predictions.jsonl`은 생성하지 않으며 정확도 Gate로 진행하지 않는다.
`qualification.status=HOLD`이며 manifest에 실패한 stage의 return code가
기록된다. 반복 안정성 재채점도 동일하게 실패를 수집하고 전체 배포를
차단한다. 이 기능은 미해결 요구사항을 승인하거나 점수를 보정하지 않는다. 대표
`sil_target_operations_issue1`의 A/B/C/D/E와 요구별 source span,
fatal·ceiling, 전문가 10.0~14.5 범위는 실제 평가 결과에서 대조하고,
라벨 오류 또는 근거 누락이 독립적으로 확인되기 전에는 어떤 점수도
재보정하지 않는다.

### 19.1.A 48건 적격성 실패 원인 진단 (비공개·읽기 전용)

실제 `qualify`의 `provider_predictions/case_results.jsonl`에 `FAILED`
사례가 남아 있으면, 아래 스크립트로 **승인된 Golden 요구 ID와 실제
Grade 요구 ID의 직접 일치 여부만** 검사한다. 짝지어지지 않은 ID는
수동으로 검증한다. 원문 인용, provider 응답, API Key는 보고하지 않는다.

```bash
umask 077
python3 -B scripts/audit_expert_qualification_failures.py \
  --case-results /absolute/private/qualify/provider_predictions/case_results.jsonl \
  --golden calibration/expert_accuracy_golden.jsonl \
  --output /absolute/private/qualify/failed_case_review.json
```

보고서는 `HOLD` 전용 진단 결과이며 **정확도 Gate 또는 `READY`
판정을 대체하지 않는다**. `unmapped_expert_ids`는 Golden ID와 현재
Grade ID의 의미상 불일치를 시사할 뿐 채점 오류로 단정하지 않는다.
`Grade`가 없는 ABSTAIN 사례는 승인된 scoring Anchor/contract 근거
확보 전까지 HOLD하며, scoring-exclusion을 해제하지 않는다. 저장된
Grade/진단 자료는 GitHub에 커밋하지 않는다.

실제 `grade.json`을 확보한 운영 환경에서는 다음 읽기 전용 분석을 사용한다.
출력에는 답안 본문이나 인용문 대신 점수·상태·식별자만 포함한다.
요구 ID가 Golden과 직접 일치하지 않으면 임의 매핑하지 않고 미대응으로 남긴다.

```bash
umask 077
python3 -B scripts/audit_sil_expert_case.py \
  --grade-json /absolute/private/path/sil_target_operations_issue1/grade.json \
  --output /absolute/private/path/sil_issue1_diagnostic.json
```

`wp-post:9529`의 Master/artifact content hash가 일치하지 않으면
원본·버전·백업을 보존하여 정식 소스 갱신 및 검토 승인을 수행한다.
확인되지 않은 최신본은 별도 보류하고 승인된 채점 Fact로 승격하지 않는다.
`HOLD`이면 `docker compose restart/up`을 실행하지 않으며
기존 운영 checkout 및 비공개 자료를 이전 상태로 유지/복구한다.

출력된 manifest가 `qualification.status=READY`일 때만 배포할 수 있다. `HOLD`이면
manifest에 실패 단계와 사유가 남고 Docker 명령은 실행되지 않는다.

실제 endpoint smoke는 운영 환경마다 Telegram chat과 감시 방식이 다르므로 executable
script로 명시한다. 이 script는 실제 endpoint를 확인하고 성공 시 0, 실패 시 0이 아닌
exit code를 반환해야 한다.

```bash
python3 scripts/release_candidate.py deploy \
  --manifest reports/release_candidates/<UTC>_<commit>/manifest.json \
  --compose-file docker-compose.yaml \
  --service prof-eng-answer-bot \
  --endpoint-smoke-script /absolute/path/to/telegram_endpoint_smoke.sh
```

`deploy`는 다음을 자동 확인하고 같은 manifest에 저장한다.

1. manifest commit과 현재 HEAD 일치 및 clean worktree
2. Compose `build`가 있으면 image build, 없으면 bind-mount recreate
3. container ID 교체, 시작 시각, image ID와 runtime `engine_commit`
4. 핵심 채점 module의 host/container SHA256 parity
5. container 내부 SIL production replay
6. 운영자가 지정한 endpoint smoke

모든 항목이 통과해야 `deployment.status=PASS`와
`issue_close_eligible=true`가 기록된다. 이 값은 Issue 자동 종료 명령이 아니다.

## 20. 기존 Telegram 답안 재채점

배포 후 기존 OCR 답안을 현재 deterministic primary로 다시 채점하여 동일한 Telegram
chat으로 보낼 때 다음 명령을 사용한다. 원본 session은 변경하지 않고 새로운
`regrade_*` session을 생성한다.

```bash
cd /home/now0930/hermes

docker compose exec -T prof-eng-answer-bot \
  python3 -B /workspace/prof_eng_answer/scripts/regrade_to_telegram.py \
  --session-id 20260901_125506_5960502198
```

가장 최근 일반 session을 선택하려면 `--latest`, 전송 전 결과만 확인하려면
`--dry-run`을 사용한다.

```bash
docker compose exec -T prof-eng-answer-bot \
  python3 -B /workspace/prof_eng_answer/scripts/regrade_to_telegram.py \
  --latest --dry-run
```

필수 조건은 `DETERMINISTIC_GRADING_PRIMARY=true`, Telegram token과
`PROF_ENG_CHAT_ID`이다. 재채점은 저장된 OCR 텍스트만 사용하며 기존 사진을 다시 OCR
처리하지 않는다. 성공 출력은 `TELEGRAM_DETERMINISTIC_REGRADE_V1`, `decision=PASS`,
`provider_calls=0`을 포함한다.

기본적으로 결과 앞에 `[재채점 원문 — 복사용]`, `/grade`, 정규화된 문제·답안,
`끝.`을 전송하므로 Telegram에서 그대로 복사해 다시 제출할 수 있다. 원문이 길면 Bot의
메시지 길이 제한에 맞춰 자동 분할된다. 원문 표시가 필요 없으면 `--no-source-text`를
지정한다.

전체 과거 답안을 재채점하되 변경된 결과만 원문과 함께 받으려면 다음을 실행한다.

```bash
cd /home/now0930/hermes

docker compose exec -T prof-eng-answer-bot \
  python3 -B /workspace/prof_eng_answer/scripts/regrade_to_telegram.py \
  --all --resume --changed-only --delay 5
```

`--all`은 기본 `--dedupe-mode canonical`로 Unicode·대소문자·공백뿐 아니라 전송
span 표식, 구분선과 표현용 문장부호를 제거한 공학 내용이 같은 session을 한 건으로
처리한다. 비교 방향과 수식 연산자는 보존한다. 첫 session만 채점하며 나머지는 보고서에
`SKIPPED_DUPLICATE`와 대표 session(`duplicate_of`)을 기록한다. 엄격한 기존 비교는
`--dedupe-mode exact`, 중복을 포함한 전수 실행은 `--dedupe-mode none`을 사용한다.
같은 engine commit으로 이미 Telegram에 전송한 canonical 답안은 다음 실행에서
`SKIPPED_ALREADY_DELIVERED`로 자동 차단된다. 의도적으로 다시 보내야 할 때만
`--force-resend`를 사용한다.

대상과 엔진 실행만 먼저 확인하려면 `--dry-run --all --resume`을 사용하고, Telegram에는
개별 답안 없이 총계만 보내려면 `--all --resume --send-summary`를 사용한다. Batch는
한 session이 실패해도 다음 session을 계속 처리하지만 최종 exit code는 0이 아니며,
성공·건너뜀·실패·변경 목록은 JSON 보고서에서 확인한다.

과거 입력의 `문제:`/`답안:` 표식이 없을 때는 다음의 명시적 경계만 복원한다.

- 첫 줄의 `...설명하시오` 등 완결된 문제문
- 독립 `문제` 표식부터 첫 `1. 배경/개요` 전까지
- 첫 `1. 배경/개요` 전의 문제 요구 또는 Markdown 제목
- 저장된 `pattern` 계약 또는 명시적 `[답안] ...설계 기준` 제목

일반 답안 본문만 존재하면 계속 fail-closed로 중단한다. 콘솔 결과는 집계와 최대 10개
실패 예시만 표시하며 전체 session별 결과는 `report_path`의 JSON에서 확인한다.
