"""Small answer-derived S7 Claim/Fact shadow; never part of grading."""
from __future__ import annotations

import re
from typing import Any

VERSION = "s7_answer_derived_shadow.v1"
_FACTS = {
    "deadband_definition_direction_reversal": ("deadband", ("입력 방향을 반전", "입력 방향 반전"), ("출력 변화가 없", "출력 변화 없는")),
    "sw06_baseline_approved_reference": ("baseline", ("승인된 기준선", "공식 승인"), ("변경 관리", "기준")),
    "effective_unbalanced_area": ("area", ("실효 불평형 면적", "등가 투영 면적"), ("압력 작용면", "밸브 구조")),
    "sw04_v_model_definition": ("vmodel", ("개발 단계", "설계 단계"), ("검증 단계", "시험 단계")),
    "nyquist_contour_and_mapping": ("nyquist", ("우반평면", "Nyquist 경로"), ("L(s)", "복소평면")),
}
_NEG = re.compile(r"(?:아니|않|없다|무관|틀리|잘못|부정확|not\b|never\b)", re.I)
_QUOTE = re.compile(r'["“”‘’「」『』]')


def _sentences(text: str) -> list[tuple[str, int, int]]:
    return [(m.group(), m.start(), m.end()) for m in re.finditer(r"[^.!?。\n]+(?:[.!?。]|$)", text)]


def extract_answer_claims(answer_text: str) -> dict[str, Any]:
    """Extract only answer-visible surface cues. No Fact/Registry input is accepted."""
    if not isinstance(answer_text, str):
        raise ValueError("answer_text must be a string")
    claims = []
    for sentence, start, end in _sentences(answer_text):
        norm = sentence.casefold()
        for fid, (kind, subject_cues, object_cues) in _FACTS.items():
            if kind == "deadband":
                subject = next((x for x in subject_cues if x in norm), None)
                obj = next((x for x in object_cues if x in norm), None)
                relation = "정의/특성" if subject and obj else None
            elif kind == "baseline":
                subject = next((x for x in subject_cues if x in norm), None)
                obj = next((x for x in object_cues if x in norm), None)
                relation = "기준으로 사용" if subject and obj else None
            elif kind == "area":
                subject = next((x for x in subject_cues if x in norm), None)
                obj = next((x for x in object_cues if x in norm), None)
                relation = "결정에 의존" if subject and obj else None
            elif kind == "vmodel":
                subject = next((x for x in subject_cues if x in norm), None)
                obj = next((x for x in object_cues if x in norm), None)
                relation = "단계 대응" if subject and obj else None
            else:
                subject = next((x for x in subject_cues if x in norm), None)
                obj = next((x for x in object_cues if x in norm), None)
                relation = "사상" if subject and obj else None
            if not relation:
                continue
            # Quoted/negated, multi-cue, or uncertain surface statements abstain.
            cue_count = sum(x in norm for x in subject_cues + object_cues)
            quoted = bool(_QUOTE.search(sentence))
            negated = bool(_NEG.search(norm))
            status = "ABSTAIN" if quoted or negated or cue_count != 2 else "SURFACE_CLAIM_REVIEW_ONLY"
            claims.append({
                "surface_subject": subject,
                "surface_relation": relation,
                "surface_object": obj,
                "polarity": "NEGATIVE" if negated else "POSITIVE",
                "conditions": [],
                "condition_status": "NOT_EXTRACTED",
                "evidence_span": {"start": start, "end": end},
                "extraction_status": status,
                "candidate_fact_hint": fid,
            })
    return {"schema_version": VERSION, "mode": "RESEARCH_ONLY", "claims": claims,
            "score_admission": "DISABLED", "score_effect": "none"}


def compare_claim_to_registry(claim: dict[str, Any], registry_fact: dict[str, Any]) -> dict[str, Any]:
    """Compare an independently extracted surface claim to a verified relation."""
    relation = registry_fact.get("relation") if isinstance(registry_fact, dict) else None
    if (not isinstance(claim, dict) or claim.get("extraction_status") != "SURFACE_CLAIM_REVIEW_ONLY"
            or not isinstance(relation, dict) or registry_fact.get("verification_status") != "verified"
            or registry_fact.get("review_status") != "approved"):
        status = "ABSTAIN"
    else:
        # Surface strings are not Registry IDs; without a reviewed alias mapping,
        # semantic identity is not established by lexical overlap.
        status = "NOT_ESTABLISHED"
    return {"status": status, "source_match_proven": False,
            "score_admission": "DISABLED", "score_effect": "none"}


def evaluate_answer_shadow(answer_text: str, registry_facts: list[dict[str, Any]]) -> dict[str, Any]:
    extracted = extract_answer_claims(answer_text)
    comparisons = []
    for claim in extracted["claims"]:
        fact = next((f for f in registry_facts if f.get("fact_id") == claim.get("candidate_fact_hint")), None)
        comparisons.append(compare_claim_to_registry(claim, fact or {}))
    return {**extracted, "comparisons": comparisons, "accuracy": None,
            "accuracy_status": "NOT_ESTABLISHED", "score_admission": "DISABLED", "score_effect": "none"}
