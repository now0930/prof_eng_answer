# 잔여 승인 Fact 1,272건 전수 일반원리 선별 결과 (2026-10-30)

## 완료 범위와 한계

기존 첫 배치 20건을 제외한 **1,272개 Fact ID를 모두 한 번씩** 구조 감사와 로컬 모델 일반원리 선별에 통과시켰다. Registry SHA-256은 `918a0b0c594929ab34068630311a54005df0dd9152ee36ac0d670022f3f450de`이다. 사설 WordPress DB·개인 답안·세션은 입력하지 않았다. 모델은 호스트 내부 Ollama `qwen3.5:9b`이며 외부 API를 호출하지 않았다. AI 검토를 사람 승인이나 원문 대조로 기록하지 않는다.

구조 감사에서는 1,272건 모두 현재 Anchor ID·Topic 연결, Fact 문장, 조건 목록, 근거 URL·locator의 **형식**을 통과했다. 이는 링크의 실제 본문 내용이나 Fact의 기술적 참을 보증하지 않는다. [전수 계약 감사 CSV](remaining_fact_contract_audit_20261030.csv)와 [집계](remaining_fact_contract_audit_20261030.json)에 모든 ID의 형식 결과가 있다.

로컬 모델의 단독 출력은 `GENERAL_OK` 1,086건, `SOURCE_SCOPE` 157건, `NARROW` 29건이었다. 모델 응답 오류·누락·중복은 0건이다. [모델 원시 이력](remaining_fact_local_review_20261030.jsonl)은 보조 의견이며 `GENERAL_OK`를 승인으로 전환하지 않는다. 수치·표준·제조사 범위 신호가 있으면 결정론적 플래그가 모델보다 우선한다.

| 후속 조치 | 건수 | 의미 |
| --- | ---: | --- |
| GENERAL_PRINCIPLE_CANDIDATE | 663 | 일반원리 수준의 명백한 범위 신호가 없고 모델도 수용. 정식 source-grounded 재승인은 아님. |
| NUMERIC_CONDITION_REVIEW | 230 | 수치·식·단위·경계 조건을 식 또는 권위 있는 근거와 대조할 대상. |
| SOURCE_SCOPE_REVIEW | 350 | 회사·제품·표준 조항의 범위를 보편 정답으로 확대하지 않았는지 확인할 대상. |
| NARROW_CLAIM_REVIEW | 29 | 모델이 문구 축소를 제안했으나 오탐 가능성이 있으므로 사람/독립 근거로 재판정할 대상. |

이 집계의 정본은 [행별 후속 조치 CSV](remaining_fact_review_actions_20261030.csv)와 [JSON 집계](remaining_fact_review_actions_20261030.json)다. 모든 행의 `technical_verification`은 `NOT_SOURCE_VERIFIED`, `score_effect`는 `none`이다. **최종 기술 사실 재승인 0건**, 운영 Registry·Topic Pack·generated·채점 점수 변경 0건이다.

## 모델 오탐 확인

`NARROW` 29건을 곧바로 Pack 수정 대상으로 삼지 않는다. 예컨대 `sil_target_pfd_relation`에 대해 모델은 PFDavg에 시간 역수 차원이 있다고 잘못 지적했다. [IEC 61508-1 공개 미리보기](https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTA4LTF7ZWQyLjB9Yi5wZGY)는 저요구 모드의 **평균 요구고장확률**과 고요구/연속 모드의 **시간당 위험고장빈도**를 구별한다. PFDavg는 확률이므로 무차원이며, 이 모델 지적은 수정 근거가 아니다. `control_valve_required_cv_inverse_sqrt_pressure_drop`에도 Registry 조건에 단상·비기화·난류가 이미 명시돼 있는데 모델은 해당 조건이 없다고 지적했다. [IEC 60534-2-1 공개 설명](https://webstore.iec.ch/en/publication/2461)은 비압축성 유체의 모델 범위와 비난류 보정을 구분한다. 이 사례는 모델이 조건 필드를 놓칠 수 있음을 보여 준다.

첫 배치의 극저온 보닛 표현은 [별도 보고서](remaining_fact_recheck_batch01_20261030.md)의 범위 검토 후보로 유지한다. 특정 밸브에서 액추에이터까지 분리될 수 있으므로 ‘오류 확정’으로 처리하지 않는다. 제조사 제품 설명의 범위와 보편적인 패킹 보호 원리는 구별한다.

## 운영 유지 및 다음 내용 감사

이번 단계는 1,272건을 **전수 선별·검토 이력화**하는 작업을 완료했다. 609건(수치 230 + 출처 범위 350 + 문구 29)은 실제 내용·출처 대조가 남아 있으며, 663건도 원문 대조 완료를 의미하지 않는다. 따라서 기존 `verified`를 일괄 재승인하거나 점수 기준에 새 가점을 주지 않았다. 확정 오류가 발견된 Fact만 관련 Pack 소스와 승인 해시·generated·회귀 검증을 한 배치씩 갱신한다.

재현 명령:

```bash
python3 -B scripts/triage_remaining_fact_recheck.py
python3 -B scripts/audit_remaining_fact_contracts.py
python3 -B scripts/local_fact_general_review.py --batch-size 8
python3 -B scripts/adjudicate_remaining_fact_review.py
python3 -B -m pytest -q tests/test_remaining_fact_recheck_triage.py tests/test_remaining_fact_contract_audit.py tests/test_adjudicate_remaining_fact_review.py
python3 -B scripts/rubric_manager.py validate-all
PROMOTE_GENERATED=0 scripts/validate_release.sh
```

Ollama 단계는 `127.0.0.1:11434` 접근 가능한 호스트에서만 실행하며 출력은 Fact ID별 재개 가능하다. Registry 해시가 바뀌면 이전 모델 행을 그대로 재사용하지 않고 새 기준으로 재선별한다.
