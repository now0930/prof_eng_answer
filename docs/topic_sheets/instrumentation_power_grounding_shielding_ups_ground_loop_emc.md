# 계장 전원·접지·차폐·UPS·Ground Loop·EMC 진단 및 대책

## 1. Topic identity

- Topic ID: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- Criterion: `IC-2027-W-2-6`
- Lane: `SOFTWARE_LLM_LANE_A`
- Focus: 계장 전원·설치·환경·하드웨어·전자오차 중 전원/접지 ownership
- Primary Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Historical frequency: 사용하지 않음

## 2. 출제 의도

이 Topic은 접지 종류를 나열하는 문제가 아니다. 계장 신호가 불안정하거나 noise가 유입되는 현장에서 전원 품질, 기준전위, 접지·본딩, cable shield, ground loop, UPS와 EMC coupling path를 분리 진단하고 안전한 개선대책을 제시할 수 있는지를 평가한다.

핵심 답안 chain은 다음과 같다.

`전원·기준전위 → 접지·본딩 → 차폐·coupling path → ground-loop/EMI evidence → UPS·EMC 대책 → 현장 재검증`

## 3. 전원 품질과 기준전위

계장 전원 문제는 nominal voltage만 확인해서는 부족하다. Voltage sag, interruption, transient, harmonic/noise, source transfer와 DC distribution voltage drop이 실제 신호 이상 시점과 연결되는지 확인해야 한다.

Protective earth(PE)는 감전과 고장전류 안전 경로이다. Signal/reference ground는 측정 및 신호의 기준전위이다. 두 기능을 구분해야 하며 noise 저감을 이유로 PE를 임의 해제하는 것은 허용되지 않는다.

Equipotential bonding은 설비 간 전위차와 공통 임피던스를 줄인다. 고주파에서는 저항뿐 아니라 inductance가 중요하므로 짧고 낮은 임피던스의 접속 경로가 중요하다.

## 4. Single-point와 multi-point grounding

Single-point grounding은 저주파 회로에서 불필요한 loop current를 줄이는 데 유리할 수 있다. 그러나 설비 규모가 커지고 주파수가 높아지면 긴 접지선의 inductive impedance 때문에 등전위 유지가 어려워질 수 있다.

Multi-point grounding은 고주파 EMC에서 낮은 임피던스의 분산 본딩에 유리할 수 있다. 따라서 어느 한 방식이 모든 설비에서 절대적으로 우월하다고 서술하면 안 된다. 주파수, 시스템 topology, cable 길이, enclosure bonding과 common-mode current를 함께 판단한다.

## 5. Ground loop

Ground loop는 둘 이상의 도전성 return path와 지점 간 potential difference가 존재할 때 circulating current가 흘러 신호 기준전위를 교란하는 현상이다.

진단 순서는 다음과 같다.

1. Noise가 발생하는 signal과 operating state를 특정한다.
2. 서로 다른 grounding point 간 potential difference와 common-mode 성분을 확인한다.
3. Cable shield, signal return, equipment bond와 통신 cable 등 복수 return path를 찾는다.
4. Differential measurement와 isolation을 이용해 원인 path를 분리한다.
5. PE를 유지한 상태에서 불필요한 signal-loop path를 제거한다.
6. 대책 전후 waveform과 event를 같은 조건에서 비교한다.

## 6. Shielding

Cable shield는 외부 electric/magnetic field coupling을 줄이는 수단이다. Shield는 PE나 정상 부하전류 return conductor를 대신하지 않는다.

Shield termination은 절대 규칙이 아니다.

- 저주파 analog loop에서는 양단 전위차가 shield current를 만들 수 있어 one-end termination을 사용할 수 있다.
- 고주파 EMC에서는 pigtail의 inductance가 커질 수 있으므로 enclosure 경계의 짧은 360-degree termination과 양단 equipotential bonding이 유리할 수 있다.
- 실제 적용은 cable 구조, signal type, frequency와 plant bonding architecture에 따라 결정한다.

## 7. EMI coupling과 EMC 대책

EMI coupling path는 다음으로 구분한다.

- Conducted coupling
- Radiated coupling
- Capacitive coupling
- Inductive coupling
- Common-impedance coupling

현장 대책은 `source → path → victim`으로 구분한다.

- Source: switching edge, VFD/motor, relay·contactor transient 등 발생원 저감
- Path: cable separation, shield, bonding, filter, enclosure entry 처리
- Victim: differential input, CMRR, isolation, 적절한 filtering과 immunity 확보

EMI filter와 SPD는 단독 부품이 아니라 grounding/bonding architecture와 함께 동작한다. Filter는 enclosure entry 부근에서 우회 coupling을 줄여야 한다. SPD는 접속 lead impedance와 residual overvoltage를 고려하여 coordination한다.

## 8. DC distribution과 redundant power

DC 계장 전원은 power-supply capacity, branch fuse/protection, distribution voltage drop, common return impedance와 load transient를 함께 검토한다.

Power supply를 두 대 사용해도 공통 AC source, 공통 DC bus, ORing module, distribution terminal, cable route가 하나라면 common-cause failure가 남는다. 따라서 redundancy는 단순 장치 개수가 아니라 end-to-end power path로 평가한다.

## 9. UPS

UPS의 핵심 목적은 정전 또는 voltage abnormality 동안 중요 계장 부하를 요구 시간만큼 유지하는 것이다.

UPS sizing은 다음을 함께 고려한다.

- Load W와 VA
- Power factor
- Efficiency
- Inrush / crest characteristic
- Required autonomy time
- Redundancy
- Battery aging
- Environmental derating

UPS가 있다고 해서 surge, EMI, ground loop 또는 galvanic isolation 문제가 자동으로 사라지는 것은 아니다.

Normal, battery, bypass 운전과 transfer 시 neutral/ground reference가 plant grounding architecture와 일관되는지도 확인해야 한다.

## 10. 현장 진단 workflow

1. Symptom을 재현하고 영향 범위를 한정한다.
2. Event time, waveform, spectrum과 operating state를 기록한다.
3. Power quality와 ground-potential/common-mode를 확인한다.
4. Source와 coupling path를 분리한다.
5. Shield·bonding·isolation·filter·UPS·SPD 대책을 원인에 맞게 적용한다.
6. 한 번에 한 변수를 변경한다.
7. Normal, transient, UPS transfer와 주요 noise-source on/off 조건에서 재검증한다.

측정기의 earth clip이나 reference lead 자체가 새로운 ground path를 만들 수 있으므로 measurement reference와 input rating을 확인한다.

## 11. 대표 오답

- “Noise가 생기면 PE를 끊는다.”
- “모든 shield는 한쪽 끝만 접지한다.”
- “Single-point grounding이 모든 주파수에서 항상 최선이다.”
- “UPS 하나면 surge와 EMC 문제가 모두 해결된다.”
- “Power supply 두 대이면 common-cause failure가 없다.”
- “EMC는 filter 하나만 추가하면 해결된다.”

이러한 문장은 적용 조건과 안전 경계를 무시한 절대화이므로 감점 대상이다.

## 12. Lane A ownership boundary

### Topic 2
`instrumentation_installation_wiring_impulse_tubing_inspection_codes`

Cable tray, gland, terminal, impulse tubing, 설치 검사와 code/technical-standard 상세 적용은 Topic 2가 소유한다.

### Topic 3
`instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`

EMC emission/immunity qualification의 test method·severity와 temperature/humidity/vibration qualification은 Topic 3가 소유한다.

### Topic 4
`control_hardware_lifecycle_panel_architecture_component_selection_production_verification`

Panel architecture, component selection, HW lifecycle와 prototype/production verification은 Topic 4가 소유한다.

### Topic 5
`electronics_error_noise_drift_tolerance_aging_power_mitigation`

Electronic component-level noise, drift, tolerance, aging, power variation의 error chain은 Topic 5가 소유한다.

## 13. 고득점 답안 조건

고득점 답안은 접지 종류를 나열하는 데 그치지 않는다.

- PE와 signal reference의 safety boundary를 명확히 한다.
- Ground loop의 mechanism과 diagnostic evidence를 제시한다.
- Shield termination을 frequency-dependent rule로 설명한다.
- Source-path-victim EMC chain을 제시한다.
- UPS의 기능 한계와 sizing·bypass/ground reference를 포함한다.
- Before/after evidence와 closed-loop verification을 제시한다.
- Topic 2~5와 ownership 중복을 피한다.

## 14. Source policy

이 Topic은 repository roadmap의 `IC-2027-W-2-6` criterion과 계장 전원·접지·차폐·ground-loop·UPS·EMC의 공학적 기본 원리를 근거로 작성한다.

Historical frequency는 근거가 없으므로 사용하지 않는다. EMC qualification severity, 상세 설치 code, HW lifecycle 및 component-level error chain은 각각 별도 Topic의 ownership으로 남긴다.
