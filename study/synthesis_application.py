"""Explicit, local review decisions and first-link application of learning drafts.

Review identities are operator attestations, not authentication credentials.
No decision is inferred from model-generated content or from running preview.
"""
import copy
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile

from .learning_synthesis import require, project_synthesis, _shape
from .master_topic_pack import project_grading, project_training, validate_master_topic_pack
from .synthesis_authoring import build_candidate, encoded, sha


def _file(root, relative):
    root = Path(root).resolve()
    path = root / relative
    require(path.resolve().is_relative_to(root), 'application path escapes repository')
    require(not path.is_symlink(), 'application file must not be a symlink')
    return path


def _candidate(root, workspace):
    root = Path(root).resolve()
    workspace = Path(workspace).resolve()
    require(workspace.is_relative_to(root / 'data/topic_learning_authoring'), 'workspace outside private authoring directory')
    def read(name):
        path = _file(root, workspace.relative_to(root) / name)
        return json.loads(path.read_text(encoding='utf-8'))
    packet, authored = read('sources.json'), read('candidate/authored.json')
    # Rebuild checks the current Master and source packet, not only stored hashes.
    draft, report = build_candidate(root, packet, authored)
    require(read('candidate/draft.json') == draft, 'candidate draft changed')
    require(read('candidate/report.json') == report, 'candidate report changed')
    return packet, draft, report


def _review_targets(doc):
    result = {'learning_path:' + doc['learning_path']['path_id']: doc['learning_path']}
    for group, field in [('knowledge','knowledge_id'), ('relations','relation_id'), ('conflicts','conflict_id')]:
        for row in doc[group]:
            result[group + ':' + row[field]] = row
    return result


def decision_template(root, workspace):
    packet, draft, report = _candidate(root, workspace)
    return dict(schema_version='learning-synthesis-decision-v1', topic_id=packet['topic_id'],
        candidate_sha256=report['draft_sha256'], base_master_sha256=packet['base_master_sha256'],
        application=dict(decision='pending', actor=None, actor_type='human', decided_at=None),
        reviews=[dict(target=key, status='draft', actor=None, actor_type='human', decided_at=None, note='')
                 for key in _review_targets(draft)], score_effect='none')


def _identity(row):
    require(row['actor_type'] in {'human','llm'}, 'invalid reviewer type')
    require(isinstance(row['actor'], str) and bool(row['actor'].strip()), 'review actor required')
    try:
        stamp = datetime.fromisoformat(row['decided_at'].replace('Z','+00:00'))
        require(stamp.tzinfo is not None, 'decision timestamp requires timezone')
    except (AttributeError, ValueError) as exc:
        raise ValueError('invalid decision timestamp') from exc


def preview_application(root, workspace, decision):
    """Read-only preflight. Pending application may be previewed but not applied."""
    root = Path(root).resolve()
    packet, draft, report = _candidate(root, workspace)
    schema = json.loads((Path(__file__).resolve().parents[1] / 'schemas/learning_synthesis_decision.schema.json').read_text())
    _shape(decision, schema)
    require(isinstance(decision, dict) and set(decision) == {
        'schema_version','topic_id','candidate_sha256','base_master_sha256','application','reviews','score_effect'}, 'invalid decision fields')
    require(decision['schema_version'] == 'learning-synthesis-decision-v1' and decision['score_effect'] == 'none', 'invalid decision contract')
    require(decision['topic_id'] == packet['topic_id'] and decision['candidate_sha256'] == report['draft_sha256'] and decision['base_master_sha256'] == packet['base_master_sha256'], 'decision targets another candidate or Master')
    application = decision['application']
    require(isinstance(application, dict) and set(application) == {'decision','actor','actor_type','decided_at'}, 'invalid application decision')
    require(application['decision'] in {'pending','approve','reject'}, 'invalid application status')
    require(application['actor_type'] in {'human', 'llm'}, 'invalid application actor type')
    if application['decision'] != 'pending':
        _identity(application)
    else:
        require(application['actor'] is None and application['decided_at'] is None, 'pending approval must not assert identity')
    targets = _review_targets(draft)
    require(isinstance(decision['reviews'], list), 'reviews must be a list')
    seen = set()
    for review in decision['reviews']:
        require(isinstance(review, dict) and set(review) == {'target','status','actor','actor_type','decided_at','note'}, 'invalid content review')
        key = review['target']
        require(isinstance(key,str) and key in targets and key not in seen, 'unknown or duplicate review target')
        seen.add(key)
        require(review['status'] in {'draft','llm_reviewed_human_pending','llm_verified','human_review_required','human_verified','rejected'}, 'invalid review status')
        require(review['actor_type'] in {'human','llm'} and isinstance(review['note'],str), 'invalid review metadata')
        if review['status'] == 'draft':
            require(review['actor'] is None and review['decided_at'] is None, 'draft must not assert a reviewer')
        else:
            _identity(review)
        if review['status'] == 'human_verified':
            require(review['actor_type'] == 'human', 'LLM cannot attest human verification')
        if review['status'] in {'llm_reviewed_human_pending', 'llm_verified'}:
            require(review['actor_type'] == 'llm', 'LLM review requires LLM identity')
        if review['status'] in {'llm_verified', 'human_review_required'}:
            require(bool(review['note'].strip()), 'review rationale required')
        targets[key]['review'] = dict(status=review['status'], reviewed_by=review['actor'],
            reviewed_at=review['decided_at'], note=review['note'])
    require(seen == set(targets), 'review targets incomplete')
    if application['actor_type'] == 'llm' and application['decision'] == 'approve':
        require(draft['learning_path']['review']['status'] in {'llm_verified', 'human_verified'}, 'LLM approval requires verified learning path')
        require(all(r['status'] != 'llm_reviewed_human_pending' for r in decision['reviews']),
                'classify uncertain content as human_review_required before LLM approval')
    topic = packet['topic_id']
    master_path = _file(root, f'master_topic_packs/{topic}.json')
    before = master_path.read_bytes()
    require(sha(before) == packet['base_master_sha256'], 'Master changed')
    master = json.loads(before)
    require('learning_synthesis' not in master, 'first-link only; existing synthesis update requires a new workflow')
    training = project_training(root, master)
    projected = project_synthesis(root, master, draft, training['source_materials'], training['curated_learning_materials'])
    require(all(s == 'matching' for s in projected['evidence_states'].values()), 'candidate evidence stale or unavailable')
    content_hash = sha(encoded(draft))
    target_path = f'data/topic_learning_synthesis/{topic}/{content_hash}.json'
    after = copy.deepcopy(master)
    after['learning_synthesis'] = dict(path=target_path, revision=draft['revision'], content_sha256=content_hash)
    after['revision'] += 1
    validate_master_topic_pack(after)
    require(project_grading(root, after) == project_grading(root, master), 'grading payload changed')
    can_apply = application['decision'] == 'approve' and bool(projected['eligible_section_ids'])
    return dict(topic_id=topic, can_apply=can_apply, status='ready' if can_apply else 'review_pending_or_rejected',
        base_master_sha256=sha(before), base_master_revision=master['revision'],
        candidate_sha256=report['draft_sha256'], decision_sha256=sha(encoded(decision)),
        before_master=master, after_master=after, reviewed_document=draft,
        human_review_targets=[r['target'] for r in decision['reviews'] if r['status'] in {'human_review_required', 'llm_reviewed_human_pending'}],
        eligible_section_ids=projected['eligible_section_ids'], score_effect='none')


def _write_once(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.is_symlink(), 'refusing symlink output')
    try:
        with path.open('xb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        require(path.read_bytes() == content, 'immutable output already differs')


def apply_application(root, workspace, decision, *, applied_by):
    """Use immutable artifacts then one atomic Master replacement as commit point.

    A prepared audit bundle can remain after failure. It is not an applied receipt:
    compare current Master bytes to master.after.json to determine commit state.
    """
    require(isinstance(applied_by,str) and bool(applied_by.strip()), 'applied_by required')
    root = Path(root).resolve()
    topic = decision.get('topic_id')
    require(isinstance(topic,str) and re.fullmatch('[a-z][a-z0-9]*(?:_[a-z0-9]+)+',topic), 'invalid topic')
    lock_path = _file(root, f'data/topic_learning_synthesis/{topic}/application.lock')
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open('a+b') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        preview = preview_application(root, workspace, decision)
        require(preview['can_apply'], 'explicit approval and eligible lessons required')
        artifact = _file(root, preview['after_master']['learning_synthesis']['path'])
        _write_once(artifact, encoded(preview['reviewed_document']))
        audit_id = sha(encoded({'decision':decision, 'applied_by':applied_by}))
        audit = _file(root, f'data/topic_learning_synthesis/{topic}/applications/{audit_id}')
        master_path = _file(root, f'master_topic_packs/{topic}.json')
        original = master_path.read_bytes()
        require(sha(original) == preview['base_master_sha256'], 'Master changed before preparation')
        _write_once(audit / 'master.before.json', original)
        _write_once(audit / 'master.after.json', encoded(preview['after_master']))
        _write_once(audit / 'decision.json', encoded(decision))
        metadata = dict(status='prepared', applied_by=applied_by, decision_sha256=preview['decision_sha256'],
                        candidate_sha256=preview['candidate_sha256'], commit_marker='Master matches master.after.json')
        receipt_path = audit / 'receipt.json'
        metadata['prepared_at'] = (json.loads(receipt_path.read_text())['prepared_at']
                                   if receipt_path.is_file() else datetime.now(timezone.utc).isoformat())
        _write_once(audit / 'receipt.json', encoded(metadata))
        # Recheck all inputs immediately before the only mutable replacement.
        require(preview_application(root,workspace,decision) == preview, 'preflight changed')
        fd, temporary = tempfile.mkstemp(prefix='.learning-apply-', dir=master_path.parent)
        try:
            with os.fdopen(fd,'wb') as stream:
                os.fchmod(stream.fileno(), master_path.stat().st_mode & 0o777)
                stream.write(encoded(preview['after_master']))
                stream.flush()
                os.fsync(stream.fileno())
            require(sha(master_path.read_bytes()) == preview['base_master_sha256'], 'Master changed before commit')
            os.replace(temporary, master_path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return dict(status='applied', topic_id=topic, master_revision=preview['after_master']['revision'],
                    audit_path=str(audit), score_effect='none')
