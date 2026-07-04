#!/usr/bin/env python3
"""
Run the topic_pack release validation suite.

This is the one-command release gate for topic pack changes.

It runs:
  1. py_compile for rubric manager and topic-pack helper scripts
  2. validate-generated-pipeline
  3. validate-topic-pack-quality
  4. smoke-topic-pack for every topic pack, or selected topic ids
  5. cleanup of synthetic smoke sessions and smoke report unless --keep-artifacts

Examples:

  python3 scripts/validate_topic_pack_release.py

  python3 scripts/rubric_manager.py validate-topic-pack-release

  python3 scripts/rubric_manager.py validate-topic-pack-release \
    --topic-id second_order_lag_response_by_damping_ratio

  python3 scripts/rubric_manager.py validate-topic-pack-release \
    --strict-generic-aliases \
    --require-logic-check
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SMOKE_SESSION_PREFIX = "synthetic_topic_pack_smoke_"
SMOKE_REPORT = Path("reports/rubric_bank_mode_smoke_compare.json")


def _project_root() -> Path:
    here = Path(__file__).resolve()
    candidates = [
        here.parents[1],
        Path.cwd(),
        Path("/workspace/prof_eng_answer"),
    ]

    for candidate in candidates:
        if (candidate / "rubrics" / "topic_packs").exists():
            return candidate

    raise SystemExit("ERROR: project root not found. Run from prof_eng_answer repo.")


def _topic_ids(root: Path, selected: list[str] | None) -> list[str]:
    if selected:
        missing = [
            topic_id
            for topic_id in selected
            if not (root / "rubrics" / "topic_packs" / topic_id).is_dir()
        ]
        if missing:
            raise SystemExit(f"ERROR: topic pack not found: {missing}")
        return selected

    base = root / "rubrics" / "topic_packs"
    topic_ids = sorted(path.name for path in base.iterdir() if path.is_dir())

    if not topic_ids:
        raise SystemExit(f"ERROR: no topic packs found under {base}")

    return topic_ids


def _run(root: Path, cmd: list[str], *, allow_failure: bool = False) -> int:
    print()
    print("RUN:", " ".join(cmd))

    proc = subprocess.run(cmd, cwd=root, text=True)

    if proc.returncode != 0 and not allow_failure:
        raise SystemExit(proc.returncode)

    return proc.returncode


def _compile_targets(root: Path) -> list[str]:
    candidates = [
        "scripts/rubric_manager.py",
        "scripts/create_topic_pack.py",
        "scripts/smoke_topic_pack.py",
        "scripts/validate_topic_pack_quality.py",
        "scripts/validate_topic_pack_release.py",
        "scripts/validate_topic_packs.py",
        "scripts/build_generated_rubrics.py",
        "scripts/validate_generated_rubrics.py",
        "rubric_bank_paths.py",
        "rubric_registry.py",
        "grading_agents.py",
        "logic_check_evaluator.py",
        "difficulty_strategy.py",
        "difficulty_output_adapter.py",
        "grade_score_reconciler.py",
    ]

    return [path for path in candidates if (root / path).exists()]


def _cleanup_synthetic_sessions(root: Path) -> int:
    sessions_dir = root / "data" / "sessions"
    if not sessions_dir.exists():
        return 0

    count = 0
    for path in sessions_dir.iterdir():
        if path.is_dir() and path.name.startswith(SMOKE_SESSION_PREFIX):
            import shutil

            shutil.rmtree(path)
            count += 1

    return count


def _is_git_tracked(root: Path, rel_path: Path) -> bool:
    proc = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(rel_path)],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return proc.returncode == 0


def _cleanup_smoke_report(root: Path) -> str:
    report_path = root / SMOKE_REPORT

    if not report_path.exists():
        return "not_found"

    if _is_git_tracked(root, SMOKE_REPORT):
        proc = subprocess.run(
            ["git", "restore", "--", str(SMOKE_REPORT)],
            cwd=root,
            text=True,
        )
        if proc.returncode == 0:
            return "restored_tracked"
        return "restore_failed"

    report_path.unlink()
    return "removed_untracked"


def _cleanup_artifacts(root: Path) -> dict[str, object]:
    removed_sessions = _cleanup_synthetic_sessions(root)
    report_status = _cleanup_smoke_report(root)

    return {
        "removed_synthetic_sessions": removed_sessions,
        "smoke_report": report_status,
    }


def _smoke_cmd(args: argparse.Namespace, topic_id: str) -> list[str]:
    cmd = [
        sys.executable,
        "scripts/rubric_manager.py",
        "smoke-topic-pack",
        "--topic-id",
        topic_id,
        "--min-gap",
        str(args.min_gap),
        "--min-ratio",
        str(args.min_ratio),
    ]

    if args.require_logic_check:
        cmd.append("--require-logic-check")

    return cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run release validation for topic packs.")
    parser.add_argument(
        "--topic-id",
        action="append",
        default=None,
        help="validate only this topic id; can be repeated",
    )
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="skip smoke-topic-pack checks",
    )
    parser.add_argument(
        "--keep-artifacts",
        action="store_true",
        help="keep synthetic sessions and smoke report",
    )
    parser.add_argument(
        "--strict-generic-aliases",
        action="store_true",
        help="pass through to validate-topic-pack-quality",
    )
    parser.add_argument(
        "--require-logic-check",
        action="store_true",
        help="pass through to quality and smoke checks",
    )
    parser.add_argument(
        "--min-gap",
        type=float,
        default=30.0,
        help="minimum primary-second candidate score gap for smoke-topic-pack",
    )
    parser.add_argument(
        "--min-ratio",
        type=float,
        default=1.2,
        help="minimum primary/second candidate score ratio for smoke-topic-pack",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root = _project_root()
    topics = _topic_ids(root, args.topic_id)

    print("TOPIC PACK RELEASE VALIDATION")
    print("root:", root)
    print("topics:", len(topics))
    for topic_id in topics:
        print(" -", topic_id)

    compile_targets = _compile_targets(root)
    _run(root, [sys.executable, "-m", "py_compile", *compile_targets])

    _run(root, [sys.executable, "scripts/rubric_manager.py", "validate-generated-pipeline"])

    quality_cmd = [
        sys.executable,
        "scripts/rubric_manager.py",
        "validate-topic-pack-quality",
    ]

    for topic_id in args.topic_id or []:
        quality_cmd.extend(["--topic-id", topic_id])

    if args.strict_generic_aliases:
        quality_cmd.append("--strict-generic-aliases")

    if args.require_logic_check:
        quality_cmd.append("--require-logic-check")

    _run(root, quality_cmd)

    smoke_results: list[tuple[str, int]] = []

    if not args.skip_smoke:
        for topic_id in topics:
            rc = _run(root, _smoke_cmd(args, topic_id), allow_failure=True)
            smoke_results.append((topic_id, rc))
            if rc != 0:
                print()
                print("TOPIC PACK RELEASE VALIDATION FAILED")
                print("failed smoke topic:", topic_id)
                if not args.keep_artifacts:
                    cleanup = _cleanup_artifacts(root)
                    print("cleanup:", cleanup)
                return rc

    cleanup = {}
    if not args.keep_artifacts:
        cleanup = _cleanup_artifacts(root)

    print()
    print("TOPIC PACK RELEASE SUMMARY")
    print("generated_pipeline: PASS")
    print("quality: PASS")

    if args.skip_smoke:
        print("smoke: SKIPPED")
    else:
        print("smoke: PASS")
        for topic_id, rc in smoke_results:
            status = "PASS" if rc == 0 else "FAIL"
            print(f" - {topic_id}: {status}")

    if cleanup:
        print("cleanup:", cleanup)

    print()
    print("TOPIC PACK RELEASE VALIDATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
