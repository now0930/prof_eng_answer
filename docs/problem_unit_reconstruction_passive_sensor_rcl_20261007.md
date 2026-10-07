# 수동형 R·C·L 센서 Topic Pack 문제 단위 감사

갱신: 2026-10-07
대상: `passive_sensor_resistive_capacitive_inductive_transduction`
판정: 내부 지식·문항 단위는 유지하되, 중복 alias와 문항별 과잉 평가범위를 보완했다. 공식 출제분류나 기출 증거로 간주하지 않는다.

## 핵심 검토

- Pack의 중심은 저항·정전용량·인덕턴스라는 세 파라미터 변환 계열을 비교하는 통합 원리다. 다섯 문항도 전체 변환 사슬, 재료물성/기하, Young's modulus와 전기·자기물성 구분, 식·readout 비교, 감도·오차·교정으로 서로 연결된다. 따라서 세 계열을 하나의 비교형 내부 학습 단위로 유지했다.
- 기존 18개 routing alias 중 `strain gauge`, `Wheatstone bridge`가 전용 strain-gauge Pack과 정규화 중복됐고, `LVDT`도 독립된 전용 Topic이 있었다. 이 세 구체 alias를 광범위 R·C·L Pack에서 제거했다. Source alias 전체 재검사 결과 다른 Pack과 정규화 중복은 0건이다.
- Gauge factor Anchor는 다섯 대표 문항 어느 것에도 직접 요구되지 않는 특수 사례다. Anchor는 보존하되 `optional`로 낮춰 required union 밖에 두고, strain-gauge 상세·bridge 온도보상·로드셀은 전용 Pack에 handoff하도록 README/Topic Sheet에 명시했다.
- LVDT/RVDT 상세 구조·복조도 전용 Topic 소유로 분리했다. 본 Pack은 일반 자기회로·인덕턴스 변환만 다룬다.
- 5개 expected question pattern에 intent를 추가하고 `question_examples`를 동일 순서로 맞췄다. High-score, common-missing, importance unlock 항목은 질문별 적용범위로 한정했다.
- Fact Anchor 14개 중 13개가 적어도 하나의 질문에서 required이며, 14개 모두 outline에서 설명 위치가 있다. 유일한 non-required Anchor는 위의 optional Gauge factor다.
- Question Type, fatal 8건, LLM-only semantic authority, 결정론적 검사 설정은 바꾸지 않았다. JSON source contract만 수정했고 generated rubric은 release 검사 뒤 원래 snapshot으로 복원했다. 따라서 새로운 alias 제외는 아직 generated runtime에 promote되지 않았다.

## 검증

- 신규 focused contract: `scripts/test_passive_sensor_rcl_problem_unit.py` PASS
- Schema validation: PASS
- Quality validation: PASS, errors 0 / warnings 0
- Atomicity audit: PASS, warnings 0
- Scoped generated-pipeline release: PASS; live LLM smoke는 실행하지 않음
- Model-answer router regression: 53 tests PASS
- Deterministic topic-router regression: 3 tests PASS
- 인접 owner 회귀: pressure, humidity, speed/rotation Pack 각 9 tests PASS
- `git diff --check`: PASS

이번 작업은 Topic Pack source/문서와 focused tests를 변경했으며 commit/push는 하지 않았다. 전체 worktree에 기존 미커밋 변경이 있어 관련 변경만 보존했다.
