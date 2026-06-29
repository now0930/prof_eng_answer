# Grading Architecture

## 1. 목적

이 문서는 `prof_eng_answer`의 현재 채점 구조를 설명한다.

현재 채점은 단순 키워드 매칭이 아니라 다음 요소를 결합한다.

- A/B/C/D/E 25점 구조
- 교수·기술사·기업 임원 3인 layer 평가
- Gemini 또는 Naver CLOVA semantic grader
- Python rule 기반 점수 후처리
- Fact Anchor 및 Model Answer Bank 참조
- Question Type v2 coverage
- Difficulty Profile 및 ceiling 후보
- Telegram 최종 출력 정리

## 2. 기본 채점 철학

기술사 답안은 다음 흐름을 갖춰야 한다.

1. 문제 배경을 제시한다.
2. 문제 요구를 정확히 해석한다.
3. 핵심 Fact를 기술적으로 설명한다.
4. 현장 적용 조건, 리스크, 개선방안을 제시한다.
5. 결론과 판단 근거가 연결되어 면접 방어가 가능해야 한다.

핵심 평가 철학은 다음과 같다.

| 평가축 | 의미 |
|---|---|
| 문제 의도 파악 | 문제에서 요구한 대상과 범위를 정확히 잡는가 |
| Fact 기반 설명 | 기술사 수준의 핵심 개념, 구조, 원리, 절차를 설명하는가 |
| 문제점·리스크 진단 | 현장 적용 시 발생 가능한 문제를 설명하는가 |
| 대책·판단 제시 | 개선방안, 설계 판단, 운영 제언을 제시하는가 |
| 면접 방어 가능성 | 답안의 논리와 근거가 질문에 방어 가능한가 |

## 3. A/B/C/D/E 25점 구조

| 항목 | 배점 | 평가 내용 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용·설계 판단·제언 |
| E | 2 | 연결성·면접 방어 가능성 |
| 합계 | 25 | 전체 답안 점수 |

기준선은 다음과 같다.

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15점 |
| 실전 목표선 | 17.5점 |
| 고득점 기준 | 20점 |

## 4. A항목: 배경과 문제 진입

A항목은 답안이 문제 배경에서 자연스럽게 시작하는지 평가한다.

좋은 답안은 다음을 포함한다.

- 왜 이 기술이나 장치가 필요한지
- 산업계측제어 관점에서 어떤 의미가 있는지
- 문제 요구로 들어가기 위한 배경 설명
- 단순 정의가 아니라 현장 문제와 연결되는 도입

나쁜 답안은 바로 정의만 쓰거나, 문제와 무관한 일반론으로 시작한다.

## 5. B항목: 문제 요구 파악

B항목은 문제에서 묻는 핵심 요구를 정확히 잡았는지 평가한다.

예를 들어 다음 문제를 보자.

    차압전송기의 교정회로와 교정절차를 설명하시오.

이 문제는 단순히 차압전송기의 정의를 묻는 문제가 아니다.

핵심 요구는 다음이다.

- 교정회로 구성
- 교정에 필요한 장비
- zero/span 조정
- 단계별 교정 절차
- 교정 후 판정과 검증
- 현장 설치 조건에 따른 오차 보정

따라서 “기준 압력을 인가하고 4~20mA를 확인한다” 정도로만 쓰면 B항목은 낮게 평가된다.

## 6. C항목: 유형별 Fact 기반 내용 설명

C항목은 기술사 답안의 핵심이다.

평가 대상은 다음과 같다.

- 핵심 개념
- 구조와 구성요소
- 동작 원리
- 절차와 방법
- 수식과 변수
- 적용 범위와 한계
- 문제 요구와 Fact의 연결성

C항목은 Question Type v2 lens의 영향을 받는다.

예를 들어 적용·평가형 문제에서는 다음 Fact가 중요하다.

- 적용 대상
- 시스템 구성
- 절차·방법
- 선정 기준
- 평가 지표

원리·해석형 문제에서는 다음 Fact가 중요하다.

- 원리와 메커니즘
- 수식과 변수
- 계산 또는 해석 과정
- 결과 의미

## 7. D항목: 현장 적용·설계 판단·제언

D항목은 기술사 답안과 일반 기사식 답안을 가르는 핵심이다.

좋은 답안은 다음을 포함한다.

- 현장 적용 조건
- 기존 설비와의 연계
- 비용과 실현 가능성
- 유지보수성
- 운전 리스크
- 검증 방법
- 개선 효과와 한계
- 우선순위와 trade-off

단순히 “개선해야 한다”, “주의해야 한다”라고 쓰는 것은 부족하다.

## 8. E항목: 연결성·면접 방어 가능성

E항목은 답안이 하나의 논리 흐름으로 연결되는지 평가한다.

좋은 흐름은 다음과 같다.

    배경
    문제 요구
    Fact 설명
    현장 적용 판단
    결론

면접 방어 가능성이 낮은 답안은 다음 특징을 가진다.

- 용어만 나열함
- 설명 간 연결이 없음
- 왜 그런지 근거가 없음
- 현장 조건 질문에 답하기 어려움
- 결론이 문제 요구와 연결되지 않음

## 9. 3인 layer 평가

Bot은 하나의 답안을 세 관점으로 나누어 평가한 뒤 layer별 가중 합성을 수행한다.

| 관점 | 중점 |
|---|---|
| 교수 채점자 | 원리, 개념 정확성, 체계성, 이론적 설명 |
| 기술사 채점자 | 현장 절차, 적용 조건, 리스크, 검증 기준 |
| 기업 임원 채점자 | 비용, 유지보수성, 기존 설비 영향, 실현 가능성 |

Telegram 출력에는 3인 단순 평균과 최종 가중 점수가 함께 표시된다.

## 10. 채점 pipeline

현재 채점 흐름은 다음과 같다.

    1. Telegram /grade 입력
    2. 문제·답안 파싱
    3. provider 선택: auto / gemini / clova
    4. Gemini 또는 CLOVA semantic grader 실행
    5. Python rule 기반 A/B/C/D/E 점수 후처리
    6. Fact Anchor 및 Model Answer Bank 기반 보강
    7. Question Type v2 coverage attach
    8. Difficulty Profile attach
    9. Telegram formatter 구성
    10. send_message boundary cleanup

## 11. Semantic grader와 Python rule의 역할

| 구분 | 역할 |
|---|---|
| Semantic grader | 답안 의미, 논리, 누락 요소, 기술사적 깊이 평가 |
| Python rule | 점수 cap, fallback, coverage 보정 후보, 출력 정규화 |
| Fact Anchor | 핵심 개념 포함 여부와 정확성 보조 평가 |
| Model Answer Bank | 대표 문항의 모범 구조와 비교 기준 제공 |

LLM 의미 평가만으로 점수를 확정하지 않고, Python rule을 통해 운영상 안정성을 보강한다.

## 12. Question Type v2

Question Type v2는 별도 점수 체계가 아니다.

C항목 Fact 설명과 D항목 현장 판단을 보완하는 lens이다.

현재 대분류는 다음 4개이다.

| question_type | 한국어명 | 의미 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 동작, 수식, 계산, 결과 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제, 원인, 영향, 대책, 검증 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교축, 장단점, 적용 조건, 선정 판단 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 대상, 구성, 절차, 평가 지표, 운영 개선 |

기존 `DEFINE`, `PRINCIPLE`, `COMPARE`, `PROCEDURE` 같은 legacy 유형은 내부 호환을 위해 v2로 mapping한다.

## 13. Question Type coverage

Semantic grader는 가능하면 `question_type_coverage`를 반환한다.

Telegram 출력 예시는 다음과 같다.

    [Question Type Coverage]
    - 문제 유형 lens: 적용·평가형(IMPLEMENTATION_EVALUATION)
    - 세부 요구 충족도: poor
    - C항목 보완 필요: 시스템 구성, 절차·방법, 평가 지표
    - D항목 보완 필요: 운영 리스크, 유지보수성, 적용 후 검증 방법
    - coverage 보정 후보: -0.75점, mode=warn

기본 모드는 다음과 같다.

    QUESTION_TYPE_COVERAGE_SCORE_MODE=warn

| 모드 | 의미 |
|---|---|
| `warn` | 점수 변경 없이 보정 후보만 표시 |
| `strict` | 약한 보정을 실제 점수에 적용 |
| `off` | coverage 보정 비활성 |

fallback 또는 unknown coverage는 점수 보정에 사용하지 않는다.

## 14. Difficulty Profile

Difficulty Profile은 점수를 대체하지 않는다.

답안의 고득점 가능성, 문항 선택 전략, ceiling 후보를 설명하는 보조 lens이다.

| Profile | 의미 | 기본 ceiling |
|---|---|---:|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 | 15.00 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 | 15.75 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 | 16.50 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 | 17.50 |

기본 모드는 다음과 같다.

    DIFFICULTY_CEILING_MODE=warn

`warn` 모드는 점수를 바꾸지 않고 ceiling 후보만 표시한다.

## 15. 짧은 답안 cap

답안이 1~5줄 또는 500자 미만인 경우 요약 답안 상한을 적용할 수 있다.

이는 기술사 시험에서 요구하는 배경, Fact, 현장 판단, 결론 구조를 충분히 전개하지 못한 답안을 제한하기 위한 장치이다.

Telegram 출력 예시:

    답안 이미지 없이 텍스트가 1~5줄 또는 500자 미만이므로 요약 답안 상한을 적용한다.

## 16. 대표 짧은 답안 해석

예시 문제:

    차압전송기의 교정회로와 교정절차를 설명하시오.

예시 답안:

    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

이 답안은 핵심 용어는 일부 포함하지만 다음이 부족하다.

- 교정회로 구성
- 표준 압력 발생기, 전류계, HART communicator 연결
- 5점 교정 절차
- zero/span 조정 순서
- 선형성, 히스테리시스 확인
- 현장 오차 요인
- 교정 후 판정 기준
- 기록 관리와 유지보수성

따라서 낮은 점수대가 자연스럽다.

## 17. 출력 정리 원칙

`bot.py`는 운영 시 다음 방식으로 실행된다.

    python -u bot.py

실행 흐름은 다음과 같다.

    if __name__ == "__main__":
        main()

`main()` 내부에는 `while True` polling loop가 있으므로, 이 코드 아래에 append한 wrapper는 실행되지 않는다.

따라서 Telegram 최종 출력 정리는 반드시 `send_message()` 경계 또는 그보다 앞쪽에서 처리해야 한다.

현재 legacy `GENERAL(일반 설명형)` 문구 정리는 `send_message()` 내부의 send boundary cleanup에서 처리한다.

## 18. 운영 검증 포인트

대표 smoke test:

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

정상 출력 기준:

- `[Question Type Coverage]`가 표시된다.
- 문제 유형 lens가 `적용·평가형(IMPLEMENTATION_EVALUATION)`로 표시된다.
- `C항목 보완: 일반 설명형 유형에서는 ...` 문구가 나오지 않는다.
- `C항목 보완: 문제 유형 lens에 맞는 핵심 fact...` 문구가 나온다.

## 19. 관련 파일

| 파일 | 역할 |
|---|---|
| `grading_agents.py` | 채점 pipeline 중심 |
| `gemini_grader.py` | Gemini semantic grader |
| `clova_grader.py` | CLOVA semantic grader |
| `difficulty_output_adapter.py` | Difficulty 설명 attach |
| `difficulty_score_ceiling.py` | ceiling 후보 및 strict 적용 |
| `question_type_taxonomy.py` | Question Type v2 taxonomy |
| `question_type_coverage_adapter.py` | coverage 출력 보강 |
| `question_type_coverage_score_adjuster.py` | coverage 점수 보정 후보 |
| `semantic_question_type_prompt.py` | semantic grader prompt contract |
| `semantic_question_type_postprocess.py` | fallback/postprocess |
| `bot.py` | Telegram formatter와 send boundary cleanup |
