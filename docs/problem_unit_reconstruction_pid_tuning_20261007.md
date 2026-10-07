# PID 튜닝 Topic Pack 문제 단위·coverage 재검토

검토일: 2026-10-07
대상: `pid_controller_tuning_sequence_gain_effects`
유형: coverage 전수검토 후보 — 구조 원자성 경고 대상은 아님
상태: 문서 및 source Pack 구조 보완; 사람 기술 검토 전

## 대표 Problem Unit

> **PID 제어기의 P/I/D 동작이 폐루프 응답특성에 미치는 영향과 일반적인 현장 튜닝 순서,
> 적용상 주의사항을 설명하시오.**

이 질문은 기존 기술지식으로 구성한 예상문제다. 과거 기출이나 공식 출제분류라는 증거는
확인하지 않았다.

## 발견한 문제

- 10개 Anchor 중 기존 expected patterns의 필수 Anchor union은 6개(60%)만 참조했다.
- 7개 답안 outline 모두 `anchor_refs`가 비어 있어 outline과 fact bank 연결을 확인할 수
  없었다.
- 대표 문제는 tuning/gain 영향인데, 고득점 항목에 PD 존재 설명이 포함되어 있었고,
  개별 질문 패턴은 PD/PI 비교를 요구하지 않았다. 이는 요구 밖의 내용을 보너스 기준처럼
  보이게 할 수 있다.
- `pid_s_domain_formula`, PI의 일반성, PD 적용 가능성은 유용한 배경지식이지만 대표 문제의
  모든 변형에 필수는 아니다.

## 조정 결과

| 영역 | 처리 |
|---|---|
| 대표 문제 필수 지식 | 정의, 시간영역 기본식, P/I/D 응답 효과, 일반 튜닝 순서 |
| 현장·튜닝 패턴 | 위 backbone에 `field_constraints` 추가 |
| 선택적 표현/배경 | s-domain 등가식, PI 일반성, PD 적용 fact를 `optional`로 분류 |
| 오개념 처리 | “PD 제어기는 존재하지 않는다”처럼 명시적 오류는 false-claim guard로 유지. PD를 정답에 자발적으로 추가하지 않았다는 이유로 감점하지 않음 |
| 답안 outline | 7개 section에 관련 Anchor refs를 채워 요구→지식 추적을 명시 |
| 범위 외 점수화 | PD 존재를 고득점 필수 항목 및 common-missing penalty에서 제거 |
| 문항 표현 추적 | 네 expected pattern에 의도를 추가하고 같은 순서의 `question_examples`와 정합 |

시간영역 기본식을 중심 pattern #1의 필수 Anchor에 추가해 자동 참조율은 60%에서 70%가
되었다. 남은 미참조 Anchor는 누락으로 간주하지 않고, 문제 요구상 선택 배경이라고
문서화했다. 이를 위해 unrelated facts를 모든 pattern에 억지로 추가하지 않았다.

## 보호한 경계

- Fatal wrong-claim schema, A/B/C/D/E scoring contract, deterministic scoring, Question Type,
  router aliases/authority와 release gates는 수정하지 않았다.
- expected question 문장과 점수 가중치를 바꾸지 않았다.
- 본 변경은 source content/view를 정리한 것이므로 generated output은 release 검증 뒤
  snapshot으로 복원됐다. Runtime promotion은 하지 않았다.

## 한계와 후속 검증

- PID equation과 qualitative effects는 기존 source pack에 이미 있었으나, 이 턴에 외부
  handbook 판본/페이지 대조는 하지 않았다.
- 70%는 자동 pattern-to-anchor union 지표이지 문제 답안 충족률의 증명은 아니다.
- 전체 release `--all`은 다른 managed drafts의 사람 승인 부재 때문에 통과할 수 없다.
- 다음 inventory 작업은 `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`다.
