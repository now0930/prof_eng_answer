"""Read score-neutral, topic-specific model answers for /review only.

Never consume these files in the grading pipeline or generated banks.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "review-model-answer-v1"
_VALID_REVIEW_STATUSES = {"llm_reviewed_human_pending", "human_verified"}


def load_review_model_answer(repository_root: str | Path, topic_id: str) -> dict[str, Any] | None:
    """Return optional reviewed-study text; malformed files fail closed."""
    topic = str(topic_id or "")
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", topic):
        return None
    root = Path(repository_root).resolve()
    path = (root / "study" / "review_model_answers" / f"{topic}.json").resolve()
    if not path.is_relative_to(root) or not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        return None
    if data.get("topic_id") != topic or data.get("score_effect") != "none":
        return None
    if data.get("review_status") not in _VALID_REVIEW_STATUSES:
        return None
    if not all(isinstance(data.get(k), str) and data[k].strip() for k in ("title", "question", "attribution")):
        return None
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections or len(sections) > 20:
        return None
    if any(
        not isinstance(row, dict)
        or not isinstance(row.get("title"), str)
        or not row["title"].strip()
        or not isinstance(row.get("body"), str)
        or not row["body"].strip()
        for row in sections
    ):
        return None
    checks = data.get("self_check")
    if not isinstance(checks, list) or any(not isinstance(v, str) or not v.strip() for v in checks):
        return None
    return copy.deepcopy(data)
