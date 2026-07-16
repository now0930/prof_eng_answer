# 제어밸브에 작용하는 유체력, 불평형력, 마찰력과 액추에이터·Fail-Safe 설계

## 1. Topic 기본정보

- Topic ID: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- 국문 제목: 제어밸브에 작용하는 유체력, 불평형력, 마찰력과 액추에이터·Fail-Safe 설계
- Question Type: `PRINCIPLE_INTERPRETATION`
- Theory Depth: `FIELD_APPLICATION`
- Preparation Priority: `NORMAL`
- Grading Mode: `LLM_ONLY`
- Deterministic Check: 비활성화
- Logic Check: D/E 점수에 직접 반영하지 않고 Topic trust 판단에 사용

## 2. 대표 시험문제

제어밸브가 유체 중에서 동작할 때 플러그와 스템에 작용하는 힘을 자유물체도로 나타내시오.

유체 불평형력, 패킹 및 가이드 마찰력, 시트 하중과 액추에이터 구동력의 관계를 설명하시오.

공압식 액추에이터 선정과 Fail-Close 및 Fail-Open 스프링 설계 시 고려사항을 설명하시오.

## 3. 분석 대상과 범위

### 3.1 주 분석 대상

직동식 Sliding-Stem 글로브형 제어밸브를 주 분석 대상으로 한다.

자유물체도에서는 다음 가동부를 하나의 물체로 고립한다.

- 플러그
- 밸브 스템
- 액추에이터 스템
- 연결부
- 필요 시 다이어프램 또는 피스톤 가동부

### 3.2 포함 범위

- 상류압력 `P1`과 하류압력 `P2`
- 플러그 표면에 작용하는 압력력
- 유체 불평형력
- Pressure-Tends-to-Open
- Pressure-Tends-to-Close
- Unbalanced trim
- Balanced trim
- 스템 및 balance seal 유효면적
- 패킹 마찰력
- 플러그·케이지·가이드 마찰력
- Breakaway friction
- Running friction
- 시트 하중
- 액추에이터 공압력
- 스프링 예압과 스프링 레이트
- Bench set
- Operating range
- Fail-Close
- Fail-Open
- 액추에이터 사이징
- 동적 유체력과 측면하중
- 회전식 밸브의 토크 해석 경계

### 3.3 제한 범위

다음 항목은 개념 경계만 설명한다.

- 회전식 밸브의 상세 토크 계산
- 캐비테이션 상세 계산
- 초크 유동 상세 계산
- 소음 예측
- 유량계수 계산
- 스프링 재료 상세 설계
- CFD 및 유한요소해석

## 4. 자유물체도 기본 원칙

### 4.1 좌표계

밸브 스템의 이동축을 `x`축으로 설정한다.

예를 들어 밸브가 열리는 방향을 `+x`로 정한다.

힘의 부호는 이 좌표축과 실제 힘의 방향에 따라 결정한다.

### 4.2 주요 힘

- 액추에이터 힘: `F_act`
- 스프링 힘: `F_s`
- 유체 불평형력: `F_u`
- 패킹 마찰력: `F_pack`
- 가이드 마찰력: `F_guide`
- 시트 반력: `R_seat`
- 요구 시트 하중: `F_seat`
- 가동부 중량의 축방향 성분: `W_x`
- 동적 유체력: `F_dyn`

시트와 접촉하지 않은 정지 상태의 일반 평형식은 다음과 같다.

`ΣF_x = F_act + F_s + F_u + F_pack + F_guide + W_x + F_dyn = 0`

각 항은 실제 방향에 따라 양 또는 음의 부호를 갖는다.

## 5. 압력력과 유체 불평형력

### 5.1 압력력의 기본식

압력은 젖은 표면에 수직으로 작용한다.

밸브 이동축 방향의 순 압력력은 다음과 같이 표현한다.

`F_p = ∫ p n_x dA`

- `p`: 국부 압력
- `n_x`: 표면 법선의 이동축 방향 성분
- `dA`: 미소 면적

### 5.2 단순 근사식

압력 분포와 유효면적을 단순화할 수 있는 경우 다음 근사식을 사용한다.

`F_u ≈ ΔP A_eff`

`ΔP = P1 - P2`

`A_eff`는 트림 형상과 압력 경계로 결정되는 유효 투영면적이다.

`A_eff`를 모든 밸브에서 포트 면적과 동일하게 취급하면 안 된다.

### 5.3 일반 유효면적식

여러 압력 작용면이 존재하면 다음과 같이 표현한다.

`F_u = Σ(P_i A_i)_positive - Σ(P_j A_j)_negative`

다음 항목을 검토한다.

- 포트 면적
- 플러그 상부와 하부 면적
- 스템 단면적
- balance seal 직경
- 압력 평형 구멍
- 플러그 개도
- 상부 및 하부 압력 분포

## 6. Pressure-Tends-to-Open과 Pressure-Tends-to-Close

### 6.1 Pressure-Tends-to-Open

유체 압력의 축방향 합력이 플러그를 시트에서 이탈시키는 방향으로 작용한다.

- 유체력이 개방을 보조한다.
- 폐쇄 시 액추에이터가 유체 불평형력을 이겨야 한다.
- 차단 시 요구 추력이 증가할 수 있다.

### 6.2 Pressure-Tends-to-Close

유체 압력의 축방향 합력이 플러그를 시트 방향으로 이동시킨다.

- 유체력이 폐쇄를 보조한다.
- 개방 시 스프링 또는 액추에이터가 불평형력을 이겨야 한다.
- Fail-Open 조건에서 불리할 수 있다.

### 6.3 FTO와 FTC 해석 원칙

FTO와 FTC를 단순히 아래에서 위 또는 위에서 아래로 흐르는 배관 방향으로 정의하지 않는다.

다음 요소를 함께 확인한다.

- 실제 유동 방향
- 플러그의 폐쇄 이동 방향
- 플러그와 시트의 상대 위치
- 트림 형상
- 압력 작용면
- 유체력이 플러그를 열거나 닫는 방향

답안에서는 Pressure-Tends-to-Open 또는 Pressure-Tends-to-Close를 먼저 판단한다.

## 7. Balanced Trim과 Unbalanced Trim

### 7.1 Unbalanced Trim

단순 싱글 시트 트림에서는 차압에 의한 순 압력력이 가동부에 크게 전달될 수 있다.

차단 조건에서 구조가 단순하면 다음 근사를 사용할 수 있다.

`F_u ≈ ΔP A_port`

단, 스템 면적과 다른 압력 작용면을 무시할 수 있는 조건이어야 한다.

### 7.2 Balanced Trim

Balanced trim은 서로 반대되는 플러그 면에 압력을 작용시켜 순 정적 불평형력을 줄인다.

장점:

- 요구 액추에이터 추력 감소
- 고차압 적용성 향상
- 액추에이터 크기 감소

잔류 영향:

- 스템 유효면적
- balance seal 유효면적
- 압력 평형 구멍의 압력손실
- seal ring 마찰
- 플러그 상하부의 잔류 차압
- 제조공차
- 개도별 동적 유체력

Balanced trim에서도 유체력이 완전히 사라지는 것은 아니다.

Balanced trim은 seal 마찰, 누설등급, 유지보수성과 함께 검토한다.

## 8. 정적 불평형력과 동적 유체력

### 8.1 정적 불평형력

정적 불평형력은 주로 압력과 유효면적의 관계로 평가한다.

대표적인 평가조건은 다음과 같다.

- 완전 폐쇄
- 시트 이탈 직전
- 낮은 유속
- 최대 차압

### 8.2 동적 유체력

밸브가 열린 상태에서는 압력 분포와 유체 운동량 변화로 동적 유체력이 발생한다.

- 제트 반력
- 축방향 유체력
- 비대칭 유동에 의한 측면하중
- 개도별 힘 변화
- 진동
- 가이드 접촉력 증가

동적 유체력은 패킹 마찰력과 동일한 항이 아니다.

### 8.3 유체 점성 전단력

유체가 플러그 표면을 따라 흐르며 만드는 점성 전단력은 존재한다.

그러나 다음 항과 구분한다.

- 압력에 의한 불평형력
- 운동량 변화에 의한 동적 유체력
- 패킹 및 가이드의 고체 접촉 마찰력

## 9. 기계적 마찰력

### 9.1 패킹 마찰력

패킹 마찰력은 스템과 패킹 사이에서 발생한다.

주요 영향요인은 다음과 같다.

- 패킹 재질
- 패킹 조임력
- 스템 직경
- 내부 압력
- 온도
- 윤활
- 마모
- 저배출 패킹 구조

### 9.2 가이드 마찰력

가이드 마찰력은 플러그, 케이지 또는 가이드 면에서 발생한다.

주요 원인은 다음과 같다.

- 조립 편심
- 스템 휨
- 유체 측면하중
- 이물질
- 마모
- 열팽창
- 가이드 간극 불량

패킹 마찰과 가이드 마찰은 발생 위치와 원인이 다르다.

### 9.3 Breakaway와 Running Friction

장시간 정지한 밸브가 움직이기 시작할 때 breakaway friction이 발생한다.

Breakaway friction은 운전 중 running friction보다 클 수 있다.

다음 현상과 연결한다.

- Stiction
- Deadband
- Hysteresis
- 방향 전환 지연
- Limit cycle
- Positioner 출력 포화

### 9.4 마찰력 방향

마찰력은 실제 운동 또는 임박한 운동의 반대 방향으로 작용한다.

- 플러그가 위로 움직이려 하면 마찰력은 아래로 작용한다.
- 플러그가 아래로 움직이려 하면 마찰력은 위로 작용한다.

마찰력의 방향을 액추에이터 힘만 보고 고정하면 안 된다.

## 10. 시트 하중과 차단

### 10.1 시트 하중

시트 하중은 플러그가 시트에 접촉한 후 요구 차단등급을 확보하기 위한 접촉력이다.

다음 힘과 구분한다.

- 플러그 이동력
- 불평형력을 이기는 힘
- 마찰력을 이기는 힘
- 최종 차단을 위한 접촉력

### 10.2 차단 시 요구 추력

Pressure-Tends-to-Open인 밸브를 닫는 개념식은 다음과 같다.

`F_required,close = F_u + F_f + F_seat`

`F_f = F_pack + F_guide`

실제 시트 하중은 제조사의 shutoff pressure 및 leakage class 자료를 적용한다.

### 10.3 시트 접촉 전후

- 이동 중: 시트 반력이 없다.
- 접촉 직후: 시트 반력이 발생한다.
- 완전 차단: 요구 시트 하중을 유지한다.

자유물체도는 접촉 전과 접촉 후를 구분한다.

## 11. 공압 액추에이터와 스프링

### 11.1 공압 구동력

다이어프램 또는 피스톤 액추에이터의 기본 힘은 다음과 같다.

`F_air = P_a A_a`

- `P_a`: 액추에이터 로딩 압력
- `A_a`: 유효 다이어프램 또는 피스톤 면적

유효면적은 스트로크에 따라 변할 수 있으므로 제조사 자료를 우선한다.

### 11.2 스프링 힘

선형 근사 시 스프링 힘은 다음과 같다.

`F_s(x) = F_preload + kx`

- `F_preload`: 초기 예압
- `k`: 스프링 레이트
- `x`: 추가 압축량

예압 조정과 스프링 레이트 변경은 서로 다른 개념이다.

### 11.3 가용 추력

액추에이터 구조와 이동 방향에 따라 다음과 같이 평가한다.

`F_available = F_air - F_s`

또는 스프링 힘이 요구 이동 방향을 보조하는 구조에서는 두 힘을 같은 방향으로 합산한다.

Air-to-Open, Air-to-Close와 스프링 방향을 먼저 확인한다.

## 12. Bench Set과 Operating Range

### 12.1 Bench Set

Bench set은 일반적으로 공정압력이 없는 기준조건에서 액추에이터 스프링을 완전 스트로크시키는 압력 범위이다.

- 밸브 몸체에 공정압력이 없다.
- 유체 불평형력이 없다.
- 액추에이터 스프링의 초기 압축 상태를 조정한다.
- 실제 운전부하가 없는 기준조건이다.

Bench set을 제어신호 범위와 동일한 개념으로 단정하지 않는다.

### 12.2 Operating Range

실제 operating range에는 다음 부하가 반영된다.

- 공정 차압
- 유체 불평형력
- 패킹 마찰
- 가이드 마찰
- 시트 하중
- 스프링 힘
- 동적 유체력

따라서 Bench set과 실제 요구 로딩 압력은 달라질 수 있다.

### 12.3 잘못된 조정 설명

차압이 크다는 이유만으로 Bench set을 임의로 높이면 안 된다.

스프링 조정기로 예압을 변경해도 스프링 레이트 자체가 증가하는 것은 아니다.

추력이 부족하면 다음을 검토한다.

- 다른 스프링
- 더 큰 다이어프램 또는 피스톤
- 허용 공급압력
- 다른 액추에이터
- Balanced trim
- 밸브 및 트림 크기 변경

## 13. Fail-Safe 힘 조건

### 13.1 Fail-Close

공기 상실 시 스프링이 밸브를 닫는다.

최악 조건의 개념식은 다음과 같다.

`F_s,close ≥ F_u,resist + F_f,close + F_seat + margin`

검토항목:

- 폐쇄를 방해하는 불평형력
- 폐쇄 방향 breakaway friction
- 패킹 마찰
- 가이드 마찰
- 요구 시트 하중
- 중량
- 동적 유체력
- 최소 스프링 힘 위치

Pressure-Tends-to-Close이면 유체력이 폐쇄를 보조할 수 있다.

최소 차압에서는 이 보조력이 감소하므로 스프링 자체 힘도 검증한다.

### 13.2 Fail-Open

공기 상실 시 스프링이 밸브를 연다.

최악 조건의 개념식은 다음과 같다.

`F_s,open ≥ F_u,resist + F_f,open + F_breakout + margin`

검토항목:

- 개방을 방해하는 불평형력
- 시트 이탈력
- 개방 방향 breakaway friction
- 패킹 마찰
- 가이드 마찰
- 동적 유체력
- 최소 스프링 힘 위치

Pressure-Tends-to-Close인 밸브에서는 Fail-Open 조건이 불리할 수 있다.

### 13.3 최악조건 조합

- 최대 상류압력
- 최소 하류압력
- 최대 차압
- 최소 차압
- 극한온도
- 최대 패킹 마찰
- 장기 정지 후 breakaway
- 완전 개방
- 중간 개도
- 완전 폐쇄
- 시트 이탈
- 시트 접촉
- 최소 공급압력
- Positioner 최소 출력

## 14. 액추에이터 선정 절차

1. 밸브 형식과 트림 구조를 확인한다.
2. Push-Down-to-Close 또는 Push-Down-to-Open을 확인한다.
3. Pressure-Tends-to-Open 또는 Pressure-Tends-to-Close를 확인한다.
4. 최대 및 최소 차압을 정한다.
5. 개도별 유효 압력면적을 확인한다.
6. 정적 불평형력을 계산한다.
7. 제조사 동적 유체력 자료를 확인한다.
8. 패킹 형식별 마찰력을 확인한다.
9. 가이드 마찰과 측면하중을 검토한다.
10. 요구 차단등급의 시트 하중을 확인한다.
11. 개방, 폐쇄, 시트 이탈 및 접촉 조건을 각각 계산한다.
12. 액추에이터 유효면적과 공급압력으로 가용 추력을 구한다.
13. 스트로크 위치별 스프링 힘을 구한다.
14. 정상운전과 Air Loss 조건을 각각 검증한다.
15. 스템 압축하중과 좌굴 한계를 검토한다.
16. 안전여유와 노화여유를 적용한다.
17. 제조사 사이징 표 또는 소프트웨어로 확인한다.
18. 조립 후 스트로크, 마찰과 fail action을 시험한다.

## 15. 회전식 밸브 경계

볼밸브, 버터플라이밸브와 회전 플러그밸브는 축방향 추력보다 토크 평형으로 해석한다.

`ΣT = T_act + T_s + T_hyd + T_seat + T_bearing = 0`

주요 토크:

- 액추에이터 토크
- 스프링 토크
- Breakout torque
- 시트 마찰 토크
- 베어링 마찰 토크
- 동적 유체 토크
- 최대 차압 토크

직동식 밸브의 `ΔP × A` 식을 회전식 밸브에 그대로 적용하지 않는다.

## 16. Fact Anchor 설계안

1. `control_valve_moving_assembly_free_body_diagram`
2. `control_valve_pressure_force_surface_integration`
3. `control_valve_unbalance_force_effective_area_approximation`
4. `control_valve_pressure_tends_to_open_close_direction`
5. `control_valve_flow_direction_trim_geometry_dependency`
6. `control_valve_stem_area_pressure_force`
7. `control_valve_balanced_trim_residual_unbalance`
8. `control_valve_dynamic_flow_force_momentum_side_load`
9. `control_valve_packing_friction`
10. `control_valve_guide_friction_side_load`
11. `control_valve_breakaway_running_friction_hysteresis`
12. `control_valve_friction_opposes_motion_not_actuator`
13. `control_valve_seat_load_shutoff_class`
14. `control_valve_pneumatic_actuator_force_effective_area`
15. `control_valve_spring_preload_rate_travel_force`
16. `control_valve_bench_set_operating_range_difference`
17. `control_valve_fail_close_force_balance`
18. `control_valve_fail_open_force_balance`
19. `control_valve_actuator_sizing_worst_case_conditions`
20. `control_valve_rotary_valve_torque_boundary`
21. `control_valve_stiction_deadband_diagnostics`
22. `control_valve_balanced_trim_tradeoff_maintenance`

예상 Fact Anchor 수: 22개

## 17. Model Answer 설계안

### 17.1 Expected Question Patterns

- 제어밸브 가동부에 작용하는 힘과 자유물체도를 설명하시오.
- 제어밸브의 불평형력과 유효면적을 설명하시오.
- Pressure-Tends-to-Open과 Pressure-Tends-to-Close를 비교하시오.
- FTO와 FTC에 영향을 주는 트림 형상과 유로를 설명하시오.
- 패킹 마찰력과 가이드 마찰력을 비교하시오.
- Balanced trim과 unbalanced trim의 요구 추력 차이를 설명하시오.
- 공압식 액추에이터의 힘 평형과 선정 절차를 설명하시오.
- Fail-Close와 Fail-Open 스프링 설계기준을 설명하시오.
- Bench set과 operating range의 차이를 설명하시오.
- 직동식 밸브의 힘 해석과 회전식 밸브의 토크 해석을 비교하시오.

### 17.2 Recommended Outline

1. 배경과 분석 대상
2. 자유물체도와 힘의 종류
3. 압력력·불평형력과 FTO/FTC
4. 마찰력·시트 하중과 Balanced Trim
5. 액추에이터·스프링·Bench Set
6. Fail-Safe와 현장 선정·검증

### 17.3 High Score Features

- 압력이 표면에 수직으로 작용함을 설명한다.
- 축방향 압력 합력을 설명한다.
- `ΔP × A`를 조건부 근사식으로 설명한다.
- 유효면적과 스템 면적을 언급한다.
- Pressure-Tends-to-Open과 Close를 구분한다.
- FTO/FTC를 단순 상하 유동으로 정의하지 않는다.
- Balanced trim의 잔류 불평형력과 seal 마찰을 언급한다.
- 패킹 마찰과 가이드 마찰을 구분한다.
- Breakaway와 running friction을 구분한다.
- 마찰력 방향을 운동방향과 연결한다.
- 시트 하중을 차단등급과 연결한다.
- Bench set과 operating range를 구분한다.
- 스프링 예압과 레이트를 구분한다.
- Fail-Close 및 Fail-Open의 최악조건을 각각 설명한다.
- 최대 및 최소 차압을 모두 검토한다.
- 회전식 밸브는 토크로 해석한다.
- 제조사 사이징 자료와 조립 후 시험을 제시한다.

### 17.4 Common Missing Points

- 모든 밸브에 포트면적 근사식을 적용함
- FTO와 FTC를 유동의 상하 방향으로만 설명함
- 패킹 마찰과 가이드 마찰을 구분하지 않음
- 마찰력 방향을 구동력만으로 결정함
- Balanced trim의 잔류력을 누락함
- 시트 하중을 누락함
- Bench set과 operating range를 동일시함
- 스프링 예압과 스프링 레이트를 혼동함
- Fail-Safe 방향만 제시하고 힘 평형을 누락함
- 회전식 밸브에 직동식 힘 방정식을 적용함

## 18. Logic Check 설계안

### 18.1 Logic Check ID

1. `control_valve_unbalance_force_universal_port_area`
2. `control_valve_pressure_direction_independent_of_trim`
3. `control_valve_fto_ftc_vertical_flow_only`
4. `control_valve_balanced_trim_zero_force`
5. `control_valve_friction_always_opposes_actuator`
6. `control_valve_fluid_drag_equals_packing_friction`
7. `control_valve_fail_safe_spring_ignores_loads`
8. `control_valve_bench_set_arbitrary_supply_range`
9. `control_valve_spring_adjustment_changes_rate`
10. `control_valve_rotary_uses_linear_force_equation`
11. `control_valve_pressure_assist_always_available`
12. `control_valve_seat_load_omitted_from_shutoff`

### 18.2 오류 정의

- 모든 밸브의 불평형력을 `(P1-P2) × 포트면적`으로 단정함
- 트림 형상을 보지 않고 압력만으로 힘 방향을 단정함
- FTO/FTC를 배관의 수직 유동 방향으로만 정의함
- Balanced trim의 잔류력과 seal 마찰을 모두 0으로 설명함
- 마찰력 방향을 구동력의 반대 방향으로 고정함
- 유체 점성 전단력과 패킹 마찰을 동일시함
- Fail-Safe 스프링 설계에서 마찰력과 시트 하중을 누락함
- 차압 증가 시 Bench set을 임의로 높이면 된다고 설명함
- 예압 조정으로 스프링 레이트가 증가한다고 설명함
- 회전식 밸브를 직동식 힘 방정식만으로 선정함
- 유체 보조력이 모든 차압 조건에서 항상 존재한다고 가정함
- 차단등급 설명에서 시트 하중을 완전히 누락함

### 18.3 Topic Trust 정책

- Fatal 오류 발생: `limited`
- Fatal 오류 없음: `trusted`
- Logic Check는 D/E 점수에 직접 반영하지 않는다.
- Fact 정확성과 Topic 신뢰도 판단에 사용한다.

## 19. Topic Importance 설계안

- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `FIELD_APPLICATION`
- `selection_importance`: `NORMAL`
- `grading_mode`: `LLM_ONLY`
- `deterministic_checks`: 비활성화

분류 근거:

- 제어밸브와 액추에이터 선정의 실무 주제이다.
- 제어이론 Topic은 아니다.
- 트림 구조와 힘 방향의 인과관계가 중요하다.
- 밸브 제조사와 구조에 따라 유효면적 계산식이 다르다.
- 의미평가가 필요하므로 LLM 기반 채점을 사용한다.

## 20. 작성 및 검증 기준

1. Source JSON 5종의 Topic ID가 일치해야 한다.
2. Fact Anchor의 `id`와 `anchor_id`가 일치해야 한다.
3. Fact Anchor ID는 전체 저장소에서 고유해야 한다.
4. Fact Anchor importance는 허용 enum을 사용해야 한다.
5. Rich Question Pattern은 실제 Fact Anchor ID를 참조해야 한다.
6. Recommended Outline은 실제 Fact Anchor ID를 참조해야 한다.
7. `FIELD_APPLICATION / NORMAL` 분류를 유지해야 한다.
8. `CORE_MUST_PREPARE`를 사용하지 않아야 한다.
9. Logic Check는 D/E 점수에 직접 연결하지 않아야 한다.
10. Generated Bank 6종과 Source가 일치해야 한다.
11. Model Answer Router가 신규 Topic을 선택해야 한다.
12. 외부 LLM 검증은 스크립트에서 수행하지 않는다.
13. 컨테이너 전용 변경이 없으므로 컨테이너 회귀를 생략한다.

## 21. 자료 적용 원칙

Fact Anchor 작성 시 다음 종류의 자료를 우선한다.

- 제어밸브 제조사 Control Valve Handbook
- Sliding-Stem Valve Actuator Sizing 자료
- Spring-and-Diaphragm Actuator 매뉴얼
- 제어밸브 설치·운전·정비 자료
- 사용자가 제공한 밸브 힘 평형 대화 기록

사용자 제공 대화에서는 다음 문제의식을 반영한다.

- `P1`, `P2`와 힘 방향
- FTO와 FTC
- 플러그 형상
- 패킹과 가이드 마찰
- 자유물체도
- Fail-Safe 스프링

다음 내용은 Topic Pack 작성 시 교정한다.

- FTO/FTC를 단순 유동 방향으로 정의하는 설명
- Balanced trim에서 유체력이 완전히 사라진다는 설명
- 패킹 마찰과 유체 점성 마찰을 동일시하는 설명
- Bench set을 임의로 상향하면 된다는 설명
- 스프링 예압과 스프링 레이트를 혼동하는 설명
