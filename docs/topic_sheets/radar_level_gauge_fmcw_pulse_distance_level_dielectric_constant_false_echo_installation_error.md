# 레이더식 레벨계의 FMCW·펄스 방식, 거리·레벨 측정원리, 유전율 영향 및 허위에코·설치오차

## 1. Topic metadata

- `topic_id`: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
- `title_ko`: `레이더식 레벨계의 FMCW·펄스 방식, 거리·레벨 측정원리, 유전율 영향 및 허위에코·설치오차`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `semantic_execution`: `LLM_ONLY`
- `deterministic_checks.enabled`: `false`
- `candidate_extraction`: `{}`
- `topic_label`: `레이더식 레벨계`

이 Topic Pack은 자유공간형 비접촉 레이더식 레벨계를 중심으로 한다.

펄스 레이더의 왕복 비행시간 방식과 FMCW 레이더의 선형 주파수 스윕·비트주파수 방식을 구분한다.

거리와 레벨의 관계, 유전율에 따른 반사강도, 빔 경로, 불감대, 허위에코, 다중반사 및 설치오차를 하나의 측정사슬로 평가한다.

## 2. Scope

포함 범위는 다음과 같다.

1. 레이더식 레벨계의 송신부, 안테나, 수신부, 신호처리부 및 출력부
2. 자유공간에서의 전자기파 송신과 액면·분체 표면 반사
3. 펄스 레이더의 왕복 비행시간과 거리식
4. FMCW 레이더의 선형 주파수 스윕과 지연시간
5. 송신파와 수신파의 비트주파수 생성
6. 스윕 기울기와 비트주파수를 이용한 거리 계산
7. 변조 대역폭과 거리 분해능의 관계
8. 기준거리, 빈 탱크 거리, 측정거리 및 레벨 계산
9. 상대유전율과 반사계수 및 에코강도의 관계
10. 저유전율 유체·분체의 약한 반사 문제
11. 안테나 크기, 주파수, 빔각 및 조사면적
12. 안테나 부근의 불감대와 블로킹 거리
13. 노즐, 탱크 벽, 교반기 및 내부구조물에 의한 허위에코
14. 다중반사와 바닥·천장 반사
15. 거품, 난류, 경사면, 파동 및 분진의 영향
16. 증기, 응축, 고온·고압 및 가스층의 영향
17. 안테나 오염, 부착물 및 결로
18. 설치각도, 노즐 치수 및 빔 경로 확보
19. 에코맵, 허위에코 억제, 임계값 및 진단
20. 펄스식, FMCW식, GWR식 및 초음파식의 적용조건 비교

제외 범위는 다음과 같다.

- 항공·차량용 속도 레이더의 도플러 속도측정
- SAR 영상처리
- 레이더 안테나의 전자기장 수치해석
- 통신용 FMCW 변복조 설계
- 도파관 내부의 상세 모드 해석
- GWR 프로브 구조만을 독립적으로 다루는 문제
- 방사선식 레벨계의 감마선 감쇠원리

## 3. Required principle chain

답안은 다음 측정사슬을 논리적으로 연결해야 한다.

1. 송신부가 마이크로파 펄스 또는 선형 주파수 스윕 신호를 생성한다.
2. 안테나가 전자기파를 공정공간으로 방사한다.
3. 전자기파가 액면 또는 분체 표면에서 반사된다.
4. 안테나와 수신부가 반사 에코를 검출한다.
5. 펄스식은 송신과 수신 사이의 왕복시간을 계측한다.
6. 펄스식 거리는 `D=cτ/2`로 계산한다.
7. FMCW식은 송신주파수를 시간에 따라 선형적으로 변화시킨다.
8. 지연된 수신파와 현재 송신파를 혼합하여 비트주파수를 구한다.
9. 정지 표적의 이상적인 선형 스윕에서는 `f_b=Sτ`가 성립한다.
10. FMCW 거리는 `D=cf_b/(2S)`로 계산한다.
11. 기준점에서 표면까지의 거리 `D`를 얻는다.
12. 탱크 기준거리 또는 빈 탱크 거리 `E`에서 `D`를 빼 레벨 `L=E-D`를 구한다.
13. 유전율과 표면상태에 따른 에코강도를 평가한다.
14. 노즐과 내부구조물에서 발생한 허위에코를 실제 표면 에코와 분리한다.
15. 설치조건과 공정조건을 반영해 에코맵, 임계값 및 필터를 설정한다.
16. 진단정보와 실제 기준레벨을 비교하여 시운전·교정한다.

## 4. Technical boundary and wording rules

### 4.1 Electromagnetic propagation

레이더식 레벨계는 음파가 아니라 전자기파를 사용한다.

기체공간에서의 전파속도는 대체로 광속에 가깝다.

일반적인 공정조건에서는 온도변화가 초음파식의 음속변화만큼 직접적인 거리오차를 만들지 않는다.

다만 고압가스, 고밀도 증기, 응축층 또는 특수한 가스조성은 전파특성과 에코품질에 영향을 줄 수 있으므로 절대적으로 무관하다고 표현하지 않는다.

### 4.2 Pulse radar distance

펄스 레이더는 송신펄스와 반사펄스 사이의 왕복시간 `τ`를 측정한다.

표면까지의 편도거리는 다음과 같다.

`D=cτ/2`

`c`는 해당 매질에서의 전자기파 전파속도이다.

왕복거리이므로 반드시 2로 나눈다.

### 4.3 FMCW radar distance

FMCW 레이더는 주파수를 시간에 따라 연속적으로 변화시키는 처프 신호를 송신한다.

선형 스윕의 기울기를 `S=Δf/T_s`라 한다.

정지한 표면에서 도플러 성분을 무시하면 수신파는 왕복지연 `τ`만큼 늦게 도착한다.

현재 송신파와 지연된 수신파의 주파수 차가 비트주파수 `f_b`가 된다.

이상적인 선형 스윕에서는 다음 관계를 사용한다.

`f_b=Sτ`

`D=cτ/2=cf_b/(2S)`

비트주파수는 스윕 기울기와 지연시간을 함께 고려해야 한다.

### 4.4 Bandwidth and range resolution

FMCW 거리 분해능은 변조 대역폭 `B`와 관련된다.

이상적인 대표식은 다음과 같다.

`ΔR≈c/(2B)`

대역폭이 클수록 서로 가까운 두 반사면을 분리하기 유리하다.

펄스식에서도 짧은 펄스폭과 넓은 신호대역폭은 거리 분해능 향상에 유리하다.

분해능, 최대거리, 신호대잡음비, 안테나 구조 및 신호처리는 함께 검토해야 한다.

### 4.5 Level calculation

레이더식 레벨계가 직접 구하는 기본값은 기준점에서 표면까지의 거리 `D`이다.

탱크 기준거리 또는 빈 탱크 거리 `E`가 정의되면 레벨은 다음과 같이 계산한다.

`L=E-D`

기준점, 안테나 기준면, 노즐 높이 및 탱크 바닥 기준이 일치해야 한다.

### 4.6 Dielectric constant and reflection

레이더 반사는 표면의 전기적 특성과 경계조건에 영향을 받는다.

공기에서 비자성 유전체로 수직입사하는 이상화된 경계에서 전기장 진폭 반사계수는 다음과 같다.

`Γ=(1-√ε_r)/(1+√ε_r)`

반사계수의 크기는 `|Γ|=(√ε_r-1)/(√ε_r+1)`이며, 반사전력 비율은 `R=|Γ|²`에 대응한다.

상대유전율 `ε_r`이 낮으면 일반적으로 반사에코가 약해질 수 있다.

유전율만으로 모든 현장 에코를 결정할 수 없으며 표면경사, 거칠기, 안테나 편파, 빔각, 거리 및 장애물도 고려해야 한다.

### 4.7 Echo amplitude and distance

에코 진폭은 반사면의 존재와 신뢰도, 에코마진을 판단하는 정보이다.

거리는 펄스의 왕복시간 또는 FMCW의 비트주파수로 결정한다.

에코 진폭 자체를 거리 또는 레벨과 동일시하지 않는다.

### 4.8 Blocking distance

안테나 부근에서는 송신 누설, 수신기 포화, 내부반사 및 신호처리 한계 때문에 정상측정이 어려운 구간이 생길 수 있다.

이 구간을 블로킹 거리, 불감대 또는 최소 측정거리로 관리한다.

블로킹 거리는 모든 기기에서 0이라고 가정하지 않는다.

### 4.9 Beam, antenna and frequency

빔각은 안테나 크기, 구조 및 사용주파수에 영향을 받는다.

같은 개구크기에서는 일반적으로 높은 주파수가 더 좁은 빔을 형성하기 유리하다.

좁은 빔은 벽, 노즐 및 내부구조물의 영향을 줄이는 데 유리할 수 있다.

그러나 고주파가 모든 공정에서 항상 우수한 것은 아니다.

응축, 안테나 부착물, 분진, 최대거리, 공정창 구조 및 비용을 함께 검토한다.

### 4.10 False echo and multiple reflection

노즐, 탱크 벽, 사다리, 보강재, 교반기, 가열코일 및 충전물은 허위에코를 만들 수 있다.

표면과 탱크 구조물 사이에서 다중반사가 발생할 수 있다.

허위에코는 에코맵, 거리창, 추적 알고리즘, 임계값 및 설치개선으로 억제한다.

실제 표면 에코와 허위에코를 단순히 진폭 크기 하나만으로 구분하지 않는다.

### 4.11 Process effects

난류, 파동, 경사진 분체표면 및 교반은 반사방향과 에코분포를 변화시킨다.

거품은 두께, 수분함량, 밀도 및 유전특성에 따라 투과·반사·감쇠 특성이 달라진다.

증기와 분진은 일반적인 조건에서 초음파식보다 영향이 작을 수 있지만 항상 무시할 수 있는 것은 아니다.

고온·고압, 응축 및 안테나 결로는 적용성과 신뢰도를 별도로 검토한다.

### 4.12 Installation and diagnostics

안테나는 가능한 한 노즐 내부반사를 줄이고 빔 경로가 표면을 향하도록 설치한다.

긴 노즐, 작은 노즐직경, 안테나 매몰, 기울어진 설치 및 충전물 유입경로는 오차요인이 된다.

안테나 끝이 적절히 노출되도록 제조사 설치기준을 확인한다.

시운전 시 빈 탱크 기준, 실제 레벨, 에코곡선, 에코마진, 허위에코 맵 및 진단상태를 확인한다.

## 5. Fact Anchors

1. `radar_level_system_structure`
   - 레이더식 레벨계는 송신·주파수생성부, 안테나, 수신·혼합부, 거리신호처리부, 레벨환산부 및 출력부로 구성된다.
   - 펄스식과 FMCW식은 거리추정 방법이 다르지만 반사에코를 이용한다.

2. `radar_electromagnetic_wave_reflection`
   - 안테나가 마이크로파 전자기파를 방사하고 액면 또는 분체표면에서 반사된 에코를 수신한다.
   - 레이더식은 음파식이 아니다.

3. `radar_pulse_time_of_flight`
   - 펄스식은 송신펄스와 반사펄스 사이의 왕복 비행시간을 측정한다.
   - 수신지연은 표면까지의 왕복경로에 해당한다.

4. `radar_pulse_distance_equation`
   - 펄스식 거리는 `D=cτ/2`로 계산한다.
   - 왕복시간이므로 2로 나누어야 한다.

5. `radar_fmcw_linear_frequency_sweep`
   - FMCW식은 시간에 따라 주파수가 선형적으로 변하는 처프를 연속 송신한다.
   - 스윕 기울기는 `S=Δf/T_s`로 정의할 수 있다.

6. `radar_fmcw_beat_frequency_distance`
   - 지연된 수신파와 현재 송신파를 혼합하면 비트주파수가 발생한다.
   - 정지 표적의 이상적인 선형 스윕에서는 `f_b=Sτ`, `D=cf_b/(2S)`를 사용한다.

7. `radar_bandwidth_range_resolution`
   - FMCW 거리 분해능의 대표식은 `ΔR≈c/(2B)`이다.
   - 변조 대역폭이 클수록 인접한 반사면을 분리하기 유리하다.

8. `radar_level_reference_calculation`
   - 측정거리 `D`와 기준거리 또는 빈 탱크 거리 `E`를 이용해 `L=E-D`로 레벨을 계산한다.
   - 안테나 기준면과 탱크 기준점이 일치해야 한다.

9. `radar_dielectric_constant_reflection`
   - 상대유전율은 경계면의 반사계수와 에코강도에 영향을 준다.
   - 공기에서 비자성 유전체로 수직입사할 때 전기장 진폭 반사계수는 `Γ=(1-√ε_r)/(1+√ε_r)`이며, 그 크기는 `|Γ|=(√ε_r-1)/(√ε_r+1)`이다.

10. `radar_low_dielectric_echo_margin`
    - 저유전율 유체나 분체는 반사에코가 약할 수 있다.
    - 적용성은 유전율뿐 아니라 거리, 표면상태, 안테나 이득과 잡음마진을 함께 검토한다.

11. `radar_antenna_beam_footprint`
    - 빔각과 측정거리가 조사면적을 결정한다.
    - 빔 경로에 벽, 노즐 또는 내부구조물이 들어오면 허위에코 가능성이 증가한다.

12. `radar_frequency_antenna_tradeoff`
    - 같은 개구크기에서 높은 주파수는 좁은 빔과 작은 안테나 구현에 유리할 수 있다.
    - 주파수 선택은 분해능, 최대거리, 응축, 부착물, 공정창 및 비용을 함께 고려한다.

13. `radar_blocking_distance_near_field`
    - 송신 누설, 수신기 포화, 내부반사 및 근거리 신호처리 한계로 블로킹 거리가 발생할 수 있다.
    - 최대 레벨이 블로킹 구간에 들어가지 않도록 설치범위를 정한다.

14. `radar_false_echo_multiple_reflection`
    - 노즐, 벽, 교반기, 보강재 및 가열코일은 허위에코를 만들 수 있다.
    - 탱크 구조와 표면 사이의 다중반사도 잘못된 거리피크를 만들 수 있다.

15. `radar_surface_foam_turbulence_slope`
    - 거품, 난류, 파동 및 경사진 분체표면은 에코의 방향·진폭·분포를 변화시킨다.
    - 추적필터와 평균화는 응답속도와 안정성의 절충을 가진다.

16. `radar_vapor_pressure_temperature_effect`
    - 일반적인 증기와 온도변화의 영향은 초음파식보다 작을 수 있다.
    - 고압가스, 고밀도 증기, 응축 및 특수 가스층의 영향까지 항상 0이라고 단정하지 않는다.

17. `radar_mounting_nozzle_obstruction_error`
    - 긴 노즐, 작은 노즐직경, 안테나 매몰, 기울어진 설치 및 빔 경로의 장애물은 측정오차를 유발한다.
    - 안테나와 노즐의 치수 및 돌출조건은 제조사 설치기준을 따라야 한다.

18. `radar_antenna_buildup_condensation`
    - 안테나의 부착물, 코팅, 응축 및 결로는 송수신 손실과 허위에코를 증가시킬 수 있다.
    - 퍼지, 가열, 적절한 재질과 예방정비를 검토한다.

19. `radar_echo_mapping_calibration_diagnostics`
    - 시운전 시 기준거리, 실제 레벨, 에코곡선, 에코마진과 허위에코 맵을 확인한다.
    - 거리창, 임계값, 추적설정 및 진단정보를 공정조건에 맞게 조정한다.

20. `radar_pulse_fmcw_application_selection`
    - 펄스식은 왕복시간을, FMCW식은 스윕 기울기와 비트주파수를 이용한다.
    - 방식 선정은 거리, 분해능, 유전율, 공정조건, 설치공간, 기존설비 연계 및 비용을 기준으로 한다.

## 6. Fatal Wrong Claims

1. `radar_fatal_sound_speed_principle`
   - wrong: 레이더식 레벨계는 공기 중 음속을 이용한다.
   - correction: 레이더식은 전자기파를 이용하며 기체공간에서 전파속도는 대체로 광속에 가깝다.

2. `radar_fatal_no_round_trip_half`
   - wrong: 펄스의 왕복시간에 광속을 곱한 값이 그대로 편도거리이다.
   - correction: 왕복경로이므로 `D=cτ/2`로 계산한다.

3. `radar_fatal_fmcw_direct_time_only`
   - wrong: FMCW식은 펄스식과 동일하게 송수신 시각만 직접 측정한다.
   - correction: FMCW식은 주파수 스윕과 지연된 수신파의 비트주파수를 이용한다.

4. `radar_fatal_beat_frequency_independent_of_slope`
   - wrong: FMCW 거리는 스윕 기울기와 무관하고 비트주파수만 알면 항상 동일하게 계산된다.
   - correction: `D=cf_b/(2S)`이므로 비트주파수와 스윕 기울기를 함께 사용한다.

5. `radar_fatal_narrow_band_better_resolution`
   - wrong: FMCW 변조 대역폭이 작을수록 거리 분해능이 좋아진다.
   - correction: 대표식 `ΔR≈c/(2B)`에서 대역폭이 클수록 분해능이 좋아진다.

6. `radar_fatal_dielectric_no_effect`
   - wrong: 측정물의 상대유전율은 반사에코에 전혀 영향을 주지 않는다.
   - correction: 상대유전율은 반사계수와 에코마진에 영향을 준다.

7. `radar_fatal_echo_amplitude_is_level`
   - wrong: 에코 진폭 자체가 거리 또는 레벨이다.
   - correction: 거리는 왕복시간 또는 비트주파수로 구하고 진폭은 에코 신뢰도를 판단하는 정보이다.

8. `radar_fatal_zero_blocking_distance`
   - wrong: 모든 레이더식 레벨계는 안테나 바로 앞까지 오차 없이 측정한다.
   - correction: 송신 누설, 수신기 포화와 내부반사로 블로킹 거리가 발생할 수 있다.

9. `radar_fatal_process_conditions_never_matter`
   - wrong: 증기, 고압, 응축, 거품, 난류와 안테나 오염은 레이더 측정에 절대로 영향을 주지 않는다.
   - correction: 영향이 상대적으로 작을 수 있으나 공정조건과 설치조건에 따라 에코품질과 신뢰도가 달라진다.

10. `radar_fatal_no_false_echo_installation_error`
    - wrong: 레이더식은 노즐, 벽, 교반기와 설치각도에 관계없이 항상 실제 표면만 검출한다.
    - correction: 내부구조물과 부적절한 설치는 허위에코와 다중반사를 만들 수 있다.

## 7. Routing Aliases

1. `radar level gauge`
2. `radar level transmitter`
3. `non-contact radar level measurement`
4. `free space radar level`
5. `pulse radar level`
6. `pulsed radar level transmitter`
7. `radar time of flight level`
8. `FMCW radar level`
9. `frequency modulated continuous wave level radar`
10. `FMCW beat frequency ranging`
11. `radar chirp level measurement`
12. `radar dielectric constant level`
13. `radar false echo mapping`
14. `radar blocking distance`
15. `80 GHz radar level`
16. `microwave level transmitter`
17. `레이더식 레벨계`
18. `레이더 레벨 트랜스미터`
19. `비접촉 레이더 레벨 측정`
20. `자유공간 레이더 레벨계`
21. `펄스 레이더 레벨계`
22. `펄스식 레이더 수위계`
23. `레이더 비행시간 레벨 측정`
24. `FMCW 레이더 레벨계`
25. `주파수 변조 연속파 레벨계`
26. `FMCW 비트주파수 거리측정`
27. `레이더 처프 측정`
28. `레이더 유전율 영향`
29. `레이더 허위에코 맵`
30. `레이더 불감대`
31. `80GHz 레이더 레벨계`
32. `마이크로파 레벨 트랜스미터`

## 8. Routing Field Points

1. `노즐 치수·안테나 돌출조건 및 빔 경로 확보`
2. `측정물 유전율과 에코마진에 따른 적용성 검토`
3. `탱크 내부구조물·교반기에 대한 허위에코 맵 설정`
4. `안테나 부착물·응축·결로에 대한 유지보수 대책`
5. `펄스·FMCW·GWR·초음파 방식의 비용과 기존설비 연계 비교`

## 9. Question Examples

1. 레이더식 레벨계의 측정원리와 특징을 설명하시오.
2. 펄스 레이더식 레벨계의 비행시간과 거리 계산식을 설명하시오.
3. FMCW 레이더식 레벨계의 처프와 비트주파수 측정원리를 설명하시오.
4. 펄스식과 FMCW식 레이더 레벨계의 거리측정 방식을 비교하시오.
5. FMCW 레이더의 변조 대역폭과 거리 분해능의 관계를 설명하시오.
6. 상대유전율이 레이더 레벨 측정의 반사강도에 미치는 영향을 설명하시오.
7. 레이더식 레벨계의 측정거리와 탱크 레벨 계산방법을 설명하시오.
8. 레이더식 레벨계의 블로킹 거리와 최소 측정거리 발생원인을 설명하시오.
9. 레이더 안테나의 주파수, 빔각과 조사면적이 측정에 미치는 영향을 설명하시오.
10. 레이더식 레벨계의 허위에코와 다중반사 발생원인 및 대책을 설명하시오.
11. 거품, 난류, 증기, 분진 및 고압조건이 레이더 레벨 측정에 미치는 영향을 설명하시오.
12. 레이더 레벨계의 노즐 설치, 장애물, 안테나 부착물과 결로 대책을 설명하시오.
13. 레이더 레벨 트랜스미터의 교정, 에코맵 및 진단방법을 설명하시오.
14. 펄스식·FMCW식·GWR식·초음파식 레벨계의 적용조건을 비교하시오.

## 10. Expected Question Patterns

1. **레이더식 레벨계의 전체 측정원리**
   - intent: 구성, 전자기파 송수신 및 거리·레벨 변환을 설명한다.
   - required anchors:
     - `radar_level_system_structure`
     - `radar_electromagnetic_wave_reflection`
     - `radar_pulse_time_of_flight`
     - `radar_fmcw_linear_frequency_sweep`

2. **펄스 레이더의 비행시간과 거리식**
   - intent: 왕복시간과 편도거리 계산을 설명한다.
   - required anchors:
     - `radar_electromagnetic_wave_reflection`
     - `radar_pulse_time_of_flight`
     - `radar_pulse_distance_equation`
     - `radar_blocking_distance_near_field`

3. **FMCW 처프와 비트주파수**
   - intent: 선형 스윕, 지연시간, 비트주파수 및 거리계산을 설명한다.
   - required anchors:
     - `radar_electromagnetic_wave_reflection`
     - `radar_fmcw_linear_frequency_sweep`
     - `radar_fmcw_beat_frequency_distance`
     - `radar_bandwidth_range_resolution`

4. **펄스식과 FMCW식 비교**
   - intent: 두 방식의 거리추정 변수와 적용조건을 비교한다.
   - required anchors:
     - `radar_pulse_time_of_flight`
     - `radar_pulse_distance_equation`
     - `radar_fmcw_linear_frequency_sweep`
     - `radar_fmcw_beat_frequency_distance`
     - `radar_pulse_fmcw_application_selection`

5. **대역폭과 거리 분해능**
   - intent: 변조 대역폭, 비트주파수 처리 및 안테나 주파수의 관계를 설명한다.
   - required anchors:
     - `radar_fmcw_beat_frequency_distance`
     - `radar_bandwidth_range_resolution`
     - `radar_frequency_antenna_tradeoff`

6. **유전율과 에코강도**
   - intent: 상대유전율, 반사계수, 약한 에코와 표면조건을 설명한다.
   - required anchors:
     - `radar_electromagnetic_wave_reflection`
     - `radar_dielectric_constant_reflection`
     - `radar_low_dielectric_echo_margin`
     - `radar_surface_foam_turbulence_slope`

7. **거리와 레벨 환산**
   - intent: 측정거리, 기준거리와 탱크 레벨의 관계를 설명한다.
   - required anchors:
     - `radar_pulse_distance_equation`
     - `radar_level_reference_calculation`
     - `radar_dielectric_constant_reflection`

8. **블로킹 거리**
   - intent: 근거리 불감대의 원인과 최대레벨 설정방법을 설명한다.
   - required anchors:
     - `radar_level_system_structure`
     - `radar_blocking_distance_near_field`
     - `radar_mounting_nozzle_obstruction_error`

9. **안테나, 주파수와 빔 경로**
   - intent: 빔각, 조사면적, 주파수 및 설치장애물의 영향을 설명한다.
   - required anchors:
     - `radar_antenna_beam_footprint`
     - `radar_frequency_antenna_tradeoff`
     - `radar_surface_foam_turbulence_slope`
     - `radar_mounting_nozzle_obstruction_error`

10. **허위에코와 다중반사**
    - intent: 탱크 내부구조물의 반사와 신호처리 대책을 설명한다.
    - required anchors:
      - `radar_antenna_beam_footprint`
      - `radar_false_echo_multiple_reflection`
      - `radar_mounting_nozzle_obstruction_error`
      - `radar_echo_mapping_calibration_diagnostics`

11. **거품, 난류, 증기와 고압**
    - intent: 표면변동과 가스공간의 공정조건 영향을 설명한다.
    - required anchors:
      - `radar_dielectric_constant_reflection`
      - `radar_surface_foam_turbulence_slope`
      - `radar_vapor_pressure_temperature_effect`
      - `radar_antenna_buildup_condensation`

12. **노즐 설치와 안테나 오염**
    - intent: 노즐, 설치각도, 부착물과 결로의 대책을 설명한다.
    - required anchors:
      - `radar_mounting_nozzle_obstruction_error`
      - `radar_antenna_buildup_condensation`
      - `radar_echo_mapping_calibration_diagnostics`

13. **교정, 에코맵과 진단**
    - intent: 기준거리 설정, 허위에코 억제 및 진단방법을 설명한다.
    - required anchors:
      - `radar_false_echo_multiple_reflection`
      - `radar_antenna_buildup_condensation`
      - `radar_echo_mapping_calibration_diagnostics`

14. **레벨계 방식 선정**
    - intent: 유전율, 주파수, 공정가스 및 방식별 적용한계를 비교한다.
    - required anchors:
      - `radar_low_dielectric_echo_margin`
      - `radar_frequency_antenna_tradeoff`
      - `radar_vapor_pressure_temperature_effect`
      - `radar_pulse_fmcw_application_selection`

## 11. Semantic review requirements

LLM 검증은 다음 항목을 직접 판단한다.

1. 레이더식이 음파가 아닌 전자기파 방식으로 설명되었는가.
2. 펄스식의 왕복시간과 `D=cτ/2`가 정확한가.
3. FMCW의 선형 스윕, 지연수신파 및 비트주파수의 관계가 정확한가.
4. `f_b=Sτ`와 `D=cf_b/(2S)`의 변수관계가 정확한가.
5. 대역폭과 거리 분해능의 관계가 정확한가.
6. 측정거리와 탱크 레벨의 관계가 정확한가.
7. 유전율이 반사강도와 에코마진에 미치는 영향이 설명되었는가.
8. 에코 진폭을 거리와 혼동하지 않았는가.
9. 블로킹 거리의 원인이 설명되었는가.
10. 빔각, 주파수와 안테나 크기의 관계가 과도하게 단정되지 않았는가.
11. 허위에코와 다중반사 원인 및 대책이 연결되었는가.
12. 거품, 난류, 증기, 고압, 응축 및 분진의 영향이 조건부로 설명되었는가.
13. 노즐, 설치각도, 안테나 돌출과 장애물의 영향이 설명되었는가.
14. 안테나 부착물과 결로의 유지보수 대책이 포함되었는가.
15. 펄스식과 FMCW식 중 하나를 절대적으로 우수하다고 단정하지 않았는가.
16. 기존설비 연계, 비용, 시운전 및 유지보수 조건을 방식선정에 반영했는가.
17. 20개 Fact Anchor가 질문패턴에서 모두 한 번 이상 참조되는가.
18. Fatal Wrong Claim 10개가 Fact Anchor와 모순 없이 정의되었는가.
19. Routing Alias가 다른 센서 Topic을 과도하게 탈취하지 않는가.
20. 기존 초음파 Topic의 고유 의미가 레이더 Topic에 잘못 복사되지 않았는가.

## 12. Validation policy

- Requirements Markdown을 먼저 확정한다.
- Source JSON은 이 Markdown 계약을 기준으로 ChatGPT가 직접 작성한다.
- Gemini 또는 로컬 Ollama를 이용한 JSON 생성은 수행하지 않는다.
- `deterministic_checks.enabled`는 `false`로 유지한다.
- `candidate_extraction`은 빈 객체 `{}`로 유지한다.
- 의미검증은 LLM이 Fact Anchor, Fatal Wrong Claim 및 질문패턴의 정합성을 직접 검토한다.
- Source JSON 생성 후 Generated bank를 재빌드한다.
- Source와 Generated의 Topic별 계약이 일치하는지 검증한다.
- Router의 Question Example 정상선택과 타 Topic anti-steal을 검증한다.
- 기존 Router 및 Topic Pack의 focused regression을 실행한다.
- LLM 연동 또는 컨테이너 전용 실행경로를 변경하지 않으므로 컨테이너 E2E는 생략한다.
- 최종 release validation과 Rubric Audit을 통과한 뒤에만 staging과 commit을 수행한다.
