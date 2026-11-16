"""Read-only S7 alias root-cause trace for the *actual* verified projections.

No answer text, scoring authority, approval, or ontology changes.  Import the
same alias loaders as the canonical parser and use the S7 runner's already
graded/aligned case output.  Projection counts are intentionally NOT deduped.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any, Mapping

from grading.evidence.canonical_claim_extractor import (
    ROOT, _load_aliases, _load_predicates, _normalized,
)

VERSION = "s7_alias_root_cause_audit.v1"
COMPONENTS = ("subject", "predicate", "object")
CAUSES = (
    "ID_NOT_FOUND", "EMPTY_ALIAS", "INVALID_ALIAS_FORMAT",
    "UNSUPPORTED_RELATION", "OTHER",
)
# The first reason is the projection's single primary reason. Per-component
# reason tallies can exceed the projection total (one projection has 1-3 gaps).
CAUSE_PRECEDENCE = (
    "INVALID_ALIAS_FORMAT", "UNSUPPORTED_RELATION", "ID_NOT_FOUND",
    "EMPTY_ALIAS", "OTHER",
)
EXPECTED_S7 = {
    "graded_case_count": 47,
    "expected_policy_abstention_count": 1,
    "unexpected_baseline_failure_count": 0,
    "alignment_failure_count": 0,
    "alias_missing_projection_count": 179,
    "alias_missing_component_counts": {
        "subject": 170, "predicate": 171, "object": 173,
    },
    "alias_missing_combination_counts": {
        "subject+predicate+object": 162,
        "predicate+object": 9, "subject": 6, "subject+object": 2,
    },
    "registry_literal_candidate_count": 0,
    "exact_relation_count": 0,
    "score_admission": "DISABLED",
}


def _definitions(root: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    """Read raw ontology definitions, independent of the runtime lookup."""
    value_by_role: dict[str, dict[str, dict]] = {
        "entity": {}, "predicate": {},
    }
    for file, field, role in (
        ("engineering_concepts.json", "concepts", "entity"),
        ("quantities.json", "quantities", "entity"),
        ("canonical_predicates.json", "predicates", "predicate"),
    ):
        payload = json.loads(
            (root / "grading_ontology" / file).read_text(encoding="utf-8")
        )
        rows = payload.get(field)
        if not isinstance(rows, list):
            raise ValueError("ontology definitions missing")
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise ValueError("invalid ontology definition identity")
            identifier = row["id"]
            if identifier in value_by_role[role]:
                # Exact raw duplicate IDs are a source governance ambiguity.
                # Do not silently merge them for this report.
                value_by_role[role][identifier]["duplicate_definition"] = True
            else:
                value_by_role[role][identifier] = {
                    "source_file": file,
                    "aliases": row.get("aliases"),
                    "duplicate_definition": False,
                }
    return value_by_role["entity"], value_by_role["predicate"]


def _component_info(
    role: str,
    identifier: str,
    *,
    entities: Mapping[str, dict],
    predicates: Mapping[str, dict],
    runtime_entities: Mapping[str, list[str]],
    runtime_predicates: Mapping[str, list[str]],
) -> dict[str, Any]:
    is_predicate = role == "predicate"
    definitions = predicates if is_predicate else entities
    other = entities if is_predicate else predicates
    runtime = runtime_predicates if is_predicate else runtime_entities
    # Match canonical_relation's casefold; the runtime's keys are NOT
    # independently lowercased. A mismatched key is a separate OTHER cause.
    raw = definitions.get(identifier)
    aliases = runtime.get(identifier, [])
    missing = not bool(aliases)  # EXACT same test as registry_surface_recall_audit
    detail: dict[str, Any] = {
        "id": identifier,
        "role": role,
        "missing_in_runtime": missing,
        "runtime_alias_count": len(aliases),
        "raw_definition": None if raw is None else {
            "source_file": raw["source_file"],
            "aliases": raw["aliases"],
            "duplicate_definition": raw["duplicate_definition"],
        },
    }
    if not missing:
        detail["cause"] = None
        return detail
    if raw is None:
        # ID in the wrong ontology namespace is not an unknown term:
        # it is an unsupported *role* in this relation.
        detail["cause"] = (
            "UNSUPPORTED_RELATION" if identifier in other
            else "ID_NOT_FOUND"
        )
    elif raw["duplicate_definition"]:
        detail["cause"] = "OTHER"
    elif (
        not isinstance(raw["aliases"], list)
        or any(
            not isinstance(a, str) or not _normalized(a).strip()
            for a in raw["aliases"]
        )
    ):
        detail["cause"] = "INVALID_ALIAS_FORMAT"
    elif not aliases:
        detail["cause"] = "EMPTY_ALIAS"
    else:
        detail["cause"] = "OTHER"
    return detail


class S7AliasRootCauseTrace:
    """Collect 47 identical S7 replay cases from a callback; never raw answers."""

    def __init__(
        self,
        *,
        root: Path = ROOT,
        runtime_aliases: Mapping[str, list[str]] | None = None,
        runtime_predicates: Mapping[str, list[str]] | None = None,
    ) -> None:
        self.entities, self.predicates = _definitions(root)
        self.runtime_entities = (
            _load_aliases() if runtime_aliases is None else runtime_aliases
        )
        self.runtime_predicates = (
            _load_predicates() if runtime_predicates is None else runtime_predicates
        )
        self.rows: list[dict[str, Any]] = []
        self.case_counts: dict[str, dict[str, Any]] = {}

    def observe(
        self, case_id: str, aligned: Mapping[str, Any],
        surface: Mapping[str, Any],
    ) -> None:
        if not case_id or case_id in self.case_counts:
            raise ValueError("duplicate or missing S7 case identifier")
        projections = [
            fact for fact in aligned["fact_projection"]
            if (
                fact.get("projection_status") == "VERIFIED_REGISTRY_RELATION"
                and fact.get("source_fact_id")
                and fact.get("relation_source") == "verified_registry"
                and isinstance(fact.get("relation"), dict)
            )
        ]
        if len(projections) != surface["verified_fact_projection_count"]:
            raise ValueError("S7 projection and surface audit disagree")
        combinations: Counter[str] = Counter()
        components: Counter[str] = Counter()
        for fact in projections:
            relation = fact["relation"]
            parts = {
                role: _component_info(
                    role, relation[role], entities=self.entities,
                    predicates=self.predicates,
                    runtime_entities=self.runtime_entities,
                    runtime_predicates=self.runtime_predicates,
                ) for role in COMPONENTS
            }
            missing = [role for role in COMPONENTS if parts[role]["missing_in_runtime"]]
            if not missing:
                continue
            for role in missing:
                components[role] += 1
            combinations["+".join(missing)] += 1
            causes = {parts[role]["cause"] for role in missing}
            primary = next(c for c in CAUSE_PRECEDENCE if c in causes)
            self.rows.append({
                "case_id": case_id,
                "owner_topic_id": fact["owner_topic_id"],
                "fact_id": fact["fact_id"],
                "source_fact_id": fact["source_fact_id"],
                "relation": {
                    key: relation[key] for key in
                    ("subject", "predicate", "object", "polarity", "conditions")
                },
                "missing_components": missing,
                "missing_combination": "+".join(missing),
                "primary_cause": primary,
                "component_evidence": {
                    key: parts[key] for key in COMPONENTS
                },
                "score_effect": "none",
                "approval_status": "HOLD_REVIEW_REQUIRED",
            })
        if dict(components) != surface["alias_missing_component_counts"]:
            raise ValueError("S7 component counts disagree with surface audit")
        if dict(combinations) != surface["alias_missing_combination_counts"]:
            raise ValueError("S7 combination counts disagree with surface audit")
        if sum(combinations.values()) != surface[
            "disposition_counts"
        ].get("ALIAS_INVENTORY_INCOMPLETE", 0):
            raise ValueError("S7 missing projection count disagrees")
        self.case_counts[case_id] = {
            "verified_projections": len(projections),
            "alias_missing_projections": sum(combinations.values()),
        }

    def result(self, s7_report: Mapping[str, Any]) -> dict[str, Any]:
        rows = sorted(self.rows, key=lambda r: (
            r["case_id"], r["owner_topic_id"], r["fact_id"], r["source_fact_id"]
        ))
        cause_counts: Counter[str] = Counter(row["primary_cause"] for row in rows)
        components: Counter[str] = Counter()
        combinations: Counter[str] = Counter()
        component_causes: Counter[str] = Counter()
        for row in rows:
            combinations[row["missing_combination"]] += 1
            for role in row["missing_components"]:
                components[role] += 1
                component_causes[row["component_evidence"][role]["cause"]] += 1
        scopes = {
            role: sorted({
                row["relation"][role] for row in rows
                if role in row["missing_components"]
            }) for role in COMPONENTS
        }
        all_scopes = {
            role: sorted({row["relation"][role] for row in rows})
            for role in COMPONENTS
        }
        surface = s7_report["registry_surface_recall"]
        coverage = s7_report["golden_coverage"]
        observed: dict[str, Any] = {
            "graded_case_count": s7_report["graded_case_count"],
            "expected_policy_abstention_count": s7_report[
                "expected_policy_abstention_count"
            ],
            "unexpected_baseline_failure_count": s7_report[
                "unexpected_baseline_failure_count"
            ],
            "alignment_failure_count": s7_report["alignment_failure_count"],
            "alias_missing_projection_count": len(rows),
            "alias_missing_component_counts": dict(sorted(components.items())),
            "alias_missing_combination_counts": dict(sorted(combinations.items())),
            "registry_literal_candidate_count": surface["candidate_count"],
            "exact_relation_count": coverage[
                "alignment_relation_counts"
            ].get("EXACT_RELATION", 0),
            "score_admission": s7_report["score_admission"],
        }
        mismatches = {
            key: {"expected": value, "observed": observed[key]}
            for key, value in EXPECTED_S7.items()
            if observed[key] != value
        }
        if len(rows) != sum(cause_counts.values()):
            mismatches["primary_cause_partition"] = {
                "expected": len(rows), "observed": sum(cause_counts.values())
            }
        if sum(self.case_counts[c]["alias_missing_projections"]
               for c in self.case_counts) != len(rows):
            mismatches["per_case_projection_accounting"] = {
                "expected": len(rows),
                "observed": sum(
                    c["alias_missing_projections"] for c in self.case_counts
                ),
            }
        return {
            "schema_version": VERSION,
            "status": "REPRODUCED_BASELINE" if not mismatches else "BASELINE_MISMATCH",
            "score_effect": "none",
            "score_admission": "DISABLED",
            "approval_status": "HOLD_NO_AUTOMATIC_ONTOLOGY_CHANGES",
            "baseline_reproduction": {
                "expected": EXPECTED_S7,
                "observed": observed,
                "mismatches": mismatches,
            },
            "projection_count_with_duplicates": len(rows),
            "per_case": dict(sorted(self.case_counts.items())),
            "unique_topic_fact_count": len({
                (row["owner_topic_id"], row["fact_id"]) for row in rows
            }),
            "unique_source_fact_count": len({
                (row["owner_topic_id"], row["source_fact_id"]) for row in rows
            }),
            "duplicate_projection_count_vs_unique_topic_fact": len(rows) - len({
                (row["owner_topic_id"], row["fact_id"]) for row in rows
            }),
            "unique_missing_ids_by_role": scopes,
            "unique_missing_id_counts_by_role": {
                role: len(scopes[role]) for role in COMPONENTS
            },
            "unique_all_ids_in_missing_projections_by_role": all_scopes,
            "primary_cause_projection_counts": {
                cause: cause_counts[cause] for cause in CAUSES
            },
            "component_cause_counts_non_partition": {
                cause: component_causes[cause] for cause in CAUSES
            },
            "missing_combination_counts": dict(sorted(combinations.items())),
            "rows": rows,
            "limitations": [
                "Exact ontology identifier/alias inventory is not technical evidence.",
                "Same case can project the same Fact multiple times; projections are not unique facts.",
                "Candidate alias wording needs independent evidence and false-positive testing.",
                "No answer text, learner grade or candidate approval appears in this report.",
            ],
        }
