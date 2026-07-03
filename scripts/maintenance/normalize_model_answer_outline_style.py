#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"

TYPE_DEFAULT_STRUCTURE = {
    "PRINCIPLE_INTERPRETATION": [
        "개요",
        "원리 및 구성",
        "주요 특성",
        "한계 및 유의점",
        "현장 적용 및 결론",
    ],
    "COMPARE_SELECTION": [
        "비교 대상 정의",
        "비교 기준 설정",
        "항목별 비교",
        "선정 기준",
        "현장 적용 및 결론",
    ],
    "DIAGNOSIS_ACTION": [
        "현상 및 문제 정의",
        "발생 원인",
        "진단 방법",
        "대책 및 개선방안",
        "현장 적용 및 결론",
    ],
    "IMPLEMENTATION_EVALUATION": [
        "개요",
        "적용 목적",
        "구성 및 절차",
        "평가 기준",
        "현장 적용 및 결론",
    ],
}

NUMBERED_HEADING_RE = re.compile(r"^\s*\d{1,2}[.)]\s*(.*?)\s*$")

SENTENCE_ENDINGS = (
    "다.",
    "한다.",
    "이다.",
    "있다.",
    "없다.",
    "된다.",
    "해야 한다.",
    "해야 한다",
    "해야 함",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def is_sentence_like(text: str) -> bool:
    s = text.strip()
    return s.endswith(SENTENCE_ENDINGS) or len(s) >= 35


def numbered_heading_title(text: str) -> str | None:
    s = text.strip()
    m = NUMBERED_HEADING_RE.match(s)
    if not m:
        return None

    title = m.group(1).strip()

    # "1." 단독 heading
    if not title:
        return ""

    # "1. 배경", "2. 기본 구성" 같은 목차만 heading으로 본다.
    # 본문 문장 또는 긴 설명문은 heading으로 보지 않는다.
    if is_sentence_like(title):
        return None

    if len(title) > 30:
        return None

    return title


def is_outline_heading(text: str) -> bool:
    title = numbered_heading_title(text)
    return title is not None


def extract_headings(*lists: list[str]) -> list[str]:
    out: list[str] = []
    for items in lists:
        for item in items:
            title = numbered_heading_title(str(item))
            if title is None:
                continue
            if not title:
                continue
            if title not in out:
                out.append(title)
    return out[:8]


def expected_structure_is_polluted(items: list[str]) -> bool:
    if not items:
        return True

    if any(numbered_heading_title(str(x)) is not None for x in items):
        return True

    sentence_like_count = sum(1 for x in items if is_sentence_like(str(x)))
    return sentence_like_count >= max(2, len(items) // 2)


def normalize_answer(item: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    changed = False
    report: dict[str, Any] = {}

    qtype = str(item.get("question_type", "")).strip()
    expected = [str(x).strip() for x in item.get("expected_structure", []) if str(x).strip()]
    outline = [str(x).strip() for x in item.get("model_answer_outline", []) if str(x).strip()]

    # 1) model_answer_outline에서 "1. 배경" 같은 번호 목차 제거
    cleaned_outline = [x for x in outline if not is_outline_heading(x)]

    removed_outline_headings = [x for x in outline if is_outline_heading(x)]
    if removed_outline_headings and cleaned_outline != outline:
        item["model_answer_outline"] = cleaned_outline
        changed = True
        report["removed_outline_headings"] = removed_outline_headings

    # 2) expected_structure가 본문 문장/번호 목차로 오염된 경우 정리
    if expected_structure_is_polluted(expected):
        headings = extract_headings(expected, outline)

        if len(headings) >= 4:
            new_expected = headings[:8]
        else:
            new_expected = TYPE_DEFAULT_STRUCTURE.get(
                qtype,
                ["개요", "핵심 내용", "적용 기준", "한계 및 유의점", "현장 적용 및 결론"],
            )

        if new_expected != expected:
            item["expected_structure"] = new_expected
            changed = True
            report["expected_structure"] = {
                "before": expected,
                "after": new_expected,
            }

    # 3) 추적 note 추가
    if changed:
        notes = item.setdefault("revision_notes", [])
        note = "2026-07-01 content_style_fix: normalized expected_structure and removed numbered headings from model_answer_outline."
        if note not in notes:
            notes.append(note)

    return changed, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply changes")
    args = ap.parse_args()

    bank = load_json(MODEL_PATH)
    answers = bank.get("answers", [])
    if not isinstance(answers, list):
        raise SystemExit("ERROR: answers must be a list")

    changed_reports: list[tuple[str, str, dict[str, Any]]] = []

    for item in answers:
        if not isinstance(item, dict):
            continue
        changed, report = normalize_answer(item)
        if changed:
            changed_reports.append(
                (
                    str(item.get("id", "")),
                    str(item.get("topic_id", "")),
                    report,
                )
            )

    print("changed:", len(changed_reports))
    for answer_id, topic_id, report in changed_reports:
        print(f"- {answer_id} | {topic_id}")
        if "removed_outline_headings" in report:
            print("  removed_outline_headings:", report["removed_outline_headings"])
        if "expected_structure" in report:
            print("  expected_structure:", report["expected_structure"]["after"])

    if args.write and changed_reports:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = backup_dir / f"industrial_instrumentation_control.before_outline_style_fix.{ts}.json"
        shutil.copy2(MODEL_PATH, backup)
        save_json(MODEL_PATH, bank)
        print("backup:", backup)
        print("written:", MODEL_PATH)
    elif not args.write:
        print("DRY RUN only. Re-run with --write to apply.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
