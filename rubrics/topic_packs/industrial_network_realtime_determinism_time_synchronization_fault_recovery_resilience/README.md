# SW-08 Topic Pack — 산업 네트워크 실시간성, 결정성, 시간동기화, 장애복구 및 복원력

## Metadata

- `topic_id`: `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`
- `LANE`: `SOFTWARE_LLM_LANE_B`
- `question_type`: `CALC_DESIGN`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `HIGH`
- Fact Anchor: 40
- Fatal 오류: 20
- Warn/Major: 12
- Focused regressions: 37

## Ownership 경계

SW-08은 산업 네트워크의 **정량적 실시간 성능, 시간동기, 장애복구와 복원력**을 담당한다.

- **SW-07**: Protocol 종류, 물리매체, 일반 통신구조, Device Profile과 상호운용성 선정
- **SW-08**: Latency, Jitter, Cycle time, Response time, Determinism, TSN, PTP, Redundancy, Recovery와 Resilience
- **SW-09**: Authentication, Encryption, Access control, Firewall와 Cyber incident response

Protocol 이름 나열은 SW-08의 중심답안이 아니다. Security control의 상세 역시 SW-09로 넘긴다.

## 대표 문제

- 산업 네트워크의 Latency, Jitter, Cycle time, Response time와 Determinism을 정의하고 상호관계를 설명하시오.
- 실시간 산업 Ethernet의 worst-case 성능설계 절차와 검증방법을 설명하시오.
- Network load, Priority, QoS와 Scheduling이 실시간 성능에 미치는 영향을 설명하시오.
- TSN의 주요 기능과 산업제어망 적용 시 설계조건을 설명하시오.
- IEEE 1588 PTP의 clock 구성, 오차요인과 현장 검증방법을 설명하시오.
- MRP, DLR, PRP와 HSR의 구조, 장애복구방식과 적용기준을 비교하시오.
- 산업 네트워크의 장애검출, Failover와 Recovery time 산정방법을 설명하시오.
- Packet loss, Broadcast storm, Multicast flooding과 Congestion의 원인 및 대책을 설명하시오.
- 통신장애 시 Fallback local control과 Graceful degradation 설계방안을 설명하시오.
- 산업 네트워크 복원력 검증을 위한 fault injection 및 acceptance test 절차를 설명하시오.

## 핵심 Fact

- **sw08_performance_requirements** — 산업 네트워크 설계는 허용 Latency, Jitter, Cycle time, Response time, Packet loss, 동기정확도, 장애복구시간과 가용성 목표를 정량적으로 먼저 정의해야 한다.
- **sw08_latency_definition** — Latency는 데이터가 송신 지점에서 수신 지점까지 전달되는 지연이며 serialization, switching, queueing, propagation과 protocol processing 지연의 합으로 평가해야 한다.
- **sw08_jitter_definition** — Jitter는 반복 전송 또는 도착시각 간 지연의 변동이며 평균 Latency와 구분하여 최대값, 범위 또는 통계분포로 관리해야 한다.
- **sw08_cycle_time_definition** — Cycle time은 제어 또는 통신 작업이 반복되는 주기이며 패킷 1개의 전송시간과 동일하지 않고 생산자·네트워크·소비자의 주기와 위상관계를 포함한다.
- **sw08_response_time_definition** — Response time은 입력 변화 또는 사건 발생부터 필요한 출력 또는 조치가 완료될 때까지의 end-to-end 시간으로 센싱, 연산, 통신, 출력 갱신과 장치동작을 포함한다.
- **sw08_throughput_distinction** — Throughput은 단위시간당 전달 가능한 데이터량이며 낮은 Latency나 Determinism을 자동 보장하지 않으므로 대역폭과 시간성능을 분리해 평가해야 한다.
- **sw08_determinism_definition** — Determinism은 주어진 부하와 고장조건에서 통신 완료시간이 예측 가능한 상한 내에 있음을 뜻하며 단순히 평균속도가 빠르다는 의미가 아니다.
- **sw08_worst_case_analysis** — 실시간 설계는 평균값보다 worst-case traffic, 최대 frame, queue interference, topology depth, clock error와 failure transient를 포함한 상한 분석을 우선해야 한다.
- **sw08_network_load_headroom** — Network load는 정상·시작·진단·알람·복구 시 traffic을 합산하고 burst와 성장여유를 포함해 설계하며 평균 utilization만으로 충분성을 판단하지 않는다.
- **sw08_priority_qos** — Priority와 QoS는 중요 traffic의 queueing 우선순위를 조정하지만 admission control, policing, queue 설계와 부하제한 없이 모든 deadline을 보장하지 않는다.
- **sw08_scheduling** — Cyclic scheduling과 traffic shaping은 frame 송신창, queue, producer phase와 경로를 조정하여 간섭을 제한하며 schedule의 end-to-end 일관성과 변경관리가 필요하다.
- **sw08_tsn_toolbox** — TSN은 단일 protocol이 아니라 시간동기, scheduling, shaping, policing, redundancy와 자원예약 기능을 조합하는 IEEE 802.1 기술군이며 적용 profile과 end-to-end 구성이 필요하다.
- **sw08_tsn_qbv** — IEEE 802.1Qbv Time-Aware Shaper는 공통 시간기준에 따라 queue gate를 개폐해 scheduled traffic의 송신창을 만들며 guard band, schedule cycle과 clock accuracy를 함께 설계해야 한다.
- **sw08_tsn_preemption** — Frame preemption은 긴 저우선 frame이 고우선 frame을 지연시키는 blocking time을 줄이지만 양단 지원, fragment overhead와 검증이 필요하다.
- **sw08_tsn_policing** — Per-stream filtering and policing은 stream별 rate·burst·gate 위반을 제한하여 faulty talker의 영향을 격리하지만 정책 오설정에 따른 정상 traffic 차단을 시험해야 한다.
- **sw08_ptp_purpose** — PTP는 분산 clock의 시간 또는 위상을 맞추는 protocol이며 측정, sequence of events와 scheduled communication을 지원하지만 자체만으로 control deadline을 보장하지 않는다.
- **sw08_ptp_clock_architecture** — PTP 설계는 Grandmaster, ordinary clock, boundary clock, transparent clock과 network path를 정의하고 Best Master Clock 선정과 holdover 동작을 검토해야 한다.
- **sw08_timestamping_accuracy** — 시간동기 정확도는 hardware timestamping, residence time 보정, link asymmetry, oscillator 성능, profile과 network topology의 영향을 받으므로 end-to-end 측정으로 검증해야 한다.
- **sw08_sync_not_determinism** — Clock synchronization은 schedule과 event ordering의 공통 기준을 제공하지만 queue, load, forwarding과 application scheduling을 제어하지 않으면 Determinism이 성립하지 않는다.
- **sw08_redundancy_objectives** — Redundancy 설계는 보호할 고장, 허용 packet loss, 허용 recovery time, topology, common-cause failure와 유지보수 방식을 먼저 정의한 뒤 protocol을 선정해야 한다.
- **sw08_recovery_time_components** — 장애복구시간은 고장검출, 상태판단, topology 재구성, route 또는 port 전환, address relearning, application timeout과 control state recovery의 합으로 보아야 한다.
- **sw08_ring_recovery_general** — Ring redundancy는 link 또는 node 고장 시 대체경로를 제공하지만 recovery time은 protocol, ring size, supervision interval, switch implementation과 fault type에 따라 달라진다.
- **sw08_mrp** — MRP는 일반적으로 ring manager와 ring client가 상태를 감시하고 고장 시 blocked path를 전환하는 방식이며 구성 profile과 ring 조건에 따른 복구시간을 검증해야 한다.
- **sw08_dlr** — DLR은 EtherNet/IP 계열 device-level ring에서 supervisor와 ring node가 beacon 또는 announce를 이용해 고장을 감지·복구하며 모든 Ethernet protocol의 범용 ring 표준으로 보아서는 안 된다.
- **sw08_prp** — PRP는 동일 frame을 독립된 두 LAN으로 동시에 보내고 수신 노드가 중복을 제거하여 단일 LAN 고장 시 재수렴 없이 통신을 지속하도록 설계한다.
- **sw08_hsr** — HSR은 ring 양방향으로 frame을 중복 전송하고 node가 frame을 전달·중복제거하여 단일 고장에 대한 seamless communication을 목표로 하며 node forwarding과 traffic overhead를 고려해야 한다.
- **sw08_seamless_independence** — PRP와 HSR의 seamless 특성은 정의된 단일고장과 적합한 node·path 구성에서 성립하며 공통 전원, shared switch, configuration error와 다중고장은 별도 보호가 필요하다.
- **sw08_packet_loss** — Packet loss는 bit error, buffer overflow, link flap, policing, topology change와 receiver overload에서 발생할 수 있으며 loss budget, sequence monitoring과 application의 stale-data 처리를 정의해야 한다.
- **sw08_broadcast_storm** — Broadcast storm은 loop, malfunction 또는 과도한 discovery로 대역폭과 CPU를 소진할 수 있으므로 loop prevention, storm control, segmentation과 fault containment가 필요하다.
- **sw08_multicast_management** — Multicast traffic은 one-to-many 전달에 효율적이지만 group membership, snooping·querier, flooding 범위와 receiver capacity를 관리하지 않으면 불필요한 부하가 확산될 수 있다.
- **sw08_congestion_buffering** — Congestion은 ingress traffic이 link 또는 queue service capacity를 초과할 때 지연·drop을 발생시키며 buffer 증설만으로 deadline을 보장할 수 없고 traffic engineering이 필요하다.
- **sw08_failover_state_consistency** — Network failover 후에도 controller, remote I/O, sequence, redundancy manager와 application session의 상태가 일관되어야 하며 duplicate, out-of-order, stale command를 검증해야 한다.
- **sw08_fallback_local_control** — Network 상실 시 critical equipment는 정의된 local control, hold-last, safe state 또는 제한운전으로 전환하도록 설계하고 전환조건과 복귀절차를 검증해야 한다.
- **sw08_graceful_degradation** — Graceful degradation은 일부 통신·진단·최적화 기능을 제한하면서 핵심 제어와 안전기능을 유지하는 전략이며 기능우선순위와 operator indication을 사전에 정의해야 한다.
- **sw08_redundancy_health_monitoring** — Redundancy는 standby path와 duplicate channel의 건강상태를 지속 감시하고 latent failure를 알람·시험해야 실제 가용성을 유지할 수 있다.
- **sw08_failure_domain_independence** — 복원력은 link뿐 아니라 switch, power, cabinet, cable route, clock source, controller interface와 configuration의 failure domain을 분리하고 common-cause failure를 줄여야 한다.
- **sw08_fault_injection_testing** — 복구성능은 cable open, switch power loss, node failure, clock loss, traffic burst, loop와 packet impairment를 계획적으로 주입하여 검출·전환·공정영향·복귀를 측정해야 한다.
- **sw08_measurement_acceptance** — 검증은 synchronized capture, device diagnostics와 application timestamp를 이용해 최대·분위수 Latency, Jitter, loss, clock offset, recovery time과 deadline miss를 기록하고 요구값과 비교해야 한다.
- **sw08_sw07_boundary** — Protocol 종류, 물리매체, 일반 통신구조, Device Profile과 상호운용성 선정은 SW-07의 범위이고 SW-08은 정량적 시간성능·동기·복구·복원력을 담당한다.
- **sw08_sw09_boundary** — Authentication, encryption, access control, firewall와 cyber incident response는 SW-09의 범위이며 SW-08은 장애·혼잡·고장전환에 대한 성능과 복원력에 집중한다.

## 핵심 Fatal 오류

- **sw08_fatal_throughput_is_determinism**: Throughput이 높으면 Latency와 Jitter의 상한도 자동 보장되어 Determinism이 성립한다.
  - 교정: Throughput과 Determinism을 분리하고 worst-case delay와 deadline을 검증해야 한다.
- **sw08_fatal_average_only**: 평균 Latency만 낮으면 worst-case와 deadline miss는 고려할 필요가 없다.
  - 교정: 최대값·분위수·burst·고장전환을 포함한 worst-case를 확인해야 한다.
- **sw08_fatal_jitter_equals_latency**: Jitter는 Latency와 동일한 개념이며 별도 측정할 필요가 없다.
  - 교정: Latency는 지연량이고 Jitter는 지연의 변동이므로 별도 관리해야 한다.
- **sw08_fatal_cycle_is_serialization**: Cycle time은 frame 한 개의 serialization time과 항상 같다.
  - 교정: Cycle time은 task, network update와 producer-consumer phase를 포함한다.
- **sw08_fatal_ptp_guarantees_deadline**: PTP를 적용하면 모든 packet의 deadline과 Determinism이 자동 보장된다.
  - 교정: PTP는 clock synchronization을 제공하며 traffic scheduling과 queue control은 별도 설계해야 한다.
- **sw08_fatal_software_timestamp_equal**: Software timestamping은 모든 부하에서 hardware timestamping과 동일한 정확도를 보장한다.
  - 교정: Timestamp 위치와 processing jitter가 다르므로 요구정확도에 따라 hardware timestamping을 검토해야 한다.
- **sw08_fatal_qos_eliminates_congestion**: Priority 또는 QoS 설정만으로 congestion과 deadline miss를 완전히 제거할 수 있다.
  - 교정: Admission control, policing, scheduling, load limit과 queue 검증이 함께 필요하다.
- **sw08_fatal_tsn_automatic**: TSN capable 장비를 연결하면 profile·schedule·clock 구성 없이 자동으로 결정적 통신이 된다.
  - 교정: TSN 기능조합, end-to-end profile, schedule와 clock configuration이 필요하다.
- **sw08_fatal_redundancy_zero_recovery**: 네트워크를 이중화하면 모든 고장에서 packet loss와 recovery time이 0이 된다.
  - 교정: 보호고장과 protocol 특성, path independence와 application recovery를 구분해야 한다.
- **sw08_fatal_all_ring_seamless**: 모든 ring topology는 단선 시 무손실·무지연으로 자동 전환된다.
  - 교정: Ring recovery는 protocol, ring size, supervision과 fault type에 따라 달라진다.
- **sw08_fatal_mrp_zero_universal**: MRP는 모든 장치와 ring 규모에서 zero-time recovery를 보장한다.
  - 교정: MRP recovery profile과 실제 장치·ring 조건에서 복구시간을 검증해야 한다.
- **sw08_fatal_dlr_universal**: DLR은 모든 Ethernet protocol과 임의 switch에 공통 적용되는 범용 ring 기능이다.
  - 교정: DLR은 EtherNet/IP 생태계의 device-level ring 구조와 지원 장치조건을 가진다.
- **sw08_fatal_prp_shared_path**: PRP는 두 port가 같은 switch와 cable path를 공유해도 독립 dual LAN과 같은 보호효과를 낸다.
  - 교정: PRP의 LAN A와 LAN B는 failure domain을 실질적으로 분리해야 한다.
- **sw08_fatal_hsr_plain_ring**: HSR은 일반 switch ring과 동일하여 duplicate transmission, forwarding와 duplicate discard가 필요 없다.
  - 교정: HSR은 양방향 중복전송과 node forwarding·duplicate discard를 전제로 한다.
- **sw08_fatal_packet_loss_harmless**: 소량 Packet loss는 sequence와 stale data 처리 없이도 제어에 항상 무해하다.
  - 교정: Application별 loss budget, sequence monitoring, timeout와 stale-data 정책이 필요하다.
- **sw08_fatal_multicast_always_filtered**: Multicast는 설정하지 않아도 switch가 항상 필요한 receiver port로만 전달한다.
  - 교정: Group management와 snooping·querier 동작을 확인하지 않으면 flooding될 수 있다.
- **sw08_fatal_buffer_solves_all**: Switch buffer를 크게 하면 Packet loss와 실시간 지연을 동시에 완전히 제거한다.
  - 교정: Buffer는 burst를 흡수하지만 queueing delay를 늘릴 수 있으므로 traffic engineering이 필요하다.
- **sw08_fatal_failover_state_automatic**: Link가 복구되면 controller와 remote I/O의 application state도 검증 없이 항상 정상화된다.
  - 교정: Failover 후 duplicate, sequence, stale command와 state consistency를 시험해야 한다.
- **sw08_fatal_dual_port_independent**: 장치에 network port 두 개가 있으면 power, switch와 cable route도 자동으로 독립된다.
  - 교정: Failure domain과 common-cause path를 별도로 확인해야 한다.
- **sw08_fatal_no_local_fallback**: 네트워크 redundancy가 있으면 critical equipment의 local fallback 또는 safe-state 설계는 불필요하다.
  - 교정: Residual failure에 대비해 공정위험에 맞는 local fallback·safe state를 정의해야 한다.

## Warn/Major 수준의 부족한 표현

- **sw08_major_requirements_not_quantified**: 빠름·안정적이라는 정성표현만 있고 Latency, Jitter, loss, sync와 recovery 목표를 수치화하지 않는다.
  - 보완: 기능별 performance budget과 acceptance criterion을 제시한다.
- **sw08_major_definitions_mixed**: Latency, Jitter, Cycle time와 Response time을 혼용한다.
  - 보완: 각 지표를 정의하고 end-to-end 관계를 설명한다.
- **sw08_major_average_without_worst_case**: 평균값만 제시하고 burst·최대부하·고장전환을 누락한다.
  - 보완: Worst-case traffic과 failure transient를 포함한다.
- **sw08_major_load_assumption_missing**: Network load와 traffic matrix 없이 QoS 또는 bandwidth만 제안한다.
  - 보완: 정상·시작·알람·복구 traffic과 headroom을 산정한다.
- **sw08_major_tsn_feature_listing**: TSN 기능 이름만 나열하고 profile, schedule, clock와 end-to-end 구성을 연결하지 않는다.
  - 보완: Qbv·preemption·policing을 요구와 경로에 배치한다.
- **sw08_major_ptp_architecture_missing**: PTP를 언급하지만 clock role, profile, timestamping과 failover를 설명하지 않는다.
  - 보완: Grandmaster·boundary/transparent clock·holdover를 설계한다.
- **sw08_major_redundancy_without_fault_model**: 이중화 방식만 제시하고 보호대상 고장과 failure domain을 정의하지 않는다.
  - 보완: Link·switch·power·path 고장과 common cause를 구분한다.
- **sw08_major_recovery_not_end_to_end**: Protocol recovery time만 제시하고 application timeout과 state recovery를 누락한다.
  - 보완: Network와 application recovery를 end-to-end로 측정한다.
- **sw08_major_failover_state_missing**: 전환 후 duplicate·out-of-order·stale command 검증이 없다.
  - 보완: Application state consistency와 복귀절차를 시험한다.
- **sw08_major_storm_congestion_missing**: 정상 cyclic traffic만 다루고 broadcast storm, multicast flooding과 congestion을 누락한다.
  - 보완: Fault traffic과 containment를 설계한다.
- **sw08_major_fallback_missing**: Network loss 시 local fallback, safe state 또는 graceful degradation 전략이 없다.
  - 보완: 공정위험 기반 fallback과 제한운전을 정의한다.
- **sw08_major_validation_missing**: 설계설명만 있고 synchronized measurement와 fault injection acceptance가 없다.
  - 보완: 최대·분위수·loss·clock offset·recovery를 시험한다.

## False positive 주의사항

- 낮은 평균 Latency를 제시했다는 이유만으로 Fatal로 보지 말고 worst-case 상한을 별도 제시했는지 확인한다.
- Jitter를 range, standard deviation, percentile 또는 maximum variation으로 표현할 수 있으므로 문맥상 변동을 다루면 인정한다.
- Cycle time과 update time 용어가 제조사마다 다를 수 있으므로 producer-network-consumer 주기를 정확히 설명하면 인정한다.
- QoS 사용 자체를 과대평가로 보지 말고 admission control과 load 조건을 함께 제시했는지 확인한다.
- TSN의 모든 기능을 사용하지 않아도 요구에 필요한 subset과 profile을 정당화하면 인정한다.
- PTP와 IEEE 802.1AS를 같은 것으로 단정하지 말고 profile과 적용망의 차이를 설명하는 답안을 인정한다.
- Hardware timestamping이 항상 필수인 것은 아니며 요구 정확도를 software timestamping으로 충족한다는 근거가 있으면 인정한다.
- MRP 또는 DLR recovery 수치는 장치와 profile에 따라 달라지므로 특정 수치를 보편오류로 단정하지 않는다.
- PRP와 HSR을 zero-time recovery라고 표현해도 정의된 단일고장·적합구성·application 조건을 함께 제시하면 인정한다.
- Ring을 사용했다고 낮게 평가하지 말고 허용 recovery time과 fault model에 적합한지 확인한다.
- Broadcast와 multicast를 제한한다고 해서 무조건 정답이 아니며 정상 discovery·group traffic 요구를 고려했는지 확인한다.
- Buffer 사용을 언급해도 traffic shaping과 latency 영향을 함께 설명하면 과도한 단순화로 보지 않는다.
- Hold-last가 항상 위험한 것은 아니며 공정 동특성과 hazard analysis에 근거하면 적절할 수 있다.
- Graceful degradation이 안전기능 우회라는 뜻은 아니며 핵심제어·안전기능 유지와 비핵심기능 제한을 구분하면 인정한다.
- SW-07 protocol 또는 SW-09 보안을 일부 언급해도 SW-08 정량 성능·복구 설계의 근거로 제한되면 범위이탈로 보지 않는다.

## Question pattern

- **sw08_qp_performance_metrics**: Latency, Jitter, Cycle time, Response time와 Determinism의 정의·관계를 설명하는 문제
- **sw08_qp_deterministic_design**: 산업 네트워크의 worst-case 결정성 설계절차와 acceptance를 묻는 문제
- **sw08_qp_qos_scheduling**: Priority, QoS, scheduling과 congestion 관리방안을 묻는 문제
- **sw08_qp_tsn**: TSN 구성요소와 실시간 산업망 적용조건을 설명하는 문제
- **sw08_qp_ptp**: PTP 시간동기 구조, 오차요인과 검증을 설명하는 문제
- **sw08_qp_redundancy_compare**: MRP, DLR, PRP와 HSR의 구조·복구성능·적용조건을 비교하는 문제
- **sw08_qp_fault_recovery**: 장애검출부터 application 복구까지 end-to-end recovery를 설계하는 문제
- **sw08_qp_traffic_faults**: Packet loss, Broadcast storm, Multicast와 Congestion의 원인·영향·대책을 설명하는 문제
- **sw08_qp_resilience**: Network loss 시 fallback local control과 graceful degradation을 설계하는 문제
- **sw08_qp_verification**: 실시간성·시간동기·장애복구의 계측 및 fault injection 시험절차를 묻는 문제

## Routing alias

- 산업 네트워크 실시간성 결정성 시간동기 장애복구
- industrial network realtime determinism time synchronization resilience
- latency jitter cycle time response time design
- worst case network delay deadline analysis
- industrial ethernet deterministic performance engineering
- network load QoS scheduling congestion control
- TSN PTP deterministic industrial network
- IEEE 802.1Qbv time aware shaper design
- IEEE 1588 PTP clock synchronization architecture
- grandmaster boundary clock transparent clock
- MRP DLR PRP HSR redundancy comparison
- industrial ring recovery time evaluation
- PRP HSR seamless redundancy failure domain
- packet loss broadcast storm multicast congestion
- network failover application state consistency
- fallback local control graceful degradation
- network resilience fault injection acceptance test
- redundancy health monitoring latent failure
- clock offset jitter latency recovery measurement
- industrial network deadline miss analysis
- TSN scheduling policing frame preemption
- network recovery fault containment common cause
- control network performance acceptance criteria
- 산업망 복원력 이중화 고장주입 시험
- industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience

## Focused regressions

- Metadata와 schema version 일관성
- 40개 Fact Anchor 및 20개 Fatal 계약
- Deterministic check 비활성화와 LLM semantic verification
- C 계층 single-owner score contract
- TSN·PTP·MRP·DLR·PRP·HSR 정확성
- Latency·Jitter·Cycle time·Response time 구분
- SW-07 및 SW-09 ownership 경계
- Topic Sheet 12개 section과 전체 모범답안
- 정확히 7개 source 파일 및 EOF newline

## 모범답안

### 1. 요구사항과 성능지표

산업 네트워크 설계는 먼저 제어기능별 허용 성능을 수치화해야 한다. Latency는 송신부터 수신까지의 전달지연이다. Jitter는 그 지연의 변동이다. Cycle time은 제어·통신 갱신의 반복주기이다. Response time은 센싱, 제어연산, 통신, 출력갱신과 장치동작을 포함한 전체 응답시간이다. 따라서 네트워크 지연은 전체 제어응답 budget의 일부로 배분한다. Packet loss, clock offset, 허용 recovery time과 availability도 acceptance criterion으로 정의한다.

### 2. Determinism과 Traffic Budget

Determinism은 평균속도가 빠르다는 뜻이 아니다. 정의된 최대부하와 고장조건에서 전달시간이 예측 가능한 상한 안에 있고 deadline을 만족한다는 뜻이다. Serialization, switching, queueing, propagation과 processing delay를 합산한다. 평균 traffic뿐 아니라 startup, alarm burst, diagnostic, recovery traffic과 향후 확장여유를 포함한다. Throughput과 latency를 분리하고 maximum 또는 high percentile과 deadline miss를 관리한다.

### 3. QoS, Scheduling과 TSN

Priority와 QoS는 중요한 traffic의 queueing 우선순위를 높이지만 admission control과 load limit 없이 절대 deadline을 보장하지 않는다. Cyclic scheduling과 traffic shaping으로 producer phase와 queue interference를 줄인다. TSN은 단일 protocol이 아니라 시간동기, schedule, shaping, policing과 redundancy 기능을 조합하는 기술군이다. Qbv는 공통시간에 맞춰 queue gate를 개폐한다. Frame preemption은 긴 저우선 frame의 blocking을 줄인다. Per-stream policing은 faulty talker의 rate와 burst를 제한한다. 적용 시 장치 profile, end-to-end schedule, guard band와 configuration consistency를 검증한다.

### 4. 시간동기화

PTP는 Grandmaster와 ordinary, boundary, transparent clock을 이용해 분산 clock의 시간과 위상을 맞춘다. Hardware timestamping, residence-time 보정, path asymmetry, oscillator, profile과 topology가 정확도에 영향을 준다. Grandmaster loss 시 BMCA 재선정과 holdover 성능도 확인한다. 다만 clock synchronization은 schedule의 기준일 뿐 queue와 application execution을 자동 제어하지 않으므로 Determinism과 동일하지 않다.

### 5. Redundancy와 장애복구

Redundancy는 보호할 fault와 허용 loss·recovery time을 먼저 정한 뒤 선정한다. Recovery time에는 failure detection, topology reconfiguration, port 또는 route 전환, address relearning, application timeout과 state recovery가 포함된다. MRP는 ring manager와 client 기반의 재구성 ring이다. DLR은 EtherNet/IP device-level ring에서 supervisor와 node를 사용한다. PRP는 독립된 두 LAN으로 frame을 병렬전송하고 수신측에서 duplicate를 제거한다. HSR은 ring 양방향 중복전송과 node forwarding을 사용한다. PRP와 HSR은 정의된 단일고장에서 seamless 특성을 제공할 수 있지만 shared power, cable route와 configuration 같은 common-cause는 별도 관리해야 한다.

### 6. Fault Traffic와 Failover

Packet loss는 sequence, quality, timeout와 stale-data 정책으로 검출하고 상위제어에 전달한다. Broadcast loop와 storm은 loop prevention, storm control과 segmentation으로 격리한다. Multicast는 group membership, snooping·querier와 flooding 범위를 관리한다. Congestion은 buffer 증설만으로 해결하지 않고 traffic engineering, shaping과 policing으로 다룬다. Network link가 복구되어도 application state가 자동 일치하는 것은 아니므로 duplicate, out-of-order, stale command와 sequence recovery를 시험한다.

### 7. Resilience 운전전략

복원력은 이중 port의 수보다 failure domain의 독립성이 중요하다. Switch, power, cabinet, cable route, clock source와 interface의 공통원인을 분리한다. Standby path의 latent failure를 supervision과 주기시험으로 검출한다. 모든 network redundancy가 실패할 가능성에 대비해 critical equipment는 local autonomous control, hold-last, safe state 또는 제한운전으로 전환한다. Graceful degradation은 historian, diagnostic, optimization 같은 비핵심기능을 제한하면서 핵심 제어와 안전기능을 유지하고 operator에게 상태를 명확히 알리는 전략이다.

### 8. 검증과 결론

검증은 synchronized packet capture, device diagnostics와 application timestamp를 함께 사용한다. 정상·최대부하·burst 상태에서 maximum·percentile Latency, Jitter, loss, clock offset와 deadline miss를 측정한다. Cable open, switch power loss, node failure, Grandmaster loss, loop와 traffic burst를 fault injection하여 detection, failover, recovery, 공정영향과 복귀절차를 확인한다. Protocol 종류와 상호운용성은 SW-07, authentication·encryption·firewall와 incident response는 SW-09로 구분한다. SW-08의 핵심은 정량 성능예산과 검증 가능한 복원력이다.
