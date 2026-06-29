#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "wordpress_docs" / "industrial_instrumentation_posts.json"
OUT_DIR = ROOT / "wordpress_docs" / "llm_inputs"

STOPWORDS = {
    "그리고", "그러나", "따라서", "대한", "위한", "관련", "설명", "문제",
    "기술사", "산업", "계측", "제어", "답안", "경우", "또한", "한다",
    "있다", "있는", "없는", "통해", "수행", "적용", "방법", "기준",
    "내용", "정리", "다음", "때문", "필요", "시스템", "현장",
}


def safe_name(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^\w가-힣.-]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value[:90].strip("_") or "post"


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


def compact_text(value: str, limit: int = 14000) -> str:
    value = clean_text(value)
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "\n\n[TRUNCATED: 원문이 길어 앞부분만 포함됨]"


def keyword_candidates(title: str, content: str, limit: int = 35) -> list[str]:
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


def source_block(post: dict[str, Any], content: str, keywords: list[str]) -> str:
    title = str(post.get("title", "")).strip()

    return f"""# Source Article

## Metadata

| 항목 | 값 |
|---|---|
| post_id | {post.get("id", "")} |
| title | {title} |
| date | {post.get("date", "")} |
| modified | {post.get("modified", "")} |
| status | {post.get("status", "")} |
| slug | {post.get("slug", "")} |
| link | {post.get("link", "")} |
| category | {post.get("category", "")} |

## Keyword Candidates

{chr(10).join("- " + k for k in keywords)}

## Source Content

{content}
"""


def answer_10point_prompt(source: str) -> str:
    return f"""# 10점대 답안 초안 생성 Request

아래 WordPress 글을 근거로 산업계측제어기술사 답안 초안을 작성하라.

이 요청의 목적은 최고 수준 모범답안을 바로 만드는 것이 아니다.
먼저 25점 만점 기준 10~14점대 답안 초안을 만드는 것이다.

## 목표 점수 수준

- 기준: 25점 만점
- 목표 점수: 10~14점대
- 성격: 기본 개념과 일부 핵심 fact는 있으나, 합격선 15점에는 부족한 답안
- 사용 목적: 이후 Model Answer Bank, Fact Anchor Bank, Topic Importance 초안 생성의 중간 자료

## 10점대 답안 특징

포함할 것:

1. 문제의 핵심 개념을 간단히 설명한다.
2. 주요 구성요소 또는 절차를 일부 제시한다.
3. 기본 용어는 사용한다.
4. 답안 구조는 배경, 내용, 문제점, 개선방안 또는 개념, 원리, 적용 순서로 나눈다.

의도적으로 부족하게 둘 것:

1. 현장 적용 판단은 간단히만 쓴다.
2. 비용, 실현 가능성, 기존 설비와의 연계는 자세히 쓰지 않는다.
3. 수식, 표준, 설계 판단은 과도하게 깊게 쓰지 않는다.
4. 고득점용 비교·선정 기준은 간단히만 언급한다.
5. 20점대 답안처럼 완성도 높게 쓰지 않는다.

## 출력 형식

반드시 다음 순서로 출력하라.

1. 추출 topic
2. 예상 question_type
3. 핵심 키워드
4. 10점대 답안 초안
5. 이 답안이 10점대에 머무는 이유
6. 15점 이상으로 올리기 위한 보완 포인트
7. Model Answer Bank JSON 초안 필요 여부
8. Fact Anchor Bank JSON 초안 필요 여부
9. Topic Importance JSON 초안 필요 여부

## 허용 question_type

- PRINCIPLE_INTERPRETATION
- DIAGNOSIS_ACTION
- COMPARE_SELECTION
- IMPLEMENTATION_EVALUATION

## 답안 작성 조건

- 답안은 한국어로 작성한다.
- 기술사 답안처럼 항목화한다.
- 너무 짧은 키워드 나열은 피한다.
- 너무 완성도 높은 20점대 답안으로 만들지 않는다.
- 25점 만점 기준 10~14점대 답안처럼 작성한다.
- 원문에 없는 표준 번호, 법규, 수치를 임의로 만들지 않는다.

{source}
"""


def fact_anchor_prompt(source: str) -> str:
    return f"""# Fact Anchor JSON Draft Request

아래 WordPress 글을 근거로 Fact Anchor Bank에 넣을 JSON 초안이 필요한지 판단하라.
필요하다면 JSON 초안을 작성하라.

## 목적

Fact Anchor는 모범답안이 아니다.
답안에서 확인할 핵심 fact 기준, core term, support term을 정리하는 것이다.

## 출력 지시

1. 기존 topic에 흡수 가능한지 판단한다.
2. 새 topic이 필요하면 topic_id를 snake_case로 제안한다.
3. 새 topic이 필요할 경우 anchors는 반드시 5개로 작성한다.
4. 각 anchor는 id, name, expected, core_terms, support_terms를 포함한다.
5. 불확실한 수치, 표준 번호, 법규를 임의로 만들지 않는다.

{source}
"""


def topic_importance_prompt(source: str) -> str:
    return f"""# Topic Importance JSON Draft Request

아래 WordPress 글을 근거로 Topic Importance 추가가 필요한지 판단하라.
필요하다면 JSON 초안을 작성하라.

## 목적

Topic Importance는 답안 내용이 아니다.
시험 선택 전략, 난이도, 회피 위험, 치명 오답 위험을 판단하는 보조 기준이다.

## difficulty 선택지

- BASIC_CONCEPT
- FIELD_APPLICATION
- DESIGN_EVALUATION
- THEORY_CORE

## 출력 지시

1. 이 topic이 시험 선택 전략에 영향을 주는지 판단한다.
2. 단순 세부 글이면 DO_NOT_ADD 또는 기존 topic 흡수를 제안한다.
3. 독립 topic이 필요할 때만 JSON 초안을 작성한다.
4. 과도하게 많은 세부 topic을 만들지 않는다.

{source}
"""


def combined_prompt(answer: str, fact: str, topic: str) -> str:
    return f"""# Combined LLM Draft Request

이 파일은 WordPress 글 하나를 기준으로 다음 3가지를 검토하기 위한 통합 입력이다.

1. 10점대 답안 초안
2. Fact Anchor Bank 초안 필요 여부
3. Topic Importance 초안 필요 여부

우선순위는 다음과 같다.

1. 10점대 답안 초안은 적극적으로 생성한다.
2. Fact Anchor는 기존 anchor로 설명이 어려울 때만 생성한다.
3. Topic Importance는 시험 선택 전략에 영향이 있을 때만 생성한다.

---

{answer}

---

{fact}

---

{topic}
"""


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"ERROR: source not found: {SRC}")

    data = json.loads(SRC.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("ERROR: source JSON must be a list")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# WordPress 산업계측제어기술사 LLM 입력 파일 Index",
        "",
        "이 디렉터리는 WordPress 글을 LLM이 이해하기 쉬운 prompt 파일로 변환한 것이다.",
        "",
        "| no | post_id | title | combined prompt | split prompts |",
        "|---:|---:|---|---|---|",
    ]

    for i, post in enumerate(data, 1):
        title = str(post.get("title", "")).strip()
        post_id = post.get("id", "")
        slug = safe_name(str(post.get("slug") or title or post_id))

        raw_content = str(post.get("content_text") or post.get("content_raw") or "")
        content = compact_text(raw_content)
        keywords = keyword_candidates(title, content)

        base = f"{i:03d}_{post_id}_{slug}"

        source = source_block(post, content, keywords)

        answer = answer_10point_prompt(source)
        fact = fact_anchor_prompt(source)
        topic = topic_importance_prompt(source)
        combined = combined_prompt(answer, fact, topic)

        combined_name = f"{base}_combined_prompt.md"
        answer_name = f"{base}_answer_10point_prompt.md"
        fact_name = f"{base}_fact_anchor_prompt.md"
        topic_name = f"{base}_topic_importance_prompt.md"

        (OUT_DIR / combined_name).write_text(combined, encoding="utf-8")
        (OUT_DIR / answer_name).write_text(answer, encoding="utf-8")
        (OUT_DIR / fact_name).write_text(fact, encoding="utf-8")
        (OUT_DIR / topic_name).write_text(topic, encoding="utf-8")

        index_lines.append(
            f"| {i} | {post_id} | {title} | `{combined_name}` | `{answer_name}`, `{fact_name}`, `{topic_name}` |"
        )

    (OUT_DIR / "_index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print("source:", SRC)
    print("posts:", len(data))
    print("created:", OUT_DIR)
    print("index:", OUT_DIR / "_index.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
