import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading_config import load_active_config

cfg = load_active_config(ROOT)

print("=== active profile ===")
print("version:", cfg["profile"].get("version"))
print("scoring_model:", cfg["profile"].get("scoring_model"))
print("subject_rubric:", cfg["profile"].get("subject_rubric"))
print("rater_profile:", cfg["profile"].get("rater_profile"))

print()
print("=== scoring layers ===")
for layer in cfg["scoring_model"].get("layers", []):
    print(f"{layer.get('id')}. {layer.get('name')}: {layer.get('points')}점")

print()
print("=== rater weights ===")
for layer_id, weights in cfg["scoring_model"].get("rater_weights_by_layer", {}).items():
    print(layer_id, weights, "sum=", sum(weights.values()))

print()
print("=== answer sheet volume policy ===")
volume = cfg["scoring_model"].get("answer_sheet_volume_policy", {})
print("enabled:", volume.get("enabled"))
print("expected pages:", volume.get("expected_answer_sheet_pages_per_25_point_question"))

print()
print("=== raters ===")
for r in cfg["rater_profile"].get("raters", []):
    print("-", r.get("id"), "/", r.get("name"), "/", r.get("primary_layers"))

print()
print("CONFIG VALIDATION OK")
