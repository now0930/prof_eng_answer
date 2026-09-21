# 광섬유 링크 모드·분산·손실·OTDR 진단

- Topic ID: `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics`
- Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`

## Scope

산업 계측 광섬유 링크의 전반사, single/multimode와 step/graded-index, 분산,
insertion-loss 시험과 OTDR의 역할·한계를 소유한다.

## Boundary

- 레이저 ToF·삼각측량은 `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`
- 상위 protocol은 `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- tray·conduit 시공은 `instrumentation_installation_wiring_impulse_tubing_inspection_codes`

## Correctness boundary

Single-mode에서도 chromatic·polarization-mode dispersion은 남을 수 있다. 광원과 power
meter는 전체 삽입손실을, OTDR은 event 위치를 평가하며 어느 한 시험이 다른 시험을
완전히 대체하지 않는다.

## Source

- [Lessons In Industrial Instrumentation, Chapter 8](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-8/)
