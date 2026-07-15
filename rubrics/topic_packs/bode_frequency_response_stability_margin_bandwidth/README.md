# Bode 선도에 의한 안정여유·대역폭 해석과 주파수응답 설계

## Topic 정보

- Topic ID: `bode_frequency_response_stability_margin_bandwidth`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 판정 방식: `LLM_ONLY`
- 결정론 검사: 비활성화
- candidate rule: 빈 배열

## 목적

이 Topic Pack은 Bode 선도의 크기·위상 작도에서 출발하여 개루프
안정여유, 폐루프 대역폭, 시간응답, 강인성과 보상기 설계를 하나의
논리로 평가한다.

핵심 구분은 다음과 같다.

- PM과 GM: 루프 전달함수 `L(s)=G(s)H(s)`
- 폐루프 bandwidth: `T(s)=L(s)/(1+L(s))`
- gain crossover: `|L(jω_gc)|=1`
- phase crossover: `∠L(jω_pc)=-(2k+1)180°`

## Fact Anchor

정확히 14개 Anchor를 사용한다.

1. 개루프와 폐루프 전달함수의 역할
2. 로그 주파수축과 dB 표현
3. 극점·영점의 크기 기울기
4. 위상 기여와 비최소위상 요소
5. 양의 상수 이득 변화
6. 두 교차주파수의 정의
7. 위상여유 계산
8. 이득여유 계산
9. 교차점 부재와 다중 교차점
10. 폐루프 대역폭
11. 안정여유와 시간응답의 근사 관계
12. 시간지연과 비최소위상 한계
13. 감도·강인성·잡음 trade-off
14. 보상기 설계와 현장 검증

## Fatal misconception

정확히 8개 직접 반대 주장을 판정한다.

1. PM·GM을 폐루프 Bode에서 직접 계산
2. 두 crossover를 항상 동일시
3. PM 부호 오류
4. GM dB 부호 오류
5. bandwidth와 gain crossover를 항상 동일시
6. PM과 damping ratio를 보편적 정확식으로 단정
7. 시간지연의 안정성 영향을 부정
8. 양의 margin이 모든 시스템의 안정을 보장한다고 단정

단순 누락은 fatal로 판정하지 않는다.

## 적용 한계

다음 조건에서는 단일 PM·GM만으로 판단하지 않는다.

- 개루프 불안정 극점
- multiple crossover
- phase wrapping
- 비최소위상 영점
- 큰 시간지연
- 고주파 미모델 공진
- 비선형 포화와 rate limit

필요하면 전체 Nyquist 조건과 폐루프 극점을 병행 검증한다.

## 보상기와 현장 적용

- lead: 목표 crossover 부근의 위상여유와 응답속도 개선
- lag: 저주파 이득과 정상상태 성능 개선
- PID: P·I·D의 주파수별 이득·위상 기여 검토
- 적용 전 운전점, 시간지연, 포화, deadband, 잡음과 모델 오차 검증
- 적용 후 margin, bandwidth, overshoot, 정착시간과 조작량 비교

## 파일

- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

## 검증 명령

아래 명령으로 검증한다.

    python3 scripts/rubric_manager.py validate-topic-packs
    python3 scripts/rubric_manager.py validate-topic-pack-quality         --topic-id bode_frequency_response_stability_margin_bandwidth

## 작성 원칙

다른 제어이론 Topic의 작도 규칙이나 변경 이력을 복사하지 않는다.
Bode 전용 수식, 판단 조건, 예외와 현장 검증만 유지한다.

## Fact verification references

- MathWorks Control System Toolbox, `bode`: 로그 주파수축, dB 크기와 위상응답 해석
- MathWorks Control System Toolbox, `margin` 및 `allmargin`: 이득교차·위상교차, PM·GM 및 다중 교차점
- MathWorks Control System Toolbox, `bandwidth`: 폐루프 DC 이득 대비 -3 dB 대역폭
- MathWorks Control System Toolbox, `loopsens`: 감도함수와 상보감도함수 및 강인성 trade-off
- MIT OpenCourseWare 16.30, `Feedback Control Systems - Recitation 11: Time Delays`: 시간지연과 안정여유
- MIT OpenCourseWare, `Electronic Feedback Systems`: Bode 해석, 비최소위상 요소 및 보상설계

## Rubric clarification

- `accepted_explanations`는 허용 가능한 정답 설명이다.
- `rejected_explanations`는 실제 오답, 정의 교환, 무조건적 일반화 또는 적용조건 누락 사례만 포함한다.
- 동일하거나 의미상 동등한 문장을 두 필드에 동시에 배치하지 않는다.
