# Topic Sheet: 2차 시스템 모델링과 전기계·기계계 유사성

> 상태: 사용자가 핵심 사실·범위·분류·라우팅 후보를 검토하고 승인했다. 운영 채점 반영 및 공식 Topic 승인 전 초안 상태는 유지한다.

## 1. Topic metadata

```text
topic_id: second_order_system_modeling_electromechanical_analogy
표시 이름: 2차 시스템 모델링과 전기계·기계계 유사성
문제 유형: PRINCIPLE_INTERPRETATION
난이도: THEORY_CORE (사용자 검토 승인)
선택 중요도: HIGH (사용자 검토 승인)
상태: draft / human_review_required
```

## 2. Scope and ownership

### 소유 범위

- 전기계 RLC 회로와 기계계 질량-스프링-댐퍼의 2차 지배방정식 구조
- 두 계의 계수·변수 대응을 이용한 유사성(Force–Voltage analogy)
- 대응 관계가 상태변수와 에너지 저장·소산 요소에 갖는 의미
- 제어시스템/물리계 모델링에서 2차 선형 모델을 해석하는 기초

사용자가 다음 출처 내용과 대응을 승인했다.

```text
기계계: m x¨ + D x˙ + kx = f(t)
전기계: L q¨ + R q˙ + (1/C)q = E(t)
대응: f↔E, m↔L, D↔R, k↔1/C, x↔q, 속도↔전류
```

### 소유하지 않는 범위

- 감쇠비별 계단응답, 오버슈트, 정착시간 등 시간응답 분류: `second_order_lag_response_by_damping_ratio`
- 공진주파수·공진 peak·주파수응답 계산: `second_order_system_resonance_frequency_response`
- Bode/Nyquist 안정여유, 폐루프 안정도, 제어기 보상기 설계
- 특정 기계설비의 진동 진단·구조 설계 세부기준

사용자는 이 주제를 기존 시간응답·공진 Topic과 구분되는 별도 Topic으로 유지하는 데 동의했다. 이 토픽은 기존 두 2차 시스템 토픽을 대체하거나 범용 umbrella로 합치지 않는다.

## 3. Core correct facts — 검토 후보

- 질량-스프링-댐퍼 계와 직렬 RLC 계는 각 계의 요소값에 따라 2차 선형 미분방정식으로 표현될 수 있다. (사용자 승인)
- WordPress PDF의 Force–Voltage analogy `m↔L`, `D↔R`, `k↔1/C` 및 변수 대응을 사용한다. (사용자 승인)
- 대응표는 물리량을 동일시하는 것이 아니라 두 모델 방정식의 수학적 구조를 대응시키는 것으로 설명해야 한다.
- 변수 정의, 초기조건, 입력·출력 선택 및 직렬/병렬 회로 조건에 따라 전달함수 표현이 달라질 수 있으므로 단일 대응표를 무조건 일반화하지 않는다.

## 4. Acceptable answer expressions

- “질량-스프링-댐퍼와 RLC 회로는 계수 대응을 통해 동일 형식의 2차 방정식으로 모델링할 수 있다.”
- “Force–Voltage analogy에서는 힘과 전압, 질량과 인덕턴스, 점성 감쇠와 저항, 스프링 강성과 역커패시턴스를 대응시킨다.”
- “이 유사성은 전기계 해석 도구를 기계계 모델에 대응시키는 수학적 모델링 관계다.”

대표 답안 표현으로 승인되었다. 다른 표현은 같은 의미와 모델 조건을 유지하는 범위에서 해석한다.

## 4.1 필수 차원 확인

`L q¨` 항의 차원 확인은 선택적인 참고가 아니라 이 토픽의 **핵심 학습 항목**으로 포함한다. 학습·답안 흐름에서 인덕턴스 및 전하의 단위를 두고 해당 항이 입력 전압과 차원이 일치하는지 확인한다. 구체적인 단위 전개는 첨부 PDF p.2를 따른다.

## 5. Fatal wrong claims — 확정 전 보류

내용 판단은 검토되었으나, 운영 점수에 영향을 주는 fatal rule은 별도의 rule 검증 및 공식 승인 전까지 만들지 않는다. 다음은 향후 rule 설계 시 오탐 방지를 위해 고려할 사항이다.

- 기계계와 전기계의 서로 다른 물리량을 단위·정의 확인 없이 물리적으로 동일하다고 단정
- Force–Voltage analogy에서 저항과 스프링 요소의 대응을 뒤바꿈
- 방정식의 입력, 상태변수, 초기조건을 확인하지 않고 모든 RLC 구성에 같은 대응을 적용

## 6. Warn-level weak claims

- 대응표만 제시하고 대응이 성립하는 모델 가정·방정식 구조를 설명하지 않음
- 기계계와 전기계의 대응 방향(Force–Voltage / Force–Current)을 구별하지 않음
- 에너지 저장 요소와 소산 요소의 역할을 언급하지 않음

## 7. False-positive cautions

- `m↔L`, `D↔R`, `k↔1/C`는 선택한 Force–Voltage analogy에서 쓰는 대응이다. 다른 analogy의 명칭·대응과 혼동을 곧바로 오답 처리하지 말고 문제에서 요구한 기준을 확인한다.
- 상태변수로 변위/전하 또는 속도/전류를 택하는 표현은 모델 정의와 문맥을 함께 본다.
- 단순히 “유사하다”고 표현한 것은 대응 관계를 기술하지 않은 부족 답안이지, 그 자체로 치명적 오개념은 아니다.

## 8. Regex candidate patterns

정규식 기반 fatal 판정은 만들지 않는다. 표기/OCR 변형은 Fact evidence 검색용으로만 검토한다.

## 9. Fact Anchor generation guidance

사람이 원 출처와 단위·방정식을 확인한 뒤 다음을 독립 판정 가능한 anchor로 분리한다.

1. 기계계 지배방정식과 변수·단위
2. 전기계 지배방정식과 회로구성 가정
3. 선택한 analogy의 요소 대응표
4. 대응의 물리적 의미와 한계

## 10. Logic Check generation guidance

- 출처 검토 전에는 production fatal rule을 생성하지 않는다.
- 같은 analogy 체계에서 계수 대응이 뒤바뀐 주장처럼, 확인 가능한 단일 오개념만 rule 후보로 만든다.
- Force–Voltage와 Force–Current 표현 차이를 오탐하지 않도록 기준·변수 정의를 함께 검사한다.

## 11. Model Answer generation guidance

답안 흐름 후보:

1. 2차 시스템과 모델링 목적
2. 기계계 및 전기계 지배방정식
3. 선택한 analogy와 대응표
4. 요소별 에너지 저장/소산 및 변수 의미
5. 모델 적용 가정·한계와 현장 적용
6. 감쇠비별 시간응답·공진주파수는 인접 Topic으로 handoff

대표 WordPress 자료: [136회 2교시 2번](https://now0930.pe.kr/wordpress/136%ed%9a%8c-2%ea%b5%90%ec%8b%9c-2%eb%b2%88/) 및 첨부 `fourier_Transform-2.pdf` (2쪽). 출처 내용의 정확성은 미승인 상태다.

## 12. Topic Importance guidance

- 분류 후보: `THEORY_CORE`, `HIGH`
- 출제 빈도·난이도·선택 중요도는 기출 원문과 기존 분포를 확인한 후 확정한다.
- 본 초안은 점수 상향·감점·fatal ceiling을 정의하지 않는다.

## 13. Human review checklist

- [x] 기계계·직렬 RLC 식과 Force–Voltage 대응 검토 — 사용자 승인
- [x] `L q¨` 차원 확인을 핵심 학습 항목으로 설정 — 사용자 승인
- [x] 기존 시간응답·공진 Topic과 별도 소유 범위로 유지 — 사용자 승인
- [x] 난이도 `THEORY_CORE`, 선택 중요도 `HIGH` — 사용자 승인
- [x] 현재 question pattern 및 라우팅 표현을 대표 후보로 사용 — 사용자 승인
- [ ] 운영용 fatal/major 규칙 및 점수 영향 검증
- [ ] 변경사항 release 검증 후 공식 `approve-topic` 및 운영 반영 여부 결정

## 14. Cross-topic handoff

```text
2차 시스템 모델·계간 유사성
  ├─ 감쇠비별 시간응답 → second_order_lag_response_by_damping_ratio
  └─ 주파수응답·공진 → second_order_system_resonance_frequency_response
```
