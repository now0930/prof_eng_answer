import argparse
import json
from pathlib import Path

BANK_PATH = Path("rubrics/model_answers/industrial_instrumentation_control.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=False, help="topic_id")
    parser.add_argument("--type", required=False, help="question_type")
    parser.add_argument("--list", action="store_true", help="list all entries")
    args = parser.parse_args()

    data = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    answers = data.get("answers", [])

    if args.list:
        for a in answers:
            print(f"{a.get('topic_id')} | {a.get('question_type')} | {a.get('id')} | {a.get('title')}")
        return

    matched = []
    for a in answers:
        if args.topic and a.get("topic_id") != args.topic:
            continue
        if args.type and a.get("question_type") != args.type:
            continue
        matched.append(a)

    if not matched:
        print("No matched model answer.")
        return

    for a in matched:
        print("=" * 80)
        print(a.get("title"))
        print("- id:", a.get("id"))
        print("- topic_id:", a.get("topic_id"))
        print("- question_type:", a.get("question_type"))
        print()

        print("[Expected structure]")
        for x in a.get("expected_structure", []):
            print("-", x)
        print()

        print("[Model answer outline]")
        for x in a.get("model_answer_outline", []):
            print("-", x)
        print()

        print("[High score features]")
        for x in a.get("high_score_features", []):
            print("-", x)
        print()

        print("[Low score patterns]")
        for x in a.get("low_score_patterns", []):
            print("-", x)
        print()

        print("[Field connection points]")
        for x in a.get("field_connection_points", []):
            print("-", x)
        print()


if __name__ == "__main__":
    main()
