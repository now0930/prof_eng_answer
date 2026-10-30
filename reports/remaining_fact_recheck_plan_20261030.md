# 잔여 승인 Fact 재검토: 선별·운영 유지 계획 (2026-10-30)

## 현재 기준

2026-10-29 감사 스냅샷은 1,524행 중 233행을 검토하고 1,291행을 남겼다. 현재 Registry는 1,522행이며, 그중 과거에 검토된 **현존 Fact는 230행**이다. 따라서 현재 Fact ID 기준의 미검토는 **1,292행**이다. 차이 1행은 과거의 특정 회사 수리보고서 사례 Fact를 제거하고 일반 원리 Fact `valve_as_found_as_left_results_require_comparable_test_basis`로 대체한 뒤, 대체 Fact가 별도 독립 재검토 목록에 아직 포함되지 않았기 때문이다. 기존 감사 완료 수를 소급 변경하지 않는다.

새 선별 결과는 [행별 큐](remaining_fact_recheck_queue_20261030.csv) 및 [집계와 Registry 해시](remaining_fact_recheck_summary_20261030.json)에 고정한다. 현 시점 P0 386, P1 503, Topic별 SAMPLE 70, DEFER 333이다. 텍스트 신호가 넓게 잡히는 것을 감안해 **우선순위는 오류·검증 완료 판정이 아니다**. 특정 제조사의 사례나 보고서 필드는 일반 공학 사실의 필수 정답으로 승격하지 않는다.

[첫 배치 20건](remaining_fact_recheck_first_batch_20261030.csv)은 P0에서 Topic별 최대 1건만 뽑았다. 이 파일은 검토 대상 목록이며, 20건을 내용 검증했다는 뜻이 아니다.

## 검토 기준과 배치 절차

1. 한 배치는 10~20개 Fact ID로 제한한다. P0의 절대적 의무·보편 주장, P1의 수치·수식·적용조건, Topic별 표본 순으로 고른다. 한 Topic에 쏠리지 않도록 배치당 Topic별 상한을 둔다.
2. 각 Fact에 대해 **핵심 일반 원리**, 적용 조건, 정량식의 차원·경계, Anchor 문구, 인용 근거의 실제 지지 범위를 따로 판단한다. 학계·표준기관·공공기관·산업단체의 공개 자료 또는 명시적 유도식을 우선한다. 제조사 자료는 특정 장치 설명에는 쓸 수 있지만 보편적 의무의 유일한 근거가 될 수 없다.
3. 판정은 `GENERAL_VERIFIED`, `NARROW_OR_CORRECT`, `EVIDENCE_ONLY_FIX`, `INTERNAL_CONTRACT`, `HOLD` 중 하나로 기록하고, 검토자·검토일·현재 Registry 해시·근거 URL/수식·적용 제외 범위를 남긴다. `HOLD`는 점수 근거로 신규 승격하지 않는다. 출처 링크가 있다는 이유만으로 `GENERAL_VERIFIED`를 주지 않는다.
4. 문구 정정이 필요하면 별도 변경으로 진행한다. Topic Pack 변경 시 `docs/topic_pack_workflow.md`를 먼저 읽고 승인·source hash·generated 재생성 계약을 따른다. 수정 전후에 `validate-all`, 해당 회귀, `PROMOTE_GENERATED=0 scripts/validate_release.sh`를 확인한다. 실패한 배치는 승격하지 않고 원인과 영향 범위를 기록한다.
5. 운영 채점의 기존 Registry·Pack·generated 파일은 검증된 변경 배치가 통과하기 전까지 그대로 둔다. P0/P1 또는 미검토라는 이유만으로 기존 `verified` 상태를 일괄 변경하거나 점수 계약을 수정하지 않는다. 실제 위험 오류가 확인되면 해당 Fact의 운영 영향부터 조사한다.

재선별 명령: `python3 -B scripts/triage_remaining_fact_recheck.py`. 배치마다 Registry SHA-256을 비교하여 중복 검토나 최신 변경 누락을 방지한다. 이 선별기는 비공개 답안·세션·WordPress DB를 열지 않으며, 채점 파일을 변경하지 않는다.
