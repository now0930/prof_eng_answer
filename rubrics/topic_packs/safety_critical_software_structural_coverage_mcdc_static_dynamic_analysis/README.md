# 안전필수 소프트웨어의 정적·동적 분석, 구조적 커버리지 및 MC/DC 검증

## Topic ID

`safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`

## 목적

안전필수 소프트웨어의 복합 Boolean Decision에서 각 조건의 독립 영향을 입증하는 MC/DC와 구조적 커버리지 분석, 미실행 코드 처분 및 Tool 증거를 평가한다.

## 대표 문제

1. MC/DC의 개념, 목적과 충족조건을 설명하시오.
2. Statement, Decision, Condition 및 MC/DC Coverage를 비교하시오.
3. Unique-cause와 Masking MC/DC의 차이를 설명하시오.
4. Coverage Gap과 Dead·Deactivated Code 처리방법을 설명하시오.
5. 산업용 안전필수 소프트웨어에 MC/DC를 적용할 때 고려사항을 설명하시오.

## Topic boundary

이 Topic이 소유하는 범위:

- Statement·Decision·Condition·MC/DC·MCC 비교
- 각 원자 조건의 독립 영향 Test Pair
- Unique-cause와 Masking MC/DC
- Short-circuit, Coupled Condition과 Boolean masking
- Requirements Coverage와 Structural Coverage의 폐루프
- Coverage Gap, Dead·Deactivated·Defensive Code 처분
- Source·Object Code, Compiler와 Instrumentation 영향
- Coverage Tool Qualification과 Target 환경 증거
- 100% MC/DC의 한계 및 산업별 적용경계

인접 Topic으로 넘기는 범위:

- 일반 SW Lifecycle, V-Model, 일반 정적·동적 분석: `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`
- SIL, Systematic Failure, 독립성 및 Safety V&V: `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- Voting, Trip, Fail-safe 실행논리: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`

## 핵심 정답

- MC/DC는 각 조건이 Decision 결과에 독립적으로 영향을 미치는지 입증한다.
- Condition Coverage나 Decision Coverage만으로 MC/DC가 되지 않는다.
- 요구사항 기반 시험 후 구조적 커버리지 분석으로 미실행 구조를 찾는다.
- Coverage Gap은 시험 추가, 요구 보완, 코드 제거 또는 정당화로 종결한다.
- 100% MC/DC는 전체 SIL 달성의 단독 증거가 아니다.

## Fatal 오류

- Decision Coverage와 MC/DC를 동일시함
- 여러 비마스킹 조건을 함께 바꾼 Pair를 독립 영향으로 인정함
- 모든 n조건 Decision은 항상 n+1 시험이면 충분하다고 단정함
- Dead Code를 근거 없이 유지함
- Source Coverage가 Object Coverage와 항상 동일하다고 단정함
- MC/DC 100%로 요구사항 정확성과 전체 SIL을 선언함

## 관리 원칙

Coverage 결과는 대상 Source·Object, Compiler·Option, Tool Version, Target 환경, Test Case와 Requirement Traceability를 함께 식별하여 형상관리한다.

<!-- guard:M1_100_PERCENT_MCDC_DOES_NOT_GUARANTEE_SIL -->
## MC/DC·SIL·수명주기 경계

- 100% MC/DC는 구조적 커버리지 목표 달성의 증거이다.
- 100% MC/DC만으로 SIL 달성을 보장하지 않는다.
- MC/DC는 요구사항 추적성, 독립성, 검증·확인 등 소프트웨어 수명주기 활동을 대체하지 않는다.
