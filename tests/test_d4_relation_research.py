import json
from pathlib import Path

from grading.evidence.d4_relation_research import diagnose_surface, evaluate_claim, project_fact

ROOT = Path(__file__).resolve().parents[1]


def test_six_approved_registry_proposals_preserve_relation_and_do_not_approve():
    anchors = {'absolute_humidity_definition', 'diaphragm_sensor_vs_seal', 'pulse_frequency_speed_equation',
               'thermocouple_law_of_intermediate_metals', 'encoder_resolution_ppr_cpr_definition',
               'encoder_frequency_limit_selection'}
    facts = [f for f in json.loads((ROOT / 'grading/evidence/approved_fact_registry.json').read_text())['facts']
             if isinstance(f, dict) and f.get('legacy_anchor_id') in anchors]
    assert len(facts) == 6
    for fact in facts:
        result = project_fact(fact['fact_id'], fact['topic_id'])
        assert result['conditions'] == fact['relation']['conditions']
        assert result['subject'] == fact['relation']['subject']
        assert result['source_provenance'] == fact['verification_refs']
        assert result['semantic_equivalence_status'] == 'NOT_ESTABLISHED'
        assert evaluate_claim({'subject': result['subject'], 'polarity': 'positive'}, fact['topic_id'], fact['fact_id'], result)['status'] == 'UNRESOLVED'
        assert evaluate_claim({}, 'other_topic', fact['fact_id'], result)['reason'] == 'INVALID_SCOPE_OR_PROPOSAL'
        assert evaluate_claim({}, fact['topic_id'], fact['fact_id'], {**result, 'conditions': []})['status'] == 'UNRESOLVED'


def test_surface_diagnostic_distinguishes_missing_same_sentence_and_unknown():
    family = 'x4_decoding_vs_channel_ppr'
    result = diagnose_surface('x4 복호를 사용한다. 채널 PPR을 읽는다.', family)
    assert result['status'] == 'NO_CANDIDATE'
    assert result['conditions'] == 'NOT_EXTRACTED'
    assert diagnose_surface('x4 복호와 PPR 관계는 미상이다.', family)['status'] == 'SURFACE_AVAILABLE'
    assert diagnose_surface('anything', 'unknown')['status'] == 'UNRESOLVED'
    assert project_fact('unknown', 'unknown')['status'] == 'UNRESOLVED'


def test_private_replay_creates_unique_hashed_results_without_answer_text(tmp_path):
    import hashlib
    import subprocess
    import sys
    source = tmp_path / 'input.json'
    source.write_text(json.dumps([{'case_id': 'p1', 'family': 'x4_decoding_vs_channel_ppr',
                                   'answer_text': 'x4와 PPR의 관계는 미상이다.'}]))
    root = tmp_path / 'runs'
    cmd = [sys.executable, str(ROOT / 'scripts/evaluate_d4_relation_research.py'),
           '--input', str(source), '--output-root', str(root)]
    subprocess.run(cmd, check=True, capture_output=True)
    subprocess.run(cmd, check=True, capture_output=True)
    runs = list(root.iterdir())
    assert len(runs) == 2 and runs[0] != runs[1]
    for run in runs:
        result = (run / 'results.json').read_bytes()
        manifest = json.loads((run / 'manifest.json').read_text())
        assert manifest['result_sha256'] == hashlib.sha256(result).hexdigest()
        assert manifest['input_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
        assert '미상' not in result.decode()
        assert manifest['score_admission'] == 'DISABLED'
        assert (run.stat().st_mode & 0o777) == 0o700


def test_thermocouple_bounded_relation_conditions_and_adversarial_context():
    from grading.evidence.d4_relation_research import evaluate_thermocouple_answer
    topic = 'thermocouple_temperature_sensor_seebeck_reference_junction_compensation'
    fact = 'thermocouple_law_of_intermediate_metals'
    prefix = '열전대 회로에 제3 금속을 삽입할 때 '
    conditions = '재료가 균질하고 두 신규 접점이 같은 온도이면 '
    correct = prefix + conditions + '순 열기전력은 변하지 않는다.'
    wrong = prefix + conditions + '순 열기전력은 변한다.'
    missing = prefix + '두 신규 접점이 같은 온도이면 순 열기전력은 변하지 않는다.'
    supported = evaluate_thermocouple_answer(correct, topic, fact)
    contradicted = evaluate_thermocouple_answer(wrong, topic, fact)
    held = evaluate_thermocouple_answer(missing, topic, fact)
    assert supported['comparisons'][0]['status'] == 'SUPPORT_CANDIDATE'
    assert supported['comparisons'][0]['condition_status'] == 'SATISFIED'
    assert contradicted['comparisons'][0]['status'] == 'CONTRADICT_CANDIDATE'
    assert held['comparisons'][0]['status'] == 'UNRESOLVED'
    assert held['comparisons'][0]['condition_status'] == 'MISSING'
    unequal = correct.replace('두 신규 접점이 같은 온도이면', '두 신규 접점의 온도가 서로 다르면')
    conflict = evaluate_thermocouple_answer(unequal, topic, fact)
    assert conflict['comparisons'][0]['condition_status'] == 'CONFLICT'
    assert conflict['comparisons'][0]['status'] == 'UNRESOLVED'
    claim = supported['extraction']['claims'][0]
    assert claim['subject'] == '열전대 회로에 제3 금속을 삽입할 때'
    assert claim['object'] == '순 열기전력'
    assert claim['polarity'] == 'NEGATIVE' and claim['negation_scope'] == 'PREDICATE'
    for span in claim['component_spans'].values():
        assert 0 <= span['start'] < span['end'] <= len(correct)
    assert correct[claim['component_spans']['predicate']['start']:claim['component_spans']['predicate']['end']] == '변하지 않는다'
    assert supported['score_admission'] == 'DISABLED' and supported['score_effect'] == 'none'
    assert not supported['comparisons'][0]['source_match_proven']
    for text in [
        '“' + correct + '”라고 인용했다.',
        wrong + ' 이 설명은 틀렸다.',
        correct + ' ' + wrong,
        correct.replace('변하지 않는다', '변하지 않는 것은 아니다'),
        correct.replace('같은 온도이면', '다른 온도이면'),
        correct.replace('순 열기전력은', '순 열기전력 3 rpm은'),
        'PID 온도제어와 열전대 접점을 비교한다.',
    ]:
        result = evaluate_thermocouple_answer(text, topic, fact)
        assert result['status'] == 'UNRESOLVED'
        assert result['comparisons'] == []
    assert evaluate_thermocouple_answer(correct, 'other', fact)['status'] == 'UNRESOLVED'
