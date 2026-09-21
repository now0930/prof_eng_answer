# Force-balance 압력변환기와 null detection

- Topic ID: `pressure_transmitter_force_balance_null_detection`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`

## Scope

압력·차압이 만든 sensing force와 feedback counter-force를 balance하고 position error를
null로 되돌리는 pneumatic/electronic force-balance transmitter의 원리·특성·한계를
소유한다.

## Boundary

- 압력센서 일반은 `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- manifold·bleed·정비는 `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`

## Core boundary

Force 자체를 직접 계측·비교하는 단순 open-loop 장치가 아니라 작은 position error를
검출하고 counter-force를 조절하는 null-balance feedback 구조로 설명한다.

## Source

- [Lessons In Industrial Instrumentation, Chapter 19](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-19/)
