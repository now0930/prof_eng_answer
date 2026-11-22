"""Regression for a real source-swap vulnerability in the 55-row audit."""
import hashlib

from scripts.replay_d4_common_relation import _claim_review_source_matches


def _span(answer, token):
    start=answer.index(token)
    return {'start':start,'end':start+len(token),'text':token}


def test_source_swap_is_rejected_even_when_value_elsewhere_is_correct():
    answer = '임계감쇠에 대한 잘못된 설명.\n| 구분 | Critical damp |\n| ζ | ζ = 1 |'
    selected=_span(answer,'임계감쇠에 대한 잘못된 설명.')
    elsewhere=_span(answer,'ζ = 1')
    claim={'answer_sha256':hashlib.sha256(answer.encode()).hexdigest(),
           'span':_span(answer,'| 구분 | Critical damp |\n| ζ | ζ = 1 |'),
           'relation':{'evidence':[elsewhere]}}
    assert not _claim_review_source_matches(answer,selected,claim)


def test_included_table_cell_and_wider_valid_span_is_accepted():
    answer = '| 구분 | Critical damp |\n| ζ | ζ = 1 |'
    row=_span(answer,'| ζ | ζ = 1 |')
    claim={'answer_sha256':hashlib.sha256(answer.encode()).hexdigest(),
           'span':{'start':0,'end':len(answer),'text':answer},
           'relation':{'evidence':[_span(answer,'ζ = 1')]}}
    assert _claim_review_source_matches(answer,row,claim)
    claim['answer_sha256']='0'*64
    assert not _claim_review_source_matches(answer,row,claim)


def test_partial_outside_source_and_nonliteral_quote_are_rejected():
    answer='원문 A. 올바른 진술 B.'
    selected=_span(answer,'원문 A.')
    claim={'answer_sha256':hashlib.sha256(answer.encode()).hexdigest(),
           'span':{'start':0,'end':len(answer),'text':answer},
           'relation':{'evidence':[_span(answer,'올바른 진술 B.')]}}
    assert not _claim_review_source_matches(answer,selected,claim)
    claim['relation']['evidence']=[_span(answer,'원문 A.')]
    assert _claim_review_source_matches(answer,selected,claim)
    claim['relation']['evidence'][0]['text']='위조된 텍스트'
    assert not _claim_review_source_matches(answer,selected,claim)

