# Deterministic Grading Completion Plan

## 1. 목표와 기준선

목표는 Gemini 또는 다른 LLM 없이 requirement 상태, fatal/core error, 점수와 최종 verdict를 결정하는 것이다. Stage38 offline full-chain은 Topic routing recall 100%, known-fatal 9/9, score coverage 30/30, 허용구간 적중률 86.67%, 평균 범위 이탈 0.045점, known-overgrading 0건으로 Authority Gate `READY`다. production authority는 entrypoint 연결·rollback·운영 증거 전까지 이전하지 않는다.

완료 목표:

```text
KNOWN_FATAL_RECALL=100%
FATAL_FALSE_POSITIVE_COUNT=0
DETERMINISTIC_REPEATABILITY=100%
UNEXPLAINED_VERDICT_DIFF=0
EXTERNAL_LLM_REQUIRED_FOR_VERDICT=0
LLM_VERDICT_AUTHORITY=0
DETERMINISTIC_GRADING_PRIMARY=TRUE
```

## 2. 미검출 8건과 설계 소유자

| 묶음 | Fatal ID | 일반화할 오류 유형 | 주 소유자 |
|---|---|---|---|
| Q1 | `fatal_target_pfd_frequency_product` | 확률 목표값에 빈도×빈도를 사용하는 차원·연산 오류 | global quantity/expression ontology + SIL target contract |
| Q2 | `fatal_demand_mode_by_fault_detection` | demand frequency와 diagnostic detectability 역할 혼동 | global concept-role ontology + SIL target contract |
| Q3 | `fatal_pst_replaces_full_test_or_reduces_mttr` | 부분시험·전체시험·수리시간의 역할/대체 관계 혼동 | global activity-role ontology + SIL lifecycle contract |
| Q4 | `fatal_certificate_interval_as_operating_minimum` | 인증 가정을 현장 최소·최적 운전조건으로 오인 | global assurance/constraint relation + SIL lifecycle contract |
| S1 | `sw04_fatal_misra_is_unit_test_tool` | 표준·규칙집과 실행 시험도구의 분류 혼동 | global artifact/tool ontology + SW-04 contract |
| S2 | `sw05_fatal_software_test_is_random_hardware_integrity` | software V&V와 random hardware integrity 통제축 혼동 | global integrity-domain ontology + SW-05 contract |
| S3 | `sw05_fatal_hft_is_integration_test` | hardware architecture constraint와 test level 혼동 | global architecture/test ontology + SW-05 contract |
| S4 | `sil_four_universal_rule` | 적용 표준·범위를 무시한 SIL4/MC/DC 보편 의무화 | global normative-applicability rule + MC/DC contract |

특정 fixture 문장을 규칙으로 사용하지 않는다. 전역 ontology는 개념의 불변 분류와 허용 관계만 소유하고, Topic Pack은 해당 문제에서 요구되는 관계와 기존 fatal ID binding만 소유한다.

## 3. 실행 단계

### Stage36A — Fatal taxonomy와 canonical relation 확정

산출물:

- 8개 fatal의 `error_class`, canonical subject/predicate/object, polarity 확정
- 기존 fatal ID와 requirement reference 보존
- global ontology와 Topic Pack 중 단일 owner 지정
- 같은 의미의 중복 fatal ID·충돌 규칙 목록 작성

Gate:

- 각 fatal에 owner 1개
- fixture 전체 문자열·session ID·문제 제목 조건 0개
- 기존 fatal rule 삭제 0개

### Stage36B — SIL 운영 오류 4종 결정론화

구현 순서:

1. 수식 AST에 multiply/divide와 결과 차원 전파 추가
2. demand mode와 diagnostic detectability의 concept-role 제약 추가
3. PST/full proof test/MTTR의 `supplements`, `replaces`, `reduces` 관계 추가
4. certificate assumption과 operating interval의 `constraint`, `minimum`, `optimal` 관계 추가
5. `sil_target_determination_risk_reduction_and_lifecycle` machine contract에 invariant binding 추가

필수 mutation:

- 올바른 `PFDavg_target = F_tolerable/F_unmitigated`와 잘못된 곱
- demand frequency 정의와 fault detection 정의의 교환
- PST가 일부 coverage를 제공한다는 정상문과 full test 대체/MTTR 자동 감소 오답
- 인증 조건을 설계 입력으로 검토한다는 정상문과 현장 최소주기 단정
- 부정·정정·오류 인용 문맥

Gate:

- SIL 운영 fatal 4/4 검출
- 해당 정상·정정 mutation false positive 0
- 기존 λ/PFD 차원 회귀 유지

### Stage36C — 안전 소프트웨어 오류 4종 결정론화

구현 순서:

1. MISRA=`coding_guideline`, xUnit/harness=`test_tool` 분류 추가
2. software test=`systematic_fault_control`, PFD/PFH/HFT=`random_hardware_integrity` 분류 추가
3. HFT=`hardware_architecture_constraint`, integration test=`test_level`, HIL=`test_environment` 분류 추가
4. `always/all/universal` 주장에 applicability qualifier가 없는 normative overgeneralization 검사 추가
5. SW-04, SW-05, MC/DC Topic Pack machine contract에 기존 fatal ID binding 추가

필수 mutation:

- 올바른 도구/표준/시험단계 매핑과 각 역할의 교환
- software systematic integrity와 random hardware integrity의 정상·오답 매핑
- HFT·voting architecture·integration test·HIL 역할 교환
- 특정 표준/Safety Plan 조건부 MC/DC 요구와 무조건 SIL4 100% 단정
- 표·bullet·한영 혼용·OCR 공백·부정·정정문맥

Gate:

- SW fatal 4/4 검출
- 정상·조건부·정정 mutation false positive 0
- multi-topic routing과 기존 owner fatal ID 보존

### Stage36D — Requirement 상태 결정론화

canonical evidence와 machine contract만 사용해 상태를 계산한다.

우선순위:

```text
verified contradiction/invariant violation -> WRONG
minimum required facts 충족             -> SATISFIED
일부 required facts 충족                 -> PARTIAL
관련 evidence 없음                       -> MISSING
해석 불충분                              -> UNKNOWN
```

규칙:

- LLM 상태 출력은 입력으로 사용하지 않는다.
- fatal과 연결된 requirement는 `SATISFIED`가 될 수 없다.
- fatal 존재 시 requirements 100%와 perfect-theory 문구를 금지한다.
- 동일 evidence를 B/C/D/E에 중복 감점하지 않는다.

Gate:

- Golden 30건 demand-state confusion matrix 생성
- known fatal requirement의 `WRONG` 전파 100%
- 동일 입력 10회 상태 fingerprint 일치 100%

### Stage36E — 점수·verdict deterministic owner

순서:

1. machine contract 결과를 canonical evaluation ledger에 기록
2. 단일-owner 감점과 fatal/core ceiling 적용
3. 최종 점수·score range·threshold flag 계산
4. fatal/pass/strong/full-credit 충돌 차단
5. 총평은 template으로 생성하고 선택적 LLM 문장이 판정을 바꾸지 못하게 고정

Gate:

- score/verdict consistency PASS
- fatal false pass/strong/high-score 0
- 반복 점수 fingerprint 100%
- shadow와 primary 차이의 원인 미분류 0

### Stage36F — Authority 전환과 운영 검증

1. Gemini-off 30건 replay를 두 번 실행
2. `scripts/check_deterministic_authority_gate.py --require-ready` 통과
3. shadow/legacy 비교 artifact를 고정하고 unexplained diff 0 확인
4. deterministic primary를 release candidate에서만 활성화
5. rollback switch와 이전 legacy 결과 비교 확인
6. image rebuild/recreate, container fingerprint, host parity, production replay, endpoint smoke 저장
7. 조건 충족 후에만 production 기본값과 Issue #1 상태 변경

## 4. 작업 단위와 커밋 원칙

각 커밋은 하나의 architectural boundary만 변경한다.

```text
36A taxonomy/schema
36B-1 expression dimension
36B-2 concept-role constraints
36B-3 activity/certificate constraints
36C-1 artifact/test classification
36C-2 integrity/architecture classification
36C-3 normative applicability
36D requirement evaluator
36E score/verdict owner
36F authority cutover
```

각 구현 커밋은 positive, fatal mutation, false-positive/정정문맥 테스트를 함께 포함한다. generated bank 변경은 source 변경과 분리해 기계적 rebuild 커밋으로 남긴다.

## 5. 매 단계 검증

```bash
python3 scripts/validate_topic_packs.py
bash scripts/validate_release.sh
python3 scripts/run_deterministic_replay_audit.py
python3 scripts/check_deterministic_authority_gate.py
```

- focused test 실패 시 다음 오류 유형으로 넘어가지 않는다.
- expected value 완화, fatal rule 삭제, fixture 삭제로 통과시키지 않는다.
- 정확도 Gate가 `HOLD`이면 primary 전환과 Docker 배포를 실행하지 않는다.
- 외부 모델 장애 시에도 이미 결정 가능한 결과와 evidence는 유지한다.

## 6. 진행 표시

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| Stage35 기반 | 완료 | evidence·ontology pilot·shadow·authority Gate |
| Stage36A | 완료 | fatal 8건 taxonomy/owner 확정 |
| Stage36B | 완료 | SIL 4/4 + false positive 0 |
| Stage36C | 완료 | SW 4/4, 전체 fatal 9/9 + false positive 0 |
| Stage36D | 완료 | invariant→`WRONG`, 불완전 해석→`UNKNOWN` |
| Stage36E | 완료 | deterministic score/verdict와 coverage 부족 `ABSTAIN` |
| Stage36F | Gate 완료·전환 HOLD | 2회 replay `STABLE`, score coverage 6.67% |

| Stage37A | 완료 | 미점수 28건과 Topic owner inventory |
| Stage37B | 완료 | 질문별 명시 contract 우선 Fact Anchor evidence adapter |
| Stage37C | 완료 | provider-free 개념 토큰 evidence와 weak-match 전체-anchor fallback |
| Stage37D | 완료·정확도 HOLD | score coverage 30/30, 적중률 43.33%, 평균 이탈 1.432667 |
| Stage37E | 완료·전환 HOLD | 권한 Gate 재평가 및 premature cutover 차단 |

| Stage38A | 완료 | 질문-only deterministic Topic router와 multi-topic alias evidence |
| Stage38B | 완료 | A/B/C/D/E provider-free score evidence |
| Stage38C | 완료 | full-chain Golden 30건 Accuracy·overgrading Gate `READY` |
| Stage38D | 완료 | 2회 exact replay `STABLE`, external provider call 0 |
| Stage39A | 완료 | production entrypoint의 feature flag와 현재-code READY 재검증 |
| Stage39B | 완료 | legacy grader·score adjudicator·finalizer·LLM 요약 우회 |
| Stage39C | 완료 | provider-neutral grade persistence와 rollback 기본값 |
| Stage39D | 완료 | container parity·production replay·rollback·실제 endpoint PASS |

Stage39D 운영 증거까지 완료했다. commit `1e343fc` 운영 container에서 deterministic primary가 활성화됐고, Telegram 세션 `20260907_041003_5960502198`과 `20260907_041028_5960502198`의 persisted raw/final marker·score·verdict·pass flag가 exact match했다. 저장소 예제 기본값은 rollback을 위해 `false`로 유지하고 실제 운영 `.env`만 `true`를 사용한다.

## 7. Stage42 — Canonical Claim 정확도 강화

Stage42는 Topic 수를 늘리지 않고 machine contract가 있는 모든 Topic에 동일한 claim
판정 경계를 적용한다.

```text
answer span
  -> subject / predicate / object / conditions / polarity
  -> asserted / quoted / rejected / corrected
  -> deterministic requirement evaluator
```

- `canonical_claim_extractor.py`가 global concept·predicate ontology와 routed Topic의
  machine contract를 결합한다. 특정 답안 전체 문자열은 규칙으로 사용하지 않는다.
- 명시적 반대 polarity와 contract 밖 관계 object는 `WRONG`, 최소 사실 미달은
  `PARTIAL`, evidence 부재는 `MISSING`으로 분리한다.
- `quoted`와 `rejected` claim은 정답 credit과 오류 판정에서 제외하고, 최종 정정
  claim만 `corrected` evidence로 채택한다.
- claim 하나는 한 requirement에만 배정한다. 인접 절의 concept를 교차 결합하지
  않으며 배정 결과에 `duplicate_credit_count=0`을 기록한다.
- deterministic parser가 해석하지 못한 경우 `UNKNOWN`, score engine은 이를
  `ABSTAIN`으로 유지한다. optional semantic resolver도 conditions와
  assertion context를 명시해야 하며 score·status·fatal 권한은 계속 0이다.

현재 정밀 relation coverage는 additive `machine_contract`가 있는 Topic부터 적용한다.
나머지 Topic의 Fact Anchor lexical evidence는 기존 회귀를 유지하고, 실제 오분류가
확인된 Topic부터 machine contract를 추가한다. Topic Pack 전체 일괄 migration은 하지
않는다.

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| Stage42A schema/context | 완료 | condition·assertion context provider-neutral 계약 |
| Stage42B extractor | 완료 | global ontology + routed contract, provider call 0 |
| Stage42C evaluator | 완료 | 상태 precedence·claim 단일 배정·UNKNOWN 보존 |
| Stage42D mutation | 완료 | 정상·부분·오답·인용·정정·교차절·반복성 회귀 |
| Stage42E release | 완료 | 30건 replay `READY`·2회 `STABLE`·전체 release·GitHub Actions PASS |

## 8. Stage43 — V-Model Fact Anchor canonical 승격

Stage43은 실제 과대평가 사례(과거 20.57점)를 첫 lexical-to-canonical 전환
fixture로 고정한다. V-Model, 시험수준, V&V, RTM, baseline의 8개 핵심 anchor는
관계와 필수 세부 사실을 machine contract로 판정한다.

- 질문의 `required_anchor_ids`만 활성화해 좁은 질문에 불필요한 요구를 부과하지 않는다.
- 동일 anchor에서는 canonical 상태가 lexical 상태보다 우선한다.
- lexical/canonical 상태 차이는 promotion 비교 evidence로 보존한다.
- 정상 완전답안, 역사적 과대평가 답안, 관계 부정 mutation, 인접 개념 교차결합을
  focused regression으로 고정한다.
- 특정 답안 문자열이나 V-Model 전용 점수 cap은 사용하지 않는다.

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| Stage43A contract | 완료 | 8개 anchor의 canonical fact·minimum 관계 정의 |
| Stage43B scope/promotion | 완료 | question scope 제한·canonical 우선·비교 evidence |
| Stage43C regression | 완료 | 과대평가·정상·오답·교차결합 회귀 |
| Stage43D release | 완료 | 30건 `READY`·2회 `STABLE`·Authority `READY`·전체 release PASS |

## 9. Stage44 — SIL 목표 결정 원본·교정 쌍 승격

Stage44는 기존 fatal 검출만 보호하던 SIL 목표 결정 machine contract를 정상 교정
관계까지 확장한다. 원본의 오류 판정과 교정 답안의 정상 판정을 동시에 고정한다.

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| Stage44A audit | 완료 | 원본 4 fatal·교정 PFD 비율 false negative 확인 |
| Stage44B contract | 완료 | scope·RRF·achieved SIL·MOC·AI/OT 7 anchor canonical 승격 |
| Stage44C mutations | 완료 | 원본/교정·비율 표기·PST 부정표면형·AI 통제 부정 회귀 |
| Stage44D release | 완료 | Topic 생성물·30건 `READY`·2회 `STABLE`·Authority `READY`·전체 release PASS |

## 10. Stage45 — HAZOP/LOPA 운영 회귀 canonical 승격

Stage45는 canonical 비교가 0이던 반응기 과압력 운영 fixture를 9개 원자 requirement로
전환한다. Global FSRM fatal owner는 유지하고 Topic-local coverage만 승격한다.

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| Stage45A audit | 완료 | 9개 lexical anchor·global fatal owner·0 comparison 확인 |
| Stage45B contract | 완료 | scenario→IPL→RRF/PFD→SIF/SRS 9개 관계 정의 |
| Stage45C parser/evaluator | 완료 | OCR 줄바꿈·점 포함 식·주어 소유·다중 fact 순서 독립성 |
| Stage45D regression | 완료 | 역사적 12.42점·정상 9/9·부분·오답·질문범위 회귀 |
| Stage45E release | 완료 | Topic 생성물·30건 replay READY·stability STABLE·authority READY·전체 release PASS |

## 11. Stage46 — MC/DC 복합 운영 회귀 canonical 승격

전문가 승인된 MC/DC–V-Model–SIL 복합 회귀를 이용해 MC/DC의 목적·독립영향·100%
한계·수명주기 경계와 일반 정적·동적 분석을 canonical 관계로 판정한다. 기존 네 fatal
owner와 `10.5~14.5`점 승인 범위는 유지한다.

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| Stage46A audit | 완료 | 3개 Topic·4 fatal·기존 canonical 비교 8건 확인 |
| Stage46B contract | 완료 | MC/DC 4관계와 정적·동적 분석 2관계 승격 |
| Stage46C regression | 완료 | 역사적 10.83점·4 fatal·정상·부정·질문범위 mutation |
| Stage46D release | 완료 | Topic 생성물·30건 replay READY·stability STABLE·authority READY·전체 release PASS |

다음 Stage에서는 복합 질문을 원자 요구축으로 좁힐 때 `WRONG` 비율이 과도하게
증폭되는 점수 정규화를 먼저 교정한다. 이 경계를 고치기 전에는 정확한 질문 scope
계약을 추가해 승인 점수 범위를 깨뜨리지 않는다.
