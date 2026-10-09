# P&ID Topic Pack 문제 단위 감사 — 2026-10-07

대상: `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`
유형: 문제 단위·문항별 coverage 및 ownership 경계 감사

## 판정

P&ID라는 공통 설계 문서를 중심으로 유지한다. 다만 11개 예상 문항은 같은 내용을 반복하지 않고 네 개의 독립된 요구군을 이룬다. 그러므로 Pack을 통합형 학습 원천으로 유지하되, 한 문항의 답안에 다른 요구군을 일괄 요구하지 않도록 문항별 필수 Anchor와 고득점·누락 설명에 적용 범위를 명시했다. 독립된 요구군을 연결하기 위해 문항에 불필요한 사실을 추가하지 않았다.

## 발견 및 보완

- 초기 화면의 `DISCONNECTED_QUESTION_FAMILIES` 경고는 required-anchor 그래프의 네 연결요소(4·5·1·1)를 뜻한다. 이는 단순 누락률이 아니라 문항들이 필수 Anchor를 공유하지 않는 구조적 신호다.
- 네 연결요소는 (1) 문서 역할 비교·P&ID 목적·alarm/logic 문서 경계, (2) 기호·Tag·신호선·측정/feedback loop·밸브 판독, (3) 설계검토 cross-document consistency, (4) 변경관리·as-built 문항이다.
- 네 군 모두 P&ID 문서의 판독·설계·운영이라는 공통 owner에 속한다. 이번 source 단계에서는 별도 Topic 생성이나 Router·taxonomy 소유권 변경 대신 문항별 경계를 보존한다. `DISCONNECTED_QUESTION_FAMILIES` 경고는 허위 연결을 만들지 않기 위해 남긴다.
- `equipment_and_piping_representation` Anchor는 24개 중 기존 expected-question union에서 빠져 있었다. P&ID 목적·구성 문항(pattern 2)에만 추가해 required union을 23/24에서 24/24로 보완했다.
- 11개 expected patterns 각각에 intent가 있으며 `question_examples`를 같은 순서·문장으로 맞췄다. outline은 이미 24/24 Anchor를 참조하고 있었다.
- High-score/common-missing과 importance unlock 문구를 해당 문항 번호에 한정했다. 예를 들어 MOC/as-built는 pattern 10, P&ID/PID 용어 구분은 pattern 11에서만 평가하도록 표현했다.
- `IC-2027-W-3-7`은 repository 내부 매핑 식별자다. 출제기준의 문구를 참고했다는 사실과 개별 예상문항이 실제 기출문제라는 주장은 분리해 README·Topic Sheet·importance note에 표시했다.

## 보호한 범위

- Question Type `IMPLEMENTATION_EVALUATION`, routing aliases, fatal IDs, deterministic/LLM authority, A/B/C/D/E scoring contract 및 release gate는 변경하지 않았다.
- 신규 Topic이나 Anchor를 만들지 않았고 generated projection도 promote하지 않았다.
- P&ID와 PID controller의 구분은 문항 11의 내용 요구로만 유지했다. bare `PID` 배제는 routing 정책이지 답안의 고득점 조건이 아니다.

## 검증

- `scripts/test_pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative.py`: 17 tests PASS
- `validate_topic_packs.py --topic-id ...`: PASS
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS
- `audit_topic_pack_atomicity.py --topic-id ... --json`: PASS, warning 1건(`DISCONNECTED_QUESTION_FAMILIES`, 분할/허위 연결 미적용)
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS, live LLM smoke 생략
- Release validator가 `rubrics/generated/`를 검증 전 snapshot으로 복원했다.
- `git diff --check`: PASS

## 남은 판단

사람이 검토할 때는 이 네 요구군을 하나의 P&ID 학습 Pack으로 계속 둘지, 설계검토·문서관리 요구군을 별도 Pack으로 분리할지만 확인하면 된다. 현재는 분리의 이득이 Router/owner 변경의 위험보다 명확하지 않아 기존 단일 source owner를 유지한다.
