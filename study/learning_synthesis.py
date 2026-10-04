"""Read-only, score-neutral synthesis validation. No content promotion."""
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


class SynthesisError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise SynthesisError(message)


def _shape(value, schema, path='$'):
    """Evaluate only the keywords used by our bundled schema; fail on new ones."""
    supported = {'$schema', 'type', 'required', 'properties', 'additionalProperties',
                 'items', 'minItems', 'uniqueItems', 'enum', 'const', 'pattern',
                 'minimum', 'minLength'}
    require(set(schema) <= supported, 'unsupported schema keyword')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'null': type(None)}
    if 'type' in schema:
        kinds = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        require(any(type(value) is types[k] for k in kinds), f'{path}: type')
    if 'const' in schema:
        require(value == schema['const'], f'{path}: const')
    if 'enum' in schema:
        require(value in schema['enum'], f'{path}: enum')
    if isinstance(value, dict):
        require(set(schema.get('required', [])) <= set(value), f'{path}: missing fields')
        if schema.get('additionalProperties') is False:
            require(set(value) <= set(schema['properties']), f'{path}: unknown fields')
        for key, item in value.items():
            _shape(item, schema['properties'][key], f'{path}.{key}')
    if isinstance(value, list):
        require(len(value) >= schema.get('minItems', 0), f'{path}: minItems')
        if schema.get('uniqueItems'):
            require(len({json.dumps(x, sort_keys=True) for x in value}) == len(value), f'{path}: duplicate')
        for item in value:
            _shape(item, schema['items'], path + '[]')
    if isinstance(value, str):
        require(len(value) >= schema.get('minLength', 0), f'{path}: minLength')
        if 'pattern' in schema:
            require(re.search(schema['pattern'], value) is not None, f'{path}: pattern')
    if 'minimum' in schema:
        require(value >= schema['minimum'], f'{path}: minimum')


def _index(rows, field):
    result = {row[field]: row for row in rows}
    require(len(result) == len(rows), f'duplicate {field}')
    return result


def validate_synthesis(payload):
    schema = json.loads((Path(__file__).resolve().parents[1] / 'schemas/topic_learning_synthesis.schema.json').read_text())
    _shape(payload, schema)
    evidence = _index(payload['evidence'], 'evidence_id')
    knowledge = _index(payload['knowledge'], 'knowledge_id')
    sections = _index(payload['learning_path']['sections'], 'section_id')
    for group, field in [('relations', 'relation_id'), ('conflicts', 'conflict_id'), ('grading_links', 'link_id')]:
        _index(payload[group], field)

    def check(item):
        if isinstance(item, dict):
            for key, index in [('evidence_ids', evidence), ('knowledge_ids', knowledge), ('section_ids', sections)]:
                if key in item:
                    require(set(item[key]) <= set(index), f'unknown {key}')
            if 'review' in item:
                review = item['review']
                if review['status'] != 'draft':
                    require(bool(review['reviewed_by'] and review['reviewed_by'].strip()), 'review identity required')
                    try:
                        stamp = datetime.fromisoformat(review['reviewed_at'].replace('Z', '+00:00'))
                        require(stamp.tzinfo is not None, 'review timezone required')
                    except (ValueError, AttributeError) as exc:
                        raise SynthesisError('invalid review timestamp') from exc
            for value in item.values():
                check(value)
        elif isinstance(item, list):
            for value in item:
                check(value)
    check(payload)
    for conflict in payload['conflicts']:
        if conflict['status'] == 'resolved':
            require(bool(conflict['resolution'] and conflict['resolution'].strip()) and conflict['review']['status'] == 'human_verified', 'unreviewed conflict resolution')
        else:
            require(conflict['resolution'] is None, 'unresolved conflict has resolution')
    for item in [*knowledge.values(), *sections.values()]:
        if item['origin'] == 'source_excerpt':
            text = item.get('statement', item.get('body'))
            require(any(text == evidence[e]['excerpt'] for e in item['evidence_ids']), 'source_excerpt differs from evidence')
    graph = {key: [] for key in knowledge}
    positions = {}
    for i, section in enumerate(sections.values()):
        for key in section['knowledge_ids']:
            positions.setdefault(key, i)
    for relation in payload['relations']:
        a, b = relation['from_id'], relation['to_id']
        require(a in knowledge and b in knowledge, 'unknown relation endpoint')
        if relation['kind'] == 'prerequisite':
            graph[a].append(b)
            if b in positions:
                require(a in positions and positions[a] <= positions[b], 'prerequisite order')
    # Kahn traversal avoids recursion limits on large authored graphs.
    degree = dict.fromkeys(graph, 0)
    for children in graph.values():
        for child in children:
            degree[child] += 1
    ready = [key for key, count in degree.items() if count == 0]
    visited = 0
    while ready:
        key = ready.pop()
        visited += 1
        for child in graph[key]:
            degree[child] -= 1
            if degree[child] == 0:
                ready.append(child)
    require(visited == len(graph), 'prerequisite cycle')
    return copy.deepcopy(payload)


def validate_reference(ref):
    require(isinstance(ref, dict) and set(ref) == {'path', 'revision', 'content_sha256'}, 'invalid synthesis reference')
    path = ref['path']
    require(isinstance(path, str) and path.endswith('.json') and not path.startswith('/') and '\\' not in path and all(p not in {'', '.', '..'} for p in path.split('/')), 'unsafe synthesis path')
    require(type(ref['revision']) is int and ref['revision'] >= 1, 'invalid synthesis revision')
    require(isinstance(ref['content_sha256'], str) and re.fullmatch('[a-f0-9]{64}', ref['content_sha256']) is not None, 'invalid synthesis hash')


def _read(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root), 'path escapes repository')
    return path.read_bytes()


def load_synthesis(root, master, source_materials, learning_materials):
    """Return full review data and eligible section IDs; never write files."""
    ref = master.get('learning_synthesis')
    if ref is None:
        return None
    validate_reference(ref)
    root = Path(root).resolve()
    raw = _read(root, ref['path'])
    require(hashlib.sha256(raw).hexdigest() == ref['content_sha256'], 'synthesis file hash mismatch')
    payload = validate_synthesis(json.loads(raw))
    require(payload['topic_id'] == master['topic_id'] and payload['revision'] == ref['revision'], 'synthesis identity mismatch')
    sources = {s['source_id']: s for s in master['sources']}
    materials = _index(source_materials, 'source_id')
    aids = _index(learning_materials, 'material_id')
    states = {}
    for e in payload['evidence']:
        source = sources.get(e['source_id'])
        require(source is not None, 'unlinked source')
        material = materials.get(e['source_id'])
        expected_url = source.get('source_url', source['wordpress_url'])
        state = 'matching'
        if type(e['source_version']) is not type(source['version']) or e['source_version'] != source['version'] or e['source_url'] != expected_url or source['verification_status'] == 'stale':
            state = 'stale'
        elif material is None or source['verification_status'] == 'unavailable':
            state = 'unavailable'
        elif (material.get('version') != e['source_version'] or material.get('source_url') != e['source_url'] or hashlib.sha256(material['text'].encode('utf-8')).hexdigest() != e['source_content_sha256'] or e['excerpt'] not in material['text']):
            state = 'stale'
        states[e['evidence_id']] = state
    for link in payload['grading_links']:
        target = link['target']
        relative = master['legacy_topic_pack']['source_files'].get(target['source_key'])
        require(relative is not None, 'missing canonical source')
        canonical = _read(root, relative)
        require(hashlib.sha256(canonical).hexdigest() == target['source_content_sha256'], 'canonical hash mismatch')
        doc = json.loads(canonical)
        require(doc.get('topic_id') == master['topic_id'], 'canonical topic mismatch')
        from .learning_feedback import canonical_record
        canonical_record(doc, target['source_key'], target['record_id'])
    blocked = {k['knowledge_id'] for k in payload['knowledge'] if k['review']['status'] in {'draft', 'rejected'} or any(states[e] != 'matching' for e in k['evidence_ids'])}
    for conflict in payload['conflicts']:
        if conflict['status'] == 'unresolved':
            blocked.update(conflict['knowledge_ids'])
    for relation in payload['relations']:
        if relation['review']['status'] in {'draft', 'rejected'} or any(states[e] != 'matching' for e in relation['evidence_ids']):
            blocked.update([relation['from_id'], relation['to_id']])
    # A dependent concept is unavailable if its prerequisite is unavailable.
    changed = True
    while changed:
        before = len(blocked)
        for relation in payload['relations']:
            if relation['kind'] == 'prerequisite' and relation['from_id'] in blocked:
                blocked.add(relation['to_id'])
        changed = len(blocked) != before
    eligible = []
    for section in payload['learning_path']['sections']:
        require(set(section['material_ids']) <= set(aids), 'unknown learning material')
        if not (set(section['knowledge_ids']) & blocked) and all(states[e] == 'matching' for e in section['evidence_ids']) and payload['learning_path']['review']['status'] not in {'draft', 'rejected'}:
            eligible.append(section['section_id'])
    return {'status': 'loaded', 'master_revision': master['revision'], 'document': payload, 'evidence_states': states,
            'eligible_section_ids': eligible, 'score_effect': 'none'}


def synthesis_for_training(root, master, source_materials, learning_materials):
    """Optional material failures remain explicit and do not abort old views."""
    try:
        return load_synthesis(root, master, source_materials, learning_materials)
    except (SynthesisError, OSError, ValueError) as exc:
        return {'status': 'unavailable', 'error': str(exc), 'eligible_section_ids': [], 'score_effect': 'none'}
