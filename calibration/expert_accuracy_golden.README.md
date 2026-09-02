# Expert Accuracy Golden Set

- `draft`는 개발용이며 공식 정확도에서 제외한다.
- 전문가 1인 검토 후 `reviewed`, 의견 조정 완료 후 `adjudicated`로 변경한다.
- Golden label과 모델 prediction은 분리한다.
- 실행: `python scripts/measure_expert_accuracy.py --predictions predictions.jsonl`
- 개발 중 draft 포함: `--include-draft`
- CI에서 평가 건수를 강제하려면 `--require-cases`를 사용한다.
- 운영 배포 기준: `docs/accuracy_release_gate.md`
- 현재 30건은 모두 `reviewed`이며 25개 주제와 4개 Question Type을 포함한다.
- 사례 수 기준은 충족했지만 정확도·오류 재현율·점수 MAE 기준 미달 시 배포 gate는 계속 `HOLD`다.
