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
