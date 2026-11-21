import copy
import hashlib
import sys
import types

import pytest

from grading.evidence.d4_structured_claim import (
    SCHEMA, FACT, TOPIC, EXPECTED_REGISTRY_SHA256, assess_proposal, evaluate_against_registry,
)

TEXT = '열전대에 균질한 제3 금속을 삽입하고 두 신규 접점이 등온이면 순 기전력은 변하지 않는다.'


def sample(text=TEXT, outcome='PRESERVED'):
    def span(value):
        start = text.index(value)
        return {'start': start, 'end': start + len(value), 'text': value}
    full = span(text)
    vals = {'stance': ('ASSERTED', '순 기전력은'), 'scope': ('IN_SCOPE', '열전대'),
            'homogeneous': ('YES', '균질한 제3 금속'), 'isothermal': ('YES', '두 신규 접점이 등온'),
            'outcome': (outcome, '변하지 않는다' if outcome == 'PRESERVED' else '증가한다'),
            'causal_binding': ('INSERTION_EFFECT', '제3 금속을 삽입')}
    return {'schema': SCHEMA, 'answer_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'claims': [{'span': full, 'fields': {k: {'value': v, 'evidence': [span(s)]} for k, (v, s) in vals.items()}}]}


def assert_safe(result):
    assert result['score_admission'] == 'DISABLED'
    assert result['score_effect'] == 'none'
    assert result['source_match_proven'] is False
    assert result['accuracy_status'] == 'NOT_ESTABLISHED'


def test_positive_and_negative_proposal_comparisons():
    right = assess_proposal(TEXT, sample())
    wrong_text = TEXT.replace('변하지 않는다', '증가한다')
    wrong = assess_proposal(wrong_text, sample(wrong_text, 'CHANGED'))
    assert right['conditional_candidate'] == 'SUPPORT_CANDIDATE'
    assert wrong['conditional_candidate'] == 'CONTRADICT_CANDIDATE'
    for r in [right, wrong]:
        assert r['status'] == 'UNRESOLVED'  # no trusted Registry yet
        assert_safe(r)


@pytest.mark.parametrize('field,value', [('stance', 'UNKNOWN'), ('scope', 'AMBIGUOUS'),
    ('homogeneous', 'UNKNOWN'), ('isothermal', 'UNKNOWN'), ('isothermal', 'NO'),
    ('causal_binding', 'UNKNOWN'), ('outcome', 'POSSIBLE'), ('outcome', 'CHANGED')])
def test_missing_conflicting_or_wrong_direction_proposals_hold(field, value):
    p = sample()
    p['claims'][0]['fields'][field]['value'] = value
    r = assess_proposal(TEXT, p)
    assert r['conditional_candidate'] == 'UNRESOLVED'
    assert_safe(r)


@pytest.mark.parametrize('mutate', ['hash', 'span', 'extra', 'bool_offset', 'missing_evidence', 'multi_claim', 'out_of_span', 'bad_enum'])
def test_invalid_or_forged_structure(mutate):
    p = sample()
    c = p['claims'][0]
    if mutate == 'hash': p['answer_sha256'] = '0' * 64
    if mutate == 'span': c['fields']['isothermal']['evidence'][0]['text'] = '위조'
    if mutate == 'extra': p['score_admission'] = 'ENABLED'
    if mutate == 'bool_offset': c['span']['start'] = False
    if mutate == 'missing_evidence': c['fields']['homogeneous']['evidence'] = []
    if mutate == 'multi_claim': p['claims'].append(copy.deepcopy(c))
    if mutate == 'out_of_span': c['span'] = c['fields']['scope']['evidence'][0].copy()
    if mutate == 'bad_enum': c['fields']['stance']['value'] = []
    r = assess_proposal(TEXT, p)
    assert r['structure_status'] == 'UNRESOLVED'
    assert r['conditional_candidate'] == 'UNRESOLVED'
    assert_safe(r)


@pytest.mark.parametrize('text', ['“' + TEXT + '”라고 인용했다.', TEXT + ' 이는 틀린 주장이다.',
    TEXT.replace('균질한 제3 금속', '균질한 제3 금속이 아닌 물질'),
    TEXT.replace('두 신규 접점이 등온이면', '두 신규 접점이 등온이 아니라면'),
    TEXT.replace('변하지 않는다', '변하지 않는 것은 아니라고 한다'),
    TEXT.replace('변하지 않는다', '변하지 않는다 그러나 증가한다')])
def test_misleading_exact_evidence_does_not_grant_candidate(text):
    # Copy literal subspans even though the full sentence defeats the annotations.
    p = sample()
    p['answer_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    p['claims'][0]['span'] = {'start': 0, 'end': len(text), 'text': text}
    for item in p['claims'][0]['fields'].values():
        for ev in item['evidence']:
            if ev['text'] not in text:
                ev['text'] = ev['text'].replace('변하지 않는다', '변하지 않는').replace('제3 금속을 삽입', '삽입')
            start = text.index(ev['text'])
            ev.update(start=start, end=start + len(ev['text']))
    assert assess_proposal(text, p)['conditional_candidate'] == 'UNRESOLVED'


def test_registry_binding_uses_trusted_loader_not_model(monkeypatch):
    fake = types.ModuleType('grading.evidence.d4_relation_research')
    row = {'status': 'PROPOSAL', 'fact_id': FACT, 'topic_id': TOPIC,
           'verification_status': 'verified', 'review_status': 'approved',
           'conditions': ['homogeneous_materials', 'isothermal_added_junctions'],
           'source_provenance': ['test-fixture-only'], 'source_statement': 'test fixture',
           'registry_sha256': EXPECTED_REGISTRY_SHA256, 'registry_fact_sha256': 'b' * 64}
    fake.project_fact = lambda fact, topic: row
    monkeypatch.setitem(sys.modules, fake.__name__, fake)
    result = evaluate_against_registry(TEXT, sample())
    assert result['source_binding'] == 'APPROVED_METADATA_BOUND'
    assert result['status'] == 'SUPPORT_CANDIDATE'
    assert_safe(result)
    for key, value in [('review_status', 'pending'), ('conditions', []), ('fact_id', 'other'), ('registry_sha256', 'a' * 64)]:
        old = row[key]
        row[key] = value
        r = evaluate_against_registry(TEXT, sample())
        assert r['source_binding'] == 'SCOPE_OR_SOURCE_MISMATCH'
        assert r['status'] == 'UNRESOLVED'
        row[key] = old
    fake.project_fact = lambda f, t: (_ for _ in ()).throw(OSError('missing'))
    assert evaluate_against_registry(TEXT, sample())['source_binding'] == 'UNAVAILABLE'


def test_non_asserted_and_out_of_scope_are_proposals_only():
    for field, value, expected in [('stance', 'QUOTED', 'NON_ASSERTED'),
                                   ('scope', 'OUT_OF_SCOPE', 'OUT_OF_SCOPE')]:
        p = sample()
        p['claims'][0]['fields'][field]['value'] = value
        r = assess_proposal(TEXT, p)
        assert r['conditional_candidate'] == expected
        assert r['status'] == 'UNRESOLVED'
        assert_safe(r)


def test_invalid_unicode_fails_closed():
    p = sample()
    assert assess_proposal('\ud800', p)['reason'] == 'INVALID_UNICODE'


def test_actual_registry_binding_if_repository_is_present():
    from pathlib import Path
    registry = Path(__file__).resolve().parents[1] / 'grading/evidence/approved_fact_registry.json'
    if not registry.is_file():
        pytest.skip('actual repository Registry not mounted in isolated ChatGPT test environment')
    r = evaluate_against_registry(TEXT, sample())
    assert r['source_binding'] == 'APPROVED_METADATA_BOUND'
    assert r['status'] == 'SUPPORT_CANDIDATE'
    assert_safe(r)
