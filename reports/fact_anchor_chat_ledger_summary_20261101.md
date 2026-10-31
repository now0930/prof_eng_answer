# Fact Anchor Chat 검토 통합 장부 (2026-11-01)

- 현행 Registry: 1,520 Fact; 현행 작업 Queue: 1290 Fact.
- **검토 메모를 가진 서로 다른 Fact ID: 183건** (Batch A 20 / B 38 / C 71 / D 54). 미검토 1107건. ID 중복 또는 Queue 불일치 0건.
- 상태별 장부: `APPLICATION_SCOPE` 8, `GENERALIZE_PRODUCT_CASE` 10, `GENERAL_KEEP` 132, `GENERAL_VERIFIED` 8, `HOLD` 1, `HOLD_ANNEX_DETAIL` 2, `HOLD_MIXED_CLAIM` 1, `NARROW_OR_CORRECT` 2, `REMOVE_GENERIC_CORE` 5, `REMOVE_PRODUCT_NUMERIC` 2, `SCOPE_KEEP` 9, `SCOPE_NARROW` 1, `STANDARD_SCOPE_KEEP` 2.
- 최초 2026-10-30의 1,272 스냅샷(2 제거/5 대조 후 유지/1,265 미확인)과 **다른 분모**. 과거 이력은 소급 수정하지 않음.
- ***경고:*** 장부의 `chat_verdict`는 독립 원문 검증 완료/기존 `verified` 재승인/제품 사양 인증/Registry 반영 상태가 아님. `NOT_REVIEWED`는 아직 분석하지 않은 Fact. 모든 행의 `source_verified_by_this_ledger=NO`와 `registry_update=NOT_PERFORMED`는 장부 자체의 승인/수정 부재를 뜻한다.
- 검토 보고서: [Batch A](fact_anchor_chat_review_20261101.md), [Batch B](fact_anchor_industry_scope_batch_b_20261101.md), [Batch C](fact_anchor_industry_scope_batch_c_20261101.md), [Batch D](fact_anchor_industry_scope_batch_d_20261101.md).
- [행별 CSV](fact_anchor_chat_ledger_20261101.csv).
- 지엽적인 제품·기관 사례는 `REMOVE_GENERIC_CORE`/`REMOVE_PRODUCT_NUMERIC`/`GENERALIZE_PRODUCT_CASE` 등의 권고로 분리. **실제 삭제·Pack 동기화·CLI generated·release/validate-all은 미실행.** 로컬 미커밋 두 파일, 운영 checkout, 컨테이너 보존.
