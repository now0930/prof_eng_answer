"""Optional real-data rehearsal. Private WordPress text never enters Git."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
from unittest.mock import patch

import pytest
import bot
from study.learning_runtime import record_completed_grade
from study.master_topic_pack import project_grading, project_training, project_diagnosis
from study.review_presentation import learning_review_messages
from study.synthesis_authoring import build_candidate, encoded
from study.training_history import TrainingHistoryStore

ROOT = Path(__file__).resolve().parents[1]
TOPIC = 'nyquist_stability_criterion_gain_phase_margin'
WORK = ROOT / 'data/topic_learning_authoring' / TOPIC / 'stage4_initial'


def test_private_nyquist_synthesis_flow(tmp_path):
    if not (WORK / 'candidate/draft.json').is_file():
        pytest.skip('private authored candidate absent')
    packet = json.loads((WORK / 'sources.json').read_text())
    authored = json.loads((WORK / 'authored.json').read_text())
    master_path = Path('master_topic_packs') / f'{TOPIC}.json'
    baseline = (ROOT / master_path).read_bytes()
    if hashlib.sha256(baseline).hexdigest() != packet['base_master_sha256']:
        backups = (ROOT / 'data/topic_learning_synthesis' / TOPIC / 'applications').glob('*/master.before.json')
        matches = [p.read_bytes() for p in backups
                   if hashlib.sha256(p.read_bytes()).hexdigest() == packet['base_master_sha256']]
        assert matches, 'exact historical Master backup required for private rehearsal'
        baseline = matches[0]
    master = json.loads(baseline)
    bundle_path = Path('data/wordpress_topic_packs') / f'{TOPIC}.json'
    paths = [master_path, bundle_path, *map(Path, master['legacy_topic_pack']['source_files'].values()),
             *map(Path, master.get('learning_materials', []))]
    annotation = Path('study/source_review_annotations') / f'{TOPIC}.json'
    if (ROOT / annotation).exists():
        paths.append(annotation)
    before = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    for relative in paths:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    # Reproduce the original candidate against its exact baseline in isolation.
    # Never weaken the live stale-Master gate or modify the installed Master.
    (tmp_path / master_path).write_bytes(baseline)
    draft, report = build_candidate(tmp_path, packet, authored)
    assert draft == json.loads((WORK / 'candidate/draft.json').read_text())
    assert report['source_count'] == 2
    grade_before = project_grading(tmp_path, master)

    def install_in_sandbox(doc):
        content = encoded(doc)
        (tmp_path / 'synthesis.json').write_bytes(content)
        master['learning_synthesis'] = dict(path='synthesis.json', revision=doc['revision'],
                                          content_sha256=hashlib.sha256(content).hexdigest())
        (tmp_path / master_path).write_bytes(encoded(master))

    install_in_sandbox(draft)
    assert '검토 대기' in learning_review_messages(project_training(tmp_path, master))[0]

    # Exercise the LLM-reviewed path only in this isolated rehearsal; never human approval.
    reviewed = copy.deepcopy(draft)
    def mark_llm_review(value):
        if isinstance(value, dict):
            if 'review' in value:
                value['review'] = dict(status='llm_reviewed_human_pending', reviewed_by='stage7-rehearsal',
                    reviewed_at='2026-10-05T00:00:00Z', note='Isolated presentation rehearsal; human review pending')
            for child in value.values(): mark_llm_review(child)
        elif isinstance(value, list):
            for child in value: mark_llm_review(child)
    mark_llm_review(reviewed)
    install_in_sandbox(reviewed)
    training = project_training(tmp_path, master)
    assert len(training['learning_synthesis']['eligible_section_ids']) == 6
    rendered = '\n'.join(learning_review_messages(training))
    assert rendered.index('[S0]') < rendered.index('[S4]') < rendered.index('[S5]')
    assert '사람 검토 대기' in rendered and '자가 점검' in rendered
    assert project_grading(tmp_path, master) == grade_before
    assert project_diagnosis(tmp_path, master)['learning_navigation']['targets'] == []

    history = TrainingHistoryStore(tmp_path / 'history.sqlite3')
    grade = dict(topic_id=TOPIC, final_total_score=12.0, verdict='needs_correction', weaknesses=['복습 예시'])
    before_grade = copy.deepcopy(grade)
    record_completed_grade(history, learner_id='123', sid='synthesis-rehearsal', grade=grade,
        submission_normalization={'question_text':'Nyquist 복습'}, master_directory=tmp_path / 'master_topic_packs',
        session_directory=tmp_path / 'session')
    messages = []
    with patch.object(bot,'BASE_DIR',tmp_path), patch.object(bot,'DATA_DIR',tmp_path), \
         patch.dict('os.environ',{'TRAINING_HISTORY_DB':str(tmp_path / 'history.sqlite3')}), \
         patch.object(bot,'send_message',side_effect=lambda chat,msg:messages.append(msg)):
        bot.handle_text({'text':'/review ' + TOPIC},123,{})
        assert '[S5]' in '\n'.join(messages)
        bot.handle_text({'text':'/review done ' + TOPIC},123,{})
        assert '복습 완료' in messages[-1]
    attempt = history.list_attempts(learner_id='123',topic_id=TOPIC)[0]
    assert attempt['score'] == 12.0 and attempt['last_reviewed_at']
    assert grade == before_grade

    # Honest rehash of edited source still invalidates the pinned evidence hash.
    bundle = json.loads((tmp_path / bundle_path).read_text())
    for source in bundle['sources']:
        if source['source_id'] == 'wp-post:6134':
            source['extracted_text'] += '\nChanged for rehearsal.'
            source['extracted_text_sha256'] = hashlib.sha256(source['extracted_text'].encode()).hexdigest()
    (tmp_path / bundle_path).write_bytes(encoded(bundle))
    stale = project_training(tmp_path, master)['learning_synthesis']
    assert not stale['eligible_section_ids']
    assert project_grading(tmp_path, master) == grade_before
    assert before == {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
