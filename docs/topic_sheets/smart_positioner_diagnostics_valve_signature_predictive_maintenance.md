# 스마트 포지셔너 진단, 밸브 시그니처 및 예지보전


## 1. Topic 정보

- Topic ID: `smart_positioner_diagnostics_valve_signature_predictive_maintenance`
- Primary: `DIAGNOSIS_ACTION`
- Secondary: `IMPLEMENTATION_EVALUATION`
- Tertiary: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Importance: `CORE_MUST_PREPARE`

## 2. Diagnostic Data Chain

Command → I/P·relay output → actuator pressure → travel → feedback sensor → status·event
Timestamp, unit, quality flag, sampling rate와 operating context를 함께 저장한다.

## 3. Online과 Offline

Online monitoring은 정상 운전 trend를 관찰한다.
Offline diagnostic test는 계획된 stroke·signature excitation을 사용한다.
Full-stroke test는 process interruption과 safety authorization을 검토한다.

## 4. Static과 Dynamic Signature

Static signature는 quasi-static position-pressure relation을 분석한다.
Dynamic signature는 time response와 operating disturbance를 포함한다.

## 5. As-Left Baseline

Commissioning·overhaul 후 정상 as-left signature를 저장한다.
Direction, supply, process ΔP, temperature와 test mode가 같은 baseline을 사용한다.

## 6. Travel Error

$$e_x=x_{cmd}-x_{meas}$$
$$E_{FS}=100\frac{x_{cmd}-x_{meas}}{x_{max}-x_{min}}$$
Sign convention을 고정하고 xmax>xmin을 확인한다.

## 7. Hysteresis

$$H(u)=|x_{up}(u)-x_{down}(u)|$$
동일 command와 comparable context를 사용한다.

## 8. Actuator Pressure Band

$$\Delta P_{sig}(x)=|P_{open}(x)-P_{close}(x)|$$
동일 position에서 opening·closing pressure를 비교한다.

## 9. Friction Proxy

$$F_{proxy}\approx\frac{A_{eff}\Delta P_{sig}}{2}$$
Effective area, spring와 process-force 가정이 성립할 때만 사용한다.

## 10. Confounding Factors

Process ΔP, flow direction, temperature, supply pressure와 unbalanced force를 함께 확인한다.

## 11. Supply·I/P·Relay Health

Regulator droop, I/P zero·span drift와 relay fill·vent asymmetry를 구분한다.

## 12. Air Usage와 Leakage

$$\Delta Q_{air}=Q_{current}-Q_{baseline}$$
동일 supply와 command condition에서 비교한다.
증가만으로 leakage 위치와 원인을 확정하지 않는다.

## 13. Feedback Sensor

Drift, noise, dropout와 bad-quality flag를 mechanical resistance와 구분한다.

## 14. Cycle과 Accumulated Travel

Full·partial cycle과 direction reversal 정의를 명시한다.
$$TAT=\sum|x_k-x_{k-1}|$$

## 15. Stroke-Time Trend

$$\Delta t_s=t_{current}-t_{baseline}$$
Direction, range, supply, load와 exhaust path를 동일하게 한다.

## 16. Baseline Residual

$$r_z=z_{current}-z_{baseline}(context)$$

## 17. Percentage와 Rate

$$\Delta z_\%=100\frac{z_{current}-z_{baseline}}{|z_{baseline}|}$$
$$\dot z=\frac{z_2-z_1}{t_2-t_1}$$
Nonzero baseline과 t2>t1을 확인한다.

## 18. Alarm Logic

Threshold, persistence, reset logic와 deadband를 함께 사용한다.

## 19. Multi-Evidence Isolation

Travel, pressure, supply, air usage, timing, status와 process context를 결합한다.

## 20. Confidence와 Data Quality

Confidence, quality flag, missing·invalid data 처리를 포함한다.

## 21. Detection과 Confirmation

Detection은 이상 징후이다.
Inspection과 functional test가 physical root cause를 확인한다.

## 22. Maintenance Strategy

| 전략 | Trigger | 장점 | 한계 |
|---|---|---|---|
| Time-based | Calendar·run time | 단순 | 과잉·과소 정비 가능 |
| Condition-based | Condition threshold | 상태 반영 | Data quality 필요 |
| Predictive | Degradation trend·lead time | 계획 최적화 | Exact failure date 보장 불가 |

## 23. Closed-Loop Workflow

Detect → verify → diagnose → prioritize → plan → repair → as-left

## 24. Priority

Diagnostic severity와 production, safety, quality, environmental consequence를 결합한다.

## 25. Asset Integration

HART·Fieldbus·asset-management의 update rate, communication quality와 configuration governance를 확인한다.

## 26. As-Found·As-Left

Repair 전·후 signature와 work-order result를 연결한다.

## 27. Topic 경계

- Topic 1: 물리적 힘·마찰·액추에이터 사이징
- Topic 3: Deadband·stiction·hysteresis·response 시험과 tuning
- Topic 11: Positioner·I/P·booster·accessory 원리와 calibration
- Topic 13: Seat leakage·packing·fugitive emissions
- Topic 15: SIS·ESD·PST
- Topic 16: Full valve-package lifecycle

## 28. 대표 오답

- Smart alarm 하나로 root cause가 확정된다.
- Signature 변화만으로 seat leakage를 확정한다.
- Static과 dynamic signature는 같다.
- Operating context가 달라도 baseline을 직접 비교한다.
- Pressure band 전체가 항상 friction force이다.
- Stroke time 증가만으로 stiction을 확정한다.
- 단일 threshold만으로 충분하다.
- 모든 valve에 같은 health-index weight를 사용한다.
- Predictive maintenance가 exact failure date를 보장한다.
- Smart diagnostics가 physical inspection을 대체한다.

## 29. 고득점 답안 기준

1. Diagnostic data chain을 제시한다.
2. Online·offline과 static·dynamic을 구분한다.
3. Comparable as-left baseline을 정의한다.
4. Travel error·hysteresis·pressure band를 계산한다.
5. Friction proxy의 가정과 confounding factor를 설명한다.
6. Supply·I/P·relay·air·sensor 이상을 구분한다.
7. Usage·stroke-time·residual trend를 설명한다.
8. Persistence·multi-evidence·confidence를 포함한다.
9. Maintenance strategy와 closed-loop workflow를 설명한다.
10. Topic 1·3·11·13·15·16 경계를 명시한다.
