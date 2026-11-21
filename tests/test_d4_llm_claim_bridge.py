import hashlib
import json
from pathlib import Path

import pytest

from grading.evidence.d4_llm_claim_bridge import (
    EXTRACT_SCHEMA, FACT_HASH, REGISTRY_PATH, build_prompt, normalize_extraction,
    evaluate_extraction, extract_and_evaluate, load_registry_binding, load_verified_export,
)

TEXT='열전대에 균질한 제3 금속을 삽입하고 두 신규 접점이 등온이면 순 기전력은 변하지 않는다.'


def raw(text=TEXT, changed=False):
    fields={'stance':('ASSERTED','순 기전력은'),'scope':('IN_SCOPE','열전대'),
            'homogeneous':('YES','균질한 제3 금속'),'isothermal':('YES','두 신규 접점이 등온'),
            'outcome':('CHANGED' if changed else 'PRESERVED','증가한다' if changed else '변하지 않는다'),
            'causal_binding':('INSERTION_EFFECT','제3 금속을 삽입')}
    return {'schema':EXTRACT_SCHEMA,'claims':[{'span_text':text,'fields':{
        k:{'value':v,'quotes':[q]} for k,(v,q) in fields.items()}}]}


def safety(r):
    assert r['status']=='UNRESOLVED'
    assert r['score_admission']=='DISABLED' and r['score_effect']=='none'
    assert r['source_match_proven'] is False and r['accuracy_status']=='NOT_ESTABLISHED'


def test_answer_only_prompt_and_exact_offsets():
    prompt=build_prompt(TEXT)
    assert FACT_HASH not in prompt and 'SUPPORT_CANDIDATE' not in prompt and 'CONTRADICT_CANDIDATE' not in prompt
    assert json.loads(prompt.split('ANSWER_JSON=',1)[1])==TEXT
    obj=normalize_extraction(TEXT,json.dumps(raw()))
    assert obj['answer_sha256']==hashlib.sha256(TEXT.encode()).hexdigest()
    for f in obj['claims'][0]['fields'].values():
        for e in f['evidence']: assert TEXT[e['start']:e['end']]==e['text']


@pytest.mark.parametrize('kind',['bad_quote','duplicate_key','extra_fact','wrong_enum','wrong_schema','missing_field','repeated_quote','nonfinite','markdown','overlong'])
def test_untrusted_response_rejected(kind,tmp_path):
    answer=TEXT; obj=raw(); f=obj['claims'][0]['fields']
    if kind=='bad_quote': f['isothermal']['quotes']=['없는 구절']
    if kind=='extra_fact': obj['fact_id']='spoofed'
    if kind=='wrong_enum': f['outcome']['value']='SUPPORT_CANDIDATE'
    if kind=='wrong_schema': obj['schema']='other'
    if kind=='missing_field': f.pop('scope')
    if kind=='repeated_quote':
        answer=TEXT+' 열전대'; obj['claims'][0]['span_text']=answer
    body=json.dumps(obj)
    if kind=='duplicate_key': body=body.replace('"schema":','"schema":"duplicate", "schema":',1)
    if kind=='nonfinite': body=body[:-1]+',"number":NaN}'
    if kind=='markdown': body='```json\n'+body+'\n```'
    if kind=='overlong': body=' '*60001
    r=evaluate_extraction(answer,body,registry_path=tmp_path/'missing')
    assert r['extraction_status']=='REJECTED'
    safety(r)


def test_provider_callable_and_failure(tmp_path):
    calls=[]
    def provider(prompt):
        calls.append(prompt); return json.dumps(raw())
    r=extract_and_evaluate(TEXT,provider,registry_path=tmp_path/'missing')
    assert len(calls)==1 and r['conditional_candidate']=='SUPPORT_CANDIDATE'
    assert r['registry_bound_candidate']=='UNRESOLVED'
    safety(r)
    def fail(prompt): raise RuntimeError('never logged')
    r=extract_and_evaluate(TEXT,fail)
    assert r['reason']=='PROVIDER_FAILED'; safety(r)


@pytest.mark.parametrize('text',[
    TEXT.replace('변하지 않는다','변하지 않는다고 주장한다'),
    TEXT.replace('균질한 제3 금속','균질한 제3 금속이 아닐 때의 도체'),
    TEXT.replace('두 신규 접점이 등온이면','두 신규 접점이 등온임을 확인하지 않고'),
    TEXT+' 그러나 이 설명은 틀렸다.',
    '“'+TEXT+'”라고 인용한다.',
])
def test_literal_evidence_does_not_automatically_prove_claim(text,tmp_path):
    obj=raw(); obj['claims'][0]['span_text']=text
    for field in obj['claims'][0]['fields'].values():
        field['quotes']=[q if q in text else q.replace('변하지 않는다','변하지 않는').replace('제3 금속을 삽입','삽입') for q in field['quotes']]
    r=evaluate_extraction(text,json.dumps(obj),registry_path=tmp_path/'missing')
    assert r['conditional_candidate']=='UNRESOLVED'
    safety(r)


def test_no_or_multiple_claims_not_promoted(tmp_path):
    for claims in [[],raw()['claims']*2]:
        r=evaluate_extraction(TEXT,json.dumps({'schema':EXTRACT_SCHEMA,'claims':claims}),registry_path=tmp_path/'missing')
        assert r['conditional_candidate']=='UNRESOLVED'; safety(r)


def test_full_registry_wrong_hash_rejected(tmp_path):
    f=tmp_path/'r.json'; f.write_text('{"facts":[]}')
    with pytest.raises(ValueError,match='REGISTRY_HASH_MISMATCH'): load_registry_binding(f)


def test_full_registry_when_checkout_available():
    if not REGISTRY_PATH.is_file(): pytest.skip('full Registry not in isolated environment')
    assert load_registry_binding()['kind']=='FULL_REGISTRY_FILE'
    r=evaluate_extraction(TEXT,json.dumps(raw()))
    assert r['registry_bound_candidate']=='SUPPORT_CANDIDATE'; safety(r)
    wrong=TEXT.replace('변하지 않는다','증가한다')
    r=evaluate_extraction(wrong,json.dumps(raw(wrong,True)))
    assert r['registry_bound_candidate']=='CONTRADICT_CANDIDATE'; safety(r)


def test_verified_actual_export_if_available(tmp_path):
    export=Path(__file__).resolve().parents[1]/'verified_registry_projection.json'
    if not export.is_file(): pytest.skip('separate GitHub row export not supplied')
    b=load_verified_export(export); assert b['kind']=='PINNED_GITHUB_ROW_EXPORT'
    r=evaluate_extraction(TEXT,json.dumps(raw()),export_path=export)
    assert r['registry_bound_candidate']=='SUPPORT_CANDIDATE'; safety(r)
    obj=json.loads(export.read_text()); obj['row']['relation']['conditions']=[]
    altered=tmp_path/'bad.json'; altered.write_text(json.dumps(obj))
    assert evaluate_extraction(TEXT,json.dumps(raw()),export_path=altered)['registry_bound_candidate']=='UNRESOLVED'
