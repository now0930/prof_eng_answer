# Grading Quality Roadmap

이 문서는 채점 정확도, 회귀 검증, Topic Pack 확장과 운영 배포의 장기 관리 정책을 정의한다. [GitHub Issue #1](https://github.com/now0930/prof_eng_answer/issues/1)은 현재 상태와 실행 증거만 추적하고, 반복 가능한 정책은 이 문서를 정본으로 사용한다.

## 1. 현재 기준선

| 항목 | 현재 상태 | 정본 |
|---|---|---|
| 채점 구조·점수 소유권 | 구현 완료, 지속 회귀 | [`grading_architecture.md`](grading_architecture.md) |
| Canonical demand ledger와 공개 coverage summary | 구현 완료, 지속 회귀 | `evaluation_ledger.py`, SIL output/coverage tests |
| 전문가 정확도 Gate | `HOLD`: 요구 상태 정확도 55.86% | [`accuracy_release_gate.md`](accuracy_release_gate.md), `reports/expert_accuracy_seed_current.json` |
| Topic Pack authoring·검증 | `ab94b69`에서 범용·대상 기반 흐름 적용 | [`topic_pack_workflow.md`](topic_pack_workflow.md) |
| Runtime provenance | process 수준 구현, image/container 증명 미완료 | [`operation_runbook.md`](operation_runbook.md), Issue #1 |

코드 회귀 PASS와 운영 정확도 `READY`, 배포 증명 완료는 서로 다른 판정이다. 하나의 판정으로 다른 판정을 대체하지 않는다.

## 2. 변경 등급과 필수 Gate

| 변경 등급 | 예시 | 필수 검증 |
|---|---|---|
| 문서 | 링크, 설명, 절차 | Markdown 링크·`git diff --check` |
| Topic source | Fact, alias, Logic Check, 신규 Topic | 단일 Topic release, 필요 시 routing smoke |
| 채점 runtime | 점수, coverage, verifier, finalizer | focused regression, 전체 release, 전문가 정확도 Gate |
| 배포 runtime | image, Compose, provider, 환경변수 | rebuild/recreate, container replay, fingerprint·parity, endpoint smoke |

정확도 Gate가 `HOLD`이면 코드 병합 여부와 무관하게 새 채점 정책의 운영 배포를 승인하지 않는다. Gate를 다시 열 때는 현재 코드와 provider로 prediction 30건 이상을 재생성하고 전문가 label과 대조한다.

## 3. 채점 오류 관리

1. 실제 사례를 익명화한 재현 fixture로 만든다.
2. 문제 제목이나 session ID 전용 예외를 추가하지 않는다.
3. 최초 오류 owner를 Question Demand, Fact Anchor, Logic Check, evaluator, score reconciliation 또는 formatter 중 하나로 지정한다.
4. 정답·부분정답·핵심오답과 false-positive 사례를 함께 검증한다.
5. focused regression과 전체 release를 통과시킨다.
6. 정확도 의미가 바뀌면 기존 prediction을 재사용하지 않고 전문가 정확도 Gate를 재측정한다.
7. 배포 후 container와 실제 endpoint에서 동일 판정을 확인한다.

핵심 지표는 fatal 답안의 pass/strong escape 0건, verified defect와 `incorrect` 동기화 실패 0건, 출력·저장 판정 불일치 0건이다.

## 4. Golden Set 관리

- 최소 운영 Gate는 reviewed/adjudicated 30건, Topic 10개, Question Type별 3건과 major/fatal label 8개다.
- 모든 신규 Topic마다 세 개의 Golden case를 기계적으로 추가하지 않는다.
- 점수·fatal·major·coverage 의미를 바꾸거나 안전 중요도가 높은 Topic은 정답/부분정답/핵심오답 사례를 추가한다.
- 단순 alias·문서·비채점 metadata 변경은 focused source/routing regression으로 검증할 수 있다.
- provider, prompt, scoring 또는 evidence 상태 의미가 바뀌면 prediction을 재생성하고 Gate 결과와 생성 commit을 함께 기록한다.
- 과거 `READY` 결과는 이후 정책 변경의 배포 근거로 재사용하지 않는다.

## 5. Topic Pack 관리

신규 Topic은 Topic Sheet의 ownership과 negative boundary를 먼저 확정한다. 생성·검증 절차는 [`topic_pack_workflow.md`](topic_pack_workflow.md)를 따른다.

관리 원칙:

- 기술 내용은 Topic Sheet와 검토된 source JSON이 소유한다.
- 신규 Topic은 `add-topic`으로 시작하고 `approve-topic`으로 사람 검토와 source hash를 기록한다.
- 생성기는 다른 Topic의 공식·규칙을 주입하지 않는다.
- 분류는 각 `topic_importance.json`의 `difficulty`가 정본이며 별도 Topic 목록이나 고정 총계를 중복 관리하지 않는다.
- 기본 release는 변경 Topic 또는 `--topic-id`만 검증한다. 전체 inventory는 통합 시점에 `--all`로 실행한다.
- live LLM smoke는 외부 환경이 필요한 별도 Gate이며 기본 source 검증에 포함하지 않는다.
- 생성 또는 release 실패 시 canonical source와 generated bank를 작업 전 상태로 복구한다.
- 승인 이후 source가 바뀐 관리 대상 Topic은 promote와 전체 integration을 차단한다.
- generated bank는 직접 수정하지 않는다.

## 6. Release와 배포

세 Gate는 소유권을 합치지 않고 `scripts/release_candidate.py`가 순서만 조정한다.
`qualify`는 Topic Pack 전체 검증과 코드 release validation 이후 현재 provider로
30건 이상을 새로 채점하고 Accuracy Gate가 `READY`인지 확인한다. `deploy`는 같은
commit의 READY manifest만 받아 rebuild 또는 recreate와 배포 증거를 수집한다.
Accuracy Gate가 `HOLD`이면 Docker 명령은 실행되지 않는다.

### 매 release

1. 변경 범위의 focused regression
2. `scripts/validate_release.sh`
3. 채점 의미 변경 시 전문가 정확도 Gate
4. generated source/build 정합성과 clean worktree 확인
5. push 후 local/tracking/remote SHA와 CI 확인

### 매 deployment

1. 배포 대상 commit과 image digest 기록
2. container ID·시작 시각과 process 교체 확인
3. host/container 핵심 module SHA parity 확인
4. container 내부 production replay
5. Telegram 또는 동등 endpoint smoke
6. 결과 artifact 저장

fingerprint, parity, replay 또는 endpoint 증거가 빠지면 배포 완료로 기록하지 않는다.
manifest의 `issue_close_eligible=true`는 기술 Gate가 모두 통과했다는 뜻이며 Issue를
자동으로 닫지는 않는다.

## 7. 문서와 Issue 관리

- 이 문서: 장기 정책, Gate와 관리 원칙
- [`grading_architecture.md`](grading_architecture.md): 현재 채점 구조와 owner
- [`topic_pack_workflow.md`](topic_pack_workflow.md): Topic 추가·수정 실행 절차
- [`operation_runbook.md`](operation_runbook.md): 운영·배포 명령
- [`accuracy_release_gate.md`](accuracy_release_gate.md): 정확도 Gate 수치와 실행법
- Issue #1: 최신 HEAD, Gate 결과, 배포 증거와 남은 blocker
- `docs/archive/`: 종료된 Stage와 과거 판단 기록

Issue 본문은 현재 상태만 유지한다. 긴 실행 로그는 comment 또는 repository artifact에 남기고, 완료된 과거 Stage를 현재 blocker처럼 유지하지 않는다.
