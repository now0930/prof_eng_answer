"""Provider adapters for the V6 planner and editor contracts."""

import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass


def configured_command(env, name):
    if name not in env:
        return None
    try:
        argv = json.loads(env[name])
    except json.JSONDecodeError as exc:
        raise ValueError(f"{name} must be a JSON argument array") from exc
    if (
        not isinstance(argv, list)
        or not argv
        or any(not isinstance(arg, str) or not arg or "\0" in arg for arg in argv)
    ):
        raise ValueError(f"{name} must be a nonempty JSON array of strings")
    executable = shutil.which(argv[0], path=env.get("PATH"))
    if executable is None:
        raise ValueError(f"Executable for {name} is unavailable")
    return [os.path.abspath(executable), *argv[1:]]


def ollama_command(env, role, argv):
    prefix = f"V6_OLLAMA_{role.upper()}"
    model = env.get(f"{prefix}_MODEL")
    if model is None:
        return argv
    if argv is not None or not model.strip():
        raise ValueError(f"Select one nonempty {role} backend")
    adapter = Path(__file__).with_name("ollama_backend.py").resolve()
    command = [sys.executable, str(adapter), role, "--model", model]
    if role == "plan":
        try:
            paths = json.loads(env.get("V6_OLLAMA_PLAN_CONTEXT", "[]"))
        except json.JSONDecodeError as exc:
            raise ValueError("V6_OLLAMA_PLAN_CONTEXT must be a JSON path array") from exc
        if (
            not isinstance(paths, list)
            or not paths
            or any(not isinstance(path, str) or not path for path in paths)
        ):
            raise ValueError("V6_OLLAMA_PLAN_CONTEXT must be a nonempty JSON path array")
        for path in paths:
            command.extend(["--context", path])
    return command


@dataclass
class PlanBackend:
    argv: list[str] | None

    @classmethod
    def from_env(cls, env):
        argv = ollama_command(env, "plan", configured_command(env, "V6_PLANNER_COMMAND"))
        if argv is None:
            if env.get("COPILOT_FREE_CONFIRMED") != "1":
                raise ValueError("Copilot 추가 과금 차단 확인 필요")
            if not shutil.which("copilot", path=env.get("PATH")):
                raise ValueError("Copilot CLI 없음")
        return cls(argv)

    @property
    def stdout_name(self):
        return "planner_raw.txt" if self.argv else "copilot_raw.txt"

    @property
    def stderr_name(self):
        return "planner_stderr.log" if self.argv else "copilot_stderr.log"

    def run(self, prompt, workspace, run_dir, env):
        cmd = self.argv or [
            "copilot",
            "--available-tools=view,grep,glob",
            "--allow-tool=read",
            "--deny-tool=write,shell",
            "--no-ask-user",
            "--silent",
            "-p", prompt,
        ]
        with (run_dir / self.stdout_name).open("wb") as out:
            with (run_dir / self.stderr_name).open("wb") as err:
                return subprocess.run(
                    cmd,
                    input=prompt.encode("utf-8") if self.argv else None,
                    cwd=workspace,
                    stdout=out,
                    stderr=err,
                    env=env,
                    timeout=900,
                )


@dataclass
class EditBackend:
    argv: list[str] | None

    @classmethod
    def from_env(cls, env):
        return cls(ollama_command(env, "edit", configured_command(env, "V6_EDITOR_COMMAND")))

    def preflight(self):
        if self.argv is None:
            try:
                with socket.create_connection(("127.0.0.1", 11435), timeout=3):
                    pass
            except OSError as exc:
                raise ValueError("Inkling 프록시 11435가 실행 중이 아닙니다.") from exc

    def command(self, task_file, files, root, repo):
        if self.argv is not None:
            return [*self.argv, str(task_file), *files], repo

        existing = subprocess.check_output([
            "docker", "ps", "-a", "-q",
            "--filter", "name=^/aider_batch$"
        ]).strip()

        if existing:
            raise ValueError("기존 aider_batch 컨테이너가 존재합니다.")

        cmd = [
            "docker", "compose", "run", "--rm", "-T",
            "--name", "aider_batch",
            "-v", f"{task_file}:/app/task.md:ro",
            "-e", "OLLAMA_API_BASE=http://127.0.0.1:11435",
            "-e", "PYTHONUNBUFFERED=1",
            "--entrypoint", "/bin/sh",
            "aider_inkling",
            "-c", 'exec timeout 3600 aider "$@"',
            "sh",
            "--model", "ollama_chat/inkling-2-mini-aider",
            "--weak-model", "ollama_chat/inkling-2-mini-aider",
            "--model-settings-file", "/app/.aider.model.settings.yml",
            "--map-tokens", "0",
            "--max-chat-history-tokens", "3072",
            "--no-auto-commits",
            "--no-dirty-commits",
            "--no-gitignore",
            "--no-auto-lint",
            "--no-auto-test",
            "--no-suggest-shell-commands",
            "--no-pretty",
            "--no-stream",
            "--yes-always",
            "--message-file", "/app/task.md",
        ]

        for name in files:
            cmd.extend(["--file", name])

        return cmd, root
