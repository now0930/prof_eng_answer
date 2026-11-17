"""S7 nonformula source-relation triage and narrow lexical pilot (research only).

Four text cues are deliberately *not* canonical Claim-Fact extraction or new
aliases. They have no scoring authority; unrecognized or conflicting wording
is always held for review. Other ten cases are classified, not auto-parsed.
"""
from __future__ import annotations

from collections import Counter
import re
import unicodedata
from typing import Any

from grading.evidence.s7_registry_formula_shadow import SPECS as FORMULA_SPECS

VERSION = "s7_nonformula_surface_triage.v1"
SOURCE_STATUS = "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
BRIDGE_STATUS = "BORROWED_SOURCE_IDS_ONLY_RESEARCH_INCONCLUSIVE"

# Each item is (triage group, verified-source predicate). The group records an
# engineering review task, not a truth claim or a new ontology class.
TRIAGE: dict[str, tuple[str, str]] = {
    "effective_unbalanced_area": ("DEFINITION_OR_CONSTRUCTION", "is"),
    "sw06_baseline_approved_reference": ("DEFINITION_OR_CONSTRUCTION", "is"),
    "deadband_definition_direction_reversal": ("DEFINITION_OR_CONSTRUCTION", "has"),
    "single_port_globe_throttling_structure": ("DEFINITION_OR_CONSTRUCTION", "uses"),
    "rtd_four_wire_kelvin_measurement": ("DEFINITION_OR_CONSTRUCTION", "reduces"),
    "safe_state_process_hazard_basis": ("CONDITIONAL_DEPENDENCY", "depends_on"),
    "residual_frequency_before_sif": ("CONDITIONAL_DEPENDENCY", "equals"),
    "thermocouple_measures_temperature_difference": ("CONDITIONAL_DEPENDENCY", "depends_on"),
    "rh_temperature_dependence": ("TREND_OR_TIME_BASIS", "changes"),
    "radar_pulse_time_of_flight": ("TREND_OR_TIME_BASIS", "measures"),
    "sw04_v_model_definition": ("MAPPING_OR_TRACEABILITY", "maps"),
    "nyquist_contour_and_mapping": ("MAPPING_OR_TRACEABILITY", "maps"),
    "closed_loop_rhp_poles_count": ("POLE_ZERO_SCOPE_COUNT", "counts"),
    "open_loop_rhp_poles_count": ("POLE_ZERO_SCOPE_COUNT", "counts"),
}

# Only these four are currently suitable for bounded surface-form probes.
PILOT = frozenset({
    "single_port_globe_throttling_structure",
    "rtd_four_wire_kelvin_measurement",
    "rh_temperature_dependence",
    "radar_pulse_time_of_flight",
})
_EXPECTED = "EXPECTED_SURFACE_CUE_NOT_SEMANTICALLY_VALIDATED"
_CONTRARY = "CONTRARY_SURFACE_CUE_REVIEW"
_UNRESOLVED = "NO_UNAMBIGUOUS_SURFACE_CUE"
_AMBIGUOUS = "AMBIGUOUS_SURFACE_CUE_HOLD"
_REJECTED = "ASSERTION_CONTEXT_UNVERIFIED"
_REJECTION = re.compile(
    r"(?:틀리(?:다|며|다고|ㄴ)|잘못(?:된|이다|이라고)|오류|"
    r"성립하지|아니라고\s*주장|incorrect|invalid)",
    re.I,
)


def _normalized(s: str) -> str:
    return unicodedata.normalize("NFKC", s).casefold()


def _surface_cue(fact_id: str, answer: str) -> str:
    """Return answer-derived syntax cues, never a verified relation or verdict."""
    if fact_id not in PILOT:
        raise ValueError("not an explicitly scoped S7 nonformula pilot")
    s = _normalized(answer)
    if _REJECTION.search(s):
        return _REJECTED

    owner = False
    expected = False
    contrary = False
    if fact_id == "single_port_globe_throttling_structure":
        owner = bool(re.search(r"single\s*-?\s*port\s+globe", s))
        one = bool(re.search(r"(?:한\s*개|1\s*개)\s*(?:의\s*)?시트링", s))
        two = bool(re.search(r"(?:두\s*개|2\s*개)\s*(?:의\s*)?시트링", s))
        expected = one and ("선형" in s or "직선 이동" in s)
        contrary = two
    elif fact_id == "rtd_four_wire_kelvin_measurement":
        owner = "rtd" in s and (
            bool(re.search(r"4\s*선식", s)) or bool(re.search(r"2\s*선식", s))
        )
        expected = (
            bool(re.search(r"4\s*선식\s+kelvin\s+rtd", s))
            and "전류 인가 두 선" in s
            and "고입력 임피던스" in s
            and "전압 검출 두 선" in s
            and "분리" in s
            and "오차" in s
            and any(word in s for word in ("줄인다", "줄이", "감소"))
        )
        contrary = (
            bool(re.search(r"2\s*선식\s+rtd", s))
            and ("4선식과 같은" in s or "별도 검출선 없이" in s)
        )
    elif fact_id == "rh_temperature_dependence":
        owner = (
            "수증기 분압" in s and "일정" in s
            and bool(re.search(r"온도[가는은]?\s*(?:증가|상승|높아)", s))
        )
        expected = bool(re.search(
            r"상대습도[가는은]?\s*(?:감소|낮아|줄|떨어)", s
        ))
        contrary = bool(re.search(
            r"상대습도[가는은]?\s*(?:반드시\s*)?(?:증가|상승|높아)", s
        ))
    elif fact_id == "radar_pulse_time_of_flight":
        owner = (
            bool(re.search(r"fmr56\s*/\s*fmr57", s))
            and "왕복" in s and "레이더" in s
        )
        expected = bool(re.search(
            r"(?<![a-z0-9_])d\s*=\s*c\s*\*?\s*t\s*/\s*2(?![0-9])", s
        ))
        contrary = bool(re.search(
            r"(?<![a-z0-9_])d\s*=\s*c\s*\*?\s*t(?!\s*/\s*2|[a-z0-9_])", s
        ))

    if not owner:
        return _UNRESOLVED
    if expected and contrary:
        return _AMBIGUOUS
    if expected:
        return _EXPECTED
    if contrary:
        return _CONTRARY
    return _UNRESOLVED


def evaluate_nonformula_triage(
    source_review: dict[str, Any],
    challenge: dict[str, Any],
    bridge: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Classify 14 source-owned relations, test only four author-draft pairs."""
    if (
        source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
        or source_review.get("status") != SOURCE_STATUS
        or challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
        or challenge.get("adjudication_status") != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
        or bridge.get("schema_version") != "s7_registry_relation_bridge.v1"
        or bridge.get("status") != BRIDGE_STATUS
        or bridge.get("candidate_decision") != "HOLD"
        or bridge.get("automatic_alias_admission") is not False
        or any(obj.get("score_admission") != "DISABLED"
               for obj in (source_review, challenge, bridge))
        or source_review.get("score_effect") != "none"
        or bridge.get("score_effect") != "none"
        or bridge.get("source_inventory_execution_sha")
        != source_review.get("inventory_execution_sha")
        or bridge.get("execution_commit_sha")
        != source_review.get("inventory_execution_sha")
    ):
        raise ValueError("source, challenge, bridge baselines unsafe or not identical")
    src_rows = source_review.get("rows")
    cases = challenge.get("cases")
    bridge_rows = bridge.get("rows")
    if not all(isinstance(x, list) for x in (src_rows, cases, bridge_rows)):
        raise ValueError("missing triage evidence")
    if strict and (
        len(src_rows) != 119 or len(cases) != 20 or len(bridge_rows) != 20
        or source_review.get("unique_topic_fact_count") != 119
        or source_review.get("projection_count_with_duplicates") != 179
        or source_review.get("decision_counts", {}).get("HOLD") != 119
        or source_review.get("decision_counts", {}).get("ACCEPT") != 0
        or bridge.get("formula_source_id_candidate_count") != 6
        or bridge.get("uncovered_nonformula_fact_count") != 14
    ):
        raise ValueError("119/179/20/6/14 triage baseline drift")
    if set(TRIAGE) & set(FORMULA_SPECS) or len(TRIAGE) != 14 or len(PILOT) != 4:
        raise ValueError("nonformula scope is not disjoint from original six")
    index = {(x["owner_topic_id"], x["fact_id"]): x for x in src_rows}
    b_index = {(x["owner_topic_id"], x["fact_id"]): x for x in bridge_rows}
    if len(index) != len(src_rows) or len(b_index) != len(bridge_rows):
        raise ValueError("duplicate source or bridge Fact")
    triage_rows: list[dict[str, Any]] = []
    visited: set[tuple[str, str]] = set()
    groups: Counter[str] = Counter()
    cues_positive: Counter[str] = Counter()
    cues_adversarial: Counter[str] = Counter()
    for case in cases:
        fid = case.get("fact_id")
        if fid not in TRIAGE:
            continue
        owner = case.get("owner_topic_id")
        key = owner, fid
        if key in visited:
            raise ValueError("duplicate 14-Fact challenge identity")
        visited.add(key)
        source = index.get(key)
        joined = b_index.get(key)
        if source is None or joined is None:
            raise ValueError("14-Fact source or bridge missing")
        if (
            case.get("score_effect") != "none"
            or case.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
            or case.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"
            or source.get("review_decision") != "HOLD"
            or source.get("registry_review_status") != "approved"
            or source.get("registry_verification_status") != "verified"
            or not source.get("registry_verification_refs")
            or source.get("technical_equivalence_of_candidate") != "NOT_ASSESSED"
            or source.get("candidate_alias") is not None
            or source.get("score_effect") != "none"
            or joined.get("score_effect") != "none"
            or joined.get("source_fact_id") != source.get("source_fact_id")
            or joined.get("source_relation_candidate_not_answer_parsed") is not None
            or joined.get("positive_probe_status") != "NO_FORMULA_SHADOW_COVERAGE"
            or source.get("relation", {}).get("subject")
            != case.get("relation_subject_id")
            or source.get("relation", {}).get("predicate") != TRIAGE[fid][1]
            or source.get("relation", {}).get("polarity") != "positive"
        ):
            raise ValueError("source-owned nonformula relation or status drift")
        cat = TRIAGE[fid][0]
        pilot = fid in PILOT
        results: dict[str, str] = {}
        for kind, field in (("positive", "positive_answer"),
                            ("adversarial", "adversarial_answer")):
            answer = case.get(field)
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("invalid author-draft test sentence")
            results[kind] = _surface_cue(fid, answer) if pilot else "NOT_PROBED"
        groups[cat] += 1
        if pilot:
            cues_positive[results["positive"]] += 1
            cues_adversarial[results["adversarial"]] += 1
        triage_rows.append({
            "case_id": case["case_id"],
            "owner_topic_id": owner,
            "fact_id": fid,
            "source_fact_id": source["source_fact_id"],
            "source_predicate_id": source["relation"]["predicate"],
            "source_condition_id_count_not_verified_by_answer":
                len(source["relation"]["conditions"]),
            "triage_group_research_only": cat,
            "pilot_selected": pilot,
            "positive_surface_cue": results["positive"],
            "adversarial_surface_cue": results["adversarial"],
            "answer_relation_extraction": "NOT_ESTABLISHED",
            "score_effect": "none",
        })
    if len(triage_rows) != 14 or len(visited) != 14:
        raise ValueError("14 nonformula Fact classification incomplete")
    status = (
        "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY"
        if cues_positive[_EXPECTED] == 4 and cues_adversarial[_CONTRARY] == 4
        else "NONFORMULA_PILOT_CUE_MISMATCH_HOLD"
    )
    return {
        "schema_version": VERSION,
        "status": status,
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "score_effect": "none",
        "score_admission": "DISABLED",
        "automatic_alias_admission": False,
        "candidate_decision": "HOLD",
        "author_draft_labels_only": True,
        "nonformula_fact_count": len(triage_rows),
        "triage_group_counts": dict(sorted(groups.items())),
        "pilot_fact_count": len(PILOT),
        "pilot_positive_surface_cues": dict(sorted(cues_positive.items())),
        "pilot_adversarial_surface_cues": dict(sorted(cues_adversarial.items())),
        "unprobed_nonformula_fact_count": len(triage_rows) - len(PILOT),
        "answer_parsed_exact_relations": None,
        "measured_accuracy": None,
        "measured_precision": None,
        "measured_recall": None,
        "rows": sorted(triage_rows, key=lambda x: x["fact_id"]),
        "limitations": [
            "Research type taxonomy is analyst judgment based on verified Registry predicates.",
            "Only four tightly scoped phrase/symbol pilots, not a general natural-language parser.",
            "Original 14 author-drafted positive/negative pairs have no independent labels.",
            "Surface patterns cannot establish the asserted engineering conditions or truth.",
            "No source or answer text, scoring, canonical aliases, or ontology is modified.",
        ],
    }
