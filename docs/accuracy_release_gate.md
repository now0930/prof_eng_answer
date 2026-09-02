# Expert Accuracy Release Gate

코드 회귀검증 통과와 운영 정확도 입증은 별도 조건이다. 운영 배포는 전문가가 검토한
교차 주제 Golden Set과 실제 채점 prediction으로 아래 기준을 모두 만족해야 한다.

## 데이터 최소 기준

- `reviewed` 또는 `adjudicated` 30건 이상
- 서로 다른 Topic 10개 이상
- 4개 Question Type별 3건 이상
- major/fatal 정답 label 8개 이상

## 정확도 기준

- 요구 추출 F1 ≥ 0.90
- 요구 상태 정확도 ≥ 0.85
- major/fatal precision ≥ 0.90, recall ≥ 0.85
- 점수 허용구간 MAE ≤ 1.0
- false pass, false strong, confidence ceiling 위반 = 0

정본은 `calibration/expert_accuracy_release_policy.json`이다.

## 실행

```bash
python3 scripts/measure_expert_accuracy.py \
  --predictions calibration/expert_accuracy_predictions.jsonl \
  --require-cases \
  --output reports/expert_accuracy_report.json

python3 scripts/check_accuracy_release_gate.py \
  --report reports/expert_accuracy_report.json \
  --require-ready
```

`--require-ready`는 기준 미달 시 exit code 2를 반환한다. 현재 30건은 모두
`reviewed`이며 사례 수·주제·Question Type 분포 기준을 충족한다. 다만 현재
정확도, 치명 오류 재현율과 점수 MAE가 정책 기준에 미달하므로 운영 정확도
배포 판정은 `HOLD`이다.
