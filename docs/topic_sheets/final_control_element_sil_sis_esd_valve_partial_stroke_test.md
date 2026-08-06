# 최종제어요소의 SIL·SIS·ESD 밸브와 부분행정시험

## 1. Topic 정의

`final_control_element_sil_sis_esd_valve_partial_stroke_test`는 Safety Instrumented Function(SIF)의 Final Element subsystem을 다룬다.

Final Element는 logic solver의 trip output을 실제 공정 변화로 변환한다. 일반적으로 solenoid-operated valve, actuator, shutdown valve, position indication와 utility interface를 포함한다. Topic 15는 장치 선정 자체보다 **요구된 safe state를 demand 시점에 신뢰성 있게 달성하는가**를 평가한다.

## 2. 핵심 관계

SIS는 여러 SIF를 포함할 수 있다. 하나의 SIF는 sensor, logic solver와 final element로 구성된다. SIL은 개별 valve의 고정 등급이 아니라 SIF가 요구하는 risk reduction과 integrity requirement를 나타낸다.

따라서 Final Element 검증은 다음 순서로 진행한다.

1. Hazard analysis와 SRS에서 safe state와 allowable response time을 확인한다.
2. Valve, actuator, solenoid와 utility의 subsystem boundary를 정의한다.
3. Dangerous, safe와 spurious failure mode를 구분한다.
4. PFDavg 또는 PFH budget에서 Final Element의 기여를 평가한다.
5. Diagnostics, PST와 Full Stroke Proof Test의 detectable failure set을 정의한다.
6. Worst-case response time, bypass, restoration와 common cause를 검증한다.
7. Test·demand·maintenance 결과를 lifecycle assumption에 feedback한다.

## 3. Safe State와 Trip Action

Fail-close와 fail-open은 기계적 동작 방향이다. Safe State는 공정 위험분석 결과이다. 두 개념이 일치하지 않을 수 있다.

De-energize-to-trip은 power 또는 signal loss 시 trip을 유도하는 설계 철학이다. 그러나 spring energy, actuator pressure, solenoid vent path, shared utility와 process consequence를 함께 검토해야 한다.

## 4. Final-element Architecture

Typical chain은 다음과 같다.

`Logic Solver Output → Relay/Output Module → Solenoid Valve → Actuator → Shutdown Valve → Process Safe State`

각 component는 서로 다른 failure mode를 가진다.

- Solenoid: coil fault, sticking, blocked vent, wrong energization state
- Actuator: seal leakage, insufficient force, spring degradation, slow venting
- Valve: stiction, corrosion, deposit, wrong travel, seat leakage
- Utility: low air pressure, common power loss, frozen line, blocked exhaust
- Feedback: false position indication, switch misadjustment, diagnostic blind spot

## 5. PFDavg와 PFH

Low-demand mode의 단순 screening은 다음과 같다.

\[
\mathrm{PFD}_{avg}\approx \frac{\lambda_{DU}T_I}{2}
\]

이 식은 constant failure rate, low-demand mode, specified proof-test interval와 단순 restoration assumption에서만 사용한다.

High-demand 또는 continuous-mode의 단순 screening은 다음과 같다.

\[
\mathrm{PFH}\approx \lambda_{DU}
\]

Sensor, logic solver와 Final Element가 모두 성공해야 하는 series SIF는 independent assumption에서 다음과 같이 결합할 수 있다.

\[
\mathrm{PFD}_{series}
=1-\prod_i(1-\mathrm{PFD}_i)
\]

각 PFD가 충분히 작을 때만 단순 합을 approximation으로 사용한다.

## 6. Diagnostic Coverage와 Proof Test Coverage

Diagnostic Coverage는 online diagnostics가 검출하는 dangerous failure의 비율이다.

\[
DC=
\frac{\lambda_{DD}}
{\lambda_{DD}+\lambda_{DU}}
\]

Proof Test Coverage는 proof test가 otherwise undetected dangerous failure 중 검출 가능한 비율이다.

\[
PTC=
\frac{\lambda_{DU,PT}}
{\lambda_{DU,total}}
\]

두 coverage는 동일하지 않다. Detectable failure set과 test procedure를 연결해야 한다.

## 7. PST와 Full Stroke Proof Test

PST는 valve를 제한된 범위로 이동해 selected hidden failure를 검출한다. Stiction, movement initiation, selected solenoid-actuator path와 position feedback fault를 검출할 수 있다.

그러나 PST는 다음 항목을 완전히 검증하지 못할 수 있다.

- Complete travel와 end stop
- Full isolation 또는 depressurization
- Seat leakage
- Full-stroke response time
- 모든 solenoid·actuator·valve failure mode
- Final safe position에서의 process effect

따라서 PST coverage는 Full Stroke Proof Test coverage와 분리한다.

PST residual dangerous-rate screening은 다음과 같다.

\[
\lambda_{DU,res}
=
\lambda_{DU}(1-C_{PST})
\]

이 식도 PST가 적용되는 failure subset에서만 사용한다.

## 8. Response Time

Simple serial screening은 다음과 같다.

\[
t_{FE}
=
t_{SOV}
+t_{actuator}
+t_{valve}
\]

실제 dynamic overlap이 있으면 package measured response를 사용한다.

SRS allowable time 대비 margin은 다음과 같다.

\[
M_t=
\frac{t_{allow}-t_{measured}}
{t_{allow}}
\]

Worst-case instrument air pressure, maximum process load, extreme temperature, aged friction와 actual tubing volume에서 확인한다.

## 9. Common Cause와 Redundancy

Redundant valve를 추가해도 common cause가 자동으로 제거되지 않는다.

공통 원인은 다음과 같다.

- Shared instrument-air header
- Shared power 또는 output module
- 동일 fire·flood·temperature zone
- 동일 maintenance procedure와 human error
- 동일 design defect와 environmental contamination

Beta-factor screening은 다음과 같다.

\[
\lambda_{CCF}=\beta\lambda_D
\]

Beta는 universal constant가 아니다.

## 10. Bypass, Override와 Restoration

Bypass 또는 override 중에는 SIF risk reduction이 감소한다.

필수 관리항목은 다음과 같다.

- Authorization와 time limit
- Compensating protection
- Alarm와 operator communication
- Test permit와 impairment record
- Bypass removal
- Solenoid energization와 valve position 복구
- Independent restoration verification

## 11. Acceptance Evidence

Final Element acceptance는 SRS requirement와 trace해야 한다.

- Safe direction
- Trip response time
- Final position
- Required seat leakage
- Solenoid·actuator·valve chain
- Diagnostic alarm
- PST와 Full Stroke Proof Test coverage
- Bypass duration와 restoration
- As-found·repair·as-left result

Vendor SIL certificate나 FMEDA는 application assumption을 대신하지 않는다.

## 12. Lifecycle

Demand, proof test와 maintenance에서 발견된 failure를 다음 항목에 feedback한다.

- Failure-rate assumption
- Proof-test coverage와 interval
- PST interval와 stroke fraction
- Spare equivalence
- Procedure revision
- Training
- Management of Change
- Revalidation

## 13. Topic 경계

- Topic 1: actuator force·spring sizing
- Topic 3: deadband·stiction·generic response
- Topic 4: valve body·actuator taxonomy
- Topic 8: cavitation·flashing
- Topic 10: balanced trim·seal mechanics
- Topic 11: positioner·I/P·booster calibration
- Topic 12: valve signature·predictive diagnostics
- Topic 13: seat leakage·packing·emissions
- Topic 14: severe-service mechanical suitability
- Topic 16: complete package selection과 enterprise lifecycle

## 14. 답안 작성 순서

1. SIS·SIF·SIL 문맥과 Final Element 소유 범위를 정의한다.
2. Safe State와 valve-actuator-solenoid architecture를 설명한다.
3. Dangerous·safe·spurious failure mode를 구분한다.
4. PFDavg·PFH와 subsystem budget을 설명한다.
5. Diagnostics, PST와 Full Stroke Proof Test를 비교한다.
6. Response time, common cause와 bypass control을 설명한다.
7. Acceptance record, MOC와 lifecycle feedback을 제시한다.

## Keytags

SIS, SIF, SIL, Final Element, ESD Valve, Safe State, PFDavg, PFH, Partial Stroke Test, Proof Test
