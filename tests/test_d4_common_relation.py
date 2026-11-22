import copy
import hashlib
import pytest
from grading.evidence.d4_common_relation import PROFILES, REGISTRY_PATH, compare_component, evaluate_component, _interval, _row_matches

FID = 'second_order_critical_damping_response'
TEXT = '| 구분 | Critical damp |\n| ζ | ζ = 1 |'


def proposal(fid=FID, text=TEXT, value=None, mode=None):
    p = PROFILES[fid]
    span = {'start': 0, 'end': len(text), 'text': text}
    slot = lambda v: {'value': v, 'evidence': [span.copy()]}
    return {'answer_sha256': hashlib.sha256(text.encode()).hexdigest(), 'span': span,
            'stance': 'ASSERTED', 'scope': slot(p['scope']),
            'context': {c: slot('SATISFIED') for c in p['context']},
            'relation': {'kind': p['kind'], 'axis': p['axis'], 'unit': p['unit'], 'value': copy.deepcopy(p['value'] if value is None else value),
                         'mode': mode or ('EXACT_CLASSIFICATION' if p['kind']=='interval' else 'GENERAL_RULE'),
                         'evidence': [{'start': text.index('ζ = '), 'end': text.index(' |', text.index('ζ = ')), 'text': text[text.index('ζ = '):text.index(' |', text.index('ζ = '))]}] if p['kind']=='interval' else [span.copy()]}}


def safe(r):
    assert r['status']=='UNRESOLVED' and r['score_admission']=='DISABLED' and r['score_effect']=='none'
    assert r['source_match_proven'] is False


@pytest.mark.parametrize('literal,v,expected', [('1',['1.00',True,'1',True],'SUPPORT_CANDIDATE'),('0.7',['0.7',True,'0.7',True],'CONTRADICT_CANDIDATE'),('1',['0.7',True,'0.7',True],'UNRESOLVED')])
def test_range(literal, v, expected):
    text=TEXT.replace('ζ = 1','ζ = '+literal)
    r=compare_component(text,proposal(text=text,value=v),FID); assert r['component_candidate']==expected; safe(r)


@pytest.mark.parametrize('v', [['1',False,'1',True],['NaN',False,None,False],['2',True,'1',True],[None,True,'1',False],['1',1,'2',False],['1e99999',True,None,False]])
def test_invalid_interval(v):
    with pytest.raises(ValueError): _interval(v)


@pytest.mark.parametrize('mutation', ['hash','span','stance','scope','condition','no_condition','mode','relation_span','kind','unit','axis'])
def test_guards(mutation):
    c=proposal()
    if mutation=='hash': c['answer_sha256']='0'*64
    if mutation=='span': c['span']['text']='changed'
    if mutation=='stance': c['stance']='QUOTED'
    if mutation=='scope': c['scope']['value']='UNKNOWN'
    if mutation=='condition': c['context']['standard_second_order_model']['value']='UNKNOWN'
    if mutation=='no_condition': c['context'].clear()
    if mutation=='mode': c['relation']['mode']='SUFFICIENT_ONLY'
    if mutation=='relation_span': c['span']={'start':0,'end':2,'text':TEXT[:2]}
    if mutation=='kind': c['relation']['kind']='direction'
    if mutation=='unit': c['relation']['unit']='Hz'
    if mutation=='axis': c['relation']['axis']='other' 
    r=compare_component(TEXT,c,FID); assert r['component_candidate']=='UNRESOLVED'; safe(r)


@pytest.mark.parametrize('fid',[x for x in PROFILES if PROFILES[x]['kind']=='direction'])
def test_direction(fid):
    for value,expected in [(PROFILES[fid]['value'],'SUPPORT_CANDIDATE'),(PROFILES[fid]['opposite'],'CONTRADICT_CANDIDATE'),('OTHER','UNRESOLVED')]:
        r=compare_component(TEXT,proposal(fid,value=value),fid); assert r['component_candidate']==expected; safe(r)


def test_unavailable_registry_and_unknown_fact(tmp_path):
    r=evaluate_component(TEXT,proposal(),FID,registry_path=tmp_path/'missing'); assert r['registry_bound_candidate']=='UNRESOLVED'; safe(r)
    (tmp_path/'bad').write_text('{}'); r=evaluate_component(TEXT,proposal(),FID,registry_path=tmp_path/'bad'); assert r['source_binding']=='UNAVAILABLE_OR_MISMATCH'; safe(r)
    assert compare_component(TEXT,proposal(),'unprofiled')['reason']=='NO_RESEARCH_PROJECTION'


def test_registry_row_checks():
    p=PROFILES[FID]; row=dict(fact_id=FID,topic_id=p['topic'],relation=copy.deepcopy(p['relation']),verification_status='verified',review_status='approved',verification_refs=['fixture'])
    assert _row_matches([row],FID,p)
    assert not _row_matches([row,row],FID,p)
    row['relation']['conditions']=[]; assert not _row_matches([row],FID,p)


def test_full_registry_if_present():
    if not REGISTRY_PATH.is_file(): pytest.skip('actual full Registry not mounted')
    r=evaluate_component(TEXT,proposal(),FID); assert r['source_binding']=='PINNED_FULL_REGISTRY'; assert r['registry_bound_candidate']=='SUPPORT_CANDIDATE'; safe(r)


def test_table_wrong_column_holds():
    text = '| 구분 | Critical damp | Other |\n| ζ | ζ = 1 | ζ = 0.7 |'
    c=proposal(text=text,value=['0.7',True,'0.7',True]); offset=text.index('ζ = 0.7')
    c['relation']['evidence']=[{'start':offset,'end':offset+7,'text':'ζ = 0.7'}]
    assert compare_component(text,c,FID)['component_candidate']=='UNRESOLVED'


def test_generic_inequality_grammar():
    from grading.evidence.d4_common_relation import _parse_range
    assert _parse_range('0 < x ≤ 1',('x',)) == _interval(['0',False,'1',True])
    assert _parse_range('x > 1',('x',)) == _interval(['1',False,None,False])
    assert _parse_range('1 > x',('x',)) == _interval([None,False,'1',False])
    assert _parse_range('x = 1',('x',)) == _interval(['1',True,'1',True])
    with pytest.raises(ValueError): _parse_range('x < 1 < 2',('x',))


def test_batch_multiple_fact_conflicts_share_provisional_cause_only():
    from grading.evidence.d4_common_relation import evaluate_claim_batch
    text = '| 구분 | Under damp | Critical damp | Over damp |\n| ζ | ζ = 1 | ζ = 0.7 | ζ = 0.8 |'
    span = {'start': 0, 'end': len(text), 'text': text}
    ids = ['second_order_underdamped_response', 'second_order_critical_damping_response',
           'second_order_overdamped_response']
    values = ['1', '0.7', '0.8']
    items = []
    for i, (fid, val) in enumerate(zip(ids, values)):
        c = proposal(fid, text=text, value=[val, True, val, True])
        start = text.index('ζ = ' + val)
        c['relation']['evidence'] = [{'start': start, 'end': start + len('ζ = ' + val), 'text': 'ζ = ' + val}]
        items.append({'claim_id': str(i), 'claim': c, 'fact_ids': [fid], 'cause_span': span})
    result = evaluate_claim_batch(text, items)
    assert result['score_effect'] == 'none' and result['score_admission'] == 'DISABLED'
    assert [x['registry_bound_candidate'] for x in result['comparisons']] == ['CONTRADICT_CANDIDATE'] * 3
    assert all(x['source_span'] == {'start': 0, 'end': len(text)} for x in result['comparisons'])
    assert all(x['assertion_context_proposed'] == 'ASSERTED' for x in result['comparisons'])
    assert all(x['conditions_proposed']['standard_second_order_model'] == 'SATISFIED' for x in result['comparisons'])
    assert len(result['proposed_error_groups']) == 1
    assert len(result['proposed_error_groups'][0]['members']) == 3
    assert result['proposed_error_groups'][0]['semantic_validation'] == 'NOT_ESTABLISHED'
    # A duplicate never adds a second comparison candidate.
    duplicate = {**items[0], 'claim_id': 'duplicate'}
    result = evaluate_claim_batch(text, items + [duplicate])
    assert result['comparisons'][-1]['reason'] == 'DUPLICATE_PROPOSAL'
    assert len(result['proposed_error_groups'][0]['members']) == 3
    # Different condition evidence cannot merge, even if the same cause was proposed.
    changed = copy.deepcopy(items[2])
    changed['claim']['context']['standard_second_order_model']['evidence'] = [
        {'start': 0, 'end': 1, 'text': text[:1]}]
    result = evaluate_claim_batch(text, items[:2] + [changed])
    assert len(result['proposed_error_groups'][0]['members']) == 2


def test_batch_rejects_duplicates_quotes_and_unverified_causes(tmp_path):
    from grading.evidence.d4_common_relation import evaluate_claim_batch
    c = proposal()
    item = {'claim_id': 'a', 'claim': c, 'fact_ids': [FID], 'cause_span': c['span']}
    assert evaluate_claim_batch(TEXT, [item, item])['reason'] == 'DUPLICATE_CLAIM_ID'
    quoted = copy.deepcopy(item); quoted['claim']['stance'] = 'QUOTED'
    r = evaluate_claim_batch(TEXT, [quoted]); assert r['comparisons'][0]['component_candidate'] == 'UNRESOLVED'
    assert r['proposed_error_groups'] == []
    r = evaluate_claim_batch(TEXT, [item], registry_path=tmp_path/'missing')
    assert r['comparisons'][0]['registry_bound_candidate'] == 'UNRESOLVED'
    assert r['proposed_error_groups'] == []
    assert evaluate_claim_batch(TEXT, [{**item, 'fact_ids': [FID, FID]}])['status'] == 'REJECTED_INPUT'


def test_entire_real_registry_audit_and_hash_fail_closed(tmp_path):
    from grading.evidence.d4_common_relation import audit_full_registry
    real = audit_full_registry()
    assert real['status'] == 'PASS'
    assert real['fact_count'] == real['verified_approved_count']
    assert real['fact_count'] > real['profile_count']
    assert real['matching_profiles'] == len(PROFILES) and not real['unmatched_profiles']
    assert real['technical_verification'] == 'NOT_ESTABLISHED'
    altered = tmp_path / 'registry.json'; altered.write_text('{}')
    assert audit_full_registry(altered)['reason'] == 'REGISTRY_HASH_MISMATCH'
    assert audit_full_registry(tmp_path/'absent')['status'] == 'REJECTED'


def test_batch_cli_preserves_source_privacy_and_refuses_overwrite(tmp_path):
    import json
    import os
    import subprocess
    import sys
    from pathlib import Path
    script = Path(__file__).resolve().parents[1] / 'scripts/replay_d4_claim_batch.py'
    c = proposal()
    source = tmp_path / 'input.json'; target = tmp_path / 'output.json'
    source.write_text(json.dumps({'answer': TEXT, 'proposals': [
        {'claim_id': 'a', 'claim': c, 'fact_ids': [FID], 'cause_span': c['span']}]}, ensure_ascii=False))
    cmd = [sys.executable, str(script), '--input', str(source), '--output', str(target)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    data = target.read_text()
    assert TEXT not in data and 'score_effect' in data
    assert os.stat(target).st_mode & 0o777 == 0o600
    assert subprocess.run(cmd, capture_output=True).returncode != 0
    assert target.read_text() == data


def test_single_claim_can_target_multiple_facts_without_inventing_matches():
    from grading.evidence.d4_common_relation import evaluate_claim_batch
    c = proposal()
    other = 'second_order_overdamped_response'
    item = {'claim_id': 'one', 'claim': c, 'fact_ids': [FID, other], 'cause_span': None}
    result = evaluate_claim_batch(TEXT, [item])
    assert len(result['comparisons']) == 2
    assert result['comparisons'][0]['registry_bound_candidate'] == 'SUPPORT_CANDIDATE'
    assert result['comparisons'][1]['registry_bound_candidate'] == 'UNRESOLVED'
    assert result['proposed_error_groups'] == []


@pytest.mark.parametrize('fid', [
    'v_model_design_test_mapping', 'sil_sis_sif_scope',
    'final_element_safe_action_process_dependent',
    'thermocouple_measures_temperature_difference',
    'thermocouple_reference_junction_compensation',
    'rtd_three_wire_bridge_compensation_assumptions',
    'rtd_four_wire_kelvin_measurement',
    'sw04_unit_test_verifies_isolated_software_units',
    'sw04_integration_test_verifies_software_interfaces',
    'sw04_system_test_checks_system_requirements_in_intended_environment',
])
def test_source_relation_profiles_are_exact_and_remain_unverified_candidates(fid):
    profile = PROFILES[fid]
    c = proposal(fid)
    assert evaluate_component(TEXT, c, fid)['registry_bound_candidate'] == 'SUPPORT_CANDIDATE'
    assert evaluate_component(TEXT, c, fid)['status'] == 'UNRESOLVED'
    assert evaluate_component(TEXT, c, fid)['source_match_proven'] is False
    c['relation']['value'] = 'DENIES_LISTED_RELATION'
    assert evaluate_component(TEXT, c, fid)['registry_bound_candidate'] == 'CONTRADICT_CANDIDATE'
    c['stance'] = 'QUOTED'
    assert evaluate_component(TEXT, c, fid)['registry_bound_candidate'] == 'UNRESOLVED'
    if profile['context']:
        c = proposal(fid)
        c['context'].pop(profile['context'][0])
        assert evaluate_component(TEXT, c, fid)['registry_bound_candidate'] == 'UNRESOLVED'
    else:
        assert fid == 'v_model_design_test_mapping' and profile['relation']['conditions'] == []


def test_existing_replay_requires_proposals_unless_explicit_inventory_mode(tmp_path):
    import json
    import subprocess
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    answers = tmp_path / 'answers.json'; review = tmp_path / 'review.json'; proposals = tmp_path / 'proposals.json'
    target = tmp_path / 'results.json'
    answers.write_text(json.dumps({'cases': [{'case_id': 'c1', 'answer': TEXT}]}, ensure_ascii=False))
    answer_hash = hashlib.sha256(answers.read_bytes()).hexdigest()
    review.write_text(json.dumps({'input_sha256': answer_hash, 'rows': [{'case_id':'c1', 'claim_id':'r1',
        'fact_id': FID, 'input_sha256': hashlib.sha256(TEXT.encode()).hexdigest(),
        'start': 0, 'end': len(TEXT), 'evidence': TEXT, 'manual_candidate':'UNRESOLVED'}]}, ensure_ascii=False))
    proposals.write_text(json.dumps({'input_sha256': answer_hash,
        'review_sha256': hashlib.sha256(review.read_bytes()).hexdigest(), 'proposals': []}))
    command = [sys.executable, str(root / 'scripts/replay_d4_common_relation.py'), '--answers', str(answers),
               '--review', str(review), '--proposals', str(proposals), '--output', str(target)]
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert not target.exists()
    result = subprocess.run(command + ['--allow-missing-proposals'], capture_output=True)
    assert result.returncode == 0
    payload = json.loads(target.read_text())
    assert payload['rows'][0]['proposal_availability'] == 'MISSING'
    assert payload['rows'][0]['component_candidate'] == 'UNRESOLVED'
    assert payload['rows'][0]['registry_bound_candidate'] == 'UNRESOLVED'
    assert target.stat().st_mode & 0o777 == 0o600
