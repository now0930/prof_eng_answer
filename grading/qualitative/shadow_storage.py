"""Opt-in storage/projection for private D/E shadow results only."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from grading.qualitative.de_shadow import VERSION


def save_private_shadow(path: str | Path, shadow: Mapping[str, Any]) -> Path:
    target = Path(path)
    if shadow.get("version") != VERSION or shadow.get("score_effect") != "none":
        raise ValueError("invalid_score_neutral_shadow")
    if not target.parent.is_dir() or target.parent.is_symlink() or target.is_symlink():
        raise ValueError("private_shadow_parent_missing_or_symlink")
    payload = json.dumps(dict(shadow), ensure_ascii=False, indent=2, allow_nan=False)
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
    except Exception:
        target.unlink(missing_ok=True)
        raise
    return target


def project_learning_diagnosis(shadow: Mapping[str, Any]) -> dict[str, Any]:
    if shadow.get("version") != VERSION or shadow.get("score_effect") != "none":
        raise ValueError("invalid_score_neutral_shadow")
    if shadow.get("status") != "SHADOW_VALIDATED":
        return {"status": "UNEVALUATED", "score_effect": "none",
                "training_candidates": [], "diagnosis_candidates": []}
    return {
        "status": "CANDIDATE", "score_effect": "none",
        "training_candidates": [
            {key: item[key] for key in ("question_id", "question", "topic_id", "reason", "expected_elements")}
            | {"review_status": "candidate", "score_effect": "none"}
            for item in shadow["interview_questions"]
        ],
        "diagnosis_candidates": [
            {"criterion_id": row["criterion_id"], "topic_id": row["topic_id"],
             "proposed_score": row["score"], "review_status": "candidate", "score_effect": "none"}
            for row in shadow["criteria"]
        ],
    }
