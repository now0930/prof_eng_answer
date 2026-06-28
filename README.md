# 기술사 답안 채점 Telegram Bot MVP

산업계측제어기술사 답안을 Telegram으로 입력받아 기술사 답안지 기준에 맞춰 채점하는 MVP 프로젝트이다.

현재 채점 방식은 단순 키워드 매칭이 아니라 다음 두 축을 결합한다.

- Gemini: A/B/C/D/E 의미 기반 원점수와 정성 사유 평가
- Python: 채점 규정, 답안지 분량 cap, Fact 부족 cap, 3인 채점자 가중 합성, 결과 저장과 Telegram 출력

---

## 1. 채점 구조

25점 문항을 다음 5개 Layer로 평가한다.

| Layer | 항목 | 배점 |
|---|---|---:|
| A | 배경과 문제 진입 | 4 |
| B | 문제 요구 파악 | 5 |
| C | 유형별 Fact 기반 내용 설명 | 8 |
| D | 현장 적용·설계 판단·제언 | 6 |
| E | 연결성·면접 방어 가능성 | 2 |
| 합계 |  | 25 |

기준선은 다음과 같다.

- 공식 합격선: 15점
- 실전 목표선: 17.5점
- 고득점 기준: 20점

---

## 2. 답안지 분량 정책

기술사 25점 문항은 답안지 약 3쪽 수준의 전개를 기준으로 본다.

| 답안 상태 | 판단 | 상한 |
|---|---|---:|
| 사진 없음 + 짧은 텍스트 | `text_only_short_answer` | 9점 |
| 답안지 1쪽 수준 | `one_page_level` | 13점 |
| 답안지 2쪽 수준 | `two_page_level` | 17점 |
| 답안지 3쪽 수준 | `three_page_level` | 고득점 가능 |

사진 3장이 있으나 OCR 텍스트가 짧은 경우에는 OCR 누락 가능성을 표시하고 잠정 평가한다.

---

## 3. 채점 파이프라인

현재 흐름은 다음과 같다.

1. Telegram `/grade` 입력 수신
2. 세션 생성 및 입력 저장
3. active profile 기준 설정 로드
4. Ollama/Gemma 보조 분석
5. Python A/B/C/D/E 기본 구조 분석
6. Fact Anchor 평가
7. Connection 평가
8. Gemini 의미 기반 A/B/C/D/E 원점수 평가
9. Python volume cap 적용
10. Fact 부족 시 D/E 상한 적용
11. 교수·기술사·기업 임원 layer 가중 합성
12. Telegram 결과 출력
13. 세션별 JSON 산출물 저장

정상 로그 예:

```text
[agent] Gemini semantic grader applied.
```

---

## 4. 3인 채점자

| 채점자 | 핵심 관점 |
|---|---|
| 교수 채점자 | 개념, 용어, fact 설명의 정확성 |
| 기술사 채점자 | 문제점, fact, 대책의 현장 연결성 |
| 기업 임원 채점자 | 비용, 시간, 적용 가능성, 기존 설비 영향, 운영 리스크 |

설정 파일:

```text
rubrics/raters/layered_default.json
```

---

## 5. Fact Anchor Bank

기출 분석 기반 주요 주제별 Fact Anchor를 JSON으로 관리한다.

```text
rubrics/fact_anchors/industrial_instrumentation_control.json
```

예시 주제:

- 제어밸브 캐비테이션
- Cv 밸브 유량계수
- PID 제어
- 전달함수·상태방정식
- 온도센서 열전대·RTD
- 유량계·차압식 유량측정
- 압력·차압전송기
- PLC/DCS 및 Remote I/O
- 산업통신·네트워크·프로토콜
- 방폭·SIL·SIS 안전
- 계측 오차·정확도·정밀도·교정
- 노이즈·접지·서지 대책
- 스마트팩토리·IIoT·디지털트윈
- HMI/SCADA
- 모터·인버터·구동계

Fact Anchor Bank 검증:

```bash
python3 scripts/validate_fact_anchor_bank.py
```

---

## 6. 주요 파일 구조

```text
prof_eng_answer/
├── README.md
├── bot.py
├── gemini_grader.py
├── grading_agents.py
├── grading_config.py
├── rubrics/
│   ├── active_profile.json
│   ├── default.json
│   ├── fact_anchors/
│   │   └── industrial_instrumentation_control.json
│   ├── raters/
│   │   ├── default.json
│   │   └── layered_default.json
│   ├── scoring_model/
│   │   └── default.json
│   └── subjects/
│       └── industrial_instrumentation_control.json
├── scripts/
│   ├── gemini_audit_grading_engine.py
│   ├── validate_config.py
│   └── validate_fact_anchor_bank.py
├── docs/
├── examples/
├── schemas/
├── data/
└── logs/
```

다음 항목은 Git에 커밋하지 않는다.

```text
data/sessions/
data/audits/
logs/
backups/
__pycache__/
*.pyc
*.backup.*
*.broken.*
.env
test_assets/
```

---

## 7. 환경변수

컨테이너는 `~/hermes/.env`를 사용한다.

필수 값:

```env
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-3.1-flash-lite
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=gemma4:e4b
TELEGRAM_TOKEN=...
PROF_ENG_CHAT_ID=...
```

API key와 Telegram token은 절대 커밋하지 않는다.

---

## 8. 실행

봇 재시작:

```bash
cd ~/hermes/workspace/prof_eng_answer

docker exec hermes_agent bash -lc 'pkill -f "python.*bot.py" || true'

docker exec -d hermes_agent bash -lc '
cd /workspace/prof_eng_answer &&
nohup python bot.py >> logs/prof_eng_answer.log 2>&1 &
'
```

로그 확인:

```bash
tail -n 120 logs/prof_eng_answer.log
```

---

## 9. Telegram 사용법

짧은 답안 채점:

```text
/grade
문제: Cv(Valve Flow Coefficient)를 설명하시오.

답안:
Cv는 밸브의 유량계수로 밸브를 통과할 수 있는 유량의 크기를 나타낸다.
```

새 세션 시작:

```text
/new
```

답안지 사진을 올린 뒤 `/grade`를 실행하면 이미지 수와 OCR 텍스트 길이를 함께 고려한다.

---

## 10. 검증

호스트 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 scripts/validate_config.py
python3 scripts/validate_fact_anchor_bank.py
python3 -m py_compile gemini_grader.py grading_config.py grading_agents.py bot.py
```

컨테이너 검증:

```bash
docker exec -it hermes_agent bash -lc '
cd /workspace/prof_eng_answer &&
python -m py_compile gemini_grader.py grading_config.py grading_agents.py bot.py &&
python scripts/validate_config.py &&
python scripts/validate_fact_anchor_bank.py
'
```

---

## 11. 세션 산출물

각 채점 세션은 `data/sessions/`에 저장된다.

주요 산출물:

- `grade.json`
- `volume_evaluation.json`
- `fact_anchor_evaluation.json`
- `connection_evaluation.json`
- `interview_followup.json`
- `rater_weighted_evaluation.json`
- `gemini_semantic_evaluation.json`

세션 파일에는 사용자 답안과 이미지가 포함될 수 있으므로 커밋하지 않는다.

---

## 12. 현재 구현 단계

- phase1: active_profile 및 설정 snapshot
- phase2: A/B/C/D/E layer scoring
- phase3: Fact Anchor scoring
- phase3.1: Fact Anchor 엄격화
- phase4: 교수·기술사·기업 임원 layer 가중 합성
- phase5: 답안지 이미지 수 + OCR 분량 판단
- phase6: Gemini semantic grader 적용
- phase7: Fact Anchor Bank JSON 분리

---

## 13. 남은 개선 과제

- 실제 답안지 사진 3장 + OCR 테스트 확대
- OCR 품질이 낮을 때 Gemini Vision 또는 별도 OCR 보정 검토
- 기출 주제별 Fact Anchor Bank 지속 확장
- Blind Test 세트 구축
- 키워드 나열 답안과 구조화 답안의 점수 차이 검증
- 이의제기/재채점 인터페이스 추가

---

## 14. 보안 주의

다음 값과 파일은 외부 공유 및 커밋 금지이다.

- `.env`
- `GEMINI_API_KEY`
- `TELEGRAM_TOKEN`
- `data/sessions/`
- `logs/`
- `backups/`
- 사용자 답안 이미지
- 사용자 답안 텍스트

---

## Rubric Authoring Workflow

평가 기준과 유형별 모범 답안은 JSON으로 관리한다.

핵심 원칙:

- 문제 유형은 별도 점수 체계가 아니라 C항목 평가 렌즈이다.
- 모범 답안은 정답 문장 매칭용이 아니라 구조·깊이·현장 적용성 기준이다.
- D/E는 모든 문제 유형에서 현장 적용성, 설계 판단, 제언, 독창성을 공통 평가한다.

주요 파일:

```text
rubric_registry.py
question_type_router.py
model_answer_router.py
rubrics/question_types/default.json
rubrics/model_answers/industrial_instrumentation_control.json
docs/rubric_authoring_guide.md
scripts/rubric_manager.py
```

자주 쓰는 명령:

```bash
python3 scripts/rubric_manager.py list-types
python3 scripts/rubric_manager.py list-model-answers
python3 scripts/rubric_manager.py validate-all
```

새 모범 답안 후보 생성:

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

후보 편집 후 승격:

```bash
vim rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py promote-model-answer \
  --candidate rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py validate-all
```

현재 구현 단계:

```text
phase8  : 독창성·기술사적 판단성 평가
phase8b : 독창성 반영 후 최종 volume cap 강제
phase9  : question_type을 C항목 평가 렌즈로 적용
phase10 : model answer bank를 기준 답안으로 참조
phase11 : B/C 명칭을 문제 요구·유형별 Fact 설명으로 정리
phase12 : D/E 표현을 현장 적용·설계 판단·제언 중심으로 정리
phase13 : rubric_registry와 rubric_manager로 기준 작성 workflow 정리
```

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
