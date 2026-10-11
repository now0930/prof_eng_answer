# 전체 Topic Pack Fact 출처 감사 (2026-10-12)

## 최신 상태 — 전체 2,073개 Anchor 검토 완료 (2026-10-12)

전체 2,073개 Anchor를 중복 없이 분류하고 개별 출처 검토를 마쳤다. Fact Registry는 1,515개 레코드이며, 현행 Pack Anchor와 연결되는 고유 검증 Fact는 1,513개다. 구조 경계 51개, Pack scope 확인 18개, 구체적인 owner를 찾지 못한 scope 1개를 별도 분류했다. 나머지 기술 Anchor 490개는 출처를 확인했지만 주장 전체를 확정하기에 부족하여 `unresolved_evidence_insufficient`로 기록했다. 따라서 “전체 검토 완료”는 모든 사실이 검증되었다는 뜻이 아니라, 모든 Anchor가 verified·구조 경계/scope·근거 부족 중 하나로 분류되었다는 뜻이다. 미해결 항목은 승인 Fact Registry에 넣지 않았고 기존 채점 영향도 없다.

스마트 포지셔너 진단 Pack의 35개 미승격 Anchor를 검토했다. 5개는 FIELDVUE/ValveLink 제품·모델별 제한과 계산 가정을 명시해 Fact Registry에 score-neutral로 등록했고, 29개는 근거 부족·범위 과일반화·백분율 기준 모호성 때문에 unresolved로 남겼다. `smart_positioner_diagnostic_scope`는 기술 주장이 아닌 내부 Pack 범위 선언으로 별도 분류했다. 기존 계산 기반 verified Fact 7개는 해당 조건에서만 유지한다. 근거: [Emerson Control Valve Diagnostics](https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics), [Emerson ValveLink Pro manual](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/documents/instruction-manual-fisher-valvelink-pro-solo-software.pdf), [Emerson DVC6200 SIS manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc6200-sis-digital-valve-controller-en.pdf), [Emerson diagnostic guide](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d352709x012.pdf), [HART overview](https://www.fieldcommgroup.org/technologies/hart).

최종요소 SIS/ESD 밸브 및 Partial Stroke Test Pack의 33개 기술 Anchor를 개별 검토했다. 15개는 IEC 61508, HSE, ISA-TR96 및 Emerson 공개 자료 또는 명시적 확률 계산으로 지지되는 범위에서 verified 등록했고, 18개는 구성·SRS·시험절차·FMEDA·운전조건별 근거가 부족해 unresolved로 남겼다. `system_sif_sil_context_boundary`는 내부 topic 소유권 선언으로 구조 scope에 분리했다. 특히 PST coverage는 시험 방법과 검출 고장 집합에 종속되며, full-stroke proof test를 일반적으로 대체하지 않는다고 한정했다. 이 검토에서 채점 점수 영향은 없고 (`score_effect=none`), 모든 후속 기록은 `reports/unresolved_technical_anchor_reviews_20261012.json` 및 `reports/structural_boundary_anchor_review_20261012.json`에 보존한다. 근거: [IEC 61508-1](https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTA4LTF7ZWQyLjB9Yi5wZGY), [IEC 61508-6](https://webstore.iec.ch/en/publication/5520), [HSE Control Systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [HSE Partial Proof Testing Example](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf), [ISA-TR96.05.01](https://www.isa.org/products/isa-tr96-05-01-2017-partial-stroke-testing-of-auto), [ISA-TR96.05.02 preview](https://www.isa.org/getmedia/0fdf7b91-86c4-42e6-9cbe-2f42449204c6/ISA-TR96-05-02-2022-Preview.pdf), [Emerson Control Valve Handbook, Ch. 12](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf).

제어 소프트웨어 프로젝트/FAT·SAT/시운전 팩의 미분류 31개 중 SW-10 범위 선언 1개는 구조 범위로 분리했다. 기술 Anchor 30개 중 6개(FAT, FAT 한계, SAT, FAT/SAT 관계, IEC 62382 loop check, commissioning)는 IEC/ISA/HSE가 직접 뒷받침하는 범위에서 verified 등록했고, 나머지 24개는 프로젝트 문서 체계·수용기준·실행절차에 종속되어 unresolved로 남겼다. 특히 URS/FRS/FDS/SDS 문서 계층, alarm/I/O/tag 목록 필드와 수용·punch closure는 보편 의무 목록으로 보지 않았다. 근거: [IEC 62382:2024](https://webstore.iec.ch/en/publication/67573), [ISA-105 / IEC 62381 overview](https://www.isa.org/standards-and-publications/isa-standards/isa-105-standards), [HSE Commissioning Procedures](https://www.hse.gov.uk/comah/sragtech/techmeasoperatio.htm), [HSE Design Codes—Plant](https://www.hse.gov.uk/comah/sragtech/techmeasplant.htm).

제어 하드웨어 수명주기/패널 아키텍처 팩의 미분류 30개 중 7개는 다른 Topic의 내용을 경계로 명시한 repository scope로 분리했다. 나머지 23개는 IEC 61010, IEC 61131, IPC 제조·조립 표준 및 NIST 공급망 자료와 대조했으나, 대부분은 product/project별 설계·제조 선택사항으로서 해당 목록 전체를 보편 요구로 지지하지 않아 unresolved로 남겼다. 특히 component derating·power margin, thermal 조건, I/O·connector selection, design review, DFM/DFA, production test coverage와 release-gate 절차는 실제 product requirement와 owner QMS가 있어야 확정할 수 있다. 신규 verified Fact는 없으며 채점 영향도 없다. 근거: [IEC 61010-1](https://webstore.iec.ch/en/publication/4279), [IEC 61131-2](https://webstore.iec.ch/en/publication/6078), [IPC J-STD-001/A-610](https://www.ipc.org/meet-your-standards), [NIST SP 800-171 Rev. 3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html).

계측기기 설치/배선/Impulse tubing Pack의 미분류 29개 중 3개는 Pack scope 또는 shield/FAT owner handoff로 구조 scope에 분리했다. 7개는 Rosemount 3051·3051S 설명서가 직접 지원하는 service별 impulse-line 조건과 IEC 60079-14/OSHA 적용 범위의 Ex/IS 설치조건에 한정해 verified로 등록했다. 나머지 19개는 프로젝트 도면, cable·gland 제조사 한계, 적용 법규, 현장 환경 및 owner inspection/turnover 절차가 없으면 보편 규칙으로 확정할 수 없어 unresolved로 남겼다. 특히 OSHA 조항은 해당 미국 규정·대상 cable에만 적용했고, 제조사 impulse-line 권고를 모든 transmitter에 일반화하지 않았다. 근거: [Rosemount 3051 manual (2024)](https://www.emerson.com/documents/automation/manual-rosemount-3051-pressure-transmitter-en-89452.pdf), [Rosemount 3051S manual (2024)](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051s-00809-0200-4802.pdf), [IEC 60079-14:2024](https://webstore.iec.ch/en/publication/66049), [OSHA 29 CFR 1926.405](https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.405).

계측제어 소프트웨어 수명주기/V-Model Pack(SW-04)의 미분류 29개를 검토했다. 범위 선언 1개는 구조 scope로 분리하고, 단위·통합·시스템 시험, Verification/Validation 및 양방향 추적성 7개를 NASA Software Engineering Handbook의 해당 절차와 대조해 독립 검증했다. 나머지 21개는 구성·환경·코딩 규칙·특정 시험기법의 세부목록과 보편 적용 범위를 직접 입증할 근거가 부족해 unresolved로 기록했다. SW-04 29개는 모두 Fact·구조 scope·unresolved로 분류되어 미분류 잔여는 0개다. 전체 후속 검토 내역은 `reports/unresolved_technical_anchor_reviews_20261012.json`, 범위 분류는 `reports/structural_boundary_anchor_review_20261012.json`에 저장한다. 근거: [NASA SWE-067](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604539/SWE-067%2B-%2BVerify%2BImplementation), [NASA SWE-028](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604465/SWE-028%2B-%2BVerification%2BPlanning), [NASA SWE-052](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052%2B-%2BBidirectional%2BTraceability).

프로젝트 관리·Basic Design·Cost/Schedule·문서·인수 Pack의 28개 기술 Anchor를 개별 검토했다. ISO 21502는 프로젝트관리 관행의 고수준 지침, GAO-20-195G는 cost estimate best practice, DOE PEP는 미국 DOE 자본 프로젝트의 실행계획이라는 적용범위로 확인했다. 이 근거만으로 계측 문서목록, tag register, 검사·인수 기준, 특정 단계순서와 handover dossier 전체를 모든 프로젝트의 보편 요구로 확인할 수 없으므로 28개 모두 unresolved에 기록했고 verified 승격은 하지 않았다. 미분류 잔여는 0개다. 근거: [ISO 21502](https://committee.iso.org/sites/tc258/home/projects/published/iso-21502.html), [GAO-20-195G](https://www.gao.gov/products/gao-20-195g), [DOE Project Execution Plan](https://www.energy.gov/projectmanagement/articles/sample-project-execution-plan).

Control Valve Severe Service Pack의 기술 Anchor 27개를 개별 검토했다. Emerson 공식 Control Valve Handbook 및 제품 문서로 differential thermal expansion이 plug/cage binding·looseness 또는 gasket-load/leakage risk를 만들 수 있다는 점, 그리고 particulate가 포함된 유체에서 anti-cavitation trim의 작은 passage가 plugging/erosion 검토 대상임을 해당 제품·구성 범위로 확인해 2개를 verified 등록했다. 그 외 25개는 출처가 설명하는 제품별 설계 사례 또는 일반 배경만으로 보편적인 transient envelope, non-Newtonian/multiphase sizing, purge·orientation·maintenance workflow 등의 전체 문구를 입증할 수 없어 unresolved로 기록했다. 이 Pack의 미분류 잔여는 0개다. 근거: [Emerson Control Valve Handbook, Ch. 6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [Emerson differential thermal expansion guidance](https://www.emerson.com/is/content/emerson/en/final-control/fctl/solutions/common-applications/steam-conditioning-valves/documents/D352003X012.pdf), [Emerson Severe Service](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves).

Industrial IoT/Smart Factory/Digital Thread Pack의 미분류 27개를 검토했다. OPC UA Part 1/3의 AddressSpace, Node, Reference, Information Model 의미와 구현 Profile 경계, IDTA AAS 구조 안내, NIST Digital Thread의 lifecycle 정보 재사용·추적 가능성으로 4개 개념을 한정해 verified 등록했다. 나머지 23개는 cloud/OT 제어경계, buffer·resynchronization, fleet/update·security 운영요건, data-contract 필드 전체, API retry/order/idempotency 또는 digital-thread 추적항목처럼 구현·위험·상호운용성 프로파일에 종속된 상세 처방을 공개 표준 요약만으로 보편 요구라고 입증할 수 없어 unresolved로 기록했다. 미분류 잔여는 0개다. 근거: [OPC UA Part 1](https://reference.opcfoundation.org/specs/OPC-10000-1/5.3.4.4), [OPC UA Part 3](https://reference.opcfoundation.org/specs/OPC-10000-3/full), [IDTA AAS Specifications](https://industrialdigitaltwin.io/aas-specifications/index/home/index.html), [NIST Digital Thread](https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/enabling-digital), [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

HMI/SCADA·Alarm·Setpoint·SOE Pack의 미분류 26개를 대조했다. ISA-18 alarm lifecycle 문서로 Alarm의 actionability, philosophy, rationalization, shelving과 designed suppression의 차이, alarm flood 개념을 한정해 6개를 verified 등록했다. `sw03_scope_operator_information`은 내부 Pack scope로 분리했다. 나머지 19개는 HMI hierarchy/color·alarm KPI 임계값·setpoint 권한·Trip/Interlock 경계·SOE 시간정확도·Historian/First-out/Audit 세부기록처럼 ISA/IEC 적용판, site philosophy, safety allocation 및 제어 플랫폼에 종속된 구체사항을 공개 개요만으로 일반 규칙이라 확인할 수 없어 unresolved로 기록했다. 미분류 잔여는 0개다. 근거: [ISA-18 Series](https://www.isa.org/standards-and-publications/isa-standards/isa-18-series-of-standards), [ISA alarm suppression explanation](https://www.isa.org/intech-home/2017/september-october/features/from-managing-to-optimizing-alarms), [OPC UA SourceTimestamp](https://reference.opcfoundation.org/specs/OPC-10000-4/7.11.3), [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

제어밸브 정비 Pack에서 기술 Anchor 18개를 추가로 상세 검토했고, `seat_leakage_test`에는 기존에 승인된 Fisher HP/HPA TSO 전용 verified Fact가 있음을 재확인했다. 그 Fact는 특정 제품·trim의 factory test 조건만 다루며 모든 밸브의 허용기준으로 일반화하지 않는다. OSHA 29 CFR 1910.147은 적용 범위 내 작업의 위험에너지 통제·격리·저장에너지 처리·격리 확인을, Emerson/Fisher 자료는 특정 밸브 구성의 격리 및 모델별 분해·검사·조립을 지원한다. IEC 60534-4는 적용 범위의 제어밸브 검사·routine test를, IEC 60534-9는 step-input response 측정 절차를 다룬다. 그러나 공개된 요약만으로 정비 후 모든 밸브에 동일한 permit, 감압·세정, 치수 허용치, pressure/stroke 시험 항목과 acceptance limit, accessory fail test, as-left 기록이 보편적으로 요구된다고 확인할 수 없다. 이 18개 Anchor는 전부 unresolved로 두고, 근거 공백과 필요한 후속 확인을 `reports/unresolved_technical_anchor_reviews_20261012.json`에 기록했다. `maintenance_scope_boundary`는 외부 기술 사실이 아니라 내부 Pack 범위 선언으로 분리했다. 신규 verified Fact 및 채점 영향은 없다 (`score_effect=none`).

근거: [OSHA 29 CFR 1910.147](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147), [Emerson Fisher 4320 Instruction Manual](https://www.emerson.com/is/content/emerson/fr/final-control/flow-controls/bu-content/general/documents/d103621x012-manual-fisher-4320-fisher-4320-wireless-position-monitor-fisher-5.pdf), [Emerson Control Valve Handbook, Chapter 8](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [IEC 60534-4:2021](https://webstore.iec.ch/en/publication/31136), [IEC 60534-9:2007](https://webstore.iec.ch/en/publication/2477).

Physical AI Pack의 나머지 21개 미검토 Anchor도 출처 범위를 확인했다. ISO 10218/TS 15066은 산업용 robot system·application·cell 안전 및 collaborative application의 system 성격을, ISO 23247은 manufacturing digital twin의 fit-for-purpose representation과 동기화를 정의한다. NIST AI RMF는 맥락 기반의 AI 위험관리·모니터링을 지원한다. 그러나 이 자료들은 Physical AI의 보편 정의, 모든 sensor 조합의 상보성, world-model schema, 동일한 safety envelope/fallback/ODD/runtime metric 목록을 규정하지 않는다. 따라서 21개는 모두 미해결 기록으로 남겼고 verified로 승격하지 않았다. 기존에 승인된 `industrial_robot_architecture`, `collaborative_robot_application`, `digital_twin_definition`, `digital_twin_fidelity`, `simulation_scenario_coverage`, `synthetic_data_domain_gap`, `localization`, `timestamp_and_synchronization`, `observability_limits` Fact는 각각의 제한된 문구·범위에만 적용된다. 근거: [ISO/TS 15066](https://www.iso.org/standard/62996.html), [ISO 10218-2:2025](https://www.iso.org/standard/73933.html), [ISO 23247-1:2021](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A23247%3A-5%3Adis%3Aed-1%3Av1%3Aen), [NIST AI RMF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf).

제어밸브 선정 Pack의 49개 기술 Anchor를 모두 개별 검토했다. sizing·installed characteristic·response·actuator·inspection 등은 IEC/ISA/제조사 자료가 개념이나 특정 test scope를 지원하지만, 나머지 통합 checklist·프로젝트 절차·수치 기준은 universal requirement로 확정할 수 없어 unresolved로 남겼다. 기존에 승인된 Fact는 별도 제품/계산 범위로만 유지한다. 현재 Pack에는 상세 검토 전 기술 Anchor가 없다. 전체 Pack 목록 중 다음 미검토 Pack은 smart-positioner diagnostics다. 근거: [IEC 60534-2-1:2011](https://webstore.iec.ch/en/publication/2461), [IEC 60534-4:2021](https://webstore.iec.ch/en/publication/31136), [IEC 60534-9:2007](https://webstore.iec.ch/en/publication/2477), [Emerson Control Valve Sizing](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valves-sizing), [ISA installed-characteristic guidance](https://www.isa.org/intech-home/2023/june-2023/features/understanding-control-valve-flow-characteristics), [HSE Control Systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm).

## 진행 이력 (2026-10-12; 이후 갱신은 하단의 최신 상태 참고)

현재 승인 Fact **1,452개**, 고유 Anchor 연결 **1,450개**, 미검증 기술 Anchor **572개**다. `deployment_environment`는 NIST AI RMF의 deployment-similar evaluation, Google MLOps의 인프라/API 호환성 검증, scikit-learn의 runtime dependency 조건으로 대조했다. 입력 Schema·전처리·Prediction API와 필요한 runtime 호환성은 배포 경로에서 확인하되, Sensor·Hardware·Latency 허용기준은 시스템별로 정하도록 범위를 제한해 승인했다. `retraining_trigger`는 Google MLOps가 제시하는 일정·새 자료·성능저하 등 선택형 trigger와 배포 전 validation/baseline comparison에 맞춰 확인했다. 공정변경·drift는 재평가 신호이지 자동 재학습·배포의 충분조건이 아니라고 한정했다. 반면 `process_optimization_boundary`, `decision_cost_and_lead_time`, `regression_and_champion_challenger`는 관련 일반 가이드가 개념 일부만 지원하고 Anchor의 보편적 목록·구조 전체를 입증하지 못해 미해결로 남겼다. 특히 최적화 출력과 SIS/승인 경계, 현장 KPI·비용항목, 동일 Test/Replay/Stress 및 전체 성능·Latency·운영비용 회귀시험은 적용 공정과 위험기반 요구가 필요하다. Sequence/Interlock Topic의 9 Anchor도 장치·안전요구·운전철학에 따른 차이를 확인해 미해결 검토에 기록했다. 특히 `sw02_override`는 ISA의 process override-control 용례와 “강제 명령” 정의가 충돌할 수 있어 operator command priority, controller force, selector control, SIS bypass 중 의도한 의미를 구분해야 한다. 전체 상세 미해결 검토 25건이며, 이 중 25건을 포함해 기술 미검증 572개 중 547개가 아직 개별 상세 검토 전이다.

환경 Qualification Topic의 추가 11개 Anchor(`ieeq_scope_chain`, `ieeq_operating_mode_worst_case`, `ieeq_pretest_baseline`, `ieeq_vibration_functional_monitor`, `ieeq_post_vibration_inspection`, `ieeq_combined_environment_interaction`, `ieeq_failure_evidence_capture`, `ieeq_failure_root_cause`, `ieeq_corrective_action_retest`, `ieeq_traceable_report`, `ieeq_change_control_requalification`)는 IEC 60068의 공개 scope·시험 요약과 대조했다. 시험-tailoring과 mechanical/performance degradation 확인은 지지되지만, 모든 시험군에 동일한 운영모드·감시목록·고장분석·재시험·보고 필드를 적용한다는 주장은 공개 요약만으로 확인되지 않아 미해결 등록했다. 상세 적용은 정식 표준 전문과 제품별 acceptance plan이 필요하다. 이에 따라 상세 미해결 검토는 36건이며, 기술 미검증 572건 가운데 개별 검토가 끝나지 않은 Anchor는 536건이다.

## 최신 상태 — quantum Topic 검토 이후

승인 Fact 1,456개, 고유 Anchor 연결 1,454개, 구조·범위 경계 51개, 상세 미해결 검토 48개다. 총 2,073개 중 기술 Anchor 568개는 아직 verified가 아니며, 그중 48개는 상세 근거 검토 후 미해결로 분류했고 520개는 개별 상세 검토 전이다. Quantum Topic에서는 NIST 자료를 통해 sensing과 computing의 기능 구분을, NIST/IBM 자료로 hybrid classical-quantum architecture를, peer-reviewed Quantum 논문으로 input-state preparation cost를, NIST 자료로 device quality/resource trade-off를 조건부 Fact로 검증했다. 산업 최적화·estimation 후보, hard-real-time 경계, latency, maturity·benchmark·pilot·TCO·security governance 등의 12개 문구는 현재 기술 성숙도나 workload별 근거가 부족하거나 권고 프레임이므로 미해결로 남겼다.

## 최신 상태 — 산업 통신 Topic 검토 이후

승인 Fact 1,458개, 고유 Anchor 연결 1,456개, 구조·범위 경계 51개, 상세 미해결 검토 63개다. 총 2,073개 중 기술 Anchor 566개는 아직 verified가 아니며, 그중 63개는 상세 근거 검토 후 미해결로 분류했고 503개는 개별 상세 검토 전이다. 산업 통신 Topic에서는 FOUNDATION Fieldbus의 profile-dependent 디지털 필드 장치·host 통신 범위와 OPC UA의 정보통합 역할/구성에 따른 hard-real-time 한계를 검증했다. 나머지 15개는 통신 선정 기준, copper/fiber trade-off, topology, commissioning 순서, gateway semantic mapping, lifecycle compatibility 등 추천·구현 조합의 범위가 표준 또는 protocol마다 달라 보편 Fact로 승인하지 않고 상세 검토에 기록했다.

## 집계 이력 — 직전 업데이트 (2026-10-12)

현재 최신 재계산: 승인 Fact **1,432개**, 고유 Anchor 연결 **1,430개**, 미검증 기술 Anchor **592개**. `sw01_common_cause_failure`는 NRC의 공통원인고장 정의와 사례 및 동일 소프트웨어 결함의 다중 채널 영향까지 대조해 score-neutral 등록했다. `sw07_layered_view`는 Modbus 응용계층/TCP-IP 매핑과 OPC UA 정보모델·프로파일·전송 매핑 구조를 대조하고, 보편적인 단일 계층 모델이 아니라 분석 관점이라는 경계를 조건으로 등록했다. `sw07_device_profile`은 PI의 PROFINET profile 정의 및 PROFIdrive 검증 범위를 대조해, 장치 class의 필수·선택 기능과 파라미터/진단 의미를 표준화해 동일 profile scope 안에서 vendor-neutral host 접근성을 높이는 주장으로 조건화했다. `sw07_rs485_multidrop`은 TI·Analog Devices 자료로 물리계층 주장을 일부 확인했지만 주소 및 접지·차폐까지 보편화하지 않고 미해결 검토에 남겼다. `sw07_modbus_rtu`는 프레임 구조와 device-specific mapping을 확인했으나, bit table과 표준 big-endian 규칙을 구분하지 않은 채 byte order 전반을 device-dependent라고 표현해 미해결로 유지했다. `sw07_conformance_vs_interoperability`는 인증 제도에 따라 상호운용 시험도 포함될 수 있고 조합 시험·승인목록은 프로젝트 조건에 좌우되어 보편 명제로 확정하지 않았다. 따라서 미해결 상세 검토는 10건이며, 모두 기술 미검증 수 592개 안에 포함된다. 아래 이어지는 상세 요약의 직전 집계 수치는 이 갱신 전 스냅샷이다.

현재 재계산은 Fact 기록 **1,429개**, 고유 Anchor 연결 **1,427개**, 미검증 기술 Anchor **595개**다. Smart Positioner Topic의 `command_travel_error_signed`, `full_span_travel_error`, `up_down_hysteresis_signature`, `baseline_residual_context`, `rate_of_change_time_domain`, `accumulated_travel_direction_reversal`, `actuator_pressure_open_close_band`는 명시된 계산 정의와 domain 조건을 수치 대입·차원 확인으로 검증해 승인 registry에 score-neutral Fact로 추가했다. `command-minus-measured` 부호는 유일한 업계 표준이라고 주장하지 않고 정의된 convention으로 한정했다. 누적 이동량은 샘플 기반 total variation으로 제한하며 샘플 사이 관측되지 않은 이동까지 포착한다고 주장하지 않는다. 개별 pressure band는 단독 root-cause 진단이 아닌 signature feature로 한정했다. 수리가능 단일 시스템의 `A=MTBF/(MTBF+MTTR)`와 독립고장 직렬·병렬 reliability 관계도 확률식에서 도출하고 각각의 적용 경계를 기록했다. `sw01_reliability_definition`은 NIST IR 8323 Rev. 1 용어집 정의와 대조해 요구기능·조건·시간구간을 포함하는 실패 없는 수행 확률로 확인했다. `sw01_maintainability_definition`은 IEC 60300-3-10:2025의 restore/ease/speed 정의, 시간 내 정비조치 측정, accessibility·절차 조건, fault finding 및 modular replacement 관련 내용을 대조했다. 영향요인은 비한정 예시로 기록했다. `sw01_availability_definition`은 IEC 60300-3-10의 readiness 및 uptime/total-time measure와 IEC 61703의 수명주기 신뢰성·가용도 척도 경계를 대조했다. availability 수치는 측정의 operational profile과 downtime 정의를 특정해야 하므로 instantaneous probability와 uptime ratio를 동일한 지표로 취급하지 않도록 관계 조건을 기록했다. `percent_change_domain`은 음수 baseline에서 절대값 분모를 쓰는 비율을 일반적인 percentage change라고 부를 수 있는지 모호해 미승격 상태로 두었다.

습도·환경 Qualification 후속 검토에서는 `ieeq_in_test_monitoring`, `ieeq_humidity_recovery_check`, `ieeq_humidity_failure_mechanisms`를 최신 IEC 60068-2-30:2025 및 IEC 60068-2-78:2025의 공개 공식 요약과 대조했다. 요약은 cyclic damp heat의 일반적인 표면 응축, steady-state damp heat의 비응축 조건, 중간측정·보고 변경 등 시험 범위는 확인해 주지만 각 Anchor에 적힌 상세 감시 신호, 회복·절연·부식 판정, 복합 failure mechanism 전체를 입증하지 않는다. 그러므로 세 Anchor는 승인 Fact에 넣지 않고 `reports/unresolved_technical_anchor_reviews_20261012.json`에 근거 공백과 후속 확인조건을 기록했다. 상세 조항은 적용 판본의 전문과 제품별 qualification 계획이 필요하다. [IEC 60068-2-30:2025](https://webstore.iec.ch/en/publication/82356), [IEC 60068-2-78:2025](https://webstore.iec.ch/en/publication/82357).

이전 진행 시점의 재계산 값은 Fact 기록 **1,417개**, 고유 Anchor 연결 **1,415개**, 미검증 기술 Anchor **607개**였다. 이 수치는 Topic Pack, 승인 Fact registry, 구조·범위 감사 등록부의 고유 `(topic_id, anchor_id)`를 대조해 산출했다. `precision_metric`은 scikit-learn 공식 API와 사용자 가이드의 TP/(TP+FP) 정의로 확인했다. Binary classification에서 Positive 판정 중 실제 Positive 비율이며 TP를 고정한 채 FP가 증가하면 Precision은 감소한다. Positive 예측이 없는 경우의 미정의 처리도 경계 조건으로 기록했다. `score_effect=none`이다. `sw03_alarm_deadband`는 ISA-TR18.2.5, Rockwell 및 Emerson 자료로 확인했다. Deadband는 활성화와 해제 임계값 사이 hysteresis로 경계 부근 반복 알람을 줄이며, 설정값은 공정 신호 노이즈와 필요한 응답에 맞춰야 한다. `sw03_alarm_priority`는 ISA-TR18.2.2, ISA InTech 및 Emerson Alarm Rationalization 자료로 대조해 consequence severity와 allowable response time을 함께 고려하는 site-defined priority matrix로 한정했다. `sw03_alarm_state_acknowledgement`는 Rockwell과 Emerson 제조사 문서에서 acknowledgement와 active/clear 상태가 별도임을 확인했다. 이 세 등록도 `score_effect=none`이다.

이전 시점의 미검증 607개 중 네 개의 compound/범위 민감 Anchor(`mcdc_safety_plc_boundary`, `orientation_thermal_cycle_history`, `specification_test_lifecycle_workflow`, `sw02_scan_edge_memory`)는 출처를 확인했으나 문장 전체를 뒷받침하지 못해 별도 미해결 검토 기록에 근거 공백과 다음 확인 조건을 남겼다. 이들은 승인 Fact로 등록하지 않았다.

`instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`의 `ieeq_temperature_operating_storage`는 IEC 60068-1:2013 tailoring framework와 IEC 60068-2-1/-2-2:2025 최신판 scope를 대조해 검증했다. 운전·수송·저장 use condition, heat-dissipating/energized specimen 및 온도 안정화 구분을 확인했고, temperature-change effect는 별도 시험방법으로 다뤄야 한다. self-heating·thermal gradient는 제품 구성과 설치환경에 따라 고려할 engineering variable이지 고정 시험조건으로 일반화하지 않는다. `score_effect=none`이다.

같은 Topic의 `ieeq_requirement_traceability`는 IEC 60068-1의 intended-use 기반 test-tailoring framework에 대조해 검증했다. 시험방법과 severity는 운전·수송·저장 조건 및 적용 제품·프로젝트 요구로 정당화해야 하며 모든 장비에 적용하는 고정 profile이 아니다. `score_effect=none`이다.

`ieeq_vibration_mounting`은 IEC 60068-2-47:2005와 IEC 60068-2-6:2007의 specimen mounting·fixing point·measurement point 조건으로 검증했다. Normal service mounting, fixture rigidity/resonance, 케이블·배관 restraint/mass, bolt size·torque는 해당 제품 규격에 따라 설정하며, 보편적으로 동일한 fixture/torque를 강제하지 않는다. `score_effect=none`이다.

같은 Topic의 `recall_metric`은 scikit-learn 공식 문서에서 TP/(TP+FN)과 false negative의 정의를 확인했으며, 위험 고장 미검출이 중요한 경우라는 조건부 의미를 유지했다. `confusion_matrix`는 공식 사용자 가이드와 API의 TP/FP/TN/FN 정의에서 오경보와 미검출의 구분을 확인했다. `f1_metric`은 Precision·Recall 조화평균 공식과 TP/FP/FN 수식으로 확인했고, 운영비용과 공정조건은 F1 계산식에 포함되지 않는다는 한계를 함께 기록했다. 세 등록 모두 `score_effect=none`이며, 지표 정의만으로 현장 비용·경보 임계값을 결정하지 않는다.

`pressure_temperature_rating_and_class`는 ASME 공식 B16.34-2025 범위에 대조했다. 해당 표준의 적용 대상인 신규 valve construction과 material별 pressure-temperature rating·시험·표시 사항으로 한정했으며, 배관·flange에 보편 적용되는 기준이라고 확대하지 않는다. `score_effect=none`이다.

`sw07_device_description`은 FieldComm Group EDDL, PI GSDML, ODVA EDS 및 ETG ESI 문서의 역할을 교차 확인했다. 각 형식이 장치 파라미터·기능·진단·통신·process data 중 서로 다른 범위를 기술한다는 점으로 한정했고, 어느 형식이든 모든 정보를 포함하거나 서로 교환 가능하다고 주장하지 않는다. `sw07_wireless_power_lifecycle`은 WirelessHART 설계 지침의 update rate/배터리 관계, FieldComm Group의 power budget·화학·교체 안전 지침, Emerson 648의 제품별 routing·온도 기준을 확인했다. `sw07_wireless_site_survey`는 NIST 산업 무선 배치 가이드의 factory/RF survey, 주파수·간섭·channel planning, 금속 반사·장애물·높이, installed-device black-box test와 network monitoring을 확인하고 FieldComm Group의 WirelessHART site-walkdown/coexistence 권고로 보강했다. 조사·측정 범위는 적용 환경과 기술에 맞춰야 하며 고정 설치높이나 채널구성을 일반화하지 않는다. 세 등록 모두 `score_effect=none`이다.

`sw07_modbus_rtu`는 문구 전체 확인을 위해 미검증으로 유지한다. Modbus Application Protocol은 주소와 data item의 다중 바이트 전송을 big-endian으로 규정한다. 반면 application-level register meaning/unit/scale은 장치 mapping에 따르며, 32-bit·실수 등 여러 16-bit register의 word ordering은 구현별 확인이 필요하다. 현재 Anchor의 “byte order는 장치 문서와 mapping에 의존”은 16-bit protocol field와 multi-register value의 byte/word order를 구분하지 않아 그대로 verified 처리하지 않았다. 확인된 부분을 유지하려면 주장 분리 또는 표현 정밀화가 필요하다. 근거: [Modbus Application Protocol V1.1b3, §4.2 Data Encoding](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf), [Modbus Organization FAQ / Introduction](https://www.modbus.org/introduction-to-modbus).

`mcdc_industrial_application_boundary`를 verified로 추가했다. IEC 61508-3의 공식
범위는 안전관련 시스템의 소프트웨어이며, 조치·기법은 요구 Systematic Capability에
맞춰 등급화된다. NASA SWE-189도 coverage 기준을 software classification과 system
requirements에 맞춰 선정하고 등급별 기대가 달라짐을 설명한다. 따라서 MC/DC를 모든
일반 PLC·HMI에 일괄 적용하는 주장이 아니라 적용 대상과 coverage 기준을 안전분류·요구에
맞춘다는 현재 Anchor 범위로 확인했다. NASA 자료는 NASA 프로젝트 지침 범위의 근거로만
사용했다. [IEC 61508-3](https://webstore.iec.ch/en/publication/5517),
[NASA SWE-189](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695524/SWE-189%2B-%2BCode%2BCoverage%2BMeasurements).

`mcdc_safety_plc_boundary`는 아직 미검증이다. Rockwell GuardLogix Safety Reference
Manual은 특정 인증 제품에서 Safety Application Program의 specification 기반 test
case, critical-value/range 확인, I/O channel 및 전체 safety function의 현장 기능시험과
safety signature 관리를 요구한다. 이는 인증된 controller를 써도 application-specific
검증이 별도로 필요함을 뒷받침한다. 그러나 해당 단일 제품 매뉴얼만으로 모든 Safety PLC의
내부 firmware MC/DC 재수행 조건을 일반화할 수 없어 복합 Anchor 전체는 미승격으로 남긴다.
[Rockwell GuardLogix Safety Reference Manual 1756-RM093](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/1756-rm093_-en-p.pdf),
[GuardLogix safety application requirements](https://www.rockwellautomation.com/en-us/docs/technical/logix5000/_online/1756-rm012/guardlogix-5580-and-compact-guardlogix-5580-safety/safety-applications.html).

추가 검토에서 `fibrous_sticky_polymerizing_plugging`은 미검증으로 유지했다. Valmet의
제지 공정증기 사례는 특정 밸브에서 섬유 축적과 잠재적 plugging, fines/fibers 존재 시
Q-Trim을 신중히 평가할 필요를 직접 뒷받침한다. 별도 polymer-slurry 보고서는 특정
제품의 seat·bearing cavity/groove 내 polymer buildup을 설명하고, Fisher EZ 자료는
sticky/non-lubricating fluid 및 entrained-solids buildup이 plug sticking 가능성과
연관됨을 설명한다. 그러나 이 자료들은 Anchor가 결합한 모든 fibrous·sticky·polymerizing
fluid에서 narrow passage, cavity 및 dead zone의 bridging·deposit·plugging을 함께
일반화하지 않는다. 특히 bridging 기계작용을 해당 밸브 운전조건에서 직접 지지하는 자료를
확보하지 못했으므로, 확인된 부분 근거만으로 복합 Anchor를 verified 처리하지 않았다.
추후에는 개별 주장으로 분리·축소한 뒤 각 범위에 맞춰 재검토한다. [Valmet process-steam
application report](https://www.valmet.com/globalassets/sharepoint/imported/2621_06_01en.pdf),
[Valmet polymer-slurry application report](https://www.valmet.com/globalassets/sharepoint/imported/2722_08_01en.pdf),
[Emerson Fisher EZ product documentation](https://www.emerson.com/en/final-control/products/fisher-ez).

Fisher 제조사 자료로 `stem_shaft_packing_leakage_paths`와
`packing_material_ring_arrangement`의 과도하게 일반적인 문구를 좁혀 확인했다.
Rotary와 sliding-stem packing의 차이는 Sourcebook이 직접 설명하는 motion에 따른
packing material 이동 경향 및 흔한 운전압력 비교로 한정했다. 재료·배열 Anchor는 Fisher
sliding-stem 제품별 pressure-temperature 적용 범위와 single/double 구성·부품 예시로 제한했으며,
제조사 공통 chemical compatibility 규칙으로 확대하지 않았다.

최신 등록부는 1,382개 Fact 기록이며, 1,381개가 Anchor 연결, 1개가 독립 사실이다.
`sw07_modbus_tcp`를 Modbus Organization의 Application Protocol과 TCP/IP Messaging Guide에 대조해 verified로 추가했다. PDU와 transport mapping의 분리, vendor/device-specific data mapping, MBAP Unit Identifier의 gateway routing 용도와 TCP connection 관리가 각각 명시돼 있다. Direct TCP server에서 Unit Identifier가 non-significant일 수 있다는 조건도 함께 기록했다. [Modbus Application Protocol V1.1b3](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf), [Modbus TCP Messaging Guide V1.0b](https://www.modbus.org/file/secure/messagingimplementationguide.pdf).

`sw07_hart_overlay`를 FieldComm Group의 HART 기술 설명과 command-set 자료에 대조해 verified로 등록했다. 4–20 mA 아날로그 채널과 중첩 digital FSK 채널의 병행, PV·상태·진단·추가 변수 전달, 지원 명령을 통한 parameter/range 설정을 확인했다. 개별 장치의 command와 variable 지원 차이는 조건으로 남겼다. [HART Technology Explained](https://www.fieldcommgroup.org/technologies/hart/hart-technology-explained), [FieldComm Group HART command-set guide](https://www.fieldcommgroup.org/sites/default/files/imce_files/technology/documents/HART_FCG_AG10319%7B1.0%7D_How-to-Develop-and-Register-a-WirelessHART-Device.pdf).

`sw07_hart_multidrop`을 FieldComm Group HART Application Guide와 Emerson/Biffi의 제품 매뉴얼로 확인했다. 한 쌍 배선에서 여러 장치의 디지털 process value를 전달하고 polling address를 고유하게 할당하며, HART revision에 따라 address 범위가 달라지고 loop current는 최소값(통상 4 mA)으로 고정될 수 있다. 전원·종단 조건은 선택 장치와 설계에 종속된다고 한정했다. [FieldComm HART Application Guide](https://www.fieldcommgroup.org/sites/default/files/imce_files/technology/documents/HART_ApplicationGuide_r7.1.pdf), [Emerson/Biffi HART Bus Module Manual](https://www.emerson.com/is/content/emerson/en/final-control/shared-assets/biffi/installation-and-maintenance-instructions/documents/manuals-biffi-icon3000-elehrt-24-hart-bus-module-en-us-11639244.pdf).

2026-10-12 후속 검증을 포함한 현재 수치는 Fact 기록 1,404개, 고유 Anchor 연결 기록 1,402개, 미검증 기술 Anchor 620개다. `sw07_opcua`는 OPC Foundation OPC 10000-1/3/4에 대조해 verified로 추가했다. Part 1의 platform-independent 범위·AddressSpace 정보모델, Part 3의 Variables·Methods·Events 구조, Part 4의 Method·MonitoredItem·Subscription 서비스 정의가 각각 확인됐다. Profile과 서버 구현에 따라 capability가 달라질 수 있고, 자동 의미 상호운용이나 보편 실시간 성능은 주장하지 않았다. 근거: [OPC UA Part 1](https://reference.opcfoundation.org/specs/OPC-10000-1/full), [Part 3](https://reference.opcfoundation.org/specs/OPC-10000-3/full), [Part 4](https://reference.opcfoundation.org/specs/OPC-10000-4/4).

`sw07_profibus_pa`는 PROFIBUS & PROFINET International의 System Description과 Design Guideline으로 확인했다. MBP가 버스 전력과 통신을 같은 케이블에서 전달할 수 있고, PA profile이 지정된 장치 기능·데이터 형식·진단을 표준화하며, PA segment는 coupler/link로 DP와 연결될 수 있음을 확인했다. 종료저항 양단 배치와 방폭 구분은 설치 설계에 따라야 한다. 모든 PA 장치가 버스전원형이거나 모든 segment가 같은 topology라는 의미는 아니다. 근거: [PROFIBUS System Description](https://se.profibus.com/fileadmin/media/downloadsection/PROFIBUS_Systembeschreibung_ENG_web.pdf), [PROFIBUS Design Guideline](https://www.profibus.com/fileadmin/media/downloadsection/installation_guide/PROFIBUS_Design_Guideline_8012_V129_Sep20.pdf).

`sw07_foundation_fieldbus`는 FieldComm Group의 기술 개요와 System Engineering Guideline으로 확인했다. 표준 User Layer의 function block·Device Description·진단 기능과 H1 segment의 전원조절·coupler·spur/barrier 구성 및 trunk 양단 두 개 종단 조건을 대조했다. 블록 availability와 host compatibility는 선정 장치·호스트 기준으로 확인해야 하므로 이를 자동 보장으로 일반화하지 않았다. 근거: [FOUNDATION Fieldbus Technology Explained](https://www.fieldcommgroup.org/technologies/foundation-fieldbus/foundation-technology-explained), [System Engineering Guidelines, Rev. 3.2.1](https://www.fieldcommgroup.org/sites/default/files/imce_files/technology/documents/Ff_system_engineering_guidelines_version_3.2.1.pdf).

`sw07_foundation_fieldbus_function_blocks`는 FieldComm Group의 FF-890 기능 블록 사양 개요와 engineering guideline으로 확인했다. 사양은 기본 및 확장 function-block 유형의 정의를 규정하고, guideline은 application block의 schedule/use가 설정 대상이며 장치 제조사와 host 양쪽의 기능 지원을 확인하라고 명시한다. 따라서 상호운용성은 지원·인증 범위 내 기능으로 한정했다. 근거: [FOUNDATION Fieldbus specifications](https://www.fieldcommgroup.org/foundation-fieldbus-technical-specifications), [System Engineering Guidelines, Rev. 3.2.1](https://www.fieldcommgroup.org/sites/default/files/imce_files/technology/documents/Ff_system_engineering_guidelines_version_3.2.1.pdf).

`sw07_serial_communication`은 NI와 Siemens의 serial communication 문서 및 Modbus Organization의 RTU framing guide를 대조했다. 순차 bit 전송과 baud/character frame 설정, 인터페이스별 duplex·전기적 특성 차이를 확인했다. RTU의 server address는 상위 protocol frame에 속하며 모든 point-to-point serial link의 보편 속성이 아니라고 제한했다. 근거: [NI Serial Port Communication](https://www.ni.com/docs/es-ES/bundle/labview/page/serial-port-communication.html), [Siemens Serial Data Transmission](https://docs.tia.siemens.cloud/r/simatic_s7_1500_et_200mp_manual_collection_enus_21/comprehensive-information/communication-function-manuals/cm-ptp-configurations-for-point-to-point-connections/basics-of-serial-communication/serial-data-transmission), [Modbus Serial Line Guide](https://www.modbus.org/file/secure/modbusoverserial.pdf).

`sw07_ethernetip_cip`는 ODVA 개발자 가이드와 EtherNet/IP architecture 자료를 대조했다. CIP object/service/device profile의 application 역할과 EtherNet/IP의 Ethernet·TCP/IP mapping, Scanner의 I/O connection 요청, Adapter의 target 응답, EDS 기반 configuration을 확인했다. 구체 profile·connection capability와 controller/Scanner 호환성은 장치별로 점검해야 한다. 근거: [ODVA EtherNet/IP Quick Start](https://www.odva.org/wp-content/uploads/2020/05/PUB00213R0_EtherNetIP_Developers_Guide.pdf), [ODVA EtherNet/IP Adapter Class Products](https://www.odva.org/wp-content/uploads/2024/04/PUB00138R8_Ethernet.pdf).

`sw07_profinet`은 PI System Description과 GSDML/Conformance 문서로 확인했다. IO Controller/IO Device 역할, cyclic IO·acyclic record 서비스·alarm 채널 및 GSDML에 기록되는 device structure·process data·parameter·diagnostics를 대조했다. Conformance class와 controller-device 기능 조합은 실제 버전과 구현별로 확인해야 한다. 근거: [PROFINET System Description](https://sea.profibus.com/fileadmin/media/downloadsection/technical_description_%26_books/PROFINET_System_Description_engl_2018_Update.pdf), [GSDML specification](https://uk.profibus.com/downloads/gsdml-gsdx-specification-for-profinet), [PROFINET test specification](https://www.profibus.com/download/profinet-test-specification/).

`sw07_ethercat`은 EtherCAT Technology Group의 기술 설명과 SubDevice implementation guide로 확인했다. frame이 통과하는 동안 SubDevice가 할당된 process data를 읽고 쓰는 방식, ESI를 사용한 ENI/network configuration 생성, 계획 topology와 실제 topology 비교를 대조했다. ESI·포트·topology 지원은 장치별이므로 모든 장치가 모든 구성을 지원한다고 확대하지 않았다. 근거: [ETG EtherCAT technology](https://www.ethercat.org/en/technology.html), [ETG.2200 SubDevice Implementation Guide](https://www.ethercat.org/download/documents/ETG2200_V3i1i0_G_R_SlaveImplementationGuide.pdf).

`sw07_wirelesshart`는 FieldComm Group의 WirelessHART 개요, system engineering guide 및 security 안내로 확인했다. Mesh field device·Gateway·Access Point·Network Manager와 host 연계, manager의 configuration/scheduling/routing/network health 기능, join key 및 network provisioning을 확인했다. Manager가 gateway·host·controller 중 어디에 통합되는지는 제품별일 수 있으므로 하나의 고정 배치를 전제하지 않았다. 근거: [WirelessHART overview](https://www.fieldcommgroup.org/technologies/wirelesshart), [IEC 62591 System Engineering Guide](https://www.fieldcommgroup.org/sites/default/files/imce_files/technology/documents/WirelessHART_system_eng_guide.pdf), [WirelessHART Security](https://www.fieldcommgroup.org/wirelesshart-security).

`sw07_isa10011a`는 ISA의 ISA-100.11a 표준 범위 정보와 Yokogawa 기술자료, 표준 본문에서 네트워크 역할을 대조했다. Field device·backbone router·gateway 및 management 역할과 host 연결을 확인했으며, gateway/system/security manager 역할은 하나의 장비에 통합되거나 분리될 수 있어 고정 하드웨어 구성을 주장하지 않는다. 실제 host/application mapping은 대상 profile과 장치 지원을 확인해야 한다. 근거: [ISA-100 Standards](https://www.isa.org/standards-and-publications/isa-standards/isa-100-standards), [Yokogawa ISA100.11a integration report](https://yokogawaelectric.org/library/resources/yokogawa-technical-reports/worlds-first-wireless-field-instruments-based-on-isa10011a/index.html), [ISA-100.11a-2011 text](https://www.normsplash.com/FreeDownload/124617698/ISA-100.11a-2011-en.pdf).
미승격 검토 기록: `operating_case_envelope` 및 `min_normal_max_transient_cases`는 제조사 자료가 min/normal/max와 “all possible process conditions”를 고려하라고 지지하지만, cleaning·depressurization·모든 upset을 모든 밸브의 의무 operating case로 열거하지는 않는다. 필요한 운전 사례는 실제 공정·설계 basis에 따라 정해야 하므로 보편 문구를 그대로 verified 처리하지 않고 미검증으로 유지한다.
추가 유보: `differential_growth_binding_leakage`의 출처는 differential expansion에 의한 binding/과도한 간극과 seat 계통 누설은 뒷받침하지만 galling의 인과까지 직접 확인하지 못해 전체 Anchor는 미검증으로 둔다. `installed_rangeability_handoff`는 installed characteristic의 시스템 압력 의존성은 확인 가능하나, 문구의 `process gain`과 Topic 5 소유범위까지 같은 근거가 증명하는지 불충분해 보류한다.
중복 Topic–Anchor 연결을 제외한 verified 고유 매핑은 1,380개다. 전체 기술 Fact Anchor 2,022개 중
642개가 아직 미검증이다. 따라서 전체 Anchor 검증은 아직 완료되지 않았다. 최근 검토에서는 NASA Fault Tree Handbook과 NPR, HSE 지침이 직접 지지하는 FTA Top Event 전개, Minimal Cut Set 정의, demand mode별 실패지표 선택, 저수요 PFDavg, 고수요/연속수요 PFH를 확인했다. 또한 λDU가 일정하고 전체 주기시험이 고장을 복구하며 λDU·T≪1인 1oo1 조건에서 PFDavg≈λDU·T/2임을 직접 적분해 확인했다. HSE의 별도 proof-testing guidance는 진단 coverage와 proof test의 구분, 미검출 고장의 시험 목적, partial test가 남기는 고장모드와 PFD 계산 반영을 지지한다. NASA 자료는 FTA/RBD/Markov의 서로 다른 표현 관점과 모델 경계, 전체 SIF 구성 및 HFT·구성품 SIL 주장만으로 달성 SIL이 입증되지 않는다는 경계를 뒷받침한다. 저수요 RRF는 HSE 가이드의 `PFDavg⁻¹` 정의로 확인했다. β-factor는 NASA PRA 지침에 따라 total rate의 common-cause fraction을 추정하는 단순 모델로 한정했다. HSE는 정량 모델의 구조, 진단·시험·수리 조건 기록과 systematic/common-mode 보호 및 안전수명주기 증거를 요구한다. 최신 추가 검토에서는 NASA SWE-189/190을 근거로 미실행 구조의 분석·처분과 정적분석/실행 커버리지 증거의 차이를 확인했다. HSE와 ISA 자료는 voting architecture가 위험고장 방지와 spurious trip 특성 간 trade-off를 만들 수 있음을 지지한다. 이는 구성별 분석이지 보편적 순위가 아니다. NASA 지침 범위에 한정하며 산업 전반의 일률 요구로 확대하지 않는다. 근거: [NASA NPR 8621.1 FTA](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8621_0001_&page_name=AppdxI35), [NASA Fault Tree Handbook](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Fault%20Tree%20Handbook_NASA.pdf), [NASA System Engineering Tools and Techniques](https://extapps.ksc.nasa.gov/Reliability/Documents/SystemEngineeringTools_and_Techniques.pdf), [NASA Reliability Modeling Method](https://ntrs.nasa.gov/api/citations/19980174903/downloads/19980174903.pdf), [NASA PRA Guide](https://ntrs.nasa.gov/api/citations/20120001369/downloads/20120001369.pdf?attachment=true), [HSE Functional Safety Inspection Guide](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf), [HSE Control Systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [HSE Proof Testing Appendix 1](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf), [HSE Partial Proof Testing Appendix 3](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf), [NASA SWE-189](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695524/SWE-189%2B-%2BCode%2BCoverage%2BMeasurements), [NASA SWE-190](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695525/SWE-190%2B-%2BVerify%2BCode%2BCoverage), [Fisher Sliding-Stem Packing Selection Bulletin D101986X012](https://www.emerson.com/documents/automation/product-bulletin-packing-selection-guidelines-for-fisher-sliding-stem-valves-en-11742708.pdf).

`fsrm_voting_tradeoff`는 HSE guidance와 ISA voting architecture 설명을 대조해 확인했다. 1oo2 등의 투표는 단일 센서 위험고장에 대한 보호를 개선할 수 있지만 spurious trip 가능성도 달라지고, 2oo3는 일부 사례에서 두 성능 간 절충에 사용된다. 이는 정량 SIL 보장이나 모든 구조의 보편 순위가 아니다. `score_effect=none`이다. [HSE Control Systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [ISA, Essentials of Modern Measurements and Final Elements, Chapter 1](https://www.isa.org/getmedia/eb76a613-3961-4db0-8efe-a91dc308ec68/Essentials-of-Modern-Measurements_McMillan_Chapter-1-Essentials.pdf).

MC/DC Anchor 검토에서는 NASA SWE-189의 uncovered/dead/deactivated code 처분 지침, FAA의 source/object structural coverage 문제 및 FAA AC 20-115D의 DO-330 도구 적격성 기준을 확인했다. 해당 근거들은 NASA/항공 인증 맥락에 한정되며 다른 산업의 보편 의무로 확대하지 않았다. 모두 `score_effect=none`이다. [NASA SWE-189](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695524/SWE-189%2B-%2BCode%2BCoverage%2BMeasurements), [FAA DOT/FAA/AR-02/113](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/02-113_OOT.pdf), [FAA AC 20-115D](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf), [FAA DOT/FAA/AR-06/54](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/AR-06-54_VerificationTools.pdf).

추가로 FAA AR-06/54는 source/object coverage의 대응이 compiler short-circuit 구현과 최적화 조건에 달려 있음을 설명하고, NASA TM-2015-218675는 MC/DC 계측 도구가 상당한 실행 overhead를 낼 수 있음을 보고한다. 특정 toolchain의 효과 크기를 일반화하지 않고 해당 프로젝트 환경에서 평가한다. [FAA AR-06/54, §3](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/AR-06-54_VerificationTools.pdf), [NASA TM-2015-218675](https://ntrs.nasa.gov/citations/20150011052).

인벤토리 분류도 재조정했다. `control_valve_positioner_accessory_scope`는 내부 scope 선언만이
아니라 Fisher 846·Emerson positioner·Fisher VBL의 모델별 동작을 주장하며 독립 제조사 근거가
등록되어 있으므로 기술 Fact 한 건으로 센다. 구조 전용 scope declaration은 `sw02_scope_operational_logic`
한 건이다. 이로써 Fact/구조/scope/미해결 분류의 합계가 2,073개 원본 Anchor와 일치한다.

`eem_scope_chain`은 모든 계측회로가 같은 블록과 오차항을 갖는다는 식의 포괄 문구를
제거했다. Analog Devices의 precision signal-chain 자료에 맞춰 실제 센서-아날로그단-ADC
구성의 적용 가능한 오차·잡음을 식별하고, 입력 또는 출력의 공통 기준점으로 환산해
성능 요구와 비교하는 원칙으로 범위를 제한했다. 보정·보상·신호처리는 일부 오차를 줄일
수 있으나 잔류 불확도가 남을 수 있으며, 세부 항목은 회로 구성에 따라 다르다.
`score_effect=none`이다. [ADI Practical Input-Referred Calculations](https://www.analog.com/en/resources/analog-dialogue/articles/practical-input-referred-calculations-in-precision-systems.html),
[ADI AN-1464](https://www.analog.com/en/resources/app-notes/an-1464.html).

`eem_diagnosis_chain`은 오프셋·잡음의 가능한 원인을 과도하게 열거하던 표현 대신,
아날로그 DAQ의 측정 이상을 입력단 독립 확인과 장치 설정·배선·샘플링·센서·교정 점검으로
단계 분리하는 제한적 진단 절차로 수정했다. NI 자료의 구체 절차는 해당 DAQ 장치와 조건에
종속되므로 보편 순서·수치 한계로 확대하지 않았다. `score_effect=none`이다.
[NI DAQ offset/noise troubleshooting](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P9K1SAK&l=en-CA),
[NI analog measurement noise diagnosis](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html).

`eem_residual_verification`은 모든 회로에 동일한 zero/span·온도·전원·장기추세 시험을
강제하던 목록을 제거하고, 측정시스템 특성화에서 표준값과 지시값 비교, 적용 가능한
영향량·운전조건·분해능·반복성 및 불확도 고려가 필요하다는 NIST 설명에 맞췄다.
구체적인 검증 항목과 불확도 기록은 목적·기준에 따라 다르므로 보편적 시험 세트로 확대하지
않는다. `score_effect=none`이다. [NIST measuring-system characterization](https://www.nist.gov/publications/traceability-considerations-characterization-and-use-measuring-systems-0),
[NIST VIM verification definition](https://www.nist.gov/glossary-term/34441).

`eem_mitigation_hierarchy`는 일률적인 대책 순서 주장을 제거하고, 확인된 오차·잡음 기여와
회로구조에 맞춰 대책을 고르며 일부 오차를 줄인 뒤 남는 불확도를 성능 평가에 반영한다는
범위로 수정했다. Analog Devices는 센서-ADC 신호체인의 기여분을 합산하고 calibration·
compensation·signal processing이 일부 기여를 줄일 수 있으나 잔류 오차가 불확도로 남는다고
설명한다. 보편적인 대책 순서는 주장하지 않는다. `score_effect=none`이다.
[ADI Practical Input-Referred Calculations](https://www.analog.com/en/resources/analog-dialogue/articles/practical-input-referred-calculations-in-precision-systems.html).

`excessive_seat_load_damage`는 과도한 seat load가 일률적으로 deformation·galling을 일으킨다는
일반 주장을 제거했다. Fisher HP/HPA의 지정 C-seal·bore-seal trim 문서가 뒷받침하는 초기
seating force 조건과, Control Valve Handbook이 설명하는 overtravel의 seat-load 감소·shutoff
영향·trim damage 가능성으로 한정해 verified 등록했다. 다른 trim의 보편 force limit나 손상기구로
확대하지 않는다. `score_effect=none`이다. [Fisher Control Valve Handbook, §8.5.6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf),
[Fisher HP/HPA Instruction Manual D101634X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012-hp-and-hpa-control-valves-fisher.pdf).

`final_control_element_variability_path`는 범위를 좁혀 verified 등록했다. Emerson/Fisher 핸드북은
제어밸브가 유량을 조작해 공정변수를 설정값에 가깝게 유지한다고 설명하고, Choudhury·Thornhill·Shah의
논문은 deadband와 stiction 같은 밸브 비선형성이 제어루프 성능을 제한한다고 명시한다. 실제 PV 변동의
크기·발생 여부는 밸브 및 루프 조건에 달려 있으므로 보편적 증가량이나 항상 발생하는 결과로 주장하지 않는다.
[Emerson/Fisher Control Valve Handbook, Chapter 1](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valve-handbook),
[Choudhury et al., 2005](https://sites.ualberta.ca/~slshah/files/modelling_valve_stiction.pdf). `score_effect=none`이다.

`hunting_multicausal_diagnosis`는 기존의 보편적인 다원인 목록을 제거하고, Fisher 핸드북이 직접
뒷받침하는 hunting 정의, 안정한계 부근 운전 가능성, control system/positioner 불안정과 actuator
loading-pressure 진동의 연결로 범위를 줄여 verified 등록했다. controller output·pressure·travel·PV의
동시 trend 비교는 진단 권고로만 두며, 핸드북의 의무 시험절차라고 표현하지 않는다. 따라서 booster gain,
feedback noise, linkage looseness, pneumatic compressibility는 이 Anchor만으로 확정한 원인으로 취급하지 않는다.
[Fisher Control Valve Handbook, Chapter 2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf). `score_effect=none`이다.

`control_valve_positioner_accessory_scope`는 positioner·I/P·booster 기능을 제품별 근거 범위로
좁혀 verified 등록했다. Fisher 846 매뉴얼은 입력-출력 mapping, pressure feedback, direct/reverse·split
range 구성, 별도 calibration 절차 및 power-off response 차이를 설명한다. Emerson positioner 자료는
stem/shaft feedback과 actuator pressure output을, Fisher VBL 자료는 빠른 stroking 목적과 적용 조건을
설명한다. integrated package review는 이 구성별 mapping·feedback·calibration·fail behavior를 확인하는
engineering approach이며 보편 architecture나 fail action을 뜻하지 않는다. `score_effect=none`이다.

`collaborative_robot_application`은 “협동로봇”을 별도 제품유형으로 규정하던 표현을 수정했다.
ISO는 collaborative robotics를 사람과 robot system이 작업공간을 공유하는 system/application 개념으로
설명하며, OSHA는 end-effector·workpiece·payload·속도/힘 기능과 safeguards를 포함한 application별
hazard/risk assessment를 안내한다. 실제 안전 여부를 제품 표시만으로 추정하지 않는다.
[ISO collaborative robotics overview](https://committee.iso.org/news/2016/03/Ref2057.html),
[ISO 10218-2:2025](https://www.iso.org/standard/73934.html),
[OSHA Technical Manual](https://www.osha.gov/otm/section-4-safety-hazards/chapter-4). `score_effect=none`이다.

`industrial_robot_architecture`는 robot 본체, robot system, 통합 application/cell을 구분하도록
수정해 verified 등록했다. OSHA는 manipulator·controller·end-effector·sensor·power·interface를 robot
system 요소로 설명하고, 주변설비·workpiece·safeguards가 포함된 application 경계를 별도로 제시한다.
ISO 10218-2:2025도 통합 robot application/cell의 안전을 다룬다. 구성요소 및 안전기능은 개별 시스템 설계로
한정한다. `score_effect=none`이다.

`timestamp_and_synchronization`은 sample rate와 도착 지연을 보편적으로 고정하는 표현을 제거했다.
ROS message filters는 header timestamp 기준 exact/approximate matching을 제공하고, NIST TN 2258은
500 Hz IMU와 30–240 Hz optical tracking의 로봇 센서 fusion 사례를 설명한다. 분산 계측에서 common time은
latency 영향과 synchronization 문제를 분리하는 데 도움을 주므로, 허용 시간 오차는 application dynamics에
따라 정하도록 범위를 제한했다. `score_effect=none`이다.

`digital_twin_definition`은 보편 정의를 주장하던 문구를 ISO 23247 제조 분야의 정의로 한정했다.
ISO 23247은 observable manufacturing element의 fit-for-purpose digital representation과 physical/digital
간 적절한 synchronization을 설명한다. NIST는 분야별 단일 통일 정의가 없다고 밝혀, purpose·lifecycle을
모든 digital twin의 보편 필수조건처럼 쓰지 않도록 정리했다. `score_effect=none`이다.

`simulation_scenario_coverage`는 시뮬레이션 결과의 신뢰성이 intended use 및 검증된 조건·영역에
한정된다는 범위로 수정했다. 검증 지점/영역 밖 적용에는 별도 공학적 정당화가 필요하며, 그 밖의
성능을 시뮬레이션만으로 입증할 수 있다고 일반화하지 않는다. NIST는 digital twin V&V를 intended
purpose와 design goals에 연결하고, FDA의 ASME V&V 10 표준 설명은 검증 지점 외의 영역 적용에
공학적 판단이 필요함을 명시한다. 후자는 로봇 특화 근거가 아니라 모델 검증 범위 원칙으로만 사용했다.
`score_effect=none`이다. [NIST VVUQ credibility](https://www.nist.gov/publications/credibility-consideration-digital-twins-manufacturing),
[FDA recognized ASME V&V 10 scope](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=43696).

`temperature_error_reduction_measures`는 종전의 보편적 대책 목록을 근거가 확인되는 조건부 설명으로
수정했다. BIPM은 접촉 온도계의 열누설 오차가 침지 길이에 영향을 받고 thermocouple 사용·교정 조건을
가급적 일치시켜야 한다고 설명한다. NIST BSS 153은 온도 구배가 평균온도 지시 오차를 만들 수 있고
그 오차가 유속·온도에 따라 달라질 수 있으며, 혼합을 임의 적용하면 유속 측정에 영향을 줄 수 있다고
주의한다. 따라서 유속 증가·차폐·단열을 보편 처방으로 두지 않고, 측정 목적과 조건에 맞춰 침지·위치·
혼합/평균센서·교정을 선택한다. 제한된 범위에서 score-neutral verified 등록했다.
[BIPM Thermocouple Thermometry Part 1, §§5.8, 6](https://www.bipm.org/documents/20126/41773843/Thermocouple_Thermometry_Part1.pdf/d23088f8-3bab-bacc-0cae-7358eb2666b4),
[NIST NBS BSS 153, §3.2](https://nvlpubs.nist.gov/nistpubs/Legacy/BSS/nbsbuildingscience153.pdf).

`eem_drift_definition`은 전자부품의 온도·전원 의존성까지 하나의 일반적인 instrumental drift로
묶던 표현을 VIM 용어와 부품사양 용례로 분리했다. VIM 4.21은 instrumental drift를 계측기의
계량특성 변화에 따른 지시값의 시간 변화로 정의하고, 측정량 또는 인식된 영향량의 변화는 제외한다.
Analog Devices의 정밀 증폭기 자료는 온도에 따른 offset drift를 별도 조건의 전자부품 사양으로
사용한다. 따라서 분석 시 시간 drift와 영향량 민감도를 구별하되 데이터시트의 용어·조건을 보존하도록
수정해 score-neutral verified 등록했다. [JCGM VIM 4.21](https://jcgm.bipm.org/vim/en/4.21.html),
[Analog Devices, DC Error Characteristics](https://www.analog.com/en/resources/technical-articles/dc-error-characteristics-of-an-op-amp-and-the-effect-on-precision-applications.html).

`eem_aging_reliability_boundary`는 모든 aging mechanism으로 일반화하지 않고 voltage-reference의
long-term output drift 사례에 한정했다. Analog Devices AN-713은 이 drift가 시스템 정확도를 제한할
수 있으며 initial accuracy 및 tempco와 구별된다고 설명한다. NIST degradation 방법론은 측정 가능한
파라미터가 시간에 따라 critical failure value를 향해 변하는 경우 실제 catastrophic failure를 기다리지
않고 parametric degradation을 분석할 수 있다고 설명한다. NIST는 또한 교정주기를 일률 지정하지 않고
정확도 요구, 기기 안정성, 환경을 고려하도록 안내한다. 이를 반영해 적용별 정확도·안정성 평가 및 유지관리
판단으로 범위를 제한해 score-neutral verified 등록했다. [ADI AN-713](https://www.analog.com/en/resources/app-notes/an-713.html),
[NIST degradation modeling](https://www.itl.nist.gov/div898/handbook/apr/section4/apr423.htm),
[NIST calibration interval](https://www.nist.gov/calibrations/recommended-calibration-interval).

`eem_auto_zero_ratiometric`은 오차저감 기법을 보편적으로 묶지 않고 각 회로가 줄이는 오차와 적용조건을
구분하도록 수정했다. Analog Devices 자료는 auto-zero offset/drift 저감과 chopping 주파수/고조파의
switching artifact를 함께 설명한다. RTD ratiometric 예시는 입력과 ADC reference 경로가 비례할 때
excitation 변동이 상쇄되고, TI는 `Vsupply = Vref`가 아닐 때 오차가 남을 수 있음을 명시한다. Matched
resistor network는 differential amplifier CMRR이 저항비·온도추종에 좌우되는 조건에서 개선효과를 낸다.
따라서 topology 및 신호 대역 확인을 요구하는 조건부 Fact로 score-neutral verified 등록했다.
[ADI auto-zero](https://www.analog.com/en/resources/analog-dialogue/articles/demystifying-auto-zero-amplifiers-part-1.html),
[ADI RTD ratiometric](https://www.analog.com/en/resources/analog-dialogue/articles/afe-design-considerations-rtd-ratiometric.html),
[TI ratiometric acquisition](https://www.ti.com/lit/an/sboa628/sboa628.pdf),
[ADI matched-resistor CMRR](https://www.analog.com/en/resources/technical-articles/common-mode-instrumentation-amplifiers.html).

`eem_layout_local_mitigation`은 analog/digital partition 및 ground split을 무조건 처방하던 표현을
회로 토폴로지·return-current 경로·기기 권고에 따라 결정하도록 수정했다. Analog Devices의 mixed-signal
PCB 자료는 저 digital-current 시스템에서 solid ground를 권하고, 복잡한 고전류 시스템에서는 분리를
고려하도록 구분한다. AN-1142는 무조건적인 split이 return inductance와 noise를 높일 수 있다고 설명한다.
고임피던스 입력은 누설이 정확도에 유의한 조건에서 guard·청결·절연 조치를 검토하도록 한정했다.
이를 score-neutral verified 등록했다. [ADI mixed-signal PCB guidance](https://www.analog.com/en/resources/analog-dialogue/articles/2022/09/02/02/40/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html),
[ADI AN-1142](https://www.analog.com/en/resources/app-notes/an-1142.html),
[ADI precision op-amp layout](https://www.analog.com/en/resources/technical-articles/layout-for-precision-op-amps.html).

`thermal_distortion_hot_leakage`는 기존의 일반적인 cold-test/hot-service 문구를 유지하지 않고,
Fisher EH/EHA 자료가 직접 설명하는 온도 cycling에 따른 seat-ring distortion·leakage 위험 저감
설계와 hung cage의 gasket-load 경계로 축소해 verified 등록했다. 일반 밸브 전반의 hot-service
누설 법칙을 주장하지 않는다. [Fisher EH/EHA Product Bulletin 51.2:EH, p. 6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d100042x012.pdf).

같은 날 `excessive_seat_load_damage`도 재검토했으나 미검증으로 유지했다. Fisher Sourcebook은
seat life 보존을 위해 recommended seat load보다 높은 값을 사용할 수 있다고 설명하고, 특정
HPA 매뉴얼은 해당 제품의 initial seating에 actuator sizing full-load를 쓰도록 한다. 두 자료는
필요 하중을 정하는 근거이지, Anchor가 열거한 deformation·indentation·galling·wear 전체를
증명하지 않는다. 재료·trim별 최대 하중 초과와 손상 메커니즘의 직접 근거를 확보하기 전까지
승격하지 않는다. 상세 판정: [Seat load 근거 재검토](topic_anchor_evidence_followup_20261012_seat_load.md).

`as_found_as_left_leakage`는 보편적인 기록 의무 주장을 제거하고 Emerson Lifecycle Services의
공개 repair report 한 건에 한정했다. 이 보고서는 정비 전·후 진단 상태와 정비 후 seat-leakage
class·test pressure·allowable/actual leakage를 기록한다. NIST 교정 절차는 조정 전후 결과를 별도로
보고하고 혼합하지 않는 사례를 제공하지만 밸브 전용 요구사항은 아니다. 따라서 기술 사실은 해당
보고서의 사례로만 `verified` 등록했으며, 모든 밸브 정비기록의 의무나 전후 시험조건이 동일하다는
주장은 포함하지 않았다. 시험조건이 서로 다르면 직접 비교만으로 정비 효과를 단정할 수 없다는 부분은
시험 basis 확인 원칙으로 제한했다. [Emerson repair report](https://documentation.emersonprocess.com/intradoc-cgi/ASCMExt02/weblayout/groups/nocrawl/documents/orderfiledocs/cdey/odkw/~edisp/rep12890169.pdf),
[NIST IR 7383-2019 §3.7, §4.1](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.7383-2019.pdf),
[Emerson/Fisher Control Valve Handbook §5.2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf).

`standard_edition_exact_citation`과 `vendor_purchase_spec_alignment`은 ANSI/FCI 70-2 seat-leakage
test basis와 IEC 60534-4 inspection/routine test scope, 별도 ISO 15848 external fugitive-emission
qualification/acceptance scope를 구분해 확인했다. 적용 class와 시험조건은 governing standard edition 및
구매자-제조사 합의에 맞춰 문서 간 일치하도록 한정해 verified 등록했다. [FCI current standards](https://www.fluidcontrolsinstitute.org/fci-standards-control-valves.asp),
[IEC 60534-4:2021](https://webstore.iec.ch/en/publication/72947),
[FCI 70-2 informational sheet](https://www.fluidcontrolsinstitute.org/70_2_InformationalSheet.pdf),
[ISO 15848-1](https://www.iso.org/standard/61441.html), [ISO 15848-2](https://www.iso.org/standard/61442.html).

`topic15_topic16_standard_boundary`는 시험 정확도라는 기술 주장과 결합되지 않도록 Topic ownership만
남겨 structural boundary로 재분류했다. final-element SIS/ESD·PST/proof-test credit와 valve-package
selection/lifecycle economics의 대상 Anchor 존재를 테스트한다.

SIS/SIL SW-05의 `audit_role`, `competence_management`, `diversity_tradeoff`, `tool_qualification_basis`,
`certified_product_scope`, `safety_manual_constraints`, `proven_in_use_evidence`, `quantitative_assumptions`,
Random Hardware Integrity와 구분하는 단위시험, V-Model의 SIL 보장 한계, MISRA 오분류 방지, Library 재사용
Anchor를 합쳐 미검증이었던 12건을
근거에 맞춰 verified 등록했다. HSE는 IEC 61511 기능안전 관리 프로세스에 audit를 포함하고 FSA와 구별하며,
안전 관련 업무의 competence는 담당 책임·업무와 연계해 평가하고 기록해야 한다고 안내한다.
MISRA 원문은 코딩 지침 준수 절차와 정적 분석 도구 검토를 설명하고, 소프트웨어 모듈 시험은 별도
활동으로 다룬다. 따라서 MISRA 자체를 동적 단위시험 도구라고 분류하지 않는다는 해석을 등록했다.
다양성은 공통원인을 줄이는 수단으로만 서술하고 완전 제거를 주장하지 않도록 Anchor 문구를 좁혔다.
Tool Qualification은 도구 오류의 잠재 안전영향과 검출 수단을 고려하는 근거 원칙으로 제한했으며,
도구 분류와 요구 증거는 적용 IEC 61508 판본·사용사례에 따라 확인해야 한다. Siemens Library 통제는
서명·instruction version을 기록하고 차이가 나면 재시험하는 특정 제품 절차로 한정했다. 따라서 이
Pack에서 이번 검토 전 미해결이던 12개는 모두 근거 등록했으며, 다른 제조사에 같은 절차를 일반화하지 않는다.
HSE 검사 가이드는 장치 Safety Manual의
시험 방법을 proof-test 절차에 반영하고 설치 특유의 미검출 고장을 별도로 고려하도록 한다. 61508
Association의 proven-in-use 가이드는 software scope/version, configuration history, similar operational
profile, operating hours와 auditable fault records를 요구하는 근거로 사용했다.
[HSE functional safety](https://www.hse.gov.uk/eci/functional.htm),
[HSE Control Systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm),
[HSE proof-testing guidance](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix2.pdf),
[HSE Functional Safety Inspection Guide](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf),
[HSE competence guidance](https://www.hse.gov.uk/humanfactors/assets/docs/mancomppt1.pdf),
[MISRA Compliance:2020](https://www.misra.org.uk/app/uploads/2021/06/MISRA-Compliance-2020.pdf),
[61508 Association certificate guidance](https://61508.org/wp-content/uploads/2023/10/T6A033_-_FS_Certificates_and_Safety_Manuals_-_V1_e092022.pdf),
[61508 Association software proven-in-use guide](https://61508.org/wp-content/uploads/2023/12/CASS-GUIDE-508-SW-IEC61508-3-Software-TOES-v3.3.pdf).
[Siemens Safety Integrated Commissioning Manual §4.9](https://cache.industry.siemens.com/dl/files/294/109801294/att_1077949/v1/MC_SI_commiss_man_0721_en-US.pdf).

`measurement_calibration_detection_uncertainty`는 원래의 보편 누설측정 불확도 목록을 걷어내고,
40 CFR Part 60 Appendix A-7 Method 21의 VOC equipment-leak screening 계기 기준(response factor,
calibration precision, response time)으로 좁혀 verified 등록했다. 이는 valve stem/packing의
외부 fugitive-emission screening 범위이며 ANSI/FCI seat-leakage 시험에는 확대하지 않는다.
[Current eCFR Method 21](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-7%20to%20Part%2060).

`false_pass_false_fail_background`도 원래의 여러 오판 원인을 보편적으로 나열한 문구에서 EPA
Method 21 Type II의 ambient-background/source concentration 비교 절차와 주변 방해배출 시
최소 거리 제한으로 범위를 축소해 verified 등록했다. 이는 VOC external fugitive-emission
screening에 한정한다. [Current eCFR Method 21 §8.3.2](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-7%20to%20Part%2060).

`special_service_sealing_boundary`는 Fire-safe·고온·극저온을 공통 원리처럼 묶은 문구를 서비스별
근거 예시로 좁혔다. ISO 10497의 fire-test leakage/operability 범위, ISO 21011의 −40 °C 이하
cryogenic valve 설계·시험 범위, Fisher EH/EHA의 온도 cycling 대응 설계를 구분해 verified
등록했으며, 모든 special-service valve에 공통되는 단일 qualification rule을 주장하지 않는다.

Noise Topic의 `flashing_two_phase_noise`는 flashing 물리현상이 일반적으로 broadband noise·
vibration을 만든다는 기존 문구를 그대로 승인하지 않았다. Fisher Sourcebook은 flashing/two-phase
noise 예측 방법이 잘 확립되지 않았다고 설명하고, IEC 60534-8-4:2015는 normal turbulence와 liquid
cavitation을 예측하지만 flashing 조건·unstable flow noise를 고려하지 않는다고 명시한다. 따라서
Anchor를 “flashing noise prediction의 표준 범위 한계”로 재작성해 verified 등록했다. 근거:
[IEC 60534-8-4](https://webstore.iec.ch/en/publication/23315), [Fisher Control Valve Sourcebook](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf).

## 과거 점검 스냅샷 (2026-10-11; 이후 갱신으로 대체됨)

2026-10-11 최신 배치: 위험장소 Topic의 Ex m/t 복합 보호원리, 가스·분진 그룹 호환성 표, 온도등급과 실제 열조건 확인, Ex p, 본질안전 보호수준, entity U/I/P·C/L, barrier 구성요소, 배선 식별·분리·차폐/접지 조건을 검증에 포함했다. Ex m은 점화 가능한 부품을 encapsulation하고 Ex t는 dust ingress 보호 외함과 표면온도 제한을 결합한다. `certificate_special_conditions_control_drawing` 및 Ex e 보호수준 문구를 범위 축소 후 확인하여 이 Topic은 21개 verified, 1개 미검증이다.

남은 1개는 `protection_method_risk_matching`이다. 다요소 공학적 선택 권고의 모든 요인을 한 표준문구가 직접 입증하지 않으므로 미승격이다. 근거: [IEC 60079-14:2024](https://webstore.iec.ch/en/publication/66049), [IECEx 2024 installation selection guidance](https://www.iecex.com/dmsdocument/4423/).

당시 인벤토리는 86개 Topic Pack, 2,073개 Anchor였다. 이 가운데 독립 근거로 확인된 기술 Fact는
1,240개 고유 Topic–Anchor 매핑이며, 46개는 기술 Fact가 아닌 내부 소유경계·범위계약으로
분리 기록했다. 따라서 아직 확인되지 않은 기술 Fact는 787개다. WordPress 출처가 없다는
이유만으로 미검증 처리하지 않으며, 공식 표준·정부 문서·교재·제조사 자료 등 해당 주장에
적합한 근거로 판단한다. 출처만 있다는 이유로 claim 전체를 승인하지 않고, 근거가 문장 범위를
직접 지지하는지 확인한다. 이 수치는 전체 내용 검토 완료를 뜻하지 않는다.

2026-10-11 추가 재검토에서도 `temperature_error_reduction_measures`는 미검증으로 유지했다.
ASHRAE Handbook과 ISA의 온도계측 자료는 복사오차 저감, 적정 침지, 대표 측정 위치 및 단열의
조건부 적용을 뒷받침한다. 반면 모든 열거 대책을 모든 센서·공정에 보편 적용하라는 주장은
뒷받침하지 않는다. 특히 고유속은 bare element의 진동·피로 검토를 요구할 수 있어 무조건적인
오차 저감책으로 쓸 수 없다. 근거: [ASHRAE Handbook—Fundamentals, Ch. 38](https://handbook.ashrae.org/Handbooks/F25/IP/f25_ch38/f25_ch38_ip.aspx),
[ISA, Advanced Temperature Measurement and Control, Ch. 1](https://www.isa.org/getmedia/6ce25f6c-8fa6-4eae-a6cd-c7ee5b2a4c8a/Advanced-Temperature-Measurement-and-Control-Second-Edition-Chapter-1-Temp-Meas.pdf),
[NIST SP 250-35](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication250-35.pdf).

같은 날 위험장소 Topic의 미승격 Anchor를 다시 대조했다. 원래의
`certificate_special_conditions_control_drawing` 문구는 X 조건·제조사 control drawing의 역할과
cable gland 예시를 한데 묶어 오해 소지가 있어 그대로 승인하지 않았다. IECEx는 X suffix를
설치·사용·정비에 필요한 인증서 조건의 식별자로
설명하지만, cable-gland 선정은 IEC 60079-14의 설치 요건으로 분리하고 인증서에서 다루지 않도록
명시한다. 반면 IECEx OD 017은 control drawing이 연결정보 및 특별 설치·사용조건을 정리하는 권고
형식이며 본질안전 파라미터·환경 조건을 문서에 포함할 수 있음을 직접 설명한다. 따라서 현재
복합 Anchor는 보류하고, 향후 수정 시 “X 조건은 해당 인증서의 특수사용조건을 확인하고, control
drawing/system document의 회로·설치 제한과 IEC 60079-14 요건을 각각 반영한다”처럼 역할을
분리해야 한다. 이후 Anchor를 이 한정 문구로 수정하고 근거를 등록했다. 근거:
[IECEx OD 011-2](https://www.iecex.com/assets/dmsdocuments/1594/IECEx-OD-011-2Ed5.9-RLV.pdf),
[IECEx OD 017](https://www.iecex.com/dmsdocument/2524/),
[IEC 60079-14:2024](https://webstore.iec.ch/en/publication/66049).

원래 `increased_safety_ex_e_principle`은 IEC 60079-7의 보호수준별 요구를 구분하지 않고 “정상 및
규정된 이상조건”이라고 일반화했다. 이를 추가 설계·구조 조치라는 원리와 eb/ec 보호수준 및 fault
assumption의 구분으로 수정했고, IEC의 보호수준 정의와 NSW Government TestSafe의 level별 설명에
대조해 verified 등록했다. `protection_method_risk_matching`은
EPL과 장비·설치 적합성을 함께 검토해야 한다는 방향은 IEC 60079-14의 범위와 일치하지만,
현재의 전력수준·유지보수성 등 열거 전체를 단일 표준 문구가 직접 뒷받침하지 않아 복합 권고로
보류했다. `certificate_special_conditions_control_drawing`은 잘못 일반화된 예시를 걷어내고 IECEx
OD 011-2와 OD 017이 직접 지지하는 조건으로 재작성해 독립 Fact로 등록했다. 이 업데이트로 확인된
고유 Topic–Anchor는 1,240개이며, 전체 기술 Fact 미검증 수는 787개다. 근거:
[IEC 60079-14:2024](https://webstore.iec.ch/en/publication/66049),
[IECEx OD 504](https://www.iecex.com/assets/dmsdocuments/1556/IECEx-OD-504Ed4.0-RLV.pdf).

등록부는 1,242개 기록을 포함한다. 이 중 1,241개는 Anchor에 연결되어 있고, 1개는 개별 사실로는
검증됐으나 복합 Anchor 전체를 뒷받침하지 않아 독립 기록으로 남겼다. Anchor에 연결된 항목 중
같은 Topic–Anchor를 가리키는 중복 1건이 있다. 전체 기술 Fact 수는 등록 행이 아니라 고유 매핑 수로 계산한다.

2026-10-12 `vendor_hand_calculation_crosscheck`를 액체 sizing 계산 basis의 재현 가능한 교차 검산으로 좁혔다. 독립 검산에는 같은 flow/pressure 단위, 실제 valve ΔP, 같은 service case와 적용 equation을 사용하며, piping/Reynolds 보정은 해당 조건에서만 반영한다. 결과 차이는 입력·가정·식의 재검토 사유이지 vendor 오류의 단독 증거가 아니다. 근거: [Masoneilan Control Valve Sizing Handbook](https://dam.bakerhughes.com/m/47616eb160214a1d/original/Masoneilan-Valve-Sizing-Rules-Tech-Spec-English.pdf), [Emerson/Fisher Control Valve Handbook, Chapter 5](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf). `score_effect=none`.

2026-10-11 `control_valve_sizing_cv_kv_reynolds_liquid_selection`에서 Cv의 용량계수 의미,
Cv–Kv 환산, sizing 식의 단위 일관성, 일정 유량·밸브 차압에서 비중 증가 시 요구 계수 증가를
제조사 sizing 자료와 식의 직접 대수 변형으로 확인했다. Kv 기준 정의 anchor는 기준온도 표현을
포함해 현재 문구에 정확히 맞는 독립 근거를 찾지 못해 미검증으로 유지했다. 따라서 Kv 정의는
검증 건수에 포함하지 않았다. 근거: [Fisher Control Valve Sourcebook, Ch. 3–4](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf).
`score_effect=none`이다.

2026-10-12 `protection_method_risk_matching`은 IECEx OD 504의 역량평가 기준으로 범위를 좁혔다. 해당 문서는 위험장소 분류에 따른 장비·배선 선정과 인증 적합성 확인, 환경/유지보수 고려, hazard risk·기능·경제성을 포함한 설계 선택지 정당화를 역량 증거로 열거한다. 이를 특정 보호방식의 보편 우선순위나 단일 선정 알고리즘으로 일반화하지 않는다. 근거: [IECEx OD 504 Ed. 4.0, §§5.42–5.44](https://www.iecex.com/assets/dmsdocuments/1556/IECEx-OD-504Ed4.0-RLV.pdf). `score_effect=none`.

같은 날 `operating_case_noise_matrix`를 IEC 60534-8-3 계열의 aerodynamic noise prediction 범위로 재작성했다. Fisher 자료는 예측이 밸브 geometry 및 적용 service conditions에 기반한다고 설명한다. 따라서 project에 정의된 상이한 credible cases는 case별 입력으로 평가하되, 모든 설비에 동일한 startup/shutdown 포함 행렬을 강제하지 않는다. 근거: [Fisher Control Valve Sourcebook—Oil and Gas, Chapter 6](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [Emerson/Fisher Control Valve Handbook](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf). `score_effect=none`.

같은 날 `positioner_closed_loop_position_feedback`는 Emerson/Fisher 설명으로 확인했다. 공통 포지셔너 기능은 stem/shaft position feedback을 사용하고 actuator 압력을 조절해 제어 setpoint에 대응하는 위치를 만든다. Fisher 3710/3720 manual은 input force와 feedback spring을 균형시키고 spool output으로 actuator를 공급·배기하는 구체 동작을 설명한다. 이 검증은 완전 추종이나 deadband 부재를 의미하지 않는다. 근거: [Emerson Valve Positioners](https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners), [Fisher 3710/3720 manual, pp. 30–31](https://www.documentation.emersonprocess.com/intradoc-cgi/groups/public/documents/instruction_manuals/d101728x012.pdf). `score_effect=none`.

`stiction_limit_cycle_path`는 deadband와 stiction을 같은 현상으로 취급하던 기존 문구를 수정했다. Choudhury, Shah, Thornhill의 연구는 static friction을 넘을 때의 valve jump와 모델 조건에서 stiction에 의한 limit cycle을 다루며, PI loop의 pure deadband/backlash는 plant integrator가 없는 조건에서 limit cycle을 만들지 않는다고 명시한다. 따라서 현 앵커는 stiction에 의한 진동을 조건부로 표현하고 deadband의 보편 효과를 주장하지 않는다. 근거: [“Modelling valve stiction,” Control Engineering Practice 13 (2005), DOI 10.1016/j.conengprac.2004.05.005](https://doi.org/10.1016/j.conengprac.2004.05.005). `score_effect=none`.

같은 팩의 `response_time_dead_dynamic_separation`은 Emerson/Fisher Control Valve Handbook §2.1.3.1–2에서 직접 확인했다. Step response의 초기 dead time은 입력 변화부터 가시적 밸브 반응 시작까지이며, dynamic time은 움직임이 시작된 뒤 위치응답이 진행되는 구간으로 설명된다. 실제 수치는 step 크기·방향과 response threshold에 의존하므로 보편 상수로 취급하지 않는다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf). `score_effect=none`.

`small_step_test_control_resolution`은 IEC 60534-9의 step-response 시험 범위와 Emerson/Fisher의 deadband·resolution 및 100% stroking-time 설명에 대조했다. 실제 제어에 가까운 작은 입력 step의 응답을 측정해야 작은 신호 성능을 판단할 수 있으며, full-stroke time은 이를 대신하지 않는다. 근거: [IEC 60534-9:2007](https://webstore.iec.ch/en/publication/2477), [Emerson/Fisher Control Valve Handbook, Chapter 2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf). `score_effect=none`.

`large_step_test_pneumatic_capacity`는 full-stroke 시험의 실제 측정량으로 범위를 좁혔다. 100% step 시험은 지정 방향에 대한 전체 travel 완료 시간을 측정하며, 시간만으로 공압 제한 원인을 단정할 수 없다. 공급압력·actuator pressure와 travel을 추가로 보아야 하며 작은 신호 성능은 별도 시험으로 판단한다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [IEC 60534-9:2007](https://webstore.iec.ch/en/publication/2477). `score_effect=none`.

`positioner_gain_speed_stability_tradeoff`는 일반 gain 법칙으로 검증하지 않고 Fisher FIELDVUE DVC6200 SIS의 tuning guidance로 한정했다. 해당 manual은 tuning set C/M을 각각 slowest/fastest response로 설명하고, unstable이면 decrease response, sluggish이면 increase response를 안내한다. 사전 설정은 초기값이며 실제 assembly에서 확인하도록 되어 있다. 원 Anchor의 공압 소비 증가 주장은 해당 자료가 직접 지지하지 않아 제거했다. 근거: [Fisher FIELDVUE DVC6200 SIS manual, §§Tuning/Stable-Optimize](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc6200-sis-digital-valve-controller-en.pdf). `score_effect=none`.

`volume_booster_flow_capacity_feedback_condition`은 최신 Fisher VBL manual에 맞게 제품 범위로 좁혔다. 큰 입력 변화는 supply/exhaust port를 열어 빠른 stroke를 만들고, integral bypass는 작은 positioner 신호를 통과시킨다. bypass 조정은 안정성에 필요하며, 설명된 구성은 positioner saturation 위험을 다룬다. 이를 모든 volume booster의 동일 구조로 일반화하지 않는다. 근거: [Fisher VBL Volume Booster Manual D103317X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103317x012.pdf), §§1.2, 3–4. `score_effect=none`.

`pneumatic_supply_tubing_spool_capacity`는 일반 배관 길이·내경과 응답시간의 정량 관계로 검증하지 않았다. 대신 Fisher FIELDVUE DVC6200 SIS manual의 제품별 사실로 좁혔다. Low Bleed Relay에는 3/8 in tubing을 권장하고 High Cv relay에는 port connection size 이상을 권장하며, 공급압력과 출력용량도 relay 구성별로 기재되어 있다. 이 사양을 다른 positioner에 일반화하거나 universal tubing-delay 법칙으로 사용하지 않는다. 근거: [Fisher FIELDVUE DVC6200 SIS manual D103557X012, Table 1, pp. 5–6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc6200-sis-digital-valve-controller-en.pdf). `score_effect=none`.

`oscillation_requires_differential_diagnosis`의 기존 광범위 원인 목록은 직접 근거가 부족해 축소했다. Fisher Control Valve Handbook은 hunting을 외부 자극이 사라진 뒤에도 지속되는 유의한 진동으로 정의하며 안정한계 부근의 운전일 수 있다고 설명한다. 밸브에서는 control system 또는 positioner 불안정이 actuator loading pressure 진동으로 나타날 수 있다는 범위만 verified했다. 이는 모든 설비의 원인을 판별하거나 현장 원인 목록을 완성한 것이 아니다. 근거: [Emerson/Fisher Control Valve Handbook, Ch. 1 hunting terminology; Ch. 2 §2.1.3.3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf). `score_effect=none`.

`positioner_cannot_replace_actuator_thrust`는 Fisher 685SR sizing 사례로 범위를 고정했다. 제조사 예제는 서비스별 하중·unbalance·seat load·packing friction으로 required valve thrust를 산정해 available actuator thrust와 비교하며, size 10의 가용 thrust가 부족한 경우 size 12로 재선정해 계산을 반복한다. 따라서 positioner pressure output과 actuator thrust sizing은 별도이며, 예제 수치는 보편 설계값으로 적용하지 않는다. 근거: [Fisher Catalog 14, 685SR sizing example, pp. B-80.3–B-80.4](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf), [DVC6200 SIS manual, Table 1](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc6200-sis-digital-valve-controller-en.pdf). `score_effect=none`.

`opening_closing_response_asymmetry`는 원래 제시된 spring force·공압 면적·유체력 등 원인 전체를 검증하지 않고, Fisher Handbook Figure 2.4의 Valve A 사례로 범위를 제한했다. 동일 크기 2% step에 대해 opening과 closing의 Td/T63가 각각 0.25/0.34 s와 0.50/0.74 s로 기록되어 있어 방향별 응답 측정이 필요함을 확인했다. 해당 수치는 특정 assembly의 시험 예이며 보편값이 아니다. 근거: [Emerson/Fisher Control Valve Handbook, Ch. 2, Figure 2.4](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf). `score_effect=none`.

`reversal_test_deadband_hysteresis`는 IEC 60534-4:2021의 dead-band test로 한정했다. 약 25%, 50%, 75% rated travel에서 입력을 반전시키고 stem/shaft 움직임을 반전시키는 데 필요한 operating-signal 변화를 측정한다. 표준의 정의에서 dead band와 hysteresis는 서로 다른 특성이며, factory test 결과가 실제 process-loaded 성능을 보증하는 것은 아니다. 근거: [IEC 60534-4:2021, §§3.2–3.5, 4.6, 5.8](https://webstore.iec.ch/en/publication/72947). `score_effect=none`.

`step_sensitivity_not_resolution_only`는 IEC 60534-9의 용어와 측정기 조건으로 좁혔다. 같은 방향 입력 step에 대해 출력 움직임이 나타나는 최소 increment를 valve resolution으로 정의하고, 측정기 resolution은 valve resolution의 1/3 이하(권장 1/10 이하)로 따로 제한한다. “step sensitivity”를 이와 무관한 별도 표준 용어나 보편 수치로 주장하지 않는다. 근거: [IEC 60534-9:2007, §§3.11, 5.3, 8.2](https://webstore.iec.ch/en/publication/2477). `score_effect=none`.

`positioner_cannot_remove_mechanical_backlash`는 모든 positioner의 보편 능력 주장으로 검증하지 않았다. Fisher 3660 매뉴얼은 feedback lever/range spring을 통해 stem movement가 positioner beam에 돌아와 relay output pressure를 조절한다고 설명한다. 별도로 Fisher 1052 자료는 clamped lever와 single-pivot linkage가 actuator–valve lost motion을 줄인다고 명시한다. 두 기능을 구분했으며, positioner 조정으로 모든 기계적 clearance가 제거된다는 증거로 확대하지 않는다. 근거: [Fisher 3660/3661 manual, p. 28](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101402x012.pdf), [Fisher 1052 actuator supplement, p. 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103790x012.pdf). `score_effect=none`.

`improvement_verify_same_test_and_process_result`는 IEC 60534-9의 시험·보고 범위와 공정 KPI를 나눠 기록했다. 표준은 baseline, small-step, response-time 시험, valve assembly configuration 및 결과에 영향을 주는 조건의 기록을 규정하고 in-process test에서 process variable을 측정한다. 동일 조건 비교는 합리적인 before/after engineering practice로 표현하되, PV variability·품질·에너지·air consumption은 프로젝트별 KPI 선택사항이며 표준 공통 의무 목록으로 단정하지 않는다. 근거: [IEC 60534-9:2007, §§5.1–5.2, 7.1–7.3, 8.1–8.3](https://webstore.iec.ch/en/publication/2477). `score_effect=none`.

2026-10-11 추가 검증: `small_flow_trim_special_review`는 IEC 60534-2-1 Annex A.7의
정격계수비 `C_rated/(d²N18)=0.016` 기준으로 full-size/reduced trim을 구분하고, A.8a/A.8b의
trim별 `n` 식을 각각 적용한다는 내용으로 좁혔다. 이 `n`은 A.6/A.7의 Reynolds factor `FR`
계산에 사용되므로 reduced trim에 full-size trim의 `n` 관계식을 대입하지 않는다는 범위에서
verified 등록했다. 저유량의 보편 임계값이나 모든 밸브의 설계 권고를 주장하지 않는다.
`score_effect=none`이다. 근거: [IEC 60534-2-1:2011, Annex A.7](https://webstore.iec.ch/en/publication/2461).

같은 날짜에 `bellows_backup_packing_boundary`는 보편적인 bellows 설계 보증으로 다루지 않고,
Fisher ENVIRO-SEAL 제품 bulletin이 직접 설명하는 범위로 축소했다. 해당 자료는 stem seal을 통한
대기 방출 억제 목적, bellows 위쪽 packing 구성, pressure-temperature rating 및 pressure·temperature·travel에
따른 cycle-life 영향을 제시한다. 이 제품별 경계 안에서 verified했으며 다른 bellows 설계나 무누설
보증으로 일반화하지 않는다. `score_effect=none`이다. 근거:
[Fisher ENVIRO-SEAL Bellows Seal Product Bulletin 59.1:070, pp. 1–3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101641x012.pdf).

같은 CV leakage Topic에서 `gas_liquid_test_medium_difference`를 ANSI/FCI 70-2의 class별 시험
기준으로 한정했다. Fisher Catalog 12의 표에서 Class V는 물, Class VI는 공기를 시험 매체로
제시하고 Class VI 결과는 port size별 bubble 또는 volumetric basis로 표시한다. 따라서 서로 다른
매체·시험법·단위의 수치를 조건 확인 없이 같은 leakage 결과로 간주하지 않는다는 범위에서 verified했다.
`score_effect=none`이다. 근거: [Fisher Catalog 12, Section 2, p. 2-1](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf),
[ANSI/FCI 70-2:2021 catalog record](https://www.intertekinform.com/en-us/standards/ansi-fci-70-2-2021-509586_saig_fci_fci_2918128/).

또한 `live_loaded_packing_function`은 Fisher ENVIRO-SEAL 제품자료의 범위로 한정했다. 해당 자료는
live-loading이 packing material 수명 동안 지속 하중을 제공하고 packing-box 조정 필요를 줄이며,
많은 적용에서 없앨 수 있다고 설명한다. 이는 제품 설명이지 모든 live-loaded packing을 무정비로
보증하는 것은 아니므로 그 일반화는 명시적으로 배제했다. `score_effect=none`이다. 근거:
[Fisher enhanced ENVIRO-SEAL Packing Systems, Improved Service Life](https://www.emerson.com/en/final-control/products/fisher-enviro-seal).

`seat_damage_erosion_wire_drawing`은 일반적인 wear·scoring·galling 전체를 묶은 문구 대신,
Emerson/Fisher가 공개한 boiler-feedwater 적용 사례에 범위를 제한했다. 문서는 entrained particle로
인한 plug-tip erosion이 plug-seat 접촉을 방해하고 shutoff를 낮추며 추가 trim erosion을 일으킨
과정을 설명한다. 이 단일 사례 범위에서 verified했으며 모든 밸브·손상원인으로 외삽하지 않았다.
`score_effect=none`이다. 근거: [Fisher Protected Inside Seat boiler-feedwater case history, pp. 1–2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351913x012.pdf).

Garlock Low Emission Compression Packing Product Owner Manual을 확인해 `misalignment_stem_guide_wear`,
`surface_finish_lapping_hardness_coating`, `gland_geometry_compression`, `packing_consolidation_relaxation`을
각각 stem-packing 접촉·설치 절차에 한정해 verified했다. Manual은 runout/deflection의 편하중·마모,
stem 표면 scratch·pitting·roughness의 누설·마모 영향, stuffing-box 치수와 packing load 및 follower
centering 관리, 그리고 cycling/consolidation 후 torque loss가 있을 때 재확인하는 절차를 설명한다.
Seat lapping, coating, 모든 packing의 열주기 거동이나 보편적인 adjustment interval은 입증하지 않아
주장에서 제외했다. `score_effect=none`. 근거: [Garlock Low Emission Compression Packing Product Owner Manual, pp. 10–15](https://legacy.garlock.com/sites/default/files/documents/en/Garlock_CMP%204-79_LEProductOwnerManual_05.2017_LR_EN-NA.pdf).

같은 CV/Kv sizing Topic에서 직접 부착 fitting에 대한 Fp 보정 범위, Fp 식에서 Fp<1일 때의
capacity 저하와 geometry 의존성을 확인했다. IEC 60534-2-1 공식 범위 설명은 비뉴턴 유체·혼합물·slurry·액고 혼합 이송에 대해 해당 비압축성 식을 무조건 적용하지 않도록 명시한다. 이 근거를 바탕으로 복합 유체 anchor도 범위를 한정해 verified했다. 근거: [Fisher Control Valve Sourcebook, Ch. 3, pp. 3-2–3-5](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [IEC 60534-2-1:2011 official scope](https://webstore.iec.ch/en/publication/2461). `score_effect=none`이다.

동일 Topic의 비난류 유동 조건, FR의 입력 의존성, 요구 Cv 보정 방향 및 선택된 valve style의 FL 값이 달라질 때 sizing 절차를 반복하는 조건은 Fisher Catalog 12의 계산 단계·표로 대조했다. FR 값은 selecting-size, flow-prediction, pressure-drop 용도가 서로 다르므로 하나의 curve를 모든 계산에 혼용하지 않는다는 조건도 기록했다. 근거: [Fisher Catalog 12, Section 2, pp. 2-2, 2-6–2-8](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf). `score_effect=none`이다.

2026-10-11 추가 검증: `valve_reynolds_number_meaning`은 기존의 관성력·점성력 설명을 넓게 유지하지 않고, Fisher Catalog 12가 직접 제시하는 제어밸브용 `Rev` sizing 식의 목적과 입력으로 좁혔다. 식에는 `Cv`, 밸브 style modifier `Fd`, `FL`, 유량, 운동점도 및 배관 직경이 들어가며, 이후 `Rev`로 sizing 목적별 Reynolds factor `FR`을 구한다. 따라서 해당 제어밸브 sizing 식을 사용하고 일반 배관 Reynolds 식을 임의 대입하지 않는다는 점을 verified했다. `score_effect=none`이다. 근거: [Fisher Catalog 12, Section 2, pp. 2-6–2-7](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf), [IEC 60534-2-1:2011](https://webstore.iec.ch/en/publication/2461).

또한 required coefficient와 rated capacity의 구분, min/normal/max 각 운전점에서의 별도 요구계수·travel 산정, trim characteristic으로 travel을 대응하는 절차를 Fisher DVC7K 매뉴얼의 입력 정의와 대조했다. body size와 trim capacity는 Fisher 제품 문서의 reduced-capacity trim 사례로 확인했다. 과대선정은 특정 travel band를 일반화하지 않고, manufacturer 자료가 설명하는 저유량 rangeability 및 stiction/hysteresis 위험으로 범위를 제한해 기록했다. 근거: [Fisher DVC7K-H Instruction Manual, p. 27](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc7k-h-digital-valve-controller-en.pdf), [Emerson Globe Control Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/globe-control-valves), [Emerson Properly Size Control Valves](https://www.emerson.com/content/dam/emerson/es/final-control/flow-controls/products/valves/properly-size-control-valves.pdf). `score_effect=none`이다.

Kv의 1 bar·m³/h 물 기준은 IEC 60534-1:2023의 정의와 제조사별 온도 표기를 교차 대조해 anchor의 온도 caveat까지 확인했다. 입력변수, valve-style-dependent Reynolds factor, corrected coefficient와 catalog capacity의 비교, 그리고 액체 cavitation/flashing/choked screening은 Emerson sizing procedure 및 product manual의 범위에서 확인했다. 근거: [IEC 60534-1:2023](https://webstore.iec.ch/en/publication/32585), [SAMSON DB 20a-kd EN, p. 3](https://www.samsongroup.com/document/DB20a-kd_EN.pdf), [Emerson Control Valve Sizing](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valves-sizing), [Fisher Catalog 12, Section 2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf). 부족한 rated capacity가 specified maximum duty를 만족시키지 못한다는 조건부 판단도 sizing 절차와 capacity comparison에 한정했다. `score_effect=none`이다.

정상 travel에 대해 보편 opening band를 고정하지 않는다는 앵커는 밸브 형식·characteristic·system 조건에 따른 gain 차이, 각 유량점별 travel 산정, positioner/actuator가 assembly resolution에 주는 영향을 대조해 verified했다. 근거: [Fisher Control Valve Handbook, Chapters 2 and 5](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher DVC7K-H Instruction Manual, p. 27](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc7k-h-digital-valve-controller-en.pdf). `score_effect=none`이다.

`hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`에서는 가스·분진 구역의 빈도/지속시간 구분, zone–EPL 표, 그리고 Ex 기기 선택 시 zone 외 물질그룹·온도·주위환경·인증서 specific conditions 확인을 IEC/IECEx 및 OSHA 자료와 대조했다. OSHA Zone 정의는 미국 규정 예시로만 사용하고, 국제 적용은 IEC 기준과 IECEx guidance 범위로 한정했다. 근거: [IEC 60079-10-1](https://webstore.iec.ch/en/publication/23265), [IEC 60079-10-2:2026](https://webstore.iec.ch/en/publication/90124), [IECEx selection/EPL guidance](https://www.iecex.com/dmsdocument/4336/), [IECEx 2024 selection information](https://www.iecex.com/dmsdocument/4423/), [IECEx specific conditions guidance](https://www.iecex.com/dmsdocument/4196/), [OSHA 29 CFR 1910.399](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.399). `score_effect=none`이다.

2026-10-11 `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`의
`internal_external_leakage_boundary`는 SAMSON T 8000-6의 leakage-path 도식/설명과 Emerson
Control Valve Handbook의 stem·rotary-shaft packing 설명으로 확인했다. 내부 경로는 plug-seat 및
seat-body 접점, 외부 경로는 plug stem/shaft seal 또는 body gasket·flanged joint에서 대기로
이어지는 경로로 구분한다. 이는 경로 분류이며 누설 허용량이나 모든 valve 설계의 전수 목록을
정의하지 않는다. `score_effect=none`이다. 근거: [SAMSON T 8000-6 EN, p. 2](https://australia.samsongroup.com/document/t80006en.pdf),
[Emerson Control Valve Handbook, §8.5.3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf).

같은 Topic의 `concentration_mass_emission_boundary`는 U.S. EPA Method 21과 equipment-leak
emission protocol에 대조했다. Method 21의 local concentration reading은 component sampling
location에서의 농도 신호이며, EPA의 high-flow 방식은 captured flow와 hydrocarbon concentration을
결합해 mass emission rate를 산정한다. 따라서 농도와 질량배출률은 같은 물리량이 아니다. 모든
배출량 산정법이 직접 유량을 측정한다고 일반화하지 않았다. `score_effect=none`이다. 근거:
[U.S. EPA Method 21, §§3.5, 8.3](https://www.epa.gov/sites/default/files/2017-08/documents/method_21.pdf),
[U.S. EPA Protocol for Equipment Leak Emission Estimates, §3.2, p. 22](https://www.epa.gov/sites/production/files/2016-08/documents/8_equipmentleaks.pdf).

`packing_leakage_friction_tradeoff`는 SAMSON T 8000-6의 패킹 설치·작동 설명, Emerson 657
액추에이터의 deadband 정의, Emerson A11 회전밸브의 packing adjustment 주의사항으로 확인했다.
적절한 압축력은 잠재 누설경로를 막을 수 있지만, 과소·과도 조임 모두 누설 문제를 만들 수 있다.
과도 조임은 마찰·마모·불규칙 stem 동작 및 요구 액추에이터 힘을 증가시킬 수 있고, packing
마찰은 deadband의 여러 원인 중 하나다. 따라서 압축 증가에 따라 누설이 단조 감소한다고
해석하지 않으며 live-loaded 등 다른 구조는 제조사 절차를 따른다. `score_effect=none`이다.
근거: [SAMSON T 8000-6 EN, pp. 2–3](https://www.samsongroup.com/document/t80006en.pdf),
[Emerson 657 Actuator Manual, p. 10](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d100306x012-instruction-manual-657-diaphragm-actuator-sizes-30-30i-through-70-70i-and-87-fisher.pdf),
[Emerson A11 Valve Manual, p. 9](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d104223x012.pdf).

`packing_adjustment_replacement_inspection`은 Emerson/Fisher의 sliding-stem D/DA manual과
rotary 8540 manual을 대조했다. 두 설계 모두 누설을 멈추는 데 필요한 제조사 한도 내 gland
조정, 조정 실패 시 packing 교체, stem/shaft 및 packing-box 표면 손상 확인을 지시하며,
과도한 조임은 마찰 증가 또는 packing-box 부품 손상을 일으킬 수 있다고 경고한다. 적용 설계별
load/torque와 안전한 격리·감압 절차는 각 모델 매뉴얼을 따른다. `score_effect=none`이다.
근거: [Emerson D/DA Valve Manual D100386X012, p. 6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d100386x012.pdf),
[Emerson 8540 Valve Manual D104709X012, pp. 9–10](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d104709x012.pdf).

`low_emission_qualification_field_boundary`는 ISO 15848-1:2015 type-test 범위와 시험절차를
검토했다. 이 표준은 지정 조건에서 valve stem/shaft seal 및 body joint의 external leakage를
평가·분류하는 type qualification이며, test-rig 설치, 압력, 온도 안정화, mechanical cycle과
leakage measurement를 규정한다. 그러므로 특정 type-test 성능은 현장 설치·stem/shaft 상태와
유지관리 성능을 자동 보증하지 않는다. ISO 공식 목록에서 2015판과 2017 Amendment 1이 확인되며,
수치·등급은 적용판 및 인증서를 확인해야 한다. `score_effect=none`이다. 근거:
[ISO 15848-1:2015 §§1, 5.1.5, 5.2](https://cdn.standards.iteh.ai/samples/61441/090700bf78cd4746bf4eec99f7d50f57/ISO-15848-1-2015.pdf),
[ISO 공식 표준 기록](https://www.iso.org/standard/61441.html).

`seat_packing_acceptance_separation`은 IEC 60534-4와 ISO 15848-1의 서로 다른 test scope를
대조해 검증했다. IEC 60534-4는 seat leakage test를 class·test fluid·procedure·maximum seat
leakage 기준으로 별도 수행하고, main packing test를 다른 조항의 별도 test로 둔다. ISO 15848-1은
stem/shaft seal 및 body joint의 external leakage를 자체 type-test 절차에 따라 검사하며, 결과는
concentration 또는 leak-rate로 표현한다. 따라서 경로·시험방법·단위와 적용 기준을 섞지 말고,
해당 계약·규정에서 지정한 각각의 합격기준으로 판정한다. `score_effect=none`이다. 근거:
[IEC 60534-4:2021, Table 1, §§4.3–4.4](https://webstore.iec.ch/en/publication/31136),
[ISO 15848-1:2015, §§1, 3.6–3.9, 5.1.5](https://www.iso.org/standard/61441.html).

2026-10-11 `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`의
`sw02_state_transition_model`을 PLCopen의 상태·이벤트·전이 튜플 정의와 IEC 61131-3의 SFC 범위에
대조해 verified 등록했다. 다만 결정론은 표준이 모든 응용 chart에 자동 보장하는 속성이 아니다.
현재 상태와 명령·피드백·허가·인터록·트립·타이머 등 평가 입력을 빠짐없이 모델에 포함하고,
동시 조건 및 우선순위를 설계에서 명시해 같은 상태/입력 조합의 다음 상태를 유일하게 해야 한다.
`score_effect=none`이다. 근거: [PLCopen Software Construction Guidelines, § state-diagram formal definition, p. 45](https://www.plcopen.org/download_file/force/5f66721e-9586-43d0-9f7c-79faa00e9ae4/342/),
[IEC 61131-3:2025 official scope](https://webstore.iec.ch/en/publication/68533).

같은 Topic의 `sw02_fail_safe`도 HSE 기능안전·제어시스템 지침에 대조해 verified 등록했다.
Fail-safe의 목표는 정의된 안전상태의 달성·유지이며, HSE는 상실 시 트립상태로 가는 actuator의
예로 held-open spring-return 구성을 들고, 특정 조건에서는 전원을 유지해야 안전할 수 있다고
명시한다. 따라서 고장응답은 위험분석, 요구 안전기능 및 실제 최종요소의 고장거동을 기준으로
정해야 하며 fail-close 또는 de-energize를 보편 규칙으로 단정하지 않는다. `score_effect=none`이다.
근거: [HSE Functional safety](https://www.hse.gov.uk/eci/functional.htm),
[HSE Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm),
[HSE Electrical power systems](https://www.hse.gov.uk/eci/electrical.htm).

`sw02_manual_mode_boundary`도 HSE control-system guidance로 verified 등록했다. HSE는 정상
운전의 자동 sequence가 manual procedure로 수행될 수도 있음을 인정하면서, 보호 interlock은
운전자나 process control system 모두의 위험유발 동작을 막아야 하며, 보호계통에 demand를
발생시킬 수 있는 operator command는 차단하거나 검증하도록 한다. 따라서 manual mode는 정상
sequence 소유권을 바꿀 수 있지만 필수 보호를 자동 해제하는 권한은 아니다. 별도 보호 override는
해당 안전요건에 따라 관리해야 한다. `score_effect=none`이다. 근거: [HSE Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm).

`sw02_cause_effect`는 IEC 62881:2018에 대조해 verified 등록했다. 표준은 C&E matrix를 기존
설계문서에서 도출된 원인-결과 관계를 discipline 간 일관되게 교환하는 문서형식으로 다루며,
PLC/DCS 코드로의 전환과 복잡한 순차논리의 플랫폼별 구현은 그 범위에서 제외한다. 따라서
matrix가 설계 의도를 명확히 하고 안전 검증의 참조가 될 수는 있어도 실행 로직 자체를 대신한다고
해석하지 않도록 claim을 제한했다. `score_effect=none`이다. 근거: [IEC 62881:2018 official scope](https://webstore.iec.ch/en/publication/33097).

`sw02_debounce_hysteresis`는 접점 채터·짧은 입력펄스에 대한 필터 동작, 임계값 주변 노이즈에
대한 hysteresis, 그리고 입력필터가 보호 응답을 늦추거나 짧은 유효 펄스를 누락시킬 수 있다는
문장 범위를 Rockwell·Siemens·Analog Devices의 공식 자료로 교차 확인해 verified 등록했다.
이를 모든 입력에 일괄 적용하라는 뜻으로 해석하지 않도록, 방법·시간은 신호와 요구 응답시간에
맞춰 선택한다는 조건을 기록했다. `score_effect=none`이다. 근거: [Rockwell chatter detection](https://www.rockwellautomation.com/en-gb/docs/add-on-profiles/ra-1756-discrete/40/pv1756discrete-ditamap/1756-sequence-of-events-input-device/points-view/about-chatter-detection.html),
[Siemens S7-1200 input filter](https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/device-configuration/configuring-the-operation-of-the-cpu/configuring-digital-input-filter-times),
[Analog Devices hysteresis](https://www.analog.com/en/resources/analog-dialogue/articles/curing-comparator-instability-with-hysteresis.html),
[Siemens safety input debounce manual](https://cache.industry.siemens.com/dl/files/827/70235827/att_100115/v1/Safety_Integrated_Function_Manual_en-US.pdf).

`sw02_trip_latch_reset`은 현재 문구 전체를 verified 처리하지 않았다. HSE는 보호 Trip이 정당화되지
않는 한 self-reset 되지 않아야 한다고 하고, Siemens의 특정 fail-safe module은 fault 원인이
해결됐거나 더 이상 존재하지 않을 때 acknowledgment를 허용한다. 그러나 이 자료만으로 모든
Trip에 Reset edge, 조작권한, 모든 안전조건 재확인이 반드시 필요하다고 일반화할 수 없다.
이 세부조건은 SRS·설비 위험·구현에 따라 명시해야 하므로, 현 Anchor의 복합적 의무 문구는
이 상태로 미검증 유지한다. 근거: [HSE Control systems – protection systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm),
[Siemens fail-safe module Trip RESET](https://docs.tia.siemens.cloud/r/fail_safe_modules_manual_collection_enus_20/device-specific-information/et-200sp-fail-safe-modules/motor-starters/motor-starter-3rk1308-0-00-0cp0/functions/trip-reset?contentId=ZuCb_TJ4~85z5jxg67cg7g),
[European Commission JRC Seveso inspection questions – SIF reset](https://minerva.jrc.ec.europa.eu/en/shorturl/technical_working_group_2_seveso_inspections/questions_and_tips_for_seveso_inspections_safety_instrumented_functions).

### 검증 결과 및 release gate

2026-10-11 `electronics_error_noise_drift_tolerance_aging_power_mitigation`의
`eem_power_supply_sensitivity`를 Analog Devices와 National Instruments 자료에 대조해
verified 등록했다. 전원 ripple/variation은 ADC·reference signal chain에 조건부로 결합될 수
있으며, sensor excitation과 ADC reference를 공유하는 ratiometric 구조는 공통 변동을 상쇄할
수 있다. Ground-potential difference는 ground-referenced 입력에서 측정오차가 될 수 있지만
모든 differential architecture에 일반화하지 않는다. `score_effect=none`이다.
근거: [ADI signal-chain supply-noise sensitivity](https://www.analog.com/en/resources/analog-dialogue/articles/optimizing-power-systems-for-the-signal-chain-part-1.html),
[ADI sensor excitation and ratiometric measurement](https://www.analog.com/en/resources/analog-dialogue/articles/transducer-sensor-excitation-and-measurement-techniques.html),
[ADI ADC reference design](https://www.analog.com/en/resources/analog-dialogue/articles/precision-successive-approximation-adcs.html),
[NI DC voltage measurement](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-direct-current-dc-voltage.html).

2026-10-11 `electronics_error_noise_drift_tolerance_aging_power_mitigation`의
`eem_filter_not_offset_fix`를 Analog Devices 자료와 대조해 verified 등록했다. 일반적인
noise/bandwidth conditioning은 offset·gain·reference error의 calibration을 대신하지 않는다.
단, DC 차단 high-pass가 오프셋을 제거한다고 표현할 경우 원하는 DC 신호도 함께 차단하므로
이를 오차 calibration과 혼동하지 않는다는 적용조건을 명시했다. 채점 영향은 `none`이다.
근거: [ADI Design Note 9: Chopper Amplifiers Complement a DC Accurate Low-Pass Filter](https://www.analog.com/en/resources/design-notes/chopper-amplifiers-complement-dc-accurate-low-pass-filter.html),
[ADI Methods for Calibrating Gain Error in Data-Converter Systems](https://www.analog.com/en/resources/technical-articles/methods-for-calibrating-gain-error-in-dataconverter-systems.html).

이번 작업에서 SW-06 병행운전 주장과 제어밸브 저소음 트림 용량 관계를 근거가 뒷받침하는
범위로 한정해 각각 검증 등록했다. SW-09 원격접속·Jump server·훈련 관련 본문과 집중 회귀
테스트도 실제 근거 범위에 맞춰 정합화했다. 최종 관련 회귀는 통과했지만 전체
`PROMOTE_GENERATED=0 scripts/validate_release.sh`는 offline deterministic replay 점수
범위율 0.8125로 기존 기준 0.85에 미달해 실패했다. 점수 계약이나 기준은 변경하지 않았다.
따라서 전체 release gate는 아직 PASS가 아니며, 이는 기술 Fact 미검증 873건과 별도 추적한다.

2026-10-11 최신 재실행은 DP 매니폴드 토픽의 기존 사람 승인 해시가 변경된 앵커 내용과
불일치하여 `build_generated_rubrics.py` 단계에서 중단됐다. 기존 사람 승인 메타데이터를
LLM이 임의로 갱신하거나 사람 승인으로 가장하지 않았다. 이 승인 불일치가 해소된 뒤 전체
gate를 다시 실행해야 한다. 앞선 실행에서 관찰된 offline deterministic replay 범위율
0.8125/0.85 실패도 별도 회귀 항목으로 남아 있다.

### 전자오차 Topic: ADC·필터 Anchor 검증 (2026-10-11)

`electronics_error_noise_drift_tolerance_aging_power_mitigation`에서 아래 21개 Anchor를
제조사 기술자료와 대조해 verified 등록했다. 출처 없는 WordPress 원문을 기술 근거로 삼지
않았고 모든 항목은 `score_effect=none`이다.

| Anchor | 확인 사항 | 독립 근거 |
|---|---|---|
| `eem_adc_resolution_accuracy` | 코드 step/bit 수에 관련된 resolution과 실제값 근접도인 accuracy는 다르며 시스템 noise/error가 실제 유효 성능을 제한할 수 있음 | [TI ADC Accuracy Part 1](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/adc-accuracy-part-1-is-accuracy-different-from-resolution), resolution 정의 및 signal-chain noise; [TI ADC Accuracy Part 2](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/adc-accuracy-part-2-total-unadjusted-error-explained), offset/gain/INL 및 reference·driver 기여 |
| `eem_adc_quantization` | 연속 입력을 유한 코드로 매핑할 때 생기는 양자화 오차와 offset/gain/INL 등 전체 정확도 오차를 구분 | [ADI ADC Glossary](https://www.analog.com/en/resources/glossary/adc.html), ADC 동작 및 quantization error; [TI ADC Accuracy Part 2](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/adc-accuracy-part-2-total-unadjusted-error-explained) |
| `eem_adc_aliasing_boundary` | 대역 밖 입력 성분이 Nyquist 조건 위반 시 관심 대역으로 접힐 수 있고 입력 필터가 이를 감쇠; 양자화 오차와 다른 sampled-data 현상 | [ADI Filter Basics: Anti-Aliasing](https://www.analog.com/en/resources/technical-articles/guide-to-antialiasing-filter-basics.html), “Background” 및 “Anti-Alias Filters”; quantization 구분은 [ADI ADC Glossary](https://www.analog.com/en/resources/glossary/adc.html) |
| `eem_noise_bandwidth` | noise density와 대역폭으로 통합 noise를 평가하고 좁은 RC bandwidth가 settling/응답에 영향을 줌 | [ADI Front-End Amplifier and RC Filter Design](https://www.analog.com/en/resources/analog-dialogue/articles/front-end-amp-and-rc-filter-design.html), noise calculation/settling; [ADI Practical Filter Design](https://www.analog.com/en/resources/analog-dialogue/articles/practical-filter-design-precision-adcs.html), 좁은 bandwidth와 settling |
| `eem_filter_noise_mitigation` | 필터가 선택된 대역 외 noise를 줄일 수 있지만 passband attenuation, phase/group delay, settling/latency trade-off가 있음 | [ADI Practical Filter Design](https://www.analog.com/en/resources/analog-dialogue/articles/practical-filter-design-precision-adcs.html), “Ideal and Practical Filters,” “RC Antialias Filter,” “Phase Delay,” latency and conclusion |
| `eem_psrr` | PSRR은 supply disturbance의 출력 전달을 나타내며 주파수 sweep과 실제 signal-chain 조건에서 평가해야 함 | [ADI Characterizing PSRR](https://www.analog.com/en/resources/analog-dialogue/articles/characterizing-the-psrr-of-data-acquisition-umodule-devices-with-internal-bypass-capacitors.html), “PSRR Definition” 및 PSRR characterization sections |
| `eem_linearity_error` | ADC INL은 선택한 직선 기준에 대한 transfer deviation이며 정적 offset/gain 제거 후에도 남을 수 있음 | [ADI INL/DNL Measurements](https://www.analog.com/en/resources/technical-articles/inldnl-measurements-for-types-of-highspeed-adcs.html), “INL and DNL Definitions” |
| `eem_random_noise` | 열·shot·증폭기·reference·supply 등 signal-chain noise source와 bandwidth·aliasing의 관측 영향 | [ADI Sigma-Delta ADC Driver](https://www.analog.com/en/resources/analog-dialogue/articles/maximize-the-performance-of-your-sigma-delta-adc-driver.html), noise sources/bandwidth; [ADI ADC Input Noise](https://www.analog.com/en/resources/analog-dialogue/articles/adc-input-noise.html), input-referred noise |
| `eem_rss_worstcase` | deterministic bounded errors는 절댓값 합으로 보수적 상계를 둘 수 있고 RSS는 표준불확도와 공분산을 전제로 적용 | [NIST TN 1297 §5.1](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty), 표준불확도·공분산·RSS; 삼각부등식 직접 유도 |
| `eem_reference_error` | reference의 초기 정확도·온도계수·noise·장기 안정도와 부하 영향은 제품/회로 조건에 따른 시스템 scale error 및 drift 요인 | [ADI AN-82](https://www.analog.com/en/resources/app-notes/an-82f.html), 초기 정확도·온도계수·장기 안정도·noise; [ADI Selecting the Optimum Voltage Reference](https://www.analog.com/en/resources/technical-articles/selecting-the-optimum-voltage-reference.html), ADC reference와 부하/안정도 조건 |
| `eem_offset_error` | zero/reference 입력에서의 transfer offset 및 입력 offset voltage·bias current의 저항 경로 유입에 따른 회로 offset | [ADI ADC accuracy](https://www.analog.com/en/resources/technical-articles/an-inside-look-at-high-speed-analog-to-digital-converter-accuracy-part-one.html), offset 정의; [TI Op Amp Offset Voltage and Bias Current Limitations](https://www.ti.com/lit/pdf/sboa590), offset 및 bias-current voltage error |
| `eem_gain_error` | 실제/이상 transfer slope 차이의 scale error; resistor ratio, amplifier gain, reference 및 ADC/full-scale path의 구체 사례 | [ADI CN0393](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0393.html), documented chain contributor analysis; [ADI ADC error overview](https://www.analog.com/en/resources/technical-articles/the-abcs-of-analog-to-digital-converters-how-adc-errors-affect-system-performance.html), gain 정의와 reference test boundary |
| `eem_error_classification` | 반복 시 예측 가능한 systematic error, 반복 시 예측 불가능하게 달라지는 random error, 계측기 metrological property 변화에 따른 시간적 drift를 구분 | [JCGM VIM 2.17](https://jcgm.bipm.org/vim/en/2.17.html), systematic error; [VIM 2.19](https://jcgm.bipm.org/vim/en/2.19.html), random error; [VIM 4.21](https://jcgm.bipm.org/vim/en/4.21.html), instrumental drift |
| `eem_calibration_interval` | required uncertainty·한계초과 risk·사용 severity·환경·규제, 과거 교정 기록 및 drift, 비용/위험 균형에 따라 calibration interval을 초기 설정·재검토하며 보편 단일 주기를 두지 않음 | [ILAC-G24:2022 / OIML D 10:2022 §§4.5–4.8, 5.1, 6.1](https://ilac.org/?ddownload=124891), 위험평가·기록·재검토·비용 균형 |
| `eem_tolerance_definition` | 납품 시 명목값 대비 tolerance와 운전 중 온도/시간에 따른 특성변화·stability를 구분 | [Vishay, Basics of Linear Fixed Resistors](https://www.vishay.com/docs/28771/basics.pdf), Nominal Value·Tolerance·Stability·TCR 정의 |
| `eem_temperature_coefficient` | resistor·reference·amplifier/ADC의 temperature coefficient 또는 온도 drift가 회로 및 sensor-interface error budget에 기여할 수 있음; 구체 영향은 회로·측정모델별로 한정 | [ADI AN-0970](https://www.analog.com/en/resources/app-notes/an-0970.html), ADC offset/gain·reference-resistor drift in RTD interface; [ADI temperature drift example](https://www.analog.com/en/resources/technical-articles/2022/07/16/10/51/understanding-temperature-drift-in-a-precision-digital-to-analog-converter-dac.html), converter/reference error budget; [Vishay TCR](https://www.vishay.com/en/resistors/change-resistance-due-to-rtc-calculator/), resistance change vs temperature |
| `eem_tolerance_propagation` | 회로감도에 따른 component error 전파, 공통 기준 입력환산, worst-case 합산 및 공분산을 반영하는 통계적 불확도 결합 | [ADI CN0393](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0393.html), component tolerance·gain·reference의 system error 변환과 worst-case table; [NIST TN 1297 §5.1](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty), 표준불확도·공분산 기반 통계 결합 |
| `eem_error_budget` | 실제 signal-chain sensitivity를 통해 offset·gain·resistor/reference 및 converter error를 같은 input-referred 기준으로 옮겨 전체 범위와 항별 기여를 비교하는 방식 | [ADI CN0393](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0393.html), input-referred system error 계산 및 항목별 표; [NIST TN 1297 §5.1](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty), 통계 불확도 결합 및 covariance |
| `eem_aging_definition` | 사용·보관·stress 조건에 따른 장기 component parameter 변화가 calibration stability에 영향을 줄 수 있음; 보편적인 aging rate나 단조 drift로 일반화하지 않음 | [Vishay TN0015](https://www.vishay.com/docs/49418/vsd-tn00.pdf), load-life stability가 시간·온도·부하·시험법에 의존; [ADI AN-713](https://www.analog.com/en/resources/app-notes/an-713.html), voltage-reference long-term drift와 초기 정확도·온도계수의 구분 및 장기 측정 |
| `eem_snr_dynamic_range` | SNR·dynamic range·ENOB/effective resolution은 noise floor와 signal/range 조건에 좌우되고, 더 많은 ADC bits만으로 analog front-end noise가 없어지지 않음 | [ADI Understanding Noise, ENOB, and Effective Resolution](https://www.analog.com/en/resources/technical-articles/noise-enob-and-effective-resoluition-in-analog-to-digital-converter-circuits--maxim-integrated.html), RMS noise에 따른 effective resolution/SINAD; [ADI ADC Accuracy Part 2](https://www.analog.com/en/resources/technical-articles/an-inside-look-at-high-speed-analog-to-digital-converter-accuracy-part-2.html), front-end noise가 시스템 dynamic range와 accuracy를 제한 |
| `eem_aging_definition` | 사용·보관·stress 조건에 따른 장기 component parameter 변화가 calibration stability에 영향을 줄 수 있음; 보편적인 aging rate나 단조 drift로 일반화하지 않음 | [Vishay TN0015](https://www.vishay.com/docs/49418/vsd-tn00.pdf), load-life stability가 시간·온도·부하·시험법에 의존; [ADI AN-713](https://www.analog.com/en/resources/app-notes/an-713.html), voltage-reference long-term drift와 초기 정확도·온도계수의 구분 및 장기 측정 |
| `eem_calibration_systematic` | calibration은 reference 비교로 bias를 줄이고 설정된 모델의 offset/gain을 교정할 수 있으나 결과 불확도와 향후 성능 변동은 남음 | [NIST/SEMATECH §2.3](https://www.itl.nist.gov/div898/handbook/mpc/section3/mpc3.htm), reference comparison과 bias reduction; [ADI gain calibration](https://www.analog.com/en/resources/technical-articles/methods-for-calibrating-gain-error-in-dataconverter-systems.html), offset/gain 보정 예와 방법 한계; [NIST calibration policy](https://www.nist.gov/calibrations/policies), 사용 불확도 및 미래 성능 비보장 |

이 21개는 전자오차 Topic의 나머지 Anchor를 자동 검증하지 않는다. 다른 회로원인, component drift 및 mitigation 세부사항은 해당 Claim 전체를 지지하는 근거를 별도로 확보해야 한다.

#### 전자오차 Topic 후속 검토 보류

`eem_drift_definition`은 아직 verified로 올리지 않았다. 현 문장은 온도·전원·self-heating·운전조건의 변화와 시간에 따른 계측기 drift를 모두 같은 용어로 묶는다. JCGM VIM 4.21은 instrumental drift를 시간에 따른 계측 indication의 연속/증분 변화로 정의하며, 측정량이나 인식된 영향량의 변화와 구별한다. 따라서 현 문구는 `drift`와 영향량 변화에 따른 variation을 혼합할 소지가 있어, 주장을 분리·정리한 뒤 Pack 문구를 재검증해야 한다. 근거: [JCGM VIM 4.21](https://jcgm.bipm.org/vim/en/4.21.html), [ILAC-G24:2022 / OIML D 10:2022 §3.10](https://ilac.org/?ddownload=124891).

### SW-06 병행운전 Anchor의 근거 범위 정리 (2026-10-11)

`sw06_parallel_operation_controls`의 기존 문구는 control ownership 충돌, 공통원인 오류,
복귀 보장 등 근거가 확인되지 않은 OT 위험을 한 문장에 포함하고 있었다. 이를 GAO/JFMIP의
일반 정보시스템 전환 자료가 직접 뒷받침하는 범위로 수정했다. 구·신 시스템 출력 비교를 위한
시험으로 parallel operation을 사용할 수 있지만, 중복 입력과 결과 조정에 자원이 들 수 있으며
적절한 backup·재해복구계획이 있을 때 continuity의 기본 대체수단이라고 간주하지 않는다는
내용이다. 해당 자료는 OT 표준이 아니므로 이 구분을 명시했고 `score_effect=none`으로 등록했다.
근거: [GAO/JFMIP Parallel Operation of Software](https://www.gao.gov/assets/a02633.pdf),
[GAO Lessons Learned, guidance item 63](https://www.gao.gov/assets/LESSONS_LEARNED_ABOUT.pdf).

### 저소음 트림의 용량 관계 Anchor 범위 수정 (2026-10-11)

`low_noise_trim_capacity_rangeability_tradeoff`의 일률적 tradeoff 문구를 수정했다. Emerson은
전통적인 복잡형 저소음 설계에서 저감량·비용·용량 간 상충을 설명하지만, Fisher WhisperFlo 및
Whisper 계열 제품에는 소음저감과 함께 높은 유량용량을 제시하는 설계도 있다. 따라서 특정
저소음 트림 전체에 고정 tradeoff를 적용하지 않고 제조사·제품별 유량용량/범위 및 소음 자료를
확인하도록 한정했다. 제품 문서는 해당 제조사 제품 주장으로만 사용했고 `score_effect=none`이다.
근거: [Emerson Whisper trim product announcement](https://www.emerson.com/en/corporate/news/2023/11-new-fisher-whisper-trim-technology-rotary-and-globe-valves),
[Fisher WhisperFlo](https://www.emerson.com/en/final-control/products/fisher-whisperflo).

### 성과 KPI gaming Anchor의 적용범위 한정 (2026-10-11)

`kpi_gaming_single_metric_tradeoff`의 기존 문구는 정비분야에서 실제 발생하는 고장 미등록·
정비 조기종결·과잉 예방정비라는 구체 사례를 근거 없이 일반화했다. 이를 GAO의 일반 성과측정
지침으로 한정해, 목표 정렬·명확한 정의·균형 잡힌 지표 집합과 단일 지표에 대한 과도한 의존이
만들 수 있는 gaming/왜곡 유인만 기술한다. 이는 정비 KPI에 대한 실증 결과나 보편 산식이
아니며 `score_effect=none`으로 등록했다.
근거: [GAO-19-216 Appendix VII](https://www.gao.gov/pdf/product/697768),
[GAO/GGD-98-162](https://www.gao.gov/assets/ggd-98-162.pdf),
[GAO-26-107609](https://www.gao.gov/assets/gao-26-107609.pdf).

### DP transmitter 3-valve zero-check sequence 교정 (2026-10-11)

`manifold_isolation_sequence`에 있던 `3-valve` + `bleed open` 조합은 구성상 잘못된 일반화였다.
Rosemount 2051 manual은 3-valve를 H/L isolation 2개와 equalizer 1개로 설명하며, zero check에서
LP isolation을 먼저 닫고 equalizer를 연 다음 복귀 시 equalizer를 닫고 LP isolation을 다시
열도록 한다. 정상상태는 H/L open, equalizer closed다. 이 자료를 model-specific 절차로만
등록하고, equalizer가 process depressurization/bleed를 의미하지 않는다는 경계를 명시했다.
다른 모델이나 5-valve/vent 구성의 절차로 전용하지 않는다. `score_effect=none`.
근거: [Emerson/Rosemount 2051 Reference Manual, §2.8.4, Tables 2-7](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-00809-0100-4101.pdf).

### OT 보안 목적·자산관리 Anchor 범위 축소 검증 (2026-10-11)

OT cybersecurity Pack의 `sw09_security_objectives`는 NIST SP 800-82 Rev. 3의 표현으로
범위를 좁혔다. NIST는 OT가 성능·신뢰성·안전 요구를 고려하고 CIA 손실 영향을 분류하며,
가용성이 일반적으로 가장 큰 OT 우려라고 설명한다. 보안 요구 배정에서도 성능·안전 영향을
고려한다. 이를 모든 플랜트에서 confidentiality보다 availability가 절대 우선한다는 규칙으로
일반화하지 않는다. `sw09_asset_inventory`는 NIST §6.1.1의 hardware, software/firmware version,
vendor, asset owner와 운영·정비·사이버보안 역할, 변경 시 inventory 갱신 권고로 제한했다.
세부 목록은 source의 예시이지 모든 사이트의 고정·완전 schema라고 주장하지 않는다.
두 항목 모두 `score_effect=none`. 근거: [NIST SP 800-82 Rev. 3, §4.3.2 / §6.1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

같은 NIST 가이드의 `sw09_risk_assessment`는 threats, vulnerabilities, harm, likelihood와 OT 물리·공정·안전 영향을 식별한다는 범위로 한정했다. `sw09_system_under_consideration`는 NIST의 asset identification, authorization boundary, information type, network data-flow/interconnection 작업으로 표현을 축소했다. 이를 IEC 62443의 System under Consideration·trust boundary 용어와 같은 뜻이라고 주장하지 않는다. 두 항목 모두 `score_effect=none`.

`sw09_zone_conduit`는 IEC 62443-3-2:2020의 공식 scope summary에 맞춰 SUC 정의, zones/conduits 분할, 각 단위 위험평가, target security level 설정과 security requirements 문서화로 한정했다. zone grouping의 세부 기준이나 trust boundary·정책장치와의 동의어 관계는 이 summary만으로 검증하지 않았다. `score_effect=none`. 근거: [IEC 62443-3-2:2020](https://webstore.iec.ch/en/publication/30727).

`sw09_segmentation`은 NIST SP 800-82 Rev. 3의 구체 예시(관리권한, trust, 기능 중요도, data flow, 위치에 따른 구분; 성능·안전을 고려한 levels/tiers/zones; 인접 segment 사이만 허용하는 firewall rules)로 범위를 좁혔다. 다른 모든 논리·물리 경계와 우회경로가 같은 checklist를 따라야 한다고 확대하지 않는다. `score_effect=none`.

`sw09_industrial_dmz`는 corporate/enterprise와 OT 간 direct traffic 방지, enterprise↔operations-management 통신의 DMZ services 경유, 해당 서비스 감시·보호라는 NIST guidance로 한정했다. historian relay·patch staging 등은 보편 필수 항목으로 주장하지 않는다. `sw09_unidirectional_gateway`는 NIST의 hardware-enforced one-way 특성 및 operational→enterprise 예시로 축소했고, 이를 모든 maintenance·control use에 적합하다고 확대하지 않았다. 두 항목 모두 `score_effect=none`.

`sw09_allowlisting`은 NIST §5.2.5.1의 host application 실행 제한, 올바른 설정 시 비인가 application 실행 차단으로 좁혔다. update·emergency·learning-mode 절차는 이 출처로 확인하지 않았다. `sw09_patch_management`는 sandbox/test 선행시험(가능한 경우), scheduled maintenance 적용과 recovery plan, zone별 availability 제약이라는 NIST §5.2.5.2 범위로 한정했다. 양쪽 모두 `score_effect=none`.

`sw09_firewall_policy`는 NIST의 인접 level/tier/zone 통신 제한과 authorized inbound/outbound communication으로, `sw09_logging`은 장치·시간·위치·event/source·계정·결과 필드 및 기기 capability에 따른 선택으로 축소했다. `sw09_time_synchronization_forensics`는 공통 primary clock과 일관된 timestamp/timezone 표기 권고로 한정했으며 특정 protocol이나 보편 timezone policy는 덧붙이지 않았다. 세 항목 모두 `score_effect=none`.

### 제어밸브 seat leakage 기준의 시험조건 범위 검증 (2026-10-11)

`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`의
`shutoff_class_purpose_scope`는 FCI 공식 안내문이 말하는 범위로 정리했다. ANSI/FCI 70-2는
정의된 시험조건에서 제어밸브 seat tightness의 최대 허용 누설량을 기준화하며, 사용자의
적용별 rated leakage 선정과 제조자 시험 결과 비교를 돕는다. 이를 다른 운전조건의 현장 누설량
보증으로 확대하지 않는다. `class_test_condition_dependency`도 Fisher Catalog 12 §2-28의
실제 표·주석 범위로 좁혔다. 이 표는 class별 maximum leakage expression, test medium,
pressure와 temperature를 제시하고 이를 factory acceptance test 조건으로 한정하며, 아주 낮은
leakage를 다른 조건에 외삽하는 것의 오해 가능성을 경고한다. 이 자료가 duration·stabilization·
pressure direction 등 다른 변수를 모든 경우에 의무화한다고 확대하지 않는다. 두 항목 모두
`score_effect=none`. 근거: [FCI ANSI/FCI 70-2 informational sheet](https://www.fluidcontrolsinstitute.org/70_2_InformationalSheet.pdf),
[Fisher Catalog 12 §2-28](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf).

### 예비품 보충정책 Anchor 범위 축소·검증 (2026-10-11)

`spares_stock_policy_reorder_leadtime`를 수요·조달 Lead Time·운전/수리 중 공급완충,
reorder point와 주문·보유비용 균형을 다룬 문구로 한정했다. GAO-09-103 pp. 7–8의
미 해군 사례는 재주문기간 수요, 조달 Lead Time, 안전수준, 수리주기 재고 및 주문·보유비용
균형을 설명한다. DOE OIG-24-30 pp. 1–2는 WAPA의 critical spare 재고수준과 현지 요건에
따른 reorder point 설정 필요를 다룬다. 이 근거는 적용 사례를 뒷받침할 뿐 모든 플랜트의
보편 산식, min/max, MOQ 또는 공용화 규칙을 정하지 않는다. `score_effect=none`이며
기존 채점 영향은 없다. 근거: [GAO-09-103](https://www.gao.gov/assets/gao-09-103.pdf),
[DOE OIG-24-30](https://www.energy.gov/ig/articles/audit-doe-oig-24-30).

같은 Pack의 `spares_preservation_shelf_life_rotation`은 NASA Lessons Learned 724가
직접 다루는 제한 shelf-life 품목으로 범위를 축소했다. 해당 NASA 우주 시스템 사례는
그런 예비품을 식별·주기 조달하고 만료품은 제거·교체하도록 권고한다. 이 근거로 방습·방진,
정기 기능시험, firmware/license 상태 또는 FIFO/rotation을 모든 계장 예비품의 보편 요건으로
간주하지 않는다. `score_effect=none`. 근거: [NASA LLIS Lesson 724](https://llis.nasa.gov/lesson/724).

`spares_obsolescence_substitution_moc`는 supplier-specific product lifecycle 예시와
OT 구성변경 통제의 접점으로 축소했다. NI 문서는 자사 제품에 대해 Mature/LTB/support/
discontinued 상태별 구매·후속품·수리 지원 차이를 설명하며, NIST SP 800-82 Rev. 3은 OT
baseline을 문서화하고 변경을 배포 전 문서화·시험·승인하도록 권고한다. NI 수명주기 정의를
다른 업체 정책으로 일반화하지 않고, 공통 I/O·통신·안전 적합성 체크리스트도 주장하지 않는다.
`score_effect=none`. 근거: [NI Hardware Product Lifecycle Policies](https://www.ni.com/en/support/hardware-product-life-cycle-policies.html),
[NIST SP 800-82 Rev. 3, §6.2.4.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

SW-06의 `sw06_data_configuration_transformation_validation`은 HHS EPLC Data Conversion
가이드가 직접 제시하는 source-target mapping, blank/new-code/부적절 값 처리규칙,
표본 및 모의 변환, accuracy/completeness 조정과 duplicate 제거로 문구를 축소했다.
이 IT practice guide를 OT 보편 규격으로 취급하지 않으며 체크섬·단위/인코딩·record-count·
공정 의미 검증은 프로젝트별 acceptance criteria로 남겼다. `score_effect=none`.
근거: [HHS EPLC Data Conversion Practice Guide v1.0](https://www.hhs.gov/sites/default/files/ocio/eplc/EPLC%20Archive%20Documents/30-Data%20Conversion/eplc_data_conversion_practices_guide.pdf).

같은 HHS 가이드의 전환전략 계획 문구를 `sw06_migration_strategy_selection`에 반영했다.
parallel operation 대 one-time cutover, 구 시스템 archive 대 계속 운영은 실제 계획에서
결정하는 선택지로만 확인된다. 단계전환·pilot·hybrid 등은 모든 OT 전환에 대한 가이드의
의무 전략이 아니며, 현장 허용정지시간과 위험조건을 함께 정해야 한다. `score_effect=none`.

`sw06_cutover_freeze_gonogo`도 HHS 가이드 pp. 2–3에 직접 기술된 사전 backup,
sample/mock conversion, accuracy/completeness 조정, 전환일 계획·공유, online service 중지
검토 및 직전 backup 복귀 예로 한정했다. universal OT 승인·go/no-go나 공정안전 checklist는
이 IT practice guide에서 도출하지 않는다. `score_effect=none`.

`sw06_post_cutover_stabilization_decommission`은 HHS 가이드 §3의 전환 data format·
completeness·accuracy 검증, 중복 제거와 이슈 해결로 한정했다. 해당 IT guide는 OT alarm·
communications·performance 안정화 기간이나 legacy controller 폐기 기준을 정하지 않는다.
`score_effect=none`.

`sw06_emergency_change_retrospective_control`은 OSHA 29 CFR 1910.119(l)(1)–(3)의
covered-process MOC로 범위를 바꿨다. 대상 공정에서는 in-kind 대체 외 변경에 사전 기술근거·
안전영향·절차수정·기간·승인 검토와 영향 인력 통지·교육이 요구된다. OSHA 조항은 보편적인
긴급변경 면제나 OT backup/통신 체크리스트를 규정하지 않는다. `score_effect=none`.
근거: [OSHA 29 CFR 1910.119](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119).

### Manifold 운전 순서 재검토 (2026-10-11)

`manifold_isolation_sequence`와 `manifold_return_sequence`는 과거 batch audit의 `확인` 상태와
달리 제조사 자료에서 보편적 단일 절차로 확인되지 않아 미승인으로 유지한다. 특히 3-valve와
5-valve 구성 및 zero-trim / isolation / venting 작업을 구분해야 한다. 상세 대조 근거는
[DP transmitter manifold Anchor 후속 감사](topic_anchor_evidence_followup_20261011_manifold.md)에 기록했다.

### 광학 센서 방식 선정 Anchor 검증 (2026-10-11)

`optical_method_selection_tradeoff`는 KEYENCE의 변위센서 선정 가이드, ifm의 광전식 센서 응용별
선정 자료, OSHA 레이저 위험등급 자료를 대조해 검증했다. 요구 정확도·범위·속도, 대상 재질 및
환경, 설치·안전·투자 조건은 application-specific selection criteria이며, 특정 방식이 모든 조건에서
최적이라는 주장은 하지 않는다. 출처와 한정조건은 approved fact registry에 기록했다.

`production_defect_containment_traceability`는 NIST IR 8536 제조 추적성 프레임워크와 ISO 29001의
부적합 산출물·추적성 기록 및 책임 지정 근거로 검증했다. 추적 필드와 격리 범위는 적용되는 제품·고객·
규제·QMS에 따라 달라질 수 있으므로, 고정 필드 목록이나 단일 처분방식을 요구하지 않도록 조건을 기록했다.

같은 Pack의 `production_daily_management_visual_control`은 Lean Enterprise Institute의 production
analysis board 자료로 계획 대비 실적 비교, 이상 기록 및 문제원인 탐색은 뒷받침됨을 확인했다. 그러나
현행 Anchor의 지표 전체(manpower, material shortage, WIP 등), 반드시 짧은 주기로 모두 검토해야 한다는
주장, 모든 조치의 owner·due date 및 다음 교대 반영을 보편 계약으로 지지하는 근거는 부족하다. 현행 문구는
조건·권고와 보편 요건을 분리하지 않아 미승인으로 유지한다. 출처: [Lean Enterprise Institute, Production
Analysis Board](https://www.lean.org/lexicon-terms/production-analysis-board/).

### Gas sizing Anchor 교차검증 (2026-10-11)

`control_valve_gas_sizing_choked_flow_critical_pressure_ratio`에서 `absolute_temperature_required`,
`pressure_ratio_direction`, `compressibility_factor_meaning`, `choked_flow_not_zero_flow`,
`choked_flow_downstream_independence`, `valve_pressure_drop_ratio_factor_meaning`,
`xTP_fitting_adjusted_factor`, `no_fitting_reference_condition`, `choked_pressure_ratio_limit`,
`expansion_factor_subcritical_relation`, `expansion_factor_bounds`, `subcritical_flow_behavior`,
`standard_volume_formula_structure`, `mass_flow_formula_structure`, `gas_property_input_selection`, `compressible_control_valve_sizing_scope`, `xT_valve_style_trim_travel_dependency`, `required_vs_rated_gas_coefficient`, `minimum_normal_maximum_gas_cases`, `steam_vapor_property_boundary`, `vendor_hand_calculation_crosscheck_gas`, `aerodynamic_noise_handoff`을 Emerson/Fisher gas sizing 자료와 대조하고, 가스물성 설명에는 NIST Natural Gas Handbook도 사용했다. `T1`은 절대온도이고 `x=ΔP/P1`이므로 고정된 `P1`에서 `P2` 하락은 `x`를 증가시킨다.
`Z1`은 inlet 상태의 실가스 보정계수이며, 초크 유동은 유량 0을 뜻하지 않고 동일한 상류조건·밸브상태에서
하류압력 저하가 더 이상 유량 증가를 만들지 않는 제한 상태다. `xT`는 attached fittings가 없는 밸브의
critical-flow pressure-drop ratio이고 `xTP`는 부착 fitting 영향을 sizing 식에 반영하는 대체 인자다.
제조사 sizing method의 no-attached-fitting 조건에서는 `FP=1`, `xTP=xT`가 된다.
Fisher Catalog 12의 제품표는 `xT`를 valve type/trim, flow direction, travel 구간별로 제공하며, gas sizing 예제는
100% travel에서 시작한 값과 계산된 travel의 `xT`를 다르게 적용해 재계산한다. 같은 예제는 process 조건으로
계산한 required `Cv`와 catalog의 rated `Cv`를 별도로 비교한다. 따라서 selected travel과 제품표를 대조해야 하며
required capacity와 rated capacity를 같은 값으로 취급하지 않는다.
`minimum_normal_maximum_gas_cases`는 project-defined minimum/normal/maximum service cases를
각각 검토하는 sizing practice로 한정해 등록했다. Valmet은 실제 운전조건 의존성과 minimum/maximum
등 여러 flow condition을 사용한 process model 검토를 설명하고, Emerson은 sizing input으로 pressure,
temperature 및 fluid properties를 든다. 세 case가 모든 프로젝트에서 의무라는 주장이나 특정 case가
항상 용량·소음의 governing case라는 주장은 하지 않는다. 근거: [Valmet Flow Control Manual §2.2, §2.4.4](https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/),
[Emerson Control Valve Sizing](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valves-sizing).
`steam_vapor_property_boundary`는 단상 증기/기체 property를 해당 압력·온도 상태에 맞추고,
wet-steam의 품질/건도는 이를 처리할 수 있는 sizing 검토에 반영하는 경계로 한정했다.
Emerson Handbook의 표준 compressible-flow 범위와 Spirax Sarco의 wet-steam 사례가 이를 뒷받침한다.
보편적인 wet-steam 방법이나 단일 허용 속도는 주장하지 않는다. 근거: [Emerson/Fisher Control Valve Handbook, 6th ed. §5.9](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf),
[Spirax Sarco Module 6.4, Example 6.4.2](https://www.spiraxsarco.com/learn-about-steam/control-hardware-electric-pneumatic-actuation/control-valve-sizing-for-steam-systems).
`vendor_hand_calculation_crosscheck_gas`는 vendor output의 일괄 승인/거절이 아니라 동일한 flow basis·단위·service case·equation 판본을 사용한 재현 가능한 계산 검산으로 한정했다. `FP`, `xT/xTP`, `Y`, travel은 구성과 식에서 적용될 때만 확인하며, 차이가 있으면 입력·방법 차이를 해소해야 한다. 근거: [Emerson/Fisher Control Valve Handbook §5.9.3](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [Fisher Catalog 12 Section 2, sample problem 1](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf).
`aerodynamic_noise_handoff`는 Fisher의 특정 sizing/noise 방법에서 gas sizing 후 `Cg=40 Cv xT` 관계를 noise prediction에 연결하고, pressure regime 및 service conditions와 저소음 trim 검토를 별도로 다루는 범위로 확인했다. `Topic 9`라는 소유권 표기는 이 저장소 내부 scope contract이지 보편 산업 분류가 아니다. 근거: [Fisher Catalog 12 Section 2, §5.9, p. 2-13](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf), [Emerson/Fisher Handbook §5.15–5.16](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf).
`fail_open_maximum_flow_case`는 아직 conditional/unverified로 유지한다. 제조사 sizing 식은 주어진 service case의 실제 pressure·flow·properties와 valve configuration으로 capacity를 계산하지만, 모든 fail-open scenario에서 최대 상류압력과 최소 하류압력이 동시에 신뢰성 있게 발생한다고 정하지 않는다. 해당 조합이 process cause/consequence analysis에서 credible함을 확인한 뒤 계산해야 하며, 그런 plant-specific 근거가 없어 지금은 `verified`로 승격하지 않았다. Fisher Catalog 12 §5.9는 지정된 service conditions에서 `P1`, `P2`, `T1`, gas properties와 xT/xTP를 넣어 용량을 계산하고, 초크 이후에는 같은 P1에서 P2를 더 낮춰도 flow가 증가하지 않음을 설명한다; 이 자료는 독립적으로 fail-open 사건 조합의 신뢰성을 입증하지 않는다. 근거: [Fisher Catalog 12 Section 2, §5.9, pp. 2-12–2-14](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf).
각 주장은 해당 식·장치구성 범위에 한정했고 모든 계수의 보편값이나 운전점에 무관한 유량 불변성을
주장하지 않는다. 압축성 유체 sizing의 적용범위는 Emerson Handbook이 표준 sizing 식의 정확도 범위를 single-component, single-phase 유체로 제한하고, gas·natural gas·steam을 예시 유체로 다룬다는 내용으로 한정했다. Valmet은 multiphase sizing의 정확도와 계산법을 별도로 다루므로 2상 유체를 이 단상 식에 일반화하지 않는다. 근거: [NIST Natural Gas Handbook, NBSIR 86-3057](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nbsir86-3057.pdf),
[Emerson/Fisher Control Valve Handbook, Chapter 5](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf),
[Valmet Flow Control Manual, Multiphase Flow](https://www.valmet.com/flowcontrol/valves/flow-control-manual/multi-phase-flow/),
[Emerson/Fisher Catalog 12, Section 2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s2.pdf),
[Emerson/Fisher Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf),
[Emerson/Fisher Valve Sizing Calculations (Traditional Method)](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351798x012_02.pdf).
모든 등록 Fact는 `score_effect=none`이다.

### 최신 근거 보강 (2026-10-11)

`optical_laser_photoelectric_noncontact_measurement_tof_triangulation`에서
`triangulation_range_resolution_tradeoff`, `surface_reflectivity_color_effect`,
`alignment_occlusion_geometry`, `tof_timing_jitter_resolution`, `accuracy_resolution_repeatability_boundary`,
`ambient_light_filtering`, `optical_vs_ultrasonic_tof_comparison`, `multipath_mixed_pixel_error`, `specular_transparent_surface_error` 아홉 Anchor를 출처가 직접 지지하는 관계로 좁혀 검증했다.
Hamamatsu는 far-field 근사 `d >> f`에서 `d=f·b/u`와 spot 좌표 오차 전파식
`δd=d²·δu/(f·b)`를 제시한다. 따라서 동일 거리와 검출기 좌표 오차에서 baseline 또는
focal length 증가는 모델상 거리 불확도를 낮추고, 거리가 멀어질수록 불확도는 거리 제곱에
비례해 증가한다. 같은 Hamamatsu 자료의 Direct ToF 사례에서는 target distance·color·orientation·surface smoothness가 return light amount와 pulse amplitude에 영향을 주고, 광로 차단은 shadowing/occultation으로 거리 측정을 막을 수 있으며 baseline 축소에는 불확도 증가가 따른다고 한다. 또한 `δd≈c·δt/(2n)`이며 detector jitter·rise-time variation·electrical noise·threshold crossing이 timing variation 원인으로 열거된다. 각각의 주장은 해당 기하·수광 구성 안에 한정하며 제품 성능 보증값이나 모든 광학센서의 보편식은 아니다.
같은 자료는 특정 Direct ToF setup에서 송신파장 `λ₀` 중심의 band-pass filter를 배경광 감소에 사용한다. JCGM VIM3는 resolution, repeatability/precision, accuracy를 별개 정의하며 accuracy가 수치량이 아니라고 명시한다.
`optical_vs_ultrasonic_tof_comparison`은 반사형 Direct optical ToF의 `d=ct/(2n)`와 초음파 pulse-echo의 `d=c_s·t/2`를 분리해 적고, 기체 조성·온도·증기압 조건은 탱크 ullage 경로로 한정했다. 광학 식은 Hamamatsu의 특정 pulsed Direct ToF 구성, 초음파 식은 Baumer의 왕복 음향시간 관계를 따른다. microsonic은 음향 echo 왕복시간 원리를 설명하며 Siemens/Milltronics와 Emerson/Rosemount는 ullage 음속 조건을 뒷받침한다. 다른 초음파 보상·설치 주장을 이 Pack으로 확장하지 않았다. `score_effect=none`. 근거: [Hamamatsu Direct ToF](https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html), [Baumer ultrasonic distance measurement](https://www.baumer.com/pl/en/service-support/function-principle/ultrasonic-sensors---function/a/Know-how_Function_Ultrasonic-sensors), [microsonic ultrasonic principle](https://www.microsonic.de/en/service/ultrasonic-sensors/principle), [Siemens/Milltronics HYDRO+ manual](https://support.industry.siemens.com/cs/attachments/18161433/7ML19981AC02.3.pdf), [Emerson/Rosemount 3100 manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf).
`optical_vs_ultrasonic_tof_comparison`은 반사형 Direct optical ToF의 `d=ct/(2n)`와 초음파 pulse-echo의 `d=c_s·t/2`를 분리해 적고, 기체 조성·온도·증기압 조건은 탱크 ullage 경로로 한정했다. 광학 식은 Hamamatsu의 특정 pulsed Direct ToF 구성, 초음파 식은 Baumer의 왕복 음향시간 관계를 따른다. microsonic은 음향 echo 왕복시간 원리를 설명하며 Siemens/Milltronics와 Emerson/Rosemount는 ullage 음속 조건을 뒷받침한다. 다른 초음파 보상·설치 주장을 이 Pack으로 확장하지 않았다. `score_effect=none`. 근거: [Hamamatsu Direct ToF](https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html), [Baumer ultrasonic distance measurement](https://www.baumer.com/pl/en/service-support/function-principle/ultrasonic-sensors---function/a/Know-how_Function_Ultrasonic-sensors), [microsonic ultrasonic principle](https://www.microsonic.de/en/service/ultrasonic-sensors/principle), [Siemens/Milltronics HYDRO+ manual](https://support.industry.siemens.com/cs/attachments/18161433/7ML19981AC02.3.pdf), [Emerson/Rosemount 3100 manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf).

`multipath_mixed_pixel_error`는 AMCW ToF range camera의 한 pixel에 direct/global multiple return path가 유입되면 depth 측정 오차가 생길 수 있다는 주장을 확인했다. Optical Engineering 논문은 multiple propagation path가 수신 pixel로 들어오는 측정오차와 direct/global return 분리를 설명하고, Optics Letters 논문은 broad illumination 투명체의 여러 scene point 반사가 하나의 pixel에 들어가 erroneous depth map을 만들 수 있다고 보고한다. 따라서 ToF range camera의 장면·센서 조건부 오차로 한정하며 보편 오차 방향이나 크기를 주장하지 않는다. `score_effect=none`. 근거: [Whyte et al., Optical Engineering 54(11), 113109 (2015)](https://researchcommons.waikato.ac.nz/entities/publication/5ac6413e-72b7-404e-bba3-2931bc9ea350), [Bhandari et al., Optics Letters 39(6), 1705–1708 (2014)](https://opg.optica.org/OL/abstract.cfm?uri=ol-39-6-1705).

`specular_transparent_surface_error`는 광택 반사와 투명 매질에 관한 일반론을 Mitsubishi MH11 및 ToF-camera 근거 범위로 한정했다. Mitsubishi MH11 manual은 diffuse/specular mounting mode와 대칭 송·수광 기하를 구분하고, 투명체의 front/rear 등 여러 measurement surface 및 reference 선택을 기술한다. Tanaka et al.은 투명체 굴절률로 인한 ToF-camera depth distortion을 다룬다. 따라서 한 장치의 설치·surface selection과 ToF camera의 굴절 왜곡을 구분하며 모든 광학 센서의 동일 오류를 주장하지 않는다. `score_effect=none`. 근거: [Mitsubishi Electric MH11 User’s Manual SH-081705ENG-C, §§1.6, 4.3, 7.1](https://dl.mitsubishielectric.com/dl/fa/document/manual/sensor/sh081705eng/sh081705engc.pdf), [Tanaka et al., CVPR 2016](https://openaccess.thecvf.com/content_cvpr_2016/html/Tanaka_Recovering_Transparent_Shape_CVPR_2016_paper.html).

`score_effect=none`이다. 근거: [Hamamatsu Photonics, Measuring distance with light,
Active triangulation Eqs. (3)–(4), Direct ToF Eqs. (6)–(7), timing/reflectance/occlusion discussion](https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html),
[JCGM VIM3 resolution 4.14](https://jcgm.bipm.org/vim/en/4.14.html), [repeatability 2.21](https://jcgm.bipm.org/vim/en/2.21.html), [accuracy 2.13](https://jcgm.bipm.org/vim/en/2.13.html), [NIST TN 1682, §1 and Fig. 1](https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote1682.pdf).

### 현재 Anchor 검증 상태 (2026-10-12 갱신)

현재 기준은 Topic Pack 원본의 canonical `topic_id` + `anchor_id`와 승인 Fact registry의
고유 `topic_id` + `legacy_anchor_id`를 직접 대조한 결과다. 배치 감사 문서의 과거
`확인`/`조건 확인` 표시는 근거 계약을 갖춘 독립 검증과 같지 않으므로 완료 수에 포함하지
않는다. 기술 사실이 아니라 Topic 소유범위만 연결하는 cross-topic boundary Anchor는
registry의 기술 사실 검증에서 분리하고 대상 Pack 존재·범위 테스트로 확인한다.
2026-10-12 현재 SW-08↔SW-07/SW-09 및 HEC↔HMI ownership boundary를 포함해 추가
47개를 검토했다. baseline 4건을 합친 구조 경계는 51개이며, source-topic/anchor 중복은
최종 인벤토리 계산에서 제거했다.
다른 handoff/boundary 표현은 기술 주장을 함께 포함할 수 있으므로 개별 근거 전까지
자동 분류하지 않는다.

| 상태 | 수 | 처리 |
|---|---:|---|
| 전체 canonical Anchor | 2,073 | 원본 Topic Pack에서 재산출 |
| registry의 고유 기술 Fact Anchor | 1,513 | 독립 근거·적용범위를 registry에 기록하고 `verified` |
| cross-topic ownership boundary | 51 | 기술 Fact가 아닌 참조계약; source/target Pack 구조 테스트로 확인 |
| Topic scope declaration | 18 | Pack 내부 내용 범위 선언; 포함 Anchor의 존재와 정합성 검사 |
| unresolved structural owner mapping | 1 | 구체적인 metrology/calibration owner Pack과 anchor를 찾지 못해 구조 분류 보류 |
| **미해결 기술 Fact Anchor** | **490** | 출처를 개별 확인했으나 주장 전체가 검증되지 않아 미승격 상태 |

등록부는 1,515개 record를 갖고, 현재 Anchor에 연결되는 record는 1,514개다. 고유
Topic–Anchor 매핑은 1,513개이며, 중복 연결 record 1건과 독립 fact record 1건은 고유 Anchor
수와 별도로 센다. 중복 record는 고유 검증 범위에 한 번만 센다. 과거 배치 문서의 canonical ID
불일치 참조는 현재 Anchor의 근거로 재사용하지 않는다. 나머지 handoff/boundary 표현은 기술 명제를
포함할 수 있으므로 자동 면제하지 않는다.
`eem_metrology_boundary`는 owner Pack이 특정되지 않아 기술 Fact나 verified 구조 경계로 승격하지 않았다.
현재 총계는 `1,513 verified Fact-to-Anchor mappings + 51 structural boundaries + 18 structural scope declarations + 1 unresolved structural mapping + 490 unresolved technical Facts = 2,073`이다. Registry 레코드는 1,515개이며, 중복 연결 1건과 독립 Fact 1건은 고유 Anchor coverage와 별도로 센다. 최근에는 IEEE 802.1Qbv·802.1AS·Qci 자료로 시간동기와 트래픽 스케줄링의 역할을 구분하고 Qbv의 guard band·schedule cycle·clock accuracy 설계 고려점을 score-neutral 검증했다. Industrial network Topic의 `sw08_latency_definition`은 IETF RFC 7928과 ITU-T Y.2617을 대조해 one-way network latency의 transmission/serialization, propagation, node/switch processing 및 queueing delay 구성과 경로별 합산을 확인했다. `sw08_cycle_time_definition`은 IEEE 802.1 작업그룹 use-case 자료와 Siemens PROFINET 문서로 application/network cycle, frame transfer interval, reduction ratio와 phase의 구분을 확인했다. IEEE 자료는 최종 규격이 아닌 설계 use-case 문서로 취급했으며 특정 cycle 수치나 관계를 모든 프로토콜에 일반화하지 않는다. `sw08_response_time_definition`은 Siemens S7-1500/SIRIUS ACT 자료로 입력 이벤트에서 출력 동작까지의 반응 경계와 process-image/user-program/network/I/O/actuator 지연 구성요소를 확인했다. 계산은 해당 구성과 실행 위상에 따르며 모든 시스템에서 단순한 고정합으로 가정하지 않는다. latency 역시 프로토콜·측정계층·measurement points에 따라 세부 구성요소가 달라 application response time이나 round-trip time과 혼동하지 않는다. Physical AI Topic에서는 디지털 트윈 fidelity의 목적 적합성·검증 범위, synthetic robotics data의 sim-to-real gap, robot localization의 map/coordinate-frame·uncertainty, 그리고 state estimator의 sensor placement·observability 한계를 동료심사·NIST·ROS 자료로 검증했다. Quantum Computing Topic에서는 NIST 근거로 entanglement의 비고전적 상관과 no-signaling 경계를, IBM Quantum 공식 문서로 measurement-to-classical result 경로 및 shot·precision·sampling error·후처리 비용을 end-to-end 평가에 포함해야 한다는 Anchor를 검증했다. 수치적 shot 수나 플랫폼별 성능은 일반화하지 않는다. Synthetic data와 localization 방법은 application에 따라 다르며 모든 배포에서 동일 구성을 강제한다는 뜻이 아니다. MRP의 ring manager/client 및 단일 장애 복구 관련 Anchor는 IEC 62439-2 공개 범위에 맞춰 2026-10-12 verified Fact로 승격했다. sw08_congestion_buffering은 RFC 7567의 queue arrival/egress 관계, queue-induced latency, full-queue loss 및 burst 기반 buffer sizing 권고로 기술 주장 범위에서 verified 등록했다. RFC는 일반 packet-network 지침이므로 산업 응용 deadline 보장은 실제 traffic profile과 경로를 사용한 별도 검증 조건으로 제한했다. 검증 범위는 정해진 MRP profile 및 명시된 장애 조건이며, 제품별 복구시간은 별도 확인 대상이다. 등록 Fact는 채점 점수에 영향을 주지 않는다.

### 제어밸브 표준 차단시험과 현장 누설의 예측 경계 (2026-10-11)

`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`의
`shop_test_field_service_boundary`는 표준/공장 차단시험 결과만으로 설치 후 운전 누설을 정확히
예측할 수 없다는 범위에서 score-neutral verified로 등록했다. Emerson/Fisher Sourcebook은 실제
누설 영향요인으로 pressure drop, temperature, sealing-surface condition 및 actuator force를
들고 표준시험조건과 service 조건이 다르면 정확한 예측이 불가하다고 명시한다. IEC 60534-4도
정의된 시험 유체·절차·누설 기준과 실제 설치 운전 누설 예측을 구분한다. 입자 오염은 모든
입자가 누설을 만든다는 의미가 아니라 seating surface 상태에 영향을 줄 수 있는 서비스 요인이고,
cycling 이력도 열화가 항상 일어난다는 주장이 아니라 고주기 시험에서 누설·마찰·성능을 따로
추적하는 설계별 고려사항으로 한정했다. 특정 밸브의 현장 누설량이나 보편적 열화율은 추정하지
않는다. 근거: [Emerson/Fisher Control Valve Sourcebook, §1, p. 1-9](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf),
[IEC 60534-4:2021, §4.3 and Table 1](https://webstore.iec.ch/en/publication/31136),
[Emerson Fisher Dirty Service Trim](https://www.emerson.com/en/final-control/products/fisher-dst),
[Fisher high-cycle control-valve brochure, pp. 6–8](https://www.emerson.com/is/content/emerson/fr/final-control/pressure-management/common-applications/psa/documents/brochure-fisher-control-valves-for-high-cycle-applications-en-124052.pdf).

같은 Topic의 `balanced_trim_additional_leakage_path`는 균형 플러그에서 압력이 plug의 상·하면에
작용해 정적 불균형력을 대부분 상쇄할 수 있는 한편, plug와 cage bore 사이의 별도 2차 유로가
존재하며 piston ring 또는 Bore Seal로 제한됨을 확인했다. 따라서 이를 주 seat leakage와 혼동하지
않고, 모든 balanced trim에 측정 가능한 누설이 있다는 뜻도 아닌 것으로 score-neutral verified
등록했다. 근거: [Emerson/Fisher Control Valve Handbook, §1, pp. 1-3–1-4](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf),
[Fisher EH/EHA Product Bulletin, p. 13](https://www.emerson.com/content/dam/emerson/en/final-control/flow-controls/bu-content/general/documents/D100042X012-Fisher-EH-and-EHA-Control-Valves-EN.pdf).

`soft_metal_seat_tradeoff`는 동일한 일반 서열이 아니라 설계별 선택 trade-off로 검증했다. Fisher 자료는
soft-seat construction의 별도 shutoff/material option과 PTFE 온도·anti-extrusion 설계 제한을 제시하며,
다른 Fisher 사례는 metal seat가 특정 scraper·erosive high-pressure-drop service 및 고온 seal 설계에
사용되는 예를 든다. IEC 60534-4 seat class acceptance는 material label만으로 결정되지 않고 지정된
시험조건·절차에 따른다. 따라서 재질 적합성, 압력·온도, 유체 및 표면상태를 실제 모델의 데이터시트와
보증조건으로 확인해야 하며 “soft는 항상 더 tight” 또는 “metal은 언제나 더 rugged”라고 일반화하지
않는다. 근거: [Fisher EW Product Bulletin D100023X012, Tables 20](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/product-bulletin-fisher-ew-series-ewd-ews-ewt-sliding-stem-control-valves-through-nps-12x8-en-122400.pdf),
[Fisher Control Valve Handbook, §§1 and 10B](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf),
[IEC 60534-4:2021](https://webstore.iec.ch/en/publication/31136). `score_effect=none`.

`ideal_gas_reference_conversion`은 재현 가능한 열역학 관계로 검증했다. 동일 몰 유량의 ideal gas는
`pV=nRT`에서 `Q_ref = Q_meas × (P_abs,meas/P_abs,ref) × (T_abs,ref/T_abs,meas)`를 얻는다.
따라서 압력은 absolute, 온도는 K 등 열역학적 절대온도로 넣고, 실제가스라면 압축성계수 보정 필요성을
검토해야 한다. 특정 표준 reference state나 시험 acceptance limit를 뜻하지 않는다. 근거: [NIST NBSIR 82-2401, Appendix A3.1.7](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nbsir82-2401.pdf). `score_effect=none`.

### MC/DC 정의·조건 결합 Anchor 검증 (2026-10-11)

`safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`의 열한 Anchor를
FAA DOT/FAA/AR-01/18의 MCDC 정의 및 결합조건 분석과 대조했다. Unique-Cause는 대상 조건만
변화시키는 independence pair로 정의하고, Masking은 다른 조건의 값이 바뀌어도 그 영향이
Boolean 구조상 가려짐을 보여야 한다. FAA 보고서의 표본 분석과 반복 조건 예시는 단순한
`n+1` Test Case 구성이 모든 decision에서 보장되지 않으며, 강결합 조건에서는 Unique-Cause
pair가 없을 수도 있음을 보여준다. 산업 표준에서 채택한 정확한 MCDC 변형과 도구별 규칙은
프로젝트의 승인된 기준을 따라야 한다. 열한 건 모두 `score_effect=none`으로 등록했다.
근거: [FAA DOT/FAA/AR-01/18, §§3.1–3.2, §§5.1, 6.1.2, 7.1](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/AR-01-18_MCDC.pdf), [FAA DOT/FAA/AR-06/54, §1](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/AR-06-54_VerificationTools.pdf), [FAA DOT/FAA/TC-15/57, structural coverage criteria](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/TC-15-57.pdf), [NASA SWE-189, §§3.2–3.3](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695524/SWE-189%2B-%2BCode%2BCoverage%2BMeasurements), [Hayhurst & Veerhusen, A Practical Approach to MC/DC, Introduction](https://ntrs.nasa.gov/api/citations/20040086014/downloads/20040086014.pdf).

`mcdc_one_hundred_percent_limit`을 NASA SWE-066·NPR 7150.2D 및 IEC 61511-1의 범위와
대조해 verified 등록했다. NASA는 100% code coverage만으로 코드 정확성, 요구사항 정확성 또는
모든 요구사항 시험이 보장되지 않는다고 명시한다. NASA 안전 핵심 소프트웨어 요구사항은 safe
state, 상태전이, 응답시간 등과 MC/DC coverage를 별도 항목으로 다루며, IEC 61511-1의 SIS
보증범위도 specification부터 operation·maintenance까지 포함한다. 따라서 100% MC/DC는 해당
구조 커버리지 증거이지, 요구사항 완전성·알고리즘·timing 안전성 또는 SIL 달성의 단독 증거가
아니다. `score_effect=none`이다. 근거: [NASA SWE-066, Code Coverage limitations](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604537/SWE-066%2B-%2BPerform%2BTesting),
[NASA NPR 7150.2D, Chapter 3 §§3.7.1–3.7.5](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7150_002D_&page_name=Chapter3),
[IEC 61511-1:2016+A1:2017](https://webstore.iec.ch/en/publication/61289).

### 환경·EMC Qualification Anchor 검증 (2026-10-11)

`instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`에서 12개 Anchor를 IEC, DLA, NASA 및 EU의 공개 문서와 대조해 verified로 등록했다. 확인 범위는 EMC와 EMI의 구분, emission과 immunity의 구분, EMC 시험군과 선택 책임, 시험구성의 방법별 기록, 사전 합격기준, 환경 온도 프로파일의 tailoring, EMC 측정 불확도, 측정장비의 방법별 교정·검증, edition·시험수준 적용, 표준화 시험과 현장 측정의 구분, 환경조건에 따른 vibration 시험방법 선택 및 condensation/비응축 damp-heat 조건의 구분이다. 모든 등록은 `source_refs=[]`, `score_effect=none`이다.

IEC 61000 기본 시험표준은 개별 ESD·radiated RF·EFT/burst·surge·conducted RF 시험방법을 분리해 정의하며, 제품위원회가 해당 방법의 적용 여부·수준·성능기준을 정한다고 명시한다. MIL-STD-810H는 보편적인 시험규격값을 부과하기보다 시스템 성능요구에 따른 환경 tailoring 절차라고 범위를 제한한다. IEC TR 61000-1-1은 표준화된 setup의 EMC 시험과 설치 현장에서 수행하는 in-situ measurement를 구분한다. NASA NESC-NPP-17-01은 시험 전에 accept/reject criteria를 설정하고 intended application을 왜곡하지 않는 fixture·환경인가, 적정 계측계획과 모니터링을 두도록 하는 예시 근거로만 사용했다. 이 aerospace 예시를 산업용 계측기 전체에 강제되는 규정으로 확대하지 않았다.

근거: [EU EMC Directive 2014/30/EU, Article 3](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014L0030), [IEC 61000-4-2:2025](https://webstore.iec.ch/en/publication/68954), [IEC 61000-4-3:2020](https://webstore.iec.ch/en/publication/59849), [IEC 61000-4-4:2012](https://webstore.iec.ch/en/publication/4222), [IEC 61000-4-5:2014+A1:2017](https://webstore.iec.ch/en/publication/61166), [IEC 61000-4-6:2023](https://webstore.iec.ch/en/publication/65586), [IEC 61000-4-8:2009](https://webstore.iec.ch/en/publication/4229), [IEC 61000-4-11:2020](https://webstore.iec.ch/en/publication/63503), [IEC 61000-6-8:2020](https://webstore.iec.ch/en/publication/62839), [IEC TS 61000-1-6:2026](https://webstore.iec.ch/en/publication/87113), [IEC TR 61000-1-1:2023](https://webstore.iec.ch/en/publication/70473), [IEC 60068-3-8 vibration method selection](https://webstore.iec.ch/en/publication/575), [IEC 60068-2-6 sinusoidal vibration](https://webstore.iec.ch/en/publication/544), [IEC 60068-2-64:2026 random vibration](https://webstore.iec.ch/en/publication/104354), [IEC 60068-2-78:2025 non-condensing damp heat](https://webstore.iec.ch/en/publication/82357), [IEC 60068-2-30:2025 cyclic damp heat](https://webstore.iec.ch/en/publication/82356), [DLA MIL-STD-810H Change 1](https://quicksearch.dla.mil/qsDocdetails.aspx?ident_number=35978), [NASA NESC-NPP-17-01, §5.2](https://ntrs.nasa.gov/api/citations/20170007186/downloads/20170007186.pdf). 상세 locator와 claim boundary는 registry에 보존했다.

2026-10-11 추가 검증: 같은 OT cybersecurity Pack에서 `sw09_ids_ips_monitoring`,
`sw09_vulnerability_management`, `sw09_detection_triage`, `sw09_containment_eradication`을
NIST SP 800-82 Rev. 3 §5.2.3.3, §6.3.2.1, §6.3.2.4, §6.3.3, §6.2.4.5에 따라 보완했다.
IDS/IPS는 감시·경보 지원 도구로, 취약점 스캔은 OT 영향 사전평가를 거치는 식별 방법으로,
탐지는 정상 OT 상태에 기초한 경보 해석으로, 격리는 공정 성능·안전 영향 평가 후 선택하는
대응 옵션으로 범위를 한정했다. 이 네 건은 registry에 `score_effect=none`으로 기록했다.

같은 날 `sw09_secure_remote_session`은 NIST §6.2.10의 고유 사용자명·기본 자격증명 변경,
불필요 권한 제거, 원격활동 모니터링, 운전원 통지, OT 시작 연결과 식별 가능한 해제수단으로
범위를 한정했다. 전체 화면기록, 동시 세션 제한, 유휴 timeout 등 해당 절에서 보편 요건으로
정하지 않은 내용을 삭제하고, 등록부에 비점수성 근거로 추가했다.
`sw09_legacy_compensating_control`도 NIST Appendix F.4의 동등/비교 보호, 위험과 기능 절충,
불가 사유·대체효과·잔여위험을 보안계획에 기록하는 요건으로 한정했다. 특정 통제를 보편적인
대체책으로 고정하지 않았다. `sw09_removable_media`는 NIST §6.2.7의 정책기반 제한, 라벨링,
보관·운송, sanitization·파기·폐기와 비인가 매체 금지로 한정했다. scanning station, hash,
quarantine, write protection은 이 절의 보편 필수사항으로 간주하지 않았다.
`sw09_secure_configuration_baseline`은 NIST §6.2.4.1–6.2.4.2의 승인 기준구성 문서화,
변경의 사전 문서화·시험·승인과 불필요 기능 비활성화 전 운전영향 시험으로 정리했다.
보편적 설정 스키마나 자동 drift 탐지 의무는 이 근거에서 주장하지 않았다.
`sw09_security_change_control`은 NIST §6.2.4.2와 CM-3의 생애주기 구성관리 및 조직 MOC 정렬로
한정하고, 별도 필드·특정 SW-06 워크플로우를 NIST의 직접 요구사항으로 보지 않았다.
`sw09_lifecycle_decommissioning`은 NIST §6.2.3의 폐기 전 중요 데이터·매체 wiping/sanitizing/파기
고려와 적용 자산 범위로 축소했다. 계정·인증서 등 모든 접근경로 제거 의무는 이 단락이 직접
뒷받침하지 않아 주장에서 제외했다.
`sw09_safety_coordination`은 NIST §4.2.2·§5.3.1에서 확인되는 risk-based separation과 보안통제가
안전시스템에 미치는 영향 평가로 축소했다. 모든 구조의 물리적 air gap이나 별도 안전승인 절차를
NIST의 보편 요구사항으로 단정하지 않았다.
`sw09_exercise_metrics`는 NIST §5.3.1의 tabletop 재해 시나리오 모의·복구계획 시험과
§6.4.5의 탐지·대응 교훈 반영으로 한정했다. 기존의 수치지표 정의 요구는 출처 근거가 없어
삭제하고, 보편 MTTD/containment-time 산식 또는 필수 지표 세트라고 주장하지 않도록 했다.
`sw09_jump_server`는 NISTIR 7966의 SSH 전용 접근관리 설명에 한정했다. 승인된 jump server는
필요한 제한적 trust/pivot의 예로 다루고 승인·문서화·키 기록과 권한 종료 시 키 교체를 포함했다.
OT 전 제품에 적용되는 hardening·malware·session 기능 목록이라고 확대하지 않았다.

2026-10-11 추가 검증: OT cybersecurity Pack의 `sw09_incident_response_plan`과
`sw09_business_continuity`는 NIST SP 800-82 Rev. 3 §3.3.8–3.3.9 문구에 맞춰 범위를
좁혔다. 전자는 NIST가 계획 구성요소로 열거한 역할·책임, workflow, incident type/severity,
내·외부 연락처, 정보공유와 통신으로 제한했다. 후자는 중대한 cyber disruption 대비 DRP/BCP와
재가동 전 인명·환경 안전 우선이라는 recovery objective로 제한했다. 법률 escalation, evidence
handling, 대체운전 방식 등 NIST 해당 절에서 직접 확인되지 않은 기존 세부요건은 이 Anchor의
검증 범위에 포함하지 않는다. 두 Fact 모두 `score_effect=none`이다.
근거: [NIST SP 800-82 Rev. 3, §§3.3.8–3.3.9](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

같은 Pack의 `sw09_criticality_classification`은 공정안전·복구시간·연결성·취약성·대체성 등을
모든 분석의 고정 필수요인처럼 나열하던 문구를 제거했다. NISTIR 8179의 정의대로 조직 목표에
대한 중요도와 부적절한 운영·손실의 영향으로 프로그램·시스템·구성요소를 우선화한다는 점을
검증했으며, NIST SP 800-82 Rev. 3 §6.1.4에서 이 모델을 OT 위험관리 참고자료로 인용하는 것도
대조했다. 보편 점수식이나 고정 요인 목록은 검증 범위에 넣지 않았다. `score_effect=none`이다.
근거: [NIST IR 8179](https://csrc.nist.gov/pubs/ir/8179/final),
[NIST SP 800-82 Rev. 3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

추가로 `sw09_trusted_recovery`는 사고 전 상태 복구, 관련 OT 상태·데이터·구성·프로그램의
정기 백업, 조직에 적절한 간격의 복구계획 시험으로 제한했다. `sw09_backup_recovery_security`는
위험기반 백업 대상·주기·복제본 수·위치·보존기간과 immutable read-only storage의 선택적
무결성 이점으로 한정했다. 분리 credential, encryption, malware 관리와 모든 사이트의 정기
restore test를 NIST가 이 근거에서 일률 요구한다고 해석하지 않는다. 두 Fact 모두
`score_effect=none`이다. 근거: [NIST SP 800-82 Rev. 3, §§3.3.9, 6.2.4.5, Appendix E](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

2026-10-11 추가 검증: OT 공급망 관련 Anchor 4개를 NIST SP 800-82 Rev. 3 §6.1.5 및
Appendix F SI-7(15) 범위로 다시 작성했다. 위험 유형·공급자 계약과 평가·대응/복구 계획,
공급자 출처·제품 authenticity 확인과 review, SBOM의 component/dependency 및 보고 취약점 영향
판단 지원, 자동 code authentication이 없는 경우의 수동 확인 예시만 남겼다. 이를 고정 계약조항,
SBOM의 제품 보안 보증, compatibility·rollback 보장으로 확대하지 않는다. 4개 모두
`score_effect=none`이다. 근거: [NIST SP 800-82 Rev. 3, §6.1.5 and Appendix F](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

같은 Pack의 identity/access Anchor 5개도 §§6.2.1, 6.2.1.1, 6.2.1.4.4 및 6.2.10에
대조했다. RBAC 기반 직무상 최소권한, identity·credential lifecycle, ACL/RBAC/ABAC 접근모델,
정당한 business need에 한정한 원격접속과 MFA의 OT별 적용 고려만 반영했다. 계정 잠금·정기
권한검토 주기·고정 원격접속 schema·모든 OT 계정 MFA 같은 보편 요건은 근거 범위에서 제외했다.
5개 모두 `score_effect=none`이다. 근거: [NIST SP 800-82 Rev. 3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

2026-10-11 추가 검증: Positioner Topic의 `hysteresis_deadband_stiction_topic3_handoff`는
IEC 62382:2024 Annex A.4의 control-stroke 예에 한해 증가·감소 방향 중간 travel 비교가
hysteresis 검출을 위한 것임을 확인했다. 이 비교만으로 deadband 또는 stiction 원인을
확정하지 않도록 Anchor를 좁혔으며, 보편적인 허용오차를 표준이 제시한다고 주장하지 않는다.
근거: [IEC 62382:2024, IEC Webstore](https://webstore.iec.ch/en/publication/67573),
Annex A.4 control-stroke example. `score_effect=none`이다.

같은 날 `seat_endpoint_overtravel_mechanical_stop`은 포괄적 체크리스트 표현을 장치별
근거로 교체했다. Baker Hughes Masoneilan SVI II ESD manual은 일부 밸브의 full stroke가
nominal travel보다 클 때 표시 100%를 nominal travel에 맞추는 STOP OP 절차를 제공한다.
Emerson Fisher DVC2000 manual은 Travel Cutoff Low가 seat load 확보에 쓰일 수 있고
해당 모델에서 0.5%를 권고한다고 명시한다. 0.5%를 다른 positioner·valve에 일반화하지
않으며, 이 근거는 기계적 stop 또는 positioner saturation에 관한 보편 규칙을 뜻하지 않는다.
근거: [Baker Hughes Masoneilan SVI II ESD manual, p. 97](https://dam.bakerhughes.com/m/6c0ae949e371774d/original/Masoneilan-SVI-II-ESD-Positioner-Manual-English.pdf),
[Emerson Fisher DVC2000 manual D103176X012, pp. 20–21](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103176x012.pdf).
`score_effect=none`이다.

같은 날 `operating_pressure_case_calibration_validity`의 원래 문구는 ΔP나 startup/shutdown만으로
positioner calibration이 무효가 된다고 읽힐 수 있어 철회하고 Fisher 3570 모델의 명시 조건으로
대체했다. 매뉴얼은 주문된 travel·input range·action과 현재 nameplate/운전조건의 대조를 요구하며,
운전조건 변경·분해/재조립·valve travel 불일치 시 adjustment를 검토하도록 한다. 이 근거는 모든
공정의 압력변화가 calibration 오류를 만든다는 일반 명제가 아니다. 근거: [Emerson Fisher 3570
Positioners Instruction Manual D200137X012, p. 11](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200137x012.pdf).
`score_effect=none`이다.

`maintenance_bypass_manual_operation_boundary`는 보편적인 handwheel·local-operation 복귀지시를 주장하지 않도록 Fisher 3570의 action-change 절차로 좁혔다. Fisher manual은 assembly 정지 전 임시 공정제어를 요구하며, action 변경 중 control valve bypass와 positioner input/supply 차단, 이후 운전 확인 및 action label 갱신을 안내한다. 다른 모델의 maintenance bypass 절차나 수동 핸드휠 restoration을 이 근거로 일반화하지 않는다. 근거: [Emerson Fisher 3570 Positioners Instruction Manual D200137X012, pp. 12–13](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200137x012.pdf). `score_effect=none`이다.

`vendor_action_cam_relay_setting_crosscheck`도 범용 설정 목록을 검증된 것처럼 두지 않고 Fisher 3570 사례로
재작성했다. D200137X012는 bias spring을 zero/start-point 조정, range spring을 input range에 대한 span/full-travel 조정,
relay-nozzle을 steady-state output-pressure 조정으로 정의하고, 주문 구성과 nameplate를 현재 조건에 대조하도록 한다.
이는 3570의 기구·조정 절차만 뒷받침하며 다른 제조사의 cam, I/P converter 또는 booster 설정을 뒷받침하지 않는다.
근거: [Emerson Fisher 3570 Positioners Instruction Manual D200137X012, pp. 10–11](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200137x012.pdf).
`score_effect=none`이다.

2026-10-11 추가 검증: Positioner Topic의 `booster_pressure_follower_boundary`는
Emerson/Fisher D103541X012 보충설명서 §Product/System Properties의 명시 사양에 따라
Fisher 2625·2625SST·2625NS 모델에 한정해 1:1 출력압력 추종과 설계 deadband를 기록했다.
과거의 일반 문구 “booster는 압력 증폭기가 아니다”는 다른 pressure-booster 설계에
과도하게 일반화될 수 있어 모델 한정 Anchor와 fatal 오답 계약으로 좁혔다. 새 Fact는
`score_effect=none`이며 근거는 [Emerson Fisher manual supplement D103541X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103541x012.pdf)이다.

같은 Topic의 `volume_tank_energy_storage_response_tradeoff`는 이상기체식과 고정 질량유량
가정을 명시해 저장량·충전시간의 용적 의존성을 계산으로 확인했다. `tubing_output_capacity_pressure_drop`는
Fisher VBL 설명서의 flow coefficient·배관/actuator port 용량 선정 지침으로 범위를 좁히고,
압력강하·stroke time의 실제값은 모델과 설치조건에서 산정하도록 했다. 두 Fact 모두
누설·부하·용량 의존성을 유지하고 고정 holding time, 보편 tube size 또는 보편 stroke time을
주장하지 않으며 `score_effect=none`이다. 근거: [Fisher VBL manual D103317X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103317x012.pdf).

같은 Topic의 multipoint·loop-check·failure-response Anchor 네 건은 IEC 62382:2024 Annex A.4와
§§5.2, 6.2.4에 맞춰 project별 조건을 포함하도록 수정했다. 표준은 control-stroke 예에서 full
stroke와 25·50·75% 중간점의 증가·감소 검사를 예시하고, actuator air/electrical-signal failure
simulation 및 loop 구성요소의 결합 기능 확인을 설명한다. 실제 시험점·acceptance criteria는 각
loop plan이 정하며 IEC 62382 loop check는 SIS validation을 대신하지 않는다. 근거: [ANSI/ISA-62382-2026 / IEC 62382:2024](https://www.isa.org/products/ansi-isa-62382-2026-iec-62382-2024-control-systems).

2026-10-11 추가 검증: `control_system_operations_maintenance_calibration_inspection_spares_kpi`의
`inspection_program_routine_functional_loop`은 routine condition inspection과 기능검증을
구분해 계획한다는 Fact를 확인했다. ISA/IEC 62382는 설치 후 cold commissioning 전 loop-check를
별도 검증활동으로 정의하고, OSHA PSM 지침은 적용대상 공정의 검사·시험, 계기·인터록 분류,
위험 우선순위와 검사주기 기준을 설명한다. NASA RCM Guide의 자동밸브 정비 절차도 작동확인과
외관·누설점검을 서로 다른 작업 단계로 기록한다. OSHA 규정 범위와 NASA 사례를 모든 산업의
일률 절차로 확대하지 않는다. Fact는 `score_effect=none`이다.

같은 Topic의 `kpi_pm_compliance_backlog_schedule`은 SMRP 공식 카탈로그의 MTBF, MTTR,
가용도, PM/PdM compliance, schedule compliance, planned/ready backlog와 reactive-work 지표,
그리고 DOE FEMP 가이드의 schedule-compliance 및 emergency-maintenance 분모 정의로 확인했다.
SMRP가 metric별 formula, component, qualification, target 및 caution을 제시하는 점을 반영해
시설별 목표와 분모·제외·데이터 규칙을 명시하도록 범위를 제한했다. 발행된 benchmark를 보편
목표로 취급하지 않는다. `score_effect=none`이다.

같은 Topic의 나머지 5개 Anchor(`spares_criticality_classification`,
`spares_stock_policy_reorder_leadtime`, `spares_preservation_shelf_life_rotation`,
`spares_obsolescence_substitution_moc`, `kpi_gaming_single_metric_tradeoff`)도 NASA·DOE·NIST 및
SMRP 자료에 대조했지만, 현재 문구의 모든 판단요소와 인과 예시를 한정 없이 뒷받침하지 않아
미승격으로 유지했다. Anchor별 직접 근거와 부족한 범위는
[예비품·KPI 후속 감사 노트](topic_anchor_evidence_followup_20261011_spares.md)에 기록했다.

2026-10-11 추가 검증: Noise Topic의 `pipe_transmission_loss_dependency`는 IEC 60534-8-3:2010의
주파수 의존 pipe-wall transmission-loss 모델(강·강합금 배관 적용 범위, pipe-wall 두께,
fluid density/sound-speed 변수)과 Emerson Control Valve Handbook의 pipe-wall 재질·크기·형상
및 frequency-dependent loss 설명으로 뒷받침해 score-neutral 등록했다. 같은 Topic의
`topic8_hydrodynamic_noise_handoff`는 Topic 8 target pack에 liquid-choked, cavitation/flashing,
FL anchor가 모두 존재하는 것을 확인해 구조 소유권 boundary로 분류했으며 기술 사실 검증과
분리했다. 이어 `diffuser_pressure_drop_distribution`도 Valmet Flow Control Manual과 Emerson/Fisher
inline-diffuser 자료로 범위를 확인해 score-neutral 등록했다. Pressure-drop split은 적절한
high/near-constant-drop case에 한정하고, governing flow에서 diffuser capacity·intermediate
pressure를 sizing하며, 구성요소별 noise와 service-dependent velocity/erosion을 검토하는
문구로 해석했다. `source_path_receiver_hierarchy`도 ASHRAE의 source–path–receiver 체계,
Valmet의 control-valve source/path 저감 구분, IEC 예측모델의 generated-noise→pipe-transmission→external-sound
연계를 대조해 score-neutral 등록했다. 중첩 저감효과를 서로 독립·가산으로 가정하지 않는 계산조건으로
한정했다. 현재 Noise Topic에는 기술 근거 대기 Anchor 4개가 남았으며, 범위를 충족하지 않는 항목은
미승격으로 둔다. 근거 상세:
[Noise prediction follow-up](topic_anchor_evidence_followup_20261011_noise_prediction.md),
[structural boundary review](structural_boundary_anchor_review_20261011.md).

2026-10-11 추가 검증: `control_valve_noise_scope`는 Noise 평가 프레임워크로 한정해 확인했다.
IEC 60534-8-1/8-2의 별도 실험실 측정 범위, IEC 60534-8-3/8-4의 구분된 예측 범위,
ISA75.07의 측정·예측·검증 위원회 범위, Valmet의 발생원/전달경로 저감 설명을 함께 사용했다.
이는 한 표준이 모든 현장에 고정 workflow를 요구하거나 모든 예측에서 현장 측정을 요구한다는
뜻이 아니다. 따라서 해당 Noise Topic의 추가 미검증 기술 Anchor는 8개다. 근거 상세는
[Noise prediction follow-up](topic_anchor_evidence_followup_20261011_noise_prediction.md)에 기록했다.

2026-10-11 추가 검증: `balanced_trim_unbalanced_trim_structure_sealing_applications`의
`dynamic_friction_topic3_handoff`는 sliding-stem valve packing friction의 범위를 Emerson/Fisher
Control Valve Handbook §2.1.1.4와 ISA/McMillan §1.5에 맞춰 좁혔다. Packing friction은 해당
구조의 주요 마찰원이자 deadband 원인이 될 수 있지만, 모든 hysteresis·stiction 증상을
단독으로 설명하지 않는다. `low_noise_trim_topic9_boundary`는 balanced trim의 정적
불평형력 저감과 multistage noise attenuation의 기능을 구분하되 같은 제품에 함께 적용될 수
있도록 정정했다(Fisher Catalog 14 및 Fisher TBX 제품자료). 두 Fact의 Topic 3/9 소유 표기는
저장소 내부 경계다. `severe_service_material_topic14_boundary`는 target Pack의 명시 Anchor를
확인해 기술 사실과 분리된 구조 경계로 분류했다. `control_valve_severe_service.../hardfacing_coating_ceramic`는
hardfacing·ceramic·hardened material의 포괄적 손상 한계 목록을 제거하고, Emerson의 특정
trim/service 사례와 제조사별 적용범위로 좁혀 verified 처리했다. 세 기술 Fact와 구조 경계는
점수 중립이며, 근거는 [Valve friction/noise follow-up](topic_anchor_evidence_followup_20261011_valve_friction_noise_materials.md)에 기록한다.

`dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`의 manifold isolation/return
순서는 Kuphaldt의 INST 240 학습문제에 나온 3-valve manifold + 별도 bleed 예시로 한정했다.
제조사 지침과 현장 절차는 다른 operating/zeroing 시퀀스를 다룰 수 있으므로 이를
universal sequence로 승인하지 않았고, Pack 문구도 해당 교재 예시임을 명시한다.
근거: [INST 240, Section 2, Q9 pp. 24–25 and Q63 pp. 74–75](https://www.ibiblio.org/kuphaldt/socratic/src/output/INST240_sec2.pdf).

추가 검증: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation/calibration_reference_traceability`의 기존 문구는 광학 비접촉 센서 전체에 주기점검 항목과 drift 원인을 일반화하고 있었다. 이를 레이저 삼각측량의 모델별 보정·표적·설치 조건으로 좁혔다. Micro-Epsilon 자료는 표면 거칠기, 센서 기울기, 측정 중 온도변화 등이 해당 보정자료와 편차를 만들 수 있다고 명시하고, OMRON ZP manual은 선형도 사양이 표준 백색 확산 표적 기준이며 실제 대상에 따라 달라질 수 있다고 밝힌다. NIST는 일률적인 재교정 간격을 정하지 않고 요구 정확도, 기기 안정성, 환경 및 외부 요구에 따라 주기를 설정하도록 안내한다. 렌즈 오염·기구변형의 보편적 영향이나 광학 센서 공통 고정 주기는 주장에서 제외했다. `score_effect=none`. 근거: [Micro-Epsilon T017](https://www.micro-epsilon.com/fileadmin/download/products/T017--en--Calibration-ILD2300.pdf), [OMRON ZP Series Manual Z495](https://files.omron.eu/downloads/latest/manual/en/z495_zp_series_-_laser_displacement_sensor_users_manual_en.pdf), [NIST Recommended Calibration Interval](https://www.nist.gov/calibrations/recommended-calibration-interval).

추가 검증: 같은 Pack의 `detector_saturation_dynamic_range`는 “noise floor”, 보편적인 SNR 기준, 모든 센서에 공통인 광원·이득·노출 조정 처방을 제거했다. Mitsubishi MH11 매뉴얼은 특정 sampling cycle에서 수광량 부족 또는 정반사 포화를 각각 보고하고 해당 모델의 sampling·방출량 조정이나 ND filter를 안내한다. ToF 카메라 연구는 수광 진폭 및 integration time과 깊이 노이즈의 관계, 측정범위 끝단의 포화 문제를 실험한다. 따라서 저수광량과 포화가 신뢰도 한계가 될 수 있다는 점만 확인하고, 조정은 모델·표적·측정조건에 따르도록 범위를 한정했다. `score_effect=none`. 근거: [Mitsubishi MH11 Manual, §§4.3, 7.1](https://dl.mitsubishielectric.com/dl/fa/document/manual/sensor/sh081705eng/sh081705engc.pdf), [Belhedi et al., IET Computer Vision (2015)](https://doi.org/10.1049/iet-cvi.2014.0135), [Statistical analysis of signal measurement in time-of-flight cameras](https://www.sciencedirect.com/science/article/pii/S0924271611000724).

추가 검증: 같은 Pack의 `wavelength_material_selection`에서 모든 광학 측정의 파장 선택요건으로 넓게 적은 주변광·레이저 안전 요소를 제거하고 광전식 센서의 파장·표적 응답에 한정했다. OMRON은 대상의 반사·흡수가 조사 파장과 대상 색상에 따라 달라진다고 설명하며, Banner는 red/blue/IR/1450 nm sensor beam에 대해 각기 다른 특성과 응용 예를 든다. 이는 단일 파장의 보편적 우위를 뒷받침하지 않고, 개별 sensor family 및 대상에 따른 선택이 필요함을 보여준다. `score_effect=none`. 근거: [OMRON Overview of Photoelectric Sensors](https://www.ia.omron.com/support/guide/43/introduction.html), [Banner Engineering Photoelectric Sensors—Sensing Beams](https://www.bannerengineering.com/us/en/products/sensors/photoelectric-sensors.html).

추가 검증: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance/deadband_not_dead_time`은 deadband를 방향 반전 뒤 관측 출력이 움직이지 않는 입력 신호 범위로, dead time을 step 입력부터 첫 관측 응답까지의 시간으로 고정해 구분했다. Emerson/Fisher Control Valve Handbook은 deadband 정의에서 입력·출력 변수를 명시하도록 하고, 별도 장에서 dead time과 이후의 dynamic time을 나눠 정의한다. 따라서 본 Anchor는 두 측정량의 구분만 주장하고 원인을 단일화하지 않는다. `score_effect=none`. 근거: [Fisher Control Valve Handbook, Chapter 1](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [Fisher Control Valve Handbook, Chapter 2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf).

추가 검증: 같은 Pack의 `stiction_stick_then_jump`는 정지마찰이 상대운동 시작 전에 극복되어야 한다는 Emerson 정의와, 구동력이 저항을 넘으면 밸브가 새 위치로 급이동할 수 있다는 AIChE의 밸브 운전 설명을 결합했다. 증상만으로 원인을 단정하지 않도록 밸브·positioner·actuator 구성 의존 조건을 명시했다. `score_effect=none`. 근거: [Fisher Control Valve Handbook, Chapter 1](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [AIChE, Empirical Process Control: Part 1](https://publications.aiche.org/cep/2021/june/empirical-process-control-part-1).

추가 검증: 같은 Pack의 `stick_slip_repeated_motion`은 “반복되는 정지·급이동”이라는 용어를 stiction의 stationary/stick phase 및 slip-jump travel 국면으로 구체화했다. 두 동료심사 논문은 정지마찰을 넘은 뒤 급격한 travel 변화가 나타날 수 있고, 특정 폐루프·시험 조건에서 limit-cycle 응답으로 이어질 수 있음을 다룬다. Anchor는 valve travel 형태만 서술하며 단일 jump로 반복주기나 PV 진동을 추론하지 않는다. `score_effect=none`. 근거: [Processes 11(7), 1913 (2023)](https://www.mdpi.com/2227-9717/11/7/1913), [Control Engineering Practice 148 (2024), 105953](https://doi.org/10.1016/j.conengprac.2024.105953).

추가 검증: `instrumentation_power_grounding_shielding_ups_ground_loop_emc/ipgse_measurement_reference_safety`는 접지·공통모드 진단 전에 신호원/계측기 기준점과 입력 공통모드 한계를 확인하고, grounded source의 부적합한 ground-referenced 연결이 ground-loop 전류 또는 source 단락을 만들 수 있다는 NI 설명으로 한정했다. 위험 전기 환경에서는 meter와 probe/lead 양쪽의 CAT 및 전압 정격이 환경에 맞아야 한다는 Fluke 안전 체크리스트도 반영했다. 차동/비참조 연결은 해당 DAQ 적용사례의 권고이지 모든 측정에 대한 보편 지침으로 표현하지 않았고, 보호접지 해제는 정당화하지 않았다. `score_effect=none`. 근거: [NI Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [Fluke Test Tool Selection Safety Checklist](https://media.fluke.com/26017a07-f3af-49c9-9a95-b1060068a09d_original%20file.pdf).

추가 검증: 같은 Pack의 `ipgse_bonding_impedance_frequency`는 고주파 본딩의 임피던스·접속형상 주장을 보편 치수나 보호접지 규칙으로 확대하지 않도록 수정했다. Schneider Electric의 EMC guide는 병렬 등전위 도체가 해당 구성에서 common-mode impedance와 loop area를 줄일 수 있고, 고주파에서는 짧고 평평한 본딩형상이 유리할 수 있음을 설명한다. TDK의 filter installation guidance도 특정 converter/filter 환경에서 저인덕턴스·넓은 접촉면·짧은 연결을 권고한다. 따라서 구체 치수·형태는 주파수, 설치 및 보호요건에 따라 설계하도록 했다. `score_effect=none`. 근거: [Schneider Electric Electrical Installation Guide](https://www.electrical-installation.org/enwiki/EMC_implementation_-_Improving_equipotential_conditions), [TDK EMC Filters Technical Information](https://www.tdk-electronics.tdk.com/download/528632/7f30b0110a521bb506ace36f0c56af5c/pdf-technical-information.pdf).

같은 Pack의 `ipgse_scope_chain`은 광범위한 “전원·접지·UPS·EMC 전 항목을 하나의 원인사슬로 진단”한다는 표현을 줄였다. Siemens EMC reference manual은 source-to-victim 결합경로 모델을, NI는 실제 측정 setup·주파수 특성과 가능한 전원·접지·배선 요인을 살펴볼 진단 절차를 뒷받침한다. 따라서 source/path/victim은 원인 후보를 나누는 진단 모델로 한정하며, 전원·접지·차폐 항목은 측정으로 확인할 후보일 뿐 원인 단정으로 취급하지 않는다. `score_effect=none`. 근거: [Siemens EMC Reference Manual, §4.4](https://cache.industry.siemens.com/dl/files/796/109739796/att_889889/v1/practice_of_emc_directive_2014_30_EU_en-US.pdf?download=true), [NI Diagnosing & Reducing Measurement Noise](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html).

같은 Pack의 `ipgse_diagnostic_workflow`는 고정된 현장 절차처럼 보이던 순서를 DAQ 잡음 진단으로 좁혔다. NI는 FFT/주파수 특징과 물리적 setup 조사를 초기 단계로 제시하며, 장비 단독 baseline 및 구성요소를 하나씩 분리하는 방법으로 원인을 분리할 수 있다고 설명한다. 이는 해당 DAQ 진단의 방법이며 플랜트 회로를 임의 분리하거나 PE를 해제해도 된다는 뜻은 아니다. 수정 후 원래 적용조건과 장비 사양에 대조 확인한다. `score_effect=none`. 근거: [NI Diagnosing & Reducing Measurement Noise](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html).

`ipgse_evidence_before_rewire`는 모든 항목을 공식 필수 기록형식처럼 요구하던 주장을 축소했다. NI의 FFT·기준측정·setup 점검과 Fluke의 equipment/event timestamp 비교를 근거로, 측정 기준과 운전상태가 비교 가능하도록 baseline/follow-up evidence를 보존하는 현장 권고로 정리했다. 이 방법은 formal record mandate가 아니며 event correlation은 인과 증명이 아니고 보호접지 해제의 근거가 될 수 없다. `score_effect=none`. 근거: [NI Diagnosing & Reducing Measurement Noise](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html), [Fluke power-quality troubleshooting](https://www.fluke.com/en-gb/learn/blog/power-quality/a-fresh-look-at-power-quality-basics).

`ipgse_final_verification`의 기존 문구에서 UPS transfer 및 주요 noise-source 조작을 일률적 시험처럼 보이게 하는 표현은 좁혔다. NI의 DAQ baseline·장비 사양 비교를 바탕으로, 적용에 적절하고 안전한 상태에서 신호를 재확인하는 권고로 한정했고, transfer/source-switching 시험은 설비 설계와 승인된 안전 절차가 허용할 때만 실시하도록 했다. 이는 보편적 acceptance requirement를 주장하지 않는다. `score_effect=none`. 근거: [NI Diagnosing & Reducing Measurement Noise](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html).

`pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative/pid_line_list_spec_relation`은 모든 프로젝트에 동일한 Line List와 문서위계가 있다는 식의 주장을 피하도록 범위를 명시했다. Autodesk Plant 3D 공식 문서는 P&ID Line List에서 line segment, 연결 component·nozzle·equipment를 표시하고 속성 불일치를 보일 수 있으며, 별도의 line/nozzle reports와 선택 piping spec 기준의 in-spec/off-spec 확인을 제공한다. 이는 해당 기능의 예시이지 보편적 프로젝트 문서 요구나 우선순위 규정이 아니다. `score_effect=none`. 근거: [Autodesk P&ID Line List](https://help.autodesk.com/cloudhelp/2027/ENU/Plant3D-UserGuide/files/GUID-0C1DF078-D00F-4AA1-899F-6FB26132D9FF.htm), [Autodesk Data Manager Reports](https://help.autodesk.com/cloudhelp/2022/ENU/Plant3D-UserGuide/files/GUID-8B0EFA0A-7E50-42C1-BED5-C5D699CB4F2C.htm), [Autodesk Spec-Driven P&IDs](https://help.autodesk.com/cloudhelp/2022/ENU/Plant3D-UserGuide/files/GUID-44E99CF5-2C39-4391-B475-92CBB710576A.htm).

`instrumentation_production_management_planning_quality_cost_resources/production_energy_consumables_cost`의 “에너지·Utility·소모품 및 peak/idle loss를 함께 관리”하던 복합 주장은 직접 근거가 확보된 에너지성과 지표 부분으로 좁혔다. ISO 50006은 EnPI/기준선 관리 지침을 정하고, DOE는 산업 에너지 사용에서 생산량 등 relevant variables와 제품 mix 변화가 단위생산당 에너지 지표의 해석에 미치는 영향을 설명한다. 단위 에너지 지표를 사용할 수 있으나 조건이 바뀌면 필요에 따라 정규화하며, 소모품·peak·idle loss를 필수 지표라고 주장하지 않는다. `score_effect=none`. 근거: [ISO 50006:2023](https://www.iso.org/standard/79367.html), [U.S. DOE AMO eGuide, relevant variables](https://www1.eere.energy.gov/manufacturing/eguide/iso_step_2_5.html), [U.S. DOE Energy Intensity Methodology](https://www.energy.gov/cmei/energy-intensity-indicators-methodology-caveats-and-cautions).

같은 Pack의 `production_schedule_adherence_delivery_kpi`를 KPI명만 나열한 일반 규칙에서 재현 가능한 KPI 정의 요건으로 좁혔다. ISO 22400-2 KPI 서술은 formula·구성요소·time behaviour·단위 등을 포함하고, SAP의 schedule attainment 예는 schedule period와 freeze 시점의 planned work를 비교기준으로 사용한다. 지연원인 분류와 metric 공식은 조직/구현에 따라 달라지므로 보편 taxonomy나 서로 다른 KPI의 동일성을 주장하지 않는다. `score_effect=none`. 근거: [ISO 22400-2:2014](https://www.iso.org/obp/ui/?_escaped_fragment_=iso%253Astd%253A54497%253Aen), [SAP Key Information for Tracking Schedule Execution](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/8308e6d301d54584a33cd04a9861bc52/9a3262c243ef4c649eaeed4e63bf510f.html).

같은 Pack의 `production_management_objective_scope`는 고객요구·안전·품질·납기·원가 전부를 고정적으로 우선해야 하는 보편 정의처럼 읽히지 않도록 정리했다. ISO 22400-2에 나오는 MOM 영역·운영활동, KPI 기술요소, 회사별 threshold와 조치라는 확인 가능한 부분을 Fact로 삼고, 적용 목표의 선택과 우선순위는 조직·제품·규제 맥락에 맡겼다. `score_effect=none`. 근거: [ISO 22400-2:2014](https://www.iso.org/obp/ui/?_escaped_fragment_=iso%253Astd%253A54497%253Aen), 특히 Introduction 및 §1.

2026-10-11 추가: 레이더/GWR pack의 두 미검증 Anchor를 source-matched claim으로 좁혀 검증했다. `radar_upper_null_zone_overfill_coordination`은 Rosemount 5408의 model-specific Upper Null Zone 동작과 API 2350 Category 3의 적용범위를 구분했고, `gwr_quasi_tem_return_path`는 보편 quasi-TEM 주장을 제거하고 Magnetrol Model 706 single-rod/nozzle 반사 사례로 교체했다. 따라서 해당 pack은 28/28 Anchor가 registry에 연결되어 있다. 과거 본문에 남아 있는 26/28 및 두 Anchor 보류 문구는 이 최신 판정으로 supersede된다. 상세 근거: [Radar/GWR evidence follow-up](topic_anchor_evidence_followup_20261011_radar.md).

추가 승격: `control_valve_sizing_cv_kv_reynolds_liquid_selection/cv_reference_definition_us_units`는 Baker Hughes Masoneilan Control Valve Sizing Handbook의 “Flow Coefficient CV” 절(인쇄 p. 3, PDF p. 2)에서 Cv를 60°F 물의 US gpm, 1 psi 차압 기준으로 명시함을 확인해 registry에 등록했다. 이는 reference definition이며 실제 운전 유량이나 완전한 밸브 사이징 절차를 뜻하지 않는다. 같은 Pack의 `required_coefficient_inverse_pressure_root`는 handbook의 완전 난류·비기화 액체 기본식 `Cv = q·√(Gf/ΔP)`를 확인했다. 관계는 유량·비중과 보정인자를 고정한 경우에만 적용하며, 기화·초크·비난류 흐름이나 가변 보정인자를 일반화하지 않는다. 두 Fact는 `score_effect=none`이다. 근거: [Baker Hughes, Masoneilan Control Valve Sizing Handbook](https://dam.bakerhughes.com/m/47616eb160214a1d/original/Masoneilan-Valve-Sizing-Rules-Tech-Spec-English.pdf), “Flow Coefficient CV” 인쇄 p. 3 및 “Liquid Flow Equations” 인쇄 p. 7·“CV” 식 인쇄 p. 11.

추가 승격: 같은 Pack의 `sizing_pressure_drop_definition`은 handbook의 “Pressure Drop Across the Valve” 절(인쇄 p. 4)에서 실제 밸브 차압이 시스템 특성과 목표 유량으로 결정됨을 확인해 총 가용차압과 구별했다. 앞서 등록한 두 Cv Fact와 함께 세 항목 모두 `score_effect=none`이다.

### 추가 검증 기록 (2026-10-11)

`control_valve_types_globe_rotary_body_actuator_selection/port_guided_plug_alignment`는 기존의 가이드 간극·오염·마모 인과가 확보한 근거보다 넓어 해당 주장을 제거했다. Emerson/Fisher Control Valve Handbook 6판 Chapter 3 §3.1.1.2 및 Table 3.1은 plug가 valve body port에 의해 정렬되는 정의와 post/port-guided body의 고차압 진동 가능성 및 설계상 주의를 뒷받침한다. 이를 제품·운전조건에 따른 가능성으로 한정해 registry에 등록했다. `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Handbook, 6th ed.](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf).

같은 Final Element 팩에서 조건부였던 6개 Anchor를 더 좁혀 확인했다. `full_stroke_proof_test_scope`는 “모든 component/기능을 full stroke가 증명한다”는 식의 범위를 제거하고, expected-trip condition 시험·적절한 주기의 end-to-end test·SIF별 절차로 한정했다. `impairment_alarm_and_permit`은 유지보수 bypass 시의 동등 안전수준과 임시 방벽/작업허가 예시로, `shared_air_power_environment`는 공유 utility·환경·정비절차/인력이 독립성 및 CCF 평가에 미치는 영향으로 범위를 좁혔다. `diagnostic_credit_validation`에서 보편적 SIL credit을 제거하고 HSE가 열거한 actuator monitoring 신호의 제한적 검출능력으로 바꿨다. `maintenance_moc_spares`는 HSE의 변경 통제·기능/무결성 확인 및 불량 spare 격리·유사 부품 오교환 방지로, `lifecycle_closed_loop_reverification`은 고진단 시스템의 수리성능을 설계기준과 비교·검토하는 요구로 정정했다. 여섯 Fact 모두 `score_effect=none`이다. 근거: [HSE Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [HSE HSG238](https://www.hse.gov.uk/pubns/priced/hsg238.pdf).

`final_control_element_sil_sis_esd_valve_partial_stroke_test`에서는 14개 고유 Anchor를 HSE COMAH 지침, HSE SIS proof-testing guidance와 functional-safety guidance에 대조했다. Final Element/SIF 범위, process-dependent safe action, de-energize-to-trip의 적용 조건, utility/shared dependency, PST와 full-stroke proof-test의 경계, 시험 간격·수리시간·절차, bypass/restoration, 진단·변경·수명주기 재검증을 등록했다. “모든 failure mode/seat leakage/full isolation을 PST가 검증한다”, “PST가 전체 Proof Test를 대체한다”, “복구는 보편적으로 독립 확인해야 한다”는 식의 강한 주장은 출처 범위가 뒷받침하지 않아 제거하거나 보류했다. 14개 Fact 모두 `score_effect=none`이다. 근거: [HSE Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [HSE SIS Proof Testing Appendix 1](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf), [HSE Functional safety](https://www.hse.gov.uk/eci/functional.htm).

같은 SIS/SIL 검토에서 `independence_purpose`는 프로젝트팀과 독립된 인원이 증거를 근거로 기능안전 달성 여부를 판단하는 FSA 정의로 한정했다. `bidirectional_traceability`는 NIOSH safety-file이 기술하는 위험분석→요구사항→할당→설계→Verification의 lifecycle 추적성으로 좁혀 양방향 요구를 제거했다. `modification_revalidation`은 HSE가 명시하는 변경관리, 안전기능·무결성 유지 확인, 유능한 인원의 설계·구현으로 좁혔다. 세 Fact는 모두 `score_effect=none`이다. 근거: [HSE HSG238](https://www.hse.gov.uk/pubns/priced/hsg238.pdf), [HSE Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [NIOSH, Independent Functional Safety Assessment Guidance](https://www.cdc.gov/niosh/docs/mining/UserFiles/works/pdfs/2006-131.pdf).

SIS/SIL Pack에는 현재 21개 고유 verified Fact가 있다. 이번 보강에서는 `srs_functional_integrity_requirements`, `application_program_role`, `functional_test_boundary`, `bypass_override_controls`, `independence_purpose`, `bidirectional_traceability`, `modification_revalidation`을 HSE, NIOSH, Rockwell 공식 안전자료와 대조해 추가·정교화했다. 앞서 검증한 SIF/SIL 관계, 위험에서 SRS로의 할당, systematic/random failure 구분, Verification/Validation, proof-test 경계, shared resource/common-cause와 PFD/PFH 모드 경계도 포함한다. 21개 Fact는 모두 `score_effect=none`이다. 근거: [HSE, Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [HSE, HSG238](https://www.hse.gov.uk/pubns/priced/hsg238.pdf), [NIOSH, Independent Functional Safety Assessment Guidance](https://www.cdc.gov/niosh/docs/mining/UserFiles/works/pdfs/2006-131.pdf), [Rockwell Automation, Logix SIS Safety Reference Manual](https://www.rockwellautomation.com/en-us/docs/technical/logix5000/_online/1756-rm015/logix-sis-safety-reference-manual-ditamap/safety-applications/commissioning-lifecycle/specification-of-the-safety-function.html).

추가 SIS/SIL 검증에서는 `srs_functional_integrity_requirements`의 “명확하고 검증 가능” 표현을 근거가 직접 지지하는 범위로 좁혔다. HSE HSG238은 safety-function과 safety-integrity 요구를 구분해 명세하며, 상세한 명세가 설계자의 해석과 오류 가능성을 줄인다고 설명한다. `application_program_role`은 Rockwell 공식 Logix SIS 문서에 따라 안전 프로그램 로직이 application-specific safety-function specification을 올바르고 완전하게 구현하는지 검증하는 범위로 명시했다. `functional_test_boundary`는 일반 기능시험에 대한 과잉 일반화를 제거하고 HSE가 구분하는 control-system validation/FAT와 overall safety validation의 관계로 정정했다. `bypass_override_controls`에서 보편적 시간제한 및 독립 복구검증 주장은 삭제했다. 근거가 확인된 override 권한·보안·기록·감시·검토·reset, 불가피한 유지보수 bypass의 동등 안전수준, 복구 후 시험만 남겼다. 네 Fact는 모두 `score_effect=none`이다. 근거: [HSE HSG238](https://www.hse.gov.uk/pubns/priced/hsg238.pdf), [HSE Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [Rockwell Logix SIS safety function specification](https://www.rockwellautomation.com/en-us/docs/technical/logix5000/_online/1756-rm015/logix-sis-safety-reference-manual-ditamap/safety-applications/commissioning-lifecycle/specification-of-the-safety-function.html).

제어밸브 사이징 Pack에서 `basic_nonchoked_liquid_flow_relation` 및 `basic_equation_applicability_boundary`도 같은 Baker Hughes handbook으로 검증했다. 기본식은 완전 난류·비기화 액체 흐름에 한정되며, 고정된 비중·유량·배관/레이놀즈 보정 조건에서만 유량과 Cv·압력강하 관계를 적용한다. 핸드북은 초크·2상·비뉴턴 유체 및 캐비테이션/플래싱을 별도 처리 또는 일반식 적용 제외로 구분한다. 두 Fact는 `score_effect=none`이다.

`extension_bonnet_temperature_isolation`은 Fisher Control Valve Handbook §6.4와 cryogenic EZ-C/ET-C/EWT-C 설치 매뉴얼을 대조해 verified 등록했다. 핸드북은 cryogenic condensation/frost가 packing 손상을 일으킬 수 있어 extension bonnet이 packing box를 ambient로 따뜻하게 하고, 연장 길이가 적용 온도·단열 조건에 좌우된다고 설명한다. 해당 제품 매뉴얼은 장착 각도가 bonnet 내부 액체를 packing에 접촉시키지 않도록 해야 한다고 경고하되, 제품에 대해 별도 제약이 없으면 여러 방향 설치가 가능하다고 구분한다. 따라서 방향을 보편 각도로 고정하지 않고 제품·서비스별 기준으로 한정했다. `score_effect=none`이다. 근거: [Fisher Control Valve Handbook, Chapter 6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [Fisher Cryogenic Control Valve Instruction Manual D102175X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d102175x012.pdf), [Fisher easy-e Cryogenic Control Valve](https://www.emerson.com/en/final-control/products/fisher-cryogenic).

`control_valve_types_globe_rotary_body_actuator_selection`의 `eccentric_plug_noncontact_rotation`은 Fisher V500 제품자료, Emerson의 eccentric plug 기술 개요 및 제품 bulletin으로 대조해 verified 등록했다. 자료는 해당 V500에서 eccentric path가 개방 중 seat 접촉을 줄여 wear와 friction을 감소시키며, 제품이 erosive·coking 등 어려운 service를 대상으로 trim 재질과 유로 구성을 적용에 맞춰 선택함을 설명한다. 이 근거를 모든 eccentric-plug 제품이나 모든 오염·침식 유체에 확대하지 않는다. `score_effect=none`이다. 근거: [Fisher V500, Emerson](https://www.emerson.com/en/final-control/products/fisher-v500), [Emerson Eccentric Plug Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/eccentric-plug-valves), [Fisher V500 Product Bulletin D100054X012](https://www.documentation.emersonprocess.com/intradoc-cgi/groups/public/documents/bulletins/d100054x012.pdf).

`body_actuator_selection_multi_criteria`는 Emerson/Fisher Control Valve Handbook의 valve selection sequence, actuator sizing 절차 및 selection guidance와 NIST life-cycle-cost 지침을 대조해 verified 등록했다. 문서는 공정조건·용량·noise/cavitation·body/trim/material/shutoff 옵션, force/torque·fail action·공급원, response characteristics, 공간/치수 및 구매·운전·유지관리·폐기 비용을 고려하는 근거를 제공한다. 항목의 적용 여부와 중요도는 service/project에 따라 달라지므로 고정된 universal weighting이나 언제나 최적인 단일 조합을 주장하지 않는다. `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 5](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher Catalog 14](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf), [Fisher Actuator Selection Guidance](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf), [NIST Handbook 135](https://nvlpubs.nist.gov/nistpubs/hb/2022/NIST.HB.135e2022-upd1.pdf).

`humidity_lifecycle_maintainability_selection`은 Vaisala의 humidity/dew-point selection guidance와 HMD60U/Y 제품 매뉴얼, NIST life-cycle-cost 지침을 대조해 verified 등록했다. 제조사는 측정범위, 온도/압력, 응축 회복, 오염, 위험장소 인증, 설치·교정, maintenance/shutdown 조건을 application-specific 요구로 열거하고, HMD60 매뉴얼은 filter/sensor 교체·calibration·spare part와 4–20 mA 출력을 명시한다. 전기 출력은 실제 PLC/DCS 입력과 매칭해야 하고 life-cycle cost는 프로젝트별 비교요소다. 이는 모든 센서에 동일한 점검주기나 보편 가중치를 부여하지 않는다. `score_effect=none`이다. 근거: [Vaisala humidity/dew-point instrument selection](https://www.vaisala.com/en/expert-article/how-to-choose-the-right-instrument-for-measuring-humidity-and-dew-point), [Vaisala HMD60U/Y Operating Manual](https://www.vaisala.com/sites/default/files/documents/HMD60%20Operating%20Manual%20Multilingual%20M210276EN.pdf), [NIST Handbook 135](https://nvlpubs.nist.gov/nistpubs/hb/2022/NIST.HB.135e2022-upd1.pdf).

`rubrics/topic_packs`의 86개 Pack, 2,073개 Anchor를 비공개 WordPress source DB와
Master source reference에 대조했다. 재실행 명령은 다음과 같다.

```bash
python3 scripts/audit_all_topic_fact_sources.py --database /path/to/private/wordpress_sources.sqlite3
```

대상 DB는 read-only로 열며 보고서에는 Topic ID와 개수만 저장한다. 문장 원문,
추출 본문, 개인 답안, DB 경로는 보고서에 넣지 않는다. anchor statement의 단어가
현재 버전의 first-party 추출 본문에 포함되는 비율은 검토 우선순위 신호다. 의미가
맞다는 보증이나 자동 승인 기준으로 쓰지 않는다.

| 결과 | Anchor 수 |
|---|---:|
| first-party 추출 본문이 연결된 source에서 80% 이상 단어 신호 | 31 |
| 같은 조건에서 50–79% 신호 | 338 |
| 같은 조건에서 50% 미만 신호 | 804 |
| first-party 추출 본문 없음 | 900 |
| 합계 | 2,073 |

Master의 WordPress source reference 397건은 해당 출처 DB와 비교해 `verified` 3,
`unverified` 221, `stale` 170, `unavailable` 3이다. 이 source 상태는 개별 기술 사실의
정확성 판정과 별개다. 사용자가 위임한 독립 검증으로 현재 승인 Fact registry에는
**1,047개 verified fact 레코드(1,046개 고유 Anchor, 65개 Topic)**가 등록되어 있고, 각 항목은 표준·제조사 자료·공식
기술문서 또는 재현 가능한 계산 근거를 기록한다. WordPress 출처가 없어도 기술적으로
확인할 수 있는 사실은 검증할 수 있으며, 현재 등록분은 모두 `score_effect=none`이다.

이 문단의 상세 미승격 분류는 이전 snapshot이다. 현재 registry 수량은 위의 `현재 Anchor 검증 상태` 표를 기준으로 한다. 동일 Anchor에 대해 둘 이상의 독립 Fact 표현이 존재할 수 있으므로 승인 Fact 레코드 수와 고유 Anchor 수를 구분한다.
그중에는 검토가 남은 항목과 조건·적용범위가 넓어 보류한 항목이 함께 있으므로, 미등록을
곧바로 오류 또는 최종 기각으로 해석해서는 안 된다. 31건의 강한 단어 신호도 기술적
정확성 검증을 대신하지 않는다.

2026-10-11 추가 검증: 생산관리 Pack의 `production_erp_mes_role_boundary`는 ISA-95 Level 3 제조운영관리(MES 등)와 Level 4 business planning/logistics(ERP 포함) 구분 및 두 기능 간 개념적 정보교환 모델로 범위를 좁혀 verified 등록했다. `production_mes_data_handoff`도 ISA-95가 Level 3/4의 인터페이스·객체·거래 모델을 정의한다는 범위로 정정·검증했으며, 특정 사업장의 Historian 데이터 집합이나 의사결정 책임을 표준이 일률적으로 정한다고 주장하지 않는다. `production_pdca_tradeoff_improvement`는 기존의 포괄적 KPI/재검증 의무 표현을 좁혀, NIST가 제조업 Lean의 반복적 낭비저감 방법으로 PDCA를 제시하고 개선 선택에서 전략적 중요도와 기대편익을 고려한다고 확인했다. 세 항목 모두 `score_effect=none`이다. `production_energy_consumables_cost`, `production_schedule_adherence_delivery_kpi`, `production_daily_management_visual_control`, `production_defect_containment_traceability` 등은 이번 근거만으로 Anchor 전체의 보편적 세부 주장을 뒷받침하지 못해 미승격 유지했다. 근거: [ISA-95 Standard](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard), [NIST, Methods and Tools for Performance Assurance of Smart Manufacturing Systems, §3.5.2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920944).
2026-10-11 추가 검증: 생산관리 Pack의 `production_erp_mes_role_boundary`는 ISA-95 Level 3 제조운영관리(MES 등)와 Level 4 business planning/logistics(ERP 포함) 구분 및 두 기능 간 개념적 정보교환 모델로 범위를 좁혀 verified 등록했다. `production_mes_data_handoff`도 ISA-95가 Level 3/4의 인터페이스·객체·거래 모델을 정의한다는 범위로 정정·검증했으며, 특정 사업장의 Historian 데이터 집합이나 의사결정 책임을 표준이 일률적으로 정한다고 주장하지 않는다. `production_pdca_tradeoff_improvement`는 기존의 포괄적 KPI/재검증 의무 표현을 좁혀, NIST가 제조업 Lean의 반복적 낭비저감 방법으로 PDCA를 제시하고 개선 선택에서 전략적 중요도와 기대편익을 고려한다고 확인했다. 세 항목 모두 `score_effect=none`이다. `production_energy_consumables_cost`, `production_schedule_adherence_delivery_kpi`, `production_daily_management_visual_control`, `production_defect_containment_traceability` 등은 이번 근거만으로 Anchor 전체의 보편적 세부 주장을 뒷받침하지 못해 미승격 유지했다. 근거: [ISA-95 Standard](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard), [NIST, Methods and Tools for Performance Assurance of Smart Manufacturing Systems, §3.5.2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920944).

2026-10-11 추가 검증: LVDT Topic의 `lvdt_null_residual_voltage`를 Texas Instruments SPRA946 §3.2.1과 대조했다. 보고서는 null에서 실제 잔류신호 원인으로 권선 불균형, 내부 기생 정전용량 및 누설저항을 들고, 기본 여자주파수 및 고조파 성분이 포함될 수 있다고 설명한다. 이에 기존 문구의 `누설자속`을 근거에 있는 `누설저항`으로 바로잡고, TI 자료에서 직접 확인되지 않은 자기회로 비대칭은 원인목록에서 제거했다. 센서 원시 AC 잔류신호와 신호조절 후 DC offset도 분리했다. `score_effect=none`이다. 근거: [Texas Instruments SPRA946, §3.2.1](https://e2e.ti.com/cfs-file/__key/CommunityServer-Discussions-Components-Files/171/7127.TI-_2D00_-Signal-Conditioning-an-LVDT-Using-a-TMS320F2812-DSP.pdf).

2026-10-11 추가 검증: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`의 `ipgse_pe_signal_reference_boundary`를 OSHA Electrical Safety 및 NI ground-terminology guidance와 대조했다. OSHA의 equipment-grounding conductor는 감전 위험을 낮추고 고장전류를 보호장치로 귀환시키는 경로이며, 접지 경로는 영구·연속이어야 한다. NI는 earth, chassis, circuit/reference ground가 반드시 동일 전위가 아니며, power-line ground는 안전 목적이라고 구분한다. 이에 보호접지와 측정 신호 기준전위는 기능상 구분하고 noise 대책으로 필요한 보호접지 경로를 끊지 않는다는 범위로 independently verified 등록했다. 전기안전 규정 및 설비 구성은 관할·장치별 요구사항을 따른다. `source_refs=[]`, `score_effect=none`이다. 근거: [OSHA, Electrical Safety—Grounding](https://obis.osha.gov/dte/library/electrical/electrical.html), [NI, Chassis, Earth and Signal Grounding](https://www.ni.com/en/support/documentation/supplemental/18/chassis--earth-and-signal-grounding--terminology-and-symbols.html).

같은 Topic의 `ipgse_ground_loop_mechanism`도 Analog Devices의 계장 신호 grounding 설명과 대조해 verified 등록했다. 자료는 ground/common/reference 경로를 통한 비의도 전류, 서로 다른 접지점의 전위차로 인한 신호선 전류, 그리고 측정 drift·shift·noise 증상을 연결한다. 본 Fact는 발생 구조를 설명하며, 특정 시설의 전류 크기나 측정오차를 정량화하지 않는다. `source_refs=[]`, `score_effect=none`이다. 근거: [Analog Devices, Ask The Applications Engineer—27: Signal Corruption in Industrial Measurement, “Ground Loops”](https://www.analog.com/en/resources/analog-dialogue/articles/ask-the-applications-engineer-27.html).

`ipgse_ground_loop_safe_mitigation`도 공식 NI, Analog Devices 및 OSHA 자료로 교차 확인했다. NI는 grounded source에 differential/nonreferenced measurement 선택, ground-loop breaking, 분리 return 경로와 coupling별 shielding을 설명하고, Analog Devices는 isolation이 unwanted conductive loop를 끊는 방식을 설명한다. OSHA grounding path의 영구·연속 및 fault-current 보호기능에 따라 PE를 noise 대책으로 끊지 않는 안전 경계를 함께 기록했다. NI의 source-end shield 연결 예는 capacitive coupling 상황에 한정했으며 보편 차폐 규칙으로 확대하지 않았다. `source_refs=[]`, `score_effect=none`이다. 근거: [NI, Field Wiring and Noise Considerations for Analog Signals](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [Analog Devices, Ground Loops](https://www.analog.com/en/resources/analog-dialogue/articles/ask-the-applications-engineer-27.html), [OSHA, Electrical Safety—Grounding](https://obis.osha.gov/dte/library/electrical/electrical.html).

`ipgse_cable_separation_coupling`은 NI의 coupling 모델과 ABB ACQ810 설치 매뉴얼을 함께 확인했다. NI는 capacitive coupling이 conductors의 overlap 증가·거리 감소로, inductive coupling이 separation 감소·signal-loop area 증가로 커질 수 있음을 설명한다. ABB는 해당 drive family 설치에서 motor/power/control cable의 분리, 긴 평행 배선 회피와 불가피한 교차의 약 90° 배치를 권고한다. 따라서 분리·평행구간 저감이 coupling을 낮추는 원리는 verified하되, ABB의 구체 배치 권고와 거리는 모든 drive·site에 보편화하지 않았다. `source_refs=[]`, `score_effect=none`이다. 근거: [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [ABB, ACQ810-04 Hardware Manual, Routing the cables, p. 47](https://library.e.abb.com/public/e42d63323f094d0690ad5061b12701fa/EN_ACQ810-04_A-D_hw_B_scrres.pdf?x-sign=X6piKX6Q8j3gMKz6KqLH4Td68%2BNp5BlkkS1Tr8r3vGA4kzopLSLFcNK8nChQae9Q).

`ipgse_emi_coupling_paths`는 Schneider Electric Electrical Installation Guide의 disturbance source/victim 및 네 가지 coupling type 분류, 그리고 NI의 계장 wiring별 conductive, capacitive, inductive, radiative 설명으로 verified 등록했다. 공통 임피던스 결합은 galvanic/conductive path로 한정하며, 실제 설치에서 여러 결합 경로가 함께 나타날 수 있으므로 source-path-victim 분석은 특정 현장의 경로 확인을 대신하지 않는다. `source_refs=[]`, `score_effect=none`이다. 근거: [Schneider Electric, EMC—Coupling mechanisms and counter-measures](https://www.electrical-installation.org/enwiki/EMC_-_Coupling_mechanisms_and_counter-measures), [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html).

`ipgse_common_differential_mode`는 NI의 계측 입력 기준·CMRR 한계, Analog Devices의 CM/DM noise 분리 및 filter 대응 사례, isolation의 conductive loop 단절 설명, Schneider의 coupling-path 분류를 대조해 verified 등록했다. CM rejection은 receiver의 rated common-mode range와 CMRR 한계 안에서만 유효하며, 특정 filter·bonding·isolation 조치가 모든 간섭모드에 보편 효과를 낸다고 보지 않는다. `source_refs=[]`, `score_effect=none`이다. 근거: [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [Analog Devices, Separating CM and DM Emissions](https://www.analog.com/en/resources/analog-dialogue/articles/separating-common-mode-and-differential-mode-emissions-in-conducted-emissions-testing.html), [Analog Devices, Signal Corruption in Industrial Measurement](https://www.analog.com/en/resources/analog-dialogue/articles/ask-the-applications-engineer-27.html), [Schneider Electric, EMC Coupling Mechanisms](https://www.electrical-installation.org/enwiki/EMC_-_Coupling_mechanisms_and_counter-measures).

`ipgse_ups_function_boundary`는 Schneider Electric의 UPS 기능·전원교란 설명과 Vertiv PowerUPS 6000의 galvanic-isolation 선택사항을 교차 확인했다. UPS는 부하·battery configuration에 따른 요구 backup autonomy 동안 중요부하 전원을 유지하고, 일부 topology/mode에서 voltage·frequency conditioning을 제공할 수 있다. 다만 galvanic isolation은 해당 Vertiv model family에서도 transformer option에 따라 달라지므로 단순 UPS 보유만으로 isolation이나 모든 EMC/surge 문제가 해소된다고 볼 수 없다. 특정 장비 보호성능은 실제 model, mode, accessory와 installation을 확인해야 한다. `source_refs=[]`, `score_effect=none`이다. 근거: [Schneider Electric, How does a UPS system work?](https://www.se.com/us/en/faqs/FAQ000244169/), [Vertiv, PowerUPS 6000 Industrial brochure, p. 2](https://www.vertiv.com/490d38/globalassets/products/critical-power/uninterruptible-power-supplies-ups/vertiv-powerups-6000-industrial-6-200kva-400v-single-and-three-phase-ups/liebert-power6000--industrial_brochure_en_r0925.pdf).

`ipgse_redundant_supply_boundary`는 Siemens SITOP redundancy/PSU 매뉴얼로 범위를 확인했다. Decoupled pair는 한 power-supply unit의 고장 후 다른 unit이 load를 인계할 수 있지만, Siemens는 100% redundancy 또는 높은 신뢰도를 위해 primary-side feeds의 separate fuse/protection과 가능하면 다른 phases/line supplies 사용을 권한다. 따라서 공통 primary feed는 전체 redundancy의 남은 공통경로이며, ORing/diode, battery, distribution 경로의 실제 위험과 효과는 해당 구성의 failure data와 아키텍처로 판정한다. 수치적 가용성·공통고장 확률은 주장하지 않는다. `source_refs=[]`, `score_effect=none`이다. 근거: [Siemens, SITOP Expansion Modules, §9.1, p. 125](https://cache.industry.siemens.com/dl/files/751/109977751/att_1309422/v1/A5E36605235-3-76_MANUAL_SITOP-Ergaenzungsmodule_en-US.pdf), [Siemens, SITOP modular 1ph/2ph, §9.2, p. 59](https://cache.industry.siemens.com/dl/files/605/109988605/att_1328468/v1/A5E52984737-5-76_MANUAL_SITOP-modular-1ph-2ph-200M_en-US.pdf).

`ipgse_power_quality_scope`는 Schneider Electric의 power-quality event 분류(정전, sag/swell, transient, harmonics, frequency variation)와 Fluke의 장비 증상 시각·전압 dip 시각 및 event recorder 비교 권고를 확인했다. Schneider Electric ATS 자료는 source voltage/frequency 감시 및 transfer sequence 설명을 뒷받침한다. 따라서 nominal voltage 하나만 보지 말고 기록 가능한 교란과 source-transfer 시점을 증상과 비교하되, 시간상 상관을 인과 증명으로 과장하지 않는다. 분류는 적용 측정 표준/계측기 능력에 따르고, transfer 동작은 설계·순서에 한정했다. `source_refs=[]`, `score_effect=none`이다. 근거: [Schneider Electric, Power Monitoring Expert events and disturbances](https://product-help.schneider-electric.com/EcoStruxure/Power-Monitoring-Expert-2023/content/8_reference/configuring/sw_modules/pqperf/trpqperf/pqevntsdistbnces.htm), [Fluke, Detecting Power Quality Issues](https://www.fluke.com/en-gb/learn/blog/power-quality/a-fresh-look-at-power-quality-basics), [Schneider Electric, What is a Transfer Switch?](https://www.se.com/us/en/work/featured-articles/what-is-a-transfer-switch/).

`ipgse_dc_supply_distribution`는 Siemens SITOP의 24 V branch selectivity 안내와 제품별 load-step 응답, NI의 배선 저항·전류에 따른 전압강하 계산 및 공통 return impedance가 sensor measurement에 주는 영향을 교차 확인했다. 따라서 이 항목들은 부하, 전선 경로/저항, PSU current-limit·dynamic response, 보호기기 조합별 설계 검토사항으로 등록했다. 특정 전압강하 한계·퓨즈 정격·보호협조 수치를 보편 규칙으로 제시하지 않으며, return-path 영향은 NI가 예시한 analog measurement 구성에 한정한다. `source_refs=[]`, `score_effect=none`이다. 근거: [Siemens, SITOP Catalog KT 10.1 (selectivity and model load-step data)](https://cache.industry.siemens.com/dl/files/655/109745655/att_1083770/v1/SITOP_KT10_1_complete_English.pdf), [NI, Cabling and Current-Resistance Loss](https://www.ni.com/en/shop/electronic-test-instrumentation/power-supplies-and-loads/what-are-programmable-power-supplies/cabling-and-current-resistance-loss-considerations-for-programma.html), [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html).

`ipgse_source_path_victim_mitigation`은 NI의 EMI source–susceptible receiver–intervening path 설명, NI의 conductive/capacitive/inductive/radiated coupling 구분, Analog Devices AN-1161의 source 억제·경로 비효율화·victim port 보호 대책을 대조했다. 이를 현장 EMC 진단의 분석틀로 한정하고 제품 적합성 시험이나 단일 보편 처방으로 확대하지 않았다. 한 가지 filter 또는 grounding 변경만으로 충분하다고 가정하지 않고 영향받은 조건에서 재시험하도록 scope를 보존했다. `source_refs=[]`, `score_effect=none`이다. 근거: [NI, Eliminate Noise in Your GPIB System](https://www.ni.com/en/support/documentation/supplemental/06/eliminate-noise-in-your-gpib-system.html/), [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [Analog Devices AN-1161](https://www.analog.com/en/resources/app-notes/an-1161.html).

`ipgse_single_multi_point_conditional`은 Analog Devices의 mixed-signal grounding 설명과 NI의 측정 노이즈 진단 지침을 대조했다. 접지방식은 cookbook 처방으로 결정하지 않고 실제 전류 귀환경로·주파수·system configuration을 고려하도록 범위를 확정했다. Analog Devices는 간단한 단일 보드 star 구성이 multi-card 및 다중 고주파 귀환경로에 그대로 맞지 않을 수 있다고 설명한다. 이는 protective earth를 약화·제거할 근거가 아니며, 본 Fact도 시설 전체 접지 설계에 관한 보편 규칙으로 확장하지 않는다. `source_refs=[]`, `score_effect=none`이다. 근거: [Analog Devices, Staying Well Grounded](https://www.analog.com/en/resources/analog-dialogue/articles/staying-well-grounded.html), [NI, Diagnosing & Reducing Measurement Noise](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html).

`ipgse_shield_not_pe`의 기존 문장은 cable shield가 어떤 경우에도 PE가 될 수 없다는 식으로 읽힐 수 있어 범위를 바로잡았다. NI는 계장 신호 cable shield를 유도 전류가 신호회로를 통과하지 않도록 하는 EMC 경로로 설명한다. OSHA는 보호접지 경로의 fault-current 용량·저임피던스 요건을 제시하고, ABB는 특정 power cable shield/armor를 PE로 사용하는 예외를 그 PE 도전율 조건에 한정한다. 따라서 계장 신호 shield/drain wire를 통상 PE나 normal load return으로 간주하지 않되, 적격 power-cable shield 예외는 인정한다. `score_effect=none`이다. 근거: [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [OSHA, Portable Grounding Equipment](https://www.osha.gov/etools/electric-power/hazardous-energy-control/portable-grounding-equipment), [ABB, Grounding and cabling of drive systems](https://library.e.abb.com/public/9fbb4caf7e4b4bf7970839b083ba5396/EN_Drive_systems_grounding_and_cabling_REF_D_A4.pdf).

`ipgse_shield_termination_frequency`는 NI의 특정 capacitively coupled measurement 예시에서 source-end termination을 권고하면서 both-end shield의 ground current 가능성을 경고하는 내용과, ABB drive motor cable에서 양단/360° shield bonding을 권고하는 제품군별 설명을 함께 대조했다. 상반된 지침이 아니라 coupling·cable·bonding 조건이 다른 사례다. 이를 근거로 현재 Anchor의 조건부 결론을 확인했으며 어느 한 종단법도 전 설비에 일반화하지 않는다. `score_effect=none`이다. 근거: [NI, Field Wiring and Noise Considerations](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), [ABB, Grounding and cabling of drive systems](https://library.e.abb.com/public/9fbb4caf7e4b4bf7970839b083ba5396/EN_Drive_systems_grounding_and_cabling_REF_D_A4.pdf).

`ipgse_filter_entry_bonding` 문구는 확보한 제조사 자료가 직접 뒷받침하는 범위로 좁혔다. TDK-Lambda는 filter를 enclosure power input 진입점 가까이 두도록 권하고, COSEL은 filter input/output 배선 분리와 짧고 굵은 ground wire를 권한다. Schaffner는 conductive unpainted mounting surface와 PE 연결을 안내한다. 따라서 `feedthrough`/경계부에 대한 보편 배치 주장은 빼고, 해당 power-line filter의 placement·wire routing·bonding 지침으로 특정했다. 최종 layout은 제품 매뉴얼과 실제 EMC 검증에 따른다. `score_effect=none`이다. 근거: [TDK-Lambda](https://www.us.lambda.tdk.com/resources/blogs/20230831.html), [COSEL](https://www.cosel.com/en/coselplus/product/46), [Schaffner, Safety and Installation Guidelines](https://www.schaffner.com/fileadmin/user_upload/pim/products/downloads/Schaffner_file_Safety_and_Installation_Guidelines_1.pdf).

`ipgse_spd_coordination`은 Phoenix Contact의 power/signal line용 coordinated SPD와 equipotential bonding, 짧은 연결선 및 protected/unprotected cable 분리 설명을 Schneider Electric·Phoenix Contact의 lead-inductance/voltage-protection-level 자료와 대조했다. 접속 리드의 전압강하가 잔류 보호수준에 더해질 수 있으므로 접속 임피던스 관리가 중요하다는 점을 등록했다. 특정 수치 길이, SPD 조합/거리 또는 규정 조항은 해당 제품·표준 맥락에만 한정했다. `source_refs=[]`, `score_effect=none`이다. 근거: [Phoenix Contact, Fundamentals for surge protection](https://www.phoenixcontact.com/assets/c8428ddc-254d-40b8-a2f2-540ac13bd818/epaper/5131327_TT_Basics_EN.pdf), [Schneider Electric, SPD Wire Length vs. Let-Through Voltage](https://www.se.com/us/en/faqs/FAQ000240088/), [Phoenix Contact, Surge protection installation](https://www.phoenixcontact.com/en-us/technologies/surge-protection-technology/surge-protection-installation).

`ipgse_ups_sizing_factors`는 Eaton의 W/VA·runtime·redundancy sizing, Fuji Electric의 autonomy 및 battery discharge/aging/temperature correction, Schneider Electric의 crest-factor와 efficiency 설명을 대조했다. load W와 VA를 별도로 확인하고, actual autonomy 및 battery condition을 vendor-specific discharge data에 따라 확인해야 한다. UPS power factor, inrush/crest response, efficiency, battery correction factor는 모델·부하·배터리별 값이므로 보편 수치로 등록하지 않았다. `source_refs=[]`, `score_effect=none`이다. 근거: [Eaton, UPS Sizing Guide](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/ups-sizing-guide.html), [Fuji Electric, UPS Sizing Calculation](https://www.india.fujielectric.com/resources/technical-guide/ups-sizing-calculation), [Schneider Electric, UPS crest factor FAQ](https://www.se.com/co/es/faqs/FA372337/), [Schneider Electric, UPS efficiency FAQ](https://www.se.com/us/en/faqs/FAQ000244215/).

`ipgse_ups_bypass_grounding`은 Vertiv Series 610과 ABB TLE UPS 설치매뉴얼의 configuration별 neutral/bypass grounding diagram, 그리고 Fuji Electric topology discussion을 대조했다. source neutral, bypass neutral, output bond의 배치는 제품과 topology별로 실제 달라지고, 일부 구성에서는 neutral-ground jumper와 source neutral을 함께 쓰지 말라는 제조사 경고가 있다. 따라서 neutral bond를 임의 추가·이동하지 말고 해당 UPS 정확한 manual·site single-line·local code를 검토해 qualified electrical personnel이 처리하도록 claim을 한정했다. `source_refs=[]`, `score_effect=none`이다. 근거: [Vertiv Series 610 installation manual, §§6.1–6.5](https://www.vertiv.com/globalassets/products/critical-power/uninterruptible-power-supplies-ups/discontinued---liebert-series-610-on-line-ups-225-1000kva/liebert-series-610-ups-100-225kva-multi-module-installation-manual.pdf), [ABB TLE UPS installation guide, p. 41](https://library.e.abb.com/public/01e2246dead74d6d8e4ba3c303255c99/ABB_UPS_ISG_TLE_SUL_M16_M50_2bU_REV-A.pdf), [Fuji Electric earthing-system guide](https://www.india.fujielectric.com/resources/technical-guide/earthing-system).

`ipgse_symptom_frequency_correlation`의 기존 문구는 VFD broadband 및 time-correlation을 과도하게 단정하지 않도록 좁혔다. NI의 spectrum guidance는 50/60 Hz peaks를 power-line coupling의 indicator, SMPS를 고주파 noise source로 설명한다. Fluke는 VFD switching pulse fast edge에서 cable transient reflection이 발생할 수 있다고 설명하고, OMRON은 relay/contactor coil switching surge를 명시한다. 증상 spectrum과 event timestamp는 원인 후보를 줄이는 evidence일 뿐 단독으로 인과를 증명하지 않는다고 기록했다. `score_effect=none`이다. 근거: [NI, Diagnosing & Reducing Measurement Noise](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html), [Fluke, VFD transient troubleshooting](https://www.fluke.com/en-us/learn/blog/predictive-maintenance/troubleshooting-transient-voltage-variable-frequency-drive-digital-multimeter), [OMRON FAQ02557](https://www.ia.omron.com/support/faq/answer/14/faq02557/), [Fluke, Power Quality event correlation](https://www.fluke.com/en-gb/learn/blog/power-quality/a-fresh-look-at-power-quality-basics).
2026-10-11 추가 검증: LVDT Topic의 `lvdt_null_residual_voltage`를 Texas Instruments SPRA946 §3.2.1과 대조했다. 보고서는 null에서 실제 잔류신호 원인으로 권선 불균형, 내부 기생 정전용량 및 누설저항을 들고, 기본 여자주파수 및 고조파 성분이 포함될 수 있다고 설명한다. 이에 기존 문구의 `누설자속`을 근거에 있는 `누설저항`으로 바로잡고, TI 자료에서 직접 확인되지 않은 자기회로 비대칭은 원인목록에서 제거했다. 센서 원시 AC 잔류신호와 신호조절 후 DC offset도 분리했다. `score_effect=none`이다. 근거: [Texas Instruments SPRA946, §3.2.1](https://e2e.ti.com/cfs-file/__key/CommunityServer-Discussions-Components-Files/171/7127.TI-_2D00_-Signal-Conditioning-an-LVDT-Using-a-TMS320F2812-DSP.pdf).

같은 Topic의 `lvdt_core_alignment_eccentricity_error`는 기존의 “편심이 보편적으로 영점·히스테리시스·반복성 오차를 만든다”는 표현이 지나치게 일반적임을 확인해 구조별 문구로 수정했다. TE Connectivity는 free-core의 방사상 간극·비접촉 구조와 guided/spring-loaded 구성을 구분하고, 일부 probe에서 베어링으로 radial play 및 side loading을 줄이는 설계를 설명한다. NewTek은 일부 오정렬이 측정 품질에 영향을 주지 않을 수도 있다고 하면서 설치별 side-load 저감 지침을 제시한다. 따라서 정렬 허용성은 선택한 구조와 제조사 한계로 판정하며 특정 오차를 모든 LVDT에 일반화하지 않는다. `score_effect=none`이다. 근거: [TE Connectivity, Understanding LVDTs](https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html), [NewTek Sensor Solutions LVDT FAQ](https://www.newteksensors.com/faq/).

2026-10-11 추가 검증: `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`에서 기존 13개에 더해 `pid_logic_diagram_relation`, `alarm_trip_interlock_boundary`, `pid_control_narrative_relation`, `legend_project_convention_priority`, `revision_moc_document_control`, `pid_lifecycle_use`, `pid_instrument_index_io_relation`, `design_review_cross_document_consistency`, `field_verification_asbuilt`를 조건·적용 범위를 한정해 verified 등록했다. 이번에는 `pid_not_pid_controller`도 ISO 10209:2022의 P&ID/PID 도면 용어와 ISA의 proportional-integral-derivative controller 용어를 대조해 verified 등록했다. 따라서 약어만으로 의미를 단정하지 않고, document/drawing context와 legend를 통해 구분한다. `pid_line_list_spec_relation`은 Line List와 P&ID의 대응은 공학 실무상 타당하지만 이번에 확보한 권위 있는 근거만으로 Anchor의 line spec·nozzle 일치 범위를 모두 입증하지 못해 미승격 유지한다. 기존 근거의 범위도 보존한다: OSHA는 PSM 적용 공정에, DOE-STD-1073은 DOE 원자력 시설 형상관리 범위에 한정한다. 근거: [ISO 10209:2022, §§3.10.133, 3.10.174–175](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A10209%3Aed-2%3Av1%3Aen), [ISA Fundamentals of PID Control](https://www.isa.org/intech-home/2023/june-2023/features/fundamentals-pid-control), [ISA-5.1](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa5-1), [ISA-5.2](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa5-2), [ISA, Control Loop Foundation, Chapter 7](https://www.isa.org/getmedia/e122051e-8c8c-48be-97ef-5d344c585771/Chapter7_Control-1.pdf), [OSHA 29 CFR 1910.119 Appendix C](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119AppC), [DOE-STD-1073-2003](https://www.energy.gov/documents/doe-std-1073-2003).

2026-10-11 추가 확인: `pid_line_list_spec_relation`에 대해 Autodesk Plant 3D 공식 도움말을 확인했다. P&ID Line List에서 line group별 FROM/TO equipment·nozzle을 볼 수 있고, 설정한 `Spec-Service-Line` tag format은 해당 정보를 line identification에 담을 수 있으며, matching line number로 P&ID와 3D model 간 property difference를 검증할 수 있다고 명시한다. 이는 제품 설정이 구성된 경우 line ID·spec/service·endpoint 데이터를 교차확인하는 제한적 근거다. 다만 현재 승인 Anchor는 project-independent한 검토 의무처럼 읽히고, 별도 Line List/piping class 문서 및 equipment nozzle schedule의 일치가 보편적으로 요구된다는 범위를 Autodesk 문서가 정하지 않는다. 그러므로 추가 근거는 일부 구성·기능을 지지하지만 Anchor 전체를 verified 처리하기에는 부족하여 미승격을 유지한다. 근거: [Autodesk Plant 3D, To Place Equipment and Nozzles from the P&ID Line List](https://help.autodesk.com/cloudhelp/2027/ENU/Plant3D-UserGuide/files/GUID-4240B827-A951-4332-9FB4-A50C8D226210.htm), [Autodesk Plant 3D, About Pipe Line Numbers](https://help.autodesk.com/cloudhelp/2027/ENU/Plant3D-UserGuide/files/GUID-531801FA-638C-4B16-B80B-2A66632DDA5C.htm).

`control_valve_types_globe_rotary_body_actuator_selection`의 `standard_bonnet_pressure_boundary`는 Emerson Control Valve Handbook §3.3으로 확인했다. Globe/angle body bonnet은 압력 유지 경계의 한쪽 closure이며 stem/shaft 통로와 packing box를 제공한다. Rotary body에서는 packing이 body에 있고 bonnet이 없을 수 있어 적용 범위를 함께 명시했다. 같은 Topic의 `post_guided_plug_alignment`는 Fisher EZ 자료의 plug stability 및 특정 유체·고형물 조건에서의 sticking 경감 설명, Fisher SS-204 자료의 travel 전 구간 plug stability·vibration 관련 서술, Handbook의 post-/port-guided 구성 및 횡방향 지지 설명, 조건부 정역학 관계를 결합해 범위를 한정하여 verified 등록했다. 가이드 지지 간격이 커지면 동일한 외력 모멘트에서 이상화된 지지 반력이 감소할 수 있다는 역학 관계이지, 가이드 길이가 유체력·마모율을 보편적으로 결정한다는 뜻은 아니다. `port_guided_plug_alignment`는 포트 가이드의 세부 간극·오염 내성·마모 비교를 직접 확증하는 자료가 부족해 미검증이다. 점수 영향은 없다. 근거: [Emerson Control Valve Handbook, §3.1.1.2 and §3.3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher EZ Control Valve](https://www.emerson.com/en-us/catalog/fisher-ez), [Fisher SS-204 Product Bulletin D104803X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/product-bulletin-fisher-ss-204-ultra-high-temperature-control-valve-en.pdf), [Ferrari, transverse-load experiment on an instrumented globe valve](https://arxiv.org/abs/0909.0874).

`process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`의 `loop_interaction_coordination`은 조건부 범위로 검증했다. ISA Advanced PID Control은 다중루프 간 영향과 relative-gain pairing/decoupling을 설명하고, Siemens PID_Compact override 문서는 여러 controller가 하나의 actuator를 공유할 때 selector authority, control direction, inactive-controller tracking, output limits 및 windup/switchover 동작을 다룬다. MathWorks는 tracking을 이용한 bumpless transfer 예를 제공한다. 따라서 interaction assessment, shared-actuator authority 및 전환·포화 관리는 해당 구조에서 중요하지만, 모든 다중루프에 decoupling이 필요하다는 주장은 하지 않는다. 같은 Pack의 `field_implementation_validation`은 광범위한 종전 문구를 제거하고, Siemens PID_Compact V3 공식 매뉴얼로 확인 가능한 제품별 예시로 축소했다: 자동·수동 모드, anti-windup, 출력 제한 도달 시 방향에 따른 적분 정지 및 설정 한계와 control logic의 일치 요구다. 이 제품 예시를 다른 DCS/PLC의 보편 기능으로 확대하지 않는다. 점수 영향은 없다. 근거: [Siemens PID_Compact V3 description](https://docs.tia.siemens.cloud/r/en-us/v21/pid-control-s7-1200-s7-1500-s7-1200-g2/pid_compact-s7-1200-s7-1500-s7-1200-g2/pid_compact-as-of-v2-s7-1200-s7-1500-s7-1200-g2/description-of-pid_compact-v3-s7-1200-s7-1500-s7-1200-g2), [Siemens PID parameters V3](https://docs.tia.siemens.cloud/r/en-us/v20/using-pid_compact-s7-1200-s7-1500/pid_compact-as-of-v2-s7-1200-s7-1500/configuring-pid_compact-as-of-v2-s7-1200-s7-1500/advanced-settings-as-of-v2-s7-1200-s7-1500/pid-parameters-v3-s7-1200-s7-1500?contentId=Bx~00pCcEGZLkmfQJ3v_SA), [Siemens Override Control](https://docs.tia.siemens.cloud/r/simatic_s7_1500_et_200mp_manual_collection_enus_21/comprehensive-information/technology-function-manuals/pid-control/using-pid_compact/pid_compact-as-of-v2/override-control-with-pid_compact-as-of-v2?contentId=kd~EOUBnmcafM1UaJukk5w), [MathWorks Bumpless Control Transfer](https://www.mathworks.com/help/simulink/slref/bumpless-control-transfer.html).

## 독립 기술 사실 검토 진행상태

### 추가 미승격 검토

`control_valve_types_globe_rotary_body_actuator_selection`의 `sliding_stem_rotary_motion_classification`은 Emerson/Fisher Control Valve Handbook의 정의와 대조해 verified 등록했다. Handbook은 sliding-stem valve의 closure member가 seating surface 방향으로 직선 이동하고, rotary valve에서는 ball/disk/eccentric plug 등이 shaft 회전으로 유로를 바꾸며 actuator lever가 linear stem motion을 rotary torque로 전달하는 구조를 구분한다. 따라서 Anchor의 motion-based classification 및 actuator linkage 기본 구분을 확인했다. 이 구분만으로 최종 body, flow characteristic 또는 actuator sizing을 결정할 수 있다는 뜻은 아니다. `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 1](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf), [Emerson, What Are the Different Types of Control Valves?](https://videos.emerson.com/detail/videos/regulators/video/6281259529001/what-are-the-different-types-of-control-valves?autoStart=true).

`ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`의 `sw09_zone_conduit`은 ISA/IEC 62443의 zone 및 conduit 정의와 NIST SP 800-82 Rev. 3의 OT 네트워크 세그멘테이션 안내를 교차 확인해 verified 등록했다. Zone은 공통 보안요구를 공유하는 자산의 논리적 grouping이고, conduit는 zone 사이를 연결하는 통신 채널 grouping이다. 경계별 허용 통신과 보안통제는 실제 위험·구성에 따라 정의해야 하며 보편 네트워크 토폴로지를 규정하지 않는다. 나머지 같은 Topic의 운영·기술 통제 Anchor는 이 두 출처만으로 복합 처방 전체를 검증하지 않아 미승격이다. `score_effect=none`이다. 근거: [ISA Security Compliance Institute, ISA/IEC 62443 Overview](https://isasecure.org/hubfs/Webinars/Webinars%20PDFs/62443-Overview-Presentation.pdf?hsLang=en), [NIST SP 800-82 Rev. 3, §5.1.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

`control_valve_types_globe_rotary_body_actuator_selection`의 `actuator_output_matches_valve_motion`은 Emerson/Fisher actuator design 자료 및 Control Valve Handbook의 sliding-stem/rotary 정의와 대조했다. Sliding-stem은 stem travel을 위한 linear thrust, rotary shaft valve는 요구 rotation을 위한 torque가 필요하며, 선형 actuator를 rotary valve에 쓰는 경우에는 motion-converting actuator/linkage와 coupling의 lost motion을 고려해야 한다. 실제 stroke·rotation·force/torque 값은 application-specific이므로 이 Fact는 output type matching까지만 검증한다. `score_effect=none`이다. 근거: [Emerson/Fisher, Control Valve Actuators D103540X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf), [Emerson/Fisher Control Valve Handbook, Chapter 1](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf).

같은 Pack의 `rack_pinion_rotary_torque_conversion`은 Emerson의 pneumatic rack-and-pinion 제품 설명 및 Bettis sizing procedure와 대조했다. Rack/pinion은 linear rack 운동을 pinion 회전으로 변환하며 quarter-turn ball·butterfly·plug valve에 사용하는 사례가 명시되어 있다. sizing은 실제 최소 공급압력에서 해당 회전 위치·방향별 torque가 valve torque를 초과하는지 확인하고 actuator 최대 허용압력을 넘지 않도록 한다. 이는 특정 제품 구조/정격에 적용되는 선정 조건이며 모든 rack-and-pinion actuator를 동일한 압력 또는 torque 곡선으로 취급하지 않는다. `score_effect=none`이다. 근거: [Emerson Pneumatic Rack and Pinion Actuators](https://www.emerson.com/en/final-control/catalog/products-and-software/actuators/pneumatic-actuators/rack-pinion-actuators), [Emerson/Bettis Actuator Selection Procedures](https://www.emerson.com/is/content/emerson/en/final-control/actuation/documents/data-sheet-bettis-actuator-selection-procedures.pdf).

같은 Pack의 `butterfly_compact_high_capacity`는 Fisher/Emerson Control Valve Handbook 6판 3장·10장 및 High Performance Butterfly Valves 적용자료와 대조했다. Butterfly는 quarter-turn disk 방식이며, 특히 큰 구경에서 compact/lightweight 및 경제성이 장점으로 설명되고 설치공간도 작다. Throttling 또는 on/off에 사용할 수 있으나 고성능 형식도 일반적으로 precision throttling용은 아니며, 특정 characterized design은 제어범위를 넓힐 수 있다. Seat/disk 형상, torque 및 요구 차단성은 실제 선택 형식에 따라 확인해야 한다. `score_effect=none`이다. 근거: [Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [Control Valve Handbook, Chapter 10](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [High Performance Butterfly Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/butterfly-valves/high-performance-butterfly-valves).

같은 Pack의 `full_port_ball_low_restriction_scope`는 Fisher/Emerson Control Valve Handbook 6판 3장 §3.1.3.5와 대조했다. Full-port ball은 비감쇠 상태에서 완전 개방 시 유동 저항이 작고 pigging을 허용할 수 있다. 다만 완전 개방 상태에서 일정 초기 회전구간 동안 유체 에너지를 유의하게 흡수하지 못해 제어 lag가 생길 수 있으므로, throttling 목적이면 reduced-port 또는 attenuated 구조가 더 적절할 수 있다. 따라서 저저항·pigging 장점이 모든 정밀 throttling 업무에서의 우월성을 뜻하지 않는다. `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf).

같은 Pack의 `multiport_selector_flow_routing`은 Fisher Multiport Flow Selector에 한정해 Control Valve Handbook 6판 3장 §3.1.3.6 및 2022년 제품 매뉴얼을 대조했다. 이 구성은 8개 inlet 중 한 line을 rotating plug로 test/diversion outlet에 보내면서 나머지 7개는 common group outlet으로 계속 흐르게 하며, 다른 생산 흐름을 중단하지 않는 compact selection/testing을 제공한다. Body·bonnet·rotor plug·actuator 구성과 tight sealing을 확인했으나, 이는 해당 제품의 routing 구성이지 모든 multiport valve의 port 수·배관 절감·격리 성능을 일반화하지 않는다. `score_effect=none`이다. 근거: [Control Valve Handbook, Chapter 3](https://documentation.emersonprocess.com/intradoc-cgi/groups/public/documents/book/d101881x012.pdf), [Fisher Multiport Flow Selector Manual D104239X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d104239x012.pdf).

같은 Pack의 `end_connection_threaded_flanged_welded`는 Fisher/Emerson Control Valve Handbook 6판 3장 §§3.2.1–3.2.3과 대조했다. Threaded 연결은 작은 밸브에 흔하고 본체 제거·고온 적용에서 제한이 있으며, flange 연결은 분해·제거가 쉽고 service rating은 flange 형식·재료에 따르고, welded 연결은 제거가 더 어렵고 용접 가능한 재료로 제한된다. 따라서 연결 방식에 따라 joint/sealing 경로, 유지보수성, pressure-temperature 적용 범위가 달라진다는 비교 주장은 확인했다. 개별 사용압력·온도 및 누설성능은 연결 형식만으로 단정하지 않고 적용 코드·재료·정격을 확인해야 한다. `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf).

같은 Pack의 `electric_actuator_motor_gear_control`은 Emerson Bettis TorqPlus/HQ-series 제품자료 및 Biffi fail-safe electric actuator 매뉴얼과 대조했다. 문헌상 motor/gear actuator는 torque를 내며 continuous/modulating duty, hazardous-area enclosure 및 loss-of-power fail-safe 옵션이 실제 제품에 구현되어 있다. 따라서 electric actuator가 instrument air 부재 때만 쓰이는 것은 아니며, 전원·속도·duty·방폭·정전 시 동작을 모델별 정격과 구성으로 확인해야 한다. 제품별 사례를 모든 electric actuator에 동일한 fail-safe 기능이 있다고 일반화하지 않았다. `score_effect=none`이다. 근거: [Bettis TorqPlus](https://www.emerson.com/en/final-control/products/bettis-pl9), [Bettis HQ-Series](https://www.emerson.com/en/final-control/products/bettis-hqe), [Biffi EFS2000v4 manual](https://www.emerson.com/is/content/emerson/en/final-control/actuation-technologies/electrics/general/documents/ACT-IOM-Fail-Safe-Electric-Actuators-model_-EFS2000v4-IOM-BIFCS-0026-EN.pdf).

같은 Pack의 `hydraulic_actuator_force_and_stored_energy_fail_safe`는 Emerson hydraulic actuator 자료, Bettis EHO 회로 설명, HAWE의 stiffness 기술자료 및 Emerson/Biffi RPHS 유지보수 매뉴얼을 교차 확인했다. 유압은 큰 force/torque를 낼 수 있고, 적절한 회로에서는 accumulator가 에너지원 상실 시 지정된 fail-safe 동작을 지원한다. 다만 stiffness는 cylinder geometry·stroke·enclosed fluid volume 및 system design에 좌우되며, 모든 hydraulic actuator에 높은 stiffness가 자동 보장되는 것은 아니다. Leakage, fluid level/filter 및 accumulator의 저장 압력은 특정 제품 매뉴얼대로 점검·방출해야 한다. `score_effect=none`이다. 근거: [Emerson Hydraulic Actuators](https://www.emerson.com/en/final-control/catalog/products-and-software/actuators/hydraulic-actuators), [Bettis EHO manual](https://www.emerson.com/is/content/emerson/en/final-control/actuation-technologies/electrics/general/documents/ACT-IOM-EHO-Electro-Hydraulic-Operated-Spring-Return-Actuator-VCIOM-15345-EN.pdf), [HAWE, Stiffness of Actuators](https://www.hawe.com/fr-fr/fluid-lexicon/detail/stiffness-of-actuators/), [Biffi RPHS manual](https://www.emerson.com/is/content/emerson/en/final-control/actuation-technologies/hydraulics/general/documents/ACT-IOM-RPHS-Hydraulic-Actuators-IOM-VCIOM-03748-EN.pdf).

같은 Pack의 `double_port_capacity_force_balance_limit`은 Fisher/Emerson Control Valve Handbook 6판 §3.1.1.4와 PIP PCECV001:2022 §4.2.2를 대조했다. 같은 body size의 double-port가 single-port보다 높은 capacity를 가질 수 있고, 서로 반대 방향의 dynamic force가 부분 상쇄되어 actuator force 요구를 줄일 수 있다고 기술되어 있다. 두 plug가 동시에 seat하는 것이 어렵고 일반적인 metal-seat shutoff는 Class II(일부 구성에서 Class III 가능)로 single-port보다 제한적이라는 설명도 교차 확인했다. 이는 완전한 힘 상쇄나 보편적 leakage class를 뜻하지 않으며 실제 정격은 제품별 시험으로 확인해야 한다. `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/es/final-control/flow-controls/documents/d101881x012.pdf), [PIP PCECV001:2022](https://www.scribd.com/document/1076022918/PCECV001) (공개 미러본; §4.2.2 items 4–6).

같은 Pack의 `segmented_v_notch_ball_throttling`은 Fisher/Emerson Control Valve Handbook 6판 §3.1.3.2, Vee-Ball 제품 bulletin 및 Emerson의 segmented-ball 기술자료로 대조했다. V-notch ball contour는 특정 제품에서 equal-percentage 또는 modified equal-percentage 특성을 만들고, 제조사는 해당 제품군의 rangeability·capacity·non-clogging 및 shutoff 성능을 기술한다. 이 설명을 모든 segmented ball valve에 적용되는 정량 성능이나 일정 차단등급으로 확장하지 않았다. `score_effect=none`이다. 근거: [Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [Vee-Ball product bulletin D101363X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101363x012-bulletin-vee-ball-v150-v200-and-v300-rotary-control-valves-fisher.pdf), [Segmented Ball Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/ball-valves/segmented-ball-valves).

같은 Pack의 `plug_guiding_alignment_and_side_load`은 Fisher/Emerson Control Valve Handbook 6판 §3.6, Fisher Control Valve Sourcebook 및 Ferrari의 globe-valve 횡하중 측정 연구로 대조했다. Cage-, top-, stem-, top-and-bottom-, port-guiding은 plug를 seat에 정렬하는 구조가 서로 다르다. Sourcebook은 특정 구조에서 plug/cage 또는 post/bushing 마모, side-load와 vibration/instability를 기술하고, 연구는 특정 2-inch globe valve 조건에서 transverse stem load가 guidance-part wear 예측에 관련됨을 보인다. 따라서 load·진동·마찰·마모를 형식 선정과 운전 중 점검에서 고려한다는 범위로 확인했으며, 특정 guide가 모든 service에서 우월하다고 일반화하지 않았다. `score_effect=none`이다. 근거: [Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher Control Valve Sourcebook](https://www.scribd.com/doc/106510786/Fisher-Control-Valve-Sourcebook-Power-and-Severe-Service) (공개 미러본), [Ferrari, 2009](https://arxiv.org/abs/0909.0874).

당시에는 `post_guided_plug_alignment`의 guide geometry와 하중·마모 사이의 일반 인과를 직접 입증할 자료가 부족해 보류했다. 후속 검토에서 Fisher EZ 및 SS-204의 제품별 stability 설명과 Handbook의 구성 설명, 지지 간격에 따른 조건부 정역학 관계를 조합해, 보편적인 유체력·마모율 주장을 제외한 제한된 fact로 승격했다. 따라서 과거의 미승격 판단은 이 범위 한정으로 대체되며, `port_guided_plug_alignment`는 별도로 미검증 상태다. 과거 부분 근거: [Fisher EZ Control Valve, Emerson](https://www.emerson.com/en-us/catalog/fisher-ez), [Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf).

같은 Pack의 `cage_guided_alignment_and_flow_path`는 Emerson/Fisher Control Valve Handbook §3.1.1.3, §3.7 및 제품별 trim 자료로 대조해 verified 등록했다. 핸드북은 cage-style trim의 plug guiding, seat-ring retention, flow characterization 역할과 interchangeable/restricted-capacity trim에 따른 flow characteristic·capacity·noise attenuation·anti-cavitation 선택을 설명한다. 제품자료도 clean cavitating service와 dirty/cavitating service의 별도 cage-trim 제품·입자 통과 한계를 구분한다. 따라서 cage-guided라는 이유만으로 모든 입자 유체에 적합하다고 일반화하지 않았다. 점수 영향은 없다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher NotchFlo DST](https://www.emerson.com/en/final-control/products/fisher-notchflo-dst), [Fisher Cavitrol III Trim](https://www.emerson.com/en/final-control/products/fisher-cavitrol-iii).

이 검토 시점에는 `standard_bonnet_pressure_boundary`와 `extension_bonnet_temperature_isolation`을 함께 보류했으나, 후속 검증에서 bonnet anchor를 globe/angle body로 한정하고 rotary-body 차이를 명시해 전자만 verified 등록했다. `extension_bonnet_temperature_isolation`은 설치방향 및 응축 조건까지 직접 뒷받침하는 자료가 부족해 계속 미승격이다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), §§3.3–3.3.1.

`cage_guided_alignment_and_flow_path`의 registry record는 이번 재검증에서 기존 verified 상태를 유지하되, 근거 범위를 강화했다. 공식 핸드북은 cage의 plug guidance·seat-ring retention·flow characterization과 interchangeable/restricted-capacity trim의 적용을 설명한다. Fisher 제품자료는 clean cavitating service와 dirty/cavitating service의 구별 및 dirty-service 제품별 입자 통과 한계를 보여준다. 따라서 cage-guided라는 형식만으로 모든 입자 함유 유체에 적합하다고 주장하지 않는다. 이 변경은 이미 등록된 하나의 Anchor에 대한 근거 보강이며 집계 수는 변하지 않는다. 점수 영향은 없다. 근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher NotchFlo DST](https://www.emerson.com/en/final-control/products/fisher-notchflo-dst), [Fisher Cavitrol III Trim](https://www.emerson.com/en/final-control/products/fisher-cavitrol-iii).

이번 대조로 `balanced_trim_unbalanced_trim_structure_sealing_applications`의 `control_valve_balanced_unbalanced_scope` Anchor를 verified 등록했다. Emerson/Fisher Refining Sourcebook은 특정 cage-style balanced plug에서 downstream pressure가 plug 양면에 작용해 static unbalance force를 줄이고, plug-to-cage seal이 upstream-to-downstream leakage를 제한하는 구조를 설명한다. Fisher Oil & Gas sizing sourcebook은 net unbalance area와 shutoff differential pressure를 force basis로 두면서 balanced valve에도 잔류 unbalance area가 있고 actuator sizing에는 seat load, packing friction 및 application/construction-specific force가 추가됨을 분리한다. 따라서 trim의 balance 여부만으로 zero force, shutoff class 또는 actuator size를 추론하지 않는 범위로 Fact를 확정했다. 이는 제조사 구성례이지 모든 trim의 보편 규격이 아니며 `score_effect=none`이다. 근거: [Emerson/Fisher Control Valve Sourcebook—Refining](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/control-valve-sourcebook-refining-en.pdf), [Fisher Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf).

같은 Pack의 남은 6개 hand-off/boundary Anchor는 개별 기술 사실이 아니라 내부 토픽 소유권 주장이다. 현재 Pack inventory 및 소유 Topic의 제목·Anchor scope와 대조해 `actuator_sizing_topic1_handoff`→`control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`, `dynamic_friction_topic3_handoff`→`control_valve_deadband_stiction_response_time_positioner_dynamic_performance`, `body_cage_guide_topic4_handoff`→`control_valve_types_globe_rotary_body_actuator_selection`, `low_noise_trim_topic9_boundary`→`control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`, `leakage_packing_topic13_boundary`→`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`, `severe_service_material_topic14_boundary`→`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`의 crosswalk가 일치함을 확인했다. 이를 `scope_consistent`로 기록하되 기술사실의 독립 검증과 섞지 않고 approved Fact registry에는 넣지 않았다.

초기 검토에서 `lvdt_null_residual_voltage`와 `lvdt_core_alignment_eccentricity_error`는 원문이 나열한 원인·결과 전체를 근거가 보증하지 않아 미승격했다. 2026-10-11 후속 대조에서는 두 원문을 근거에 맞게 좁혀 각각 TI SPRA946에 의한 raw AC null residual signal 및 TE/NewTek의 구조별 alignment sensitivity로 수정·verified 등록했다. `lvdt_excitation_frequency_voltage_sensitivity`는 NI 안내의 최고 예상 core-motion frequency 대비 최소 10배 선정 조건과 AD698의 conditioner-specific 범위를 반영해 verified됐다. 이어 `lvdt_magnetic_saturation_nonlinearity`는 과도한 1차 여자에 따른 코어 포화·고조파와 자기재료 포화에 따른 비선형으로 범위를 줄여, `lvdt_calibration_traceability_diagnostics`는 정격 여자·지정 stroke에서의 출력특성화와 측정결과에 대한 문서화된 교정사슬·불확도로 범위를 줄여 각각 verified 등록했다. 복조오차, 보편 교정주기 및 frequency-response calibration은 주장하지 않는다. 그 밖의 LVDT 복합·조건부 주장은 근거 범위 전체가 확인되기 전까지 registry에 추가하지 않는다.

`process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`의 구조 선정 Anchor `architecture_selection_criteria`는 후속 교차검토 후 verified 등록했다. ISA는 공정 동특성, 상호작용과 복잡한 loop의 실제 이득을 고려하고, ISA CAP 설계기준은 safety/network architecture·instrument preference·비용을 project basis에 포함하며, Skogestad의 plant-wide control 절차는 운영·경제목표, 자유도와 제약을 control configuration 선택에 연결한다. 다만 이를 고정·동일가중의 보편 체크리스트가 아니라 application-specific 고려사항으로 한정했다. 현재 미등록 Anchor는 `loop_interaction_coordination`과 `field_implementation_validation` 두 개다. 근거: [ISA, Design Principles for Complex Process Control](https://www.isa.org/intech-home/2016/march-april/features/design-principles-for-complex-process-control), [ISA CAP Body of Knowledge](https://www.isa.org/certification/cap/cap-body-of-knowledge), [Skogestad, Plantwide control: Towards a systematic procedure](https://www.sciencedirect.com/science/article/abs/pii/S1570794602800396), [MathWorks, Anti-Windup Control Using PID Controller Block](https://www.mathworks.com/help/simulink/examples/anti-windup-control-using-a-pid-controller.html), [MathWorks, Prevent Block Windup in Multiloop Control](https://www.mathworks.com/help/simulink/slref/prevent-block-windup-in-multiloop-control.html).

`gwr_quasi_tem_return_path`의 원래 quasi-TEM·귀환경로·분산 문구는 범용 전자기 주장으로 뒷받침되지 않아 그대로 승인하지 않았다. 대신 Magnetrol Eclipse 706 manual §3.3.5.2의 직접 근거에 맞춰 Pack Anchor를 제품별 single-rod 설치 효과로 좁혔다. Manual은 해당 probe 주변 전자기장이 설치·적용조건에 민감하고, nozzle 임피던스 불연속 및 근접 금속물이 추가 반사·false echo·측정오류를 만들 수 있다고 설명하며, 그 Model 706 구성에서 접지 coax outer tube의 영향을 구별한다. 따라서 새 verified Fact는 TEM/quasi-TEM 모드를 일반화하지 않는다. 근거: [AMETEK/Magnetrol Eclipse 706 HART I&O Manual BE 57-606, §§3.3.5.2, pp. 50–51](https://www.ametek-measurement.com/-/media/project/oneweb/oneweb/lms/documents/instruction-manuals/magnetrol/57-606_eclipse_model_706_hart_io.pdf?la=en&revision=3cc2fa2d-2023-4d70-8a74-8a74b6bebae0).

`radar_upper_null_zone_overfill_coordination`의 원래 송신누설·ringdown·수신기 포화 원인 묶음 및 전 서비스 공통 독립-HH 요구는 문서만으로 일반화할 수 없어 제거했다. 좁힌 Anchor는 Rosemount 5408 manual의 model-specific UNZ 계약(에코 무시, 영역 안에서 측정하지 않음, Upper Range Value 제한)과 API Std 2350 5th ed. §5.2.4.1의 적용범위 내 Category 3 구성(ATG+독립 LAHH)을 구분한다. API 2350의 판본·범위는 API 공식 catalog로 확인했고, 독립 LAHH 사례는 HSE HSG176의 flammable-liquid storage tank guidance와 대조했다. 다른 설비·서비스에 같은 독립 센서 의무를 보편 적용하지 않는다. 근거: [Emerson Rosemount 5408 Reference Manual, §7.5.3, p. 138](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-5408-non-contacting-radar-transmitter-202470.pdf), [API Standard 2350, 5th Edition](https://www.api.org/products-and-services/standards/important-standards-announcements/standard-2350), [HSE HSG176, Fig. 9, p. 33](https://www.hse.gov.uk/pubns/priced/hsg176.pdf).

별도 fact registry는 출처 문장 유사도가 아니라 표준·공식 기술문서·재현 계산으로
사실을 독립 확인한 항목만 기록한다. 최신 registry는 **1,016개 레코드 / 1,015개 고유
Anchor / 64개 Topic**을 담고 있다. 전체 2,069개 technical Fact Anchor 중 1,054개는 아직 verified로
등록하지 않았으며, 이는 오류 판정이 아니라 미검토 또는 보류 상태를 포함한다.

`humidity_measurement_capacitive_resistive_dew_point_selection_compensation`의 `humidity_lifecycle_maintainability_selection`은 당초 보편 checklist로 해석했을 때는 보류했으나, 후속 검토에서 claim을 application-specific selection principle로 한정해 verified 등록했다. Vaisala 자료는 measurement range, 극한 온도·압력, condensation recovery, contamination, hazardous-area certification, 설치·교정 접근성 및 유지보수를 위한 process isolation을 다루며 HMD60 manual은 model-specific sensor/filter maintenance, calibration interval 조건 및 receiver와의 output compatibility를 명시한다. NIST Handbook 135는 비교 목적에 따라 acquisition, operation, maintenance, disposal 비용을 lifecycle cost에 포함할 수 있음을 뒷받침한다. 고정된 필수 checklist나 동일한 중요도는 주장하지 않는다. 근거: [Vaisala humidity instrument selection](https://www.vaisala.com/en/expert-article/how-to-choose-the-right-instrument-for-measuring-humidity-and-dew-point), [Vaisala HMD60 manual](https://www.vaisala.com/sites/default/files/documents/HMD60%20Operating%20Manual%20Multilingual%20M210276EN.pdf), [NIST Handbook 135](https://nvlpubs.nist.gov/nistpubs/hb/2022/NIST.HB.135e2022-upd1.pdf).

2026-10-11 추가 검증 갱신: SW-02 Pack은 28개 중 10개 Anchor에 대응하는 verified Fact가 등록되어 있다. 추가 확인한 `sw02_voting_logic`은 ISA 교재의 1oo2/2oo3 사례에서 false-trip과 failure-to-trip 위험 간 trade-off로 한정했다. `sw02_first_out`은 Rockwell PlantPAx의 동일 scan 내 복수 발생 시 복수 first-out 표시 동작에 한정했다. `sw02_transition_guard`는 Siemens S7 SFC 전이의 Boolean 조건과 successor-step enable 정의에 한정했다. `sw02_bypass`는 Rockwell PlantPAx 설정·요청·downstream enable 및 문서가 설명하는 전형적 Engineering/Maintenance 역할분담에 한정했다. 이들은 일반적인 SIL 설계 요구나 보편적 운영절차를 확정하지 않으며 모두 `score_effect=none`이다. 근거: [ISA, Essentials of Modern Measurements, ch. 1](https://www.isa.org/getmedia/eb76a613-3961-4db0-8efe-a91dc308ec68/Essentials-of-Modern-Measurements_McMillan_Chapter-1-Essentials.pdf), [Rockwell PlantPAx PINTLK](https://www.rockwellautomation.com/en-be/docs/studio-5000-logix-designer/38-02/contents-ditamap/instruction-set/plantpax-instructions/pintlk.html), [Siemens SIMATIC S7 SFC manual](https://cache.industry.siemens.com/dl/files/980/109805980/att_1092610/v1/s7sfcs7b_en-US.pdf). 아래의 개별 팩 설명은 앞선 검토 시점의 기록일 수 있으며, 본 갱신 수치가 최신 registry 기준이다.

`control_hardware_lifecycle_panel_architecture_component_selection_production_verification`의 35개 Anchor 중 이번에 4개를 NASA Systems Engineering Handbook의 요구사항 검증 matrix, V&V plan 및 glossary와 대조했다. `chl_requirement_traceability`는 applicable shall-requirement에 고유 ID와 source document를 부여하고 requirement flowdown 및 양방향 추적방법을 정하는 범위로 확인했다. 적용되는 requirement category와 traceability tool은 project-specific이므로 보편적인 고정 목록으로 주장하지 않는다. `chl_verification_plan`은 검증 method(analysis, inspection, demonstration, test), 담당 역할, unit flow 및 test-article pedigree를 계획 문서에서 다루는 범위로 제한했다. 개별 acceptance criterion과 execution detail은 연결된 test procedure에 둘 수 있다. `chl_verification_vs_validation`은 설계 요구사항 적합성의 증명과 의도한 사용/승인된 stakeholder expectation 충족의 구분으로 확인했다. `chl_bom_configuration`은 approved product baseline이 production configuration과 acceptance-test definition을 문서화한다는 범위로 확인했으며, 보편적인 BOM field list를 주장하지 않는다. 나머지 31개 Anchor는 미검토 또는 주장의 세부범위가 충분히 확인되지 않아 미등록으로 유지한다. 4개 Fact 모두 `score_effect=none`이다. 근거: [NASA Systems Engineering Handbook Appendix D: Requirements Verification Matrix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), [NASA Appendix I: Verification and Validation Plan Outline](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), [NASA Handbook glossary: Product Baseline, Product Verification and Validation](https://www.nasa.gov/reference/system-engineering-handbook-appendix/).

`control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`의 28개 Anchor 중 6개를 ISA guidance와 실제 PLC sequencer 구현 문서로 대조했다. `sw02_sequence_definition`은 공정 sequence/state, 활성 단계의 actions, 조건을 만족한 transition, 구현별 timer·fault supervision이 조합될 수 있음을 확인했다. Timeout·fault policy는 Rockwell 구현 예시이므로 모든 sequence의 필수 동작으로 일반화하지 않았다. `sw02_permissive_definition`은 허가조건이 해당 device/sequence 동작을 enable하는 개념으로 확인했으나, 필수 조건의 개수·AND 구성·적용 전이 시점은 application-specific으로 두었다. `sw02_interlock_definition`은 ISA의 emergency shutdown 예시와 Siemens의 configured safe-position/inhibit 예로 동작을 inhibit/alter하는 제어논리를 알람표시와 구분하되, 실제 action은 application-specific으로 한정했다. `sw02_trip_definition`은 Siemens 안전 시퀀스 예에서 보호 Trip이 정상 sequence step을 reset하며 acknowledgement로 자동 재기동을 방지할 수 있음을 확인했다. latch/reset과 trip state는 보편 의무로 주장하지 않았다. `sw02_feedback_confirmation_timeout`은 Rockwell sequencer의 device/logic feedback으로 단계완료를 판정하고 timeout으로 초과시간을 표시하는 범위로 확인했다. 이 기능만으로 기계적 고장, stuck sensor, sensor disagreement의 원인을 판별한다고 보지 않는다. `sw02_state_entry_exit_actions`는 Siemens SFC의 initialization/processing/termination과 Rockwell의 step activation/deactivation qualifier, 미기록 output이 이전 값을 유지하는 사례를 대조해 action lifecycle 및 output release/retention 관리 필요성을 확인했다. 다만 phase와 qualifier 의미는 구현별이며 모든 step에 세 phase가 필수라고 주장하지 않는다. 나머지 22개 Anchor는 compound claim을 직접 뒷받침할 충분한 근거를 아직 확보하지 못해 미등록 상태다. 여섯 Fact 모두 `score_effect=none`이다. 근거: [ISA, Automating procedures in the continuous process](https://www.isa.org/intech-home/2016/september-october/features/automating-procedures-in-the-continuous-process), [ISA, Passive loopback process simulation](https://www.isa.org/intech-home/2017/november-december/departments/passive-loopback-process-simulation), [Siemens, SIMATIC SFC for S7](https://cache.industry.siemens.com/dl/files/488/21400488/att_61540/v1/s7sfcs7b_e.pdf), [Rockwell Studio 5000 SFC Action documentation](https://www.rockwellautomation.com/en-us/docs/studio-5000-logix-designer/38-03/contents-ditamap/instruction-set/sfc-instructions/action.html), [Rockwell Automation P_Seq Reference Manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/proces-rm006_-en-p.pdf), [Siemens, SIMATIC Control Function Library](https://cache.industry.siemens.com/dl/files/120/109814120/att_1117464/v1/LCFLHMRSenUS_en-US.pdf), [Siemens, Advanced Permissive Sequencing](https://cache.industry.siemens.com/dl/files/865/109770865/att_1000583/v3/109770865_aps_nonlinear_logic_with_safety_matrix_en.pdf).

`radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`에서는 28개 Anchor 중 `radar_pulse_time_of_flight`와 `radar_level_reference_calculation` 두 항목을 Endress+Hauser Micropilot FMR56/FMR57의 ToF 매뉴얼 §Function and system design과 대조했다. 제조사는 기준점부터 표면까지 pulse echo의 왕복 비행시간을 사용하고, measured distance `D`와 설정된 empty distance `E`로 `L=E−D`를 계산한다고 정의한다. 문서에서 확인되지 않은 고압가스 보정, FMCW 동작 세부나 다른 모델의 개별 적용범위까지 확대하지 않았다. 두 Fact 모두 `score_effect=none`이다. 근거: [Endress+Hauser Micropilot FMR56/FMR57, TI01042F/00/EN/11.25-0, p. 7](https://bdih-download.endress.com/files/DLA/005056A500261FD083C4762E39599E59/TI01042FEN_1125-00.pdf).

같은 radar/GWR Pack에서 앞서 기록한 `radar_pulse_time_of_flight`와 `radar_level_reference_calculation`에 더해 확인한 10개 Anchor는 FMCW 전자기파·스윕·beat-frequency 거리식, Fresnel 반사계수, GWR의 TDR 구성, false-echo mapping, 안테나 빔과 기체상 전파속도다. 각 항목은 제조사 문서 또는 조건을 명시한 계산에 한정했다.

`radar_bandwidth_range_resolution`은 TI의 대역폭 기반 two-target resolution, BIPM VIM의 accuracy/repeatability 정의, Infineon의 FFT bin 관계, 동료심사 FMCW 연구의 SNR·주파수/위상 추정·chirp 선형성 영향을 대조했다. `radar_low_dielectric_echo_margin`은 Endress+Hauser FMR57의 저유전율·poor-reflection에 따른 범위 제한, Emerson 5408의 약한 echo·antenna gain·surface orientation 지침, echo-quality 진단으로 검증했다. 제조사 고유 적용범위는 다른 모델 전체로 일반화하지 않았다.

이전 검토 시점에는 **28개 중 12개 Anchor를 검증**했다. 당시 나머지 16개는 이번 근거 확인으로 전체 주장 범위를 확인하지 못했으며, 오류 판정이 아니라 미검증 상태다. 등록 Fact는 모두 `score_effect=none`이다. 근거: [VEGA radar](https://www.vega.com/en-us/products/product-catalog/level/radar), [Endress+Hauser Micropilot NMR81](https://bdih-download.endress.com/files/DLA/005056A500261EDEBB9A69E45B7373B7/TI01252GEN_0723-00.pdf), [Texas Instruments FMCW range estimation](https://www.ti.com/video/5415203482001), [TI AWR1243 radar front-end](https://www.ti.com/lit/wp/spyy003/spyy003.pdf), [BIPM VIM accuracy](https://jcgm.bipm.org/vim/en/2.13.html), [BIPM VIM repeatability](https://jcgm.bipm.org/vim/en/2.21.html), [Infineon FMCW DSP](https://www.infineon.com/dgdl/Infineon-FMCW_RADAR_Digital_Signal_Processing_Handout-Training-v01_00-EN.pdf?fileId=8ac78c8c8929aa4d018a178075b06be9), [FMCW range-accuracy study](https://pmc.ncbi.nlm.nih.gov/articles/PMC6767344/), [Endress+Hauser Levelflex FMP40](https://portal.endress.com/wa001/dla/5000079/2669/000/02/BA243FEN.pdf), [E+H WP01077F guided radar](https://bdih-download.endress.com/file/005056A5E3831EDBB8DDE8FF36B03140/WP01077F00EN0118.pdf), [VEGA VEGAFLEX 81](https://www.vega.com/en-ca/products/product-catalog/interface/guided-wave-radar/vegaflex-81), [E+H FMR245](https://bdih-download.endress.com/files/DLA/4E0914F8AE6421F2E10000000A35E042/BA00253FEN_1311.pdf), [E+H FMR531](https://bdih-download.endress.com/files/DLA/4A689A5096252380E10000000A35E042/BA207FEN_0409.pdf), [Emerson Rosemount 5408 manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-5408-non-contacting-radar-transmitter-202470.pdf), [Emerson 5408 Smart Echo Supervision](https://www.emerson.com/en/measurement-instrumentation/products/rosemount-5408-non-contacting-radar-transmitter), [E+H high-pressure radar propagation note](https://www.ca.endress.com/_storage/asset/4766645/storage/master/file/15366622/download/EHtalkline82.pdf), [E+H FMR57 application limits](https://www.apsc.endress.com/en/field-instruments-overview/level-measurement/Radar-Micropilot-FMR57).
추가 검토에서 `radar_mounting_nozzle_obstruction_error`를 검증했다. Emerson Rosemount 5408 문서는 기종별 nozzle diameter/height, liquid-surface 수직 정렬, 약한 solids echo에 대한 경사면 정렬을 제시하고, Endress+Hauser FMR51/FMR52 문서는 antenna별 nozzle 높이·직경, recessed mounting, near-range echo 및 maximum level 제한을 설명한다. 이 근거는 설치치수를 타 모델에 일반화하지 않도록 범위를 제한한다. 근거: [Emerson Rosemount 5408 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-5408-non-contacting-radar-transmitter-202470.pdf), [Endress+Hauser Micropilot FMR51/FMR52 TI01040F](https://bdih-download.endress.com/files/DLA/005056A500261EDAB3AE2266BFE11B4D/TI01040FEN_1020.pdf).

이후 `radar_antenna_buildup_condensation`을 추가 검토했다. Emerson 5408 매뉴얼은 안테나 부착물을 측정 교란 원인으로 들고 세척 또는 호환 기종의 에어 퍼지를 권고한다. 동일 제조사는 중응축·공격성 매질에 process-seal 안테나를 제시하고, 신호품질 진단을 예방정비에 연결한다. 노즐 단열·열추적은 황 증기 서비스 사례에 한정해 기록했으며 모든 레이더에 필요한 보편 조치로 확대하지 않았다. Emerson 5400 자료의 퍼지도 해당 연결부·모델 및 먼지 조건에 한정했다. 근거: [Emerson Rosemount 5408 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-5408-non-contacting-radar-transmitter-202470.pdf), [Rosemount 5408 product information](https://www.emerson.com/en/measurement-instrumentation/products/rosemount-5408-non-contacting-radar-transmitter), [Emerson Level Measurement Solutions for Sulfur Pits](https://www.emerson.com/en/measurement-instrumentation/industries/oil-and-gas/level-measurement-solutions-for-sulfur-pits), [Rosemount 5400 Product Data Sheet](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00813-0100-4026.pdf).

`radar_false_echo_multiple_reflection`은 KROHNE의 기술서와 Emerson 5408 매뉴얼로 확인했다. 내부 배관·주입 노즐·교반기 등은 간섭반사를 만들 수 있고, 표면–탱크 지붕/강한 반사체 사이의 다중반사나 벽 반사 경로는 특정 형상에서 잘못된 echo 또는 측정정확도 저하를 유발할 수 있다. 발생 여부와 크기는 탱크 형상·설치·기기별이므로 보편 발생으로 표현하지 않았다.

추가로 `radar_vapor_pressure_temperature_effect`는 KROHNE의 공기/가스 전파속도 비교·조건별 감쇠 설명과 E+H의 가스층 기술자료로 확인했다. 일반 공기·통상 탱크 높이에서 영향이 작다는 설명과 고압 또는 특정 기체(예: 가압 암모니아)의 조건부 예외를 구분했다. `radar_point_target_equation_scope`는 빔을 채우는 대면적 반사체와 빔보다 작은 표적의 거리 의존성을 구분해 R⁻⁴를 액면 전체에 보편 적용하지 않도록 했다. `radar_frequency_antenna_tradeoff`는 개구/파장에 따른 빔폭, FMCW 대역폭 기반 분해능과 제조사 응용 비교를 확인했다. `radar_surface_foam_turbulence_slope`와 `radar_adaptive_threshold_echo_tracking`은 각각 거품·에코 변화·필터 동특성, 5408의 threshold/search window/false-echo suppression 및 E+H tank-history 추적을 모델 범위에 한정해 확인했다. 이번 추가 검토에서 system structure, 모델별 blocking/null zone 정의, pulse/FMCW 방식의 응용별 선정, Levelflex 계면 에코의 상부 매질 지연 및 계면측정 제한 등 5개를 공식 KROHNE·Endress+Hauser·Emerson 문서와 대조했다. 후속으로 `radar_echo_polarity_sign_convention`의 Fresnel 전기장 반사계수는 정상 입사·비자성·손실 없는 유전체 조건에서 계산으로 확인하고, E+H Levelflex의 양·음 envelope echo 설명과 Emerson Rosemount 5300의 모델별 threshold 정의로 실제 표시극성과 물리적 반사 위상을 구분했다. 따라서 polarity Anchor는 verified로 승격했다. `radar_upper_null_zone_overfill_coordination`은 safety requirements와 제품별 불감영역 설정을, `gwr_quasi_tem_return_path`는 일반 probe의 보편 전자기장을 직접 뒷받침할 출처가 아직 부족해 미검증으로 유지한다. 현재 이 Pack은 **28개 중 26개 Anchor를 검증**했고 나머지 2개는 미검증(오류 판정 아님)이다. 모든 Fact는 `score_effect=none`이다. 근거: [KROHNE, Fundamentals of Radar Technology for Level Gauging, 4th ed.](https://cdn.krohne.com/dlc/BR_LEVELRADAR_en_72.pdf), [KROHNE, Radar Level Measurement Systems](https://cdn.krohne.com/dlc/WP_Radar-Level-Measurement-Systems_en.pdf), [TI FMCW range estimation](https://www.ti.com/video/5415203482001), [E+H Solutions for Continuous Level Measurement](https://www.uk.endress.com/_storage/asset/7792226/storage/master/file/24418706/download/Level%2520eBook.pdf), [Emerson Rosemount 5408 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-5408-non-contacting-radar-transmitter-202470.pdf), [Endress+Hauser Levelflex FMP45 Manual](https://bdih-download.endress.com/files/DLA/4ECBD5CF9BD7ED83E10000000A35E035/BA00281FEN_1511.pdf), [Emerson Rosemount 5300 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-00809-0100-4530.pdf), [Endress+Hauser Continuous level measurement selection guide](https://bdih-download.endress.com/file/005056A5E3831FD186F556C786248000/CP00023F00EN2126.pdf).

`process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`에서 이번에 6개를 추가 확인했다. ISA 자료의 feedback-loop block diagram으로 측정·오차·제어기·최종요소 흐름과 단일 feedback의 응답 특성을 확인했다. Ratio-control의 wild-flow→secondary setpoint 관계와 비 정의는 ISA/Wiley 교재 및 Control.com 설명으로 한정했고, feedforward 이상 상쇄식은 선형 중첩 모델에서 직접 유도해 APMonitor 자료와 대조했다. Split-range의 gap에서의 oscillation, 밸브 개방부 비선형성과 range 간 process-gain 차이로 인한 전환 문제 및 remedy는 ISA 전문가 논의와 현장 제어 기술자료로 확인했다. 실제 구현의 안정성·인과성·properness와 전환 tuning은 이상식·범용 규칙과 구분해 조건으로 기록했다. 저유량 ratio 처리와 현장 validation 등의 미검증 앵커는 근거가 직접 닿지 않아 보류한다. 여섯 Fact 모두 `score_effect=none`이다. 근거: [ISA, Essentials of Modern Measurements and Final Elements, Fig. 1-7](https://www.isa.org/getmedia/eb76a613-3961-4db0-8efe-a91dc308ec68/Essentials-of-Modern-Measurements_McMillan_Chapter-1-Essentials.pdf), [ISA InTech, Single-loop control](https://www.isa.org/getmedia/f2b593dd-02c9-4a82-ba9f-e55400564f2e/InTech-May-June-2019.pdf), [ISA/Wiley, Fundamentals of Process Control—Ratio Control](https://onlinelibrary.wiley.com/doi/10.1002/9781394438266.ch14), [Control.com, Ratio Control](https://control.com/textbook/flow-measurements-and-reynolds-numbers/ratio-control/), [APMonitor, Feedforward Control](https://apmonitor.com/pdc/index.php/Main/FeedforwardControl), [ISA Automation.com, Split-range control](https://www.automation.com/article/how-can-we-improve-or-eliminate-split-range-control), [Control Global, Ways to improve split-range control](https://www.controlglobal.com/control/loop-control/article/11300584/ways-to-improve-split-range-control).

`control_valve_gas_sizing_choked_flow_critical_pressure_ratio`에서는 34개 Anchor 중 11개를
Emerson Control Valve Handbook 6판, 전통적 sizing 안내서 및 IEC 60534-2-1과 대조해
등록했다. 검증 범위는 서로 다른 유량 basis와 식 선택, 명시된 standard-volume 기준상태,
절대압력·절대온도, 압력강하비 `x`, `Fγ`, 직접 부착 fitting의 `FP`/`xTP`, choked limit에서의
`xsizing` 및 `Y`, 초크 상태의 유량 거동, 단위별 `N` 상수, 선정 Cv와 제조사 `xT`의 반복
대조다. `Z1`의 구체적 산정, 습증기 2상 물성 경계, 각 운전 시나리오 선정 및 소음 handoff 등
나머지 Anchor는 자료가 전체 문구를 직접 뒷받침하지 않거나 이 감사 범위를 넘어 등록하지 않았다.
검증한 11개 모두 `score_effect=none`이며 채점 점수에는 연결하지 않는다. 근거: [Emerson
Control Valve Handbook, 6th ed.](https://stage.www.emerson.com/content/dam/emerson/en/final-control-fctl/isolation-valves/documents/control-valve-handbook-en-3661206.pdf),
[Emerson Valve Sizing Calculations (Traditional Method)](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351798x012_11.pdf),
[IEC 60534-2-1:2011](https://webstore.iec.ch/en/publication/2461).

`high_temperature_material_strength_oxidation`은 ASME B16.34의 pressure-temperature rating/material
범위와 Fisher의 고온 trim/body material 선정 자료, National Board의 creep·scale·oxidation 설명으로
verified했다. allowable strength 및 압력등급은 재질과 설계금속온도에 따라 확인해야 하며, 산화·스케일·
creep은 실제 환경·응력·시간에 따라 평가하는 손상 메커니즘이다. 이는 모든 고온 서비스에서 모두
발생한다고 단정하는 Anchor가 아니다. `score_effect=none`이다. 근거: [ASME B16.34](https://www.asme.org/codes-standards/find-codes-standards/b16-34-valves-flanged-threaded-welding-end/2017),
[Fisher Steam Conditioning Technologies, Materials of Selection](https://www.emerson.com/is/content/emerson/en/final-control/fctl/solutions/common-applications/steam-conditioning-valves/documents/D352003X012.pdf),
[National Board, Creep and Creep Failures](https://www.nationalboard.org/Index.aspx?pageID=181).

`corrosion_erosion_corrosion`은 AMPP의 chemical/electrochemical corrosion 정의, ASTM G40의 기계적
wear/erosion 범위, ASTM G119의 wear-corrosion 상호작용 평가 목적을 대조해 verified했다. erosion-corrosion은
두 과정의 동시 작용 및 상호작용을 뜻하며, 실제 손상률이 항상 단순 합보다 커진다고 일반화하지 않았다.
현장에서 어떤 기여가 지배적인지는 유체·입자·재료·유속·화학환경을 확인해야 한다. `score_effect=none`이다.
근거: [ASTM G40](https://store.astm.org/g0040-10a.html),
[AMPP, What is Corrosion?](https://www.ampp.org/technical-research/what-is-corrosion),
[ASTM G119](https://store.astm.org/g0119-09r16.html).

`slurry_erosion_impingement`은 solid-particle/slurry 실험과 동료심사 리뷰가 particle impact velocity,
각도, impact frequency/mass flux, 입자 및 target 특성(경도 포함), slurry concentration을 erosion
parameter로 보고한다는 점에서 verified했다. 단, bulk fluid velocity는 particle impact velocity와 같지
않을 수 있고, concentration·각도·경도 효과의 방향과 크기 및 예측식 지수는 재료·입자·유동·시험 조건에
따라 달라진다. 따라서 일반적인 정량 erosion rate law로 확대하지 않았다. `score_effect=none`이다.
근거: [JMRT slurry erosion experiment, 2021](https://doi.org/10.1016/j.jmrt.2021.07.013),
[Yadav et al., slurry erosion review, 2023](https://doi.org/10.1177/14644207221108565),
[ASTM G40](https://store.astm.org/g0040-10a.html).

`high_flow_erosion_vibration`은 Valmet/Fisher의 유속·flash erosion 자료와 고압 배관 유동진동의
피로 손상 사례를 대조해 verified했다. 다만 고유속은 erosion·동적 가진의 한 요인이며, 실제 위치와
속도·크기는 2상/입자 상태, trim 및 배관 형상·재료·지지·공진 조건에 의존한다. JAEA 사례처럼
진동 응력이 피로 허용한계 이하일 수도 있으므로 high flow만으로 손상이나 피로파괴를 확정하지 않는다.
`score_effect=none`이다. 근거: [Valmet Flow Control Manual, §§3.3, 3.7](https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/),
[Fisher Control Valve Handbook, §§5.14.1–5.14.2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf),
[Ziada et al., 2001](https://doi.org/10.1006/jfls.2000.0374),
[JAEA R&D Review](https://rdreview.jaea.go.jp/review_en/2006/e2006_1_4.html).

`process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`에서는
ISA의 Loop Checking 안내서, Fundamentals of Process Control 제15장 및 ISA InTech 자료로
6개 Anchor를 확인했다. Cascade의 master-output→slave-setpoint 구조와 inner-loop의
외란 보상, cascade 채택 시 상대 동특성을 고려해야 한다는 조건, override selector의 선택과
미선택 적분기 reset-windup 보호, split-range의 단일 controller output→복수 final element
범위 배분을 등록했다. 속도비는 특정 튜닝 방법의 휴리스틱으로만 기록했으며 모든 공정에 고정된
법칙으로 주장하지 않는다. Ratio 계산의 저유량 경계, feedforward의 수식/실현성, split-range
응답 전이의 설치 gain 영향, 일반 설계·현장 검증 목록은 Anchor 전체를 직접 지지할 근거가
부족해 보류했다. 후속으로 ratio-control setpoint 방식과 actual-ratio feedback의 차이를
교과서 설명과 미분으로 검증했다. `R=F_controlled/F_wild`의 wild-flow 오차 민감도는
`−F_controlled/F_wild²`이므로 분모가 0에 접근할수록 비율 계산은 ill-conditioned해진다.
따라서 유량 신호를 일관된 물리 단위/질량·체적 기준으로 구성하고, 운전범위에 저유량이
포함되는 경우에 한해 저유량 처리나 setpoint-ratio 구조를 검토한다. 보편적 cutoff는
정하지 않았다. 이후 구조선정 기준은 application-specific 조건을 명시해 verified 등록했다. 현재 이 Topic에서 남은 미등록 Anchor는 `loop_interaction_coordination`과 `field_implementation_validation` 두 개다.
모든 등록 Fact는 점수 중립이다. 근거: [Woolf et al., Chemical Process Dynamics and Controls—Ratio Control](https://eng.libretexts.org/Bookshelves/Industrial_and_Systems_Engineering/Chemical_Process_Dynamics_and_Controls_(Woolf)/11:_Control_Architectures/11.04:_Ratio_control-_What_is_it_When_useful_When_not_Common_usage.),
[ISA Loop Checking](https://www.isa.org/getmedia/946ebd14-8930-42bc-9d7e-5693e3aaf752/LoopChecking_ATechniciansGuide_Jeffery_Chapter1.pdf),
[ISA Fundamentals of Process Control, Chapter 15](https://www.isa.org/getmedia/8a0ae5d3-6761-4bc4-a4d0-798b6618543b/Fundamentals-of-Process-Ctrl-Bouwman-Chapter-15.pdf),
[ISA InTech—Design Principles](https://www.isa.org/intech-home/2016/march-april/features/design-principles-for-complex-process-control),
[ISA InTech—Complex Process Responses](https://www.isa.org/intech-home/2016/september-october/features/loop-tuning-basics-complex-process-responses).

`humidity_measurement_capacitive_resistive_dew_point_selection_compensation`에서는 22개 Anchor
중 21개를 NIST 계량자료, Vaisala 기술자료/제품 가이드, TI 설계세미나, HDK 제품 구동지침, Michell Optidew 제품 설명서에 대조해 등록했다. 검증 범위는
수증기 partial pressure, RH 정의와 온도의 영향, 이상기체 근사의 absolute humidity 관계,
dew/frost point의 액상·고상 구분, 압력 dew point, HUMICAP capacitive polymer의 유전율-용량
변환, 온도 보상, 제조사 문서가 밝힌 특정 sealant outgassing/condensation 관련 drift·hysteresis,
chilled-mirror 측정 원리, psychrometric wet-bulb와 dew-point의 구별, probe 온도차에 따른 RH
오차·결로, 고습 warmed-probe 방식, ultra-dry 조건의 dew/frost-point 선택, reference 기반
calibration/field comparison 및 안정화, resistive humidity element의 저항/임피던스 변화 원리와 일부 polymer element의 AC excitation 요구, TI가 제시한 ESI SRHR-233C 예시의 제한된 RH range 및 비선형 impedance curve다. 또한 필요한 습도 물리량/range와 공정 온도·압력·응축·오염·설치·응답 요구를 모델별 사양에 대조하고 단일 universal instrument가 없다는 제조사 선정 원칙을 확인했다. 저항성 원리는 TI의 polymer/conductive-salt 설명과 HDK HIS-08V 제품 문서의 범위로 한정했고, ESI 응답 예시도 모든 resistive sensor에 일반화하지 않았다. 위험지역 적합성은 별도 인증 기준으로 분리했다. HUMICAP·warmed-probe 관련 내용은 문서화된 제품 구성과
노출 예시로 한정했고 모든 humidity sensor에 일반화하지 않았다. Michell Optidew 설명서의 mirror/optics 세정과 오염경고 후 DCC 절차는 특정 제품에 한해 확인했으며 chilled-mirror 전체의 보편적 유지보수 부담으로 일반화하지 않았다. replacement/spare/shutdown/lifecycle을 모두 묶은 운영선정 Anchor는 확인 자료가 Anchor 전체를 뒷받침하지 못해 보류했다. 새 Fact는 모두
`score_effect=none`이다. 근거: [NIST Humidity Metrology](https://emtoolbox.nist.gov/wavelength/documentation.asp),
[NIST SP 250-83 Rev. 1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.250-83r1.pdf),
[NIST dew-point/RH definitions](https://nvlpubs.nist.gov/nistpubs/jres/74c/jresv74cn3-4p117_a1b.pdf),
[Vaisala HUMICAP HMM170 Guide](https://docs.vaisala.com/r/M212259EN-D/en-US/GUID-483A8D7D-0A10-4A90-980A-CB88E2F4CD51),
[Vaisala RH test-chamber guidance](https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers),
[Vaisala warmed-probe guidance](https://www.vaisala.com/en/blog/2020-10/measuring-humidity-condensing-environments),
[Vaisala ultra-dry measurement guidance](https://www.vaisala.com/en/expert-article/why-choose-dew-pointfrost-point-temperature-over-relative-humidity-or-ppm-measurements-ultra-dry-conditions), [TI Precision Analog Applications Seminar](https://www.ti.com/lit/pdf/slyp160), [HDK resistive humidity sensor driving method](https://www.hdk.co.jp/pdf/tece/appe_krh1901003.pdf).

`control_valve_deadband_stiction_response_time_positioner_dynamic_performance`에서 deadband의
방향반전 입력구간 정의, backlash의 연결부 lost-motion 범위, hysteresis의 상·하향 응답 차이,
정지 물체의 움직임을 시작하기 위한 static-friction 극복 요건을 ISA/Emerson 자료와 기계학적
정의로 교차 확인해 등록했다. 모두 `score_effect=none`이다. `stiction_stick_then_jump`는 정지마찰
극복 후 응답한다는 핵심은 지지되지만, 허용 설명에 든 packing·alignment·deposit·thrust margin의
원인 목록을 이번 근거로 모두 검증하지 못해 등록하지 않았다.

`bode_frequency_response_stability_margin_bandwidth`의 `open_loop_closed_loop_roles`에서
비단위 피드백에도 `T=L/(1+L)`를 적용한 일반화 오류를 수정했다. 음의 피드백의 일반식은
`T=G/(1+GH)`이며 `T=L/(1+L)`은 `H=1`인 특수 경우다. 루프 전달함수와 폐루프 reference-to-output
전달함수의 구분을 Topic Pack의 Grading source에 반영하고, 재현 가능한 블록대수와 MIT OCW 강의자료의
기존 독립 근거를 정합시켰다. 점수 영향은 없다.

Ultrasonic Topic의 `ultrasonic_round_trip_distance_equation`은 반사형 펄스 에코에서
측정시간이 센서→대상물→센서의 왕복시간이므로 한 방향 거리 `d=ct/2`라는 관계를
제조사 기술자료로 직접 대조했다. `ultrasonic_sound_speed_medium_dependence`와
`ultrasonic_air_temperature_compensation`은 음속이 전달 매질의 온도·조성 조건에 영향을 받고,
해당 경로를 대표하지 않는 음속값을 사용하면 거리환산에 편향이 생긴다는 범위로 검증했다.
근거: [Baumer, Ultrasonic sensors—function](https://www.baumer.com/pl/en/service-support/function-principle/ultrasonic-sensors---function/a/Know-how_Function_Ultrasonic-sensors), Distance measurement; [Siemens/Milltronics HYDRO+ manual](https://support.industry.siemens.com/cs/attachments/18161433/7ML19981AC02.3.pdf), Sound Velocity; [Emerson/Rosemount 3100 manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf), §F.3.29. 세 Fact는 제조사 근거로 확인했고 `source_refs`는 비어 있어 WordPress 자료를 사실 근거로 사용하지 않았다. 점수 영향은 없다.

같은 Topic에서 `ultrasonic_piezoelectric_transduction`, `ultrasonic_pulse_echo_time_of_flight`,
`ultrasonic_sensor_crosstalk`도 제조사 기술자료와 대조했다. 압전소자의 송·수신 변환과 송신부터
반사 에코 복귀까지의 시간 측정은 ifm의 동작 원리 설명으로 확인했다. 센서 간 크로스토크 가능성은
ifm 설치 지침과 Pepperl+Fuchs의 동기화·멀티플렉싱 안내로 교차 확인했다. 구체적 간격과 동기화 방식은
제품 및 배치조건에 종속되므로 보편 수치로 일반화하지 않았다. [ifm, Ultrasonic technology overview](https://www.ifm.com/us/en/us/learn-more/ultrasonic/full-metal-ultrasonic/technology), [Pepperl+Fuchs, Synchronization and Common Mode](https://blog.pepperl-fuchs.com/en/2019/ultrasonic-sensor-faq-synchronization-and-common-mode/). 이들 항목도 `source_refs` 없이 독립 확인했고 점수 영향은 없다.

`ultrasonic_target_reflectivity_orientation`은 제조사 자료 두 곳에서 교차 확인했다. 대상물의 크기,
방향, 표면 거칠기와 음향반사 특성이 반사 에코 및 검출거리·정확도에 영향을 주며, 표면과 배치에
따라 성능 차이가 있으므로 보편적 각도나 거리를 고정하지 않았다. [microsonic installation instructions](https://www.microsonic.de/en/service/ultrasonic-sensors/installation-instructions), [Senix distance and level sensor FAQ](https://senix.com/faqs/). `source_refs`는 없고 점수 영향은 없다.

`ultrasonic_beam_angle_footprint`은 ifm 응답곡선 설명(거리별 빔 폭·검출영역)과 Rosemount 3100
설치 지침(해당 모델의 6° 반각 및 빔 안 장애물의 허위 에코)을 대조해 검증했다. 각도나 간격은
다른 모델에 일반화하지 않았다. `ultrasonic_level_measurement_reference`는 Rosemount 3100의
bottom-reference 구성에서 액면 높이를 기준점과 측정거리의 차이로 계산하며, offset 보정을 별도
적용하는 계산 절차를 통해 확인했다. 자료: [ifm response curves](https://www.ifm.com/us/en/us/learn-more/position/ultrasonic/technology), [Rosemount 3100 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf), §§3.3.1, 4.3.2, Appendix F. 두 Fact는 `source_refs` 없이 독립 확인했고 점수 영향은 없다.

추가로 `ultrasonic_false_echo_multiple_reflection`, `ultrasonic_echo_amplitude_validity`,
`ultrasonic_mounting_nozzle_obstruction_error`를 Endress+Hauser Prosonic 및 Rosemount 3100
매뉴얼과 대조했다. Tank fittings 및 multiple reflections가 간섭 에코를 만들 수 있고 실제 액면
에코와 혼동될 수 있다는 근거를 확인했다. Echo size는 신호 진단으로 제시되며, 거리는 ToF와 음속으로
계산된다. 노즐 돌출 길이 5 mm와 수직 설치는 Rosemount 3100에 한정된 기기별 설치요건으로 기록했다.
[Endress+Hauser Prosonic M Operating Instructions](https://bdih-download.endress.com/files/DLA/4F7C96183550A513E10000000A35E042/BA00240FEN_1311.pdf), [Rosemount 3100 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf). 점수 영향은 없다.

`ultrasonic_foam_vapor_turbulence_error`는 복합 주장을 조건부 범위로 대조했다. Rosemount 3100은
foam에 따른 반환 에코 감소를 설명하고, Siemens HYDRO+는 가스/증기 조성과 온도·증기압의 음속
영향을 다룬다. Pepperl+Fuchs는 강한 dust loading으로 인한 acoustic energy/range 감소와 난류·경계층의
산란·편향을 설명한다. 이는 모든 먼지·증기·파동 조건이 항상 측정오차를 만든다는 뜻이 아니며 영향은
크기와 장치·경로 조건에 종속된다. [Rosemount 3100 manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf), [Siemens HYDRO+ manual](https://support.industry.siemens.com/cs/attachments/18161433/7ML19981AC02.3.pdf), [Pepperl+Fuchs external influences](https://blog.pepperl-fuchs.com/en/2018/ultrasonic-sensor-faq-external-influences-on-sensor-operation/). 점수 영향은 없다.

`ultrasonic_dead_zone_ringdown`과 `ultrasonic_sensor_system_structure`도 확인했다. TI와
Pepperl+Fuchs는 monostatic 트랜스듀서 잔류 진동이 근거리 blind zone을 만든다고 설명한다. ADI
CN0343은 송신 펄스 감쇠 시점까지 수신부를 blanking하는 설계와 그 blanking 시간에 따른 최소 측정거리를
보여준다. 시스템 구성 앵커는 고정된 하드웨어 분할이 아니라 송신·변환·수신·ToF·보상·출력 기능을
뜻하도록 해석했다. TI는 discrete/AFE/ASSP/MCU 통합 구현을 나열하고, ADI는 한 구체적 구현을 제시한다.
[TI SLAA907D](https://www.ti.com/lit/an/slaa907d/slaa907d.pdf), [Pepperl+Fuchs UC manual](https://files.pepperl-fuchs.com/webcat/navi/productInfo/doct/tdoct0736__eng.pdf?v=20230403152657), [ADI CN0343](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0343.html). 점수 영향은 없다.

같은 Topic의 `ultrasonic_frequency_range_resolution_tradeoff`는 공기 중 초음파 거리측정에 범위를 한정했다. TI는 주파수가 높아질수록 공간 분해능이 높고 지향성이 좁아지는 반면 감쇠가 커지고 측정거리가 짧아지는 일반 경향을 제시한다. `ultrasonic_attenuation_max_range`는 송신 음압·경로 감쇠·빔/응답 기하·표적 크기와 반사특성·수신감도가 검출 가능 거리를 함께 좌우하는 시스템 조건으로 한정했다. 특정 센서의 정격거리나 보편 수치는 주장하지 않았다. 근거: [TI SLAA907D, §§2.5–2.6 and Fig. 2-8](https://www.ti.com/lit/an/slaa907d/slaa907d.pdf), [ADI CN0343, Ultrasonic Measurement Theory](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0343.html), [ifm, Ultrasonic technology](https://www.ifm.com/us/en/us/learn-more/position/ultrasonic/technology), [microsonic, Installation instructions](https://www.microsonic.de/en/service/ultrasonic-sensors/installation-instructions). 점수 영향은 없다.

회전속도 계측 Topic의 `proximity_airgap_target_error`는 근접형 기어 톱니 센서에 대해 대상 재질·크기·톱니 대 간극 비·설치 간격이 제조사 sensing 조건을 좌우함을 확인했다. 축/대상의 runout이나 진동은 운전 간극을 바꾸는 경우에만 검출 여유와 출력특성에 영향을 줄 수 있으며, 보편 dropout 한계는 주장하지 않았다. 근거: [ifm, Inductive sensor technology overview](https://www.ifm.com/us/en/us/overview/inductive/technology-overview/tech-overview), [ifm, Compact speed monitor installation guidelines](https://www.ifm.com/us/en/us/learn-more/motion-control/speed-sensors/di-learn-more/installation-guidelines), [Allegro ATS685LSH datasheet](https://www.allegromicro.com/-/media/files/datasheets/ats685-datasheet.pdf). Allegro는 Hall 기어톱니 센서 자료로서 진동·동적 간극변화 메커니즘만 보강하며, 유도형 센서와 감지 원리를 동일시하지 않았다.

`tachogenerator_direction_loading_error`는 영구자석 DC 타코제너레이터의 속도비례 출력과 회전방향에 따른 단자 극성, 부하에 따른 단자전압 저하, 자석 온도계수, 브러시·정류자 리플/고조파, 장착·커플링 오차에 따른 추가 고조파를 제조사 자료로 확인했다. 수치·보상·허용부하는 모델별 사양으로 한정했고 일반적인 zero 오차값을 만들지 않았다. 근거: [Hübner TDP 1,2 catalog](https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-catalog-en.pdf), [Hübner TDP 1,2 operating manual](https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-user-manual-en.pdf), [maxon DC-Tacho DCT 22](https://www.maxongroup.com/maxon/view/product/sensor/dctacho/118910), [maxon Motors as Generators](https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators). 점수 영향은 없다.

`selection_speed_range_low_high`는 encoder 기반 속도측정 및 overspeed monitoring에 한정해 검증했다. 저속 측정분해능은 counts/rev와 평가주기에 좌우되고, 고속 한계는 센서/입력 주파수와 기계 정격에 좌우된다. 안전 overspeed·acceleration 감시에서는 response time과 분해능의 관계도 장치 문서에 명시돼 있다. 시작·creep RPM이나 가속도 수치를 모든 센서에 공통 적용하지 않고 해당 모델·제어기 사양으로 제한했다. 근거: [maxon, Encoder: minimum speed](https://support.maxongroup.com/hc/en-us/articles/360007824054-Encoder-minimum-speed), [maxon, Encoder Selection – Speed Control](https://www.maxongroup.com/en-us/knowledge-and-support/blog/encoder-selection-part-three-speed-control-25728), [Rockwell PowerFlex Safe Speed Monitor manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/750-rm001_-en-p.pdf), [Pepperl+Fuchs Rotation Speed Monitor](https://files.pepperl-fuchs.com/webcat/navi/productInfo/pds/231209_eng.pdf). 점수 영향은 없다.

`mechanical_mounting_coupling_error`는 원래의 encoder와 tachogenerator 전체에 대한 misalignment·radial/axial load·runout·loose mount·torsional vibration·slip 복합 주장을 그대로 승인하지 않았다. Anchor를 EPC hollow-bore encoder 및 Hübner TDP 1,2에 특정하고, 정렬·runout·radial/axial shaft load가 정확도·bearing life·vibration/harmonics에 미치는 제조사 문서상 효과로 한정했다. EPC 가이드는 shaft runout/bore misalignment의 정확도·bearing life 영향과 권장 alignment/load를, Hübner §7.3.1은 zero-play flexible coupling, centering, radial eccentricity limit, shaft load 회피 및 misalignment harmonics를 명시한다. coupling slip과 보편 torsional-vibration error는 제외했다. 근거: [EPC General Installation & Wiring Guide](https://www.encoder.com/hubfs/pdf-downloads/general-info-installation-troubleshooting/general-installation-wiring-guide.pdf), [Hübner TDP 1,2 Operating and Assembly Instructions](https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-user-manual-en.pdf), [HEIDENHAIN coupling product information](https://www.heidenhain.com/fileadmin/pdf/en/01_Products/Produktinformationen/PI_ROC415_ROC417_ID627679_en.pdf). Fact `score_effect=none`이다.

DP transmitter manifold Topic에서 `bleed_vent_service_location`은 기존에 verified로 등록되어 있다. 이번 재검토는 `manifold_isolation_sequence`와 `manifold_return_sequence`의 적용범위가 잘못 섞였음을 확인했다. 공식 Rosemount 3051 Coplanar 매뉴얼은 zero trim 시 low-side isolate close → equalize open, 완료 후 equalize close → low-side isolate open 절차를 설명하지만, 이 단계는 plant maintenance isolation·depressurization·LOTO를 정의하지 않는다. 해당 Pack이 이미 사람 승인된 managed source이므로 canonical source, model answer 및 registry를 이 두 anchor에 대해 수정·승격하지 않았다. 현재 주장은 미검증으로 남기고, 후속 사람 승인 제안만 아래에 기록한다.

수동 R·C·L 센서 Topic에서 `sensor_rcl_excitation_signal_conditioning`은 브리지·복조·선형화·ADC를 모든 센서가 거치는 단일 필수 사슬처럼 단정한 표현을 바로잡았다. `sensor_rcl_sensitivity_linearity_environment`는 미분 가능한 직렬 변환단에서 연쇄법칙으로 국부감도를 구하는 점과 성능 간 trade-off가 조건 의존적임을 분리했다. `sensor_rcl_calibration_implementation_validation`은 교정관계와 요구 성능 확인을 유지하면서 개별 특성시험은 적용성에 따라 선정하도록 범위를 한정했다. NIST의 센서 핸드북은 교정관계와 민감도·선형성·히스테리시스·반복성의 의미를 구분하고, NIST 불확도 지침은 측정방법 및 연구설계에 따라 불확도 요소가 달라짐을 밝힌다. 근거: [ADI CN-0371 LVDT](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0371.html), [ADI AD7745/AD7746](https://www.analog.com/media/en/technical-documentation/data-sheets/AD7745_7746.pdf), [NI Sensor Terminology](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/sensor-terminology.html), [NIST Sensor Handbook](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication615.pdf), [NIST TN 1297](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d4-measurand-defined-measurement-method), [NIST e-Handbook](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc46.htm). 등록 Fact는 `score_effect=none`이다.

Control valve characteristics Topic의 `control_valve_commissioning_characteristic_verification`은 제조사 inherent curve나 stroke test만으로 installed flow characteristic이 입증되지 않음을 구분했다. Installed 특성은 실제 계통에서 flow와 assembly input/travel 관계이며 valve pressure drop이 시스템에 따라 변하므로, 현장 평가를 수행하는 경우 흐름·travel·압력 조건을 해당 범위와 안전한 commissioning 계획에 따라 비교한다. 전체 유량곡선 시험이 모든 시운전에 보편적 의무인 것처럼 확대하지 않았다. 근거: [Emerson/Fisher Control Valve Handbook, §2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [ISA, Using Control Valve Installed Gain Calculations](https://www.isa.org/intech-home/2021/december-2021/features/using-control-valve-installed-gain-calculations). 등록 Fact는 `score_effect=none`이다.

SIL 수명주기 Topic에서 `srs_lifecycle_handoff`는 HSE가 요약한 BS EN 61511의 위험평가부터
설계·검증·운전·proof-test·변경관리·폐기까지의 수명주기 원칙으로 확인했다. 다만 구체적 SRS
항목 전체는 적용 표준과 프로젝트 요구사항에 맡기고, HSE 요약만으로 임의 확정하지 않았다.
`operations_moc_revalidation`은 HSE COMAH 지침이 요구하는 SIS 유지보수, proof-test 주기 근거,
SIS 변경절차와 설계 기능안전 유지 목표까지 확인했다. Anchor의 모든 운전 데이터 필드가 보편적
의무 기록이라고 확대하지 않았다. 두 Fact 모두 `score_effect=none`이다.

근거: [HSE Functional safety](https://www.hse.gov.uk/eci/functional.htm), [HSE COMAH C&I assessment guidance](https://www.hse.gov.uk/comah/sragtech/discguidciindex.htm).

`feedback_system_closed_loop_sensitivity_steady_state_error`의 `feedback_field_design_validation`은
MathWorks 제어설계 자료에서 시간·주파수응답과 안정여유 분석, sensitivity/noise와 disturbance 설계,
포화·anti-windup, delay, prefilter/feedforward 구성 및 비선형 모델 검증을 확인했다. 이를 모든 루프에
동일한 시험을 강제하는 규격으로 해석하지 않고, 적용 구조와 운전위험에 맞게 선택하는 현장 검토항목으로
한정해 verified 등록했다. 점수 영향은 없다.

근거: [MathWorks, Validate Tuned Control System](https://www.mathworks.com/help/control/ug/validate-tuned-control-system.html), [Anti-Windup Control Using PID Controller Block](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html), [Frequency-Domain Specifications](https://www.mathworks.com/help/control/ug/frequency-domain-specifications.html), [Control System Designer Tuning Methods](https://www.mathworks.com/help/control/ug/control-system-designer-tuning-methods.html).

생산관리 Topic의 `production_takt_cycle_time_boundary`는 Lean Enterprise Institute의 정의로 확인했다.
Takt time은 같은 기간 기준 가용 생산시간/고객수요이며 수요가 정하는 생산 pace이고, cycle time은
실제 공정·설비에서 관찰한 제품/공정 처리시간이다. 설비·작업자 cycle time의 세부 구성은 정의별로
다를 수 있으므로 둘을 동의어로 취급하지 않는다. 점수 영향은 없다.

근거: [Lean Enterprise Institute, Takt Time](https://www.lean.org/lexicon-terms/takt-time/), [Cycle Time](https://www.lean.org/lexicon-terms/cycle-time/).

같은 생산관리 Topic의 `production_bottleneck_throughput_constraint`는 NIST의 제조시스템 분석과
동료심사 serial-line 연구로 확인했다. 병목은 운전조건에 따라 시스템 산출을 가장 강하게 제한하는
자원이며, finite buffer의 blocking/starvation도 처리량에 영향을 준다. 따라서 비병목 설비의 국부
효율 개선이 전체 throughput의 동일 비율 증가를 자동 보장하지 않는다는 범위로 verified했다.
점수 영향은 없다.

근거: [NIST, Manufacturing System Design and Analysis](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=923721), [Kuo, Lim & Meerkov, Bottlenecks in serial production lines](https://doi.org/10.1155/S1024123X96000348).

생산관리 Topic의 `production_oee_apq_formula_boundary`는 Lean Enterprise Institute의 APQ 곱셈
정의와 Availability·Performance·Quality 손실 설명, ISO 22400-2의 KPI formula/context 원칙 및
KPI만으로 management/execution을 충족하지 못한다는 주의, NIST의 OEE productivity 용도를 대조해
확인했다. 각 분모·대상·시간범위의 정의를 일관되게 고정하고, OEE를 납기·원가·안전·수요대응 전체의
대리 지표로 쓰지 않는 범위다. 점수 영향은 없다.

근거: [Lean Enterprise Institute, Overall Equipment Effectiveness](https://www.lean.org/lexicon-terms/overall-equipment-effectiveness/), [ISO 22400-2](https://www.iso.org/obp/ui/?_escaped_fragment_=iso%253Astd%253A54497%253Aen), [NIST, Methods and Tools for Performance Assurance of Smart Manufacturing Systems](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920944).

`production_horizon_master_detailed_schedule`는 SAP 공식 문서에서 장기 시뮬레이션 계획, 중요 완제품·조립품을 먼저 별도 계획하는 MPS, BOM 하위 단계의 종속요구, 자원·자재 가용성을 고려하는 PP/DS 상세일정의 구분을 확인했다. 계획층위는 확인했지만, 이를 모든 기업의 고정 기간 구간으로 일반화하지 않도록 주·월 등 horizon 길이는 운영정책별로 다르다고 한정해 verified했다. 점수 영향은 없다.

근거: [SAP Long-Term Planning](https://help.sap.com/docs/PRODUCT_ID/feded183701e4ba0b42bc4fc31ad7a12/7073b6535fe6b74ce10000000a174cb4.html), [Master Production Scheduling Procedure](https://help.sap.com/docs/SAP_ERP/85d3fce10e264972a0155c8b46ecf93b/0fadce5314894208e10000000a174cb4.html), [Production Planning and Detailed Scheduling](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/21aead0c98bd4755abdacd91c99e3393/f431c95360267614e10000000a174cb4.html).

상태공간 Topic의 `pole_placement_conditions`는 완전 제어가능 LTI 쌍에 대한 임의 극점배치
정리와 제어 불가능 모드의 불변성을 확인해 등록했다. `ackermann_and_numerical_limits`는
Ackermann 식의 제어가능성 행렬 역행렬 요건을 MIT 강의자료에서 확인하고, pole-assignment
수치 민감도는 조건수에 의존한다는 점을 동료심사 논문으로 교차 확인했다. 따라서 “고차라서
항상 민감하다”는 식의 단정은 피하고 ill-conditioning일 때 수치 위험이 커진다는 범위로
제한했다. 두 항목 모두 점수 영향은 없다.

같은 Topic의 `separation_principle_conditions`는 University of Illinois ECE 486의 상태/오차
좌표 유도와 특성다항식 인수분해를 확인했다. 독립 임의 배치는 각각 제어가능성·관측가능성을
요구한다는 조건을 명시했다. `reference_tracking_integral_action`은 MIT OCW 예제에서 극점
배치 후에도 DC 이득 및 계단 정상오차가 자동으로 정해지지 않는 사례와 precompensator 계산을
확인하고, 별도의 MIT 자료로 적분 상태 방식도 교차 확인했다. 모델 정확도·폐루프 안정성·실현
가능성 조건을 붙였으며 둘 다 점수 영향은 없다.

`implementation_tradeoffs_validation`은 control effort, observer noise sensitivity,
sampling/model mismatch와 검증 권고를 한 Anchor에 결합하고 있다. 현재 확인한 자료만으로
모든 세부 주장을 동일한 조건 범위에서 검증하지 못해 등록하지 않았다. 이는 해당 권고가
틀렸다는 판정이 아니라, 세부 claim별 근거를 더 확인하기 전까지 보류한다는 뜻이다.

## 2026-10-10 추가 검토: 제어기 운전·설계 Anchor

다음 4개 Topic의 현장/설계 Anchor를 MathWorks 공식 문서 및 ISA InTech 기술문서와
대조했다. 문서가 확인하는 하위 사실과 Pack Anchor 전체의 범위가 다르면 Anchor를
`verified`로 올리지 않았다.

| Topic / Anchor | 확인 결과 | 처리 |
|---|---|---|
| `pid_controller_tuning_sequence_gain_effects` / `i_action_effect` | 안정·단위 음의 피드백, 유한한 비영 DC 이득, 비포화, 적분기 비상쇄 등 조건에서 단위 계단 정상상태 오차가 0임을 최종값 정리로 유도했다. 포화 시 적분 windup 가능성은 MathWorks 문서로 확인했다. | 조건을 명시해 verified 등록; 점수 영향 없음 |
| `pid_controller_tuning_sequence_gain_effects` / `general_tuning_sequence` | ISA InTech의 manual-tuning 사례는 I·D를 끄고 P를 안정화한 뒤 I를 추가하며, D는 필요에 따라 선택한다고 설명한다. 이를 보편 절차로 일반화하지 않고 해당 접근법의 사례로 한정했다. | 범위를 한정해 verified 등록; 점수 영향 없음 |
| `pid_controller_tuning_sequence_gain_effects` / `pi_controller_common_in_process_control` | UNIDO 교육자료와 IChemE 기술 기고는 공정에서 PI가 흔히 쓰이는 점, D의 잡음 증폭, D 추가 시 재튜닝 난이도, 노이즈에 따른 최종요소 과도 동작과 마모·고장 가능성을 각각 설명한다. “유지보수 부담”은 모든 D 적용의 필연 결과가 아니라 이 실무 위험을 가리키는 조건부 표현으로 제한했다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `pid_controller_tuning_sequence_gain_effects` / `field_constraints` | ISA는 공정 dead time/time constant를 식별해 튜닝에 반영하고, 계기·최종요소 성능, 밸브 deadband/stiction, 노이즈 필터와 이에 따른 재튜닝, output limit/anti-windup, 실행주기, derivative filter와 bumpless 전환을 적용성에 따라 확인하도록 설명한다. 별도 ISA 자료는 stiction이 반복 움직임과 장비 wear를 키울 수 있음을 다룬다. | 항목별 scope와 “as applicable” 조건을 명시해 verified 등록; 점수 영향 없음 |
| `lead_lag_compensator_phase_margin_steady_state_error` / `lead_lag_lead_bandwidth_noise_effort_tradeoff` | 표준 연속 lead 함수에서 고주파/DC 이득비가 `1/α`임을 계산으로 확인했다. MathWorks는 안정여유·대역폭 증가와 상승시간 감소를, 미시간대 CTMS는 고주파 이득 증가에 따른 측정 노이즈 증폭 가능성을 설명한다. 포화 발생은 보장되지 않으며 신호 크기와 액추에이터 한계에 좌우된다고 범위를 제한했다. | 조건부 Fact로 verified 등록; 점수 영향 없음 |
| `lead_lag_compensator_phase_margin_steady_state_error` / `lead_lag_plant_robustness_limits` | MIT OCW는 비최소위상 영점이 대역폭을 제한하는 rule of thumb, 순수 지연의 `−ωT` 위상손실과 보상 한계를 설명한다. 기존의 포화·공진·센서·액추에이터 대역폭·불확실성까지 포괄하는 단정은 제외하고, 직접 근거가 있는 RHP zero와 delay로 범위를 축소했다. | 범위를 좁혀 verified 등록; 점수 영향 없음 |
| `lead_lag_compensator_phase_margin_steady_state_error` / `lead_lag_implementation_validation` | MathWorks는 제어기 검증을 명시 요구조건과 관련 응답에 따라 하고, 선형화로 튜닝한 Simulink 제어기는 전체 비선형 모델로 확인하도록 설명한다. 무관한 시험항목까지 일률적으로 요구하지 않도록 수정했다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` / `thermocouple_type_material_range_atmosphere_selection` | IEC 60584-1의 type별 EMF 기준함수·허용오차, 제조사 자료의 type별 environment 및 선경에 따른 사용범위를 확인했다. 기존 광범위한 선택 체크리스트는 type, 온도·환경 요구와 probe construction으로 좁혔다. | 범위를 좁혀 verified 등록; 점수 영향 없음 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` / `thermocouple_calibration_tolerance_uncertainty_drift` | IEC는 type별 reference/tolerance 조건을 정하고, NIST의 comparison/fixed-point 방법 선택과 Type T 교정 불확도 예시는 교정 절차에 따라 budget 항목이 달라짐을 뒷받침한다. 모든 측정에 동일한 요소 목록을 강제하지 않도록 수정했다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` / `thermocouple_fault_diagnostics_open_polarity_cjc_validation` | Fluke는 correct polarity·compatible extension wire·clean connections 및 CJC reference path를 설명한다. NI와 Emerson은 open-circuit detection이 input device에 따라 지원 여부와 한계가 다름을 명시한다. 따라서 모든 진단 항목을 일괄 의무화하지 않고 end-to-end 경로를 조건부 점검하도록 범위를 정리했다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_design_objective` | UIUC pole-placement 강의는 pole placement와 reference scaling을 구분하고, integral action은 상수 추종·외란 요구에 대한 별도 내부모델 수단으로 설명한다. 안정화 자체와 추종 조건을 혼동하지 않도록 좁혔다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_robustness_noise_gain_tradeoff` | MIT OCW는 observer gain을 높여 오차수렴을 빠르게 하면 측정잡음과 모델오차 영향이 커질 수 있다고 설명한다. MathWorks는 actuator saturation 시 integral windup과 anti-windup 수단을 설명한다. 검증되지 않은 포괄적 “모든 성능 악화” 목록은 제거했다. | 범위를 좁혀 verified 등록; 점수 영향 없음 |
| `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_implementation_validation` | MathWorks 및 UIUC 자료에 따라 검증을 설계 요구와 실제 state augmentation/observer/implementation 구조에 연결했다. 적용되지 않는 검사까지 모든 설계에 강제하는 열거를 제거했다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `flashing_service_geometry_location` | Emerson은 `P2 < Pv`에서 flashing이 지속되고 밸브 자체가 상변화를 방지할 수 없으며, 손상 저감이 유속·유량·압력·유체·geometry·재질 등에 의존한다고 설명한다. 손상 intensity를 정량 예측하는 보편식도 없다고 밝혀, 단일 고정 checklist가 아닌 적용별 저감 원칙으로 문구를 좁혔다. | 조건부 범위로 verified 등록; 점수 영향 없음 |
| `second_order_lag_response_by_damping_ratio` / `so2_design_tradeoff` | 표준 2차계의 감쇠비와 응답 특성은 기존 이론 앵커와 구분되지만, 목표 감쇠비를 설비 보호·구동기 한계 등으로 선택한다는 설계 판단에는 이 검토에서 적합한 출처를 확보하지 못했다. | 보류: 설계 권고의 범위를 뒷받침할 자료 필요 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` / `feedback_field_design_validation` | MathWorks/ISA 자료는 일부 고려사항(필터와 재튜닝, 밸브 deadband, 안정여유, 포화 처리)을 지원한다. 샘플링·통신지연·set-point prefilter·feedforward 및 열거된 검증 묶음 전체의 근거는 충분히 확인하지 못했다. | 부분 근거만 확인, Anchor 단위 승격 보류 |

확인한 자료: [MathWorks PID Controller](https://www.mathworks.com/help/simulink/slref/pidcontroller.html),
[MathWorks Anti-Windup Control Using PID Controller Block](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html),
[ISA, Automation Basics: Closed-loop control troubleshooting](https://www.isa.org/intech-home/2018/march-april/departments/closed-loop-control-troubleshooting),
[MathWorks, Edit Compensator Dynamics](https://www.mathworks.com/help/control/ug/edit-compensator-dynamics.html),
[University of Michigan CTMS, Designing Lead and Lag Compensators](https://ctms.engin.umich.edu/CTMS/index.php/Content/MotorSpeed/Simulink/Control/?aux=Extras_Leadlag),
[ISA InTech, Optimizing to the Tune of a PID Equation](https://www.isa.org/intech-home/2017/may-june/features/optimizing-to-the-tune-of-a-pid-equation),
[ISA InTech, Loop Tuning Basics: Self-Regulating Processes](https://www.isa.org/intech-home/2016/may-june/departments/loop-tuning-basics-self-regulating-processes),
[ISA InTech, Loop Tuning Basics: Complex Process Responses](https://www.isa.org/intech-home/2016/september-october/features/loop-tuning-basics-complex-process-responses),
[ISA PID Tuning Appendices](https://www.isa.org/getmedia/e5c068e9-57ea-4ebf-b806-c25ee4e3e081/PID-Tuning-Appendices_WEB_PDF.pdf).
이번 검토에서 조건을 명시한 PID 적분 동작, lead 고주파 이득, P→PI→선택적 D 수동 튜닝, 현장 튜닝 체크리스트 Fact를 등록했으며, registry의 모든 Fact는 `score_effect=none`이다. 나머지 Anchor는 부분 근거 또는 scope 과다로 보류했다.

같은 PID Topic의 `pi_controller_common_in_process_control`은 UNIDO 교육자료에서 일반적인 공정의 PI 사용 사례와 D에 의한 측정 잡음 증폭·최종요소 마모 가능성을 확인했다. IChemE의 공정제어 기술 기고는 PI가 다수인 현장 관행, D 추가 후 기존 설정값 재튜닝의 필요성과 수동 탐색 난이도, 잡음이 밸브의 빠른 전행·고장으로 이어질 수 있음을 설명한다. 따라서 “유지보수 부담”은 보편적 인과 법칙이 아니라 D의 노이즈 민감성에 따른 튜닝·최종요소 관련 실무 위험으로 한정해 등록했다. 신호가 깨끗하고 공정 동특성이 요구하면 D가 유효할 수 있으므로 PI가 항상 우월하다는 뜻은 아니다. Fact는 `score_effect=none`이다. 자료: [UNIDO process simulation and optimization training report, PID control section](https://downloads.unido.org/ot/48/13/4813540/20001-_22436.PDF), [IChemE, Practical Process Control Part 6: Derivative Action](https://www.thechemicalengineer.com/features/practical-process-control-part-6-derivative-action/).

상태피드백 기준추종 Topic의 14개 Anchor 중 11개를 확인해 등록했다: `state_tracking_feedback_law_closed_loop`, `state_tracking_pole_placement_tracking_distinction`, `state_tracking_prefilter_steady_state_derivation`, `state_tracking_prefilter_existence_model_dependence`, `state_tracking_integral_internal_model_principle`, `state_tracking_augmented_system_formulation`, `state_tracking_augmented_controllability_stabilizability`, `state_tracking_prefilter_integral_role_separation`, `state_tracking_disturbance_reference_performance`, `state_tracking_saturation_anti_windup`, `state_tracking_observer_separation_principle`. State equation, prefilter DC-gain 식과 augmentation 행렬은 대수 유도로 확인하고, reference와 독립 disturbance path는 중첩 원리로 분리했다. Integral tracking claim에는 폐루프 안정, feasibility, 원점 invariant zero 부재, 포화 조건을 붙였다. Observer separation은 state-feedback 쪽 stabilizability와 observer 쪽 detectability가 안정화에 함께 필요하며, 임의 pole placement에는 controllability/observability가 필요하도록 조건을 명시했다. Illinois ECE 486 자료와 [MIT Murray 교재의 separation theorem](https://introcontrol.mit.edu/_static/fall21/extras/Feedback%20Systems%20Murray.pdf)을 확인했다. `state_tracking_design_objective`, `state_tracking_robustness_noise_gain_tradeoff`, `state_tracking_implementation_validation` 3개는 설계 권고가 포괄적이거나 적용조건을 더 분리해야 해 보류했다.

제어밸브 특성 Topic은 22개 중 19개 Anchor를 독립 확인했다. Inherent 특성의 constant-ΔP 정의, installed 특성의 배관계 의존성, Linear·Equal Percentage·Quick Opening 정의, equal-percentage 지수식과 기울기, 액체 Cv 관계, 유량 제곱에 비례하는 난류 마찰손실, 안정 고정속도 펌프 곡선과 static head의 조건을 확인했다. Valmet Flow Control Manual, Emerson Fisher의 액체 sizing 식, KSB 펌프 시스템 곡선 자료 및 수학적 유도를 사용했다. 특히 펌프의 감소 head 주장은 모든 원심펌프에 대한 무조건 명제가 아니라 고정속도 안정 음의 기울기 H–Q 구간으로 제한했다. 보류한 `control_valve_installed_local_slope_topic_boundary`, `control_valve_manufacturer_curve_system_model_verification`, `control_valve_commissioning_characteristic_verification` 3개는 저장소 내 Topic 책임 경계 또는 일반 설계·시운전 권고로서 이번에 확인한 기술 자료만으로 Anchor 전체를 뒷받침하기 어려웠다. 등록 Fact는 모두 `score_effect=none`이다. 확인 자료: [Valmet Flow Control Manual—installed performance](https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/), [Emerson Fisher liquid sizing relation](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [KSB system characteristic curve](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/system-characteristic-curve-1116274), [KSB centrifugal pump characteristic curve](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/characteristic-curve-1117926), [Emerson Control Valve Handbook, Chapter 1](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf).

제어밸브 authority·rangeability·gain Topic의 28개 중 22개를 검토해 등록했다. Authority는 국제적으로 단일 정의가 고정되어 있지 않으므로 운전점·시스템 경계·압력강하 convention을 먼저 명시해야 한다. 단순 직렬회로 식은 가변 압력강하 정의를 둔 조건부 유도로만 기록했다. Oversizing, installed gain의 국부 기울기와 운전범위 변화, inherent/installed gain 차이, equal-percentage의 조건부 보상, rangeability의 controllable Cv/flow 비 및 실제 시스템에서의 범위 차이를 확인했다. 보류한 6개는 `process_gain_operating_point_dependency`, `loop_gain_component_product`, `valve_process_gain_compensation`, `control_range_gain_acceptance_concept`, `minimum_controllable_flow_limits`, `seat_leakage_not_minimum_control_flow`다. 이번에 확인한 자료만으로 Anchor 전체의 세부 범위를 뒷받침하기 어렵고, 특히 rangeability의 controllability tolerance와 vendor별 정의 차이가 있어 보류했다. 확인 자료: [Valmet authority 정의와 비표준화 주의](https://www.valmet.com/insights/articles/flow-control/control-valve-authority---ask-the-flow-control-expert/), [Valmet installed gain 매뉴얼](https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/), [Valmet rangeability 정의](https://www.valmet.com/insights/articles/flow-control/flow-control-expert3/), [Emerson Control Valve Handbook rangeability](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf). 등록된 Fact는 모두 `score_effect=none`이며, authority 공식은 정의한 단순 직렬 경계에서만 유효하다고 조건을 달았다.

`pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`의 `dp_level_boundary`도 확인했다. 이 Anchor는 기술적으로 DP transmitter가 level에 쓰일 수 없다는 명제가 아니라, 저장소에서 기본 압력/DP 센서 내용과 DP-level 설치·수두 계산의 책임을 나눈다는 taxonomy 계약이다. revision 18의 압력 센서 Pack과 revision 4의 DP-level Pack을 대조해 해당 범위가 서로 분리되어 있음을 확인하고, 이 한정된 의미로만 기록했다. 이는 repository scope 검증이며 외부 기술 사실 검증으로 취급하지 않는다.

2차계 응답 Topic의 마지막 Anchor `so2_design_tradeoff`를 확인했다. MIT OCW의 표준 underdamped 2차계 식은 damping ratio와 overshoot/rise-time 간 trade-off를 보여주고, 별도 MIT 제어 강의는 disturbance rejection을 명시적인 성능 요구로 구분한다. 실제 제어설계는 actuator 포화·물리/안전 한계도 고려해야 한다는 조건을 붙여, 이상적인 2차계 식만으로 실제 장치 feasibility를 보증하지 않도록 범위를 제한했다. 특정 ζ가 모든 설비에서 최적이라는 주장은 하지 않는다. 자료: [MIT OCW 2.004 Lecture 21](https://ocw.mit.edu/courses/2-004-dynamics-and-control-ii-spring-2008/8e6878353de8beaeacbab817cb8c314b_lecture_21.pdf), [MIT OCW 6.241J course text](https://ocw.mit.edu/courses/6-241j-dynamic-systems-and-control-spring-2011/996025f6db0d90b00f11c44fc49b85f9_MIT6_241JS11_textbook.pdf), [Engineering LibreTexts, Chapter 10: System](https://eng.libretexts.org/Courses/California_State_Polytechnic_University_Humboldt/Measurements_Instrumentation_and_Controls/Chapter_10%3A_System).

Routh–Hurwitz 안정도 Topic의 `field_gain_selection_requires_margin`을 확인했다. Routh로 얻은 gain 구간은 모델의 명목 특성방정식에 대한 안정 여부이며, 현장 강건성·제어성능·구동기 가능성까지 자동 보장하지 않는다. Lund University 교재의 gain/phase/delay margin을 안정 경계로부터의 robustness 지표로, MIT OCW 자료의 actuator 포화·hardware stress 및 별도 disturbance/noise 성능 요구를 교차 확인했다. 따라서 적용 운전점과 모델 변화, 지연, 잡음, 포화 조건을 추가 확인하라는 범위로 기록했다. 특정 margin 숫자를 모든 계통에 요구하지 않는다. 자료: [Lund University control theory §8.5](https://www.control.lth.se/fileadmin/control/Education/EngineeringProgram/FRTF10/2019/book2016.pdf), [MIT OCW 2.017J pole-placement constraints](https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/bfcda6f40bad59b61b3f28ab8da1c86f_MIT2_017JF09_control.pdf), [MIT OCW 6.241J performance specifications](https://ocw.mit.edu/courses/6-241j-dynamic-systems-and-control-spring-2011/996025f6db0d90b00f11c44fc49b85f9_MIT6_241JS11_textbook.pdf).

LQR Topic에서는 표준 비용함수, Q/R 조건, CARE/DARE, stabilizing solution의 존재조건,
gain 및 폐루프 행렬, Bryson 초기 가중치 경험칙, hard constraint의 한계, LQR과 극점배치의
설계 차이를 MIT 자료 및 Hespanha 교재와 대조했다. 동일 배율 Q/R 불변성은 비용함수와 CARE
대수 유도로 확인했다. 이번 검토에서는 `state_lqr_q_weight_state_tradeoff`,
`state_lqr_r_weight_control_tradeoff`, `state_lqr_tracking_prefilter_lqi`도 독립 확인해
등록했다. Q 가중치는 비용함수에서 해당 상태편차의 페널티를 정할 뿐 전체 응답의 단조 개선을
보장하지 않으며, R은 입력비용이지 액추에이터 한계가 아니다. 추종에서는 명목 프리필터와
적분상태 확대 LQI를 구분하고, LQI의 stabilizability/Riccati 조건 및 포화 시 windup 대책을
명시했다. MIT 자료와 MathWorks 공식 문서를 확인했으며 모두 점수 영향은 없다.

4–20 mA 2선식 루프의 `acl_closed_loop_verification`은 Emerson 장치의 공식 loop-verification
절차가 4/12/20 mA와 alarm-current 점검을 제공하는 점, Rockwell의 공식 analog input 문서가
raw mA와 engineering-unit scaling 및 관련 process alarm 설정을 구분하는 점으로 확인했다.
이는 해당 시험 지점과 동작을 모든 기기에 강제한다는 뜻이 아니다. 복구 후 실제 채널 끝단까지
검증하고 기록하되, 허용값과 trip 방향은 적용 기기 설명서 및 승인된 site cause-and-effect에
따르도록 fact 범위를 한정했다. 이 Fact도 `score_effect=none`이다.

Thermistor Topic의 `thermistor_fault_diagnostics_open_short_range_fail_safe`도 TI의 ADC
open/short 진단 예제와 Analog Devices의 NTC-to-ADC 회로 자료를 대조해 등록했다. 판정은
고장별 ADC 값이나 임계값이 모든 회로에서 같다는 뜻이 아니다. 센서 저항 범위·divider 구성·ADC
레일/허용범위·공차에 따라 진단 구간을 정하고, 고장 시 안전 출력은 공정 위험 및 시스템 설계에서
정하도록 조건을 붙였다. 등록 Fact는 점수 중립이다.

`temperature_error_reduction_measures`는 현재 보류다. NIST 자료는 적정 담금 깊이와 줄기 방향
열손실 저감을 뒷받침하고, Endress+Hauser 자료는 thermowell의 길이·두께·유속·강도·응답 상충을
설명하지만, 현재 확보한 근거만으로 대표 측정 위치, 차폐·단열, 보정계산과 교정까지 포함한 전체
복합 권고를 하나의 일반 규칙처럼 확인하지 못했다. 이는 Anchor가 틀렸다는 판정이 아니라, 주장별
근거를 더 모으거나 범위를 나눌 때까지 verified 승격을 보류한다는 뜻이다.

Force-balance transmitter의 `force_balance_tradeoffs`는 Kuphaldt의 산업계측 교재와
Techniques de l'Ingénieur 기술자료에서 평형 피드백, sensing-element 운동 제한과 fatigue 이점,
기구 크기·진동 민감도 trade-off를 대조해 verified 처리했다. 전력·방폭 문제는 모든 force-balance
구조에 동일하게 적용하지 않고, 전자식 구동 모델의 전력/인증을 해당 기기별 확인사항으로 한정했다.

Root-locus Topic의 `compensator_design_application`은 MIT OCW의 lead-compensation 설계 예제에서
원하는 극점이 gain-only 근궤적에 없으면 이득만으로 실현할 수 없고 보상기 동특성을 추가해
근궤적을 바꾸는 것을 확인했다. MathWorks 공식 문서는 root-locus 편집에서 lead/lag/lead-lag와
pole/zero, integrator/differentiator 동특성을 추가하는 방법을 설명한다. 구체적인 구조 선택과
현장 제약 검증은 plant·구현 조건에 따라야 하며, 보편적인 성능 보장으로 해석하지 않는다.

Strain-gage/load-cell Topic의 `wiring_shield_ground_fault_diagnostics`는 NI·OMEGA의 브리지
계측 기술자료와 Interface load-cell 제조사 점검 절차를 대조했다. lead 저항·여자전압 강하,
저레벨 신호 EMI·접지 전류, 브리지 저항·zero balance·절연 점검은 확인했지만, 수치 기준이나
단일 shield/ground 방식은 특정 모델·배선 topology에 한정했다. 이에 따라 Fact를 topology와
제조사 사양/기준선 의존으로 기록했고 score effect는 없다.

Nyquist Topic의 `field_robustness_validation`은 MathWorks의 운전점 선형화와 classical/disk/delay
margin 자료, 모델 불확실성·센서 잡음 자료, 포화 시 비선형 동작과 anti-windup 자료를 분리해
대조했다. 따라서 -1 임계점 주변 여유 및 선형 강인성은 관련 운전점·불확실성 모델에서 확인하고,
액추에이터 포화는 선형 Nyquist margin이 보증하지 않으므로 별도 비선형 검증 대상으로 한정했다.
수치 여유값은 시스템 요구조건에 따라 정하며 보편값으로 제시하지 않는다. 이 Fact도 점수 중립이다.

Power-electronics Topic의 `power_electronics_converters_motor_drive_control_anchor_03`은 Infineon의
power diode·thyristor 자료에서 다이오드의 비제어 동작과 SCR의 gate turn-on/외부 commutation
turn-off를 확인했다. IGBT switching application note는 부하전류·전압·온도·gate resistance·회로
기생성분 및 freewheel diode recovery의 영향을 설명하고, ST의 gate-drive 자료는 MOSFET/IGBT의
절연 gate 구동 특성을 구분한다. 시험 조건과 실제 회로 의존성을 그대로 제한조건에 남겼다. 점수 중립이다.

같은 Topic의 `power_electronics_converters_motor_drive_control_anchor_01`은 현재 미승격 상태를
유지한다. 문구가 전력변환기 전반을 전력반도체 스위칭 기반으로 한정하지만, Infineon의 공식
전력변환 자료는 linear conversion과 switch-mode conversion을 모두 구분한다. 따라서 해당 문구는
전력전자 변환기와 스위칭 변환기의 범위를 혼합했을 가능성이 있어, 현 상태로는 verified 처리하지
않으며 Topic Pack 문구 수정 대상으로 기록한다. `anchor_02`는 아래 출처 재확인으로 기존 verified
Fact의 근거를 보강했다.

기존 verified Fact인 `power_electronics_converters_motor_drive_control_anchor_02`의 네 가지 입력·출력
분류는 TU Delft 강의자료로 재확인했다. Infineon의 분류표도 범주를 교차 확인하는 데 썼지만,
DC/AC 행의 general-purpose 명칭에 AC/DC로 보이는 표기 오류가 있어 inverter라는 용어의 근거로는
사용하지 않았다. 이 Fact는 topology나 단방향/양방향 기능까지 추론하지 않으며 점수 중립이다.

`power_electronics_converters_motor_drive_control_anchor_07`은 Rockwell Automation의 drive
비교표, TI의 AC drive design requirements 및 EMC/isolation 설명, Infineon의 drive 효율·손실·열
자료, ABB의 product-specific maintenance 절차로 확인했다. 입력·부하, 전력품질, 보호·EMC/절연,
회생 및 유지관리 항목을 설계 검토목록으로 승인했으며, 모든 drive에 동일 topology나 완화장치가
필요하다는 뜻은 아니다. 허용값·기능 선택은 해당 부하·현장 표준·제품·운전 조건에 따른다. 점수 중립이다.

HAZOP/LOPA Topic의 `hazop_lopa_srs_handoff`는 ISA의 LOPA 시나리오·빈도·IPL·위험감소 분석,
Rockwell SafeBook의 IEC 61511 기반 SRS 항목, HSE의 안전수명주기 구분을 대조해 등록했다.
LOPA 결과는 원인·빈도·IPL·위험감소/target SIL의 traceable input이며, 응답시간·trip point·safe
state·proof-test·bypass/reset·운전모드는 후속 SRS에서 상세화하는 항목임을 명시했다. 이를 LOPA
계산 자체가 전부 결정한다는 뜻으로 쓰지 않는다.

같은 Topic의 `hazop_lopa_scenario_aggregation_moc`는 ISA 자료의 shared-SIF combined demand/RRF
요구와 OSHA PSM·HSE의 변경관리 및 안전검증 지침으로 확인했다. 변경은 관할 및 site MOC 절차로
screening하고, 위험분석 또는 SIF 설계기준이 바뀐 경우에 영향을 받는 LOPA/SIL/SRS/verification을
필요 범위에서 갱신하도록 조건을 붙였다. `replacement-in-kind`의 처리와 규제 적용범위를 보편화하지 않았다.

RTD Topic의 `rtd_fault_diagnostics_environment_validation`은 제품·설치별 시험 범위로 한정해
verified 등록했다. Emerson Rosemount 3144S 자료는 4선 RTD의 open wire/loose/corroded connection
보호, loop integrity 및 sensor drift 진단과 loop test를 구체적으로 설명하지만, 같은 자료에서
moisture intrusion 진단 예시는 thermocouple degradation 진단으로 기술된다. 그러므로 그 예시만으로
일반 RTD 채널이 moisture ingress를 직접 진단해야 한다고 일반화할 수 없다. 단선·단락과 3선식 lead
저항 불평형은 NI/제조사 문서에서 회로별 조건으로 확인되나, 이 Anchor 전체의 진단목록 및 의무 수준을
모든 RTD에 자동 내장된다고 해석하지 않도록 fact 조건에 이 구분을 반영했다. NI 자료는 3·4선
토폴로지별 lead resistance 영향을, WIKA 자료는 sheath 절연저항 누설의 측정오차를, Rosemount 644
자료는 open/short·단자 문제 점검을 보강한다. 이에 따라 설치별 verification/maintenance plan의
체크항목으로 승인했으며, 모든 장비의 자동진단 기능이나 보편적인 수치 기준이라는 주장은 하지 않는다.

Lead–lag 보상기 Topic에서는 정규화된 1차 lead/lag의 극점·영점, 최대 위상 및 주파수응답,
lag의 DC gain과 유한 정상상태오차 관계를 대수 유도와 Texas A&M 강의자료로 확인했다.
Lead·lag 결합의 목적, 표준 frequency-response 설계 순서와 root-locus/Bode가 같은 loop
transfer function을 다르게 분석한다는 범위도 등록했다. 성능 절충·현장 검증 권고처럼 plant와 구현에 의존하는
나머지 Anchor는 이 결과만으로 일반화하지 않고 보류한다. 등록분은 점수 중립이다.

이번 검토에서 유지보수 KPI의 `kpi_mtbf_definition_boundary`를 verified로 등록했다.
NIST/SEMATECH는 MTBF 추정치를 운전시간/고장 수로 정의하고, repair·waiting·requalification
시간을 운전시간에서 제외하는 용어 정의를 제공한다. NASA 자료도 누적 운전시간/확정
고장 수를 제시한다. 따라서 고장 정의와 관찰·운전시간 경계가 일관된다는 조건을
Anchor 근거에 포함했다.

압력 측정 Topic의 `accuracy_total_performance_terms`, `ambient_environment_hazardous_selection`, `bourdon_error_protection`, `bourdon_forms_application`, `dp_static_line_pressure_effect`, `impulse_line_installation_error`, `overrange_working_burst_pressure`, `process_media_wetted_material_selection`, `pulsation_vibration_dynamic_response`, `range_turndown_resolution_selection`, `selection_lifecycle_maintainability`, `zero_span_drift_calibration`과
`piezoresistive_temperature_compensation`을 verified로 등록했다. Emerson의
Rosemount 1151 설명서는 고정(static) 압력에서 입력 차압이 0이어도 양·저압 측 효과가
완전히 상쇄되지 않아 잔류 zero 영향이 생길 수 있고 span도 영향받을 수 있다고 설명한다.
Rosemount 3150 설명서는 Range 1–3과 4–5의 보정·잔류 불확도 방식이 다름을 명시한다.
따라서 모든 DP transmitter에 같은 크기·방향·보정법이 적용된다고 일반화하지 않고,
모델/Range별 설명서에 따라 운전 정압에서 확인·교정한다는 조건을 함께 기록했다.
WIKA 자료는 C형 Bourdon tube와 helical/spiral 형상의 고압 적용 경향을 설명하며,
제품 사양서별 실제 전환 압력은 달라질 수 있음을 확인했다. 따라서 형상별 절대 압력
경계가 아니라 제조사별 rated range를 확인한다는 조건을 기록했다.
Ashcroft와 WIKA의 제조사 문서는 Bourdon gauge의 히스테리시스·기구 마찰과 온도,
진동·맥동·과압 보호방법을 제시한다. 보호수단별 응답 지연·막힘 등 절충도 있어,
무조건적인 액세서리 설치가 아니라 공정 조건에 맞춘 선정으로 Fact 범위를 한정했다.
Analog Devices 자료는 piezoresistive bridge의 온도 의존 offset과 sensitivity/span을
설명하고 저항 네트워크 및 전자식 신호조절 보상 사례를 제시한다. 따라서 단일한 보상
회로를 모든 센서에 강제하지 않고, 센서별 압력·온도 교정 범위와 잔류 오차를 확인하도록
조건을 한정했다.

`dp_level_boundary`는 압력 측정 Topic과 `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
Topic 사이의 범위·소유권을 지정하는 내부 라우팅 계약이지 외부 기술사실이 아니다.
따라서 기술적으로 false라고 판정하지도, 독립 기술 Fact로 verified 승격하지도 않았다.
이 항목은 Fact-anchor 정확성 감사와 별도로 Topic routing/범위 계약 검증 대상이다.

`kpi_mttr_definition_boundary`는 현재 승격 보류다. 자료와 조직에 따라 MTTR이 의미하는
복구 구간 및 지연시간 포함 여부가 달라질 수 있어, 현 문구의 진단·수리·시험·승인
범위를 하나의 보편 정의로 뒷받침하는 근거가 충분하지 않다. 이 판단은 Anchor가
거짓이라는 뜻이 아니며, 더 명확한 범위 정의나 표준별 근거 전에는 미등록 상태를 유지한다.

`calibration_as_found_as_left_oot`는 검교정 품질 프로그램 범위로 한정해 verified로
등록했다. WIPP 절차는 OOT 발견 시 마지막 교정 이후 사용 이력에서 잠재 영향 대상과
수집 데이터를 평가하도록 명시하며, NIST 자료는 조정 전·후 결과 구분 및 OOT 품질
영향평가 절차를 뒷받침한다. 이 Anchor는 모든 산업·관할에 동일한 법적 의무가 있다는
뜻이 아니며, 적용 프로그램의 절차와 품질 요구사항에 따른다.

`calibration_interval_risk_history`는 NIST의 일반 고정주기 비권고·주기 결정 요소,
DOE WIPP의 제조사 권고·사용량·시설 이력·as-found 주기 조정 사례, NIST HB 145의
안정성·목적·사용량 및 과거 결과 기준을 교차 확인해 verified 등록했다. 법률·계약의
개별 요구는 해당 계기와 관할에 적용되는 외부 조건으로 남겨 일반 주기로 대체하지 않는다.

`calibration_reference_standard_control`은 NIST metrological traceability policy,
NIST laboratory handbook, DOE WIPP 현장 M&DC 절차를 대조해 verified 등록했다.
장비의 요구 정확도·불확도에 맞는 기준기 적합성을 확인하되 고정된 정확도비를 주장하지
않으며, 보관·환경·기록 의무의 구체적 형식은 적용되는 품질 프로그램에 따른다.

`isa95_hierarchy_interface`는 ISA의 현행 시리즈 개요와 ISA InTech 설명을 확인해
verified 등록했다. ISA-95 Part 6에 Messaging Service Model이 별도로 존재하므로,
이 사실은 ISA-95 전체가 단일 전송 프로토콜이라는 해석을 부정할 뿐 구체적 구현이나
Part 6의 메시징 의미를 부정하지 않는다.

`source_timestamp_event_time`은 OPC UA의 SourceTimestamp 정의, Flink의 Event/Processing
Time 정의, Kafka의 CreateTime/LogAppendTime 동작을 교차 확인해 verified 등록했다.
이는 원천 timestamp가 항상 제공·정확하다고 가정하지 않으며, 미제공 시 null/미상 처리와
clock basis·fallback 기록을 요구하는 제한을 포함한다.

`quality_code_semantics`는 OPC UA StatusCode의 Good·Uncertain·Bad 의미, SubCode에 의한
상세 조건, DataValue와의 연관 및 Client의 사용 전 상태 확인 요구를 OPC Foundation
Part 4에서 확인했다. Part 8은 OPC UA→OPC DA의 구체적인 quality 매핑을 보여준다.
따라서 시스템 간 매핑 필요성은 명시적·인터페이스별 계약으로 한정했으며, 모든 시스템에
보편적인 일대일 매핑이 보장된다는 뜻은 아니다. 이 Fact 역시 점수 영향은 없다.

`bad_uncertain_propagation`은 OPC UA Part 4의 Bad/Uncertain 사용성 원칙과 Part 13의
Aggregate 품질 계산·보간·계산 상태 표기를 대조했다. 따라서 Bad를 정상 원시값으로
묵시 취급하지 않고, 비-Good 값 처리나 대체·보간 결과의 품질 및 제한을 명시하는 데이터
무결성 원칙으로 범위를 한정했다. 구체적인 대체 정책은 응용별로 정해야 한다.

`data_completeness_metric`은 OPC UA Historical Access가 “기대된 시간 구간의 데이터 없음”과
단순 조회에서의 “데이터 없음”을 구분하는 점, AWS 데이터 품질 기능이 completeness를
non-null 비율로 계산하는 사례를 대조했다. 따라서 기대 샘플 주기와 유효성 기준이 정의된
정규 샘플링 historian에 한정한 운영 지표로 확인했으며, 모든 이벤트형 데이터에 통용되는
보편 공식으로 주장하지 않는다.

`timeliness_latency_metric`은 OPC UA의 SourceTimestamp/ServerTimestamp 구분과 Flink의
event/processing time, source-to-downstream latency histogram 및 clock synchronization
가정을 확인했다. 따라서 지연의 측정 endpoint·timestamp·통계량·업무 기준을 명시해야 하며,
허용 임계값은 시스템별로 정해야 한다. 이는 일률적인 표준 임계값 주장이 아니다.

회전속도 측정 Topic의 `period_measurement_low_speed`와 `gear_tooth_speed_equation`은
펄스 주파수·주기에서 rpm을 구하는 단위 유도식을 확인해 verified 등록했다. 유효 pulse/rev,
실제 edge-counting 방식, 초 단위 주기와 pulse 누락 조건을 명시했다. 인접한
`counting_window_speed_equation`은 식 자체의 count step이 `60/(N_eff·Δt)`로 창 길이에
의해 정해지고, 저속에서 커지는 것은 그 step의 상대오차이지 절대 속도 step이 아니라는
불일치가 있어 verified 등록하지 않았다. 기존 Anchor 문구 수정 검토 대상으로 남긴다.

RTD Topic의 `rtd_calibration_tolerance_uncertainty`는 승격 보류했다. NIST는 IPRT 교정에
복수 온도점, 온도 균일성이 관리되는 비교 bath와 기준 SPRT를 사용하는 사례를 제시하고,
온도범위·요구 불확도에 따라 교정점 수를 결정한다고 설명한다. 하지만 센서 허용오차는
교정 전 사양인지, 교정 보정 후 잔류오차인지에 따라 불확도 예산에 반영하는 방법이 다르고,
이를 무조건 더하면 교정 불확도와 중복 계산할 수 있다. 현 Anchor에 그 경계가 명시되지 않아
현재는 verified 처리하지 않는다. NIST 예시의 교정 예산도 지시계 분해능, reference SPRT,
self-heating, bath 안정도·균일도 및 immersion을 각각 구분한다.

저항형 센서의 `sensor_resistive_geometry_conductivity_relation`,
`sensor_resistive_strain_gauge_factor`, `sensor_resistive_voltage_current_conversion`은
각각 균일 도체의 저항 유도, R=rho·l/A의 미소변화에 따른 strain-gauge factor 구성, Ohm 법칙과
Wheatstone bridge 분압 불평형으로 확인했다. 재료·기하의 균일성, 작은 변형 근사와 브리지
극성·arm 구성 조건을 함께 기록했다.

같은 Topic의 `sensor_capacitive_geometry_permittivity_relation`,
`sensor_capacitive_dynamic_current_readout`,
`sensor_inductive_magnetic_circuit_permeability_relation`은 평행판 전계,
q=CV의 시간 미분, 선형 자기회로의 reluctance·flux-linkage 관계로 확인했다. 각각 fringe,
lumped/quasi-static, 선형·균일 자로 가정과 실제 readout topology 한계를 계약 조건에 적었다.

압력 측정 Topic의 `pressure_relation_equations`는 NIST의 대기압 기준 gauge 정의와
Emerson 3051의 HP−LP 차압 convention을 확인해 verified 등록했다. 실제 H/L 포트 연결과
계기 설정 확인을 조건으로 두어 부호 convention이 장치/설치에 무관하게 고정된다고
과장하지 않았다.

같은 Topic의 `pressure_reference_abs_gauge_dp`도 NIST gauge 기준과 DP 입력 정의로 확인했다.
`bourdon_elastic_deformation_principle`은 WIKA 자료 두 건에서 oval 단면의 원형화 경향,
곡관 변형, free-end 이동과 pointer mechanism 전달을 교차 확인했다. Bourdon 기구의
변위량·압력범위·선형성은 구조와 재질에 따라 달라진다는 제한을 포함했다.

`dp_transmitter_two_port_principle`은 WIKA의 차압 diaphragm 입력과 Emerson의 동일 압력
조건 zero trim 절차를 대조했다. 따라서 동일 포트 압력은 이상적 zero differential input을
뜻할 뿐, 정압 효과·zero offset이 있는 실제 계기의 출력이 자동으로 정확히 0임을 보장하지
않는다고 명시했다. `piezoresistive_principle_bridge`는 TI·Analog Devices 자료의 압력에 따른
bridge resistor strain, 저항 변화 및 차동 출력으로 검증했다. `piezoresistive_static_capability`는
저항 브리지의 외부 여기 및 지속 출력과 charge-output piezoelectric의 static-load drift를
대조하되, piezoelectric 정압 측정도 시간·압력·정확도에 따라 가능하다는 한계를 보존했다.

`diaphragm_sensor_vs_seal`은 WIKA의 seal 기능 정의와 Emerson의 fill-fluid 온도·capillary
응답 영향 자료를 확인했다. sensing diaphragm의 transduction 역할과 seal assembly의
process isolation·pressure transfer 역할을 구분했고, seal이 오차를 제거한다고 일반화하지 않았다.
`diaphragm_deflection_principle`은 WIKA의 차압 diaphragm 변위와 Analog Devices의 전기식
변환 설명, 선형 탄성 plate 이론을 대조했다. 두께 감소에 따른 감도 증가는 같은 재료·지름·지지
조건과 소변형 범위에서만 성립하도록 제한했고, 응력·과압·선형성 제약을 명시했다.

Topic별 집계와 위 수치의 재현 가능한 원자료는
[`full_topic_fact_source_audit_20261010.json`](../reports/full_topic_fact_source_audit_20261010.json)에
있다. 새 점수 경로는 아직 켜지지 않았다. 기존 점수에 기여시키려면 Topic별
demand-to-fact mapping과 Stage 5 점수 adapter, 독립 답안 평가가 뒤따라야 한다.

유압·공압 시스템 선정 Anchor `fluid_power_selection_is_application_specific_across_load_motion_and_lifecycle`은
U.S. Navy의 NAVEDTRA 14050A에서 액체와 기체 작동유체의 압축성 차이를 확인하고,
Festo의 구동기술 선정 지침과 DOE 압축공기 에너지관리 자료에서 적용 부하·운동과
시스템 에너지 효율 평가 필요를 교차 확인했다. 따라서 한 방식이 보편적으로 우월하다고
하지 않고, 실제 부하·운동 요구, 유체 특성, 설치환경과 시스템 경계를 기준으로 선정한다는
조건을 Fact에 명시했다. 출처 없는 내용을 보태지 않도록 유지관리·안전 항목은 적용 요구로
한정하고 보편적 성능 우위로 해석하지 않는다.

SIS/SIL Topic의 `sis_sif_relation`, `sil_property_of_safety_function`,
`sif_end_to_end_boundary`, `risk_to_srs_flow`는 IEC 61511-1 공식 미리보기, IEC의
기능안전 개요자료, ISA의 IEC 기반 용어정의 및 영국 HSE 가이드로 확인했다. 이 검토는
SIS와 SIF의 시스템/기능 구분, SIL의 기능 단위 속성, sensor–logic–final-element 기능
경계와 위험분석 결과의 SIF별 요구사항·SIL 연결만 승인한다. SRS의 검증 가능성 등 별도
Anchor는 근거가 충분하지 않아 아직 등록하지 않았다.

같은 Topic의 `software_safety_lifecycle`은 IEC 61511-1의 application-program lifecycle
표와 SIS lifecycle 단계, HSE의 process-sector lifecycle 설명을 대조해 추가 확인했다.
확인된 범위는 요구·설계·구현·검증·통합·안전 validation과 운전·유지보수·변경이며,
해당 표준의 적용범위 및 phase별 증거가 달라질 수 있다는 조건을 함께 기록했다.

Liquid control valve cavitation/flashing Topic에서는 Fisher Catalog 12 용어표와 Emerson/Fisher
Control Valve Handbook를 사용해 압력 기호의 절대압 기준, 운전온도에서의 Pv, Pc의 의미,
vena contracta의 최소 유로 단면/저압 영역, 기화 시작 조건, downstream pressure recovery,
liquid choked-flow capacity limit, cavitation/flashing의 후속 압력거동 구분 등 10개 Anchor를
확인했다. 실제 값의 산정, 특정 trim의 FL/FP 계수, damage onset/severity 및 예방책은
제조사·geometry·운전점 의존성이 커 이번 verified 범위에 포함하지 않았다.
같은 Topic에서 FL·FF·FP·FLP의 용어 및 적용범위, bare/fitting-adjusted allowable choked
pressure-drop 식, sizing에 actual/choked allowable pressure drop 중 낮은 값을 쓰는 규칙,
choked flow의 비영(非零) capacity 의미, bubble collapse 연관 cavitation damage mechanism 및
cavitation/flashing의 후속 압력거동 차이를 추가 확인했다. 계수는 선정된 valve, attached
fittings 및 표준 계산 방식에 종속되므로 임의의 일반 상수로 해석하지 않도록 조건을 기록했다.

추가로 flashing의 침식 가능성, choked capacity·vapor formation·damage severity의 구분,
backpressure 상승에 따른 vena-contracta 압력 변화, 다단 trim의 단계별 압력강하, recovery
특성에 따른 cavitation susceptibility, anti-cavitation trim과 application-defined flashing의
경계를 확인했다. backpressure와 다단 trim은 해당 설계조건에서만 효과를 주장하고, 고장·다른
운전점·하류 장치의 cavitation 전이 가능성을 조건에 포함했다. flashing은 밸브 자체가 상변화
조건을 제거하지 못하므로 형상·재료로 손상을 완화하는 영역과 구분했다.
이번에는 Fisher Sourcebook의 characterized-cage 사례로 특정 anti-cavitation trim의
기하와 cavitation-control 능력이 plug travel에 따라 달라질 수 있음을 확인했다. 이는
모든 trim의 보편 특성이 아니라 해당 설계의 사례이므로, flow direction까지 일반화하는
주장은 이 등록으로 검증하지 않았다. IAPWS 자료로 물의 온도 상승에 따라 포화증기압이
증가함을 확인하여, 동일 압력·조성에서 온도를 낮추면 정적 증기압 여유가 커질 수 있다는
범위만 등록했다. 이것만으로 실제 밸브의 cavitation/flashing이나 손상 방지를 단정하지 않는다.

상태공간 제어 Topic의 `state_feedback_closed_loop`는 MIT OpenCourseWare 유도식에서
u=-Kx 적용 시 폐루프 행렬이 A−BK가 되는 것을 확인했다. `controllability_matrix_rank`는
유한차원 연속시간 LTI 모델에서 [B, AB, …, A^(n−1)B]의 rank가 n인 조건과 controllability의
필요충분성을 MIT 강의자료로 확인했다. 두 결과는 모델·피드백 가정 범위에 한정했으며,
구현 제약이나 실제 plant의 controllability 보장은 의미하지 않는다.
이어 `observability_matrix_rank`는 관측행렬 [C; CA; …; CA^(n−1)]의 full-rank 관측성
검사와 초기상태 추정 맥락을 확인했다. `observer_error_dynamics`는 명목 LTI plant와
Luenberger observer 식을 직접 빼서 e_dot=(A−LC)e를 재현하고 observer poles가 A−LC의
고유값임을 확인했다. 잡음과 plant/model mismatch가 있을 때 실제 추정 오차에 같은 무잡음
식만 적용된다고 일반화하지 않았다.
`eigenvalue_pole_minimal_realization`은 MIT 강의의 Kalman decomposition과 최소 realization
정리에서 전달함수의 zero-state I/O가 reachable-observable subsystem으로 정해짐을 확인했다.
따라서 최소 realization에서 A의 eigenvalue가 전달함수 pole이라는 조건과, 비최소 모델에는
외부 전달함수에 나타나지 않는 내부 모드가 남을 수 있다는 경계를 함께 기록했다.
마지막으로 PBH controllability/observability 행렬식과 stabilizability/detectability의
경계를 확인했다. 연속시간에서 이 두 안정화 가능성은 불제어·비관측 모드가 모두 엄격히
open LHP에 있어야 하므로, Anchor의 “불안정 모드”는 Re(λ)≥0인 모드로 해석할 때 정확하다.
따라서 허수축 모드도 검사 대상임을 Fact 조건에 명시했다. Pack 원문에 이 경계가 드러나지
않는 용어 모호성은 추후 문구 정리 대상으로 남긴다.

2차 시스템 공진 Topic의 적용 Anchor `F5`도 검토했다. NI 구조시험 자료는 고유진동수 부근의
가진이 구조 응답을 키우고 피로·손상을 일으킬 수 있음을, Control Global의 계장제어 자료는
외란 주기와 controller tuning에 따라 루프 진동이 증폭될 수 있고 측정 noise가 controller
output에 전달될 수 있음을 뒷받침한다. 이를 모든 공진이 불안정이나 손상을 일으킨다는 법칙으로
보지 않고, 감쇠·루프 bandwidth/tuning·기계 공진·실제 가진과 장비 한계를 함께 검토해야 하는
조건부 적용 판단으로 등록했다.

상태공간 극점배치의 `implementation_tradeoffs_validation`은 MathWorks pole-placement 문서의
large-gain·모델 perturbation 민감도 경고, actuator effort/saturation 예시, discrete controller의
bandwidth/sample-time 제약과 고이득 관측기의 속도–noise·peaking tradeoff에 관한 논문을 대조했다.
따라서 관측기 noise/peaking은 모든 빠른 observer pole에 일반화하지 않고 고이득 관측기 조건으로
제한했고, sampling은 고정 비율 규칙이 아닌 실제 sample time과 설계 동특성의 적합성 확인으로
표현했다. 이 Anchor는 score-neutral이며 런타임 채점에 활성화되지 않는다.

온도 측정오차 Topic의 `temperature_error_reduction_measures`는 현재 미검증으로 남겼다. NIST와
NBS 자료는 immersion, 교정·불확도 및 복사차폐·단열·유속 등의 영향이 적용에 따라 중요할 수 있음을
보여주지만, Anchor는 이 조치를 일괄적으로 “종합 적용”해야 한다고 묶어 놓았다. 보호관, 충분한
유속, 복사차폐, 단열, 보정 계산이 모든 센서·공정에 보편적으로 요구되는 것은 아니므로, 각 조치를
조건부 선택으로 재기술하거나 적용 조건을 확인하기 전에는 verified 처리하지 않는다.

Historian Topic의 `historian_time_series_role`은 Emerson DeltaV Continuous Historian FAQ와
AVEVA Historian 문서에서 시계열 수집·저장·압축·조회, 값 상태/품질 및 timestamp 설정을 확인했다.
단, 확인된 구현 예시를 모든 historian의 고정 기능으로 일반화하지 않았으며, timestamp가 source/event
time이 아니라 write/storage 시각일 수 있다는 점과 설정·제품별 차이를 Fact 조건에 명시했다.
같은 Topic의 `mes_execution_role`은 ISA-95 공식 개요, OPC Foundation의 ISA-95 모델 설명과
IEC 62264-3 activity-model preview를 확인했다. MOM/MES를 Level 3의 제조운영 기능으로 ERP의
Level 4 business planning과 구분하고, scheduling/dispatch, execution, tracking 및 자원·제품
추적 모델을 반영하되 개별 MES가 모든 기능이나 genealogy 상세도를 구현한다고 일반화하지 않았다.
`erp_business_role`은 ISA-95의 Level 3/Level 4 구분과 SAP·Oracle ERP 기능 개요로 대조했다.
주문·계획·자재/공급망·원가/재무 같은 업무 기능은 ERP 제품군에서 일반적으로 제공되지만
모든 설치에 모든 모듈이 있는 것은 아니다. “MES 실시간 제어를 대체하지 않는다”는 표현은
기능 책임·아키텍처 경계로 한정하고, ERP의 실시간 데이터 연계 자체를 부정하지 않도록 조건화했다.
`time_sync_alignment`은 OPC UA의 source/server timestamp 정의와 UTC 규칙, Network Time Foundation의
clock offset·frequency offset·drift 설명, NIST의 다중 clock ordering 한계를 대조했다. 시간표시 기반
상관분석에는 공통 시간축과 offset/drift 관리를 요구하되, wall-clock synchronization만으로 인과성이
보장된다고 주장하지 않고 timestamp uncertainty와 event/sequence 근거가 필요한 조건을 명시했다.
`store_and_forward_recovery`는 Microsoft IoT Edge 오프라인 동작 및 OPC UA queue/history 표준과
대조했다. 특정 구현에서 재접속 후 저장 순서대로 내보내는 것과 달리, 보존은 TTL·디스크·queue limit에
제한되고 queue overflow는 데이터 손실을 낼 수 있다. 전달 순서와 중복/재전송은 제품·프로토콜·ack
계약 범위에서만 주장하도록 조건을 붙였으며, source continuity를 확인할 수 없는 historian gap은
성공적인 완전 복구로 간주하지 않도록 기록했다.
`compression_deadband_tradeoff`는 Emerson Historian compression configuration, OPC UA deadband와
queue overflow semantics, ISA InTech의 post-compression 분석 데이터 주의를 대조했다. 저장 이득은
구현별 알고리즘과 threshold에 의존하며, raw trace가 필요한 적용에서 손실·짧은 event 누락 가능성이
있다. 이 Fact는 trend compression이 모든 alarm/state/event를 대신 보존한다고 주장하지 않도록 한정했다.
`quality_event_preservation`은 아직 verified하지 않았다. 값·status 수집과 OPC UA event queue/overflow
가 정의된다는 것은 확인되지만, 모든 상태 변화·Alarm·Batch 경계를 반드시 원시 trend와 별도 보존해야
하는지는 요구되는 분석·규제·운영 용도와 별도 Event/Batch 시스템 책임에 달린다. 따라서 요구사항별
retention 계약과 손실 영향이 확인될 때까지 해당 문장의 보편적 의무 표현은 미검증으로 남긴다.
`historian_not_backup_only`는 AVEVA Historian 제품 문서에 한정해 역사 데이터, process/alarm/event
이력, 저장 압축, 조회, 트렌드 및 트렌드 위 alarm 상세 표시 기능을 확인하여 해당 제품 기능 범위를
verified로 등록했다. 이는 “모든 Historian이 같은 기능을 가진다”거나 모든 시스템에서 각 기능이 켜져
있다는 뜻이 아니다. 백업·복구 역할의 대체를 주장하지 않으며, Pack이 열거한 data quality·Context·
traceability 전체를 모든 제품의 보편 기능으로 확인한 것도 아니다. 해당 확장 주장은 계속 미검증이다.
`edge_gateway_role`은 Microsoft Azure IoT Edge의 gateway translation, 오프라인 store-and-forward 및
TTL/저장 한계 문서와 OPC Foundation의 cloud reference architecture를 대조했다. 번역·buffering·로컬
처리는 기능 구현과 설정에 따라 제공될 수 있고, 이 장치 단 기능만으로 전사 의미 모델과 governance가
자동 완성되지 않는다는 범위로 verified했다. 특정 제품의 기능을 모든 gateway에 일반화하지 않는다.
`streaming_event_processing`은 현재 문장 그대로 verified하지 않았다. Apache Beam/Flink 문서는 무한
stream aggregation에서 windowing을 쓰고, event-time window에서는 watermark와 out-of-order/late-event
처리 정책을 설계해야 함을 보여준다. 그러나 모든 streaming 처리가 event-time 또는 작은 window를
사용해야 하는 것은 아니며 “도착 즉시 처리”도 지연 0을 뜻하지 않는다. Anchor를 event-time window가
요구되는 적용으로 한정하기 전까지 미검증으로 둔다.
`realtime_fit_for_purpose`는 IEEE의 real-time 시스템 정의와 NIST glossary를 대조했다. 결과의
논리적 정합성뿐 아니라 애플리케이션이 요구하는 시점 내 결과 산출이 정확성 판단에 포함되고,
deadline과 시간 변동 허용치는 hard/soft 요구 및 제어 대상에 따라 달라진다는 조건으로 verified했다.
이는 0 지연이나 모든 시스템의 결정성을 주장하지 않는다.
`tag_naming_namespace`는 OPC UA Part 3와 OPC Foundation Industrial Automation Basics에서 NamespaceUri,
NodeId 및 BrowseName의 구분을 확인했다. Namespace는 naming authority 충돌을 줄이는 식별 문맥이며
BrowseName 단독은 고유 식별자가 아니라는 범위로 한정했다.
`information_model_semantics`는 OPC UA Part 3의 Object/Reference 구조, UA Modelling Best Practices의
Type·DataType·ReferenceType 의미와 OPC Foundation의 protocol connectivity/semantic gap 설명을
대조했다. 공유 모델을 실제로 채택·매핑하는 경우에 typed domain semantics를 교환할 수 있다는 뜻이며,
protocol 연결만으로 의미 상호운용성이 보장된다고 확대하지 않았다.
`metadata_context_role`은 OPC UA AddressSpace의 typed Variables/Attributes/References와 ISA-95 Common
Object Model의 equipment, physical asset, material, personnel 범위를 확인했다. 이 모델들은 관련 값을
문맥 객체에 연결할 수 있지만, 개별 historian의 모든 값에 설비·Batch·교정 등 모든 필드가 항상
존재한다는 뜻은 아니므로 구현 조건을 명시했다.
`batch_genealogy`는 OPC UA ISA-95 Material Model의 Lot/Sublot assembly traceability와 ISA-88 batch
production record가 recipe execution, equipment, alarms 등 batch 기록을 포함할 수 있음을 대조했다.
추적 목적과 모델은 확인했지만 완전성은 실제 식별자·실행·품질 데이터를 capture, correlate, version,
retain하는 현장 시스템에 달려 있으므로 genealogy 자동 보장을 주장하지 않도록 조건화했다.
`event_snapshot_distinction`은 OPC UA Part 3의 Event가 시간상 발생하는 transient occurrence라는 정의,
Part 9의 Condition이 현재/과거 상태 branch를 구분하는 모델, Part 11의 historical event/time ordering을
대조했다. 전이 이력을 저장해야 중간 상태 변화를 재구성할 수 있다는 점은 확인했지만, 시간순 event가
곧 물리적 인과 증명은 아니며 실제 이력 보존 여부는 서버 설정에 달려 있음을 조건으로 기록했다.
`it_ot_layered_integration`은 ISA-95 정보교환/기능경계, NIST SP 800-82 Rev. 3의 OT 성능·신뢰성·안전
요구를 고려한 보안지침, OPC Foundation의 의미·거버넌스 연결 원칙을 대조했다. 이를 보편적인 물리
토폴로지 요구가 아니라 책임·데이터 의미·보안 경계를 현장 위험에 맞게 설계해야 한다는 원칙으로
한정했고, 계층화만으로 안전이나 보안이 보장된다는 해석은 배제했다.
`master_data_consistency`는 ISA-95 Common Object Model에서 장비 ID가 vendor/app 간 다를 수 있고
이를 관리해야 한다는 설명, Part 7 alias mapping, recipe version 이력 필요성을 대조했다. 따라서 모든
시스템에서 ID 문자열을 동일하게 만드는 것이 아니라 alias/namespace 변환과 실행에 적용된 정의의
version을 보존한다는 조건으로 verified했다.
`data_governance_ownership`과 `retention_lifecycle`은 GOV.UK Data Ownership Model의 data owner/steward/
custodian 책임, 변경 승인, 데이터 정의·품질·접근, issue remediation, retention schedule 및 archive/
disposal/preservation 항목을 대조했다. 이를 단일 보편 조직도나 보존기간 규칙으로 해석하지 않고 조직·법역·
용도에 맞춰 책임과 데이터 유형별 정책을 정해야 한다는 한계와 함께 verified했다.
`semantic_interoperability`는 OPC Foundation의 connectivity reference architecture, OPC UA DataValue의
상태·source/server timestamp 필드, ISA-95 domain object model을 대조했다. 데이터가 transport로 전달되는
것과 양측이 단위·품질·시간·식별자·공정 문맥을 같은 의미로 해석하는 것은 구분된다는 범위로 verified했다.
`acquisition_sampling_semantics`는 OPC UA Part 4의 best-effort sampling interval, server-revised rate,
source update/exception model 및 reporting/filter/queue behavior와 Part 6/8의 status, timestamp,
engineering unit metadata를 확인했다. 실제 rate와 관측 누락 가능성을 포함하고 요구 주기는 process와
consumer 용도에 따라 정한다는 조건으로 verified했다.
`traceability_audit`는 W3C PROV가 표현하는 entity/activity/agent/derivation/revision lineage와 OPC UA
Historian이 이력값 수정 시 원본·수정자·audit event를 기록하는 규칙을 대조했다. 다만 auditing 미지원
서버가 있고 lineage 세부도는 적용에 따라 다르므로, 필요한 입력·버전·설정·품질·변경기록을 실제로
캡처해야 결과 재구성이 가능하다는 조건으로 verified했다.
`topic_boundary_transport_model`은 외부 보편 사실이 아니라 이 저장소의 routing ownership 계약으로
분류했다. `docs/topic_pack_architecture.md`, SW-07 Topic Sheet, SW-12 Topic Sheet가 동일하게 SW-07 통신,
SW-11 데이터 기반/통합, SW-12 데이터 이용 Model lifecycle을 분리하고 있어 이 내부 계약 범위에서
verified했다. 이 분류가 물리 시스템에 반드시 적용되는 산업 표준이라고 해석하지 않는다.
RTD Topic의 `rtd_calibration_tolerance_uncertainty`는 NIST 산업용 thermometer comparison calibration
절차, IPRT performance-effect guidance와 calibration uncertainty 사례를 대조했다. 기준 온도계·안정된
source와의 비교, measurement-chain 불확도 포함, self-heating/immersion/lead effects 검토를 확인했으며,
다점 수·위치는 모든 적용에 고정하지 않고 목표 범위와 정확도에 따라 정하도록 조건화했다.
`compensator_and_field_validation`은 MathWorks loop-shaping/margin/dead-time/actuator-saturation 자료와
ISA control-loop troubleshooting을 대조했다. crossover·PM·저주파 이득·고주파 roll-off가 성능/잡음/
모델불확실성 trade-off임을 확인하고, 선형 margin만으로 포화·rate limit·valve deadband가 있는 현장
구현을 대체 검증할 수 없다는 범위로 verified했다.

## 추가 검토: 온도 오차 저감 대책 Anchor 보류

`temperature_measurement_error_heat_transfer`의 `temperature_error_reduction_measures`는 충분한 담금,
대표 위치, 보호관, `유속 확보`, 복사 차폐, 단열, 보정 계산 및 교정을 하나의 필수 종합 목록처럼
서술한다. BIPM의 Thermocouple Thermometry 안내는 immersion 열누설이 immersion length에 따라
감소하고, 고온에서는 복사 열전달 영향이 커질 수 있으며, 교정은 실제 사용조건과 일치시켜야 한다고
설명한다. Emerson은 thermowell tip을 관 중앙에 두는 것과 보호관별 구조/response 검토를 권한다.
NIST 자료는 대표 평균온도 측정에 설치위치/혼합이 중요하고 오차가 유속에 따라 달라질 수 있다고 하며,
고속 기체에서는 속도에 따른 kinetic-temperature 오차가 생길 수 있어 용도별 probe/보정이 필요하다고
설명한다. 따라서 `유속 확보`는 항상 속도를 높이라는 보편 대책으로 검증되지 않는다. 복사 차폐·단열·
현장 교정은 적용 매체 및 운전조건에 따라 필요성이 다르므로 이 Anchor 전체는 현재 verified 처리하지
않고 보류한다. 정확한 기술 설명은 “유속을 무조건 높인다”가 아니라 의도한 정온도(static) 또는
전온도(total) 측정과 열전달·속도오차를 평가해 위치/보호관/차폐·단열/보정·교정을 선택한다”에
가깝다. 이번 검토로 registry 수는 변하지 않는다. 확인 자료: [BIPM Guide on Secondary Thermometry,
§§5.8, 6](https://www.bipm.org/documents/20126/41773843/Thermocouple_Thermometry_Part1.pdf/d23088f8-3bab-bacc-0cae-7358eb2666b4),
[NIST Calibration of Temperature Measurement Systems Installed in Buildings](https://nvlpubs.nist.gov/nistpubs/Legacy/BSS/nbsbuildingscience153.pdf),
[NIST Sensor Handbook, SP 615](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication615.pdf),
[Emerson Thermowells](https://www.emerson.com/en/measurement-instrumentation/catalog/temperature-measurement/thermowells),
[Fluke Thermocouple Calibration](https://www.fluke.com/en/learn/blog/temperature-calibration/how-calibrate-thermocouple).

## 추가 검토: 회전속도 계측 계산 Anchor

`speed_rotation_measurement_encoder_proximity_tachometer_selection_error`에서 펄스 주파수와 고정 측정창 count의 rpm 환산식을 단위 유도로 확인했다. `N_eff`는 encoder catalog PPR이 아니라 실제 receiver decoding 이후의 count/revolution으로 정의해야 하며, x1/x2/x4 convention을 혼용하지 않도록 조건을 명시했다. 고정창 한 count에 해당하는 rpm step은 해당 gate estimator의 양자화 간격이며 모든 오차의 보편적 상한으로 해석하지 않는다.

| Anchor | 검증 근거 | 처리 |
|---|---|---|
| `pulse_frequency_speed_equation` | `(pulse/s)/(pulse/rev)=rev/s`; 60을 곱해 rpm 변환 | 계산 유도로 verified; 점수 영향 없음 |
| `counting_window_speed_equation` | `m/(N_eff·Δt)=rev/s`; 60을 곱해 rpm 변환. 1-count step은 `60/(N_eff·Δt)` rpm | 계산 유도로 verified; 점수 영향 없음 |
| `incremental_encoder_principle` | 위치는 증분 pulse/count를 외부 counter/controller가 누적해 얻고, 정전 후 count 보존 또는 기준점 재설정이 없으면 absolute 위치를 보장하지 않는다. | Dynapar 제조사 handbook으로 verified; 예외 조건 명시; 점수 영향 없음 |
| `quadrature_direction_principle` | A/B 90 electrical degree 위상과 lead/lag로 방향을 판별하며, 유효 count/rev는 x1/x2/x4 수신기 decoding에 따른다. | Dynapar handbook 및 Rockwell HSC 문서로 verified; 점수 영향 없음 |
| `index_z_channel_role` | Z/index는 통상 회전당 reference pulse이며 homing/count 확인에 쓰지만, 누적 다회전 위치 자체를 encode하지 않는다. | Dynapar 제조사 문서로 verified; 점수 영향 없음 |
| `absolute_encoder_principle` | Absolute encoder는 모델의 single/multi-turn 범위 내 위치 word를 출력한다. 위치 샘플의 차분으로 속도를 추정할 수 있고 update/통신 속도도 동특성을 제한한다. | Dynapar 제조사 handbook 및 resolution/data-rate 가이드로 verified; 조건 한정; 점수 영향 없음 |
| `encoder_resolution_ppr_cpr_definition` | 카탈로그 PPR와 수신기 decoding 이후의 유효 count/rev는 다를 수 있다. PPR/CPR 약어만 보고 N_eff를 정하지 않고 선택 모델의 정의 및 receiver x1/x2/x4 mode를 확인한다. | Dynapar·OMRON 공식 제조사 문서로 verified; 약어의 보편 정의를 단정하지 않음; 점수 영향 없음 |
| `encoder_frequency_limit_selection` | `f=n·N_eff/60` 관계에서 최대 속도와 decoding mode가 event frequency를 결정한다. Encoder 출력단 및 receiving counter 입력의 frequency/pulse-width 제한을 각각 만족해야 한다. | Dynapar·Rockwell 공식 문서 및 단위 관계로 verified; 점수 영향 없음 |
| `inductive_proximity_principle` | 고주파 oscillator형 inductive prox는 금속 target eddy-current loss에 따른 oscillator damping을 threshold로 검출한다. 반복 target pulse를 RPM으로 변환할 때는 회전당 target event 수가 필요하다. | Balluff·Dynapar 공식 문서로 verified; sensor type 및 target 조건 명시; 점수 영향 없음 |
| `tachogenerator_voltage_speed_principle` | PM DC tachogenerator의 전압 크기는 지정 동작 범위에서 shaft speed에 대체로 비례하고, 극성은 회전 방향을 나타낼 수 있다. 상수·선형성·부하·온도 영향은 제품별 사양/교정으로 확인한다. | NEMA MG 1 정의와 Nidec 제조사 가이드로 verified; 점수 영향 없음 |
| `magnetic_pickup_variable_reluctance` | Passive magnet/coil형 VR pickup은 ferromagnetic target에 따른 자속 변화를 AC로 유도한다. 원시 신호 amplitude는 speed와 air gap/target에 의존해 저속 검출은 signal conditioner threshold에 좌우된다. | Analog Devices, NI 및 Magnetic Sensors Corp. 기술자료로 verified; sensitivity/minimum speed는 제품별 조건 명시; 점수 영향 없음 |
| `digital_tachometer_instrument_boundary` | Digital tachometer는 encoder 등 외부 pulse 또는 optical/contact sensing으로 RPM을 표시하는 계측기일 수 있다. `tachometer`라는 기기명만으로 tachogenerator sensor 원리를 뜻한다고 단정하지 않는다. | Tsuruga 및 Fluke 공식 사용자 매뉴얼로 verified; 모델별 입력방식 구분; 점수 영향 없음 |

## 추가 검토: OT 형상관리 Fact Anchor

`configuration_change_release_backup_rollback_migration_obsolescence_management`의 관련 Anchor를 NASA 형상관리 지침 및 NIST OT 보안 지침과 대조했다. baseline·version accounting·restore test는 기존 레지스트리 등록을 확인해 중복 추가하지 않았다. 이번 묶음에서 새로 추가한 것은 CI 범위 1건이다.

| Anchor | 확인 내용과 범위 | 처리 |
|---|---|---|
| `sw06_configuration_item_scope` | CI는 계획에서 통제 대상으로 선택·식별하는 항목이며, NASA는 통제 목록의 예로 문서·하드웨어·소프트웨어·모델을 든다. Pack의 펌웨어·설정·화면·인터페이스·라이선스가 모든 설비에서 반드시 별도 CI가 되어야 한다는 의미로 확대하지 않도록 조건을 붙였다. | verified 신규 등록; 점수 영향 없음 |
| `sw06_configuration_identification_relationship` | NIST SP 800-128은 CI별 고유 식별자, 시스템 소속, 구성요소·버전, 위치, 소유자, 운영 상태, 다른 CI와의 관계·의존성 및 재구성에 필요한 속성을 제시한다. 이 속성은 시스템 및 형상관리 계획에 맞춰 선택하며, 승인·현장 적용 상태는 변경 상태기록과 연계해야 한다. | 조건부 verified 신규 등록; 점수 영향 없음 |
| `sw06_change_request_problem_objective` | NASA SWE-113은 소프트웨어 변경/문제 보고서의 대상 항목, 현재 구성, 문제·변경 사유, 요청자·우선순위, 영향분석, disposition, 상태 및 이행·release 검증을 제시한다. “기대효과”와 상세 완료기준은 프로젝트별 추가 필드로 한정했다. | 범위를 제한해 verified 신규 등록; 점수 영향 없음 |
| `sw06_risk_based_approval_authority` | NASA SWE-082는 item criticality와 변경 영향 범위에 따라 변경통제 수준을 달리하고, 낮은 위험/영향은 낮은 권한에서, 중요·광범위 변경은 더 공식적인 권한에서 승인할 수 있다고 설명한다. 권한자와 변경 실행자의 역할을 계획에 명시하되, 요청·승인·배포의 완전한 분리가 모든 조직에 강제된다고 확대하지 않았다. | 조건을 제한해 verified 신규 등록; 점수 영향 없음 |
| `sw06_release_package_content` | NASA SWE-085 release guidance는 승인·release 절차, CI/버전/의존성 식별, master copy와 checksum 비교, 적용 가능한 VDD·release notes·설치·시험·rollback 자료를 다룬다. SWE-077은 source/executable 및 as-built 기록을 포함한 delivery 자료를 설명한다. 정확한 필수 산출물은 프로젝트·소프트웨어 분류에 따라 달라지므로 모든 항목을 모든 플랜트의 보편 의무로 확대하지 않았다. | 범위를 한정해 verified 신규 등록; 점수 영향 없음 |
| `sw06_release_control_authorized_artifact` | release authority, 절차, master-copy 식별·보관·checksum 비교, 적절한 접근통제와 configuration audit 근거는 확인했다. 다만 “임의 재빌드 또는 현장 직접수정을 방지”하는 표현은 결과/목표를 강하게 단정하므로, 이를 모든 환경의 보장 사실로 뒷받침하는 직접 근거는 부족하다. | 미등록 유지; release control 절차와 효과 보장 주장을 분리해 후속 검토 |
| `sw06_release_acceptance_and_asbuilt_update` | NASA SWE-077/084/085는 해당 소프트웨어 프로젝트의 정확한 버전·as-built/support records·형상감사와 release change의 시험·검증·종결을 지지한다. 하지만 Pack의 플랜트별 알람·인터페이스·운전성 확인 및 일률적인 사용자 인수를 모든 환경의 보편 요구로 주장하지 않도록 범위를 한정했다. | 범위를 제한해 verified 신규 등록; 점수 영향 없음 |

## 추가 검토: DP transmitter 3-valve manifold

Emerson/Rosemount 3051 manual §3.11.4에 따라 Coplanar transmitter zero-trim 순서를 확인했다. 기존 Pack의 `manifold_isolation_sequence`는 3-valve manifold에 bleed 조작을 포함하고 이를 일반 process isolation/depressurization으로 표현한다. `manifold_return_sequence`도 여러 밸브 동작을 보편 순서로 단정한다. 별도 교육자료의 H–equalize–L–bleed 순서는 하나의 절차 예로 확인되지만, Foxboro의 다른 bypass 구성과 Rosemount의 zero-trim 절차를 포함한 OEM 지침은 장치·구성·작업별이다. 사람 승인된 source hash를 바꾸지 않고 이 두 원문은 미검증으로 유지한다. 후속 검토 근거와 범위는 [`manifold sequence evidence follow-up`](topic_anchor_evidence_followup_20261011_manifold_sequences.md)에 기록한다.

| Anchor | 근거·판정 |
|---|---|
| `manifold_normal_state` | Emerson/Rosemount 3051 manual §2, pp. 2-20–2-21 및 3051S Reference Manual (Dec. 2025), p. 70: 해당 3-valve 구성에서 양쪽 isolate open, equalize closed. 별도 bleed/vent는 실제 구성 확인 조건으로 한정해 verified; 점수 영향 없음 |
| `dp_pressure_test_reference` | 비영 span 입력에는 H/L 포트 사이에 알려진 비영 ΔP가 필요하다. Equalizing passage가 열려 있으면 두 포트 압력을 평형시켜 span 자극을 shunt한다. 실제 시험배관·격리방식은 제품별 절차를 따라야 한다. | 물리 정의와 Emerson equalize 기능으로 verified; 구체적인 field sequence는 주장하지 않음 |
| `manifold_isolation_sequence` | 현재 Pack은 H close → equalize open → L close → bleed open을 일반 격리로 주장한다. 3051 manual §3.11.4의 zero-trim setup과 목적·단계가 다르며 3-valve에서 bleed 여부도 configuration-dependent. 미검증 유지; 사람 승인 후 zero-trim 예시와 actual isolation 경계를 분리 제안 |
| `manifold_return_sequence` | 현재 Pack의 bleed close → L open → equalize close → H open을 universal return으로 직접 뒷받침하는 자료 없음. 3051 manual은 zero-trim 이후 equalize close → LP isolate open만 명시. 미검증 유지; 제품·현장 절차 승인 필요 |

`process_isolation_fill_fluid`는 Emerson remote-seal 자료의 응답시간 변수(센서 범위, 모세관 길이/내경, 충전액 점도)와 온도·용도별 충전액 선정 근거를 확인해 성능·선정 범위만 verified로 등록했다. 앵커의 전체 pressure-transfer 구조를 더 넓게 입증했다고 보지는 않는다. `pulsation_damping_tradeoff`는 Emerson Anderson Greenwood의 특정 가스용 pressure-spike snubber가 고정 오리피스/소용적 챔버로 과도 압력상승을 감쇠하고 평균 정압은 바꾸지 않는다는 범위만 등록했다. 모든 snubber에 적용되는 response-speed trade-off는 입증되지 않았다.

“liquid service trapped gas는 항상 상부, gas service condensate는 항상 하부에서 처리”라는 문구도 보편 규칙으로 검증하지 않았다. 실제 배관 기울기·압력탭·설치 위치가 중요하다. Yokogawa 매뉴얼은 기체 서비스에서 transmitter를 탭보다 높게, 액체/증기 서비스에서는 낮게 두는 원칙과 기포·응축액 축적 시 측정오차를 설명하지만, 임의 manifold의 vent/drain 포트 위치를 단일 규칙으로 정하지 않는다.

## 추가 검토: 수동 R·C·L 센서 변환

`passive_sensor_resistive_capacitive_inductive_transduction`에서 두 Anchor를 독립 근거로
검증해 등록했다. `sensor_passive_transduction_chain`은 파라미터형 센서에서 측정량이 R/C/L을
바꾸고, 회로가 이를 읽을 수 있는 신호로 변환한다는 범위로 한정했다. 여기·브리지·증폭 등은
모든 센서에 동시에 필요한 기능이 아니라 선택 회로에 따라 달라지는 대안으로 명시했다.
NI의 DAQ 신호조절 문서와 Analog Devices의 CDC 회로 예, Rice ECE 센서 자료를 확인했다.

`sensor_material_property_geometry_separation`은 균일 도체 R=ρl/A, 평행판 C=εA/d, 선형
집중정수 자기회로의 ℜ≈lₘ/(μA), L≈N²/ℜ를 각 모델의 가정 아래 확인했다. Young's modulus는
선형 탄성의 기계적 응력-변형률 물성으로 구분했다. OpenStax, MIT OCW 및 기존 NIST 자료를
대조했다. 두 레코드 모두 `score_effect=none`이다.

같은 Pack의 `sensor_rcl_excitation_signal_conditioning`은 여기·브리지·증폭·필터·복조·선형화·
ADC 기능을 한 문장에 모두 묶어 모든 RCL 센서의 보편적 필수사슬처럼 읽힐 여지가 있어 미등록이다.
감도·선형성·환경 trade-off 및 교정/검증 전체 목록도 응용별 적용조건을 하나의 Anchor로
일반화하기 어려워 미등록 상태를 유지했다.

근거: [Emerson/Rosemount 3051 Reference Manual, Integral Manifold Operation](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/manual-rosemount-3051-revision-5.pdf), §2, pp. 2-20–2-21.

## 추가 검토: 수동형 센서 변환의 Young's modulus 기초

`sensor_mechanical_stress_strain_youngs_modulus`는 NIST SP 960-11 및 NISTIR 7847의 응력–변형률 설명으로 확인했다. 선형 탄성·단축응력 조건에서 `σ=Eε`이며, 같은 응력에서 E가 크면 axial strain이 작다. 단, 부품 전체 변위는 형상·길이·경계조건과 하중 분포까지 필요하므로 Pack의 “기하학적 변형”을 이 modulus만으로 완전히 정한다는 의미로 확장하지 않았다. 새 Fact는 점수 중립이다.

`sensor_inductive_gap_eddy_current_conductivity`는 variable-reluctance 공극과 와전류 probe를 분리해 검토했다. 단순 비포화 자기회로에서 `L=N²/ℜ`이고 공극 증가가 reluctance를 증가시킨다는 학술 교재의 근거를 확인했다. 와전류 쪽은 ASTM E2884 및 FHWA guide가 재료의 conductivity/permeability, 주파수, lift-off와 geometry가 penetration·coil response에 영향을 준다고 뒷받침한다. 결합변수 응답의 방향과 크기는 probe 구조·주파수·교정에 좌우되므로 보편적인 단조 관계로 일반화하지 않았다. 점수 중립.

`sensor_inductive_voltage_impedance_readout`는 `λ=Li`의 미분과 AC 소신호 회로 모델을 분리했다. 가변 L에서 `v=dλ/dt=L·di/dt+i·dL/dt`가 되는 것은 flux-linkage 정의의 chain rule 결과이며, 선형/소신호 가정과 passive sign convention을 명시했다. AC bridge 및 differential inductive sensor는 센서 L·impedance 변화가 출력전압으로 변환되는 대표 구현이며, 모든 센서에 모든 readout 방식이 동시에 적용되는 것은 아니다. 점수 중립.
| `sw06_baseline_approved_reference` | NASA의 baseline 정의와 승인된 기준선이 후속 변경의 기준이라는 설명을 확인했다. 이 Anchor는 기존 레지스트리에 이미 등록되어 있어 중복 생성하지 않았다. | 기존 verified 등록 유지 |
| `sw06_version_control_status_accounting` | NASA는 change control, status accounting, configuration authentication/audit를 별도 기능으로 다루며 변경·구현 상태와 as-built 기록을 추적한다. 기존 등록의 취지를 재확인했으며 새 중복 레코드는 추가하지 않았다. | 기존 verified 등록 유지 |
| `sw06_as_built_consistency` | 실제 작업물과 문서 대조는 NASA 절차로, OT backup 범위와 restore test는 NIST로 각각 지원된다. 그러나 현장·저장소·백업 사본이 항상 같은 시점을 나타내야 한다는 복합 주장의 직접 근거는 확보하지 못했다. | 미등록 유지; 각 하위 요구의 근거와 상호 일치 보장은 구분 필요 |
| `sw06_moc_trigger_and_scope` | NIST SP 800-82 Rev. 3는 OT configuration change control을 조직의 MOC에 맞추고, 안전·보안에 영향을 줄 수 있는 변경은 관련 담당자를 참여시키도록 안내한다. OSHA PSM MOC는 적용 대상 공정에서 지정된 변화의 기술 근거, 안전·보건 영향, 절차, 기간, 승인 등을 다루지만 이 법적 범위를 모든 산업의 품질·환경·보안·정비·규제 영향까지 포괄하는 보편 정의로 일반화할 근거는 아니다. | 보류; 관할·프로세스 범위를 붙이거나 일반 운영정책 권고임을 구분해야 함 |

범위가 넓은 `sw06_pre_change_backup_restore_readiness`는 복구 도구·버전·권한·매체별 요구까지 출처가 직접 뒷받침하지 않아 미등록으로 유지한다. `sw06_backup_scope_and_consistency`도 Pack의 레시피·화면·인증서/키·펌웨어·드라이버·라이선스·설치도구 전부가 보편적인 필수 백업 대상이라는 근거가 부족하다. NIST는 운전 데이터·프로그램·설정 파일·시스템 이미지·방화벽 규칙·ACL 등을 중요 백업 예시로 들며, 적용 시스템에 맞춘 백업 선정과 복원시험을 권고한다. 자료: [NASA Systems Engineering Handbook §6.5](https://www.nasa.gov/reference/6-5-configuration-management/), [NASA NPR 7123.1B Appendix C](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_7123_001B_&page_name=AppendixC), [NASA SWE-082 Authorizing Changes](https://swehb.nasa.gov/spaces/7150/pages/16450445/SWE-082%2B-%2BAuthorizing%2BChanges), [NIST SP 800-128](https://doi.org/10.6028/NIST.SP.800-128), [NIST SP 800-82 Rev. 3](https://doi.org/10.6028/NIST.SP.800-82r3), [NIST SP 1339](https://doi.org/10.6028/NIST.SP.1339).

MOC 범위 비교 자료: [NIST SP 800-82 Rev. 3, CM-3 / CM-4 OT Discussion](https://doi.org/10.6028/NIST.SP.800-82r3), [OSHA 29 CFR 1910.119(l)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119), [OSHA Appendix C, §11 Managing Change](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119AppC).

변경요청 필드 비교 자료: [NASA SWE-113](https://swehb.nasa.gov/spaces/7150/pages/16449697/SWE-113%2B-%2BSW%2BChange%2BRequest_Problem%2BReport), [NASA CR-PR recommended content](https://swehb.nasa.gov/spaces/SWEHBVD/pages/140640589/CR-PR%2B-%2BSoftware%2BChange%2BRequest%2B-%2BProblem%2BReport).

## 추가 검토: 수동 R·C·L 센서 파라미터와 readout

`passive_sensor_resistive_capacitive_inductive_transduction`의 파라미터형 변환 Anchor를
독립 확인했다. `sensor_passive_transduction_chain`은 측정량이 R/C/L 파라미터를 변화시키고
회로가 그 변화를 읽는 신호로 바꾼다는 범위로 한정했다. 여기·브리지·증폭·필터링 등은 모든
센서에 동시에 필요한 항목이 아니라 선택한 readout에 따라 달라지는 기능으로 제한했다.

`sensor_material_property_geometry_separation`은 균일 도체 `R=ρl/A`, 평행판 근사
`C=εA/d`, 선형 집중정수 자기회로 `ℜ≈lₘ/(μA)`, `L≈N²/ℜ`를 각 모델 가정 안에서 확인했다.
Young's modulus는 선형 탄성의 기계 물성으로 분리했다. `sensor_resistive_voltage_current_conversion`
과 `sensor_capacitive_dynamic_current_readout`은 기존 Fact가 이미 존재해 중복 등록하지 않았다.
해당 기존 Fact의 정전류·정전압·저항 브리지 대안과 `q=CV` 미분식은 각각 회로 조건과
passive sign convention을 포함한 기존 유도와 대조해 재확인했다. OpenStax, MIT OCW, NI,
Analog Devices 자료도 검토했다. 이번 회차에서 새로 추가한 두 레코드는 `score_effect=none`이다.

같은 Pack의 `sensor_rcl_excitation_signal_conditioning`은 여기·브리지·증폭·필터·복조·선형화·
ADC를 모든 RCL 센서가 함께 쓰는 보편적 신호사슬처럼 읽을 수 있어 미등록이다. 감도·선형성·환경
trade-off 및 전체 교정/검증 목록도 여러 세부 주장의 적용조건이 달라 단일 Anchor 전체를
검증하지 못해 보류했다.

## 추가 검토: 회전속도 센서 선정 및 설치

`speed_rotation_measurement_encoder_proximity_tachometer_selection_error`에서
`selection_direction_position_resolution`은 EPC의 encoder application guide로 확인했다.
필요한 정보가 speed/count, direction, incremental position 또는 absolute position인지 먼저
정의하고, quadrature decoding·해상도·encoder/receiver 최대 주파수와 controller 입력 호환을
함께 고려해야 한다. `electrical_interface_noise_error`도 EPC의 output-type, signal-noise 및
wiring guide로 확인했다. 차동 출력은 호환 차동 수신기가 있어야 common-mode noise 억제에
효과가 있고, supply/output voltage·cable·shield/ground·termination은 선택한 제품과 receiver
지침을 따라야 한다. 두 Fact 모두 점수 중립이다.

기존 네 복합 Anchor는 근거가 확인되는 범위로 source 문구를 좁혀 모두 verified했다. 각 제품의
정량 한계와 적용별 조건을 보편 규칙으로 확장하지 않았다.
`proximity_airgap_target_error`는 ifm의 inductive sensor 감지거리/target 가이드와 speed-monitor
gear-tooth 설치 가이드로 재료·target 크기·tooth-to-gap geometry·설치거리 의존성을 확인했다.
추가로 Allegro gear-tooth sensor 자료는 air-gap 변화와 target vibration을 signal-processing
이상 상태로 명시하지만 inductive와 Hall sensing 원리를 동일시하지 않았다. Pack 문구를
operating gap 변화가 있을 때의 조건부 영향으로 좁히고 보편적 dropout 한계를 주장하지 않도록
수정했다. 근거: [ifm inductive sensor technology overview](https://www.ifm.com/us/en/us/overview/inductive/technology-overview/tech-overview), [ifm speed monitor installation guidelines](https://www.ifm.com/us/en/us/learn-more/motion-control/speed-sensors/di-learn-more/installation-guidelines), [Allegro ATS685 datasheet](https://www.allegromicro.com/-/media/files/datasheets/ats685-datasheet.pdf). `tachogenerator_direction_loading_error`는 제조사별 근거로 속도비례 출력, TDP 모델의 회전방향 polarity, 부하전류에 따른 단자전압 저하, magnet 온도계수, brush/commutator 및 기계 부착에 따른 ripple/harmonic을 확인했다. 일반적인 zero/linearity 변화 표현은 제거하고 수치·보상·허용부하·장착한계는 모델별 data sheet와 교정절차로 확인하도록 제한했다. 근거: [Hübner TDP 1,2 catalog](https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-catalog-en.pdf), [Hübner TDP 1,2 manual](https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-user-manual-en.pdf), [maxon DC-Tacho DCT 22 data](https://www.maxongroup.com/maxon/view/product/sensor/dctacho/118910), [maxon Motors as Generators](https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators). `selection_speed_range_low_high`는 encoder-based application의 속도범위·resolution·pulse frequency·response와 signal-chain limits, 적용 가능한 overspeed/acceleration 한계를 확인하는 범위로 등록했다. Startup/creep과 VR pickup amplitude는 기술·모델별이며 보편적 RPM 임계값을 주장하지 않는다. 근거: [maxon Encoder Selection – Speed Control](https://www.maxongroup.com/en-us/knowledge-and-support/blog/encoder-selection-part-three-speed-control), [Rockwell PowerFlex 750 Safe Speed Monitor manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/750-rm001_-en-p.pdf), [Pepperl+Fuchs KFU8-DWB-1.D data](https://files.pepperl-fuchs.com/webcat/navi/productInfo/pds/231209_eng.pdf). `mechanical_mounting_coupling_error`는 EPC hollow-bore encoder의 runout/bore misalignment와 Hübner TDP 1,2 coupling/centering/축하중 지침 및 misalignment harmonic 효과로 한정해 등록했다. coupling slip 또는 보편적인 torsional-vibration 오차를 주장하지 않는다. 근거: [EPC General Installation & Wiring Guide](https://www.encoder.com/hubfs/pdf-downloads/general-info-installation-troubleshooting/general-installation-wiring-guide.pdf), [Hübner TDP 1,2 manual](https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-user-manual-en.pdf). `lifecycle_maintainability_selection`은 원래의 replacement, shutdown,
hazardous-area 및 lifecycle-cost 일괄 요구를 제거하고, EPC WP-2002가 제시하는 encoder 분해능·출력·주파수·기계 형식·환경과 receiver/controller 호환 기준으로 좁혀 등록했다. 높은 분해능이 encoder/receiver 주파수 한계를 넘거나 시스템 정확도를 자동 향상하지 않는다는 EPC 설명, 그리고 Siemens S7-1200 HSC input filter를 HSC용으로 설정하라는 기종별 문서를 대조했다. PLC filter 값은 CPU/input별이므로 일반 수치로 확장하지 않았다. spare/shutdown/방폭/lifecycle 비용을 보편 요구로 보지 않으며, 방폭 세부는 별도 Topic 소유다. 근거: [EPC Applying Encoders WP-2002](https://www.encoder.com/wp2002-applying-encoders), [Siemens S7-1200 System Manual V4.7](https://support.industry.siemens.com/cs/attachments/109977302/s71200_system_manual_en-US.pdf).

## 추가 검토: balanced/unbalanced trim pressure-force 및 sealing

`balanced_trim_unbalanced_trim_structure_sealing_applications`의 4개 미등록 Anchor를
Emerson/Fisher Handbook, Fisher HP/HPA 제조사 매뉴얼·force sizing 자료와 대조해 독립 Fact로
등록했다. `trim_pressure_boundary_terms`는 대표 cage-guided balanced sliding-stem construction의
seat interface와 plug-to-cage balance seal이 서로 다른 압력/밀봉 경로임을 확인하되, 실제 area와
경계는 제품 도면·매뉴얼 종속이라고 한정했다. `force_direction_sign_convention`은 제조사의
balanced/unbalanced 및 flow-up/down별 signed force equation과 pressure traction resultant를
대조하여, 양의 stem axis와 실제 젖은 면/유효 면적이 정의되어야 방향을 말할 수 있다고 제한했다.
`balance_seal_leakage_path`는 Fisher가 plug-to-cage seal과 plug-to-seat sealing surfaces를
별도로 그린 자료로 확인했다. `seat_load_shutoff_margin_boundary`는 Fisher actuator method가
plug unbalance, seat load, packing friction 및 construction-specific force를 구분하는 것을
확인했다. 새 Fact 4개도 모두 `score_effect=none`이다.

나머지 12개 Anchor는 다음 사유로 verified 승격하지 않았다.

| Anchor | 판정 |
|---|---|
| `control_valve_balanced_unbalanced_scope` | 단일 사실보다 본 Topic의 범위/종합 요구를 정의하는 메타 Anchor다. 기술적으로 참·거짓인 하나의 명제로 축약하지 않아 Fact registry에 넣지 않았다. |
| `balance_seal_loading` | ΔP·seal 구조와 제품 설계가 영향을 주는 점은 합리적이나, preload·온도·wear까지 포함한 일반식/보편 하중 모델을 확인할 근거가 부족하다. |
| `actuator_sizing_topic1_handoff`, `dynamic_friction_topic3_handoff`, `body_cage_guide_topic4_handoff`, `low_noise_trim_topic9_boundary`, `leakage_packing_topic13_boundary`, `severe_service_material_topic14_boundary` | 기술법칙이 아니라 저장소 내 Topic 소유권·routing contract다. 각 목적지 Pack의 존재와 제목은 확인할 수 있지만, 이를 독립 기술 사실로 verified하는 것은 범주 오류이므로 별도 분류 대상으로 남긴다. |
| `clean_high_dp_large_size_application` | 제조사 자료는 특정 balanced trim이 high-ΔP에 쓰이고 unbalance force를 줄이는 사례를 지원한다. 하지만 “clean” 조건 및 일반적인 size/선정 기준까지 일괄 뒷받침하지는 않는다. |

근거: [Emerson Fisher Control Valve Handbook, 5th ed., Chapter 3](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf), [Fisher HP/HPA Instruction Manual D101634X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012-hp-and-hpa-control-valves-fisher.pdf), [Fisher HP/HPA force equations D103428X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf), [Valmet Neles AU/AB/AM catalogue 4GV23EN](https://www.valmet.com/globalassets/sharepoint/imported/4gv23en.pdf).

## 추가 검토: Historian·streaming·quality 이벤트

`historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`에서 표준/제품 문서가
직접 지지하는 하위 사실 2개를 기존 Anchor에 연결했다. `streaming_event_processing`은 Apache Flink의
event-time 모델로 한정했다. Flink에서 watermark는 event-time 진행을 표시하며 watermark가 지난 뒤
도착한 레코드는 late event가 된다. 따라서 late-data 처리는 해당 애플리케이션의 window/result 정책에
달려 있다. 이를 모든 historian 제품의 필수 기능으로 일반화하지 않았다.

`quality_event_preservation`은 더 좁게 OPC UA Part 4의 DataChangeFilter 계약만 등록했다. OPC UA는
StatusCode 변경만으로 notification을 발생시키는 `STATUS` trigger를 정의한다. 다만 서버/monitored-item
지원과 클라이언트 설정, 후단 archive 보존은 별도이므로 “모든 deadband/compression이 quality·alarm·batch
경계를 자동 보존한다”는 뜻으로 확대하지 않았다. 두 Fact 모두 `score_effect=none`이다.

`historian_not_backup_only`는 AVEVA의 공식 제품 페이지로 AVEVA Historian의 process/alarm/event
이력, 압축·쿼리·trend 및 trend 내 alarm context 기능만 제품 한정으로 verified 등록했다. AVEVA는
Historian을 operations-control과 통합된 process database로 설명한다. 다만 품질 의미·Context·
traceability가 모든 제품에서 Historian 단독으로 제공된다는 보편 주장은 미등록이다.

근거: [AVEVA Historian 공식 제품 문서](https://www.aveva.com/en/products/historian/).

근거: [Apache Flink, Timely Stream Processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/), [OPC Foundation, OPC UA Part 4: Services, §7.22](https://reference.opcfoundation.org/specs/OPC-10000-4/7).

`temperature_measurement_error_heat_transfer`의 `temperature_error_reduction_measures`는
복합 권고 전체(설치위치·보호관·유속·복사차폐·단열·계산·교정)를 하나의 보편 규칙으로 검증하지 않았다.
다만 NIST 자료가 직접 지원하는 좁은 하위 사실—액체봉입 유리 온도계에서 교정 보정값은 지정 침지와
노출 stem 온도에 조건부이며 사용조건이 다르면 stem correction이 필요할 수 있음—은 별도 조건부
Fact로 기록했다. 이를 열전대·RTD나 산업용 전체 조립체의 같은 보정식으로 확대하지 않는다.
점수 영향은 없다. 근거: [NIST SP 300 Vol. 2, §5.4](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication300v2.pdf), [NIST Monograph 174](https://nvlpubs.nist.gov/nistpubs/Legacy/MONO/nbsmonograph174.pdf).

## 추가 검토: SW-06 형상관리·OT 백업

`configuration_change_release_backup_rollback_migration_obsolescence_management`의 SW-06 Anchor 중
NIST가 직접 지지하는 백업 복구 의존성 fact 1개를 새로 등록했다. 기존 `sw06_baseline_approved_reference`,
`sw06_backup_integrity_separation_retention`, `sw06_restore_test_recovery_evidence` 세 fact도 NIST
SP 800-82r3·SP 1339 원문으로 교차 재확인했다. 승인된 기준선은 “최신 파일”이나 “최근 백업”과 같다고
보지 않는다.

`sw06_pre_change_backup_restore_readiness`는 복구 대상 자산별 필요한 logic/configuration, I/O list,
firmware, HMI files, license, vendor tool, support documentation, OS/VM image 등을 식별하라는 NIST
SP 1339 지침으로 한정해 등록했다. 구체적 backup 항목과 테스트 시점은 설비와 복구 시나리오에 달린다.
기존 `sw06_backup_integrity_separation_retention`은 무결성 확인, 동일 재해에 영향받지 않는 보조 보관,
접근통제와 위험·중요도에 근거한 주기·보존 전략을 지지하는 범위로 유지하며, 모든 자산에 같은 매체나
보존기간을 요구하지 않는다.

기존 `sw06_restore_test_recovery_evidence`는 비생산 환경에서의 반복 복원시험, media 신뢰도·복원 절차·복구
시스템 기능 무결성 확인, 시험 교훈에 따른 절차/문서 개선으로 좁혔다. 보편적인 시험 주기나 acceptance
threshold는 주장하지 않는다. 네 Fact 모두 점수 영향이 없다.

나머지 SW-06 복합 체크리스트 Anchor는 NIST 자료가 개별 원칙 일부를 지지하더라도 모든 열거 항목을
보편적 필수조건으로 증명하지 못하거나, 조직 정책·제품·공정 위험에 종속되어 계속 미등록이다.

근거: [NIST SP 800-82 Rev. 3, §6.2.4.2–6.2.4.3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf), [NIST SP 1339, OT Backup Quick Start Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1339.pdf).

## 추가 검토: control-valve gain 및 저유량 구분

`control_valve_authority_rangeability_gain_installed_performance`의 `process_gain_operating_point_dependency`는
Fisher의 process-gain 정의와 installed-gain/installed-characteristic 자료를 대조했다. installed valve gain은
실제 계통에서 pressure drop 변화에 따라 달라지므로 특정 운전점·설치조건에서 평가해야
한다. `loop_gain_component_product`는 단일 피드백 루프를 한 운전점에서 선형화한 경우 controller,
actuator/positioner, installed valve, process 및 measurement blocks를 직렬 곱으로 취급하는 사실로
조건을 한정했다. `valve_process_gain_compensation`은 두 gain의 반대 방향 변화가 실제로 곱의 변동을 줄이는
경우만 대수적으로 확인했으며, 특정 valve trim이 모든 공정에서 보상을 달성한다고 주장하지 않는다.

`seat_leakage_not_minimum_control_flow`는 Fisher 자료의 정의를 대조했다. Seat leakage는 완전 닫힘 상태에서
정해진 시험 ΔP/온도의 누설이고, rangeability는 최대/최소 controllable flow를 다룬다. 따라서 차단 누설과
스로틀링 최저 제어 유량은 다른 operating condition/metric이다. 네 새 Fact 모두 점수 영향이 없다.

`control_range_gain_acceptance_concept`는 “gain 또는 성능 기준을 만족하는 control range”라는 현장/분석상
정의에 가깝고, 보편적인 업계 정의로 특정하기 어려워 보류했다. `minimum_controllable_flow_limits`는 trim,
resolution/deadband/stiction, Reynolds 및 measurement 영향이 한 문장에 결합되어 있다. 이번 자료는 일부
요소를 뒷받침하지만 전체 목록을 동일 적용범위에서 확인하지 못해 미승격 상태로 유지한다.

근거: [ISA InTech, Understanding Control Valve Flow Characteristics](https://www.isa.org/intech-home/2023/june-2023/features/understanding-control-valve-flow-characteristics), [Fisher Control Valve Sourcebook—Refining](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/control-valve-sourcebook-refining-en.pdf), [Fisher Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [MIT OCW control-system notes](https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/bfcda6f40bad59b61b3f28ab8da1c86f_MIT2_017JF09_control.pdf).

## 추가 검토: 액체 제어밸브 상변화·초크

`control_valve_cavitation_flashing_choked_flow_damage_prevention`에서 기술 Fact 3개를 Emerson/Fisher 자료와
사이징 관계식으로 교차 확인했고, 별도 내부 ownership Anchor 1개를 Topic Sheet와 현재 canonical Topic ID로 확인했다.

- `liquid_pressure_profile_scope`: Fisher의 액체 초크 유량 관계식은 P1, Pv, Pc, FF, FL을 명시하고,
  설명은 vena contracta에서의 압력저하와 증기 형성을 연결한다. P2는 실제 밸브 차압 정의에 포함된다.
- `fl_direction_and_cavitation_susceptibility`: Fisher 자료는 비교한 밸브 구성에서 낮은 FL이 높은 압력회복과
  더 큰 cavitation susceptibility와 연결될 수 있다고 설명한다. 이를 모든 제품의 절대 순위로 일반화하지 않았다.
- `reduce_total_pressure_drop_prevention`: Fisher 자료에서 downstream pressure를 높여 밸브 차압을 낮추면
  vena-contracta pressure를 올릴 수 있고, 해당 운전점에서 vapor pressure 위로 유지되면 cavitation을
  방지할 수 있다. 다른 조건과 운전점도 별도 검토해야 한다.
- `topic9_topic14_handoff`: 저장소 내부 handoff 계약으로 한정했다. 현재 Topic 9는 noise prediction,
  Topic 14는 severe-service material 상세를 소유한다. 이는 외부 표준이나 보편 공학법칙이 아니다.

`cavitation_inception_development_damage_levels`는 Fisher가 Ki와 Kc를 구분하고 Kc는 valve style/trim에
의존하며 예시 지침에도 적용 범위가 있다고 명시한다. 따라서 특정 계수와 서비스 범위를 넘는 하나의 universal
threshold는 두지 않는 조건부 사실로 등록했다. `flashing_service_geometry_location`은 flashing 발생 자체가 계통 조건에 달려 있고 밸브 위치·유로 방향이
손상 위치·크기에 영향을 준다는 자료는 확인했지만, Anchor에 열거된 downstream pipe size까지 같은 근거로
포괄하지 않아 미승격으로 남겼다. 전체 기동·정지/운전점 목록도 조건·제품별 근거가 충분하지 않아 보류했다.
`vendor_crosscheck_liquid_phase_change`는 Fisher Sourcebook의 액체 사이징 절차·계수 정의·초크 한계와
선정 개도 예제를 대조해 조건부로 검증했다. 검증 범위는 적용되는 ISA/IEC 사이징 방법에 따라 각 서비스
케이스의 절대압력·온도별 증기압·필요 계수·초크 제한·선정 밸브 용량/개도를 동일 방법의 수계산으로 재현
점검하는 것이다. FF는 Pv/Pc에 따라 산정하며, FL은 밸브 계수이고 FP/FLP는 해당 배관 피팅 구성과 방법이
요구할 때만 적용한다. 계수는 제품/구성에 종속되며, 수계산 일치는 계수 자체의 시험 정확도나 손상 예측을
독립 입증하지 않는다. `topic9_topic14_handoff`는 기술 사실이 아니라 토픽 범위 메타데이터이므로 미승격이다.
이 Fact도 `score_effect=none`이다.

`balanced_trim_unbalanced_trim_structure_sealing_applications`의
`clean_high_dp_large_size_application`은 Fisher Sourcebook의 정적 불평형력 식과 balanced valve 잔류면적,
그리고 Fisher cryogenic balanced-trim 제품자료의 고압·고유량 actuator-force 이점을 대조했다. 따라서
서비스가 선택된 seal/trim과 호환되는 경우 고압차 또는 큰 globe valve에서 balanced trim을 후보로 평가할 수
있다는 조건부 내용만 verified 처리했다. 추력 감소량·작은 actuator의 보장·zero-force를 주장하지 않으며,
실제 선정은 잔류 불평형면적, seat load, seal/packing 마찰, 동적 힘과 제조사 한계를 포함해 수행한다.
`score_effect=none`이다. 근거: [Emerson/Fisher, Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), Chapter 2, pp. 2-7–2-8; [Fisher easy-e Cryogenic Valves](https://www.emerson.com/content/dam/emerson/en/final-control-fctl/pressure-management/jt-valves/documents/product-bulletin-fisher-easy-e-cryogenic-sliding-stem-control-valves-en-122402.pdf), Features.

`vendor_cutaway_force_table_crosscheck`는 Fisher sizing 자료의 제조사별 force-calculation 차이, balanced valve의 net unbalance area를 vendor로부터 확인한다는 지시, actuator output과 critical travel force comparison을 근거로 등록했다. 모델 instruction manual은 seal/backup-ring의 재료·온도 한계 및 cyclic wear·정비 권고를 별도로 제공한다. 따라서 cutaway, effective-area/force table, seal limit, maintenance 자료를 **선정한 모델·trim·revision에 해당하는지 대조하는 절차**로 확인했으며, 제품별 수치나 inspection interval을 일반화하지 않는다. `score_effect=none`이다. 근거: [Emerson/Fisher, Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), Chapter 2, pp. 2-7–2-8; [Fisher EHAT NPS 16x20 Instruction Manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103600x012.pdf), Table 2, Table 7.

`high_temperature_cryogenic_seal_limit`도 제품별 확인 사실로 verified 처리했다. Fisher HP 자료는 고온 balanced trim의 graphite piston-ring 및 tight-shutoff 구성에서의 PTFE/PEEK anti-extrusion 조합을 서로 다른 적용조건으로 제시하고, easy-e Cryogenic 자료는 별도 spring-loaded seal 구성과 해당 제품별 저온·누설등급을 제시한다. 따라서 재료의 P/T 한계, clearance/anti-extrusion, actuator force·friction 및 shutoff class를 선택 모델의 자료로 확인해야 한다. 하나의 공통 seal 한계나 모든 hot/cryogenic trim에 적용되는 수치는 주장하지 않는다. `score_effect=none`이다. 근거: [Fisher HP Series Product Bulletin D101635X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101635x012-bulletin-hp-series-control-valves-fisher.pdf), [Fisher easy-e Cryogenic Product Bulletin](https://www.emerson.com/content/dam/emerson/en/final-control-fctl/pressure-management/jt-valves/documents/product-bulletin-fisher-easy-e-cryogenic-sliding-stem-control-valves-en-122402.pdf), [Fisher Catalog 14](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf).

`fluid_compatibility_seal_degradation`을 탄성체 seal 범위로 한정해 확인했다. Parker의 seal handbook에 따르면 매질의 흡수·추출로 팽윤·수축과 물성 변화가 생길 수 있고, 압력·간극·온도와 매질 변화가 압출 위험에 영향을 준다. 가압 가스 투과·급속 감압 손상은 해당 가스 service와 감압 조건에, 마모는 동적 seal motion에 적용되는 조건부 고장 양상이다. 이를 PTFE·graphite·금속 등 모든 balance seal 재료에 일반화하지 않도록 Anchor를 명시적으로 좁혔다. `score_effect=none`이다. 근거: [Parker O-Ring Handbook PTD5705-EN](https://www.parker.com/content/dam/Parker-com/Literature/Praedifa/Catalogs/Catalog_O-Ring-Handbook_PTD5705-EN.pdf), §§1.2, 2.2, 6.8, 10.2, 10.5–10.6.

`dirty_slurry_particulate_limit`은 입자 크기와 실제 trim 유로에 종속되는 plugging/erosion 위험으로 범위를 제한했다. Fisher HP/HPA 매뉴얼은 small internal passage와 미청정 매질에서 입자 lodging을 막기 위한 upstream strainer 검토를 권고하고, 해당 balance-hole 구성에서는 분해 정비 때 퇴적·막힘을 점검·제거하도록 한다. 별도 dirty-service trim 사례는 sand/clay를 포함한 특정 서비스에 큰 particle-passing opening을 적용한 것으로, 모든 slurry의 입자 한계나 seal wear를 일반화할 근거로 쓰지 않았다. `score_effect=none`이다. 근거: [Fisher HP/HPA Instruction Manual D101634X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012-hp-and-hpa-control-valves-fisher.pdf), §§2, 3.6; [Fisher HPT Dirty Service Trim case](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351454x012_1.pdf).

`operating_case_force_matrix`의 minimum/normal/maximum은 제조사 sizing 도구가 명시하는 service-condition 종류로 확인했다. 각 정의된 조건 중 선택 밸브·액추에이터에 영향을 주는 case에 대해 critical travel에서 압력차, 잔류 불평형 면적, 정·동적 유체력, seal/bearing/packing 마찰과 seat load를 검토한다. Startup/shutdown은 설계기준에 해당 case가 있을 때만 포함하고 모든 밸브에 공통 필수라고 보지 않는다. `score_effect=none`이다. 근거: [Fisher Specification Manager Quick Start Guide D103533X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103533x012.pdf), pp. 9–11; [Fisher Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), Chapter 2, pp. 2-7–2-9.

`balanced_trim_unbalanced_trim_structure_sealing_applications`의 `balance_seal_loading`은
Fisher의 balanced plug 설명에서 balance seal이 plug–cage 사이의 secondary pressure/leakage boundary임을,
cryogenic product bulletin에서 spring-loaded seal ring·backup/retaining ring 및 재료별 온도한계를,
EHAT instruction manual에서 plug spring-loaded seal ring이 cycled wear part임을 대조했다. 이 근거를
종합해 차압·압력전달, seal/backup-ring geometry와 spring loading, 온도별 재료 한계, 반복 운전 마모가
설계별 seal 거동 또는 정비에 영향을 줄 수 있다고 조건부 확인했다. 이는 요인의 방향·크기를 정량화하거나
보편적인 seal-load 방정식을 주장하지 않으며, 실제 선정과 정비는 해당 모델의 제조사 자료 및 서비스 조건을
따른다. `score_effect=none`이다.
근거: [Emerson/Fisher Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf); [Fisher easy-e Cryogenic Valves, Product Bulletin](https://www.emerson.com/content/dam/emerson/en/final-control-fctl/pressure-management/jt-valves/documents/product-bulletin-fisher-easy-e-cryogenic-sliding-stem-control-valves-en-122402.pdf); [Fisher EHAT Instruction Manual D103600X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103600x012.pdf).

근거: [Emerson/Fisher, Choked Flow, Product Bulletin 59.1:095](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d104173x012.pdf), [Emerson/Fisher, Control Valve Handbook, Chapter 4](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf), [Emerson/Fisher, Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/it/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf).

`safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`의 MC/DC 기준 정의와 기초 coverage 간 차이를 NASA 자료로 독립 확인했다. NASA/TM-2001-210876은 statement coverage를 실행 가능한 statement 실행, decision coverage를 각 decision의 True/False 결과, condition coverage를 각 atomic condition의 모든 결과로 구분하며, decision과 condition coverage가 독립 영향 증거를 보장하지 않는 예를 든다. NASA/CR-2006-214307의 MC/DC 설명은 entry/exit invocation, condition outcome과 independent effect를 포함한다. 따라서 기존 `mcdc_definition`의 “진입점·종료점 실행은 MC/DC 정의와 구분한다”는 문구는 바로잡아, 인용한 DO-178B 정의의 일부로 반영했다. Unique-cause와 masking 같은 pair 허용방법은 적용 기준에 따라 다를 수 있어 일반화하지 않았다. `score_effect=none`이다. 근거: [NASA/TM-2001-210876, A Practical Tutorial on MC/DC](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20010057789.pdf), §§2.3.1–2.3.5; [NASA/CR-2006-214307, Testing Strategies for Model-Based Development](https://ntrs.nasa.gov/api/citations/20060018336/downloads/20060018336.pdf?attachment=true), §4.2.1.

## 추가 검토: installed characteristic 설계 검토

`control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`에서
`control_valve_manufacturer_curve_system_model_verification`을 확인해 Fact로 등록했다. 제조사 inherent
curve는 일정한 시험 밸브 차압을 전제로 하고, installed characteristic은 실제 계통의 pump head 및
배관·기기 손실로 달라질 수 있다. Fisher sizing 자료는 운전 flow와 상·하류 압력, 유체 특성을 사용한다.
normal point는 해당 설계
운전범위에 정의된 경우 포함하는 조건부 적용으로 기록했으며, 특정 계산 도구나 보편 gain acceptance limit을
요구하지 않는다. 점수 영향은 없다.

같은 토픽의 `control_valve_commissioning_characteristic_verification`은 아직 등록하지 않았다. commissioning에서
매번 command·travel·상하류 pressure·flow를 함께 비교해 기대 installed curve를 검증해야 한다는 전체 절차를
직접 뒷받침하는 근거를 확인하지 못해 미검증으로 남겼다.

근거: [ISA InTech, Understanding Control Valve Flow Characteristics](https://www.isa.org/intech-home/2023/june-2023/features/understanding-control-valve-flow-characteristics), [ISA InTech, Using Control Valve Installed Gain Calculations](https://www.isa.org/intech-home/2021/december-2021/features/using-control-valve-installed-gain-calculations), [ISA-75 standards overview](https://www.isa.org/standards-and-publications/isa-standards/isa-75-standards).

## 추가 검토: control range와 minimum controllable flow

`control_valve_authority_rangeability_gain_installed_performance`에서 두 앵커의 검증 범위를 보완했다.
`control_range_gain_acceptance_concept`는 Emerson/Fisher Sourcebook의 정의—installed gain이 normalized
0.5–2.0 범위에 있는 valve travel 구간—로 제품 자료 내 기준을 verified했다. 이 band를 모든 process의
보편 합격 기준으로 확대하지 않았다.

`minimum_controllable_flow_limits`는 Emerson/Fisher가 `clearance flow`를 minimum controllable flow 이하의
비착좌 유량으로 별도 정의하고 rangeability를 명시 편차 한계 내 max/min Cv 또는 controllable flow 비로
정의한 점을 확인했다. Siemens 자료는 variable-flow hydronic 사례에서 최소 제어부하를 rangeability와
authority에 연계한다. 따라서 “최소 제어 유량은 seat leakage와 같지 않고 installed rangeability/authority와
연관된다”는 한정 사실만 verified했다. Anchor의 나머지 요인 전체—Reynolds effect, resolution, deadband,
stiction 및 measurement noise를 모든 제어밸브에 적용되는 결정요인으로 묶은 부분—은 충분히 검증되지 않아
미승격 상태다. 두 Fact 모두 `score_effect=none`이다.

근거: [Emerson/Fisher Control Valve Sourcebook—Refining](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/control-valve-sourcebook-refining-en.pdf), §5.2/§5.5; [Siemens, Balancing and Control Valve Sizing for Direct-Return Variable-Flow Hydronic Systems](https://sid.siemens.com/api/khub/documents/7YnMwxxqJYd7WDqKRycmhQ/content), pp. 10–15.

## 추가 검토: 생산 단위원가의 분모와 비용 경계

`production_unit_cost_volume_yield`를 검토해 `production_unit_cost_defined_cost_boundary_and_output_denominator` Fact로 등록했다. OpenStax 관리회계 교재는 제품원가를 직접재료·직접노무·제조간접비로 구성하고, 단위·배치·제품 수준 비용을 구분하며, 공정원가에서는 미완성품을 등가생산량으로 처리함을 설명한다. 따라서 단위원가는 먼저 비용 범위와 생산량 분모를 정의해야 한다. 양품당 운영원가로 사용할 때는 양품·불량·재작업 포함 여부를 밝히도록 제한했다. 이는 모든 회계 목적에 양품 수량을 분모로 강제하는 정의가 아니다. 고정비와 변동비 행동이 다르므로 생산량 증감만으로 단위원가가 같은 비율로 변한다고도 단정하지 않는다. 점수 영향은 없다.

근거: [OpenStax, Managerial Accounting §6.3](https://openstax.org/books/principles-managerial-accounting/pages/6-3-calculate-activity-based-product-costs), [§2.2](https://openstax.org/books/principles-managerial-accounting/pages/2-2-identify-and-apply-basic-cost-behavior-patterns), [§5.3](https://openstax.org/books/principles-managerial-accounting/pages/5-3-explain-and-compute-equivalent-units-and-total-cost-of-production-in-an-initial-processing-stage).

같은 생산관리 Topic의 `production_material_requirement_availability`는 SAP S/4HANA MRP 절차에서 요구량과 재고·예정입고 비교, 부족 시 조달제안, 자재별 설정 lot-sizing과 일정 산정, 자체생산의 BOM 전개를 확인했다. Oracle MRP 문서도 master schedule·BOM·예정입고·재고·lead time·order modifier를 계획입력으로 제시하면서 해당 MRP 계획이 무한능력을 가정한다고 명시한다. 따라서 fact 범위를 MRP 계획·제안 산출로 제한하고, 공급자 실물공급 보장·라인사이드 도착·대체품 적격성·유한능력 가능성은 별도 검증 대상으로 남겼다. 점수 영향은 없다.

근거: [SAP S/4HANA, Net Requirements Calculation](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/fe39e10a9a864a8f8dc9537704f0fa13/46abce5314894208e10000000a174cb4.html), [SAP S/4HANA, MRP Procedure](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/fe39e10a9a864a8f8dc9537704f0fa13/d5aace5314894208e10000000a174cb4.html), [Oracle E-Business Suite, MRP User's Guide](https://docs.oracle.com/cd/E26401_01/doc.122/e48795/T478564T478850.htm).

`production_fpy_yield_scrap_rework`는 ASQ의 FPY 정의와 NIST 논문의 품질 KPI 정의·식을 대조했다. FPY는 정의된 공정을 재작업·재검사 없이 통과한 양품을 세는 반면, 일부 최종 품질률은 재작업 후 양품을 포함할 수 있다. NIST 논문은 scrap ratio, rework ratio, first-time quality와 quality-buy-rate의 서로 다른 분모·계산식을 구분하고, quality-rate의 재작업 포함 여부가 ISO 22400-2 정의와 다를 수 있다고 명시한다. 따라서 지표 이름만으로 분모/재작업 취급이 같다고 보지 않도록 검증 범위를 한정했다. 점수 영향은 없다.

근거: [ASQ Quality Glossary, First Pass Yield](https://asq.org/quality-resources/quality-glossary/f), [Kang et al., NIST-hosted peer-reviewed study](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=919754), §§3.1.2 and 3.2.2.

`production_line_balancing_workload`는 기초 assembly-line-balancing 문제에서 작업을 station에 배정하며 선후관계와 cycle-time 제한을 만족하는 정의를 검증했다. 목적함수는 모델 variant에 따라 cycle time 또는 station 수 최소화 등으로 달라진다. Lean Enterprise Institute는 takt를 고객수요를 만족하기 위한 생산 pace로 정의하고 operator work sequence·manual/walk/machine content를 이에 맞춰 설계하는 표준작업을 설명한다. 기본 모델에 없는 작업자 적격성·장비능력·제품 Mix 등의 제약은 관련 시 별도로 모델링하도록 범위를 제한했다. 점수 영향은 없다.

근거: [Battaïa & Dolgui, Assembly line balancing review](https://doi.org/10.1016/j.ejor.2021.11.043), [Lean Enterprise Institute, Standardized Work](https://www.lean.org/lexicon-terms/standardized-work/).

`production_throughput_cycle_lead_wip_kpi`는 UC Berkeley P2SL glossary의 정의·Little's Law 표현, NIST TN 1890의 제조 flow time 정의와 process-boundary 기반 측정 방법을 대조해 확인했다. Throughput은 단위시간당 산출량, WIP는 공정 경계 내 재공량, flow/cycle/lead time은 시간 지표로 차원이 다르므로 같은 지표로 취급할 수 없다. Little's Law 적용 시 같은 경계·단위·기간의 장기 평균을 비교하고 시스템 안정성을 가정해야 하며, cycle time/lead time 용어는 조직별 정의를 먼저 고정하도록 제한했다. 점수 영향은 없다.

근거: [UC Berkeley P2SL, Little's Law and WIP glossary](https://p2sl.berkeley.edu/glossary/knowledge-center-glossaryatoz/), [NIST TN 1890, Inventory and Flow Time in US Manufacturing](https://doi.org/10.6028/NIST.TN.1890).

`production_manpower_skill_shift`는 workforce skills matrix와 작업능력/훈련 공백을 관리하는 부분만 verified했다. LEI는 Skills Matrix를 개인별 standardized-work 계획의 일부로 설명하고, OSHA는 robot application 작업자에 대해 assignment 전 안전훈련과 안전한 작업 수행능력의 증명을 구체적으로 요구한다. NIST TWI 자료는 표준화된 Job Instruction과 교차훈련을 설명한다. 이 근거들은 해당 역량·자격 검토를 지지하지만, Anchor에 포함된 교대별 인원 산정, 휴무·교육·결원 보정 공식이나 모든 직무의 보편 자격요건을 뒷받침하지 않는다. 해당 수량·규칙은 현장 조건으로 남기고 점수 영향은 부여하지 않았다.

근거: [Lean Enterprise Institute, Skills Matrix](https://www.lean.org/the-lean-post/articles/five-missing-pieces-in-your-standardized-work-part-3-of-3/), [OSHA Technical Manual, Robotics](https://www.osha.gov/otm/section-4-safety-hazards/chapter-4), [NIST MEP, Training Within Industry](https://www.nist.gov/mep/training-within-industry-twi).

`production_capacity_available_time_rate`는 per-shift operating time과 manual/machine/tool-change content를 포함해 resource/process capacity를 계산하고, operator/equipment loading을 takt와 비교하는 부분을 verified했다. LEI 표준작업 자료는 실제 양식 예를 제시하며, MIT Production Operations 자료는 변동 수요를 단일 capacity point가 아닌 operating range로 설계할 수 있음을 설명한다. 실제 출력은 제품 Mix·shift calendar·자원 범위와 관측조건에 좌우되고 보편적인 효율 계수는 이 근거만으로 정할 수 없으므로, 해당 일반화는 하지 않았다. 점수 영향은 없다.

근거: [Lean Enterprise Institute, Process Capacity Form and Operator Loading Chart](https://www.lean.org/wp-content/uploads/2022/05/breaking_through_standardized_work_confusion_joe_murli.pdf), [MIT Production Operations Guideline, Appendix A](https://dspace.mit.edu/bitstream/handle/1721.1/81899/PRD_TTL_ProdOpsDoc_V.1_2000.pdf).

`production_changeover_sequence_batch_tradeoff`는 batch size와 setup 빈도, WIP·cycle stock, queue/lead time의 상호작용을 확인했다. 대량 batch는 바꾸는 횟수를 줄일 수 있고, LEI의 value-stream 자료는 특정 긴 생산 run이 해당 흐름에서 lead time과 재공을 늘리고 mix 수요 대응을 어렵게 할 수 있음을 설명한다. 반대로 Vaughan의 queueing lot-size 모델은 lot을 계속 줄이면 setup 빈도와 이용률이 높아져 어느 지점 이후 queue 및 총 lead time이 늘 수 있음을 보인다. 그러므로 한 방향의 보편 최적화 규칙 대신 수요·설비능력·setup·흐름 조건을 함께 봐야 한다. 점수 영향은 없다.

근거: [Palaniswami, setup cost and batch-size factors](https://doi.org/10.1016/0925-5273(92)90064-E), [Vaughan, lot size and queueing/lead-time tradeoff](https://doi.org/10.1016/j.ijpe.2004.09.012), [Lean Enterprise Institute, Value-Stream Mapping](https://email.lean.org/hubfs/ebook%20files/eBook-Top5-VSM-final.pdf).

`production_standard_actual_cost_variance`는 OpenStax 표준원가와 variance analysis 내용을 검토해 등록했다. 비교 기준은 단순 전월 Actual이 아니라 정의된 standard/budget 및 생산량·기간의 비교 가능성이며, 일반적 변동 분석의 예로 재료 price/quantity, labor rate/efficiency, variable-overhead spending/efficiency를 확인했다. Scrap/rework·energy·downtime은 조직이 원가에 반영하고 원인 추적할 수 있으나, 모두가 보편적으로 같은 formal variance account인 것은 아니다. 숫자 차이만으로 원인을 확정하거나 개선조치를 자동 도출하지 않는다는 범위를 명시했다. 점수 영향은 없다.

근거: [OpenStax Managerial Accounting §8.1](https://openstax.org/books/principles-managerial-accounting/pages/8-1-explain-how-and-why-a-standard-cost-is-developed), [§8.2 Materials Variances](https://openstax.org/books/principles-managerial-accounting/pages/8-2-compute-and-evaluate-materials-variances), [§8.4 Overhead Variances](https://openstax.org/books/principles-managerial-accounting/pages/8-4-compute-and-evaluate-overhead-variances), [§8.5 Variance Analysis](https://openstax.org/books/principles-managerial-accounting/pages/8-5-describe-how-companies-use-variance-analysis).

`production_cost_structure`는 OpenStax의 manufacturing product-cost categories를 기준으로 직접재료·직접노무·제조간접비 구성을 확인했다. 간접재료·간접노무·utilities·설비 depreciation은 overhead 예시이며, 비용을 직접 추적할 수 있는지와 선택한 costing method에 따라 분류와 배부가 달라진다. 따라서 scrap/rework/energy/consumables의 unit-cost 포함 규칙을 모든 목적에 대해 고정하지 않고, 원가 측정 목적과 회계정책에 기록하도록 제한했다. 점수 영향은 없다.

근거: [OpenStax §4.2 Manufacturing Product Costs](https://openstax.org/books/principles-managerial-accounting/pages/4-2-describe-and-identify-the-three-major-components-of-product-costs-under-job-order-costing), [§4.4 Overhead Allocation](https://openstax.org/books/principles-managerial-accounting/pages/4-4-compute-a-predetermined-overhead-rate-and-apply-overhead-to-production), [§6.3 Activity-Based Product Costs](https://openstax.org/books/principles-managerial-accounting/pages/6-3-calculate-activity-based-product-costs).

`production_demand_order_plan_translation`은 SAP Demand Management가 planned independent/customer requirements를 구분하고 날짜·수량·전략을 제공하며, 이후 생산계획이 due date·capacity·제약을 고려해 mixed-model sequence를 구성하는 부분을 verified했다. SAP 문서의 make-to-order forecast consumption은 특정 strategy 예시이므로 보편 규칙으로 확대하지 않았다. rolling replan 주기, 제품 mix 우선순위 정책은 조직/시스템 설정이므로 고정하지 않았다. 점수 영향은 없다.

근거: [SAP Transfer to Demand Management](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/d853922bdd584e8e83027e5a0b8122f2/5e6ebd534f22b44ce10000000a174cb4.html), [SAP Model Mix Planning](https://help.sap.com/saphelp_scm700_ehp02/helpdata/en/da/5a0751b9134338e10000000a154ce5/content.htm), [SAP Sales Order Oriented Planning](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/f899ce30af9044299d573ea30b533f1c/5a51c95360267614e10000000a174cb4.html).

`control_valve_installed_local_slope_topic_boundary`는 ISA의 installed-characteristic 정의와 installed-flow/gain 자료, Emerson/Fisher Control Valve Handbook을 대조했다. 특정 시스템의 installed flow–travel 곡선은 밸브 차압이 시스템에 따라 변하는 관계이며, 그 곡선의 국부 기울기는 해당 운전점의 installed gain이다. 이 사실을 authority 또는 rangeability와 같은 개념으로 취급하지 않도록 범위를 제한했다. Topic 간 소유권 문구 자체를 보편 기술사실로 확장하지 않았으며 점수 영향은 없다.

근거: [ISA InTech, Understanding Control Valve Flow Characteristics](https://www.isa.org/intech-home/2023/june-2023/features/understanding-control-valve-flow-characteristics), [ISA InTech, Using Control Valve Installed Gain Calculations](https://www.isa.org/intech-home/2021/december-2021/features/using-control-valve-installed-gain-calculations), [Emerson/Fisher Control Valve Handbook, Chapter 2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf).

`dp_level_remote_seal_structure`의 구성을 Emerson/Rosemount QSG, remote seal manual 및 제품자료에서 교차 확인했다. 공정 격리막과 액체 충전계가 압력을 전달하고, capillary 길이·온도와 설치 높이가 온도 영향·수두·응답시간에 영향을 준다. 원 Anchor의 “비압축성 충전액” 표현은 실제 물성처럼 읽힐 수 있어 “액체 충전액”으로 정정했다. 압축성 무시는 모델링 근사로만 다룬다. 점수 영향은 없다.

근거: [Rosemount DP Level Quick Start Guide](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/dp-level/documents/doc-rosemount-dp-00825-0100-4016.pdf), [Rosemount Model 1159 Remote Diaphragm Seals Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-1159-00809-0100-4504.pdf), [Rosemount DP Level/1199 Seal System Data Sheet](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/dp-level/documents/dl-rmt-00813-0100-4016.pdf).

같은 Pack의 `dp_level_capillary_response_time`은 원래 문구가 충전액 점도·모세관 내경·온도·격리막 면적과 강성 모두를 열거해, 확보된 자료보다 범위가 넓었다. 이를 Rosemount Model 1159 매뉴얼이 직접 뒷받침하는 관계로 제한했다: 해당 설명서는 모세관 길이 증가가 충전액 부피와 온도영향을 증가시키고 response time도 증가시킨다고 기술한다. 이는 해당 제품 자료의 정성 관계이며 모든 remote-seal 설계의 보편 정량모델로 일반화하지 않는다. 점수 영향은 없다. 근거: [Rosemount Model 1159 Remote Diaphragm Seals Manual, §2 Performance](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-1159-00809-0100-4504.pdf).

`dp_level_interface_compensated_taps`의 두 액층 계면 차압식은 두 비혼화·정지 액체, 두 탭 완전 침수, 계면이 두 탭 사이에 있음, 탭 간격 및 밀도 일정의 조건을 먼저 고정한 뒤 `dP/dz=-ρg`를 층별 적분해 확인했다. 상부 탭 위의 공통 기상압과 경액 수두는 차감에서 소거된다. 탭 노출이나 계면 범위 이탈에서는 식을 그대로 적용하지 않도록 Anchor에도 조건을 명시했다. 점수 영향은 없다.

같은 Pack에서 fill-fluid signed head를 equal fill-fluid hydrostatic derivation과 Rosemount 설명서로 확인하고, 온도 영향은 해당 설명서가 구분하는 seal back-pressure와 density/head 효과로 재정의했다. balanced-system은 같은 seal·capillary 길이로 seal-temperature effect를 줄일 수 있지만 head-temperature effect는 남고, tuned system은 비대칭일 수 있음을 명시했다. 탱크 volume은 Rosemount 3051의 표준 geometry 또는 level-volume strapping table 구성으로 한정하고, 수평 원통의 비선형 관계는 원형 segment 면적 적분으로 확인했다. impulse-line Anchor도 제조사 목록의 오류원인 및 설치 권고로 좁혀, 막힘/누설·trapped phase와 freezing으로 인한 pressure isolation을 기록했다. Model 1159 설치 높이 오차 및 재영점 조치는 해당 제품 설명서와 범위에 한정했다. 모두 점수 영향은 없다.

근거: [Rosemount DP Level Remote Seal Systems Reference Manual, §§2.3–2.4](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/dp-level/documents/doc-rosemount-dp-00809-0100-4002.pdf), [Rosemount 3051 Reference Manual](https://www.emerson.com/content/dam/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-3051-pressure-transmitter-76002.pdf), [Rosemount 3051 Plugged Impulse Line Diagnostic](https://videos.emerson.com/detail/video/6318808015112/rosemount%25C2%25AE-3051-pressure-transmitter-plugged-impulse-line-diagnostic), [DP Level outdoor-vessel heat tracing guidance](https://www.emerson.com/en/measurement-instrumentation/industries/chemical/differential-pressure-dp-level-solutions-for-distillation-columns-and-outdoor-vessels), [Rosemount 3051 Manual—volume configuration](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051-00809-0105-4007.pdf), [Rosemount Model 1159 Remote Diaphragm Seals Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-1159-00809-0100-4504.pdf).

이 Pack은 28개 중 28개 Anchor를 verified로 기록했다. LRV/URV 계산은 configured level endpoints의 signed ΔP와 실제 설치에 존재하는 pressure-head만 포함하도록 한정했다. Overpressure 항목은 Rosemount 3051SHP 문서의 MWP·과압 한계, mis-valving 뒤 출력 이동과 re-zero 요구에 한정했다. 기술비교 항목은 Emerson의 DP 밀도보상·비접촉 radar 설명과 Endress+Hauser의 GWR 유전율 경계 반사 원리로 뒷받침하며, 한 방식이 보편적으로 우수하다는 결론은 배제했다. 각 제조사 제품자료의 주장을 타사 전체나 모든 설치에 일반화하지 않는다.

`dp_level_three_pressure_density`와 `dp_level_three_pressure_level`은 균일 정지액의 정수압 관계식을 직접 적분해 확인했다. 두 탭 사이의 같은 액체 기둥은 ΔP=ρgx를 주므로 x와 ΔP가 알려졌을 때 ρ를 계산할 수 있고, 알려진 대표 밀도와 기상압 기준이 있을 때 하부-상부 압력차로 높이를 계산할 수 있다. 밀도·높이를 하나의 차압만으로 동시에 식별할 수 없고, 탭 노출·층분리·기준수두 미보정 시 단순 식을 적용할 수 없다는 조건도 계약에 기록했다. 점수 영향은 없다.

근거: 정수압 미분식 dP/dz = −ρg를 일정 밀도 조건에서 구간 적분한 재현 계산(차원 확인 포함).

`liquid_phase_change_operating_cases`는 Fisher Specification Manager의 Minimum/Normal/Maximum/Others 서비스 조건과 각 조건의 flow·pressure·temperature 입력, 그리고 제조사 자료가 설명하는 특정 기동·정지 운전사례를 대조했다. 원 Anchor의 무조건적 기동·정지 case 열거는 적용범위를 과장할 수 있어, 실제 설계 서비스에 포함되고 sizing/상변화에 영향을 주는 경우로 한정했다. 임의의 모든 변수 조합을 의무화하지 않는다. 점수 영향은 없다.

근거: [Fisher Specification Manager Quick Start Guide](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103533x012.pdf), [Fisher Control Valve Sourcebook—Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [Emerson Severe Service Applications](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves).

`cyber_ai_safety_boundary`를 NIST OT security, HSE cyber/functional-safety guidance, IEC 61508-3 scope summary, NIST SSDF Profile 및 HSE HSG238와 대조했다. OT cyber risk와 SIS/common-dependency 관계, 안전 SW lifecycle/change controls, AI 생성코드도 사용 전 평가 대상이라는 점을 확인했다. AI 코드에 대한 IEC 전용 조항이라고 주장하지 않으며, lifecycle controls 적용은 IEC software scope와 NIST guidance를 연결한 제한적 추론이다. 검증 강도와 독립 평가는 SIL·복잡도·안전계획에 종속된다. 점수 영향은 없다.

근거: [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final), [HSE Cyber Security](https://www.hse.gov.uk/eci/cyber-security.htm), [HSE Control Systems—Independence](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [IEC 61508-3](https://webstore.iec.ch/en/publication/5517), [NIST SP 800-218A](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218A.pdf), [HSE HSG238](https://www.hse.gov.uk/pubns/priced/hsg238.pdf).

`control_valve_positioner_ip_converter_booster_accessories_calibration` 토픽에서는 I/P의 전류-압력 변환과 846의 내부 출력압력 feedback을 밸브 travel feedback과 분리했고, conventional 4–20 mA/3–15 psig 선형 range의 끝점·중간점을 확인했다. Positioner의 valve-stem/shaft feedback과 actuator 압력 조절은 Emerson positioner 자료와 대조했다. Volume booster 기능은 positioner 유량이 actuator demand를 제한하는 경우의 stroke-speed 증가로 한정했다. Fisher VBL/SS-263 문서에 나온 bypass 조정 영향도 반영했다. 전류 및 압력 범위 정규화·선형 mapping 식은 명시한 범위 가정 아래 끝점 대입으로 검산했다. Fisher 3582/3582i/582i 자료로 전공/공압 결합 방식과 공급 공기 요건을 특정 제품 구성에 한정해 확인했다. Filter-regulator Anchor의 `moisture`는 수증기까지 제거하는 듯한 확대 해석을 막도록 액상 응축수 분리·배출로 좁혀 수정했고, 필터 등급 의존성을 명시했다. ASCO 문서로 quick-exhaust와 solenoid switching 기능을 확인하되 실제 port state/fail state는 선택 기기와 circuit에 종속시켰다. Fisher 3582의 Direct/Reverse 입력-출력 압력 관계, zero/travel 재조정 순서, current→converter→positioner→actuator→stem feedback chain, cam/linkage alignment 및 3582/582i의 nozzle–flapper/relay 구성도 설명서 절차에 한정해 확인했다. 이번에 등록한 Fact는 모두 `score_effect=none`이다.

근거: [Fisher 846 Instruction Manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-846-current-to-pressure-transducers-en.pdf), [Fisher 3582/3582i/582i Instruction Manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200138x012.pdf), [Fisher 67C Series Regulator Manual](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/regulators/fisher/others/documents/PRM-IOM-67C-Series-Instrument-Supply-Regulators-Instruction-Manual-VCIMD-11001-EN.pdf), [Emerson Valve Positioners](https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners), [Fisher 3582A](https://www.emerson.com/en/final-control/products/fisher-3582a), [Fisher VBL](https://www.emerson.com/en/final-control/products/fisher-vbl), [Fisher SS-263 bulletin](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103592x012.pdf), [ASCO Quick Exhaust Manual](https://www.emerson.com/documents/automation/installation-manual-european-accessory-quick-exhaust-valves-800-asco-en-5041998.pdf), [ASCO Series 327 safety manual](https://www.emerson.com/documents/automation/european-instruction-manual-series-327-solenoid-valves-safety-applications-en-5180470.pdf).

`lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`의 22개 Anchor 중 11개를 TE Connectivity LVDT 기술 안내서와 Analog Devices 동기검파 설계 자료로 대조해 verified 했다. 확인 범위는 LVDT 권선/가동철심 구조, AC 여자와 유도, 2차 직렬 역접속 및 차동 출력, 이상 영점 상쇄, 규정 선형범위의 출력-변위 관계와 범위 초과 선형성 저하, 영점 통과에 따른 약 180° 위상반전, 동기복조 예시 및 복조 후 출력 필터의 잡음·대역폭·settling 절충이다. 두 제조사 자료는 예시 회로의 설명이지 모든 신호조절기 구조를 규정하지 않으므로 architecture 조건을 Fact에 남겼다. 상호인덕턴스/결합계수의 세부 문구, null residual 발생원인, 영점·온도·정렬·케이블 복합오차, 특정 여자주파수 선정, RVDT의 제품별 각도범위, calibration traceability 및 스트레인 게이지와의 비교는 자료가 Anchor 전체를 직접 뒷받침하지 않아 보류했다. 등록 Fact는 모두 `score_effect=none`이며, 내용은 검증 참고자료일 뿐 점수 산정에는 투입되지 않는다.

후속 확인에서는 제조사·회로 자료가 직접 뒷받침하는 6개 사실을 추가했다: LVDT의 위치 의존 결합(상호인덕턴스를 일반화하지 않고 선형 작동조건으로 제한), 온도에 따른 권선 저항/임피던스 및 위상 영향(기술문서에 서술된 영향으로 한정), RVDT의 회전각 측정과 TE R30A 모델별 각도·비선형성 사양, LVDT와 스트레인 게이지의 변환 원리 차이, conditioner architecture에 따른 DC offset/phase compensation 차이, 케이블·차폐 영향의 conditioner/설치 의존성이다. 마지막 비교는 변환 원리만 구분하고 정확도 우열을 주장하지 않는다. AD598의 null/phase immunity와 장거리 케이블 예외를 같이 기록해 모든 conditioner에 일반화하지 않았다. 이 추가로 해당 Pack의 verified 수는 17/22가 되었고, 남은 5개는 원인·조건의 전체 범위를 직접 뒷받침할 근거가 부족해 보류했다. 모두 `score_effect=none`이다. 근거: [TE temperature effects](https://www.te.com/en/products/sensors/position-sensors/resources/temperature-effect-on-lvdt-sensors.html), [ADI CN-0371](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0371.html), [TE R30A RVDT](https://www.te.com/en/product-CAT-RVDT0002.html), [NI strain-gage measurement](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-strain-with-strain-gages.html), [ADI CN0301](https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/CN0301.html), [ADI AD598 data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ad598.pdf), [TE LVDT installation guidelines](https://www.te.com/content/dam/te-com/documents/sensors/global/te-lvdt-technology-application-note.pdf), [eddylab LVDT installation guidance](https://www.lvdt.eu/).

근거: [TE Connectivity, Understanding LVDTs](https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html), [Analog Devices, Low-Power Synchronous Demodulator Design Considerations](https://www.analog.com/en/resources/analog-dialogue/articles/low-power-synchronous-demodulator.html).

`control_valve_types_globe_rotary_body_actuator_selection`의 29개 Anchor 중 11개를 Emerson Control Valve Handbook 6판 및 제품 기술자료와 대조했다. 확인 범위는 single-port body의 구성, angle valve의 수직 포트와 elbow 적용, cage의 plug guiding/characterization, 3-way valve의 mixing/diverting, sanitary valve의 오염 방지·CIP/SIP, 제품에 한정한 offset butterfly sealing 작동, bellows bonnet의 stem leak barrier와 secondary packing, reduced-capacity trim, spring-diaphragm 및 piston actuator의 작동·fail action, 그리고 수동조작 적용 조건이다. 해당 Fact는 제품 구조와 Handbook에 기술된 기능에 한정했으며 모든 valve/actuator에 일반화하지 않았다. 남은 cage/port/post guidance의 세부 오차, double-port seating 한계, segmented ball·eccentric plug·multiport의 서비스 경계, 연결부·bonnet selection, actuator sizing 및 복합선정 기준은 근거가 문장 전체를 직접 지지하지 않아 보류했다. 모두 `score_effect=none`이다.

근거: [Emerson, Control Valve Handbook, Chapter 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [Emerson, Angle Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/angle-valves), [Emerson, Control Valve Handbook, Chapter 1](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf).

`dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`의 two sequence anchors는 current registry에 미등록이다. [Rosemount 3051 Reference Manual 00809-0100-4001 Rev KB](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051-00809-0100-4001.pdf), §3.11.4, pp. 54–55 supports a model-specific zero-trim sequence only: low-side isolate close → equalize open; after trim, equalize close → low-side isolate open. It does not support the existing Pack's generic `H close → equalize open → L close → bleed open` isolation sequence or its proposed universal return sequence. Because `topic_status.json` records human approval of the existing source hash, this audit does not modify/reapprove the Pack; the two anchors remain unresolved pending human review. This prevents an accurate model-specific procedure from being misrepresented as a plant-wide isolation instruction.

`ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`의 마지막 3개 Anchor를 검토했다. `ultrasonic_repetition_rate_response_averaging`은 pulse-echo 거리식·독립 표본 평균 계산과 Siemens SITRANS 응답률 지침으로 확인했다. 재발사 주기는 최대 echo 왕복시간과 연결되고, N개 독립 표본 평균은 잡음 표준편차를 `1/√N`으로 낮추는 대신 여러 표본 시간에 걸쳐 응답한다. `ultrasonic_calibration_echo_mapping_diagnostics`는 원래의 일반적 echo-map/threshold 필수 주장이 근거 범위를 넘어서므로 이를 제거하고 Rosemount 3100의 수직 설치, 거리·echo size/count·온도 진단값 및 lost-echo troubleshooting으로 범위를 좁혔다. `ultrasonic_application_limits_comparison`은 모델별 range/blanking/response와 공정 acoustic path 및 설치요건을 확인하도록 재작성했고, 3100의 0.3 m blanking zone과 약 1 Hz 반복률은 예시로만 명시했다. 온도·기체·거품·증기·분진·난류·장애물 영향은 제조사 기술자료가 뒷받침하는 조건부 한계로 쓰고, 대체기술은 실제 공정에 따라 비교하도록 했다. 근거: [Siemens SITRANS LT500 Ultrasonic Operating Instructions](https://support.industry.siemens.com/cs/attachments/109828396/A5E52003538en_LT500_ultrasonic_OI_en-US.pdf); [Rosemount 3100 Reference Manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf), §§3.3.1–3.3.2, 5.3.2, 5.4.3, P020; [Emerson/Rosemount Level Measurement Technology Guide](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/marketing/products/level/documents/dl-rmt-00805-0100-1034.pdf), §2.3.3; [VEGA technology comparison](https://www.vega.com/en-ca/company/blog/2019/80-ghz-radar-vs-ultrasonic). Evidence score effect is none.

추가 검증: 제어밸브 소음 Topic에서 난류 공력소음, 캐비테이션 기포붕괴, 초크/고압력비의 충격파-난류 상호작용, 초크의 유한 유량 의미, 유속·밸브/배관 기하와 외부 관측점의 SPL 영향을 독립 확인했다. Valmet 가스·증기 유동 매뉴얼은 저압력비 난류와 고압력비/초크 충격파 상호작용을 구분하고, 초크를 vena contracta의 sonic flow 및 유량 증가 한계로 설명한다. Fisher는 공력소음 예측에 운전 regime, 측정 가능한 밸브 기하와 서비스 조건, pipe-wall transmission loss 및 관측 위치까지 반영한다. 외부 SPL의 거리·방향 및 반사 환경은 Valmet과 ISO 3744:2025의 관측/시험환경 설명으로 한정해 등록했다. 캐비테이션은 액체 유동의 기포 형성·붕괴, 소음·진동·손상으로 한정하고 지속 증기상 flashing과 구분했다. 추가로 process-fluid noise와 configuration-specific pneumatic accessory exhaust를 구분하고, noise field measurement에 위치/거리·weighting·운전/노출 조건과 해당 방법에서 요구하는 correction을 기록해야 한다는 점을 확인했다. 이 두 claim은 무조건적인 accessory exhaust 존재 또는 모든 현장 측정에 correction 적용을 뜻하지 않는다. 신규 6개 Fact는 모두 `score_effect=none`이다. 최신 등록부는 **991개 레코드 / 990개 고유 Anchor**, 기술 검증 잔여는 **1,079개**다. 근거: [Emerson/Fisher Whisper Trim III](https://www.emerson.com/en/final-control/products/fisher-whisper-trim-iii); [Emerson Cavitation in Control Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/cavitation); [Fisher Catalog 12, Section 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s3.pdf), p. 3-5; [Fisher Control Valve Sourcebook, Ch. 5](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), pp. 5-1–5-4; [Valmet Flow Control Manual](https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/), §§4.1, 4.3–4.5; [ISO 3744:2025](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/08/08/80866.html?browse=tc); [ISO 9612:2025](https://www.iso.org/standard/81317.html); [OSHA Technical Manual, Noise](https://www.osha.gov/otm/section-3-health-hazards/chapter-5); [Foxboro VBS200 Quick Guide](https://d38005r3ny6olb.cloudfront.net/images/data_sheets/Schneider/QG_EVE0602_A-EN_VBS200_Series.pdf); [SMC IP8001 Manual](https://static.smc.eu/binaries/content/assets/smc_global/product-documentation/operation-manuals/en/om_ip8001_om00013en-a.pdf); [CDC/NIOSH, Eliminate or Reduce Noise](https://www.cdc.gov/niosh/noise/prevent/eliminate.html).

`control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing`의 `seat_leakage_test`는 Fisher HP/HPA의 optional TSO trim에 한정해 검증했다. D101634X012는 TSO가 ANSI/FCI 또는 IEC leakage class가 아니라고 명시하고, 공장시험에 물을 사용하며 service ΔP를 지정하고 ANSI/FCI Class V test procedure B를 따른다고 설명한다. 이 문서는 다른 trim·제품에 대한 보편 시험절차나 모든 service acceptance criteria를 정하지 않으므로 그 확장은 보류했다. 나머지 19개 앵커는 작업허가 정책, 현장 as-found/as-left 양식, 프로젝트 허용기준 및 모델별 정비절차처럼 사업장·제품별 기준이 섞여 있거나, 이 검토에서 문구 전체를 직접 뒷받침할 근거를 확인하지 못해 verified로 올리지 않았다. Fact는 `score_effect=none`이다. 근거: [Emerson, Fisher HP and HPA Valves Instruction Manual D101634X012, Table 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012-hp-and-hpa-control-valves-fisher.pdf).
`instrumentation_production_management_planning_quality_cost_resources`의 `production_finite_capacity_schedule_dispatch`는 NIST 생산일정 검토, ISA-95 기반 운영관리 모델, Microsoft Dynamics finite-capacity 문서로 범위를 확인해 verified 등록했다. 근거 자료들은 작업/자원 배정에서 장비·작업자·공구·치공구·자재, 가용능력 및 선후관계·설정시간·납기 제약을 고려하는 사례와, 현장 dispatch sequence를 합의된 한계·가용성 안에서 바꾸는 구조를 설명한다. 유한능력 및 자재 availability 상세는 Microsoft 제품 동작에 한정했고, 구체적인 dispatch 우선순위는 사업장 정책으로 남겨 보편 알고리즘을 주장하지 않는다. `score_effect=none`이다. 근거: [NISTIR 5910, Production Scheduling](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821499), [NIST Chapter 63, Monitoring and Controlling Operations](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821207), [Microsoft Learn, Job Scheduling](https://learn.microsoft.com/en-us/dynamics365/supply-chain/production-control/job-scheduling).

같은 Pack의 `production_equipment_resource_availability`는 NISTIR 5910의 resource availability/resource sharing 제약과 NIST의 ISA-95 기반 운영관리 자료의 equipment·tool·labor·material 할당 및 dispatch를 대조해 verified 등록했다. 계획정지는 해당 일정의 설비 가용시간을 줄이는 범위에서만 반영한다. 이는 일정에서 쓸 자원 상태를 고려해야 한다는 사실이지, 보편 정비전략이나 MTBF/MTTR 목표를 정하는 근거는 아니다. 정비 정책은 별도 O&M 범위로 남겼고 `score_effect=none`이다. 근거: [NISTIR 5910, Production Scheduling](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821499), [NIST Chapter 63, Monitoring and Controlling Operations](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821207).

같은 Pack의 `production_quality_plan_ctq_spec`은 기존 문구가 모든 제조현장에 CTQ·표본계획·Control Plan 의무를 일반화할 위험이 있어 Ford IATF 공급자 적용범위로 한정해 수정했다. 2026-06-15 발효 Ford CSR은 해당 Ford 부품에 Control Plan을 요구하고, special-characteristic control을 FMEA/SCCAF/Control Plan에 추적하며, 지정된 검사빈도 변경 승인과 작업지침의 부적합 reaction step을 정한다. 따라서 automotive customer 사례는 verified지만, 보편 CTQ 명칭·표본 방식·서식은 미주장이다. `score_effect=none`이다. 근거: [Ford IATF CSR effective 15 June 2026](https://www.iatfglobaloversight.org/wp/wp-content/uploads/2026/06/Ford-IATF-CSR_Jun-2026-SCCAF_Final.pdf), [IATF CSR index](https://www.iatfglobaloversight.org/oem-requirements/customer-specific-requirements/).

같은 Pack의 `production_process_quality_feedback`은 NIST/SEMATECH control-chart 지침과 2026 Ford CSR로 범위를 재정립해 verified 등록했다. Control Limit은 제품 합격규격이 아니며, 관리이탈/비랜덤 패턴은 원인조사·OCAP를 촉발하지만 그 자체가 제품 부적합의 증명은 아니다. Ford 공급자 범위에서는 규격 밖 읽기의 반응기록, 부적합품 출하 방지, 원인시정·재발방지를 확인했다. Control chart 적용과 현장 격리·복구 절차는 공정·고객 요구에 따라야 하므로 보편 절차로 주장하지 않는다. `score_effect=none`이다. 근거: [NIST/SEMATECH §6.3.1](https://itl.nist.gov/div898/handbook/pmc/section3/pmc31.htm), [NIST/SEMATECH §6.1.4](https://itl.nist.gov/div898/handbook/pmc/section1/pmc14.htm), [Ford IATF CSR effective 15 June 2026](https://www.iatfglobaloversight.org/wp/wp-content/uploads/2026/06/Ford-IATF-CSR_Jun-2026-SCCAF_Final.pdf).
`instrumentation_production_management_planning_quality_cost_resources`의 `production_wip_flow_lead_time`은 WIP 정의와 buffer 목적, Little’s Law 관계를 확인했다. 평균 throughput을 고정한 상태에서 WIP가 커지면 평균 flow/cycle time이 늘어난다는 관계는 일관된 시스템 경계와 장기 평균 조건에 한정한다. 고WIP의 공간·비용·품질 feedback 지연·cycle-time 영향은 MIT Sloan 연구의 한 제조사업부 사례로만 기록했으며 모든 공정에 같은 크기의 효과를 단정하지 않는다. `score_effect=none`이다. 근거: [Lean Enterprise Institute, Inventory](https://www.lean.org/lexicon-terms/inventory/), [MIT OpenCourseWare, Lean Thinking Part II](https://ocw.mit.edu/courses/16-660j-introduction-to-lean-six-sigma-methods-january-iap-2012/f044431285fe865dd395b27f5d3c83ce_MIT16_660JIAP12_1-3part2.pdf), [Repenning & Sterman, MIT Sloan Working Paper 4372-02](https://dspace.mit.edu/bitstream/handle/1721.1/1815/4372-02.pdf).

같은 Pack의 `production_horizon_master_detailed_schedule`은 NISTIR 6058과 NISTIR 5910으로 확인했다. NISTIR 6058은 수요에서 장기 MPS와 capacity requirement를 만들고 production order를 job/batch로 구체화한 뒤, resource-assigned schedule과 machine-specific dispatch list로 나누는 예를 제시한다. NISTIR 5910은 상세 scheduling이 MRP/MPS/capacity planning을 기반으로 자원을 시간에 배정한다고 설명한다. 이 자료들은 계획에서 실행일정으로의 상세화는 뒷받침하지만, 모든 공장의 고정 horizon 길이·rolling 주기·조직계층을 규정하지 않으므로 해당 부분은 보편 규칙으로 주장하지 않는다. `score_effect=none`이다. 근거: [NISTIR 6058, Production Management Standards: Industrial Need](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir6058.pdf), [NISTIR 5910, Requirements and Current Practices for Process Planning and Scheduling in Manufacturing](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821499).


`control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`의 22개 Anchor 모두를 Fisher Catalog 14, Fisher 657 manual, Fisher/Valmet 제조사 자료, Emerson Control Valve Handbook, 1차 실험연구 및 재현 가능한 역학 관계와 대조했다. 기존에 확인한 힘 평형·압력력·시트하중·액추에이터·스프링·bench-set·fail action·마찰 방향과 rotary torque 사실에 더해, 제조사 지침의 동적 유체력 고려와 계측된 2인치 globe valve 실험의 조건부 횡하중을 검증했다. Valmet의 공압 실린더 액추에이터 제어밸브 모델에서는 움직임 시작 직후 마찰계수가 크게 낮아질 수 있어 breakaway와 초기 running friction의 차이를 인정하도록 앵커를 좁혔다. Fisher 지침은 패킹 마찰 결정요인과 패킹의 service pressure/temperature 기반 선택을 구분해 서술하도록 앵커를 좁혔다. 또 Fisher 제품 문서로 balanced trim의 residual thrust·seal/piston-ring friction·제품별 shutoff class와 EDR/ETR balance-hole 정비 요구를 확인하고 해당 제품 범위로 한정했다. 마지막 guide 앵커는 bushing/cage의 문서화된 지지·정렬·유도 기능과 Ferrari의 시험조건 한정 횡하중이 guidance 부품 마모 예측에 관련될 수 있다는 범위로 축소했다. 편심·스템 휨이 마찰을 보편적으로 증가시킨다는 주장은 근거가 없어 제외했다. 어느 결과도 모든 제품·조건의 보편값으로 일반화하지 않았고 모두 `score_effect=none`이다. 근거: [Fisher Catalog 14, Actuator Sizing for Sliding-Stem Valves: Force Method](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf), [Fisher Control Valve Sourcebook, Actuator Sizing and Packing Selection](https://www.emerson.com/is/content/emerson/pt/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [Fisher EDR/ETR Instruction Manual D100391X012](https://documentation.emersonprocess.com/intradoc-cgi/groups/public/documents/instruction_manuals/d100391x012.pdf), [Emerson Control Valve Handbook](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [Ferrari, Measurement of the Fluid Flow Load on a Globe Valve Stem](https://arxiv.org/abs/0909.0874), [Valmet, Friction Model](https://www.valmet.com/flowcontrol/valves/flow-control-manual/mathematical-simulation-of-control-valve-behavior/).
2026-10-11 추가 검증: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`에서 직접 거리식 이외에 photoelectric measurement chain/conversion, through-beam, retroreflective, diffuse-reflective sensing, Direct ToF round trip, iToF phase relation, laser-triangulation geometry와 detector coordinate 등 9개 Anchor를 추가 대조해 verified 등록했다. OMRON/Rockwell의 sensor technical guides와 NIST triangulation research로 범위를 확인했다. 제품별 사거리·오차·교정주기, 모든 대상재질에 대한 검출성능은 일반화하지 않았다. 모두 `score_effect=none`이다. 상세: [optical ToF and photoelectric evidence note](topic_anchor_evidence_followup_20261011_optical_tof.md).

같은 Pack의 `laser_speckle_effect`는 거친 표면에서 coherent laser의 산란파 간섭이 speckle intensity pattern을 만들고, triangulation CCD spot의 centroid 위치 불확실성과 random measurement error를 일으킬 수 있음을 동료심사 연구로 확인했다. speckle와 오차 크기는 표면·광학계 조건에 따라 달라지므로 수치나 보편 반복도 저하로 확대하지 않았다. `score_effect=none`이다. 근거: [Springer, Laser line triangulation for fast 3D measurements on large gears, §4.3](https://link.springer.com/article/10.1007/s00170-018-2636-z), [Optica, Laser triangulation: Fundamental uncertainty in distance measurement](https://opg.optica.org/ao/abstract.cfm?uri=ao-33-7-1306).

`photoelectric_intensity_boundary`는 광원·광학계·입사각·오염·배경 전체의 보편 인과를 단정하던 문구를 좁혔다. OMRON은 diffuse-reflective 방식의 대상 색·매끄러움이 반사광량, 동작 안정성 및 sensing distance에 영향을 줄 수 있다고 명시하고, 별도 distance-setting 방식은 PSD reflected-spot 위치 또는 dual-photodiode의 수광량 차로 판단한다고 구분한다. 이에 따라 두 검출방식의 경계만 verified 등록하고 보편적인 intensity-to-distance 식은 주장하지 않았다. `score_effect=none`이다. 근거: [OMRON Photoelectric Sensors overview](https://www.ia.omron.com/support/guide/43/introduction.html), [OMRON FAQ00320](https://www.ia.omron.com/support/faq/answer/43/faq00320/).

`optical_itof_phase_ambiguity`는 기존의 “다중주파수·코딩·추가 추정” 묶음 주장을 좁혀 검증했다. OMRON iToF 식 `d=cθ/(4πf)`는 단일 주파수 위상에서 유한 거리 주기가 생김을 뒷받침하고, Droeschel et al.은 측정 phase의 modulo 관계와 다중 변조주파수 기반 phase-unwrapping을 설명·실험한다. 이에 따라 coding이나 특정 알고리즘의 효과는 claim에서 제외했고, 실제 비모호 범위/성능은 구현 종속임을 명시했다. `score_effect=none`이다. 근거: [OMRON TECHNICS, §2.1 Eq. (1)](https://www.omron.com/global/en/technology/omrontechnics/vol58/005.html), [Droeschel et al., IEEE IROS 2010](https://doi.org/10.1109/IROS.2010.5649488).

`lvdt_magnetic_saturation_nonlinearity`는 과도한 1차 여자에 따른 코어 포화와 2차 출력 고조파 증가를 NAI 시험 가이드로, 자기재료 포화에 따른 규정 선형범위의 비선형 및 영점 3차 고조파 가능성을 기술자료로 교차 확인했다. 기존의 “부적절한 자기회로” 및 일반적인 “복조오차” 인과는 자료 범위를 넘어 제거했다. 허용 여자 수준은 모델별 정격·사양으로 한정하며, 두 자료 모두 보편 임계값을 정하지 않는다. `score_effect=none`이다. 근거: [NAI, Bench-Testing LVDT/RVDT Performance](https://docs.naii.com/faq/Synchro--and--Resolver/Bench-Testing-an-LVDT-RVDT), [All About Circuits, Introduction to LVDTs](https://www.allaboutcircuits.com/technical-articles/introduction-to-linear-variable-differential-transformer-lvdt/).

정정된 과거 진행 수치: 소음 Topic 등록 Anchor는 26개다. 이후 `fail_open_maximum_flow_case`, `sw06_release_control_authorized_artifact`, `maintenance_strategy_corrective_preventive_condition_predictive`, `maintenance_plan_task_interval_basis`, `calibration_program_traceability`, `maintenance_criticality_risk_prioritization`, `om_asset_register_system_boundary`, `work_order_history_closed_loop`, `maintenance_data_quality_cmms_taxonomy`, `om_continuous_improvement_pdca_lifecycle_cost`, `maintenance_configuration_backup_change_handoff`, `maintenance_roles_competence_permit_restoration`, `inspection_findings_defect_priority_closeout`, `failure_coding_rca_bad_actor_feedback`, `deferred_maintenance_risk_control`, `kpi_mttr_definition_boundary`, `sw06_as_built_consistency`, `sw06_backup_scope_and_consistency`, `sw06_moc_trigger_and_scope`, `sw06_impact_analysis_multidisciplinary`, `sw06_change_implementation_plan`을 각 표준·시나리오의 직접 지원 범위로 제한해 등록했다. OSHA 근거는 미국 연방 규정의 적용범위에 한정하며 보편 작업허가·SIS bypass·기능시험 의무를 주장하지 않는다. OSHA PSM MOC 및 impact review 의무는 covered process와 29 CFR 1910.119(l)의 변경 범위에 한정하고 replacement-in-kind를 제외하며, NIST OT 변경 guidance와 구분한다. NIST/OSHA에 제시된 영향요소 목록은 전 변경의 고정 체크리스트가 아니다. 실행계획 항목도 관련 규정·사업장 절차와 변경별 운전위험에 맞추며, 동일한 보편 체크리스트라고 주장하지 않는다. ISO 14224는 failure-data taxonomy를 뒷받침하지만 사업장별 Bad Actor·RCA 운영방법을 규정하지 않는다. HSE deferral 근거는 offshore SIS 지침에 한정된다. MTTR 수리시간과 MTTRes 전체 복구시간은 ISO 표준 convention에 따라 구분하며, OT 백업은 현재 온라인 형상과 반드시 같은 시점의 사본이라고 가정하지 않는다. 아래 수치는 이 단락이 작성된 2026-10-10 시점의 스냅샷이다: 1,016 records / 1,015 unique Topic-Anchors이며, 2,069개 technical Fact anchor 중 1,054개는 당시 검증 등록되지 않았다. 2026-10-10 생성 감사 JSON과 batch-review 상태 수치는 기술 검증 판정이 아니다. 앞선 항목의 “신규 6개”는 그 시점의 배치 등록 수를 가리킨다.

2026-10-11 추가 검증: `configuration_change_release_backup_rollback_migration_obsolescence_management`의 `sw06_legacy_system_risk_based_management`는 NIST SP 800-82 Rev. 3이 설명하는 OT의 장기 수명, 구형·미지원 운영체제, vendor support 제약, 사전 계획이 필요한 outage, replacement part 수급 및 운전·안전 영향과 NSTAC의 “legacy asset 일괄 제거” 권고에 대한 경계를 근거로 score-neutral verified 등록했다. 이는 연식만으로 결정하지 않고 해당 자산·사업장에 맞는 위험기반 대안을 비교하라는 권고이며, 모든 요소를 모든 설비에 적용해야 한다거나 NIST 지침이 보편 강제규정이라는 뜻은 아니다. 근거: [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final), [NSTAC IT/OT Convergence Report (2022)](https://www.cisa.gov/sites/default/files/publications/NSTAC%20IT-OT%20Convergence%20Report%20%288-23-2022%29.pdf). 상세 범위와 source locator는 Fact registry에 기록했다.

2026-10-11 추가 검증: `configuration_change_release_backup_rollback_migration_obsolescence_management`의 `sw06_vendor_lockin_lifecycle_risk`는 특정 공급자 사용 자체를 금지하지 않고 가치·이동성·전환비용을 함께 평가한다는 원칙으로 score-neutral verified 등록했다. UK GDS의 cloud guidance는 technical lock-in의 편익과 portability·exit 비용의 균형을 직접 명시하나 OT 지침은 아니므로 원칙 범위에만 사용했다. NIST SP 800-82 Rev. 3은 OT에서 proprietary protocol, 단일 vendor support 및 licensing/service 제약, 장기 component life와 부품 수급을 설명해 OT 수명주기 맥락을 보완한다. 이 근거들은 모든 OT에 open interface, source-code access, 대체공급자 또는 특정 contract term을 요구하지 않는다. 근거: [UK GDS, Managing technical lock-in in the cloud](https://www.gov.uk/guidance/managing-technical-lock-in-in-the-cloud), [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final), [UK Government Open Standards Principles](https://www.gov.uk/government/publications/open-standards-principles/open-standards-principles). 상세 범위와 source locator는 Fact registry에 기록했다.

2026-10-11 추가 검증: `configuration_change_release_backup_rollback_migration_obsolescence_management`의 `sw06_migration_discovery_dependency_inventory`는 NIST SP 800-82 Rev. 3의 OT asset/configuration inventory 권고를 기준으로 재작성하고 score-neutral verified 등록했다. 구체적으로 asset 식별정보, vendor·model·location, 설치 software·firmware version, system/data interconnection 기록 및 구성요소 추가·제거·변경 시 inventory 갱신, accurate inventory의 risk·vulnerability·obsolescence tracking 지원을 근거 범위로 삼았다. 이를 migration planning baseline으로 사용하는 것은 지침의 공학적 적용이다. 기존의 custom logic·운전절차·license·spare·기타 숨은 의존성 전체를 NIST의 필수·완전 migration checklist인 것처럼 주장하지 않으며, 이 부분은 현장별 추가 확인으로 명시했다. 근거: [NIST SP 800-82 Rev. 3 publication page](https://csrc.nist.gov/pubs/sp/800/82/r3/final), [official PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf), §§6.1.1, 6.1.1.1–6.1.1.2, 6.1.3, 6.2.4.2, pp. 91–92, 94, 111–112. `score_effect=none`이며 Fact registry가 상세 claim boundary와 locator를 보존한다.

2026-10-11 추가 검증: 같은 SW-06 Pack의 `sw06_compatibility_matrix`는 일반화된 포괄 checklist 문구를 제조사·제품·버전에 한정한 compatibility 확인으로 재작성하고 score-neutral verified 등록했다. Rockwell PCDC는 선택 제품과 시스템 내 제품의 compatibility 비교·의존성 확인을 제공한다. Siemens S7-1200 G2 Migration Checker는 해당 migration 범위에서 hardware/software 구성요소의 target TIA Portal 지원 및 migration 가능성을 점검한다. Emerson Config600 matrix는 Config600과 S600+ binary.app 버전을 짝지으며 firmware upgrade 뒤 full-system test를 권고한다. 이 사례들은 제품별 지원자료를 대상으로 하며, 모든 OT migration에서 OS·application·firmware·driver·protocol·database·license 전체를 단일 matrix에 빠짐없이 넣으라는 보편 요건은 아니다. 근거: [Rockwell Product Compatibility and Migration](https://www.rockwellautomation.com/en-se/support/product/product-compatibility-migration.html), [Siemens S7-1200 G2 Migration Guideline, Entry ID 109986503](https://contentpath.siemens.com/en-s71200g2-migration/migration_guide_s7-1200g2), [Emerson Config600 Compatibility Matrix D301853X012](https://www.emerson.com/is/content/emerson/en/systems-and-software/deltav-scada-systems/product-data-sheets/documents/D301853X012.pdf). `score_effect=none`; 상세 locator와 적용범위는 Fact registry에 기록했다.

2026-10-11 추가 검증: `instrumentation_production_management_planning_quality_cost_resources`의 `production_daily_management_visual_control`은 원래 모든 현장에 다수의 특정 KPI와 shift별 review를 요구하는 식으로 과도하게 일반화되어 있어, 제조 사례 및 일일관리 practice에 한정해 재작성하고 score-neutral verified 등록했다. NIST에 공개된 Honeywell FM&T Baldrige application은 부서별 daily target, 목표 미달의 status/issues board 기록, daily stand-up 검토, 미해결 이슈의 상위 단계 escalation과 해결사항 전달을 기술한다. Lean Enterprise Institute 자료는 정기적인 짧은 meeting에서 visual board와 문제를 review하고, action에 누가 무엇을 언제까지 할지 지정하는 practice를 설명한다. 이 자료는 현장 적용 가능한 운영방식의 근거이지, 모든 사업장에 같은 metric 목록·회의 주기·shift handover를 요구하는 표준은 아니다. 근거: [NIST Honeywell Federal Manufacturing & Technologies Malcolm Baldrige Award Application Summary](https://www.nist.gov/system/files/documents/2017/10/11/Honeywell_Award_Application_Summary.pdf), §4.1.a(1), p. 19; [Lean Enterprise Institute, Making Pivots Operational](https://www.lean.org/the-lean-post/articles/making-pivots-operational/); [Lean Enterprise Institute, Combat Isolation with Productivity by Using PDCA for Effective Meetings, Part 2](https://www.lean.org/the-lean-post/articles/combat-isolation-with-productivity-by-using-pdca-for-effective-meetings-part-two/). `score_effect=none`이다.

2026-10-11 추가 검증: `control_system_operations_maintenance_calibration_inspection_spares_kpi`의 `spares_criticality_classification`은 사용빈도·부품가격 및 복수의 미검증 고려요소를 단정하는 기존 표현에서, 중요 자산 복구 필요성, 고장 결과, redundancy, 조달·수리 lead time에 근거한 자산별 위험판단으로 범위를 정리하고 score-neutral verified 등록했다. DOE OIG의 WAPA 감사는 credible failures 이후 critical asset을 복구할 spare와 reasonable procurement lead time을 설명한다. NASA 시설 RCM 지침은 안전·환경·임무 영향, redundancy, 높은 수리비 및 과도한 조달시간을 criticality 판단의 예로 들며, NASA Chapter 7은 고장 결과 및 수리부품 부족 시 복구 지연을 설명한다. 이 자료들은 자산별로 중요한 요인을 선택할 근거이지, 모든 공장에 공통인 criticality 점수식·범주·가중치를 규정하지 않는다. repairability·substitution·obsolescence는 site-specific 추가요인으로만 남겼다. 근거: [DOE OIG DOE-OIG-24-30](https://www.energy.gov/ig/articles/audit-doe-oig-24-30); [NASA NPR 8831.2D Appendix G](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8831_002D_&page_name=AppdxG), Criticality and Condition / Critical Codes; [NASA NPR 8831.2E Chapter 7](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8831_002E_&page_name=Chapter7), §§7.4.4, 7.4.9, 7.7.2.1–7.7.2.2. `score_effect=none`이다.

### 제어밸브 오염 손상 및 누설 허용량 정규화 근거 (2026-10-11)

`foreign_material_contamination`은 Fisher Control Valve Handbook의 pipeline-cleaning 지침과
HP/HPA manual에 대조했다. pipe scale·metal chip·welding slag 등 이물질은 seat surface를 손상시키거나
plug/ball/disk 폐쇄를 방해해 shutoff가 불완전해질 수 있다. 따라서 오염이 누설을 일으킬 가능성은
verified하되, 특정 입자가 항상 끼거나 반드시 누설을 만든다고는 주장하지 않는다. polymerizing media와
다른 고형물의 세부 거동은 물질·온도·운전별 사례를 추가 확인해야 한다. 근거:
[Emerson/Fisher Control Valve Handbook, §8.2.2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf),
[Fisher HP/HPA Instruction Manual D101634X012, p. 8](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012.pdf).

`size_normalization_basis`는 ANSI/FCI 70-2 및 IEC 60534-4 leakage class table을 대조해 verified했다.
Fisher Handbook의 class 표에서 II–IV는 rated capacity 비율, V는 port diameter와 differential pressure에
정규화된 물 누설량, VI는 port diameter별 허용량으로 정의된다. 적용 standard·edition·class와 구매사양이
지정한 basis를 사용해야 하며, anchor에 나열된 nominal size·seat diameter·capacity를 임의로 골라
적용하지 않는다. 근거: [Fisher Control Valve Handbook, Chapter 5](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf),
[IEC 60534-4:2021, §4.3 and Table 3](https://webstore.iec.ch/en/publication/31136). `score_effect=none`이다.

`volumetric_mass_bubble_basis`는 서로 다른 검사 대상·규격이 서로 다른 보고량을 사용한다는 범위로
verified했다. ISO 15848-1은 external fugitive emission을 지정조건의 concentration 또는 stem-size로
정규화한 mass/volumetric leak rate로 표현하며, IEC/Fisher seat leakage는 해당 class·test medium·절차의
누설량을 사용한다. Class VI bubble/min은 특정 교정 apparatus의 대안일 뿐 universal emission 단위가
아니다. 따라서 경로, 시험법, 단위, test fluid와 필요한 reference condition을 함께 보존한다. 근거:
[ISO 15848-1](https://www.iso.org/standard/61441.html),
[IEC 60534-4:2021](https://webstore.iec.ch/en/publication/31136),
[Fisher Control Valve Handbook, §5.3](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf).

`bubble_count_conversion`은 Emerson/Fisher Class VI 표의 bubble/min 값이 지정된 tube geometry·water
immersion과 calibrated device에만 대응하며 다른 apparatus는 volumetric calibration이 필요하다는 점을
확인해 verified했다. IEC 60534-4의 class별 gas/pressure/test-temperature 범위와 안정된 유량을 정확도에
필요한 시간 관찰하는 절차도 함께 조건화했다. 해당 변환을 packing fugitive emission 등 다른 leakage
path로 확대하지 않는다. 근거: [Fisher Control Valve Handbook, §5.3](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf),
[IEC 60534-4:2021, §§4.3, 5.2, 5.5.3.1](https://webstore.iec.ch/en/publication/31136). `score_effect=none`이다.

`test_pressure_temperature_duration_stabilization`은 IEC 60534-4의 방법별 test fluid·temperature·pressure,
누설유량 안정화 및 정확도에 필요한 관찰조건과 대조해 verified했다. 기록은 결과를 재현·해석하기 위한
현장 권고로 읽으며, 표준이 모든 시험에서 단일 hold duration이나 동일한 thermal stabilization 절차를
요구한다고 해석하지 않는다. 표준은 실제/허용 leak rate와 시험압력의 성적서 기록도 제조사·사용자
합의사항으로 둔다. 근거: [IEC 60534-4:2021, §§4.3, 5.1.3, 5.2, 5.5.3](https://webstore.iec.ch/en/publication/31136),
[Fisher Control Valve Handbook, §§5.2–5.3](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf). `score_effect=none`이다.

`seat_contact_geometry`는 Emerson/Fisher 핸드북의 plug guiding/alignment 설명과 제품별 정비 매뉴얼의
plug-seat 접촉면·lapping 절차를 대조해 verified했다. 이 근거는 정렬과 접촉면 상태가 해당 설계의
seating 및 누설에 중요하다는 점을 지지한다. 접촉 폭·형상은 trim별 제조사 설계·절차에 종속되므로,
모든 ball/disc/seal-ring 형식에 동일한 geometry나 보편 허용 치수가 있다는 뜻으로 확장하지 않는다.
`score_effect=none`이다. 근거: [Fisher Control Valve Handbook, §3.6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf),
[Fisher 24000CVF/SVF Instruction Manual, “Lapping the Valve Seat”](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103360x012.pdf),
[Fisher EW Valve Instruction Manual D100399X012, Fig. 13](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d100399x012.pdf).

`seat_load_contact_stress_relation`은 Fisher의 seat/seat-load 정의, 압력 unbalance force·leak class·port circumference에 따른 actuator sizing 지침과 기본 solid mechanics의 평균응력 정의로 교차 확인했다. 명목 평균응력은 힘/정의된 접촉면적의 관계로 설명할 수 있지만, 실제 접촉면의 국부 응력분포가 균일하다고 가정하지 않는다. 필요한 seat load는 trim 형상과 pressure 방향·차압, seat construction, shutoff 목표 및 service severity에 따라 달라지며, 특정 수치를 모든 밸브에 적용하지 않는다. 근거: [Fisher Control Valve Handbook, Ch. 1, §5.11.1.2](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf), [Fisher Control Valve Sourcebook—Oil and Gas, Ch. 2](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [UIUC Introductory Solid Mechanics: Stress](https://mechref.engr.illinois.edu/sol/stress.html). `score_effect=none`이다.

`insufficient_seat_load_leakage`는 Fisher Sourcebook의 pressure-unbalance force와 leak-class별 seat-load 선정, HPNS Bore Seal 매뉴얼의 충분한 초기 seating force 요구, Fisher 정비 매뉴얼의 손상된 plug-seat 접촉면과 과다 누설 설명을 대조해 verified했다. 매뉴얼 사례는 Bore Seal 설계에 한정하고, 모든 trim에 공통인 최소 하중이나 누설-힘 정량 법칙으로 확대하지 않는다. 근거: [Fisher Control Valve Sourcebook—Oil and Gas, Ch. 2](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), [Fisher HPNS Valve Instruction Manual D103466X012, pp. 24–29](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103466x012.pdf), [Fisher 24000CVF/SVF Instruction Manual, “Lapping the Valve Seat”](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103360x012.pdf). `score_effect=none`이다.

`pressure_direction_sealing`은 Fisher 액추에이터 sizing 자료의 pressure-tends-to-open/close 및 reverse-flow 별도 계산, 제어밸브의 differential-pressure unbalance-force 식, 특정 제품의 pressure-assisted seating 설명과 대조해 verified했다. 따라서 방향별 공정압력 사례를 구분해 평가해야 한다는 범위만 확인했으며, reverse pressure가 항상 누설을 악화시킨다거나 모든 trim이 pressure-assisted라고 주장하지 않는다. 근거: [Fisher Actuator Sizing Manual D103428X012, Catalog 14, pp. B-1–B-2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf), [Fisher Control Valve Handbook, §5.11.1.1](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf), [Fisher Baumann 26000 product documentation](https://www.emerson.com/en/final-control/products/fisher-26000). `score_effect=none`이다.

`single_double_seat_leakage_paths`는 Fisher 핸드북의 double-ported valve force balance 설명과 HS valve 정비 절차의 두 seat ring 동시 접촉 및 각 port 누설 재시험 지침으로 확인했다. 따라서 double-seat에서 두 접촉면의 동시 seating과 shutoff leakage 측정이 필요하다는 구조적 차이를 기록한다. 특정 두 seat 설계가 언제나 동일한 leakage class를 만족하거나 모든 double-seat 구조의 허용 누설이 같다는 뜻은 아니다. 근거: [Fisher Control Valve Handbook, §3.1.1.4](https://stage.www.emerson.com/content/dam/emerson/en/final-control-fctl/isolation-valves/documents/control-valve-handbook-en-3661206.pdf), [Fisher HS Valve Instruction Manual D100381X012, “Lapping Metal Seats”](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d100381x012.pdf). `score_effect=none`이다.

`cavitation_flashing_damage_handoff`는 Emerson의 flashing 설명과 Fisher Control Valve Handbook의 cavitation/flashing 설명으로 확인했다. 두 현상 모두 특정 공정조건에서 trim 표면을 손상시킬 수 있지만 damage severity는 유체·압력회복·속도·재질 등에 의존한다. 이 Topic은 손상 사실과 Topic 8 소유경계를 연결하는 범위만 다루며, 유동 regime나 예방 설계의 상세를 대신하지 않는다. 근거: [Emerson, Control Valve Flashing](https://www.emerson.com/en-ca/automation/valves/controlvalves/control-valve-flashing), [Fisher Control Valve Handbook, §5.14.2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf). `score_effect=none`이다.

`fugitive_emission_source_monitoring`은 EPA Method 21의 VOC leak scope, stem/packing-gland 및 housing interface별 probe 위치, local ambient concentration과 source concentration 비교를 대조해 verified했다. Method 21은 screening으로 누설원을 locate/classify할 뿐 direct mass-emission-rate measurement가 아니므로, 이 근거를 모든 fugitive-emission 측정법에 일반화하지 않는다. 근거: [U.S. EPA Method 21, §§1.2, 2.1, 3.3–3.4, 8.3.1.1, 8.3.2](https://www.epa.gov/sites/default/files/2017-08/documents/method_21.pdf), [EPA Method 21 공식 페이지](https://www.epa.gov/emc/method-21-volatile-organic-compound-leaks). `score_effect=none`이다.

`screening_bagging_quantification_methods`는 EPA Method 21의 source screening과 EPA Equipment Leak Protocol의 bagging/source-enclosure mass-emission method를 비교해 verified했다. screening 수치는 같은 calibration·species·조건의 범위에서 비교 또는 상관에 쓰이며, mass rate는 enclosure와 sample/analysis setup을 별도로 요구한다. 이 내용은 모든 배출원에 bagging이 필요하다는 뜻이 아니다. 근거: [U.S. EPA Method 21, §2.1](https://www.epa.gov/sites/default/files/2017-08/documents/method_21.pdf), [EPA Protocol for Equipment Leak Emission Estimates, §§3–4](https://www.epa.gov/sites/default/files/2020-09/documents/protocol_for_equipment_leak_emission_estimates.pdf). `score_effect=none`이다.

### 이번 검토에서 미검증 유지한 복합 주장

- `gas_liquid_test_medium_difference`: IEC 60534-4가 gas/liquid별 표준 시험 매체와 절차를 구분하는 점은 확인했지만, 앵커가 열거한 compressibility·density·viscosity·surface tension 모두와 “같은 숫자는 직접 비교 불가”의 전체 범위를 한 근거로 입증하지 못했다.
- `excessive_seat_load_damage`: 제조사 자료는 높은 seat load의 stem-load/buckling 위험과 과도한 actuator thrust에 의한 internal damage를 설명하지만, 현재 문구의 seat/plug deformation·indentation·galling·wear 전체를 과도 seat load의 직접 결과로 입증하기에는 부족하다.
- `orientation_thermal_cycle_history`: 아직 미검증이다. IEC 60534-4는 표준 shop leakage test가 설치 후 실제 운전 누설을 예측하지 못한다고 명시하지만, 현재 anchor가 열거한 orientation·thermal state·pressure/stroke cycle·long-term history 각각을 seat 및 packing leakage의 진단 context로 확인하는 직접 근거는 확보하지 못했다. NRC 사례와 isolation-valve thermal-cycle 결과를 일반 control-valve/packing claim의 근거로 확대하지 않는다.
- `specification_test_lifecycle_workflow`: 아직 미검증이다. IEC 60534-4는 routine inspection/test 절차 및 reporting을 규정하지만, anchor의 specification→selection→shop test→installation→commissioning→monitoring→maintenance→as-left verification 전체를 규정된 보편 순서로 요구하지 않는다. 이를 기술 사실로 등록하지 않는다.

### 기존 미검증 판정 정정: `thermal_distortion_hot_leakage`

앞서 이 Anchor를 미검증으로 분류한 문구는 현재 Topic Pack과 registry 상태를 반영하지 못한 오래된 기록이었다. Anchor는 Fisher EH/EHA 제품 공보에 한정되도록 수정되어 있으며 registry의 `fisher_eh_eha_thermal_cycle_seat_ring_distortion_control`이 이를 verified로 등록하고 있다. 공보는 seat-ring이 temperature cycling에 따른 distortion 및 그로 인한 leakage 가능성을 줄이도록 설계되고, hung cage가 seat-ring gasket loading에 영향 없이 열팽창하도록 설계됐다고 직접 설명한다. 이 근거는 해당 제품 설계 범위에 한정되며 모든 밸브의 cold-shop-test 대 hot-service leakage를 보편화하지 않는다. `score_effect=none`. 근거: [Emerson/Fisher Product Bulletin 51.2:EH, D100042X012, p. 6](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d100042x012.pdf), [Emerson/Fisher Steam Conditioning Technologies—Critical Service](https://www.emerson.com/is/content/emerson/en/final-control/fctl/solutions/common-applications/steam-conditioning-valves/documents/D352003X012.pdf).
- `special_service_sealing_boundary`: fire-test 자료 ISO 10497은 soft/metal-seated isolation valve에 관한 것이고, ISA 75.27.01은 sliding-stem control valve의 저온 seat-leakage test다. 현재 복합 문구의 fire-safe·고온·극저온 material/thermal contraction/qualification 경계를 통째로 뒷받침하기에는 적용 범위와 기술 근거가 일치하지 않아 보류한다.

## 2026-10-12 추가: 전자부품 derating 적용범위

`control_hardware_lifecycle_panel_architecture_component_selection_production_verification`의
`chl_derating_rule`은 NASA/GSFC EEE-INST-002의 EEE 부품 정의와 part-category별 요구사항으로
확인했다. Derating은 정상 운전 중 전기·열 스트레스를 낮춰 열화율을 줄이고 기대수명을 늘리는 것으로
정의되며, 기준은 18개 부품 범주 및 project reliability level 별로 제시된다. 이 근거는 NASA 우주비행
EEE 부품 적용의 사례이며 산업 제어기기의 일률 percentage나 NASA 등급의 보편 의무를 뜻하지 않는다.
`score_effect=none`이다. 근거: [NASA/GSFC EEE-INST-002, §§1.0, 3.0, 5.0, 6.0](https://nepp.nasa.gov/docuploads/FFB52B88-36AE-4378-A05B2C084B5EE2CC/EEE-INST-002_add1.pdf).

## 2026-10-11 추가: 위험장소 보호방식

`hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`에서 Ex d의 내부 폭발 containment와 flamepath joint, Ex i의 에너지 제한 원리, Ex 인증과 별개인 현장 환경 적합성, 설치 후 검사·정비 필요성을 각각 확인했다. Ex e는 앵커가 규정된 이상조건까지 일반화하지만 확인한 개요 자료는 정상서비스에서 비발생 아크·스파크를 대상으로 해 보류했다. Ex m/t 결합 앵커와 IS 회로 계산·배선·인증조건 등 세부 주장은 근거 범위가 아직 충분하지 않아 미검증으로 유지한다. 근거: [Emerson Hazardous Area Classifications, D103222X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103222x012.pdf), [IECEx OD 017](https://www.iecex.com/assets/dmsdocuments/3537/IECEx_OD_017_Ed7-v3.0_RLV.pdf), [UNECE Common Regulatory Arrangements, Second Edition](https://www.iecex.com/assets/Uploads/ECE-TRADE-391-Rev.1.pdf), [IECEx Certified Service Facilities Scheme](https://www.iecex.com/certified-service-facility-scheme/). 신규 4개 Fact는 `score_effect=none`이다.

## 2026-10-12 추가: 제어밸브 고유량 수력동력의 screening 한계

`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`의
`high_flow_hydraulic_power`는 압력차와 체적유량의 곱이 장치의 유압동력 변화라는 UF 교육자료와,
실제 flashing/cavitation 손상이 압력회복 위치·국부 속도·압력단계·trim/body geometry와 재료에
좌우된다는 Fisher 자료를 대조해 verified했다. 따라서 Δp·Q는 손상률이나 심각도를 직접 산출하는
공식이 아니라 유동 에너지 규모를 보는 screening 지표로만 해석한다. `score_effect=none`이다.
근거: [University of Florida, Hydraulic Systems, slide 10](https://abe.ufl.edu/faculty/tburks/Presentations/ABE4171/Hydraulic%20Systems.pdf),
[Fisher Control Valve Handbook, §§5.14.1–5.14.2](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf),
[Fisher Cavitrol III Trim](https://www.emerson.com/en/final-control/products/fisher-cavitrol-iii).

### 제어밸브 고유량 local velocity와 유로 면적 (2026-10-12)

`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`의
`high_flow_velocity_area_relation`은 연속방정식과 제어밸브 제조사 기술자료로 verified했다.
정상 1차원 유동에서 체적유량은 단면적과 평균속도의 곱이며, 밀도가 일정할 때만 유로를 따라
체적유량이 일정하다. Valmet은 제어밸브의 실제 유로가 trim/orifice에서 vena contracta까지
변하고, 최소 유로 위치가 압력조건·밸브 형식·크기에 따라 하류 배관까지 이동할 수 있음을
설명한다. 따라서 trim throat, valve outlet 및 연결 배관의 실제 단면·유동상태를 확인해야 한다.
기체·압축성·2상 유동에 액체용 일정 체적유량 관계를 그대로 적용하지 않는다. 연결 reducer도
사이징 저항계수에 반영한다. 특정 유속 한계는 액체 종류·밸브 형식·운전 duty 등 제조사 적용범위에
종속된다. `score_effect=none`이다.

`high_flow_kinetic_energy_density`의 specific kinetic energy 항은 일반 물리식으로 설명 가능하지만,
같은 Anchor의 impingement intensity가 항상 velocity에 따라 증가한다는 일반 주장은 매질·입자·각도·
재료·형상 등 영향 변수를 포함한 직접 근거가 부족해 미검증으로 남겼다. 근거: [NCEES FE Reference
Handbook 10.0.1, Fluid Mechanics, p. 181](https://www.cee.msstate.edu/wp-content/uploads/fe-handbook-10-0-1.pdf),
[Valmet Flow Control Manual, Liquid Flow §§3.1, 3.7](https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/),
[Emerson/Fisher Control Valve Handbook, Ch. 5](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf).

같은 Pack의 `low_reynolds_laminar_correction`은 IEC 60534-2-1의 비난류 유동 보정 개정과
Valmet의 Reynolds number factor 설명으로 verified했다. Valmet은 비난류 조건이 높은 점도,
낮은 유속, 작은 밸브에서 나타날 수 있고 sizing에 Reynolds 보정이 영향을 준다고 명시한다.
IEC는 비압축성 sizing 방정식의 유체 범위 및 비뉴턴·슬러리 등의 제외 범위를 함께 제시한다.
따라서 실제 점도·유량·밸브 조건에 맞는 표준 또는 제조사 sizing 절차를 적용하고, 난류식만을
무조건 적용하지 않는다는 범위로 확인했다. `score_effect=none`이다. 근거: [IEC 60534-2-1:2011](https://webstore.iec.ch/en/publication/2461),
[Valmet Flow Control Manual, Liquid Flow §3.3.1](https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/).

`low_flow_minimum_controllable_flow`은 inherent rangeability의 최소 controllable Cv와
installed rangeability의 최소 controllable process flow를 구분하는 Valmet 자료, actual process
pressure 및 piping과 valve characteristic이 installed performance를 정한다는 Valmet manual,
그리고 Fisher의 rangeability 정의를 대조해 verified했다. 실제 minimum controllable flow는 밸브의
명목 Cv 한 값만으로 확정하지 않고 process operating range, installed gain/characteristic, 허용
controllability tolerance와 작은 입력 변화에 대한 valve response를 함께 평가한다. 공급사별 정의와
valve type이 다르므로 특정 보편 수치나 안정도 threshold를 지정하지 않는다. `score_effect=none`이다.
근거: [Valmet, Rangeability](https://www.valmet.com/insights/articles/flow-control/flow-control-expert3/),
[Valmet, Control Valve Installed Performance](https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/),
[Emerson/Fisher Control Valve Handbook, §1.5](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf).

`cryogenic_thermal_contraction`은 냉각 중 구성품별 열전달·질량·위치와 재료 열팽창계수 차이가
mating dimensions, alignment와 sealing contact/load에 영향을 줄 수 있음을 NASA SP-8097 및
NASA cryogenic control valve 사례로 확인했다. 방향과 크기는 설계마다 다르다. NASA 자료는 로켓
밸브 설계 맥락의 예이며 일반 산업 밸브에 동일한 누설 방향·간극 변화가 발생한다는 의미가 아니다.
저온에서의 실제 clearance, seat load와 packing 조건은 재료·형상·온도구배에 맞춰 평가하고 필요한
저온 시험으로 확인해야 한다. `score_effect=none`이다. 근거: [NASA SP-8097, Liquid Rocket Valve Assemblies](https://ntrs.nasa.gov/citations/19740018866),
[NASA Cryogenic Control Valve Tech Brief](https://ntrs.nasa.gov/citations/20040001048),
[Emerson/Fisher Control Valve Handbook, Ch. 6](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf).

`trapped_liquid_cavity_pressure`는 차단된 밸브 공동부의 액체가 가열될 때 내부압력이 상승할 수 있고,
밸브 형식에 맞는 cavity relief 또는 별도 relief 경로를 검토해야 한다는 Valmet/Jamesbury 자료와
LBNL cryogenic safety guidance로 verified했다. 증기화 여부와 압력 상승량은 유체의 포화상태,
압력·온도 변화, 공동부 체적 및 유연성에 따라 달라진다. Valmet 자료가 인용한 ANSI B16.34의
압력 한계 책임도 확인했으나, 모든 밸브에 같은 relief 방향·seat 구조를 요구한다고 일반화하지 않는다.
`score_effect=none`이다. 근거: [Valmet/Jamesbury B100-0EN, Cavity Relief](https://www.valmet.com/globalassets/sharepoint/imported/b100-0en.pdf),
[Jamesbury Series 6FRF IMO-R24EN](https://new.valmet.com/globalassets/sharepoint/imported/imo-r24en.pdf),
[LBNL EHS Manual, Safe Handling of Cryogenic Liquids](https://ehs.lbl.gov/resource/esh-manual-pub-3000/ch29/).

`cryogenic_vaporization_two_phase`는 압력강하로 valve downstream pressure가 액체 증기압보다 낮아지면
일부가 기화되어 2상 유동이 될 수 있다는 Valmet 정의와, 열 유입으로 cryogenic liquid가 비등하고
폐쇄용기 압력이 상승한다는 LBNL 안전지침으로 verified했다. 이 현상은 모든 운전점에서 발생한다는
주장이 아니며 실제 상분율·flash 양과 sizing 정확도는 유체물성·압력·온도·열유입에 좌우된다.
따라서 sizing 시 실제 상상태와 해당 계산법의 적용범위를 확인해야 한다. `score_effect=none`이다.
근거: [Valmet Flow Control Manual, Liquid Flow §3.3.3](https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/),
[LBNL, Pressurization and Explosion Hazards](https://ehs.lbl.gov/service/cryogenic-liquid-safety/pressurization-and-explosion-hazards/),
[IEC 60534-2-1:2011](https://webstore.iec.ch/en/publication/2461).

2026-10-12 추가 검증: `low_temperature_toughness_brittle_fracture`는 ASME B31.3의 cryogenic piping 적용범위, ASME BPVC 공식 교육자료의 MDMT별 toughness/impact-test 적합성 및 예외, MSS SP-134의 cryogenic valve 재료·설계·저온 시험 범위를 대조해 verified했다. MDMT와 impact-test 요구는 부품·재료·두께·적용 코드 및 예외 조건에 종속되므로, 모든 control valve에 공통인 등급이나 시험 의무로 확대하지 않는다. 실제 구성품의 최저 금속온도와 구매 사양을 기준으로 적용 코드를 확인해야 한다. `score_effect=none`이다. 근거: [ASME B31.3-2024 catalog](https://golive.asme.org/), [ASME BPVC MDMT/toughness course catalog](https://www.asme.org/wwwasmeorg/media/ResourceFiles/Shop/Courses/ASMETrainingDevelopment/ASME_Training_and_Development-Spring-Catalog.pdf), [MSS SP-134 preview](https://store.accuristech.com/mss/products/preview/1832278).
