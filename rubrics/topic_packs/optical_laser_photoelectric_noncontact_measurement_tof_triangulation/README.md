# 광전·레이저 비접촉 측정의 검출원리, ToF·삼각측량 알고리즘 및 오차·선정

- Topic ID: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`
- Official criterion: `IC-2027-W-2-2`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency used: `false`

## Scope

이 Topic은 광학·광전·레이저 기반 비접촉 측정의 원리와 알고리즘을 다룬다.

핵심 범위는 다음과 같다.

1. 광전식 센서의 광전변환과 투과형·미러반사형·확산반사형
2. Optical Direct ToF의 왕복시간과 `d=c·Δt/2`
3. Indirect ToF의 위상지연과 phase ambiguity
4. Laser triangulation의 baseline·spot 위치·검출기 좌표·기하보정
5. 반사율·색상·투명체·고광택·주변광·speckle·occlusion·multipath 오차
6. Calibration 및 accuracy·resolution·repeatability
7. 측정범위·분해능·응답속도·대상·환경·안전·비용 기반 선정

## Boundary

- 초음파 ToF의 음속·온도보상은 기존 ultrasonic Topic의 소유 범위다.
- Radar FMCW/Pulse와 유전율·허위에코는 기존 radar Topic의 소유 범위다.
- 이 Topic은 **광학·광전·laser ToF·triangulation**에 집중한다.
- 광전식 존재검출을 자동으로 절대거리 측정으로 간주하지 않는다.
- Laser triangulation을 ToF로 간주하지 않는다.

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank와 공용 release/classification 정책은 이 lane에서 수정하지 않는다.
