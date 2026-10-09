#!/usr/bin/env python3
"""Rank existing Topic Packs for WordPress posts using a local incremental index.

This is candidate retrieval only. Scores are ranking signals, not probabilities
or link decisions; recommendations must be checked against post evidence and
Topic ownership boundaries before they are applied.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = ROOT / "data" / "wordpress_sources.sqlite3"
DEFAULT_TOPIC_ROOT = ROOT / "rubrics" / "topic_packs"
DEFAULT_CACHE = ROOT / "data" / "wordpress_topic_match_cache.sqlite3"
SCHEMA_VERSION = "wordpress-topic-retrieval-v3"
SOURCE_JSON_NAMES = (
    "fact_anchor.json",
    "logic_check.json",
    "model_answer.json",
    "topic_importance.json",
)
K1 = 1.5
B = 0.75


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _flatten_json(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _flatten_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _flatten_json(child)
    elif value is not None and isinstance(value, (str, int, float, bool)):
        yield str(value)


def _topic_source_text(name: str, value: dict[str, Any]) -> str:
    """Keep authored scope/criteria while excluding bulky generic answer prose."""
    if name == "fact_anchor.json":
        fields = ("topic_id", "title_ko", "topic_label", "core_facts")
        anchors = value.get("anchors", [])
        if isinstance(anchors, list):
            selected_anchors = []
            for anchor in anchors:
                if not isinstance(anchor, dict):
                    continue
                selected_anchors.append({
                    field: anchor[field]
                    for field in ("statement", "claim", "keywords", "core_terms")
                    if field in anchor
                })
            if selected_anchors:
                fields += ("anchors",)
                value = {**value, "anchors": selected_anchors}
    elif name == "model_answer.json":
        fields = ("topic_id", "title_ko", "expected_question_patterns")
    elif name == "topic_importance.json":
        fields = (
            "topic_id", "difficulty", "selection_importance",
            "question_type", "high_band_unlock_conditions",
        )
    else:
        fields = ("topic_id", "title", "llm_profile")
    selected = {field: value[field] for field in fields if field in value}
    return "\n".join(_flatten_json(selected))


def _tokens(text: str) -> list[str]:
    normalized = text.casefold().replace("_", " ").replace("-", " ")
    tokens: list[str] = []
    stopwords = {
        "about", "after", "also", "and", "are", "can", "does", "for", "from",
        "has", "have", "into", "its", "may", "not", "our", "that", "the",
        "their", "then", "there", "these", "this", "those", "through", "with",
        "without", "using", "use", "used", "when", "where", "which", "while",
        "will", "would", "system", "systems", "topic", "pack", "question",
        "answer", "section", "scope", "core", "fact", "anchor", "design",
        "설명", "이하", "이상", "다음", "경우", "대한", "위한", "통한", "등의",
        "관련", "적용", "평가", "핵심", "기본", "기준", "구성", "사용", "설계",
        "설명하시오", "설명한다", "고려", "고려사항",
    }
    for match in re.finditer(r"[a-z0-9]+|[가-힣]+", normalized):
        term = match.group()
        is_hangul = bool(re.fullmatch(r"[가-힣]+", term))
        if len(term) <= 1 or term in stopwords or term.isdigit():
            continue
        if not is_hangul and len(term) < 3:
            continue
        tokens.append(term)
        if is_hangul and len(term) >= 5:
            tokens.extend(term[index:index + 3] for index in range(len(term) - 2))
    return tokens


def build_topic_documents(topic_root: Path) -> tuple[list[dict[str, Any]], str]:
    """Load searchable scope and authored source text for every existing pack."""
    documents: list[dict[str, Any]] = []
    digest = hashlib.sha256(SCHEMA_VERSION.encode("ascii"))
    for readme in sorted(topic_root.glob("*/README.md")):
        topic_id = readme.parent.name
        readme_bytes = readme.read_bytes()
        readme_text = readme_bytes.decode("utf-8")
        parts = [topic_id.replace("_", " "), readme_text]
        digest.update(str(readme.relative_to(topic_root)).encode("utf-8"))
        digest.update(readme_bytes)
        for name in SOURCE_JSON_NAMES:
            source = readme.parent / name
            if not source.is_file():
                continue
            source_bytes = source.read_bytes()
            try:
                parsed = json.loads(source_bytes)
                if isinstance(parsed, dict):
                    parts.append(_topic_source_text(name, parsed))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid Topic Pack source JSON: {source}") from exc
            digest.update(str(source.relative_to(topic_root)).encode("utf-8"))
            digest.update(source_bytes)
        content = "\n".join(parts)
        tokens = _tokens(content)
        if not tokens:
            continue
        heading = next(
            (line.lstrip("# ").strip() for line in parts[1].splitlines() if line.startswith("# ")),
            topic_id,
        )
        documents.append({
            "topic_id": topic_id,
            "title": heading,
            "tokens": tokens,
            "scope_excerpt": " ".join(readme_text.split())[:700],
        })
    if not documents:
        raise ValueError(f"no Topic Pack README files found in {topic_root}")
    return documents, digest.hexdigest()


def rank_topics(query: str, documents: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    """Return BM25-ranked candidates with lexical evidence, not a semantic verdict."""
    if limit < 1:
        raise ValueError("candidate limit must be positive")
    query_tokens = _tokens(query)
    query_terms = set(query_tokens)
    if not query_terms:
        return []
    frequencies = [
        Counter({term: min(count, 3) for term, count in Counter(doc["tokens"]).items()})
        for doc in documents
    ]
    lengths = [len(doc["tokens"]) for doc in documents]
    average_length = sum(lengths) / len(lengths) or 1.0
    document_frequency = Counter(
        term for term in query_terms
        if any(term in frequency for frequency in frequencies)
    )
    total_documents = len(documents)
    ranked: list[dict[str, Any]] = []
    for index, document in enumerate(documents):
        frequency = frequencies[index]
        matched = [term for term in sorted(query_terms) if frequency.get(term, 0)]
        score = 0.0
        for term in matched:
            df = document_frequency[term]
            inverse_frequency = math.log(1 + (total_documents - df + 0.5) / (df + 0.5))
            term_frequency = frequency[term]
            denominator = term_frequency + K1 * (
                1 - B + B * lengths[index] / average_length
            )
            score += inverse_frequency * term_frequency * (K1 + 1) / denominator
        if score <= 0:
            continue
        ranked.append({
            "topic_id": document["topic_id"],
            "title": document["title"],
            "bm25_score": round(score, 6),
            "matched_terms": matched[:40],
            "scope_excerpt": document["scope_excerpt"],
        })
    ranked.sort(key=lambda item: (-item["bm25_score"], item["topic_id"]))
    return ranked[:limit]


def _read_posts(database: Path) -> list[dict[str, Any]]:
    uri = database.resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    try:
        connection.row_factory = sqlite3.Row
        posts = connection.execute(
            """SELECT post_id,title,url,excerpt,tags_json,content_text,content_sha256
               FROM posts ORDER BY post_id"""
        ).fetchall()
        links: dict[int, list[dict[str, str]]] = {}
        for row in connection.execute(
            """SELECT post_id,topic_id,status FROM topic_links
               WHERE status IN ('approved','pending_review')
               ORDER BY post_id,CASE status WHEN 'approved' THEN 0 ELSE 1 END,topic_id"""
        ):
            links.setdefault(row["post_id"], []).append({
                "topic_id": row["topic_id"],
                "status": row["status"],
            })
        sources: dict[int, list[dict[str, str]]] = {}
        for row in connection.execute(
            """SELECT ps.post_id,s.source_id,s.source_type,s.title,s.content_sha256,
                      s.extracted_text,s.extraction_status
               FROM post_sources ps JOIN sources s USING(source_id)
               WHERE s.first_party=1 AND s.source_type IN ('pdf','image')
                 AND s.extraction_status='extracted' AND s.extracted_text IS NOT NULL
               ORDER BY ps.post_id,ps.position,s.source_id"""
        ):
            sources.setdefault(row["post_id"], []).append({
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "title": row["title"],
                "content_sha256": row["content_sha256"] or "",
                "extracted_text": row["extracted_text"],
            })
        result = []
        for post in posts:
            post_id = post["post_id"]
            asset_rows = sources.get(post_id, [])
            asset_material = [
                (item["source_id"], item["content_sha256"], item["extracted_text"])
                for item in asset_rows
            ]
            body_text = "\n".join([
                post["title"] or "",
                post["excerpt"] or "",
                " ".join(json.loads(post["tags_json"] or "[]")),
                post["content_text"] or "",
            ])
            asset_text = "\n".join(
                [
                    f"{item['title']} {item['extracted_text']}"
                    for item in asset_rows
                ]
            )
            content_digest = _sha256(json.dumps(
                [post["content_sha256"], post["title"], post["excerpt"],
                 post["tags_json"], asset_material],
                ensure_ascii=False, separators=(",", ":"),
            ).encode("utf-8"))
            result.append({
                "post_id": post_id,
                "title": post["title"],
                "url": post["url"],
                "text": body_text,
                "asset_text": asset_text,
                "content_sha256": content_digest,
                "existing_links": links.get(post_id, []),
            })
        return result
    finally:
        connection.close()


def _initialize_cache(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS retrieval_cache (
             post_id INTEGER NOT NULL,
             content_sha256 TEXT NOT NULL,
             topic_index_sha256 TEXT NOT NULL,
             candidate_limit INTEGER NOT NULL,
             candidates_json TEXT NOT NULL,
             PRIMARY KEY(post_id,content_sha256,topic_index_sha256,candidate_limit)
           )"""
    )
    return connection


def retrieve_posts(
    database: Path,
    topic_root: Path,
    cache_path: Path,
    *,
    candidate_limit: int = 12,
    post_ids: set[int] | None = None,
) -> dict[str, Any]:
    documents, topic_index_sha256 = build_topic_documents(topic_root)
    posts = _read_posts(database)
    if post_ids is not None:
        posts = [post for post in posts if post["post_id"] in post_ids]
    connection = _initialize_cache(cache_path)
    results: list[dict[str, Any]] = []
    cache_hits = 0
    try:
        connection.execute("BEGIN")
        for post in posts:
            cached = connection.execute(
                """SELECT candidates_json FROM retrieval_cache
                   WHERE post_id=? AND content_sha256=? AND topic_index_sha256=?
                     AND candidate_limit=?""",
                (post["post_id"], post["content_sha256"], topic_index_sha256, candidate_limit),
            ).fetchone()
            if cached:
                candidates = json.loads(cached[0])
                cache_hits += 1
            else:
                body_ranked = rank_topics(post["text"], documents, len(documents))
                asset_ranked = rank_topics(post["asset_text"], documents, len(documents))
                body_by_id = {
                    candidate["topic_id"]: (rank, candidate)
                    for rank, candidate in enumerate(body_ranked, start=1)
                }
                asset_by_id = {
                    candidate["topic_id"]: (rank, candidate)
                    for rank, candidate in enumerate(asset_ranked, start=1)
                }
                topic_by_id = {document["topic_id"]: document for document in documents}
                body_limit = max(1, candidate_limit * 3 // 4)
                body_ids = list(body_by_id)[:body_limit]
                asset_ids = [
                    topic_id for topic_id in asset_by_id
                    if topic_id not in body_by_id
                ][:max(0, candidate_limit - len(body_ids))]
                fused = []
                for topic_id in body_ids + asset_ids:
                    body_item = body_by_id.get(topic_id)
                    asset_item = asset_by_id.get(topic_id)
                    body_rank = body_item[0] if body_item else None
                    asset_rank = asset_item[0] if asset_item else None
                    retrieval_score = (
                        (1.0 / body_rank if body_rank else 0.0)
                        + (0.05 / asset_rank if not body_rank and asset_rank else 0.0)
                    )
                    document = topic_by_id[topic_id]
                    fused.append({
                        "topic_id": topic_id,
                        "title": document["title"],
                        "retrieval_score": round(retrieval_score, 8),
                        "body_rank": body_rank,
                        "body_score": body_item[1]["bm25_score"] if body_item else 0.0,
                        "asset_rank": asset_rank,
                        "asset_score": asset_item[1]["bm25_score"] if asset_item else 0.0,
                        "matched_terms": sorted(set(
                            (body_item[1]["matched_terms"] if body_item else [])
                            + (asset_item[1]["matched_terms"] if asset_item else [])
                        ))[:40],
                        "scope_excerpt": document["scope_excerpt"],
                    })
                fused.sort(key=lambda item: (-item["retrieval_score"], item["topic_id"]))
                candidates = fused[:candidate_limit]
                connection.execute(
                    """INSERT OR REPLACE INTO retrieval_cache
                       (post_id,content_sha256,topic_index_sha256,candidate_limit,candidates_json)
                       VALUES(?,?,?,?,?)""",
                    (post["post_id"], post["content_sha256"], topic_index_sha256,
                     candidate_limit, json.dumps(candidates, ensure_ascii=False, separators=(",", ":"))),
                )
            existing_ids = {item["topic_id"] for item in candidates}
            for link in post["existing_links"]:
                if link["topic_id"] not in existing_ids:
                    candidates.append({
                        "topic_id": link["topic_id"],
                        "title": "",
                        "bm25_score": 0.0,
                        "matched_terms": [],
                        "scope_excerpt": "",
                        "included_as": "existing_" + link["status"],
                    })
            results.append({
                "post_id": post["post_id"],
                "title": post["title"],
                "url": post["url"],
                "content_sha256": post["content_sha256"],
                "body_character_count": len(post["text"]),
                "existing_links": post["existing_links"],
                "candidates": candidates,
            })
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "retrieval_only": True,
        "scores_are_probabilities": False,
        "ranking_policy": "body BM25 top candidates first; first-party OCR contributes only additional candidates at low weight; retrieval-only",
        "database_path": str(database),
        "topic_index_sha256": topic_index_sha256,
        "topic_count": len(documents),
        "post_count": len(results),
        "candidate_limit": candidate_limit,
        "cache_hits": cache_hits,
        "cache_misses": len(results) - cache_hits,
        "posts": results,
    }


def write_report(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--topic-root", type=Path, default=DEFAULT_TOPIC_ROOT)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path, required=True, help="New JSON report; must not exist")
    parser.add_argument("--candidate-limit", type=int, default=12)
    parser.add_argument("--post-id", type=int, action="append", dest="post_ids")
    args = parser.parse_args()
    report = retrieve_posts(
        args.database,
        args.topic_root,
        args.cache,
        candidate_limit=args.candidate_limit,
        post_ids=set(args.post_ids) if args.post_ids else None,
    )
    write_report(report, args.output)
    print("WORDPRESS_TOPIC_RETRIEVAL=COMPLETE")
    print(f"POSTS={report['post_count']} TOPICS={report['topic_count']}")
    print(f"CACHE_HITS={report['cache_hits']} CACHE_MISSES={report['cache_misses']}")
    print(f"OUTPUT={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
