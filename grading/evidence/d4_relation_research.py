"""D4 research projections; never used for grading or Fact admission."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from grading.evidence.d4_wrong_shadow_probe import _RULES, _SENTENCE, _norm

REGISTRY = Path(__file__).resolve().parents[2] / 'grading/evidence/approved_fact_registry.json'
SCHEMA = 'd4_relation_research.v1'


def _digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def project_fact(fact_id: str, topic_id: str) -> dict[str, Any]:
    """Project an exact approved Registry relation without approving a crosswalk."""
    rows = json.loads(REGISTRY.read_text(encoding='utf-8'))['facts']
    matches = [r for r in rows if isinstance(r, dict) and r.get('fact_id') == fact_id]
    allowed = {r['fact'] for r in _RULES.values()}
    if len(matches) != 1:
        return {'status': 'UNRESOLVED', 'score_effect': 'none'}
    f = matches[0]
    if (f.get('topic_id') != topic_id or f.get('legacy_anchor_id') not in allowed
            or f.get('verification_status') != 'verified' or f.get('review_status') != 'approved'
            or not isinstance(f.get('relation'), dict) or not f.get('verification_refs')):
        return {'status': 'UNRESOLVED', 'score_effect': 'none'}
    rel = f['relation']
    return {'schema_version': SCHEMA, 'status': 'PROPOSAL', 'fact_id': fact_id,
            'topic_id': topic_id, 'registry_sha256': hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
            'registry_fact_sha256': _digest(f), 'source_statement': f['statement'],
            'subject': rel.get('subject'), 'predicate': rel.get('predicate'), 'object': rel.get('object'),
            'conditions': rel.get('conditions', []), 'polarity': 'NOT_EXPLICIT_IN_REGISTRY',
            'quantities': 'NOT_STRUCTURED', 'units': 'NOT_STRUCTURED', 'scope': 'SEE_SOURCE_STATEMENT',
            'exceptions': 'SEE_SOURCE_STATEMENT', 'source_provenance': f['verification_refs'],
            'verification_status': f['verification_status'], 'review_status': f['review_status'],
            'semantic_equivalence_status': 'NOT_ESTABLISHED', 'score_admission': 'DISABLED', 'score_effect': 'none'}


def diagnose_surface(answer: str, family: str) -> dict[str, Any]:
    """Explain bounded surface availability without asserting a semantic Claim."""
    rule = _RULES.get(family)
    if not isinstance(answer, str) or rule is None:
        return {'status': 'UNRESOLVED', 'reason': 'INVALID_INPUT', 'score_effect': 'none'}
    observations = []
    for m in _SENTENCE.finditer(answer):
        sentence = _norm(m.group())
        observations.append({'left': bool(rule['left'].search(sentence)),
                             'right': bool(rule['right'].search(sentence)),
                             'relation_cue': bool(rule['support'].search(sentence) or rule['contradict'].search(sentence) or (rule.get('extra_contradict') and rule['extra_contradict'].search(sentence)))})
    both = any(x['left'] and x['right'] for x in observations)
    return {'status': 'SURFACE_AVAILABLE' if both else 'NO_CANDIDATE',
            'reason': 'BOTH_CUES_IN_SENTENCE' if both else 'MISSING_SAME_SENTENCE_CONCEPT_CUES',
            'observations': observations, 'subject': 'NOT_EXTRACTED', 'predicate': 'NOT_EXTRACTED',
            'object': 'NOT_EXTRACTED', 'polarity': 'UNKNOWN', 'conditions': 'NOT_EXTRACTED',
            'quantities': 'NOT_EXTRACTED', 'units': 'NOT_EXTRACTED', 'context': 'NOT_ESTABLISHED',
            'score_admission': 'DISABLED', 'score_effect': 'none'}


def evaluate_claim(claim: Any, topic_id: str, fact_id: str, proposal: Any) -> dict[str, Any]:
    """Compare only a fresh source-bound proposal; withhold all semantic approval."""
    current = project_fact(fact_id, topic_id)
    base = {'status': 'UNRESOLVED', 'source_match_proven': False,
            'accuracy_status': 'NOT_ESTABLISHED', 'score_admission': 'DISABLED', 'score_effect': 'none'}
    if current.get('status') != 'PROPOSAL' or proposal != current or not isinstance(claim, dict):
        return {**base, 'reason': 'INVALID_SCOPE_OR_PROPOSAL'}
    # A caller-supplied label alone cannot prove quotation, relation, polarity,
    # conditions, or semantic identity. No SUPPORT is granted by this prototype.
    return {**base, 'reason': 'CLAIM_AND_CONDITION_SEMANTICS_NOT_ESTABLISHED'}
