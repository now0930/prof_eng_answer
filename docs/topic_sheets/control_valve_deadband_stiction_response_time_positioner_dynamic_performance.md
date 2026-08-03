# 제어밸브의 데드밴드·스틱션·응답시간 및 포지셔너 동특성

## 1. Topic 개요
제어밸브는 Controller output을 실제 유량과 공정변수 변화로 변환하는 Final Control Element다.

핵심 문제는 명령이 정상이어도 밸브가 위치를 재현하지 못하는 경우다.

대표 원인은 Deadband, backlash, static friction, stiction, stick-slip, 공압 용량 부족, 부적절한 positioner gain이다.

## 2. 신호 전달 경로
`Controller output → I/P 또는 positioner → actuator pressure → stem/shaft travel → valve capacity → flow → PV`

원인 진단은 command, travel, pressure와 PV를 동시에 확인해야 한다.

## 3. Deadband
Deadband는 입력이 변해도 출력이 반응하지 않는 입력 구간이다.

방향 반전 시 linkage 유격 또는 마찰 때문에 두드러질 수 있다.

Deadband는 입력 변화량의 불감 영역이다. Dead time은 시간축 지연이다.

## 4. Backlash와 Hysteresis
Backlash는 기계 연결부의 방향 반전 유격이다.

Hysteresis는 동일 입력에서도 접근 방향에 따라 출력이 달라지는 현상이다.

Deadband, backlash와 hysteresis를 동일한 개념으로 사용하지 않는다.

## 5. Static Friction과 Stiction
Static friction은 정지 상태에서 움직임을 시작하기 위해 극복해야 하는 마찰이다.

Stiction은 밸브가 붙어 있다가 충분한 구동력이 형성되면 갑자기 이동하는 현상이다.

Packing 압축, stem alignment, guide friction, deposits, actuator thrust margin과 supply pressure를 확인한다.

## 6. Stick-Slip
Stick-slip은 정지와 급격한 이동이 반복되는 운동이다.

Controller output은 부드럽게 변해도 travel은 `정지 → jump → 정지 → jump` 형태가 될 수 있다.

모든 oscillation을 stick-slip으로 단정하지 않는다.

## 7. Limit Cycle 형성 경로
1. PV가 setpoint에서 벗어난다.
2. Controller output이 변한다.
3. 밸브는 deadband 또는 stiction 때문에 움직이지 않는다.
4. Output이 더 누적된다.
5. 밸브가 갑자기 이동한다.
6. PV가 목표를 지나칠 수 있다.
7. 반대 방향 보정이 반복된다.

기계적 원인은 PID tuning만으로 제거되지 않을 수 있다.

## 8. Valve Response Time
Response time은 command 변화 후 유효 이동과 목표 접근에 필요한 시간이다.

- Dead time: 명령 후 측정 가능한 이동이 시작되기 전 지연
- Dynamic time: 이동 시작 후 목표 변화에 접근하는 시간

측정 시작점과 종료점을 시험 절차에 명시한다.

## 9. Opening과 Closing 비대칭
Spring force, actuator area, supply/exhaust capacity, fluid force와 friction 방향 때문에 opening과 closing 응답이 다를 수 있다.

시험 결과를 방향별로 기록한다.

## 10. Small-Step Test
Small-step은 실제 제어 영역에서 작은 command 변화의 재현성을 확인한다.

평가 항목은 movement 시작, dead time, 최소 travel, overshoot, repeatability와 방향 반전 deadband다.

## 11. Large-Step Test
Large-step은 stroke speed와 pneumatic capacity를 확인한다.

Supply pressure droop, chamber pressure, output saturation, opening/closing 비대칭과 overshoot를 확인한다.

Large-step이 빨라도 small-step 제어가 좋은 것은 아니다.

## 12. Direction Reversal Test
증가 step 후 감소 step으로 방향을 반전한다.

Command 변화량과 travel 시작점을 비교해 deadband, backlash와 hysteresis를 확인한다.

## 13. Step Sensitivity
Step sensitivity는 작은 command 변화가 실제 travel을 만드는 능력이다.

Sensor resolution, positioner algorithm, friction, backlash와 noise의 영향을 받는다.

Resolution과 완전히 같은 개념이 아니다.

## 14. Positioner의 역할
Positioner는 command와 실제 valve position의 오차를 이용해 actuator pressure를 조절한다.

마찰과 supply pressure 변화에 대한 위치 추종을 개선할 수 있다.

Mechanical backlash를 제거하지 않으며 부족한 actuator thrust를 대신하지 않는다.

## 15. Positioner Gain
Gain이 너무 낮으면 느린 응답과 큰 position error가 발생할 수 있다.

Gain이 너무 높으면 overshoot, hunting, air consumption과 wear가 증가할 수 있다.

최적 gain은 actuator volume, pneumatic path와 valve load에 따라 달라진다.

## 16. Pneumatic Supply와 Tubing
- Supply pressure 부족: force와 충전속도 저하
- Long tubing: 전달 지연 증가
- Small tubing: 충·배기 유량 제한
- Relay/spool capacity 부족: large actuator response 저하
- Filter blockage와 contamination: 응답과 신뢰성 저하

## 17. Volume Booster
Volume booster는 actuator의 공급·배기 공기 유량을 증가시킨다.

Position feedback을 유지해야 한다.

Bypass 또는 gain 조정이 부적절하면 hunting이 발생할 수 있다.

Booster는 deadband, backlash 또는 thrust 부족을 해결하지 않는다.

## 18. Hunting
Hunting은 목표 위치 주변에서 밸브가 반복 이동하는 현상이다.

과도한 positioner gain, booster 조정, feedback noise, linkage looseness, 공압 압축성과 상위 loop interaction을 검토한다.

## 19. Overshoot
빠른 response만 강조하면 목표 위치를 초과할 수 있다.

Dead time, stroke speed, overshoot, small-step stability와 air consumption 사이의 균형이 필요하다.

## 20. 진단 Trend
권장 trend:
1. Setpoint
2. PV
3. Controller output
4. Positioner command
5. Valve travel
6. Supply pressure
7. Actuator chamber pressure
8. Flow 또는 주요 process value

| 관찰 | 가능한 원인 |
|---|---|
| Output 변화, travel 정지 | deadband, stiction, supply 문제 |
| Travel jump | stiction, gain 과다 |
| Travel 정상, PV oscillation | process 또는 sensor 문제 |
| Large-step만 느림 | pneumatic capacity 부족 |
| Small-step만 불량 | friction, deadband, resolution |
| Pressure와 travel 동시 hunting | positioner 또는 booster tuning |

## 21. 개선 절차
1. SP, PV, output, travel을 함께 확인한다.
2. Travel 정지, jump와 방향 반전 deadband를 확인한다.
3. Supply와 chamber pressure를 확인한다.
4. Packing, linkage, alignment와 guide를 점검한다.
5. Positioner calibration, feedback와 gain을 확인한다.
6. Tubing, relay capacity와 actuator volume을 확인한다.
7. 필요한 경우 volume booster를 조건부 검토한다.
8. 동일 시험으로 전후 결과를 비교한다.

## 22. 개선 후 검증
- Deadband
- Minimum reproducible step
- Dead time
- Dynamic time
- Opening/closing stroke time
- Overshoot
- Hunting
- Air consumption
- PV variability
- Product quality
- Energy consumption

## 23. 기술사 답안 구조
1. 배경과 Final Control Element 문제
2. Command-pressure-travel-flow-PV 경로
3. Deadband, stiction와 stick-slip
4. Response time과 시험
5. Positioner와 pneumatic capacity
6. Booster 적용 조건
7. 개선 절차
8. 동일 시험과 공정 성과 검증

## 24. 핵심 Fact Anchor
1. Command-travel-flow-PV 전달 경로
2. Deadband의 방향 반전 불감 영역
3. Deadband와 dead time 구분
4. Backlash
5. Hysteresis
6. Static friction
7. Stiction의 sticking 후 jump
8. Stick-slip
9. Stiction과 limit cycle
10. Oscillation의 다원인 진단
11. Dead time과 dynamic time
12. Opening/closing 비대칭
13. Small-step 시험
14. Large-step 시험
15. Reversal 시험
16. Step sensitivity
17. Positioner feedback
18. Positioner와 backlash 한계
19. Positioner와 actuator thrust 한계
20. Positioner gain trade-off
21. Supply·tubing·spool capacity
22. Volume booster 조건
23. Hunting 다원인 진단
24. 동일 시험과 process result 검증

## 25. 치명적 오류
1. Deadband와 dead time은 같다.
2. Stiction은 단순 느린 응답이다.
3. Hysteresis와 deadband는 완전히 같다.
4. Resolution과 step sensitivity는 같다.
5. 모든 oscillation은 stiction 때문이다.
6. Positioner는 mechanical backlash를 제거한다.
7. Positioner는 부족한 actuator thrust를 대신한다.
8. Positioner gain은 높을수록 항상 좋다.
9. Volume booster는 항상 안정성을 높인다.
10. Volume booster는 deadband를 제거한다.
11. Response time은 dead time만 의미한다.
12. Response time은 stroke time만 의미한다.
13. Small-step과 large-step은 같은 시험이다.
14. PID tuning으로 mechanical stiction을 제거한다.

## 26. 조건부 주장
- Positioner는 항상 2차 시스템을 만든다.
- Positioner integral action은 항상 꺼야 한다.
- 모든 loop에 동일 gain 범위를 적용한다.
- 특정 비율의 loop 문제가 항상 valve 때문이다.
- 특정 packing이 모든 stiction을 해결한다.
- Booster가 모든 느린 response를 해결한다.

## 27. Routing Keywords
강한 조합:
- control valve deadband stiction
- 제어밸브 데드밴드 스틱션
- valve stick slip
- valve response time dead time dynamic time
- valve step response test
- step sensitivity control valve
- positioner dynamic performance
- valve hunting volume booster
- pneumatic tubing valve response

단독 사용 금지:
- valve
- control valve
- friction
- response
- time
- positioner
- gain
- hunting
- dynamic
- performance

## 28. 권장 문제
1. 제어밸브의 데드밴드와 스틱션을 설명하고 개선방안을 제시하시오.
2. Stick-slip이 공정변동을 유발하는 과정을 설명하시오.
3. 응답시간을 dead time과 dynamic time으로 구분하시오.
4. Small-step과 large-step 응답시험을 비교하시오.
5. Step sensitivity 시험의 목적을 설명하시오.
6. Positioner가 밸브 동특성에 미치는 영향을 설명하시오.
7. 공압 공급계통이 응답속도에 미치는 영향을 설명하시오.
8. Volume booster의 적용 목적과 주의사항을 설명하시오.
9. Valve hunting의 원인과 개선방안을 설명하시오.
10. Final Control Element 성능이 공정변동성에 미치는 영향을 설명하시오.
