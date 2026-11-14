#!/usr/bin/env python3
"""Read-only, per-Anchor source/generated wording drift audit.

Checks an immutable 48-row review manifest against current Topic Pack source
and the generated Fact Bank. Does not regenerate banks, change approvals,
promote Facts, decide technical equivalence, or alter scoring.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = "calibration/fact_anchor_simplification_review_20261114.json"
GENERATED_REL = "rubrics/generated/fact_anchors.generated.json"


def _read(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected JSON object")
    return data


def audit_source_generated(root: Path = ROOT) -> dict[str, Any]:
    manifest = _read(root / MANIFEST_REL)
    if (manifest.get("schema_version") != "fact_anchor_simplification_review.v1"
            or manifest.get("score_effect") != "none"
            or manifest.get("review_status") != "PENDING_TECHNICAL_REVIEW"
            or not isinstance(manifest.get("entries"), list)
            or len(manifest["entries"]) != manifest.get("changed_anchor_count")):
        raise ValueError("invalid Fact sentence review manifest")
    generated = _read(root / GENERATED_REL)
    topics = generated.get("topics")
    if not isinstance(topics, list):
        raise ValueError("generated Fact Bank topic list missing")
    bank_index: dict[str, dict[str, dict]] = {}
    for topic in topics:
        if not isinstance(topic, dict) or not isinstance(topic.get("anchors"), list):
            raise ValueError("invalid generated topic")
        tid = topic.get("topic_id")
        if not isinstance(tid, str) or tid in bank_index:
            raise ValueError("duplicate or invalid generated Topic")
        anchors = {}
        for anchor in topic["anchors"]:
            if not isinstance(anchor, dict):
                raise ValueError("invalid generated Fact Anchor")
            aid = anchor.get("anchor_id") or anchor.get("id")
            if not isinstance(aid, str) or aid in anchors:
                raise ValueError("duplicate or invalid generated Fact ID")
            anchors[aid] = anchor
        bank_index[tid] = anchors
    source_cache: dict[str, dict[str, dict]] = {}
    counts: Counter[str] = Counter()
    changed_topics: Counter[str] = Counter()
    seen: set[tuple[str, str]] = set()
    cases: list[dict[str, Any]] = []
    for item in manifest["entries"]:
        if not isinstance(item, dict):
            raise ValueError("invalid review entry")
        topic = item.get("topic_id")
        aid = item.get("anchor_id")
        previous = item.get("previous_statement")
        new = item.get("simplified_statement")
        if (not all(isinstance(x, str) and x for x in (topic, aid, previous, new))
                or item.get("review_status") != "PENDING_TECHNICAL_REVIEW"
                or (topic, aid) in seen):
            raise ValueError("invalid or repeated review identity")
        seen.add((topic, aid))
        if topic not in source_cache:
            path = root / "rubrics/topic_packs" / topic / "fact_anchor.json"
            if path.resolve().parent.name != topic or "/" in topic or ".." in topic:
                raise ValueError("unsafe Topic ID")
            raw = _read(path)
            if raw.get("topic_id") != topic or not isinstance(raw.get("anchors"), list):
                raise ValueError("invalid source Topic ownership")
            d = {}
            for a in raw["anchors"]:
                key = a.get("anchor_id") or a.get("id")
                if not isinstance(key, str) or key in d:
                    raise ValueError("duplicate or invalid source Fact")
                d[key] = a
            source_cache[topic] = d
        source = source_cache[topic].get(aid)
        if (not isinstance(source, dict) or source.get("statement") != new
                or previous not in source.get("accepted_explanations", [])):
            raise ValueError("source text drifted from reviewed snapshot")
        changed_topics[topic] += 1
        anchor = bank_index.get(topic, {}).get(aid)
        if anchor is None:
            state = "GENERATED_ANCHOR_MISSING"
        else:
            generated_text = (
                anchor.get("expected") or anchor.get("fact")
                or anchor.get("statement") or anchor.get("description")
            )
            if generated_text == new:
                state = "GENERATED_WORDING_MATCHES_SOURCE"
            elif generated_text == previous:
                state = "GENERATED_WORDING_MATCHES_PREVIOUS"
            else:
                state = "GENERATED_WORDING_OTHER"
        counts[state] += 1
        cases.append({
            "topic_id": topic, "anchor_id": aid, "generated_wording_status": state,
            "technical_equivalence_reviewed": False,
            "score_effect": "none",
        })
    return {
        "schema_version": "fact_anchor_sentence_sync_audit.v1",
        "status": "AUDIT_ONLY",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "anchor_count": len(cases),
        "topic_count": len(changed_topics),
        "generated_wording_counts": dict(sorted(counts.items())),
        "cases": sorted(cases, key=lambda x: (x["topic_id"], x["anchor_id"])),
        "generated_wording_match_is_not_routing_equivalence": True,
        "technical_equivalence_reviewed": False,
        "safe_to_promote_automatically": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    result = audit_source_generated()
    if args.summary_only:
        result.pop("cases")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
