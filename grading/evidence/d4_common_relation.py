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


def _source_relation_profile(topic, fid, subject, predicate, obj, conditions):
    """Proposal tokens cover only the exact listed Registry relation.

    They do not prove that the answer asserts it, that a negation has the
    intended scope, or that its cited conditions hold.
    """
    return _profile(topic, subject, predicate, obj, conditions,
                    'SOURCE_RELATION:' + fid, conditions, 'direction',
                    'AFFIRMS_LISTED_RELATION', 'DENIES_LISTED_RELATION')


# Explicit source-relation projections. These are NOT synonyms, full Fact
# endorsements, or scoring admission. Conditions reproduce pinned rows.
_SOURCE_RELATIONS = {
    'v_model_design_test_mapping': ('instrumentation_control_software_lifecycle_v_model_traceability_verification_validation', 'v_model', 'maps', 'design_and_test_stages', []),
    'sil_sis_sif_scope': ('sil_target_determination_risk_reduction_and_lifecycle', 'sil_requirement', 'is_assigned_to', 'specific_safety_instrumented_function', ['scenario_and_function_defined']),
    'final_element_safe_action_process_dependent': ('final_control_element_sil_sis_esd_valve_partial_stroke_test', 'protective_system_safe_action', 'depends_on', 'process_hazard_and_safety_requirement', ['safe_action_is_defined_for_the_specific_process', 'valve_mechanical_fail_action_is_not_assumed_to_equal_process_safe_state']),
    'thermocouple_measures_temperature_difference': (TC, 'thermocouple_emf', 'depends_on', 'measuring_and_reference_junction_temperatures', ['thermocouple_material_pair_known']),
    'thermocouple_reference_junction_compensation': (TC, 'cold_junction_compensation', 'corrects', 'reference_junction_temperature_contribution', ['cjc_sensor_tracks_actual_terminal_junction_temperature', 'thermocouple_type_known']),
    'rtd_three_wire_bridge_compensation_assumptions': ('rtd_temperature_sensor_principle_pt100_wiring_compensation', 'three_wire_rtd_compensation', 'cancels_lead_error_to_first_order_if', 'compared_lead_resistances_match', ['specified_three_wire_circuit', 'symmetric_lead_wiring']),
    'rtd_four_wire_kelvin_measurement': ('rtd_temperature_sensor_principle_pt100_wiring_compensation', 'four_wire_kelvin_rtd_measurement', 'reduces', 'lead_resistance_voltage_error', ['separate_force_and_sense_paths', 'high_impedance_voltage_input']),
    'sw04_unit_test_verifies_isolated_software_units': ('instrumentation_control_software_lifecycle_v_model_traceability_verification_validation', 'software_unit_test', 'verifies_software_unit_against_defined_requirements_and_interfaces', 'isolated_unit_behavior', ['unit_boundary_and_test_depth_follow_software_architecture_and_risk', 'normal_and_off_nominal_cases_are_selected_from_requirements']),
    'sw04_integration_test_verifies_software_interfaces': ('instrumentation_control_software_lifecycle_v_model_traceability_verification_validation', 'software_integration_test', 'verifies_interactions_and_interfaces_between_integrated_items', 'integrated_software_behavior', ['test_scope_follows_defined_architecture_and_interface_requirements', 'timing_and_error_cases_are_tested_when_required_by_specification']),
    'sw04_system_test_checks_system_requirements_in_intended_environment': ('instrumentation_control_software_lifecycle_v_model_traceability_verification_validation', 'software_system_test', 'checks_integrated_software_against_system_requirements_and_operational_conditions', 'system_level_test_evidence', ['operational_conditions_are_approximated_as_required_by_test_objectives', 'tested_modes_and_recovery_behaviors_are_selected_from_requirements']),
}
PROFILES.update({fid: _source_relation_profile(topic, fid, subject, predicate, obj, conditions)
                 for fid, (topic, subject, predicate, obj, conditions) in _SOURCE_RELATIONS.items()})


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


def evaluate_claim_batch(answer, proposals, *, registry_path=REGISTRY_PATH):
    """Compare caller-supplied claims and propose same-cause groups, without scoring.

    Each item has claim_id, claim, fact_ids, and optional cause_span. The cause
    span is only a model-proposed grouping hint, not proof of shared causality.
    A group requires identical scope, condition evidence and source span; each
    contradiction remains individually auditable. Unknowns never become errors.
    """
    base = {'status': 'RESEARCH_ONLY', 'score_admission': 'DISABLED',
            'score_effect': 'none', 'semantic_validation': 'NOT_ESTABLISHED',
            'source_match_proven': False, 'comparisons': [], 'proposed_error_groups': []}
    if not isinstance(answer, str) or not isinstance(proposals, list) or len(proposals) > 256:
        return {**base, 'status': 'REJECTED_INPUT', 'reason': 'INVALID_BATCH'}
    ids = []
    for item in proposals:
        if (not isinstance(item, dict) or set(item) != {'claim_id', 'claim', 'fact_ids', 'cause_span'}
                or not isinstance(item['claim_id'], str) or not item['claim_id'] or len(item['claim_id']) > 128
                or not isinstance(item['fact_ids'], list) or len(item['fact_ids']) > 64
                or not all(isinstance(fid, str) and fid for fid in item['fact_ids'])
                or len(item['fact_ids']) != len(set(item['fact_ids']))):
            return {**base, 'status': 'REJECTED_INPUT', 'reason': 'INVALID_ITEM'}
        ids.append(item['claim_id'])
    if len(ids) != len(set(ids)):
        return {**base, 'status': 'REJECTED_INPUT', 'reason': 'DUPLICATE_CLAIM_ID'}
    try:
        registry = registry_profiles(registry_path)
        registry_status = 'PINNED_FULL_REGISTRY'
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RecursionError):
        registry, registry_status = set(), 'UNAVAILABLE_OR_MISMATCH'
    rows, groups, seen = [], {}, set()
    for item in proposals:
        claim = item['claim']
        try:
            fingerprint = _hash(json.dumps(claim, sort_keys=True, ensure_ascii=False,
                                           separators=(',', ':'), allow_nan=False).encode())
        except (TypeError, ValueError, UnicodeError, RecursionError):
            return {**base, 'status': 'REJECTED_INPUT', 'reason': 'INVALID_CLAIM'}
        for fid in item['fact_ids']:
            key = (fingerprint, fid)
            if key in seen:
                rows.append({'claim_id': item['claim_id'], 'fact_id': fid,
                             'reason': 'DUPLICATE_PROPOSAL', 'component_candidate': 'UNRESOLVED',
                             'registry_bound_candidate': 'UNRESOLVED'})
                continue
            seen.add(key)
            result = compare_component(answer, claim, fid)
            bound = (result['component_candidate'] if fid in registry else 'UNRESOLVED')
            profile = PROFILES.get(fid)
            primary = claim.get('span') if isinstance(claim, dict) else None
            source_span = ({'start': primary['start'], 'end': primary['end']}
                           if _span(answer, primary) else None)
            stance = claim.get('stance') if isinstance(claim, dict) else None
            stance = stance if stance in ('ASSERTED', 'QUOTED', 'REJECTED', 'HYPOTHETICAL') else 'UNKNOWN'
            scope = claim.get('scope') if isinstance(claim, dict) else None
            context = claim.get('context') if isinstance(claim, dict) else None
            context_values = {}
            if profile and isinstance(context, dict):
                for name in profile['context']:
                    slot = context.get(name)
                    value = slot.get('value') if isinstance(slot, dict) else None
                    context_values[name] = value if value in ('SATISFIED', 'MISSING', 'UNKNOWN', 'CONFLICT') else 'UNKNOWN'
            rows.append({'claim_id': item['claim_id'], 'fact_id': fid, **result,
                         'source_span': source_span, 'assertion_context_proposed': stance,
                         'scope_proposed': profile['scope'] if profile and isinstance(scope, dict)
                                           and scope.get('value') == profile['scope'] else 'UNKNOWN',
                         'conditions_proposed': context_values,
                         'source_binding': registry_status if fid in registry else
                                           ('NO_MATCHING_PROJECTION' if registry_status == 'PINNED_FULL_REGISTRY' else registry_status),
                         'registry_bound_candidate': bound})
            cause = item['cause_span']
            if (bound != 'CONTRADICT_CANDIDATE' or not _span(answer, cause)
                    or not isinstance(claim, dict) or not _span(answer, claim.get('span'))
                    or cause['start'] < claim['span']['start'] or cause['end'] > claim['span']['end']):
                continue
            # Shared proposed location is insufficient for certainty; grouping
            # stays explicitly provisional even when the source text is exact.
            group_context = json.dumps({'scope': claim['scope'], 'context': claim['context']},
                                       sort_keys=True, ensure_ascii=False, separators=(',', ':'))
            group_key = (cause['start'], cause['end'], _hash(group_context.encode()))
            groups.setdefault(group_key, []).append({'claim_id': item['claim_id'], 'fact_id': fid})
    grouped = [{'cause_span': {'start': key[0], 'end': key[1]}, 'members': members,
                'status': 'PROPOSED_SAME_CAUSE', 'semantic_validation': 'NOT_ESTABLISHED',
                'score_effect': 'none'} for key, members in groups.items() if len(members) > 1]
    return {**base, 'registry_status': registry_status, 'comparisons': rows,
            'proposed_error_groups': grouped}


def audit_full_registry(path=REGISTRY_PATH):
    """Validate the complete pinned Registry structure, not technical truth."""
    output = {'status': 'REJECTED', 'score_admission': 'DISABLED', 'score_effect': 'none',
              'technical_verification': 'NOT_ESTABLISHED'}
    try:
        raw = Path(path).read_bytes()
        digest = _hash(raw)
        if digest != REGISTRY_SHA:
            return {**output, 'reason': 'REGISTRY_HASH_MISMATCH', 'sha256': digest}
        data = json.loads(raw, object_pairs_hook=_unique)
        rows = data['facts']
        if not isinstance(rows, list) or not rows:
            return {**output, 'reason': 'INVALID_FACTS'}
        ids = []
        for row in rows:
            if not isinstance(row, dict):
                return {**output, 'reason': 'INVALID_FACT'}
            fid, rel = row.get('fact_id'), row.get('relation')
            if (not isinstance(fid, str) or not fid.strip() or not isinstance(row.get('topic_id'), str)
                    or not row['topic_id'].strip() or row.get('schema_version') != 'fact-grounded-contract-v1'
                    or not isinstance(rel, dict) or any(not isinstance(rel.get(k), str) or not rel[k].strip()
                                                        for k in ('subject', 'predicate', 'object'))
                    or not isinstance(rel.get('conditions'), list)
                    or not all(isinstance(c, str) and c.strip() for c in rel['conditions'])
                    or row.get('verification_status') != 'verified' or row.get('review_status') != 'approved'
                    or not isinstance(row.get('verification_refs'), list) or not row['verification_refs']):
                return {**output, 'reason': 'INVALID_FACT_SCHEMA_OR_APPROVAL'}
            ids.append(fid)
        if len(ids) != len(set(ids)):
            return {**output, 'reason': 'DUPLICATE_FACT_ID'}
        matching = registry_profiles(path)
        unmatched = sorted(set(PROFILES) - matching)
        return {**output, 'status': 'REJECTED' if unmatched else 'PASS',
                'reason': 'PROFILE_RELATION_MISMATCH' if unmatched else 'REGISTRY_STRUCTURE_VALID',
                'sha256': digest, 'fact_count': len(rows),
                'verified_approved_count': len(rows), 'duplicate_fact_ids': 0,
                'profile_count': len(PROFILES), 'matching_profiles': len(matching),
                'unmatched_profiles': unmatched}
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RecursionError):
        return {**output, 'reason': 'REGISTRY_READ_OR_SCHEMA_ERROR'}
