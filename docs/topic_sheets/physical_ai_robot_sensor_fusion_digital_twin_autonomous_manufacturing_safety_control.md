# Physical AI, 로봇, 센서융합, Digital Twin, 자율제조 및 안전제어

## Topic

- SW 번호: `SW-13`
- Topic ID: `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
- 한글 주제: Physical AI, 로봇, 센서융합, Digital Twin, 자율제조 및 안전제어
- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`

## 범위

포함 범위:

1. Physical AI와 Sensor–Actuator Closed Loop
2. Industrial Robot와 Collaborative Robot Application
3. Camera, LiDAR, Radar, Encoder, Force·Torque Sensor
4. Sensor Fusion, Calibration, Time Alignment와 Common Cause
5. State Estimation, Localization, SLAM과 World Model
6. Digital Twin, Fidelity, Synchronization과 Validation
7. Simulation, Synthetic Data와 Domain Gap
8. Robot Planning, Edge AI, On-device AI와 Latency
9. Autonomous Manufacturing와 Human–Robot Collaboration
10. Safety Envelope, Safe State, Fallback과 Degraded Mode
11. Supervisory Control, Human Override와 Functional Safety
12. 승인 운영범위, Runtime Monitoring과 Change Control

## 제외 범위

- 산업 AI Model의 Train·Validation·Test, Data Leakage, Precision·Recall, Drift와 Retraining 상세
- Historian, MES, ERP, Timestamp, Quality Code와 Batch Genealogy 상세
- SIS Safety Application Program의 SIL·Systematic Failure·Safety V&V 상세
- PLC Sequence, Interlock, Trip과 일반 Fail-safe Logic 상세
- 통신 Protocol Frame, QoS와 Wire-level 상호운용
- Generated Bank, 공통 Router, Production Python과 공통 Release Script 수정

## 인접 Topic Ownership

### SW-12와의 경계

SW-12가 소유하는 내용:

- 데이터 기반 학습·추론 Model
- Anomaly Detection, Predictive Maintenance와 Model Lifecycle
- Data Leakage, 성능지표, Drift와 Retraining

SW-13이 소유하는 내용:

- AI와 물리 설비·Robot의 상호작용
- Sensor Fusion, Localization, SLAM과 World Model
- Digital Twin, Planning과 Closed-loop Control
- Safety Envelope, Safe State, Fallback과 Human Override

### SW-05와의 경계

- SW-05는 SIS·SIL Safety Software Lifecycle, Systematic Failure와 Safety V&V를 소유한다.
- SW-13은 Robot·자율제조 Application의 물리적 위험, Runtime Assurance와 안전제어 구조를 소유한다.
- Functional Safety 표준 Clause와 인증범위는 verify-first 한다.

### SW-11과의 경계

- SW-11은 데이터의 Timestamp, Quality, Context, 저장과 상위시스템 통합을 소유한다.
- SW-13은 해당 Data를 실시간 Perception과 물리 Action에 사용하는 Closed-loop를 소유한다.

## 대표 문제

> Physical AI 기반 Robot·자율제조 시스템에서 Sensor Fusion, State Estimation, Digital Twin, Planning과 Closed-loop AI를 설명하고 Safety Envelope, Safe State, Fallback, Supervisory Control 및 Human Override를 포함한 안전제어 방안을 제시하시오.

## 핵심 Fact

1. Physical AI는 AI의 인식·추론·계획 결과가 Sensor와 Actuator를 통해 실제 물리환경에 작용하고 그 결과를 다시 Feedback으로 받는 폐루프 시스템 영역이다.
2. Industrial Robot System은 Manipulator, Controller, Drive, End-effector, Sensor, Cell 설비와 Safety 기능을 포함한 시스템 경계로 평가한다.
3. Collaborative Robot은 협업기능을 지원하는 Robot이며 실제 협업 Application의 안전성은 Tool, Payload, 속도, 힘, 작업공간, 공정위험과 보호조치를 포함해 평가한다.
4. Camera, LiDAR, Radar, Encoder와 Force·Torque Sensor는 측정원리, 범위, 해상도, 지연과 환경민감도가 달라 상호 보완적으로 사용한다.
5. Sensor Fusion은 측정값뿐 아니라 Timestamp, Sample Rate, Transport Delay와 Clock Synchronization을 관리하여 동일 물리상태의 관측을 정렬해야 한다.
6. 다중 Sensor는 Intrinsic·Extrinsic Calibration과 좌표계 변환을 통해 공통 Frame에 정렬하며 Calibration Drift를 Monitoring해야 한다.
7. Sensor Fusion은 각 Sensor의 Bias, Noise, Covariance와 신뢰도를 반영해 상태와 불확실성을 추정하며 단순 평균이 항상 최적은 아니다.
8. Sensor를 여러 개 사용해도 공통전원, 공통시야, 동일 환경조건, Calibration 오류와 공통 Software 결함이 남을 수 있으므로 Residual, Plausibility와 상태진단이 필요하다.
9. State Estimation은 직접 측정할 수 없는 위치, 속도, 자세와 외력 등을 System Model과 Sensor 관측으로 추정하고 오차공분산을 함께 관리한다.
10. Localization은 Robot 또는 이동체의 위치와 자세를 기준좌표계에서 추정하는 기능이며 Map, Landmark, Odometry와 Sensor 불확실성에 의존한다.
11. SLAM은 위치추정과 Map 생성을 상호 의존적으로 수행하지만 안전정지, 충돌회피와 Functional Safety를 단독으로 보장하지 않는다.
12. State Estimator의 성능은 Sensor 배치와 Motion에 따른 Observability에 제한되며 관측되지 않는 상태는 Model만으로 확정할 수 없다.
13. World Model은 Robot 주변의 객체, 자유공간, 작업상태, 관계와 불확실성을 표현하여 Planning과 Supervisory 판단에 제공한다.
14. Digital Twin은 특정 목적과 수명주기 범위에서 실제 자산·공정의 상태와 거동을 데이터와 Model로 연결한 디지털 표현이다.
15. Digital Twin의 Fidelity는 목적, Model 가정, 해상도, Parameter, Boundary Condition과 Validation 범위에 따라 달라지며 실제 설비와 항상 완전히 동일하지 않다.
16. Digital Twin은 실제 설비와의 Data Synchronization, Version, Timestamp, Latency와 상태정합성을 Monitoring해야 하며 Stale Twin은 잘못된 의사결정을 만들 수 있다.
17. Simulation은 반복가능한 시험과 위험 Scenario 탐색에 유용하지만 Model 경계와 Scenario Coverage 밖의 실제환경 성능을 자동 증명하지 않는다.
18. Synthetic Data는 희귀상황과 위험상황을 보강할 수 있으나 Sensor Noise, Material, Lighting, Contact와 Human 행동의 Domain Gap을 실제 Data로 확인해야 한다.
19. Robot Planning은 Task·Motion·Trajectory 계획으로 목표와 제약을 결정하고 저수준 Control은 계획을 추종하므로 두 계층의 책임과 Interface를 구분한다.
20. Closed-loop AI는 인식과 추론 결과를 Control Action으로 적용하고 물리결과를 다시 관측하므로 Model 오류, Delay와 Actuator 제한이 누적되는 Feedback Risk를 검토한다.
21. Edge AI와 On-device AI는 Latency, 대역폭과 연결의존성을 줄일 수 있으나 Resource, Thermal, Version, Cybersecurity와 중앙 Monitoring 책임을 제거하지 않는다.
22. Physical AI의 Loop는 Sensing, 전처리, Inference, Planning, 통신과 Actuation 지연을 합한 End-to-end Latency와 Jitter가 Control Deadline을 만족해야 한다.
23. Autonomous Manufacturing은 상태인식, 계획, 실행, 품질확인과 재계획을 연결하되 생산목표보다 Safety Constraint와 승인된 운영범위를 우선한다.
24. Human–Robot Collaboration은 작업분담, 접근감지, 속도·힘 제한, 정지·복구, 의도전달, Ergonomics와 비정상상황의 인간행동을 포함한다.
25. Safety Envelope은 위치, 속도, 힘, 거리, 공정상태와 금지영역의 허용범위를 정의하고 AI 명령보다 우선하는 독립 Constraint로 집행한다.
26. Sensor, Model, Network 또는 Actuator 이상 시 Safe State, Fallback과 Degraded Mode를 위험분석으로 정의하고 전환조건과 복구조건을 검증한다.
27. Supervisory Control은 AI 명령의 권한, 한계, 상태와 이상을 감시하며 Human Override는 접근성, 우선권, 표시, 기록과 안전한 복구를 포함해야 한다.
28. AI Model의 Accuracy와 Robot Functional Safety는 서로 다른 증거이며 Safety Function은 위험분석, 독립성, 진단, 검증과 Lifecycle 관리로 입증한다.
29. Physical AI는 속도, Payload, 조도, 바닥, 작업물, 사람행동과 Network 조건을 포함한 승인 운영범위를 정의하고 경계·희귀·고장 Scenario를 검증해야 한다.
30. 배포 후에는 Sensor Health, Calibration, Localization Confidence, Twin Error, Latency, Intervention과 Near-miss를 Monitoring하고 Model·Map·Tool·Safety Parameter 변경을 통제한다.

## 필수 수식·지표

### 좌표계 변환

\[
{}^{A}\mathbf{p}
=
{}^{A}\mathbf{R}_{B}\,{}^{B}\mathbf{p}
+
{}^{A}\mathbf{t}_{B}
\]

- Sensor \(B\) 좌표의 점을 공통 Frame \(A\)로 변환한다.
- 회전행렬과 이동벡터의 Calibration 오차를 관리한다.

### 독립 Scalar 측정의 분산 가중 Fusion

\[
\hat{x}
=
\frac{\sum_{i=1}^{n}w_i x_i}
{\sum_{i=1}^{n}w_i},
\qquad
w_i=\frac{1}{\sigma_i^2}
\]

\[
\sigma_{\hat{x}}^2
=
\frac{1}{\sum_{i=1}^{n}w_i}
\]

- Unbiased, 독립 Gaussian 오차라는 제한적 가정이다.
- Bias, 상관과 공통원인이 있으면 그대로 적용하지 않는다.

### Kalman Filter의 핵심 관계

\[
\hat{\mathbf{x}}_{k}^{-}
=
\mathbf{F}\hat{\mathbf{x}}_{k-1}
+
\mathbf{B}\mathbf{u}_{k}
\]

\[
\mathbf{P}_{k}^{-}
=
\mathbf{F}\mathbf{P}_{k-1}\mathbf{F}^{T}
+
\mathbf{Q}
\]

\[
\mathbf{K}_{k}
=
\mathbf{P}_{k}^{-}\mathbf{H}^{T}
\left(
\mathbf{H}\mathbf{P}_{k}^{-}\mathbf{H}^{T}
+
\mathbf{R}
\right)^{-1}
\]

\[
\hat{\mathbf{x}}_{k}
=
\hat{\mathbf{x}}_{k}^{-}
+
\mathbf{K}_{k}
\left(
\mathbf{z}_{k}
-
\mathbf{H}\hat{\mathbf{x}}_{k}^{-}
\right)
\]

- \(\mathbf{Q}\)는 Process Noise, \(\mathbf{R}\)은 Measurement Noise Covariance다.
- Model과 Noise 가정이 실제조건과 맞는지 검증한다.

### Innovation과 이상검출

\[
\mathbf{r}_{k}
=
\mathbf{z}_{k}
-
\mathbf{H}\hat{\mathbf{x}}_{k}^{-}
\]

\[
d_k^2
=
\mathbf{r}_{k}^{T}
\mathbf{S}_{k}^{-1}
\mathbf{r}_{k}
\]

- \(d_k^2\)가 Threshold를 넘는다고 특정 Sensor 고장이 자동 확정되지는 않는다.
- Mode와 Fault Hypothesis에 따라 진단한다.

### End-to-end Loop Latency

\[
T_{\mathrm{loop}}
=
T_{\mathrm{sense}}
+
T_{\mathrm{pre}}
+
T_{\mathrm{infer}}
+
T_{\mathrm{plan}}
+
T_{\mathrm{comm}}
+
T_{\mathrm{act}}
\le T_{\mathrm{deadline}}
\]

- 평균뿐 아니라 Worst-case와 Jitter를 평가한다.

### Digital Twin 동기화 오차

\[
e_{\mathrm{twin}}(k)
=
\left\|
\mathbf{y}_{\mathrm{physical}}(k)
-
\mathbf{y}_{\mathrm{twin}}(k)
\right\|_{\mathbf{W}}
\]

- Variable, 운전 Mode와 목적에 따라 Weight와 허용범위를 정한다.
- 낮은 동기화오차가 모든 미모델링 위험을 제거하지 않는다.

### Safety Constraint

\[
\mathbf{x}_{k}\in\mathcal{X}_{\mathrm{safe}},
\qquad
g_j(\mathbf{x}_{k},\mathbf{u}_{k})\le0
\]

- 위치, 속도, 힘, 거리와 공정제약을 Safety Envelope로 표현할 수 있다.
- 실제 Safety Function 설계와 정량한계는 위험분석 및 적용표준으로 verify-first 한다.

## Fatal 오류

1. **Digital Twin은 실제 설비와 항상 완전히 동일하므로 별도 Calibration과 Validation이 필요 없다.** → Twin은 목적과 범위가 제한된 Model이므로 Fidelity, 동기화오차, 가정과 Validation 범위를 관리한다.
2. **Sensor Fusion을 사용하면 개별 Sensor 고장과 측정오류가 자동으로 제거된다.** → Fusion은 불확실성을 결합할 뿐 고장을 자동 제거하지 않으므로 진단, Residual, 공통원인과 Fallback을 설계한다.
3. **AI Model의 Accuracy가 높으면 Robot과 자율제조의 현장 안전성이 자동으로 보장된다.** → Model 성능과 Functional Safety는 별도 증거이며 Safety Envelope, 독립감시, Safe State와 Scenario Validation이 필요하다.
4. **Edge AI를 적용하면 Network와 Cybersecurity 검토가 더 이상 필요 없다.** → Edge에서도 Update, 중앙연계, 시간동기, Device 자원, 접근통제와 Cybersecurity를 검토한다.
5. **Collaborative Robot 제품을 사용하면 Tool, Payload와 공정위험에 관계없이 사람과 안전하게 협업할 수 있다.** → 실제 협업 Application 전체의 위험과 보호조치를 평가해야 한다.
6. **Camera 한 대가 정상 동작하면 모든 조도, 가림과 반사조건에서 작업자와 장애물을 확실히 검출한다.** → 환경조건, Occlusion, Blind Spot, Diagnostic와 보완 Sensor를 운영범위에 맞게 검증한다.
7. **Sensor Fusion에서는 Timestamp와 좌표계 Calibration이 달라도 Algorithm이 자동 보정하므로 영향이 없다.** → 시간정렬과 좌표계 오차는 상태추정을 왜곡하므로 동기화, Calibration과 Drift Monitoring이 필요하다.
8. **SLAM이 정확히 동작하면 충돌회피와 Functional Safety가 자동으로 인증된다.** → SLAM은 Localization·Mapping 기능이며 안전정지와 충돌방지는 독립된 위험통제와 검증이 필요하다.
9. **Simulation에서 모든 시험이 통과하면 실제 설비 Validation은 생략할 수 있다.** → Simulation Coverage와 Model Gap을 분석하고 실제 설비와 단계적 현장시험으로 확인한다.
10. **Synthetic Data가 충분하면 실제 Sensor와 현장 Data는 필요 없다.** → Synthetic Data는 보강수단이며 Domain Gap과 실제 분포를 현장 Data로 확인한다.
11. **AI Planner가 생성한 명령은 별도 Safety Constraint나 Supervisory Control 없이 Actuator에 직접 적용해도 된다.** → 명령은 독립 Safety Envelope, 권한검사, Interlock와 Fallback을 거쳐야 한다.
12. **AI가 실시간으로 재계획하므로 Sensor나 Model 장애 시 Safe State와 Fallback이 필요 없다.** → 재계획 실패와 불확실성을 고려해 위험분석 기반 Safe State, Degraded Mode와 복구조건을 정의한다.
13. **자율제조 시스템은 사람이 개입하면 성능이 낮아지므로 Human Override와 비상개입을 제거해야 한다.** → 권한과 위험도에 맞는 Human Override, Emergency Action, 표시와 안전한 복구를 제공한다.
14. **On-device AI는 Network를 거치지 않으므로 Latency가 0이고 실행시간이 항상 결정적이다.** → Inference, Preprocessing, Scheduling, Thermal Throttling과 Actuation 지연·Jitter를 측정한다.
15. **Sensor를 여러 개 설치하면 공통원인고장은 자동으로 제거된다.** → 공통전원, 환경, 위치, Algorithm과 Calibration의 종속성을 분석하고 다양성·분리·진단을 적용한다.
16. **Physical AI는 현장에서 계속 학습할수록 좋아지므로 Model과 Safety Parameter를 승인 없이 Online 변경해도 된다.** → Online Learning과 Parameter 변경은 운영범위, 검증, 승인, Rollback과 변경관리 대상이다.

## Warn 기준

1. Physical AI를 일반 AI 분석과 구분하지 않고 Sensor–Actuator Feedback을 누락함 → 물리환경 인식, Action, Feedback과 Runtime Risk를 연결한다.
2. Sensor를 결합한다고만 설명하고 Bias, Covariance, Time Alignment와 Calibration이 없음 → 불확실성과 시간·좌표 정렬을 Fusion의 전제로 제시한다.
3. Redundancy를 제시하지만 공통원인, Residual과 Plausibility 진단이 없음 → 공유자원과 공통환경을 평가하고 고장격리·Fallback을 설계한다.
4. SLAM과 Collision Avoidance 또는 Safety Function을 동일시함 → Localization·Mapping과 독립 Safety Control을 분리한다.
5. Digital Twin을 설명하지만 Model 범위, Fidelity, 동기화와 Staleness가 없음 → 목적·가정·Validation·Version과 Synchronization 지표를 제시한다.
6. Simulation·Synthetic Data를 사용하지만 Scenario Coverage와 Domain Gap 검토가 없음 → 경계·희귀·고장 Scenario와 실제 Data 비교를 포함한다.
7. Planning과 저수준 Control을 혼용하고 제약 Interface가 불명확함 → Task·Motion·Trajectory 계획과 Control Tracking 책임을 구분한다.
8. 실시간 동작을 언급하지만 End-to-end Latency, Jitter와 Deadline이 없음 → Sensing부터 Actuation까지 지연예산을 측정한다.
9. AI 명령을 적용하면서 위치·속도·힘·거리 제한과 독립 집행계층이 없음 → Safety Envelope과 권한검사, Safe State를 AI보다 우선시한다.
10. Fallback을 언급하지만 전환 Trigger, Degraded Mode와 복구검증이 없음 → 장애별 전환·정지·복구조건과 책임을 정의한다.
11. 협업을 Sensor 감지만으로 설명하고 작업분담, 표시, 예측가능성과 Human 행동이 없음 → Human Factors, Override, Training과 비정상상황을 포함한다.
12. AI Model Lifecycle, Physical Closed-loop와 Functional Safety Lifecycle을 혼용함 → SW-12는 Model 분석, SW-13은 물리상호작용, SW-05는 Safety Software Lifecycle로 구분한다.

## False Positive 기준

1. Sensor Fusion은 독립적이고 적절히 Calibration된 Sensor의 추정오차를 줄일 수 있으나 고장제거를 자동 보장하지 않는다.
2. Camera 중심 Perception은 승인된 조도와 시야조건에서 사용할 수 있으나 Blind Spot과 환경변화를 검증한다.
3. Collaborative Robot은 협업기능을 제공할 수 있으나 실제 Application Risk Assessment를 대체하지 않는다.
4. Digital Twin은 목적에 충분한 Fidelity를 가질 수 있으나 모든 물리현상을 동일하게 재현할 필요는 없다.
5. Simulation은 실제시험을 줄이고 위험 Scenario를 탐색할 수 있으나 현장 Validation을 전부 대체하지 않는다.
6. Synthetic Data는 희귀 Event를 보강할 수 있으나 실제 Sensor 분포와 Domain Gap을 확인한다.
7. SLAM은 Localization과 Mapping의 유효한 방법이지만 독립 Safety Function으로 자동 간주하지 않는다.
8. Edge AI는 Latency와 연결의존성을 줄일 수 있으나 Device 관리, Update와 Cybersecurity가 필요하다.
9. On-device 처리는 Network 장애 시 일부 기능을 유지할 수 있으나 Resource와 Thermal 제한을 평가한다.
10. AI Planner 출력은 Recommendation 또는 제한적 자동명령으로 사용할 수 있으며 권한과 Safety Constraint를 별도로 둔다.
11. Degraded Mode는 즉시정지보다 안전하고 합리적일 수 있으나 위험분석과 허용조건을 명시한다.
12. Human Override는 항상 수동운전만을 뜻하지 않고 위험도에 따른 승인·개입·정지권한을 의미할 수 있다.
13. Online Adaptation은 제한된 Parameter에 사용할 수 있으나 검증범위, Monitor와 Rollback을 둔다.
14. World Model은 불확실한 환경표현이며 Ground Truth와 동일하다고 가정하지 않는다.
15. Digital Twin Error는 단일 Threshold로 관리할 수 있으나 Variable, Mode와 안전영향에 따라 기준을 달리할 수 있다.
16. Functional Safety와 AI 성능은 연계해 평가할 수 있으나 어느 한쪽이 다른 쪽의 증거를 자동 대체하지 않는다.


## Model Answer

Physical AI는 AI의 인식과 계획 결과가 Robot·설비의 Actuator에 적용되고 물리결과를 다시 Sensor로 관측하는 폐루프 시스템이다. 따라서 Offline Model Accuracy만이 아니라 Sensor, Controller, Actuator, Tool, Payload, 작업공간과 사람을 포함한 System Boundary를 평가해야 한다.

Perception 단계에서는 Camera, LiDAR, Radar, Encoder와 Force·Torque Sensor의 측정특성을 상호 보완적으로 사용한다. Fusion 전에 Timestamp, Clock, Sample Rate와 Transport Delay를 정렬하고 Intrinsic·Extrinsic Calibration으로 공통 좌표계에 변환한다. 각 Sensor의 Bias와 Covariance를 반영해 상태와 불확실성을 추정한다. Sensor를 여러 개 사용해도 공통전원, 동일시야, 환경조건과 공통 Algorithm의 고장은 남으므로 Residual과 Plausibility 진단, Fallback이 필요하다.

State Estimation은 직접 측정하기 어려운 위치, 속도, 자세와 외력을 추정한다. Localization은 기준좌표계의 Pose를 구하고 SLAM은 Localization과 Mapping을 동시에 수행한다. 그러나 SLAM 성능이 충돌회피나 Functional Safety를 자동 보장하지 않는다. World Model은 객체, 자유공간과 불확실성을 Planning에 제공한다.

Digital Twin은 실제 자산의 모든 현상을 동일하게 복제하는 것이 아니라 특정 목적과 범위의 Model이다. 따라서 Fidelity, Boundary Condition, Parameter, Version, Timestamp와 실제 설비와의 Synchronization Error를 관리한다. Simulation과 Synthetic Data는 위험 Scenario와 희귀상황을 시험하는 데 유용하지만 Model Gap과 Domain Gap을 실제 Data와 현장시험으로 확인해야 한다.

Robot Planning은 Task, Motion과 Trajectory를 결정하고 저수준 Control은 계획을 추종한다. Closed-loop AI에서는 Perception 오류와 Delay가 Feedback을 통해 누적될 수 있다. Sensing, 전처리, Inference, Planning, 통신과 Actuation의 End-to-end Latency와 Jitter가 Control Deadline을 만족해야 한다. Edge AI는 지연과 연결의존성을 낮출 수 있지만 Resource, Thermal, Version, Network와 Cybersecurity 검토를 제거하지 않는다.

자율제조와 Human–Robot Collaboration은 생산목표보다 Safety Constraint를 우선한다. Collaborative Robot 제품을 사용하더라도 Tool, Payload, 속도, 힘, 작업공간과 공정위험을 포함한 Application Risk를 평가한다. 위치, 속도, 힘, 거리와 금지영역의 Safety Envelope은 AI 명령보다 우선하는 독립계층에서 집행한다.

Sensor, Model, Network나 Actuator 이상 시 위험분석에 따른 Safe State, Fallback과 Degraded Mode로 전환한다. Supervisory Control은 AI 권한과 상태를 감시하고 Human Override의 우선권, 표시, 기록과 안전한 복구를 제공한다. AI Accuracy와 Functional Safety는 다른 증거이므로 독립 Safety Function과 Scenario Validation이 필요하다.

마지막으로 승인 운영범위의 정상·경계·희귀·고장 Scenario를 검증하고, 배포 후 Sensor Health, Calibration, Localization Confidence, Twin Error, Latency, Intervention과 Near-miss를 Monitoring한다. Model, Map, Tool과 Safety Parameter 변경은 영향분석, Regression, 승인과 Rollback으로 관리한다.

## Topic Importance

- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- 고득점 조건:
  1. Physical AI를 Sensor–Actuator Feedback 폐루프로 정의한다.
  2. Robot System Boundary에 Tool, Payload, Cell과 Safety 기능을 포함한다.
  3. Sensor Fusion의 Time Alignment, Calibration, Covariance와 공통원인을 설명한다.
  4. State Estimation, Localization, SLAM, Observability와 World Model을 구분한다.
  5. Digital Twin의 목적, Fidelity, Synchronization, Version과 Staleness를 설명한다.
  6. Simulation Coverage와 Synthetic Data Domain Gap을 설명한다.
  7. Planning과 Control 계층 및 End-to-end Latency를 설명한다.
  8. Collaborative Robot 제품과 협업 Application 안전성을 구분한다.
  9. Safety Envelope, Safe State, Fallback과 Degraded Mode를 설명한다.
  10. Supervisory Control과 Human Override를 설명한다.
  11. AI Accuracy와 Functional Safety 증거를 분리한다.
  12. 운영범위, Scenario Validation, Runtime Monitoring과 Change Control을 연결한다.

## Routing Alias

1. `physical AI robot closed loop safety control`
2. `industrial robot sensor fusion state estimation`
3. `collaborative robot human robot safety application`
4. `camera LiDAR radar encoder sensor fusion`
5. `robot localization SLAM world model`
6. `digital twin fidelity synchronization validation`
7. `simulation synthetic data domain gap robot`
8. `robot planning trajectory supervisory control`
9. `autonomous manufacturing safety envelope fallback`
10. `edge AI on-device latency control deadline`
11. `human robot collaboration safe state override`
12. `functional safety AI model physical system`
13. `sensor calibration coordinate frame observability`
14. `closed-loop AI runtime monitoring change control`


Broad Alias로 단독 사용하지 않는 표현:

```text
Physical AI
Robot
Sensor
Fusion
Digital Twin
SLAM
Safety
Edge AI
Autonomous
Planning
```

## Question Examples

### Positive

1. Physical AI의 개념과 산업 Robot Closed-loop 구조를 설명하시오.
2. Camera·LiDAR·Radar·Encoder·Force Sensor의 Sensor Fusion 방안을 설명하시오.
3. Robot State Estimation, Localization과 SLAM의 관계를 설명하시오.
4. Digital Twin의 구성, Fidelity, 동기화와 Validation 방안을 설명하시오.
5. Robot Simulation과 Synthetic Data의 활용 및 Domain Gap 관리방안을 설명하시오.
6. Robot Planning, Control과 Safety Envelope의 관계를 설명하시오.
7. Edge AI·On-device AI의 장점과 Physical Control 적용 한계를 설명하시오.
8. 자율제조에서 Safe State, Fallback, Supervisory Control과 Human Override를 설명하시오.
9. Collaborative Robot과 Human–Robot Collaboration의 안전설계 방안을 설명하시오.
10. Physical AI의 운영범위, Scenario Validation과 Runtime Monitoring을 설명하시오.

### Negative Boundary

1. 산업 AI Model의 Train·Validation·Test와 Data Leakage를 설명하시오. → SW-12
2. 예지보전 Model의 Precision, Recall, Drift와 Retraining을 설명하시오. → SW-12
3. Historian, MES, Timestamp와 Batch Genealogy를 설명하시오. → SW-11
4. SIS Safety Application Program의 SIL, 독립성과 Verification을 설명하시오. → SW-05
5. OPC UA와 MQTT Protocol의 상호운용성을 설명하시오. → SW-07
6. PLC Sequence, Interlock, Trip과 Fail-safe Logic을 설명하시오. → SW-02
7. 일반 Software V-Model과 Configuration Management를 설명하시오. → SW-04
8. Robot 제어망의 QoS, Redundancy와 장애복구 성능을 설명하시오. → SW-08


## Focused Regression

1. Source 6개와 Focused Test 1개 존재
2. JSON 4개 Parsing
3. Topic ID와 Modern Root Schema 일치
4. Anchor 30개
5. Fatal 16개
6. Major 12개
7. Physical AI와 Robot System Boundary
8. Sensor Fusion Time·Calibration·Uncertainty·Common Cause
9. State Estimation·Localization·SLAM·World Model
10. Digital Twin Fidelity·Synchronization
11. Simulation·Synthetic Data Domain Gap
12. Planning·Closed-loop·Edge AI·Latency
13. Safety Envelope·Safe State·Fallback·Override
14. Functional Safety와 AI Accuracy 분리
15. SW-05·SW-11·SW-12·SW-13 경계
16. Generated/Production 수정 금지

## 생성 파일

```text
docs/topic_sheets/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control.md
rubrics/topic_packs/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control/README.md
rubrics/topic_packs/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control/fact_anchor.json
rubrics/topic_packs/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control/logic_check.json
rubrics/topic_packs/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control/model_answer.json
rubrics/topic_packs/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control/topic_importance.json
scripts/test_physical_ai_robot_sensor_fusion_safety_topic.py
```

## Lane 완료 후 검증 및 Push

SW-13 Topic 커밋 후 다음을 수행한다.

1. SW-05, SW-11, SW-12, SW-13 source와 focused test 존재
2. 네 focused test 통과
3. 네 Topic 커밋 분리와 Commit Subject 확인
4. Working Tree Clean
5. `rubrics/generated/**` 변경 없음
6. Lane A/B와 기존 Topic 파일 변경 없음
7. 원격 Lane C 브랜치가 Local HEAD의 조상인지 확인
8. `origin/software/lane-c-safety-data-ai`로 Fast-forward Push 1회
9. `main` 직접 Push 금지

## Verify-first

- 적용 Robot·Functional Safety 표준과 Edition
- 협업 Application의 Force, Speed, Separation 한계
- Sensor Diagnostic Coverage와 Common Cause 가정
- Localization Confidence와 Residual Threshold
- Twin Fidelity·Synchronization 허용기준
- Worst-case Latency·Jitter와 Control Deadline
- Safe State·Degraded Mode·Human Override 권한
- Online Adaptation과 Change Approval 조건
