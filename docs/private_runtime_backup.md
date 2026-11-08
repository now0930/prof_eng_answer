# 비공개 운영 데이터 백업 및 복원 점검

운영 기준: `~/hermes/workspace/prof_eng_answer` (GitHub `main`).
Codex 테스트 기준: `~/codex/pro_engineer`. 실제 비공개 파일을 GitHub에 올리지 않는다.

## 보호 대상

`scripts/backup_private_runtime.py`는 서버 호스트에서 실행하며 다음을 별도 개인
백업 폴더로 복사한다.

- `prof_eng_answer/data/`: Telegram `state.json`, 저장 답안/이미지 `sessions/`,
  복습 이력과 설정. 루트 디렉터리 안의 모든 하위 폴더(심볼릭 링크 제외).
- `prof_eng_answer/logs/`: 운영 로그가 존재할 때 포함.
- `~/hermes/.env`, `~/hermes/workspace/.env`, 저장소의 `.env` 및
  `~/codex/pro_engineer/.env`: 존재하는 파일만 포함.
- `~/hermes/docker-compose.yml`: 배포 설정.
- `data/`, `logs/` 안의 `*.sqlite3`, `*.sqlite`, `*.db`, `*.db3`:
  raw copy가 아닌 SQLite online backup을 사용. WAL이 열려 있는 상태에서도
  커밋된 트랜잭션의 일관된 snapshot을 취한 뒤 `PRAGMA quick_check` 확인.
- 추가 SQLite DB 탐색: `~/chatgpt_project/` (기존 `private_backups` 제외),
  `~/hermes/hermes_home/`, 운영 `.env`에 명시된 일부 DB 파일 경로.

**포함되지 않는 범위**: `/opt/data`에 마운트된 Hermes Agent Docker 볼륨,
WordPress/Immich 등 별도 MySQL/MariaDB/PostgreSQL 서비스,
`~/codex/pro_engineer`의 프로젝트 전체 복제,
기존 `private_deploy_backup_*` 백업과 이미 생성된 비공개 백업들.
별도 서비스 DB는 그 서비스의 `mysqldump`/`pg_dump` 및 볼륨 전략으로
백업해야 하며 이 스크립트가 이를 백업했다고 주장하지 않는다.

## 백업 절차 (운영 컨테이너 중지 없음)

운영 코드가 아직 옛 커밋에 있어도, GitHub의 **스크립트만** 실행하면 된다.
코드를 설치하거나 `git pull` 할 필요는 없다.

```bash
set -euo pipefail
cd ~/hermes/workspace/prof_eng_answer

git fetch origin main
git show origin/main:scripts/backup_private_runtime.py |
  python3 -B -
```

기본 저장 위치는
`~/chatgpt_project/private_backups/prof_eng_answer/<UTC>_<random>/`이다.

별도 SSD에 저장하려면:

```bash
git show origin/main:scripts/backup_private_runtime.py |
  python3 -B - --backup-root /mnt/ExtSSD1/private_backups/prof_eng_answer
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
`runtime/data` 및 해당 DB 백업을 원본의 상대 경로에 되돌린다.
복원 전에는 기존 운영 data를 보존하고, 원본 백업 스냅샷을 수정하지 않는다.

현재 스크립트는 **실시간 JSON과 세션 파일 전체의 원자적 스냅샷을 보장하지는 않는다**.
엄밀한 일관성 복원 점검이 필요할 때는 서비스 정지 후 두 번째 콜드 백업을
수행하고, 별도 디렉터리에서 복원 테스트를 완료한다.

## 디렉터리 정리 전 절대 조건

1. `BACKUP_STATUS=OK` 및 `manifest.status=OK` 확인.
2. 최소 1개의 실제 복습 이력 SQLite가 백업됐다면, 복원본에서 SQL 조회 성공 확인.
3. `state.json`, `sessions`, 개인 설정 파일의 보존 확인.
4. 가능하면 다른 물리 장치에 백업 한 벌 추가 보관(동일 SSD의 복제만으로 디스크 장애 대비 불가).
5. 운영 컨테이너의 실제 bind mount 및 볼륨 경로 확인 후 worktree만 선택 정리.
6. 비공개 DB, `.env`, 채점 답안, session/로그를 Git commit·PR·issue·채팅으로 업로드하지 않음.
