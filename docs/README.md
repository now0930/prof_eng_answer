# Docs Index

이 문서: `README.md`

이 디렉터리는 `prof_eng_answer`의 운영, 채점 구조, question type, difficulty, rubric 관련 문서를 정리한다.

현재 운영 기준은 다음과 같다.

| 항목 | 기준 |
|---|---|
| Telegram Bot 실행 주체 | `prof_eng_answer_bot` |
| Compose 위치 | `~/hermes/docker-compose.yml` |
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 nohup 실행 | 사용하지 않음 |
| LLM 기본 모드 | `auto` |
| Question Type coverage | `warn` 기본 |
| Difficulty ceiling | `warn` 기본 |

## 1. 핵심 문서

| 문서 | 목적 |
|---|---|
| `operation_runbook.md` | 운영 점검, 재시작, 장애 대응 |
| `docker_compose_usage.md` | Docker Compose 운영 방식 |
| `grading_architecture.md` | A/B/C/D/E 25점 채점 구조와 pipeline |
| `question_type_taxonomy.md` | Question Type v2 taxonomy, sub criteria, coverage |
| `difficulty_and_selection_strategy.md` | Difficulty Profile, ceiling, 문항 선택 전략 |
| `llm_provider.md` | Gemini, CLOVA provider 설정 |
| `rubric_authoring_guide.md` | Rubric, Fact Anchor, Model Answer 추가·수정·삭제 절차 |
| `model_answer_generator_prompt.md` | 키워드 기반 Model Answer Bank 초안 생성 LLM 프롬프트 |

## 2. 보조 문서

| 문서 | 성격 |
|---|---|
| `migration_plan.md` | 구조 변경 및 migration 기록 |
| `structure_review.md` | 과거 구조 검토 문서. 현재 기준과 다를 수 있음 |

## 3. 가장 먼저 볼 문서

운영 중 문제가 생기면 다음 순서로 확인한다.

    operation_runbook.md
    docker_compose_usage.md
    grading_architecture.md

## 4. 현재 채점 구조 요약

채점 구조는 다음 흐름을 따른다.

    Telegram /grade 입력
    문제와 답안 파싱
    Gemini 또는 CLOVA semantic grader 실행
    Python rule 기반 A/B/C/D/E 점수 후처리
    Question Type v2 coverage attach
    Difficulty Profile attach
    Telegram formatter 구성
    send_message boundary cleanup

## 5. Question Type v2 요약

현재 question type은 4개 lens로 정리한다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 |
| `DIAGNOSIS_ACTION` | 진단·대책형 |
| `COMPARE_SELECTION` | 비교·선정형 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 |

`DEFINE`은 독립 유형으로 사용하지 않고, legacy mapping을 통해 v2 유형으로 흡수한다.

## 6. Difficulty Profile 요약

| Profile | 의미 |
|---|---|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 |

Difficulty Profile은 A/B/C/D/E 점수를 대체하지 않는다.  
고득점 가능성, ceiling 후보, 문항 선택 전략을 설명하는 보조 lens이다.

## 7. 운영상 중요한 주의

`bot.py`는 운영 시 다음 방식으로 실행된다.

    python -u bot.py

파일 내부에서는 다음 흐름으로 진입한다.

    if __name__ == "__main__":
        main()

`main()` 내부에는 polling loop가 있으므로, 이 코드 아래쪽에 append한 wrapper는 실행되지 않는다.

따라서 최종 Telegram 출력 정리는 `send_message()` boundary에서 처리해야 한다.

## 8. 대표 smoke test

Telegram에서 다음을 보낸다.

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

정상 확인 기준:

- 채점 완료 메시지가 온다.
- `[Question Type Coverage]`가 출력된다.
- 문제 유형 lens가 `적용·평가형(IMPLEMENTATION_EVALUATION)`로 표시된다.
- `C항목 보완: 일반 설명형 유형에서는 ...` 문구가 없어야 한다.
- `C항목 보완: 문제 유형 lens에 맞는 핵심 fact...` 문구가 나와야 한다.

## 9. 문서 정합성 확인

README가 참조하는 docs 파일이 실제 존재하는지 확인한다.

    cd ~/hermes/workspace/prof_eng_answer

    echo "[README referenced docs]"
    grep -oE 'docs/[A-Za-z0-9_./-]+\.md' README.md | sort -u

    echo
    echo "[missing referenced docs]"
    for f in $(grep -oE 'docs/[A-Za-z0-9_./-]+\.md' README.md | sort -u); do
      [ -f "$f" ] || echo "MISSING: $f"
    done

docs README가 docs 디렉터리의 모든 문서를 설명하는지도 확인한다.

    echo
    echo "[docs files not mentioned in docs/README.md]"
    for f in $(find docs -maxdepth 1 -type f -name '*.md' -printf '%f\n' | sort); do
      grep -q "\`$f\`" docs/README.md || echo "MISSING_IN_DOCS_README: $f"
    done

정상 기준:

    MISSING 출력 없음
    MISSING_IN_DOCS_README 출력 없음
