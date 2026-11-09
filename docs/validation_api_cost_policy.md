# 채점 검증 API 비용 단계 및 한도

## 목적과 불변 정책

API 비용을 줄이기 위해 오프라인 회귀, 선택적 API smoke, 운영 후보 정확도·안정성 Gate를 분리한다. **A/B/C 결정론적 권한, Argon D/E 적용 정책, A~E 배점, Fatal·상한·15점 참고선, 정확도/안정성 기준은 변경하지 않는다.** L1/L2 통과는 운영 배포 적격성을 의미하지 않는다.

개인 답안·OCR·세션 원문·프롬프트·API 키는 공개 저장소와 API 사용량 장부에 기록하지 않는다. API 장부에는 사례 수, 실제 HTTP 시도 수, provider가 응답한 토큰 수, 제한값과 provider/model 식별자만 기록한다.

## 검증 단계

| 단계 | 실행 | 유료 API | 의미 |
|---|---|---:|---|
| L1 오프라인 | 관련 `pytest`, `validate-all`, `PROMOTE_GENERATED=0 scripts/validate_release.sh` | 0회 | 구조·회귀·Release Gate 확인. mock/saved fixture를 사용하며 provider 정확도 검증은 아님 |
| L2 API smoke | `scripts/run_validation_api_smoke.py` | 명시적 실행 때 3~5건 | 선택 사례의 실제 채점 경로와 provider 연결 확인. 기본 실행은 dry-run이며 네트워크·키 검사를 하지 않음. READY 판정 불가 |
| L3 qualification | `scripts/release_candidate.py qualify` | 정확도 48건 + 안정성 반복 48건 | 기존 Accuracy/Stable Gate와 전체 48건을 그대로 평가. 전부 통과할 때만 READY 후보 |

### L2 smoke

기본 dry-run은 사례 ID와 한도만 출력한다. 유료 호출은 별도 validation credential과 명시적인 `--execute-live`가 모두 필요하다.

```bash
# Secret Manager/environment injection은 아래 validation key를 제공해야 함.
export VALIDATION_LIVE_API=1
export DETERMINISTIC_GRADING_PRIMARY=true
export QUALITATIVE_DE_MODE=argon
python3 -B scripts/run_validation_api_smoke.py \
  --case-id sil_target_operations_issue1 \
  --case-id sis_lopa_architecture_issue1 \
  --case-id mcdc_vmodel_sil_issue1 \
  --output-dir /tmp/prof-eng-validation-smoke-<run-id> \
  --max-http-calls 24 --max-total-tokens 250000 \
  --execute-live
```

실제 command line에 키 값을 쓰지 말고 서버 Secret Manager/environment injection을 사용한다. 운영 채점 키로 fallback하지 않는다. 각 L2 run은 최대 지정 사례 수, HTTP 호출 수 및 token reservation/usage 총량을 공유하는 SQLite 장부를 사용한다. `--workers 2`에서도 장부의 transaction이 모든 worker를 하나의 한도로 제한한다. 재시도는 각각 별도 HTTP 호출로 센다.

Gemini 생성 요청은 생성 전에 provider `countTokens`로 입력 token 수를 가져오고, 요청의 `max_output_tokens`를 합산해 전역 token budget에 예약한다. 완료 응답에 usage가 있으면 정확한 provider 보고량으로 예약을 정산한다. usage가 응답에 없으면 임의 추정값을 기록하지 않고 최악 예약량을 유지한다. CLOVA direct transport는 현재 입력 token preflight 계약이 없어 live validation budget 경로에서 호출을 차단한다. 필요한 경우 별도 계측 계약을 먼저 구현한다.

앱의 token reservation 외에 provider project/account quota도 설정해야 한다. 모델 내부 처리·provider 오류 과금처럼 앱이 사전에 확정할 수 없는 범위를 포함한 외부 절대 지출 상한은 provider quota가 담당한다. `api_usage.json`은 비용 금액을 추정하지 않고 provider가 보고한 token 수만 기록한다.

### L3 표본 결정

현재 Golden Set 48건은 31개 Topic, 5개 Question Type, 15개 `model_reference` 사례, 그리고 여러 분야의 정상·부분·치명 결과 triplet를 포함한다. 30건 subset은 정책의 최소치(30건, 10 Topic, 요구 유형별 3건, Major/Fatal 8개)를 숫자상 충족하도록 만들 수 있지만, 위 데이터 구성과 상태 범위를 동시에 보존하는 대표 표본으로 입증되지 않았다. 따라서 이번 비용 최적화에서는 **48건 전체를 유지**한다.

두 번의 uncached 실행은 96 submitted grades다. 기존 기본 한도 60에서는 유료 요청 전에 중단된다. 실제 L3 실행에는 `VALIDATION_LIVE_API=1`, 독립 Gemini validation key, 그리고 명시적 `VALIDATION_MAX_LIVE_GRADES`(96 이상), `VALIDATION_MAX_HTTP_CALLS`, `VALIDATION_MAX_TOTAL_TOKENS`가 모두 필요하다. 한도 누락·초과는 fail-closed HOLD다. 30건 표본으로 축소하거나 gate 기준을 낮추지 않는다.

## API 경로 요약

| 경로 | credential | 계측/제한 |
|---|---|---|
| Telegram `/grade` 운영 | 운영 provider key | 현재 운영 경로. 이번 변경으로 호출/점수 동작은 변경하지 않음 |
| 오프라인 release/pytest | key 없음 | provider 네트워크 0회 |
| L2 smoke의 `regrade_expert_accuracy_seed.py` | 분리된 validation Gemini key만 | 각 grade·provider HTTP attempt·Gemini 입력/출력/thinking token 집계, 단일 SQLite 예산 |
| L3 `release_candidate.py qualify`의 두 regrade run | 분리된 validation Gemini key만 | 전체 48×2, 두 subprocess가 동일 SQLite 예산 공유. 한도 초과/usage 오류는 HOLD |
| CLOVA live validation | validation CLOVA key가 있더라도 현재 token preflight 미구현 | 예산 계측 구현 전 HTTP 전송 자체를 차단 |

## 장부 해석

- `http_calls`: 실제 전송을 시도하도록 예산을 확보한 provider 요청 수. Retry와 `countTokens` 사전조회도 각각 포함.
- `actual_tokens`: 응답 metadata가 제공한 total. 입력/출력/thinking 세부값은 provider가 준 경우만 집계.
- `reserved_tokens`: 성공 사용량을 받지 못한 요청 또는 아직 정산되지 않은 요청의 보수적 예약량.
- `usage_unknown_calls`: provider가 사용량을 제공하지 않아 예약을 유지한 요청 수.
- `over_budget=1`: provider 보고 사용량이 예약/총량 한도를 초과함. Qualification은 계속 진행하지 않고 HOLD.

장부는 provider/model과 합계만 저장하며 question, answer, raw response, key는 저장하지 않는다. 비공개 qualification artifact로 보관한다.
