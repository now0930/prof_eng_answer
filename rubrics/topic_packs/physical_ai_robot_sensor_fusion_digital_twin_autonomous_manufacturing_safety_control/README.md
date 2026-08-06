# Physical AI, 로봇, 센서융합, Digital Twin, 자율제조 및 안전제어

## Topic ID

`physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`

## Lane

`SOFTWARE_LLM_LANE_C`

## Question type

`PRINCIPLE_INTERPRETATION`

## Scope

- Physical AI와 Closed-loop Robot
- Camera·LiDAR·Radar·Encoder·Force Sensor Fusion
- State Estimation, Localization, SLAM과 World Model
- Digital Twin, Simulation과 Synthetic Data
- Robot Planning, Edge AI와 End-to-end Latency
- Autonomous Manufacturing와 Human–Robot Collaboration
- Safety Envelope, Safe State, Fallback과 Supervisory Control
- Functional Safety, Human Override와 Runtime Monitoring

## Ownership Boundary

- SW-12: 데이터 기반 AI Model 학습·평가·Drift·Retraining
- SW-13: AI와 물리시스템 상호작용, Robot와 안전제어
- SW-05: SIS·SIL Safety Software Lifecycle
- SW-11: 산업데이터 품질·Context·저장·상위통합

## Authoring Contract

- Fact Anchor: 30
- Fatal misconception: 16
- Major/Warn condition: 12
- Routing alias: 14
- Positive question: 10
- Negative boundary question: 8
- Deterministic checks: disabled
- External LLM validation: excluded
- Generated Bank promotion: excluded
- Production Python/Common Router modification: excluded

## Representative Question

Physical AI 기반 Robot·자율제조 시스템에서 Sensor Fusion, State Estimation, Digital Twin, Planning과 Closed-loop AI를 설명하고 Safety Envelope, Safe State, Fallback, Supervisory Control 및 Human Override를 포함한 안전제어 방안을 제시하시오.

## Fatal Guard

- Digital Twin은 실제 설비와 항상 완전히 동일하지 않다.
- Sensor Fusion은 Sensor 고장과 공통원인을 자동 제거하지 않는다.
- 높은 AI Accuracy는 Robot Functional Safety를 자동 보장하지 않는다.
- Edge AI는 Network·Cybersecurity 검토를 제거하지 않는다.
- Collaborative Robot 제품만으로 협업 Application 안전성이 보장되지 않는다.
- Simulation·Synthetic Data는 실제 현장 Validation을 전부 대체하지 않는다.
- AI Planner 명령은 Safety Constraint 없이 Actuator에 직접 적용하지 않는다.
- Safe State, Fallback, Human Override와 Change Control을 제거하지 않는다.

## Verify-first

정량 Sensor Threshold, 협업한계, Twin Error, Deadline, Safe State와 적용표준은 Robot Cell Risk Assessment와 승인된 운영범위로 확인한다.
