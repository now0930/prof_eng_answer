"""Prevent EMC polarity inversion and positive Fact credit from negative claims."""
from unittest.mock import patch

import pytest
from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.scoring import deterministic_requirement_evaluator as evaluator

TOPIC = 'instrumentation_power_grounding_shielding_ups_ground_loop_emc'
KEY_EMI = ('emc_coupling_modes', 'diagnoses', 'emc_source_path_victim')
KEY_SCOPE = ('emc_interference_source', 'distinct_from', 'emc_coupling_path')


def _evidence(answer):
    return extract_canonical_claim_evidence(answer, topic_ids=[TOPIC])


def _matching(answer, key):
    result = _evidence(answer)
    return [r for r in result['canonical_evidence']['claims']
            if tuple(r.get(k) for k in ('subject', 'predicate', 'object')) == key
            and r.get('assertion_context') in ('asserted', 'corrected')]


@pytest.mark.parametrize('answer,expected', [
    ('전도성·용량성·유도성·방사성 결합으로 간섭원·결합경로·피해기기를 진단한다.', 'positive'),
    ('전도성·용량성·유도성·방사성 결합은 간섭원·결합경로·피해기기 진단과 무관하다.', 'negative'),
    ('전도성·용량성·유도성·방사성 결합은 간섭원·결합경로·피해기기 진단과 무관하지 않다.', 'positive'),
])
def test_emi_irrelevance_polarity(answer, expected):
    claims = _matching(answer, KEY_EMI)
    assert claims
    assert {r['polarity'] for r in claims} == {expected}


@pytest.mark.parametrize('answer,expected', [
    ('간섭원과 결합경로를 구분한다.', 'positive'),
    ('간섭원과 결합경로는 구분할 필요가 없다.', 'negative'),
])
def test_distinct_from_correct_subject_and_polarity(answer, expected):
    result = _evidence(answer)
    claims = _matching(answer, KEY_SCOPE)
    assert claims
    assert {r['polarity'] for r in claims} == {expected}
    assert not [r for r in result['canonical_evidence']['claims']
                if r.get('subject') == r.get('object')
                and r.get('predicate') == 'distinct_from']


@pytest.mark.parametrize('answer,requirement', [
    ('전도성·용량성·유도성·방사성 결합은 간섭원·결합경로·피해기기 진단과 무관하다.', 'ipgse_emi_coupling_paths'),
    ('간섭원과 결합경로는 구분할 필요가 없다.', 'ipgse_scope_chain'),
])
def test_negative_never_earns_fact_credit(answer, requirement):
    result = _evidence(answer)
    with patch.object(evaluator, 'excluded_from_scoring', return_value=False):
        decision = evaluator.evaluate_deterministic_requirements(
            claims=result['canonical_evidence']['claims'], invariant_codes=(),
            topic_ids=[TOPIC], extraction_complete=bool(result['extraction_complete'])
        )
    selected = {r['requirement_id']: r for r in decision['requirements']}
    assert selected[requirement]['status'] == 'WRONG'
    assert not selected[requirement]['matched_fact_ids']
