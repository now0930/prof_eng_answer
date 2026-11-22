"""Build a private blind expert packet; no judgments or scoring authority.

Inputs are sensitive. Outputs must be in a new directory outside the repository.
"""
import argparse
import hashlib
import json
import os
import secrets
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from grading.evidence.d4_common_relation import REGISTRY_PATH, REGISTRY_SHA
from scripts.replay_d4_common_relation import _claim_review_source_matches


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_private(path, data):
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')


def build(answers_path, review_path, proposals_path, replay_path, output):
    root = Path(__file__).resolve().parents[1]
    output = output.resolve()
    if output == root or root in output.parents:
        raise ValueError('private output must be outside repository')
    raw = answers_path.read_bytes()
    review_raw = review_path.read_bytes()
    proposal_raw = proposals_path.read_bytes()
    replay_raw = replay_path.read_bytes()
    registry_raw = REGISTRY_PATH.read_bytes()
    if digest(registry_raw) != REGISTRY_SHA:
        raise ValueError('registry hash mismatch')
    answers, review, proposals, replay, registry = map(json.loads, (raw, review_raw, proposal_raw, replay_raw, registry_raw))
    if review['input_sha256'] != digest(raw) or proposals['input_sha256'] != digest(raw) or proposals['review_sha256'] != digest(review_raw):
        raise ValueError('input provenance mismatch')
    if (replay['input_sha256'], replay['review_sha256'], replay['proposals_sha256']) != (digest(raw), digest(review_raw), digest(proposal_raw)):
        raise ValueError('replay provenance mismatch')
    cases = {x['case_id']: x for x in answers['cases']}
    rows = {x['claim_id']: x for x in review['rows']}
    props = {x['claim_id']: x for x in proposals['proposals']}
    results = {x['claim_id']: x for x in replay['rows']}
    facts = {x['fact_id']: x for x in registry['facts']}
    if (len(cases), len(rows), len(props), len(results), len(facts)) != (9, 55, 55, 55, len(registry['facts'])) or set(rows) != set(props) or set(rows) != set(results):
        raise ValueError('missing or duplicated input records')
    if len({x['fact_id'] for x in rows.values()}) != 26:
        raise ValueError('unexpected fact count')
    for cid, row in rows.items():
        case, prop, result = cases[row['case_id']], props[cid], results[cid]
        text = case['answer']
        if digest(text.encode()) != row['input_sha256'] or text[row['start']:row['end']] != row['evidence']:
            raise ValueError('answer span mismatch')
        if (prop['case_id'], prop['fact_id']) != (row['case_id'], row['fact_id']) or (result['case_id'], result['fact_id']) != (row['case_id'], row['fact_id']):
            raise ValueError('mapping mismatch')
        if not _claim_review_source_matches(text, row, prop['claim']):
            raise ValueError('proposal evidence mismatch')
    selected = [r for r in replay['rows'] if r['reason'] == 'SCOPE_UNRESOLVED' or r['component_candidate'] in ('SUPPORT_CANDIDATE', 'CONTRADICT_CANDIDATE')]
    if len(selected) != 23 or sum(r['reason'] == 'SCOPE_UNRESOLVED' for r in selected) != 17 or sum(r['component_candidate'] == 'SUPPORT_CANDIDATE' for r in selected) != 3 or sum(r['component_candidate'] == 'CONTRADICT_CANDIDATE' for r in selected) != 3:
        raise ValueError('unexpected selected cohort')
    ids = [secrets.token_hex(12) for _ in selected]
    if len(set(ids)) != len(ids):
        raise ValueError('case ID collision')
    packet, mapping, forms = [], [], []
    for blind_id, result in zip(ids, selected):
        row = rows[result['claim_id']]; case = cases[row['case_id']]; fact = facts[row['fact_id']]
        if fact['verification_status'] != 'verified' or fact['review_status'] != 'approved':
            raise ValueError('registry record not verified and approved')
        packet.append(dict(case_id=blind_id, question=case['question'], answer=case['answer'], answer_sha256=digest(case['answer'].encode()), claim_evidence=dict(start=row['start'], end=row['end'], text=row['evidence']), fact=dict(fact_id=fact['fact_id'], topic_id=fact['topic_id'], statement=fact['statement'], relation=fact['relation'], source_refs=fact['source_refs'], verification_refs=fact['verification_refs'])))
        mapping.append(dict(case_id=blind_id, original_case_id=row['case_id'], claim_id=row['claim_id'], fact_id=row['fact_id'], selection_reason=result['reason'], candidate=result['component_candidate']))
        forms.append(dict(case_id=blind_id, relation_judgment=None, scope_judgment=None, reviewer_identity=None, reviewer_evidence=None, status='PENDING'))
    secrets.SystemRandom().shuffle(packet)
    secrets.SystemRandom().shuffle(forms)
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    common = dict(review_status='PENDING', independent_accuracy='NOT_ESTABLISHED', score_admission='DISABLED', score_effect='none')
    write_private(output / 'blind_packet.json', dict(schema='d4_wrong19_blind.v1', instructions='Judge the specific evidence in its full answer context against the fact. Record relation and scope separately. Do not infer independent samples from repeated answers.', cases=packet, **common))
    write_private(output / 'review_results_template.json', dict(schema='d4_wrong19_review.v1', allowed_relation=['SUPPORT','CONTRADICT','UNRESOLVED'], allowed_scope=['IN_SCOPE','OUT_OF_SCOPE','UNRESOLVED'], reviews=forms, **common))
    grouped = {}
    for item in mapping:
        grouped.setdefault(item['original_case_id'], []).append(item['case_id'])
    same_answer_groups = [ids for ids in grouped.values() if len(ids) > 1]
    damping_ids = {'ACTUAL-DAMP-002-C02', 'ACTUAL-DAMP-002-C03', 'ACTUAL-DAMP-002-C04'}
    possible_common_cause = [item['case_id'] for item in mapping if item['claim_id'] in damping_ids]
    write_private(output / 'private_mapping.json', dict(schema='d4_wrong19_mapping.v1', mappings=mapping, same_answer_groups=same_answer_groups, possible_common_cause=dict(case_ids=possible_common_cause, status='PENDING'), **common))
    write_private(output / 'manifest.json', dict(schema='d4_wrong19_manifest.v1', input_sha256=digest(raw), review_sha256=digest(review_raw), proposals_sha256=digest(proposal_raw), replay_sha256=digest(replay_raw), registry_sha256=digest(registry_raw), outputs={name:digest((output/name).read_bytes()) for name in ('blind_packet.json','review_results_template.json','private_mapping.json')}, cases=23, **common))
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('answers', 'review', 'proposals', 'replay', 'output'):
        p.add_argument('--'+name, required=True, type=Path)
    a = p.parse_args()
    build(a.answers, a.review, a.proposals, a.replay, a.output)
    print('PRIVATE_PACKET_CREATED cases=23 reviews=PENDING')


if __name__ == '__main__':
    main()
