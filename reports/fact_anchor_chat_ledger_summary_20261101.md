# Fact Anchor Chat 검토 통합 장부 — 2026-11-01

- **현재 Registry** 1,520건, **현행 Queue** 1,290건. Chat에서 개별 내용 판정이 기록된 현행 Queue Fact **242건**, 현행 Queue 미검토 **1048건**.
- Batch A 20, B 38, C 71, D 54, E 69개 독립 Fact 재검토(현행 Queue에 속한 E 59 + 과거 검토 항목 재점검 10). **현행 Queue 총 처리량은 242건이며 과거 검토 항목 10은 중복 합산하지 않는다.**
- 상태별 현행 Queue 검토 판정: `APPLICATION_SCOPE` 8, `GENERALIZE_PRODUCT_CASE` 10, `GENERAL_KEEP` 132, `GENERAL_VERIFIED` 8, `HOLD` 1, `HOLD_ANNEX_DETAIL` 2, `HOLD_MIXED_CLAIM` 1, `KEEP_GENERAL` 50, `NARROW_OR_CORRECT` 2, `REMOVE_GENERIC_CORE` 5, `REMOVE_PRODUCT_NUMERIC` 2, `SCOPE_KEEP` 9, `SCOPE_NARROW` 1, `SCOPE_ONLY` 9, `STANDARD_SCOPE_KEEP` 2.
- [행별 장부](fact_anchor_chat_ledger_20261101.csv), [Batch A](fact_anchor_chat_review_20261101.md), [B](fact_anchor_industry_scope_batch_b_20261101.md), [C](fact_anchor_industry_scope_batch_c_20261101.md), [D](fact_anchor_industry_scope_batch_d_20261101.md), [E](fact_anchor_industry_scope_batch_e_20261101.md).
- [제품별 Fact 채점 제외/치환 후보](fact_anchor_product_specific_change_candidates_20261101.md): Pack 비교에서 Registry 단독 제품 사례 제거 후보 4건, Core/Important 문구 동시 수정 후보 7건. 별도 혼합 Fact 1건 보류.

## 반드시 구분할 것
- Chat 판정 `GENERAL_KEEP` / `KEEP_GENERAL`은 **수식·물리원리·범용성 1차 검토**이지 표준 전문 완독, 신규 Registry `verified` 인증이나 실제 삭제를 뜻하지 않는다.
- `SCOPE_ONLY` / `APPLICATION_SCOPE` / `REMOVE_GENERIC_CORE` / `REMOVE_PRODUCT_NUMERIC` / `GENERALIZE_PRODUCT_CASE`는 지엽적 제품·기관 사례를 **보편 필수 채점에서 빼거나 일반원리로 치환**하라는 권고.
- 최초 1,272건 스냅샷의 2 제거·5 근거 대조 후 유지·1,265 미확인은 다른 시점·분모의 역사적 기록이므로 소급 갱신하지 않는다.
- Registry·Topic Pack·generated·score 실제 변경 **0건**. Source-hash/승인 갱신, CLI-generated, pytest, validate-all, full release gate **미실행**. 로컬 README 및 운영 checksheet 사용자 미커밋 변경, 운영 checkout·컨테이너는 모두 미변경.
