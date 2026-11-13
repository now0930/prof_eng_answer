# Expert Accuracy / Stability Audit (Optional)

> **사람용 핵심:** 이 문서는 **선택형 정확도 감사**입니다. 현재 코드 배포 승인 조건은
> 전체 오프라인 pytest이며, 여기의 Golden 수치·`READY`·`STABLE`은 배포 허가를 대신하지 않습니다.
> 비용이 발생할 수 있는 검증은 별도 자격증명·예산이 필요합니다.
>
> **AI·개발자:** [구현 지도](ai_implementation_reference.md) · [검증 비용](validation_api_cost_policy.md) · [운영 절차](operation_runbook.md)


> **2026-11-09 사용자 지시:** Accuracy Gate와 Qualification `READY`는 운영 배포 필수 조건에서 제외했다. 이 문서의 검증은 **선택적 품질 감사**이며 pytest 기반 배포 승인에 영향을 주지 않는다. 현재 배포 코드 검증은 `scripts/release_candidate.py validate`가 수행한다.

코드 회귀검증과 채점 정확도 점검은 별도 목적을 가진다. 전문가 Golden Set으로 아래 기준을 평가할 수 있으나,
운영 배포 때마다 실행하거나 READY를 요구하지 않는다.

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

선택적 정확도 감사에서는 단일 실행 결과만으로 안정성을 증명하지 않는다. Accuracy Gate를 통과한 경우 동일
현재 canonical Golden 48건 전체를 동일 commit과 provider 설정으로 uncached 재실행하여 다음을 확인한다. 안정성 Gate의 정책 최소치는 30건이지만, 검증 표본 자체는 이번 비용 최적화에서 48건으로 유지한다.

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

**선택적 품질 감사**에서는 위 명령을 개별 실행하는 대신 다음 Orchestrator를 사용할 수 있다.
이 명령은 기존 prediction을 재사용하지 않고 **현재 운영과 동일한 provider 채점 경로를
검증 전용 자격증명으로** 실행한다. Accuracy 통과 후 두 번째 uncached 실행으로
Stability Gate를 검사한다. `VALIDATION_LIVE_API=1` 및 독립된
`VALIDATION_GEMINI_API_KEY`가 없는 경우 유료 검증을 시작하지 않고 HOLD한다.
선택적 감사의 `READY/STABLE` 기준 미충족 시 감사 실행이 실패하지만, 현재 pytest 기반 운영 배포를 차단하지 않는다. 실행 전에 선택 provider의
credential, Ollama endpoint와 지정 model을 사전점검하므로 준비되지 않은 환경에서는
전체 release와 Golden 재채점을 시작하지 않는다.
재채점 중 provider 오류·quota 초과·비정상 JSON이 한 건이라도 발생하면 해당 결과를
저점수 prediction으로 간주하지 않고 qualification 자체를 `HOLD`로 종료한다.

```bash
python3 scripts/release_candidate.py qualify --workers 2
```

운영 키(`GEMINI_API_KEY`)는 qualification에 전달하지 않는다. 검증 중
Argon과 다른 provider가 이용하는 legacy 변수에는 `VALIDATION_*` 값을 격리
주입하며, 생산 API 키와 동일하면 중단한다. 기본적으로 한 번에
`VALIDATION_MAX_LIVE_GRADES=60`까지만 제출할 수 있다. 현재 48건 Golden Set은
최소 2회 실행 시 96건이므로 기본 한도에서는 **API 요청 전에 중단**된다.
L3를 실행하려면 분리된 검증 프로젝트에서 96건 이상의 grade budget과 함께
`VALIDATION_MAX_HTTP_CALLS`, `VALIDATION_MAX_TOTAL_TOKENS`를 명시해야 한다.
모든 worker와 반복 subprocess가 같은 사용량 장부를 공유한다. HTTP 재시도와
`countTokens` 사전조회도 각각 세며, Gemini 요청 전 input token 수와 output 상한을
예약하고 응답의 실제 usage metadata로 정산한다. provider가 usage를 주지 않으면
상한 예약을 풀지 않는다. 상세 한도·외부 프로젝트 quota 조건은
[API 비용 단계 정책](validation_api_cost_policy.md)을 따른다.

현행 운영(결정론적 A/B/C + Argon D/E)에서는 `qualify`가
`--require-production-success`로 각 결과의 **실제 채점 경로**를 확인한다.
이 조건은 `gemini_semantic_evaluation`의 과거 성공 여부를 대신하지 않고,
`deterministic_score.decision=SCORED`, `llm_verdict_authority=0`,
`qualitative_de_evaluation.status=APPLIED`, 호출·근거·D/E 점수 반영 상태와
최종 점수의 일치를 검증한다. Argon provider 실패·미적용 `FALLBACK`·
미완성 JSON·미해결 요구사항은 **선택적 감사에서** HOLD로 기록한다. 사용자가 선택한 운영 설정은
변경하지 않고, 평가 30건 미만 또는 release validation 생략도 거부한다.
오프라인 검사 환경은 [운영 Runbook §19.1](operation_runbook.md)을 참고한다.

결과와 provider 설정 fingerprint는
`reports/release_candidates/<UTC>_<commit>/manifest.json`에 기록된다. provider API
호출이 있으므로 독립된 검증 credential과 프로젝트 quota·비용·rate limit을
확인한 환경에서 실행한다. 기본 offline 회귀검증은 외부 유료 API를 호출하지 않는다.

`--require-ready`는 기준 미달 시 exit code 2를 반환한다. 2026-09-03의 과거
30건 snapshot은 모두 `reviewed`이며 25개 Topic, 4개 Question Type 분포 기준을 충족했다.
최근 완료된 후보 `ac79b20`의 당시 30건 결과는 요구 추출 F1 1.0, 요구 상태 정확도
0.8018, major/fatal precision·recall 1.0, 평균 허용구간 외 거리 0.4857,
false pass/strong/high-score 0건이다. 요구 상태 정확도 기준에 미달하므로 운영 배포
감사 판정은 당시 `HOLD`였다(현재 배포 보류 상태를 뜻하지 않음). 현재 evidence-resolution 변경은 새 commit의 반복 실행으로
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

정본은 `calibration/deterministic_authority_policy.json`이다. Stage58 Gemini-off 48건은 질문-only Topic routing recall 100%, known-fatal recall 100%(16/16), false positive 0, score coverage 100%(48/48), 점수 허용구간 적중률 85.42%, 평균 범위 이탈 0.35875점, known-overgrading 0건이다. 따라서 offline Authority Gate는 `READY`, 동일 입력 2회 Gate는 `STABLE`이다. 근거 artifact는 `reports/deterministic_replay_stage58_20260917.json`, `reports/deterministic_authority_stage58_20260917.json`, `reports/deterministic_stability_stage58_20260917.json`이다. 실제 Telegram 저장 세션의 provider-zero dry-run도 canonical 고유답안 60/60을 처리했다. 일반 합격은 질문 계약의 `pass_required_anchor_ids` 충족, 최소 만족 비율과 WRONG 없음이 필요하고, 고득점은 core gap과 심화 evidence Gate를 추가로 통과해야 한다. Stage39~41에서 provider-zero 운영 검증을 완료했으며 저장소 기본값은 rollback을 위해 `false`, 당시 운영 `.env`가 `true`였다는 기록은 현재 실행 환경값을 증명하지 않는다. 운영값은 실제 서버에서 따로 확인해야 한다.
