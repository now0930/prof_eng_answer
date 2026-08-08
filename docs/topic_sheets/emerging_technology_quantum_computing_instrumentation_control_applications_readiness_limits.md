# Topic Sheet — 양자컴퓨팅 등 신기술의 계측제어 적용·성숙도·한계 평가

## 1. Topic identity

- Topic ID: `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits`
- Official criterion: `IC-2027-W-5-1`
- Official scope: 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등)
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `HIGH`
- Historical frequency: 근거가 없어 사용하지 않음

## 2. Coverage gap

현재 `IC-2027-W-5-1`은 PARTIAL이다.

기존 source가 AI/ML, Physical AI·robot, Digital Twin, IIoT·Smart Factory, Edge/Cloud, interoperability, Digital Thread를 소유하지만 공식 예시에 명시된 quantum computing과 기타 emerging technology를 독립 답안으로 구성할 static owner가 없다.

본 Topic은 이 residual scope를 닫기 위해 작성한다.

## 3. Quantum computing의 정의

Quantum computing은 qubit의 양자상태와 quantum operation을 이용하여 특정 계산문제를 처리하는 계산 패러다임이다.

모든 문제를 classical computer보다 빠르게 처리하는 범용 가속기로 정의하면 안 된다.

핵심은 problem structure와 algorithm, hardware, data encoding, output sampling을 포함한 **end-to-end advantage**다.

## 4. Qubit, superposition, measurement

Classical bit는 측정 가능한 0 또는 1을 사용한다.

Qubit는 probability amplitude로 표현되는 quantum state를 가진다.

Superposition은 basis state amplitude가 결합된 상태다.

하지만 measurement는 classical outcome을 반환한다.

따라서 superposition을 “모든 답을 동시에 계산하고 한 번에 읽는 기능”으로 설명하면 안 된다.

## 5. Entanglement와 interference

Entanglement는 복수 qubit 사이의 비고전적 correlation을 제공할 수 있다.

이는 faster-than-light information transfer를 의미하지 않는다.

Interference는 계산경로 amplitude를 강화·상쇄하여 원하는 outcome의 측정확률을 변화시키는 핵심 메커니즘이다.

## 6. Gate-based와 quantum annealing

Gate-based 방식은 initialization → quantum gate sequence → measurement의 circuit model이다.

Quantum annealing은 주로 optimization problem을 energy landscape에 매핑하여 낮은 energy state를 탐색하는 문제특화 접근이다.

두 방식은 동일하지 않다.

계측제어 답안에서는 기술명보다 어떤 workload에 맞는지 설명해야 한다.

## 7. Hybrid quantum-classical architecture

현장 적용은 다음 구조로 보는 것이 적절하다.

`Plant/OT data → classical preprocessing → problem encoding → quantum subproblem → measurement/sampling → classical post-processing/optimization → existing OT decision boundary`

Quantum processor가 sensor-to-actuator control chain 전체를 대체하는 구조가 아니다.

## 8. 계측제어 candidate use case

Candidate use case는 다음처럼 제시할 수 있다.

- 생산·정비·에너지 scheduling
- constrained combinatorial optimization
- parameter/state estimation
- inverse problem
- uncertainty evaluation
- supervisory optimization

다만 candidate라는 사실만으로 quantum advantage를 의미하지 않는다.

동일문제의 classical baseline이 필요하다.

## 9. Input/output overhead

Classical plant data를 quantum state로 encoding하는 state preparation 비용이 존재할 수 있다.

Output도 measurement와 repeated sampling을 거쳐 classical result로 해석한다.

따라서 quantum kernel time만으로 성능을 평가하면 안 된다.

`T_total = T_preprocess + T_encode + T_queue/network + T_quantum + T_shots + T_postprocess`

이 식은 특정 hardware의 고정 수식이 아니라 end-to-end latency decomposition을 위한 개념식이다.

## 10. Noise와 error

실제 quantum hardware는 gate error, readout error, decoherence 등 noise의 영향을 받는다.

Error mitigation은 noisy result의 bias를 줄이는 접근이다.

Quantum error correction은 logical information을 보호하기 위해 추가 physical resource와 correction을 사용하는 별도 개념이다.

두 개념을 동일시하면 안 된다.

Physical qubit count만으로 useful capability를 판단하지 않는다.

## 11. Real-time control boundary

PLC·DCS·SIS는 deterministic I/O, local availability, fail-safe와 lifecycle verification을 담당한다.

Quantum computation은 계산 subproblem의 후보이다.

따라서 hard real-time protection/control loop를 직접 대체한다고 전제하지 않는다.

우선 검토대상은 offline, planning, supervisory optimization처럼 시간여유가 있는 계산이다.

End-to-end latency, jitter, determinism을 실제 control requirement와 비교한다.

## 12. Quantum sensing boundary

Quantum sensing은 quantum state의 민감도를 이용하는 측정기술이다.

Quantum computing은 계산처리 기술이다.

둘은 quantum technology라는 상위 범주에서 관련될 수 있지만 같은 기술이 아니다.

본 Topic은 quantum computing 중심의 emerging-technology application evaluation을 소유한다.

## 13. Readiness와 maturity

다음 세 수준을 구분한다.

1. **Research potential**: 원리·논문·laboratory result가 존재한다.
2. **Pilot readiness**: representative problem에서 repeatability와 integration을 검증할 수 있다.
3. **Production readiness**: scale, supportability, availability, verification, lifecycle operation이 충족된다.

Research result를 production readiness로 직접 승격하면 안 된다.

## 14. Benchmark와 pilot

도입 판단은 다음 순서로 수행한다.

1. Problem bottleneck 정의
2. Classical baseline 확보
3. Quantum/hybrid candidate mapping
4. Representative data/problem으로 PoC
5. Solution quality·runtime·repeatability 비교
6. End-to-end latency·failure handling 검증
7. Pilot acceptance
8. Production integration 여부 결정

Vendor benchmark 하나만으로 ROI를 확정하지 않는다.

## 15. TCO, skills, legacy integration

Company adoption에서는 다음 비용을 포함한다.

- compute/service access
- network/interface
- classical orchestration
- data engineering
- specialist skill
- verification and validation
- support and incident response
- migration
- legacy coexistence
- lifecycle change management

기존 설비를 전면 교체하기보다 가치가 확인된 calculation subproblem부터 단계적으로 연계하는 방법이 현실적일 수 있다.

## 16. Security와 governance

External 또는 hybrid compute를 OT/IT에 연결하면 다음을 평가한다.

- data exposure
- access control
- dependency
- algorithm/result provenance
- change control
- auditability
- fallback path

신기술이라고 기존 보안·변경관리 원칙이 사라지지 않는다.

## 17. 기타 emerging technology 평가프레임

공식 criterion의 “등”에 대응하기 위해 개별 기술명을 무한히 추가하지 않는다.

기타 신기술은 다음 공통 프레임으로 평가한다.

`원리 → 해결문제 → 계측제어 use case → maturity → integration → limitation → verification → TCO`

최신 뉴스, 법령, 표준 edition의 rolling update는 `IC-2027-W-5-2 / DYNAMIC_REVIEW_LANE`으로 분리한다.

## 18. Ownership boundary

본 Topic의 OUT:

- `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle`
- `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
- `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread`
- `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability`
- `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- `IC-2027-W-5-2 / DYNAMIC_REVIEW_LANE`

위 영역은 필요할 때 경계 설명만 하고 세부 지식을 중복 소유하지 않는다.

## 19. 기술사 답안 권장 흐름

1. 신기술과 quantum computing의 위치를 정의한다.
2. Qubit·superposition·measurement·interference 원리를 간결히 설명한다.
3. Gate/annealing과 hybrid architecture를 설명한다.
4. 계측제어 use case를 problem-fit과 classical baseline으로 선정한다.
5. Encoding·sampling·noise·latency·determinism 한계를 설명한다.
6. Readiness와 pilot acceptance를 제시한다.
7. TCO·skills·legacy·governance를 회사 적용조건으로 제시한다.
8. 기타 emerging technology에도 같은 평가프레임을 확장한다.

## 20. Coverage gate

이 Topic source를 생성했다고 `IC-2027-W-5-1`을 즉시 `COVERED`로 승격하지 않는다.

Focused validation, release/classification registration, generated rebuild, full validation 및 ChatGPT semantic re-audit를 모두 통과한 뒤 coverage를 다시 판정한다.
