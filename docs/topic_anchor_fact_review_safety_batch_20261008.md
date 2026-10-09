# Anchor 사실 검증: 기능안전 신뢰도·HAZOP/LOPA 배치 (2026-10-08)

범위: 아래 두 Topic Pack의 Anchor 51개. `확인`은 표에 기재한 1차 자료와 문장 경계를 대조했다는 뜻이다. `수정`은 이번 배치에서 과도한 표현을 고쳤다는 뜻이다. `추가 근거 필요`는 틀렸다는 판정이 아니라 현재 공개 자료만으로 문장의 세부 조건을 확정하지 않았다는 뜻이다. 계산식의 대수적 귀결은 별도로 표시했다. 이 표는 전체 2,073개에 대한 검증 증명이나 현장 SIF 인증이 아니다.

## 기능안전 신뢰도 모델 (`functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`)

| Anchor ID | 판정 | 확인한 주장과 경계 | 1차 근거 |
| --- | --- | --- | --- |
| `fsrm_rbd_success_path` | 확인 | RBD는 성공/가용 경로를 블록으로 모델링한다. | [NASA RBD][nasa_rbd] |
| `fsrm_rbd_series_parallel` | 확인 | 직렬·병렬 구성의 성공조건이 다르다. | [NASA RBD][nasa_rbd] |
| `fsrm_fta_top_event` | 확인 | FTA는 정의된 top event의 원인조합을 논리 gate로 전개한다. | [NASA FTA][nasa_fta] |
| `fsrm_minimal_cut_set` | 확인 | Minimal cut set은 top event를 일으키는 최소 실패조합이다. | [NASA FTA][nasa_fta] |
| `fsrm_markov_state_transition` | 추가 근거 필요 | 상태전이 모델이라는 핵심은 확인했다. 원문이 나열한 모든 상태(진단·proof test·degraded)를 모든 Markov 모델의 필수 구성으로 해석하지 않는다. | [NASA 가용도 분석][nasa_markov] |
| `fsrm_markov_complexity` | 확인 | 상태전이 확장에 따라 해석 비용이 커질 수 있다. | [NASA FTA Handbook][nasa_handbook] |
| `fsrm_model_purpose_boundary` | 확인 | RBD·FTA·Markov는 서로 다른 성공/실패/상태 관점이며 동일 모델로 취급하지 않는다. | [NASA 가용도 분석][nasa_markov], [NASA FTA][nasa_fta] |
| `fsrm_low_demand_pfdavg` | 확인 | 저요구 SIF의 지표는 평균 요구시 고장확률이다. | [HSE 제어시스템][hse_control] |
| `fsrm_high_continuous_demand_pfh` | 확인 | 고요구·연속 기능은 시간당 위험고장 빈도 지표를 사용한다. | [HSE 제어시스템][hse_control], [IEC 61511 미리보기][iec] |
| `fsrm_demand_mode_metric_selection` | 확인 | PFDavg/PFH 선택은 요구/연속 운전 모드에 연동한다. | [IEC 61511 미리보기][iec] |
| `fsrm_one_oo_one_low_demand_approximation` | 확인 | 일정 λDU·완전 proof test 등 단순 가정에서 PFDavg가 λDU와 시험주기에 비례한다. 일반 설계식으로 확장하지 않는다. | [exida 계산 설명][exida_pfd], [HSE proof test][hse_proof] |
| `fsrm_approximation_conditions` | 확인 | 진단·시험·수리·독립성 가정을 명시해야 하며 1oo1 근사를 다중 채널에 그대로 적용하지 않는다. | [HSE 검사 지침][hse_inspection], [HSE 제어시스템][hse_control] |
| `fsrm_rrf_relationship` | 확인 | 저요구의 `RRF ≈ 1/PFDavg`는 동일 SIF 경계와 정의된 위험감소 조건에서 사용하는 관계다. | [HSE 검사 지침][hse_inspection] |
| `fsrm_voting_tradeoff` | 확인 | Voting 성공조건에 따라 위험고장과 불필요 동작의 trade-off가 달라진다. 특정 구조가 언제나 우월하지 않다. | [HSE 제어시스템][hse_control] |
| `fsrm_hft_not_sil_guarantee` | 확인 | HFT는 전체 SIL 검증의 일부이며 단독 보증이 아니다. | [HSE 검사 지침][hse_inspection] |
| `fsrm_ccf_redundancy_impact` | 확인 | CCF는 독립 중복의 이점을 축소한다. | [NASA FTA Handbook][nasa_handbook], [HSE 제어시스템][hse_control] |
| `fsrm_beta_factor` | 확인 | β-factor는 공통원인 기여분을 단순화하는 모델이다. | [NASA FTA Handbook][nasa_handbook] |
| `fsrm_ccf_reduction_measures` | 확인 | 물리적 분리·독립 유틸리티·다양성·정비 분리는 CCF 검토 수단이다. ‘적용하면 CCF가 0’이라는 의미는 아니다. | [HSE 제어시스템][hse_control] |
| `fsrm_diagnostic_vs_proof_coverage` | 확인 | 온라인 진단과 proof test는 발견 시점·대상 고장이 다르다. | [HSE proof test][hse_proof] |
| `fsrm_proof_test_purpose` | 확인 | Proof test는 평상시 드러나지 않는 위험고장을 찾는다. | [HSE proof test][hse_proof] |
| `fsrm_proof_test_interval_exposure` | 확인 | 완전 시험 등 가정 아래 간격이 길어지면 잠복고장의 평균 불가용 시간이 커진다. | [HSE 제어시스템][hse_control] |
| `fsrm_partial_test_boundary` | 확인 | PST/partial proof test는 검출 coverage와 잔여 DU 고장을 분리해야 한다. | [HSE proof test][hse_proof], [HSE PST][hse_pst] |
| `fsrm_complete_sif_boundary` | 확인 | 계산 경계는 센서에서 최종요소까지이며 필요한 공유 유틸리티·인터페이스의 영향도 고려한다. | [IEC 61511 미리보기][iec], [HSE 제어시스템][hse_control] |
| `fsrm_component_certificate_limit` | 확인 | 단일 인증품이 전체 SIF의 achieved SIL을 보증하지 않는다. | [HSE 제어시스템][hse_control] |
| `fsrm_hardware_systematic_boundary` | 확인 | 정량 하드웨어 계산 외에 체계적 능력과 수명주기 검증이 필요하다. | [HSE 검사 지침][hse_inspection] |
| `fsrm_model_assumption_documentation` | 추가 근거 필요 | 고장률·진단·시험·수리·CCF 기록 필요성은 확인했다. 원문이 열거한 bypass까지 모든 모델 입력에 동일하게 필수인지 여부는 모델·SRS 경계별로 확인해야 한다. | [HSE 검사 지침][hse_inspection] |

## HAZOP·LOPA (`hazop_lopa_ipl_risk_reduction_sil_target_allocation`)

| Anchor ID | 판정 | 확인한 주장과 경계 | 1차 근거 |
| --- | --- | --- | --- |
| `hazop_lopa_hazop_role` | 확인 | HAZOP은 guideword/deviation 기반 위험 식별이며 그 자체로 SIL을 산정하지 않는다. | [CCPS HAZOP 용어][ccps_glossary], [HSE HAZOP][hse_hazop] |
| `hazop_lopa_lopa_scenario_boundary` | 확인 | LOPA는 하나의 cause-consequence pair 단위다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_consequence_without_credited_protection` | 확인 | Credit할 IPL의 효과를 consequence와 PFD에 중복 반영하지 않는다. CCPS 계산 구조에서 도출한 중복계산 방지 조건이다. | [CCPS LOPA][ccps_lopa], [CCPS modifier 조건][ccps_mod] |
| `hazop_lopa_initiating_event_frequency` | 확인 | IE 빈도는 정의한 시나리오와 자료 근거에 종속된다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_enabling_and_conditional_modifiers` | 확인 | Modifier는 유효한 조건·자료·조직 기준이 있을 때만 적용한다. 모든 LOPA에 필수인 것은 아니다. | [CCPS modifier 조건][ccps_mod] |
| `hazop_lopa_lopa_frequency_equation` | 확인 | IE 빈도 × 적용 가능한 조건확률 × 독립 IPL PFD는 CCPS의 시나리오 결과빈도 계산 구조다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_tolerable_event_frequency` | 확인 | 위험수용 기준은 사전에 승인된 기준에 따라 적용하며 분석자가 임의로 만들지 않는다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_ipl_definition` | 확인 | IPL은 해당 시나리오의 결과 진행을 막는 독립적 장치·시스템·행동이다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_ipl_independence` | 수정 | 공통원인 동시 상실이 ‘없음’을 입증하도록 한 절대적 표현을 공유 자원·CCF 위험의 평가와 관리로 변경했다. | [CCPS LOPA][ccps_lopa], [HSE 제어시스템][hse_control] |
| `hazop_lopa_ipl_specificity` | 확인 | 특정 원인–결과에 작동하는 보호기능만 credit한다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_ipl_dependability_auditability` | 확인 | IPL 신뢰성·유지관리·감사가능성은 수명주기 성능 주장의 일부다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_no_double_counting` | 확인 | 공유 구성요소·동일 행동을 독립 IPL처럼 중복 credit하지 않는다. | [CCPS LOPA][ccps_lopa], [HSE 제어시스템][hse_control] |
| `hazop_lopa_common_cause_dependency` | 확인 | 공유 전원·배관·환경·정비 등 CCF 가능성을 독립성 평가에 반영한다. | [HSE 제어시스템][hse_control] |
| `hazop_lopa_bpcs_ipl_credit` | 확인 | BPCS가 원인인 시나리오에서 동일 기능을 자동 IPL credit할 수 없다. 독립 경계가 필요하다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_alarm_operator_ipl` | 확인 | Alarm/operator credit은 탐지·인지·반응시간, 절차와 성능 근거에 달려 있다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_proposed_safeguard_not_creditable` | 확인 | 계획된 보호수단은 현재 구현·검증된 IPL과 구분한다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_residual_frequency_after_existing_ipls` | 확인 | 유효 IPL 적용 후 빈도가 기준보다 크면 추가 위험감소가 필요하다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_required_rrf` | 확인 | `RRF_required = F_residual / F_tolerable`은 빈도 비교에서 도출되며 무차원이다. | [CCPS LOPA][ccps_lopa] |
| `hazop_lopa_no_additional_sif_when_ratio_below_one` | 수정 | 비율 ≤1은 **해당 시나리오의 빈도 기준만으로** 추가 SIF 요구가 없다는 뜻이다. 다른 시나리오·ALARP 조치까지 불필요하다는 뜻은 아니다. | [CCPS LOPA][ccps_lopa], [HSE ALARP][hse_alarp] |
| `hazop_lopa_pfdavg_rrf_relation` | 확인 | 저요구에서 목표 PFDavg ≤ 1/RRF은 동일 시나리오 경계에서 도출한다. | [CCPS LOPA][ccps_lopa], [HSE 제어시스템][hse_control] |
| `hazop_lopa_sil_band_mapping` | 확인 | 제시한 SIL 1~3의 PFDavg 범위는 저요구 구간이며 고요구 PFH와 혼용하지 않는다. | [HSE 검사 지침][hse_inspection] |
| `hazop_lopa_target_vs_achieved_sil` | 확인 | 위험분석의 target과 설계·시험 증거의 achieved는 별도로 확인한다. | [IEC 61511 미리보기][iec], [HSE 검사 지침][hse_inspection] |
| `hazop_lopa_sif_allocation_boundary` | 확인 | 센서-로직-최종요소 및 trip, safe state, response time을 기능 경계에 포함한다. | [IEC 61511 미리보기][iec] |
| `hazop_lopa_srs_handoff` | 확인 | 시나리오 분석 결과는 적용 가능한 안전기능·무결성 요구로 SRS에 인계한다. | [IEC 61511 미리보기][iec], [HSE 기능안전][hse_functional] |
| `hazop_lopa_scenario_aggregation_moc` | 수정 | 모든 변경에서 LOPA/SRS를 자동 재작성한다는 표현을 MOC 영향평가 후 관련 단계·가정만 갱신하도록 고쳤다. | [HSE 검사 지침][hse_inspection] |

이번 배치 합계: **51개 검토 = 확인 46, 수정 3, 추가 근거 필요 2**. 앞선 [SIL 결정 배치](topic_anchor_fact_review_sil_target_20261008.md) 16개를 합하면 Anchor별 기록은 **67/2,073개**, 미검토는 **2,006개**다. 수정 3개는 해당 Topic source와 관련 설명·검증 계약에 반영한다. 추가 근거 필요 2개는 사실 확정·사람 승인으로 승격하지 않는다.

[nasa_rbd]: https://llis.nasa.gov/lesson/829
[nasa_fta]: https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8621_0001_&page_name=AppdxI35
[nasa_markov]: https://llis.nasa.gov/lesson/841
[nasa_handbook]: https://extapps.ksc.nasa.gov/Reliability/Documents/Fault_Tree_Handbook_with_Aerospace_Applications_August_2002.pdf
[iec]: https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTExLTF7ZWQyLjB9Yi5wZGY%3D
[hse_control]: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm
[hse_inspection]: https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf
[hse_proof]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf
[hse_pst]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf
[hse_functional]: https://www.hse.gov.uk/eci/functional.htm
[hse_alarp]: https://www.hse.gov.uk/foi/internalops/hid/pmtech12.pdf
[hse_hazop]: https://www.hse.gov.uk/pubns/web34.pdf
[ccps_glossary]: https://ccps.aiche.org/resources/glossary?page=6&title=safety+integrity+level
[ccps_lopa]: https://ccps.aiche.org/resources/tools/lopa
[ccps_mod]: https://ccps.aiche.org/resources/tools/lopa/when-when-not-use-enabling-conditions-conditional-modifiers
[exida_pfd]: https://www.exida.com/blog/how-is-sil-used
