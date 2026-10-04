import copy
from unittest.mock import patch

import bot
from study.learning_synthesis import load_synthesis
from study.review_presentation import learning_review_messages, _pages
from test_learning_synthesis import fixture, save
from test_synthesis_authoring import setup_packet


def training_fixture(tmp_path):
    master, doc, raw = fixture(tmp_path)
    doc['knowledge'][0]['conditions'] = ['Only under condition A']
    doc['knowledge'][0]['exceptions'] = ['Exception B']
    doc['knowledge'][0]['units'] = ['rad/s']
    doc['learning_path']['sections'][1]['self_check'] = [dict(question='Why?', answer='Because of condition A.')]
    save(tmp_path, master, doc)
    return master, doc, raw, {'learning_synthesis': load_synthesis(tmp_path, master, raw, [])}


def test_order_provenance_conditions_and_immutability(tmp_path):
    _, _, _, training = training_fixture(tmp_path)
    before = copy.deepcopy(training)
    messages = learning_review_messages(training)
    output = '\n'.join(messages)
    assert output.index('학습 목표') < output.index('Lesson 0') < output.index('Lesson 1') < output.index('자가 점검')
    for text in ['Only under condition A','Exception B','rad/s','작성한 설명','원문 인용','LLM 검토·사람 검토 대기','https://example.org','점수 영향 없음']:
        assert text in output
    assert before == training


def test_unavailable_does_not_leak_errors_or_draft_text():
    assert learning_review_messages({}) == []
    output = learning_review_messages({'learning_synthesis': {'status':'unavailable','error':'/private/secret'}})
    assert '기존 복습 자료' in output[0]
    assert '/private' not in output[0]


def test_draft_path_not_displayed(tmp_path):
    _, _, _, training = training_fixture(tmp_path)
    training['learning_synthesis']['document']['learning_path']['review']['status'] = 'draft'
    output = '\n'.join(learning_review_messages(training))
    assert '검토 대기' in output
    assert 'Authored teaching explanation' not in output


def test_stale_source_hides_section_and_dependents(tmp_path):
    master, doc, raw, _ = training_fixture(tmp_path)
    raw[0]['text'] = 'changed'
    training = {'learning_synthesis': load_synthesis(tmp_path, master, raw, [])}
    output = '\n'.join(learning_review_messages(training))
    assert '출처 확인 필요' in output
    assert 'Synthetic concept' not in output
    assert 'Authored teaching explanation' not in output


def test_long_unicode_text_not_lost_or_over_limit(tmp_path):
    text = ('한글😀 수식 L(s)=1/(s+1)\n' * 1000)
    pages = _pages(text)
    assert ''.join(pages) == text
    assert all(len(page.encode('utf-16-le')) // 2 <= 3000 for page in pages)


def test_real_review_handler_sends_learning_pages_then_completion(tmp_path):
    master, doc, packet = setup_packet(tmp_path)
    save(tmp_path, master, doc)
    synthesis = load_synthesis(tmp_path, master, packet['sources'], [])
    material = dict(training={'learning_synthesis': synthesis}, feedback=None, prior_diagnosis={})
    messages = []
    with patch.object(bot, 'BASE_DIR', tmp_path), patch.object(bot, 'DATA_DIR', tmp_path), \
         patch('study.learning_runtime.review_material_for_topic', return_value=material), \
         patch.object(bot, 'send_message', side_effect=lambda chat, msg: messages.append(msg)), \
         patch.dict('os.environ', {'TRAINING_HISTORY_DB': str(tmp_path / 'history.sqlite3')}):
        bot.handle_text({'text':'/review ' + master['topic_id']}, 123, {})
    output = '\n'.join(messages)
    assert '학습 목표' in output
    assert output.index('Lesson 0') < output.index('Lesson 1')
    assert messages[-1].startswith('복습 후 /review done')
