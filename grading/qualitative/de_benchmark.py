"""Expert D/E benchmark manifest and label contract; never scores an answer."""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .de_shadow import LIMITS


VERSION = "qualitative_de_expert_benchmark_v1"


def _source_text(root: Path, row: dict[str, Any]) -> tuple[str, str]:
    source = row["source"]
    path = (root / source["path"]).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("source_outside_repository")
    data = json.loads(path.read_text(encoding="utf-8"))
    if source["kind"] == "regression_fixture":
        if data.get("regression_id") != source["regression_id"]:
            raise ValueError("source_case_mismatch")
        question, answer = data["question"], data.get("original_answer", data.get("answer"))
    else:
        matches = [case for case in data["cases"] if case.get("case_id") == source["source_case_id"]]
        if len(matches) != 1:
            raise ValueError("source_case_mismatch")
        question, answer = matches[0]["question"], matches[0]["answer"]
    if not isinstance(question, str) or not question.strip() or not isinstance(answer, str) or not answer.strip():
        raise ValueError("empty_source_question_or_answer")
    return question, answer


def build_manifest(root: Path, *, per_type: int = 5) -> dict[str, Any]:
    """Select reviewed cases across types and source kinds without copying answers."""
    if not isinstance(per_type, int) or per_type < 1:
        raise ValueError("invalid_per_type")
    source = root / "calibration/expert_accuracy_golden.jsonl"
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("review_status") in {"reviewed", "adjudicated"}:
            groups[row["question_type"]].append(row)
    selected = []
    for question_type in sorted(groups):
        # Sort by source kind before round-robin selection; this avoids treating
        # model answers as the only expert examples in a heterogeneous pool.
        by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in sorted(groups[question_type], key=lambda item: item["case_id"]):
            by_kind[row["source"]["kind"]].append(row)
        chosen = []
        while len(chosen) < per_type and any(by_kind.values()):
            for kind in sorted(by_kind):
                if by_kind[kind] and len(chosen) < per_type:
                    chosen.append(by_kind[kind].pop(0))
        if len(chosen) < per_type:
            raise ValueError(f"insufficient_reviewed_cases:{question_type}")
        for row in chosen:
            question, answer = _source_text(root, row)
            selected.append({
                "case_id": row["case_id"], "question_type": question_type,
                "topic_ids": row["topic_ids"], "source": row["source"],
                "review_status": row["review_status"],
                "question_sha256": hashlib.sha256(question.encode("utf-8")).hexdigest(),
                "answer_sha256": hashlib.sha256(answer.encode("utf-8")).hexdigest(),
                "expert_de_status": "UNLABELED",
            })
    return {"version": VERSION, "per_type": per_type, "case_count": len(selected), "cases": selected}


def blank_labels(manifest: dict[str, Any]) -> dict[str, Any]:
    return {"version": VERSION, "labels": [{
        "case_id": row["case_id"], "answer_sha256": row["answer_sha256"],
        "reviewer": None, "reviewed_at": None,
        "criteria": [{"criterion_id": key, "score": None, "reason": None,
                      "quote": None, "start": None, "end": None} for key in LIMITS],
    } for row in manifest["cases"]]}


def validate_labels(manifest: dict[str, Any], labels: dict[str, Any], root: Path) -> list[str]:
    """Return safe case-level errors; never infer missing expert decisions."""
    errors = []
    if labels.get("version") != VERSION or not isinstance(labels.get("labels"), list):
        return ["invalid_label_document"]
    by_id = {row["case_id"]: row for row in manifest["cases"]}
    seen = set()
    for row in labels["labels"]:
        if not isinstance(row, dict) or row.get("case_id") not in by_id:
            errors.append("unknown_case_id")
            continue
        case_id = row["case_id"]
        if case_id in seen:
            errors.append(f"{case_id}:duplicate_label")
        seen.add(case_id)
        source = by_id[case_id]
        if row.get("answer_sha256") != source["answer_sha256"]:
            errors.append(f"{case_id}:answer_hash_mismatch")
        try:
            reviewed_at = datetime.fromisoformat(row["reviewed_at"])
            provenance_valid = (isinstance(row.get("reviewer"), str) and bool(row["reviewer"].strip())
                                and reviewed_at.tzinfo is not None)
        except (KeyError, TypeError, ValueError):
            provenance_valid = False
        if not provenance_valid:
            errors.append(f"{case_id}:missing_review_provenance")
        criteria = row.get("criteria")
        if not isinstance(criteria, list) or len(criteria) != len(LIMITS) or {c.get("criterion_id") for c in criteria if isinstance(c, dict)} != set(LIMITS):
            errors.append(f"{case_id}:invalid_criteria")
            continue
        _, answer = _source_text(root, source)
        for criterion in criteria:
            key = criterion["criterion_id"]
            score = criterion.get("score")
            if (isinstance(score, bool) or not isinstance(score, (int, float))
                    or not math.isfinite(score) or not 0 <= score <= LIMITS[key]):
                errors.append(f"{case_id}:{key}:invalid_score")
            if not isinstance(criterion.get("reason"), str) or not criterion["reason"].strip():
                errors.append(f"{case_id}:{key}:missing_reason")
            quote, start, end = (criterion.get(name) for name in ("quote", "start", "end"))
            if isinstance(score, (int, float)) and not isinstance(score, bool) and math.isfinite(score) and score > 0:
                if (not isinstance(quote, str) or not quote.strip()
                        or not isinstance(start, int) or isinstance(start, bool)
                        or not isinstance(end, int) or isinstance(end, bool)
                        or start < 0 or end > len(answer) or answer[start:end] != quote):
                    errors.append(f"{case_id}:{key}:invalid_evidence")
            elif any(value is not None for value in (quote, start, end)):
                errors.append(f"{case_id}:{key}:zero_score_evidence")
    for case_id in sorted(set(by_id) - seen):
        errors.append(f"{case_id}:missing_label")
    return errors
