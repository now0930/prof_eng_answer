# Guided Wave Radar (GWR) 레벨 측정원리와 적용

## Topic metadata

- topic_id: `guided_wave_radar_level_measurement_tdr_interface_application`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL` (편집상 중요도; 기출빈도 근거 아님)
- status: managed draft / human review required

## 대표 예상 문제

> **Guided Wave Radar (GWR) 레벨계의 TDR 측정원리와 프로브 구조에 따른 전파경로를
> 설명하고, 상부 액면 및 계면 측정 시 유전율·공정조건이 미치는 영향과 적용상 한계를
> 설명하시오.**

기출 확인을 하지 않은 지식 기반 예상문제다. 공통 레이더 계측·설치 및 상세 제조사 선정은
기존 free-space Radar/계측 설치 Pack과 경계를 둔다.

## Problem unit and knowledge flow

이 문제의 응집축은 free-space pulse/FMCW 거리계산이 아니라 **프로브를 따라 전파되는
GWR 펄스의 TDR·반사·전파매질 구간**이다.

1. 송신기에서 rod/cable/coaxial probe로 저전력 pulse를 보낸다.
2. probe를 따른 전파 중 임피던스가 바뀌는 제품 경계면에서 반사된다.
3. 왕복시간으로 표면/계면 위치를 추정한다.
4. 상부 기체공간의 액면거리와 상부 액체층을 통과하는 계면 측정의 전파속도 경로를 구분한다.
5. probe 형태·탱크 return path·부착물·유전율·공정조건과 기계 부하에 따른 적용 한계를 검토한다.

## Candidate Fact Anchor IDs

| 요구 | 신규 고유 ID | 기존 source 근거 후보 |
|---|---|---|
| GWR TDR·probe 경로 | `gwr_tdr_probe_guided_reflection` | `gwr_tdr_guided_wave_principle` |
| 액면/계면 전파경로 | `gwr_surface_interface_permittivity_path` | `gwr_effective_permittivity_propagation_path` |
| probe·return-path 경계 | `gwr_probe_return_path_quasi_tem_boundary` | `gwr_quasi_tem_return_path` |
| 공정·기계 적용 한계 | `gwr_process_probe_application_limits` | `gwr_interface_and_process_limitations` |

기존 Radar source Anchor는 삭제하거나 소유권 이전하지 않는다. 새 ID는 중복방지용 draft
copy이며, 출처 책자 section/page·제조사 문서는 아직 원문 대조되지 않았다.

## Ownership boundary

- Free-space pulse/FMCW 거리·처프·비트주파수·안테나 beam·false echo는
  `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
  소유 후보로 유지한다.
- 일반 설치규정, 교정, 시운전·기기별 선정 상세는 기존 Radar/계측 설치 Pack에 handoff한다.
- GWR의 interface layer별 전파경로, probe propagation/return-path 및 probe-specific process
  limitation은 이 draft 범위 후보이다.
- 예상문제 내 free-space Radar와의 비교가 필요하면 기존 Radar Pack을 교차참조하되, 그
  이유만으로 두 원리를 하나의 필수 answer unit으로 합치지 않는다.

## Non-claims / review questions

- 모든 single-rod/cable probe를 완전한 TEM 또는 무분산 구조라고 단정하지 않는다.
- 상부 액면거리 전체에 제품 액체의 상대유전율을 일률 적용하지 않는다.
- 모든 GWR이 자유공간 레이더의 문제를 제거한다고 하지 않는다.
- Probe material, pressure/temperature rating, tensile load, product compatibility 등은
  제품별 자료를 확인하기 전까지 일반화하지 않는다.
- Reviewer should check whether the interface/permittivity wording and probe ownership match
  the primary manufacturer sources and the user's intended Topic boundary.
