# 초음파 센서의 비행시간 원리, 거리·레벨 측정, 온도보상 및 반사·설치 오차

## 1. Topic metadata

- `topic_id`: `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`
- `title_ko`: `초음파 센서의 비행시간 원리, 거리·레벨 측정, 온도보상 및 반사·설치 오차`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `semantic_execution`: `LLM_ONLY`
- `deterministic_checks.enabled`: `false`
- `candidate_extraction`: `{}`
- Fact Anchor 수: `20`
- Fatal Wrong Claim 수: `10`
- Routing Alias 수: `32`
- Routing Field Point 수: `5`
- Question Example 수: `14`
- Expected Question Pattern 수: `14`

## 2. Scope

이 Topic Pack은 공기 중 초음파를 이용한 비접촉 거리 및 레벨 측정을 다룬다.

핵심 범위는 다음과 같다.

- 압전소자의 송신·수신 변환
- 펄스 에코 비행시간 측정
- 왕복 전파시간과 거리 계산
- 음속의 온도 및 매질 의존성
- 온도보상
- 링다운과 사각지대
- 빔각과 대상물 반사특성
- 주파수·분해능·감쇠의 절충관계
- 탱크 레벨 계산
- 허위에코와 다중반사
- 거품·증기·난류·분진 영향
- 노즐·장애물·설치각도 오차
- 센서 간 크로스토크
- 반복주기·평균화·동특성
- 교정·에코맵·진단
- 레이더식 레벨 측정과의 적용조건 비교

의료용 영상, 수중 소나, 초음파 유량계와 비파괴검사는 주범위에서 제외한다.

## 3. Required principle chain

1. 송신회로가 압전소자에 전기 펄스를 인가한다.
2. 압전소자는 전기 에너지를 초음파 진동으로 변환한다.
3. 초음파는 공기 중을 진행하여 대상물 또는 액면에서 반사된다.
4. 반사파가 돌아오면 압전소자 또는 별도 수신소자가 전기신호를 발생한다.
5. 계측회로는 송신시점과 에코 수신시점 사이의 비행시간을 측정한다.
6. 반사형 펄스 에코 방식은 왕복 전파시간을 측정하므로 거리식은 \(d=ct/2\)이다.
7. `c`는 측정 매질에서의 음속이고 `t`는 왕복 비행시간이다.
8. 기체 중 음속은 온도와 기체 조성 등 매질조건의 영향을 받는다.
9. 온도보상 없이 고정 음속을 사용하면 거리 및 레벨 오차가 발생한다.
10. 송신 직후의 압전소자 링다운과 수신회로 회복시간은 사각지대를 만든다.
11. 빔각과 대상물 크기·경사·표면상태는 에코 수신 안정성에 영향을 준다.
12. 높은 주파수는 일반적으로 분해능과 지향성에 유리하지만 공기 중 감쇠가 커질 수 있다.
13. 거리의 기본 측정량은 반사파 진폭이 아니라 유효 에코의 비행시간이다.
14. 레벨은 기준높이 또는 빈 탱크 거리에서 센서와 액면 사이 거리를 빼서 계산한다.
15. 노즐, 벽면, 내부 구조물과 다중반사는 허위에코를 만들 수 있다.
16. 시간 게이트, 임계값, 에코맵과 설치개선으로 유효 에코를 선택한다.
17. 거품, 증기, 난류, 파동과 분진은 감쇠·산란·음속 또는 반사면을 변화시킨다.
18. 인접 센서의 동시 송신은 크로스토크를 발생시킬 수 있다.
19. 반복주기와 평균화는 응답속도와 측정 안정성 사이의 절충관계를 가진다.
20. 적용 시 측정범위, 공정조건, 설치구조와 진단정보를 함께 검토한다.

## 4. Technical boundary and wording rules

### 4.1 Pulse-echo distance

- 기본 반사형 거리식은 \(d=ct/2\)이다.
- `t`는 송신부터 반사파 수신까지의 왕복시간이다.
- 송신기와 수신기가 대상물 양쪽에 있는 투과형 구성과 구분한다.
- 모든 초음파 응용에 무조건 `1/2`을 적용한다고 설명하지 않는다.

### 4.2 Sound speed and compensation

- 건조 공기의 음속은 제한된 온도범위에서 근사적으로 \(c \approx 331.3+0.606T\,[m/s]\)로 표현할 수 있다.
- `T`는 섭씨온도이다.
- 실제 음속은 온도, 기체 조성, 습도와 운전환경의 영향을 받을 수 있다.
- 기체 압력에 단순 비례하여 음속이 증가한다고 설명하지 않는다.
- 정밀 적용에서는 제조사의 보상모델과 실제 매질조건을 확인한다.

### 4.3 Echo amplitude

- 반사파 진폭은 거리, 대상물 크기, 경사, 표면상태와 감쇠의 영향을 받는다.
- 에코 진폭은 유효 에코 판별에 사용할 수 있다.
- 반사파 진폭 자체를 거리의 직접 측정량으로 설명하지 않는다.

### 4.4 Dead zone

- 송신 직후 압전소자의 기계적 링다운이 발생한다.
- 송신회로에서 수신회로로 전환하고 수신증폭기가 회복하는 데 시간이 필요하다.
- 이 때문에 최소 측정거리 또는 사각지대가 생긴다.
- 센서 표면의 영거리부터 항상 측정할 수 있다고 설명하지 않는다.

### 4.5 Beam, target and frequency

- 초음파 센서는 유한한 빔각을 가진다.
- 거리가 증가하면 검출영역이 넓어진다.
- 작은 대상물이나 기울어진 평탄면은 반사파를 센서 밖으로 보낼 수 있다.
- 높은 주파수는 일반적으로 짧은 파장과 높은 분해능에 유리하다.
- 높은 주파수는 공기 중 감쇠가 커 장거리 측정에 불리할 수 있다.
- 주파수가 높을수록 최대 측정거리가 항상 증가한다고 설명하지 않는다.

### 4.6 Level measurement

- 센서는 일반적으로 탱크 상부에서 액면까지의 거리를 측정한다.
- 레벨은 기준높이 또는 빈 탱크 거리에서 측정거리를 빼서 계산한다.
- 센서 기준점, 노즐 높이와 탱크 형상을 명확히 정의해야 한다.

### 4.7 Process and installation errors

- 거품은 실제 액면과 다른 반사면을 만들거나 에코를 약화시킬 수 있다.
- 증기는 음속과 감쇠를 변화시킬 수 있다.
- 난류와 파동은 반사면의 위치와 각도를 변동시킨다.
- 분진은 초음파를 산란·감쇠시킬 수 있다.
- 긴 노즐, 좁은 노즐, 장애물과 부적절한 설치각도는 허위에코 또는 에코 손실의 원인이 된다.
- 인접 센서의 동시 송신은 크로스토크를 발생시킬 수 있다.

### 4.8 Signal processing and diagnostics

- 시간 게이트는 관심 거리범위 밖의 에코를 제외한다.
- 임계값과 에코 추적 알고리즘은 유효 반사파를 선택한다.
- 고정 구조물의 반사패턴은 에코맵 또는 허위에코 억제 기능으로 관리할 수 있다.
- 평균화는 노이즈를 줄이지만 응답속도를 늦출 수 있다.
- 에코 강도, 신호대잡음비와 에코 손실은 진단정보로 활용할 수 있다.

## 5. Fact Anchors

1. `ultrasonic_sensor_system_structure`
   - 초음파 거리·레벨 측정시스템은 송신구동부, 압전 송수신소자, 수신증폭부, 비행시간 계측부, 보상 및 출력처리부로 구성된다.

2. `ultrasonic_piezoelectric_transduction`
   - 압전소자는 전기 펄스를 초음파 진동으로 변환하고 수신된 초음파 진동을 전기신호로 변환한다.

3. `ultrasonic_pulse_echo_time_of_flight`
   - 펄스 에코 방식은 초음파 송신시점부터 대상물에서 반사된 에코의 수신시점까지의 비행시간을 측정한다.

4. `ultrasonic_round_trip_distance_equation`
   - 반사형 펄스 에코 방식에서는 초음파가 센서와 대상물 사이를 왕복하므로 거리는 \(d=ct/2\)로 계산한다.

5. `ultrasonic_sound_speed_medium_dependence`
   - 초음파 전파속도는 매질의 물성과 상태에 따라 달라지며 기체에서는 온도와 기체 조성의 영향이 중요하다.

6. `ultrasonic_air_temperature_compensation`
   - 공기 중 음속의 온도 의존성을 보상하지 않으면 비행시간을 거리로 환산할 때 측정오차가 발생한다.

7. `ultrasonic_dead_zone_ringdown`
   - 송신 직후의 압전소자 링다운과 수신회로 회복시간 때문에 근거리 에코를 구분하지 못하는 사각지대가 생긴다.

8. `ultrasonic_beam_angle_footprint`
   - 초음파 빔은 유한한 빔각을 가지며 거리가 증가할수록 검출영역이 넓어져 주변 구조물이 에코에 포함될 수 있다.

9. `ultrasonic_target_reflectivity_orientation`
   - 대상물의 크기, 경사, 표면 거칠기와 음향반사 특성은 에코 세기와 검출 안정성에 영향을 준다.

10. `ultrasonic_frequency_range_resolution_tradeoff`
    - 높은 초음파 주파수는 일반적으로 분해능과 지향성에 유리하지만 공기 중 감쇠가 증가하여 최대 측정거리에는 불리할 수 있다.

11. `ultrasonic_attenuation_max_range`
    - 최대 측정거리는 송신출력, 주파수, 공기 중 흡수, 빔 확산, 대상물 반사특성과 수신감도의 영향을 받는다.

12. `ultrasonic_echo_amplitude_validity`
    - 에코 진폭은 유효 에코 판별에 활용할 수 있지만 거리의 기본 측정량은 에코 진폭이 아니라 비행시간이다.

13. `ultrasonic_level_measurement_reference`
    - 탱크 레벨은 센서 기준점부터 액면까지의 측정거리를 탱크 기준높이 또는 빈 탱크 거리에서 빼서 계산한다.

14. `ultrasonic_false_echo_multiple_reflection`
    - 노즐, 탱크 벽, 내부 구조물과 다중반사에서 발생한 허위에코는 실제 액면 에코와 경쟁하여 오검출을 일으킬 수 있다.

15. `ultrasonic_foam_vapor_turbulence_error`
    - 거품, 증기, 난류, 파동과 분진은 초음파의 감쇠·산란·음속 또는 반사면 상태를 변화시켜 측정오차를 일으킬 수 있다.

16. `ultrasonic_mounting_nozzle_obstruction_error`
    - 긴 노즐, 좁은 개구부, 장애물, 부적절한 설치각도와 센서축 정렬은 허위에코와 에코 손실의 원인이 된다.

17. `ultrasonic_sensor_crosstalk`
    - 인접 초음파 센서가 동시에 송신하면 다른 센서의 펄스를 자신의 에코로 인식하는 크로스토크가 발생할 수 있다.

18. `ultrasonic_repetition_rate_response_averaging`
    - 송신 반복주기와 신호 평균화는 갱신속도, 최대 측정거리, 노이즈 억제와 동적 응답 사이의 절충관계를 가진다.

19. `ultrasonic_calibration_echo_mapping_diagnostics`
    - 기준거리 확인, 온도보상 점검, 에코맵 설정, 임계값 조정과 에코 강도 진단은 측정 신뢰성 확보에 필요하다.

20. `ultrasonic_application_limits_comparison`
    - 초음파 방식은 측정범위, 사각지대, 공정기체, 거품·증기·분진, 설치구조와 응답속도를 검토하고 필요하면 레이더식과 비교하여 적용한다.

## 6. Fatal Wrong Claims

1. `ultrasonic_fatal_light_speed`
   - 잘못된 주장: 초음파 거리센서는 빛의 속도로 거리를 계산한다.
   - 올바른 기준: 측정 매질에서의 음속을 사용한다.

2. `ultrasonic_fatal_no_round_trip_half`
   - 잘못된 주장: 반사형 펄스 에코 거리식은 \(d=ct\)이다.
   - 올바른 기준: 왕복시간을 측정하므로 \(d=ct/2\)이다.

3. `ultrasonic_fatal_temperature_independent`
   - 잘못된 주장: 공기 중 음속은 온도와 무관하다.
   - 올바른 기준: 공기 중 음속은 온도에 따라 달라지므로 온도보상이 필요하다.

4. `ultrasonic_fatal_echo_amplitude_is_distance`
   - 잘못된 주장: 반사파 진폭만으로 거리를 직접 계산한다.
   - 올바른 기준: 기본 거리 측정량은 반사파의 비행시간이다.

5. `ultrasonic_fatal_no_dead_zone`
   - 잘못된 주장: 센서 표면의 영거리부터 모든 거리를 측정할 수 있다.
   - 올바른 기준: 링다운과 수신회복시간 때문에 사각지대가 존재한다.

6. `ultrasonic_fatal_all_targets_equal`
   - 잘못된 주장: 대상물의 크기, 경사와 표면상태는 에코 검출에 영향을 주지 않는다.
   - 올바른 기준: 대상물의 음향반사 특성과 방향은 에코 검출에 영향을 준다.

7. `ultrasonic_fatal_high_frequency_longer_range`
   - 잘못된 주장: 주파수가 높을수록 최대 측정거리는 항상 증가한다.
   - 올바른 기준: 높은 주파수는 분해능에 유리하지만 공기 중 감쇠가 증가할 수 있다.

8. `ultrasonic_fatal_pressure_proportional_speed`
   - 잘못된 주장: 기체 압력에 비례하여 음속이 증가하므로 압력만 보상하면 된다.
   - 올바른 기준: 온도와 기체 조성 등 실제 매질조건을 고려해야 한다.

9. `ultrasonic_fatal_no_false_echo`
   - 잘못된 주장: 초음파 센서에는 허위에코나 다중반사가 발생하지 않는다.
   - 올바른 기준: 노즐, 벽면, 내부 구조물과 다중반사가 오검출을 만들 수 있다.

10. `ultrasonic_fatal_process_installation_no_error`
    - 잘못된 주장: 거품, 증기, 난류, 분진과 설치구조는 측정에 영향을 주지 않는다.
    - 올바른 기준: 공정 및 설치조건은 감쇠, 산란, 음속과 반사면을 변화시킨다.

## 7. Routing Aliases

1. `ultrasonic time of flight sensor`
2. `ultrasonic pulse echo sensor`
3. `ultrasonic distance sensor`
4. `ultrasonic level sensor`
5. `ultrasonic ranging sensor`
6. `ultrasonic transducer pulse echo`
7. `ultrasonic echo timing`
8. `ultrasonic round trip time`
9. `ultrasonic dead zone`
10. `ultrasonic blanking distance`
11. `ultrasonic temperature compensation`
12. `ultrasonic beam angle`
13. `ultrasonic false echo`
14. `ultrasonic multiple echo`
15. `ultrasonic level transmitter`
16. `non-contact ultrasonic level measurement`
17. `초음파 센서 비행시간`
18. `초음파 거리센서`
19. `초음파 레벨센서`
20. `초음파 수위센서`
21. `초음파 펄스 에코`
22. `초음파 반사파 시간`
23. `초음파 왕복시간`
24. `초음파 사각지대`
25. `초음파 센서 불감대`
26. `초음파 블랭킹 거리`
27. `초음파 온도보상`
28. `초음파 센서 빔각`
29. `초음파 허위에코`
30. `초음파 다중반사`
31. `초음파 레벨 트랜스미터`
32. `비접촉 초음파 레벨 측정`

## 8. Routing Field Points

1. `탱크 노즐 구조와 허위에코 맵 설정`
2. `거품·증기·난류·분진에 따른 적용성 검토`
3. `온도센서 위치와 음속 보상 검증`
4. `측정거리·분해능에 따른 주파수 선정`
5. `시운전 교정·에코 진단·센서 간 크로스토크 방지`

## 9. Question Examples

1. `초음파 센서의 측정원리와 특징을 설명하시오.`
2. `초음파 펄스 에코 방식의 비행시간과 거리 계산식을 설명하시오.`
3. `초음파 거리센서의 음속 변화와 온도보상 방법을 설명하시오.`
4. `초음파 센서의 사각지대와 최소 측정거리 발생원인을 설명하시오.`
5. `초음파 센서의 빔각과 대상물 크기·경사가 측정에 미치는 영향을 설명하시오.`
6. `초음파 주파수와 측정거리·분해능의 관계를 설명하시오.`
7. `초음파식 탱크 레벨 측정원리와 레벨 계산방법을 설명하시오.`
8. `초음파 레벨센서의 허위에코와 다중반사 대책을 설명하시오.`
9. `거품, 증기, 난류와 분진이 초음파 레벨 측정에 미치는 영향을 설명하시오.`
10. `초음파 센서의 노즐 설치, 장애물과 센서 간 간섭 대책을 설명하시오.`
11. `초음파 레벨 트랜스미터의 교정, 에코맵과 진단방법을 설명하시오.`
12. `초음파 센서의 반복주기, 평균화와 동적 응답의 관계를 설명하시오.`
13. `초음파식과 레이더식 비접촉 레벨 측정의 적용조건을 비교하시오.`
14. `초음파 거리·레벨 측정의 주요 오차원인과 개선방법을 설명하시오.`

## 10. Expected Question Patterns

1. `초음파 센서의 기본 구성과 펄스 에코 측정원리`
   - required anchors:
     - `ultrasonic_sensor_system_structure`
     - `ultrasonic_piezoelectric_transduction`
     - `ultrasonic_pulse_echo_time_of_flight`
     - `ultrasonic_round_trip_distance_equation`
     - `ultrasonic_sound_speed_medium_dependence`

2. `비행시간과 왕복 거리 계산`
   - required anchors:
     - `ultrasonic_pulse_echo_time_of_flight`
     - `ultrasonic_round_trip_distance_equation`
     - `ultrasonic_sound_speed_medium_dependence`
     - `ultrasonic_air_temperature_compensation`

3. `음속 변화와 온도보상`
   - required anchors:
     - `ultrasonic_sound_speed_medium_dependence`
     - `ultrasonic_air_temperature_compensation`

4. `사각지대와 최소 측정거리`
   - required anchors:
     - `ultrasonic_dead_zone_ringdown`
     - `ultrasonic_repetition_rate_response_averaging`

5. `빔각과 대상물 반사특성`
   - required anchors:
     - `ultrasonic_beam_angle_footprint`
     - `ultrasonic_target_reflectivity_orientation`
     - `ultrasonic_echo_amplitude_validity`

6. `주파수, 분해능과 최대 측정거리`
   - required anchors:
     - `ultrasonic_frequency_range_resolution_tradeoff`
     - `ultrasonic_attenuation_max_range`

7. `탱크 레벨 측정과 기준높이`
   - required anchors:
     - `ultrasonic_pulse_echo_time_of_flight`
     - `ultrasonic_round_trip_distance_equation`
     - `ultrasonic_level_measurement_reference`

8. `허위에코와 다중반사 대책`
   - required anchors:
     - `ultrasonic_false_echo_multiple_reflection`
     - `ultrasonic_mounting_nozzle_obstruction_error`
     - `ultrasonic_calibration_echo_mapping_diagnostics`

9. `거품, 증기, 난류와 분진 영향`
   - required anchors:
     - `ultrasonic_echo_amplitude_validity`
     - `ultrasonic_foam_vapor_turbulence_error`

10. `노즐, 장애물과 센서 간 간섭`
    - required anchors:
      - `ultrasonic_beam_angle_footprint`
      - `ultrasonic_mounting_nozzle_obstruction_error`
      - `ultrasonic_sensor_crosstalk`

11. `시운전 교정과 에코 진단`
    - required anchors:
      - `ultrasonic_air_temperature_compensation`
      - `ultrasonic_false_echo_multiple_reflection`
      - `ultrasonic_calibration_echo_mapping_diagnostics`

12. `반복주기, 평균화와 동적 응답`
    - required anchors:
      - `ultrasonic_attenuation_max_range`
      - `ultrasonic_repetition_rate_response_averaging`

13. `초음파식과 레이더식 적용조건 비교`
    - required anchors:
      - `ultrasonic_foam_vapor_turbulence_error`
      - `ultrasonic_mounting_nozzle_obstruction_error`
      - `ultrasonic_application_limits_comparison`

14. `거리·레벨 측정의 종합 오차와 개선`
    - required anchors:
      - `ultrasonic_sound_speed_medium_dependence`
      - `ultrasonic_air_temperature_compensation`
      - `ultrasonic_dead_zone_ringdown`
      - `ultrasonic_beam_angle_footprint`
      - `ultrasonic_target_reflectivity_orientation`
      - `ultrasonic_frequency_range_resolution_tradeoff`
      - `ultrasonic_attenuation_max_range`
      - `ultrasonic_echo_amplitude_validity`
      - `ultrasonic_false_echo_multiple_reflection`
      - `ultrasonic_foam_vapor_turbulence_error`
      - `ultrasonic_mounting_nozzle_obstruction_error`
      - `ultrasonic_sensor_crosstalk`
      - `ultrasonic_repetition_rate_response_averaging`
      - `ultrasonic_calibration_echo_mapping_diagnostics`
      - `ultrasonic_application_limits_comparison`

## 11. Semantic review requirements

ChatGPT는 Source JSON 생성 전에 다음 사항을 직접 검토한다.

1. 반사형 거리식이 \(d=ct/2\)인지 확인한다.
2. 반사형과 투과형 구성을 혼동하지 않았는지 확인한다.
3. 음속의 온도 및 매질 의존성을 설명했는지 확인한다.
4. 기체 압력만으로 음속을 단순 비례 보정하지 않았는지 확인한다.
5. 반사파 진폭과 비행시간의 역할을 구분했는지 확인한다.
6. 링다운과 수신회복시간이 사각지대를 만드는 과정을 설명했는지 확인한다.
7. 빔각, 대상물 경사와 표면상태의 영향을 설명했는지 확인한다.
8. 주파수와 분해능·최대거리의 절충관계를 설명했는지 확인한다.
9. 레벨 계산에서 기준높이와 측정거리를 구분했는지 확인한다.
10. 허위에코, 다중반사와 에코 선택대책을 설명했는지 확인한다.
11. 거품, 증기, 난류와 분진의 영향을 절대적으로 단정하지 않았는지 확인한다.
12. 노즐, 장애물과 센서 간 크로스토크를 포함했는지 확인한다.
13. 평균화가 안정성을 높이지만 응답속도를 늦출 수 있음을 설명했는지 확인한다.
14. 초음파식과 레이더식의 적용성을 공정조건에 따라 비교했는지 확인한다.

## 12. Validation policy

- 요구사항 Markdown을 먼저 확정한다.
- ChatGPT가 기존 Schema에 맞춰 Source JSON을 직접 작성한다.
- Gemini 또는 Ollama에 JSON 생성을 요청하지 않는다.
- 독립 LLM semantic evaluation은 실행하지 않는다.
- Source JSON의 LLM 검토는 ChatGPT가 직접 수행한다.
- 스크립트에서는 LLM 검증을 건너뛴다.
- Production source 변경이 없는 Topic Pack이므로 host focused validation을 수행한다.
- 컨테이너 hostname, mount, dependency와 runtime 동작 변경이 없으면 container smoke를 실행하지 않는다.
- 테스트 수는 코드에서 동적으로 계산한다.
- 요구사항 검토가 끝나기 전에는 파일을 stage하지 않는다.
