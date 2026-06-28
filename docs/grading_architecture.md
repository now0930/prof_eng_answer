# 채점 구조: A/B/C/D/E Architecture

이 문서는 산업계측제어기술사 답안 채점 구조를 설명한다.

README는 프로젝트 개요와 실행 방법만 제공하고, 채점 구조 상세 설명은 이 문서에서 관리한다.

## 1. 기본 채점 구조

25점 문항은 다음 5개 항목으로 평가한다.

| 항목 | 설명 | 배점 |
|---|---|---:|
| A | 배경과 문제 진입 | 4 |
| B | 문제 요구 파악 | 5 |
| C | 유형별 Fact 기반 내용 설명 | 8 |
| D | 현장 적용·설계 판단·제언 | 6 |
| E | 연결성·면접 방어 가능성 | 2 |
| 합계 |  | 25 |

핵심 원칙은 다음과 같다.

- 문제 유형은 별도 점수 체계가 아니라 C항목 평가 렌즈로 사용한다.
- Fact Anchor Bank는 주제별 핵심 Fact를 확인하는 기준이다.
- Model Answer Bank는 동일 문장 매칭용이 아니라 구조, 깊이, 현장 적용성 기준으로 사용한다.
- D/E는 모든 문제 유형에서 현장 적용성, 설계 판단, 제언, 독창성을 공통 평가한다.
- LLM semantic grader는 의미 평가를 수행한다.
- Python rule은 volume cap, 3인 layer 가중치, originality gate, fallback, 출력 후처리를 관리한다.

## 2. 문제 유형 Lens

문제 유형은 다음 10개를 사용한다.

| 유형 | 설명 |
|---|---|
| DEFINE | 정의·개념 설명형 |
| PRINCIPLE | 원리·메커니즘형 |
| STRUCTURE | 구성·분류형 |
| COMPARE | 비교·선정형 |
| PROBLEM_SOLVE | 문제점·개선방안형 |
| CAUSE_ACTION | 원인·대책형 |
| PROCEDURE | 절차·방법론형 |
| CALC_DESIGN | 계산·설계형 |
| APPLICATION | 사례·적용형 |
| EVALUATION | 평가·효과 분석형 |

이 유형들은 별도 agent가 아니라 `C. 유형별 Fact 기반 내용 설명`의 평가 방식만 결정한다.

## 3. 주요 평가 구성요소

| 구성요소 | 역할 |
|---|---|
| Fact Anchor Bank | 주제별로 반드시 들어가야 할 핵심 Fact 확인 |
| Question Type Lens | 문제 유형에 따라 C항목의 Fact 전개 방식 결정 |
| Model Answer Bank | 주제 + 문제유형별 기준 답안 참조 |
| Originality | 현장 조건, 대안 비교, 적용 우선순위, 검증 기준 평가 |
| Volume Cap | 답안 분량이 지나치게 짧을 경우 최종 점수 상한 적용 |
| 3인 Layer Weighting | 교수, 기술사, 기업 임원 관점의 layer별 가중 합성 |

## 4. 현재 주요 Phase

| Phase | 내용 |
|---|---|
| phase8 | 독창성·기술사적 판단성 평가 |
| phase8b | 독창성 반영 후 최종 volume cap 강제 |
| phase9 | question_type을 C항목 평가 렌즈로 적용 |
| phase10 | model answer bank를 기준 답안으로 참조 |
| phase11 | B/C 명칭을 문제 요구·유형별 Fact 설명으로 정리 |
| phase12 | D/E 표현을 현장 적용·설계 판단·제언 중심으로 정리 |
| phase13 | rubric_registry와 rubric_manager로 기준 작성 workflow 정리 |
| phase14 | Telegram 보완 방향 중복 제거 |
| phase15 | 내부 metric dict 숨김 |
| phase16 | 최종 사용자 문구 polish |
| phase17 | 잔여 표현 정리 |
| phase18 | Gemini 503/timeout retry wrapper |
| phase19 | Gemini + CLOVA provider 선택 구조 |

## 5. 산출물

각 채점 세션은 `data/sessions/`에 저장된다.

주요 산출물은 다음과 같다.

- `grade.json`
- `volume_evaluation.json`
- `fact_anchor_evaluation.json`
- `connection_evaluation.json`
- `interview_followup.json`
- `rater_weighted_evaluation.json`
- `gemini_semantic_evaluation.json`

주의: 기존 호환성 때문에 semantic evaluation 파일명은 `gemini_semantic_evaluation.json`으로 남아 있을 수 있다. 실제 provider는 파일 내부의 `llm_provider` 값을 확인한다.
