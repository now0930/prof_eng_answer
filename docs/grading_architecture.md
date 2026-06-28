# 채점 구조

이 문서는 산업계측제어기술사 답안 채점 구조를 설명한다.

기본 채점 체계는 A/B/C/D/E 25점 구조이다.  
난이도, 문제유형, 모범답안, LLM semantic grader는 이 구조를 대체하지 않고 보조한다.

---

## 1. 기본 점수 구조

| 항목 | 배점 | 의미 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용, 설계 판단, 제언 |
| E | 2 | 연결성, 면접 방어 가능성 |

총점은 25점이다.

---

## 2. 평가 핵심

채점은 다음을 본다.

- 문제 의도 파악
- 기술사가 알아야 할 fact 기반 설명
- 문제점, 리스크, 적용상 쟁점 진단
- 해결책, 설계안, 대책 또는 제언
- 본인 판단, 현장 노하우, 적용 조건, trade-off
- 배경에서 제언까지의 연결성

---

## 3. Question Type Lens

문제 유형은 별도 채점 agent가 아니다.  
기존 A/B/C/D/E 구조를 유지하면서 C항목의 Fact 설명 방식을 보정하는 lens로 사용한다.

| Type | 의미 |
|---|---|
| `DEFINE` | 정의·개념 설명형 |
| `PRINCIPLE` | 원리·메커니즘형 |
| `STRUCTURE` | 구성·분류형 |
| `COMPARE` | 비교·선정형 |
| `PROBLEM_SOLVE` | 문제점·개선방안형 |
| `CAUSE_ACTION` | 원인·대책형 |
| `PROCEDURE` | 절차·방법론형 |
| `CALC_DESIGN` | 계산·설계형 |
| `APPLICATION` | 사례·적용형 |
| `EVALUATION` | 평가·효과 분석형 |

---

## 4. Model Answer Bank

모범 답안은 문장 매칭용 정답지가 아니다.

사용 목적:

- 답안 구조 기준
- 설명 깊이 기준
- 현장 적용성 기준
- 보완 피드백 기준

사용하지 않는 방식:

- 문장 그대로 매칭
- 모범 답안과 다르면 감점
- 키워드 개수만으로 점수 산정

---

## 5. 현재 Pipeline 순서

현재 주요 채점 pipeline은 다음 순서를 따른다.

```text
1. 기본 채점자별 분석
2. Gemini 또는 CLOVA semantic grader 적용
3. phase2 layered scoring 적용
4. phase20 difficulty strategy 출력
5. phase21 difficulty ceiling 적용
```

정상 로그 예:

```text
[agent] phase2 layered scoring applied: ...
[agent] phase20 final difficulty strategy applied: ...
[agent] phase21 final difficulty ceiling evaluated: ...
```

중요 순서:

```text
phase2 -> phase20 -> phase21
```

이 순서가 중요한 이유는 phase21이 최종 점수를 기준으로 ceiling을 적용하기 때문이다.  
phase21이 phase2보다 먼저 실행되면 phase2가 점수를 다시 덮어쓸 수 있다.

---

## 6. Phase 역할

| Phase | 역할 |
|---|---|
| phase2 | layered scoring으로 최종 점수 계산 |
| phase20 | 난이도 Profile, 선택 중요도, 고득점 조건 설명 |
| phase21 | 난이도별 ceiling 또는 THEORY_CORE unlock 조건 적용 |

phase20은 설명 layer이다.  
phase21은 `DIFFICULTY_CEILING_MODE=strict`일 때 실제 점수를 제한할 수 있다.

---

## 7. Fallback 채점

로그에 다음이 나올 수 있다.

```text
모델 분석 JSON 파싱에 실패하여 fallback 채점을 적용합니다.
```

이는 초기 로컬 모델 분석 단계에서 JSON 파싱이 실패했다는 의미이다.  
이후 Gemini 또는 CLOVA semantic grader가 정상 적용되면 전체 채점은 계속 진행된다.

fallback 로그는 곧바로 전체 채점 실패를 의미하지 않는다.

---

## 8. Session 산출물

채점 결과는 session 디렉터리에 저장된다.

```text
data/sessions/<session_id>/
```

주요 산출물 예:

```text
gemini_semantic_evaluation.json
active_profile.json
scoring_model.json
subject_rubric.json
layered_rater.json
```

파일명에 `gemini`가 남아 있어도 내부 `llm_provider` 값으로 실제 provider를 판단한다.
