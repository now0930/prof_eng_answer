# SIS·SIL 안전 소프트웨어, 독립성, 체계적 고장 및 검증·확인

## Topic ID

`sis_sil_safety_software_independence_systematic_failure_verification_validation`

## Lane

`SOFTWARE_LLM_LANE_C`

## Question type

`PRINCIPLE_INTERPRETATION`

## Scope

- SIS, SIF, SIL 관계
- Safety Requirement Specification
- Safety Application Program과 Software Safety Lifecycle
- Random Hardware Failure와 Systematic Failure
- Independence, Separation, Common Cause, Diversity
- Safety Manual, Certified Product, Proven in Use
- Tool Qualification과 Library Validation
- Verification, Validation, Functional Test, Proof Test 관계
- Modification, Bypass, Override, Audit, Competence

## Ownership Boundary

- SW-02: 일반 Sequence, Interlock, Trip, First-out, Fail-safe 동작
- SW-04: 일반 제어 Software SDLC와 일반 V&V
- SW-05: 기능안전 요구가 추가된 Safety Software Lifecycle, SIL, SRS, 독립성, 체계적 고장과 Safety V&V
- Final Element/PST Topic: Valve와 Final Element의 PFD/PST/Proof Test 상세

## Authoring Contract

- Source schema: modern Topic Pack schema with Anchor references

- Fact Anchor: 31
- Fatal misconception: 16
- Major/Warn condition: 12
- Routing alias: 14
- Positive question: 10
- Negative boundary question: 8
- Deterministic checks: disabled
- Generated Bank promotion: excluded
- Production Python/Common Router modification: excluded

## Representative Question

SIS·SIL 안전 소프트웨어에서 Safety Lifecycle, 체계적 고장, 독립성 및 Verification·Validation 방안을 설명하시오.

## Fatal Guard

- 인증 제품은 전체 SIF의 SIL 달성을 자동 보장하지 않는다.
- Proof Test는 Safety Software Validation을 대체하지 않는다.
- 다른 CPU 또는 Diversity는 독립성이나 Common Cause 제거를 자동 보장하지 않는다.
- Software 고장을 Random Hardware Failure와 동일한 일정 고장률로 단순화하지 않는다.
- Bypass, Override와 Modification은 기능안전 관리대상이다.

## Verify-first

표준 Clause 번호, 독립성 수준, Tool Qualification, Proven in Use 최소 증거, Certificate Scope 및 정량 가정은 적용 Edition과 프로젝트 Functional Safety Plan으로 확인한다.

## MC/DC 상세 Topic 경계

SW-05는 SIL, Systematic Failure, Independence, Tool Qualification 원칙과 Safety V&V의 적용근거를 계속 소유한다.

다음 상세영역은 `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`로 이관한다.

- MC/DC 독립 영향과 Test Pair 설계
- Unique-cause·Masking MC/DC
- Coverage Gap과 Dead·Deactivated·Defensive Code
- Source·Object Code, Compiler·Instrumentation
- Coverage Tool 증거와 100% Coverage의 한계

SIL 숫자만으로 MC/DC 100%를 보편 의무로 단정하지 않는다.
