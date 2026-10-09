import copy
import json

import pytest

from study.learning_synthesis import SynthesisError
from study.synthesis_authoring import (
    build_candidate, compile_draft, encoded, prepare_sources, write_new_bundle,
)
from test_learning_synthesis import fixture, digest


def setup_packet(tmp_path):
    master, doc, raw = fixture(tmp_path)
    directory = tmp_path / 'master_topic_packs'
    directory.mkdir()
    (directory / f'{master["topic_id"]}.json').write_bytes(encoded(master))
    rows = []
    for source, material in zip(master['sources'], raw):
        rows.append(dict(source_id=source['source_id'], source_type=source['source_type'], wordpress_url=source['wordpress_url'],
                         source_url=source['source_url'], version=source['version'],
                         extracted_text=material['text'], extracted_text_sha256=digest(material['text'].encode()),
                         extraction_status='extracted', extraction_method='wordpress_wxr_html'))
    bundles = tmp_path / 'data/wordpress_topic_packs'
    bundles.mkdir(parents=True)
    (bundles / f'{master["topic_id"]}.json').write_bytes(encoded(dict(topic_id=master['topic_id'], private=True, sources=rows)))
    return master, doc, prepare_sources(tmp_path, master['topic_id'])


def test_multiblog_candidate_keeps_inputs_and_resets_approval(tmp_path):
    master, authored, packet = setup_packet(tmp_path)
    original = copy.deepcopy(authored)
    before = {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    draft, report = build_candidate(tmp_path, packet, authored)
    assert report['source_count'] == 2
    assert draft['learning_path']['review']['status'] == 'draft'
    assert all(k['review']['status'] == 'draft' for k in draft['knowledge'])
    assert authored == original
    assert before == {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    assert draft['grading_links'] == []


def test_exact_dedup_keeps_provenance_and_rewrites_references(tmp_path):
    _, doc, packet = setup_packet(tmp_path)
    duplicate = copy.deepcopy(doc['knowledge'][0])
    duplicate['knowledge_id'] = 'K2'
    doc['knowledge'].append(duplicate)
    doc['learning_path']['sections'][0]['knowledge_ids'].append('K2')
    draft, report = compile_draft(packet, doc)
    assert report['merged_knowledge_ids'] == {'K2':'K0'}
    assert len(draft['knowledge']) == 2
    assert draft['learning_path']['sections'][0]['knowledge_ids'] == ['K0']
    duplicate['conditions'] = ['Different operating conditions']
    draft, report = compile_draft(packet, doc)
    assert not report['merged_knowledge_ids']
    assert len(draft['knowledge']) == 3


def test_unresolved_conflict_is_preserved(tmp_path):
    _, doc, packet = setup_packet(tmp_path)
    doc['conflicts'] = [dict(conflict_id='C1',knowledge_ids=['K0','K1'],evidence_ids=['E0','E1'],
                             description='Author reported conflict',status='unresolved',resolution=None,
                             review=copy.deepcopy(doc['learning_path']['review']))]
    draft, report = compile_draft(packet, doc)
    assert draft['conflicts'][0]['status'] == 'unresolved'
    assert report['conflict_detection'] == 'author_supplied_not_automatic'


@pytest.mark.parametrize('mutation', ['source','hash','quote','url','topic','packet','master','single_source'])
def test_forged_or_stale_input_rejected(tmp_path, mutation):
    master, doc, packet = setup_packet(tmp_path)
    if mutation == 'source': doc['evidence'][0]['source_id'] = 'not_linked'
    if mutation == 'hash': doc['evidence'][0]['source_content_sha256'] = '0'*64
    if mutation == 'quote': doc['evidence'][0]['excerpt'] = doc['knowledge'][0]['statement'] = 'invented quote'
    if mutation == 'url': doc['evidence'][0]['source_url'] += '/forged'
    if mutation == 'topic': doc['topic_id'] = 'different_topic'
    if mutation == 'packet': packet['sources'][0]['text'] += 'tampered'
    if mutation == 'master':
        master['revision'] += 1
        (tmp_path / 'master_topic_packs' / f'{master["topic_id"]}.json').write_bytes(encoded(master))
    if mutation == 'single_source':
        doc['knowledge'][1]['evidence_ids'] = ['E0']
        doc['knowledge'][1]['origin'] = 'authored'
    with pytest.raises(SynthesisError): build_candidate(tmp_path, packet, doc)


def test_exclusive_output_does_not_replace_existing(tmp_path):
    path = tmp_path / 'run'
    write_new_bundle(path, {'draft.json': b'original'})
    with pytest.raises(FileExistsError): write_new_bundle(path, {'draft.json': b'new'})
    assert (path / 'draft.json').read_bytes() == b'original'
