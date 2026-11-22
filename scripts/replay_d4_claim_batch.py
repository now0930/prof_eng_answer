#!/usr/bin/env python3
"""Replay caller-provided ChatGPT Claim proposals; research only, no scores."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.d4_common_relation import REGISTRY_SHA, _unique, evaluate_claim_batch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path, help='private answer and proposed Claim batch')
    parser.add_argument('--output', required=True, type=Path, help='new private result file')
    args = parser.parse_args()
    raw = args.input.read_bytes()
    if len(raw) > 2_000_000:
        raise ValueError('input too large')
    payload = json.loads(raw, object_pairs_hook=_unique)
    if not isinstance(payload, dict) or set(payload) != {'answer', 'proposals'}:
        raise ValueError('invalid batch envelope')
    result = evaluate_claim_batch(payload['answer'], payload['proposals'])
    if result['status'] == 'REJECTED_INPUT':
        raise ValueError(result['reason'])
    result['metadata'] = {
        'input_sha256': hashlib.sha256(raw).hexdigest(),
        'registry_sha256_expected': REGISTRY_SHA,
        'code_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'command': 'replay_d4_claim_batch.py --input <private> --output <private>',
        'research_only': True,
    }
    content = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2).encode()
    fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(content)
    print('output_sha256=' + hashlib.sha256(content).hexdigest())


if __name__ == '__main__':
    main()
