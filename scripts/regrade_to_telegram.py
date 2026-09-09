#!/usr/bin/env python3
"""Regrade stored OCR text and deliver the new result to Telegram.

This does not forge an incoming Telegram update.  It invokes the production
grading entrypoint directly, creates an isolated session, and uses only the
Bot API's outbound ``sendMessage`` operation.  The polling bot's state.json is
never read or written.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="현재 deterministic engine으로 OCR 답안을 재채점해 Telegram으로 전송"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--session-id", help="data/sessions 아래 기존 session ID")
    source.add_argument("--latest", action="store_true", help="가장 최근 일반 session 재채점")
    source.add_argument("--input", type=Path, help="직접 지정할 UTF-8 OCR 텍스트 파일")
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

    sessions_dir = args.sessions_dir.expanduser().resolve()
    sessions_dir.mkdir(parents=True, exist_ok=True)
    source_label: str
    if args.session_id:
        source_dir = resolve_source_session(sessions_dir, args.session_id)
        raw_text = read_session_input(source_dir)
        source_label = source_dir.name
    elif args.latest:
        source_dir = latest_source_session(sessions_dir)
        raw_text = read_session_input(source_dir)
        source_label = source_dir.name
    else:
        input_path = args.input.expanduser().resolve()
        if not input_path.is_file():
            raise FileNotFoundError(f"input file not found: {input_path}")
        raw_text = input_path.read_text(encoding="utf-8").strip()
        if not raw_text:
            raise ValueError("input file is empty")
        source_label = str(input_path)

    from grade_submission_normalizer import normalize_grade_submission
    from grading_agents import run_agent_pipeline
    import bot

    if not args.dry_run and not bot.TELEGRAM_TOKEN:
        raise SystemExit("TELEGRAM_TOKEN/TELEGRAM_BOT_TOKEN/BOT_TOKEN is required")
    if not bot.chat_allowed(args.chat_id):
        raise SystemExit("requested chat id is not authorized")

    session_dir = create_regrade_session(sessions_dir, args.chat_id)
    sid = session_dir.name
    normalized = normalize_grade_submission(raw_text)
    normalized_text = normalized["normalized_text"]
    (session_dir / "input.raw.txt").write_text(raw_text, encoding="utf-8")
    (session_dir / "input.normalized.txt").write_text(normalized_text, encoding="utf-8")
    (session_dir / "input.txt").write_text(normalized_text, encoding="utf-8")

    def forbidden_provider(_: str) -> str:
        raise RuntimeError("external provider call is forbidden during deterministic regrade")

    raw_result, grade = run_agent_pipeline(
        call_ollama_fn=forbidden_provider,
        raw_text=normalized_text,
        rubric={},
        sid=sid,
        image_count=0,
        session_dir=session_dir,
    )
    if grade.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
        raise RuntimeError("regrade did not use deterministic primary")
    if grade.get("provider_calls") != 0:
        raise RuntimeError("provider call count is not zero")

    grade["backend"] = "deterministic"
    grade["model"] = None
    (session_dir / "grade.json").write_text(
        json.dumps(grade, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (session_dir / "meta.json").write_text(
        json.dumps({
            "session_id": sid,
            "chat_id": args.chat_id,
            "status": "graded",
            "regrade_source": source_label,
            "provider_calls": 0,
            "graded_at": datetime.now().isoformat(timespec="seconds"),
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    rendered = bot.format_result(grade, raw_result)
    if args.dry_run:
        print(rendered)
        print(f"저장 위치: {session_dir}")
    else:
        bot.send_message(
            args.chat_id,
            "재채점을 시작합니다.\n"
            "채점 엔진: Deterministic Topic Pack + Engineering Ontology\n"
            f"원본 세션: {source_label}",
        )
        bot.send_message(args.chat_id, rendered)
        bot.send_message(
            args.chat_id,
            f"재채점 저장 위치: /workspace/prof_eng_answer/data/sessions/{sid}",
        )

    print(json.dumps({
        "marker": "TELEGRAM_DETERMINISTIC_REGRADE_V1",
        "decision": "PASS",
        "source": source_label,
        "session_id": sid,
        "telegram_sent": not args.dry_run,
        "provider_calls": 0,
        "total_score": grade.get("total_score"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
