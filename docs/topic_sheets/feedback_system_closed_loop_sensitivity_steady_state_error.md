# Feedback System의 폐루프 구조·민감도·정상상태 오차 Topic Sheet

## 1. Topic metadata

- topic_id: `feedback_system_closed_loop_sensitivity_steady_state_error`
- title: `피드백 시스템의 폐루프 구조·민감도·정상상태 오차`
- question_type: `PRINCIPLE_INTERPRETATION`
- difficulty: `THEORY_CORE`
- selection_importance: `CORE_MUST_PREPARE`
- authoring_policy: 이 문서를 사람이 먼저 검토한 요구사항 원본으로 사용하고, JSON source는 기존 MD→LLM authoring workflow로 생성한다.

## 2. 대표 문제

1. 피드백 시스템의 폐루프 전달함수와 민감도 함수를 설명하시오.
2. 음의 피드백 시스템의 민감도 함수 S와 상보 민감도 함수 T의 의미를 설명하시오.
3. 피드백 시스템의 시스템 형과 정상상태 오차의 관계를 설명하시오.
4. 폐루프 제어계에서 외란 억제, 측정 잡음 및 안정성의 상충관계를 설명하시오.

## 3. 출제 의도

피드백 제어의 기본 신호 관계에서 출발하여 폐루프 전달함수, 안정성, 민감도, 외란 억제, 측정 잡음, 정상상태 오차를 하나의 논리로 연결하는지를 평가한다.

## 4. 문제 범위와 제외 범위

### 포함 범위

- E(s)=R(s)-H(s)Y(s)
- L(s)=G(s)H(s)
- Y/R=G/(1+GH)
- 1+L=0
- S=1/(1+L)
- T=L/(1+L)
- S+T=1
- 출력단 외란과 측정 잡음 전달경로
- 최종값 정리와 정상상태 오차
- 시스템 형과 원점 극
- Kp_e, Kv, Ka
- Type 0, 1, 2의 입력별 정상상태 오차
- 적분 동작과 anti-windup
- 루프 이득, 대역폭, 위상여유, 시간지연, 잡음 및 포화의 trade-off
- prefilter와 feedforward
- Bode, Nyquist, 시간응답, 외란응답 및 포화시험

### 제외 또는 분리 범위

- 상태공간 모델 자체의 상세 유도
- PID 일반 튜닝 순서
- 감쇠비 분류 자체
- 공진주파수 공식 자체
- 단순 누락을 핵심 오개념의 직접 주장과 동일하게 처리하는 것

## 5. Core correct facts

### 5.1 표준 음의 피드백

- E(s)=R(s)-H(s)Y(s)
- Y(s)=G(s)E(s)
- L(s)=G(s)H(s)
- Y(s)/R(s)=G(s)/[1+G(s)H(s)]
- 특성방정식: 1+L(s)=0

### 5.2 일반 피드백과 단위 피드백

- 일반 피드백: Y/R=G/(1+GH)
- 단위 피드백: H=1, L=G이므로 Y/R=L/(1+L)=T

### 5.3 민감도와 상보 민감도

- S(s)=1/[1+L(s)]
- T(s)=L(s)/[1+L(s)]
- S(s)+T(s)=1

S와 T는 같은 함수가 아니다.

### 5.4 외란과 측정 잡음

단위 피드백에서 출력단 외란 Do가 출력에 가산되면 Y=TR+SDo로 해석할 수 있다.

측정 경로 잡음 N은 표준 구조에서 Yn=-TN으로 나타난다.

외란과 잡음 전달은 주입 위치에 따라 달라지므로 신호 위치를 먼저 정의해야 한다.

### 5.5 정상상태 오차

- `e_ss=lim(t→∞)e(t)=lim(s→0)sE(s)`

최종값이 존재하고 `sE(s)`의 모든 극이 개방 좌반평면에 있을 때만 최종값 정리를 적용한다.

우반평면 또는 허수축 극으로 발산하거나 지속 진동하면 최종값 정리를 적용하지 않는다.

### 5.6 시스템 형

표준 단위 피드백에서 원점 극·영점 상쇄를 반영한 유효 개루프 `L(s)`에 상쇄되지 않고 남은 원점 극의 수를 시스템 형으로 정의한다.

`L(s)=L0(s)/s^n`, `0<|L0(0)|<∞`이면 Type `n`이다.

폐루프 차수 또는 폐루프 극 전체의 수로 시스템 형을 정의하지 않는다.

정상상태 오차 관계를 적용하기 전에 폐루프 안정성을 별도로 확인한다.

### 5.7 정적 오차상수

표준 단위 피드백에서 정적 오차상수는 다음과 같다.

- `Kp_e=lim(s→0)L(s)`
- `Kv=lim(s→0)sL(s)`
- `Ka=lim(s→0)s²L(s)`

원점 극·영점 상쇄를 반영한 유효 개루프에 대해 계산한다.

각 정적 오차상수가 존재하고 해당 입력 조건에 적용 가능한지 확인한다.

### 5.8 Type별 정상상태 오차

폐루프가 안정한 표준 단위 피드백과 표준 단위 계단·램프·포물선 입력을 전제로 한다.

- Type 0: 계단 오차 `1/(1+Kp_e)`, 램프 오차 `∞`
- Type 1: 계단 오차 `0`, 램프 오차 `1/Kv`
- Type 2: 계단 오차 `0`, 램프 오차 `0`, 포물선 오차 `1/Ka`

각 관계는 해당 정적 오차상수가 정의되는 조건에서 적용한다.

### 5.9 적분과 trade-off

유효 루프에 상쇄되지 않은 원점 적분기를 추가하면 시스템 형이 증가하여 정상상태 오차 제거에 기여할 수 있다.

그러나 적분 동작은 위상여유 감소, 액추에이터 포화, 적분 windup 및 과도응답 악화를 유발할 수 있다.

루프 이득과 대역폭 증가는 추종성과 저주파 외란 억제를 개선할 수 있다.

시간지연, 우반평면 영점 및 미모델 고주파 동특성은 달성 가능한 대역폭을 제한하고 위상여유와 강인 안정성을 저하시킬 수 있다.

높은 대역폭은 센서 잡음 전달과 제어입력을 증가시킬 수 있다.

액추에이터 포화는 선형 위상여유의 직접 원인이라기보다 비선형 성능 저하와 적분 windup을 유발할 수 있다.

## 6. Acceptable answer expressions

- 부궤환, 음의 피드백, negative feedback
- loop transfer, loop gain
- sensitivity function, complementary sensitivity
- system type, 원점 극의 수, 순수 적분기 수
- output disturbance shaped by S
- measurement noise shaped by T
- 저주파 S 저감, 고주파 T roll-off
- phase margin, gain margin
- anti-windup, prefilter, feedforward

기호가 다르더라도 정의와 부호 관례를 제시하고 일관되게 사용하면 인정한다.

## 7. Fatal wrong claims

Fatal은 답안이 핵심 오개념을 실제 정답으로 직접 주장할 때만 적용한다.

### 7.1 negative_feedback_wrong_denominator

- 오개념: E=R-HY인 표준 음의 피드백의 폐루프 분모를 1-GH라고 단정한다.
- 정정: 폐루프 분모는 1+GH이다.

### 7.2 sensitivity_complementary_same

- 오개념: S와 T가 같은 함수라고 단정한다.
- 정정: S=1/(1+L), T=L/(1+L), S+T=1이다.

### 7.3 high_loop_gain_always_stable

- 오개념: 루프 이득을 높이면 모든 시스템이 항상 더 안정해진다고 단정한다.
- 정정: 이득과 대역폭 증가는 지연과 미모델 동특성 때문에 안정여유를 감소시킬 수 있다.

### 7.4 system_type_from_closed_loop_order

- 오개념: 폐루프가 2차이므로 Type 2라고 설명한다.
- 정정: 시스템 형은 개루프 L(s)의 원점 극 수이다.

### 7.5 type_zero_step_error_zero

- 오개념: Type 0의 계단 정상상태 오차가 항상 0이라고 단정한다.
- 정정: 일반적으로 1/(1+Kp_e)이다.

### 7.6 measurement_noise_always_rejected

- 오개념: 루프 이득을 높이면 측정 잡음이 모든 주파수에서 완전히 제거된다고 단정한다.
- 정정: 측정 잡음은 표준 구조에서 -T 경로이며 주파수별 T와 센서 필터로 판단한다.

### 7.7 final_value_without_stability

- 오개념: 불안정한 폐루프에도 최종값 정리를 항상 적용할 수 있다고 단정한다.
- 정정: 관련 극 조건과 최종값 존재 조건을 만족해야 한다.

### 7.8 feedback_rejects_all_disturbances

- 오개념: 피드백은 외란의 위치와 주파수에 관계없이 모든 외란을 완전히 제거한다고 단정한다.
- 정정: 외란 억제는 주입 위치, 주파수 및 해당 전달경로에 따라 달라진다.

## 8. Warn-level weak claims

다음은 fatal이 아니라 major 또는 minor 보완 대상으로 처리한다.

- 핵심 식이나 적용 조건 일부 누락
- 외란 주입 위치 미정의
- S와 T의 물리적 의미 누락
- 최종값 정리 안정 조건 누락
- Type별 오차표 일부 누락
- windup, 포화, 지연 및 안정여유 누락
- 답안이 짧거나 애매하지만 직접적인 오개념 주장이 없음

## 9. False positive cautions

1. 오답 문장을 인용한 뒤 틀렸다고 정정하는 문맥은 fatal이 아니다.
2. “주의할 오류”, “잘못된 주장”, “오개념” 목록의 문장을 실제 주장으로 해석하지 않는다.
3. 단위 피드백에서 Y/R=T라고 설명하는 것은 정상이다.
4. 저주파에서 루프 이득을 높여 S를 줄인다는 조건부 설명은 정상이다.
5. 양의 피드백 또는 다른 합산점 부호를 명시한 설명은 자동 fatal이 아니다.
6. 외란 주입 위치가 다르면 전달함수가 달라질 수 있다.
7. 단순 누락과 애매한 표현은 fatal이 아니다.
8. LLM이 답안에 없는 내용을 추론하여 fatal claim을 만들면 안 된다.

## 10. 고득점 답안 구조

1. 피드백 목적과 적용 배경
2. 블록선도와 신호 정의
3. 폐루프 전달함수와 특성방정식
4. S, T, S+T=1
5. 추종, 외란 및 측정 잡음 전달
6. 최종값 정리와 정상상태 오차
7. 시스템 형과 정적 오차상수
8. Type별 정상상태 오차
9. 루프 성능과 안정성 trade-off
10. anti-windup, prefilter, feedforward
11. 현장 검증
12. 결론

## 11. 현장 적용 판단 기준

- 센서 정확도, 잡음 및 필터
- 샘플링 주기와 계산 지연
- 통신 지연과 jitter
- 공정 dead time
- 액추에이터 용량, slew rate 및 포화
- 밸브 stiction과 dead band
- anti-windup
- prefilter와 feedforward
- 기존 설비 변경 비용
- 정지시간과 commissioning 위험
- Bode/Nyquist 안정여유
- 계단응답, 외란응답 및 포화시험
- 운전 trend와 rollback 계획

## 12. Logic Check LLM judgement requirements

### 12.1 기본 원칙

Logic Check의 fatal 판정은 정규표현식 직접 매칭으로 결정하지 않는다.

`wrong_patterns` 또는 keyword hit는 fatal의 최종 근거로 사용하지 않는다.

LLM이 전체 답안 문맥을 읽고 8개 fatal 항목을 각각 독립적으로 판정한다.

### 12.2 항목별 출력

각 항목은 다음 필드를 채운다.

- rule_id
- status: pass | major | fatal
- asserted
- evidence
- reason
- correction
- confidence

### 12.3 Fatal 조건

Fatal은 다음 조건을 모두 만족할 때만 허용한다.

1. 답안에 직접적인 핵심 오개념 주장이 존재한다.
2. 인용, 반박, 정정 및 주의사항 문맥이 아니다.
3. 다른 부호 관례 또는 신호 위치에 따른 정상 표현이 아니다.
4. 실제 evidence를 답안에서 제시할 수 있다.
5. confidence가 fatal threshold 이상이다.

### 12.4 Major 조건

- 핵심 설명 또는 적용 조건 누락
- 신호 위치 미정의
- 직접 오개념 주장으로 확정할 수 없는 모호한 표현
- confidence가 fatal threshold보다 낮음

### 12.5 Runtime output contract

LLM은 JSON object 하나만 반환한다.

필수 root field:

- verdict
- confidence
- reason
- checks
- findings

checks에는 8개 fatal rule 판정을 모두 포함한다.

findings에는 실제 major 또는 fatal 항목만 포함한다.

LLM 호출 실패, JSON parse 실패, 필수 필드 누락 또는 confidence 오류는 fatal로 처리하지 않는다.

## 13. fact_anchor.json generation guidance

Fact Anchor에는 핵심 수식, 물리적 의미, 적용 조건, Type별 오차 관계, trade-off 및 현장 검증 근거를 반영한다.

Fact Anchor는 정답 fact를 담고 감점 정책을 직접 정의하지 않는다.

## 14. logic_check.json generation guidance

1. llm_profile을 핵심 판정 source로 사용한다.
2. 8개 fatal misconception을 독립적으로 유지한다.
3. truth_schema, fatal_conditions, safe_conditions, ambiguity_policy, output_contract를 작성한다.
4. 정규표현식은 fatal 최종 판정기로 사용하지 않는다.
5. deterministic_checks.enabled는 false로 설정한다.
6. deterministic fatal list는 비우거나 runtime에서 실행되지 않도록 한다.
7. candidate extraction은 LLM에 전달할 문맥 후보 축소 용도로만 사용한다.
8. 누락과 설명 부족은 major이며 fatal이 아니다.
9. LLM 실패 또는 malformed JSON은 fatal cap을 만들지 않는다.

## 15. model_answer.json generation guidance

- 배경과 피드백 목적
- 블록선도와 신호 정의
- 폐루프 전달함수
- S와 T
- 외란과 잡음 전달
- 정상상태 오차와 시스템 형
- 성능·안정성 trade-off
- 현장 적용과 검증
- 결론

Low-score pattern은 평가 기준이며 합성 정답에 오답 문장을 삽입하는 용도가 아니다.

## 16. topic_importance.json generation guidance

- difficulty: THEORY_CORE
- selection_importance: CORE_MUST_PREPARE
- 고득점은 구조 유도, S/T 해석, 안정 조건 및 현장 trade-off를 연결할 때 허용한다.
- 누락만으로 fatal cap을 적용하지 않는다.

## 17. Cross-file consistency requirements

1. 동일한 topic_id
2. 동일한 question type
3. 동일한 difficulty와 importance
4. 동일한 8개 fatal misconception ID
5. Fact Anchor 정답과 Logic Check correction 일치
6. Model Answer 고득점 기준과 Fact Anchor 일치
7. Topic Importance high-band 조건과 Model Answer 일치
8. Logic Check는 A/B/C/D/E 점수를 직접 산정하지 않음

## 18. Human review checklist

- [ ] 음의 피드백 부호 관례가 명시되어 있는가?
- [ ] 일반 피드백과 단위 피드백이 구분되어 있는가?
- [ ] S, T, S+T=1이 정확한가?
- [ ] 외란 주입 위치가 구분되어 있는가?
- [ ] 측정 잡음의 -T 경로가 설명되어 있는가?
- [ ] 최종값 정리의 sE(s) 극 조건이 포함되어 있는가?
- [ ] 시스템 형이 원점 극·영점 상쇄를 반영한 유효 개루프의 상쇄되지 않은 원점 극 수로 정의되어 있는가?
- [ ] Type별 오차표가 정확한가?
- [ ] 루프 이득의 장점과 안정성 위험이 함께 제시되어 있는가?
- [ ] fatal과 단순 누락이 구분되어 있는가?
- [ ] 오답 인용·정정 문맥이 보호되는가?
- [ ] 정규식 직접 fatal 판정이 비활성화되어 있는가?
- [ ] LLM이 8개 항목을 각각 JSON으로 판정하는가?
- [ ] LLM 실패가 fatal로 변환되지 않는가?

## 19. Review decision

이 Topic Sheet를 사람이 검토하고 확정한 뒤 다음 단계로 진행한다.

1. generate_topic_pack_from_sheet.py로 JSON candidate 생성
2. candidate와 기존 source JSON diff 검토
3. schema-lock 검증
4. LLM Logic Check profile 검토
5. source Topic Pack 반영
6. generated bank 재생성
7. routing smoke
8. 정상 답안과 fatal 답안의 LLM 판정 검증

## Fact verification references

- MathWorks `feedback`: 표준 피드백 폐루프 전달함수
- MathWorks `loopsens`: 민감도 함수, 상보 민감도 함수 및 입력·출력 전달경로
- MathWorks loop-shaping guidance: 시간지연, 우반평면 영점, 미모델 고주파 동특성, 잡음 및 제어입력 trade-off
- MathWorks PID anti-windup guidance: 액추에이터 포화와 적분 windup
- MIT OpenCourseWare 16.06: 최종값 정리, 시스템 형, 정적 오차상수 및 Type별 정상상태 오차
