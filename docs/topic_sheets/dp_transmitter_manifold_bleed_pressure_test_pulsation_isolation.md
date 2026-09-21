# DP transmitter manifold·bleed·압력시험·pulsation isolation

## 0. Topic metadata

- Topic ID: `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `CORE_MUST_PREPARE`
- Source: Lessons In Industrial Instrumentation, Chapter 19

## 1. Scope and ownership

DP transmitter의 3-valve manifold 정상상태, 격리·equalizing·bleed 조작순서,
zero-energy 확인, hand-pump 압력시험, trapped gas/condensate 배출, pulsation damping과
process isolation을 소유한다.

- 압력센서 원리·선정·오차: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- impulse tubing 시공·slope·inspection: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
- DP level wet/dry leg·remote seal head: `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`

## 2. Core correct facts

1. 정상상태는 H/L block open, equalizing closed이며 표준 3-valve manifold의 bleed는 transmitter flange의 별도 fitting일 수 있다.
2. 격리는 H close → equalizing open → L close → bleed open 순으로 differential pressure와 잔압을 제어한다.
3. 복귀는 bleed close → L open → equalizing close → H open 순으로 vent 경로를 먼저 닫고 정상 ΔP를 회복한다.
4. DP 압력시험은 process를 격리하고 H에 시험압, L에 reference를 두며 equalizing open 상태에서는 ΔP 시험이 되지 않는다.
5. liquid service의 trapped gas는 상부, gas service의 condensate는 하부 vent/drain으로 제거한다.
6. snubber/damper는 pulsation을 줄이지만 damping과 response speed 사이 trade-off가 있다.
7. isolating diaphragm은 process fluid 접촉을 막고 fill fluid로 pressure를 전달하므로 온도·호환성·응답 영향을 평가한다.

## 3. Fatal wrong claims

- H/L block가 열린 상태에서 bleed를 열어도 안전한 zero-energy 상태다.
- equalizing valve를 연 채 DP span pressure test를 수행한다.
- 정상운전에서 equalizing valve를 열어 실제 ΔP를 측정한다.
- damping을 크게 할수록 응답 지연 없이 항상 성능이 좋아진다.

## 4. False-positive cautions

- 실제 작업은 현장 절차서, manifold 구성, process hazard와 LOTO/permit를 우선한다.
- 5-valve manifold와 remote seal 등 다른 구성에 3-valve 순서를 기계적으로 적용하지 않는다.

## 5. Expected question patterns

- DP transmitter 3-valve manifold의 정상·격리·복귀 조작절차와 안전상 유의점을 설명하시오.
- DP transmitter의 bleed, 압력시험, pulsation damping 및 process isolation 방안을 설명하시오.

## 6. Human review checklist

- [x] 정상·격리·복귀 valve 상태와 순서를 검토했다.
- [x] equalizing open 상태의 DP test 오류를 명시했다.
- [x] 실제 LOTO와 절차서 우선 경계를 포함했다.

## 7. Source

- https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-19/
