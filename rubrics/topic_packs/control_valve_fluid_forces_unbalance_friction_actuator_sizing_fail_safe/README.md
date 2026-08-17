# 제어밸브에 작용하는 유체력, 불평형력, 마찰력과 액추에이터·Fail-Safe 설계

## Topic metadata

- Topic ID: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Grading mode: `LLM_ONLY`
- Deterministic checks: disabled

## Scope

직동식 sliding-stem 글로브 제어밸브의 가동부에 작용하는 힘을
자유물체도와 힘 평형으로 해석한다.

- 압력력과 유체 불평형력
- Pressure-Tends-to-Open 및 Pressure-Tends-to-Close
- FTO·FTC와 트림 형상
- Balanced 및 unbalanced trim
- 패킹·가이드·breakaway 마찰력
- 시트 하중
- 공압 액추에이터와 스프링 힘
- Bench set과 operating range
- Fail-Close 및 Fail-Open
- 최악조건 액추에이터 선정
- 회전식 밸브의 토크 해석 경계

## Ownership boundary

- 본 Topic은 sliding-stem 제어밸브의 유체력, 유효면적, 마찰, 시트 하중, actuator 요구추력, spring force, Bench set과 operating range의 차이를 소유한다.
- `balanced_trim_unbalanced_trim_structure_sealing_applications`는 balance hole·pressure communication·balance seal·residual force 및 적용조건을 소유한다.
- `control_valve_positioner_ip_converter_booster_accessories_calibration`는 valve-actuator coupling 이후 positioner linkage·action·zero·span·multipoint calibration 및 loop test를 소유한다.
- `control_valve_types_globe_rotary_body_actuator_selection`는 valve body와 actuator 종류 및 일반 선정 taxonomy를 소유한다.
- 회전식 밸브의 상세 actuator sizing은 torque basis와 vendor data를 사용하며 sliding-stem force equation을 그대로 적용하지 않는다.

## Source inventory

- Fact Anchors: 22
- Fatal misconception contracts: 12
- Rich question patterns: 10
- Recommended Outline sections: 6

## Grading policy

Logic Check는 Topic 신뢰도 판단에 사용한다.

Fatal 오류가 있으면 Topic trust를 `limited`로 본다.

Logic Check 결과는 D/E 점수에 직접 반영하지 않는다.
