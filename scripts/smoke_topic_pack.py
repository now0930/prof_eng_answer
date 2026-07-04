#!/usr/bin/env python3
"""
Smoke-test a topic_pack routing path.

This script creates a synthetic session from an existing base session, rewrites
its text/json payloads with a topic-specific question and answer, runs
scripts/smoke_compare_rubric_bank_modes.py, and validates generated-mode routing.

Checks:
  - generated model_answer_reference.primary_reference.topic_id == --topic-id
  - generated difficulty_strategy.topic_id == --topic-id
  - generated logic_check_evaluation.topic_id == --topic-id when available
  - primary candidate score gap passes configured thresholds

Examples:

  python3 scripts/smoke_topic_pack.py \
    --topic-id second_order_system_resonance_frequency_response

  python3 scripts/rubric_manager.py smoke-topic-pack \
    --topic-id second_order_system_resonance_frequency_response
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_BASE_SESSION = Path("data/sessions/20260627_213430_5960502198")
DEFAULT_TMP_SESSION_PREFIX = "synthetic_topic_pack_smoke"


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


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_topic_pack(root: Path, topic_id: str) -> dict[str, Any]:
    pack_dir = root / "rubrics" / "topic_packs" / topic_id
    if not pack_dir.exists():
        raise SystemExit(f"ERROR: topic pack not found: {pack_dir}")

    model_answer_path = pack_dir / "model_answer.json"
    if not model_answer_path.exists():
        raise SystemExit(f"ERROR: model_answer.json not found: {model_answer_path}")

    model_answer = _read_json(model_answer_path)

    logic_check = {}
    logic_check_path = pack_dir / "logic_check.json"
    if logic_check_path.exists():
        logic_check = _read_json(logic_check_path)

    return {
        "pack_dir": pack_dir,
        "model_answer": model_answer,
        "logic_check": logic_check,
    }


def _first_non_empty(values: list[Any], default: str = "") -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return default


def _list_strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return []


def _outline_items(model_answer: dict[str, Any]) -> list[str]:
    outline = model_answer.get("model_answer_outline")
    if isinstance(outline, list):
        items = _list_strings(outline)
        if items:
            return items

    recommended = model_answer.get("recommended_outline")
    if isinstance(recommended, dict):
        intents = _list_strings(recommended.get("intents"))
        if intents:
            return intents

        sections = _list_strings(recommended.get("sections"))
        if sections:
            return sections

    high_score_points = _list_strings(model_answer.get("high_score_points"))
    if high_score_points:
        return high_score_points

    high_score_features = _list_strings(model_answer.get("high_score_features"))
    if high_score_features:
        return high_score_features

    return []


def _question_from_model_answer(model_answer: dict[str, Any]) -> str:
    examples = _list_strings(model_answer.get("question_examples"))
    if examples:
        return examples[0]

    expected_patterns = _list_strings(model_answer.get("expected_question_patterns"))
    if expected_patterns:
        return expected_patterns[0]

    title = _first_non_empty([
        model_answer.get("title"),
        model_answer.get("title_ko"),
        model_answer.get("name"),
        model_answer.get("topic_id"),
    ], "topic pack smoke question")

    return f"{title}에 대해 설명하시오."


def _answer_from_model_answer(model_answer: dict[str, Any], question: str) -> str:
    title = _first_non_empty([
        model_answer.get("title"),
        model_answer.get("title_ko"),
        model_answer.get("name"),
        model_answer.get("topic_id"),
    ], "Topic Pack Smoke")

    high_score_points = _list_strings(model_answer.get("high_score_points"))
    if not high_score_points:
        high_score_points = _list_strings(model_answer.get("high_score_features"))

    field_points = _list_strings(model_answer.get("routing_field_points"))
    if not field_points:
        field_points = _list_strings(model_answer.get("field_connection_points"))

    missing_points = _list_strings(model_answer.get("common_missing_points"))
    if not missing_points:
        missing_points = _list_strings(model_answer.get("low_score_patterns"))

    outline_items = _outline_items(model_answer)

    lines: list[str] = [
        question,
        "",
        "## 1. 개요",
        f"{title}은 기술사 답안에서 개념, 원리, 판단 조건, 현장 적용성을 함께 설명해야 하는 주제이다.",
        "",
        "## 2. 핵심 내용",
    ]

    if outline_items:
        for idx, item in enumerate(outline_items[:8], start=1):
            lines.append(f"{idx}. {item}")
    else:
        lines.append("1. 핵심 정의와 적용 범위를 설명한다.")
        lines.append("2. 주요 원리와 판단 조건을 설명한다.")
        lines.append("3. 현장 적용성과 한계를 연결한다.")

    if high_score_points:
        lines.extend(["", "## 3. 고득점 판단 기준"])
        for idx, item in enumerate(high_score_points[:8], start=1):
            lines.append(f"{idx}. {item}")

    if field_points:
        lines.extend(["", "## 4. 현장 연결 및 키워드"])
        lines.append(", ".join(field_points[:20]))

    if missing_points:
        lines.extend(["", "## 5. 주의할 오류"])
        for idx, item in enumerate(missing_points[:5], start=1):
            lines.append(f"{idx}. {item}")

    lines.extend([
        "",
        "## 6. 결론",
        f"{title} 답안은 단순 키워드 나열이 아니라 fact, 판단 기준, 현장 적용, 오류 방지를 함께 제시해야 한다.",
    ])

    return "\n".join(lines).strip() + "\n"


def _find_base_session(root: Path, explicit: str | None) -> Path:
    if explicit:
        path = root / explicit if not Path(explicit).is_absolute() else Path(explicit)
        if not path.exists():
            raise SystemExit(f"ERROR: base session not found: {path}")
        return path

    default = root / DEFAULT_BASE_SESSION
    if default.exists():
        return default

    sessions_dir = root / "data" / "sessions"
    if not sessions_dir.exists():
        raise SystemExit(f"ERROR: sessions dir not found: {sessions_dir}")

    candidates = [
        p for p in sessions_dir.iterdir()
        if p.is_dir() and (p / "input.txt").exists()
    ]

    if not candidates:
        raise SystemExit(f"ERROR: no usable base session found under {sessions_dir}")

    return max(candidates, key=lambda p: p.stat().st_mtime)


def _clean_synthetic_sessions(root: Path, topic_id: str) -> None:
    sessions_dir = root / "data" / "sessions"
    if not sessions_dir.exists():
        return

    prefix = f"{DEFAULT_TMP_SESSION_PREFIX}_{topic_id}"
    for path in sessions_dir.iterdir():
        if path.is_dir() and path.name.startswith(prefix):
            shutil.rmtree(path)


def _make_target_session(root: Path, base_session: Path, topic_id: str, keep: bool) -> Path:
    sessions_dir = root / "data" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    if not keep:
        _clean_synthetic_sessions(root, topic_id)

    target = sessions_dir / f"{DEFAULT_TMP_SESSION_PREFIX}_{topic_id}"

    if target.exists():
        shutil.rmtree(target)

    shutil.copytree(base_session, target)
    return target


def _replace_in_obj(obj: Any, question: str, answer: str, topic_id: str) -> Any:
    if isinstance(obj, dict):
        updated: dict[str, Any] = {}
        for key, value in obj.items():
            key_lower = str(key).lower()

            if key_lower in {
                "input",
                "input_text",
                "text",
                "answer",
                "answer_text",
                "student_answer",
                "raw_text",
                "ocr_text",
                "content",
                "prompt",
            }:
                updated[key] = answer
            elif key_lower in {
                "question",
                "question_text",
                "problem",
                "exam_question",
            }:
                updated[key] = question
            elif key_lower in {"topic_id", "inferred_topic_id", "logic_check_topic_id"}:
                updated[key] = topic_id
            else:
                updated[key] = _replace_in_obj(value, question, answer, topic_id)
        return updated

    if isinstance(obj, list):
        return [_replace_in_obj(item, question, answer, topic_id) for item in obj]

    if isinstance(obj, str):
        if len(obj) > 500 and ("##" in obj or "감쇠비" in obj or "2차" in obj):
            return answer
        return obj

    return obj


def _rewrite_session_payload(target_session: Path, question: str, answer: str, topic_id: str) -> int:
    rewritten = 0

    canonical_text_files = [
        "input.txt",
        "prompt.txt",
        "evidence_prompt.txt",
        "question_analysis_prompt.txt",
        "question_analysis_raw.txt",
        "evidence_raw.txt",
    ]

    for name in canonical_text_files:
        path = target_session / name
        if path.exists():
            path.write_text(answer, encoding="utf-8")
            rewritten += 1

    for path in target_session.rglob("*.json"):
        try:
            data = _read_json(path)
        except Exception:
            continue

        data = _replace_in_obj(data, question, answer, topic_id)
        _write_json(path, data)
        rewritten += 1

    # Ensure a clean minimal input exists even if the base was unusual.
    input_path = target_session / "input.txt"
    input_path.write_text(answer, encoding="utf-8")

    return rewritten


def _run_smoke_compare(root: Path, target_session: Path) -> dict[str, Any]:
    cmd = [
        sys.executable,
        "scripts/smoke_compare_rubric_bank_modes.py",
        str(target_session),
    ]

    print()
    print("RUN:", " ".join(cmd))

    env = os.environ.copy()
    proc = subprocess.run(
        cmd,
        cwd=root,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    print(proc.stdout)

    if proc.returncode != 0:
        raise SystemExit(proc.returncode)

    report_path = root / "reports" / "rubric_bank_mode_smoke_compare.json"
    if not report_path.exists():
        raise SystemExit(f"ERROR: smoke report not found: {report_path}")

    return _read_json(report_path)


def _candidate_score_and_topic(candidate: dict[str, Any]) -> tuple[float, str | None]:
    score = candidate.get("score")
    try:
        score_value = float(score)
    except Exception:
        score_value = 0.0

    answer = candidate.get("answer") or {}
    topic = answer.get("topic_id") if isinstance(answer, dict) else None

    return score_value, topic


def _validate_generated_result(
    report: dict[str, Any],
    topic_id: str,
    min_gap: float,
    min_ratio: float,
    require_logic_check: bool,
) -> dict[str, Any]:
    generated = report.get("generated") or {}

    ref = generated.get("model_answer_reference") or {}
    primary = ref.get("primary_reference") or {}
    candidates = ref.get("candidates") or []

    primary_topic = primary.get("topic_id") if isinstance(primary, dict) else None

    difficulty = generated.get("difficulty_strategy") or {}
    difficulty_topic = difficulty.get("topic_id") if isinstance(difficulty, dict) else None

    logic_eval = generated.get("logic_check_evaluation") or {}
    logic_topic = logic_eval.get("topic_id") if isinstance(logic_eval, dict) else None

    if not logic_topic:
        # Some smoke reports do not lift logic_check_evaluation into the summary.
        # In that case accept missing logic topic unless explicitly required.
        logic_topic = generated.get("logic_check_topic_id")

    if logic_topic == topic_id:
        logic_status = "matched"
    elif logic_topic:
        logic_status = "mismatch"
    else:
        logic_status = "missing_optional"

    candidate_summary = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        score, candidate_topic = _candidate_score_and_topic(candidate)
        candidate_summary.append(
            {
                "score": score,
                "topic_id": candidate_topic,
            }
        )

    primary_score = candidate_summary[0]["score"] if candidate_summary else 0.0
    second_score = candidate_summary[1]["score"] if len(candidate_summary) >= 2 else 0.0
    gap = primary_score - second_score
    ratio = (primary_score / second_score) if second_score > 0 else float("inf")

    failures: list[str] = []

    if primary_topic != topic_id:
        failures.append(f"primary topic mismatch: expected={topic_id}, actual={primary_topic}")

    if difficulty_topic != topic_id:
        failures.append(f"difficulty topic mismatch: expected={topic_id}, actual={difficulty_topic}")

    # Logic checks are optional by design. Easy topics may not have a logic_check
    # profile. However, if a logic topic is present, it must match the routed topic.
    if logic_topic and logic_topic != topic_id:
        failures.append(f"logic check topic mismatch: expected={topic_id}, actual={logic_topic}")
    elif require_logic_check and logic_topic != topic_id:
        failures.append(f"logic check topic required but missing: expected={topic_id}, actual={logic_topic}")

    if candidate_summary and candidate_summary[0].get("topic_id") != topic_id:
        failures.append(
            "top candidate topic mismatch: "
            f"expected={topic_id}, actual={candidate_summary[0].get('topic_id')}"
        )

    if gap < min_gap:
        failures.append(f"candidate score gap too small: gap={gap}, min_gap={min_gap}")

    if ratio < min_ratio:
        failures.append(f"candidate score ratio too small: ratio={ratio:.3f}, min_ratio={min_ratio}")

    return {
        "passed": not failures,
        "failures": failures,
        "primary_topic": primary_topic,
        "difficulty_topic": difficulty_topic,
        "logic_topic": logic_topic,
        "logic_status": logic_status,
        "total_score": generated.get("total_score"),
        "candidate_summary": candidate_summary,
        "primary_score": primary_score,
        "second_score": second_score,
        "gap": gap,
        "ratio": ratio,
    }


def _print_validation_summary(summary: dict[str, Any]) -> None:
    print()
    print("TOPIC PACK SMOKE SUMMARY")
    print("passed:", summary["passed"])
    print("primary_topic:", summary["primary_topic"])
    print("difficulty_topic:", summary["difficulty_topic"])
    print("logic_topic:", summary["logic_topic"])
    print("logic_status:", summary["logic_status"])
    if summary["logic_status"] == "missing_optional":
        print("logic_note: logic_check topic is optional; use --require-logic-check when the topic must have one.")
    print("total_score:", summary["total_score"])
    print("primary_score:", summary["primary_score"])
    print("second_score:", summary["second_score"])
    print("gap:", summary["gap"])
    print("ratio:", "inf" if summary["ratio"] == float("inf") else round(summary["ratio"], 3))

    print()
    print("candidates:")
    for idx, candidate in enumerate(summary["candidate_summary"], start=1):
        print(f" {idx}. score={candidate['score']} topic={candidate['topic_id']}")

    if summary["failures"]:
        print()
        print("FAILURES:")
        for failure in summary["failures"]:
            print(" -", failure)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke-test generated routing for a topic_pack.")
    parser.add_argument("--topic-id", required=True, help="topic_id under rubrics/topic_packs")
    parser.add_argument("--base-session", default=None, help="base session path to copy")
    parser.add_argument("--min-gap", type=float, default=30.0, help="minimum primary-second candidate score gap")
    parser.add_argument("--min-ratio", type=float, default=1.2, help="minimum primary/second candidate score ratio")
    parser.add_argument("--keep", action="store_true", help="keep synthetic session and smoke report")
    parser.add_argument(
        "--require-logic-check",
        action="store_true",
        help="require a logic check topic; by default missing logic topics are allowed, but present mismatches fail",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root = _project_root()
    topic_pack = _load_topic_pack(root, args.topic_id)
    model_answer = topic_pack["model_answer"]

    question = _question_from_model_answer(model_answer)
    answer = _answer_from_model_answer(model_answer, question)

    base_session = _find_base_session(root, args.base_session)
    target_session = _make_target_session(root, base_session, args.topic_id, args.keep)
    rewritten = _rewrite_session_payload(target_session, question, answer, args.topic_id)

    print("TOPIC PACK SMOKE")
    print("topic_id:", args.topic_id)
    print("question:", question)
    print("base_session:", base_session)
    print("target_session:", target_session)
    print("rewritten_files:", rewritten)

    report = _run_smoke_compare(root, target_session)
    summary = _validate_generated_result(
        report=report,
        topic_id=args.topic_id,
        min_gap=args.min_gap,
        min_ratio=args.min_ratio,
        require_logic_check=args.require_logic_check,
    )

    _print_validation_summary(summary)

    if not args.keep:
        try:
            shutil.rmtree(target_session)
            print()
            print("removed synthetic session:", target_session)
        except Exception:
            pass

    if not summary["passed"]:
        raise SystemExit(1)

    print()
    print("TOPIC PACK SMOKE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
