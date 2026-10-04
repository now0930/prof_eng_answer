"""Exact canonical requirement -> lesson navigation, with no scoring authority."""
import copy

from .learning_synthesis import require


def canonical_record(doc, key, record_id):
    """Use known source collections and IDs, not recursive string matching."""
    rows = []
    fields = {'fact_anchor': ['anchors', 'core_facts'],
              'logic_check': ['deterministic_checks'],
              'model_answer': ['expected_question_patterns', 'question_patterns'],
              'topic_importance': [], 'question_demand_axes': ['requirements']}
    for field in fields[key]:
        value = doc.get(field, [])
        if isinstance(value, list):
            rows.extend(value)
        elif key == 'logic_check' and isinstance(value, dict):
            for group in ('fatal_checks', 'major_checks', 'question_type_checks'):
                rows.extend(value.get(group, []))
    matches = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ids = [row[k] for k in ('id', 'anchor_id', 'rule_id', 'requirement_id') if k in row]
        if record_id in ids:
            require(len(set(ids)) == 1, 'ambiguous canonical ID aliases')
            matches.append(row)
    require(len(matches) == 1, 'unsupported or ambiguous canonical record ID')
    return matches[0]


def navigation_view(root, master, materials, aids):
    from .learning_synthesis import synthesis_for_training
    import json
    from pathlib import Path
    result = synthesis_for_training(root, master, materials, aids)
    if result is None:
        return None
    output = dict(status=result['status'], topic_id=master['topic_id'],
                  master_revision=master['revision'], targets=[], score_effect='none')
    if result['status'] != 'loaded':
        return output
    doc = result['document']
    output['synthesis_revision'] = doc['revision']
    sections = {s['section_id']: s for s in doc['learning_path']['sections']}
    for link in doc['grading_links']:
        # Knowledge correctness and mapping correctness are separate approvals.
        if link['review']['status'] != 'human_verified':
            continue
        target = link['target']
        if target['source_key'] != 'question_demand_axes':
            continue  # Other result ID namespaces require an explicit consumer.
        source_file = master['legacy_topic_pack']['source_files'][target['source_key']]
        canonical = json.loads((Path(root) / source_file).read_text(encoding='utf-8'))
        record = canonical_record(canonical, target['source_key'], target['record_id'])
        lessons = [{'section_id': sid, 'title': sections[sid]['title']}
                   for sid in link['section_ids'] if sid in result['eligible_section_ids']]
        if lessons:
            output['targets'].append(dict(target=copy.deepcopy(target), source_file=source_file,
                requirement_text=record.get('requirement_text'), knowledge_ids=list(link['knowledge_ids']),
                lessons=lessons))
    return output


def feedback_navigation(grade, navigation):
    """Consume final ledger + exact question-contract provenance. Never infer IDs."""
    if not navigation or navigation.get('status') != 'loaded':
        return None
    topic = grade.get('topic_id') or grade.get('inferred_topic_id')
    if navigation.get('topic_id') != topic or navigation.get('score_effect') != 'none':
        return None
    contract = grade.get('question_demand_contract') or {}
    ledger = grade.get('canonical_evaluation_ledger') or {}
    requirements = contract.get('requirements', []) if isinstance(contract, dict) else []
    rows = ledger.get('rows', []) if isinstance(ledger, dict) else []
    recommendations = []
    for target in navigation['targets']:
        rid = target['target']['record_id']
        definitions = [r for r in requirements if isinstance(r, dict) and r.get('requirement_id') == rid]
        matches = [r for r in rows if isinstance(r, dict) and r.get('requirement_id') == rid]
        if len(definitions) != 1 or len(matches) != 1:
            continue
        definition, row = definitions[0], matches[0]
        if (definition.get('source') != 'topic_pack_question_demand_axes'
                or definition.get('topic_id') != topic
                or definition.get('source_file') != target['source_file']
                or definition.get('requirement_text') != target['requirement_text']
                or row.get('requirement_text') != target['requirement_text']
                or row.get('status') not in {'missing', 'partial', 'incorrect'}):
            continue
        recommendations.append(dict(requirement_id=rid, status=row['status'],
            knowledge_ids=copy.deepcopy(target['knowledge_ids']),
            lessons=copy.deepcopy(target['lessons'])))
    return dict(topic_id=topic, master_revision=navigation['master_revision'],
                synthesis_revision=navigation['synthesis_revision'],
                recommendations=recommendations, score_effect='none')
