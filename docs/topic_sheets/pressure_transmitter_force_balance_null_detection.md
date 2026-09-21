# Force-balance 압력변환기와 null detection

## 0. Topic metadata

- Topic ID: `pressure_transmitter_force_balance_null_detection`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Source: Lessons In Industrial Instrumentation, Chapter 19

## 1. Scope and ownership

압력·차압이 만든 force와 feedback counter-force를 balance하고 position error를 null로
되돌리는 pneumatic/electronic force-balance pressure transmitter의 원리·특성·한계를
소유한다.

- Bourdon·diaphragm·piezoresistive·DP 센서 일반: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- 제어계 폐루프 안정도 일반: 제어이론 Topic
- manifold·bleed·정비 절차: `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`

## 2. Core correct facts

1. sensing force는 `Fsensed=ΔP·A`이며 equilibrium에서 `Fsensed=Fbalance`이다.
2. 장치는 force를 직접 비교하는 대신 force bar의 position error를 null detector로 검출한다.
3. pneumatic 방식은 baffle-nozzle·relay·bellows pressure로 counter-force를 만든다.
4. electronic 방식은 sensor·amplifier·force coil의 current로 counter-force를 만든다.
5. 작은 sensing-element motion은 선형성과 피로 측면에 유리하지만 진동·복잡성·전력 요구를 함께 평가한다.

## 3. Fatal wrong claims

- force-balance transmitter는 open-loop로 displacement만 확대한다.
- balance 상태에서 position error가 클수록 정확한 측정이다.
- baffle-nozzle 출력은 무조건 process pressure와 직접 동일하다.

## 4. False-positive cautions

- pneumatic과 electronic 구현의 출력·전원·방폭 특성을 동일하게 일반화하지 않는다.
- 진동 민감도와 intrinsic safety는 제품·구조·설계조건을 함께 본다.

## 5. Expected question patterns

- Force-balance 압력변환기의 pneumatic 및 electronic 동작원리를 설명하시오.
- Null-balance 방식의 장단점과 현장 적용 시 고려사항을 설명하시오.

## 6. Human review checklist

- [x] position error 검출과 force balance를 구분했다.
- [x] pneumatic/electronic feedback chain을 확인했다.
- [x] 기존 압력센서 Topic과 경계를 분리했다.

## 7. Source

- https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-19/
