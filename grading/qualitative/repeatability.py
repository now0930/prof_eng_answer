"""Redacted, score-neutral measurement of repeated D/E shadow proposals."""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter
from typing import Any, Callable, Mapping

from grading.qualitative.de_shadow import LIMITS, evaluate_qualitative_de


VERSION = "qualitative_de_repeatability_v1"


def measure_repeated_shadow(
    question: str, answer: str, abc_result: Mapping[str, Any],
    topic_context: Mapping[str, Any], llm_call: Callable[[str], str] | None,
    model_metadata: Mapping[str, Any], *, runs: int = 3,
) -> dict[str, Any]:
    """Return hashes, statuses and score dispersion, never answer quotations.

    Even identical scores are not proof of correct qualitative judgment.
    The production total and all A/B/C inputs remain outside this function.
    """
    if not isinstance(runs, int) or isinstance(runs, bool) or not 2 <= runs <= 20:
        raise ValueError("runs_must_be_between_2_and_20")
    before = hashlib.sha256(json.dumps([abc_result, topic_context], sort_keys=True,
                                       ensure_ascii=False).encode("utf-8")).hexdigest()
    results = [evaluate_qualitative_de(question, answer, abc_result, topic_context,
                                      llm_call=llm_call, model_metadata=model_metadata)
               for _ in range(runs)]
    after = hashlib.sha256(json.dumps([abc_result, topic_context], sort_keys=True,
                                      ensure_ascii=False).encode("utf-8")).hexdigest()
    if before != after or any(row.get("score_effect") != "none" or "total_score" in row for row in results):
        raise RuntimeError("shadow_authority_violation")
    accepted = [row for row in results if row["status"] == "SHADOW_VALIDATED"]
    scored = {key: [next(item["score"] for item in row["criteria"] if item["criterion_id"] == key)
                    for row in accepted] for key in LIMITS}
    score_range = {key: {"min": min(values), "max": max(values),
                         "pstdev": statistics.pstdev(values)} if values else None
                   for key, values in scored.items()}
    request_hashes = {row.get("request_hash") for row in results if row.get("request_hash")}
    return {
        "version": VERSION, "score_effect": "none", "expert_agreement": "NOT_MEASURED",
        "semantic_truth_verified": False, "acceptance_status": "REVIEW_REQUIRED",
        "measurement_status": "MEASURED" if len(accepted) == runs else "INCOMPLETE",
        "runs_requested": runs, "runs_completed": len(results), "validated_runs": len(accepted),
        "provider_calls": sum(row["provider_calls"] for row in results),
        "status_counts": dict(sorted(Counter(row["status"] for row in results).items())),
        "reason_counts": dict(sorted(Counter(row.get("reason_code", "") for row in results).items())),
        "input_hash_distinct": len({row["input_hash"] for row in results}),
        "request_hash_distinct": len(request_hashes),
        "criterion_dispersion": score_range,
        "proposed_d_values": [row["proposed_d"] for row in accepted],
        "proposed_e_values": [row["proposed_e"] for row in accepted],
        "model_metadata": {key: model_metadata[key] for key in
                           ("provider", "model_id", "temperature", "prompt_version")
                           if key in model_metadata},
    }
