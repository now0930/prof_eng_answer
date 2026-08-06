# 산업 AI·Machine Learning, 이상탐지, 예지보전 및 모델 수명주기

## Topic ID

`industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle`

## Lane

`SOFTWARE_LLM_LANE_C`

## Question type

`PRINCIPLE_INTERPRETATION`

## Scope

- AI·Machine Learning·Deep Learning
- Supervised·Unsupervised Learning
- Classification·Regression·Forecasting·Anomaly Detection
- Predictive Maintenance와 Remaining Useful Life
- Feature Engineering, Training·Validation·Test와 Data Leakage
- Class Imbalance, Precision·Recall·F1과 False Alarm
- Deployment, Monitoring, Drift와 Retraining
- Explainability, Human Review, Model Registry와 MLOps

## Ownership Boundary

- SW-11: 데이터 수집·품질·시간·Context·Historian·MES 기반
- SW-12: 데이터 기반 학습·추론, 평가와 Model Lifecycle
- SW-13: Robot·Sensor Fusion·Digital Twin·Closed-loop AI와 안전제어
- SW-04: 일반 Software SDLC

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

산업 AI·Machine Learning의 유형과 이상탐지·예지보전 적용방안을 설명하고, Data Leakage·불균형·성능지표·Drift·Retraining을 포함한 Model Lifecycle 관리방안을 제시하시오.

## Fatal Guard

- 높은 Accuracy는 현장 안전성이나 정비효과를 자동 보장하지 않는다.
- Train·Test 중복과 미래정보 Leakage를 허용하지 않는다.
- 불균형 고장데이터를 Accuracy 하나로 평가하지 않는다.
- Anomaly Score를 특정 고장의 확정진단으로 단정하지 않는다.
- 예지보전은 모든 고장을 제거하지 않으며 RUL은 불확실한 추정치다.
- Retraining, Explainability와 MLOps 자동화는 현장 Validation을 대체하지 않는다.
- AI 출력을 제약과 승인 없이 폐루프 제어에 직접 적용하지 않는다.

## Verify-first

정량 Threshold, Drift Trigger, RUL 신뢰구간, 현장 오류비용, 적용 표준과 Closed-loop 안전조건은 프로젝트 데이터와 승인기준으로 확인한다.
