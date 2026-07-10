#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SESSION = ROOT / "data" / "sessions" / "20260627_213430_5960502198"


def run_mode(mode: str, session_dir: Path) -> dict[str, Any]:
    env = os.environ.copy()
    env["RUBRIC_BANK_MODE"] = mode
    env.setdefault("OLLAMA_TIMEOUT", "90")

    code = r'''
import json
from pathlib import Path

import bot as bot_module
from rubric_bank_paths import get_rubric_bank_report

ROOT = Path(__ROOT__)
session_dir = Path(__SESSION_DIR__)
input_path = session_dir / "input.txt"

if not input_path.exists():
    raise SystemExit(f"ERROR: input.txt not found: {input_path}")


def patch_bot_paths() -> None:
    """Force bot.py runtime paths to this local checkout for smoke tests."""
    data_dir = ROOT / "data"
    sessions_dir = data_dir / "sessions"
    logs_dir = ROOT / "logs"

    if hasattr(bot_module, "BASE_DIR"):
        bot_module.BASE_DIR = ROOT
    if hasattr(bot_module, "ROOT"):
        bot_module.ROOT = ROOT
    if hasattr(bot_module, "PROJECT_ROOT"):
        bot_module.PROJECT_ROOT = ROOT

    if hasattr(bot_module, "DATA_DIR"):
        bot_module.DATA_DIR = data_dir
    if hasattr(bot_module, "SESSIONS_DIR"):
        bot_module.SESSIONS_DIR = sessions_dir
    if hasattr(bot_module, "SESSION_DIR"):
        bot_module.SESSION_DIR = sessions_dir

    if hasattr(bot_module, "LOG_DIR"):
        bot_module.LOG_DIR = logs_dir
    if hasattr(bot_module, "LOGS_DIR"):
        bot_module.LOGS_DIR = logs_dir

    # Preserve existing filename if the variable exists.
    for attr in ["STATE_FILE", "STATE_PATH"]:
        if hasattr(bot_module, attr):
            old = getattr(bot_module, attr)
            try:
                filename = Path(old).name
            except Exception:
                filename = "state.json"
            setattr(bot_module, attr, data_dir / filename)

    for attr in ["CONFIG_FILE", "CONFIG_PATH"]:
        if hasattr(bot_module, attr):
            old = getattr(bot_module, attr)
            try:
                filename = Path(old).name
            except Exception:
                filename = "config.json"
            setattr(bot_module, attr, ROOT / filename)

    # Generic remap for legacy absolute paths embedded in bot.py.
    # Example:
    # /workspace/prof_eng_answer/rubrics/default.json
    # -> <current checkout>/rubrics/default.json
    legacy_root = Path("/workspace/prof_eng_answer")

    for attr, value in list(vars(bot_module).items()):
        if isinstance(value, Path):
            try:
                rel = value.relative_to(legacy_root)
            except Exception:
                continue
            setattr(bot_module, attr, ROOT / rel)

    for attr, value in list(vars(bot_module).items()):
        if isinstance(value, str) and value.startswith(str(legacy_root)):
            rel = value[len(str(legacy_root)):].lstrip("/")
            setattr(bot_module, attr, str(ROOT / rel))


patch_bot_paths()

raw_text = input_path.read_text(encoding="utf-8")
state = bot_module.load_state()

import time

smoke_user_id = (
    909000000001 if __MODE__ == "legacy" else 909000000002
) + int(time.time() * 1000) % 100000000

# Avoid reusing an existing active session from bot state.
for key in [
    str(smoke_user_id),
    smoke_user_id,
]:
    if isinstance(state, dict):
        state.pop(key, None)

for key in [
    "current_sessions",
    "sessions",
    "active_sessions",
]:
    if isinstance(state, dict) and isinstance(state.get(key), dict):
        state[key].pop(str(smoke_user_id), None)
        state[key].pop(smoke_user_id, None)

sid, raw_result, parsed = bot_module.grade_answer(smoke_user_id, raw_text, state)

summary = {
    "mode": __MODE__,
    "new_session": sid,
    "rubric_bank_report": get_rubric_bank_report(),
    "total_score": parsed.get("total_score"),
    "final_total_score": parsed.get("final_total_score"),
    "pre_ceiling_total_score": parsed.get("pre_ceiling_total_score"),
    "score_range": parsed.get("score_range"),
    "question_type": parsed.get("question_type"),
    "topic_id": (
        parsed.get("difficulty_strategy", {}).get("topic_id")
        or parsed.get("fact_anchor_evaluation", {}).get("topic_id")
        or parsed.get("model_answer_reference", {}).get("topic_id")
        or parsed.get("model_answer_reference", {}).get("primary_reference", {}).get("topic_id")
    ),
    "model_answer_reference": parsed.get("model_answer_reference"),
    "logic_check": (
        parsed.get("logic_check_evaluation")
        or parsed.get("logic_check_result")
        or parsed.get("logic_check")
    ),
    "logic_check_evaluation": (
        parsed.get("logic_check_evaluation")
        or parsed.get("logic_check_result")
        or parsed.get("logic_check")
    ),
    "logic_check_topic_id": (
        parsed.get("logic_check_topic_id")
        or (
            parsed.get(
                "logic_check_evaluation",
                {},
            ).get("topic_id")
            if isinstance(
                parsed.get(
                    "logic_check_evaluation"
                ),
                dict,
            )
            else None
        )
    ),
    "difficulty_strategy": parsed.get("difficulty_strategy"),
    "difficulty_ceiling_evaluation": parsed.get("difficulty_ceiling_evaluation"),
    "llm_cap_reconciliation": (
        parsed.get("difficulty_ceiling_evaluation", {}).get("llm_cap_reconciliation")
        if isinstance(parsed.get("difficulty_ceiling_evaluation"), dict)
        else None
    ),
}

print("SMOKE_RESULT_JSON=" + json.dumps(summary, ensure_ascii=False))
'''
    code = code.replace("__ROOT__", repr(str(ROOT)))
    code = code.replace("__SESSION_DIR__", repr(str(session_dir)))
    code = code.replace("__MODE__", repr(mode))

    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(ROOT),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(f"\n===== RUBRIC_BANK_MODE={mode} raw output =====")
    print(proc.stdout)

    if proc.returncode != 0:
        raise SystemExit(f"ERROR: mode={mode} failed with rc={proc.returncode}")

    result_line = None
    for line in proc.stdout.splitlines():
        if line.startswith("SMOKE_RESULT_JSON="):
            result_line = line.split("=", 1)[1]

    if not result_line:
        raise SystemExit(f"ERROR: mode={mode} did not emit SMOKE_RESULT_JSON")

    return json.loads(result_line)


def main() -> int:
    session_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SESSION

    if not session_dir.exists():
        raise SystemExit(f"ERROR: session dir not found: {session_dir}")

    legacy = run_mode("legacy", session_dir)
    generated = run_mode("generated", session_dir)

    report = {
        "session_dir": str(session_dir),
        "legacy": legacy,
        "generated": generated,
        "comparison": {
            "legacy_total_score": legacy.get("total_score"),
            "generated_total_score": generated.get("total_score"),
            "legacy_question_type": legacy.get("question_type"),
            "generated_question_type": generated.get("question_type"),
            "legacy_topic_id": legacy.get("topic_id"),
            "generated_topic_id": generated.get("topic_id"),
            "legacy_session": legacy.get("new_session"),
            "generated_session": generated.get("new_session"),
        },
    }

    out_dir = ROOT / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "rubric_bank_mode_smoke_compare.json"
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\n===== SUMMARY =====")
    print(json.dumps(report["comparison"], ensure_ascii=False, indent=2))
    print(f"\nwrote: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
