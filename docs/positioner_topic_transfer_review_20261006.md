# 포지셔너 Pack 하위 문제의 owner 이관/신규 Pack 검토

검토일: 2026-10-06
대상: `control_valve_positioner_ip_converter_booster_accessories_calibration`의 기존 10개 expected patterns
상태: **기존 검토안 + 2026-10-07 managed 신규 Pack 초안 생성. 기존 Pack owner/Router/채점 자료는 미이관**

## 1. 결론

중심 포지셔너 Pack은 사용자가 지정한 **전통 공압식·전기공압식 포지셔너 구조와 작동원리**에
집중시키는 것이 타당하다. 주변 패턴은 아래와 같이 처리하는 안을 제안한다.

- **기존 owner로 이관:** split-range process architecture → `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`; 정비 후 교정·진단 → `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing`; actuator force/bench range → Topic 1; safety final-element solenoid/fail/proof-test → Topic 15; installed acceptance/lifecycle → Topic 16.
- **신규 Pack 후보:** 공압 부속기기(booster, filter regulator, lock-up, quick exhaust, volume tank)의 구조·기능·적용을 소유할 기존 독립 Topic은 없다. 별도 Pack을 두는 편이 경계를 가장 명료하게 한다.
- **중심 Pack에 남김:** command→positioner→actuator→travel feedback, conventional pneumatic/electropneumatic positioner 원리, I/P 역할, feedback, action 용어의 최소 구분.

새 Pack 이름 후보: `control_valve_pneumatic_accessories_function_application`.
대표 예상 문제 후보: **제어밸브의 공압 부속기기(Volume Booster, Filter Regulator,
Lock-up Relay, Quick Exhaust 및 Volume Tank)의 구조·기능, 적용 목적과 구성상 주의사항을
설명하시오.**
기출 증거는 확인되지 않았으므로 지식원천 기반 예상 문제다.

## 2. 패턴별 owner 결정안

| # | 기존 문제 축 | 권고 owner | 판정 근거 / 인계 조건 |
|---:|---|---|---|
| 1 | 전체 command–I/P–positioner–actuator–travel chain | 기존 Positioner Pack | 중심 구조·feedback 문제의 답안 backbone |
| 2 | Nozzle-flapper·force balance·relay | 기존 Positioner Pack | 전통 공압식 positioner 작동원리의 중심 |
| 3 | I/P current-pressure mapping | 기존 Positioner Pack | 별도 I/P와 integrated electropneumatic positioner 경계를 설명하는 데 직접 필요. 4–20 mA/3–15 psi는 conventional condition 예시로 한정 |
| 4 | Positioner direct/reverse, actuator action, fail action | 분할 유지: 용어 경계는 Positioner, spring/thrust는 Topic 1, SIS safe-state/proof는 Topic 15 | 기존 패턴 전체를 하나의 owner에 두지 않는다. 중심 문제는 action과 fail을 동의어로 쓰지 않는 구분만 유지 |
| 5 | Volume Booster pilot-following과 flow capacity | 신규 pneumatic accessories Pack; hunting/bypass dynamic effect는 Topic 3 | Topic 3이 booster의 dynamic/hunting tradeoff를 소유하지만 accessory 기초구조/steady flow-capacity 원리 전체의 단독 owner는 아님 |
| 6 | Filter regulator·lock-up·quick exhaust·solenoid·volume tank 비교 | 신규 pneumatic accessories Pack; solenoid의 SIS/ESD logic·credit은 Topic 15 | 다섯 기능의 pneumatic accessory chain은 응집된 예상문제가 될 수 있음. safety solenoid architecture는 분리 |
| 7 | Bench set→coupling→endpoint→linkage→zero/span→multipoint→loop/fail/as-left 절차 | 기존 valve maintenance Pack으로 이관 검토; actuator bench set 산정은 Topic 1 | maintenance Pack의 post-maintenance stroke/fail/accessory test 및 as-left return-to-service와 같은 절차형 backbone. 기존 README가 상세 positioner calibration을 현 Pack에 둔다고 명시하므로 양쪽 owner 문구와 tests를 함께 고쳐야 함 |
| 8 | Split-range local mapping, gap/overlap, calibration | process architecture는 기존 Loop Pack; local device normalization은 calibration owner에 handoff | Loop Pack이 split-range control/transition을 이미 묻고 소유한다. 포지셔너 Pack은 특정 positioner의 local input normalization만 설명 보조로 유지 가능 |
| 9 | signal/air/power/accessory failure diagnosis | 기존 valve maintenance Pack, 원인별 specialist handoff | maintenance Pack에 symptom triage, external cause elimination, fail-action/accessory test가 이미 있음. stiction/hunting 상세는 Topic 3, smart diagnostics Topic 12, SIS credit Topic 15 |
| 10 | integrated command/current/pressure/travel/fail/action/records 및 다중 Topic handoff | 통합 시험 목적에 따라 maintenance Pack 또는 Topic 16, SIS이면 Topic 15 | 여러 Topic의 경계를 한 개 scoring pattern에서 평가하지 않는다. 정비 후 as-left는 maintenance, project acceptance는 16, safety proof는 15 |

## 3. 후보 Pack의 coverage 및 경계

새 `control_valve_pneumatic_accessories_function_application` Pack은 기능 비교라는 한
문제 backbone에 다음 요구를 연결할 수 있다.

| 요구 | 최소 답안 지식 | 기존 anchor 후보 |
|---|---|---|
| Accessory chain의 목적 | supply conditioning → pilot/output → actuator chamber fill/hold/vent 및 저장 | `filter_regulator_supply_conditioning`, `volume_booster_flow_capacity_function`, `lockup_relay_supply_failure_holding`, `quick_exhaust_rapid_vent_function`, `volume_tank_energy_storage_response_tradeoff` |
| Volume booster | pilot-pressure following과 fill/vent capacity, actuator volume/tubing 영향 | `booster_pressure_follower_boundary`, `tubing_output_capacity_pressure_drop` |
| 응용·한계 | response improvement와 hunting/bypass tradeoff; setting은 vendor/load/service에 의존 | `booster_bypass_hunting_topic3_handoff`, Topic 3 handoff |
| Failure/fail-state 조건 | supply loss, hold/vent path, package configuration 및 fail action 차이 | `loss_signal_air_power_failure_response`, `actuator_action_fail_action_separation` 일부 |
| Solenoid 경계 | general pneumatic path switching까지만; SIF/ESD logic, SIL/PST credit은 별도 | `solenoid_on_off_pneumatic_switching`, Topic 15 handoff |

주의: 위 ID들은 기존 Positioner Pack의 소유 anchor 후보였다. 2026-10-07 draft는 의미가
겹치는 지식을 신규 고유 ID로 재구성했으며, source anchor는 삭제·이관하지 않았다. 따라서
중복 소유권/라우팅은 여전히 미해결이고, 새 Pack이 승인·운영화되기 전까지 기존 source와
routing을 유지한다.

## 4. 기존 Router evidence와 영향

현재 결정론 Router에 넣은 대표 질의 결과:

| 질의 | 현재 primary route | 의미 |
|---|---|---|
| Positioner zero/span·up/down calibration | 기존 Positioner Pack | calibration 이관 시 exclusive/specific route와 기존 회귀를 함께 변경해야 함 |
| split-range local normalization·gap/overlap | Loop Architecture + Positioner Pack | owner overlap이 실제 관찰됨. process transition과 local actuator scaling을 분리해야 함 |
| Booster 및 5 accessory 기능 비교 | 기존 Positioner Pack | 신규 accessory owner가 생기면 exact/specific alias 충돌 검사 필요 |
| signal/air/power accessory diagnosis | 기존 Positioner Pack | maintenance pack으로 옮기려면 positive routing fixture와 tie-break 확인 필요 |
| post-calibration loop test | 기존 Positioner Pack | maintenance/Topic 16/SIS 15 중 요구조건을 기준으로 분기해야 함 |

기존 `scripts/test_control_valve_positioner_ip_booster_accessories_topic.py`는 40 Anchor,
10 patterns, route samples와 generated manifest/source-directory 동등성을 고정하는 계약을
포함한다. 현재 전체 script는 source directory 85개(Chapter 20 draft 3개 포함)와 generated
manifest 82개의 기존 불일치 때문에 manifest test가 실패하며, Router/semantic 하위 29개는
PASS했다. 이 baseline 불일치는 이번 검토로 발생한 것이 아니다. owner 이관 시 해당 test의
의미 있는 기대값을 새 contract에 맞춰 재설계하되 기존 golden score fixtures/채점 계약은
보호해야 한다.

## 5. 권고 실행 순서

1. **신규 pneumatic accessory Pack**을 managed `rubric_manager.py add-topic` 경로로 draft 생성한다. 고유 anchor를 작성해 기능/범위/출처 coverage를 구성한다.
2. 이관 anchor와 세부 기능만 신규 Pack으로 옮기고, Positioner Pack에서는 accessory 전용 expected pattern/alias를 owner migration 계획에 따라 단계적으로 제거한다.
3. calibration과 정비 후 failure/test 패턴은 maintenance Pack과 함께 source/test/Router를 한 단위로 보완한다. Topic 1의 actuator-only bench-set 산정은 이동하지 않는다.
4. split-range는 Loop Architecture와 positioner local calibration 사이에 “process transition vs device input scaling” handoff를 명시한다.
5. 각 단계에서 pattern → owner → anchors → model outline → routing tests → training/diagnosis consumers를 추적하고, targeted source/quality/router regressions 및 전체 validator를 수행한다.
6. 새 Pack은 실제 source를 사람이 검토하기 전까지 `draft / human_review_required`로 둔다. 승인·promote를 위조하지 않는다.

기존 전체 focused test 중 manifest/source-directory mismatch가 남아 있으므로, 첫 이관 전
그 baseline 문제를 별도 integration issue로 기록·분리해야 한다. 그것을 우회하기 위해
source inventory 또는 test를 임의 수정하지 않는다.

## 6. 2026-10-07 후속 작업 결과

- `scripts/rubric_manager.py add-topic`의 managed workflow를 사용해
  `control_valve_pneumatic_accessories_function_application` 초안을 만들었다.
- Topic Sheet, README, fact anchors 9개, model answer coverage, advisory logic profile,
  importance metadata를 작성했다. 단, source Handbook/Primer의 판본·페이지·도면을
  원문 대조하지 않았으므로 **기술 승인본이 아닌 knowledge-source-derived draft**다.
- 새 Fact Anchor는 고유 ID를 쓰고 기존 Positioner Pack anchor 삭제·수정은 하지 않았다.
  기존 anchor 출처임을 `source_basis`로 표시했다. 새 Pack aliases는 문서 검토용 후보이며,
  실제 route activation은 사람 검토와 통합 migration 전까지 금지했다.
- `logic_check.json` deterministic checks는 비활성화했고 fatal/major check도 추가하지 않았다.
  채점 점수·fatal 처리·Question Type·routing authority에는 새 Pack의 활성 영향이 없다.
- `topic_status.json`: `draft / human_review_required`; reviewer/approval/hash 비어 있음.
  source sheet hash와 draft content hash를 동기화했으나 이를 사람 승인으로 간주하지 않는다.
- 신규 Pack 전용 `validate_topic_packs.py --topic-id`, quality validator 및
  `validate-topic-pack-release --topic-id`는 PASS했다. generated 파이프라인이 검증용으로
  만든 파일들은 실행 후 사전 snapshot으로 복원됐다.
- 전체 source schema validation: 86 packs, 2,062 anchors PASS.
- 전체 release `--all`: workflow gate가 승격을 차단했다. 이 신규 초안 외에도
  `bubbler_level_measurement_purge_backpressure_diagnostics`,
  `float_level_measurement_buoyancy_guidance_tape_errors`,
  `sight_glass_level_gauge_communicating_vessels_interface`가 human review/approval을
  요구한다. 승인 상태를 임의로 바꾸지 않았다.
- Positioner regression: Router/semantic 및 39개 계약 검사는 통과했고 manifest alignment
  검사는 실패했다. 고정 manifest 82개와 현재 source directory 86개(기존 3개 draft + 새
  draft 1개)가 다르기 때문이다. 기존 상태에서도 82 대 85 불일치로 실패했으므로 이는
  선행 integration defect이며, 이번에는 그 차이가 1개 더 증가했지만 운영 generated/runtime
  파일은 바꾸지 않았다. 향후 manifest 대조는 승인된 운영 inventory와 draft inventory를
  구분하도록 별도 수정해야 한다. 현재 regression script는 변경하지 않았다.

## 7. 이번 검토의 범위

- 기존/신규 owner 권고와 Router smoke observation만 수행했다.
- Topic Pack source JSON, generated bank, tests, Router 및 topic directory는 변경하지 않았다.
- 새 Pack의 source reference 검토와 기존 consumer/routing migration은 여전히 남았다.
