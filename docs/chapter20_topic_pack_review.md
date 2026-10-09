# Chapter 20 Topic Pack 검토본

출처: [Lessons In Industrial Instrumentation, Chapter 20](https://now0930.pe.kr/wordpress/chapter-20/), 2026-09-30 열람.

## 추가·중복 정리

| 범위 | 처리 | 검토할 source |
|---|---|---|
| Sight Glass의 연통·연결·계면 재현 | 신규, 5 anchors | [README](../rubrics/topic_packs/sight_glass_level_gauge_communicating_vessels_interface/README.md) |
| Float의 부력·위치·가이드·테이프 오차 | 신규, 5 anchors | [README](../rubrics/topic_packs/float_level_measurement_buoyancy_guidance_tape_errors/README.md) |
| Bubbler의 퍼지·배압·진단 | 신규, 6 anchors | [README](../rubrics/topic_packs/bubbler_level_measurement_purge_backpressure_diagnostics/README.md) |
| 정수압·Wet/Dry Leg·Remote Seal·밀도·계면 | 기존 DP owner에 통합, 25→28 anchors | [README](../rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/README.md) |

각 README와 같은 디렉터리의 fact_anchor.json, model_answer.json, logic_check.json,
topic_importance.json이 검토 대상이다. 기존 anchor ID와 기존 질문의 필수 anchor는
보존했다. Tank Expert System과 보상 계면 질문은 각각 자체 required_anchor_ids를 갖는다.
초음파와 Radar의 기존 owner는 유지한다.

## 원문에서 명확히 한 조건

- Bubbler는 표면압을 뺀 배압과 침수깊이의 관계다. 낮은 안정 퍼지에서만 관 마찰 등의 생략이 타당하다.
- 세 압력으로 밀도를 계산하려면 하부·중간 탭이 동일 액체에 잠겨 있고 밀도가 대표성을 가져야 한다.
- 계면 측정의 전체 레벨 보상은 상부 탭 침수와 탭 사이 계면 조건을 요구한다.
- 밀도차×높이는 수두 환산 단위를 명시한다. SI 압력에는 g가 필요하다.
- 자유 부자의 위치 검출, 고정 displacer의 부력 검출, 초음파 TOF를 구분한다.

## 검증 및 상태

신규 3개는 draft / human_review_required이며 reviewer와 승인 해시는 비어 있다.
검토 없는 사람 승인 기록을 만들지 않는다. 운영 generated inventory는 82개,
이번 source 초안을 포함한 inventory는 85개 / 2,053 anchors다.

변경 4개 focused schema·quality·generated preview는 PASS(각 quality 오류·경고 0건)이다.
신규·기존 routing 및 질문별 scope 회귀 8개 테스트가 통과했다.
Atomicity는 85개 source에서 오류 0건, 기존 경고 35건으로 PASS다.
전체 validate-topic-pack-release --all은 신규 3개의 사람 승인 부재로 차단됐다.
generated 6개 파일은 HEAD와 동일하며 commit·push·운영 배포는 수행하지 않았다.
미리보기는 메모리에서 builder를 사용하며 운영 generated를 승격하지 않는다.
신규 semantic fatal 후보는 결정론적 오류 검출 구현·정확도 검증을 의미하지 않는다.

사람이 위 README와 JSON을 검토한 후 실제 reviewer ID로 각각 approve-topic을 실행한다.
그 뒤 validate-topic-pack-release --all, generated rebuild, non-promote release,
commit·push·CI 순으로 통합한다. 승인 전 전체 integration gate 차단은 예상된 상태다.
