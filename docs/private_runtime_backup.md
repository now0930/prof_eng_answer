# 비공개 운영 데이터 백업 및 복원 점검

> **사람용 핵심:** 개인 세션·학습 DB·WordPress 자료의 백업은 코드 배포와 별개입니다. SQLite online backup을 사용하지만 일반 파일은 원자적 snapshot이 아닙니다.
>
> **AI·개발자:** [코드·데이터 권한 참조](ai_implementation_reference.md) · [프로젝트 정책](../AGENTS.md). 과거 실행 기록과 현재 필수 Gate를 혼동하지 않습니다.


운영 기준: `~/hermes/workspace/prof_eng_answer` (배포 SHA는 GitHub `main`과 대조).
실제 비공개 파일을 GitHub에 올리지 않는다.

## 보호 대상

`scripts/backup_private_runtime.py`는 서버 호스트에서 실행하며 다음을 별도 개인
백업 폴더로 복사한다.

- `prof_eng_answer/data/`: Telegram `state.json`, 저장 답안/이미지 `sessions/`,
  복습 이력과 설정. 루트 디렉터리 안의 모든 하위 폴더(심볼릭 링크 제외).
- `prof_eng_answer/logs/`: 운영 로그가 존재할 때 포함.
- `prof_eng_answer/reports/`: 로컬 채점·검토 보고서가 존재할 때 포함.
- `prof_eng_answer/wordpress_docs/`: Git에서 제외된 비공개 WordPress 자료가 존재할 때 포함.
- `~/hermes/.env`, `~/hermes/workspace/.env`, 저장소의 `.env` 및
  `~/hermes/docker-compose.yml`: 존재하는 파일만 포함.
- `data/`, `logs/`, `reports/`, `wordpress_docs/` 안의 `*.sqlite3`, `*.sqlite`, `*.db`, `*.db3`:
  raw copy가 아닌 SQLite online backup을 사용. WAL이 열려 있는 상태에서도
  커밋된 트랜잭션의 일관된 snapshot을 취한 뒤 `PRAGMA quick_check` 확인.
- 추가 SQLite DB 탐색: `~/chatgpt_project/` (기존 `private_backups` 제외),
  `~/hermes/hermes_home/`, 운영 `.env`에 명시된 일부 DB 파일 경로.

**포함되지 않는 범위**: `/opt/data`에 마운트된 Hermes Agent Docker 볼륨,
WordPress/Immich 등 별도 MySQL/MariaDB/PostgreSQL 서비스,
삭제된 `~/codex/pro_engineer`의 프로젝트 전체 복제,
기존 `private_deploy_backup_*` 백업과 이미 생성된 비공개 백업들.
별도 서비스 DB는 그 서비스의 `mysqldump`/`pg_dump` 및 볼륨 전략으로
백업해야 하며 이 스크립트가 이를 백업했다고 주장하지 않는다.

## 백업 절차 (운영 컨테이너 중지 없음)

운영 checkout의 백업 스크립트를 실행한다. Bot을 중지하거나 Git 상태를
변경할 필요는 없다. root 셸에서 실행할 때는 `--repo`와 `--backup-root`를
명시해 root의 홈 디렉터리를 기본값으로 사용하지 않도록 한다.

```bash
set -euo pipefail
cd ~/hermes/workspace/prof_eng_answer

python3 -B scripts/backup_private_runtime.py \
  --repo /home/now0930/hermes/workspace/prof_eng_answer \
  --backup-root /home/now0930/hermes/private_backups/prof_eng_answer
```

기본 저장 위치는
`~/hermes/private_backups/prof_eng_answer/<UTC>_<random>/`이다.

별도 SSD에 저장하려면:

```bash
python3 -B scripts/backup_private_runtime.py \
  --repo /home/now0930/hermes/workspace/prof_eng_answer \
  --backup-root /mnt/ExtSSD1/private_backups/prof_eng_answer
```

백업 성공 시 `BACKUP_STATUS=OK`, `BACKUP_DIR=...`, `MANIFEST=...`가
출력된다. 실패하면 0이 아닌 exit code가 반환된다. **실패 또는 INCOMPLETE
백업을 근거로 원본 디렉터리를 정리하지 않는다.**

백업 폴더와 파일은 0700/0600으로 잠근다. `manifest.json`의
`sqlite_databases`에 파일별 원본 경로, sha256, `quick_check=ok`가
기록된다. `sqlite_databases`가 0개라면 SQLite 백업 대상이 실제로
존재하는지 확인해야 한다.

## 백업 검증

```bash
# BACKUP_DIR은 백업 도구가 출력한 정확한 경로로 바꾼다.
python3 - "$BACKUP_DIR" <<'PY'
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
m = json.loads((root / "manifest.json").read_text())
assert m["status"] == "OK", m["status"]
for item in m["sqlite_databases"]:
    assert (root / item["backup"]).is_file()
    assert item["quick_check"] == "ok"
assert (root / "runtime/data").is_dir()
print("BACKUP_VERIFIED", "sqlite_count=", len(m["sqlite_databases"]),
      "private_directories=", len(m["copied_directories"]))
PY
```

`training_history.sqlite3`는 원본이 복사된 위치에서 온라인 SQL 백업으로
저장된다. `-wal`/`-shm` 파일을 임의로 다시 합치지 않는다.
복원 시에는 운영 서비스를 안전하게 중지하고 새 복원 대상에 확인한 후
`runtime/data`, `runtime/logs`, `runtime/reports`, `runtime/wordpress_docs` 중
필요한 자료와 해당 DB 백업을 원본의 상대 경로에 되돌린다.
복원 전에는 기존 운영 data를 보존하고, 원본 백업 스냅샷을 수정하지 않는다.

현재 스크립트는 **실시간 JSON과 세션 파일 전체의 원자적 스냅샷을 보장하지는 않는다**.
엄밀한 일관성 복원 점검이 필요할 때는 서비스 정지 후 두 번째 콜드 백업을
수행하고, 별도 디렉터리에서 복원 테스트를 완료한다.

## 학습 이력 DB 쓰기 권한 복구

운영 Bot은 Compose에서 UID/GID `1001:1001`로 실행한다. 기본
`data/training_history.sqlite3`가 다른 소유자로 만들어져 Bot이 쓸 수 없으면
호스트의 권한 있는 계정에서 다음을 실행한다. 첫 명령은 계획만 출력한다.
`--apply`는 중앙 경로에 새 비공개 백업을 만들고 해당 SQLite 복원본의
`quick_check`와 해시를 확인한 뒤 DB 및 존재하는 WAL/SHM 부속 파일의
소유권을 `now0930:now0930`으로 바꾼다. 해당 파일에는
`codex_now0930`의 읽기 ACL을 부여한다. Bot을 재시작하거나 DB 내용을
수정하지 않는다.

```bash
python3 -B /home/now0930/hermes/workspace/prof_eng_answer/scripts/repair_training_history_permissions.py \
  --repo /home/now0930/hermes/workspace/prof_eng_answer \
  --backup-root /home/now0930/hermes/private_backups/prof_eng_answer \
  --compose /home/now0930/hermes/docker-compose.yml

# 위 계획과 백업 경로를 확인한 뒤 root 셸에서 실행
python3 -B /home/now0930/hermes/workspace/prof_eng_answer/scripts/repair_training_history_permissions.py \
  --repo /home/now0930/hermes/workspace/prof_eng_answer \
  --backup-root /home/now0930/hermes/private_backups/prof_eng_answer \
  --compose /home/now0930/hermes/docker-compose.yml --apply
```

출력된 `BACKUP_DIR`에 `permission_repair_before.json`이 이전 파일
소유권·권한을 기록한다. 실패했다면 `TRAINING_DB_PERMISSIONS_OK`가 없는
상태에서 Bot 동작을 정상이라고 간주하지 않는다.

## 디렉터리 정리 전 절대 조건

1. `BACKUP_STATUS=OK` 및 `manifest.status=OK` 확인.
2. 최소 1개의 실제 복습 이력 SQLite가 백업됐다면, 복원본에서 SQL 조회 성공 확인.
3. `state.json`, `sessions`, 개인 설정 파일의 보존 확인.
4. 가능하면 다른 물리 장치에 백업 한 벌 추가 보관(동일 SSD의 복제만으로 디스크 장애 대비 불가).
5. 운영 컨테이너의 실제 bind mount 및 볼륨 경로 확인 후 worktree만 선택 정리.
6. 비공개 DB, `.env`, 채점 답안, session/로그를 Git commit·PR·issue·채팅으로 업로드하지 않음.
