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

# This deliberately narrow grammar accepts only a complete, directly stated
# conditional proposition. It is an experimental crosswalk, not an alias or
# a general Korean parser. A surrounding explanation, quotation, correction,
# negation of the whole proposition, or non-isothermal case fails closed.
_THERMO_FACT = 'thermocouple_law_of_intermediate_metals'
_THERMO_TOPIC = 'thermocouple_temperature_sensor_seebeck_reference_junction_compensation'
import re

_THERMO = re.compile(
    r'(?P<subject>열전대 회로에 제3 금속을 삽입할 때)\s*'
    r'(?:(?P<homogeneous>재료가 균질하고)\s*)?'
    r'(?P<isothermal>두 신규 접점이 같은 온도이면|두 신규 접점의 온도가 서로 다르면)\s*'
    r'(?P<object>순 열기전력)은\s*'
    r'(?P<predicate>변하지 않는다|변한다)[.]?'
)


def extract_thermocouple_claims(answer_text: str) -> dict[str, Any]:
    """Extract bounded propositions from answer text only, without Fact input."""
    base = {'schema_version': 'd4_thermocouple_claim.v1', 'claims': [],
            'score_admission': 'DISABLED', 'score_effect': 'none',
            'accuracy_status': 'NOT_ESTABLISHED'}
    if not isinstance(answer_text, str):
        return {**base, 'extraction_status': 'UNRESOLVED'}
    sentences = list(_SENTENCE.finditer(answer_text))
    # A later sentence can quote, retract, or contradict an earlier one.
    # Do not infer author intent across sentences in this prototype.
    if len(sentences) != 1:
        return {**base, 'extraction_status': 'UNRESOLVED'}
    claims = []
    for sentence in sentences:
        text = sentence.group()
        # Whitespace is removed only around the sentence, preserving offsets.
        trimmed = text.strip()
        match = _THERMO.fullmatch(trimmed)
        if not match:
            continue
        offset = sentence.start() + len(text) - len(text.lstrip())
        span = lambda name: {'start': offset + match.start(name), 'end': offset + match.end(name)}
        claims.append({'subject': match.group('subject'), 'predicate': '변하다',
                       'object': match.group('object'),
                       'polarity': 'NEGATIVE' if match.group('predicate') == '변하지 않는다' else 'POSITIVE',
                       'negation_scope': 'PREDICATE' if match.group('predicate') == '변하지 않는다' else 'NONE',
                       'conditions': {'homogeneous_materials': bool(match.group('homogeneous')),
                                      'isothermal_added_junctions': match.group('isothermal') == '두 신규 접점이 같은 온도이면'},
                       'quantities': [], 'units': [], 'assertion_context': 'ASSERTED',
                       'source_span': {'start': offset, 'end': offset + len(trimmed)},
                       'component_spans': {name: span(name) for name in ('subject', 'object', 'predicate', 'isothermal')},
                       'extraction_status': 'EXTRACTED'})
    return {**base, 'claims': claims, 'extraction_status': 'EXTRACTED' if claims else 'UNRESOLVED'}


def evaluate_thermocouple_answer(answer_text: str, topic_id: str, fact_id: str) -> dict[str, Any]:
    """Compare answer-derived claims with an approved fact; never affects scoring."""
    extraction = extract_thermocouple_claims(answer_text)
    proposal = project_fact(fact_id, topic_id)
    base = {'schema_version': 'd4_thermocouple_evaluation.v1', 'extraction': extraction,
            'comparisons': [], 'score_admission': 'DISABLED', 'score_effect': 'none',
            'accuracy_status': 'NOT_ESTABLISHED'}
    if fact_id != _THERMO_FACT or topic_id != _THERMO_TOPIC or proposal.get('status') != 'PROPOSAL':
        return {**base, 'status': 'UNRESOLVED', 'reason': 'INVALID_SCOPE_OR_FACT'}
    comparisons = []
    for claim in extraction['claims']:
        conditions = claim['conditions']
        condition_status = ('CONFLICT' if not conditions['isothermal_added_junctions'] else
                            'SATISFIED' if conditions['homogeneous_materials'] else 'MISSING')
        status = 'UNRESOLVED'
        if condition_status == 'SATISFIED':
            status = 'SUPPORT_CANDIDATE' if claim['polarity'] == 'NEGATIVE' else 'CONTRADICT_CANDIDATE'
        comparisons.append({'status': status, 'condition_status': condition_status,
                            'condition_details': conditions, 'unit_status': 'NOT_APPLICABLE',
                            'source_span': claim['source_span'],
                            'fact_id': fact_id, 'registry_fact_sha256': proposal['registry_fact_sha256'],
                            'registry_sha256': proposal['registry_sha256'],
                            'source_match_proven': False, 'score_effect': 'none'})
    return {**base, 'status': 'CANDIDATES' if comparisons else 'UNRESOLVED',
            'comparisons': comparisons}
