#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from topic_pack_status import iter_topic_ids, load_status, project_root, topic_pack_dir, update_status, write_status  # noqa: E402


SMOKE_SESSION_PREFIX = "synthetic_topic_pack_smoke_"
SMOKE_REPORT = Path("reports/rubric_bank_mode_smoke_compare.json")


def _topic_ids(root: Path, selected: list[str] | None, *, changed_only: bool, include_frozen: bool) -> list[str]:
    topic_ids = selected or iter_topic_ids(root)
    missing = [tid for tid in topic_ids if not topic_pack_dir(root, tid).is_dir()]
    if missing:
        raise SystemExit(f"ERROR: topic pack not found: {missing}")

    if not changed_only:
        return topic_ids

    result: list[str] = []
    for topic_id in topic_ids:
        status = load_status(topic_pack_dir(root, topic_id), topic_id)
        if not status.get("_changed"):
            print("SKIP unchanged:", topic_id)
            continue
        if not include_frozen and status.get("status") == "frozen" and not status.get("_changed"):
            print("SKIP frozen unchanged:", topic_id)
            continue
        result.append(topic_id)
    return result


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
        "scripts/topic_pack_status.py",
        "scripts/review_topic_pack.py",
        "scripts/review_topic_pack_all.py",
        "scripts/topic_review_llm.py",
        "scripts/validate_topic_packs.py",
        "scripts/build_generated_rubrics.py",
        "scripts/validate_generated_rubrics.py",
        "rubric_bank_paths.py",
        "rubric_registry.py",
        "grading_agents.py",
        "logic_check_evaluator.py",
        "logic_llm_verifier.py",
        "difficulty_strategy.py",
        "difficulty_output_adapter.py",
        "grade_score_reconciler.py",
    ]
    return [p for p in candidates if (root / p).exists()]


def _snapshot_generated(root: Path) -> dict[Path, bytes]:
    generated_dir = root / "rubrics" / "generated"
    if not generated_dir.exists():
        return {}
    return {p.relative_to(root): p.read_bytes() for p in sorted(generated_dir.glob("*.json"))}


def _restore_generated(root: Path, snapshot: dict[Path, bytes]) -> None:
    generated_dir = root / "rubrics" / "generated"
    current = {p.relative_to(root) for p in generated_dir.glob("*.json")} if generated_dir.exists() else set()
    original = set(snapshot)

    for rel in current - original:
        (root / rel).unlink()
        print("removed generated temp:", rel)

    for rel, data in snapshot.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print("restored generated:", rel)


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
    proc = subprocess.run(["git", "ls-files", "--error-unmatch", str(rel_path)], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc.returncode == 0


def _cleanup_smoke_report(root: Path) -> str:
    report = root / SMOKE_REPORT
    if not report.exists():
        return "not_found"
    if _is_git_tracked(root, SMOKE_REPORT):
        proc = subprocess.run(["git", "restore", "--", str(SMOKE_REPORT)], cwd=root)
        return "restored_tracked" if proc.returncode == 0 else "restore_failed"
    report.unlink()
    return "removed_untracked"


def _cleanup_artifacts(root: Path) -> dict[str, object]:
    return {"removed_synthetic_sessions": _cleanup_synthetic_sessions(root), "smoke_report": _cleanup_smoke_report(root)}


def _smoke_cmd(args: argparse.Namespace, topic_id: str) -> list[str]:
    cmd = [sys.executable, "scripts/rubric_manager.py", "smoke-topic-pack", "--topic-id", topic_id, "--min-gap", str(args.min_gap), "--min-ratio", str(args.min_ratio)]
    if args.require_logic_check:
        cmd.append("--require-logic-check")
    return cmd


def _mark_validated(root: Path, topics: list[str]) -> None:
    for topic_id in topics:
        pack_dir = topic_pack_dir(root, topic_id)
        status = load_status(pack_dir, topic_id)
        status = update_status(status, sync_hash=True, mark_validated=True)
        write_status(pack_dir, status)
        print("updated validated status:", pack_dir / "topic_status.json")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run release validation for topic packs.")
    p.add_argument("--topic-id", action="append", default=None)
    p.add_argument("--changed-only", action="store_true", help="smoke only changed topic packs")
    p.add_argument("--include-frozen", action="store_true")
    p.add_argument("--skip-smoke", action="store_true")
    p.add_argument("--keep-artifacts", action="store_true")
    p.add_argument("--promote-generated", action="store_true", help="leave rubrics/generated changes in the worktree")
    p.add_argument("--sync-status", action="store_true", help="mark validated topic hashes after successful validation")
    p.add_argument("--strict-generic-aliases", action="store_true")
    p.add_argument("--require-logic-check", action="store_true")
    p.add_argument("--min-gap", type=float, default=30.0)
    p.add_argument("--min-ratio", type=float, default=1.2)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = project_root()
    topics = _topic_ids(root, args.topic_id, changed_only=args.changed_only, include_frozen=args.include_frozen)

    print("TOPIC PACK RELEASE VALIDATION")
    print("root:", root)
    print("topics:", len(topics))
    for topic_id in topics:
        print(" -", topic_id)

    generated_snapshot = _snapshot_generated(root)

    try:
        _run(root, [sys.executable, "-m", "py_compile", *_compile_targets(root)])
        _run(root, [sys.executable, "scripts/rubric_manager.py", "validate-generated-pipeline"])

        quality_cmd = [sys.executable, "scripts/rubric_manager.py", "validate-topic-pack-quality"]
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
                        print("cleanup:", _cleanup_artifacts(root))
                    return rc

        cleanup = {}
        if not args.keep_artifacts:
            cleanup = _cleanup_artifacts(root)

        if args.sync_status:
            _mark_validated(root, topics)

        print()
        print("TOPIC PACK RELEASE SUMMARY")
        print("generated_pipeline: PASS")
        print("quality: PASS")
        if args.skip_smoke:
            print("smoke: SKIPPED")
        else:
            print("smoke: PASS")
            for topic_id, rc in smoke_results:
                print(f" - {topic_id}: {'PASS' if rc == 0 else 'FAIL'}")
        if cleanup:
            print("cleanup:", cleanup)
        print()
        print("TOPIC PACK RELEASE VALIDATION PASS")
        return 0

    finally:
        if args.promote_generated:
            print()
            print("generated output: promoted in worktree")
        else:
            print()
            print("generated output: restoring pre-validation snapshot")
            _restore_generated(root, generated_snapshot)


if __name__ == "__main__":
    raise SystemExit(main())
