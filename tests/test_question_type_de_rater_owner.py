#!/usr/bin/env python3
from pathlib import Path

src = Path("grading_agents.py").read_text(encoding="utf-8")

required = [
    'if layer_id in {"D", "E"}:',
    'new_layer["rater_weighted_candidate_score"]',
    'new_layer["rater_weighted_diagnostic_only"] = True',
    'new_layer["rater_weighted_diagnostic_only"] = False',
]
for token in required:
    assert token in src, token

# D/E의 numeric owner가 rater 이전 score임을 구조적으로 보장한다.
block_start = src.index('if layer_id in {"D", "E"}:')
block = src[block_start:block_start + 1400]
assert 'new_layer["score"] = round(float(layer.get("score", 0)), 2)' in block
assert 'new_layer["score"] = round(weighted_score, 2)' in block

print("PASS")
