# 제어밸브 정비·점검·고장진단·분해정비·재조립 및 시험

## 1. Topic 정보

- Topic ID: `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing`
- Official criterion: `CV-MAINT-01`
- Primary: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Importance: `CORE_MUST_PREPARE`

## 2. Topic 소유 범위

이 Topic은 제어밸브의 현장 정비 실행 절차를 소유한다.

핵심 범위는 안전격리, as-found 기록, 고장진단, 분해·세정·검사, 수리·교체 판단, 재조립, 정비 후 시험, 복구와 as-left 기록이다.

## 3. 전체 정비 절차

```text
작업허가·LOTO·감압
  → as-found 기록
  → 증상 분류와 외부 원인 배제
  → 표시·분해·세정
  → 손상·치수 검사
  → repair·replace·lapping 판단
  → seal 복원과 재조립
  → pressure·leakage·stroke·fail-action 시험
  → 복구·as-left 기록·specialist hand-off
```

## 4. 안전격리

1. 작업허가와 작업범위를 확인한다.
2. Isolation point와 bypass 상태를 확인한다.
3. 전기·공기·유압·스프링 등 저장에너지를 격리한다.
4. 감압·배출·세정을 수행한다.
5. Zero-energy 상태를 확인한 뒤 분해한다.

## 5. As-Found 기록

분해 전 상태를 동일 시험조건으로 기록한다.

- Tag와 설치 방향
- Signal과 air supply
- Valve travel과 endpoint
- Internal·external leakage
- 소음·진동
- Stick-slip·deadband·hunting
- Fail-action과 accessory 상태

As-found는 정비 후 as-left와 비교하는 기준이다.

## 6. 고장진단 순서

증상과 원인을 구분한다.

1. Stick-slip, deadband, hunting, 누설, 응답지연과 fail-action 불량을 분류한다.
2. Signal, air supply, tubing과 process disturbance를 확인한다.
3. Positioner와 actuator 등 외부 원인을 먼저 배제한다.
4. 외부 원인 배제 후 valve 내부 failure mode를 진단한다.
5. 반복고장은 현장 증거와 limitation을 남겨 specialist Topic으로 전달한다.

## 7. 분해와 추적성

- Orientation과 flow direction을 표시한다.
- Stem·plug·seat·actuator coupling 위치를 표시한다.
- 부품 순서와 방향을 기록한다.
- 지정된 분해 절차와 전용 공구를 사용한다.
- Sealing surface와 정밀 부품을 보호한다.

## 8. 세정과 부품검사

유체 특성에 맞게 세정하고 이물 재유입을 방지한다.

검사 대상:

- Plug·seat·cage
- Stem·guide
- Body와 bonnet
- Packing·gasket·seal
- Actuator coupling과 mechanical stop

손상 형태:

- Erosion·corrosion
- Cavitation·galling
- Crack·bending
- Surface damage
- Abnormal wear와 contamination

## 9. 치수와 수리 판단

다음 항목을 허용기준과 비교한다.

- Stem runout
- Guide clearance
- Seat contact
- Surface finish
- 주요 부품 치수와 마모량

Repair·replace·lapping은 손상 원인, 수리한계, 잔여수명, 부품가용성과 acceptance 기준으로 결정한다.

## 10. Seal 복원과 재조립

- Packing·gasket·seal의 재질과 방향을 확인한다.
- Packing preload와 stem friction의 trade-off를 관리한다.
- Stem·plug·seat·cage·actuator를 정렬한다.
- 지정 체결 순서와 torque를 적용한다.
- Seat endpoint, rated travel과 mechanical stop을 복구한다.
- Overtravel과 binding을 방지한다.

## 11. 정비 후 Acceptance Test

### 11.1 Pressure-Boundary Test

Pressure boundary 건전성을 지정 압력, 유체, 유지시간과 안전조건으로 확인한다.

### 11.2 Seat Leakage Test

요구 차압, 유체, 방향, 측정조건과 허용기준을 기록한다.

Pressure-boundary test와 seat leakage test는 목적이 다르다.

### 11.3 Stroke Test

0·25·50·75·100%의 upstroke와 downstroke를 확인한다.

- Rated travel
- Friction
- Hysteresis
- Deadband
- Response
- Endpoint repeatability

### 11.4 Fail-Action Test

Signal·air·power loss에서 fail position을 확인한다.

Solenoid, booster와 기타 accessory 기능도 실제 조건으로 확인한다.

## 12. Return-to-Service와 As-Left

1. 보호장치와 배관을 복구한다.
2. 최종 누설과 stroke를 확인한다.
3. As-left 값을 기록한다.
4. 교체부품과 수리내용을 기록한다.
5. 시험조건, 허용기준, 결과와 승인자를 기록한다.
6. 반복고장과 전문판단 대상은 stable Topic ID로 hand-off한다.

## 13. Acceptance Evidence

Pass·fail만 기록하지 않는다.

다음을 추적 가능하게 남긴다.

- As-found와 as-left
- 계측기와 시험유체
- 압력·온도·방향·유지시간
- 치수와 부품상태
- 수리·교체·lapping 판단
- 교체부품
- 시험결과와 승인 근거

## 14. 주요 Trade-Off

- Packing preload 증가 ↔ stem friction 증가
- Tight shutoff 확보 ↔ trim·seat 손상 위험
- 현장 수리 ↔ 전문 workshop 또는 vendor hand-off
- Repair ↔ replace의 비용·납기·잔여수명
- 빠른 복구 ↔ 충분한 진단·시험·기록

## 15. Topic 경계

- `control_system_operations_maintenance_calibration_inspection_spares_kpi`: 정비전략, CMMS/EAM, 주기, 예비품, KPI와 O&M governance
- `control_valve_positioner_ip_converter_booster_accessories_calibration`: bench set, linkage·cam, action, zero·span와 상세 교정
- `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`: shutoff class, packing-system 설계와 fugitive-emission 규격
- `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`: sizing, body·trim·actuator·재질 선정과 lifecycle decision

이 Topic은 현장 손상증거, 정비결과와 limitation을 위 전문 Topic으로 전달한다.

## 16. 대표 오답

- 작업허가와 감압 없이 바로 분해한다.
- As-found 기록 없이 정비 후 결과만 제시한다.
- 외부 원인을 배제하지 않고 valve 내부를 먼저 분해한다.
- 치수 허용기준 없이 육안으로만 판정한다.
- Pressure test와 seat leakage test를 같은 시험으로 취급한다.
- Endpoint만 확인하고 multipoint up·down stroke를 생략한다.
- Fail-action을 문서로만 확인하고 실제 시험하지 않는다.
- 반복고장을 현장 정비만으로 종결하고 specialist hand-off를 생략한다.

## 17. 고득점 답안 기준

1. 안전격리와 zero-energy 확인을 선행조건으로 제시한다.
2. As-found와 as-left를 동일 조건으로 비교한다.
3. 외부 원인 배제 후 내부 failure mode를 진단한다.
4. 분해·세정·검사·수리·재조립 순서를 추적 가능하게 설명한다.
5. 손상형태와 치수 허용기준을 함께 제시한다.
6. Repair·replace·lapping 판단기준을 제시한다.
7. Packing preload와 friction trade-off를 설명한다.
8. Pressure, leakage, stroke와 fail-action 시험을 분리한다.
9. 시험조건, 허용기준, 결과와 승인자를 기록한다.
10. 인접 전문판단을 stable Topic ID로 hand-off한다.
