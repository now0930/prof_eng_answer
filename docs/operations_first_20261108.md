# 운영 우선 전환 결정 및 후속 기술 부채 — 2026-11-08

> 상태: **운영 방향 결정 및 후속 작업 기록. 새 후보 배포 승인 아님.**
> 기준: `d3683c8` 48건 최초 qualification과 `34aaca8` SIL 수정 커밋.
> 정본: `docs/operation_runbook.md`, `docs/accuracy_release_gate.md`,
> `calibration/expert_accuracy_release_policy.json`, `calibration/demand_state_stability_policy.json`.
> 실행 상태와 최종 배포 증거는 해당 환경의 비공개 `release_candidate` manifest로만 판정한다.

## 1. 결정: 사용자 학습 기능을 먼저 안정적으로 운영한다

**운영을 중단하고 모든 교정이 끝날 때까지 기다리는 방식은 선택하지 않는다.**
이미 배포된 Telegram 봇의 학습/복습 기능은 현재 운영 상태를 검증한 뒤 계속 사용한다.
그러나 **새 커밋을 운영 컨테이너에 반영하는 행위는 별도 승인/검증 문제**다.
기존 컨테이너를 그대로 두는 것과 검증 실패 후보를 배포하는 것은 다르다.

- 학습·복습(`/review`, 기존 승인된 Master Topic Pack): 기존 운영본 유지. 새로운 학습 계층을 운영본에 덮어쓰지 않는다.
- 채점: 검증된 Fact/Anchor 및 공식적인 질문 계약만 근거로 사용. `A/B/C`는 결정론적, `D/E`는 실제 적용된 Argon 제안에 한정한다.
- 채점 불능(`DeterministicPrimaryError`), 의미 미해결(`resolution_review.required`), Argon `FALLBACK`, 중복 양수 근거, 공급자 오류: **정식 점수·합격 판정을 승인하지 않는다.** 비공개 답안을 보존하고 보류 사유를 기록한다. 기존 UI에 보류 출력이 구현되지 않았다면 신규 배포 전에 구현·시험한다.
- `Fact Anchor`가 보류된 영역은 **자동 승격 금지**. 기술 내용 설명/복습과 정량 채점 가능 여부를 분리한다.
- 새 봇 후보는 `release_candidate.py qualify`가 `READY`를 출력하고 `deploy`가 endpoint smoke까지 통과하기 전에는 운영 봇을 교체하지 않는다.

## 2. 확인된 증거 (수치의 범위를 확대 해석하지 말 것)

| 범위 | 관측 결과 | 판정 |
|---|---|---|
| `d3683c8` 전체 qualification | reviewed 48건 중 45건 생산 경로 PASS, 3건 FAIL | **HOLD**. 정확도 Gate/안정성 Gate 진입 전 종료 |
| `34aaca8` SIL 코드 회귀 | `test_deterministic_primary_grader.py` + `test_unresolved_grade_review.py` 23/23 PASS | 집중 테스트 PASS; 전체 validation 아님 |
| `34aaca8` SIL 단일 운영 채점 | 6.79/25, `resolution_required=False`, Argon `APPLIED`, exit 0 | **생산 채점 완료**. `passing_score_allowed=False` 유지 |
| SIL 전문가 허용 점수 | 10.0–14.5점, 프로그램 6.79점 | 하한 대비 3.21점 차이 **미해결**. 임의 보정 금지 |
| Nyquist 단일 재채점 | 첫 실행 `duplicate_positive_evidence`로 FALLBACK, 새 실행 PASS | **재현 가능한 성공 1회**만 확인. 안정성 미입증 |
| EMC 계장 전원·접지·차폐 | 채점 예외 `DeterministicPrimaryError` | 기존 테스트가 보류된 긍정 Anchor 때문에 abstain을 의도적으로 기대함 |

상기 검증 증거는 사용자 운영 서버의 **비공개** `~/chatgpt_project/private_backups/release_qualification/` 아래에 있다.
답안 원문, provider 응답, API 키, 세션, private artifact를 공개 GitHub에 커밋하지 않는다.

## 3. 최소 운영 범위와 경계

**현재 가능한 작업**: 이미 실행 중인 버전의 Telegram 봇을 변경 없이 사용하고,
학습/복습, 승인된 근거 검색, 지원되는 문제의 연습 답안을 활용한다.
이는 **새 버전이 인증되었다는 뜻이 아니며**, 저장된 점수도 운영 후보의 Golden 통과를 보증하지 않는다.

**새 후보에서 자동 점수 확정이 불가능한 경우**:

1. 결정론적 라우팅·요구 근거가 ABSTAIN하면 채점 결과를 만들어내지 않는다.
2. Argon이 중복 양수 근거·JSON 파싱·transport 실패 등으로 `FALLBACK`이면 기존 D/E로 임의 확정하여 합격 판정을 내리지 않는다.
3. 문장의 공학적 관계가 미해결이면 `REVIEW_REQUIRED`; 관측된 오답 및 치명 규칙은 유지한다.
4. 학습 자료나 WordPress OCR/신규 Fact 후보만으로 A/B/C를 승인하지 않는다.

이 사용자 표시/이력 기록용 **fail-closed 보류 UX**는 독립 개발·회귀시험을 거쳐야 한다.
현재 구현 여부가 확인되지 않은 상태에서는 **지원 불가 주제의 숫자 점수를 신뢰해서는 안 된다**.

## 4. 미완료 작업 — 우선순위 및 종결 조건

| 순위 | 과제 | 처리 원칙 | 종결 조건 |
|---|---|---|---|
| P0 | **EMC 사례가 포함된 48건 Gate와 의도적 ABSTAIN 충돌** | 보류된 Fact Anchor를 무조건 풀지 않는다. 공식 원문 검증을 거쳐 채점 가능한 계약으로 바꾸거나, 범위가 명시된 **별도 제한 파일럿**을 설계한다. 기존 48건 Golden을 삭제·숨김·수정하지 않는다. | 채점 가능 근거 승인 + 전체 Gate 통과, **또는** 명확히 '정식 배포가 아닌 제한 파일럿'으로 분리되고 실제 runtime abstain·비점수 출력·격리 테스트가 검증됨 |
| P0 | **Telegram 오류/Argon fallback 때 확정점수·학습 이력 보존 경계** | 실패를 0점 또는 합격 결과로 바꾸지 않는다. 사용자에게 `채점 보류`를 표시하고 비공개 진단 유지. 미완료 채점은 완료된 학습 이력으로 적재하지 않는다. | DeterministicPrimaryError·FALLBACK·의미 미해결·정상 APPLIED 통합 테스트 |
| P1 | **Nyquist 간헐적 `duplicate_positive_evidence`** | 동일 인용의 복수 양수 근거 사용 금지를 유지. 필요 시 제한된 재요청과 실제 호출 횟수 기록을 설계한다. retry로 부실 증거를 승인하지 않는다. | 동일 후보의 두 uncached 실행 및 Stability Gate 통과 |
| P1 | **SIL 점수 6.79 vs 전문가 범위 10.0–14.5** | 재검증한 fatal/Wrong·MISSING을 유지하고, 인간 전문가 라벨과 계약 요구 ID를 독립 감사한다. 점수 하한에 맞추는 임의 가점 금지. | 근거별 독립 판정 기록 + 정확도 정책 통과 |
| P1 | **전문가 demand ID와 현재 Topic Pack ID 불일치** | 의미상 매핑을 자동 승인하지 않는다. 적용 범위·근거를 명시하고 검토한다. | 대응표 및 검토 기록, 회귀 테스트 |
| P2 | **SIL 구문의 나머지 미해석 span·별칭과 정확도 확장** | 관측된 미해결 12개 span이 모두 실제 요구 미해결을 뜻하지 않는다. 형식·기술 내용을 구분한다. | 정상/부분/오답/반박 문장 회귀와 Golden 변경 없는 개선 |
| P2 | **보류 Fact Anchor와 WordPress source freshness** | `wp-post:9529`처럼 원문/버전 불일치 시 보류·백업. 검증되지 않은 최신 후보는 채점에 사용하지 않는다. | 원문 감사, 출처 및 hash 일치, 공식 승인 |

## 5. 배포까지의 실행 순서 (Gate 약화 없이)

1. 운영 컨테이너의 현재 ID, commit, volume, 백업을 기록한다. 기존 Docker는 재시작하거나 재생성하지 않는다.
2. 변경 후보는 별도 clean worktree로 검증한다. 현재 SIL 수정은 `34aaca8`; 이 문서 후속 커밋은 작업 브랜치에서만 유지한다.
3. Source/Topic Pack + 전체 `scripts/validate_release.sh` 실행. `PROMOTE_GENERATED=0`; 자동 업데이트/승격 금지.
4. 현재 운영 설정을 **변경하지 않고** `scripts/release_candidate.py qualify --workers 2` 실행. 48 reviewed 실제 Argon 채점, 정확도 Gate, 두 번째 uncached 안정성 검사가 모두 포함된다.
5. `QUALIFICATION=READY`가 나오고 manifest가 동일 commit을 기록한 경우에만 `release_candidate.py deploy` 수행한다. `HOLD`이면 배포하지 않는다.
6. 배포 직후 commit/container parity와 Telegram `/review`·지원 주제 `/grade` endpoint smoke, 재시작 및 rollback 준비 확인.
7. 새 후보가 HOLD라면 **기존 동작 중인 운영본을 유지**하고 부족한 작업은 이 문서의 Queue에서 처리한다.

권장 운영 서버의 읽기 전용 상태 확인:

```bash
cd ~/hermes/workspace/prof_eng_answer
git rev-parse --short HEAD
git status --short
docker ps --filter "name=prof_eng_answer_bot" --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'
```

`qualify`는 실제 API 호출과 비공개 파일 생성을 포함하므로 운영 서버에서 시행한다.
명령 실행 전 `~/hermes/.env`는 **출력하지 말고** 내부적으로만 읽는다.

## 6. 제한 파일럿을 별도로 구현할 경우의 필수 조건

전체 48건 Gate를 우회하는 `--skip-release-validation`, `minimum-predictions <30`,
`Golden` 변조, `scoring-exclusion` 임의 해제, `--allow-dirty` 배포는 **금지**한다.

EMC를 채점 불능으로 남겨야 하는 경우 정식 `READY`를 가장하지 않고
**별도의 제한 파일럿 계약**(`SCOPED_PILOT` 등)을 신규 설계한다.
필수 조건: 명시적 허용 Topic/기능, 미지원 범위의 runtime 자동 abstain 및 **숫자/합격 판정 비출력**,
Golden 원본 48건 유지와 제외 사례의 별도 안전 시험, 점수화 가능 사례의 독립 Accuracy/안정성 증거,
별도 Telegram token/데이터 영역(또는 운영 트래픽과 물리적으로 격리된 검증),
모든 실패 시 즉시 기존 운영본으로 복귀.
이 제한 파일럿은 `release_candidate.py deploy`가 요구하는 `READY`나 전체 성공을 대체하지 않는다.
**상기 격리/검증 구현은 이번 문서 커밋의 범위 밖이다.**

## 7. 이번 결정에서 바꾸지 않는 것

- `calibration/expert_accuracy_golden.jsonl` 및 전문가 점수/라벨
- Fact Anchor Registry/Topic Pack의 승인 및 제외 상태
- A/B/C 결정론 점수식, D/E Argon 근거 유효성 판정, fatal·ceiling 규칙
- Release Accuracy Policy, Stability Policy, `release_candidate.py`의 배포 차단 조건
- `main`, 현행 서버의 Docker 컨테이너와 비공개 데이터

**운영 책임 경계**: 이 문서는 '지금부터 진행할 범위'와 '나중에 해결할 항목'을 확정한다.
새 후보의 **배포 성공**은 독립적으로 기록된 `qualification.status=READY`와
`deployment.status=PASS`를 확인하기 전에는 주장하지 않는다.
