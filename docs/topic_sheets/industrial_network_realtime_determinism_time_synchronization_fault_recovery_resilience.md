# Topic Sheet — 산업 네트워크 실시간성, 결정성, 시간동기화, 장애복구 및 복원력

## 1. Topic metadata

- `topic_id`: `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`
- `SW_NUMBER`: `SW-08`
- `LANE`: `SOFTWARE_LLM_LANE_B`
- `question_type`: `CALC_DESIGN`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `HIGH`

## 2. Scope와 Ownership

SW-08은 Latency, Jitter, Cycle time, Response time, Determinism, Throughput, Network load, Priority, QoS, Scheduling, TSN, PTP, Redundancy, Ring recovery, PRP, HSR, MRP, DLR, Packet loss, Broadcast storm, Multicast, Congestion, Failover, Fallback local control, Graceful degradation과 Network resilience를 담당한다.

SW-07은 Protocol 종류, 물리매체, 일반 통신구조와 상호운용성을 담당한다. SW-09는 Authentication, Encryption, Access control, firewall와 incident response를 담당한다.

## 3. 대표 문제와 답안방향

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

답안은 `정량 요구 → worst-case traffic → scheduling/TSN → PTP → redundancy/recovery → degraded operation → fault validation` 순서로 전개한다.

## 4. 실시간 성능지표

Latency는 end-to-end 전달지연이다. Jitter는 지연변동이다. Cycle time은 반복 갱신주기이다. Response time은 sensing부터 최종동작까지의 전체 시간이다. Throughput은 데이터량이며 Determinism과 동일하지 않다.

- 산업 네트워크 설계는 허용 Latency, Jitter, Cycle time, Response time, Packet loss, 동기정확도, 장애복구시간과 가용성 목표를 정량적으로 먼저 정의해야 한다.
- Latency는 데이터가 송신 지점에서 수신 지점까지 전달되는 지연이며 serialization, switching, queueing, propagation과 protocol processing 지연의 합으로 평가해야 한다.
- Jitter는 반복 전송 또는 도착시각 간 지연의 변동이며 평균 Latency와 구분하여 최대값, 범위 또는 통계분포로 관리해야 한다.
- Cycle time은 제어 또는 통신 작업이 반복되는 주기이며 패킷 1개의 전송시간과 동일하지 않고 생산자·네트워크·소비자의 주기와 위상관계를 포함한다.
- Response time은 입력 변화 또는 사건 발생부터 필요한 출력 또는 조치가 완료될 때까지의 end-to-end 시간으로 센싱, 연산, 통신, 출력 갱신과 장치동작을 포함한다.
- Throughput은 단위시간당 전달 가능한 데이터량이며 낮은 Latency나 Determinism을 자동 보장하지 않으므로 대역폭과 시간성능을 분리해 평가해야 한다.
- Determinism은 주어진 부하와 고장조건에서 통신 완료시간이 예측 가능한 상한 내에 있음을 뜻하며 단순히 평균속도가 빠르다는 의미가 아니다.
- 실시간 설계는 평균값보다 worst-case traffic, 최대 frame, queue interference, topology depth, clock error와 failure transient를 포함한 상한 분석을 우선해야 한다.

## 5. Determinism과 Traffic Engineering

- Network load는 정상·시작·진단·알람·복구 시 traffic을 합산하고 burst와 성장여유를 포함해 설계하며 평균 utilization만으로 충분성을 판단하지 않는다.
- Priority와 QoS는 중요 traffic의 queueing 우선순위를 조정하지만 admission control, policing, queue 설계와 부하제한 없이 모든 deadline을 보장하지 않는다.
- Cyclic scheduling과 traffic shaping은 frame 송신창, queue, producer phase와 경로를 조정하여 간섭을 제한하며 schedule의 end-to-end 일관성과 변경관리가 필요하다.
- TSN은 단일 protocol이 아니라 시간동기, scheduling, shaping, policing, redundancy와 자원예약 기능을 조합하는 IEEE 802.1 기술군이며 적용 profile과 end-to-end 구성이 필요하다.

Worst-case traffic matrix에는 정상 cyclic traffic뿐 아니라 startup, alarm, diagnostic, maintenance와 recovery burst를 포함한다.

## 6. TSN 설계

- TSN은 단일 protocol이 아니라 시간동기, scheduling, shaping, policing, redundancy와 자원예약 기능을 조합하는 IEEE 802.1 기술군이며 적용 profile과 end-to-end 구성이 필요하다.
- IEEE 802.1Qbv Time-Aware Shaper는 공통 시간기준에 따라 queue gate를 개폐해 scheduled traffic의 송신창을 만들며 guard band, schedule cycle과 clock accuracy를 함께 설계해야 한다.
- Frame preemption은 긴 저우선 frame이 고우선 frame을 지연시키는 blocking time을 줄이지만 양단 지원, fragment overhead와 검증이 필요하다.
- Per-stream filtering and policing은 stream별 rate·burst·gate 위반을 제한하여 faulty talker의 영향을 격리하지만 정책 오설정에 따른 정상 traffic 차단을 시험해야 한다.

TSN은 요구에 맞는 profile과 end-to-end configuration을 전제로 한다. 지원표시만으로 성능이 자동 보장되지 않는다.

## 7. PTP와 시간동기화

- PTP는 분산 clock의 시간 또는 위상을 맞추는 protocol이며 측정, sequence of events와 scheduled communication을 지원하지만 자체만으로 control deadline을 보장하지 않는다.
- PTP 설계는 Grandmaster, ordinary clock, boundary clock, transparent clock과 network path를 정의하고 Best Master Clock 선정과 holdover 동작을 검토해야 한다.
- 시간동기 정확도는 hardware timestamping, residence time 보정, link asymmetry, oscillator 성능, profile과 network topology의 영향을 받으므로 end-to-end 측정으로 검증해야 한다.
- Clock synchronization은 schedule과 event ordering의 공통 기준을 제공하지만 queue, load, forwarding과 application scheduling을 제어하지 않으면 Determinism이 성립하지 않는다.

Clock synchronization accuracy와 packet delivery deadline은 별도의 acceptance criterion이다.

## 8. Redundancy와 장애복구

- Redundancy 설계는 보호할 고장, 허용 packet loss, 허용 recovery time, topology, common-cause failure와 유지보수 방식을 먼저 정의한 뒤 protocol을 선정해야 한다.
- 장애복구시간은 고장검출, 상태판단, topology 재구성, route 또는 port 전환, address relearning, application timeout과 control state recovery의 합으로 보아야 한다.
- Ring redundancy는 link 또는 node 고장 시 대체경로를 제공하지만 recovery time은 protocol, ring size, supervision interval, switch implementation과 fault type에 따라 달라진다.
- MRP는 일반적으로 ring manager와 ring client가 상태를 감시하고 고장 시 blocked path를 전환하는 방식이며 구성 profile과 ring 조건에 따른 복구시간을 검증해야 한다.
- DLR은 EtherNet/IP 계열 device-level ring에서 supervisor와 ring node가 beacon 또는 announce를 이용해 고장을 감지·복구하며 모든 Ethernet protocol의 범용 ring 표준으로 보아서는 안 된다.
- PRP는 동일 frame을 독립된 두 LAN으로 동시에 보내고 수신 노드가 중복을 제거하여 단일 LAN 고장 시 재수렴 없이 통신을 지속하도록 설계한다.
- HSR은 ring 양방향으로 frame을 중복 전송하고 node가 frame을 전달·중복제거하여 단일 고장에 대한 seamless communication을 목표로 하며 node forwarding과 traffic overhead를 고려해야 한다.
- PRP와 HSR의 seamless 특성은 정의된 단일고장과 적합한 node·path 구성에서 성립하며 공통 전원, shared switch, configuration error와 다중고장은 별도 보호가 필요하다.

MRP·DLR은 재구성형 ring의 특성을 가지며 PRP·HSR은 적합구성에서 seamless redundancy를 목표로 한다. 공통원인과 application recovery는 별도 검증한다.

## 9. Packet loss, Storm와 Congestion

- Packet loss는 bit error, buffer overflow, link flap, policing, topology change와 receiver overload에서 발생할 수 있으며 loss budget, sequence monitoring과 application의 stale-data 처리를 정의해야 한다.
- Broadcast storm은 loop, malfunction 또는 과도한 discovery로 대역폭과 CPU를 소진할 수 있으므로 loop prevention, storm control, segmentation과 fault containment가 필요하다.
- Multicast traffic은 one-to-many 전달에 효율적이지만 group membership, snooping·querier, flooding 범위와 receiver capacity를 관리하지 않으면 불필요한 부하가 확산될 수 있다.
- Congestion은 ingress traffic이 link 또는 queue service capacity를 초과할 때 지연·drop을 발생시키며 buffer 증설만으로 deadline을 보장할 수 없고 traffic engineering이 필요하다.
- Network failover 후에도 controller, remote I/O, sequence, redundancy manager와 application session의 상태가 일관되어야 하며 duplicate, out-of-order, stale command를 검증해야 한다.

Sequence, quality, timeout, storm control, multicast group 관리와 traffic engineering을 함께 사용한다.

## 10. Failover와 Resilience 운전전략

- Network failover 후에도 controller, remote I/O, sequence, redundancy manager와 application session의 상태가 일관되어야 하며 duplicate, out-of-order, stale command를 검증해야 한다.
- Network 상실 시 critical equipment는 정의된 local control, hold-last, safe state 또는 제한운전으로 전환하도록 설계하고 전환조건과 복귀절차를 검증해야 한다.
- Graceful degradation은 일부 통신·진단·최적화 기능을 제한하면서 핵심 제어와 안전기능을 유지하는 전략이며 기능우선순위와 operator indication을 사전에 정의해야 한다.
- Redundancy는 standby path와 duplicate channel의 건강상태를 지속 감시하고 latent failure를 알람·시험해야 실제 가용성을 유지할 수 있다.
- 복원력은 link뿐 아니라 switch, power, cabinet, cable route, clock source, controller interface와 configuration의 failure domain을 분리하고 common-cause failure를 줄여야 한다.

통신복구와 공정상태 복구를 구분한다. Critical control에는 local fallback과 graceful degradation을 둔다.

## 11. 검증, 채점기준과 Focused regression

- 복원력은 link뿐 아니라 switch, power, cabinet, cable route, clock source, controller interface와 configuration의 failure domain을 분리하고 common-cause failure를 줄여야 한다.
- 복구성능은 cable open, switch power loss, node failure, clock loss, traffic burst, loop와 packet impairment를 계획적으로 주입하여 검출·전환·공정영향·복귀를 측정해야 한다.
- 검증은 synchronized capture, device diagnostics와 application timestamp를 이용해 최대·분위수 Latency, Jitter, loss, clock offset, recovery time과 deadline miss를 기록하고 요구값과 비교해야 한다.
- Protocol 종류, 물리매체, 일반 통신구조, Device Profile과 상호운용성 선정은 SW-07의 범위이고 SW-08은 정량적 시간성능·동기·복구·복원력을 담당한다.
- Authentication, encryption, access control, firewall와 cyber incident response는 SW-09의 범위이며 SW-08은 장애·혼잡·고장전환에 대한 성능과 복원력에 집중한다.

- Fatal: 평균값을 Determinism으로 간주하거나 PTP·QoS·TSN·Redundancy를 자동보장으로 설명하는 경우
- Major: 정량 목표, worst-case, failure domain, application recovery 또는 fault test가 누락된 경우
- Safe: 조건, profile, 적용범위와 acceptance를 명시한 경우
- Focused regression: 37개

## 12. 모범답안

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
