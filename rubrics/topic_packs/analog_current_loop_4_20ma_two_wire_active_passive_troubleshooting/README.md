# 4–20 mA 아날로그 전류루프·2선식·4선식·Source/Sink·진단

## Topic ID

`analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting`

## 분류

- Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `CORE_MUST_PREPARE`

## 핵심 소유범위

4–20 mA 전류루프의 원리·live zero·loop voltage/load budget, 2선식 loop-powered
transmitter, 4선식 active/source·passive/sink 결선 적합성과 전류 측정·주입을 이용한
현장 구간 분리를 소유한다.

## 소유권 경계

- HART·Fieldbus: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- tray·gland·terminal 시공: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
- grounding·shield·EMC: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- 개별 transmitter의 센서 원리·정확도: 해당 측정 Topic

## 안전·정확도 경계

- 전류가 직렬 루프에서 같다는 설명을 선로저항·부하와 무관하다는 절대명제로 확장하지 않는다.
- source/sink·극성·전원 유무를 매뉴얼과 loop diagram에서 확인한다.
- calibrator의 source·simulate·measure mode를 회로 전원과 맞춰 사용한다.
- 250 ohm 수신저항과 NAMUR 경계는 모든 설비의 절대값으로 단정하지 않는다.

## 대표 답안 흐름

`원리·live zero → 2/4선식·source/sink → load budget → 증상 가설 → 측정·주입 구간 분리 → end-to-end 재검증`

## Source

- [Lessons In Industrial Instrumentation, Chapter 13](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-13/)
- IEC 60381-1
- NAMUR NE 43, when adopted by the project/device
- Project loop drawings and device/I/O-card manuals
