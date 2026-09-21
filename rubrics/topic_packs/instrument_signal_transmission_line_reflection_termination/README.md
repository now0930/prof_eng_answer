# 계장 신호 전송선로·반사·종단

- Topic ID: `instrument_signal_transmission_line_reflection_termination`
- Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`

## Scope

급상승 계장 신호에서 전송선로 판단, 특성임피던스 불연속·반사계수, 종단과
topology, 파형 기반 ringing·overshoot 진단을 소유한다.

`상승시간/전파지연 판단 → 불연속·반사 → 파형 영향 → 정합·배선 대책 → 재측정`

## Boundary

- 저주파 EMI·shield·ground는 `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- cable tray·conduit 시공은 `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
- 상위 통신 protocol 선정은 `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- 광섬유 모드·분산·OTDR은 `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics`

## Safety and correctness

- 느린 4–20 mA loop에 고속 digital termination 규칙을 무조건 적용하지 않는다.
- termination 값·위치는 physical-layer와 driver/receiver 사양으로 확인한다.
- 임피던스 불연속이 커질수록 반사가 감소한다고 설명하지 않는다.

## Source

- [Lessons In Industrial Instrumentation, Chapter 8](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-8/)
