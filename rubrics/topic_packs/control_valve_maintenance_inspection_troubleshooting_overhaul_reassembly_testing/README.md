# 제어밸브 정비·점검·고장진단·분해정비·재조립 및 시험

- Topic ID: `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing`
- Official criterion: `CV-MAINT-01`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `CORE_MUST_PREPARE`
- Historical frequency used: `false`

## Scope

이 Topic은 제어밸브의 **현장 정비 실행 절차**를 소유한다.

핵심 범위는 다음과 같다.

1. 작업허가, LOTO, 감압·배출·세정과 zero-energy 확인
2. Tag·방향·설치상태·signal·air supply·travel·누설의 as-found 기록
3. Stick-slip·deadband·hunting·누설·응답지연·fail-action 불량의 증상 분류
4. 외부 원인 배제 후 valve·actuator 내부 failure mode 진단
5. 표시·추적성을 유지한 분해, 세정과 오염관리
6. Plug·seat·cage·stem·guide·body 손상 및 치수검사
7. Repair·replace·lapping과 packing·gasket·seal 복원 판단
8. 정렬·torque·seat endpoint·rated travel·mechanical stop 복구
9. Pressure-boundary·seat leakage·stroke·fail-action 시험
10. Return-to-service, as-left 기록과 specialist hand-off

## Boundary

- `control_system_operations_maintenance_calibration_inspection_spares_kpi`는 정비전략, criticality, CMMS/EAM, 작업지시, 주기, 예비품, KPI, 조직 RCA와 O&M governance를 소유한다.
- `control_valve_positioner_ip_converter_booster_accessories_calibration`는 actuator bench set, linkage·cam, direct·reverse action, zero·span, multipoint calibration과 loop test의 상세 교정 절차를 소유한다.
- `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`는 shutoff class 선정, packing-system 설계, fugitive-emission 규격·인증과 측정기준을 소유한다.
- `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`는 Cv/Kv sizing, body·trim·actuator·material 선정, 공정조건과 lifecycle procurement decision을 소유한다.
- 이 Topic은 위 전문판단을 반복하지 않고 현장 손상증거, 정비결과, limitation과 재검토 필요성을 stable Topic ID로 hand-off한다.

## Maintenance sequence

1. 작업범위·permit·isolation point와 stored energy를 확인한다.
2. 분해 전 as-found 상태와 증상을 동일 시험조건으로 기록한다.
3. Signal·air supply·tubing·positioner·actuator·process disturbance 등 외부 원인을 먼저 배제한다.
4. Orientation·coupling·부품 순서와 방향을 표시하고 지정 절차로 분해한다.
5. 유체 특성에 맞게 세정하고 sealing surface와 내부 통로를 보호한다.
6. 손상형태와 치수를 허용기준에 비교하여 repair·replace·lapping을 결정한다.
7. Packing·gasket·seal을 적합한 재질·방향·preload로 복원한다.
8. Stem·plug·seat·cage·actuator를 정렬하고 지정 순서·torque로 재조립한다.
9. Pressure boundary, seat leakage, up/down stroke와 fail-action을 별도 acceptance로 시험한다.
10. 보호장치와 배관을 복구하고 as-left·교체부품·시험결과·승인자를 기록한다.

## Acceptance evidence

- As-found와 as-left는 같은 기준과 시험조건으로 비교한다.
- Pressure, leakage, stroke와 fail-action은 계측기, 유체, 압력, 온도, 방향, 유지시간과 허용기준을 기록한다.
- 반복고장이나 sizing·selection·calibration·certification 문제는 현장 증거와 limitation을 specialist Topic으로 전달한다.
- Pass/fail만 기록하지 않고 부품상태, 치수, 수리판단, 교체부품과 승인 근거를 남긴다.

## Routing aliases

- `control valve maintenance inspection overhaul testing`
- `control valve troubleshooting repair reassembly`
- `control valve disassembly inspection reassembly sequence`
- `control valve overhaul procedure`
- `control valve maintenance procedure`
- `control valve post maintenance testing`
- `control valve pressure leak stroke test`
- `control valve repair replace lapping decision`
- `control valve as found as left maintenance record`
- `control valve 반복고장 원인분석`
- `제어밸브 정비 절차`
- `제어밸브 점검 분해 조립 시험`
- `제어밸브 overhaul`
- `제어밸브 고장진단`
- `제어밸브 정비 후 시험`
- `제어밸브 누설 stroke fail action 시험`

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank는 source focused validation 이후 repository generator로만 갱신한다.
