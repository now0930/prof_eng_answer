# 적용 순서

## 1단계: 파일 추가

현재 코드를 바로 덮어쓰지 말고 아래 파일을 추가한다.

- rubrics/scoring_model/default.json
- rubrics/subjects/industrial_instrumentation_control.json
- rubrics/raters/default.json

기존 rubrics/default.json은 당분간 호환용으로 유지한다.

## 2단계: grading_agents.py 정리

grading_agents.py는 아래 책임으로 분리한다.

1. Config Loader
2. Model Assistant
3. Scoring Engine
4. Result Builder

채점 철학과 배점은 코드에 하드코딩하지 말고 scoring_model/default.json에서 읽는다.

## 3단계: 세션 산출물 추가

각 채점 세션에 다음 파일을 저장한다.

- scoring_model_snapshot.json
- subject_rubric_snapshot.json
- rater_snapshot.json
- answer_structure.json
- fact_anchor_evaluation.json
- connection_evaluation.json
- interview_followup.json
- grade.json

## 4단계: Telegram 출력 변경

단순 항목 점수 대신 아래를 표시한다.

- 단계별 점수
- fact anchor 충족도
- 연결성 평가
- 상한 규칙 적용 여부
- 면접 재검증 질문

## 5단계: 데이터 기반 보정

사용자가 추후 제공하는 실제 채점 데이터로 아래 값을 보정한다.

- A/B/C/D/E 배점
- fact-only 상한
- D/E cap 규칙
- 항목별 채점자 가중치
- fact anchor 평가 스케일
