# Fact Anchor Chat 심사 장부 — 2026-11-01

원천: `reports/remaining_fact_current_queue_20261030.csv` (GitHub work branch). 판정 보고서: `fact_anchor_chat_review_20261101.md` (Batch A), `fact_anchor_industry_scope_batch_b_20261101.md` (Batch B), `fact_anchor_industry_scope_batch_c_20261101.md` (Batch C).

| 지표 | 건수 |
|---|---:|
| 현행 Registry | 1,520 |
| 현행 Queue | 1290 |
| 검토 보고서와 연결된 개별 Fact | 129 |
| 이번 Chat에서 미검토 | 1161 |
| 이 Chat에서 Registry 수정·실제 삭제 | 0 |

Batch A 20, Batch B 38, Batch C 71. ID 중복 및 Queue 미존재 0건. **Chat 판정은 기존 Registry의 `verified` 승인에 대응하는 신규 사실 인증이 아니며**, 표준 전문·모든 제품자료를 개별 완독한 뜻도 아니다. 분류 상세: `GENERALIZE_PRODUCT_CASE` 10, `GENERAL_KEEP` 87, `GENERAL_VERIFIED` 8, `HOLD` 1, `HOLD_ANNEX_DETAIL` 2, `HOLD_MIXED_CLAIM` 1, `NARROW_OR_CORRECT` 2, `REMOVE_GENERIC_CORE` 5, `REMOVE_PRODUCT_NUMERIC` 2, `SCOPE_KEEP` 9, `STANDARD_SCOPE_KEEP` 2.

- [행별 장부](fact_anchor_chat_ledger_20261101.csv)의 `batch` 비어 있음과 `chat_verdict=NOT_REVIEWED`는 실제 미검토를 뜻한다.
- `GENERAL_KEEP` 등은 공학 원리 적합성 후보. `SCOPE_KEEP`는 해당 표준/제품 문맥만. `REMOVE_GENERIC_CORE` 및 `REMOVE_PRODUCT_NUMERIC`은 **채점 근거 제외 권고**이며 Registry 삭제 수행 상태가 아니다.
- 실제 변경은 Topic별 source, required anchor, model answer, logic, golden과 승인/source-hash를 동시에 검토하고, **CLI로만 generated 승격**, 모든 release gate 후 단계별 커밋하는 별도 실행이다.
- 운영 checkout, 로컬 두 미커밋 파일, 컨테이너는 건드리지 않았다.

현행 Queue 1,290건과 최초 과거 1,272건 스냅샷은 **다른 집계**다. 2 제거·5 근거 대조 후 유지·1,265 미확인 과거 기록은 변경하지 않는다.
