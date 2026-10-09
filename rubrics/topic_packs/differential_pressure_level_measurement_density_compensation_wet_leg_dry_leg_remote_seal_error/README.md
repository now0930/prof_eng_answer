# 차압식 레벨계의 원리, 밀도 보정, Dry/Wet Leg, Remote Seal 및 설치 오차

## Topic Pack

- Topic ID: `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Theory Depth: `FIELD_APPLICATION`
- Preparation Priority: `NORMAL`
- Runtime verdict authority: deterministic primary (legacy LLM profile retained as reference)
- Deterministic Checks: `disabled`

## Scope

1. 정수압과 `ΔP=ρgh`
2. Open/Closed Tank
3. Dry Leg와 Wet Leg
4. Zero Suppression과 Zero Elevation
5. 밀도 보정
6. Remote Diaphragm Seal
7. 모세관 수두·온도오차·응답시간
8. 계면 측정과 밀도차
9. 도압관·동결·설치높이 오차
10. LRV·URV·Span
11. 정압효과와 과압
12. Radar·GWR 선정 비교

## Contract summary

- Fact Anchors: 28
- Explicit Fatal Checks: 4
- Nonfatal Major Checks: 10
- Fatal direct-score layers: `B`, `C`
- D/E: direct score unchanged; related claim trust only
- External LLM validation: skipped by scripts

## Fact verification references

- Emerson DP level measurement guidance
- Yokogawa DP level application notes
- Endress+Hauser Deltabar guidance
- WIKA diaphragm-seal systems
- ISA hydrostatic-level practices

## Chapter 20 보강 (2026-09-30)

[Chapter 20](https://now0930.pe.kr/wordpress/chapter-20/)을 참조해 기존 정수압·Wet/Dry Leg·Remote Seal·계면 owner를 유지한다.

- Tank Expert System에서 하부와 중간 압력탭의 수직 간격 x>0이 고정되고 두 탭이 같은 균일 밀도 액체에 잠겨 있을 때 ρ=(P_bottom-P_middle)/(gx)이다. 설치수두는 보정하며 중간 탭 노출·층분리 시 이 밀도 계산을 그대로 적용하지 않는다.
- 밀도가 액주 전체에 대표성을 갖고 압력 기준과 설치수두를 보정하면 h=(P_bottom-P_top)/(ρg)로 하부 탭 기준 액면 높이를 계산한다. P_top은 기상부 압력이며 압력 하나만으로 미지의 밀도와 높이를 동시에 결정할 수 없다.
- 고정 간격 H의 하부·상부 탭 사이에 계면이 있고 하부는 중액, 상부는 경액에 잠기면 ΔP=C+g[ρ_L H+(ρ_H-ρ_L)h_i]이다. 상부 탭 위 경액 수두와 기상압은 공통항으로 상쇄된다. C는 충전액·설치수두 항이며 상부 탭 노출 또는 계면의 탭 범위 이탈 시 이 보상 조건은 깨진다.

계면 span의 수두 단위 예: Δh=36 in, SG_H=1.1, SG_L=0.78이면 36×(1.1−0.78)=11.52 inH₂O이다. SI 압력은 ΔP=g(ρ_H−ρ_L)Δh이며 수두·압력 단위를 섞지 않는다.

Sight Glass 연결은 `sight_glass_level_gauge_communicating_vessels_interface`, Float 위치 전달은 `float_level_measurement_buoyancy_guidance_tape_errors`, purge 배압과 유량 진단은 `bubbler_level_measurement_purge_backpressure_diagnostics`에 위임한다. 이들 상세 원리를 기존 레벨 질문의 필수 anchor로 추가하지 않는다.
