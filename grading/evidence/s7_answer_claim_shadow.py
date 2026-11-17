"""Answer-derived S7 surface Claim pilot. Isolated from operational grading."""
from __future__ import annotations

import re
from typing import Any

VERSION = "s7_answer_derived_shadow.v1"
_QUOTE = re.compile(r'["“”‘’「」『』]')
_SUBJECTS = {
    "deadband": ("제어밸브 데드밴드", "데드밴드"),
    "baseline": ("승인된 기준선", "형상 기준선"),
    "area": ("실효 불평형 면적",),
    "vmodel": ("개발 단계", "설계 단계"),
    "nyquist": ("Nyquist 경로", "Nyquist contour"),
}


def _span(sentence: str, offset: int, text: str) -> dict[str, int]:
    at = sentence.find(text)
    return {"start": offset + at, "end": offset + at + len(text)}


def _split_sentences(text: str):
    return [(m.group(), m.start()) for m in re.finditer(r"[^.!?。\n]+(?:[.!?。]|$)", text)]


def extract_answer_claims(answer_text: str) -> dict[str, Any]:
    """Parse a small set of explicit Korean surface relations from answer text only."""
    if not isinstance(answer_text, str):
        raise ValueError("answer_text must be a string")
    claims = []
    for sentence, offset in _split_sentences(answer_text):
        text = sentence.strip()
        left_trim = len(sentence) - len(sentence.lstrip())
        base = offset + left_trim
        norm = text.casefold()
        # A quoted assertion is reported only as an abstention; it is not the
        # author's asserted relation. This pilot does not resolve attribution.
        quoted = bool(_QUOTE.search(text))
        rows = []
        patterns = [
            ("deadband", re.compile(r"(?P<s>제어밸브\s*데드밴드|데드밴드)는\s*(?:입력\s*방향(?:을)?\s*반전(?:할\s*때|시))\s*(?P<p>출력\s*변화가\s*없는|출력\s*변화가\s*발생하지\s*않는)\s*(?P<o>입력\s*구간|범위)")),
            ("baseline", re.compile(r"(?P<s>승인된\s*기준선|형상\s*기준선)은\s*(?P<o>변경\s*관리(?:의)?\s*기준)(?P<p>으로\s*사용(?:된다|한다)?)")),
            ("area", re.compile(r"(?P<s>실효\s*불평형\s*면적)은\s*(?P<o>압력\s*작용면과\s*밸브\s*구조)(?P<p>에\s*따라\s*결정(?:된다|한다)?)")),
            ("vmodel", re.compile(r"(?P<s>개발\s*단계|설계\s*단계)는\s*(?P<o>검증\s*단계|시험\s*단계)(?P<p>에\s*대응(?:한다|된다)?)")),
            ("nyquist", re.compile(r"(?P<s>Nyquist\s*(?:경로|contour))(?:은|는)\s*(?P<o>우반평면)을\s*(?P<p>둘러싸고)" , re.I)),
            ("nyquist_mapping", re.compile(r"(?P<s>L\s*\(\s*s\s*\))의\s*(?P<o>복소평면)\s*(?P<p>사상)" , re.I)),
        ]
        if "데드밴드" in text and re.search(r"입력\s*방향.*무관", text):
            m = re.search(r"(?P<s>데드밴드)는\s*(?P<o>입력\s*방향)(?P<p>.*?무관)", text)
            if m:
                claims.append({"surface_kind": "deadband", "subject": {"text": m.group("s"), "span": {"start": base+m.start("s"), "end": base+m.end("s")}},
                    "relation": {"text": m.group("p"), "span": {"start": base+m.start("p"), "end": base+m.end("p")}},
                    "object": {"text": m.group("o"), "span": {"start": base+m.start("o"), "end": base+m.end("o")}},
                    "polarity": "NEGATIVE_OR_AMBIGUOUS", "conditions": [], "condition_status": "NOT_EXTRACTED",
                    "evidence_span": {"start": base+m.start(), "end": base+m.end()}, "extraction_status": "ABSTAIN"})
        for kind, pattern in patterns:
            for match in pattern.finditer(text):
                rows.append((kind, match))
        for kind, match in rows:
            # Negation scoped to the relation phrase; deadband's "변화가 없는"
            # is the positive definition, not negation of the whole relation.
            relation_text = match.group("p")
            negative = bool(re.search(r"(?:무관|관계가\s*없|not\b|never\b|틀리|잘못)", text, re.I))
            ambiguous_negation = negative or (kind != "deadband" and "않" in relation_text)
            if quoted or ambiguous_negation:
                status, polarity = "ABSTAIN", "NEGATIVE_OR_AMBIGUOUS" if negative else "UNKNOWN"
            else:
                status, polarity = "SURFACE_CLAIM_REVIEW_ONLY", "POSITIVE"
            fields = {name: {"text": match.group(name), "span": {"start": base + match.start(name), "end": base + match.end(name)}}
                      for name in ("s", "p", "o")}
            claims.append({
                "surface_kind": kind,
                "subject": fields["s"], "relation": fields["p"], "object": fields["o"],
                "polarity": polarity, "conditions": [], "condition_status": "NOT_EXTRACTED",
                "evidence_span": {"start": base + match.start(), "end": base + match.end()},
                "extraction_status": status,
            })
        # Recognizable topic terms without the complete supported relation are
        # explicitly unresolved; no Registry facts are consulted to fill gaps.
        if not rows and not any(c["evidence_span"]["start"] >= base and c["evidence_span"]["end"] <= base + len(text) for c in claims):
            for kind, subjects in _SUBJECTS.items():
                hit = next((s for s in subjects if s.casefold() in norm), None)
                if hit:
                    claims.append({"surface_kind": kind, "subject": {"text": hit, "span": _span(text, base, hit)},
                                   "relation": None, "object": None, "polarity": "UNKNOWN",
                                   "conditions": [], "condition_status": "NOT_EXTRACTED",
                                   "evidence_span": {"start": base, "end": base + len(text)},
                                   "extraction_status": "ABSTAIN"})
    return {"schema_version": VERSION, "mode": "RESEARCH_ONLY", "claims": claims,
            "score_admission": "DISABLED", "score_effect": "none"}


def compare_claim_to_registry(claim: dict[str, Any], registry_fact: dict[str, Any]) -> dict[str, Any]:
    """No reviewed crosswalk exists yet, so semantic identity cannot be asserted."""
    valid = (isinstance(claim, dict) and claim.get("extraction_status") == "SURFACE_CLAIM_REVIEW_ONLY"
             and isinstance(registry_fact, dict) and registry_fact.get("review_status") == "approved"
             and registry_fact.get("verification_status") == "verified"
             and isinstance(registry_fact.get("relation"), dict))
    return {"status": "NOT_ESTABLISHED" if valid else "ABSTAIN", "source_match_proven": False,
            "score_admission": "DISABLED", "score_effect": "none"}


def evaluate_answer_shadow(answer_text: str, registry_facts: list[dict[str, Any]]) -> dict[str, Any]:
    extracted = extract_answer_claims(answer_text)
    # Deliberately do not select Registry rows by an answer-side hint. A caller
    # must supply independently scoped comparisons in a later reviewed stage.
    return {**extracted, "comparisons": [], "accuracy": None,
            "accuracy_status": "NOT_ESTABLISHED", "score_admission": "DISABLED", "score_effect": "none"}
