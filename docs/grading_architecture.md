# Grading Architecture

이 문서는 현재 `prof_eng_answer` 채점 pipeline을 설명한다. 세부 provider 설정은 `llm_provider.md`, Difficulty와 ceiling은 `difficulty_and_selection_strategy.md`, Question Type은 `question_type_taxonomy.md`를 우선한다.

## 1. 현재 채점 철학

기술사 답안은 단순 키워드 포함 여부가 아니라 다음을 함께 평가한다.

- 문제 요구를 정확히 잡는가
- 핵심 Fact를 정확하고 간결하게 설명하는가
- 답안이 문제 요구축에서 벗어나지 않는가
- 현장 적용 조건, 리스크, 비용, 유지보수성을 판단하는가
- 결론과 제언이 fact에서 논리적으로 도출되는가
- 면접에서 근거를 방어할 수 있는가

## 2. Runtime 흐름

```text
Telegram /grade
→ bot.py::handle_text()
→ bot.py::grade_answer()
→ grading_agents.run_agent_pipeline()
→ session input/prompt/raw/grade 저장
→ semantic grader 적용
→ A/B/C/D/E layer 점수 재산정
→ Fact Anchor 평가
→ Model Answer Bank 참조
→ Originality/connection/volume 평가
→ Question Type coverage attach
→ Difficulty strategy attach
→ Difficulty ceiling 평가
→ bot.py::format_result()
→ bot.py::send_message()
```

`run_agent_pipeline()`은 legacy 1차 분석 결과가 약하더라도 phase2 후처리 결과로 grade를 교체할 수 있다. 따라서 최종 사용자 출력은 `grade.json`의 최종 phase2 결과와 `bot.py::format_result()` 기준으로 본다.

## 3. A/B/C/D/E 25점 구조

| 항목 | 배점 | 평가 내용 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용·설계 판단·제언 |
| E | 2 | 연결성·면접 방어 가능성 |
| 합계 | 25 | 전체 답안 점수 |

| 기준선 | 점수 |
|---|---:|
| 공식 합격선 | 15 |
| 실전 목표선 | 17.5 |
| 고득점 기준 | 20 |

## 4. 3인 layer 평가

| 채점자 | 중점 |
|---|---|
| 교수 채점자 | 원리, 개념 정확성, 체계성, 이론적 설명 |
| 기술사 채점자 | 현장 절차, 적용 조건, 리스크, 검증 기준 |
| 기업 임원 채점자 | 비용, 유지보수성, 기존 설비 영향, 실현 가능성 |

A/B/C/D/E 항목별로 3인 layer 가중치가 다르다. Telegram 출력에서는 3인 단순 평균과 layer 가중 점수를 보여준다. Difficulty ceiling이 적용된 경우 가중 점수는 ceiling 적용 전 점수이며, 최종 점수는 별도로 표시한다.

## 5. Semantic grader와 Python rule의 역할

| 구분 | 역할 |
|---|---|
| Gemini/CLOVA semantic grader | 의미, 논리, 누락 요소, 기술사적 깊이 평가 |
| Ollama 보조 모델 | 1차 분석과 보조 코멘트 생성 |
| Python rule | 점수 cap, fallback, coverage, ceiling, 출력 정합성 보정 |
| Fact Anchor | topic별 핵심 fact 충족 여부 평가 |
| Model Answer Bank | 모범 답안 구조와 고득점/저득점 패턴 참조 |
| Question Type v2 | C/D 항목의 유형별 요구 lens |
| Difficulty Profile | 고득점 가능성과 ceiling 후보 |

LLM 응답이 malformed JSON을 반환할 수 있으므로, 파서는 code fence, 일부 괄호 누락, LaTeX backslash 등 흔한 오류를 복구하려고 시도한다. 복구가 실패해도 phase2 semantic/Python scoring이 최종 결과를 보강한다.

## 6. Fact Anchor 평가

Fact Anchor는 topic별 핵심 fact 기준이다. 일반적으로 한 문제에 핵심 anchor 5개를 선택한다.

평가 관점:

- 핵심 개념 인지
- 정확한 설명
- 문제 요구와 연결
- 간결성
- 현장 의미 또는 한계

Fact Anchor는 Model Answer보다 더 기초적인 factual 기준이며, 같은 topic의 여러 Model Answer가 공유할 수 있다.

## 7. Model Answer Bank 역할

Model Answer Bank는 정답 문장 매칭용이 아니다.

역할:

- 답안 전개 구조 제공
- 고득점 요소 제공
- 저득점 패턴 제공
- 현장 적용 포인트 제공
- semantic grader와 Python rule 판단 보강

같은 `topic_id`에 여러 `question_type` Model Answer가 존재할 수 있다.

## 8. Question Type coverage

Question Type coverage는 다음을 확인한다.

- 해당 유형의 sub criteria 충족 여부
- C항목 fact focus 누락 여부
- D항목 field judgement focus 누락 여부
- Telegram 출력용 보완 문구
- coverage 보정 후보

기본 운영은 `warn`으로 두며, 이 경우 점수를 직접 변경하지 않고 보정 후보만 출력한다.

## 9. Difficulty ceiling

Difficulty Profile은 점수를 대체하지 않는다. 다만 `DIFFICULTY_CEILING_MODE=strict`이면 recommended cap이 실제 점수에 적용될 수 있다.

예: `THEORY_CORE`에서 핵심 수식·변수 관계·응답 해석에 fatal error가 감지되면 10점 cap 후보가 적용될 수 있다. 이 경우 사용자 출력에는 다음이 구분되어야 한다.

- ceiling 적용 전 단순 평균
- ceiling 적용 전 가중 점수
- ceiling 적용 후 최종 점수
- cap 사유
- 구체적 이론 오류 또는 보완 방향

## 10. 답안 분량 cap

25점 문항은 기술사 답안지 기준 충분한 전개량을 요구한다.

대표 cap:

| 상태 | 의미 |
|---|---|
| 매우 짧은 텍스트 | 요약 답안으로 보고 낮은 상한 적용 |
| 1쪽 수준 | 부분 답안 상한 적용 |
| 2쪽 수준 | 기본 전개는 있으나 고득점 제한 |
| 약 3쪽 수준 | 구조와 내용이 좋으면 고득점 가능 |

분량 cap은 자동 고득점/자동 감점이 아니라, A/B/C/D/E 전개 가능성을 제한하는 보정이다.

## 11. 관련 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram command, display formatter, send boundary cleanup |
| `grading_agents.py` | 채점 pipeline 중심 |
| `gemini_grader.py` | Gemini semantic grader |
| `clova_grader.py` | CLOVA semantic grader |
| `originality_grader.py` | 독창성·기술사적 판단성 평가 |
| `model_answer_router.py` | Model Answer Bank 참조 |
| `difficulty_strategy.py` | Difficulty Profile 분류 |
| `difficulty_output_adapter.py` | difficulty 설명 attach |
| `difficulty_score_ceiling.py` | ceiling 후보 계산과 strict 적용 |
| `question_type_taxonomy.py` | Question Type v2 taxonomy |
| `question_type_coverage_adapter.py` | coverage 출력 보강 |
| `question_type_coverage_score_adjuster.py` | coverage 보정 후보 |
| `semantic_question_type_prompt.py` | semantic grader prompt contract |
| `semantic_question_type_postprocess.py` | coverage fallback/postprocess |
