<!-- CURRENT_GRADING_ARCHITECTURE_START -->

## Current Grading Architecture

현재 채점 구조는 산업계측제어기술사 답안의 구조, Fact 정확성, 현장 적용성, 기술사적 판단성을 함께 평가하도록 구성되어 있다.

### 1. 기본 채점 구조

```text
A. 배경과 문제 진입: 4점
B. 문제 요구 파악: 5점
C. 유형별 Fact 기반 내용 설명: 8점
D. 현장 적용·설계 판단·제언: 6점
E. 연결성·면접 방어 가능성: 2점
총점: 25점
```

핵심 원칙은 다음과 같다.

```text
- 문제 유형은 별도 점수 체계가 아니라 C항목 평가 렌즈로 사용한다.
- 모범 답안 Bank는 정답 문장 매칭용이 아니라 구조·깊이·현장 적용성 기준으로 사용한다.
- D/E는 모든 문제 유형에서 현장 적용성, 설계 판단, 제언, 독창성을 공통 평가한다.
- Gemini semantic grader는 의미 평가를 수행한다.
- Python rule은 volume cap, 3인 layer 가중치, originality gate, fallback, 출력 후처리를 관리한다.
```

### 2. 문제 유형 렌즈

문제 유형은 다음 10개를 사용한다.

```text
DEFINE        : 정의·개념 설명형
PRINCIPLE     : 원리·메커니즘형
STRUCTURE     : 구성·분류형
COMPARE       : 비교·선정형
PROBLEM_SOLVE : 문제점·개선방안형
CAUSE_ACTION  : 원인·대책형
PROCEDURE     : 절차·방법론형
CALC_DESIGN   : 계산·설계형
APPLICATION   : 사례·적용형
EVALUATION    : 평가·효과 분석형
```

이 유형들은 별도 agent가 아니라 `C. 유형별 Fact 기반 내용 설명`의 평가 방식만 결정한다.

### 3. 주요 평가 구성요소

```text
Fact Anchor Bank
= 주제별로 반드시 들어가야 할 핵심 Fact 확인

Question Type Lens
= 문제 유형에 따라 C항목의 Fact 전개 방식 결정

Model Answer Bank
= 주제 + 문제유형별 기준 답안 참조
= 동일 문장 매칭 금지
= 구조, 깊이, 현장 적용성 기준으로만 사용

Originality / 기술사적 판단성
= 현장 조건, 대안 비교, 적용 우선순위, 검증 기준 평가

Volume Cap
= 답안 분량이 지나치게 짧을 경우 최종 점수 상한 적용

3인 Layer Weighting
= 교수, 기술사, 기업 임원 관점의 layer별 가중 합성
```

### 4. 현재 주요 Phase

```text
phase8  : 독창성·기술사적 판단성 평가
phase8b : 독창성 반영 후 최종 volume cap 강제
phase9  : question_type을 C항목 평가 렌즈로 적용
phase10 : model answer bank를 기준 답안으로 참조
phase11 : B/C 명칭을 문제 요구·유형별 Fact 설명으로 정리
phase12 : D/E 표현을 현장 적용·설계 판단·제언 중심으로 정리
phase13 : rubric_registry와 rubric_manager로 기준 작성 workflow 정리
phase14 : Telegram 보완 방향 중복 제거
phase15 : 내부 metric dict 숨김
phase16 : 최종 사용자 문구 polish
phase17 : 잔여 표현 정리
phase18 : Gemini 503/timeout retry wrapper
```

### 5. Rubric Authoring Workflow

평가 기준 및 유형별 모범 답안은 JSON으로 관리한다.

주요 파일은 다음과 같다.

```text
rubric_registry.py
question_type_router.py
model_answer_router.py
rubrics/question_types/default.json
rubrics/fact_anchors/industrial_instrumentation_control.json
rubrics/model_answers/industrial_instrumentation_control.json
rubrics/originality/default.json
rubrics/scoring_model/default.json
scripts/rubric_manager.py
docs/rubric_authoring_guide.md
```

자주 쓰는 명령은 다음과 같다.

```bash
python3 scripts/rubric_manager.py list-types
python3 scripts/rubric_manager.py list-model-answers
python3 scripts/rubric_manager.py validate-all
```

새 모범 답안 후보 생성 예시는 다음과 같다.

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

후보 편집 후 승격한다.

```bash
vim rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py promote-model-answer \
  --candidate rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py validate-all
```

자세한 작성 가이드는 `docs/rubric_authoring_guide.md`를 참조한다.

<!-- CURRENT_GRADING_ARCHITECTURE_END -->
