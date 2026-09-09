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

## 반복 안정성 기준

단일 실행 정확도만으로 운영 후보를 승인하지 않는다. Accuracy Gate가 통과하면 동일
commit과 provider 설정으로 uncached 30건을 한 번 더 생성하여 다음을 확인한다.

- 전체·pairwise 요구상태 일치율 ≥ 0.90
- 중대 상태 전이율 ≤ 0.03
- 사례별 총점 최대 편차 ≤ 4.0점
- 실행별 누락 case = 0

정본은 `calibration/demand_state_stability_policy.json`이다. 누락된 요구 예측은 비교에서
제외하지 않고 `UNKNOWN`으로 계산한다.

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
채점하고 Accuracy 통과 후 두 번째 uncached 실행으로 Stability Gate를 검사한다.
어느 하나라도 `READY/STABLE`이 아니면 exit code 2로 배포를 차단한다. 실행 전에 선택 provider의
credential, Ollama endpoint와 지정 model을 사전점검하므로 준비되지 않은 환경에서는
전체 release와 30건 채점을 시작하지 않는다.
재채점 중 provider 오류·quota 초과·비정상 JSON이 한 건이라도 발생하면 해당 결과를
저점수 prediction으로 간주하지 않고 qualification 자체를 `HOLD`로 종료한다.

```bash
python3 scripts/release_candidate.py qualify --workers 2
```

결과와 provider 설정 fingerprint는
`reports/release_candidates/<UTC>_<commit>/manifest.json`에 기록된다. provider API
호출이 있으므로 credential과 비용·rate limit을 확인한 운영 환경에서 실행한다.

`--require-ready`는 기준 미달 시 exit code 2를 반환한다. 2026-09-03 기준 현재
30건은 모두 `reviewed`이며 25개 Topic, 4개 Question Type 분포 기준을 충족한다.
최근 완료된 후보 `ac79b20`의 30건 결과는 요구 추출 F1 1.0, 요구 상태 정확도
0.8018, major/fatal precision·recall 1.0, 평균 허용구간 외 거리 0.4857,
false pass/strong/high-score 0건이다. 요구 상태 정확도 기준에 미달하므로 운영 배포
판정은 여전히 `HOLD`이다. 현재 evidence-resolution 변경은 새 commit의 반복 실행으로
다시 검증해야 하며 이 과거 수치를 배포 근거로 재사용하지 않는다.
새 policy는 기존 `score_range_mae`라는 오해 소지가 있는 이름 대신
`mean_out_of_range_distance`를 보고하며, expert total label이 있을 때만 actual
total MAE·signed error·A/B/C/D/E layer MAE·pairwise ordering을 계산한다. padding
변형 group이 제공되면 padding sensitivity도 별도로 보고한다.

## 결정론적 권한 제거 Gate

Provider Accuracy·Stability Gate와 LLM verdict authority 제거 Gate는 별도다. 전자는 현재 provider 기반 운영 후보의 정확도를 검증하고, 후자는 외부 provider 없이 correctness verdict를 소유할 준비가 됐는지 검증한다.

```bash
python3 scripts/run_deterministic_replay_audit.py
python3 scripts/check_deterministic_authority_gate.py
```

정본은 `calibration/deterministic_authority_policy.json`이다. Stage54 Gemini-off 48건은 질문-only Topic routing recall 100%, known-fatal recall 100%(16/16), false positive 0, score coverage 100%(48/48), 점수 허용구간 적중률 100%, 평균 범위 이탈 0점, known-overgrading 0건이다. 따라서 offline Authority Gate는 `READY`다. `scripts/audit_golden_risk_coverage.py` 기준 inventory는 78개 Topic, reviewed 48건, covered 31개, 3-lane 완료 6개다. 심화 증거 미충족 답안은 18.5점, 일반 자동 증거만으로 산정 가능한 최고점은 24점으로 제한한다. Stage39~41에서 provider-zero 운영 검증을 완료했으며 저장소 기본값은 rollback을 위해 `false`, 실제 운영 `.env`는 검증된 `true`를 사용한다.
