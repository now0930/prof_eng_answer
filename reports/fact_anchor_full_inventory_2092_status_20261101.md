# 전체 Topic Pack Anchor / Fact Registry 최신 현황 — 2026-11-01

> **검토·재분류 보고서이며, 채점기 승인 또는 릴리스 완료 선언이 아니다.** 
> 작업 브랜치: `codex/essay-boundary-calibration-20261028`; 기준 HEAD(본 보고서 작성 직전): `1a99e6b411696f712344b2c8ff4093636d4f263d`.
> 159건 대조 기준선: `2629eb95`. 모든 판정은 **산업적으로 일반화 가능한 물리적 사실·공식 기술문서·범위가 특정된 표준**에 한해 해석한다. 제조사 기능, 관할/판본별 의무, 좁은 예시는 보편적인 기술사 채점 필수 사실로 자동 승인하지 않는다.

## 1. 모집단 정의와 현재 크기

| 서로 다른 집계 단위 | 건수 | 근거·해석 |
|---|---:|---|
| **전체 Topic Pack Anchor** | **2,092** | 현재 브랜치의 `rubrics/topic_packs/*/fact_anchor.json` 89개를 읽어 `anchors` 개수를 합산. 기술 주장과 구조/범위 Anchor를 함께 포함 |
| 전체 Topic Pack 파일 수 | 89 | 실재하는 `fact_anchor.json` 기준 |
| 과거 전수 Anchor 스냅샷 | 2,073 | 2026-10-12, 86개 Topic, `docs/all_topic_fact_source_audit.md` |
| 과거 대비 순증 | +19 | `2,092 - 2,073`. 세 신규 Topic(Displacer 7 / Open-channel 5 / Gyroscope 5) 외 기존 Topic의 순변동도 포함 |
| 승인 이력 Registry | **1,520** | `reports/remaining_fact_current_summary_20261030.json`의 현행 Registry 스냅샷. **기존 상태값은 재인증이 아님** |
| 재검토 Queue | **1,290** | `reports/remaining_fact_current_queue_20261030.csv`와 독립 감사의 고유 Fact ID |
| Registry 중 과거 검토 이력 | 230 | `1,520 - 1,290`; 금번 Queue에 들어 있지 않으며 이번 검증으로 소급 승인·재인증하지 않음 |

**서로 더하지 말 것:** 1,290건 Queue는 Registry 1,520건의 하위 집합이고, 두 집계 모두 2,092개의 전체 Anchor와 동일한 단위가 아니다. Registry Fact ↔ Anchor 관계 및 구조 Anchor 때문에 2,092에서 바로 '승인/미승인'을 빼면 안 된다.

### 과거 미승인 기술 Anchor

`docs/all_topic_fact_source_audit.md`의 2026-10-12 후속 검토는 당시 **490개 기술 Anchor를 근거 부족·과잉 일반화 등의 이유로 미승인** 상태로 두었다. `reports/unresolved_technical_anchor_reviews_20261012.json`에는 총 491행(그중 1행은 이후 Registry 승격 이력)이 있다. 이는 최신 1,290건 Queue와 다른 과거 분류 자료이며, 최신 Anchor/Registry의 정합성 재대조 없이 **490건을 새로운 잔여 Fact로 합산하지 않는다**. 구조용/범위용 Anchor의 당시 기록(구조 51, scope 확인 18, owner 미확인 1)도 기술 사실 인증과 별개다.

## 2. 1,290개 Fact ID의 최신 보고서상 판정

아래는 `2629eb95` 당시 159개 **원문 검토 대기**를 정확히 식별하고, 이후 작성한 [159개 개별 판정 장부](fact_anchor_source_159_decision_ledger_20261101.csv)로 **동일 Fact ID 159개만** 갱신한 대조 결과다. 159개의 중복·누락은 0건이며, 기존 다른 1,131개 ID는 감사 CSV의 판정을 그대로 유지한다.

| 최신 보고서 판정 | 건수 | 일반 채점·후속 취급 |
|---|---:|---|
| `KEEP_BOUNDED` | **862** | **조건부 유지 후보**, 원문 주장 범위/정확한 근거와 캐노니컬 소유권을 확인해야 함; 자동 승인 아님 |
| `EXCLUDE_FROM_GENERAL_SCORING_ONLY` | **275** | 일반 기술사 필수 채점에서 제외 |
| `KEEP_AS_SCOPED_ONLY_NOT_GENERAL_SCORING` | **1** | 한정된 문맥에서만 사용 |
| `REVISE_REQUIRED` | **80** | 원문·Topic Pack·근거 수정 필요 |
| `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE` | **50** | 직접 원문 근거/범위 확보 전 보류 |
| `SOURCE_CHECKED_SCOPED_STANDARD_HOLD` | **11** | 판본·조항·관할 범위 한정, 일반 필수 채점 불가 |
| `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD` | **11** | 제조사/모델/적용 사례 범위 한정, 일반 필수 채점 불가 |
| **합계** | **1,290** | |

**원문 검토 미기재 Fact ID = 0건(159개 대상 검토 장부 기준)**이라는 뜻이지, **검증·승인 완료 1,290건** 또는 **핵심 채점 승인 862건**이라는 뜻이 아니다. 152개 수정/보류(80+50+11+11)에 대한 후속 조치는 아래 CSV로 소유자를 추적한다.

- **전수 판정 대조 CSV:** [`fact_anchor_1290_latest_review_reconciliation_20261101.csv`](fact_anchor_1290_latest_review_reconciliation_20261101.csv) — 원 기준선·기존 감사 상태·최신 보고서 상태·근거 보고서·승인 금지와 게이트 미실행 여부, 고유 Fact 1,290건.
- **후속 조치 152건:** [`fact_anchor_1290_open_actions_152_20261101.csv`](fact_anchor_1290_open_actions_152_20261101.csv) — Fact ID/Topic/Anchor별 수정/보류 유형과 필요한 조치.
- **159건 원문 검토 요약:** [`fact_anchor_source_159_closure_20261101.md`](fact_anchor_source_159_closure_20261101.md) — KEEP 125 / REVISE 13 / 근거부족 14 / 표준한정 4 / 제조사한정 3.

## 3. 최신 보고서와 현재 실행 데이터는 **서로 다르다**

커밋 이전의 업무 브랜치 실행 파일은 **최신 159건 보고서를 아직 반영하지 않았다**. 다음 수치는 사용자에게 혼동을 주지 않도록 별개로 유지한다.

| 기존 실행/관리 파일 | 실제 존재하는 상태 | 최신 보고서와 차이 |
|---|---|---|
| `reports/fact_anchor_independent_verification_audit_20261101.csv` | `PENDING` **115**, `KEEP` **779**, `REVISE` **67**, 불충분 **38**, 표준한정 **7**, 제조사한정 **8**, 일반제외 **275**, 범위한정 **1** | 159건 최종 검토 장부를 덮어쓰지 않은 감사 시점 스냅샷 |
| `grading/evidence/fact_anchor_unresolved_source_holds_20261101.json` | **197**보류 = 원문 검토 대기 **145**, 근거부족 **37**, 표준한정 **7**, 제조사한정 **8** | 최신 대조 장부와 동일 시점이 아님 |
| `grading/evidence/fact_anchor_independent_revision_holds_20261101.json` | **67** 수정 보류 | 최신 보고서의 80건과 미동기화 |
| `grading/evidence/fact_anchor_scoring_exclusions_20261101.json` | **276** 일반채점 제외 키 | 275 일반제외 + 별도 범위한정 1이라는 감사 판정과 같은 집합/판정 범위인지 실행 코드로 확인 필요 |
| Registry / Topic Pack / generated bank / 채점기 | 기존 캐노니컬 상태 | 이번 보고서 정리만으로 보증·수정·재생성·승인하지 않음 |

**원칙: 차이를 맞춘다고 보류 플래그를 일괄 해제하지 않는다.** 
특히 새 장부의 `KEEP_BOUNDED`는 원문 조항·판본·조건·문구를 충족해 해당 Fact가 캐노니컬 채점에 안전하게 승격되었다는 신호가 아니다. 기존 fail-closed 차단은 재검증, 관리형 원본 수정, 테스트 및 릴리스 확인 전까지 유지한다.

## 4. 실제 다음 처리 순서

1. **수정·보류 152건**: 80개는 최소한의 보편적이고 물리적으로 정당한 문구로 수정 후 근거 재대조; 50개는 직접 근거를 찾거나 일반 채점 요구에서 제외; 22개 표준/제조사 한정은 **보편 채점 불가**를 유지한다.
2. **490개 과거 미승인 Anchor의 최신 대조**: 현재 89개 Pack/2,092 Anchor와 owner·anchor_id를 조인하여 과거 미해결, 수정/교체, 구조 전환, 신규 내용을 가려낸다. 최신 미검증 건수를 추정으로 채우지 않는다.
3. **캐노니컬·채점 소유권 수선**: Registry·Topic Pack 원문·Model Answer·Logic Check·임시 보류를 묶어 조정한다. 기본 채점 A–C의 결정론적 우선권과 D–E 권고/프로그램 확정권, fatal 및 Topic ID/Question contract는 보호한다.
4. **실행 검증**: 프로젝트의 managed CLI로만 generated 뷰를 재생성하고 정확한 해당 테스트를 실행한다. `python3 scripts/rubric_manager.py validate-all`, `PROMOTE_GENERATED=0 scripts/validate_release.sh`, 관련 `pytest`와 전체 release gate의 실제 결과를 확인한다.
5. **게이트 통과 후 통합**: 이 보고서 생성에서는 GitHub 연결을 통한 자료/장부 커밋만 수행하며, 로컬 전체 회귀검증·운영 배포·main 병합을 **수행하지 않았다**.

**이번 커밋에 의한 변경 범위**: `reports/` 및 현황 안내 문서만. 실행 가능 보류·Registry·Topic Pack·generated bank·채점 점수·테스트 기준 변경 없음. Release Gate **NOT RUN**. 따라서 **승인 완료나 PASS를 주장하지 않는다**.
