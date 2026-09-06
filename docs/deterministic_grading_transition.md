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

Stage37 기준 30건의 known fatal 9개를 모두 검출해 recall은 `1.0`이며 false positive는 0, 두 번의 전체 replay는 exact match로 `STABLE`이다. 질문별 명시 `required_anchor_ids`를 우선하고 명시 mapping이 없거나 유사도가 낮으면 전체 anchor로 fail-open하는 Fact Anchor adapter를 연결해 score coverage는 30/30이 됐다. 그러나 허용구간 적중률은 `0.433333`, 평균 범위 이탈은 `1.432667`이고 known-overgrading 위반 1건이 남아 권한 Gate는 `HOLD`다. 따라서 현재 운영 상태는 다음과 같다.

```text
DETERMINISTIC_GRADING_PRIMARY=FALSE
LLM_VERDICT_AUTHORITY=1
EXTERNAL_LLM_REQUIRED_FOR_VERDICT=1
```

목표값을 환경변수로 강제해도 Gate가 `READY`가 아니거나 primary score engine이 연결되지 않았으면 실행을 거부한다.

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

평균 점수 유사성은 correctness Gate를 대신할 수 없다. known fatal owner 이전과 score coverage 확장은 완료됐다. 다음 구현 순서는 답안 길이나 Golden case ID에 맞춘 보정이 아니라 A/B/C/D/E 공통 축을 결정론적 evidence로 분리하는 것이다. 구조, 질문 요구 완전성, fact correctness, 현장 판단, 연결성을 각각 검증 가능하게 산출하고 fatal·core error의 단일-owner ceiling을 마지막에 적용한다.

세부 실행 순서와 단계별 완료 조건은 [`deterministic_grading_completion_plan.md`](deterministic_grading_completion_plan.md)를 따른다.

## 금지 사항

- 특정 답안 전체 문자열 또는 session ID hardcoding
- 기존 fatal/overgrading fixture 삭제
- expected value 완화로 Gate 통과
- Gemini를 K2로 단순 교체
- local resolver에 requirement, fatal, score 또는 verdict 판정권 부여
- 모든 Topic Pack의 일괄 migration
