# 기술사 답안 채점 Telegram Bot

산업계측제어기술사 답안을 Telegram에서 입력받아 채점하는 프로젝트입니다.

이 프로젝트는 단순 키워드 매칭 채점기가 아니라, 다음 요소를 함께 평가하는 구조를 목표로 합니다.

- 문제 요구 파악
- 유형별 Fact 기반 내용 설명
- 현장 적용성
- 설계 판단과 제언
- 기술사적 독창성
- 답안 분량과 면접 방어 가능성

---

## 1. 현재 채점 구조

현재 채점 구조는 산업계측제어기술사 답안의 구조, Fact 정확성, 현장 적용성, 기술사적 판단성을 함께 평가하도록 구성되어 있습니다.

```text
A. 배경과 문제 진입: 4점
B. 문제 요구 파악: 5점
C. 유형별 Fact 기반 내용 설명: 8점
D. 현장 적용·설계 판단·제언: 6점
E. 연결성·면접 방어 가능성: 2점
총점: 25점
```

핵심 원칙은 다음과 같습니다.

```text
- 문제 유형은 별도 점수 체계가 아니라 C항목 평가 렌즈로 사용한다.
- 모범 답안 Bank는 정답 문장 매칭용이 아니라 구조·깊이·현장 적용성 기준으로 사용한다.
- D/E는 모든 문제 유형에서 현장 적용성, 설계 판단, 제언, 독창성을 공통 평가한다.
- Gemini semantic grader는 의미 평가를 수행한다.
- Python rule은 volume cap, 3인 layer 가중치, originality gate, fallback, 출력 후처리를 관리한다.
```

---

## 2. 문제 유형 렌즈

문제 유형은 다음 10개를 사용합니다.

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

이 유형들은 별도 채점 agent가 아닙니다.  
문제 유형은 `C. 유형별 Fact 기반 내용 설명`의 평가 방식만 결정합니다.

예시는 다음과 같습니다.

```text
DEFINE
= 정의, 핵심 개념, 적용 범위, 한계, 실무 의미를 설명했는가

COMPARE
= 비교 대상, 비교축, 장단점, 적용 조건, 선정 기준을 설명했는가

CALC_DESIGN
= 공식, 변수, 단위, 계산 과정, 결과 해석, 설계 기준을 설명했는가

EVALUATION
= 평가 지표, 평가 방법, before/after, 정량·정성 효과, 한계를 설명했는가
```

---

## 3. 주요 평가 구성요소

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

---

## 4. 현재 주요 Phase

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

---

## 5. 프로젝트 구조

```text
.
├── bot.py
├── gemini_grader.py
├── grading_agents.py
├── grading_config.py
├── model_answer_router.py
├── originality_grader.py
├── question_type_router.py
├── rubric_registry.py
├── rubrics/
│   ├── active_profile.json
│   ├── default.json
│   ├── fact_anchors/
│   │   └── industrial_instrumentation_control.json
│   ├── model_answers/
│   │   ├── industrial_instrumentation_control.json
│   │   └── candidates/
│   ├── originality/
│   │   └── default.json
│   ├── question_types/
│   │   └── default.json
│   ├── raters/
│   │   ├── default.json
│   │   └── layered_default.json
│   ├── scoring_model/
│   │   └── default.json
│   └── subjects/
│       └── industrial_instrumentation_control.json
├── scripts/
│   ├── gemini_audit_grading_engine.py
│   ├── rubric_manager.py
│   ├── show_model_answer.py
│   ├── validate_config.py
│   ├── validate_fact_anchor_bank.py
│   ├── validate_model_answer_bank.py
│   └── validate_question_type_profile.py
└── docs/
    └── rubric_authoring_guide.md
```

---

## 6. 주요 파일 역할

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram Bot 진입점 |
| `grading_agents.py` | 채점 파이프라인 및 phase orchestration |
| `gemini_grader.py` | Gemini semantic grader prompt 및 API 호출 |
| `question_type_router.py` | 문제 유형 판정 및 C항목 평가 렌즈 선택 |
| `model_answer_router.py` | 주제 + 문제유형 기준 모범 답안 참조 |
| `originality_grader.py` | 독창성·기술사적 판단성 평가 |
| `rubric_registry.py` | rubric/model answer 공통 로딩·검증·template 관리 |
| `scripts/rubric_manager.py` | 모범 답안 후보 생성, 승격, 검증 CLI |
| `rubrics/question_types/default.json` | 문제 유형별 C항목 평가 기준 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | 주제별 핵심 Fact Anchor |
| `rubrics/model_answers/industrial_instrumentation_control.json` | 주제 + 문제유형별 모범 답안 Bank |
| `docs/rubric_authoring_guide.md` | 평가 기준과 모범 답안 작성 가이드 |

---

## 7. Rubric Authoring Workflow

평가 기준 및 유형별 모범 답안은 JSON으로 관리합니다.

자주 쓰는 명령은 다음과 같습니다.

```bash
python3 scripts/rubric_manager.py list-types
python3 scripts/rubric_manager.py list-model-answers
python3 scripts/rubric_manager.py validate-all
```

새 모범 답안 후보 생성 예시는 다음과 같습니다.

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

후보 파일을 편집합니다.

```bash
vim rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json
```

검증 후 본 Bank로 승격합니다.

```bash
python3 scripts/rubric_manager.py promote-model-answer \
  --candidate rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py validate-all
```

자세한 작성 가이드는 `docs/rubric_authoring_guide.md`를 참조합니다.

---

## 8. 모범 답안 작성 원칙

모범 답안은 정답 문장 매칭용이 아닙니다.

좋은 모범 답안은 다음을 포함해야 합니다.

```text
1. 문제 유형에 맞는 C항목 전개 방식
2. 반드시 들어갈 핵심 Fact
3. 현장 적용 의미
4. 설계 판단 또는 제언
5. 저득점 패턴
6. 현장 연결 포인트
```

Model Answer Bank는 다음 기준으로만 사용합니다.

```text
- 답안 구조 기준
- 설명 깊이 기준
- Fact 누락 확인
- 현장 적용성 보완 방향
- 저득점 패턴 피드백
```

다음 용도로 사용하지 않습니다.

```text
- 동일 문장 매칭
- 표현이 다르다는 이유만으로 감점
- 모범 답안에 없는 현장적으로 타당한 설명 배제
```

---

## 9. 실행 및 검증

문법 및 rubric 검증:

```bash
python3 scripts/rubric_manager.py validate-all
```

Docker 컨테이너 기준 검증:

```bash
docker exec -it hermes_agent bash -lc '
cd /workspace/prof_eng_answer &&
python scripts/rubric_manager.py validate-all &&
echo "container validation OK"
'
```

Bot 재시작:

```bash
docker exec hermes_agent bash -lc 'pkill -f "python.*bot.py" || true'

: > logs/prof_eng_answer.log

docker exec -d hermes_agent bash -lc '
cd /workspace/prof_eng_answer &&
nohup python bot.py >> logs/prof_eng_answer.log 2>&1 &
'

docker exec hermes_agent bash -lc 'ps aux | grep "[b]ot.py"'
```

Gemini 적용 로그 확인:

```bash
tail -n 120 logs/prof_eng_answer.log | grep -Ei "gemini|semantic|retry|failed|503|timeout|applied" || true
```

정상 로그 예시:

```text
[agent] Gemini semantic grader applied.
```

일시 장애 후 재시도 성공 예시:

```text
[agent] Gemini semantic grader retry 1/4: ...
[agent] Gemini semantic grader applied.
```

---

## 10. Telegram 사용 예시

```text
/grade
문제: Cv(Valve Flow Coefficient)를 설명하시오.

답안:
Cv는 밸브의 유량계수로 밸브를 통과할 수 있는 유량의 크기를 나타낸다.
Cv가 크면 유량이 많이 흐르고, 밸브 선정에 사용된다.
```

정상 평가 흐름:

```text
문제 유형: DEFINE
모범 답안 Bank: Cv 밸브 유량계수 정의형 모범 답안 참조
C항목: 정의·개념 설명형 렌즈로 평가
D/E항목: 현장 적용성, 설계 판단, 제언, 독창성 평가
```

---

## 11. Git 관리

작업 전 상태 확인:

```bash
git status --short
git log --oneline -5
```

일반 커밋:

```bash
git add <changed files>
git commit -m "Describe change"
git push origin main
```

이번 구조 정리 이후 주요 커밋 대상 예시는 다음과 같습니다.

```bash
git add README.md \
        grading_agents.py \
        gemini_grader.py \
        question_type_router.py \
        model_answer_router.py \
        rubric_registry.py \
        scripts/rubric_manager.py \
        docs/rubric_authoring_guide.md \
        rubrics/model_answers/industrial_instrumentation_control.json

git commit -m "Finalize grading architecture and rubric workflow"
git push origin main
```

---

## 12. 주의사항

- `.env`, API key, Telegram token은 커밋하지 않습니다.
- `data/sessions/`, `logs/`, `backups/`, `__pycache__/`는 커밋 대상에서 제외합니다.
- Gemini API가 503, timeout, connection reset을 반환할 수 있으므로 retry wrapper가 적용되어야 합니다.
- Gemini 실패 시 Python fallback 채점으로 전환될 수 있으며, 이 경우 신뢰도와 총평이 달라질 수 있습니다.
- 짧은 답안은 `text_only_short_answer`로 분류되어 최종 점수 상한이 적용됩니다.

<!-- EXAM_TREND_WORKFLOW_START -->

---

## 13. 기출 트렌드 기반 키워드·예상문제·예상답안 업데이트 흐름

이 프로젝트는 기출 데이터 분석 결과를 바탕으로 키워드별 예상 문제유형, 평가 기준, 예상문제, 예상답안을 확장할 수 있다.

기본 흐름은 다음과 같다.

    외부 기출 분석 사이트 JSON
        ↓
    scripts/import_exam_trend_keywords.py
        ↓
    rubrics/exam_trends/industrial_instrumentation_control_raw.json
        ↓
    rubrics/keyword_question_profiles/industrial_instrumentation_control.json
        ↓
    키워드별 예상 문제유형 확인
        ↓
    예상문제 작성
        ↓
    예상답안 작성
        ↓
    model answer bank 또는 별도 예상문제 bank에 반영
        ↓
    Telegram 채점/연습에 활용

---

### 13.1 직접 수정하는 파일

키워드별 예상 문제유형과 핵심 Fact를 수정할 때는 아래 파일을 수정한다.

    rubrics/keyword_rules/industrial_instrumentation_control.json

예를 들어 스마트 팩토리, IIoT, 디지털 트윈의 예상 문제유형을 바꾸고 싶으면 이 파일에서 해당 rule의 `types`와 `facts`를 수정한다.

문제유형별 평가 기준 문구를 수정할 때는 아래 파일을 수정한다.

    rubrics/question_type_criteria/default.json

이 파일은 DEFINE, COMPARE, APPLICATION, EVALUATION 등 문제유형별 C항목 평가 기준을 관리한다.

---

### 13.2 자동 생성되는 파일

기출 분석 사이트에서 추출한 원본 JSON은 아래 파일에 저장된다.

    rubrics/exam_trends/industrial_instrumentation_control_raw.json

키워드별 예상 문제유형, 우선순위, Fact focus, 유형별 평가 기준을 조립한 최종 결과는 아래 파일에 저장된다.

    rubrics/keyword_question_profiles/industrial_instrumentation_control.json

이 두 파일은 사람이 직접 수정하기보다 스크립트 실행으로 갱신하는 것을 원칙으로 한다.

---

### 13.3 기출 트렌드 재생성 명령

사이트의 기출 분석 JSON을 다시 가져와 최신 키워드 profile을 생성할 때는 다음 명령을 실행한다.

    python3 scripts/import_exam_trend_keywords.py

실행 결과 예시는 다음과 같다.

    JSON candidates found: 2
    keywords imported: 20
    raw json saved: rubrics/exam_trends/industrial_instrumentation_control_raw.json
    keyword profiles saved: rubrics/keyword_question_profiles/industrial_instrumentation_control.json

다른 URL을 사용하려면 다음처럼 실행한다.

    python3 scripts/import_exam_trend_keywords.py --url "https://example.com/your-analysis-page"

JSON 후보가 여러 개 있을 때 전체 count가 큰 JSON을 우선 사용하려면 다음처럼 실행한다.

    python3 scripts/import_exam_trend_keywords.py --prefer max-count

---

### 13.4 키워드별 예상문제 작성 흐름

예상문제는 `keyword_question_profiles`에서 다음 정보를 확인한 뒤 작성한다.

    keyword
    aliases
    priority_band
    expected_question_types
    fact_focus
    type_profiles

예를 들어 스마트 팩토리 키워드는 다음과 같이 해석한다.

    keyword: 인공지능/빅데이터/IoT 또는 스마트팩토리 계열
    expected_question_types:
      - DEFINE
      - STRUCTURE
      - APPLICATION
      - EVALUATION
      - PROBLEM_SOLVE
    fact_focus:
      - IT/OT 연계
      - 데이터 수집
      - 엣지
      - 디지털트윈
      - 보안

따라서 예상문제는 다음 유형으로 만든다.

    1. 개념·구성형
       스마트 팩토리의 개념과 구성요소를 설명하시오.

    2. 적용·사례형
       산업계측제어 분야에서 스마트 팩토리 적용 방안을 설명하시오.

    3. 문제점·개선방안형
       스마트 팩토리 구축 시 문제점과 개선방안을 설명하시오.

    4. 평가·효과분석형
       스마트 팩토리 도입 효과를 평가하는 방법을 설명하시오.

    5. 비교·선정형
       Edge, Cloud, On-premise 기반 스마트 팩토리 구축 방식을 비교하시오.

---

### 13.5 예상답안 작성 흐름

예상답안은 기존 기술사 답안 구조를 유지한다.

    1. 배경
    2. 내용 또는 핵심 Fact
    3. 문제점 또는 적용상 쟁점
    4. 개선방안 또는 설계 판단
    5. 결론 및 면접 방어 포인트

키워드별 예상답안을 작성할 때는 다음 기준을 반드시 포함한다.

    - 문제유형에 맞는 C항목 전개 방식
    - keyword_rules의 fact_focus
    - 현장 적용 조건
    - 기존 설비와의 연관성
    - 비용, 일정, 리스크
    - 보안, 유지보수, 검증 기준
    - 면접에서 방어 가능한 판단 근거

---

### 13.6 예상답안 반영 위치

예상답안이 채점 기준으로도 활용될 수준이면 Model Answer Bank에 반영한다.

    rubrics/model_answers/industrial_instrumentation_control.json

후보로 먼저 만들고 검토한 뒤 승격하는 흐름을 권장한다.

    python3 scripts/rubric_manager.py new-model-answer ...
    vim rubrics/model_answers/candidates/<candidate>.json
    python3 scripts/rubric_manager.py promote-model-answer --candidate <candidate>.json
    python3 scripts/rubric_manager.py validate-all

단순 연습문제나 예상문제 묶음으로만 관리하려면 별도 디렉터리를 사용할 수 있다.

    rubrics/expected_questions/

이 경우 예상문제와 예상답안을 채점 기준과 분리하여 관리할 수 있다.

---

### 13.7 업데이트 판단 기준

새 키워드를 추가할 때는 다음 기준으로 판단한다.

    high priority:
      - 최근 회차 출현 빈도가 높음
      - 여러 문제유형으로 변형 가능
      - 산업계측제어 실무와 직접 연결됨
      - 모범답안 Bank로 만들 가치가 있음

    medium priority:
      - 출제 가능성은 있으나 특정 유형에 치우침
      - 예상문제 2~3개 정도 작성

    low priority:
      - 단독 주제보다 다른 주제의 하위 항목으로 관리
      - Fact Anchor 보강 위주로 관리

---

### 13.8 최종 검증

키워드, 예상 문제유형, 예상답안 관련 파일을 수정한 뒤에는 다음을 실행한다.

    python3 scripts/import_exam_trend_keywords.py
    python3 scripts/rubric_manager.py validate-all

컨테이너 기준 검증은 다음과 같이 수행한다.

    docker exec -it hermes_agent bash -lc '
    cd /workspace/prof_eng_answer &&
    python scripts/import_exam_trend_keywords.py &&
    python scripts/rubric_manager.py validate-all &&
    echo "exam trend workflow validation OK"
    '

---

### 13.9 Git 반영 예시

    git status --short

    git add scripts/import_exam_trend_keywords.py \
            rubrics/keyword_rules/industrial_instrumentation_control.json \
            rubrics/question_type_criteria/default.json \
            rubrics/exam_trends/industrial_instrumentation_control_raw.json \
            rubrics/keyword_question_profiles/industrial_instrumentation_control.json \
            rubrics/model_answers/industrial_instrumentation_control.json \
            README.md

    git commit -m "Document exam trend keyword workflow"
    git push origin main

<!-- EXAM_TREND_WORKFLOW_END -->
