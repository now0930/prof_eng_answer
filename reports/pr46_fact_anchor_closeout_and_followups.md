# PR #46 우선순위 Fact Anchor 기술 검토 종결

기준 `ffa9222b6f33372efb8b4531e5642d4a8ef74296`. 11건의 기술 검토를 종결한다. 승인 권고 5건은 승인 대기이며, 자연어 채점 개선과 나머지 정본 보완은 별도 후속 과제다. PR은 Draft·병합 보류다.

## 1. Fact Anchor 기술 검토 및 정본

우선순위 11건을 기준 main 및 PR 정본과 정확한 Anchor ID로 대조했다. 이번 정본 수정은 `response_time_process_safety_time`의 적용조건 명시에 한정한다. 동일 문구를 Fact Anchor와 Logic Check에서 동기화했고, Model Answer 의도와 Topic Sheet도 맞췄다. 기존 문제 문구, 요구 Anchor ID와 채점 규칙은 그대로다.

전체 SIF는 해당 위험 시나리오의 PST 내에 요구 안전상태를 달성해야 한다. 최종제어요소 응답시간이 SRS 또는 추적 가능한 설계 시간 예산에 별도로 할당된 경우 해당 할당값을 검증한다. 모든 SRS에서 구성요소별 고정 응답시간 배분이 필수라는 주장은 기술 검토에서 인정하지 않는다. [exida SIF SRS Chapter 8](https://www.exida.com/pub/exSILentiaUserGuide.pdf) · [설계 시간 예산 배분 사례](https://www.arborionglobal.com/services/functional-safety-engineering/functional-safety-lifecycle/phase-3-safety-requirements-specification)

## 2. Registry 승인 및 정합성

[정확한 승인 권고 문장·대상 Fact ID·공식 출처·적용조건](pr46_registry_source_review_proposals.md)을 확정했다. 엔코더 주파수, 결손치, 증분형 엔코더, 열전대, 불완전 시험의 5개 문장은 승인 권고 상태다. 승인 전 Registry·승격 Ledger·source hash 및 제외 Overlay를 유지한다. 사후 반영은 승인된 정확한 문장과 출처 식별정보를 기존 절차에서 기록하고 동일 SHA에서 Builder와 Release Gate를 실행하는 범위다.

나머지 6건은 절대습도·고정 계수창 2건의 핵심 의미 일치, 고장 시 동작과 공정 안전상태·이중화 독립성 2건의 기존 Fact 참조, HIL 1건의 레거시 정본 관리, PST 1건의 조건부 정본 명시로 처리했다.

## 3. 별도 개발 과제 — 자연어 관계 인식과 문항 범위

[기존 관계 인식 재평가](pr46_relation_recognition_reassessment.md)의 20개 사례 ID와 143개 기준선의 결과를 유지한다. 실제 적용 대상에서 놓친 관계 17건과 PST 문항의 범위·기대값 3건을 분리한다. 후자는 Safe State·fail action·de-energize-to-trip을 묻는 문항의 범위 검토 대상이며 정본 정확성 검증과 별개다.

| 후속 범위 | 검증 목표 |
|---|---|
| 개념 및 동의 표현 추출 | 명시적 관계, 용어 나열, 인용·반박의 각각의 근거 위치를 보존한다. |
| 수식 동치와 수치·단위 관계 | 수치에 단위와 적용 대상을 연결하고 수식이 같은 관계를 뜻하는지 검토한다. |
| 조건과 문장 간 인과관계 | 어느 주장에 적용되는 조건인지 명시하고 관계가 모호하면 진단 보류를 유지한다. |
| 문항 범위와 Machine Contract | PST 3건의 평가 기대를 확인한다. 정본 2,096개 중 직접 연결·제외 정책을 통과한 45개라는 현재 범위를 기준으로 비교한다. |

이 과제는 데이터로 표현된 관계의 비교와 자연어에서의 추출을 각각 검증한다. 기존 진단은 오프라인으로 유지한다. 평가기 전면 개편이나 LLM의 A~C 권한 확대에는 별도 설계와 사용자 승인이 필요하다. 자연어 관계 추출 일반화는 이번 기술 검토의 완료 조건에 포함하지 않는다.

## 4. 후속 REVISE 20건 — 작업 범위와 변경 단위

[31건 통합 기록](https://github.com/now0930/prof_eng_answer/issues/42#issuecomment-7148136704)에서 우선순위 11건을 제외했다. Exact ID로 현행 정본을 대조했고 해당 20건의 Anchor 객체는 기존 main과 동일했다. 분류는 중요 기술 보정 3, 적용조건 보완 12, 표현 정밀화 4, 출처 보강 1이다. Overlay 제외 13건과 미등재 7건을 확인했다. 미등재는 실제 사용 확인이나 승격이 아니다. 아래 작업은 각각 소유 Topic의 별도 변경 이력으로 다루며 이번 PR에서 수정하지 않았다.

| Anchor ID | 작업 유형 / Overlay | 현행과 대조한 후속 수정 방향 |
|---|---|---|
| `dp_level_wet_leg_zero_elevation` | 중요 기술 보정 / 제외 | 현행의 ‘음의 차압 발생 가능 → 적용’ 사이에서 조건을 명시한다. 실제 H/L 설치 및 min 레벨에서 공정 수두·wet-leg 수두·고정 오프셋을 합성해 LRV를 구하고 LRV<0인 경우에 zero elevation을 적용한다. |
| `sw09_software_firmware_integrity` | 중요 기술 보정 / 제외 | 자동 인증이 없는 경우 공급자·신뢰된 배포 경로와 해시·서명 등 증거를 대조한다. 격리 시험의 기능 확인과 진위·무결성 입증을 분리한다. [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final) |
| `hazard_scenario_boundary` | 중요 기술 보정 / 제외 | 개시사건과 결과를 구분 평가한다. 동일 위험 결과·SIF에 기여하는 빈도는 공통조건, 종속성, 중복 산입을 검토한 뒤 집계할 수 있도록 현행의 절대적 합산 제한을 좁힌다. |
| `final_element_subsystem_boundary` | 적용조건 / 미등재 | 실제 SIF/SRS 기능에 필요한 요소, 인터페이스 및 유틸리티를 경계로 잡고 isolation·depressurization은 상황별 예시로 둔다. |
| `trip_signal_and_output_chain` | 적용조건 / 미등재 | 릴레이·SOV·액추에이터·밸브는 공압식 예시로 두고 구성별 존재하는 경로를 추적한다. 신호 검증과 공정 안전상태 확인을 구분한다. |
| `dp_level_hydrostatic_pressure_principle` | 적용조건 / 미등재 | 위쪽을 양의 z로 둘 때 dP/dz=−ρg, 아래점 압력−위점 압력은 관측 구간의 ρg 적분으로 쓴다. 일정 밀도 조건을 유지하고 탭과 H/L 접속 방향을 명시한다. |
| `deenergized_energized_test_condition` | 적용조건 / 미등재 | 해당 SRS에 지정된 통전·비통전 트립 방식과 실제 상실·복구 조건만 적용한다. 단일 수동 행정으로 전체 경로가 검증된다는 해석을 배제한다. |
| `partial_stroke_test_risk_controls` | 적용조건 / 미등재 | 공정 영향과 오동작·복구 위험에 따라 한계·중지·알림·복귀 확인을 선정한다. Seat damage는 해당 서비스 근거가 있을 때만 예로 남긴다. |
| `manifold_isolation_sequence` | 적용조건 / 제외 | 기존 Rosemount 2051 모델 범위를 유지한다. 매니폴드의 두 차단 밸브·평형 밸브와 트랜스미터의 별도 drain/vent를 구분한다. Equalizer와 감압 기능은 구분하고 승인된 구성별 절차를 참조한다. |
| `production_schedule_adherence_delivery_kpi` | 적용조건 / 제외 | 기준 계획 버전, 측정기간 및 완료 판정, 분자·분모 정의를 유지한다. Freeze 시점은 해당 KPI 또는 SAP 구현의 적용조건으로 한정한다. |
| `radar_echo_polarity_sign_convention` | 적용조건 / 제외 | 반사식의 공기 근사, 균질·비자성·무손실 매질, 수직 입사 및 실수 εr>1을 명시한다. 손실 매질의 복소 계수와 기기 표시 부호를 각각 구분한다. |
| `radar_adaptive_threshold_echo_tracking` | 적용조건 / 제외 | 거리별 임계값과 false-echo map·거리창·이력·추적을 장치별 선택지로 둔다. 현행의 일괄 동시 적용 표현을 제거한다. |
| `gwr_effective_permittivity_propagation_path` | 적용조건 / 제외 | 기체 구간과 상부 액체 구간 경로를 구분한다. c₀/√εr은 균질·비자성·저손실 근사이며 실제 유효 속도는 프로브 전파 모드와 해당 조건을 따른다. |
| `tolerable_risk_alarp` | 적용조건 / 제외 | 해당 법령과 승인된 위험 기준을 구분하고 gross disproportion은 UK ALARP 맥락에 한정한다. 관할을 넘는 보편 법적 의무를 추가하지 않는다. |
| `thermocouple_junction_construction_response_isolation` | 적용조건 / 제외 | 비교 가능한 치수·유체·보호관·설치조건에서 접점 구조별 경향으로 표현한다. 노출형이 모든 비교에서 가장 빠르다는 단정을 제거한다. |
| `om_asset_register_system_boundary` | 표현 / 제외 | ISO 14224 범위에서 기능·위치의 tag와 개별 장비·교체 이력의 serial을 구분한다. |
| `digital_twin_definition` | 표현 / 미등재 | ISO 23247-1:2021 §3.2.3의 정의명은 digital twin이다. 목적 적합 표현과 동기화에 초점을 맞추고 ‘Instance’를 해당 정의명으로 인용하지 않는다. |
| `lifecycle_maintainability_selection` | 표현 / 제외 | 고분해능에 따른 비용 상승 가능성으로 한정하고 물리 펄스율, 복호 계수율, 필터 한계의 구분을 보존한다. |
| `half_bridge_sensitivity_compensation` | 표현 / 제외 | 활성 게이지의 배치에 따른 감도와 더미의 온도 보상을 구분한다. 회로 명칭은 제조사 분류 범위 내에서 설명하고 물리 관계를 우선한다. |
| `resistive_sensor_ac_measurement` | 출처 / 미등재 | 기존 HIS-08V 제품명은 공식 응용자료와 일치한다. AC 구동·DC 제한을 제품 범위로 입증하고 polarization 기전은 직접 근거가 없으면 중립 표현으로 남긴다. [HDK KRH1901003 §3-3 및 §4](https://www.hdk.co.jp/pdf/tece/appe_krh1901003.pdf) |

기술 보정 3건은 내용 보정과 기존 제외 유지의 독립 검증을 같은 변경에 기록한다. 적용조건과 표현은 소유 Topic 단위로 나눠 후속 진행한다. 표현과 출처만 보완하는 작업은 기존 채점 계약과 평가기를 변경하지 않는다.

## 5. HOLD 9건 — 근거 확인과 시험 필요성

[Issue #42 본문](https://github.com/now0930/prof_eng_answer/issues/42) 4건, [10차](https://github.com/now0930/prof_eng_answer/issues/42#issuecomment-7134265349) 3건, [13차](https://github.com/now0930/prof_eng_answer/issues/42#issuecomment-7134512579) 1건, [14차](https://github.com/now0930/prof_eng_answer/issues/42#issuecomment-7134563950) 1건을 정확한 ID로 추출했다. 9건 모두 현행 정본이 존재하며 실행용 Overlay에서도 제외된다. 역사적 9개 분류와 기존 119 HOLD를 각각 유지한다.

| Anchor ID | 보류 이유와 필요한 근거 | 기술사 답안에서의 필요성 및 방향 |
|---|---|---|
| `dp_level_overpressure_and_static_pressure_effect` | 3051SHP 모델의 단측 과압 및 재영점 요구를 명시한 정확한 매뉴얼·사양과 포트별 경계가 필요하다. | 모델별 조작 항목은 참고용. 정압과 차압 과압의 차이라는 일반 원리만 기존 근거로 다룰 수 있다. |
| `operating_case_force_matrix` | 구성별 유체력·critical travel·시트 하중·마찰에 대한 정확한 sizing 근거와 적용 서비스가 필요하다. | 최악 설계 조건 검토는 유용하다. 상세 case matrix는 제품·프로젝트 예시로 제한한다. |
| `flashing_classification` | 기화 후 하류에서 증기가 지속되는 조건과 포화 경계의 온도·조성 전제에 대한 직접 출처가 필요하다. | 플래싱과 캐비테이션 구분은 핵심이다. 하류 압력 등식만으로 상 지속을 단정하지 않는 문장으로 좁혀 후속 검토한다. |
| `pst_not_full_proof_test` | 부분·완전 시험 각각의 고장 검출 범위와 SRS가 요구하는 차단·누설 검증의 근거가 필요하다. | PST가 완전시험을 대체하지 않는 일반 원리는 중요하다. Full stroke가 언제나 seat leakage까지 검증한다는 범위는 제거 대상으로 본다. |
| `lvdt_null_residual_voltage` | 원시 AC null 잔류와 DC conditioner 오프셋의 구분, 상세 기생 경로 및 고조파의 직접 설명이 필요하다. | null 잔류의 존재는 유용하다. 원인 목록 전체를 필수 답안으로 삼을 필요는 낮다. |
| `lvdt_core_alignment_eccentricity_error` | free-core 방사상 변위 허용조건과 guided 제품의 측면 하중 한계를 각각 확인할 자료가 필요하다. | 축 정렬과 설치 한계는 유용하다. 허용 편심·영향량은 제품별 정보로 둔다. |
| `lvdt_magnetic_saturation_nonlinearity` | 여자 정격, 코어 포화, 고조파 및 선형범위 내 오차를 직접 연결하는 근거가 필요하다. | 정격 여자와 선형범위 준수는 유용하다. 상세 고조파나 규정 범위 내 포화를 보편 주장으로 유지할 필요는 낮다. |
| `sw06_obsolescence_mitigation_options` | SD-22 2016 Table 9의 정확한 원문과 개정판 적용범위가 필요하다. | 일반 단종관리 원칙으로 충분하다. 군수 분류표 전체에 대한 추가 추적은 표준 한정 문항이 있을 때만 한다. |
| `sw06_license_entitlement_continuity` | 적용 라이선스 계약 및 SD-22 2016 예시의 locator가 필요하다. | 사용권·지원 연속성 검토는 유용하다. 다운그레이드 또는 이전·복구 권한은 계약별 문제이므로 일반 채점에서 제외한다. |

후속 출처 검토는 산업 일반성과 시험 필요성이 뚜렷한 일반 원리를 우선한다. 제품이나 관할·표준판에 한정된 세부 주장을 일반 채점에 복귀시키기 위한 작업은 진행하지 않는다.
