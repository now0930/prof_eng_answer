"""Entry point for the V6 plan, compile, approve, edit, and validate workflow."""

from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

from compiler import compile_plan
from executor import execute_tasks, prepare_executor
from planner import prepare_plan
from run_context import RunContext
from validator import Validation, compiler_diagnostics


def main(args):
    root = Path(__file__).resolve().parent
    repo = root / "repo"
    python = Path.home() / "hermes/validation/.venv-xdist/bin/python"
    if args and args[0] == "--diagnose":
        os.execv(str(python), [str(python), "-B", str(root / "develop.py"), "--diagnose-worker"])
    if args and args[0] == "--diagnose-worker":
        compiler_diagnostics(root, repo)
        return

    run_dir = root / "runs" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    run_dir.mkdir(parents=True)
    env = os.environ.copy()
    env["CURRENT_UID"] = str(os.getuid())
    env["CURRENT_GID"] = str(os.getgid())
    ctx = RunContext(root, repo, python, run_dir, env)
    with (root / ".develop.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            ctx.stop("다른 develop 작업이 실행 중입니다.")
        develop(args, ctx)


def develop(args, ctx):
    if not args:
        ctx.stop('사용법: ./develop.sh "개발 의도" 또는 --plan')
    if not ctx.python.is_file():
        ctx.stop("기존 pytest 가상환경을 찾을 수 없습니다.")

    compile_only = "--compile-only" in args
    if not compile_only:
        try:
            executor = prepare_executor(ctx.env)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            ctx.stop(f"Editor setup failed: {exc}")

    ctx.backup("before")
    original_head = ctx.git("rev-parse", "HEAD")
    original_index = ctx.git("diff", "--cached", "--binary")
    plan_path = prepare_plan(args, ctx, original_head, original_index)
    plan, tasks, compiled = compile_plan(plan_path, ctx.repo, ctx.git, ctx.stop)
    print("V6 exact-edit preflight PASS")

    if compile_only:
        for number, item in enumerate(compiled, 1):
            (ctx.run_dir / f"compiled_{number}.md").write_text(item["prompt"], encoding="utf-8")
        print("Compile-only: no code edit, no grade, no pytest")
        print(f"로그 위치: {ctx.run_dir}")
        return

    print("\n[2] 작업 계획")
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if any(len(task["files"]) > 1 for task in tasks):
        print("\n주의: 여러 파일을 수정하는 작업이 포함되어 있습니다.")
    if input("\nAider + Inkling 코드 수정을 시작할까요? [y/N]: ").strip().lower() != "y":
        ctx.stop("사용자가 실행을 취소했습니다.")

    validation = Validation(ctx, plan)
    validation.before()
    execute_tasks(ctx, executor, tasks, compiled, original_head, original_index)
    validation.after()

    print("\n========================================")
    print("전체 계획 실행 및 pytest 검증 통과")
    print("자동 커밋 및 Push 없음")
    print(f"실행 기록: {ctx.run_dir}")
    print("========================================")
    print(ctx.git("diff", "--stat").decode(errors="replace"))


if __name__ == "__main__":
    main(sys.argv[1:])
