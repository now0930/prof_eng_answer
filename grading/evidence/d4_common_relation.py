"""Research-only comparison of proposed normalized relation components.
Literal evidence and Registry provenance do not prove semantic extraction.
No scoring integration; unsupported projections and contexts fail closed.
"""
from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

REGISTRY_SHA = '1dbd94acea5f8677b3afdce3cabb0d1ed8cf3240e2722a68291812597341961e'
REGISTRY_PATH = Path(__file__).resolve().parents[2] / 'grading/evidence/approved_fact_registry.json'
DAMP = 'second_order_lag_response_by_damping_ratio'
VALVE = 'control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe'
TC = 'thermocouple_temperature_sensor_seebeck_reference_junction_compensation'

# Narrow reviewed-for-research projections of individual relation components.
# These are not equivalent to the complete Registry statements or score rules.
def _profile(topic, subject, predicate, obj, conditions, scope, context, kind, value, opposite=None, *, axis=None, unit=None, aliases=(), labels=()):
    return dict(topic=topic, relation=dict(subject=subject, predicate=predicate, object=obj,
                conditions=conditions), scope=scope, context=context, kind=kind, value=value, opposite=opposite,
                axis=axis or subject, unit=unit, aliases=aliases, labels=labels)


PROFILES = {
    'second_order_underdamped_response': _profile(DAMP, 'underdamped_second_order_step_response', 'exhibits', 'decaying_oscillation_and_overshoot', ['zeta_between_zero_and_one', 'standard_zero_free_step_response'], 'STANDARD_SECOND_ORDER_CLASSIFICATION', ['standard_second_order_model'], 'interval', ['0', False, '1', False], axis='damping_ratio', unit='1', aliases=('ζ', r'\zeta'), labels=('부족감쇠 (under-damped)', 'under damp')),
    'second_order_critical_damping_response': _profile(DAMP, 'critically_damped_second_order_system', 'has', 'repeated_real_pole_and_monotone_step_response', ['zeta_equals_one', 'standard_zero_free_step_response'], 'STANDARD_SECOND_ORDER_CLASSIFICATION', ['standard_second_order_model'], 'interval', ['1', True, '1', True], axis='damping_ratio', unit='1', aliases=('ζ', r'\zeta'), labels=('임계감쇠 (critically-damped)', 'critical damp')),
    'second_order_overdamped_response': _profile(DAMP, 'overdamped_second_order_system', 'has', 'two_real_poles_and_nonovershooting_step_response', ['zeta_greater_than_one', 'standard_zero_free_step_response'], 'STANDARD_SECOND_ORDER_CLASSIFICATION', ['standard_second_order_model'], 'interval', ['1', False, None, False], axis='damping_ratio', unit='1', aliases=('ζ', r'\zeta'), labels=('과감쇠 (over-damped)', 'over damp')),
    'friction_force_opposes_relative_or_impending_motion': _profile(VALVE, 'contact_friction_force', 'opposes', 'relative_or_impending_sliding_motion', ['classical_dry_friction_model_applies', 'contact_and_relative_motion_are_defined'], 'DRY_CONTACT_FRICTION_DIRECTION', ['classical_dry_friction_model_applies', 'contact_and_relative_motion_are_defined'], 'direction', 'OPPOSES_RELATIVE_MOTION', 'ALWAYS_OPPOSES_ACTUATOR_FORCE'),
    'thermocouple_law_of_intermediate_metals': _profile(TC, 'third_metal_inserted_into_thermocouple_circuit', 'preserves_net_emf_if', 'both_new_junctions_are_isothermal', ['homogeneous_materials', 'isothermal_added_junctions'], 'THERMOCOUPLE_INSERTION_EFFECT', ['homogeneous_materials', 'isothermal_added_junctions'], 'direction', 'NET_EMF_PRESERVED', 'NET_EMF_CHANGED'),
}


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _unique(items):
    out = {}
    for k, v in items:
        if k in out:
            raise ValueError('duplicate JSON key')
        out[k] = v
    return out


def registry_profiles(path=REGISTRY_PATH):
    """Read the actual pinned Registry; never accept model-provided Fact rows."""
    raw = Path(path).read_bytes()
    if _hash(raw) != REGISTRY_SHA:
        raise ValueError('registry hash mismatch')
    rows = json.loads(raw, object_pairs_hook=_unique)['facts']
    return {fid for fid, p in PROFILES.items() if _row_matches(rows, fid, p)}


def _row_matches(rows, fid, p):
    found = [r for r in rows if isinstance(r, dict) and r.get('fact_id') == fid]
    return len(found) == 1 and all((found[0].get('topic_id') == p['topic'],
        found[0].get('relation') == p['relation'], found[0].get('verification_status') == 'verified',
        found[0].get('review_status') == 'approved', bool(found[0].get('verification_refs'))))


def _span(answer, s):
    return (isinstance(s, dict) and set(s) == {'start', 'end', 'text'} and
            type(s['start']) is int and type(s['end']) is int and isinstance(s['text'], str) and
            0 <= s['start'] < s['end'] <= len(answer) and bool(s['text'].strip()) and
            answer[s['start']:s['end']] == s['text'])


def _evidence(answer, spans):
    return isinstance(spans, list) and 0 < len(spans) <= 8 and all(_span(answer, s) for s in spans)


def _interval(v):
    if not isinstance(v, list) or len(v) != 4 or type(v[1]) is not bool or type(v[3]) is not bool:
        raise ValueError('invalid interval')
    lo, lc, hi, hc = v
    if any(x is not None and (not isinstance(x, str) or len(x) > 32) for x in (lo, hi)):
        raise ValueError('invalid bound')
    lo, hi = (Decimal(x) if x is not None else None for x in (lo, hi))
    if any(x is not None and (not x.is_finite() or abs(x.adjusted()) > 12) for x in (lo, hi)):
        raise ValueError('nonfinite or excessive bound')
    if (lo is None and lc) or (hi is None and hc) or (lo is not None and hi is not None and (lo > hi or (lo == hi and not (lc and hc)))):
        raise ValueError('empty or invalid interval')
    return lo, lc, hi, hc



def _parse_range(expr, aliases):
    """Small generic inequality grammar, not natural-language extraction."""
    tokens = [s.strip() for s in re.split(r'(<=|>=|≤|≥|<|>|=)', expr.strip())]
    if len(tokens) not in (3, 5) or sum(t in aliases for t in tokens) != 1:
        raise ValueError('unsupported range expression')
    limits = [None, False, None, False]
    for left, op, right in zip(tokens[::2], tokens[1::2], tokens[2::2]):
        if left in aliases and right not in aliases:
            num, forward = right, op
        elif right in aliases and left not in aliases:
            num, forward = left, {'<':'>','>':'<','<=':'>=','>=':'<=','≤':'≥','≥':'≤','=':'='}[op]
        else:
            raise ValueError('unbound variable')
        if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)', num, flags=re.ASCII):
            raise ValueError('not an exact decimal literal')
        if forward == '=':
            if len(tokens) != 3:
                raise ValueError('mixed equality')
            limits = [num, True, num, True]
        elif forward in ('>', '>=', '≥'):
            if limits[0] is not None:
                raise ValueError('duplicate lower bound')
            limits[:2] = [num, forward != '>']
        else:
            if limits[2] is not None:
                raise ValueError('duplicate upper bound')
            limits[2:] = [num, forward != '<']
    return _interval(limits)


def _table_range(primary, evidence, profile):
    """Bind a selected label to its literal cell in a two-row pipe table.

    Missing/ambiguous or OCR-damaged layout is outside this projection.
    """
    rows = [[v.strip() for v in ln.strip()[1:-1].split('|')]
            for ln in primary.splitlines() if ln.strip().startswith('|') and ln.strip().endswith('|')]
    if len(evidence) != 1 or len(rows) not in (2, 3):
        raise ValueError('unsupported table')
    if len(rows) == 3:
        if not all(re.fullmatch(r':?-{3,}:?', v) for v in rows[1]):
            raise ValueError('unrecognized separator')
        rows.pop(1)
    header, data = rows
    idx = [i for i, label in enumerate(header) if label.casefold() in profile['labels']]
    if len(header) != len(data) or len(idx) != 1 or data[idx[0]] != evidence[0]['text'].strip():
        raise ValueError('table column binding mismatch')
    # The selected numeric cell must not occur in another column.
    if data.count(data[idx[0]]) != 1:
        raise ValueError('ambiguous numeric cell')
    return _parse_range(data[idx[0]], profile['aliases'])


def _result(reason, candidate='UNRESOLVED', **kw):
    return dict(reason=reason, component_candidate=candidate, registry_bound_candidate='UNRESOLVED',
                status='UNRESOLVED', source_binding='NOT_CHECKED', source_match_proven=False,
                semantic_validation='NOT_ESTABLISHED', score_admission='DISABLED', score_effect='none', **kw)


def compare_component(answer, claim, fact_id):
    """Compare model-proposed labels, never infer meaning from literal spans.

    Claim fields: hash, primary span, stance, scope, context with per-slot
    evidence, normalized relation with evidence. Exact source coordinates are
    checked. Other propositions in the same answer are not adjudicated here.
    """
    p = PROFILES.get(fact_id) if isinstance(fact_id, str) else None
    if p is None:
        return _result('NO_RESEARCH_PROJECTION')
    if not isinstance(answer, str) or not answer.strip() or len(answer) > 50000:
        return _result('INVALID_ANSWER')
    try:
        digest = _hash(answer.encode())
    except UnicodeError:
        return _result('INVALID_ANSWER')
    keys = {'answer_sha256', 'span', 'stance', 'scope', 'context', 'relation'}
    if not isinstance(claim, dict) or set(claim) != keys or claim['answer_sha256'] != digest or not _span(answer, claim['span']):
        return _result('INVALID_CLAIM_OR_SOURCE')
    if claim['stance'] != 'ASSERTED':
        return _result('NON_ASSERTED_OR_AMBIGUOUS')
    scope = claim['scope']
    if not isinstance(scope, dict) or set(scope) != {'value', 'evidence'} or scope['value'] != p['scope'] or not _evidence(answer, scope['evidence']):
        return _result('SCOPE_UNRESOLVED')
    context = claim['context']
    if not isinstance(context, dict) or set(context) != set(p['context']):
        return _result('CONTEXT_SCHEMA_MISMATCH')
    for c in context.values():
        if not isinstance(c, dict) or set(c) != {'value', 'evidence'} or c['value'] != 'SATISFIED' or not _evidence(answer, c['evidence']):
            return _result('CONTEXT_UNRESOLVED')
    rel = claim['relation']
    if not isinstance(rel, dict) or set(rel) != {'kind', 'value', 'mode', 'axis', 'unit', 'evidence'} or rel['kind'] != p['kind'] or rel['axis'] != p['axis'] or rel['unit'] != p['unit'] or not _evidence(answer, rel['evidence']):
        return _result('RELATION_UNRESOLVED')
    # Relation evidence must be inside the primary proposition; context may be elsewhere.
    if any(s['start'] < claim['span']['start'] or s['end'] > claim['span']['end'] for s in rel['evidence']):
        return _result('RELATION_OUTSIDE_PRIMARY_SPAN')
    if rel['kind'] == 'interval':
        if rel['mode'] != 'EXACT_CLASSIFICATION':
            return _result('CLASSIFICATION_NOT_EXACT')
        try:
            proposed = _interval(rel['value'])
            literal = _table_range(claim['span']['text'], rel['evidence'], p)
            if proposed != literal:
                return _result('NUMERIC_PROPOSAL_LITERAL_MISMATCH')
            equal = literal == _interval(p['value'])
        except (ValueError, InvalidOperation, OverflowError):
            return _result('INVALID_INTERVAL')
    else:
        if rel['mode'] != 'GENERAL_RULE' or not isinstance(rel['value'], str) or rel['value'] not in (p['value'], p['opposite']):
            return _result('DIRECTION_UNRESOLVED')
        equal = rel['value'] == p['value']
    return _result('PROPOSED_COMPONENT_COMPARISON', 'SUPPORT_CANDIDATE' if equal else 'CONTRADICT_CANDIDATE', projection_scope=p['scope'])


def evaluate_component(answer, claim, fact_id, *, registry_path=REGISTRY_PATH):
    result = compare_component(answer, claim, fact_id)
    try:
        available = registry_profiles(registry_path)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RecursionError):
        return {**result, 'source_binding': 'UNAVAILABLE_OR_MISMATCH'}
    if not isinstance(fact_id, str) or fact_id not in available:
        return {**result, 'source_binding': 'NO_MATCHING_PROJECTION'}
    return {**result, 'source_binding': 'PINNED_FULL_REGISTRY', 'registry_bound_candidate': result['component_candidate']}
