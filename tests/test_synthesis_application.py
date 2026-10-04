import copy
import json
from unittest.mock import patch

import pytest

from study.synthesis_application import decision_template, preview_application, apply_application
from study.synthesis_authoring import build_candidate, encoded, write_new_bundle
from study.master_topic_pack import project_grading, project_training
from test_synthesis_authoring import setup_packet


def setup(tmp_path):
    master, authored, packet = setup_packet(tmp_path)
    workspace = tmp_path / 'data/topic_learning_authoring' / master['topic_id'] / 'run'
    draft, report = build_candidate(tmp_path, packet, authored)
    write_new_bundle(workspace, {'sources.json':encoded(packet)})
    write_new_bundle(workspace / 'candidate', {'draft.json':encoded(draft), 'report.json':encoded(report), 'authored.json':encoded(authored)})
    return master, workspace, decision_template(tmp_path, workspace)


def approve(decision):
    result = copy.deepcopy(decision)
    result['application'] = dict(decision='approve',actor='test-operator',actor_type='human',decided_at='2026-10-05T00:00:00Z')
    for review in result['reviews']:
        review.update(status='llm_reviewed_human_pending',actor='test-model',actor_type='llm',decided_at='2026-10-05T00:00:00Z')
    return result


def snapshot(root):
    return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}


def test_pending_preview_read_only_and_apply_rejected(tmp_path):
    _, workspace, decision = setup(tmp_path)
    before = snapshot(tmp_path)
    preview = preview_application(tmp_path, workspace, decision)
    assert not preview['can_apply'] and preview['eligible_section_ids'] == []
    assert before == snapshot(tmp_path)
    with pytest.raises(ValueError,match='explicit approval'):
        apply_application(tmp_path,workspace,decision,applied_by='operator')


def test_apply_links_only_reviewed_material_and_preserves_grading(tmp_path):
    master, workspace, decision = setup(tmp_path)
    old = project_grading(tmp_path,master)
    decision = approve(decision)
    preview = preview_application(tmp_path,workspace,decision)
    assert preview['can_apply']
    result = apply_application(tmp_path,workspace,decision,applied_by='operator')
    path = tmp_path / 'master_topic_packs' / f'{master["topic_id"]}.json'
    updated = json.loads(path.read_text())
    assert updated['revision'] == master['revision'] + 1
    assert project_grading(tmp_path,updated) == old
    assert project_training(tmp_path,updated)['learning_synthesis']['eligible_section_ids'] == ['S0','S1']
    from pathlib import Path
    audit = Path(result['audit_path'])
    assert json.loads((audit / 'master.before.json').read_text()) == master
    assert (audit / 'master.after.json').read_bytes() == path.read_bytes()
    with pytest.raises(ValueError):
        apply_application(tmp_path,workspace,decision,applied_by='operator')


@pytest.mark.parametrize('change',['candidate_hash','master_hash','llm_approval','fake_human','duplicate','incomplete','timestamp','source_change','candidate_change','master_change'])
def test_stale_or_invalid_decisions_fail_closed(tmp_path,change):
    master, workspace, decision = setup(tmp_path)
    decision = approve(decision)
    if change == 'candidate_hash': decision['candidate_sha256'] = '0'*64
    if change == 'master_hash': decision['base_master_sha256'] = '0'*64
    if change == 'llm_approval': decision['application']['actor_type'] = 'llm'
    if change == 'fake_human': decision['reviews'][0]['status'] = 'human_verified'
    if change == 'duplicate': decision['reviews'].append(copy.deepcopy(decision['reviews'][0]))
    if change == 'incomplete': decision['reviews'].pop()
    if change == 'timestamp': decision['application']['decided_at'] = '2026-10-05'
    if change == 'candidate_change': (workspace / 'candidate/draft.json').write_text('{}')
    if change == 'master_change':
        master['revision'] += 1
        (tmp_path / 'master_topic_packs' / f'{master["topic_id"]}.json').write_bytes(encoded(master))
    if change == 'source_change':
        path = tmp_path / 'data/wordpress_topic_packs' / f'{master["topic_id"]}.json'
        path.write_text('{}')
    before = snapshot(tmp_path)
    with pytest.raises((ValueError,KeyError)):
        preview_application(tmp_path,workspace,decision)
    assert before == snapshot(tmp_path)


def test_replacement_failure_preserves_original_and_audit(tmp_path):
    master, workspace, decision = setup(tmp_path)
    path = tmp_path / 'master_topic_packs' / f'{master["topic_id"]}.json'
    before = path.read_bytes()
    with patch('study.synthesis_application.os.replace',side_effect=OSError('injected write failure')):
        with pytest.raises(OSError,match='injected'):
            apply_application(tmp_path,workspace,approve(decision),applied_by='operator')
    assert path.read_bytes() == before
    assert not list(path.parent.glob('.learning-apply-*'))
    assert list((tmp_path / 'data/topic_learning_synthesis').rglob('master.before.json'))
    # Reusing the same immutable staged files is safe after a pre-commit failure.
    assert apply_application(tmp_path,workspace,approve(decision),applied_by='operator')['status'] == 'applied'


def llm_approve(decision):
    result = approve(decision)
    result['application'].update(actor='test-model', actor_type='llm')
    for review in result['reviews']:
        review.update(status='llm_verified', note='Checked source, conditions and units.')
    return result


def test_llm_approval_preserves_identity_and_grading(tmp_path):
    master, workspace, decision = setup(tmp_path)
    old = project_grading(tmp_path, master)
    result = apply_application(tmp_path, workspace, llm_approve(decision), applied_by='test-model')
    updated = json.loads((tmp_path / 'master_topic_packs' / f'{master["topic_id"]}.json').read_text())
    training = project_training(tmp_path, updated)
    from study.review_presentation import learning_review_messages
    assert 'LLM 승인·사람 승인 아님' in '\n'.join(learning_review_messages(training))
    assert project_grading(tmp_path, updated) == old
    from pathlib import Path
    assert json.loads((Path(result['audit_path']) / 'decision.json').read_text())['application']['actor_type'] == 'llm'


@pytest.mark.parametrize('target,eligible', [('knowledge:K1',['S0']), ('knowledge:K0',[])])
def test_uncertain_content_and_dependents_quarantined(tmp_path, target, eligible):
    _, workspace, decision = setup(tmp_path)
    decision = llm_approve(decision)
    for review in decision['reviews']:
        if review['target'] == target:
            review.update(status='human_review_required', note='Conflicting interpretation; human review needed.')
    preview = preview_application(tmp_path, workspace, decision)
    assert preview['eligible_section_ids'] == eligible
    assert preview['human_review_targets'] == [target]
    assert preview['can_apply'] == bool(eligible)


@pytest.mark.parametrize('mutation', ['no_note','wrong_actor','pending_path'])
def test_llm_approval_requires_rationale_and_identity(tmp_path, mutation):
    _, workspace, decision = setup(tmp_path)
    decision = llm_approve(decision)
    if mutation == 'no_note': decision['reviews'][0]['note'] = ' '
    if mutation == 'wrong_actor': decision['reviews'][0]['actor_type'] = 'human'
    if mutation == 'pending_path': decision['reviews'][0]['status'] = 'human_review_required'
    with pytest.raises(ValueError): preview_application(tmp_path, workspace, decision)
