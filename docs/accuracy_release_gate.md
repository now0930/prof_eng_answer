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

운영 후보 전체 절차에서는 위 명령을 개별 실행하는 대신 다음 Orchestrator를 사용한다.
이 명령은 기존 prediction을 재사용하지 않고 현재 provider로 reviewed case를 다시
채점하며, `READY`가 아니면 exit code 2로 배포를 차단한다. 실행 전에 선택 provider의
credential, Ollama endpoint와 지정 model을 사전점검하므로 준비되지 않은 환경에서는
전체 release와 30건 채점을 시작하지 않는다.

```bash
python3 scripts/release_candidate.py qualify --workers 2
```

결과와 provider 설정 fingerprint는
`reports/release_candidates/<UTC>_<commit>/manifest.json`에 기록된다. provider API
호출이 있으므로 credential과 비용·rate limit을 확인한 운영 환경에서 실행한다.

`--require-ready`는 기준 미달 시 exit code 2를 반환한다. 2026-09-03 기준 현재
30건은 모두 `reviewed`이며 25개 Topic, 4개 Question Type 분포 기준을 충족한다.
다만 `present`를 `correct`로 취급하던 이전 prediction을 evidence-required 상태
정책으로 다시 측정하면 요구 상태 정확도는 0.5586이므로 최신
report(`reports/expert_accuracy_seed_current.json`)의 운영 배포 판정은 `HOLD`이다.
새 policy는 기존 `score_range_mae`라는 오해 소지가 있는 이름 대신
`mean_out_of_range_distance`를 보고하며, expert total label이 있을 때만 actual
total MAE·signed error·A/B/C/D/E layer MAE·pairwise ordering을 계산한다. padding
변형 group이 제공되면 padding sensitivity도 별도로 보고한다.
