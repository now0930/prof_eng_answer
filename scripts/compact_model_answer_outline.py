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

MAX_ITEMS = 6

HEADING_RE = re.compile(r"^\s*\d{1,2}[.)]\s*(.*?)\s*$")

SENTENCE_ENDINGS = (
    "다.",
    "한다.",
    "된다.",
    "있다.",
    "없다.",
    "이다.",
    "해야 한다.",
    "필요하다.",
)

CATEGORY_KEYWORDS = {
    "intro": ["정의", "개요", "배경", "목적", "필요", "역할", "의미"],
    "core": ["원리", "동작", "구성", "구조", "메커니즘", "공식", "변수", "특성", "종류"],
    "criteria": ["비교", "선정", "기준", "계산", "평가", "지표", "판정", "해석", "사양"],
    "risk": ["문제", "원인", "영향", "오차", "한계", "리스크", "주의", "장단점", "고장"],
    "action": ["대책", "개선", "절차", "방법", "적용", "설계", "운전", "검토", "진단"],
    "conclusion": ["현장", "유지보수", "안전", "비용", "관리", "결론", "제언", "후속"],
}

CATEGORY_SENTENCES = {
    "intro": "{labels}를 통해 {topic}의 개념과 출제 배경을 제시한다.",
    "core": "{labels}를 중심으로 핵심 원리와 구성 관계를 설명한다.",
    "criteria": "{labels}를 기준으로 계산, 비교, 선정 또는 평가 판단을 정리한다.",
    "risk": "{labels}를 구분하여 성능 저하, 오차, 한계 또는 운전 영향을 설명한다.",
    "action": "{labels}에 따라 적용 절차와 개선 방향을 제시한다.",
    "conclusion": "{labels}까지 연결하여 현장 적용성과 결론을 정리한다.",
}

QTYPE_FALLBACK = {
    "PRINCIPLE_INTERPRETATION": [
        "{topic}의 개념과 적용 배경을 제시한다.",
        "핵심 원리와 동작 메커니즘을 설명한다.",
        "주요 구성 요소, 변수, 특성의 관계를 정리한다.",
        "장점, 한계, 오차 또는 제약 조건을 구분한다.",
        "공정 조건과 설비 적용 시 고려사항을 연결한다.",
        "운전·유지보수·안전 관점의 결론을 제시한다.",
    ],
    "COMPARE_SELECTION": [
        "비교 대상과 적용 배경을 제시한다.",
        "비교 기준과 판단 축을 먼저 설정한다.",
        "각 방식의 핵심 특성과 장단점을 정리한다.",
        "공정 조건에 따른 선정 기준을 제시한다.",
        "기존 설비, 비용, 유지보수 조건을 함께 검토한다.",
        "최종 선정 방향과 현장 적용 시 유의점을 정리한다.",
    ],
    "DIAGNOSIS_ACTION": [
        "현상과 문제 발생 조건을 정의한다.",
        "주요 원인과 발생 메커니즘을 설명한다.",
        "설비, 제어, 품질, 안전 측면의 영향을 정리한다.",
        "진단 방법과 확인 항목을 제시한다.",
        "원인별 대책과 개선 방안을 연결한다.",
        "현장 적용 우선순위와 유지보수 관점의 결론을 제시한다.",
    ],
    "IMPLEMENTATION_EVALUATION": [
        "적용 목적과 대상 범위를 제시한다.",
        "구성 요소와 적용 절차를 설명한다.",
        "평가 지표와 판정 기준을 설정한다.",
        "도입 전후 효과와 한계를 구분한다.",
        "기존 설비 연계, 비용, 운영 리스크를 검토한다.",
        "단계적 적용과 후속 관리 방향을 제시한다.",
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_numbering(text: str) -> str:
    s = str(text).strip()
    m = HEADING_RE.match(s)
    if m:
        return m.group(1).strip()
    return s


def is_sentence_like(text: str) -> bool:
    s = str(text).strip()
    return s.endswith(SENTENCE_ENDINGS) or len(s) >= 35


def is_heading_only(text: str) -> bool:
    s = str(text).strip()
    m = HEADING_RE.match(s)
    if not m:
        return False
    title = m.group(1).strip()
    if not title:
        return True
    return len(title) <= 30 and not is_sentence_like(title)


def normalize_for_dup(text: str) -> str:
    s = strip_numbering(text)
    s = re.sub(r"[^\w가-힣A-Za-z0-9]+", "", s)
    return s.lower()


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[가-힣A-Za-z0-9]{2,}", strip_numbering(text).lower()))


def similar(a: str, b: str) -> bool:
    na = normalize_for_dup(a)
    nb = normalize_for_dup(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    if len(na) >= 12 and len(nb) >= 12 and (na in nb or nb in na):
        return True

    ta = token_set(a)
    tb = token_set(b)
    if not ta or not tb:
        return False
    jaccard = len(ta & tb) / len(ta | tb)
    return jaccard >= 0.55


def dedupe(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        s = str(item).strip()
        if not s:
            continue
        if is_heading_only(s):
            continue
        if any(similar(s, old) for old in out):
            continue
        out.append(s)
    return out


def clean_topic_title(row: dict[str, Any]) -> str:
    title = str(row.get("title") or row.get("topic_id") or "해당 주제").strip()
    title = title.replace("모범 답안", "")
    title = title.replace("모범답안", "")
    title = re.sub(r"\s+", " ", title).strip()
    return title or "해당 주제"


def extract_labels(row: dict[str, Any]) -> list[str]:
    raw: list[str] = []
    for key in ("expected_structure", "model_answer_outline"):
        values = row.get(key, [])
        if isinstance(values, list):
            raw.extend(str(x).strip() for x in values if str(x).strip())

    labels: list[str] = []
    for item in raw:
        if is_heading_only(item):
            label = strip_numbering(item)
        else:
            label = strip_numbering(item)
            if is_sentence_like(label):
                continue
            if len(label) > 28:
                continue

        if not label:
            continue
        if normalize_for_dup(label) in {normalize_for_dup(x) for x in labels}:
            continue
        labels.append(label)

    return labels


def classify_labels(labels: list[str]) -> dict[str, list[str]]:
    buckets = {k: [] for k in CATEGORY_KEYWORDS}

    for label in labels:
        placed = False
        for cat, keys in CATEGORY_KEYWORDS.items():
            if any(k in label for k in keys):
                buckets[cat].append(label)
                placed = True
                break
        if not placed:
            buckets["core"].append(label)

    return buckets


def make_flow_outline(row: dict[str, Any]) -> list[str]:
    topic = clean_topic_title(row)
    labels = extract_labels(row)
    buckets = classify_labels(labels)

    outline: list[str] = []
    for cat in ("intro", "core", "criteria", "risk", "action", "conclusion"):
        picked = buckets.get(cat, [])[:3]
        if not picked:
            continue
        label_text = "·".join(picked)
        outline.append(CATEGORY_SENTENCES[cat].format(labels=label_text, topic=topic))

    if len(outline) < 4:
        qtype = str(row.get("question_type", "")).strip()
        fallback = QTYPE_FALLBACK.get(qtype, QTYPE_FALLBACK["PRINCIPLE_INTERPRETATION"])
        outline = [x.format(topic=topic) for x in fallback]

    return dedupe(outline)[:MAX_ITEMS]


def needs_compaction(row: dict[str, Any], rewrite_all: bool) -> bool:
    outline = row.get("model_answer_outline", [])
    if not isinstance(outline, list):
        return False

    cleaned = dedupe([str(x) for x in outline])
    if rewrite_all:
        return True
    if len(outline) > MAX_ITEMS:
        return True
    if len(cleaned) != len(outline):
        return True
    if any(is_heading_only(str(x)) for x in outline):
        return True

    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument(
        "--rewrite-all",
        action="store_true",
        help="6개 초과 항목뿐 아니라 모든 model_answer_outline을 큰 흐름형으로 재작성",
    )
    args = ap.parse_args()

    bank = load_json(MODEL_PATH)
    answers = bank.get("answers", [])
    if not isinstance(answers, list):
        raise SystemExit("ERROR: answers must be list")

    changed = []

    for row in answers:
        if not isinstance(row, dict):
            continue
        if not needs_compaction(row, rewrite_all=args.rewrite_all):
            continue

        before = row.get("model_answer_outline", [])
        after = make_flow_outline(row)

        if after != before:
            row["model_answer_outline"] = after
            notes = row.setdefault("revision_notes", [])
            note = "2026-07-01 content_style_fix: compacted model_answer_outline to high-level flow, max 6 items, removed duplicated detail."
            if note not in notes:
                notes.append(note)

            changed.append({
                "id": row.get("id"),
                "topic_id": row.get("topic_id"),
                "before_len": len(before) if isinstance(before, list) else None,
                "after_len": len(after),
                "after": after,
            })

    print("changed:", len(changed))
    for item in changed:
        print(f"- {item['id']} | {item['topic_id']} | {item['before_len']} -> {item['after_len']}")
        for line in item["after"]:
            print("  ·", line)

    if args.write and changed:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = backup_dir / f"industrial_instrumentation_control.before_compact_outline.{ts}.json"
        shutil.copy2(MODEL_PATH, backup)
        save_json(MODEL_PATH, bank)
        print("backup:", backup)
        print("written:", MODEL_PATH)
    elif not args.write:
        print("DRY RUN only. Re-run with --write to apply.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
