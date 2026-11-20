#!/usr/bin/env python3
"""Private, non-overwriting D4 research replay; output has no answer text."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.d4_relation_research import REGISTRY, diagnose_surface
from grading.evidence.d4_wrong_shadow_probe import extract_d4_shadow_candidates


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output-root', required=True, type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    if not isinstance(data, list) or any(not isinstance(x, dict) or not all(isinstance(x.get(k), str) for k in ('case_id', 'family', 'answer_text')) for x in data):
        raise ValueError('input must be a list of case_id, family, answer_text objects')
    if len({x['case_id'] for x in data}) != len(data):
        raise ValueError('duplicate case IDs')
    root = args.output_root.resolve()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    run = root / uuid.uuid4().hex
    run.mkdir(mode=0o700)  # exclusive; never reuses a previous run
    rows = []
    for case in data:
        diagnosis = diagnose_surface(case['answer_text'], case['family'])
        extraction = extract_d4_shadow_candidates(case['answer_text'])
        candidates = [r for r in extraction['candidates'] if r['relation_family'] == case['family']]
        rows.append({'case_id': case['case_id'], 'family': case['family'],
                     'input_sha256': sha(case['answer_text'].encode()), 'diagnosis': diagnosis,
                     'relations': [r['surface_relation'] for r in candidates],
                     'contexts': [r['assertion_context'] for r in candidates]})
    result = json.dumps(rows, ensure_ascii=False, sort_keys=True, indent=2).encode()
    source = ROOT / 'grading/evidence/d4_relation_research.py'
    probe = ROOT / 'grading/evidence/d4_wrong_shadow_probe.py'
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain', '--', str(source), str(probe)], cwd=ROOT, text=True).strip())
    manifest = {'schema': 'd4_replay.v1', 'input_sha256': sha(raw), 'commit': head,
                'research_code_dirty': dirty, 'research_code_sha256': sha(source.read_bytes()),
                'probe_code_sha256': sha(probe.read_bytes()), 'registry_sha256': sha(REGISTRY.read_bytes()),
                'contract_version': 'd4_relation_research.v1', 'command': 'evaluate_d4_relation_research.py --input <private> --output-root <private>',
                'options': {'private_input': True}, 'result_sha256': sha(result), 'case_count': len(rows),
                'score_admission': 'DISABLED', 'score_effect': 'none'}
    for name, content in [('results.json', result), ('manifest.json', json.dumps(manifest, indent=2, sort_keys=True).encode())]:
        fd = os.open(run / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(content)
    print(f'run={run} cases={len(rows)} sha256={manifest["result_sha256"]}')


if __name__ == '__main__':
    main()
