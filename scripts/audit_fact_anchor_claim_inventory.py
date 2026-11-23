#!/usr/bin/env python3
"""Read-only Fact Anchor and optional canonical machine-contract inventory.

This is an ID-only structural audit, not technical fact verification,
Claim equivalence admission, ontology migration, or grading authority.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
from typing import Any

SCHEMA_VERSION = "fact_anchor_claim_inventory.v1"
MULTI_SENTENCE = re.compile(r"[.!?。]\s+")
CONDITION_CUE = re.compile(
    r"경우|조건|가정|한정|기준|범위|때|이하|이상|따라|하에서|provided|when|if|under", re.I
)


def _read(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError(f"expected JSON object: {path}")
    return result


def _ids(path: Path, key: str, row_key: str) -> set[str]:
    value = _read(path).get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be an array: {path}")
    out = set()
    for row in value:
        if not isinstance(row, dict) or not isinstance(row.get(row_key), str):
            raise ValueError(f"bad {key} row: {path}")
        out.add(row[row_key])
    return out


def audit_inventory(root: Path) -> dict[str, Any]:
    root = root.resolve()
    topic_dir = root / "rubrics" / "topic_packs"
    paths = sorted(topic_dir.glob("*/fact_anchor.json"))
    if not paths:
        raise ValueError("no Topic fact_anchor.json files found")
    ontology_dir = root / "grading_ontology"
    predicates = (
        _ids(ontology_dir / "canonical_predicates.json", "predicates", "id")
        | _ids(ontology_dir / "relations.json", "relations", "id")
    )
    concepts = _ids(ontology_dir / "engineering_concepts.json", "concepts", "id")
    quantities = _ids(ontology_dir / "quantities.json", "quantities", "id")
    dimensions = _ids(ontology_dir / "dimensions.json", "dimensions", "id")
    known_terms = concepts | quantities | dimensions

    topic_rows: list[dict[str, Any]] = []
    multi_candidates: list[dict[str, str]] = []
    exact_text_owners: dict[str, list[tuple[str, str]]] = defaultdict(list)
    relation_gaps: list[dict[str, str]] = []
    totals = Counter()

    for fact_path in paths:
        topic_id = fact_path.parent.name
        source = _read(fact_path)
        anchors = source.get("anchors")
        if source.get("topic_id") != topic_id or not isinstance(anchors, list):
            raise ValueError(f"invalid Topic owner or anchors: {topic_id}")
        seen_ids: set[str] = set()
        topic_multi = 0
        topic_conditions = 0
        for row in anchors:
            if not isinstance(row, dict):
                raise ValueError(f"invalid anchor record: {topic_id}")
            anchor_id = row.get("anchor_id") or row.get("id")
            if not isinstance(anchor_id, str) or not anchor_id.strip() or anchor_id in seen_ids:
                raise ValueError(f"missing or duplicate Fact ID: {topic_id}/{anchor_id}")
            seen_ids.add(anchor_id)
            statement = row.get("statement")
            if not isinstance(statement, str) or not statement.strip():
                raise ValueError(f"missing statement: {topic_id}/{anchor_id}")
            if MULTI_SENTENCE.search(statement):
                multi_candidates.append({
                    "topic_id": topic_id, "anchor_id": anchor_id,
                    "reason": "MULTI_SENTENCE_HEURISTIC_ONLY",
                })
                topic_multi += 1
            if CONDITION_CUE.search(statement):
                topic_conditions += 1
            exact_text_owners[" ".join(statement.split()).casefold()].append(
                (topic_id, anchor_id)
            )

        contract_path = fact_path.with_name("logic_check.json")
        contract_n = 0
        contract_valid_refs = 0
        if contract_path.exists():
            logic = _read(contract_path)
            contract = logic.get("machine_contract")
            if contract is not None:
                if not isinstance(contract, dict) or not isinstance(contract.get("facts"), list):
                    raise ValueError(f"bad machine_contract facts: {topic_id}")
                # Machine contracts are optional. Missing ontology identifiers or
                # different Fact IDs are review candidates, never auto-corrections.
                if contract.get("owner_topic_id") != topic_id:
                    relation_gaps.append({
                        "topic_id": topic_id, "fact_id": "*",
                        "reason": "MACHINE_CONTRACT_OWNER_MISMATCH",
                    })
                for fact in contract["facts"]:
                    if not isinstance(fact, dict) or not isinstance(fact.get("fact_id"), str):
                        raise ValueError(f"invalid contract fact: {topic_id}")
                    fact_id = fact["fact_id"]
                    contract_n += 1
                    # Machine-contract fact IDs and human-readable Anchor IDs
                    # are independent namespaces. Equality is informational,
                    # never a prerequisite nor a missing-relation error.
                    if fact_id in seen_ids:
                        contract_valid_refs += 1
                    if fact.get("predicate") not in predicates:
                        relation_gaps.append({
                            "topic_id": topic_id, "fact_id": fact_id,
                            "reason": "PREDICATE_ID_NOT_IN_GLOBAL_ONTOLOGY",
                        })
                    for key in ("subject", "object"):
                        if fact.get(key) not in known_terms:
                            relation_gaps.append({
                                "topic_id": topic_id, "fact_id": fact_id,
                                "reason": f"{key.upper()}_ID_NOT_IN_GLOBAL_ONTOLOGY",
                            })
                    conditions = fact.get("conditions") or []
                    if not isinstance(conditions, list):
                        raise ValueError(f"machine contract conditions must be array: {topic_id}/{fact_id}")
                    for condition in conditions:
                        if condition not in known_terms:
                            relation_gaps.append({
                                "topic_id": topic_id, "fact_id": fact_id,
                                "reason": "CONDITION_ID_NOT_IN_GLOBAL_ONTOLOGY",
                            })
        totals["anchors"] += len(anchors)
        totals["multi_sentence"] += topic_multi
        totals["condition_cue"] += topic_conditions
        totals["machine_contract_facts"] += contract_n
        totals["contract_id_joined"] += contract_valid_refs
        totals["contract_topics"] += int(contract_n > 0)
        topic_rows.append({
            "topic_id": topic_id, "anchor_count": len(anchors),
            "multi_sentence_heuristic_count": topic_multi,
            "condition_cue_count": topic_conditions,
            "machine_contract_fact_count": contract_n,
        })

    duplicates = [
        {
            "owners": [
                {"topic_id": t, "anchor_id": a}
                for t, a in sorted(owners)
            ],
            "reason": "CROSS_TOPIC_EXACT_TEXT_DUPLICATE_HEURISTIC_ONLY",
        }
        for owners in exact_text_owners.values()
        if len({t for t, _ in owners}) > 1
    ]
    duplicates.sort(key=lambda row: [
        (x["topic_id"], x["anchor_id"]) for x in row["owners"]
    ])
    relation_gaps.sort(key=lambda x: (x["topic_id"], x["fact_id"], x["reason"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "audit_only": True,
        "score_admission": "DISABLED",
        "score_effect": "none",
        "source_root": "rubrics/topic_packs",
        "summary": {
            "topic_count": len(paths),
            "anchor_count": totals["anchors"],
            "multi_sentence_candidate_count": totals["multi_sentence"],
            "condition_cue_count": totals["condition_cue"],
            "machine_contract_topic_count": totals["contract_topics"],
            "machine_contract_fact_count": totals["machine_contract_facts"],
            "contract_same_id_count": totals["contract_id_joined"],
            "relation_gap_count": len(relation_gaps),
            "cross_topic_exact_duplicate_groups": len(duplicates),
        },
        "topics": topic_rows,
        "multi_sentence_candidates": multi_candidates,
        "relation_gaps": relation_gaps,
        "cross_topic_exact_duplicates": duplicates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    result = audit_inventory(args.root)
    print(json.dumps(
        result["summary"] if args.summary_only else result,
        ensure_ascii=False, sort_keys=True, indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
