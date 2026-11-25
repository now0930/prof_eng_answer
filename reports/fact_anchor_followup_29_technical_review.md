# 우선순위 외 Fact Anchor 29건 기술 검토

기준 PR #46 `304833ac07bf666b375d689ae3b9bd2ac094808d`. 별도 Draft 후속 PR은 PR #46 브랜치를 base로 사용한다. 해당 선행 PR과 `main`은 변경하지 않았다. 검토한 29건은 역사적 [457건 검토](https://github.com/now0930/prof_eng_answer/issues/42) 및 [정확한 후속 목록](pr46_fact_anchor_closeout_and_followups.md)으로 추적한다.

REVISE 20건은 10건 정본 보정, 8건 승인 대기 제안, 2건 별도 채점 영향 재검토으로 처리했다. 기존 HOLD 9건은 KEEP 1건, REVISE 1건, REFERENCE_ONLY 5건, REMOVE_CANDIDATE 2건으로 기술 판정했다. 기존 HOLD 9건의 제외 상태와 119 HOLD·D4를 보존한다. 참고용 또는 삭제 후보의 원문은 추적성을 위해 보관했다.

## 대상별 기술 판정

‘승인 대기’는 현행 Registry의 수정 또는 그 정본으로의 연결을 위해 정확한 문장 재검토가 필요한 상태다. ‘유지’는 기존 승인 Registry의 범위를 유지한다는 뜻이다. 정본을 수정한 경우도 Registry 행, 승인 이력과 제외 상태를 갱신하지 않았다. 미등재는 실제 채점 적격성 판정이 아니다. 출처는 공식 원문 또는 기존 검토에서 기록된 정확한 locator를 인용한다. 물리적 도출과 범위 판단은 별도로 명시한다.

| Anchor ID | 기존 문제 | 기술 검증 근거 | 최종 판정 | 정본 | 제외 Overlay | Registry 승인 |
|---|---|---|---|---|---|---|
| `dp_level_wet_leg_zero_elevation` | 음의 LRV 가능에서 무조건 zero elevation으로 넘어감 | [Yokogawa IM01C20C01-01EN §7.4(3)](https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf) 원문 −23.73 kPa 설치 예. 일반식은 H/L 수두 차로 도출. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `sw09_software_firmware_integrity` | 격리 시험 단독으로 진위·무결성 입증 가능하다고 읽힘 | [NIST SP 800-82r3 Appendix F SI-7(15), pp. 293–294](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf)는 대체 수단의 조합을 설명한다. 기능 시험과 출처·검증값 확인의 목적 구분은 공학 판단. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `hazard_scenario_boundary` | 시나리오 구분 원칙을 동일 위험에 대한 합산 금지로 확대 | [CCPS LOPA Data](https://ccps.aiche.org/resources/tools/lopa) 및 [HSE Functional Safety Inspection Guide, Appendix 4](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf)의 시나리오·개시사건 기준. 집계 시 종속성과 중복을 구분하는 것은 확률 모델 경계. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `final_element_subsystem_boundary` | 특정 공정 결과를 공통 경계로 해석 가능 | [HSE Control systems, protective system and actuators](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm). 기능과 필요한 유틸리티를 기준으로 한 경계 판단. | REVISE | 수정 | 미등재 유지 | 기존 상태 유지 |
| `trip_signal_and_output_chain` | 공압 트립 경로를 보편 순서로 기술 | [Emerson Fisher 1061 safety manual, Connection to the SIS Logic-solver](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/actuators/documents/FCV-OSI-SIL-Safety-Manual-for-Fisher-1061-Actuator-D104499X012-EN.pdf)는 밸브·포지셔너 예시. 공정 효과의 독립 검증은 적용 판단. | REVISE | 수정 | 미등재 유지 | 기존 상태 유지 |
| `dp_level_hydrostatic_pressure_principle` | 적분의 좌표, 차압 부호 및 H/L 접속 미표기 | [Yokogawa §7.4](https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf) 비중·수두 예 및 정수압 평형 도출. | REVISE | 승인 대기 | 미등재 유지 | 문안 대기 |
| `deenergized_energized_test_condition` | 비통전 경로만 기본으로 읽힘 | [HSE Control systems, proof testing](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), 실제 트립 조건과 end-to-end 시험. | REVISE | 채점 영향 보류 | 미등재 유지 | 기존 상태 유지 |
| `partial_stroke_test_risk_controls` | 서비스별 위험과 제어 수단을 일괄 요구 | [HSE OG54 Appendix 2](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix2.pdf), 실제 시험의 실패·운전상 영향 및 절차 관리. 수단 선정은 SRS와 위험 검토에 따른다. | REVISE | 채점 영향 보류 | 미등재 유지 | 기존 상태 유지 |
| `manifold_isolation_sequence` | 3밸브와 계기 별도 기능의 구분 부족 | [Rosemount 2051 reference manual §2.8.4](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-00809-0100-4101.pdf) 장착 구성별 평형과 drain/vent 분리. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `production_schedule_adherence_delivery_kpi` | 계획 freeze를 모든 KPI에 요구 | [SAP Key Information for Tracking Schedule Execution](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/e72f747389b340229f7fa343975bfa57/9a3262c243ef4c649eaeed4e63bf510f.html?locale=en-US)은 freeze 기반 제품 구현. 일반 재현성에는 기준 계획과 측정 정의가 필요. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `radar_echo_polarity_sign_convention` | 물리식의 손실·매질 가정 생략 | 수직입사 E장 반사계수 Γ=(η₂−η₁)/(η₂+η₁) 도출. [Endress+Hauser Levelflex envelope curve 안내](https://bdih-download.endress.com/files/DLA/4ECBD5CF9BD7ED83E10000000A35E035/BA00281FEN_1511.pdf)는 제품 표시의 예. | REVISE | 수정 | 제외 유지 | 기존 상태 유지 |
| `radar_adaptive_threshold_echo_tracking` | 다양한 알고리즘을 동시에 적용한다는 서술 | [Siemens LR560 PA A.4.2, p.165](https://cache.industry.siemens.com/dl/files/829/109810829/att_1103768/v1/A5E34648471_en_LR560_PA_OI_en-US.pdf)의 TVT 및 선택 설정. | REVISE | 수정 | 제외 유지 | 기존 상태 유지 |
| `gwr_effective_permittivity_propagation_path` | 프로브 전파속도를 벌크 매질 식으로 단정 | [Endress+Hauser Levelflex FMP51/52/54 interface measurement](https://bdih-download.endress.com/files/DLA/005056A500261EDDACD86AC69782C198/TI01001FEN_2822-00.pdf) 상부층 지연. c₀/√εr은 비자성·저손실 균질 매질 근사. | REVISE | 수정 | 제외 유지 | 기존 상태 유지 |
| `tolerable_risk_alarp` | 영국 ALARP 요건의 범위 미표기 | [HSE ALARP at a glance](https://www.hse.gov.uk/enforce/expert/alarpglance.htm) gross disproportion과 범위. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `thermocouple_junction_construction_response_isolation` | 노출형 응답속도 최고의 무조건 주장 | [Omega probe response graph](https://br.omega.com/omegaFiles/temperature/Z/pdf/z052.pdf)는 침수 매질과 직경의 비교 범위를 명시. | REVISE | 수정 | 제외 유지 | 기존 상태 유지 |
| `om_asset_register_system_boundary` | 기능 위치와 개체 식별 구분 부족 | [ISO 14224:2016 공개 적용범위](https://www.iso.org/standard/64076.html) 및 기존 검토 §§3.91–3.92. 특정 필드 전체를 보편 의무로 보지 않는다. | REVISE | 승인 대기 | 제외 유지 | 문안 대기 |
| `digital_twin_definition` | 공식 정의명에 Instance를 덧붙임 | [ISO 23247-1:2021](https://www.iso.org/standard/75066.html) 및 [ISO 스마트제조 백서 Annex A](https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100459.pdf)의 manufacturing digital twin 정의. | REVISE | 수정 | 미등재 유지 | 문안 대기 |
| `lifecycle_maintainability_selection` | 고분해능이 비용을 반드시 증가시킨다고 기술 | [Encoder Products, Applying Encoders](https://www.encoder.com/wp2002-applying-encoders) 설치·인터페이스 및 [Siemens S7-1200 manual](https://support.industry.siemens.com/cs/attachments/109977302/s71200_system_manual_en-US.pdf) 입력 필터. 비용 경향은 구성 의존 공학 판단. | REVISE | 수정 | 제외 유지 | 기존 상태 유지 |
| `half_bridge_sensitivity_compensation` | 활성·더미 회로를 공통 반브리지 명칭으로 단정 | [NI SCXI-1520 Ch.4 Figure 4-4](https://download.ni.com/support/manuals/372583e.pdf)는 활성·더미를 Quarter-Bridge Type II로 분류. 감도 차이는 브리지 소신호 관계로 도출. | REVISE | 수정 | 제외 유지 | 문안 대기 |
| `resistive_sensor_ac_measurement` | 검증되지 않은 분극 원인과 제품 요건 혼재 | [HDK KRH1901003 §3-3 p.3, §4 p.4](https://www.hdk.co.jp/pdf/tece/appe_krh1901003.pdf) 원문의 HIS-08V 표기, AC 지정과 DC 경고. 분극 원인은 해당 문서에서 직접 확인되지 않음. | REVISE | 수정 | 미등재 유지 | 문안 대기 |
| `dp_level_overpressure_and_static_pressure_effect` | 특정 3051SHP의 재영점 사례 | [Rosemount 3051S High Static reference manual §§8.2.13–15](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051shighstatic-00809-0100-4851.pdf) 모델별 사양. 이 검토에서는 단측 가압 시 반드시 재영점이라는 범위를 확정하지 않음. | REFERENCE_ONLY | 보존 | 제외 유지 | 기존 상태 유지 |
| `operating_case_force_matrix` | 구성별 상세 힘 목록과 일반 원리가 혼재 | [Fisher Valve Sizing §2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103533x012.pdf) 사례별 sizing. 세부 force 항목은 선택 구성에 따른다. | REFERENCE_ONLY | 보존 | 제외 유지 | 기존 상태 유지 |
| `flashing_classification` | Pv와 하류 압력의 등호 및 적용 범위 검토 | [Emerson Understanding Flashing](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/valve-flashing) 액체의 기화 이후 하류 P₂<Pᵥ로 증기 지속. 기존 문장은 등호만으로 단정하지 않아 유지. | KEEP | 보존 | 제외 유지 | 기존 상태 유지 |
| `pst_not_full_proof_test` | PST와 proof test 자체를 구분하고 full stroke에 누설 검증을 포함할 수 있다고 넓게 읽힘 | [HSE OG54 Appendix 1 §§35–43](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf) 및 [Appendix 3](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf). 부분행정도 적용 검출 범위 내 부분 proof test로 다룰 수 있음. | REVISE | 수정 | 제외 유지 | 문안 대기 |
| `lvdt_null_residual_voltage` | 영점 잔류에 대한 상세 회로 원인의 필수화 위험 | [TI SPRA946 §3.2.1](https://e2e.ti.com/cfs-file/__key/CommunityServer-Discussions-Components-Files/171/7127.TI-_2D00_-Signal-Conditioning-an-LVDT-Using-a-TMS320F2812-DSP.pdf) null 잔류 예. 잔류 개념은 유용하며 원인 전체에 대한 시험 필수성은 낮음. | REFERENCE_ONLY | 보존 | 제외 유지 | 기존 상태 유지 |
| `lvdt_core_alignment_eccentricity_error` | 방사상 편심 영향은 센서 구조와 설치에 의존 | [TE Tutorial, Core Types](https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html). Free-core와 guided의 조건을 제품 참고로 둔다. | REFERENCE_ONLY | 보존 | 제외 유지 | 기존 상태 유지 |
| `lvdt_magnetic_saturation_nonlinearity` | 정격 선형범위 안의 포화 비선형을 일반화할 근거 부족 | [NAI Bench Testing LVDT/RVDT](https://docs.naii.com/faq/Synchro--and--Resolver/Bench-Testing-an-LVDT-RVDT)의 과여자 한계와 정격 내 주장은 범위가 다르다. 지엽적 정격 내 포화 결합 주장에 삭제 권고. | REMOVE_CANDIDATE | 보존 | 제외 유지 | 기존 상태 유지 |
| `sw06_obsolescence_mitigation_options` | 특정 군수 지침 분류표 | [DoD SD-22 2016, Table 9 기존 locator](https://www.nasa.gov/wp-content/uploads/2023/06/dmsms-guidebook-sd-22-jan2016-tagged.pdf). 군수 적용 참고용. | REFERENCE_ONLY | 보존 | 제외 유지 | 기존 상태 유지 |
| `sw06_license_entitlement_continuity` | 라이선스 다운그레이드 및 공급자 존속 사례의 낮은 일반성 | [DoD SD-22 2016, Table 9 기존 locator](https://www.nasa.gov/wp-content/uploads/2023/06/dmsms-guidebook-sd-22-jan2016-tagged.pdf). 계약 예시를 일반 기술 Fact에서 빼도록 권고. | REMOVE_CANDIDATE | 보존 | 제외 유지 | 기존 상태 유지 |

## 승인 대기 문안 12건

아래 12개 문장은 Registry의 본문·범위 재승인 또는 기존 승인 정본과의 대조가 필요한 후속 안이다. 8건의 정본은 그대로 두었다. 차압 레벨의 2건, ISO 14224의 1건, SIL의 2건은 해당 Topic의 파일 전체가 기존 승격 Ledger의 SHA-256에 고정돼 있다. 로즈마운트 매니폴드 1건은 managed Topic의 승인 source hash에 고정돼 있다. 펌웨어 진위와 생산 일정 KPI 2건은 기존 Registry와 정본의 정확한 일치를 회귀시험으로 요구한다. 공식 승인 절차에서 정확한 문장과 해당 파일의 검토를 거쳐 처리한다. 나머지 4건은 정본에 검토된 조건을 기록하고 Registry 기록을 보존했다.

- **`dp_level_wet_leg_zero_elevation`** — Wet leg의 0 % 레벨에서 LRV는 실제 설치 조건의 고압측 압력에서 저압측 압력을 뺀 값이다. 일정 밀도에서 공정액의 양의 수두가 ρ_p·g·h_min, 저압측 기준액의 수두가 ρ_w·g·H_w이면 LRV=ρ_p·g·h_min−ρ_w·g·H_w+C이다. C는 이 두 수두에 포함되지 않은 설치 오프셋의 부호 있는 합이다. 계산한 LRV가 음수일 때 zero elevation을 적용한다.
- **`sw09_software_firmware_integrity`** — OT 소프트웨어·펌웨어는 신뢰할 수 있는 배포 경로와 버전을 확인하고, 신뢰된 공급자가 제공한 서명·인증서 또는 검증 기준 해시를 적용 가능한 방식으로 대조한다. 격리 시험은 호환성과 기능을 확인하는 데 사용할 수 있다. 진위와 무결성은 배포 출처 및 검증값의 신뢰성으로 별도 확인한다.
- **`hazard_scenario_boundary`** — 목표 SIL 검토에서는 개시사건, 운전조건, 결과와 요구 안전상태를 시나리오별로 정의한다. 같은 위험 결과 및 SIF에 기여하는 시나리오 빈도를 집계할 때에는 공통 조건, 종속성과 중복 산입을 확인한다.
- **`dp_level_hydrostatic_pressure_principle`** — 정지 유체에서 위쪽을 양의 z로 잡으면 dP/dz=−ρg이다. 아래점과 위점의 압력차 P_b−P_t는 두 높이 사이의 ρg 적분이며, 밀도가 일정하면 ρgΔh이다. 전송기의 지시 부호는 실제 H/L 연결과 각 측의 수두를 기준으로 판단한다.
- **`om_asset_register_system_boundary`** — ISO 14224의 석유·천연가스·석유화학 설비 맥락에서 장비 태그는 기능과 물리적 위치를 식별하는 데 쓰고, 제조 일련번호는 개별 장비와 교체 이력을 식별하는 데 쓴다. 신뢰성·정비 데이터 항목은 해당 분류체계와 분석 목적에 맞춰 정한다.
- **`manifold_isolation_sequence`** — Rosemount 2051의 해당 3밸브 매니폴드 영점 확인 절차에서 차단 밸브 두 개와 평형 밸브 한 개를 구분한다. 해당 구성의 전송기에 별도로 설치된 drain/vent는 매니폴드의 평형 밸브와 다른 기능이다. 영점 확인과 감압에는 설치 구성에 맞는 제조사 및 현장 승인 절차를 적용한다.
- **`production_schedule_adherence_delivery_kpi`** — 생산 일정 준수·완료 KPI는 기준계획의 버전, 측정기간, 완료 판정, 분자와 분모를 정의한다. 계획 동결 시점을 사용하는 KPI에서는 동결 기준을 명시한다. ISO 22400의 KPI 기술 방식과 SAP의 Schedule Attainment 구현 예는 각각의 적용 범위에서 참고한다.
- **`tolerable_risk_alarp`** — 위험 허용 기준은 적용 법령·규제 및 승인된 위험 기준과 결과 범주에 따라 정한다. 영국 ALARP 문맥에서는 관련 모범 관행과 추가 위험저감조치를 검토하며, 조치를 합리적으로 실행할 수 없다고 판단할 때에는 필요한 희생이 안전상 이익에 비해 현저히 불균형한지 검토한다.
- **`digital_twin_definition`** — ISO 23247-1:2021의 제조용 digital twin은 관측 가능한 제조 요소의 목적에 적합한 디지털 표현이며, 해당 요소와 그 표현 사이의 동기화를 포함한다. 구체적인 동기화 방식과 주기는 용도에 따라 정한다.
- **`half_bridge_sensitivity_compensation`** — 두 활성 게이지가 같은 크기의 반대 변형을 받아 출력이 합산되도록 결선하면, 작은 변형에서 한 활성 게이지를 쓰는 회로보다 감도가 높다. 활성 게이지 하나와 무변형 보상 게이지는 온도 영향 상쇄에 쓰이며 두 활성 게이지의 감도 증가를 만들지 않는다. 회로 명칭은 배치와 제조사 분류를 확인한다.
- **`resistive_sensor_ac_measurement`** — 저항식 습도 센서의 여자 방식은 소자 사양에 따른다. HDK는 HIS-08V가 포함된 HIS-08 계열 저항식 소자에 AC 구동을 지정하고 DC 인가를 제한한다. 구동 파형·주파수와 판독 회로는 해당 제품 지침을 확인한다.
- **`pst_not_full_proof_test`** — 부분행정시험은 실제 시험 자극으로 검출할 수 있는 고장모드에 한해 시험범위를 인정한다. 완전 행정, 요구 격리 및 시트 누설 검증은 SRS가 요구하는 성능과 고장모드를 해당 시험 절차가 실제로 확인하는 경우에만 인정한다.

## 기존 점수 영향이 관측된 기술 문안 2건

최종제어요소 Topic의 아래 두 비제외 Anchor는 후보 문구 적용 시 기존 143건 중 23건의 B점수가 달라졌다. 대상 상태와 라우팅은 유지됐지만, 일부 MISSING 관계에 문장 근거가 추가되거나 제거되어 기존 부분 커버리지에 영향을 주었다. 정확한 관계를 추가로 인정한 결과가 아니므로 후보를 적용하지 않고 기존 정본을 유지한다. 두 제안은 별도 채점 영향 검토 대상으로 남긴다.

- **`deenergized_energized_test_condition`** — 시험은 SRS에 지정된 통전 또는 비통전 트립 방식에 맞추어 실제 신호 경로, 해당되는 전원·유틸리티 상실 및 복구 조건을 검증한다. 단일 수동 행정은 그 시험에 포함된 장치 동작만 확인한다.
- **`partial_stroke_test_risk_controls`** — 운전 중 부분행정시험은 오트립, 공정 교란 및 불완전한 복귀의 가능성을 검토한다. 적용 설비와 SRS에 맞춰 필요한 행정 제한, 중지 수단, 운전자 통지와 시험 후 복귀 확인을 선정한다.

정본의 모든 규칙과 Registry 문장을 통일해야 한다는 가정을 두지 않는다. 제조사 적용예나 더 좁은 모델 조건을 담는 Registry는 기존 범위에서 유지한다. 정본 변경은 Doc/Fact Anchor와 적용되는 긍정 근거 및 Model Answer 설명의 불일치를 고치는 범위로 한정했다. 기존 점수 권한, 요구 Anchor ID, 승인 Ledger, 제외 Overlay 및 운영 설정을 유지했다.
