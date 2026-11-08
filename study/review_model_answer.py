"""Optional, score-neutral, question-scoped study answers."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any


def _normalized_question(value: str) -> str:
    text = re.sub(r"\s+", "", value).casefold()
    return re.sub(r"[^\w가-힣]", "", text)


def load_review_model_answer(repository_root: str | Path, topic_id: str) -> dict[str, Any] | None:
    """Load a curated answer only when its provenance and review state are explicit."""
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", str(topic_id or "")):
        return None
    path = Path(repository_root) / "study" / "review_model_answers" / f"{topic_id}.json"
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(doc, dict) or doc.get("schema_version") != "review-model-answer-v2":
        return None
    if doc.get("topic_id") != topic_id or doc.get("score_effect") != "none":
        return None
    if doc.get("review_status") not in {"llm_reviewed_human_pending", "human_verified"}:
        return None
    for key in ("title", "question", "attribution", "reviewed_by", "reviewed_at"):
        if not isinstance(doc.get(key), str) or not doc[key].strip():
            return None
    if not isinstance(doc.get("sources"), list) or not doc["sources"]:
        return None
    if any(not isinstance(s, dict) or not isinstance(s.get("url"), str)
           or not s["url"].startswith("https://") or not isinstance(s.get("locator"), str)
           or not s["locator"].strip() for s in doc["sources"]):
        return None
    sections = doc.get("sections")
    if not isinstance(sections, list) or not 1 <= len(sections) <= 20:
        return None
    if any(not isinstance(s, dict) or not isinstance(s.get("title"), str)
           or not isinstance(s.get("body"), str) or not s["title"].strip()
           or not s["body"].strip() for s in sections):
        return None
    demands = doc.get("question_demands")
    if not isinstance(demands, list) or not demands:
        return None
    if any(not isinstance(d, dict) or not isinstance(d.get("label"), str)
           or not isinstance(d.get("requirement_ids"), list) for d in demands):
        return None
    if not isinstance(doc.get("self_check"), list):
        return None
    return copy.deepcopy(doc)


def matches_question(answer: dict[str, Any], question_text: str) -> bool:
    """Match the complete curated question, tolerating OCR prefaces and spaces."""
    target = _normalized_question(answer.get("question", ""))
    candidate = _normalized_question(question_text or "")
    return bool(target and len(target) >= 40 and target in candidate)
