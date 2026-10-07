# Quantum/emerging technology Topic Pack 문제 단위 재구성

갱신: 2026-10-07
Topic: `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits`

## 판정

기존 10개 대표 질문은 서로 다른 질문 요구를 충분히 나눠 담고 있었다. 다만 Pattern 7의 sensing 비교에
일반 신기술 framework Anchor가 required로 연결되어 문항 요구보다 범위가 넓어 해당 연결을 제거했다.
또한 required Anchor 자체보다
`high_score_points`, `common_missing_points`, `high_band_unlock_conditions`가 모든 질문에 공통인 것처럼
작성되어, sensing 비교 답안에 gate/annealing·TCO를 요구하거나 real-time 대체 질문에 pilot economics를
요구할 여지가 있다는 점이었다.

각 기준에 적용 패턴을 명시했다. 다른 패턴에서만 요구하는 지식의 미언급은 별도 명시 요구가 없는 한
감점·오답 근거가 아니다. 공통 fatal boundary도 해당 오개념을 실제로 주장한 경우에만 적용하며 단순 미언급을
fatal로 보지 않는다. 점수 계약·fatal ID·Question Type·routing authority는 변경하지 않았다.

## 패턴별 요구 추적

| # | 대표 질문 범위 | 조치 |
|---:|---|---|
| 1 | 원리·계측제어 적용 가능성·한계 | qubit/superposition/measurement와 계산상 의미를 잇도록 interference Anchor를 required에 추가. entanglement 세부는 optional |
| 2 | 산업 제어시스템 적용 고려 | problem-fit, hybrid, latency, pilot, TCO의 명시 요구를 유지 |
| 3 | gate-based와 annealing 비교 | 두 모델과 problem-fit/optimization 후보에 집중 |
| 4 | 최적화 성능검증 | encoding/sampling, baseline, pilot 수용기준에 집중 |
| 5 | PLC/DCS 실시간 제어 대체 평가 | offline/supervisory 경계, latency, controller ownership에 집중 |
| 6 | noise/error 대책과 적용성 | noise, mitigation/correction 구분, scale/readiness에 집중 |
| 7 | quantum sensing과 computing 비교 | computing 정의와 sensing 경계에 집중; 다른 적용 축은 요구하지 않음 |
| 8 | 신기술 도입 타당성 | problem-fit, readiness, baseline, pilot, TCO, 공통 평가 framework 유지 |
| 9 | 데이터·통신·보안·운영 제약 | encoding/sampling, latency, governance 및 운영 통합에 집중 |
| 10 | 연구와 production readiness | maturity, baseline, pilot, TCO/통합에 집중 |

10개 질문의 required Anchor union은 25/27 (92.6%)이다. 두 미포함 Anchor는 `etc_entanglement_role`(원리 문항에서 선택 심화)와
`etc_estimation_candidate`(추정 문제를 직접 묻는 대표 pattern이 없음)이며, 이를 coverage 수치만 높이려고 필수화하지 않았다.
전체 학습 outline의 Anchor 참조 27개는 유지했다. 이는 Pack 전체 학습지식의 연결성이지, 각 답안의 일괄 필수 checklist가 아니다.
`IC-2027-W-5-2` 최신동향 분리는 static scoring criterion에서 제외하고 source ownership/update 경계로 남겼다.

## 변경 범위 및 보류

- 변경: pattern 1 required Anchor에 `etc_interference_role` 추가.
- 변경: 고득점·누락·importance 조건을 해당 패턴 번호를 명시한 문구로 한정.
- 변경: pattern 7은 computing/sensing 구분만 required로 유지하고 일반 emerging-tech framework를 해제.
- 변경: 27개 Anchor의 source_basis에서 공식 기준/기출 근거로 읽힐 수 있던 문구를 학습용 일반 원칙 요약 및 후속 source verification 대상으로 정정.
- 문서화: README 및 Topic Sheet에 학습 outline과 문항별 평가 checklist의 차이를 기록.
- 불변: 10개 질문문·Question Type·topic ID·Anchor ID/fatal ID·Router·deterministic score contract.
- 보류: entanglement를 원리 문항의 필수요건으로 승격하지 않음. 대표 질문에 반드시 필요한 직접 요구라고 보기 어렵고 심화 배경으로 충분하다.
- 보류: 최신 산업 사례·연구 성숙도 수치를 갱신하지 않음. 이번 작업은 문제 단위 구조 검토이며 동적 사실검증 범위가 아니다.
- 주의: `IC-2027-W-5-1`은 저장소 내부 기획/coverage reference로 남기되 공식 출제 세부분류 또는 기출 근거로 표기하지 않는다. 대표 질문 10개 역시 학습용 예상 문항이다.

## 검증

- JSON 구문 검사: PASS (4개 source JSON).
- Focused Topic Pack regression: PASS 12/12.
- `validate_topic_packs.py --topic-id ...`: PASS (87 packs, 2,066 global anchors checked).
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS (errors 0, warnings 0).
- `audit_topic_pack_atomicity.py --topic-id ...`: PASS (errors 0, warnings 0).
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated banks 사전 snapshot 복구 확인.
- 전체 test suite는 실행하지 않았다. Topic Pack source/document/test 외의 grader runtime 파일은 수정하지 않았다.
- 로그: `/tmp/quantum_topic_release_20261007.log`.
- Full regression은 전체 worktree에 선행 사용자 변경이 다수 있어 무관한 파일을 staging/commit하지 않고, 이번 변경과 직접 연관된 회귀를 우선 수행한다.
