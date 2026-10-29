# 저비용 AI Topic 내용 검토 — 2026-10-29

## 정책 변경

사용자는 Astra의 반복 승인 대신 토큰 비용이 낮은 검토 방식을 요청했다. 이 기록 이후의 일상 순서는 **기존 승인 Registry 대조 → deterministic 구조·해시 검증 → 저비용 모델의 1차 출처 대조 → 확실한 경우에만 AI 승인**이다. 모델명·근거 URL·locator·검토 범위를 그대로 남긴다. 불충분한 근거, 출처 충돌, 채점 의미 변경은 보류한다. Astra의 과거 검토·승인 기록은 소급해서 다른 모델명의 승인으로 바꾸지 않는다.

## 첫 배치: 등록부 미등재 Anchor 111–150번

검토 모델: `gpt-6-luna`. 대상은 `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`의 40개 Anchor다. [Emerson Control Valve Handbook](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valve-handbook)과 [ASME B16.34 공식 안내](https://www.asme.org/codes-standards/find-codes-standards/b16-34-valves-flanged-threaded-welding-end/2017)의 적용범위를 대조했다. 두 자료는 밸브 공학 및 특정 압력·온도 등급 근거를 제공하지만, 아래 **40개 항목 전체가 모든 프로젝트에 의무인 고정 체크리스트**임을 입증하지 않는다.

검토된 ID: `tag_service_boundary`, `stakeholder_requirement_integration`, `requirement_classification_mandatory_preferred`, `operating_case_matrix`, `minimum_normal_maximum_cases`, `startup_shutdown_upset_cleaning_cases`, `pressure_reference_consistency`, `temperature_envelope_and_thermal_transient`, `flow_basis_and_uncertainty`, `fluid_phase_composition_properties`, `solids_fouling_corrosion_contaminant`, `control_objective_and_loop_dynamics`, `rangeability_turndown_travel_distribution`, `shutoff_leakage_fail_action`, `safety_environmental_regulatory_requirements`, `response_time_and_availability_requirement`, `specialist_calculation_handoff`, `liquid_gas_sizing_cross_check`, `authority_installed_characteristic_cross_check`, `cavitation_flashing_noise_velocity_cross_check`, `severe_service_and_material_cross_check`, `final_element_sis_esd_cross_check`, `selection_matrix_tradeoff`, `uncertainty_margin_and_double_margin`, `valve_body_flow_path_selection`, `trim_characteristic_and_flow_direction`, `seat_packing_gasket_emissions`, `actuator_thrust_torque_supply_minimum`, `fail_action_spring_and_stored_energy`, `positioner_solenoid_booster_accessory_package`, `installation_orientation_piping_load_accessibility`, `datasheet_completeness_and_units`, `requisition_scope_and_guarantees`, `vendor_bid_technical_comparison`, `deviation_exception_risk_register`, `vendor_sizing_assumption_validation`, `document_and_configuration_control`, `inspection_test_plan_and_hold_points`, `material_certification_nde_traceability`, `fat_functional_performance_acceptance`.

판정: **이번 근거만으로 Fact Registry에 일괄 `verified` 승격하지 않음**. Luna의 1차 분류는 프로젝트별 절차·체크리스트 성격이 강하다는 것이다. 이는 각 항목의 공학적 타당성을 부정하는 확정 판정이 아니다. 다음 단계에서 내부 소유 경계, 조건부 설계 지침, 독립 검증 가능한 물리·규격 사실을 분리한다. 기존 Pack·점수·승인 metadata는 변경하지 않았다.

재검토 보정: `specialist_calculation_handoff`, `liquid_gas_sizing_cross_check`, `authority_installed_characteristic_cross_check`, `cavitation_flashing_noise_velocity_cross_check`, `severe_service_and_material_cross_check`, `final_element_sis_esd_cross_check`의 **handoff 자체**는 내부 소유 계약이다. 나머지 항목은 대체로 프로젝트별 설계·선정 지침이며, 그 안의 기술적 하위 주장(압력 기준, 유체 물성, actuator 부하, 재질·trim 조건 등)은 각각 직접 출처를 대조할 수 있다. `rangeability_turndown_travel_distribution`은 세부 분류가 아직 명시되지 않아 보류한다. “40개 모두 비기술 사실”이라는 판정은 채택하지 않는다.

이 배치까지 읽은 미등재 ID는 150/573개(그중 Astra 71–110번은 최종 보고 전 사용량 제한으로 **임시 검토**), 아직 읽지 않은 ID는 423개다. 완료·승인 수치에는 임시 검토를 포함하지 않는다.

## 둘째 배치: 미등재 ID 151–190번

검토 모델: `gpt-6-luna`. 40개를 내부 계약·프로젝트별 지침·기술 주장으로 분리했다. **일괄 Fact 승인 0건**이다. 일부는 1차 근거로 조건부 지지되지만 원문 전체 문장을 직접 지지하지 않아 Registry 승격을 보류했다.

| 상태 | Anchor ID | 검토 결론 |
| --- | --- | --- |
| 프로젝트별 절차·지침 | `sat_loop_stroke_response_leakage`, `commissioning_installed_performance_verification`, `as_built_baseline_and_handover`, `reliability_availability_maintainability`, `spare_parts_interchangeability_obsolescence`, `lifecycle_cost_energy_downtime`, `field_feedback_moc_revalidation`, `operating_case_envelope`, `min_normal_max_transient_cases`, `purge_flushing_cleanout`, `inspection_monitoring_trim_replacement`, `specification_material_sizing_workflow`, `vendor_qualification_purchaser_acceptance`, `maintainability_spares_turnaround`, `lifecycle_cost_energy_service_life`, `repair_reverification_worst_case`, `etc_problem_fit_first` | 적용조건·합격기준·순서는 프로젝트마다 다르며 보편 의무로 읽히지 않게 한다. |
| 내부 소유 계약 | `eem_ground_emc_boundary`, `eem_environment_qualification_boundary`, `eem_hardware_lifecycle_boundary`, `eem_sensor_specific_boundary`, `eem_metrology_boundary` | 내부 Topic 경계로 검토하며 외부 Fact Registry와 분리한다. |
| 조건부 기술 주장 | `process_fluid_geometry_consequence_chain`, `installed_rangeability_handoff`, `microflow_trim_geometry`, `actuator_positioner_heat_isolation`, `icing_condensation_insulation_interface`, `fibrous_sticky_polymerizing_plugging`, `valve_geometry_solids_passage`, `etc_optimization_candidate`, `etc_estimation_candidate` | 일부 근거는 있으나 서비스·제품·연구 범위가 좁다. 일반화와 산업 성능 주장 금지. |
| 추가 1차 근거 필요 | `severe_service_combined_risk_definition`, `packing_gasket_seat_coating_temperature`, `thermal_cycling_heat_soak`, `orientation_flow_direction_self_cleaning`, `high_viscosity_non_newtonian_sizing`, `multiphase_entrained_gas_uncertainty`, `seat_packing_material_tradeoff`, `actuator_breakaway_thermal_friction_handoff`, `fouling_wear_clearance_trend` | 복합 문장을 분할하거나 각 절의 제조사·규격 원문을 확인해야 한다. |

이 배치의 1차 출처 예: [IEC 60534-4 공식 범위](https://webstore.iec.ch/en/publication/72947), [Emerson Control Valve Handbook](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf), [Fisher EZ](https://www.emerson.com/en/final-control/products/fisher-ez), [Fisher Dirty Service Trim](https://www.emerson.com/en/final-control/products/fisher-dst), [IBM 양자 응용 맥락](https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/quantum-computing-context), [NIST 연구 논문](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.133.040802). 각각 특정 범위만 지지하며, 열거된 Anchor 전체를 무조건 승인하는 근거가 아니다.

현재 읽은 범위는 190/573개(71–110번은 임시 검토), 아직 읽지 않은 ID는 383개다. 기존 Topic source와 운영 Bank는 변경하지 않았다.

## 셋째 배치: 미등재 ID 191–230번

검토 모델: `gpt-6-luna`. 일괄 승인 없이 네 영역으로 나눴다.

- 양자기술 `etc_offline_supervisory_boundary`–`etc_emerging_technology_framework`(191–199): 오프라인 평가·고전 baseline 비교·성숙도·통합비용 등의 **연구·적용 판단 지침**이며, 산업 현장 이득이 입증되었다는 Fact가 아니다. [IBM의 quantum context](https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/quantum-computing-context)는 최적화 우위 문제조차 열려 있다고 설명한다.
- SIS 최종요소 `system_sif_sil_context_boundary`–`fmeca_fmeda_vendor_data_assumptions`(200–218): 내부 소유 경계와 SIF별 계산·시험·안전 요구를 분리해야 한다. `fail_action_vs_safe_state`, CCF·독립성 원리는 [HSE functional safety](https://www.hse.gov.uk/eci/functional.htm)와 정합적이나, `failure_rate_partition_dd_du_sd_su`는 정확한 IEC 용어 근거, `pst_interval_and_online_demand_exposure`는 시험 유발고장·운영부담의 별도 근거가 부족하다. [HSE PST guidance](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf)는 coverage/interval의 적용조건 참고다.
- 유량 `flow_laminar_pressure_relation`, `flow_dp_conversion_conditions`, `flow_laminar_regime_conditions`(219–221): Newtonian·충분히 발달한 정상 층류의 Hagen–Poiseuille 관계와 차압식 계수·밀도·팽창 조건은 [NIST SP 484](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication484v2.pdf), [NIST 오리피스 연구](https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote1264.pdf)로 뒷받침된다. 해당 primary element의 규격·구성에 한정한다.
- 위험환경 제어 `hec_hazardous_environment_scope`–`hec_sensor_selection_diagnostics`(222–230): safe state·전원 상실·저장 에너지·통신 상실·로컬 보호는 [HSE control-system guidance](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm)로 원칙을 확인했다. rail·building·power 전체에 특정 구현을 의무화하지 않는다. 통신 timeout/quality/fallback과 센서 선정 목록은 시스템별 SRS·장치 자료가 필요하다.

현재 읽은 범위는 230/573개(71–110번은 임시 검토), 아직 읽지 않은 ID는 343개다. 이 배치도 source/Bank 승격 0건이다.

## 넷째 배치: 미등재 ID 231–270번

검토 모델: `gpt-6-luna`. 위험환경 제어(231–247)와 HIPPS(248–270)를 검토했다. **일괄 Fact 승인 0건**이며 기존 Pack·점수·Bank는 변경하지 않았다.

- 위험환경 제어: [HSE 제어계통 지침](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm)은 이중화·공통원인고장, 안전 상태, bypass/override 관리, 경보와 trip의 구분, 검증·변경관리 원칙을 지지한다. 다만 235–240번의 철도·전력·건물 분야 적용은 각 분야의 관련 규격과 프로젝트 조건을 별도로 확인해야 한다. `hec_ownership_boundary`(247)는 외부 공학 사실이 아니라 내부 소유 계약이다.
- HIPPS: [IOGP Report 443](https://www.iogp.org/bookstore/wp-content/uploads/sites/2/woocommerce_uploads/2021/01/443.pdf), [API 17O 안내](https://www.api.org/~/media/files/publications/whats%20new/17o_e2%20pa.pdf), [HSE 과압방지 지침](https://www.hse.gov.uk/comah/sragtech/techmeasventsyst.htm)은 relief와의 관계, SIF 범위, 응답시간·공정안전시간의 조건부 검토를 지지한다. 2oo3/1oo2 또는 특정 SIL을 보편적 정답으로 고정하지 않는다. `hipps_closure_time_and_surge`(263)는 hydraulic transient의 직접 근거, 270번 생애주기 비용 비교는 프로젝트별 데이터가 필요하다.

현재 읽은 범위는 270/573개(71–110번은 임시 검토), 아직 읽지 않은 ID는 303개다. 근거가 일부 일치하는 것과 문장 전체에 대한 검증 승인은 구분한다.

## 다섯째 배치: 미등재 ID 271–310번

검토 모델: `gpt-6-luna`. HIPPS 운영, HMI·경보·SOE, 산업 AI/ML, IIoT를 검토했다. **일괄 Fact 승인 0건**이다.

- 271–272 HIPPS 시험·우회·변경: [HSE 제어계통 지침](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm)에 부합하는 수명주기 지침. 간격·PST credit·SRS 항목은 SIF별로 결정한다.
- 273–294 HMI/SOE: `sw03_scope_operator_information`, `sw03_sw02_boundary`, `sw03_sw04_sw10_boundary`는 내부 소유 계약. HMI 구조·화면 계층·색상은 [ISA-101 안내](https://www.isa.org/standards-and-publications/isa-standards/isa-101-standards)의 설계 영역이나, 특정 4단계 화면이나 설정값 승인 양식을 모든 현장에 의무화할 수 없다. 경보 성능은 [ISA-TR18.2.5](https://www.isa.org/getmedia/3b68ebbf-eff7-476a-ad57-7b60072c7e8a/TR_18-2-5_Preview.pdf), SOE timestamp·quality는 [OPC UA 규격](https://reference.opcfoundation.org/specs/OPC-10000-4/7.11.3)과 부분적으로 부합한다. `sw03_alarm_delay`, `sw03_historian_vs_soe`, `sw03_first_out_relation`은 직접 정의 근거를 보완하고 보편적 구현으로 단정하지 않는다.
- 295–300 산업 AI: AI⊃ML⊃DL 분류는 [NIST AI 자료](https://www.nist.gov/system/files/documents/2021/08/20/ai-rmf-rif-0025-attachment2.pdf)와 [ITU/ISO 용어집](https://www.itu.int/epublications/publication/itu-t-y-sup-97-2025-11-glossary-of-terms-and-definitions-for-machine-learning)으로 지지된다. `data_leakage`는 [scikit-learn 지침](https://scikit-learn.org/stable/common_pitfalls)에 부합하나 중복 사건 사례는 조건부이다. 나머지 배포·평가 조치는 [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)에 비추어 프로젝트별 지침으로 유지한다.
- 301–310 IIoT: 층별 구성은 [NIST IIoT 문서](https://www.nist.gov/publications/scalable-data-pipeline-architecture-support-industrial-internet-things)의 흔한 패턴이지 유일한 표준 구조가 아니다. `iiot_protocol_connectivity_handoff`, `iiot_historian_mes_data_handoff`는 내부 소유 계약. 시간·품질·단위·namespace는 [OPC UA 규격](https://reference.opcfoundation.org/specs/OPC-10000-8/5.6.4)에 부분적으로 근거하나 전체 데이터 계약과 offline 복구 방식은 프로젝트별 설계다.

현재 읽은 범위는 310/573개(71–110번은 임시 검토), 아직 읽지 않은 ID는 263개다. 문장별 범위 확인 전에는 운영 Fact Registry를 변경하지 않는다.

## 여섯째·일곱째 배치: 미등재 ID 311–390번

검토 모델: `gpt-6-luna`. IIoT, 산업 네트워크·통신, 제어 SW 수명주기와 시험 항목 80개를 읽었다. 검토 중 사용한 분류는 복합 문장에 대해 겹칠 수 있으므로 승인·보류 건수로 합산하지 않는다. **현재 문구 그대로 운영 Fact Registry에 승격한 항목은 0건**이다.

| ID | 판정·필요 조치 |
| --- | --- |
| `sw07_modbus_rtu`(354) | [Modbus 공식 규격](https://www.modbus.org/modbus-specifications)에 비추어 serial-line 메시지 교환과 장치별 주소·단위·스케일 확인으로 문구를 좁히면 승격 후보. 현 문구의 포괄적인 “register 기반”만으로는 부족하다. |
| `sw07_interoperability_levels`(357) | [OPC UA Companion Specification](https://opcfoundation.org/about/opc-technologies/opc-ua/ua-companion-specifications/)은 정보 모델의 의미적 상호운용성을 뒷받침한다. Pack의 전체 단계 구분은 보편 표준이 아니라 자체 프레임임을 명시하면 일부 사실 승격 후보. |
| `sw04_hil`(380) | [NASA HIL 자료](https://ntrs.nasa.gov/api/citations/20240004147/downloads/EAP_Tutorial_2024TurboExpo_v1.pdf)에 맞추어 실제 하드웨어 구성요소와 실시간 시뮬레이션의 폐루프 시험으로 정의를 넓히는 것이 적절하다. SiL은 Software-in-the-loop로 풀어 Safety Integrity Level과 구분한다. |

Topic 간 handoff·범위(#313, #345–346, #365–369, #390)는 내부 계약이다. IIoT·네트워크·통신 선정·시험 절차의 상당 부분은 프로젝트 지침이며, 특정 네트워크 성능·deadline·failover 목표는 프로파일·조건·실측 수용 기준 없이는 보편 기술 사실로 승인할 수 없다. 특히 #327–344의 결정성·QoS·동기·복구 주장은 [IEEE 802.1AS](https://standards.ieee.org/ieee/802.1AS/11284/) 등의 범위와 문장별로 대조해야 한다. #351 RS-485 설치 조건, #358 적합성/상호운용성 구분, #376–383 분석·시험·커버리지 정의는 각각 직접 규격 근거가 더 필요하다.

현재 읽은 범위는 390/573개(71–110번은 임시 검토), 아직 읽지 않은 ID는 183개다. 세 승격 후보는 **문구 수정 및 회귀 검증 전까지 미승인**이다.

## 여덟째·아홉째 배치: 미등재 ID 391–470번

검토 모델: `gpt-6-luna`. 80개를 중복 없는 1차 분류로 기록했다: 내부 계약 18개, 프로젝트 지침 39개, 조건부 기술 주장 22개, 직접 근거 부족 1개(`codes_standards_specifications_distinction`, 469). 현재 문구 그대로 정확히 입증되어 즉시 승격할 수 있는 항목은 **0개**다.

환경시험 #392–403, #407–408은 [IEC 61000-4-3](https://webstore.iec.ch/en/publication/59849), [IEC 60068-3-4](https://webstore.iec.ch/en/publication/70588)의 시험 범위에 관련되지만 모든 장치에 동일 시험 순서를 요구하지 않는다. Ex 설치의 #432는 [IEC 60079-14](https://webstore.iec.ch/en/publication/66049)의 범위와 관련되어도 Topic 소유 경계 자체는 내부 계약이다. #439–466의 프로젝트 관리 문구는 [PMI 범위관리 자료](https://www.pmi.org/learning/library/scope-management-9099)가 세부 gate·산출물을 강제하지 않으므로 현장 지침으로 유지한다.

수정 우선 항목: #391의 V-model/MC/DC·SIL 관계는 적용 안전 표준에 맞춰 범위를 좁히고, #396–400의 환경 고장 메커니즘은 가능성·요구기반 시험으로 표현한다. #413, #415–418, #422, #425, #427의 설치·시험 수치와 절차는 승인된 장치·프로젝트 한계에 따른다고 명시한다. #469는 Code/Standard/Specification의 강제력을 단정하지 말고 **관할 규제, 채택, 계약, 프로젝트 요구에 따라 적용성과 구속력이 정해진다**고 고친다. #470도 최신 판이 자동 적용되는 것처럼 쓰지 않는다.

현재 읽은 범위는 470/573개(71–110번은 임시 검토), 아직 읽지 않은 ID는 103개다. 운영 Fact Registry 승격은 없다.

## 열째·열한째·열두째 배치: 미등재 ID 471–573번 및 71–110번 재검토

검토 모델: `gpt-6-luna`. 남은 103개와 임시 기록 40개를 재검토했다. 아래 범위의 분류는 서로 배타적이다. **분류 완료와 운영 Fact 승인은 다르다.**

| 범위 | 1차 검토 결과 |
| --- | --- |
| 471–573 (103개) | 내부 계약·프로젝트 지침·조건부 기술 주장이 혼재한다. 현 문구의 6개는 직접 근거 대조 후보이다. |
| 71–110 (40개) | 내부 계약·프로젝트 지침이 대부분이며, #79·#92–94는 적용조건을 추가해야 한다. |

현 문구에서 조건부 사실 승격을 검토할 수 있는 6개는 #490–491(자유 월류 위어의 적용조건에서 (H^{3/2})·(H^{5/2}) 지수), #553(분모 기준값이 0이 아닌 부호 있는 상대 백분율 변화식), #569·#571–572(정해진 회전·진동 조건에서 Coriolis 가속도/힘 및 속도 반전 방향)다. 근거는 [USGS 위어 자료](https://pubs.usgs.gov/wsp/wsp2175/wsp2175_vol2.pdf), [USGS V-notch 예시](https://pubs.usgs.gov/wri/1992/4025/report.pdf), [NASA 진동 자이로 자료](https://ntrs.nasa.gov/citations/20080004510), [NASA Coriolis coupling](https://ntrs.nasa.gov/citations/20110023987)이다. 실제 Registry 반영 전에는 정확한 Pack 문구·수식·조건과 원문 locator를 다시 대조한다.

471–573 중 내부 계약은 #486, #536, #552, #566–567이다. 검토자의 상세 범주 목록에서 #552가 내부 계약과 조건부 기술 주장에 중복 기재된 오류가 있어, 나머지 항목의 **범주별 정량 집계는 확정하지 않았다**. 현재는 범위별 읽기 완료와 6개 후보만 기록하며, 배타적 분류를 기계적으로 다시 확인한 뒤 건수 확정 및 승인 장부로 사용한다.

71–110 중 #79의 LOTO는 관할·정비 범위에 맞춰 [OSHA 29 CFR 1910.147](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147)을 한정 적용한다. #92–94의 압력경계·stroke/friction·fail-action 시험은 승인된 장치·정비·시험 기준이 먼저다. 이 40개는 더 이상 Astra의 임시 완료로 세지 않고, Luna의 1차 재검토 완료로 표시한다.

## 완료 범위와 미완료 범위

이번 저비용 1차 검토로 **등록부 미등재 Anchor ID 573개 전체를 읽고 분류했다**. 이는 기술 내용의 최종 승인 573건이 아니다. 현 문구에서 직접 지지된 후보는 위 6개이고, #354·#357·#380은 문구 수정 후 후보이며, 나머지는 내부 계약·프로젝트 지침·조건부 기술 주장으로 보존한다. 기존 Registry에 이미 등록된 1,520개 고유 ID도 이번 작업에서 모두 독립 재감사한 것은 아니다. 출처·조건·locator 대조, 문구 정리, 승인 기록, 생성물 갱신 및 release 검증은 후속 작업이다. **운영 Fact Registry 추가 승인 0건.**
