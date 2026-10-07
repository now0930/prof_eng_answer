# RTD Topic Pack 문제 단위·coverage 재검토

일자: 2026-10-07
대상: `rtd_temperature_sensor_principle_pt100_wiring_compensation`
감사 기준: `docs/topic_pack_problem_unit_screen_20261006.csv`의 coverage 재검토 후보

## 판정

RTD를 측정원리·결선보상·자기발열을 연결하는 하나의 학습 지식 단위로 유지한다.
다만 서로 다른 대표 질문의 필수범위를 섞어 채점하지 않도록 패턴별 required anchor를
문제 범위의 authority로 명시했다. Transmitter, 설치/동적응답, 교정/불확도/진단은
유용한 보조지식이나, 현재 대표 질문에서 직접 요구하지 않으면 고득점 필수조건이나
누락 감점 항목이 아니다.

## 패턴과 필수 anchor

| 대표 문제 패턴 | 필수 anchor | 개수 |
|---|---|---:|
| RTD 측정원리와 Pt100 특성 | `rtd_temperature_measurement_chain`, `rtd_metal_resistance_temperature_principle`, `rtd_pt100_reference_resistance_alpha_standard`, `rtd_callendar_van_dusen_characteristic` | 4 |
| Pt100 2/3/4선식 결선과 리드선 보상 | `rtd_two_wire_lead_resistance_error`, `rtd_three_wire_bridge_compensation_assumptions`, `rtd_four_wire_kelvin_measurement`, `rtd_wiring_method_selection_tradeoff` | 4 |
| 측정전류, 자기발열, 결선 선정 | `rtd_excitation_voltage_measurement`, `rtd_self_heating_thermal_error`, `rtd_wiring_method_selection_tradeoff` | 3 |

현재 패턴 required-anchor union은 14개 중 10개(71.4%)다. 나머지 4개는 transmitter
연결/신호조절, thermowell·동적응답, 교정·불확도, 고장진단이다. 이 비율은 “Topic Pack
지식의 완성도 점수”가 아니라 대표 문제 문구에 직접 연결된 필수 anchor 비율이다.
다른 문제 패턴이 실제로 채택되면 해당 질문의 필수 anchor를 별도로 정의해야 한다.

## 수정 사항

- 세 번째 패턴에서 고장진단을 required 목록에서 제거했다. 해당 문구는 측정전류·자기발열·
  결선선정을 요구할 뿐 RTD fault diagnostics나 loop check를 요구하지 않는다.
- `high_score_points`, `common_missing_points`, 중요도 unlock 조건에 패턴 조건을 명시했다.
  모든 RTD 답안에 전체 14 anchor를 요구하지 않으며, 무관한 omitted fact로 감점하지 않는다.
- 14개 fact anchor와 기존 fatal 기술 오류는 유지했다. 질문에서 관련 오개념이 실제로
  나타난 경우에는 해당 fatal 근거를 계속 사용할 수 있다.
- Question Type, scoring contract, Router, deterministic scoring, fatal ID, release gate는
  수정하지 않았다.

## 검증 의도와 한계

이번 수정은 source schema와 pack quality, pattern/anchor 참조 일관성을 검증한다. 채점
엔진이 개별 pattern required IDs를 완전하게 hard-scope하는지에 대한 별도 런타임 보증은
추가하지 않았으므로, 문서와 Topic Pack의 요구 경계를 명시한 것으로 해석한다.
