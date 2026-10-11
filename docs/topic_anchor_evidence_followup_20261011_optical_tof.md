# Topic Anchor evidence follow-up — optical direct ToF

Date: 2026-10-11

## Verified

`optical_laser_photoelectric_noncontact_measurement_tof_triangulation`의 `optical_direct_tof_distance_equation`을 검증 등록했다. 같은 센서 위치에서 빛을 송신하고 반사되어 돌아온 수신시각까지의 `Δt`는 왕복시간이다. 이상적인 전파 모델에서 거리는 `d = c·Δt/2`이며, 2로 나누는 것은 왕복경로를 한 방향 거리로 환산하기 때문이다. 여기서 `c`는 해당 측정 매질에서의 빛 전파속도다. 이 식은 이상적 거리 관계이며 실제 장치의 편향·지터·표적 반사 특성까지 포함하는 오차모델은 아니다.

근거는 제조사 기술 자료 두 건이다.

- [OMRON TECHNICS, Development of a TOF Sensor for Long-Range and Stable Wide-Angle Detection](https://www.omron.com/global/en/technology/omrontechnics/vol58/005.html), §2.1, Direct ToF Eq. (2): 펄스 투사부터 반환까지의 왕복 지연과 `d=c·Δt/2`를 명시한다.
- [Analog Devices, Time of Flight System for Distance Measurement and Object Detection](https://www.analog.com/en/resources/technical-articles/tof-system-for-distance-measurement-and-object-detection.html), “Time of flight” 설명: 방사광과 반사광 수신 간 지연, 왕복거리, `d=(c×Δt)/2` 관계를 명시한다.

`score_effect=none`이다. 검증은 이 anchor만 대상으로 하며, optical ToF의 오차, iToF, 삼각측량, 표적 반사율 또는 현장 교정 주장으로 확장하지 않았다.

## 보류

같은 Pack의 나머지 optical anchor는 이번 근거 검토로 검증 처리하지 않았다. 특히 복합적인 설치·재질·오차·성능 trade-off 주장은 각각의 전체 문구를 지지하는 자료를 확인한 뒤 별도로 승격해야 한다.

## 추가 확인 (2026-10-11)

`photoelectric_intensity_boundary`는 기존의 광원·광학계·입사각·오염·배경 전체 인과를 포괄적으로 단정하던 표현을 좁혔다. OMRON은 diffuse-reflective 방식에서 대상 표면의 색과 매끄러움이 반사광량·동작 안정성·검출거리에 영향을 줄 수 있다고 명시하고, 별도 distance-setting 방식은 PSD의 반사 spot 위치 또는 dual-photodiode의 수광량 차를 이용한다고 설명한다. 따라서 수광량 기반 확산반사 검출과 위치 기반 거리설정 방식의 경계만 verified 등록했으며 절대거리 환산식이나 모든 센서의 공통 특성을 주장하지 않는다. `score_effect=none`이다. 근거: [OMRON Photoelectric Sensors overview](https://www.ia.omron.com/support/guide/43/introduction.html), [OMRON FAQ00320](https://www.ia.omron.com/support/faq/answer/43/faq00320/).

`laser_triangulation_calibration`은 거리변환이 모든 센서에 공통인 단일 식으로 대체될 수 없다는 표현에서, 장치별 광학기하와 실제 보정 mapping에 종속된다는 범위로 좁혔다. NIST의 active triangulation 식은 기준선·초점거리·검출기 좌표·각도를 연결하고, Kienle et al.은 기준선·렌즈 초점거리·검출기 위치·삼각측량각 및 생산 공차·광학수차 때문에 알려진 parameter 계산 또는 기준거리 data 기반 calibration이 사용될 수 있음을 설명한다. 이를 고정된 universal parameter나 모든 장치의 의무 보정 절차로 일반화하지 않는다. `score_effect=none`이다. 근거: [NIST TN 1682](https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote1682.pdf), [Kienle et al., Sensors 2020](https://www.mdpi.com/1424-8220/20/17/4949).

아래 9개 추가 Anchor를 제조사 기술자료와 NIST 연구자료로 대조해 등록했다. 이 검토는 제품별 사거리, 현장 교정요건, 보편적인 오차·정확도 보증으로 확대하지 않는다.

| Anchor | 확인 범위 | 근거 |
|---|---|---|
| `optical_noncontact_measurement_chain` | 능동 광학 측정의 방사-대상 상호작용-수광-전기신호/신호처리 측정사슬 | [OMRON photoelectric overview](https://www.ia.omron.com/support/guide/43/overview.html), “What Are Photoelectric Sensors?”; [NIST laser triangulation](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920007), §1, p. 3 |
| `photoelectric_conversion_principle` | 수광부가 광량 변화를 검출해 전기 출력으로 변환 | [OMRON photoelectric overview](https://www.ia.omron.com/support/guide/43/overview.html), “What Are Photoelectric Sensors?” |
| `photoelectric_through_beam_mode` | 대향 발광기·수광기와 대상의 빔 차단; 거리/operating margin 비교는 제품·조건 종속 | [Rockwell Sensor Technology and Application Basics](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/c117-rm001_-en-p.pdf), “Transmitted beam sensing,” pp. 11–14; [OMRON overview](https://www.ia.omron.com/support/guide/43/overview.html) |
| `photoelectric_retroreflective_mode` | 한 하우징의 송수광부, 반사판 왕복광, 대상에 의한 차단; 편광형은 depolarizing reflector를 통해 많은 specular reflection을 거부 | [Rockwell manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/c117-rm001_-en-p.pdf), “Retroreflective and Polarized Retroreflective,” pp. 15–19 |
| `photoelectric_diffuse_reflective_mode` | 대상 산란광을 같은 쪽 수광부가 검출; 객체·배경 반사율과 표면 배치가 sensing margin에 영향 | [Rockwell manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/c117-rm001_-en-p.pdf), “Diffuse,” pp. 20–22; [OMRON overview](https://www.ia.omron.com/support/guide/43/overview.html) |
| `optical_direct_tof_round_trip` | 펄스 송신에서 반사광 반환까지의 왕복시간 측정 | [OMRON TECHNICS](https://www.omron.com/global/en/technology/omrontechnics/vol58/005.html), §2.1, dToF Eq. (2) |
| `optical_indirect_tof_phase_principle` | 변조광 송수신 위상차로 지연을 추정; 단일 주파수 식은 위상 범위·왕복 모델에 한정 | [OMRON TECHNICS](https://www.omron.com/global/en/technology/omrontechnics/vol58/005.html), §2.1, iToF Eq. (1) |
| `laser_triangulation_principle` | 대상에 투사된 반사 spot을 렌즈·위치검출기로 받아 센서 기하로 거리 산정; standoff/range는 geometry 종속 | [NIST laser triangulation](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920007), §1 and Fig. 1, p. 3 |
| `laser_triangulation_detector_coordinate` | target depth에 따른 detector spot 위치 및 geometry-based distance mapping | [NIST laser triangulation](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920007), §1 and Fig. 1, p. 3 |
| `laser_speckle_effect` | 거친 표면에 coherent laser를 조사할 때의 speckle가 밝기 분포와 CCD spot centroid의 확정성을 흔들어 triangulation의 random error/measurement uncertainty에 기여. 정량 오차는 장치·표면 조건 종속 | [Springer, Laser line triangulation for fast 3D measurements on large gears](https://link.springer.com/article/10.1007/s00170-018-2636-z), §4.3; [Optica, Laser triangulation: Fundamental uncertainty in distance measurement](https://opg.optica.org/ao/abstract.cfm?uri=ao-33-7-1306) |
| `optical_itof_phase_ambiguity` | 단일 변조주파수 iToF 위상의 주기성은 유한한 비모호 거리범위를 만들며, 다중주파수 phase-unwrapping은 구현 조건하에 그 범위를 확장할 수 있음. 코딩·특정 알고리즘의 효과는 주장하지 않음 | [OMRON TECHNICS](https://www.omron.com/global/en/technology/omrontechnics/vol58/005.html), §2.1 Eq. (1); [Droeschel et al., IEEE IROS 2010](https://doi.org/10.1109/IROS.2010.5649488), Abstract and §II |

모두 `score_effect=none`이다. 아직 등록하지 않은 optical Anchor는 이 결과로 자동 승격하지 않는다.

## 추가 확인: multipath depth distortion

`multipath_mixed_pixel_error`를 AMCW ToF range camera로 범위를 좁혀 verified 등록했다. Whyte et al.은 direct shortest-path return과 다른 global returns가 수신 pixel에 기여하고 다중 전파경로가 측정오차를 일으킨다고 설명한다. Bhandari et al.은 넓은 조명 아래 투명체의 여러 장면점에서 온 반사가 하나의 pixel을 비춰 잘못된 depth map을 만들 수 있다고 보고한다. 이 근거는 모든 광학 ToF 센서의 공통 오차 크기·방향을 뜻하지 않는다. `score_effect=none`이다. 근거: [Whyte et al., Optical Engineering 54(11), 113109 (2015)](https://researchcommons.waikato.ac.nz/entities/publication/5ac6413e-72b7-404e-bba3-2931bc9ea350), [Bhandari et al., Optics Letters 39(6), 1705–1708 (2014)](https://opg.optica.org/OL/abstract.cfm?uri=ol-39-6-1705).

`specular_transparent_surface_error`는 Mitsubishi MH11의 specular/diffuse mounting 및 transparent-object surface selection 동작과 ToF camera의 투명체 굴절 왜곡으로 좁혀 verified 등록했다. Mitsubishi manual §1.6은 두 반사 모드의 기하 차이와 specular 대칭 설치를, §4.3은 front/rear 등 여러 표면 및 잘못된 reference 선택의 측정 결과를 설명한다. CVPR 2016 연구는 transparent-object refractive index에 따른 ToF depth distortion을 다룬다. 이는 모델·모달리티별 설명이며 모든 광학센서에 공통인 오류방향이나 표면 응답을 주장하지 않는다. `score_effect=none`이다. 근거: [Mitsubishi Electric MH11 User’s Manual SH-081705ENG-C](https://dl.mitsubishielectric.com/dl/fa/document/manual/sensor/sh081705eng/sh081705engc.pdf), [Tanaka et al., CVPR 2016](https://openaccess.thecvf.com/content_cvpr_2016/html/Tanaka_Recovering_Transparent_Shape_CVPR_2016_paper.html).
