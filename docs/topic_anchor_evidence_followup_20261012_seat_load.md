# Seat load damage Anchor 근거 재검토 (2026-10-12)

## 최초 검토 결과와 후속 정정

최초 검토에서는 “과도한 seat load가 deformation, indentation, galling, wear 및 actuator demand를
보편적으로 증가시킨다”는 넓은 주장을 **미검증**으로 판단했다. 이후 2026-10-12 근거 검토에서
이 포괄 주장을 삭제하고, Fisher HP/HPA의 지정 C-seal·bore-seal trim에 관한 제조사별 seating-force와
travel 절차로 Anchor를 좁혔다. 기존의 보편적 손상 주장은 여전히 검증되지 않은 것으로 취급한다.

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

## 최초 판정의 적용 범위

기존 주장을 verified 처리하지 않는다. 문장을 유지하려면 soft seat의 압축변형, metal seat의
galling 등 재료·trim별 메커니즘을 분리하고, 특정 제품·설계에서 제조사가 정한 최대 thrust 또는
seat-load 초과가 실제 손상을 일으킨다는 직접 근거를 각각 확보해야 한다. 일반적인 actuator
force 증가만으로 seat deformation, indentation, galling 및 wear를 모두 추론하지 않는다.

위 최초 판정은 보편적 과부하 손상 주장의 범위다. 현재 Pack의 좁힌 Anchor는
`grading/evidence/approved_fact_registry.json`의
`fisher_hp_hpa_cseal_overtravel_can_reduce_seat_load_and_damage_trim`으로 추적하며, score effect는 none이다.
회귀 테스트는 지정 제품·trim, 초기 seating force, overtravel 및 일반화 금지 경계를 검사한다.
