"""Run approved V6 edits through Aider and local Inkling."""

import subprocess

from ai_backends import EditBackend
from validator import validate_edit


def prepare_executor(env):
    if any(name in env for name in ("V6_EDITOR_COMMAND", "V6_OLLAMA_EDIT_MODEL")):
        raise ValueError("V6 editing uses Aider + Inkling; unset alternate editor settings")
    backend = EditBackend(None)
    backend.preflight()
    return backend


def execute_tasks(ctx, executor, tasks, compiled, original_head, original_index):
    root, repo, run_dir = ctx.root, ctx.repo, ctx.run_dir
    snapshot, backup, run, stop = ctx.snapshot, ctx.backup, ctx.run, ctx.stop
    for number, task in enumerate(tasks, 1):
        print(f"\n[작업 {number}/{len(tasks)}]", flush=True)

        files = task["files"]
        before = snapshot()
        backup(f"task_{number}_before")

        item = compiled[number - 1]
        target = repo / item["target"]

        if target.read_bytes().decode("utf-8") != item["before"]:
            stop("V6: source changed since preflight")

        instruction = item["prompt"]

        task_file = run_dir / f"task_{number}.md"
        task_file.write_text(instruction, encoding="utf-8")
        log = run_dir / f"aider_{number}.log"

        try:
            cmd, cwd = executor.command(task_file, files, root, repo)
            code = run(cmd, log, cwd=cwd)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            stop(f"AI 코드 수정 실행 실패: {exc}")
        backup(f"task_{number}_after")

        if code != 0:
            stop(f"AI 코드 수정 종료 코드: {code}")

        validate_edit(ctx, files, target, item, log, before, original_head, original_index)
        print(f"[작업 {number}] 코드 수정 및 변경 범위 검사 통과")
