#!/usr/bin/env python3
"""Private authoring, review preview and versioned learning application."""
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
from study.synthesis_application import decision_template, preview_application, apply_application


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'add-mapping', 'build', 'review-template', 'preview', 'apply'])
    parser.add_argument('--topic-id', required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--authored', type=Path)
    parser.add_argument('--decision', type=Path)
    parser.add_argument('--applied-by')
    parser.add_argument('--include-mapping-targets', action='store_true')
    parser.add_argument('--link-id')
    parser.add_argument('--requirement-id')
    parser.add_argument('--knowledge-id', action='append', default=[])
    parser.add_argument('--section-id', action='append', default=[])
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
            packet = prepare_sources(ROOT, args.topic_id, include_mapping_targets=args.include_mapping_targets)
            write_new_bundle(workspace, {
                'sources.json': encoded(packet),
                'AUTHOR_INSTRUCTIONS.md': AUTHOR_INSTRUCTIONS.encode('utf-8'),
                'synthesis.schema.json': (ROOT / 'schemas/topic_learning_synthesis.schema.json').read_bytes(),
            })
            print(f'PREPARE=PASS SOURCES={len(packet["sources"])} OUTPUT={workspace}')
        elif args.action == 'add-mapping':
            from study.synthesis_mapping import add_mapping
            if args.authored is None:
                parser.error('--authored is required')
            packet = json.loads((workspace / 'sources.json').read_text(encoding='utf-8'))
            if packet.get('topic_id') != args.topic_id:
                parser.error('packet topic mismatch')
            authored = json.loads(args.authored.read_text(encoding='utf-8'))
            mapped = add_mapping(packet, authored, link_id=args.link_id,
                requirement_id=args.requirement_id, knowledge_ids=args.knowledge_id, section_ids=args.section_id)
            build_candidate(ROOT, packet, mapped)
            output = workspace / 'authored.mapping.json'
            with output.open('xb') as stream:
                stream.write(encoded(mapped))
            print(f'MAPPING_DRAFT=PASS REVIEW=pending OUTPUT={output}')
        elif args.action == 'build':
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
        elif args.action == 'review-template':
            template = decision_template(ROOT, workspace)
            output = workspace / 'decision.template.json'
            with output.open('xb') as stream:
                stream.write(encoded(template))
            print(f'REVIEW_TEMPLATE=PASS OUTPUT={output}')
        else:
            if args.decision is None:
                parser.error('--decision is required')
            decision = json.loads(args.decision.read_text(encoding='utf-8'))
            if decision.get('topic_id') != args.topic_id:
                parser.error('decision topic mismatch')
            if args.action == 'preview':
                preview = preview_application(ROOT, workspace, decision)
                print(json.dumps({key:preview[key] for key in (
                    'topic_id','can_apply','status','base_master_sha256','base_master_revision',
                    'candidate_sha256','decision_sha256','eligible_section_ids','human_review_targets','mapping_changes','score_effect')}, ensure_ascii=False))
            else:
                result = apply_application(ROOT, workspace, decision, applied_by=args.applied_by)
                print(json.dumps(result, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'{args.action.upper()}=FAIL {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
