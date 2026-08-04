# 제어밸브의 Cv·Kv, 액체 사이징, Reynolds 보정 및 선정

## Topic ID

`control_valve_sizing_cv_kv_reynolds_liquid_selection`

## Question type

Primary: `CALC_DESIGN`

Supported secondary: `COMPARE_SELECTION`

Supported tertiary: `PRINCIPLE_INTERPRETATION`

## 핵심 범위

- Cv·Kv 정의와 기준 단위
- Cv↔Kv conversion
- 비초크 난류 액체 기본식
- Required와 rated coefficient
- Body size와 trim capacity
- Minimum·normal·maximum sizing
- Operating travel mapping
- Piping geometry factor `Fp`
- Valve Reynolds number와 `FR`
- Iterative viscosity correction
- Small-flow trim
- Over·under sizing
- Cavitation·flashing·choked screening
- Vendor sizing crosscheck

## Formula 경계

- `Q = Cv × sqrt(ΔP/SG)`
- `Cv_required = Q × sqrt(SG/ΔP)`
- `Q = Kv × sqrt(ΔP/SG)`
- `Kv_required = Q × sqrt(SG/ΔP)`
- `Kv ≈ 0.865 Cv`
- `Cv ≈ 1.156 Kv`
- `C_corrected = C_basic / (Fp × FR)`

Basic relation은 single-phase, non-choked, turbulent liquid에 한정한다.

Exact `N1`, `Fp`, valve Reynolds와 `FR` correlation은 적용 standard,
unit system, valve style과 geometry를 명시한다.

## 인접 Topic 경계

- Characteristic 형상은 Topic 2이다.
- Authority·rangeability·installed gain은 Topic 5이다.
- Gas sizing은 Topic 7이다.
- Cavitation·flashing·liquid choked 상세는 Topic 8이다.
- 전체 valve package workflow는 Topic 16이다.

## Logic Check 정책

- Fact Anchor: 32개
- Fatal misconception: 18개
- Major conditional claim: 7개
- Deterministic verdict: disabled
- LLM semantic profile: enabled
- Formula regression: focused tests
- Direct score application: disabled
- Direct D/E effect: none

## Source

- `gemini_script/20260803_topic06_cv_kv_liquid_sizing_requirements.md`
- `docs/topic_sheets/control_valve_sizing_cv_kv_reynolds_liquid_selection.md`
- Control Valve Handbook Chapter 5
- Control Valve Primer Chapter 5

## 작성 상태

Source JSON authored and source-level validation pending generated-bank build.
