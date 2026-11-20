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
