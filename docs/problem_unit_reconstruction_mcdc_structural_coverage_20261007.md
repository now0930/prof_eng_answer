# 안전필수 SW 구조적 커버리지·MC/DC Topic Pack 보충 감사

## 발견과 보완

대상 `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`는 12개 패턴, 33개 Anchor의 required union 33/33이다. 각 패턴의 intent는 있었으나 열 개는 일반 영어 tag 수준이었고 두 개는 범위 문장을 그대로 복사한 intent였다. 또한 12개 패턴에 대응하는 `question_examples`가 없었다.

- 12개 intent를 문항별 요구·오류경계에 맞춰 구체화하고 expected pattern과 일치하는 example 12개를 추가했다.
- High-score, common-missing 및 importance 항목의 P1–P12 적용범위를 명시했다.
- 교차 주제 Regression pattern 11·12는 보존하되 일반 lifecycle, SIL 및 V-Model 주제가 MC/DC 모든 답안의 필수요건이 되지 않도록 범위를 한정했다.
- Question Type, routing, 33개 Anchor, fatal·logic/evaluator ownership은 변경하지 않았다.

## 검증

- 전용 pattern-scope contract test PASS.
- `scripts/test_mcdc_vmodel_sil_overgrading_regression.py` PASS; SIS/LOPA 및 MC/DC/V-Model 과대채점 case의 routing/score/fatal 결과가 보존됐다.
- Scoped Topic Pack release validation PASS; generated output은 promote하지 않고 사전 snapshot으로 복원했다.
- Screen inventory의 6개 disconnected question-family component warning은 독립 시험문항 신호로 유지하고 연결을 위조하지 않았다.
- 이번 구조 감사는 표준 요구사항 적합성 또는 기술전문가 승인을 의미하지 않는다.
