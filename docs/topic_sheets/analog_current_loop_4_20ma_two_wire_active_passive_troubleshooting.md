# 4–20 mA 아날로그 전류루프·2선식·4선식·Source/Sink·진단

## 0. Topic identity

- Topic ID: `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting`
- Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `CORE_MUST_PREPARE`
- Reference: Lessons In Industrial Instrumentation, Chapter 13

## 1. 출제 의도

4–20 mA 전류루프의 원리와 live zero, loop power budget을 설명하고 2선식과 4선식
active/source·passive/sink 결선을 구분한다. 현장에서 0 mA, 고정값, 오프셋 및
표시 불일치를 측정·구간 분리로 진단할 수 있어야 한다.

## 2. 직접 포함 범위

1. 4–20 mA 전류루프와 0–10 V 대비 특성
2. 4 mA live zero와 0 mA 고장 식별
3. 2선식 loop-powered transmitter
4. 4선식 active/source와 passive/sink
5. 수신 카드·외부 전원과 소스 충돌 방지
6. 공급전압, cable drop, load resistance를 포함한 compliance/load budget
7. 수신저항 전압으로 루프 전류 확인
8. Loop calibrator의 source/simulate/measure mode를 이용한 구간 분리
9. 4·12·20 mA 주입과 0·50·100% scaling 확인

## 3. Ownership 제외

- HART·Fieldbus 프로토콜과 상호운용: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- cable tray·gland·terminal 시공: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
- grounding·shield·EMC: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- 개별 transmitter 센서 원리·정확도: 해당 측정 Topic

## 4. 핵심 Fact

- 전류루프는 직렬 경로의 동일 전류를 정보로 사용하지만 선로저항이 무관하지는
  않으며 필요 compliance voltage 범위를 만족해야 한다.
- 4 mA는 0% 공정값과 0 mA 단선·전원상실을 구분하는 live zero이며 2선식
  기기의 전원을 제공한다.
- 2선식은 전원과 신호가 한 쌍을 공유하며 외부 loop supply가 필요하다.
- Active/source 출력은 루프 전류를 공급하고 passive/sink 출력은 외부 루프
  전원으로 전류를 조절하므로 수신 카드 형식과 결선을 맞춰야 한다.
- 진단은 회로도·전원·극성·부하를 확인한 뒤 루프 전류 측정과 수신부 신호
  주입으로 transmitter/cable/input/scaling 구간을 분리한다.

## 5. 대표 오답과 false-positive 경계

- 선로저항과 부하에 관계없이 전류가 항상 정확하다.
- 0 mA는 항상 정상 0% 공정값이다.
- 모든 4선식 transmitter가 loop current를 자체 공급한다.
- source 출력과 powered input을 조건 확인 없이 직결해도 된다.
- 250 ohm은 모든 루프에 의무인 절대값이다.
- 3.8/20.5 mA 등 장치별 alarm 경계는 해당 제품·표준 설정을 확인한 설명이면 허용한다.

## 6. 답안 전개

1. 전류루프 원리와 live zero
2. 2선식·4선식 source/sink 비교
3. loop voltage/load budget과 결선 적합성
4. 증상별 원인 가설
5. 측정·주입으로 구간 분리
6. 복구 후 4·12·20 mA·표시·알람 재검증

## 7. Source

- https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-13/
- IEC 60381-1 process control analogue dc current signals
- NAMUR NE 43 failure information conventions, when adopted by the project/device
- device manuals and loop drawings for source/sink, compliance and test-mode details
