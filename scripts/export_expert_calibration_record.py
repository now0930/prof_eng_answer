from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from expert_calibration_dataset import (
    CalibrationContractError,
    build_draft_record,
    load_jsonl,
    validate_dataset,
    write_jsonl_atomic,
)


DEFAULT_FACT_ANCHOR_BANK = Path(
    "rubrics/generated/fact_anchors.generated.json"
)

GENERIC_TOPIC_KEYS = {
    "anchors",
    "fact_anchors",
    "items",
    "topics",
    "entries",
    "data",
}

TOPIC_ID_KEYS = (
    "topic_id",
    "canonical_topic",
    "selected_topic_id",
    "source_topic_id",
)


class ExpertCalibrationExportError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        canonical_json(value).encode("utf-8")
    ).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except FileNotFoundError as error:
        raise ExpertCalibrationExportError(
            f"required file missing: {path.name}"
        ) from error
    except json.JSONDecodeError as error:
        raise ExpertCalibrationExportError(
            f"invalid JSON: {path.name}"
        ) from error


def session_fingerprint(
    session_dir: Path,
) -> dict[str, str]:
    if not session_dir.is_dir():
        raise ExpertCalibrationExportError(
            "source session directory does not exist"
        )

    output = {}

    for path in sorted(session_dir.iterdir()):
        if not path.is_file():
            continue

        output[path.name] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

    return output


def split_question_answer(
    session_dir: Path,
) -> tuple[str, str, str]:
    raw_input = (
        session_dir / "input.txt"
    ).read_text(encoding="utf-8")

    fact = read_json(
        session_dir
        / "fact_anchor_evaluation.json"
    )

    if not isinstance(fact, dict):
        raise ExpertCalibrationExportError(
            "fact_anchor_evaluation.json "
            "must contain an object"
        )

    question = str(
        fact.get("question_text") or ""
    ).strip()

    if not question:
        raise ExpertCalibrationExportError(
            "fact anchor question_text missing"
        )

    if not raw_input.startswith(question):
        raise ExpertCalibrationExportError(
            "input.txt does not start with "
            "the exact fact anchor question_text"
        )

    answer = raw_input[len(question):].lstrip(
        "\r\n "
    )

    if not answer:
        raise ExpertCalibrationExportError(
            "answer text is empty after "
            "question prefix removal"
        )

    return (
        question,
        answer,
        "fact_anchor_exact_question_prefix",
    )


def extract_question_type(
    grade: dict[str, Any],
) -> tuple[str, str]:
    candidates = [
        (
            grade.get("question_type"),
            "grade.question_type",
        ),
        (
            (
                grade.get("question_type_v2")
                or {}
            ).get("question_type"),
            "grade.question_type_v2.question_type",
        ),
        (
            (
                (
                    grade.get(
                        "question_type_evaluation"
                    )
                    or {}
                ).get("primary_type")
                or {}
            ).get("id"),
            (
                "grade.question_type_evaluation."
                "primary_type.id"
            ),
        ),
        (
            (
                (
                    (
                        grade.get(
                            "gemini_semantic_evaluation"
                        )
                        or {}
                    ).get("parsed")
                    or {}
                ).get("question_type")
            ),
            (
                "grade.gemini_semantic_evaluation."
                "parsed.question_type"
            ),
        ),
    ]

    for value, source in candidates:
        if isinstance(value, dict):
            value = (
                value.get("id")
                or value.get("question_type")
                or value.get("type")
            )

        if isinstance(value, str) and value.strip():
            return value.strip(), source

    raise ExpertCalibrationExportError(
        "question type could not be resolved"
    )


def extract_model_total(
    grade: dict[str, Any],
) -> tuple[float, str]:
    for key in (
        "total_score",
        "final_total_score",
        "score",
        "final_score",
    ):
        value = grade.get(key)

        if isinstance(value, bool):
            continue

        if isinstance(value, (int, float)):
            return float(value), f"grade.{key}"

    raise ExpertCalibrationExportError(
        "model total score could not be resolved"
    )


def extract_model_breakdown(
    grade: dict[str, Any],
) -> tuple[dict[str, float], str]:
    value = grade.get("breakdown")

    if isinstance(value, list):
        output = {}

        for item in value:
            if not isinstance(item, dict):
                continue

            layer = str(
                item.get("layer_id") or ""
            ).strip()
            score = item.get("score")

            if (
                layer in {"A", "B", "C", "D", "E"}
                and isinstance(score, (int, float))
                and not isinstance(score, bool)
            ):
                output[layer] = float(score)

        if set(output) == {
            "A",
            "B",
            "C",
            "D",
            "E",
        }:
            return output, "grade.breakdown"

    if isinstance(value, dict):
        output = {}

        for layer in ("A", "B", "C", "D", "E"):
            score = value.get(layer)

            if isinstance(score, dict):
                score = score.get("score")

            if (
                not isinstance(score, (int, float))
                or isinstance(score, bool)
            ):
                break

            output[layer] = float(score)

        if set(output) == {
            "A",
            "B",
            "C",
            "D",
            "E",
        }:
            return output, "grade.breakdown"

    raise ExpertCalibrationExportError(
        "A/B/C/D/E model breakdown "
        "could not be resolved"
    )


def extract_session_anchor_ids(
    session_dir: Path,
) -> set[str]:
    fact = read_json(
        session_dir
        / "fact_anchor_evaluation.json"
    )

    if not isinstance(fact, dict):
        raise ExpertCalibrationExportError(
            "fact anchor evaluation must be object"
        )

    anchors = fact.get("anchors")

    if not isinstance(anchors, list):
        raise ExpertCalibrationExportError(
            "fact anchor list missing"
        )

    output = {
        str(item.get("id")).strip()
        for item in anchors
        if (
            isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and item.get("id").strip()
        )
    }

    if not output:
        raise ExpertCalibrationExportError(
            "session fact anchor IDs missing"
        )

    return output


def _anchor_ids_from_collection(
    value: Any,
) -> set[str]:
    output: set[str] = set()

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                anchor_id = item.get("id")

                if (
                    isinstance(anchor_id, str)
                    and anchor_id.strip()
                ):
                    output.add(anchor_id.strip())

                output.update(
                    _anchor_ids_from_collection(item)
                )

    elif isinstance(value, dict):
        anchor_id = value.get("id")

        if (
            isinstance(anchor_id, str)
            and anchor_id.strip()
        ):
            output.add(anchor_id.strip())

        for child in value.values():
            output.update(
                _anchor_ids_from_collection(child)
            )

    return output


def collect_topic_anchor_map(
    bank: Any,
) -> dict[str, set[str]]:
    candidates: dict[str, set[str]] = {}

    def add(
        topic_id: Any,
        anchor_ids: Iterable[str],
    ) -> None:
        if (
            not isinstance(topic_id, str)
            or not topic_id.strip()
        ):
            return

        topic = topic_id.strip()
        ids = {
            anchor_id
            for anchor_id in anchor_ids
            if anchor_id
        }

        if not ids:
            return

        candidates.setdefault(
            topic,
            set(),
        ).update(ids)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            direct_ids: set[str] = set()

            for key in ("anchors", "fact_anchors"):
                if key in value:
                    direct_ids.update(
                        _anchor_ids_from_collection(
                            value[key]
                        )
                    )

            explicit_topic = None

            for key in (
                "topic_id",
                "canonical_topic",
                "selected_topic_id",
                "source_topic_id",
            ):
                candidate = value.get(key)

                if (
                    isinstance(candidate, str)
                    and candidate.strip()
                ):
                    explicit_topic = candidate.strip()
                    break

            if explicit_topic and direct_ids:
                add(explicit_topic, direct_ids)

            for key, child in value.items():
                if (
                    isinstance(key, str)
                    and key not in GENERIC_TOPIC_KEYS
                    and "_" in key
                ):
                    child_ids = (
                        _anchor_ids_from_collection(
                            child
                        )
                    )

                    if child_ids:
                        add(key, child_ids)

                walk(child)

        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(bank)

    return candidates


def _explicit_topic_from_value(
    value: Any,
) -> str | None:
    found: list[str] = []

    def walk(current: Any) -> None:
        if isinstance(current, dict):
            for key, child in current.items():
                if (
                    str(key).lower()
                    in TOPIC_ID_KEYS
                    and isinstance(child, str)
                    and child.strip()
                    and child.strip() != "unknown"
                ):
                    found.append(child.strip())

                walk(child)

        elif isinstance(current, list):
            for child in current:
                walk(child)

    walk(value)

    unique = list(dict.fromkeys(found))

    if len(unique) == 1:
        return unique[0]

    return None


def resolve_topic_id(
    session_dir: Path,
    *,
    question_text: str,
    answer_text: str,
    fact_anchor_bank_path: Path,
    override: str | None = None,
) -> tuple[str, str, dict[str, int]]:
    if override:
        return (
            override.strip(),
            "manual_override",
            {},
        )

    for name in (
        "grade.json",
        "fact_anchor_evaluation.json",
        "model_answer_reference.json",
        "question_contract.json",
    ):
        path = session_dir / name

        if not path.exists():
            continue

        explicit = _explicit_topic_from_value(
            read_json(path)
        )

        if explicit:
            return (
                explicit,
                f"session_explicit:{name}",
                {},
            )

    session_anchor_ids = (
        extract_session_anchor_ids(
            session_dir
        )
    )
    bank = read_json(
        fact_anchor_bank_path
    )
    topic_map = collect_topic_anchor_map(bank)

    overlap = {
        topic_id: len(
            session_anchor_ids
            & anchor_ids
        )
        for topic_id, anchor_ids
        in topic_map.items()
    }
    overlap = {
        topic_id: score
        for topic_id, score in overlap.items()
        if score > 0
    }

    if overlap:
        ranked = sorted(
            overlap.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )
        top_topic, top_score = ranked[0]
        second_score = (
            ranked[1][1]
            if len(ranked) > 1
            else 0
        )

        if top_score > second_score:
            return (
                top_topic,
                "generated_bank_anchor_overlap",
                overlap,
            )

    try:
        import grading_agents

        subject_path = (
            session_dir
            / "subject_rubric_snapshot.json"
        )

        if subject_path.exists():
            subject_rubric = read_json(
                subject_path
            )
            result = (
                grading_agents
                ._phase3_select_fact_anchors_from_bank(
                    question_text,
                    answer_text,
                    subject_rubric,
                )
            )
            explicit = _explicit_topic_from_value(
                result
            )

            if explicit:
                return (
                    explicit,
                    "current_phase3_selector",
                    overlap,
                )

    except Exception:
        pass

    raise ExpertCalibrationExportError(
        "topic ID could not be resolved "
        "without a manual --topic-id override"
    )


def rubric_snapshot_hash(
    session_dir: Path,
) -> tuple[str, str]:
    path = session_dir / "rubric_snapshot.json"
    value = read_json(path)

    return (
        canonical_sha256(value),
        "canonical_json:rubric_snapshot.json",
    )


def build_draft_from_session(
    session_dir: Path,
    *,
    fact_anchor_bank_path: Path = (
        DEFAULT_FACT_ANCHOR_BANK
    ),
    topic_id_override: str | None = None,
    record_id: str | None = None,
    extra_notes: str = "",
) -> tuple[dict[str, Any], dict[str, Any]]:
    session_dir = session_dir.expanduser().resolve()
    before = session_fingerprint(session_dir)

    grade = read_json(
        session_dir / "grade.json"
    )

    if not isinstance(grade, dict):
        raise ExpertCalibrationExportError(
            "grade.json must contain an object"
        )

    (
        question_text,
        answer_text,
        split_source,
    ) = split_question_answer(session_dir)

    question_type, question_type_source = (
        extract_question_type(grade)
    )
    model_total, total_source = (
        extract_model_total(grade)
    )
    model_breakdown, breakdown_source = (
        extract_model_breakdown(grade)
    )
    topic_id, topic_source, overlap = (
        resolve_topic_id(
            session_dir,
            question_text=question_text,
            answer_text=answer_text,
            fact_anchor_bank_path=(
                fact_anchor_bank_path
            ),
            override=topic_id_override,
        )
    )
    rubric_hash, rubric_source = (
        rubric_snapshot_hash(session_dir)
    )

    note_payload = {
        "source_session": session_dir.name,
        "question_answer_source": split_source,
        "topic_source": topic_source,
        "question_type_source": (
            question_type_source
        ),
        "model_total_source": total_source,
        "model_breakdown_source": (
            breakdown_source
        ),
        "rubric_snapshot_source": rubric_source,
        "anchor_overlap": overlap,
    }

    if extra_notes:
        note_payload["operator_notes"] = (
            extra_notes
        )

    record = build_draft_record(
        record_id=(
            record_id
            or f"session-{session_dir.name}"
        ),
        question_text=question_text,
        answer_text=answer_text,
        topic_id=topic_id,
        question_type=question_type,
        rubric_snapshot_hash=rubric_hash,
        model_total_score=model_total,
        model_breakdown=model_breakdown,
        notes=canonical_json(note_payload),
    )

    after = session_fingerprint(session_dir)

    if after != before:
        raise ExpertCalibrationExportError(
            "source session changed during export"
        )

    diagnostics = {
        "source_session": str(session_dir),
        "question_answer_source": split_source,
        "topic_source": topic_source,
        "question_type_source": (
            question_type_source
        ),
        "model_total_source": total_source,
        "model_breakdown_source": (
            breakdown_source
        ),
        "rubric_snapshot_source": rubric_source,
        "anchor_overlap": overlap,
        "source_session_unchanged": True,
    }

    return record, diagnostics


def export_draft_record(
    session_dir: Path,
    output_path: Path,
    *,
    fact_anchor_bank_path: Path = (
        DEFAULT_FACT_ANCHOR_BANK
    ),
    topic_id_override: str | None = None,
    record_id: str | None = None,
    extra_notes: str = "",
    replace_existing: bool = False,
) -> dict[str, Any]:
    record, diagnostics = (
        build_draft_from_session(
            session_dir,
            fact_anchor_bank_path=(
                fact_anchor_bank_path
            ),
            topic_id_override=(
                topic_id_override
            ),
            record_id=record_id,
            extra_notes=extra_notes,
        )
    )

    output_path = output_path.expanduser()
    existing = (
        load_jsonl(output_path)
        if output_path.exists()
        else []
    )

    if replace_existing:
        existing = [
            item
            for item in existing
            if (
                item.get("record_id")
                != record["record_id"]
                and item.get("submission_hash")
                != record["submission_hash"]
            )
        ]

    records = existing + [record]
    report = write_jsonl_atomic(
        output_path,
        records,
    )
    validated = validate_dataset(records)

    return {
        "ok": True,
        "output_path": str(
            output_path.resolve()
        ),
        "record": record,
        "diagnostics": diagnostics,
        "dataset_report": {
            key: value
            for key, value in report.items()
        },
        "validated_record_count": (
            validated["record_count"]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export one grading session as "
            "an offline expert calibration "
            "draft record."
        )
    )
    parser.add_argument(
        "session_dir",
        type=Path,
    )
    parser.add_argument(
        "output_jsonl",
        type=Path,
    )
    parser.add_argument(
        "--fact-anchor-bank",
        type=Path,
        default=DEFAULT_FACT_ANCHOR_BANK,
    )
    parser.add_argument(
        "--topic-id",
        default=None,
    )
    parser.add_argument(
        "--record-id",
        default=None,
    )
    parser.add_argument(
        "--notes",
        default="",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
    )

    args = parser.parse_args()

    try:
        result = export_draft_record(
            args.session_dir,
            args.output_jsonl,
            fact_anchor_bank_path=(
                args.fact_anchor_bank
            ),
            topic_id_override=args.topic_id,
            record_id=args.record_id,
            extra_notes=args.notes,
            replace_existing=(
                args.replace_existing
            ),
        )

    except (
        CalibrationContractError,
        ExpertCalibrationExportError,
        OSError,
    ) as error:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(error),
                    "production_calibration_enabled": (
                        False
                    ),
                    "score_effect": "none",
                    "direct_score_application": (
                        False
                    ),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
