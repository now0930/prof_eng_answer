#!/usr/bin/env python3
"""Score-neutral B7 adversarial probe: 20 Registry Fact pairs, 40 *draft* texts.

Use ACTUAL existing claim extractor + alignment WITHOUT inventing parser aliases.
The fixture represents author-drafted, NOT independently expert-adjudicated
semantic expectations.  A zero false-positive count when positive coverage is
zero is explicitly INCONCLUSIVE, never proof of correctness.

Never write the underlying 47 Golden answers or these probe answers to output.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.claim_alignment_engine import analyze_claim_alignment

VERSION = "s7_alias_negative_probe.v1"
QUESTION = "해당 공학 관계의 정의, 성립 조건과 제한을 기술하시오."
RELATION_LABELS = frozenset({
    "EXACT_RELATION", "CONDITION_GAP", "CONTRADICTION_CANDIDATE", "UNRESOLVED",
})


def evaluate_negative_probe(
    source_review: dict[str, Any], fixture: dict[str, Any],
    *,
    matcher: Callable[..., dict[str, Any]] = analyze_claim_alignment,
    strict: bool = True,
) -> dict[str, Any]:
    if (source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
            or source_review.get("status") != "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
            or source_review.get("score_admission") != "DISABLED"):
        raise ValueError("S7 source review is not a safe baseline")
    if (fixture.get("schema_version") != "s7_negative_claim_challenge.v1"
            or fixture.get("score_admission") != "DISABLED"
            or fixture.get("adjudication_status")
            != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"):
        raise ValueError("S7 negative challenge is unrecognized or unsafe")
    registry_rows = source_review.get("rows")
    cases = fixture.get("cases")
    if not isinstance(registry_rows, list) or not isinstance(cases, list):
        raise ValueError("missing source or challenge cases")
    if strict and (
        len(registry_rows) != 119
        or len(cases) != 20
        or source_review.get("projection_count_with_duplicates") != 179
        or source_review.get("unique_topic_fact_count") != 119
    ):
        raise ValueError("119-source / 20-challenge gate mismatch")
    identities = {
        (row["owner_topic_id"], row["fact_id"]): row for row in registry_rows
    }
    if len(identities) != len(registry_rows):
        raise ValueError("ambiguous source review identity")
    case_ids: set[str] = set()
    used: set[tuple[str, str]] = set()
    result_rows: list[dict[str, Any]] = []
    positive_exact_count = 0
    negative_exact_count = 0
    positive_unresolved = 0
    negative_unresolved = 0
    negative_relation_labels: Counter[str] = Counter()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("invalid adversarial case")
        if case.get("score_effect") != "none":
            raise ValueError("case attempted score admission")
        case_id = case["case_id"]
        owner = case["owner_topic_id"]
        fact_id = case["fact_id"]
        key = (owner, fact_id)
        if case_id in case_ids or key in used:
            raise ValueError("duplicate adversarial identity")
        case_ids.add(case_id)
        used.add(key)
        source = identities.get(key)
        if source is None:
            raise ValueError("challenge references non-reviewed Fact")
        if source["review_decision"] != "HOLD":
            raise ValueError("challenged alias cannot be pre-approved")
        relation = source["relation"]
        if relation["subject"] != case["relation_subject_id"]:
            raise ValueError("challenge subject relation drift")
        if (
            case["positive_label"] != "SOURCE_CONSISTENT_DRAFT"
            or case["adversarial_label"] != "SOURCE_INCONSISTENT_DRAFT"
            or not case.get("adversarial_type")
        ):
            raise ValueError("adversarial semantic labels are incomplete")
        answer_pairs = (
            ("positive", case["positive_answer"]),
            ("adversarial", case["adversarial_answer"]),
        )
        observed: dict[str, dict[str, Any]] = {}
        for kind, answer in answer_pairs:
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("empty challenge answer")
            audit = matcher(
                question_text=QUESTION, answer_text=answer,
                topic_ids=[owner], required_by_topic={owner: {fact_id}},
            )
            if audit.get("score_effect") != "none" or audit.get("authority") != "audit_only":
                raise ValueError("claim alignment attempted grading authority")
            projected = [
                row for row in audit["fact_projection"]
                if row["owner_topic_id"] == owner and row["fact_id"] == fact_id
            ]
            if len(projected) != 1 or (
                projected[0].get("projection_status") != "VERIFIED_REGISTRY_RELATION"
                or projected[0].get("source_fact_id") != source["source_fact_id"]
                or projected[0].get("relation") != relation
            ):
                raise ValueError("challenge target source relation not verified")
            matched = [
                x for x in audit["alignments"]
                if x["owner_topic_id"] == owner and x["fact_id"] == fact_id
            ]
            labels = sorted({x["relation"] for x in matched})
            if any(label not in RELATION_LABELS for label in labels):
                raise ValueError("unexpected alignment relation label")
            observed[kind] = {
                "target_relation_labels": labels,
                "target_alignment_count": len(matched),
                "target_exact": "EXACT_RELATION" in labels,
                "unresolved_span_count": len(audit["unresolved"]),
            }
        pos, neg = observed["positive"], observed["adversarial"]
        positive_exact_count += int(pos["target_exact"])
        negative_exact_count += int(neg["target_exact"])
        positive_unresolved += int(pos["unresolved_span_count"] > 0)
        negative_unresolved += int(neg["unresolved_span_count"] > 0)
        negative_relation_labels.update(neg["target_relation_labels"])
        result_rows.append({
            "case_id": case_id,
            "owner_topic_id": owner,
            "fact_id": fact_id,
            "source_fact_id": source["source_fact_id"],
            "source_relation_subject_id": relation["subject"],
            "source_relation_predicate_id": relation["predicate"],
            "source_relation_object_id": relation["object"],
            "condition_id_count": len(relation["conditions"]),
            "adversarial_type": case["adversarial_type"],
            "adjudication_status": fixture["adjudication_status"],
            "positive": pos,
            "adversarial": neg,
            "score_effect": "none",
        })
    if strict and len(result_rows) != 20:
        raise ValueError("challenge count drift")
    coverage = positive_exact_count / len(result_rows) if result_rows else None
    status = (
        "NEGATIVE_EXACT_REVIEW_REQUIRED" if negative_exact_count
        else "NO_POSITIVE_COVERAGE_INCONCLUSIVE" if positive_exact_count == 0
        else "RESEARCH_ONLY_SHADOW_COMPARISON"
    )
    # No TP/FP/FN claim: labels are author-drafted, not expert-adjudicated,
    # and current ontology has no matching 119 Registry relation IDs.
    return {
        "schema_version": VERSION,
        "status": status,
        "score_effect": "none",
        "score_admission": "DISABLED",
        "source_inventory_execution_sha": source_review.get("inventory_execution_sha"),
        "adjudication_status": fixture["adjudication_status"],
        "fact_pair_count": len(result_rows),
        "draft_answer_case_count": len(result_rows) * 2,
        "positive_exact_count": positive_exact_count,
        "adversarial_exact_count_needs_review": negative_exact_count,
        "positive_exact_fraction_not_validated_recall": coverage,
        "positive_with_unresolved_count": positive_unresolved,
        "adversarial_with_unresolved_count": negative_unresolved,
        "adversarial_relation_labels": dict(sorted(negative_relation_labels.items())),
        "measured_precision": None,
        "measured_recall": None,
        "measured_accuracy": None,
        "accuracy_claim": "NOT_ESTABLISHED",
        "automatic_alias_admission": False,
        "all_candidate_decisions": "HOLD",
        "rows": sorted(result_rows, key=lambda row: row["case_id"]),
        "limitations": [
            "Only actual current parser and source-verified Fact projections were used.",
            "Draft positive/negative expectations are not independent expert labels.",
            "Zero false positives with zero positive coverage proves nothing.",
            "No direct 47-case Golden answers or user answers were written.",
            "No new ontology aliases; no scoring, fatal, ceiling or pass-policy changes.",
        ],
    }


def _write_private_new(path: Path, report: dict[str, Any]) -> None:
    if (not path.is_absolute() or path.resolve().is_relative_to(ROOT.resolve())
            or path.exists() or path.is_symlink()):
        raise ValueError("output must be a new absolute path outside repository")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-review", type=Path, required=True)
    p.add_argument(
        "--challenge", type=Path,
        default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json",
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if (not args.source_review.is_absolute()
                or args.source_review.resolve().is_relative_to(ROOT.resolve())):
            raise ValueError("source-review must be an external artifact path")
        source_review = json.loads(args.source_review.read_text(encoding="utf-8"))
        fixture = json.loads(args.challenge.read_text(encoding="utf-8"))
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
            capture_output=True, check=False,
        )
        if (revision.returncode or revision.stdout.strip() !=
                source_review.get("inventory_execution_sha")):
            raise ValueError("source inventory belongs to a different commit")
        result = evaluate_negative_probe(source_review, fixture)
        result["execution_commit_sha"] = revision.stdout.strip()
        _write_private_new(args.output, result)
        print(json.dumps({
            "status": result["status"],
            "fact_pairs": result["fact_pair_count"],
            "draft_answer_cases": result["draft_answer_case_count"],
            "positive_exact": result["positive_exact_count"],
            "negative_exact_requires_review": result["adversarial_exact_count_needs_review"],
            "accuracy_claim": result["accuracy_claim"],
            "score_admission": result["score_admission"],
        }, ensure_ascii=False))
        return 0 if result["status"] != "NEGATIVE_EXACT_REVIEW_REQUIRED" else 2
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({
            "status": "NEGATIVE_PROBE_HOLD",
            "error_type": type(error).__name__,
            "score_admission": "DISABLED",
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
