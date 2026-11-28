"""Shared per-run paths, subprocess logging, and grading repository snapshots."""

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys


@dataclass
class RunContext:
    root: Path
    repo: Path
    python: Path
    run_dir: Path
    env: dict

    def stop(self, message):
        print(f"\n[중단] {message}", flush=True)
        print(f"로그 위치: {self.run_dir}", flush=True)
        sys.exit(1)

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-C", str(self.repo), *args]
        )

    def run(self, cmd, log, cwd=None):
        print("\n실행:", " ".join(map(str, cmd)), flush=True)
        with open(log, "w") as out:
            proc = subprocess.Popen(
                list(map(str, cmd)),
                cwd=self.root if cwd is None else cwd,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
            )
            for line in proc.stdout:
                print(line, end="", flush=True)
                out.write(line)
                out.flush()
            return proc.wait()

    def snapshot(self):
        result = {}
        rows = self.git(
            "status", "--porcelain=v1", "-z",
            "--untracked-files=all", "--no-renames"
        ).split(b"\0")

        for row in rows:
            if not row:
                continue

            name = os.fsdecode(row[3:])
            path = self.repo / name

            if path.is_symlink():
                content = os.readlink(path).encode()
            elif path.is_file():
                content = path.read_bytes()
            else:
                content = b""

            result[name] = (
                row[:2],
                hashlib.sha256(content).hexdigest()
            )

        return result

    def backup(self, prefix):
        (self.run_dir / f"{prefix}.patch").write_bytes(
            self.git("diff", "HEAD", "--binary")
        )
        (self.run_dir / f"{prefix}_staged.patch").write_bytes(
            self.git("diff", "--cached", "--binary")
        )
        (self.run_dir / f"{prefix}_status.txt").write_bytes(
            self.git("status", "--short")
        )
