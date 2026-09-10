#!/usr/bin/env python3
"""Regrade stored OCR text and deliver the new result to Telegram.

This does not forge an incoming Telegram update.  It invokes the production
grading entrypoint directly, creates an isolated session, and uses only the
Bot API's outbound ``sendMessage`` operation.  The polling bot's state.json is
never read or written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_SESSION_ID = re.compile(r"^[A-Za-z0-9_.-]+$")
_TRUE = {"1", "true", "yes", "on"}


def resolve_source_session(sessions_dir: Path, session_id: str) -> Path:
    if not _SESSION_ID.fullmatch(session_id):
        raise ValueError("session id contains unsupported characters")
    candidate = sessions_dir / session_id
    if not candidate.is_dir() or candidate.parent.resolve() != sessions_dir.resolve():
        raise FileNotFoundError(f"session not found: {session_id}")
    return candidate


def latest_source_session(sessions_dir: Path) -> Path:
    candidates = [
        path for path in sessions_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith("regrade_")
        and any((path / name).is_file() for name in ("input.raw.txt", "input.txt"))
    ]
    if not candidates:
        raise FileNotFoundError("no persisted session input was found")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def read_session_input(session_dir: Path) -> str:
    for name in ("input.raw.txt", "input.normalized.txt", "input.txt"):
        path = session_dir / name
        if path.is_file():
            value = path.read_text(encoding="utf-8").strip()
            if value:
                return value
    raise ValueError(f"session has no non-empty OCR input: {session_dir.name}")


def create_regrade_session(sessions_dir: Path, chat_id: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_chat = re.sub(r"[^0-9-]", "", str(chat_id)) or "unknown"
    base = f"regrade_{timestamp}_{safe_chat}"
    candidate = sessions_dir / base
    index = 1
    while candidate.exists():
        candidate = sessions_dir / f"{base}_{index}"
        index += 1
    candidate.mkdir(parents=True)
    return candidate


def build_copyable_submission(normalized_text: str) -> str:
    value = str(normalized_text or "").strip()
    if not value:
        raise ValueError("normalized submission is empty")
    return "[재채점 원문 — 복사용]\n/grade\n" + value + "\n끝."


def eligible_source_sessions(sessions_dir: Path) -> list[Path]:
    result = []
    for path in sorted(sessions_dir.iterdir()):
        if not path.is_dir() or path.name.startswith(("regrade_", "expert_accuracy_")):
            continue
        if not any((path / name).is_file() for name in ("input.raw.txt", "input.txt")):
            continue
        meta_path = path / "meta.json"
        if not meta_path.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        if meta.get("status") == "graded" and meta.get("chat_id") is not None:
            result.append(path)
    return result


def current_commit(root: Path) -> str:
    configured = str(os.getenv("ENGINE_COMMIT") or "").strip()
    if configured:
        return configured
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True, timeout=3,
        )
        if result.stdout.strip():
            return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass

    # Production containers intentionally omit .git.  A content fingerprint
    # keeps --resume scoped to the deployed engine and Topic Pack revision.
    digest = hashlib.sha256()
    excluded = {".git", "__pycache__", "data", "reports", "backups", "tmp", "tests"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in {".py", ".json", ".yaml", ".yml"}:
            continue
        if any(part in excluded for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        try:
            digest.update(path.read_bytes())
        except OSError:
            continue
    return "sha256:" + digest.hexdigest()


def completed_sources(
    sessions_dir: Path, engine_commit: str, *, include_dry_runs: bool = True
) -> set[str]:
    completed = set()
    for path in sessions_dir.glob("regrade_*/meta.json"):
        try:
            meta = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        if (
            meta.get("status") == "graded"
            and meta.get("provider_calls") == 0
            and meta.get("engine_commit") == engine_commit
            and meta.get("regrade_source")
            and (include_dry_runs or meta.get("dry_run") is False)
        ):
            completed.add(str(meta["regrade_source"]))
    return completed


def grade_signature(grade: dict | None) -> dict | None:
    if not isinstance(grade, dict):
        return None
    findings = (grade.get("logic_check_evaluation") or {}).get("findings") or []
    fatal_ids = sorted(
        str(row.get("rule_id") or row.get("finding_id") or row.get("defect_id"))
        for row in findings if isinstance(row, dict)
        and str(row.get("severity") or row.get("classification") or "").casefold()
        in {"fatal", "core_error"}
    )
    return {
        "total_score": grade.get("total_score"),
        "official_pass_met": grade.get("official_pass_met"),
        "high_score_met": grade.get("high_score_met"),
        "fatal_ids": fatal_ids,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="현재 deterministic engine으로 OCR 답안을 재채점해 Telegram으로 전송"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--session-id", help="data/sessions 아래 기존 session ID")
    source.add_argument("--latest", action="store_true", help="가장 최근 일반 session 재채점")
    source.add_argument("--input", type=Path, help="직접 지정할 UTF-8 OCR 텍스트 파일")
    source.add_argument("--all", action="store_true", help="저장된 실제 Telegram session 전체")
    parser.add_argument(
        "--chat-id",
        default=os.getenv("PROF_ENG_CHAT_ID", "").strip(),
        help="결과 수신 chat ID; 기본값은 PROF_ENG_CHAT_ID",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="채점·저장만 하고 Telegram으로 전송하지 않음",
    )
    parser.add_argument(
        "--no-source-text", action="store_true",
        help="Telegram 결과에서 복사용 원문 답안 표시를 생략",
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="현재 commit으로 이미 성공한 session을 건너뜀(--all 전용)",
    )
    parser.add_argument(
        "--changed-only", action="store_true",
        help="기존 grade와 핵심 판정이 달라진 결과만 Telegram 전송(--all 전용)",
    )
    parser.add_argument(
        "--send-summary", action="store_true",
        help="개별 답안 대신 batch 요약만 Telegram 전송(--all 전용)",
    )
    parser.add_argument(
        "--delay", type=float, default=5.0,
        help="batch 개별 전송 사이 대기 초(기본 5초)",
    )
    parser.add_argument("--report", type=Path, help="batch JSON report 경로")
    parser.add_argument(
        "--sessions-dir", type=Path, default=ROOT / "data" / "sessions",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if os.getenv("DETERMINISTIC_GRADING_PRIMARY", "").strip().lower() not in _TRUE:
        raise SystemExit("DETERMINISTIC_GRADING_PRIMARY=true is required")
    if not args.chat_id:
        raise SystemExit("--chat-id or PROF_ENG_CHAT_ID is required")

    if args.delay < 0:
        raise SystemExit("--delay must be zero or positive")
    if not args.all and (args.resume or args.changed_only or args.send_summary):
        raise SystemExit("--resume/--changed-only/--send-summary require --all")

    sessions_dir = args.sessions_dir.expanduser().resolve()
    sessions_dir.mkdir(parents=True, exist_ok=True)
    sources: list[tuple[str, str, Path | None]] = []
    if args.session_id:
        source_dir = resolve_source_session(sessions_dir, args.session_id)
        sources.append((source_dir.name, read_session_input(source_dir), source_dir))
    elif args.latest:
        source_dir = latest_source_session(sessions_dir)
        sources.append((source_dir.name, read_session_input(source_dir), source_dir))
    elif args.input:
        input_path = args.input.expanduser().resolve()
        if not input_path.is_file():
            raise FileNotFoundError(f"input file not found: {input_path}")
        raw_text = input_path.read_text(encoding="utf-8").strip()
        if not raw_text:
            raise ValueError("input file is empty")
        sources.append((str(input_path), raw_text, None))
    else:
        sources.extend(
            (path.name, read_session_input(path), path)
            for path in eligible_source_sessions(sessions_dir)
        )
        if not sources:
            raise SystemExit("no eligible graded Telegram sessions were found")

    from grade_submission_normalizer import normalize_grade_submission
    from grading_agents import run_agent_pipeline
    import bot

    if not args.dry_run and not bot.TELEGRAM_TOKEN:
        raise SystemExit("TELEGRAM_TOKEN/TELEGRAM_BOT_TOKEN/BOT_TOKEN is required")
    if not bot.chat_allowed(args.chat_id):
        raise SystemExit("requested chat id is not authorized")

    def forbidden_provider(_: str) -> str:
        raise RuntimeError("external provider call is forbidden during deterministic regrade")

    engine_commit = current_commit(ROOT)
    already_done = (
        completed_sources(
            sessions_dir, engine_commit, include_dry_runs=args.dry_run
        )
        if args.resume else set()
    )
    rows = []
    for index, (source_label, raw_text, source_dir) in enumerate(sources):
        if source_label in already_done:
            rows.append({"source": source_label, "status": "SKIPPED_RESUME"})
            continue
        try:
            session_dir = create_regrade_session(sessions_dir, args.chat_id)
            sid = session_dir.name
            normalized_text = normalize_grade_submission(raw_text)["normalized_text"]
            for name, value in (
                ("input.raw.txt", raw_text),
                ("input.normalized.txt", normalized_text),
                ("input.txt", normalized_text),
            ):
                (session_dir / name).write_text(value, encoding="utf-8")
            raw_result, grade = run_agent_pipeline(
                call_ollama_fn=forbidden_provider, raw_text=normalized_text,
                rubric={}, sid=sid, image_count=0, session_dir=session_dir,
            )
            if grade.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
                raise RuntimeError("regrade did not use deterministic primary")
            if grade.get("provider_calls") != 0:
                raise RuntimeError("provider call count is not zero")
            grade["backend"], grade["model"] = "deterministic", None
            old_grade = None
            if source_dir and (source_dir / "grade.json").is_file():
                old_grade = json.loads((source_dir / "grade.json").read_text(encoding="utf-8"))
            changed = grade_signature(old_grade) != grade_signature(grade)
            should_send = not args.dry_run and not args.send_summary and (
                not args.changed_only or changed
            )
            (session_dir / "grade.json").write_text(
                json.dumps(grade, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            meta = {
                "session_id": sid, "chat_id": args.chat_id, "status": "graded",
                "regrade_source": source_label, "provider_calls": 0,
                "engine_commit": engine_commit, "changed": changed,
                "dry_run": args.dry_run, "telegram_sent": should_send,
                "graded_at": datetime.now().isoformat(timespec="seconds"),
            }
            (session_dir / "meta.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            copyable = None if args.no_source_text else build_copyable_submission(normalized_text)
            rendered = bot.format_result(grade, raw_result)
            if should_send:
                bot.send_message(args.chat_id, f"재채점 원본 세션: {source_label}")
                if copyable:
                    bot.send_message(args.chat_id, copyable)
                bot.send_message(args.chat_id, rendered)
                bot.send_message(
                    args.chat_id,
                    f"재채점 저장 위치: /workspace/prof_eng_answer/data/sessions/{sid}",
                )
                if index + 1 < len(sources) and args.delay:
                    time.sleep(args.delay)
            elif args.dry_run and not args.all:
                if copyable:
                    print(copyable + "\n")
                print(rendered)
                print(f"저장 위치: {session_dir}")
            rows.append({
                "source": source_label, "status": "PASS", "session_id": sid,
                "changed": changed, "telegram_sent": should_send,
                "total_score": grade.get("total_score"), "provider_calls": 0,
            })
        except Exception as error:
            rows.append({
                "source": source_label, "status": "FAIL",
                "error": f"{type(error).__name__}: {error}",
            })

    passed = sum(row["status"] == "PASS" for row in rows)
    skipped = sum(row["status"] == "SKIPPED_RESUME" for row in rows)
    failed = sum(row["status"] == "FAIL" for row in rows)
    changed_count = sum(row.get("changed") is True for row in rows)
    report = {
        "marker": "TELEGRAM_DETERMINISTIC_REGRADE_BATCH_V1" if args.all else "TELEGRAM_DETERMINISTIC_REGRADE_V1",
        "decision": "PASS" if failed == 0 else "FAIL",
        "engine_commit": engine_commit, "selected": len(sources),
        "passed": passed, "skipped": skipped, "failed": failed,
        "changed": changed_count, "provider_calls": 0, "cases": rows,
    }
    report_path = args.report
    if args.all and report_path is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = ROOT / "reports" / "telegram_regrade_batches" / f"{stamp}.json"
    if report_path:
        report_path = report_path.expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        report["report_path"] = str(report_path)
    if args.send_summary and not args.dry_run:
        bot.send_message(
            args.chat_id,
            "전체 재채점 완료\n"
            f"선택 {len(sources)} · 성공 {passed} · 재개건너뜀 {skipped} · 실패 {failed}\n"
            f"기존 판정 대비 변경 {changed_count} · provider 호출 0\n"
            f"보고서: {report.get('report_path', '미지정')}",
        )
    print(json.dumps(report, ensure_ascii=False))
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
