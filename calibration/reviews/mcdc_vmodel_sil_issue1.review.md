# Golden Review: mcdc_vmodel_sil_issue1

상태: `APPROVED`

근거:

- `calibration/mcdc_vmodel_sil_overgrading_regression.json`
- V-Model, SIS/SIL software, MC/DC Topic Pack의 `logic_check.json`
- `question_demand_contract.py` atomic demand v3 결과

## 요구축 교정

기존 `PI_LOW_02_D1~D6`는 문제문의 원자 요구가 아니라 과거 QType rubric 축이므로
정확도 benchmark의 demand label로 사용할 수 없다. 문제문에서 추출한 아래 8개
canonical 요구로 교체한다.

| Canonical 요구 ID | 요구 | 제안 상태 | 근거 |
|---|---|---:|---|
| requirement_97637d466c64 | V-Model | PARTIAL | 장단점만 있고 개발단계-시험단계 대응과 추적성이 없음 |
| requirement_865945aea80e | 단위 시험 | WRONG | xUnit은 적합하나 MISRA와 Random Integrity를 단위시험에 직접 대응함 |
| requirement_e3f0fc834975 | 통합 시험 | WRONG | Stub 언급은 있으나 HFT를 통합시험 축으로 잘못 대응함 |
| requirement_4f9becba0a03 | 시스템 시험 | PARTIAL | 전체 SIS·HIL은 언급했으나 acceptance·요구사항 validation이 부족함 |
| requirement_c34b039a9f24 | 정적 분석 | PARTIAL | MISRA·정적분석을 언급했으나 목적·검출범위·한계가 부족함 |
| requirement_562ee2080922 | 동적 분석 | PARTIAL | 동적분석·fault injection을 언급했으나 대상·oracle·target 대표성이 부족함 |
| requirement_461938514cd3 | MC/DC | WRONG | SIL 3/4에 MC/DC 100%를 일률 적용하고 Systematic Integrity 증명처럼 취급함 |
| requirement_e7768e02db0c | SIL 검증방안 | WRONG | Random Hardware Integrity·HFT·software V&V 범주를 혼동하고 V-Model을 SIL 증명 수단으로 과대평가함 |

## Finding 제안

유지:

- `sw04_fatal_misra_is_unit_test_tool` — fatal
- `sw05_fatal_software_test_is_random_hardware_integrity` — fatal
- `sw05_fatal_hft_is_integration_test` — fatal
- `sil_four_universal_rule` — fatal

제외:

- `mcdc_proves_requirements`: 답안은 요구사항 완전성·정확성을 증명한다고 직접 주장하지 않음
- `sw04_fatal_general_vv_proves_sil`: 별도 Safety lifecycle 불필요를 명시적으로 주장하지 않음

## 점수·판정 제안

- score range: `10.5–14.5` 유지
- passing: `false` 유지
- strong: `false` 유지
- confidence ceiling: `medium` 유지
- canonical Question Type: `IMPLEMENTATION_EVALUATION`로 교정

## 승인 기록

- reviewer: `workspace_owner`
- reviewed_at: `2026-09-02T05:32:19+09:00`
- method: `user_approval`
- decision: 승인
- notes: Golden JSONL과 회귀 fixture에 승인된 교정을 반영했다.
