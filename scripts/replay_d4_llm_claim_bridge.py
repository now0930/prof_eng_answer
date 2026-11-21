"""Replay captured answer-only LLM responses; no live network/provider invocation."""
import argparse
import csv
import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from grading.evidence.d4_llm_claim_bridge import digest, evaluate_extraction, read_json, build_prompt


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',required=True,type=Path)
    ap.add_argument('--responses',required=True,type=Path)
    ap.add_argument('--output-root',required=True,type=Path)
    ap.add_argument('--verified-export',type=Path)
    ap.add_argument('--registry',type=Path)
    args=ap.parse_args()
    if args.verified_export and args.registry:
        ap.error('select one source mode')
    rows=list(csv.DictReader(args.input.open(encoding='utf-8-sig',newline='')))
    ids=[r['case_id'] for r in rows]
    records=[read_json(line) for line in args.responses.read_text().splitlines() if line.strip()]
    by_id={r['case_id']:r for r in records}
    if len(set(ids))!=len(ids) or len(by_id)!=len(records) or set(ids)!=set(by_id):
        raise ValueError('case ID set mismatch')
    opts={}
    if args.verified_export: opts['export_path']=args.verified_export
    if args.registry: opts['registry_path']=args.registry
    results=[]
    for row in rows:
        case_id,answer=row['case_id'],row['text']
        response=by_id[case_id]
        input_sha=digest(answer.encode())
        if input_sha!=response['answer_sha256']:
            raise ValueError('answer hash mismatch '+case_id)
        raw=response['response_json']
        result=evaluate_extraction(answer,raw,**opts)
        if result['score_admission']!='DISABLED' or result['score_effect']!='none' or result['status']!='UNRESOLVED':
            raise RuntimeError('research-only boundary violated')
        results.append({'case_id':case_id,'answer_sha256':input_sha,'prompt_sha256':digest(build_prompt(answer).encode()),
                        'response_sha256':digest(raw.encode()),**result})
    args.output_root.mkdir(mode=0o700,parents=True,exist_ok=True)
    run=args.output_root/uuid.uuid4().hex
    run.mkdir(mode=0o700)
    data=json.dumps(results,ensure_ascii=False,sort_keys=True,indent=2).encode()
    manifest={'schema':'d4_wrong10_replay.v1','method':'CAPTURED_CHATGPT_ANSWER_ONLY_RESPONSES_NOT_LIVE_PROVIDER',
              'input_sha256':digest(args.input.read_bytes()),'responses_sha256':digest(args.responses.read_bytes()),
              'bridge_sha256':digest((ROOT/'grading/evidence/d4_llm_claim_bridge.py').read_bytes()),
              'validator_sha256':digest((ROOT/'grading/evidence/d4_structured_claim.py').read_bytes()),
              'runner_sha256':digest(Path(__file__).read_bytes()),'result_sha256':digest(data),
              'case_count':len(results),'conditional_counts':dict(Counter(r['conditional_candidate'] for r in results)),
              'bound_counts':dict(Counter(r['registry_bound_candidate'] for r in results)),
              'binding_counts':dict(Counter(r['source_binding'] for r in results)),
              'extraction_counts':dict(Counter(r['extraction_status'] for r in results)),
              'reason_counts':dict(Counter(r['reason'] for r in results)),
              'accuracy_status':'NOT_ESTABLISHED','score_admission':'DISABLED','score_effect':'none'}
    if args.verified_export: manifest['export_sha256']=digest(args.verified_export.read_bytes())
    for name,blob in [('results.json',data),('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())]:
        fd=os.open(run/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb') as out: out.write(blob)
    print(json.dumps({'run':str(run),**manifest},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
