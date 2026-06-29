#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = ROOT / "wordpress_docs" / "industrial_instrumentation_posts.json"
DEFAULT_OUT_DIR = ROOT / "wordpress_docs" / "review_batches"
DEFAULT_QUEUE = ROOT / "wordpress_docs" / "review_queue.tsv"

MODEL_BANK = ROOT / "rubrics" / "model_answers" / "industrial_instrumentation_control.json"
FACT_BANK = ROOT / "rubrics" / "fact_anchors" / "industrial_instrumentation_control.json"


SKIP_TITLE_KEYWORDS = [
    "시험 결과",
    "비공개",
    "latex",
    "문서 작성",
    "기출 데이터 정밀 분석",
    "합격 전략",
]

LAW_KEYWORDS = [
    "시공",
    "설치",
    "현장",
    "계기함",
    "제어반",
    "분전반",
    "배전반",
    "접지",
    "누전",
    "차단기",
    "방폭",
    "폭발",
    "피뢰",
    "서지",
    "안전",
    "전선관",
    "케이블",
    "전기설비",
    "충전부",
    "외함",
    "보호등급",
    "작업공간",
]

NEW_MODEL_FACT_HINTS = [
    "종류",
    "비교",
    "원리",
    "특성",
    "응답",
    "제어",
    "센서",
    "전송기",
    "유량계",
    "온도",
    "압력",
    "밸브",
    "인버터",
    "모터",
    "통신",
    "프로토콜",
    "필터",
    "교정",
]

MERGE_HINTS = [
    "정리",
    "요약",
    "개론",
    "overview",
    "세부",
    "암기",
]


STOPWORDS = {
    "그리고", "그러나", "따라서", "대한", "위한", "관련", "설명", "문제",
    "기술사", "산업", "계측", "제어", "답안", "경우", "또한", "한다",
    "있다", "있는", "없는", "통해", "수행", "적용", "방법", "기준",
    "내용", "정리", "다음", "때문", "필요", "시스템", "현장",
    "합니다", "있습니다", "그리고", "에서는", "위하여", "대하여",
}


def clean_text(value: str) -> str:
    value = value or ""
    value = html.unescape(value)
    value = re.sub(r"<!--\s*/?wp:[^>]*?-->", "\n", value)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</p\s*>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\r\n?", "\n", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def extract_keywords(title: str, content: str, limit: int = 15) -> list[str]:
    text = f"{title}\n{content}"
    words = re.findall(r"[A-Za-z][A-Za-z0-9_+\-/]{1,}|[가-힣]{2,}", text)

    score: dict[str, int] = {}
    for word in words:
        if word in STOPWORDS:
            continue
        if len(word) <= 1:
            continue
        score[word] = score.get(word, 0) + 1

    ranked = sorted(score.items(), key=lambda x: (-x[1], x[0]))
    return [word for word, _ in ranked[:limit]]


def load_existing_terms() -> list[dict[str, str]]:
    existing: list[dict[str, str]] = []

    if MODEL_BANK.exists():
        data = json.loads(MODEL_BANK.read_text(encoding="utf-8"))
        answers = data.get("answers", data if isinstance(data, list) else [])
        for x in answers:
            topic_id = str(x.get("topic_id", ""))
            title = str(x.get("title", ""))
            aliases = x.get("topic_aliases", [])
            existing.append({
                "kind": "model",
                "topic_id": topic_id,
                "text": " ".join([topic_id, title] + [str(a) for a in aliases]),
            })

    if FACT_BANK.exists():
        data = json.loads(FACT_BANK.read_text(encoding="utf-8"))
        topics = data.get("topics", data if isinstance(data, list) else [])
        for x in topics:
            topic_id = str(x.get("topic_id", ""))
            name = str(x.get("name", ""))
            aliases = x.get("aliases", [])
            existing.append({
                "kind": "fact",
                "topic_id": topic_id,
                "text": " ".join([topic_id, name] + [str(a) for a in aliases]),
            })

    return existing


def existing_candidates(title: str, keywords: list[str], existing_terms: list[dict[str, str]]) -> list[str]:
    text = f"{title} {' '.join(keywords)}".lower()
    found: list[str] = []

    for item in existing_terms:
        hay = item["text"].lower()

        matched = False
        for token in keywords[:8]:
            t = token.lower()
            if len(t) >= 3 and (t in hay or hay in text):
                matched = True
                break

        if not matched and title and title.lower() in hay:
            matched = True

        if matched:
            label = f"{item['kind']}:{item['topic_id']}"
            if label not in found:
                found.append(label)

        if len(found) >= 5:
            break

    return found


def classify_post(title: str, content: str, keywords: list[str], existing: list[str]) -> tuple[str, str]:
    title_l = title.lower()
    content_l = content.lower()
    text = f"{title_l}\n{content_l}"

    if not title.strip():
        return "SKIP", "제목이 비어 있음"

    if len(content) < 120:
        return "SKIP", "본문이 너무 짧음"

    if any(k.lower() in title_l for k in SKIP_TITLE_KEYWORDS):
        return "SKIP", "시험 결과/비공개/문서작성/전략성 글 후보"

    if existing and any(k in title_l for k in MERGE_HINTS):
        return "MERGE_EXISTING", "기존 topic 보강용 정리/요약 글 후보"

    law_hits = [k for k in LAW_KEYWORDS if k.lower() in text]
    if len(law_hits) >= 2:
        return "LAW_BASED_FACT", "설치·안전·접지·방폭·전기설비 관련 법령/기준 anchor 검토 필요"

    if existing:
        return "MERGE_EXISTING", "기존 Model/Fact topic과 유사 후보 있음"

    fact_hits = [k for k in NEW_MODEL_FACT_HINTS if k.lower() in text]
    if len(fact_hits) >= 2 and len(content) >= 700:
        return "NEW_MODEL_FACT", "독립 주제와 핵심 fact anchor 생성 후보"

    if len(content) >= 500:
        return "NEW_MODEL_ONLY", "답안 구조 후보이나 fact anchor는 추가 검토 필요"

    return "SKIP", "우선순위 낮은 단편 글"


def excerpt(text: str, limit: int = 700) -> str:
    text = clean_text(text)
    text = re.sub(r"\n+", "\n", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def make_batch_prompt(batch_no: int, rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# WordPress Review Batch {batch_no:03d}",
        "",
        "아래 WordPress 글 후보를 검토하여 각 글을 다음 중 하나로 분류하라.",
        "",
        "| 분류 | 의미 |",
        "|---|---|",
        "| SKIP | 시험 결과, 개인 메모, 너무 단편적인 글, rubric 반영 가치 낮음 |",
        "| MERGE_EXISTING | 기존 topic에 흡수하여 보강하는 것이 적절 |",
        "| NEW_MODEL_ONLY | 독립 Model Answer는 필요하지만 Fact Anchor는 기존 것으로 충분 |",
        "| NEW_MODEL_FACT | 독립 Model Answer와 Fact Anchor가 모두 필요 |",
        "| LAW_BASED_FACT | 설치, 안전, 접지, 방폭, 전기설비처럼 법령·기준 기반 Fact Anchor가 필요 |",
        "",
        "출력은 반드시 표로 작성하라.",
        "",
        "| no | post_id | title | final_class | reason | suggested_topic_id | needed_action |",
        "|---:|---:|---|---|---|---|---|",
        "",
        "검토 원칙:",
        "",
        "1. 200개 글 전체를 새 topic으로 만들지 않는다.",
        "2. 제목이 유사하거나 기존 topic에 흡수 가능하면 MERGE_EXISTING을 우선한다.",
        "3. 설치·안전·접지·방폭 주제는 일반 키워드가 아니라 법령·고시·기준 문서 기반으로 판단한다.",
        "4. Model Answer Bank는 20점대 모범답안 기준이다.",
        "5. Fact Anchor는 키워드 암기가 아니라 채점 가능한 핵심 fact 기준이어야 한다.",
        "",
        "---",
        "",
    ]

    for row in rows:
        lines.extend([
            f"## {row['no']:03d}. {row['title']}",
            "",
            f"- post_id: {row['post_id']}",
            f"- date: {row['date']}",
            f"- preliminary_class: {row['preliminary_class']}",
            f"- preliminary_reason: {row['reason']}",
            f"- existing_candidates: {row['existing_candidates'] or '-'}",
            f"- keywords: {row['keywords'] or '-'}",
            "",
            "### excerpt",
            "",
            row["excerpt"],
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default=str(DEFAULT_SRC))
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--batch-size", type=int, default=20)
    args = parser.parse_args()

    src = Path(args.src)
    queue = Path(args.queue)
    out_dir = Path(args.out_dir)

    data = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("ERROR: source JSON must be a list")

    existing_terms = load_existing_terms()

    rows: list[dict[str, Any]] = []

    for no, post in enumerate(data, 1):
        title = str(post.get("title") or "").strip()
        raw_content = str(post.get("content_text") or post.get("content_raw") or "")
        content = clean_text(raw_content)
        keywords = extract_keywords(title, content)
        existing = existing_candidates(title, keywords, existing_terms)
        preliminary_class, reason = classify_post(title, content, keywords, existing)

        rows.append({
            "no": no,
            "post_id": post.get("id", ""),
            "title": title,
            "date": post.get("date", ""),
            "status": post.get("status", ""),
            "content_len": len(content),
            "preliminary_class": preliminary_class,
            "reason": reason,
            "existing_candidates": ", ".join(existing),
            "keywords": ", ".join(keywords),
            "excerpt": excerpt(content),
        })

    queue.parent.mkdir(parents=True, exist_ok=True)
    with queue.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "no",
            "post_id",
            "title",
            "date",
            "status",
            "content_len",
            "preliminary_class",
            "reason",
            "existing_candidates",
            "keywords",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("batch_*.md"):
        old.unlink()

    for idx in range(0, len(rows), args.batch_size):
        batch_no = idx // args.batch_size + 1
        batch_rows = rows[idx:idx + args.batch_size]
        path = out_dir / f"batch_{batch_no:03d}.md"
        path.write_text(make_batch_prompt(batch_no, batch_rows), encoding="utf-8")

    counts: dict[str, int] = {}
    for row in rows:
        key = row["preliminary_class"]
        counts[key] = counts.get(key, 0) + 1

    print("source:", src)
    print("posts:", len(rows))
    print("queue:", queue)
    print("batches:", out_dir)
    print("batch_size:", args.batch_size)
    print("counts:")
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
