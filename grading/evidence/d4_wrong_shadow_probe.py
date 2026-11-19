"""Narrow research-only probes for the six D4-WRONG-01 misses.

This module is deliberately disconnected from grading and scoring.  It emits
surface-supported candidates only; callers must not treat candidates as
WRONG, score evidence, or verified semantic matches.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable


VERSION = "d4_wrong_shadow_probe_v1"
_SENTENCE = re.compile(r"[^\n!?。]+?(?:\.(?![A-Za-z0-9])|[!?。]|\n|$)")
_QUOTE_PAIRS = (("\"", "\""), ("“", "”"), ("‘", "’"), ("「", "」"), ("『", "』"))
_REJECT = re.compile(r"(?:틀린|잘못된|오류|부정확|wrong|incorrect)", re.I)
_CORRECTION = re.compile(r"(?:정정|바로잡|오히려|실제로는|correct(?:ion|ly)?)", re.I)
_DENIES_RELATION = re.compile(
    r"(?:(?:같|동일|same|equal|identical).{0,12}(?:않|아니)|"
    r"(?:not|never)\s+(?:the\s+)?(?:same|equal|identical)|"
    r"(?:항상|always).{0,32}(?:것은\s*)?(?:않|아니)|"
    r"(?:증가|늘|변경|바꾸|increase|change|irrelevant|무관).{0,7}(?:않|아니|not)|"
    r"(?:않|아니|not).{0,7}(?:항상|always|증가|늘|변경|바꾸|increase|change|irrelevant|무관))",
    re.I,
)

# These bounded surface patterns were derived from the six approved, source-
# verified Registry fact families.  The family key is a research crosswalk,
# not an assertion of semantic equivalence or scoring authority.
_RULES = {
    "humidity_relative_vs_absolute": {
        "topic": "humidity_measurement_capacitive_resistive_dew_point_selection_compensation",
        "fact": "absolute_humidity_definition",
        "left": re.compile(r"(?:상대\s*습도|relative\s*humidity|\bRH\b)", re.I),
        "right": re.compile(r"(?:절대\s*습도|absolute\s*humidity|\bAH\b)", re.I),
        "contradict": re.compile(r"(?:같은\s*(?:물리량|값|개념)|동일한\s*(?:물리량|값|개념)|same\s+(?:physical\s+)?quantity|equal\s+(?:physical\s+)?quantity|equivalent)", re.I),
        "support": re.compile(r"(?:비율|단위\s*체적당.{0,12}질량|질량\s*/\s*체적|mass\s*concentration|different|다르)", re.I),
    },
    "diaphragm_sensor_vs_seal": {
        "topic": "pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error",
        "fact": "diaphragm_sensor_vs_seal",
        "left": re.compile(r"(?:압력\s*감지\s*)?(?:다이어프램|다이아프램|diaphragm)(?!\s*(?:seal|씰))", re.I),
        "right": re.compile(r"(?:다이어프램\s*)?(?:씰|seal|remote\s*seal)", re.I),
        "contradict": re.compile(r"(?:같|동일|same|identical|equivalent)", re.I),
        "support": re.compile(r"(?:다르|별개|구분|different|distinct|격리)", re.I),
    },
    "rpm_vs_pulse_frequency": {
        "topic": "speed_rotation_measurement_encoder_proximity_tachometer_selection_error",
        "fact": "pulse_frequency_speed_equation",
        "left": re.compile(r"(?:회전\s*속도|\bRPM\b|\brpm\b)", re.I),
        "right": re.compile(r"(?:pulse\s*frequency|펄스\s*(?:주파수|빈도)|\bHz\b)", re.I),
        "contradict": re.compile(r"(?:같|동일|same|equal|equivalent)", re.I),
        "support": re.compile(r"(?:60\s*[fF]|N_eff|유효\s*(?:계수|count)|PPR.{0,20}(?:정의|복호)|frequency.{0,20}counts)", re.I),
        "extra_contradict": re.compile(r"(?:PPR|펄스\s*수).{0,16}(?:무관|필요\s*없|irrelevant)", re.I),
    },
    "thermocouple_intermediate_metal": {
        "topic": "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
        "fact": "thermocouple_law_of_intermediate_metals",
        "left": re.compile(r"(?:제\s*3(?:의)?\s*금속|제삼(?:의)?\s*금속|중간\s*금속|추가\s*금속|third\s*metal|intermediate\s*metal)", re.I),
        "right": re.compile(r"(?:기전력|열기전력|emf|junction\s*temperature|접점\s*온도)", re.I),
        "contradict": re.compile(r"(?:항상|언제나|무관|상관\s*없이|independent(?:\s+of)?|always)", re.I),
        "support": re.compile(r"(?:같은\s*온도|동일\s*온도|등온|isothermal|same\s*temperature).{0,35}(?:변하|영향|순\s*기전력|net\s*emf|않)", re.I),
    },
    "x4_decoding_vs_channel_ppr": {
        "topic": "speed_rotation_measurement_encoder_proximity_tachometer_selection_error",
        "fact": "encoder_resolution_ppr_cpr_definition",
        "left": re.compile(r"(?:x\s*4|4\s*체배|4\s*배\s*복호|quadrature\s*x4)", re.I),
        "right": re.compile(r"(?:채널\s*)?(?:PPR|CPR|channel\s*pulses?\s*per\s*rev)", re.I),
        "contradict": re.compile(r"(?:증가|늘어나|바뀌|변경|increase|changes?|becomes?)", re.I),
        "support": re.compile(r"(?:N_eff|유효\s*(?:계수|count)|에지\s*계수|edge\s*count).{0,35}(?:PPR|채널|physical|물리)", re.I),
    },
    "decoded_count_rate_vs_channel_frequency": {
        "topic": "speed_rotation_measurement_encoder_proximity_tachometer_selection_error",
        "fact": "encoder_frequency_limit_selection",
        "left": re.compile(r"(?:f_count|계수\s*(?:율|이벤트율|주파수|빈도)|유효\s*계수(?:율|주파수|빈도)|count\s*rate|counting\s*rate|counter\s*rate|(?:internal\s+)?count\s+events?\s+per\s+second)", re.I),
        "right": re.compile(r"(?:f_ch|채널\s*(?:주파수|빈도)|channel\s*frequency|A\s*(?:상|채널).{0,8}(?:주파수|빈도|frequency|Hz)|(?:encoder\s+)?A[- ]channel\s+(?:output\s+)?frequency)", re.I),
        "contradict": re.compile(r"(?:같|동일|항상|same|equal|identical|always|=)", re.I),
        "support": re.compile(r"(?:f_count|계수\s*(?:율|이벤트율)|count\s*rate).{0,80}(?:f_ch|채널\s*(?:주파수|빈도)|channel\s*frequency).{0,80}(?:별도|다르|복호\s*모드|x\s*[124]|N_eff|PPR)|(?:f_ch|채널\s*(?:주파수|빈도)|channel\s*frequency).{0,80}(?:f_count|계수\s*(?:율|이벤트율)|count\s*rate).{0,80}(?:별도|다르|복호\s*모드|x\s*[124]|N_eff|PPR)", re.I),
    },
}


def _norm(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def _context(answer_text: str, cue_start: int) -> str:
    for opening, closing in _QUOTE_PAIRS:
        left = answer_text.rfind(opening, 0, cue_start + 1)
        right = answer_text.find(closing, cue_start)
        if left >= 0 and right >= cue_start:
            suffix = answer_text[right + len(closing):right + len(closing) + 32]
            return "rejected" if _REJECT.search(suffix) else "quoted"
    local = answer_text[max(0, cue_start - 32):cue_start + 32]
    if _CORRECTION.search(local) and _REJECT.search(local):
        return "rejected"
    return "asserted"


def _candidate_relation(sentence: str, rule: dict[str, Any]) -> tuple[str, int, int] | None:
    text = _norm(sentence)
    left = rule["left"].search(text)
    right = rule["right"].search(text)
    if not left or not right:
        return None
    cue = rule["contradict"].search(text)
    support = rule["support"].search(text)
    extra = rule.get("extra_contradict")
    extra_match = extra.search(text) if extra else None
    cues = [("opposes_fact", cue)] if cue else []
    cues += [("opposes_fact", extra_match)] if extra_match else []
    if support:
        cues.append(("supports_fact", support))
    if not cues:
        return ("unresolved", min(left.start(), right.start()), max(left.end(), right.end()))
    # Relation cue must occur between or adjacent to the two observed concepts.
    # A sentence with contradictory support/opposition cues is deliberately unresolved.
    states = {state for state, _ in cues}
    if len(states) != 1:
        return ("unresolved", min(left.start(), right.start()), max(left.end(), right.end()))
    state = next(iter(states))
    chosen = min((m for _, m in cues if m), key=lambda m: m.start())
    window = text[max(0, chosen.start() - 4):min(len(text), chosen.end() + 22)]
    denied = _DENIES_RELATION.search(window)
    if state == "opposes_fact" and denied:
        # Explicitly denied error language is not an assertion of the error.
        return ("supports_fact", min(left.start(), right.start()), max(left.end(), right.end()))
    return (state, min(left.start(), right.start()), max(left.end(), right.end()))


def extract_d4_shadow_candidates(answer_text: str) -> dict[str, Any]:
    """Extract bounded surface candidates; never emits a score or WRONG state."""
    candidates: list[dict[str, Any]] = []
    unresolved = 0
    for match in _SENTENCE.finditer(answer_text):
        sentence = match.group(0)
        for family, rule in _RULES.items():
            relation = _candidate_relation(sentence, rule)
            if relation is None:
                continue
            state, _, _ = relation
            cue = rule["contradict"].search(_norm(sentence)) or rule["support"].search(_norm(sentence))
            cue_at = cue.start() if cue else 0
            context = _context(answer_text, match.start() + cue_at)
            if context in {"quoted", "rejected"}:
                state = context
            if state == "unresolved":
                unresolved += 1
            candidates.append({
                "relation_family": family,
                "surface_relation": state,
                "assertion_context": context,
                "source_span": {"start": match.start(), "end": match.end()},
                "conditions": [],
                "condition_status": "NOT_EXTRACTED",
                "score_effect": "none",
            })
    return {
        "schema_version": VERSION,
        "mode": "RESEARCH_SHADOW_ONLY",
        "candidates": candidates,
        "unresolved_count": unresolved,
        "accuracy_status": "NOT_ESTABLISHED",
        "score_admission": "DISABLED",
        "score_effect": "none",
    }


def compare_d4_shadow_candidates(
    extraction: dict[str, Any],
    *,
    verified_fact_refs: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Attach caller-supplied approved Fact scope; never selects it from text."""
    if (
        not isinstance(extraction, dict)
        or extraction.get("schema_version") != VERSION
        or not isinstance(extraction.get("candidates"), list)
        or any(not isinstance(row, dict) for row in extraction.get("candidates", []))
    ):
        return {"status": "REJECTED_INPUT", "comparisons": [], "score_effect": "none"}
    registry_path = Path(__file__).resolve().parents[2] / "grading/evidence/approved_fact_registry.json"
    approved_rows = json.loads(registry_path.read_text(encoding="utf-8")).get("facts", [])
    approved_by_id = {row.get("fact_id"): row for row in approved_rows if isinstance(row, dict)}
    refs = [row for row in verified_fact_refs if isinstance(row, dict)]
    counts: dict[str, int] = {}
    for row in refs:
        fact_id = str(row.get("fact_id") or "")
        counts[fact_id] = counts.get(fact_id, 0) + 1
    by_family = {}
    for family, rule in _RULES.items():
        scoped = [
            row for row in refs
            if row.get("legacy_anchor_id") == rule["fact"]
            and row.get("topic_id") == rule["topic"]
            and row.get("verification_status") == "verified"
            and row.get("review_status") == "approved"
            and counts.get(str(row.get("fact_id") or "")) == 1
            and approved_by_id.get(row.get("fact_id")) == row
        ]
        if len(scoped) == 1:
            by_family[family] = scoped[0]
    comparisons = []
    for candidate in extraction.get("candidates", []):
        family = candidate.get("relation_family") if isinstance(candidate, dict) else None
        ref = by_family.get(family)
        if ref is None:
            comparisons.append({"relation_family": family, "status": "UNRESOLVED", "source_match_proven": False})
            continue
        relation = candidate.get("surface_relation")
        context = candidate.get("assertion_context")
        if context in {"quoted", "rejected"}:
            status = "NON_ASSERTED"
        elif relation == "opposes_fact":
            status = "CONTRADICT_CANDIDATE"
        elif relation == "supports_fact":
            status = "SUPPORT_CANDIDATE"
        else:
            status = "UNRESOLVED"
        comparisons.append({
            "relation_family": family,
            "comparison_fact_id": ref.get("fact_id"),
            "status": status,
            "source_match_proven": False,
            "accuracy_status": "NOT_ESTABLISHED",
            "condition_status": "NOT_EXTRACTED",
            "score_effect": "none",
        })
    return {
        "status": "RESEARCH_ONLY",
        "comparisons": comparisons,
        "accuracy_status": "NOT_ESTABLISHED",
        "score_admission": "DISABLED",
        "score_effect": "none",
    }
