# 안전필수 소프트웨어의 정적·동적 분석, 구조적 커버리지 및 MC/DC 검증

## 1. Topic metadata

- Topic ID: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Authoring method: 공식 Topic Pack 생성 후 직접 검토·작성

## 2. 기술사 시험에서의 위치

MC/DC는 모든 산업용 소프트웨어에 일률 적용하는 일반 시험기법이 아니다.

기능안전이 요구되는 자체 개발 Safety Software, Firmware, Runtime 또는 복잡한 Safety Application Code에서 복합 Boolean Decision의 시험 충분성을 높이는 대표적 구조적 커버리지 기법이다.

적용 여부와 목표 수준은 산업별 표준, Systematic Capability, Functional Safety Plan, 사용언어, 인증범위와 자체 개발 Code의 범위로 결정한다.

## 3. MC/DC 정의

MC/DC는 Modified Condition/Decision Coverage이다.

복합 Decision을 구성하는 각 원자 조건이 다른 조건의 영향과 구분되어 Decision 결과를 독립적으로 바꾸는지를 Test Pair로 입증한다.

필요한 증거는 다음과 같다.

- 실행 가능한 진입점과 종료점
- 각 Decision 결과의 True와 False
- 각 조건 값의 True와 False
- 각 조건이 Decision 결과에 독립적으로 영향을 주는 Test Pair

## 4. 구조적 커버리지 비교

| 구분 | 확인 대상 | 주요 한계 |
|---|---|---|
| Statement | 각 실행 문장 또는 구문 | 분기와 조건 영향 미확인 |
| Decision/Branch | Decision의 True·False | 개별 조건의 영향 미확인 |
| Condition | 각 조건의 True·False | Decision 변화의 독립성 미확인 |
| MC/DC | 각 조건의 Decision 독립 영향 | 요구사항 완전성·Data·Timing 오류 미보장 |
| MCC | 가능한 조건조합 | 조합 수의 지수적 증가 |

Coverage 수준의 이름만으로 시험의 품질을 판단하지 않는다.

Test Case, Expected Result, Requirement Trace와 실행 증거를 함께 확인한다.

## 5. 독립 영향 Test Pair

조건 `C_i`의 독립 영향을 입증하는 두 Test Case는 다음을 만족해야 한다.

1. `C_i`의 값이 변한다.
2. Decision 결과가 변한다.
3. 나머지 조건은 고정되거나 그 Pair에서 Decision 결과에 영향을 줄 수 없도록 마스킹된다.

즉, 단순히 모든 조건이 True와 False를 한 번씩 가진다고 MC/DC가 되지 않는다.

## 6. Test Pair 예시

다음 Decision을 사용한다.

```text
D = A AND (B OR C)
```

| Test | A | B | C | D | 독립 영향 |
|---|---:|---:|---:|---:|---|
| T1 | 1 | 1 | 0 | 1 | 기준 |
| T2 | 0 | 1 | 0 | 0 | A: T1↔T2 |
| T3 | 1 | 0 | 0 | 0 | B: T1↔T3 |
| T4 | 1 | 0 | 1 | 1 | C: T3↔T4 |

세 조건의 단순식에서 네 개 Test Case로 MC/DC를 구성한 예이다.

그러나 모든 n조건 Decision이 항상 n+1개 시험으로 충분한 것은 아니다.

## 7. Unique-cause와 Masking MC/DC

### Unique-cause MC/DC

대상 조건만 변경하고 나머지 조건을 고정한다.

독립성 설명이 직접적이지만 동일 변수 반복이나 논리적 종속조건에서는 불가능할 수 있다.

### Masking MC/DC

다른 조건도 값이 바뀔 수 있다.

다만 Boolean 마스킹으로 그 조건들이 Decision 결과에 영향을 줄 수 없음을 보여야 한다.

적용 표준과 프로젝트 Coverage Plan에서 허용방법을 명확히 한다.

## 8. Short-circuit와 Coupled Condition

Short-circuit Evaluation에서는 앞 조건 결과에 따라 뒤 조건이 실행되지 않는다.

따라서 Truth Table에 값을 작성한 것과 실제 Code에서 해당 조건이 평가된 것은 다를 수 있다.

동일 변수나 논리적으로 결합된 조건은 독립적으로 변화시킬 수 없을 수 있다.

대응방법은 다음과 같다.

- Decision 식 재구성
- 조건의 의미 분리
- Masking MC/DC 근거 적용
- 불가능성 분석과 승인
- Compiler와 Instrumentation 실행결과 확인

## 9. 요구사항 기반 시험과 Coverage 분석

권장 순서는 다음과 같다.

```text
Safety Requirement
→ Design와 Boolean Decision
→ Requirements-based Test
→ Target 실행과 Coverage 수집
→ Coverage Gap 분석
→ 시험·요구·Code 보완
→ Regression과 승인
```

Code 구조만 보고 Test를 만드는 방식은 누락된 요구사항을 발견하지 못할 수 있다.

MC/DC는 요구사항 기반 시험을 대체하지 않는다.

## 10. Coverage Gap 종결

미실행 Code가 발견되면 원인을 분류한다.

- 누락된 Test Case
- 누락 또는 불명확한 Requirement
- 잘못된 구현
- Dead Code
- Deactivated Code
- Defensive Code
- Compiler 또는 Instrumentation 차이
- Target 환경에서 재현되지 않은 경로

처분은 시험 추가, Requirement 보완, Code 제거, 구성별 시험 또는 승인된 정당화 중 하나로 명확히 종결한다.

## 11. Dead·Deactivated·Defensive Code

### Dead Code

허용 입력과 정상 구성에서 실행되지 않고 요구 기능도 수행하지 않는 Code이다.

원칙적으로 제거하고 영향분석과 회귀시험을 수행한다.

### Deactivated Code

특정 구성이나 모드에서 의도적으로 실행되지 않지만 다른 승인 구성에서는 실행될 수 있다.

활성조건, Requirement, 구성식별과 시험근거가 필요하다.

### Defensive Code

비정상 입력이나 내부 오류를 처리한다.

Derived Requirement, Safe State, Exception 처리와 오류경로 시험으로 추적한다.

## 12. Source와 Object Code

Source 수준의 Boolean 구조가 Compiler 최적화 후 Object Code에서 동일하게 유지된다고 단정할 수 없다.

다음을 통제한다.

- Compiler와 Version
- Optimization Option
- 자동 Code Generator
- Source–Object Trace
- 추가되거나 제거된 Branch
- Object Code Coverage 필요성

Object Code Coverage 적용여부는 표준과 Software Verification Plan으로 결정한다.

## 13. Instrumentation과 Tool Qualification

Coverage Instrumentation은 실행흐름을 기록하기 위해 Probe를 삽입한다.

이 Probe는 다음에 영향을 줄 수 있다.

- Scan 또는 Task 실행시간
- Memory 사용량
- Scheduling
- Compiler 최적화
- Race와 Timing 재현성

Coverage Tool이 미실행 Code를 실행된 것으로 잘못 보고하고 이를 후속 단계에서 독립 검출하지 못하면 Qualification, Tool Validation 또는 독립확인 근거가 필요하다.

## 14. 정적·동적 분석의 관계

정적분석은 Code를 실행하지 않고 다음을 분석한다.

- Control Flow와 Data Flow
- 복잡도
- Coding Rule
- 초기화와 자료형
- 도달불가 Code
- 잠재 Overflow와 Interface 오류

동적분석은 실행 중 다음을 확인한다.

- Path와 Boolean 결과
- Timing과 Resource
- Exception과 오류반응
- Target Interface
- Coverage와 Test Result

MC/DC는 Boolean Decision에 집중하므로 Data Coupling, Timing, Race, Boundary와 Resource 오류는 별도 분석으로 보완한다.

## 15. 산업용 Safety PLC 적용경계

인증된 Safety PLC와 검증된 Function Block을 사용하는 경우 Vendor 내부 Firmware의 MC/DC를 사용자가 다시 수행하는 것이 항상 정답은 아니다.

사용자는 다음을 확인한다.

- 인증범위와 Safety Manual
- 승인된 Function Block과 Parameter
- SRS–Application Logic–Test Trace
- 입력조합, Boundary, Bypass와 Reset
- Generated Code 또는 Custom Block 범위
- 변경 시 Regression과 Revalidation

자체 개발 Firmware, Runtime, Compiler 생성 Code와 Safety Library의 범위가 커질수록 구조적 커버리지 증거의 중요도가 증가한다.

## 16. 100% MC/DC의 한계

100% MC/DC는 다음을 단독으로 보장하지 않는다.

- Requirement의 정확성과 완전성
- 누락된 Hazard와 Safety Function
- 알고리즘의 공정 적합성
- Data Flow와 Interface 오류
- Timing, Race와 Resource Exhaustion
- Hardware Random Failure
- Sensor·Final Element 성능
- 전체 SIF의 SIL 달성

따라서 MC/DC는 Safety Lifecycle의 한 증거로 사용한다.

## 17. 인접 Topic ownership

- 일반 Software Lifecycle, V-Model, 일반 Static·Dynamic Analysis: `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`
- SIL, Systematic Failure, Independence, Safety V&V: `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- Voting, Trip, Fail-safe 실행논리: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
- 본 Topic은 MC/DC Test Pair, Coverage Gap, Code 분류, Compiler·Tool 증거의 상세를 소유한다.

## 18. 기술사 답안 권장 흐름

1. MC/DC를 독립 영향 구조적 커버리지로 정의한다.
2. Statement·Decision·Condition·MC/DC·MCC를 비교한다.
3. Unique-cause와 Masking Test Pair를 도식화한다.
4. Short-circuit와 Coupled Condition을 설명한다.
5. 요구사항 기반 시험에서 Coverage Gap 종결까지의 절차를 제시한다.
6. Dead·Deactivated·Defensive Code를 구분한다.
7. Object Code, Instrumentation과 Tool Qualification을 설명한다.
8. 산업용 Safety PLC 적용경계와 100% Coverage의 한계로 결론낸다.
