# Industrial ML, anomaly and predictive maintenance — 14 claim-by-claim primary-source comparisons

Date 2026-11-01. Exact original `rubrics/topic_packs/industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle/fact_anchor.json`; reviewer GPT-6. Every item was previously PENDING on the original 1,290 unique Fact ID ledger. These are claim-level *technical facts*, not product/vendor adoption statements or mandatory enterprise AI checklists.

**Results: 12 KEEP_BOUNDED and 2 REVISE_REQUIRED.** Key distinction: "representative of applicable modes" is a valid selection principle, whereas mandatory inventory of season, products and maintenance states on every industrial model is unjustified. Likewise NIST post-deployment monitoring does not prescribe an identical telemetry checklist for every task. Both overbroad checklist claims remain held from general scoring until source-controlled revision.

## Primary publisher documents inspected
- **NIST-M** — NIST AI RMF Playbook, Measure (2026-11-01 accessed), MEASURE 1.1, 2.4, 2.9, risk-measure selection and post-deployment monitoring: https://airc.nist.gov/airmf-resources/playbook/measure/
- **Google-R** — Google, Rules of Machine Learning, Martin Zinkevich, #9, #10, #29–33, #37 (training-serving skew, time-split and monitoring): https://developers.google.com/machine-learning/guides/rules-of-ml/
- **Google-D** — Google ML Crash Course, Datasets: Dividing original dataset, train-validation-test and leakage: https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets
- **Google-T** — Google ML Crash Course, Thresholds and confusion matrix: https://developers.google.com/machine-learning/crash-course/classification/thresholding
- **Google-P** — Google ML Crash Course, Accuracy, recall, precision and related metrics: https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall
- **Google-I** — Google ML Crash Course, Class-imbalanced datasets: https://developers.google.com/machine-learning/crash-course/overfitting/imbalanced-datasets
- **Google-L** — Google ML Crash Course, Dataset labels and errors: https://developers.google.com/machine-learning/crash-course/overfitting/labels
- **Google-S** — Google ML Introduction, Supervised Learning: https://developers.google.com/machine-learning/intro-to-ml/supervised
- **SK-C** — scikit-learn developers, User Guide 1.16 Probability calibration, empirical frequency criterion: https://scikit-learn.org/stable/modules/calibration.html
- **NIST-P** — NIST, A review of diagnostic and prognostic capabilities and best practices for manufacturing, Vogl/Weiss/Helu (2016), abstract: https://www.nist.gov/publications/review-diagnostic-and-prognostic-capabilities-and-best-practices-manufacturing
- **DOE-M** — US DOE, Energy Management Information System Capabilities, §§Automated Fault Detection and Diagnostics / Condition-based maintenance: https://www.energy.gov/cmei/femp/energy-management-information-system-capabilities

Some NIST papers provide official abstract/metadata HTML, not the full peer-reviewed report; the NIST Playbook HTML and Google developer and scikit-learn first-party HTML provide direct technical particulars. No PDF or restricted ISO clauses were claimed inspected.

## Exact-ID original statement review

| Exact Fact ID | Independent disposition | First-party source and locator | Grounding and generality boundary |
|---|---|---|---|
| `production_ai_monitoring_tracks_behavior_against_contextual_baselines` | `REVISE_REQUIRED` | NIST-M §MEASURE 2.4; Google-R #10, #37 | NIST requires fit-for-purpose production monitoring but does not mandate all listed inputs/missing/range/latency/false alarm/user action/system health on every model. Rephrase as risk- and interface-selected monitoring signals and performance; hold universal multi-item checklist. |
| `training_data_representativeness_is_intended_use_specific` | `REVISE_REQUIRED` | Google-D §test set representative; NIST-M §MEASURE 1.1, §MEASURE 2.4; Google-L | Representative data and relevant operational modes matter, but *normal, fault, operating mode, product, season, maintenance state, sensor quality* cannot be all mandatory in each industrial ML task. Bound categories to intended use and observable ground truth. |
| `anomaly_scores_are_thresholded_without_identifying_fault_cause` | `KEEP_BOUNDED` | Google-T §classification threshold; NIST-P | For score/threshold-based anomaly detectors, deviation can trigger a flag but does not logically establish root cause; not all detectors produce a continuous anomaly score. |
| `ml_deployment_validates_runtime_compatibility_and_prediction_contract` | `KEEP_BOUNDED` | Google-R #9, #29, #32, #37 | Training–serving consistency and deployed feature schema/pipeline/runtime compatibility need fit-for-purpose checks. Enumerated library, hardware and latency are relevant when used, not universal mandatory tool lists. |
| `ml_retraining_triggers_are_contextual_and_candidates_require_validation` | `KEEP_BOUNDED` | NIST-M §MEASURE 2.4; Google-R #9, #37 | Observed distribution/performance drift and changes may prompt reassessment or retraining with held-out validation; automatic retraining at every drift event is neither established nor universally safe. |
| `train_validation_test_roles_and_holdout_integrity` | `KEEP_BOUNDED` | Google-D §§Training/validation/test; Additional problems | Training fits parameters, validation tunes hyperparameters/models, independent test estimates final generalization. Reusing test to tune contaminates holdout; avoid asserting a rigid required split ratio. |
| `binary_threshold_selects_precision_recall_operating_point` | `KEEP_BOUNDED` | Google-T; Google-P | For a fixed scored dataset, lowering threshold cannot decrease recall and may increase false positives, at cost of additional inspections. Tradeoff varies with costs, prevalence and score calibration; not a monotonic guarantee for measured precision. |
| `classifier_probability_calibration_and_threshold_risk` | `KEEP_BOUNDED` | SK-C §Probability calibration; Google-T | Well-calibrated predicted probability has observed event frequency near predicted bin value; uncalibrated numeric confidence does not justify interpretation as physical risk. Must validate calibration with out-of-sample data. |
| `explainability_supports_review_but_not_causal_accuracy_or_safety_proof` | `KEEP_BOUNDED` | NIST-M §MEASURE 2.9; NIST-M §MEASURE 1.1 | Explanation is a model inspection/interpretability aid, not a standalone causal identification, empirical accuracy evaluation or functional safety certification. |
| `ml_binary_confusion_matrix_separates_error_types` | `KEEP_BOUNDED` | Google-T §Confusion matrix; Google-P | TP/FP/TN/FN correct error taxonomy for binary classification at fixed threshold; interpret positive class and units consistently. |
| `predictive_maintenance_uses_observed_condition_to_inform_maintenance` | `KEEP_BOUNDED` | NIST-P abstract; DOE-M §AFDD & Predictive Maintenance | Condition monitoring and diagnostics/prognostics inform maintenance scheduling. Neither fault prevention nor quantitative improvement is guaranteed by definition. |
| `rare_event_classification_requires_per_class_and_cost_relevant_evaluation` | `KEEP_BOUNDED` | Google-P §Choice of metric; Google-I | For minority faults, accuracy alone can mask misses. Precision/recall/false-positive rates and costs are relevant; sampling/class weights are optional techniques, not required for every task. |
| `supervised_learning_uses_input_target_pairs` | `KEEP_BOUNDED` | Google-S §Foundational concepts | Supervised ML learns associations between features and labels; regression and classification, sometimes forecasting. Learned association does not imply causation. |
| `time_series_features_must_use_prediction_time_available_history` | `KEEP_BOUNDED` | Google-R #31–33; Google-D §holdout leakage | Rolling windows, derivatives and spectral/operating-context features must be calculable using information available by prediction timestamp. Future outcomes must not leak into training/evaluation features; no prescribed feature set. |

## Controlled repair proposals

1. `production_ai_monitoring_tracks_behavior_against_contextual_baselines`: '산업 AI 운영 모니터링은 용도와 위험에 따라 입력 품질, 데이터·예측 분포 변화, 추론 지연, 판단 성능, 경보 결과와 시스템 상태 등 **해당되는 항목** 및 후속 조치의 기준선을 수립·검증한다. 모든 항목이 모든 시스템에 공통 필수라고 가정하지 않는다.'
2. `training_data_representativeness_is_intended_use_specific`: '훈련·검증 자료는 정의된 운전 범위와 예측 대상의 중요한 변동을 대표하도록 구성하며, 적용 설비에 실제로 존재하는 운전모드·제품·환경·고장사례·센서 품질 및 라벨 품질을 필요한 범위에서 평가한다. 특정 열거 항목을 보편적 필수조건으로 요구하지 않는다.'

Neither original Topic Pack nor Registry corrected in this source-evidence pass; two exact IDs enter the revision scoring hold overlay. Expected after audit: **322 pending**, **598 KEEP_BOUNDED**, **49 REVISE_REQUIRED**, 31 insufficient, 7 standard-specific, 7 vendor-specific, 275 excluded, 1 legacy scoped. Unresolved scoring holds **367** (=322+31+7+7); separate revision holds **49**. Source approval, full release and A/B/C scoring promotion remain blocked. Draft PR #17 stays unmerged.
