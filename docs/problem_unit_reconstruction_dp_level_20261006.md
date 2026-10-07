# 차압식 레벨 측정 Topic Pack 문제 단위 재구성 검토

검토일: 2026-10-06
대상: `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
상태: **기존 사용자 변경 보존, 문제 경계 검토안 — Pack source는 추가 수정하지 않음**

## 1. 결론

기존 Pack은 10개 예상 질문 패턴을 보유하고 있다. 현재 작업본은 3개 Tank Expert/
compensated-interface Anchor 및 2개 예상 패턴을 추가해 28개 Anchor가 되었다. 새 지식은
기존 관련 지식과 연결되어 있고, Sight Glass·Float·Bubbler 상세를 각 독립 Pack에 위임한
현재 경계도 적절하다. 이 변경은 보존한다.

다만 10개 패턴은 한 문항의 단순 조건 변형이 아니다. 차압 측정 원리와 교정, Remote Seal,
계면, Tank Expert 계산, 도압관 오차, 기술선정 등 답안 골격이 구별되는 문제 후보들이다.
따라서 이 Pack은 현재 하나의 문제 단위가 아니라 **관련된 여러 차압 레벨 Problem Unit을
묶은 상위 knowledge cluster**다. 기존 Topic ID를 보존한 채 대표 문제 한 문장으로 모두
대표한다고 주장하지 말고, 우선 다음 하위 단위를 식별해 이후 관리된 분리 여부를 결정한다.

## 2. 문제 단위 후보와 coverage

| 후보 Problem Unit / 대표 예상 문제 | 필수 연결 지식 | 현재 Anchor 연결 | 판정 |
|---|---|---|---|
| **A. 차압식 레벨의 구성·측정원리와 교정:** “개방/밀폐탱크에서 차압식 레벨 측정 원리를 설명하고 Dry/Wet Leg, 밀도변화 및 설치수두를 고려한 LRV/URV 교정과 오차대책을 설명하시오.” | 정수압 → 탭/기상압 조건 → leg 구성 → 고정수두와 운전밀도 → LRV·URV → 오차/대책 | `dp_level_hydrostatic_pressure_principle`, `dp_level_open_tank_equation`, `dp_level_closed_tank_vapor_pressure_cancellation`, `dp_level_dry_leg_configuration`, `dp_level_wet_leg_reference_head`, `dp_level_density_compensation`, `dp_level_process_temperature_density_error`, `dp_level_reference_elevation_and_span`, `dp_level_calibration_lrv_urv`, `dp_level_impulse_line_blockage_leak_bubble`, `dp_level_impulse_line_freezing_and_heat_tracing`, `dp_level_transmitter_mounting_elevation_error` | 하나의 적용형 종합문제로 성립. #1–4, #7 일부가 이 후보에 연결됨. 정확한 대표 범위/분량은 작성자 검토 필요 |
| **B. Remote Seal/Capillary 적용·오차:** “Remote Diaphragm Seal의 구조와 적용 목적을 설명하고 충전액 수두·온도·모세관 비대칭 및 응답 영향을 설명하시오.” | 격리막-충전액-모세관 전달, 설치 높이차, 온도/밀도, 양측 대칭, 응답시간과 적용상 tradeoff | `dp_level_remote_seal_structure`, `dp_level_remote_seal_fill_fluid_head`, `dp_level_remote_seal_temperature_error`, `dp_level_capillary_length_symmetry`, `dp_level_capillary_response_time` | 답안 중심이 독립적이어서 분리 후보. 기존 계기 설치/오차 문제의 인접 owner와 중복 조사 필요 |
| **C. 두 액체 계면 차압:** “고정 탭 간격의 두 액체 계면에서 차압식 원리·감도·상부 탭 보상조건 및 적용 한계를 설명하시오.” | 정수압 정리, 두 밀도층, 계면 높이와 ΔP, 밀도차에 따른 span, 탭 침수조건/전체수두 상쇄, 층분리·에멀전 한계 | `dp_level_interface_density_difference`, `dp_level_interface_total_level_condition`, `dp_level_interface_compensated_taps` | 새 상부 탭 계산 패턴(#10)은 기존 #6을 구체화하므로 한 unit의 변형/심화로 합치는 것이 타당 |
| **D. Tank Expert 세 압력법:** “하부·중간·상부 압력을 이용해 균일액 밀도와 레벨을 산출하는 원리, 설치수두 보정과 유효조건을 설명하시오.” | 동일 액체·균일밀도 조건에서 하부-중간 압력차로 밀도 산출, 상부 기준압/상부 기상압으로 높이 산출, 탭 간격과 침수 여부, 상수/단위 및 무효조건 | `dp_level_three_pressure_density`, `dp_level_three_pressure_level` | 독립 계산/계측 배열에 대한 예상 문제로 별도 unit 후보. 보유 source에서 표기·측정 압력 정의 추가 확인 필요 |
| **E. 측정 방식 선정 비교:** “차압식과 Radar/GWR 레벨 측정의 원리·적용조건·오차요인을 비교해 방식을 선정하시오.” | 차압의 밀도·탭·도압관 영향; Radar/GWR의 유전율·반사/에코/프로브 조건; 매질/설비/유지보수 기반 선택 | `dp_level_selection_against_radar_gwr` 및 Radar Pack 연계 | 비교 기준과 Radar/GWR owner를 함께 보아야 함. 현재 단일 Anchor만으로 상세 비교 coverage가 충분하다고 볼 수 없으므로 이 Pack의 대표문제로 유지하기보다 cross-topic 문제 후보 |

## 3. 기존 10개 패턴의 권고 배치

| 번호 | 기존 질문 축 | 권고 배치 |
|---:|---|---|
| 1 | 정수압·개방/밀폐탱크 | A의 기본 원리 |
| 2 | Dry/Wet Leg와 교정범위 | A의 구성/고정수두 |
| 3 | Wet Leg Zero Elevation | A의 교정 특수 변형 |
| 4 | 밀도 변화 오차/보정 | A의 적용 조건 |
| 5 | Remote Seal 구조·온도오차 | B로 분리 후보 |
| 6 | 차압 계면 원리/적용조건 | C의 기본 문제 |
| 7 | 도압관/설치오차 | A의 설치·진단 축. 범위가 커지면 별도 설치오류 문제 후보 |
| 8 | DP와 Radar/GWR 비교 | E cross-topic 문제 후보; Radar owner 확인 필요 |
| 9 | Tank Expert 3-pressure density/level | D로 분리 후보 |
| 10 | 두 액체 계면 상부 탭 compensation/span | C의 조건부 심화 변형으로 유지 |

현재 Anchor-ID union coverage가 89%라는 screen 수치는 요구 충족률이 아니다. #5/#9/#10
추가에 따라 연결률이 변했을 수 있으므로, 후속 source 수정 전 CSV를 재생성해야 한다.

## 4. 출처와 검증 한계

- 이 작업본은 WordPress `Chapter 20`을 근거로 추가했다고 기록되어 있고, 새 식에는 침수·균일밀도·고정 탭 간격 등의 적용 조건이 명시돼 있다.
- 본 검토에서는 WordPress 원문·OCR 도표를 대조하지 않았다. 따라서 새 계산식의 source 위치, 변수 정의, 실제 그림 배열과 범위는 아직 검증되지 않았다.
- 기존 문서 diff에 수식 표기의 비정상 이스케이프/줄바꿈 흔적이 보인다. 이를 임의로 복구하지 않았으며, 렌더된 수식과 JSON 원문이 별도로 검증되어야 한다.
- 정량 예시는 단위가 inH₂O 수두인지 SI 압력인지 분리해 유지해야 한다. (36\,in\times(1.1-0.78)=11.52\,inH_2O\)는 수두 span이며, Pascal 변환에는 물의 밀도와 중력가속도를 곱해야 한다.
- 공식 기출 출처를 확인하지 않았으므로 위 다섯 문장은 출제 가능성을 구성한 예상 문제 단위 후보이지, 과거 기출 사실이 아니다.

## 5. 후속 변경 안전조건

1. 현재 사용자 수정과 Chapter 20 보강 Anchor를 그대로 보존한다.
2. A–E를 실제 별도 Pack으로 분리하기 전에 82개 inventory에서 기존 owner, aliases,
   Router hit, 학습/진단 참조와 source overlap을 조사한다.
3. 특히 D(세 압력법)는 새 Anchor 2개가 충분한지, 변수·압력 탭 위치·reference datum이
   원문 도식과 정확히 대응하는지 source를 확인한다.
4. E는 Radar Pack의 비교 Anchor·question demand와 합쳐도 한 문제의 일관된 답안이 되는지
   평가한다. 단일 selector Anchor를 과도한 coverage로 간주하지 않는다.
5. Pack 분할 시 기존 Topic ID를 폐기하거나 routing authority를 임의 이동하지 않는다.
   신규 Topic은 `add-topic` workflow로 draft 생성하고, focused Router/alias와 전체
   release validator를 수행한다.
6. 사람의 실질 source review 전에 approval/promote는 기록하지 않는다.

## 6. 작업본 보존 관련 참고

기존 작업 트리에 있는 Topic Sheet·README·Fact Anchor·Model Answer 변경은 이번 검토에서
수정하지 않았다. 단, 해당 README의 “Fact Anchors: 28”과 원본 release/runtime 문맥이
같이 바뀐 상태이므로 source/runtime authority 표기가 프로젝트 기준과 일치하는지 별도
diff review 및 validator에서 확인해야 한다. 이 문서는 그 기존 diff를 승인하거나 기술적으로
검증했다는 뜻이 아니다.
