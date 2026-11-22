"""Research-only validation of untrusted thermocouple Claim proposals.

Literal provenance and conservative vetoes are NOT semantic proof.
No operating grader or score admission integration.
"""
from __future__ import annotations

import hashlib
import re

SCHEMA = 'd4_structured_claim.v1'
FACT = 'thermocouple_law_of_intermediate_metals'
TOPIC = 'thermocouple_temperature_sensor_seebeck_reference_junction_compensation'
CONDITIONS = {'homogeneous_materials', 'isothermal_added_junctions'}
# D4-WRONG-07 recorded Registry SHA; any change requires research review.
EXPECTED_REGISTRY_SHA256 = '1dbd94acea5f8677b3afdce3cabb0d1ed8cf3240e2722a68291812597341961e'
FIELDS = {
    'stance': {'ASSERTED', 'QUOTED', 'REFUTED', 'ATTRIBUTED', 'META', 'UNKNOWN'},
    'scope': {'IN_SCOPE', 'AMBIGUOUS', 'OUT_OF_SCOPE'},
    'homogeneous': {'YES', 'NO', 'UNKNOWN'},
    'isothermal': {'YES', 'NO', 'UNKNOWN'},
    'outcome': {'PRESERVED', 'CHANGED', 'POSSIBLE', 'NONE', 'UNKNOWN'},
    'causal_binding': {'INSERTION_EFFECT', 'UNKNOWN'},
}
EMPTY_OK = {'UNKNOWN', 'AMBIGUOUS', 'NONE'}
_SENTENCE = re.compile(r'[^\n!?。]+?(?:\.(?![A-Za-z0-9])|[!?。]|\n|$)')
_CONTEXT_VETO = re.compile(r'["“”‘’「」『』?]|인용|반박|오답|틀렸|틀린|잘못|그러나|하지만|반면|여부|수\s*있다|가능|기준\s*접점|냉접점')
_SCOPE = re.compile(r'열전대|중간\s*금속\s*법칙')
_MATERIAL = re.compile(r'균질')
_JUNCTION = re.compile(r'(?:두|둘|양단|양끝|양\s*끝).{0,18}(?:접점|접합점|접속점|접속부|연결부|연결점)|(?:접점|접합점|접속점|접속부|연결부|연결점).{0,18}(?:두|둘|양단|양끝)')
_ISOTHERMAL = re.compile(r'등온|동일\s*(?:한\s*)?온도|같은\s*온도|온도가?\s*(?:동일|일치|같)|°C\s*로\s*같', re.I)
_CONDITION_VETO = re.compile(r'균질하지|균질한.{0,25}(?:아닌|아니라)|균질성.{0,12}(?:없|미확인|모르|불명확)|비균질|비등온|등온.{0,8}(?:아니|않)|온도.{0,10}(?:다르|다르다|서로\s*다)')
_PRESERVED = re.compile(r'불변|변화가\s*없|변(?:화|경)?하지\s*않|변경하지\s*않|유지된다|영향을\s*받지\s*않|영향을\s*주지\s*않|기전력이\s*같다')
_CHANGED = re.compile(r'증가한다|감소한다|바뀐다|변한다|변화한다|추가\s*전압이\s*더해진다|오차\s*기전력이\s*발생한다|달라진다')
_OUTCOME_VETO = re.compile(r'않는\s*(?:것은|것이)\s*아니|않지\s*않|유지되지|증가하지|감소하지|변하지\s*않는\s*것')
_EFFECT = re.compile(r'추가|삽입|연결|이어\s*붙|이을\s*때|편입|끼우|중간\s*금속\s*법칙|중간금속|신규\s*접합점')
_EMF = re.compile(r'기전력|열전기력|EMF', re.I)
# Research-only fail-closed guard: words literally present in a quote do not
# establish that the author endorses that proposition. Detect other opposing
# direction cues and rebuttal/attribution language beyond the claimed span.
_AUTHOR_STANCE_VETO = re.compile(
    r'(?:(?:주장|견해|설명|문장).{0,24}(?:반대|동의하지|부정|거부)|'
    r'(?:가|것이)\s*아니라|실제(?:로는|는)|오히려|'
    r'(?:하지만|그런데|그렇지만)|(?:며|지만)\s*실제|'
    r'라고\s*(?:가르치|우기|주장|말|설명))'
)



def _result(**fields):
    return {'schema_version': SCHEMA, 'structure_status': 'UNRESOLVED',
            'conditional_candidate': 'UNRESOLVED', 'status': 'UNRESOLVED',
            'source_binding': 'NOT_CHECKED', 'source_match_proven': False,
            'accuracy_status': 'NOT_ESTABLISHED', 'score_admission': 'DISABLED',
            'score_effect': 'none', **fields}


def _span(answer, item):
    if not isinstance(item, dict) or set(item) != {'start', 'end', 'text'}:
        return False
    s, e, t = item['start'], item['end'], item['text']
    return (type(s) is int and type(e) is int and isinstance(t, str) and
            0 <= s < e <= len(answer) and bool(t.strip()) and answer[s:e] == t)


def assess_proposal(answer, proposal):
    """Validate schema/spans and compute conditional comparison, not a verdict.

    Values are untrusted annotations. Even an exact span may be misleading.
    Only single, complete propositions are eligible for directional candidates.
    """
    if (not isinstance(answer, str) or not answer.strip() or len(answer) > 20000 or
            not isinstance(proposal, dict) or set(proposal) != {'schema', 'answer_sha256', 'claims'} or
            proposal['schema'] != SCHEMA):
        return _result(reason='INVALID_SCHEMA')
    try:
        answer_hash = hashlib.sha256(answer.encode()).hexdigest()
    except UnicodeEncodeError:
        return _result(reason='INVALID_UNICODE')
    if proposal['answer_sha256'] != answer_hash:
        return _result(reason='INPUT_HASH_MISMATCH')
    claims = proposal['claims']
    if not isinstance(claims, list) or len(claims) != 1:
        return _result(reason='SINGLE_CLAIM_REQUIRED')
    claim = claims[0]
    if (not isinstance(claim, dict) or set(claim) != {'span', 'fields'} or
            not _span(answer, claim['span']) or not isinstance(claim['fields'], dict) or
            set(claim['fields']) != set(FIELDS)):
        return _result(reason='INVALID_CLAIM')
    start, end = claim['span']['start'], claim['span']['end']
    vals, evidence = {}, {}
    for field, allowed in FIELDS.items():
        item = claim['fields'][field]
        if (not isinstance(item, dict) or set(item) != {'value', 'evidence'} or
                not isinstance(item['value'], str) or item['value'] not in allowed or
                not isinstance(item['evidence'], list) or len(item['evidence']) > 8):
            return _result(reason='INVALID_FIELD', field=field)
        spans = item['evidence']
        if (item['value'] not in EMPTY_OK and not spans) or any(
                not _span(answer, s) or s['start'] < start or s['end'] > end for s in spans):
            return _result(reason='INVALID_EVIDENCE', field=field)
        vals[field] = item['value']
        evidence[field] = ' '.join(s['text'] for s in spans)
    base = {'structure_status': 'LITERAL_SPANS_VERIFIED', 'proposed_fields': vals,
            'semantic_validation': 'NOT_ESTABLISHED', 'condition_comparison': 'UNRESOLVED'}
    if vals['stance'] in {'QUOTED', 'REFUTED'}:
        return _result(**base, conditional_candidate='NON_ASSERTED', reason='PROPOSED_NON_ASSERTED')
    if vals['scope'] == 'OUT_OF_SCOPE':
        return _result(**base, conditional_candidate='OUT_OF_SCOPE', reason='PROPOSED_OUT_OF_SCOPE')
    if (vals['stance'] != 'ASSERTED' or vals['scope'] != 'IN_SCOPE' or
            vals['causal_binding'] != 'INSERTION_EFFECT' or vals['outcome'] not in {'PRESERVED', 'CHANGED'}):
        return _result(**base, reason='SCOPE_STANCE_OR_CAUSAL_UNRESOLVED')
    base['condition_comparison'] = ('PROPOSED_CONFLICT' if 'NO' in (vals['homogeneous'], vals['isothermal']) else
                                    'PROPOSED_SATISFIED' if vals['homogeneous'] == vals['isothermal'] == 'YES' else 'PROPOSED_MISSING')
    if base['condition_comparison'] != 'PROPOSED_SATISFIED':
        return _result(**base, reason='CONDITIONS_UNRESOLVED')
    if (answer[:start].strip() or answer[end:].strip() or len(list(_SENTENCE.finditer(answer))) != 1 or
            _CONTEXT_VETO.search(answer) or _CONDITION_VETO.search(answer)):
        return _result(**base, reason='CONTEXT_OR_CONDITION_VETO')
    if (not _SCOPE.search(evidence['scope']) or not _MATERIAL.search(evidence['homogeneous']) or
            not _JUNCTION.search(evidence['isothermal']) or not _ISOTHERMAL.search(evidence['isothermal']) or
            not _EFFECT.search(evidence['causal_binding']) or not _EMF.search(answer)):
        return _result(**base, reason='REQUIRED_SURFACE_EVIDENCE_MISSING')
    if _AUTHOR_STANCE_VETO.search(answer) or (_PRESERVED.search(answer) and _CHANGED.search(answer)):
        return _result(**base, reason='MIXED_RELATION_OR_AUTHOR_STANCE_UNRESOLVED')
    outcome = evidence['outcome']
    preserved, changed = bool(_PRESERVED.search(outcome)), bool(_CHANGED.search(outcome))
    if (_OUTCOME_VETO.search(answer) or preserved == changed or
            preserved != (vals['outcome'] == 'PRESERVED')):
        return _result(**base, reason='DIRECTION_EVIDENCE_UNRESOLVED')
    return _result(**base, conditional_candidate=('SUPPORT_CANDIDATE' if preserved else 'CONTRADICT_CANDIDATE'),
                   reason='UNVERIFIED_PROPOSAL_COMPARISON')


def evaluate_against_registry(answer, proposal):
    """Bind the proposal comparison to the current repository's approved Fact.

    The model cannot supply the trusted registry projection. Fail closed if the
    repository or expected conditions are unavailable. No semantic admission.
    """
    result = assess_proposal(answer, proposal)
    try:
        from grading.evidence.d4_relation_research import project_fact
        fact = project_fact(FACT, TOPIC)
    except (ImportError, OSError, ValueError, KeyError, TypeError):
        return {**result, 'source_binding': 'UNAVAILABLE'}
    if (not isinstance(fact, dict) or fact.get('status') != 'PROPOSAL' or
            fact.get('fact_id') != FACT or fact.get('topic_id') != TOPIC or
            fact.get('verification_status') != 'verified' or fact.get('review_status') != 'approved' or
            not isinstance(fact.get('conditions'), list) or len(fact['conditions']) != len(CONDITIONS) or
            any(not isinstance(c, str) for c in fact['conditions']) or set(fact['conditions']) != CONDITIONS or
            not fact.get('source_provenance') or not fact.get('source_statement') or
            fact.get('registry_sha256') != EXPECTED_REGISTRY_SHA256 or
            any(not isinstance(fact.get(k), str) or not re.fullmatch(r'[0-9a-f]{64}', fact[k])
                for k in ('registry_sha256', 'registry_fact_sha256'))):
        return {**result, 'source_binding': 'SCOPE_OR_SOURCE_MISMATCH'}
    return {**result, 'source_binding': 'APPROVED_METADATA_BOUND',
            'registry_fact_sha256': fact['registry_fact_sha256'], 'registry_sha256': fact['registry_sha256'],
            'status': result['conditional_candidate']}
