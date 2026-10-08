# SIL 결정 Topic Pack: Anchor별 사실 검증 (2026-10-08)

대상: `sil_target_determination_risk_reduction_and_lifecycle/fact_anchor.json`의 16개 Anchor. 이 문서는 공개된 IEC·HSE·CCPS/AIChE의 1차 자료와 수식의 차원 검사를 이용한 **내용 감사 기록**이다. WordPress 원문 승인, 전체 2,073개 Anchor 검증, 현장 SIF 적합성 인증을 뜻하지 않는다. 판정은 `확인`, `수정`, `추가 근거 필요`로 분리했다. `수정`은 이 감사에서 원문을 고쳤다는 뜻이며 아래 근거에 대조했다.

| Anchor ID | 판정 | 검증 내용·경계 | 근거 |
| --- | --- | --- | --- |
| `sis_sif_sil_scope` | 확인 | SIS는 SIF를 수행하고 평가는 개별 SIF 경계로 한다. 인증 부품만으로 전체 SIF의 SIL을 주장할 수 없다. | [IEC 61511-1 미리보기][iec], [HSE 제어시스템][control] |
| `hazard_scenario_boundary` | 확인 | LOPA는 하나의 원인-결과 쌍을 대상으로 하며 SIF는 정의된 안전상태를 가져야 한다. | [CCPS LOPA][lopa], [IEC 61511-1 미리보기][iec] |
| `tolerable_risk_alarp` | 확인 | 허용위험 기준을 먼저 정하고 ALARP에서 good practice와 추가 조치를 검토한다. 단순 비용편익 최대화가 아니라 현저한 불균형을 입증해야 한다. 단, 허용 기준값은 보편 상수가 아니다. | [HSE ALARP 설명][alarp], [IEC 61511-1 미리보기][iec] |
| `method_selection` | 추가 근거 필요 | Risk graph·LOPA·QRA의 대략적 역할은 확인했다. 그러나 calibrated risk graph와 safety layer matrix를 언제·어떻게 조직 자료로 보정하는지까지 현 공개 근거만으로 일괄 확정하지 않는다. | [CCPS LOPA][lopa], [CCPS LOPA 도서][lopa_book] |
| `initiating_frequency_modifiers` | 확인 | 해당 시나리오에 유효하고 조직의 위험 기준과 일관된 enabling condition/conditional modifier에 한해 곱한다. 모든 LOPA에 무조건 적용하지 않는다. | [CCPS modifier 지침][modifiers] |
| `existing_ipl_independence` | 확인 | IPL credit은 시나리오에 대한 기능·독립성·신뢰성·감사가능성 등을 확인해야 한다. 공유 자원은 독립성 주장에 영향을 준다. | [CCPS LOPA][lopa] |
| `residual_frequency_before_sif` | 확인 | 시나리오별 IE 빈도와 유효한 IPL PFD의 곱으로 SIF 이전의 결과 빈도를 산정한다. 동일 완화효과의 이중 반영 금지는 계산상 추론이며, 조건부 인자와 consequence 분류의 중복도 확인한다. | [CCPS LOPA][lopa], [CCPS modifier 지침][modifiers] |
| `required_rrf_relation` | 확인 | `F_residual > F_tolerable`일 때 `RRF_required = F_residual / F_tolerable`; 두 빈도의 비이므로 무차원. 이는 CCPS 빈도 결합식에서 도출한 식이다. | [CCPS LOPA][lopa] |
| `target_pfd_relation` | 확인 | 저요구 모드에서 `F_residual × PFDavg ≤ F_tolerable`을 정리하면 `PFDavg_target ≤ F_tolerable / F_residual`; 빈도의 곱은 차원이 맞지 않는다. | [CCPS LOPA][lopa], [HSE 제어시스템][control] |
| `sil_band_mapping` | 확인 | PFDavg/PFH의 모드별 SIL band를 구분하고 목표 등급과 실제 SIF 달성 여부를 별도로 평가한다. 조직별 rounding은 적용 규칙을 기록해야 한다. | [IEC 61511-1 미리보기][iec], [HSE 기능안전 검사 지침][inspection] |
| `demand_mode_metric_selection` | 확인 | 모드와 지표는 요구 양식에 따라 다르며 고장 검출 시점으로 분류하지 않는다. 저요구에는 PFDavg, 고요구·연속에는 시간당 위험고장 빈도 지표를 적용한다. | [IEC 61511-1 미리보기][iec], [HSE 제어시스템][control] |
| `achieved_sil_verification` | 확인 | 센서부터 최종요소까지의 전체 SIF, 고장률·진단·시험·수리·공통원인 등 설계 가정을 검증한다. 단일 인증품 등급은 달성 SIL의 충분조건이 아니다. | [IEC 61511-1 미리보기][iec], [HSE 제어시스템][control] |
| `proof_test_pst_role` | 수정 | 원문의 “proof test가 검출·복구한다”를 **검출 후 별도 복구·재시험**으로 분리했다. PST는 검출 가능한 고장모드만 cover하며 full proof test를 자동 대체하거나 MTTR을 자동 단축하지 않는다. | [HSE proof-test 부록 1][proof1], [HSE 부록 2][proof2], [HSE 부록 3][proof3] |
| `srs_lifecycle_handoff` | 확인 | 위험분석 결과는 안전기능·무결성 요구사항으로 명세하고 설계·설치·운전·수정·폐기까지 관리한다. 구체적 SRS 필드는 해당 SIF에 적용 가능성을 확인해야 한다. | [IEC 61511-1 미리보기][iec], [HSE 기능안전][functional] |
| `operations_moc_revalidation` | 수정 | 모든 변경마다 LOPA와 SIL 계산을 재실행한다는 문장을 **MOC 영향평가 후 위험 시나리오·기존 설계 가정에 영향이 있는 관련 단계만 재검토**하도록 고쳤다. 운전 기록·고장 조사와 시험주기 준수는 계속 필요하다. | [HSE 기능안전 검사 지침][inspection], [HSE proof-test 부록 2][proof2] |
| `cyber_ai_safety_boundary` | 추가 근거 필요 | OT 보안위협이 SIS에 영향을 줄 수 있고 보안조치가 기능안전을 대체하지 않는다는 범위는 확인했다. AI 작성 코드의 독립 V&V·traceability·배포경계에 관한 구체적 요구 수준은 별도 공식 근거 및 적용 표준 확인 전 확정하지 않는다. | [HSE 산업 제어 보안][cyber], [IEC 61511-1 미리보기][iec] |

요약: 16개 중 `확인` 12, `수정` 2, `추가 근거 필요` 2. 근거가 부족한 2개는 정답 확정이나 자동 승인으로 승격하지 않는다. 이번 감사에서 확정된 수정은 grading source와 README에 반영하고 generated bank는 공식 builder로 재생성한다. 다음 배치부터도 이 판정 형식을 유지한다.

[iec]: https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTExLTF7ZWQyLjB9Yi5wZGY%3D
[control]: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm
[functional]: https://www.hse.gov.uk/eci/functional.htm
[inspection]: https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf
[alarp]: https://www.hse.gov.uk/offshore/assets/docs/ed-well-examination.pdf
[lopa]: https://ccps.aiche.org/resources/tools/lopa
[lopa_book]: https://ccps.aiche.org/publications/books/layer-protection-analysis-simplified-process-risk-assessment
[modifiers]: https://ccps.aiche.org/resources/tools/lopa/when-when-not-use-enabling-conditions-conditional-modifiers
[proof1]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf
[proof2]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix2.pdf
[proof3]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf
[cyber]: https://www.hse.gov.uk/eci/cyber-security.htm
