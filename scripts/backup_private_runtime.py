#!/usr/bin/env python3
"""Private, online backup of the prof_eng_answer runtime (never GitHub data).

Usage:
  python3 -B scripts/backup_private_runtime.py
  python3 -B scripts/backup_private_runtime.py --backup-root /home/now0930/hermes/private_backups/prof_eng_answer

All paths default to the host's home-directory installation. This tool never
stops containers, reads Docker credentials, changes source files, or uploads data.
SQLite databases are snapshotted with sqlite3.Connection.backup(), not cp.
Other live files are best-effort copies, not a filesystem-atomic snapshot.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import uuid

DB_SUFFIXES = (".sqlite3", ".sqlite", ".db", ".db3")
DB_SIDECAR = re.compile(r"(?i).*\.(?:sqlite3?|db3?)-(?:wal|shm|journal)$")
PRUNE_NAMES = {".git", ".venv", "venv", "__pycache__", "node_modules", "private_backups"}
DB_ENV_NAMES = {
    "TRAINING_HISTORY_DB",
    "PRIVATE_SEMANTIC_CACHE_DB",
    "PRIVATE_SEMANTIC_CACHE_PATH",
    "SEMANTIC_CACHE_DB",
    "SEMANTIC_CACHE_PATH",
}


def is_db(path: Path) -> bool:
    return path.name.lower().endswith(DB_SUFFIXES)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def db_files(directory: Path, *, exclude_backups: bool = False):
    if not directory.is_dir() or directory.is_symlink():
        return
    for parent, folders, files in os.walk(directory, topdown=True, followlinks=False):
        folders[:] = [
            name for name in folders
            if not (Path(parent) / name).is_symlink()
            and name not in PRUNE_NAMES
            and not name.startswith("private_deploy_backup_")
            and (not exclude_backups or "backup" not in name.lower())
        ]
        for name in files:
            candidate = Path(parent) / name
            if is_db(candidate) and candidate.is_file() and not candidate.is_symlink():
                yield candidate.resolve()


def copy_directory(source: Path, destination: Path, skipped: list[str]) -> None:
    if not source.is_dir():
        return

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored: set[str] = set()
        for name in names:
            path = Path(directory) / name
            if path.is_symlink():
                ignored.add(name)
                skipped.append(str(path))
            elif path.is_file() and (is_db(path) or DB_SIDECAR.fullmatch(name)):
                ignored.add(name)
        return ignored

    shutil.copytree(source, destination, ignore=ignore, dirs_exist_ok=False)
    for path in destination.rglob("*"):
        if path.is_dir():
            path.chmod(0o700)
        elif path.is_file():
            path.chmod(0o600)


def read_configured_sqlite_paths(configs: list[Path], repo: Path, home: Path) -> set[Path]:
    result: set[Path] = set()
    for config in configs:
        if not config.is_file():
            continue
        for line in config.read_text(encoding="utf-8", errors="replace").splitlines():
            key, sep, value = line.strip().removeprefix("export ").partition("=")
            if not sep or key.strip() not in DB_ENV_NAMES:
                continue
            value = value.strip().strip("\"'")
            if not value or "$" in value or "://" in value:
                continue
            if value.startswith("/workspace/prof_eng_answer/"):
                candidate = repo / value.removeprefix("/workspace/prof_eng_answer/")
            elif value.startswith("/hermes_home/"):
                candidate = home / "hermes" / "hermes_home" / value.removeprefix("/hermes_home/")
            else:
                candidate = Path(value).expanduser()
                if not candidate.is_absolute():
                    candidate = repo / candidate
            if is_db(candidate) and candidate.is_file() and not candidate.is_symlink():
                result.add(candidate.resolve())
    return result


def sqlite_snapshot(source: Path, target: Path) -> None:
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with closing(sqlite3.connect(str(source), timeout=60)) as src:
        src.execute("PRAGMA busy_timeout=60000")
        with closing(sqlite3.connect(str(target), timeout=60)) as dst:
            src.backup(dst, pages=256, sleep=0.2)
            # Backup copies the source WAL journal mode into the destination.
            # Switch ONLY the independent backup to a single-file journal mode:
            # a later read-only quick_check must not create -wal/-shm sidecars.
            mode = dst.execute("PRAGMA journal_mode=DELETE").fetchone()
            if not mode or str(mode[0]).lower() != "delete":
                raise RuntimeError(f"SQLite backup journal mode was not normalized: {target}")
    target.chmod(0o600)
    with sqlite3.connect(f"file:{target.as_posix()}?mode=ro", uri=True) as check:
        result = check.execute("PRAGMA quick_check").fetchone()
        if not result or result[0] != "ok":
            raise RuntimeError(f"SQLite quick_check failed: {source}")


def backup(repo: Path, backup_root: Path, home: Path) -> Path:
    if not (repo / "data").is_dir():
        raise RuntimeError(f"expected project data directory is missing: {repo / 'data'}")
    if backup_root.resolve().is_relative_to(repo.resolve()):
        raise RuntimeError("backup destination must be outside the project repository")
    backup_root.mkdir(parents=True, mode=0o700, exist_ok=True)
    backup_root.chmod(0o700)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = backup_root / f"{stamp}_{uuid.uuid4().hex[:8]}"
    destination.mkdir(mode=0o700)

    manifest: dict = {
        "schema_version": "private_runtime_backup_v1",
        "created_at_utc": stamp,
        "source_repo": str(repo),
        "destination": str(destination),
        "status": "INCOMPLETE",
        "copied_directories": [],
        "configs": [],
        "sqlite_databases": [],
        "skipped_symlinks": [],
        "notes": [
            "SQLite snapshots are online and checked with PRAGMA quick_check.",
            "JSON/session, report, WordPress document, and log files are live best-effort copies.",
            "Docker /opt/data and unrelated MySQL/Postgres services are not included.",
            "Never commit, paste or upload this private directory to GitHub.",
        ],
    }
    manifest_path = destination / "manifest.json"
    configs = [
        (home / "hermes" / ".env", "hermes.env"),
        (home / "hermes" / "workspace" / ".env", "workspace.env"),
        (repo / ".env", "repository.env"),
        (home / "hermes" / "docker-compose.yml", "hermes-compose.yml"),
    ]
    try:
        for name in ("data", "logs", "reports", "wordpress_docs"):
            source = repo / name
            if not source.is_dir():
                continue
            copy_directory(source, destination / "runtime" / name, manifest["skipped_symlinks"])
            manifest["copied_directories"].append(str(source))

        config_sources: list[Path] = []
        for src, name in configs:
            if not src.is_file() or src.is_symlink():
                continue
            target = destination / "config" / name
            target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            shutil.copyfile(src, target)
            target.chmod(0o600)
            manifest["configs"].append({"source": str(src), "backup": str(target.relative_to(destination)),
                                         "sha256": file_digest(target)})
            config_sources.append(src)

        identified: dict[Path, tuple[str, Path]] = {}
        for name in ("data", "logs", "reports", "wordpress_docs"):
            for path in db_files(repo / name):
                identified[path] = (f"runtime/{name}", repo / name)
        external_roots = [
            ("external/chatgpt_project", home / "chatgpt_project"),
            ("external/hermes_home", home / "hermes" / "hermes_home"),
        ]
        for label, root in external_roots:
            for path in db_files(root, exclude_backups=True):
                identified.setdefault(path, (label, root))

        for path in read_configured_sqlite_paths(config_sources, repo, home):
            if path not in identified:
                identified[path] = ("configured", path.parent)

        for source, (label, root) in sorted(identified.items(), key=lambda item: str(item[0])):
            relative = source.relative_to(root)
            target = destination / label / relative
            sqlite_snapshot(source, target)
            manifest["sqlite_databases"].append({
                "source": str(source),
                "backup": str(target.relative_to(destination)),
                "bytes": target.stat().st_size,
                "sha256": file_digest(target),
                "quick_check": "ok",
            })

        state = destination / "runtime" / "data" / "state.json"
        if state.is_file():
            json.loads(state.read_text(encoding="utf-8"))
            manifest["state_json_valid"] = True

        manifest["status"] = "OK"
    except Exception as error:
        manifest["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        # Restrict even directories implicitly created by copytree/mkdir on hosts
        # where this function is called without the CLI's umask.
        for item in destination.rglob("*"):
            if item.is_symlink():
                continue
            if item.is_dir():
                item.chmod(0o700)
            elif item.is_file():
                item.chmod(0o600)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest_path.chmod(0o600)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    home = Path.home()
    parser.add_argument("--repo", type=Path, default=home / "hermes/workspace/prof_eng_answer")
    parser.add_argument("--backup-root", type=Path,
                        default=home / "hermes/private_backups/prof_eng_answer")
    args = parser.parse_args()
    os.umask(0o077)
    try:
        path = backup(args.repo.expanduser().resolve(), args.backup_root.expanduser().resolve(), home)
    except Exception as error:
        print(f"BACKUP_STATUS=FAILED ({type(error).__name__}: {error})", file=sys.stderr)
        return 1
    print("BACKUP_STATUS=OK")
    print(f"BACKUP_DIR={path}")
    print(f"MANIFEST={path / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
