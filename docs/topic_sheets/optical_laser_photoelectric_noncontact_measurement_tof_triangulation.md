# 광전·레이저 비접촉 측정의 검출원리, ToF·삼각측량 알고리즘 및 오차·선정

## 1. Topic metadata

- `topic_id`: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`
- `official_criterion`: `IC-2027-W-2-2`
- `official_scope`: `비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `FIELD_APPLICATION`
- `selection_importance`: `NORMAL`
- `historical_frequency_used`: `false`
- `semantic_execution`: `LLM_ONLY`
- `deterministic_checks.enabled`: `false`
- `candidate_extraction.rules`: `[]`

## 2. Coverage purpose

현재 공식 범위의 비접촉 측정은 ultrasonic ToF와 radar FMCW/Pulse Topic으로 일부 충족되어 있다.
이 Topic은 기존 coverage의 잔여 범위인 **광학식 비접촉 측정과 광센서·레이저 기반 원리·알고리즘**을 보완한다.

## 3. Scope boundary

### 3.1 In scope

- 광전식 센서의 광전변환
- 투과형, 미러반사형, 확산반사형
- Optical Direct ToF
- Optical Indirect ToF
- Laser triangulation
- PSD, CCD, CMOS 기반 spot 위치 검출
- 반사율, 표면각, 색상, 투명체, 고광택 대상
- 주변광, speckle, alignment, occlusion, saturation, multipath
- calibration, accuracy, resolution, repeatability
- 현장 선정 trade-off

### 3.2 Out of scope / handoff

- 초음파 음속과 온도보상 → `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`
- Radar FMCW/Pulse와 유전율·허위에코 → `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
- 일반 센서 분류 전체 → 관련 sensor Topic
- 광통신 네트워크 → communication Topic

## 4. Required principle chain

### 4.1 Photoelectric detection

광원 → 대상/광로 → 수광소자 → 광전변환 → 증폭·필터링 → threshold/continuous processing → 존재·상태 판정

투과형은 발광기와 수광기가 분리되고, 미러반사형은 반사판을 사용하며, 확산반사형은 대상의 반사광을 직접 이용한다.
수광세기는 거리 외에도 반사율·색상·표면각·오염·배경에 좌우되므로 단순 intensity를 범용 절대거리로 해석하지 않는다.

### 4.2 Direct ToF

반사형 Direct ToF의 기본 사슬은 다음과 같다.

광 펄스 송신 → 대상 반사 → 수신 timestamp → 왕복시간 `Δt` → 거리 계산

`d = c·Δt/2`

여기서 `c`는 광의 전파속도이고, `/2`는 송신과 귀환의 왕복경로 때문이다.

### 4.3 Indirect ToF

변조광을 사용하면 송신신호와 수신신호의 위상지연으로 왕복 전파지연을 추정할 수 있다.
단일 변조주파수의 대표 관계는 다음 형태다.

`d = c·φ/(4πf_m)`

위상은 `2π` 주기로 반복되므로 phase wrapping과 비모호 거리 한계가 있다.
다중주파수, coding 또는 추가 추정으로 모호성을 완화할 수 있다.

### 4.4 Laser triangulation

레이저 투사광과 수광광학계 사이에 알려진 baseline과 기하를 구성한다.
대상 깊이가 변하면 반사 spot의 영상위치가 PSD·CCD·CMOS에서 이동한다.
검출기 좌표를 장치별 calibration model에 넣어 거리 또는 변위로 환산한다.

Laser triangulation은 **ToF가 아니다**.
실제 거리변환은 baseline, angle, focal length, detector position과 조립오차의 보정에 의존한다.

## 5. Error and field application chain

1. 반사율·색상·파장 → 수광량/SNR 변화
2. 고광택·거울면 → 정반사 방향 이탈
3. 투명·반투명 대상 → 표면/내부/후면 반사 혼합
4. 주변광 → noise floor, saturation margin 악화
5. laser speckle → centroid/intensity 변동
6. alignment/FOV/occlusion → 기하학적 설치오차
7. timing jitter/pulse width/threshold → ToF 거리불확도
8. saturation/low SNR → 거리·위치 estimator 왜곡
9. multipath/mixed pixel → 실제 표면과 다른 거리 추정
10. temperature/contamination/mechanical drift → calibration 변화

## 6. Performance terms

- Accuracy: 기준값과 측정값의 근접성
- Resolution: 구분 가능한 최소 변화
- Repeatability: 동일조건 반복측정의 산포

세 용어를 서로 동일한 값으로 사용하지 않는다.

## 7. Selection logic

광전식 존재검출, optical ToF, laser triangulation은 다음 조건으로 비교한다.

- 측정목적: presence / distance / displacement
- 측정범위
- 요구 분해능과 정확도
- 응답속도
- 대상 반사율·색상·투명도·광택
- 주변광과 오염
- 설치공간과 occlusion
- 안전 요구
- 비용과 유지관리

하나의 방식이 모든 대상과 범위에서 자동으로 최적이라고 주장하지 않는다.

## 8. Required Fact Anchors

총 `26`개 Anchor를 `fact_anchor.json`의 정본으로 사용한다.

1. `optical_noncontact_measurement_chain` — 광학식 비접촉 측정은 광원 또는 레이저의 방사, 대상과의 상호작용, 수광소자의 광전변환, 신호처리 및 거리·위치·존재 판정의 측정사슬로 구성된다.
2. `photoelectric_conversion_principle` — 광전식 센서는 입사광을 포토다이오드·포토트랜지스터 등의 수광소자가 전기신호로 변환하고, 증폭·필터링·임계값 또는 연속량 처리로 대상 상태를 판정한다.
3. `photoelectric_through_beam_mode` — 투과형 광전센서는 발광기와 수광기를 서로 마주보게 배치하고 대상이 광로를 차단할 때 수광량 변화로 존재를 검출하므로 긴 검출거리와 높은 광학 여유를 얻기 쉽다.
4. `photoelectric_retroreflective_mode` — 미러반사형 광전센서는 발광·수광부와 반사판을 같은 쪽에 두고 반사판으로 왕복하는 광을 대상이 차단하거나 변화시키는 방식이며, 편광 기능은 반사체와 대상의 오검출을 줄이는 데 사용할 수 있다.
5. `photoelectric_diffuse_reflective_mode` — 확산반사형 광전센서는 센서에서 방사한 광이 대상 표면에서 산란되어 되돌아오는 수광량을 이용하므로 대상의 반사율·색상·표면각도와 배경의 영향을 더 크게 받을 수 있다.
6. `photoelectric_intensity_boundary` — 수광 세기 기반 광전 검출에서 신호크기는 거리뿐 아니라 광원출력, 광학계, 대상 반사율, 입사각, 오염 및 배경에 좌우되므로 수광세기 하나를 보정 없이 절대거리로 해석할 수 없다.
7. `optical_direct_tof_round_trip` — 반사형 광학 Direct ToF는 광 펄스를 방사한 시점과 대상에서 반사되어 돌아온 광의 수신시점 사이의 왕복 비행시간을 계측한다.
8. `optical_direct_tof_distance_equation` — 같은 센서 위치에서 방사·수광하는 반사형 Direct ToF의 이상적 거리관계는 d=c·Δt/2이며, c는 광의 전파속도이고 2는 송신과 반사의 왕복경로를 보정한다.
9. `optical_indirect_tof_phase_principle` — Indirect ToF는 변조된 광의 송신신호와 수신신호 사이 위상지연을 측정해 왕복 전파지연을 추정하며, 단일 변조주파수의 대표식은 d=c·φ/(4πf_m) 형태로 표현할 수 있다.
10. `optical_itof_phase_ambiguity` — Indirect ToF의 위상은 2π 주기로 반복되므로 단일 변조주파수에서는 위상 래핑에 따른 비모호 거리 한계가 있으며, 다중주파수·코딩·추가 추정으로 모호성을 완화할 수 있다.
11. `laser_triangulation_principle` — 레이저 삼각측량은 투사광과 수광광학계 사이에 알려진 기하학적 기준선과 각도를 두고, 대상에서 반사된 레이저 spot의 영상 위치 변화로 대상의 거리 또는 변위를 계산한다.
12. `laser_triangulation_detector_coordinate` — 삼각측량 센서에서는 대상 깊이가 바뀌면 렌즈를 거친 반사 spot이 PSD·CCD·CMOS 등의 검출기에서 이동하며, 검출기 좌표가 보정된 기하모델을 통해 거리·변위로 변환된다.
13. `laser_triangulation_calibration` — 레이저 삼각측량의 거리변환은 렌즈 초점거리, 기준선, 투사각, 검출기 위치 및 조립오차를 포함한 실제 광학계 보정에 의존하므로 모든 장치에 공통인 하나의 단순식만으로 대체할 수 없다.
14. `triangulation_range_resolution_tradeoff` — 삼각측량은 기준선·광학배율·검출기 분해능과 측정범위 사이에 설계 trade-off가 있으며, spot 위치 변화에 대한 민감도가 높을수록 일반적으로 좁은 범위에서 높은 변위 분해능을 얻기 쉽다.
15. `surface_reflectivity_color_effect` — 광학 센서는 대상의 반사율·색상·재질과 파장에 따라 수광 신호와 SNR이 달라질 수 있으므로 동일 거리라도 검출여유와 측정불확도가 달라질 수 있다.
16. `specular_transparent_surface_error` — 거울면·고광택면은 정반사 방향 때문에 수광광이 검출기를 벗어날 수 있고, 투명·반투명 대상은 표면·내부·후면 반사가 겹쳐 다중응답이나 잘못된 거리 추정을 만들 수 있다.
17. `ambient_light_filtering` — 주변광은 수광부의 DC 성분·잡음·포화 가능성을 증가시키므로 광학필터, 변조·동기검파, 시간게이팅, 차광 및 임계값 설계를 통해 신호와 배경을 분리한다.
18. `laser_speckle_effect` — 레이저의 높은 공간적 결맞음성은 거친 표면에서 speckle 패턴을 만들 수 있고, 이는 spot centroid나 수광세기의 변동을 유발하여 삼각측량·영상기반 측정의 반복도에 영향을 줄 수 있다.
19. `alignment_occlusion_geometry` — 광학식 센서는 발광축·수광축·대상면의 정렬, 시야각, 가림과 설치거리의 영향을 받으며, 특히 삼각측량은 송광과 수광의 서로 다른 시선 때문에 occlusion 영역이 생길 수 있다.
20. `tof_timing_jitter_resolution` — Direct ToF의 거리 분해능과 불확도는 시간계측 분해능, 송수신 지터, 검출 임계값, 펄스폭 및 신호처리 방식에 영향을 받으므로 광속이 빠르다는 사실 자체가 높은 거리정확도를 보장하지 않는다.
21. `detector_saturation_dynamic_range` — 수광기가 포화되거나 신호가 노이즈 바닥에 가까우면 거리·위치 추정이 왜곡될 수 있으므로 광원출력, 수광이득, 노출시간, 동적범위와 SNR을 측정범위에 맞게 설계해야 한다.
22. `multipath_mixed_pixel_error` — 광학 ToF에서는 서로 다른 경로의 반사광이 한 수광요소에 동시에 들어오면 multipath 또는 mixed-pixel 오차가 발생하여 하나의 거리로 단순 환산한 값이 실제 표면과 다를 수 있다.
23. `calibration_reference_traceability` — 광학 비접촉 측정은 기준거리·기준변위 또는 표준시편을 이용해 zero·scale·비선형성과 설치기하를 확인하고, 온도변화·렌즈오염·기구변형 등 장기 drift를 주기적으로 점검해야 한다.
24. `accuracy_resolution_repeatability_boundary` — 분해능은 구분 가능한 최소 변화, 반복도는 동일조건 반복측정의 산포, 정확도는 기준값과의 근접성을 나타내므로 세 성능지표를 같은 의미로 사용해서는 안 된다.
25. `wavelength_material_selection` — 광원의 파장은 대상 재질의 반사·흡수·투과 특성과 수광소자 감도, 주변광 및 안전 요구를 함께 고려해 선정해야 하며, 가시광·근적외선 중 어느 하나가 모든 대상에 항상 우수하지는 않다.
26. `optical_method_selection_tradeoff` — 광전식 존재검출, Direct/Indirect ToF 거리측정, 레이저 삼각측량은 요구범위·분해능·응답속도·표면재질·주변광·설치공간·안전·비용에 따라 선정하며 하나의 방식이 모든 거리와 대상에서 최적일 수 없다.

## 9. Fatal Wrong Claims

총 `14`개 Fatal contract를 사용한다.

1. `optical_fatal_all_photoelectric_are_distance` — 모든 광전식 센서는 수광량만으로 절대거리를 직접 측정한다.
   - Correction: 투과형·미러반사형·확산반사형은 주로 존재검출에 사용되며, 절대거리 산출에는 별도의 ToF·삼각측량 등 거리 알고리즘이 필요하다.
2. `optical_fatal_tof_no_round_trip_half` — 반사형 Direct ToF의 거리는 d=c·Δt로 계산하며 2로 나눌 필요가 없다.
   - Correction: 같은 위치에서 송수광하는 반사형 왕복 ToF는 송신과 귀환 경로를 포함하므로 d=c·Δt/2가 기본 관계다.
3. `optical_fatal_tof_sound_speed` — 레이저 ToF는 공기 중 음속을 사용해 거리를 계산한다.
   - Correction: 광학 ToF는 광의 전파지연을 사용하며 기본 거리식에는 광속 c가 들어간다.
4. `optical_fatal_itof_unlimited_unique_phase` — Indirect ToF의 단일 위상값은 거리 제한 없이 항상 유일한 절대거리를 준다.
   - Correction: 위상은 2π 주기로 반복되므로 단일 변조주파수에는 비모호 거리 한계가 있다.
5. `optical_fatal_triangulation_is_tof` — 레이저 삼각측량은 송신 펄스가 돌아오는 비행시간을 측정하는 방식이다.
   - Correction: 삼각측량은 기준선과 투사·수광 기하 및 검출기 spot 위치를 이용하는 기하학적 거리·변위 측정이다.
6. `optical_fatal_triangulation_no_calibration` — 레이저 삼각측량은 센서 구조와 무관한 하나의 범용식만 쓰므로 기하보정이 필요 없다.
   - Correction: 실제 삼각측량 변환은 기준선, 투사각, 렌즈, 검출기 위치 및 조립오차를 포함한 장치별 보정에 의존한다.
7. `optical_fatal_intensity_equals_distance` — 확산반사형에서 수광세기는 거리만의 함수이므로 수광세기만 알면 재질과 무관하게 절대거리를 얻는다.
   - Correction: 수광세기는 거리 외에도 반사율, 색상, 각도, 오염, 광학계와 배경의 영향을 받으므로 단독으로 범용 절대거리로 해석할 수 없다.
8. `optical_fatal_surface_independent` — 레이저 센서는 거울면·투명체·검은색 대상에서도 표면특성과 무관하게 항상 같은 정확도를 낸다.
   - Correction: 정반사, 투과, 흡수, 다중반사와 낮은 SNR 때문에 표면특성에 따라 검출여유와 오차가 달라질 수 있다.
9. `optical_fatal_ambient_light_no_effect` — 능동광을 쓰는 광학센서는 주변광의 영향을 전혀 받지 않는다.
   - Correction: 주변광은 수광부 잡음과 포화 여유에 영향을 주며 필터, 동기검파, 게이팅, 차광 등의 대책이 필요하다.
10. `optical_fatal_resolution_equals_accuracy` — 센서의 분해능 수치가 곧 절대 정확도와 동일하다.
   - Correction: 분해능, 반복도, 정확도는 서로 다른 성능지표이며 각각 별도로 평가해야 한다.
11. `optical_fatal_tof_timing_error_negligible` — 빛의 속도가 매우 빠르므로 ToF의 시간분해능과 지터는 거리오차에 영향을 주지 않는다.
   - Correction: ToF는 매우 작은 시간차를 거리로 환산하므로 timing resolution, jitter, threshold와 pulse width가 거리 불확도에 직접 영향을 준다.
12. `optical_fatal_no_multipath` — 광학 ToF는 항상 단일 반사경로만 측정하므로 다중경로 오차가 발생하지 않는다.
   - Correction: 복수 반사경로가 동시에 수광되면 multipath 또는 mixed-pixel 오차로 잘못된 거리 추정이 발생할 수 있다.
13. `optical_fatal_noncontact_no_calibration` — 광학식은 비접촉이므로 설치 후 zero·scale·기하 교정이나 오염 점검이 필요 없다.
   - Correction: 비접촉 방식도 광학기하, 기준거리, 렌즈오염, 온도·기구 drift를 확인하는 교정과 점검이 필요하다.
14. `optical_fatal_laser_always_best` — 레이저 방식은 측정범위·재질·주변광·안전·비용과 관계없이 모든 비접촉 계측에서 항상 최적이다.
   - Correction: 광전식, ToF, 삼각측량은 범위·분해능·속도·표면·환경·안전·비용의 trade-off로 선정해야 한다.

## 10. Routing aliases

- `광학식 비접촉 측정`
- `광학 비접촉 센서`
- `광전식 센서`
- `photoelectric sensor`
- `laser noncontact measurement`
- `레이저 비접촉 측정`
- `optical time of flight`
- `optical ToF sensor`
- `laser ToF sensor`
- `Direct ToF`
- `Indirect ToF`
- `iToF distance measurement`
- `레이저 삼각측량`
- `laser triangulation sensor`
- `triangulation displacement sensor`
- `광학 거리 센서`
- `비접촉 거리 측정`
- `광센서 측정원리`

## 11. Routing field points

- 투과형·미러반사형·확산반사형 광전센서의 검출원리
- 광전 검출과 절대거리 측정 알고리즘의 경계
- 반사형 Direct ToF의 왕복 비행시간과 d=c·Δt/2
- Indirect ToF의 위상지연과 비모호 거리
- 레이저 삼각측량의 기준선·투사각·spot 위치
- PSD·CCD·CMOS 검출기 좌표와 거리·변위 변환
- 삼각측량 장치별 기하보정
- 대상 반사율·색상·재질·파장의 영향
- 거울면·투명체의 정반사·투과·다중반사
- 주변광 필터링·동기검파·시간게이팅
- laser speckle과 centroid 변동
- 정렬·시야각·occlusion·설치거리
- ToF timing resolution·jitter·pulse width
- 수광기 saturation·dynamic range·SNR
- multipath·mixed-pixel 거리 오차
- zero·scale·linearity·기하 calibration
- accuracy·resolution·repeatability 구분
- 범위·분해능·속도·표면·환경·안전·비용에 따른 방식 선정

## 12. Expected question patterns

1. 광학식 또는 레이저 비접촉 측정의 원리와 특징을 설명하시오.
   - intent: 광학 비접촉 측정의 전체 측정사슬과 주요 방식의 차이를 설명한다.
   - required anchors: optical_noncontact_measurement_chain, photoelectric_conversion_principle, optical_direct_tof_round_trip, laser_triangulation_principle, optical_method_selection_tradeoff
2. 광전식 센서의 투과형, 미러반사형, 확산반사형을 비교하시오.
   - intent: 세 광전 검출방식의 광로와 대상·배경 의존성을 비교한다.
   - required anchors: photoelectric_conversion_principle, photoelectric_through_beam_mode, photoelectric_retroreflective_mode, photoelectric_diffuse_reflective_mode, photoelectric_intensity_boundary
3. 레이저 ToF 거리측정 원리와 거리식을 설명하시오.
   - intent: Direct ToF의 왕복시간과 거리식을 설명한다.
   - required anchors: optical_direct_tof_round_trip, optical_direct_tof_distance_equation, tof_timing_jitter_resolution, detector_saturation_dynamic_range
4. Direct ToF와 Indirect ToF를 비교하고 iToF의 거리 모호성을 설명하시오.
   - intent: 펄스 시간계측과 위상기반 추정을 구분하고 위상래핑 한계를 설명한다.
   - required anchors: optical_direct_tof_round_trip, optical_direct_tof_distance_equation, optical_indirect_tof_phase_principle, optical_itof_phase_ambiguity
5. 레이저 삼각측량 센서의 측정원리와 보정방법을 설명하시오.
   - intent: 삼각측량 기하와 검출기 spot 위치, 장치 보정을 설명한다.
   - required anchors: laser_triangulation_principle, laser_triangulation_detector_coordinate, laser_triangulation_calibration, triangulation_range_resolution_tradeoff
6. 광학 비접촉 측정의 오차요인과 대책을 설명하시오.
   - intent: 표면·주변광·speckle·정렬·SNR·다중경로 오차와 대책을 연결한다.
   - required anchors: surface_reflectivity_color_effect, specular_transparent_surface_error, ambient_light_filtering, laser_speckle_effect, alignment_occlusion_geometry, detector_saturation_dynamic_range, multipath_mixed_pixel_error
7. 광학 ToF의 측정 정확도에 영향을 주는 요소를 설명하시오.
   - intent: timing, threshold, SNR, multipath와 calibration을 거리 불확도로 연결한다.
   - required anchors: tof_timing_jitter_resolution, detector_saturation_dynamic_range, multipath_mixed_pixel_error, calibration_reference_traceability, accuracy_resolution_repeatability_boundary
8. 투명체나 고광택 대상에서 레이저 측정 오류가 발생하는 원인과 대책을 설명하시오.
   - intent: 정반사·투과·다중반사·SNR과 설치 및 신호처리 대책을 설명한다.
   - required anchors: surface_reflectivity_color_effect, specular_transparent_surface_error, ambient_light_filtering, alignment_occlusion_geometry, detector_saturation_dynamic_range
9. 광학 비접촉 센서의 선정기준을 제시하시오.
   - intent: 측정목적, range, resolution, speed, target surface, ambient, safety, cost로 방식을 선정한다.
   - required anchors: photoelectric_intensity_boundary, triangulation_range_resolution_tradeoff, surface_reflectivity_color_effect, wavelength_material_selection, accuracy_resolution_repeatability_boundary, optical_method_selection_tradeoff
10. 비접촉 거리측정에서 초음파 방식과 달리 광학·레이저 방식에서 고려할 핵심 원리를 설명하시오.
   - intent: 광속 기반 ToF, 광학 반사특성, 삼각측량 기하와 광학 고유 오차를 설명한다.
   - required anchors: optical_direct_tof_distance_equation, laser_triangulation_principle, surface_reflectivity_color_effect, laser_speckle_effect, tof_timing_jitter_resolution

## 13. Semantic review requirements

- Photoelectric detection과 absolute distance algorithm을 구분한다.
- Direct ToF와 iToF를 구분한다.
- 반사형 Direct ToF에서 `d=c·Δt/2`를 유지한다.
- iToF phase ambiguity를 누락하지 않는다.
- Laser triangulation을 ToF로 설명하지 않는다.
- 삼각측량의 장치별 geometry calibration을 인정한다.
- surface/ambient/speckle/occlusion/SNR/multipath 오차를 원인과 대책으로 연결한다.
- Accuracy, resolution, repeatability를 구분한다.
- Historical frequency는 근거가 없어 사용하지 않는다.

## 14. Lane boundary

이 STEP 1에서는 다음 파일만 생성한다.

1. Topic Sheet
2. README.md
3. fact_anchor.json
4. logic_check.json
5. model_answer.json
6. topic_importance.json

다음은 수정하지 않는다.

- `rubrics/generated/**`
- 공용 classification/release 정책
- production Python
- 다른 Topic Pack
- docs/exam_scope 공용 문서
- focused regression test는 STEP 2에서 별도 작성한다.
