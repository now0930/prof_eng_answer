# 계장 신호 전송선로·반사·종단

## 0. Topic metadata

- Topic ID: `instrument_signal_transmission_line_reflection_termination`
- Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Source: Lessons In Industrial Instrumentation, Chapter 8

## 1. Scope and ownership

고속·급상승 계장 신호에서 케이블을 전송선로로 보아야 하는 조건, 특성임피던스
불연속에 의한 반사, 링잉·오버슈트·오검출 및 종단·토폴로지·측정에 의한 진단을
소유한다.

다음은 제외한다.

- 저주파 EMI coupling·shield·ground: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- tray·conduit·gland 시공: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
- Fieldbus/Ethernet 프로토콜 선정: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- 광섬유 모드·분산·OTDR: `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics`

## 2. Core correct facts

1. 신호의 상승시간이 선로 왕복 전파지연과 비슷하거나 더 짧으면 lumped 회로 가정이 약해져 전송선로로 다룬다.
2. 임피던스 불연속에서 반사가 발생하며 반사계수는 `Γ=(ZL-Z0)/(ZL+Z0)`이다.
3. 정합 종단은 반사를 줄이지만 부하·신호진폭·전력·driver 허용조건과 함께 선정한다.
4. star stub와 과도한 branch는 불연속과 추가 반사 경로를 만들 수 있다.
5. 진단은 파형, ringing/overshoot, cable·connector·termination, topology와 측정 위치를 함께 확인한다.

## 3. Fatal wrong claims

- 케이블 길이와 상승시간에 관계없이 모든 계장 신호는 lumped 회로이다.
- 종단저항은 아무 값이나 병렬 연결하면 항상 반사를 제거한다.
- 임피던스 불연속이 커질수록 반사가 감소한다.

## 4. False-positive cautions

- 느린 4–20 mA loop에 고속 디지털 링크의 종단규칙을 무조건 적용하지 않는다.
- 종단 위치와 값은 해당 물리계층·케이블·driver/receiver 사양을 확인한다.

## 5. Expected question patterns

- 계장 고속신호에서 전송선로 효과, 반사 원인과 종단 대책을 설명하시오.
- 디지털 계장 신호의 링잉·오버슈트를 진단하고 개선하는 절차를 설명하시오.

## 6. Human review checklist

- [x] 상승시간과 전파지연의 조건을 포함했다.
- [x] 반사계수의 방향과 의미를 검토했다.
- [x] EMC·시공·프로토콜 Topic 경계를 분리했다.

## 7. Source

- https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-8/
