import copy
import json

import pytest

from study.synthesis_mapping import add_mapping
from study.synthesis_authoring import prepare_sources, build_candidate, encoded, write_new_bundle
from study.synthesis_application import decision_template, preview_application, apply_application
from study.master_topic_pack import project_grading, project_diagnosis
from test_synthesis_authoring import setup_packet
from test_synthesis_application import llm_approve


def setup(tmp_path):
    master, doc, _ = setup_packet(tmp_path)
    relative = 'demand.json'
    master['legacy_topic_pack']['source_files']['question_demand_axes'] = relative
    (tmp_path / relative).write_bytes(encoded(dict(topic_id=master['topic_id'],
        requirements=[dict(requirement_id='D1', requirement_text='Explain synthetic concept')])))
    (tmp_path / 'master_topic_packs' / f'{master["topic_id"]}.json').write_bytes(encoded(master))
    packet = prepare_sources(tmp_path, master['topic_id'], include_mapping_targets=True)
    return master, doc, packet


def candidate(packet, doc, **overrides):
    args = dict(link_id='L1', requirement_id='D1', knowledge_ids=['K0'], section_ids=['S0'])
    args.update(overrides)
    return add_mapping(packet, doc, **args)


@pytest.mark.parametrize('approved', [False, True])
def test_new_mapping_end_to_end_separate_review(tmp_path, approved):
    master, doc, packet = setup(tmp_path)
    before = copy.deepcopy(doc)
    mapped = candidate(packet, doc)
    assert doc == before
    draft, report = build_candidate(tmp_path, packet, mapped)
    assert report['mapping_changes'][0]['change'] == 'added'
    assert report['mapping_changes'][0]['before'] is None
    workspace = tmp_path / 'data/topic_learning_authoring' / master['topic_id'] / 'new'
    write_new_bundle(workspace, {'sources.json': encoded(packet)})
    write_new_bundle(workspace/'candidate', {'authored.json':encoded(mapped),
        'draft.json':encoded(draft), 'report.json':encoded(report)})
    decision = llm_approve(decision_template(tmp_path, workspace))
    mapping = decision['reviews'][-1]
    assert mapping['target'] == 'grading_links:L1'
    with pytest.raises(ValueError, match='separate human review'):
        preview_application(tmp_path, workspace, decision)
    mapping.update(status='human_verified' if approved else 'human_review_required',
        actor_type='human' if approved else 'llm', actor='test-reviewer', note='Synthetic mapping review')
    apply_application(tmp_path, workspace, decision, applied_by='test-operator')
    updated = json.loads((tmp_path/'master_topic_packs'/f'{master["topic_id"]}.json').read_text())
    assert project_grading(tmp_path, updated) == project_grading(tmp_path, master)
    targets = project_diagnosis(tmp_path, updated)['learning_navigation']['targets']
    assert bool(targets) == approved
    if approved:
        assert targets[0]['target']['record_id'] == 'D1'
        assert targets[0]['lessons'][0]['section_id'] == 'S0'


@pytest.mark.parametrize('mutation', ['unknown_requirement','unknown_knowledge','unknown_section','unrelated_section','duplicate_id','no_catalog','stale_source','forged_catalog'])
def test_new_mapping_rejects_invalid_input(tmp_path, mutation):
    master, doc, packet = setup(tmp_path)
    args = {}
    if mutation == 'unknown_requirement': args['requirement_id'] = 'missing'
    if mutation == 'unknown_knowledge': args['knowledge_ids'] = ['missing']
    if mutation == 'unknown_section': args['section_ids'] = ['missing']
    if mutation == 'unrelated_section': args['section_ids'] = ['S1']
    if mutation == 'duplicate_id': doc = candidate(packet, doc)
    if mutation == 'no_catalog': packet = prepare_sources(tmp_path, master['topic_id'])
    if mutation == 'stale_source': (tmp_path/'demand.json').write_text('{}')
    if mutation == 'forged_catalog': packet['mapping_targets'][0]['target']['source_content_sha256'] = '0'*64
    with pytest.raises(ValueError):
        mapped = candidate(packet, doc, **args)
        build_candidate(tmp_path, packet, mapped)


@pytest.mark.parametrize('mutation', ['wrong_topic','duplicate_id','empty_text','no_id'])
def test_catalog_rejects_invalid_canonical(tmp_path, mutation):
    master, _, _ = setup(tmp_path)
    path = tmp_path/'demand.json'
    doc = json.loads(path.read_text())
    if mutation == 'wrong_topic': doc['topic_id'] = 'other_topic'
    if mutation == 'duplicate_id': doc['requirements'] *= 2
    if mutation == 'empty_text': doc['requirements'][0]['requirement_text'] = ''
    if mutation == 'no_id': doc['requirements'][0].pop('requirement_id')
    path.write_bytes(encoded(doc))
    with pytest.raises(ValueError): prepare_sources(tmp_path, master['topic_id'], include_mapping_targets=True)


def test_no_canonical_axes_means_no_inferred_targets(tmp_path):
    master, _, _ = setup_packet(tmp_path)
    assert prepare_sources(tmp_path, master['topic_id'], include_mapping_targets=True)['mapping_targets'] == []


def test_manual_candidate_cannot_bypass_knowledge_section_binding(tmp_path):
    _, doc, packet = setup(tmp_path)
    mapped = candidate(packet, doc)
    mapped['grading_links'][0]['section_ids'] = ['S1']
    with pytest.raises(ValueError, match='reference mapped knowledge'):
        build_candidate(tmp_path, packet, mapped)


def test_cli_mapping_draft_is_exclusive_and_does_not_edit_input(tmp_path, monkeypatch):
    import scripts.author_topic_learning_synthesis as cli
    master, doc, packet = setup(tmp_path)
    workspace = tmp_path/'data/topic_learning_authoring'/master['topic_id']/'cli'
    write_new_bundle(workspace, {'sources.json':encoded(packet), 'authored.json':encoded(doc)})
    monkeypatch.setattr(cli, 'ROOT', tmp_path)
    monkeypatch.setattr('sys.argv', ['author', 'add-mapping', '--topic-id', master['topic_id'],
        '--run-id','cli','--authored',str(workspace/'authored.json'), '--link-id','L1',
        '--requirement-id','D1','--knowledge-id','K0','--section-id','S0'])
    assert cli.main() == 0
    output = (workspace/'authored.mapping.json').read_bytes()
    assert json.loads(output)['grading_links'][0]['review']['status'] == 'draft'
    assert cli.main() == 1
    assert (workspace/'authored.mapping.json').read_bytes() == output
    assert (workspace/'authored.json').read_bytes() == encoded(doc)
