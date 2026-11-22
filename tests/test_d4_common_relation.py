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
