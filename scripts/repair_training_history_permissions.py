#!/usr/bin/env python3
"""Back up private runtime data, then repair the Bot's learning DB permissions.

Plan by default. Run --apply as root on the host; this does not stop the Bot.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import sqlite3
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_private_runtime import backup, file_digest


def check_compose(compose: Path) -> None:
    text = compose.read_text(encoding="utf-8")
    match = re.search(r"^  prof-eng-answer-bot:\s*\n(?P<body>.*?)(?=^  [\w-]+:|^networks:|\Z)",
                      text, flags=re.MULTILINE | re.DOTALL)
    if not match or not re.search(r'^\s+user:\s*["\']?1001:1001["\']?\s*$',
                                  match.group("body"), flags=re.MULTILINE):
        raise RuntimeError("Compose Bot service user is not 1001:1001")
    env = compose.parent / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
            key, sep, value = line.strip().removeprefix("export ").partition("=")
            if sep and key.strip() == "TRAINING_HISTORY_DB" and value.strip():
                raise RuntimeError("TRAINING_HISTORY_DB override exists; inspect its path before repair")


def backup_verified(destination: Path, source: Path) -> None:
    manifest = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "OK":
        raise RuntimeError("private runtime backup is not complete")
    records = [entry for entry in manifest.get("sqlite_databases", [])
               if entry.get("source") == str(source)]
    if len(records) != 1 or records[0].get("quick_check") != "ok":
        raise RuntimeError("learning DB backup is absent or failed quick_check")
    snapshot = destination / records[0]["backup"]
    if not snapshot.is_file() or file_digest(snapshot) != records[0]["sha256"]:
        raise RuntimeError("learning DB backup hash mismatch")
    with sqlite3.connect(f"file:{snapshot.as_posix()}?mode=ro", uri=True) as connection:
        if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise RuntimeError("learning DB backup failed restore-read check")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--backup-root", type=Path, required=True)
    parser.add_argument("--compose", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    backup_root = args.backup_root.resolve()
    compose = args.compose.resolve()
    owner_home = repo.parents[2]
    owner = pwd.getpwnam("now0930")
    if (owner.pw_uid, owner.pw_gid) != (1001, 1001):
        raise RuntimeError("now0930 UID/GID does not match Compose Bot user")
    if repo != owner_home / "hermes/workspace/prof_eng_answer":
        raise RuntimeError("unexpected operational repository path")
    if backup_root != owner_home / "hermes/private_backups/prof_eng_answer":
        raise RuntimeError("backup root is not the agreed private backup location")
    if compose != owner_home / "hermes/docker-compose.yml":
        raise RuntimeError("unexpected Compose path")
    check_compose(compose)
    data = repo / "data"
    db = data / "training_history.sqlite3"
    if not db.is_file() or db.is_symlink():
        raise RuntimeError("learning DB is missing or is a symlink")
    data_stat = data.stat()
    if (data_stat.st_uid, data_stat.st_gid) != (1001, 1001):
        raise RuntimeError("data directory owner does not match Bot user")
    parts = [db]
    for suffix in ("-wal", "-shm", "-journal"):
        sidecar = Path(str(db) + suffix)
        if sidecar.exists() or sidecar.is_symlink():
            if not sidecar.is_file() or sidecar.is_symlink():
                raise RuntimeError(f"unexpected SQLite sidecar: {sidecar}")
            parts.append(sidecar)
    for path in parts:
        st = path.stat()
        print("PLAN_FILE", path, "uid=", st.st_uid, "gid=", st.st_gid,
              "mode=", oct(st.st_mode & 0o777))
    if not args.apply:
        print("PLAN_ONLY_NO_CHANGES")
        return 0
    if os.geteuid() != 0:
        raise RuntimeError("--apply requires the host root account")
    if not shutil.which("setfacl") or not shutil.which("getfacl"):
        raise RuntimeError("setfacl/getfacl are required for read-only Codex access")

    destination = backup(repo, backup_root, owner_home)
    backup_verified(destination, db)
    metadata = {str(p): {"uid": p.stat().st_uid, "gid": p.stat().st_gid,
                         "mode": p.stat().st_mode & 0o777} for p in parts}
    record = destination / "permission_repair_before.json"
    record.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    record.chmod(0o600)
    for current, dirs, files in os.walk(destination):
        os.chown(current, owner.pw_uid, owner.pw_gid)
        os.chmod(current, 0o700)
        for name in files:
            path = Path(current) / name
            if path.is_symlink():
                raise RuntimeError(f"unexpected symlink in backup: {path}")
            os.chown(path, owner.pw_uid, owner.pw_gid)
            os.chmod(path, 0o600)
    print("BACKUP_STATUS=OK")
    print(f"BACKUP_DIR={destination}")

    for path in parts:
        os.chown(path, owner.pw_uid, owner.pw_gid)
        os.chmod(path, 0o660)
        subprocess.run(["setfacl", "-m", "u:codex_now0930:r--", str(path)], check=True)
        st = path.stat()
        acl = subprocess.run(["getfacl", "-cp", str(path)], check=True,
                             capture_output=True, text=True).stdout
        if ((st.st_uid, st.st_gid) != (1001, 1001)
                or (st.st_mode & 0o600) != 0o600
                or (st.st_mode & 0o007) != 0
                or "user:codex_now0930:r--" not in acl):
            raise RuntimeError(f"permission repair verification failed: {path}")
    print("TRAINING_DB_PERMISSIONS_OK")
    print("CODEX_READ_ACL_OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"REPAIR_FAILED ({type(error).__name__}: {error})", file=sys.stderr)
        raise SystemExit(1)
