import copy
import hashlib
import json

import pytest

from study.learning_synthesis import SynthesisError, validate_synthesis, load_synthesis
from study.master_topic_pack import project_training, project_grading, validate_master_topic_pack
from test_master_topic_pack_schema import _valid_record
from test_training_diagnosis_projections import _write_sources


def digest(value):
    return hashlib.sha256(value).hexdigest()


def fixture(tmp_path):
    master = _valid_record()
    _write_sources(tmp_path, master)
    review = {'status': 'llm_reviewed_human_pending', 'reviewed_by': 'test-reviewer', 'reviewed_at': '2026-10-05T00:00:00Z', 'note': ''}
    evidence, raw = [], []
    source = master['sources'][0]
    for i in range(2):
        s = copy.deepcopy(source)
        s['source_id'] = f'wp-{i}'
        if i == 0:
            master['sources'] = []
        master['sources'].append(s)
        text = f'Synthetic concept {i}.'
        evidence.append(dict(evidence_id=f'E{i}', source_id=s['source_id'], source_url=s['source_url'], source_version=s['version'], source_content_sha256=digest(text.encode()), locator='section 1', excerpt=text))
        raw.append(dict(source_id=s['source_id'], source_url=s['source_url'], version=s['version'], text=text))
    knowledge = [dict(knowledge_id=f'K{i}', kind='concept', title=f'Concept {i}', statement=evidence[i]['excerpt'], conditions=[], units=[], exceptions=[], evidence_ids=[f'E{i}'], origin='source_excerpt', review=copy.deepcopy(review)) for i in range(2)]
    sections = [dict(section_id=f'S{i}', kind='concept', title=f'Lesson {i}', knowledge_ids=[f'K{i}'], body='Authored teaching explanation.', origin='authored', evidence_ids=[], material_ids=[], self_check=[]) for i in range(2)]
    payload = dict(schema_version='topic-learning-synthesis-v1', topic_id=master['topic_id'], revision=1, evidence=evidence, knowledge=knowledge,
        relations=[dict(relation_id='R1', from_id='K0', to_id='K1', kind='prerequisite', explanation='Study first.', evidence_ids=['E0','E1'], review=copy.deepcopy(review))], conflicts=[],
        learning_path=dict(path_id='P1', title='Learning path', objectives=['Understand concepts'], sections=sections, review=copy.deepcopy(review)), grading_links=[], score_effect='none')
    return master, payload, raw


def save(tmp_path, master, payload):
    content = json.dumps(payload).encode()
    (tmp_path / 'synthesis.json').write_bytes(content)
    master['learning_synthesis'] = dict(path='synthesis.json', revision=1, content_sha256=digest(content))


def test_multisource_read_only_adapter_and_material_reuse(tmp_path):
    master, doc, raw = fixture(tmp_path)
    doc['learning_path']['sections'][0]['material_ids'] = ['old_material']
    save(tmp_path, master, doc)
    validate_master_topic_pack(master)
    before = copy.deepcopy(master)
    result = load_synthesis(tmp_path, master, raw, [{'material_id':'old_material'}])
    assert result['eligible_section_ids'] == ['S0','S1']
    result['document']['knowledge'].clear()
    assert len(load_synthesis(tmp_path, master, raw, [{'material_id':'old_material'}])['document']['knowledge']) == 2
    assert master == before
    with pytest.raises(SynthesisError, match='unknown learning material'):
        load_synthesis(tmp_path, master, raw, [])


@pytest.mark.parametrize('mutation', ['duplicate','reference','cycle','order','review','unknown','boolean','excerpt','conflict'])
def test_invalid_contracts(tmp_path, mutation):
    _, doc, _ = fixture(tmp_path)
    if mutation == 'duplicate': doc['knowledge'].append(copy.deepcopy(doc['knowledge'][0]))
    if mutation == 'reference': doc['knowledge'][0]['evidence_ids'] = ['absent']
    if mutation == 'cycle': doc['relations'].append({**doc['relations'][0], 'relation_id':'R2','from_id':'K1','to_id':'K0'})
    if mutation == 'order': doc['learning_path']['sections'].reverse()
    if mutation == 'review': doc['learning_path']['review']['reviewed_at'] = '2026-10-05'
    if mutation == 'unknown': doc['score'] = 25
    if mutation == 'boolean': doc['revision'] = True
    if mutation == 'excerpt': doc['knowledge'][0]['statement'] = 'Invented quote'
    if mutation == 'conflict': doc['conflicts'] = [dict(conflict_id='C1', knowledge_ids=['K0'], evidence_ids=['E0','E1'], description='Conflict', status='resolved', resolution='Resolved', review=doc['learning_path']['review'])]
    with pytest.raises(SynthesisError): validate_synthesis(doc)


@pytest.mark.parametrize('mutation', ['hash','url','version','quote','missing'])
def test_evidence_mismatch_excludes_dependent_sections(tmp_path, mutation):
    master, doc, raw = fixture(tmp_path)
    if mutation == 'hash': raw[0]['text'] += ' changed'
    if mutation == 'url': doc['evidence'][0]['source_url'] += '/other'
    if mutation == 'version': doc['evidence'][0]['source_version'] = 'new'
    if mutation == 'quote': doc['evidence'][0]['excerpt'] = doc['knowledge'][0]['statement'] = 'missing quote'
    if mutation == 'missing': raw = raw[1:]
    save(tmp_path, master, doc)
    result = load_synthesis(tmp_path, master, raw, [])
    assert result['eligible_section_ids'] == []
    assert result['evidence_states']['E0'] != 'matching'


def test_conflict_and_canonical_mapping(tmp_path):
    master, doc, raw = fixture(tmp_path)
    path = tmp_path / master['legacy_topic_pack']['source_files']['fact_anchor']
    doc['grading_links'] = [dict(link_id='L1', target=dict(source_key='fact_anchor',record_id='f1',source_content_sha256=digest(path.read_bytes())),knowledge_ids=['K0'],section_ids=['S0'],review=doc['learning_path']['review'])]
    doc['conflicts'] = [dict(conflict_id='C1',knowledge_ids=['K0'],evidence_ids=['E0','E1'],description='Conflicting sources',status='unresolved',resolution=None,review=doc['learning_path']['review'])]
    save(tmp_path, master, doc)
    assert load_synthesis(tmp_path, master, raw, [])['eligible_section_ids'] == []
    doc['grading_links'][0]['target']['record_id'] = 'invented'
    save(tmp_path, master, doc)
    with pytest.raises(SynthesisError, match='canonical record'):
        load_synthesis(tmp_path, master, raw, [])


def test_training_optional_failure_preserves_grading_and_v1(tmp_path):
    master, doc, _ = fixture(tmp_path)
    original = project_training(tmp_path, master)
    grade = project_grading(tmp_path, master)
    assert 'learning_synthesis' not in original
    save(tmp_path, master, doc)
    loaded = project_training(tmp_path, master)
    assert loaded.pop('learning_synthesis')['status'] == 'loaded'
    assert loaded == original
    (tmp_path / 'synthesis.json').write_text('{}')
    result = project_training(tmp_path, master)
    assert result['learning_synthesis']['status'] == 'unavailable'
    assert project_grading(tmp_path, master) == grade


def test_unsafe_and_symlink_reference(tmp_path):
    master, doc, raw = fixture(tmp_path)
    save(tmp_path, master, doc)
    master['learning_synthesis']['path'] = '../outside.json'
    with pytest.raises(ValueError): validate_master_topic_pack(master)
    master['learning_synthesis']['path'] = 'link.json'
    (tmp_path / 'link.json').symlink_to('/etc/passwd')
    with pytest.raises(SynthesisError, match='escapes'):
        load_synthesis(tmp_path, master, raw, [])


def test_cycle_even_when_introduced_in_same_section(tmp_path):
    _, doc, _ = fixture(tmp_path)
    doc['learning_path']['sections'] = [doc['learning_path']['sections'][0]]
    doc['learning_path']['sections'][0]['knowledge_ids'] = ['K0','K1']
    doc['relations'].append({**doc['relations'][0], 'relation_id':'R2', 'from_id':'K1', 'to_id':'K0'})
    with pytest.raises(SynthesisError, match='cycle'): validate_synthesis(doc)


def test_reference_schema_and_python_agree_on_paths(tmp_path):
    from study.learning_synthesis import _shape, validate_reference
    from pathlib import Path
    schema = json.loads((Path(__file__).resolve().parents[1] / 'schemas/master_topic_pack.schema.json').read_text())['properties']['learning_synthesis']
    for path, valid in [('data/pack.json',True),('../pack.json',False),('./pack.json',False),('/pack.json',False),('a//pack.json',False),('a/../pack.json',False),('a\\pack.json',False)]:
        ref = dict(path=path, revision=1, content_sha256='a'*64)
        if valid:
            _shape(ref, schema)
            validate_reference(ref)
        else:
            with pytest.raises(SynthesisError): _shape(ref, schema)
            with pytest.raises(SynthesisError): validate_reference(ref)


@pytest.mark.parametrize('change', ['topic','revision','canonical_hash','unlinked'])
def test_snapshot_identity(tmp_path, change):
    master, doc, raw = fixture(tmp_path)
    if change == 'topic': doc['topic_id'] = 'other_topic_id'
    if change == 'revision': doc['revision'] = 2
    if change == 'canonical_hash':
        doc['grading_links'] = [dict(link_id='L1',target=dict(source_key='fact_anchor',record_id='f1',source_content_sha256='0'*64),knowledge_ids=['K0'],section_ids=['S0'],review=doc['learning_path']['review'])]
    if change == 'unlinked': master['sources'] = []
    save(tmp_path, master, doc)
    with pytest.raises(SynthesisError): load_synthesis(tmp_path, master, raw, [])
