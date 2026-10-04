import copy
import json

import pytest

from study.learning_feedback import navigation_view, feedback_navigation, canonical_record
from study.learning_synthesis import SynthesisError, load_synthesis
from study.learning_runtime import feedback_from_view
from study.review_presentation import feedback_lesson_lines
from test_learning_synthesis import fixture, save, digest


def setup(tmp_path):
    master, doc, raw = fixture(tmp_path)
    relative = 'demand.json'
    master['legacy_topic_pack']['source_files']['question_demand_axes'] = relative
    content = json.dumps(dict(topic_id=master['topic_id'], requirements=[dict(requirement_id='D1', requirement_text='Explain A')])).encode()
    (tmp_path / relative).write_bytes(content)
    review = dict(status='human_verified', reviewed_by='fixture-human', reviewed_at='2026-10-05T00:00:00Z', note='synthetic test')
    doc['grading_links'] = [dict(link_id='L1',target=dict(source_key='question_demand_axes',record_id='D1',source_content_sha256=digest(content)),knowledge_ids=['K0'],section_ids=['S0'],review=review)]
    save(tmp_path, master, doc)
    nav = navigation_view(tmp_path, master, raw, [])
    grade = dict(topic_id=master['topic_id'], final_total_score=12,
        question_demand_contract=dict(requirements=[dict(requirement_id='D1', requirement_text='Explain A',topic_id=master['topic_id'],source='topic_pack_question_demand_axes',source_file=relative)]),
        canonical_evaluation_ledger=dict(rows=[dict(requirement_id='D1',requirement_text='Explain A',status='missing')]))
    return master, doc, raw, nav, grade


def test_missing_requirement_to_lesson_without_grade_mutation(tmp_path):
    master, _, raw, nav, grade = setup(tmp_path)
    before = copy.deepcopy(grade)
    view = dict(topic_id=master['topic_id'],score_effect='none',learning_navigation=nav)
    feedback = feedback_from_view(grade, view)
    assert feedback['learning_navigation']['recommendations'][0]['lessons'] == [{'section_id':'S0','title':'Lesson 0'}]
    assert grade == before
    assert 'statement' not in json.dumps(feedback['learning_navigation'])
    training = dict(learning_synthesis=load_synthesis(tmp_path,master,raw,[]))
    assert 'Lesson 0' in feedback_lesson_lines(feedback,training)[0]
    training['learning_synthesis']['master_revision'] += 1
    assert '버전' in feedback_lesson_lines(feedback,training)[0]


@pytest.mark.parametrize('change', ['wrong_topic','wrong_file','changed_text','unknown','correct','missing_id','duplicate'])
def test_ambiguous_or_unrelated_results_do_not_map(tmp_path,change):
    _, _, _, nav, grade = setup(tmp_path)
    row = grade['question_demand_contract']['requirements'][0]
    if change == 'wrong_topic': row['topic_id'] = 'other_topic'
    if change == 'wrong_file': row['source_file'] = 'other.json'
    if change == 'changed_text': row['requirement_text'] = 'Different requirement'
    if change in {'unknown','correct'}: grade['canonical_evaluation_ledger']['rows'][0]['status'] = change
    if change == 'missing_id': row.pop('requirement_id')
    if change == 'duplicate': grade['canonical_evaluation_ledger']['rows'] *= 2
    assert feedback_navigation(grade,nav)['recommendations'] == []


def test_pending_mapping_or_stale_source_not_recommended(tmp_path):
    master, doc, raw, _, _ = setup(tmp_path)
    doc['grading_links'][0]['review']['status'] = 'llm_reviewed_human_pending'
    save(tmp_path,master,doc)
    assert navigation_view(tmp_path,master,raw,[])['targets'] == []
    doc['grading_links'][0]['review']['status'] = 'human_verified'
    save(tmp_path,master,doc)
    raw[0]['text'] = 'changed'
    assert navigation_view(tmp_path,master,raw,[])['targets'] == []


@pytest.mark.parametrize('status', ['draft', 'human_review_required', 'llm_verified', 'rejected'])
def test_unapproved_or_retired_mapping_never_recommends(tmp_path, status):
    master, doc, raw, _, grade = setup(tmp_path)
    review = doc['grading_links'][0]['review']
    review['status'] = status
    if status == 'draft':
        review.update(reviewed_by=None, reviewed_at=None)
    save(tmp_path, master, doc)
    nav = navigation_view(tmp_path, master, raw, [])
    assert nav['status'] == 'loaded'
    assert nav['targets'] == []
    assert feedback_navigation(grade, nav)['recommendations'] == []


def test_nested_rule_and_no_id_source_fail_closed():
    doc = {'deterministic_checks':{'fatal_checks':[{'rule_id':'R1'}]}}
    assert canonical_record(doc,'logic_check','R1')['rule_id'] == 'R1'
    with pytest.raises(SynthesisError): canonical_record({'title':'R1'},'topic_importance','R1')
