"""Generate V6 plans through the external planner or reuse approved JSON."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from ai_backends import PlanBackend


def prepare_plan(args, ctx, original_head, original_index):
    root, repo, run_dir, env = ctx.root, ctx.repo, ctx.run_dir, ctx.env
    git, snapshot, stop = ctx.git, ctx.snapshot, ctx.stop
    plan_path = run_dir / "plan.json"
    if args[0] == "--plan":
        paths = [value for value in args[1:] if value != "--compile-only"]
        source = Path(paths[0]) if paths else root / "plan.json"
        plan_path.write_bytes(source.read_bytes())
        print("[1] 기존 plan.json 재사용: Copilot 호출 없음")

    else:
        try:
            if env.get("V6_OLLAMA_PLAN_MODEL") is not None or env.get("V6_OLLAMA_PLAN_CONTEXT") is not None:
                raise ValueError("V6 planning requires an external provider")
            planner = PlanBackend.from_env(env)
            selected = None
            if planner.argv is not None:
                paths = json.loads(env.get("V6_EXTERNAL_PLAN_CONTEXT", "[]"))
                if (
                    not isinstance(paths, list)
                    or not paths
                    or any(not isinstance(path, str) or not path for path in paths)
                ):
                    raise ValueError("V6_EXTERNAL_PLAN_CONTEXT must list approved tracked files")
                selected = set(paths)
        except (OSError, ValueError) as exc:
            stop(f"Planner setup failed: {exc}")

        intent = " ".join(
            x for x in args
            if x != "--compile-only"
        )

        prompt = """
        You are a read-only development planner.

        User objective:
        """ + intent + """

        Inspect relevant repository files.
        Identify the root cause.
        Design the implementation.
        Select files and execution order.

        Never modify files or run shell commands.
        Use existing tracked Python or JSON files only.
        One writable file per task.
        Use exact existing function names or JSON keys.
        SEARCH must match exactly once.
        Both SEARCH and REPLACE must end with a newline.
        Maximum 8 edits per task.
        Do not include read_files or allow_no_change.
        Preserve scoring weights and Fact approval policy.
        Do not weaken existing tests.
        Do not hardcode individual answers.
        Return JSON only, without Markdown.

        Required schema:
        {
          "schema_version": "inkling_plan_v6",
          "objective": "objective",
          "analysis": {
            "root_cause": "verified cause",
            "inspected_files": ["relative path"]
          },
          "tasks": [
            {
              "id": 1,
              "files": ["existing file"],
              "target_symbols": ["existing symbol"],
              "instruction": "implementation",
              "edits": [
                {
                  "search": "exact old source",
                  "replace": "exact new source"
                }
              ],
              "acceptance": ["acceptance condition"],
              "test_files": ["tests/existing_test.py"]
            }
          ]
        }
        """

        before_planner = snapshot()

        print("[1] AI 관련 파일 분석 및 계획 작성", flush=True)

        with tempfile.TemporaryDirectory(
            prefix="planner_v6_"
        ) as directory:

            workspace = Path(directory)

            roots = {
                "grading", "rubrics", "master_topic_packs",
                "tests", "scripts", "tools",
                "calibration", "schemas"
            }

            copied = 0

            for raw in git("ls-files", "-z").split(b"\0"):
                if not raw:
                    continue

                relative = Path(os.fsdecode(raw))
                src = repo / relative
                if selected is not None and relative.as_posix() not in selected:
                    continue

                if relative.parts[0] not in roots:
                    continue

                if src.suffix not in {
                    ".py", ".json", ".yaml", ".yml", ".md", ".toml"
                }:
                    continue

                if not src.is_file() or src.is_symlink():
                    continue

                if not src.resolve().is_relative_to(repo.resolve()):
                    continue

                dst = workspace / relative
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
                if selected is not None:
                    selected.remove(relative.as_posix())

            if selected:
                stop(f"외부 계획에 사용할 수 없는 경로: {sorted(selected)}")

            print(f"AI 분석 대상: {copied}개", flush=True)

            try:
                result = planner.run(prompt, workspace, run_dir, env)
            except subprocess.TimeoutExpired:
                stop("AI 계획 실행 시간 제한 초과")
            except OSError as exc:
                stop(f"AI 계획 실행 실패: {exc}")

            if result.returncode != 0:
                stop(f"AI 계획 실행 실패: {planner.stderr_name} 확인")

        if snapshot() != before_planner:
            stop("AI 분석 중 원본 변경 감지")

        if git("rev-parse", "HEAD") != original_head:
            stop("HEAD 변경 감지")

        if git("diff", "--cached", "--binary") != original_index:
            stop("index 변경 감지")

        try:
            generated = json.loads(
                (run_dir / planner.stdout_name).read_text()
            )
            assert generated["schema_version"] == "inkling_plan_v6"
            assert isinstance(generated["tasks"], list)
            assert generated["tasks"]

            plan_path.write_text(
                json.dumps(generated, ensure_ascii=False, indent=2)
            )

        except Exception as exc:
            stop(f"AI 계획 형식 오류: {exc}")

        print("AI 개발 계획 생성 완료", flush=True)
    return plan_path
