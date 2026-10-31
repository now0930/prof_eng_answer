# Fact Anchor Chat 검토 전체 현황 및 적용 대기 — 2026-11-01

## 1. 기준선·무변경 원칙

- 작업 대상 `now0930/prof_eng_answer`, 브랜치 `codex/essay-boundary-calibration-20261028`. 내용 검토 시작 기준 `b8c6eba`.
- 현행 Registry **1,520건**. 최초 1,272건 재검토 판정 **2건 제거, 5건 근거대조 유지, 1,265건 미확인**은 과거 스냅샷으로 보존. 별도의 2026-10-30 현행 Queue는 **1290개 Fact ID**이며 두 집계는 동일 모집단이 아님.
- Source Topic Packs, 검증 상태, Review Queue, 채점 기준, Generated/Registry에는 **변경 없음**. Chat 검토 보고서가 `verified`/승인·삭제의 효력을 갖지 않는다.

## 2. 전수 ID 커버리지와 입증 범위

- Queue에 등장한 모든 **1290/1290개 Fact ID가 최소 1개 Batch A~K의 Markdown 판정 행에 포함됨**. 점검 결과 **누락 ID 0건**.
- A~I 일부는 기술적 원리/공식 공개자료를 원문과 대조한 **개별 조건부 검토**이다. J~K는 출처/표준판본·기계 원리·문장 자체의 위험을 기준으로 한 **예비 적합성 선별**이며 실제 외부 원문 대조를 개별로 완료한 것이 아니다. **1,290건 전부의 사실 인증 완료라는 표현은 금지**.
- `CORE*` 또는 `GENERAL*` 상태도 내용 채점 후보라는 뜻일 뿐, 현행 1,520개의 `verification_status=verified`를 소급 확인한 결과가 아니다.

| 파일 | 보고서 내 Queue 고유 ID 수 |
|---|---:|
| [`fact_anchor_chat_review_20261101.md`](fact_anchor_chat_review_20261101.md) | 20 |
| [`fact_anchor_chat_review_20261101_batch_b.md`](fact_anchor_chat_review_20261101_batch_b.md) | 56 |
| [`fact_anchor_chat_review_20261101_batch_c.md`](fact_anchor_chat_review_20261101_batch_c.md) | 43 |
| [`fact_anchor_chat_review_20261101_batch_d.md`](fact_anchor_chat_review_20261101_batch_d.md) | 86 |
| [`fact_anchor_chat_review_20261101_batch_e.md`](fact_anchor_chat_review_20261101_batch_e.md) | 82 |
| [`fact_anchor_chat_review_20261101_batch_f.md`](fact_anchor_chat_review_20261101_batch_f.md) | 123 |
| [`fact_anchor_chat_review_20261101_batch_g.md`](fact_anchor_chat_review_20261101_batch_g.md) | 95 |
| [`fact_anchor_chat_review_20261101_batch_h.md`](fact_anchor_chat_review_20261101_batch_h.md) | 125 |
| [`fact_anchor_chat_review_20261101_batch_i.md`](fact_anchor_chat_review_20261101_batch_i.md) | 130 |
| [`fact_anchor_chat_review_20261101_batch_j.md`](fact_anchor_chat_review_20261101_batch_j.md) | 294 |
| [`fact_anchor_chat_review_20261101_batch_k.md`](fact_anchor_chat_review_20261101_batch_k.md) | 255 |

중복 재검토가 있으므로 각 배치 합계는 1,290보다 클 수 있다. ID 합집합으로 검증해야 한다.

## 3. 채점 적합성 우선순위

- [`fact_anchor_scoring_scope_candidates_20261101.md`](fact_anchor_scoring_scope_candidates_20261101.md)에 **총 276개**의 조치 후보: **일반 채점 비핵심 190**, **규격/관할 범위 한정 66**, **중복 통합 17**, **문구 수정 3**.
- 특히 제거/설명자료 이동 후보는 Oracle ZDM switchover, Fisher/Siemens/NI/AVEVA/MLflow 등의 제품 세부 및 NASA/DoD/HHS 기관 내부 분류. 거짓으로 단정하지 않으며 일반 기술사 필수 채점에서 제외 후보로 처리.
- 수정 우선: (1) Cryogenic Extension Bonnet의 Actuator 전체 보호/보편 Vapor Space 주장, (2) Min/Normal/Max 3개 운전점 무조건 의무, (3) 모든 유동상태의 필수 물성 입력 고정.
- 별도 보류: IEC 62382 Annex 예시 시험점, IEC 60534 Annex A reduced-trim 수치 등 표준 전문 미열람 세부 조건.

## 4. 진짜 Fact 검증 완료에 필요한 조건

1. **원문 사실/기술 주장과 물리적 또는 표준 근거를 개별 대조**하고 인용 위치·판본·조건과 함께 증거를 남긴다.
2. 기준 적합하지 않은 세부 Fact는 관련 Topic Pack의 Core 채점·모범답안·Logic·테스트에서 어떤 역할인지 확인하고, 보편 원리로 통합하거나 일반 채점에서 제외한다. **선별 모델 판정만으로 승인/삭제하지 않는다.**
3. Source 내용 변경 후 Generated는 **프로젝트 제공 CLI로만 갱신**한다. 이미 승인된 Topic ID/Grading contract를 보호한다.
4. 로컬 `README.md`, `docs/operational_quality_checksheet.md`의 사용자 미커밋 작업은 반드시 보존하고 `git add .` 금지.
5. 우선 관련 집중 pytest → 전체 `validate_release.sh` → `validate-all` 수행 후 단계별 커밋/Branch Push. 이 Chat 환경에서는 로컬 명령/컨테이너 실행을 하지 않았으며 **테스트 PASS로 기록하지 않는다**.
6. 운영 checkout `/home/now0930/hermes/workspace/prof_eng_answer` (`a77d29f` 기준으로 알려짐)과 배포·재시작은 별도 작업으로 취급한다.

## 5. 이번 GitHub 변경의 정확한 효력

- 새로 추가된 문서는 Fact Anchor의 산업 공통성·범위 제한·검토 필요 사유를 추적할 수 있도록 한 **내용 검증 자료**다.
- 원본 Registry의 1,520개 기존 Verified 상태는 이미 별도 승인된 상태이며, Chat 검토 결과로 그 타당성을 보증하지 않는다.
- **전체 ID의 예비 분류는 완료됐으나 전 항목 공식 원문 대조, 원본 Fact 삭제/수정, CLI 회귀 검증, 운영 배포는 완료되지 않았다.** 이 경계를 넘는 완료 주장은 하지 않는다.
