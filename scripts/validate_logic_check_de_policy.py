#!/usr/bin/env python3
import json
import sys
from pathlib import Path

JSON_PATH = Path("rubrics/logic_checks/industrial_instrumentation_control.json")
EVALUATOR_PATH = Path("logic_check_evaluator.py")
PROMPT_PATH = Path("docs/logic_check_json_generator_prompt.md")

FORBIDDEN_TOPIC_KEYS = {
    "advanced_tradeoff_checks",
    "field_application_checks",
    "coherence_defense_checks",
    "d_e_feedback_templates",
}

FORBIDDEN_AFFECTED_LAYERS = {"D", "E"}

errors = []

def walk(obj, path="$"):
    if isinstance(obj, dict):
        for key, value in obj.items():
            cur = f"{path}.{key}"

            if key in FORBIDDEN_TOPIC_KEYS:
                errors.append(f"forbidden key remains: {cur}")

            if key == "affected_layers":
                if not isinstance(value, list):
                    errors.append(f"affected_layers is not list: {cur}")
                else:
                    bad = [x for x in value if x in FORBIDDEN_AFFECTED_LAYERS]
                    if bad:
                        errors.append(f"D/E remains in affected_layers at {cur}: {bad}")

            walk(value, cur)

    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            walk(value, f"{path}[{idx}]")

data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
walk(data)

for topic in data.get("topic_logic_checks", []):
    topic_id = topic.get("topic_id", "<unknown>")
    trust = topic.get("de_claim_trust")

    if not isinstance(trust, dict):
        errors.append(f"missing de_claim_trust: {topic_id}")
        continue

    if trust.get("score_effect") != "none":
        errors.append(f"de_claim_trust.score_effect must be none: {topic_id}")

    if trust.get("target_layers") != ["D", "E"]:
        errors.append(f"de_claim_trust.target_layers must be ['D', 'E']: {topic_id}")

evaluator_text = EVALUATOR_PATH.read_text(encoding="utf-8")

if "advanced_tradeoff_checks" in evaluator_text:
    errors.append("logic_check_evaluator.py still references advanced_tradeoff_checks")

if 'layers=["C", "E"]' in evaluator_text or 'layers=["C","E"]' in evaluator_text:
    errors.append("logic_check_evaluator.py still contains layers=['C', 'E']")

prompt_text = PROMPT_PATH.read_text(encoding="utf-8")

for forbidden in FORBIDDEN_TOPIC_KEYS:
    occurrences = prompt_text.count(forbidden)

    # docs/logic_check_json_generator_prompt.md에서는 금지 필드 목록에 1회 등장하는 것은 허용한다.
    if occurrences > 1:
        errors.append(f"prompt mentions {forbidden} too many times: {occurrences}")

if errors:
    print("INVALID")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("VALID: Logic Check D/E policy")
