"""Replay already exposed ChatGPT component proposals, not live extraction."""
import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from grading.evidence.d4_common_relation import compare_component, evaluate_component, PROFILES



def _claim_review_source_matches(answer, review_row, claim):
    """A Fact suggestion must cite this claim ID's reviewed source, not another sentence.

    Context/scope evidence can appear elsewhere in the same answer. The
    proposed *relation* evidence must be wholly contained within the reviewed
    row, valid at code-point offsets, and inside the proposed primary span.
    The author stance/technical meaning remains unverified even on success.
    """
    if not isinstance(claim, dict) or claim.get('answer_sha256') != hashlib.sha256(answer.encode()).hexdigest():
        return False
    primary = claim.get('span')
    rel = claim.get('relation')
    if not isinstance(primary, dict) or not isinstance(rel, dict):
        return False
    if not isinstance(rel.get('evidence'), list) or not rel['evidence']:
        return False
    a, b = review_row['start'], review_row['end']
    for s in [primary] + rel['evidence']:
        if not isinstance(s, dict) or set(s) != {'start','end','text'}:
            return False
        x, y = s['start'], s['end']
        if type(x) is not int or type(y) is not int or not 0 <= x < y <= len(answer):
            return False
        if not isinstance(s['text'], str) or answer[x:y] != s['text']:
            return False
    x, y = primary['start'], primary['end']
    return all(a <= s['start'] < s['end'] <= b and
               x <= s['start'] < s['end'] <= y for s in rel['evidence'])


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--answers',type=Path,required=True)
    ap.add_argument('--review',type=Path,required=True)
    ap.add_argument('--proposals',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--allow-missing-proposals', action='store_true',
                    help='record absent proposals as unresolved for inventory-only replay')
    args=ap.parse_args()
    raw=args.answers.read_bytes(); review=json.loads(args.review.read_bytes()); proposal=json.loads(args.proposals.read_bytes())
    sha=lambda data: hashlib.sha256(data).hexdigest()
    if sha(raw)!=review['input_sha256'] or sha(raw)!=proposal['input_sha256'] or sha(args.review.read_bytes())!=proposal['review_sha256']:
        raise ValueError('input hash mismatch')
    cases=json.loads(raw)['cases']; bycase={r['case_id']:r for r in cases}; rows=review['rows']
    if len(bycase)!=len(cases) or len({r['claim_id'] for r in rows})!=len(rows): raise ValueError('duplicate IDs')
    records=proposal['proposals']; byid={r['claim_id']:r for r in records}
    if len(byid)!=len(records) or not set(byid)<=set(r['claim_id'] for r in rows): raise ValueError('proposal ID mismatch')
    output=[]
    for row in rows:
        cid=row['claim_id']; answer=bycase[row['case_id']]['answer']; fid=row['fact_id']
        if sha(answer.encode())!=row['input_sha256'] or answer[row['start']:row['end']]!=row['evidence']: raise ValueError('review evidence mismatch')
        rec=byid.get(cid)
        if rec is not None and (rec['fact_id']!=fid or rec['case_id']!=row['case_id']): raise ValueError('proposal mapping mismatch')
        if fid in PROFILES and rec is None and not args.allow_missing_proposals:
            raise ValueError('missing in-scope proposal')
        if rec is not None and not _claim_review_source_matches(answer,row,rec.get('claim')):
            raise ValueError('claim source attribution mismatch: '+cid)
        if rec is not None:
            r=evaluate_component(answer,rec['claim'],fid)
        else:
            r=compare_component(answer,None,fid)
        output.append(dict(case_id=row['case_id'],claim_id=cid,fact_id=fid,
                           proposal_availability='PROVIDED' if rec is not None else 'MISSING',
                           prior_manual_candidate=row['manual_candidate'],**r))
    result=dict(method='CAPTURED_CHATGPT_COMPONENT_PROPOSALS; NOT_BLIND_OR_SEMANTIC_ACCURACY', input_sha256=sha(raw),review_sha256=sha(args.review.read_bytes()),proposals_sha256=sha(args.proposals.read_bytes()),comparison_count=len(output),profile_count=len(PROFILES),component_counts=dict(Counter(r['component_candidate'] for r in output)),reason_counts=dict(Counter(r['reason'] for r in output)),registry_bound_counts=dict(Counter(r['registry_bound_candidate'] for r in output)),rows=output)
    fd = os.open(args.output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2,sort_keys=True)

if __name__=='__main__': main()
