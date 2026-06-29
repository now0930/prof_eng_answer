#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "scripts/rubric_manager.py"]

MODEL_BANK = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_BANK = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
TOPIC_BANK = ROOT / "rubrics/topic_importance/industrial_instrumentation_control.json"


def run(*args: str) -> str:
    cmd = CLI + list(args)
    print("+", " ".join(str(x) for x in cmd))
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(p.stdout)
    if p.returncode != 0:
        raise SystemExit(p.returncode)
    return p.stdout


def help_has(command: str, option: str) -> bool:
    p = subprocess.run(
        CLI + [command, "--help"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return option in p.stdout


def maybe_no_backup(command: str) -> list[str]:
    return ["--no-backup"] if help_has(command, "--no-backup") else []


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_model(path: Path) -> int:
    return len(read_json(path).get("answers", []))


def count_topics(path: Path) -> int:
    return len(read_json(path).get("topics", []))


def assert_model_exists(path: Path, target_id: str, title: str | None = None) -> None:
    bank = read_json(path)
    for item in bank.get("answers", []):
        if item.get("id") == target_id:
            if title is not None and item.get("title") != title:
                raise AssertionError(f"title mismatch: {item.get('title')} != {title}")
            return
    raise AssertionError(f"model answer not found: {target_id}")


def assert_topic_exists(path: Path, target_id: str, label_key: str, label_value: str | None = None) -> None:
    bank = read_json(path)
    for item in bank.get("topics", []):
        if item.get("topic_id") == target_id:
            if label_value is not None and item.get(label_key) != label_value:
                raise AssertionError(f"{label_key} mismatch: {item.get(label_key)} != {label_value}")
            return
    raise AssertionError(f"topic not found: {target_id}")


def assert_model_not_exists(path: Path, target_id: str) -> None:
    bank = read_json(path)
    for item in bank.get("answers", []):
        if item.get("id") == target_id:
            raise AssertionError(f"model answer still exists: {target_id}")


def assert_topic_not_exists(path: Path, target_id: str) -> None:
    bank = read_json(path)
    for item in bank.get("topics", []):
        if item.get("topic_id") == target_id:
            raise AssertionError(f"topic still exists: {target_id}")


def model_answer_candidate() -> dict:
    topic_id = "crud_test_model_answer"
    return {
        "id": f"{topic_id}_IMPLEMENTATION_EVALUATION_v1",
        "topic_id": topic_id,
        "question_type": "IMPLEMENTATION_EVALUATION",
        "title": "[CRUD TEST] Model Answer",
        "topic_aliases": ["CRUD TEST", "모범답안 CRUD 검증"],
        "question_examples": [
            "CRUD 테스트 주제의 적용 절차와 검증 방법을 설명하시오."
        ],
        "expected_structure": [
            "배경",
            "시스템 구성",
            "절차",
            "검증 기준",
            "현장 적용 유의사항"
        ],
        "model_answer_outline": [
            "CRUD 테스트 주제는 관리 로직의 추가, 수정, 삭제, 검증 흐름을 확인하기 위한 임시 항목이다.",
            "답안은 구성, 절차, 검증 기준, 현장 적용 유의사항 순서로 전개한다.",
            "검증은 항목 수 변화와 validator 통과 여부를 기준으로 판단한다.",
            "실제 운영 bank는 직접 변경하지 않고 임시 복사본에서 CRUD 왕복을 확인한다."
        ],
        "high_score_features": [
            "절차와 검증 기준을 함께 설명한다.",
            "현장 적용 시 수정 이력과 rollback 가능성을 언급한다."
        ],
        "low_score_patterns": [
            "키워드만 나열하고 검증 기준을 제시하지 않는다.",
            "추가와 수정, 삭제의 차이를 구분하지 않는다."
        ],
        "field_connection_points": [
            "운영 중 실제 bank를 직접 수정하지 않고 백업과 검증을 거친다.",
            "자동 반영보다 후보 생성 후 검토하는 절차가 안전하다."
        ],
        "revision_notes": [
            "CRUD 테스트용 임시 항목이다."
        ]
    }


def fact_anchor_candidate() -> dict:
    topic_id = "crud_test_fact_anchor"
    return {
        "topic_id": topic_id,
        "name": "[CRUD TEST] Fact Anchor",
        "aliases": ["CRUD TEST", "Fact Anchor CRUD 검증"],
        "anchors": [
            {
                "id": f"{topic_id}_anchor_{idx}",
                "name": f"CRUD 핵심 Fact {idx}",
                "expected": f"CRUD 검증용 핵심 fact {idx}를 설명한다.",
                "core_terms": [f"core_term_{idx}"],
                "support_terms": [f"support_term_{idx}"]
            }
            for idx in range(1, 6)
        ]
    }


def topic_importance_candidate() -> dict:
    topic_id = "crud_test_topic_importance"
    return {
        "topic_id": topic_id,
        "label": "[CRUD TEST] Topic Importance",
        "aliases": ["CRUD TEST", "Topic Importance CRUD 검증"],
        "difficulty": "FIELD_APPLICATION",
        "selection_importance": "NORMAL",
        "selection_policy": "safe_or_balanced_choice",
        "minimum_attempt_floor": 10,
        "target_score": 15,
        "excellent_score_band": [15.0, 15.75],
        "omission_risk": "low",
        "fatal_error_risk": "medium",
        "score_ceiling_policy": "field_application_practical_ceiling"
    }


def test_model_answer(tmp: Path) -> None:
    print("\n=== TEST Model Answer CRUD ===")

    bank = tmp / "model_answers.json"
    cand = tmp / "model_answer_candidate.json"
    shutil.copy2(MODEL_BANK, bank)

    original_count = count_model(bank)
    entry = model_answer_candidate()
    target_id = entry["id"]

    run(
        "new-model-answer",
        "--topic-id", entry["topic_id"],
        "--question-type", entry["question_type"],
        "--title", entry["title"],
        "--out", str(cand),
    )

    write_json(cand, entry)

    run(
        "promote-model-answer",
        "--candidate", str(cand),
        "--bank", str(bank),
        *maybe_no_backup("promote-model-answer"),
    )
    run("validate-model-answers", "--bank", str(bank))

    if count_model(bank) != original_count + 1:
        raise AssertionError("model add did not increase count")
    assert_model_exists(bank, target_id, "[CRUD TEST] Model Answer")

    entry["title"] = "[CRUD TEST] Model Answer Updated"
    write_json(cand, entry)

    run(
        "promote-model-answer",
        "--candidate", str(cand),
        "--bank", str(bank),
        "--replace",
        *maybe_no_backup("promote-model-answer"),
    )
    run("validate-model-answers", "--bank", str(bank))

    if count_model(bank) != original_count + 1:
        raise AssertionError("model update created duplicate")
    assert_model_exists(bank, target_id, "[CRUD TEST] Model Answer Updated")

    run(
        "delete-model-answer",
        "--id", target_id,
        "--bank", str(bank),
        *maybe_no_backup("delete-model-answer"),
    )
    run("validate-model-answers", "--bank", str(bank))

    if count_model(bank) != original_count:
        raise AssertionError("model delete did not restore count")
    assert_model_not_exists(bank, target_id)


def test_fact_anchor(tmp: Path) -> None:
    print("\n=== TEST Fact Anchor CRUD ===")

    bank = tmp / "fact_anchors.json"
    cand = tmp / "fact_anchor_candidate.json"
    shutil.copy2(FACT_BANK, bank)

    original_count = count_topics(bank)
    entry = fact_anchor_candidate()
    target_id = entry["topic_id"]

    run(
        "new-fact-anchor-topic",
        "--topic-id", target_id,
        "--name", entry["name"],
        "--out", str(cand),
    )

    write_json(cand, entry)

    run(
        "promote-fact-anchor-topic",
        "--candidate", str(cand),
        "--bank", str(bank),
        *maybe_no_backup("promote-fact-anchor-topic"),
    )
    run("validate-fact-anchors", "--bank", str(bank))

    if count_topics(bank) != original_count + 1:
        raise AssertionError("fact anchor add did not increase count")
    assert_topic_exists(bank, target_id, "name", "[CRUD TEST] Fact Anchor")

    entry["name"] = "[CRUD TEST] Fact Anchor Updated"
    write_json(cand, entry)

    run(
        "promote-fact-anchor-topic",
        "--candidate", str(cand),
        "--bank", str(bank),
        "--replace",
        *maybe_no_backup("promote-fact-anchor-topic"),
    )
    run("validate-fact-anchors", "--bank", str(bank))

    if count_topics(bank) != original_count + 1:
        raise AssertionError("fact anchor update created duplicate")
    assert_topic_exists(bank, target_id, "name", "[CRUD TEST] Fact Anchor Updated")

    run(
        "delete-fact-anchor-topic",
        "--topic-id", target_id,
        "--bank", str(bank),
        *maybe_no_backup("delete-fact-anchor-topic"),
    )
    run("validate-fact-anchors", "--bank", str(bank))

    if count_topics(bank) != original_count:
        raise AssertionError("fact anchor delete did not restore count")
    assert_topic_not_exists(bank, target_id)


def test_topic_importance(tmp: Path) -> None:
    print("\n=== TEST Topic Importance CRUD ===")

    bank = tmp / "topic_importance.json"
    cand = tmp / "topic_importance_candidate.json"
    shutil.copy2(TOPIC_BANK, bank)

    original_count = count_topics(bank)
    entry = topic_importance_candidate()
    target_id = entry["topic_id"]

    run(
        "new-topic-importance",
        "--topic-id", target_id,
        "--label", entry["label"],
        "--difficulty", entry["difficulty"],
        "--out", str(cand),
    )

    write_json(cand, entry)

    run(
        "promote-topic-importance",
        "--candidate", str(cand),
        "--bank", str(bank),
        *maybe_no_backup("promote-topic-importance"),
    )
    run("validate-topic-importance", "--bank", str(bank))

    if count_topics(bank) != original_count + 1:
        raise AssertionError("topic importance add did not increase count")
    assert_topic_exists(bank, target_id, "label", "[CRUD TEST] Topic Importance")

    entry["label"] = "[CRUD TEST] Topic Importance Updated"
    write_json(cand, entry)

    run(
        "promote-topic-importance",
        "--candidate", str(cand),
        "--bank", str(bank),
        "--replace",
        *maybe_no_backup("promote-topic-importance"),
    )
    run("validate-topic-importance", "--bank", str(bank))

    if count_topics(bank) != original_count + 1:
        raise AssertionError("topic importance update created duplicate")
    assert_topic_exists(bank, target_id, "label", "[CRUD TEST] Topic Importance Updated")

    run(
        "delete-topic-importance",
        "--topic-id", target_id,
        "--bank", str(bank),
        *maybe_no_backup("delete-topic-importance"),
    )
    run("validate-topic-importance", "--bank", str(bank))

    if count_topics(bank) != original_count:
        raise AssertionError("topic importance delete did not restore count")
    assert_topic_not_exists(bank, target_id)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rubric_crud_test_") as d:
        tmp = Path(d)
        print("temp:", tmp)

        test_model_answer(tmp)
        test_fact_anchor(tmp)
        test_topic_importance(tmp)

    print("\nCRUD TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
