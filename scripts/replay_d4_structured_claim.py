"""Replay existing manual annotations; does not generate or certify LLM claims."""
import argparse
import csv
import hashlib
import json
import os
import uuid
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.d4_structured_claim import SCHEMA, assess_proposal, evaluate_against_registry


def digest(data):
    return hashlib.sha256(data).hexdigest()


def proposal_from_row(row):
    answer = row['answer_text']
    assert digest(answer.encode()) == row['input_sha256']
    span = {'start': 0, 'end': len(answer), 'text': answer}
    fields = {}
    for name in ('stance', 'scope', 'homogeneous', 'isothermal', 'outcome'):
        cue = row[name + '_evidence']
        fields[name] = {'value': row[name + '_reaudit'], 'evidence': [
            {'start': int(row[name + '_start']), 'end': int(row[name + '_end']), 'text': cue}
        ] if cue else []}
    # Previous audit labels causal binding manually; full sentence is coarse evidence.
    # This is not a verified causal span or a new extraction result.
    linked = row['manual_causal_binding'] == 'INSERTION_EFFECT'
    fields['causal_binding'] = {'value': 'INSERTION_EFFECT' if linked else 'UNKNOWN',
                                'evidence': [span.copy()] if linked else []}
    return {'schema': SCHEMA, 'answer_sha256': row['input_sha256'],
            'claims': [{'span': span, 'fields': fields}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--prior-manifest', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    original = args.input.read_bytes()
    prior = json.loads(args.prior_manifest.read_text())
    if digest(original) != prior['output_sha256']:
        raise ValueError('audit input hash mismatch')
    rows = list(csv.DictReader(args.input.open(encoding='utf-8-sig', newline='')))
    if len(rows) != 48 or len({r['case_id'] for r in rows}) != 48:
        raise ValueError('expected 48 distinct cases')
    output = []
    for row in rows:
        proposal = proposal_from_row(row)
        answer = row['answer_text']
        assessment = assess_proposal(answer, proposal)
        bound = evaluate_against_registry(answer, proposal)
        assert all(r['score_admission'] == 'DISABLED' and r['score_effect'] == 'none' for r in (assessment, bound))
        output.append({'case_id': row['case_id'], 'input_sha256': row['input_sha256'],
                       'previous_manual_candidate': row['new_research_candidate'],
                       'literal_structure': assessment['structure_status'],
                       'conditional_candidate': assessment['conditional_candidate'],
                       'reason': assessment['reason'],
                       'condition_comparison': assessment.get('condition_comparison', 'UNRESOLVED'),
                       'source_binding': bound['source_binding'], 'registry_bound_status': bound['status'],
                       'source_match_proven': False, 'accuracy_status': 'NOT_ESTABLISHED',
                       'score_admission': 'DISABLED', 'score_effect': 'none'})
    args.output_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    run = args.output_root / uuid.uuid4().hex
    run.mkdir(mode=0o700)
    content = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2).encode()
    manifest = {'schema': SCHEMA, 'input_sha256': digest(original), 'prior_head': prior['head'],
                'prior_manifest_sha256': digest(args.prior_manifest.read_bytes()),
                'validator_sha256': digest((ROOT / 'grading/evidence/d4_structured_claim.py').read_bytes()),
                'runner_sha256': digest(Path(__file__).read_bytes()),
                'result_sha256': digest(content), 'case_count': len(output),
                'conditional_counts': dict(Counter(r['conditional_candidate'] for r in output)),
                'bound_counts': dict(Counter(r['registry_bound_status'] for r in output)),
                'binding_counts': dict(Counter(r['source_binding'] for r in output)),
                'reason_counts': dict(Counter(r['reason'] for r in output)),
                'accuracy_status': 'NOT_ESTABLISHED', 'score_admission': 'DISABLED', 'score_effect': 'none',
                'method': 'Existing ChatGPT manual annotations; not automatic LLM extraction. No raw text retained.'}
    for name, data in [('results.json', content), ('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())]:
        fd = os.open(run / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
    print(json.dumps({'run': str(run), **manifest}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
