# 전통 포지셔너 Topic Pack 문제 단위 재구성 검토

검토일: 2026-10-06
대상: `control_valve_positioner_ip_converter_booster_accessories_calibration`
상태: **범위 재구성 제안 — source JSON과 runtime routing은 변경하지 않음**

## 1. 결론

현재 Pack은 40개 Fact Anchor와 10개 `expected_question_patterns`를 하나의 소유권으로
묶고 있다. 하지만 패턴은 단일 문제의 조건 변형이 아니라 구조·원리, I/P 변환, action,
부스터, 부속기기, 교정, split-range, 고장진단 등 서로 다른 답안 축이다. 따라서 현재
이름과 데이터는 **전통 포지셔너 중심의 독립 문제 단위라기보다 제어밸브 공압 부속기기
주제 묶음**으로 보는 편이 정확하다.

사용자가 정한 경계에 맞춘 중심 Problem Unit은 다음으로 제안한다.

> **전통적인 공압식 및 전기공압식 밸브 포지셔너의 구조와 작동 원리를 설명하고,
> 설정 신호와 밸브 이동량 사이의 피드백 동작 및 I/P 변환기의 역할을 설명하시오.**

이 문제는 과거 기출로 확인된 문항이 아니라 현재 기술 지식으로 구성한 **예상 문제**다.
정확한 기출 회차·출제 근거를 확인하지 않았으므로 기출 또는 공식 문제로 표시하지 않는다.

## 2. 요구-지식-Anchor-답안 coverage

| 문제 요구 | 연결 지식과 답안 논리 | 현재 Anchor | 상태 |
|---|---|---|---|
| 포지셔너의 목적·구조 | 설정값과 실제 이동량을 비교하는 local position controller이며, 기계식 travel feedback과 pneumatic relay/output 단계로 구성됨 | `positioner_travel_feedback_controller`, `travel_feedback_linkage_cam_alignment`, `pneumatic_positioner_force_balance_mechanism` | 핵심 coverage 있음. 구조 설명 그림/출처 위치는 별도 보강 필요 |
| 전통 공압식 작동 원리 | 입력·feedback element의 force balance가 nozzle-flapper/back-pressure를 변화시키고 relay가 actuator 압력을 조정하여 오차를 줄임 | `pneumatic_positioner_force_balance_mechanism`, `position_error_negative_feedback` | 개념 coverage 있음. 특정 내부 구조를 모든 제품에 일반화하지 않도록 “사용할 수 있다” 표현 유지 |
| 폐루프 피드백 동작 | command와 travel feedback 차이로 correction을 만들고, travel이 요구값에 도달하면 equilibrium을 이룸 | `position_error_negative_feedback`, `positioner_travel_feedback_controller`, `travel_feedback_linkage_cam_alignment` | 논리 연결 가능. 수식 부호·정의는 적용 구조와 signal convention을 설명해야 함 |
| 전기공압식과 별도 I/P 구성 구분 | 통합형 전기공압 포지셔너와 별도 I/P + 공압 포지셔너를 구분 | `electropneumatic_positioner_separate_ip_boundary`, `ip_converter_current_pressure_transduction` | 핵심 coverage 있음 |
| I/P의 역할 및 대표 신호 관계 | I/P는 전류를 공압 신호로 변환하며 travel을 직접 측정하지 않음. 4–20 mA / 3–15 psi는 명시된 conventional range 예시 | `normalized_current_command`, `ip_linear_pressure_mapping`, `conventional_4_20ma_3_15psi_endpoints`, `ip_converter_current_pressure_transduction` | 충분하나 대표 문제에서 수치 계산까지 요구하지 않음. 입력 range가 주어질 때만 계산 변형으로 둠 |
| 동작 방향과 valve fail action 구분 | positioner action, actuator air action, spring action을 연결하되 fail action과 같은 뜻으로 쓰지 않음 | `positioner_direct_reverse_action`, `actuator_action_fail_action_separation` | 이 문제의 핵심 보조 설명. 실제 조합은 actuator/valve 조건이 있어야 단정 가능 |
| 공급 공기·현장 교정 | 공급 공기 품질·압력과 linkage 조정은 정상 동작의 조건 | `ip_supply_air_dependency`, `travel_feedback_linkage_cam_alignment`, `positioner_zero_span_travel_calibration` | 짧은 조건/적용 단락으로 유지 가능. 상세 작업절차는 다른 문제 후보 |

## 3. 현재 10개 패턴 처리안

| 기존 패턴 주제 | 제안 disposition | 이유 / 경계 |
|---|---|---|
| Command→I/P→positioner→actuator→travel chain | 중심 문제의 변형으로 유지 | 구조·feedback의 전체 연결을 같은 답안 골격으로 확인 |
| Nozzle-flapper·force balance·relay 원리 | 중심 문제의 변형으로 유지 | 전통 공압식 작동 원리의 심화형 |
| I/P 4–20 mA / 3–15 psi mapping | 중심 문제의 조건 변형으로 유지하되 선택 요구로 축소 | I/P 경계 설명은 핵심, 수치 환산만 단독 문제면 별도 owner 필요 |
| Direct/reverse, actuator action, fail action 비교 | 보조/경계 변형으로 유지 | 동일 feedback 답안의 적용 결과일 수 있으나, fail-safe 선정은 독립 문제 가능성 있음 |
| Volume booster | 분리 검토 후보 | positioner 구조 원리와 답안 중심이 다른 유량용량/응답 문제. Dynamic tuning은 Topic 3과 충돌 가능 |
| Filter regulator, lock-up, quick exhaust, solenoid, tank 비교 | 분리 검토 또는 여러 owner handoff | 서로 기능이 다른 accessory를 묶은 나열형 비교 문제. SIS/ESD는 Topic 15 범위 |
| Bench set부터 full calibration·fail verification 절차 | 분리 검토 후보 | 절차형 현장 작업 단위이며 Topic 1/16 및 여러 기존 handoff와 중첩 |
| Split-range mapping | 별도 문제 후보 | 독립 입력 분할·범위 정규화·sequencing 요구로 중심 문제와 답안 골격이 다름 |
| signal/air/power/accessory failure diagnosis | 별도 문제 후보 | 고장 위치 추적·진단 절차가 중심인 독립 진단 문제 |
| 통합 loop test·records·여러 Topic handoff | Pack의 대표 expected question에서는 제외 후보 | 여러 소유권을 나열해 단일 문제 답안을 흐림. 필요하면 field checklist/학습용 교차참조로만 보존 |

이 disposition은 의미상 범위 제안이다. 기존 routing pattern을 삭제하거나 바꾸는 source
수정은 하지 않았으며, 후속 변경 전 각 독립 문제의 현행 owner와 aliases를 함께 확인해야
한다. 40개 Anchor 중 accessory·diagnosis·procedure용 지식을 무조건 폐기하지 않는다.
별도 unit, 이웃 Topic handoff 또는 비채점 참고자료 중 하나로 추적한다.

## 4. Smart Positioner 경계

이 Pack은 **전통적인 pneumatic/electropneumatic positioner의 구조와 동작**을 중심으로
한다. Smart positioner의 digital communication, embedded diagnostics, valve signature,
friction trend와 predictive maintenance는 이미 별도 Pack인
`smart_positioner_diagnostics_valve_signature_predictive_maintenance`로 넘긴다.
현 Pack의 `smart_diagnostics_topic12_handoff`는 범위 경계 근거로 유지한다.

## 5. 후속 source 변경 안전조건

패턴별 existing/new owner 검토 결과는
[`positioner_topic_transfer_review_20261006.md`](positioner_topic_transfer_review_20261006.md)에
기록했다. 핵심 권고는 기존 Pack을 전통 포지셔너 구조·작동으로 좁히고, 공압 부속기기용 새
Pack 후보를 두며, 상세 교정·정비 후 진단은 기존 valve-maintenance Pack과 함께 이관을
검토하는 것이다. Split-range는 기존 control-loop architecture Pack과 device-local mapping을
분리한다.

1. Pack을 중심 문제로 좁히려면 expected pattern과 Anchor를 함께 재구성하고 각 제거 항목의
   새 owner를 기록한다. Anchor 삭제만으로 coverage를 맞추지 않는다.
2. Split-range·accessory·교정·진단 후보는 기존 82개 inventory에서 owner/alias 중복을
   확인한다. 실제 분리가 필요하면 관리된 `add-topic` workflow를 쓰고 draft 상태로 둔다.
3. Topic Sheet/README/JSON의 대표 문제·요구축·Fact Anchor·outline 연결을 일치시킨다.
4. Topic별 validator, Router 충돌/회귀 검사와 전체 release validator를 수행한다.
5. 기존 score contract, deterministic scoring, canonical Question Type, Router authority,
   fatal handling 또는 golden/release gates는 변경하지 않는다.
6. Source JSON을 사람이 실제 검토하기 전까지 managed approval/promote를 기록하지 않는다.

## 6. 검증 한계

- 이 검토는 현재 source JSON의 구조와 기존 Topic Sheet/경계 표기를 비교한 것이다. 이후
  README/Topic Sheet에는 대표 문제와 coverage를 추가했으나 machine-consumed JSON은 그대로다.
- 출처 본문으로 포지셔너 내부 구조의 기술 정확성이나 시험 출제 빈도를 독립 검증하지 않았다.
- WP/교재의 정확한 문서 위치와 판본을 연결한 citation coverage가 아직 부족하다.
- 따라서 본 문서는 재구성 방향을 확정하는 구조 검토안이지, source JSON 기술 승인이나
  채점 승인이 아니다.
