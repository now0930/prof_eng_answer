# 광학·레이저 비접촉 측정 Topic Pack 문제 단위 감사

갱신: 2026-10-07
대상: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`
판정: 잠정 유지 후보의 내부 문제 단위 정합성 보완. 공식 시험분류나 기출 문항으로 승인된 것으로 보지 않는다.

## 감사 결과와 변경

- 기존 Topic Sheet, README, 중요도 메타데이터는 `IC-2027-W-2-2`와 “공식 잔여범위”를 근거처럼 표기했다. 해당 매핑을 입증할 자료가 이 Pack에 없어 이를 제거하고 “내부 Topic Pack 지식·문항 분류; 공식 출제기준 매핑 미확인”으로 바꿨다.
- 광전 존재검출, Direct/Indirect ToF, 삼각측량, 광학오차 및 선정의 범위는 유지했다. 기존 초음파·레이더 상세지식은 각 인접 Topic의 소유 범위로 남겼다.
- 10개 expected question pattern과 같은 순서의 `question_examples`를 추가했다.
- `high_score_points`와 `common_missing_points`의 전역 문장을 각 패턴에 한정했다. Question Type, routing aliases, deterministic/LLM ownership, 14개 fatal contract는 바꾸지 않았다.
- 10번의 광학-초음파 비교문항은 기존 required anchors만으로 초음파와 광학의 왕복 ToF 공통 구조 및 전파 현상 차이를 직접 평가할 근거가 부족했다. 비교 전용 Anchor `optical_vs_ultrasonic_tof_comparison` 하나를 추가해 10번에만 연결했다. 초음파의 온도보상·설치·에코 진단은 요구하지 않는다.
- Fact Anchor는 27개가 되었고 expected-pattern required union과 outline 참조가 각각 27/27이다. 질문 예시는 10/10 패턴과 순서 일치한다.

## 검증

- Focused regression: `scripts/test_optical_laser_photoelectric_noncontact_measurement_topic.py` PASS
- Topic schema validation: PASS (global anchor uniqueness 검사 포함)
- Topic quality validation: PASS, errors 0, warnings 1. 경고는 기존 LLM-only Pack의 `deterministic_checks.topic_aliases` 빈 배열 의도에 관한 것으로 test contract가 명시적으로 고정한다.
- Atomicity audit: PASS, warnings 0
- Scoped generated-pipeline release: PASS; live LLM smoke는 실행하지 않음
- Release 검증 뒤 `rubrics/generated/` 사전 snapshot 복원 확인
- `git diff --check`: PASS

이 수정은 source contract와 문서의 명확화다. Runtime grader가 pattern별로 해당 문장들을 자동 gate한다고 주장하지 않으며, 라우팅·점수 알고리즘은 변경하지 않았다.
