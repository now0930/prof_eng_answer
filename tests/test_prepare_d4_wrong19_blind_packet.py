import hashlib
import json
from pathlib import Path

import pytest

from scripts import prepare_d4_wrong19_blind_packet as packet


def test_private_packet_blinds_results_and_refuses_overwrite(tmp_path, monkeypatch):
    def save(name, data):
        path = tmp_path / name
        path.write_text(json.dumps(data), encoding='utf-8')
        return path
    cases = [dict(case_id=f'case{i}', answer='evidence', question='question') for i in range(9)]
    answers = save('answers', dict(cases=cases))
    input_hash = packet.digest(answers.read_bytes())
    rows = [dict(claim_id=f'claim{i}', case_id=f'case{i%9}', fact_id=f'fact{i%26}', input_sha256=packet.digest(b'evidence'), start=0, end=8, evidence='evidence') for i in range(55)]
    review = save('review', dict(input_sha256=input_hash, rows=rows))
    props = [dict(claim_id=r['claim_id'], case_id=r['case_id'], fact_id=r['fact_id'], claim={}) for r in rows]
    proposals = save('proposals', dict(input_sha256=input_hash, review_sha256=packet.digest(review.read_bytes()), proposals=props))
    results = [dict(claim_id=r['claim_id'], case_id=r['case_id'], fact_id=r['fact_id'], reason='SCOPE_UNRESOLVED' if i < 17 else 'OTHER', component_candidate='SUPPORT_CANDIDATE' if 17 <= i < 20 else 'CONTRADICT_CANDIDATE' if 20 <= i < 23 else 'UNRESOLVED') for i, r in enumerate(rows)]
    replay = save('replay', dict(input_sha256=input_hash, review_sha256=packet.digest(review.read_bytes()), proposals_sha256=packet.digest(proposals.read_bytes()), rows=results))
    fact_rows = [dict(fact_id=f'fact{i}', topic_id='topic', statement='fact', relation={'conditions': []}, source_refs=[], verification_refs=[], verification_status='verified', review_status='approved') for i in range(26)]
    registry = save('registry', dict(facts=fact_rows))
    monkeypatch.setattr(packet, 'REGISTRY_PATH', registry)
    monkeypatch.setattr(packet, 'REGISTRY_SHA', hashlib.sha256(registry.read_bytes()).hexdigest())
    monkeypatch.setattr(packet, '_claim_review_source_matches', lambda *args: True)
    out = tmp_path / 'private'
    packet.build(answers, review, proposals, replay, out)
    blind = json.loads((out / 'blind_packet.json').read_text())
    forms = json.loads((out / 'review_results_template.json').read_text())
    mapping = json.loads((out / 'private_mapping.json').read_text())
    assert len(blind['cases']) == len(forms['reviews']) == len(mapping['mappings']) == 23
    assert len({r['case_id'] for r in blind['cases']}) == 23
    serialized = json.dumps(blind)
    for forbidden in ('SUPPORT_CANDIDATE', 'CONTRADICT_CANDIDATE', 'SCOPE_UNRESOLVED', 'manual_candidate', 'claim_id', 'selection_reason'):
        assert forbidden not in serialized
    assert all(x['status'] == 'PENDING' and x['reviewer_identity'] is None and x['relation_judgment'] is None and x['scope_judgment'] is None for x in forms['reviews'])
    assert (out.stat().st_mode & 0o777) == 0o700
    assert all((p.stat().st_mode & 0o777) == 0o600 for p in out.iterdir())
    with pytest.raises(FileExistsError):
        packet.build(answers, review, proposals, replay, out)
    replay_data = json.loads(replay.read_text())
    replay_data['input_sha256'] = 'wrong'
    replay.write_text(json.dumps(replay_data))
    with pytest.raises(ValueError, match='replay provenance mismatch'):
        packet.build(answers, review, proposals, replay, tmp_path / 'bad')
    assert not (tmp_path / 'bad').exists()
