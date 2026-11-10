# ChatGPT 서버 최신 `main` 운영 반영 체크리스트

작성 기준일: 2026-11-09
목적: ChatGPT가 서버에서 GitHub 최신 `main`을 운영에 반영할 때, 코드 통합·비공개 데이터 보존·운영 배포를 구분하고 실제 증거에 따라 진행한다.

> 이 문서는 배포 절차다. 문서 작성 자체로 운영 코드나 컨테이너를 변경하지 않는다. 운영 배포는 본 체크리스트의 중단 조건과 저장소의 [운영 Runbook](operation_runbook.md)을 모두 만족할 때만 수행한다.

## 1. 현재 기준선과 알려진 상태

| 항목 | 2026-11-09 확인값 | 처리 원칙 |
|---|---|---|
| 최신 GitHub `main` | `a8aab1e3dd9a5d3418c65a751848a0597ec2f02a` | 작업 시작 때 `git fetch` 후 다시 확인한다. 이후 커밋이 있으면 새 최신 SHA를 기록한다. |
| 운영 checkout | `/home/now0930/hermes/workspace/prof_eng_answer` | 경로를 바꾸거나 삭제하지 않는다. 조사상 `d3683c8bde33041e84e519a270dab40fb31e9dcf`였으며 당시 `main`보다 55커밋 뒤였다. 서버에서 실측한다. |
| 개발 checkout | `/home/now0930/codex/pro_engineer/prof_eng_answer` | 코드 검토·수정용이다. 운영 데이터나 자격증명을 복사하지 않는다. |
| 운영 서비스 | Compose service `prof-eng-answer-bot`, container `prof_eng_answer_bot` | 배포 전 실제 이름·상태·mount를 재확인한다. |
| 저장소 검증 | release script, `rubric_manager validate-all`, generated freshness 통과 | 전체 pytest는 1,585 passed, 8 failed, 1 skipped였고 기존 실패 8건은 PR #21 기준선과 동일하다고 기록되어 있다. 이를 전체 PASS로 표현하지 않는다. |
| Qualification | 실제 48건 운영 qualification과 안정성 Gate 완료 증거 없음 | manifest에서 `READY`를 확인하기 전에는 배포 금지. release script PASS만으로 READY를 추정하지 않는다. |
| 기존 백업 | 2026-11-09 백업과 별도 물리 디스크 사본이 기록됨 | 과거 백업은 참고다. 배포 직전 새 백업을 만들고 다시 검증한다. |

이 표는 기준선일 뿐이다. 배포 시점의 상태가 다르면 실제 상태를 우선하고 차이를 기록한다.

## 2. 하드 가드레일

- `main`에 직접 커밋하지 않는다. 서버 운영 checkout에서는 개발하지 않는다.
- 비공개 답안, 세션, 학습 이력 DB, `.env`, API 키를 GitHub·PR·로그·채팅에 복사하지 않는다.
- 백업 검증 전 운영 파일을 덮어쓰거나 DB·폴더·브랜치를 삭제하지 않는다.
- 운영 checkout이 dirty이거나 untracked 파일이 있으면 내용을 먼저 분류·보존한다. `git reset --hard`, `git clean`, 강제 checkout으로 치우지 않는다.
- `qualification.status=READY`, 요구된 정확도/안정성 조건, Release Gate, 최신 CI 및 rollback 준비가 확인되지 않으면 Compose `up`, `restart`, `pull` 또는 컨테이너 재생성을 하지 않는다.
- 알려진 pytest 실패를 숨기거나 테스트·Golden 기준을 낮추지 않는다. 기존 실패와 새 회귀를 구분해 근거를 남긴다.
- `rubrics/generated/`를 직접 편집하지 않는다. 생성·검증은 `scripts/rubric_manager.py` 절차를 사용한다.

## 3. 1단계 — 서버와 Git 상태 확인

비밀정보를 출력하지 않고 다음만 확인한다.

```bash
cd /home/now0930/hermes/workspace/prof_eng_answer
pwd
git remote -v
git branch --show-current
git rev-parse HEAD
git status --short --untracked-files=all
git fetch origin main
git rev-parse origin/main
git log -1 --format='%H %cI %s' origin/main
git rev-list --left-right --count HEAD...origin/main
```

판정:

- `pwd`가 지정된 운영 경로인지 확인한다.
- origin이 기대한 `now0930/prof_eng_answer` 저장소인지 확인한다.
- 현재 브랜치, HEAD, `origin/main`, ahead/behind를 기록한다.
- dirty/untracked 항목은 비공개 데이터 또는 운영 변경일 수 있으므로 하나씩 분류한다. 미확인 항목이 있으면 `HOLD`한다.
- 아래 단계 검증 후에도 `git pull`을 무조건 실행하지 않는다. 오직 clean이며 `main`이고 fast-forward 가능한 경우에만 `git merge --ff-only origin/main`을 고려한다.

## 4. 2단계 — 배포 직전 비공개 백업

저장소의 [비공개 운영 데이터 백업 및 복원 점검](private_runtime_backup.md)을 따른다. 기존 운영 코드를 바꾸지 않고 GitHub `main`의 백업 스크립트만 실행할 수 있다.

```bash
set -euo pipefail
cd /home/now0930/hermes/workspace/prof_eng_answer
git fetch origin main
git show origin/main:scripts/backup_private_runtime.py | \
  python3 -B - --backup-root /home/now0930/hermes/private_backups/prof_eng_answer
```

스크립트가 출력한 정확한 `BACKUP_DIR`에 대해 다음을 수행한다.

1. `BACKUP_STATUS=OK` 및 manifest의 `status=OK`를 확인한다.
2. 모든 SQLite 백업 파일의 해시와 `quick_check=ok`를 확인한다.
3. 주요 DB의 스키마·레코드 수와 별도 임시 경로 복원 테스트를 확인한다.
4. `state.json`, 세션 디렉터리, 사용자 설정이 보존됐는지 파일명·개수·해시로 점검하되 원문은 출력하지 않는다.
5. 가능하면 `/mnt/ExtSSD1` 등 별도 물리 디스크에 사본을 만들고 해시 일치 여부를 확인한다.

이 백업 도구는 Hermes `/opt/data` named volume, WordPress 등 별도 DB, Codex 전체 복제본을 포괄하지 않는다. 필요한 자료가 범위 밖이면 각 저장소/서비스에 맞는 별도 백업과 검증을 완료할 때까지 `HOLD`한다. 백업 실패·불완전·복원 미검증이면 배포하지 않는다.

## 5. 3단계 — 후보 커밋 검증

배포 후보 SHA를 고정하고 다음을 운영 경로와 격리된 checkout/worktree에서 실행한다. 아래 SHA는 2026-11-09 기준선이며 실행 시 `origin/main` 최신 SHA로 대체한다.

```bash
git show -s --format='%H %cI %s' origin/main
PROMOTE_GENERATED=0 bash scripts/validate_release.sh
python3 -B scripts/rubric_manager.py validate-all
python3 -B scripts/test_generated_rubrics_freshness.py
python3 -B -m pytest -q
```

기록할 내용:

- 각 명령의 종료 코드와 로그 파일 위치
- 전체 pytest의 pass/fail/skip 수와 실패 테스트 이름
- CI가 **동일 후보 SHA**에서 성공했는지
- `RUN_GRADING_REPRODUCIBILITY` 등 opt-in Gate가 실행되었는지 또는 skip되었는지
- release/qualification manifest의 실제 파일 경로와 상태

2026-11-09 기준 알려진 결과는 release script, `validate-all`, generated freshness 통과이며, 전체 pytest는 1,585 passed / 8 failed / 1 skipped였다. 8개 실패를 이미 알고 있다는 이유만으로 현재 실행에서 무시하지 않는다. 각 실패가 동일한 기준선인지 재확인하고, 신규 실패·원인 불명·필수 Gate skip은 배포 중단 사유다. 저장소 정책이 요구하는 운영 accuracy/stability qualification이 없거나 `HOLD`이면 배포 금지다.

## 6. 4단계 — 운영 설정·DB 호환성 검토

컨테이너와 Compose 정의를 읽기 전용으로 확인한다. 토큰이나 전체 환경값을 출력하지 않는다.

```bash
cd /home/now0930/hermes
docker compose ps
docker inspect prof_eng_answer_bot \
  --format '{{.Id}} {{.Config.Image}} {{.State.Status}} {{.State.StartedAt}}'
docker inspect prof_eng_answer_bot \
  --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'
```

- 운영 service, mount, DB 경로가 예상과 같은지 확인한다.
- 후보 커밋에서 의존성·환경변수·DB schema/migration·Compose 설정 변경을 검토한다.
- `.env`는 내용 출력 없이 존재·권한·필수 키 이름만 확인한다. 백업에서 기존 키를 유지하고 운영용 키를 테스트 키로 대체하지 않는다.
- migration이 있으면 백업 복원본에서 먼저 시험하고 rollback 방법을 확보한다. 되돌릴 수 없는 migration 또는 검증되지 않은 데이터 변환은 `HOLD`한다.
- 같은 경로를 bind mount하는 구조에서 이전 코드를 보존할 방법이 없으면 배포하지 말고 별도 release 경로/복구 계획을 먼저 확정한다.

## 7. 5단계 — 조건부 운영 반영

다음 조건을 **모두** 만족해야 한다.

- [ ] 후보 SHA가 최신 `origin/main`이고 CI가 해당 SHA에서 성공
- [ ] 운영 checkout clean이며 개인 데이터·미추적 변경이 보존됨
- [ ] 배포 직전 백업과 복원 검증 완료
- [ ] 필수 release/qualification manifest가 정책상 READY
- [ ] 전체 pytest 및 알려진 실패가 분류되고 새 실패 없음
- [ ] DB/schema/환경 설정 호환성과 rollback 확인
- [ ] 기존 컨테이너·image·운영 HEAD 및 Compose 설정 기록

정책이 허용한 공식 deployment 절차가 있으면 이를 우선 사용한다. 그 절차가 현재 후보와 운영 Compose를 지원하지 않거나 `READY` 증거가 없으면 아래 업데이트를 실행하지 말고 `HOLD`한다.

표준 Git fast-forward 방식이 승인된 경우에만:

```bash
cd /home/now0930/hermes/workspace/prof_eng_answer
git status --short --untracked-files=all
git merge --ff-only origin/main
git rev-parse HEAD
```

이후 컨테이너는 저장소의 [운영 Runbook](operation_runbook.md)과 해당 Compose 설정에 기재된 정확한 절차로만 재생성한다. 서비스명을 추측하거나 `docker compose down`, 광범위한 prune, 임의 volume 삭제를 하지 않는다. 현재 문서만으로 deployment qualification 및 배포 승인 조건이 충족되지 않으면, Git checkout도 변경하지 말고 결과를 보고한다.

## 8. 6단계 — 배포 후 smoke test와 rollback

배포가 허용된 경우에 한해, 개인 이력을 오염시키지 않는 별도 테스트 계정/격리 자료로 확인한다.

- [ ] 컨테이너가 새 ID로 정상 기동하고 health/status가 healthy
- [ ] 런타임 `engine_commit`이 후보 SHA와 일치
- [ ] 핵심 grading 모듈의 host/container SHA-256 일치
- [ ] `/grade` 테스트에서 A/B/C 결정론적 경로가 동작
- [ ] 허용된 운영 설정에서 D/E provider 경로의 상태가 명확히 기록됨
- [ ] `/review`, `/review done`이 격리된 테스트 topic으로 동작하고 이력 저장 확인
- [ ] DB 연결·기존 이력 보존 확인
- [ ] 오류 로그에 비밀정보·답안 원문이 노출되지 않음

실패하면 원인을 기록하고 서비스 상태를 안정화한다. 기록된 기존 HEAD/image/config와 검증된 백업을 이용해 승인된 rollback 절차를 수행한다. 운영 DB를 새 코드로 덮어쓰거나 복원본으로 무조건 교체하지 않는다. 롤백 후 `/grade`와 `/review` 최소 smoke를 다시 수행한다.

## 9. 중단 기준과 최종 보고 양식

아래 중 하나라도 해당하면 `HOLD`, 운영 재시작 금지:

- checkout 위치·remote·branch가 예상과 다름
- untracked/dirty 변경 또는 비공개 파일의 소유·용도를 확인할 수 없음
- 백업/복원 검증 실패 또는 필요한 DB가 백업 범위 밖에 있음
- 필수 CI, qualification, accuracy/stability 또는 release Gate가 실패·미실행·HOLD
- DB migration, 환경 설정 변경, rollback 방법이 불명확
- 컨테이너 mount/runtime 버전이 후보와 일치하지 않음
- smoke test가 실제 사용자 데이터 변경 없이는 안전하게 수행될 수 없음

완료 또는 HOLD 시 비밀정보와 답안 원문 없이 다음 형식으로 결과를 남긴다.

```text
DEPLOYMENT_STATUS: PASS | HOLD | FAIL
SOURCE_MAIN_SHA: <실측 SHA>
PRODUCTION_BEFORE_SHA: <실측 SHA>
PRODUCTION_AFTER_SHA: <미변경이면 동일 SHA>
BACKUP: <비공개 경로, manifest status, 별도 디스크 사본 여부>
CI_AND_RELEASE: <각 상태와 실제 실행 여부>
PYTEST: <passed / failed / skipped 및 실패 분류>
QUALIFICATION: <실제 manifest 상태 또는 미실행 사유>
CONTAINER: <before/after ID, health, runtime commit>
SMOKE: </grade, /review, /review done 결과 또는 미실행 사유>
ROLLBACK: <검증 결과>
BLOCKERS: <없음 또는 정확한 미완료 항목>
```

운영 로그·개인 데이터 백업 Manifest는 비공개 백업 경로에 보관한다. 저장소에는 비밀정보 없는 절차/요약만 기록한다.

## 관련 문서

- [운영 Runbook](operation_runbook.md)
- [비공개 운영 데이터 백업 및 복원 점검](private_runtime_backup.md)
- [채점 품질 로드맵](grading_quality_roadmap.md)
- [정확도 배포 Gate](accuracy_release_gate.md)
