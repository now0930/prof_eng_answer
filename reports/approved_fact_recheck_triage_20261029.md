# 기존 승인 Fact 재검증 선별 — 2026-10-29

## 목적과 범위

기존 `verified` Fact 전체를 무조건 다시 LLM에 보내지 않고, **출처·연결 계약의 이상 신호가 있는 것부터** 재검증한다. 현재 Registry는 1,524행이다. 이는 이전에 보고한 1,522행에 2026-10-29 신규 승인 Coriolis Fact 2행을 더한 수치다. 현재 Anchor에 연결되는 고유 ID는 1,522개이며, 등록부 행수와의 차이는 연결 없는 1행·중복 연결 1건에서 생긴다. 신규 승인 2행은 재검증 완료로 별도 취급하되 전수 필터 입력에는 포함했다.

필터는 공개 저장소의 Registry·Topic Pack JSON만 읽는다. WordPress 개인 DB, 답안, 세션, 인증 정보는 열지 않는다. 결과는 [전체 행별 CSV](approved_fact_recheck_triage_20261029.csv)와 [기계 판독 요약](approved_fact_recheck_summary_20261029.json)에 있다.

## 결과

| 우선순위 | 행수 | 의미 |
| --- | ---: | --- |
| P0 | 4 | Anchor 연결 누락 1행과 앞선 감사에서 조건 수정이 필요하다고 확인된 3행. 즉시 사실·Pack·출처 관계 확인. |
| P1 | 138 | 계산 근거만 있음, 출처 위치가 포괄적임, 중복 Anchor 연결, URL 없는 비계산 근거 등의 신호. 오류 확정이 아니라 근거 품질 재확인 대상. |
| SAMPLE | 83 | P0/P1 외에서 Topic별 해시 고정 표본 최대 1행. 필터가 놓치는 유형을 점검하는 품질관리 표본. |
| DEFER | 1,299 | 이번 메타데이터 필터에서 우선 신호가 발견되지 않음. **기술적으로 재검증 완료라는 뜻은 아니다.** |

따라서 바로 재검토할 큐는 **225/1,524행(14.8%)**이고, 1,299행은 결과를 보면서 단계적으로 해제한다. 기존 19개 직접 재검토는 P0의 알려진 조건 문제를 포함하며, 이 선별 결과를 19개 추가 승인으로 중복 계산하지 않는다.

P0 상세:

- `liquid_in_glass_thermometer_calibration_is_immersion_condition_specific`: `legacy_anchor_id`가 없어 현 Pack Anchor와 직접 연결되지 않는다. Fact 자체의 기술적 오류 여부는 별개다.
- `second_order_normalized_frequency_response_magnitude` (`F2`): `|G(jω)|/K`의 `K>0` 조건 또는 `|K|` 정규화 필요.
- `second_order_resonance_frequency_condition` (`F3`): `ζ=0` 및 `ζ=1/√2` 경계 설명 재확인.
- `second_order_overdamped_response`: “느리다”의 비교 기준 명시 필요.

## 필터 계약과 다음 단계

P0/P1은 **재검증 요청**이지 승인 취소나 오답 확정이 아니다. 외부 URL의 실시간 접근성, 본문과의 의미 일치, 수학적 정확성은 이 기계 필터가 판정하지 않는다. 특히 `calculation_only`는 올바른 유도식일 수 있고 `coarse_locator`도 실제로는 맞는 근거일 수 있다. `DEFER`에서 추출한 표본에서 중대한 미탐이 발견되면 신호 규칙과 표본 크기를 수정하고 1,524행을 다시 선별한다. 미탐이 없더라도 전수 기술 검증 완료라고 기록하지 않는다.

실행:

```bash
python3 -B scripts/triage_approved_fact_recheck.py
python3 -B -m unittest scripts/test_triage_approved_fact_recheck.py
```

스크립트는 Registry SHA-256과 모든 Fact의 단일 배정(P0/P1/SAMPLE/DEFER)을 출력한다. 점수·운영 Bank·승인 상태를 변경하지 않는다. 다음 내용 검토는 P0 4개 → P1 138개 → SAMPLE 83개 순으로 진행하며, 근거 불일치가 확인된 Fact만 source/Registry 수정과 회귀 검증 대상으로 올린다.
