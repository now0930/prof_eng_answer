# 산업 AI·Machine Learning, 이상탐지, 예지보전 및 모델 수명주기

## Topic

- SW 번호: `SW-12`
- Topic ID: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle`
- 한글 주제: 산업 AI·Machine Learning, 이상탐지, 예지보전 및 모델 수명주기
- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`

## 범위

포함 범위:

1. AI·Machine Learning·Deep Learning의 포함관계
2. Supervised·Unsupervised Learning
3. Classification, Regression, Forecasting과 Anomaly Detection
4. Predictive Maintenance와 Remaining Useful Life
5. Process Optimization과 Recommendation
6. Feature Engineering과 산업 시계열 Context
7. Training·Validation·Test 분리와 Data Leakage
8. Class Imbalance와 Precision·Recall·F1
9. False Alarm, 미검출, Threshold와 Lead Time
10. Deployment, Monitoring, Drift와 Retraining
11. Explainability, Human Review와 Fallback
12. Model Version, Registry, Rollback과 MLOps

## 제외 범위

- Historian, MES, ERP, Timestamp, Quality Code, Metadata와 Batch Genealogy 상세
- Robot, Camera·LiDAR·Radar Sensor Fusion, SLAM과 Physical AI
- AI 출력의 실제 Actuator 폐루프 적용, Robot Planning과 Functional Safety 상세
- 통신 Protocol Frame, QoS와 Wire-level 상호운용
- 일반 Software SDLC와 범용 Unit Test 상세
- Generated Bank, 공통 Router, Production Python과 공통 Release Script 수정

## 인접 Topic Ownership

### SW-11과의 경계

SW-11이 소유하는 내용:

- 산업데이터의 수집, Timestamp, Quality Code, Context와 저장
- Historian, MES, ERP, ISA-95, Metadata와 Governance
- Traceability와 Batch Genealogy

SW-12가 소유하는 내용:

- 해당 데이터를 이용하는 Feature, Training, Validation과 Inference
- Anomaly Detection, Predictive Maintenance와 RUL
- Model Metric, Drift, Retraining, Monitoring과 MLOps

### SW-13과의 경계

SW-12가 소유하는 내용:

- 데이터 기반 분석·예측 Model
- Model의 Recommendation, 평가와 Lifecycle

SW-13이 소유하는 내용:

- AI가 Robot·설비와 물리적으로 상호작용하는 Closed-loop AI
- Sensor Fusion, Localization, Planning과 Digital Twin
- Safe State, Fallback, Envelope, Supervisory Control과 Human Override

### SW-04와의 경계

- SW-04는 일반 제어 Software 요구·설계·Coding·Test와 Configuration Management를 소유한다.
- SW-12는 Data·Feature·Model의 실험, 검증, 배포와 운영 Monitoring이 반복되는 Model Lifecycle을 소유한다.

## 대표 문제

> 산업 AI·Machine Learning의 유형과 이상탐지·예지보전 적용방안을 설명하고, Data Leakage·불균형·성능지표·Drift·Retraining을 포함한 Model Lifecycle 관리방안을 제시하시오.

## 핵심 Fact

1. AI는 지능적 과업을 수행하는 기술의 상위 개념이고 Machine Learning은 데이터에서 패턴을 학습하는 AI의 부분집합이며 Deep Learning은 다층 신경망을 사용하는 Machine Learning의 부분집합이다.
2. Supervised Learning은 입력과 정답 Label의 관계를 학습하며 Classification, Regression과 일부 Forecasting 문제에 사용한다.
3. Unsupervised Learning은 정답 Label 없이 구조, 군집 또는 정상 패턴을 학습할 수 있으나 결과의 현장 타당성 검토와 별도 평가가 필요하다.
4. Classification은 범주를, Regression은 연속값을, Forecasting은 미래 시계열을 예측하므로 목표변수와 의사결정 방식에 맞게 문제를 정의해야 한다.
5. Anomaly Detection은 정상에서 벗어난 정도를 Score로 산출하고 Threshold로 경보를 결정하며 높은 Score가 특정 고장원인의 확정을 의미하지 않는다.
6. Predictive Maintenance는 상태데이터를 이용해 고장 가능성, 열화상태 또는 정비시점을 추정하여 계획정비를 지원하지만 모든 고장을 제거하지 않는다.
7. Remaining Useful Life는 현재 상태에서 정의된 고장기준까지 남은 시간 또는 Cycle의 추정치이며 불확실성, 신뢰구간과 적용조건을 함께 제시해야 한다.
8. Process Optimization Model은 품질, 생산량, 에너지와 제약조건의 Trade-off를 지원하며 제어출력 적용 전 안전범위, 제약, 승인과 Supervisory Control을 분리해야 한다.
9. Feature Engineering은 원시데이터를 공정지식과 시간 Context에 맞는 통계량, 변화율, Window, 주파수 또는 상태특징으로 변환하며 미래정보를 포함해서는 안 된다.
10. Training Data는 정상·고장·운전모드·제품·계절·정비상태와 Sensor 품질을 대표해야 하며 수집 편향과 Label 품질을 기록해야 한다.
11. Training Set은 Parameter 학습에, Validation Set은 Model과 Hyperparameter 선택에, Test Set은 최종 일반화 성능 확인에 사용하며 역할을 분리한다.
12. 산업 시계열은 시간순 분할과 설비·Batch·제품 단위 Group 분할을 적용하여 동일 Episode와 미래정보가 Train과 Test에 섞이지 않게 해야 한다.
13. Data Leakage는 예측시점에 사용할 수 없는 미래정보, Target 파생정보 또는 동일 사건의 중복표본이 학습에 유입되어 성능을 과대평가하는 현상이다.
14. 고장과 이상 Event가 희소한 Class Imbalance 문제에서는 Accuracy만으로 성능을 판단하지 말고 Sampling, Class Weight, Precision, Recall과 PR 관점으로 평가한다.
15. Binary Classification은 TP, FP, TN, FN의 Confusion Matrix로 결과를 구분하여 오경보와 미검출을 별도로 해석해야 한다.
16. Precision은 모델이 Positive로 판정한 사례 중 실제 Positive의 비율이며 오경보가 많은 경우 낮아진다.
17. Recall은 실제 Positive 중 모델이 검출한 비율이며 위험 고장의 미검출이 중요한 경우 핵심 지표가 된다.
18. F1 Score는 Precision과 Recall의 조화평균으로 두 지표의 균형을 요약하지만 비용과 운전조건을 단독으로 대체하지 않는다.
19. Threshold를 낮추면 일반적으로 Recall은 증가하고 False Alarm도 증가할 수 있으므로 미검출 비용, 확인인력과 정비부하를 함께 최적화한다.
20. 현장 성과는 Model Metric뿐 아니라 경보 Lead Time, 확인 소요, 정비 Action 가능성, Downtime과 오경보 비용으로 평가해야 한다.
21. 예측확률은 Calibration을 확인해야 하며 Confidence 또는 Probability가 실제 발생빈도와 일치하지 않으면 Threshold와 Risk 판단이 왜곡될 수 있다.
22. Deployment 시 Training 환경과 현장 Runtime의 Sensor, 전처리, Library, Hardware, Latency와 입력 Schema 차이를 검증해야 한다.
23. Model, Dataset, Feature, Code, Hyperparameter, Threshold와 배포환경의 Version을 연결하여 결과 재현, Rollback과 Audit이 가능해야 한다.
24. 운영 중에는 입력 품질, Missing, Range, Latency, Prediction 분포, 성능, False Alarm, 사용자 조치와 System Health를 지속 Monitoring한다.
25. Data Drift는 입력분포 변화, Concept Drift는 입력과 Target 관계 변화이며 운전모드·제품·Sensor·정비정책 변화와 구분해 진단한다.
26. Retraining은 일정주기만이 아니라 성능저하, Drift, 공정변경, Label 축적과 위험기준에 따른 Trigger로 수행하고 승인된 Data Window를 사용한다.
27. 새 Model은 기존 Champion과 동일 Test Set·현장 Replay·Stress Scenario로 비교하고 성능, 안정성, Latency와 운영비용의 Regression을 확인한다.
28. Explainability는 입력과 예측의 관계를 해석하는 보조수단이며 설명 가능성이 인과성, 정확성 또는 안전성을 자동 증명하지 않는다.
29. 고위험 경보와 정비의사결정에는 Human Review, 확인절차, 불확실성 표시, Model 장애 시 Fallback과 Override 책임을 정의한다.
30. MLOps는 Data·Feature·Model·Code의 Version, 자동화된 Test, Registry, Deployment, Monitoring, Approval, Rollback과 재학습을 연결하는 Model Lifecycle 운영체계다.

## 필수 수식·지표

### Precision

\[
\mathrm{Precision}=
\frac{TP}{TP+FP}
\]

- 경보로 판정한 사례 중 실제 Positive의 비율이다.
- False Alarm이 늘면 낮아진다.

### Recall

\[
\mathrm{Recall}=
\frac{TP}{TP+FN}
\]

- 실제 Positive 중 검출한 비율이다.
- 위험 고장의 미검출 비용이 큰 경우 중요하다.

### F1 Score

\[
F_1=
2\frac{\mathrm{Precision}\cdot\mathrm{Recall}}
{\mathrm{Precision}+\mathrm{Recall}}
\]

- Precision과 Recall의 조화평균이다.
- 업무비용과 Lead Time을 단독 대체하지 않는다.

### False Positive Rate

\[
FPR=
\frac{FP}{FP+TN}
\]

- 정상기간이 매우 긴 산업데이터에서는 낮은 FPR도 많은 경보를 만들 수 있다.
- 시간당·일당 False Alarm 수를 함께 평가한다.

### Regression Error

\[
MAE=
\frac{1}{n}\sum_{i=1}^{n}|y_i-\hat y_i|
\]

\[
RMSE=
\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2}
\]

- RUL과 Forecasting에서는 평균오차뿐 아니라 조기·지연 예측의 비대칭 비용을 함께 본다.

### Calibration Error의 단순 개념

\[
ECE=
\sum_{m=1}^{M}
\frac{|B_m|}{n}
\left|
\mathrm{acc}(B_m)-\mathrm{conf}(B_m)
\right|
\]

- Bin 구성과 표본 수에 민감하므로 구현조건을 명시한다.
- 낮은 Calibration Error가 안전성을 자동 보장하지 않는다.

### 현장 의사결정 기대비용

\[
J(\tau)=
C_{FP}N_{FP}(\tau)+
C_{FN}N_{FN}(\tau)+
C_{A}N_{A}(\tau)
\]

- \(\tau\)는 경보 Threshold다.
- \(C_{FP}\), \(C_{FN}\), \(C_A\)는 오경보, 미검출과 확인·정비 Action 비용이다.
- 비용은 현장 Risk와 정비정책으로 verify-first 한다.

## Fatal 오류

1. **AI 모델의 Accuracy가 높으면 현장 안전성과 정비효과가 자동으로 보장된다.** → Model Metric과 현장 Risk, 미검출·오경보 비용, 운전범위, Human Review와 안전제어를 별도로 검증한다.
2. **Training과 Test에 같은 데이터나 같은 고장 Episode를 사용해도 일반화 성능을 정확히 평가할 수 있다.** → Training·Validation·Test 역할을 분리하고 시간·설비·Episode 단위 누수를 차단한다.
3. **예측시점 이후의 값이나 정비결과를 Feature에 포함하면 모델이 더 정확해지므로 허용된다.** → 운영 시점에 이용 가능한 정보만 Feature로 사용하고 미래·Target Leakage를 제거한다.
4. **고장 데이터가 희소해도 Accuracy 하나가 높으면 이상탐지 모델이 우수하다.** → 불균형 데이터에서는 Confusion Matrix, Precision, Recall, F1, PR와 비용을 함께 평가한다.
5. **Anomaly Score가 높으면 특정 부품 고장이 확정되므로 추가 진단이 필요 없다.** → Anomaly Score는 정상 이탈 신호이며 원인진단, Context와 Human Review를 별도로 수행한다.
6. **예지보전 모델을 도입하면 설비 고장과 비계획정지가 더 이상 발생하지 않는다.** → 예지보전은 위험을 줄이고 계획정비를 지원하지만 미관측 고장과 불확실성을 제거하지 않는다.
7. **RUL 예측값은 설비가 실제로 고장날 정확한 날짜이므로 불확실성 표시가 필요 없다.** → RUL은 정의된 고장기준과 조건에 따른 추정치이며 오차, 신뢰구간과 적용범위를 제시한다.
8. **Threshold를 낮추면 Recall만 높아지고 False Alarm이나 정비부하는 증가하지 않는다.** → Threshold 변경은 Recall, Precision, False Alarm, 미검출과 운영비용 사이의 Trade-off를 만든다.
9. **Unsupervised Learning은 Label을 사용하지 않으므로 Validation과 현장 검토가 필요 없다.** → Label이 없더라도 정상성, 군집 의미, 경보 유효성, 안정성과 현장 Action 가능성을 검증한다.
10. **최신 데이터로 Retraining하면 새 Model은 항상 기존 Model보다 좋아지므로 Regression Test가 필요 없다.** → Champion–Challenger 비교, 고정 Test, Replay, Stress Test와 승인 후 교체를 수행한다.
11. **배포 시 성능이 확인되면 공정과 데이터가 변해도 Model Monitoring은 필요 없다.** → Data·Concept Drift, 입력품질, 성능, Latency와 운영지표를 지속 Monitoring한다.
12. **설명가능성 도구가 중요 Feature를 표시하면 그 Feature가 고장의 인과원인임이 증명된다.** → Feature Attribution은 예측관계를 설명할 뿐 인과성은 실험, 공정지식과 별도 검증이 필요하다.
13. **Training Notebook에서 동작한 Model은 현장 Deployment에서도 동일하므로 Runtime 검증과 Rollback이 필요 없다.** → Training–Serving 차이, 전처리, Schema, Latency, 자원, Failure Mode와 Rollback을 검증한다.
14. **Model 파일만 보관하면 Dataset, Feature, Threshold와 Code Version은 기록하지 않아도 결과를 재현할 수 있다.** → Model과 Data·Feature·Code·Parameter·Threshold·환경 Version을 함께 추적한다.
15. **공정최적화 AI의 출력은 Accuracy가 높으면 안전제약과 운영자 승인 없이 제어기에 직접 적용해도 된다.** → 폐루프 적용은 SW-13 영역이며 안전범위, Supervisory Control, Fallback, Human Override와 별도 검증이 필요하다.
16. **MLOps CI/CD가 성공하면 Model의 현장 적합성, 기능안전과 정비효과가 자동으로 보장된다.** → 자동화 Pipeline은 증거 생성수단이며 현장 Validation, Risk 검토, 승인과 운영 Monitoring을 대체하지 않는다.

## Warn 기준

1. Classification, Regression, Forecasting과 Anomaly Detection을 나열하지만 목표변수와 의사결정 연결이 불명확함 → 예측대상, Horizon, 출력단위, Action과 실패비용을 함께 정의한다.
2. Train·Validation·Test를 언급하지만 시간순·설비·Episode 분할이 없음 → 산업 시계열의 시간·Group Leakage 방지전략을 제시한다.
3. 높은 성능을 제시하지만 미래정보, Target 파생값과 중복 Episode의 Leakage 검토가 없음 → Feature 가용시점과 Data Lineage를 기준으로 Leakage를 점검한다.
4. 희소 고장 문제에서 Accuracy만 제시하거나 Class 분포를 누락함 → Confusion Matrix, Precision, Recall, F1과 PR 기준을 함께 제시한다.
5. Threshold를 제시하지만 False Alarm, 미검출, Lead Time과 정비부하의 Trade-off가 없음 → 업무비용과 Action 가능성을 기준으로 Threshold를 선정한다.
6. RUL Point Estimate만 제시하고 고장기준, 오차와 불확실성이 없음 → Failure Threshold, Horizon, 신뢰구간과 적용조건을 명시한다.
7. Model 배포를 언급하지만 전처리·Schema·Library·Latency 차이 검증이 없음 → Training–Serving Skew와 Runtime 제한을 시험한다.
8. 운영 Monitoring이 Accuracy 확인에만 한정되고 입력품질·Latency·분포·Action 결과가 없음 → Data, Model, System과 Business Metric을 함께 Monitoring한다.
9. Drift를 언급하지만 Data/Concept 구분, 원인분석과 대응 Trigger가 없음 → Drift 종류와 공정변경을 구분하고 Retraining·Rollback 조건을 정한다.
10. Model Version만 관리하고 Dataset·Feature·Code·Threshold 연결이 없음 → Registry와 Lineage로 재현·Audit·Rollback 범위를 완성한다.
11. Explainability를 제시하지만 인과성·정확성·안전성의 한계를 설명하지 않음 → 설명은 검토 보조수단이며 현장 지식과 Validation이 필요함을 밝힌다.
12. 데이터 기반 분석과 물리 설비 폐루프 제어를 같은 Topic으로 혼용함 → SW-11은 데이터 기반, SW-12는 Model 분석수명주기, SW-13은 물리 상호작용·안전제어로 구분한다.

## False Positive 기준

1. Accuracy는 Class가 균형이고 오류비용이 유사한 제한된 문제에서는 유효한 보조지표로 사용할 수 있다.
2. Unsupervised Anomaly Detection은 Label 부족 상황에서 사용할 수 있으나 현장 검증과 경보 품질평가가 필요하다.
3. Synthetic Data와 Simulation Data는 희귀상황 보강에 사용할 수 있으나 실제 분포 대표성과 Domain Gap을 확인한다.
4. Threshold는 고정값 또는 운전모드별 동적값으로 설계할 수 있으나 Version과 선정근거를 기록한다.
5. RUL은 Point Estimate로 제공할 수 있으나 불확실성과 사용조건을 함께 관리한다.
6. AutoML은 Model 후보 탐색을 자동화할 수 있으나 Data Leakage와 현장 Validation 책임을 제거하지 않는다.
7. Deep Learning은 Feature를 자동학습할 수 있으나 Sensor Context, Data 품질과 설명 책임이 사라지지 않는다.
8. Retraining은 일정주기로 수행할 수 있으나 Trigger, 승인, Regression과 Rollback 절차를 둔다.
9. Explainability 값은 Model 동작 검토에 유용하지만 인과관계를 단독 증명하지 않는다.
10. Precision과 Recall 중 하나를 우선할 수 있으나 업무 Risk와 Threshold Trade-off를 명시한다.
11. Label 지연이 긴 환경에서는 Proxy Metric과 후행평가를 사용할 수 있으나 최종 성능확인을 생략하지 않는다.
12. Edge Inference는 Latency와 연결성을 개선할 수 있으나 중앙 Registry, Monitoring과 Cybersecurity 검토를 대체하지 않는다.
13. Human Review는 모든 경보를 수동 승인한다는 뜻이 아니라 Risk에 따른 역할분담과 Escalation을 의미할 수 있다.
14. Model Output을 Advisory로 사용할 수 있으며 이 경우에도 사용자 Action, 오경보와 무시율을 Monitoring한다.
15. Process Optimization은 Recommendation Mode로 시작해 검증 후 제한적 자동화로 확장할 수 있다.
16. MLOps 자동화는 반복성과 추적성을 높이지만 현장 적합성 판단과 안전 승인을 자동 대체하지 않는다.


## Model Answer

산업 AI는 공정과 설비 데이터에서 상태를 진단하고 미래를 예측하여 운전과 정비 의사결정을 지원한다. AI는 상위 개념이고 Machine Learning은 데이터에서 패턴을 학습하는 부분집합이며 Deep Learning은 다층 신경망을 사용하는 Machine Learning의 부분집합이다. Supervised Learning은 Label을 이용해 Classification, Regression과 Forecasting을 수행한다. Unsupervised Learning은 정상 패턴과 군집을 학습할 수 있지만 Label이 없다는 이유로 현장 검증을 생략할 수 없다.

이상탐지는 정상에서 벗어난 정도를 Score로 산출하고 Threshold로 경보를 결정한다. 높은 Anomaly Score는 특정 고장의 확정진단이 아니다. 예지보전은 고장확률, 열화상태 또는 RUL을 추정해 계획정비를 지원한다. RUL은 정의된 고장기준까지 남은 시간의 추정치이므로 오차와 불확실성을 제시해야 한다.

데이터 단계에서는 공정지식을 이용해 Window, 변화율, 통계량과 주파수 Feature를 만들되 예측시점 이후 정보가 포함되지 않게 한다. Training, Validation과 Test의 역할을 분리한다. 산업 시계열은 시간순과 설비·Batch·고장 Episode 단위로 분할하여 동일 사건이 Train과 Test에 섞이는 Leakage를 막는다. 희소 고장 문제에서는 Accuracy보다 Confusion Matrix, Precision, Recall과 F1을 함께 본다.

Precision은 경보 중 실제 고장의 비율이고 Recall은 실제 고장 중 검출한 비율이다. Threshold를 낮추면 Recall이 증가할 수 있지만 False Alarm과 정비부하도 증가한다. 따라서 경보 Lead Time, 미검출 비용, 확인인력과 Action 가능성을 포함해 Threshold를 정한다.

배포 단계에서는 Training과 현장 Runtime의 Sensor, 전처리, 입력 Schema, Library, Hardware와 Latency 차이를 검증한다. Model, Dataset, Feature, Code, Hyperparameter와 Threshold의 Version을 연결해 재현과 Rollback을 보장한다. 운영 중에는 입력품질, Missing, Latency, Prediction 분포, False Alarm과 사용자 조치를 Monitoring한다.

Data Drift는 입력분포의 변화이고 Concept Drift는 입력과 Target 관계의 변화다. Drift나 성능저하가 나타나면 승인된 Data Window로 Retraining하고 기존 Champion과 동일 Test, Replay와 Stress Scenario로 비교한다. 최신 데이터로 재학습했다는 이유만으로 개선을 가정하지 않는다.

Explainability는 Model 검토를 돕지만 인과성, 정확성이나 안전성을 자동 증명하지 않는다. 고위험 정비결정에는 Human Review, 불확실성 표시, Fallback과 Override 책임을 둔다. MLOps는 Data·Feature·Model·Code Version, Test, Registry, Deployment, Monitoring, Approval과 Rollback을 연결한다. 결론적으로 SW-11은 데이터 품질과 Context 기반을, SW-12는 학습·추론과 Model Lifecycle을, SW-13은 AI가 물리 시스템에 폐루프로 작용하는 안전제어를 담당한다.

## Topic Importance

- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- 고득점 조건:
  1. AI–ML–DL의 포함관계와 학습유형을 정확히 설명한다.
  2. Anomaly Detection, Predictive Maintenance와 RUL의 출력·한계를 구분한다.
  3. Train·Validation·Test와 시간·설비·Episode 분할을 설명한다.
  4. Data Leakage와 Class Imbalance의 성능 왜곡을 설명한다.
  5. Confusion Matrix, Precision, Recall과 F1을 수식과 함께 적용한다.
  6. Threshold, False Alarm, 미검출, Lead Time과 비용의 Trade-off를 설명한다.
  7. Training–Serving Skew와 Deployment 검증을 설명한다.
  8. Model·Dataset·Feature·Code·Threshold Version Traceability를 제시한다.
  9. Data Drift와 Concept Drift를 구분하고 Retraining Trigger를 설명한다.
  10. Champion–Challenger와 Regression·Replay 검증을 제시한다.
  11. Explainability의 한계와 Human Review·Fallback을 제시한다.
  12. SW-11·SW-12·SW-13의 Ownership 경계를 명확히 한다.

## Routing Alias

1. `industrial AI anomaly predictive maintenance lifecycle`
2. `machine learning training validation test leakage`
3. `industrial anomaly detection threshold false alarm`
4. `predictive maintenance remaining useful life uncertainty`
5. `imbalanced failure data precision recall F1`
6. `industrial time series model drift retraining`
7. `feature engineering process sensor data`
8. `MLOps model registry deployment monitoring rollback`
9. `data drift concept drift industrial process`
10. `model explainability human review maintenance`
11. `classification regression forecasting industrial AI`
12. `AI process optimization constraint recommendation`
13. `training serving skew edge inference monitoring`
14. `champion challenger model regression validation`


Broad Alias로 단독 사용하지 않는 표현:

```text
AI
ML
Machine Learning
Deep Learning
Anomaly
Prediction
Model
Training
Accuracy
MLOps
```

## Question Examples

### Positive

1. 산업 AI·Machine Learning의 유형과 Model Lifecycle을 설명하시오.
2. 산업 이상탐지 Model의 Score, Threshold, False Alarm과 미검출 관리방안을 설명하시오.
3. 예지보전과 Remaining Useful Life Model의 구축 및 평가방안을 설명하시오.
4. 산업 시계열 Machine Learning에서 Train·Validation·Test 분리와 Data Leakage 방지방안을 설명하시오.
5. 고장 데이터 불균형에서 Precision, Recall과 F1의 의미를 설명하시오.
6. 산업 AI Model의 Drift Monitoring과 Retraining 절차를 설명하시오.
7. MLOps 기반 Model Version, Deployment, Monitoring과 Rollback을 설명하시오.
8. 산업 AI의 Explainability, Human Review와 현장 적용 한계를 설명하시오.
9. 산업 Process Optimization Model의 제약조건과 안전한 적용방안을 설명하시오.
10. Classification, Regression, Forecasting과 Anomaly Detection의 적용 차이를 설명하시오.

### Negative Boundary

1. Historian의 Timestamp, Quality Code와 Batch Genealogy를 설명하시오. → SW-11
2. MES·ERP와 ISA-95 기반 IT/OT 통합 구조를 설명하시오. → SW-11
3. Physical AI와 Robot Sensor Fusion 기반 자율제어를 설명하시오. → SW-13
4. Digital Twin 기반 Closed-loop Robot Planning의 안전제어를 설명하시오. → SW-13
5. OPC UA, MQTT와 Modbus Protocol을 비교하시오. → SW-07
6. PLC Sequence, Interlock과 Trip Logic을 설명하시오. → SW-02
7. SIS Safety Application Program의 SIL과 Verification을 설명하시오. → SW-05
8. 일반 Software 요구분석, Unit Test와 Configuration Management를 설명하시오. → SW-04


## Focused Regression

1. Source 6개와 Focused Test 1개 존재
2. JSON 4개 Parsing
3. Topic ID 일치
4. Anchor 30개
5. Fatal 16개
6. Major 12개
7. Modern Root Schema
8. AI–ML–DL과 학습유형 경계
9. Train·Validation·Test와 Data Leakage
10. Class Imbalance와 Precision·Recall·F1
11. Anomaly Threshold·False Alarm·RUL
12. Deployment·Version·Monitoring
13. Drift·Retraining·Champion–Challenger
14. Explainability·Human Review·MLOps
15. SW-11·SW-12·SW-13 경계
16. Generated/Production 수정 금지

## 생성 파일

```text
docs/topic_sheets/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle.md
rubrics/topic_packs/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle/README.md
rubrics/topic_packs/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle/fact_anchor.json
rubrics/topic_packs/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle/logic_check.json
rubrics/topic_packs/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle/model_answer.json
rubrics/topic_packs/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle/topic_importance.json
scripts/test_industrial_ai_ml_model_lifecycle_topic.py
```

## Verify-first

- 적용 AI Governance·산업안전 표준과 Edition
- 현장별 False Alarm·미검출 비용과 Threshold
- RUL Failure Threshold, 신뢰구간과 허용오차
- Drift Metric, Trigger와 Retraining 승인기준
- Edge Runtime, Latency, Resource와 Cybersecurity 요구
- Closed-loop 적용의 안전제약, 승인과 규제 적합성
