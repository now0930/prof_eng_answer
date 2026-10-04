#!/usr/bin/env python3
"""Private evidence export and draft compilation; no apply or model API call."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from study.synthesis_authoring import (
    AUTHOR_INSTRUCTIONS, build_candidate, encoded, prepare_sources, write_new_bundle,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'build'])
    parser.add_argument('--topic-id', required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--authored', type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.run_id):
        parser.error('run-id must contain only ASCII letters, numbers, underscore or hyphen')
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)+', args.topic_id):
        parser.error('invalid topic-id')
    workspace = ROOT / 'data/topic_learning_authoring' / args.topic_id / args.run_id
    if not workspace.resolve().is_relative_to((ROOT / 'data/topic_learning_authoring').resolve()):
        parser.error('unsafe workspace path')
    try:
        if args.action == 'prepare':
            packet = prepare_sources(ROOT, args.topic_id)
            write_new_bundle(workspace, {
                'sources.json': encoded(packet),
                'AUTHOR_INSTRUCTIONS.md': AUTHOR_INSTRUCTIONS.encode('utf-8'),
                'synthesis.schema.json': (ROOT / 'schemas/topic_learning_synthesis.schema.json').read_bytes(),
            })
            print(f'PREPARE=PASS SOURCES={len(packet["sources"])} OUTPUT={workspace}')
        else:
            if args.authored is None:
                parser.error('--authored is required for build')
            packet = json.loads((workspace / 'sources.json').read_text(encoding='utf-8'))
            if packet.get('topic_id') != args.topic_id:
                parser.error('packet topic mismatch')
            authored = json.loads(args.authored.read_text(encoding='utf-8'))
            draft, report = build_candidate(ROOT, packet, authored)
            write_new_bundle(workspace / 'candidate', {
                'draft.json': encoded(draft), 'report.json': encoded(report),
                'authored.json': encoded(authored),
            })
            print(f'BUILD=PASS REVIEW=pending OUTPUT={workspace / "candidate"}')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'{args.action.upper()}=FAIL {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
