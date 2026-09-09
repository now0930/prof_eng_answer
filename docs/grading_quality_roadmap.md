# Grading Quality Roadmap

이 문서는 채점 정확도, 회귀 검증, Topic Pack 확장과 운영 배포의 장기 관리 정책을 정의한다. [GitHub Issue #1](https://github.com/now0930/prof_eng_answer/issues/1)은 결정론적 전환의 종료 증거를 보존한다. 이후 회귀는 별도 Issue로 추적하고, 반복 가능한 정책은 이 문서를 정본으로 사용한다.

## 1. 현재 기준선

| 항목 | 현재 상태 | 정본 |
|---|---|---|
| 채점 구조·점수 소유권 | 구현 완료, 지속 회귀 | [`grading_architecture.md`](grading_architecture.md) |
| Canonical demand ledger와 공개 coverage summary | 구현 완료, 지속 회귀 | `evaluation_ledger.py`, SIL output/coverage tests |
| 전문가 정확도 Gate | Deterministic 30건 `READY`: score in-range 100%, 평균 이탈 0점, known-overgrading 0 | [`accuracy_release_gate.md`](accuracy_release_gate.md), deterministic replay artifact |
| 요구상태 안정성 Gate | 30건 2회 exact replay `STABLE`, provider call 0 | `reports/deterministic_stability_stage38.json` |
| Topic Pack authoring·검증 | `ab94b69`에서 범용·대상 기반 흐름 적용 | [`topic_pack_workflow.md`](topic_pack_workflow.md) |
| Topic Atomicity | 78 Topic, 차단 오류 0, scoped question contract 698개, 검토 경고 38 | [`topic_pack_atomicity.md`](topic_pack_atomicity.md) |
| Runtime provenance | container parity·production replay·Telegram raw/final exact match 완료 | [`operation_runbook.md`](operation_runbook.md), `reports/deterministic_endpoint_consistency_stage41.json` |
| 결정론적 채점 전환 | 운영 완료: routing 100%·fatal 9/9·score 30/30·LLM verdict authority 0 | [`deterministic_grading_transition.md`](deterministic_grading_transition.md) |

코드 회귀 PASS와 운영 정확도 `READY`, 배포 증명 완료는 서로 다른 판정이다. 하나의 판정으로 다른 판정을 대체하지 않는다.

## 2. 변경 등급과 필수 Gate

| 변경 등급 | 예시 | 필수 검증 |
|---|---|---|
| 문서 | 링크, 설명, 절차 | Markdown 링크·`git diff --check` |
| Topic source | Fact, alias, Logic Check, 신규 Topic | 단일 Topic release, 필요 시 routing smoke |
| 채점 runtime | 점수, coverage, verifier, finalizer | focused regression, 전체 release, 전문가 정확도 Gate |
| 배포 runtime | image, Compose, provider, 환경변수 | rebuild/recreate, container replay, fingerprint·parity, endpoint smoke |

정확도 Gate가 `HOLD`이면 코드 병합 여부와 무관하게 새 채점 정책의 운영 배포를 승인하지 않는다. Gate를 다시 열 때는 현재 코드와 provider로 prediction 30건 이상을 재생성하고 전문가 label과 대조한다.

## 3. 채점 오류 관리

1. 실제 사례를 익명화한 재현 fixture로 만든다.
2. 문제 제목이나 session ID 전용 예외를 추가하지 않는다.
3. 최초 오류 owner를 Question Demand, Fact Anchor, Logic Check, evaluator, score reconciliation 또는 formatter 중 하나로 지정한다.
4. 정답·부분정답·핵심오답과 false-positive 사례를 함께 검증한다.
5. focused regression과 전체 release를 통과시킨다.
6. 정확도 의미가 바뀌면 기존 prediction을 재사용하지 않고 전문가 정확도 Gate를 재측정한다.
7. 배포 후 container와 실제 endpoint에서 동일 판정을 확인한다.

핵심 지표는 fatal 답안의 pass/strong escape 0건, verified defect와 `incorrect` 동기화 실패 0건, 출력·저장 판정 불일치 0건이다.

## 4. Golden Set 관리

- 최소 운영 Gate는 reviewed/adjudicated 30건, Topic 10개, Question Type별 3건과 major/fatal label 8개다.
- 모든 신규 Topic마다 세 개의 Golden case를 기계적으로 추가하지 않는다.
- 점수·fatal·major·coverage 의미를 바꾸거나 안전 중요도가 높은 Topic은 정답/부분정답/핵심오답 사례를 추가한다.
- 단순 alias·문서·비채점 metadata 변경은 focused source/routing regression으로 검증할 수 있다.
- provider, prompt, scoring 또는 evidence 상태 의미가 바뀌면 prediction을 재생성하고 Gate 결과와 생성 commit을 함께 기록한다.
- 과거 `READY` 결과는 이후 정책 변경의 배포 근거로 재사용하지 않는다.

## 5. Topic Pack 관리

신규 Topic은 Topic Sheet의 ownership과 negative boundary를 먼저 확정한다. 생성·검증 절차는 [`topic_pack_workflow.md`](topic_pack_workflow.md)를 따른다.

관리 원칙:

- 기술 내용은 Topic Sheet와 검토된 source JSON이 소유한다.
- 신규 Topic은 `add-topic`으로 시작하고 `approve-topic`으로 사람 검토와 source hash를 기록한다.
- 생성기는 다른 Topic의 공식·규칙을 주입하지 않는다.
- 분류는 각 `topic_importance.json`의 `difficulty`가 정본이며 별도 Topic 목록이나 고정 총계를 중복 관리하지 않는다.
- 기본 release는 변경 Topic 또는 `--topic-id`만 검증한다. 전체 inventory는 통합 시점에 `--all`로 실행한다.
- live LLM smoke는 외부 환경이 필요한 별도 Gate이며 기본 source 검증에 포함하지 않는다.
- 생성 또는 release 실패 시 canonical source와 generated bank를 작업 전 상태로 복구한다.
- 승인 이후 source가 바뀐 관리 대상 Topic은 promote와 전체 integration을 차단한다.
- generated bank는 직접 수정하지 않는다.
- 전체 Topic inventory를 일괄 migration하거나 동일한 machine contract를 복제하지 않는다.
- 실제 오판정이 재현되거나 명시 Question Demand scope가 필요한 Topic만 선택 수정한다.
- 관련 없는 anchor가 평가되는 경우 신규 Topic보다 기존 Topic의 `required_anchor_ids`와 routing boundary를 먼저 보강한다.
- 공통 단위·차원·quantity type·관계 불변조건은 Topic Pack에 반복하지 않고 `grading_ontology/`가 소유한다.

## 6. Release와 배포

결정론적 primary 변경은 Topic·routing·fatal·score regression과 Authority Gate,
2회 exact Stability Gate를 통과해야 한다. `deploy`는 같은 commit의
`READY` artifact만 받아 rebuild 또는 recreate와 container parity, provider-zero replay,
endpoint exact-match 증거를 수집한다. 어느 Gate든 `HOLD`면 Docker 명령을
실행하지 않는다.

`scripts/release_candidate.py` 기반 provider qualification은 legacy 비교나 optional
semantic resolver의 evidence 추출을 변경할 때만 별도 lane으로 수행한다. 이 Gate는
provider 품질을 증명할 수는 있지만 requirement status·fatal·score·verdict 판정권을
provider에게 부여하지 않는다.

### 매 release

1. 변경 범위의 focused regression
2. `scripts/validate_release.sh`
3. 채점 의미 변경 시 전문가 정확도 Gate
4. generated source/build 정합성과 clean worktree 확인
5. push 후 local/tracking/remote SHA와 CI 확인

### 매 deployment

1. 배포 대상 commit과 image digest 기록
2. container ID·시작 시각과 process 교체 확인
3. host/container 핵심 module SHA parity 확인
4. container 내부 production replay
5. Telegram 또는 동등 endpoint smoke
6. 결과 artifact 저장

fingerprint, parity, replay 또는 endpoint 증거가 빠지면 배포 완료로 기록하지 않는다.
manifest의 `issue_close_eligible=true`는 기술 Gate가 모두 통과했다는 뜻이며 Issue를
자동으로 닫지는 않는다.

## 7. 문서와 Issue 관리

- 이 문서: 장기 정책, Gate와 관리 원칙
- [`grading_architecture.md`](grading_architecture.md): 현재 채점 구조와 owner
- [`topic_pack_workflow.md`](topic_pack_workflow.md): Topic 추가·수정 실행 절차
- [`operation_runbook.md`](operation_runbook.md): 운영·배포 명령
- [`accuracy_release_gate.md`](accuracy_release_gate.md): 정확도 Gate 수치와 실행법
- Issue #1: 결정론적 전환 완료 증거를 보존한 종료 이력
- 신규 regression: 별도 Issue에서 fixture·owner·Gate·배포 증거를 추적하고 Issue #1을 참조
- `docs/archive/`: 종료된 Stage와 과거 판단 기록

## 8. 결정론적 판정권 전환

외부 LLM 제거는 provider 교체가 아니라 판정 소유권 이전이다. canonical evidence, 전역 ontology, Topic Pack machine contract, deterministic evaluator, fatal 전파, 점수와 verdict consistency 순으로 이전한다. LLM은 미해결 자연어의 evidence 추출만 보조할 수 있다.

현재 quantity/dimension과 engineering relation ontology, Topic Pack machine contract, 질문-only deterministic router, Fact Anchor evidence, A/B/C/D/E score evidence와 권한 제거 Gate가 구현됐다. Stage48 Gemini-off 30건은 Topic routing recall 100%, fatal 9/9, score coverage 100%, 허용구간 적중률 100%, 평균 범위 이탈 0점, known-overgrading 0건으로 offline Gate `READY`다. Stage39~41에서 production entrypoint, container parity/replay, 실제 Telegram endpoint와 persisted raw/final exact match까지 완료했다. 운영은 deterministic primary이며 외부 LLM은 requirement·fatal·score·verdict 판정권을 갖지 않는다.

구현 순서, mutation 범위와 단계별 완료 조건은 [`deterministic_grading_completion_plan.md`](deterministic_grading_completion_plan.md)가 소유한다.

Issue 본문은 현재 상태만 유지한다. 긴 실행 로그는 comment 또는 repository artifact에 남기고, 완료된 과거 Stage를 현재 blocker처럼 유지하지 않는다.

## 9. 전환 완료 후 개발 방향

Topic Pack의 일괄 정리·확장은 2026-09-09 기준으로 종료한다. 현재 기준선은 78 Topic,
Atomicity 차단 오류 0, 문자열 질문 계약 0, 검토 경고 38이다. 경고만으로 Pack을
분리하지 않으며 이후 Topic 수정은 실제 routing·scope·채점 오류가 재현된 경우에만
수행한다. 다음 개발 owner는 Topic inventory가 아니라 canonical claim과 요구상태
판정 정확도다.

### 완료 — Question scope와 Topic Atomicity 기준선

- 698개 질문을 객체형 `pattern + required_anchor_ids` 계약으로 통일했다.
- P0 owner 오염 4건을 복구하고 Atomicity Gate를 release에 연결했다.
- Nyquist/Routh alias 경계는 정상·비교·방법 미지정·답안 오염 fixture로 고정했다.
- 남은 경고는 실제 기출·routing·Golden 증거가 생길 때만 개별 처리한다.

### P0 — Canonical Claim Extractor

답안 span을 단순 키워드 hit가 아니라 다음 provider-neutral evidence로 정규화한다.

```text
subject · predicate · object · condition · polarity · source_span · extractor
```

- 정의, 분류, 적용조건, 인과, 비교, 수식 관계를 canonical predicate로 분리한다.
- 부정, 인용, 타인의 주장, 정정 전 문장과 최종 채택 주장을 구분한다.
- 한 span을 관련 없는 여러 anchor에 중복 증거로 사용하지 않는다.
- deterministic parser가 해석하지 못한 span은 `UNKNOWN/ABSTAIN`으로 남기며 추측해
  정답 또는 오답으로 확정하지 않는다.

2026-09-09 Stage42에서 이 경계를 production deterministic-primary 입력에 연결했다.
global predicate ontology, 부정·인용·정정 context, 절 경계, relation-object mutation과
claim 단일 배정을 focused regression으로 고정했다. 확대 단위는 Topic 개수가 아니라
검증된 오분류가 있는 machine contract이며 일괄 migration은 하지 않는다.

첫 확대 대상은 Stage43의 V-Model/SW 검증 과대평가 회귀다. 핵심 8개 Fact Anchor를
canonical machine contract로 승격하고 같은 anchor의 lexical 상태와 canonical 상태를
비교 기록한다. 질문 scope는 `required_anchor_ids`가 소유하며, 승격은 정상 완전답안과
오답 mutation이 함께 통과할 때만 허용한다. 다음 Topic도 실제 오분류 fixture가 있는
경우에만 같은 방식으로 한 owner씩 확대한다.

Stage44에서는 Issue #1의 SIL 목표 결정 원본·교정 쌍을 두 번째 승격 대상으로 삼는다.
원본의 fatal 4건과 13.0점 ceiling은 유지하면서, 교정 답안의 올바른
`F_target/F_residual`, `1/PFDavg`, achieved SIL 입력, MOC, AI·OT 기능안전 관계가
`MISSING`으로 떨어지던 false negative를 제거한다. 이후 대상은 canonical 비교가 0인
HAZOP/LOPA 운영 fixture이며, 현재 Stage의 전체 Gate가 유지된 뒤 별도 변경한다.

Stage45에서는 HAZOP/LOPA 반응기 과압력 fixture의 9개 anchor를 승격한다. 기존 답안은
PFD 빈도비와 SIF 구성요소만 부분 증거로 인정하고, scenario 경계·IPL 적격성·RRF·SIL
mapping·SRS 인계 누락은 canonical `MISSING`으로 구분한다. 차원 오류는 Topic에
복제하지 않고 FSRM global invariant가 단일 owner로 유지한다. 다음 확대 대상은 새
운영 오분류 또는 reviewed mutation 증거가 생긴 Topic으로 제한한다.

Stage46에서는 전문가 승인된 MC/DC–V-Model–SIL 복합 회귀를 사용한다. MC/DC를
구조적 커버리지·조건 독립영향·100% 한계·수명주기 보완 관계로 판정하고, 정적·동적
분석은 분석 대상이 서술된 경우에만 충족한다. `실행하지 않고`처럼 object의 성질을
나타내는 부정은 뒤의 분석 관계를 반전시키지 않는다. 복합 질문의 exact scope 적용
실험에서 총점이 10.83→8.35로 과도하게 낮아졌으므로, 다음 우선순위는 requirement 수에
따른 WRONG/MISSING 정규화 편향을 제거한 뒤 질문 scope를 다시 적용하는 것이다.

Stage47에서는 위 편향을 `score_group_id`로 제거한다. requirement row는 추적성과
feedback을 위해 모두 보존하되, 동일 공학 요구축에 속한 Topic anchor와 fatal 보조
requirement는 한 번만 점수화한다. 그룹 우선순위는 `WRONG > SATISFIED > PARTIAL >
MISSING`이며, 서로 다른 Topic의 동명 requirement는 명시적 group ID가 없으면 합치지
않는다. 승인 복합 회귀는 exact scope 8축, raw evidence 13건, 12.60점으로 안정화됐다.

Stage48에서는 잔여 점수 이탈 4건이 모두 경미한 과대평가임을 확인했다. Topic별 cap을
추가하지 않고 심화 자격 미충족 답안의 상한을 18.5점으로 정렬했으며, 일반적인
구조·판단·연결 키워드만으로는 24점을 초과하지 못하게 했다. 25점 부여는 향후 별도의
결정론적 exceptional-evidence contract가 실제 심화 근거를 증명할 때만 허용한다.

### P0 — 요구상태 Evaluator

- 단일 일반 단어가 여러 anchor의 `PARTIAL` 근거로 중복 사용되는 비율을 측정한다.
- `SATISFIED`: 요구된 핵심 개념·관계·조건이 정렬되고 직접 충돌이 없다.
- `PARTIAL`: 관련 개념과 일부 관계는 식별되지만 필수 관계 또는 조건이 부족하다.
- `WRONG`: 요구와 관련된 명시적 주장이 Topic contract 또는 공학 불변조건과 충돌한다.
- `MISSING`: 요구에 연결할 수 있는 실질적 evidence가 없다.
- `UNKNOWN/ABSTAIN`은 내부 해석 상태이며 최종 요구상태로 점수화하지 않는다.
- 최소 `SATISFIED` 합격 증거와 fatal ceiling은 유지하며 threshold 완화로 Golden Gate를 맞추지 않는다.
- evaluator만 `SATISFIED/PARTIAL/WRONG/MISSING`을 결정하며 extractor, LLM 또는 formatter는
  상태와 점수를 출력할 권한이 없다.

### P1 — 전체 Topic 위험 기반 Golden 확대

- 모든 Topic에 동일 개수의 사례를 강제하지 않는다.
- 안전·계산·법규·빈출 Topic부터 정답, 부분답, 핵심오답, 부정·인용·정정 문맥 mutation을 추가한다.
- 목표는 Topic inventory coverage, fatal false-negative 0, false pass 0, 동일 입력 repeatability 100%다.
- mutation은 개념, 관계 방향, 조건, 단위·차원, 극성, 부정·정정 문맥을 한 번에 하나씩
  바꾸고 어떤 deterministic rule이 작동해야 하는지 명시한다.

### P1 — Ontology와 Topic contract 분리 강화

- 공통 quantity, dimension, demand mode와 일반 관계 규칙은 global ontology에 둔다.
- 문제별 필수 설명, 허용 관계, negative boundary와 중요도만 Topic Pack이 소유한다.
- 동일 공학 사실의 Topic 간 복제·불일치 검출 validator를 추가한다.

### P2 — Optional local semantic resolver

- deterministic parser가 `UNKNOWN` 또는 `ABSTAIN`한 span에만 local resolver를 shadow로 적용한다.
- resolver 출력은 canonical evidence schema만 허용하고 status·fatal·score·verdict 필드를 계속 거부한다.
- resolver 장애 시에도 이미 결정 가능한 채점은 유지하며 외부 LLM을 production verdict 경로에 재도입하지 않는다.

### 지속 운영

1. 실제 이상 사례 수집
2. 익명화 fixture와 owner 분류
3. focused mutation regression
4. 30건 Authority·2회 Stability Gate
5. container parity·provider-zero replay
6. Telegram raw/final exact match
7. commit·CI·운영 evidence를 신규 Issue에 기록

Topic Pack 변경의 완료 기준은 "파일이 생성됨"이 아니라 문제 요구범위가 정확하고 정답·부분답·오답 경계를 재현 가능하게 보호하는 것이다.

### 정확도 완료 조건

- known core/fatal error recall 100%, false pass 0
- 정상 답안의 fatal/core-error false positive 0
- reviewed requirement status confusion matrix에서 설명되지 않은 오분류 0
- 동일 입력의 requirement status·score·verdict repeatability 100%
- score/verdict/coverage/총평 간 consistency 위반 0
- `EXTERNAL_LLM_REQUIRED_FOR_VERDICT=0`, `LLM_VERDICT_AUTHORITY=0` 유지

평균 점수 차이만으로 정확도를 승인하지 않는다. 우선순위는 core error false negative,
정상 답안 false positive, 명백한 오답의 `SATISFIED` 판정 순이다.
