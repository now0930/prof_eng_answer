# 광섬유 링크 모드·분산·손실·OTDR 진단

## 0. Topic metadata

- Topic ID: `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics`
- Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Source: Lessons In Industrial Instrumentation, Chapter 8

## 1. Scope and ownership

산업 계측 광섬유 링크의 전반사 전파, single/multimode와 step/graded-index,
modal·chromatic·polarization-mode dispersion, insertion-loss 시험과 OTDR의 역할·한계를
소유한다.

- 레이저 ToF·삼각측량: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`
- Fieldbus/Ethernet 상위 프로토콜: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- 일반 cable tray·conduit 시공: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`

## 2. Core correct facts

1. core/cladding 굴절률 조건과 임계각에 의해 전반사 경로가 형성된다.
2. multimode modal dispersion은 모드별 경로·도착시간 차이이며 graded-index가 이를 줄인다.
3. single-mode는 modal dispersion을 크게 줄이지만 chromatic·polarization-mode dispersion까지 0으로 만들지는 않는다.
4. 광원+power meter는 링크 전체 삽입손실을 측정하고 OTDR은 반사·후방산란과 왕복시간으로 event 위치를 추정한다.
5. OTDR 거리 해석은 `d=vgΔt/2=cΔt/(2ng)`이며 dead zone과 분해능 한계를 고려한다.

## 3. Fatal wrong claims

- OTDR은 입출력 전력만 비교하므로 결함 위치를 찾을 수 없다.
- 광원과 power meter만으로 손실의 정확한 위치를 항상 알 수 있다.
- single-mode 광섬유에는 어떤 종류의 분산도 존재하지 않는다.

## 4. False-positive cautions

- OTDR event만으로 접속 불량의 물리적 원인을 단정하지 않는다.
- 위상굴절률 대신 거리 계산에는 군속도·군굴절률을 사용한다.

## 5. Expected question patterns

- 광섬유의 single/multimode와 분산을 비교하고 계장 링크 선정기준을 설명하시오.
- 광원·power meter와 OTDR 시험의 목적, 원리와 한계를 비교하시오.

## 6. Human review checklist

- [x] 링크 시험과 광학 측정센서의 ownership을 분리했다.
- [x] 왕복시간의 1/2 계수를 확인했다.
- [x] single-mode의 잔여 분산을 명시했다.

## 7. Source

- https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-8/
