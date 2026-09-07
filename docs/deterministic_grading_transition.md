# Deterministic Grading Transition

채점의 정답·오답·fatal·점수·최종 verdict 소유권을 외부 LLM에서 결정론적 프로그램으로 옮긴다. LLM은 결정론 parser가 해석하지 못한 문장을 canonical evidence로 변환할 수만 있으며 판정 필드를 출력할 수 없다.

## 현재 상태

| Stage | 결과 | 소유 경계 |
|---|---|---|
| 35A | 완료 | Gemini/LLM 의존성 및 기존 Gate 분류 |
| 35B | 완료 | provider-neutral canonical evidence schema |
| 35C | 완료 | 전역 quantity/dimension ontology와 불변조건 검사 |
| 35D | 완료 | FSRM Topic Pack의 additive machine contract pilot |
| 35E | 완료, `HOLD` | Gemini-off 30건 replay audit |
| 35F | 완료 | 미해결 문장 전용 evidence-only local resolver 경계 |
| 35G | 완료 | 운영 점수에 영향 없는 deterministic shadow |
| 35H | Gate 구현 완료, 권한 전환 보류 | LLM verdict authority 제거 fail-closed Gate |
| 37 | coverage 확장 완료, 정확도 `HOLD` | 질문별 anchor scope + provider-free Fact Anchor evidence |
| 38 | offline Gate `READY` | 질문-only routing + A/B/C/D/E score evidence + full-chain replay |
| 39 | production 경로 연결 완료, 배포 증거 대기 | READY 재계산 + feature flag + LLM 전 경로 우회 |

Stage38 기준 질문-only Topic routing recall `1.0`, routing false positive 0, known fatal recall `1.0`(9/9), score coverage `1.0`, 허용구간 적중률 `0.866667`, 평균 범위 이탈 `0.045`, known-overgrading 0, 두 번의 전체 replay exact match를 달성해 offline Authority Gate는 `READY`다. 점수는 A 구조, B 요구 완전성, C fact correctness, D 공학 판단, E 연결성의 provider-free evidence를 분리하고, 3쪽 미만 evidence는 high-score eligibility만 제한한다.

Stage39 production entrypoint도 연결됐다. `DETERMINISTIC_GRADING_PRIMARY=true`이면 실행 중인 코드로 30건 Authority Gate를 다시 계산하고, READY일 때만 deterministic primary를 선택한다. 이 경로에서는 legacy LLM grader, score adjudicator, legacy finalizer와 LLM Telegram summarizer를 호출하지 않는다. 결과는 `deterministic_grade.json`, `grade_raw.txt`, 최종 `grade.json`에 provider-neutral schema로 저장된다. 저장소 기본값과 아직 전환하지 않은 운영값은 다음과 같다.

Host production-entrypoint smoke 증거는 `reports/deterministic_primary_smoke_stage39.json`에 저장한다. 이 검증은 실제 `grading_agents.run_agent_pipeline`을 호출하면서 provider callable을 금지하고 provider call 0, fatal 검출, false pass 방지와 persistence를 확인한다.

```text
DETERMINISTIC_GRADING_PRIMARY=FALSE
LLM_VERDICT_AUTHORITY=1
EXTERNAL_LLM_REQUIRED_FOR_VERDICT=1
```

운영 전환 시에는 `DETERMINISTIC_GRADING_PRIMARY=TRUE`로 설정한다. Gate가 `READY`가 아니면 fail-closed로 실행을 거부하며 legacy 결과로 조용히 fallback하지 않는다. `FALSE`로 되돌리면 즉시 legacy primary + deterministic shadow 경로로 rollback된다.

## 데이터 흐름과 소유권

```text
answer
  -> deterministic parser
  -> unresolved span only: optional local semantic resolver
  -> canonical evidence (evidence authority only)
  -> global ontology invariants
  -> Topic Pack machine contract
  -> requirement/fatal/score/verdict deterministic owner (migration target)
```

- 전역 공학 사실·차원은 `grading_ontology/`가 소유한다.
- 문제별 필수 관계와 invariant-to-fatal 연결은 Topic Pack의 선택적 `machine_contract`가 소유한다.
- `canonical_grading_evidence.py`는 score, status, verdict, fatal 등 판정권 필드를 재귀적으로 거부한다.
- `deterministic_grading_shadow.py` 결과는 `score_effect=none`이며 기존 점수와 verdict를 변경하지 않는다.
- 기존 fatal rule ID와 regression fixture는 삭제하지 않고 deterministic binding 대상으로 유지한다.

## Gate 실행

```bash
python3 scripts/run_deterministic_replay_audit.py
python3 scripts/check_deterministic_authority_gate.py
```

실제 권한 제거 전에는 모두 충족해야 한다.

- known fatal recall 100%
- fatal false positive 0
- known-overgrading regression PASS
- normal-answer regression PASS
- deterministic repeatability 100%
- score/verdict consistency PASS
- unexplained verdict difference 0
- deterministic score coverage 100%
- score 허용구간 적중률 85% 이상
- 평균 score 허용구간 이탈 1.0점 이하
- external LLM required for verdict 0

평균 점수 유사성은 correctness Gate를 대신할 수 없다. Stage38/39는 Golden case ID나 목표 score range를 runtime rule에 사용하지 않으며 질문, Topic Pack, ontology와 가시적 답안 evidence만 사용한다. 남은 운영 작업은 대상 commit image rebuild/recreate, container fingerprint·parity 확인, production replay와 endpoint smoke 저장, rollback smoke이다.

세부 실행 순서와 단계별 완료 조건은 [`deterministic_grading_completion_plan.md`](deterministic_grading_completion_plan.md)를 따른다.

## 금지 사항

- 특정 답안 전체 문자열 또는 session ID hardcoding
- 기존 fatal/overgrading fixture 삭제
- expected value 완화로 Gate 통과
- Gemini를 K2로 단순 교체
- local resolver에 requirement, fatal, score 또는 verdict 판정권 부여
- 모든 Topic Pack의 일괄 migration
