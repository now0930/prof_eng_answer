# 평가 기준과 유형별 모범 답안 작성 가이드

## 1. 기본 원칙

이 프로젝트의 채점 구조는 다음을 유지한다.

- A: 배경과 문제 진입
- B: 문제 요구 파악
- C: 유형별 Fact 기반 내용 설명
- D: 현장 적용·설계 판단·제언
- E: 연결성·면접 방어 가능성

문제 유형은 별도 점수 체계가 아니라 C항목을 평가하는 렌즈이다.

## 2. JSON 역할

| 파일 | 역할 |
|---|---|
| `rubrics/question_types/default.json` | DEFINE, COMPARE, CALC_DESIGN 등 문제 유형별 C항목 평가 렌즈 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | 주제별 핵심 Fact Anchor |
| `rubrics/model_answers/industrial_instrumentation_control.json` | 주제 + 문제유형별 기준 답안 |
| `rubrics/originality/default.json` | 독창성·기술사적 판단성 평가 기준 |
| `rubrics/scoring_model/default.json` | A/B/C/D/E 배점 구조 |

## 3. 모범 답안 작성 원칙

모범 답안은 정답 문장 매칭용이 아니다.

좋은 모범 답안은 다음을 포함해야 한다.

1. 문제 유형에 맞는 C항목 전개 방식
2. 반드시 들어갈 핵심 Fact
3. 현장 적용 의미
4. 설계 판단 또는 제언
5. 저득점 패턴
6. 현장 연결 포인트

## 4. 새 모범 답안 추가 절차

예시: Cv 비교형 모범 답안 초안 생성

```bash
python3 scripts/rubric_manager.py new-model-answer \
  --topic-id cv_valve_flow_coefficient \
  --question-type COMPARE \
  --title "Cv 비교·선정형 모범 답안" \
  --question "Cv와 Kv를 비교하고 적용 기준을 설명하시오." \
  --alias "Cv" \
  --alias "Kv" \
  --field "밸브 사이징" \
  --field "제조사 data"
```

주의: 실제 터미널에서 실행할 때도 마지막 줄에는 `\`를 붙이지 않는다.

생성된 candidate를 편집한다.

```bash
vim rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json
```

검증 후 승격한다.

```bash
python3 scripts/rubric_manager.py promote-model-answer \
  --candidate rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py validate-all
```

## 5. question_type 선택 기준

| 유형 | C항목에서 보는 것 |
|---|---|
| DEFINE | 정의, 핵심 개념, 적용 범위, 한계, 실무 의미 |
| PRINCIPLE | 발생 조건, 원리, 메커니즘, 인과관계, 결과 현상 |
| STRUCTURE | 구성요소, 분류 기준, 계층 구조, 역할 관계 |
| COMPARE | 비교 대상, 비교축, 장단점, 적용 조건, 선정 기준 |
| PROBLEM_SOLVE | 문제 현상, 요구 파악, 원인, 개선 방향, 한계 |
| CAUSE_ACTION | 직접 원인, 근본 원인, 발생 메커니즘, 원인별 대책 |
| PROCEDURE | 절차 순서, 입력 자료, 수행 방법, 판단 기준, 산출물 |
| CALC_DESIGN | 공식, 변수, 단위, 계산 과정, 결과 해석, 설계 기준 |
| APPLICATION | 적용 대상, 적용 조건, 제약, 적용 방식, 기대 효과 |
| EVALUATION | 평가 대상, 지표, 방법, before/after, 효과, 한계 |

## 6. 점검 명령

```bash
python3 scripts/rubric_manager.py list-types
python3 scripts/rubric_manager.py list-model-answers
python3 scripts/rubric_manager.py validate-all
```
