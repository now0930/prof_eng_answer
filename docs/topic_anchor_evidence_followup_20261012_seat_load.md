# Seat load damage Anchor 근거 재검토 (2026-10-12)

## 결과

`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`의
`excessive_seat_load_damage`는 **미검증으로 유지**한다. 현재 Anchor는 과도한 seat load가
seat·plug deformation, indentation, galling, wear와 actuator demand를 증가시킬 수 있다고
열거한다. 검토한 제조사 근거는 적정/필요 seat load와 seating-force 절차를 설명하지만, 이
열거 전체의 원인·결과를 직접 입증하지 않는다.

## 확인 근거와 모순 가능성

- Emerson/Fisher, *Control Valve Sourcebook—Oil and Gas*, §2.2, “Force to Provide Seat Load”,
  Table 2-2, p. 2-8: seat load를 shutoff requirement에 연계하고 actuator sizing에 고려하도록
  한다. 또한 seat life와 shutoff capability 보존을 위해 recommended seat load보다 높은 값을
  사용하라고 기술한다. 따라서 “seat load가 크면 항상 seat life/wear가 나빠진다”는 일반화의
  근거로는 사용할 수 없으며, 현재 Anchor의 포괄적 인과 주장과 긴장이 있다.
- Emerson/Fisher, *HPA Valve with Pressure Seal Bonnet Instruction Manual* D104745X012
  (Jan. 2023), p. 16: 해당 HPA 제품의 initial seating에 actuator sizing 시 계산한 full-load와
  같은 force를 사용하라고 한다. 충분하지 않은 seating force는 excessive leakage와 seat
  erosion을 피하지 못할 수 있다고 설명한다. 이는 제품별 절차이지, 과도한 force가 열거된
  손상 모두를 일으킨다는 근거는 아니다.

## 판정 및 후속 조치

기존 주장을 verified 처리하지 않는다. 문장을 유지하려면 soft seat의 압축변형, metal seat의
galling 등 재료·trim별 메커니즘을 분리하고, 특정 제품·설계에서 제조사가 정한 최대 thrust 또는
seat-load 초과가 실제 손상을 일으킨다는 직접 근거를 각각 확보해야 한다. 일반적인 actuator
force 증가만으로 seat deformation, indentation, galling 및 wear를 모두 추론하지 않는다.

이번 검토는 근거 기록만 수행했다. Topic Pack 문구·점수 계약은 변경하지 않았다.
