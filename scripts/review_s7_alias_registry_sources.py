#!/usr/bin/env python3
"""Join 119 unique S7 alias gaps to real verified Registry source evidence.

This is a human-review INPUT, not a source promotion or alias proposal engine.
Neither this tool nor its output may edit Ontology, Registry or scoring.
Only pre-existing approved/verified Fact records are used; no Golden answer text.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.claim_alignment_contract import canonical_relation


GENERIC_PREDICATES = frozenset({
    "is", "equals", "has", "maps", "uses", "counts", "requires", "depends_on",
    "includes", "changes", "measures", "provides", "controls", "reduces",
})


def _guard_output(path: Path) -> None:
    if (not path.is_absolute() or path.resolve().is_relative_to(ROOT.resolve())
            or path.exists() or path.is_symlink()):
        raise ValueError("output must be new, absolute and outside the repository")


def build_source_review(
    inventory: dict[str, Any], registry: dict[str, Any],
    *, require_full_baseline: bool = True,
) -> dict[str, Any]:
    if (inventory.get("schema_version") != "s7_alias_root_cause_audit.v1"
            or inventory.get("score_admission") != "DISABLED"
            or inventory.get("status") != "REPRODUCED_BASELINE"
            or inventory.get("baseline_reproduction", {}).get("mismatches") != {}):
        raise ValueError("S7 alias inventory has no reproduced baseline")
    projections = inventory.get("rows")
    if not isinstance(projections, list):
        raise ValueError("missing S7 projection evidence rows")
    if require_full_baseline and (
        len(projections) != 179
        or inventory.get("unique_topic_fact_count") != 119
        or inventory.get("primary_cause_projection_counts", {}).get("ID_NOT_FOUND") != 179
        or sum(inventory.get("primary_cause_projection_counts", {}).values()) != 179
    ):
        raise ValueError("S7 179/119 source-join gate failed")
    index: dict[str, dict] = {}
    for fact in registry.get("facts", []):
        if fact["fact_id"] in index:
            raise ValueError("ambiguous duplicate Registry Fact ID")
        index[fact["fact_id"]] = fact
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in projections:
        if item.get("primary_cause") != "ID_NOT_FOUND":
            raise ValueError("unexpected non-ID_NOT_FOUND cause in 119-Fact baseline")
        key = (item["owner_topic_id"], item["fact_id"])
        grouped[key].append(item)
    if require_full_baseline and len(grouped) != 119:
        raise ValueError("distinct Topic-Fact set mismatch")
    out: list[dict[str, Any]] = []
    by_risk: Counter[str] = Counter()
    topic_counts: Counter[str] = Counter()
    for (topic, anchor_id), occurrences in sorted(grouped.items()):
        first = occurrences[0]
        source_fact_id = first["source_fact_id"]
        relation = first["relation"]
        # The same owner/source Fact in multiple cases must have identical
        # immutable relational meaning. Do not silently choose one of many.
        if any(
            item["source_fact_id"] != source_fact_id or item["relation"] != relation
            for item in occurrences
        ):
            raise ValueError("conflicting source relation for same selected Fact")
        registry_fact = index.get(source_fact_id)
        if registry_fact is None or registry_fact["topic_id"] != topic:
            raise ValueError("source Fact absent from verified Registry or wrong owner")
        if (registry_fact["review_status"] != "approved"
                or registry_fact.get("verification_status") != "verified"
                or registry_fact.get("score_effect") != "none"):
            raise ValueError("source Fact no longer approved/verified/score-neutral")
        declared_anchor = registry_fact.get("legacy_anchor_id") or source_fact_id
        if declared_anchor != anchor_id:
            raise ValueError("Registry legacy-anchor mapping disagreement")
        verified_relation = canonical_relation({
            **registry_fact["relation"], "polarity": "positive",
        })
        if verified_relation != relation:
            raise ValueError("source Fact relationship changed since S7 projection")
        condition_ids = list(relation["conditions"])
        predicate = relation["predicate"]
        risks = ["ID_NOT_DEFINED_IN_PARSER_ONTOLOGY"]
        if condition_ids:
            risks.append("CONDITIONS_MUST_BE_ASSERTED_NOT_GUESSED")
        if predicate in GENERIC_PREDICATES:
            risks.append("BROAD_PREDICATE_FALSE_POSITIVE_RISK")
        if predicate in {"equals", "counts", "is_bounded_by", "maps"}:
            risks.append("FORMULA_OR_DIRECTION_CONSTRAINT_RISK")
        if any(token in predicate for token in ("_and_", "_or_", "_when_", "_if_")):
            risks.append("COMPOUND_PREDICATE_MAY_HIDE_MULTIPLE_CLAIMS")
        if len(registry_fact["verification_refs"]) == 0:
            raise ValueError("verified source Fact missing authority references")
        for risk in risks:
            by_risk[risk] += 1
        topic_counts[topic] += 1
        # Original claim and provenance are public approved Registry content.
        # The learner's Golden answer is NEVER copied into this review.
        out.append({
            "owner_topic_id": topic,
            "fact_id": anchor_id,
            "source_fact_id": source_fact_id,
            "source_statement": registry_fact["statement"],
            "source_revision": registry_fact["revision"],
            "registry_verification_status": registry_fact["verification_status"],
            "registry_review_status": registry_fact["review_status"],
            "registry_verification_refs": registry_fact["verification_refs"],
            "registry_source_refs": registry_fact["source_refs"],
            "relation": relation,
            "occurrences_in_47_golden": len(occurrences),
            "case_ids": sorted({item["case_id"] for item in occurrences}),
            "observed_missing_alias_ids": {
                component: sorted({
                    item["relation"][component] for item in occurrences
                    if component in item["missing_components"]
                }) for component in ("subject", "predicate", "object")
            },
            "original_ontology_evidence": first["component_evidence"],
            "risk_flags": risks,
            "candidate_alias": None,
            "candidate_wording": None,
            "technical_equivalence_of_candidate": "NOT_ASSESSED",
            "independent_alias_evidence": None,
            "false_positive_counterexamples": [],
            "review_decision": "HOLD",
            "review_reason": (
                "Verified Registry Fact does not automatically validate parser "
                "ID mapping or a new lexical alias; require individual evidence, "
                "conditions and negative-case review"
            ),
            "score_effect": "none",
        })
    return {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "baseline_reference_sha": inventory.get("baseline_reference_sha"),
        "inventory_execution_sha": inventory.get("execution_commit_sha"),
        "projection_count_with_duplicates": len(projections),
        "unique_topic_fact_count": len(out),
        "unique_source_fact_count": len({row["source_fact_id"] for row in out}),
        "duplicate_projections": len(projections) - len(out),
        "conditioned_fact_count": sum(bool(row["relation"]["conditions"]) for row in out),
        "unconditioned_fact_count": sum(not row["relation"]["conditions"] for row in out),
        "risk_flag_counts_nonexclusive": dict(sorted(by_risk.items())),
        "fact_count_by_topic": dict(sorted(topic_counts.items())),
        "decision_counts": {"HOLD": len(out), "ACCEPT": 0, "REVISE": 0, "REJECT": 0},
        "rows": out,
        "limitations": [
            "Approved source Fact is not approval to invent parser aliases.",
            "Source verification references are provenance, not freshly checked here.",
            "No Golden answer text, automatic acceptance or score change.",
            "Raw lexical inventory change alone cannot establish Claim-Fact accuracy.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        _guard_output(args.output)
        if (not args.inventory.is_absolute()
                or args.inventory.resolve().is_relative_to(ROOT.resolve())):
            raise ValueError("inventory input must be outside repository")
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        registry = load_approved_fact_registry(ROOT)
        result = build_source_review(inventory, registry)
        # Strict fail-closed accounting, no partial reviewed artifact accepted.
        if result["projection_count_with_duplicates"] != 179 or result["unique_topic_fact_count"] != 119:
            raise ValueError("unexpected source-review count")
        args.output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
        print(json.dumps({
            "status": result["status"],
            "projections": result["projection_count_with_duplicates"],
            "unique_facts": result["unique_topic_fact_count"],
            "with_conditions": result["conditioned_fact_count"],
            "risk_flag_counts": result["risk_flag_counts_nonexclusive"],
            "decisions": result["decision_counts"],
            "score_admission": "DISABLED",
        }, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        # Never include arbitrary exception content: source files might have
        # sensitive text. A stable error type is sufficient for the owner.
        print(json.dumps({
            "status": "SOURCE_JOIN_HOLD",
            "error_type": type(error).__name__,
            "score_admission": "DISABLED",
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
