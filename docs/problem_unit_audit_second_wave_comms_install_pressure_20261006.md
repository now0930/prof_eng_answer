# 2차 Topic Pack 감사 — 통신·설치/접지·압력 계측

점검일: 2026-10-06
기준: `docs/topic_pack_workflow.md` §4
범위: 2차 후보 중 communications 2개, installation/grounding 2개, pressure measurement 1개
상태: **Problem Unit/coverage 감사 — 기술 사실·채점 source는 수정하지 않음**

## 판정 원칙

아래 질문은 현재 Knowledge Pack의 지식으로 작성된 출제 가능성 후보이며, 확인한 기출로
표현하지 않는다. 기존 README와 expected patterns, required-anchor 연결, 명시된 owner
boundary를 비교했다. 기계 audit는 의미 판단 보조이며, connected-component 경고만으로
팩을 자동 분할하지 않는다.

## 1. 산업망 실시간 성능과 통신방식/상호운용성

### A. 실시간성·동기·장애복구

Pack: `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`
현황: 40 Anchor, 10 expected patterns; atomicity audit 6개 disconnected family(1/5/1/1/1/1),
대형 Anchor 경고.

**중심 예상문제 후보**

> 산업 제어망의 실시간 성능 요구(Latency/Jitter/Cycle time/Response time)를 정의하고,
> worst-case 결정성·시간동기·장애복구 목표를 설계 및 시험으로 검증하는 방법을 설명하시오.

| 요구 축 | 연결 지식 / Anchor family | 현재 패턴 | 판정 |
|---|---|---|---|
| 성능 요구 정의·정량화 | Latency, jitter, cycle, response, determinism 및 load/headroom | #1–3 | 개념/성능설계 unit의 같은 답안 backbone으로 연결 가능 |
| TSN scheduling/toolbox | TSN, Qbv, preemption, policing | #4 | 실시간성 설계의 수단으로 종합문제에 연결 가능. 독립 TSN 적용 문제도 가능 |
| Clock synchronization | PTP 목적·clock architecture·timestamp accuracy와 “sync ≠ determinism” 경계 | #5 | 시간동기 문제로 독립성이 높음. 성능문제에 부가 요구로만 합치지 않는 편이 명료 |
| Network redundancy/recovery | MRP/DLR/PRP/HSR, failover state, health, recovery time | #6–7 | 토폴로지 비교와 end-to-end recovery 설계는 연결되나 요구동사가 달라 하위 문제 후보 |
| Degradation/fault handling | packet loss/storm/multicast/congestion, fallback, graceful degradation | #8–9 | 성능/장애 진단의 독립 unit 후보. local control 행동은 process control owner와 interface 확인 필요 |
| 검증 | fault injection, measurement, acceptance | #10 및 #2 | 앞선 요구의 verification 축으로 연결 가능 |

**경계 확인:** README가 SW-07에 protocol/매체/interoperability, SW-08에 정량적 성능·PTP
성능·복구시간, SW-09에 cyber security를 구분한다. 이 경계는 적절해 보인다. 다만 A의
40 Anchor 중 PTP, TSN, topology recovery, packet fault, fallback까지 모두 하나의 “정량
성능” 문제에 억지로 넣지는 않는다. 최소 3개 problem family(실시간 성능·TSN, time sync,
resilience/recovery)로 추적할 것을 제안한다.

### B. 유·무선 통신, Fieldbus/Ethernet 및 상호운용성

Pack: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
현황: 40 Anchor, 10 patterns; atomicity audit 6개 disconnected family(2/1/1/3/2/1),
대형 Anchor 경고.

**중심 예상문제 후보**

> 계측제어 통신방식의 요구를 정리하고, 물리매체·프로토콜·장치 profile 및 정보모델의
> 상호운용성과 현장 lifecycle을 고려한 선정·commissioning 방안을 설명하시오.

| 요구 축 | 연결 지식 / Anchor family | 현재 패턴 | 판정 |
|---|---|---|---|
| 요구정의·방식선정 | 통신 요구, layered view, multicriteria, lifecycle | #1 | 전체 비교 문제의 backbone |
| 물리매체·serial | Copper/fiber/serial/RS-485/termination | #2 | 매체/배선 원리 문제. 설치·접지 상세는 installation/grounding owner와 handoff |
| Fieldbus·산업 Ethernet | HART/FF/PA, Modbus, EtherNet/IP/PROFINET/EtherCAT | #3–5 | 서로 독립 protocol 비교군; 하나의 주제는 “protocol 종류 나열” 대신 선정 조건으로 한정 |
| OPC UA·information model | OPC UA 역할 및 protocol conversion | #6 | 상위 정보통합과 fieldbus 역할 비교; Industrial IoT integration 경계 확인 |
| Wireless | WirelessHART/ISA100/site survey/power lifecycle | #7 | 별도 무선 적용 problem unit 후보 |
| Device interoperability | profile/description/conformance | #8 | protocol 비교와 연결되지만 별도 구성·검증 문제 가능 |
| Commissioning·brownfield | workflow, naming/addressing, maintenance, installed-base transition | #9–10 | 동일 migration/lifecycle problem family로 묶을 수 있음 |

**A와의 경계:** SW-07은 무엇을 연결하고 어떤 protocol/매체/profile을 쓸지, SW-08은
정량 실시간성·시간동기·복구 성능이 목표를 만족하는지를 소유한다. 예를 들어 PRP/HSR
명칭·기능은 SW-07 설명에 제한적으로 나타날 수 있으나 recovery time의 정량 산정/검증은
SW-08로 넘긴다. README의 분리는 실용적이며 유지 권고한다.

## 2. Field installation과 전원·접지·EMC

### C. 계측설비 설치·배선·도압배관·검사

Pack: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
현황: 33 Anchor, 10 patterns; 3 disconnected family(4/3/3).

**중심 예상문제 후보**

> 승인된 설계기준과 도면에 따라 계측기를 설치하고, 케이블·도압배관 시공을 검사한 뒤
> punch와 as-built 증적으로 인수하는 절차 및 품질관리 방안을 설명하시오.

- **작업/검사 lifecycle:** #1 + #7 + #10. 설치 → 검사/punch → FAT 이후 현장 확인 → as-built
  의 공통 backbone을 구성한다.
- **Cable workmanship:** #2 + #3. tray/gland/terminal 및 power/VFD 분리의 구현과 검사.
- **Impulse piping:** #4 + #5 + #6. tubing 배치/경사/지지 및 gas/liquid/steam service와
  high/low 대칭. 측정 원리와 밀도 보정은 DP level owner, 개별 manifold/pulsation test는
  `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`에 연결한다.
- **기준·위험장소:** #8 + #9. 승인 code/spec/drawing 우선순위, Ex/IS 상세 선정 owner와
  실제 field installation condition을 분리한다.

이 Pack은 broad field-installation umbrella로 기능할 수 있으나 10개 pattern 모두를 한
문항으로 강제하면 과도하다. 대표문제는 lifecycle/inspection에 두고 cable, impulse,
standard-conflict는 하위 독립 문제군으로 유지하는 것이 적절하다. Safety critical한 PE,
shield, IS의 결정 원칙을 installer가 임의로 변경하지 않는 경계가 중요하다.

### D. 계장 전원·접지·차폐·UPS·Ground Loop·EMC

Pack: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
현황: 29 Anchor, 10 patterns; 3 disconnected family(7/2/1).

**중심 예상문제 후보**

> 계측 신호 이상에서 전원품질·접지/본딩·차폐 및 EMC coupling을 증거 기반으로 진단하고,
> 안전한 대책과 정상/과도상태 재검증 절차를 설명하시오.

| 예상문제군 | 패턴 | 판정 |
|---|---:|---|
| 현장 잡음/ground loop 진단 | #1, #3, #5, #9, #10 | 하나의 source-path-victim 진단·개선·검증 backbone을 공유. 단, surge/SPD는 transient protection 조건을 명시 |
| PE/reference/bonding/shield 설계 | #2, #4 | 별도 원리/설계 문제. “PE 해제 금지”, shield의 주전류 귀로 금지, 주파수별 termination을 정확히 유지 |
| 전원품질·UPS·이중화 | #6, #7, #8 | 전원 reliability/ride-through 문제군. UPS sizing은 load/time/aging/bypass 근거 없이는 숫자로 가정하지 않음 |

**C와의 경계:** D는 설계철학과 고장진단(grounding topology, coupling, UPS/EMC 대책), C는
승인된 철학을 케이블·gland·terminal에 구현·검사한다. Shield termination의 설계 선택은 D,
termination drawing 준수 여부와 physical workmanship는 C다. Environmental qualification
시험의 severity/evidence는 별도 environment qualification Topic으로 넘긴다.

## 3. 압력계 원리·선정·오차

Pack: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
현황: 22 Anchor, 10 patterns; 3 disconnected family(1/8/1).

**중심 예상문제 후보**

> 압력 reference와 공정조건을 정리하고 Bourdon·diaphragm·piezoresistive·DP 측정원리를
> 비교하여 계기를 선정한 뒤, 주요 오차·보호 및 교정방법을 설명하시오.

| 요구 축 | 패턴 | 연결성·문제경계 |
|---|---:|---|
| 압력 reference와 용어 | #1 | 공통 서론: absolute/gauge/differential을 구분 |
| 센서 원리·비교·선정 | #2–5 | Bourdon/diaphragm/piezoresistive가 연결. #5가 비교의 통합 pattern이고 #2–4는 각 원리의 별도 변형 |
| DP transmitter의 static pressure | #6 | 별도 DP 적용 문제. level hydrostatic/wet-dry/remote seal은 DP-level Pack 소유 |
| 범위·공정·환경 선정 | #7 | #5의 선정축과 겹치므로 일관된 요구-Anchor 정합이 필요 |
| 정확도/교정/동특성 오차 | #8 | 여러 metrology/응답 개념 포함. calibration general Topic과 boundary 확인 |
| Impulse line | #9 | 물리적 배관 installation은 C가 소유. 본 Pack은 압력 전달 오차 영향까지만 다루는 것이 적절 |
| Smart transmitter retrofit | #10 | technology/lifecycle 적용문제; 새 smart/asset-management Topic과 중복 여부 확인 |

README는 DP-level, strain/load-cell, piezoelectric, passive transducer, hazardous-area,
metrology owner로 handoff를 선언한다. 본 Pack은 “압력 sensing element 원리·비교·선정”을
중심으로 좁혀야 하며 10개 질문을 한 문제의 동등한 필수 범위로 취급하지 않는다. 현재
22 Anchor의 #6–10은 application, error, installation, retrofit을 추가해 scope가 커진다.

## 4. Pack별 기계 screen

`audit_topic_pack_atomicity.py` 선택 실행 결과 (85-pack inventory, 선택 5개):

- decision PASS; errors 0; warnings 7.
- 경고는 위 5개 모두에 걸친 disconnected family 5건과 network pack 2개의 40-anchor 경고.
- 경고는 source validity/technical correctness를 판정하지 않는다.

## 5. 다음 구조 작업 후보

이번 배치의 다음 후보는 `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`,
`physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`,
`piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`,
`speed_rotation_measurement_encoder_proximity_tachometer_selection_error`,
`strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`와
`safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`다. 이후 대형
Control Valve 묶음과 나머지 자동경고 대상, coverage 최하위 pack을 순서대로 본다.

## 6. 제한사항과 안전조치

- Topic Pack JSON, aliases, router, grading/training/feedback projection 및 generated bank 변경 없음.
- 공식 출제기준/기출 문항 매핑을 검증하지 않았으며, 제안 문제는 모두 예상 문제다.
- 출처 원문을 다시 읽어 기술 정확성을 평가한 것은 아니다. 특히 standard edition, performance
  limit, UPS sizing, pressure sensor error는 source·operating condition 없이 고정값으로
  만들지 않는다.
- 실제 분할/수정 전에는 각 후보의 schema, anchor references, existing tests, alias collision,
  router hit 및 consumers를 조사하고 관리 workflow 및 release gate를 통과해야 한다.
- 기존 채점 계약, deterministic primary authority, canonical question taxonomy, fatal handling,
  golden/release gate를 변경하지 않는다.
