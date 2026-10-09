"""Explicit canonical requirement selection; never infer or approve a mapping."""
import copy
import hashlib
import json
from pathlib import Path

from .learning_feedback import canonical_record
from .learning_synthesis import require, validate_synthesis


def mapping_targets(root, master):
    root = Path(root).resolve()
    relative = master['legacy_topic_pack']['source_files'].get('question_demand_axes')
    if relative is None:
        return []
    path = (root / relative).resolve()
    require(path.is_relative_to(root), 'canonical path escapes repository')
    content = path.read_bytes()
    doc = json.loads(content)
    require(doc.get('topic_id') == master['topic_id'], 'canonical topic mismatch')
    require(isinstance(doc.get('requirements'), list), 'canonical requirements missing')
    targets = []
    for row in doc['requirements']:
        require(isinstance(row, dict), 'invalid canonical requirement')
        rid = row.get('requirement_id')
        require(isinstance(rid, str) and bool(rid.strip()), 'canonical requirement ID missing')
        canonical_record(doc, 'question_demand_axes', rid)
        text = row.get('requirement_text')
        require(isinstance(text, str) and bool(text.strip()), 'canonical requirement text missing')
        targets.append(dict(requirement_text=text, source_file=relative,
            target=dict(source_key='question_demand_axes', record_id=rid,
                        source_content_sha256=hashlib.sha256(content).hexdigest())))
    return targets


def add_mapping(packet, authored, *, link_id, requirement_id, knowledge_ids, section_ids):
    """Return a separate draft, retaining originals and resetting new-link review."""
    doc = validate_synthesis(authored)
    require(doc['topic_id'] == packet['topic_id'], 'mapping topic mismatch')
    require(isinstance(link_id, str) and bool(link_id.strip()), 'link ID required')
    require(link_id not in {r['link_id'] for r in doc['grading_links']}, 'link ID already exists')
    matches = [r for r in packet.get('mapping_targets', []) if r['target']['record_id'] == requirement_id]
    require(len(matches) == 1, 'select one prepared canonical requirement')
    require(bool(knowledge_ids) and bool(section_ids), 'knowledge and sections required')
    sections = {r['section_id']: r for r in doc['learning_path']['sections']}
    require(set(section_ids) <= set(sections), 'unknown section IDs')
    linked_knowledge = {k for sid in section_ids for k in sections[sid]['knowledge_ids']}
    require(set(knowledge_ids) <= linked_knowledge, 'selected lessons must reference mapped knowledge')
    doc['grading_links'].append(dict(link_id=link_id, target=copy.deepcopy(matches[0]['target']),
        knowledge_ids=list(knowledge_ids), section_ids=list(section_ids),
        review=dict(status='draft', reviewed_by=None, reviewed_at=None,
                    note='Explicit mapping candidate; separate human review required.')))
    return validate_synthesis(doc)
