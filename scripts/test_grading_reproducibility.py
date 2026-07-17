from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import shutil
import statistics
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import bot
import grading_agents
from grade_score_reconciler import (
    reconcile_grade_score,
)
from grading_identity import (
    build_grading_identity,
)


VERSION = "p0_grading_reproducibility_gate_v2"

EXPECTED_QUESTION_HASH = (
    "886f1b0603bf03dd582b23dcaac8c39a"
    "0ad288e5dc71efec1a3fd65abebea572"
)
EXPECTED_SUBMISSION_HASH = (
    "5f56603fe845f93191a0cabbe7e61d06"
    "d130dad07e41e47dfa7c7b430746bdd9"
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_json(value: Any) -> str:
    return hashlib.sha256(
        canonical_json(value).encode("utf-8")
    ).hexdigest()


def first_value(
    mapping: Any,
    keys: list[str],
    default: Any = None,
) -> Any:
    if not isinstance(mapping, dict):
        return default

    for key in keys:
        value = mapping.get(key)

        if value not in (
            None,
            "",
            [],
            {},
        ):
            return value

    return default


def locate_incident_session(
    session_root: Path,
) -> tuple[Path, str, dict[str, Any]]:
    matches: list[
        tuple[float, Path, str, dict[str, Any]]
    ] = []

    for input_path in session_root.glob(
        "*/input.txt"
    ):
        try:
            raw_text = input_path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            continue

        question_text = (
            grading_agents
            ._phase3_extract_question_text(
                raw_text
            )
        )
        answer_text = (
            grading_agents
            ._phase3_extract_answer_text(
                raw_text
            )
        )

        identity = build_grading_identity(
            question_text=question_text,
            answer_text=answer_text,
        )

        if (
            identity.question_hash
            != EXPECTED_QUESTION_HASH
            or identity.submission_hash
            != EXPECTED_SUBMISSION_HASH
        ):
            continue

        matches.append(
            (
                input_path.stat().st_mtime,
                input_path.parent,
                raw_text,
                identity.to_dict(),
            )
        )

    if not matches:
        raise RuntimeError(
            "Exact incident submission was not found"
        )

    matches.sort(
        key=lambda row: row[0],
        reverse=True,
    )

    _, session_dir, raw_text, identity = (
        matches[0]
    )

    return session_dir, raw_text, identity


def collect_anchor_ids(
    value: Any,
    path: tuple[str, ...] = (),
) -> set[str]:
    output: set[str] = set()

    if isinstance(value, dict):
        for key, item in value.items():
            lowered = key.lower()
            child_path = path + (lowered,)

            if (
                "anchor" in lowered
                and isinstance(item, list)
            ):
                for candidate in item:
                    if isinstance(
                        candidate,
                        (str, int),
                    ):
                        text = str(candidate).strip()

                        if text:
                            output.add(text)

            if (
                lowered
                in {
                    "anchor_id",
                    "fact_anchor_id",
                }
                and isinstance(
                    item,
                    (str, int),
                )
            ):
                text = str(item).strip()

                if text:
                    output.add(text)

            if (
                lowered == "id"
                and any(
                    "anchor" in element
                    for element in child_path
                )
                and isinstance(
                    item,
                    (str, int),
                )
            ):
                text = str(item).strip()

                if text:
                    output.add(text)

            output.update(
                collect_anchor_ids(
                    item,
                    child_path,
                )
            )

    elif isinstance(value, list):
        for item in value:
            output.update(
                collect_anchor_ids(
                    item,
                    path,
                )
            )

    return output


def collect_logic_finding_ids(
    value: Any,
    path: tuple[str, ...] = (),
) -> set[str]:
    output: set[str] = set()

    if isinstance(value, dict):
        for key, item in value.items():
            lowered = key.lower()
            child_path = path + (lowered,)

            if (
                lowered
                in {
                    "finding_id",
                    "logic_finding_id",
                    "check_id",
                    "rule_id",
                }
                and isinstance(
                    item,
                    (str, int),
                )
            ):
                text = str(item).strip()

                if text:
                    output.add(text)

            if (
                lowered == "id"
                and any(
                    token in element
                    for element in child_path
                    for token in (
                        "finding",
                        "violation",
                        "logic",
                    )
                )
                and isinstance(
                    item,
                    (str, int),
                )
            ):
                text = str(item).strip()

                if text:
                    output.add(text)

            output.update(
                collect_logic_finding_ids(
                    item,
                    child_path,
                )
            )

    elif isinstance(value, list):
        for item in value:
            output.update(
                collect_logic_finding_ids(
                    item,
                    path,
                )
            )

    return output


def numeric_value(value: Any) -> float | None:
    if isinstance(value, bool):
        return None

    try:
        converted = float(value)
    except Exception:
        return None

    if not math.isfinite(converted):
        return None

    return converted


def extract_layer_scores(
    grade: dict[str, Any],
) -> dict[str, float | None]:
    output: dict[str, float | None] = {
        layer: None
        for layer in "ABCDE"
    }

    direct = grade.get("layer_scores")

    if isinstance(direct, dict):
        for layer in output:
            value = numeric_value(
                direct.get(layer)
            )

            if value is not None:
                output[layer] = value

    breakdown = grade.get("breakdown")

    if not isinstance(breakdown, list):
        return output

    for item in breakdown:
        if not isinstance(item, dict):
            continue

        label = str(
            first_value(
                item,
                [
                    "layer",
                    "layer_id",
                    "code",
                    "id",
                    "name",
                    "title",
                ],
                "",
            )
        ).strip()

        layer = ""

        for candidate in "ABCDE":
            if (
                label == candidate
                or label.startswith(
                    candidate + "."
                )
                or label.startswith(
                    candidate + " "
                )
                or label.startswith(
                    candidate + "-"
                )
            ):
                layer = candidate
                break

        if not layer:
            continue

        for key in [
            "final_score",
            "adjusted_score",
            "weighted_score",
            "earned_points",
            "score",
            "points",
            "value",
        ]:
            value = numeric_value(
                item.get(key)
            )

            if value is not None:
                output[layer] = value
                break

    return output


def request_summary(
    evaluation: Any,
) -> dict[str, Any]:
    if not isinstance(evaluation, dict):
        return {
            "provider": None,
            "model": None,
            "prompt_hash": None,
            "request_hash": None,
            "applied_sampling": {},
            "unsupported_settings": [],
        }

    request = evaluation.get("llm_request")

    if not isinstance(request, dict):
        request = {}

    return {
        "provider": request.get("provider"),
        "model": request.get("model"),
        "prompt_hash": request.get(
            "prompt_hash"
        ),
        "request_hash": request.get(
            "request_hash"
        ),
        "applied_sampling": request.get(
            "applied_sampling"
        )
        if isinstance(
            request.get("applied_sampling"),
            dict,
        )
        else {},
        "unsupported_settings": (
            request.get(
                "unsupported_settings"
            )
            if isinstance(
                request.get(
                    "unsupported_settings"
                ),
                list,
            )
            else []
        ),
    }


def run_full_grade(
    *,
    run_index: int,
    raw_text: str,
    rubric: dict[str, Any],
    image_count: int,
    temp_root: Path,
) -> tuple[dict[str, Any], str]:
    run_sid = (
        f"p0_repro_gate_run_"
        f"{run_index:02d}"
    )
    run_dir = temp_root / run_sid

    run_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    input_path = run_dir / "input.txt"
    input_path.write_text(
        raw_text,
        encoding="utf-8",
    )

    original_latest = (
        grading_agents
        ._phase2_latest_session_dir
    )

    grading_agents._phase2_latest_session_dir = (
        lambda: run_dir
    )

    try:
        raw_result, parsed = (
            grading_agents.run_agent_pipeline(
                call_ollama_fn=bot.call_ollama,
                raw_text=raw_text,
                rubric=copy.deepcopy(rubric),
                sid=run_sid,
                image_count=image_count,
                session_dir=run_dir,
            )
        )
    finally:
        grading_agents._phase2_latest_session_dir = (
            original_latest
        )

    if not isinstance(parsed, dict):
        raise RuntimeError(
            "Full grading pipeline did not "
            "return a grade dictionary"
        )

    parsed = reconcile_grade_score(
        parsed=parsed,
        raw_text=raw_text,
        call_llm_fn=(
            bot.call_ollama_score_adjudicator
        ),
    )

    parsed["backend"] = "ollama"
    parsed["model"] = bot.OLLAMA_MODEL

    grade_path = run_dir / "grade.json"
    grade_path.write_text(
        json.dumps(
            parsed,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return parsed, str(raw_result or "")


def summarize_run(
    *,
    run_index: int,
    grade: dict[str, Any],
    raw_result: str,
    duration_seconds: float,
) -> dict[str, Any]:
    identity = (
        grade.get("grading_identity")
        if isinstance(
            grade.get("grading_identity"),
            dict,
        )
        else {}
    )

    question_type_eval = (
        grade.get(
            "question_type_evaluation"
        )
        if isinstance(
            grade.get(
                "question_type_evaluation"
            ),
            dict,
        )
        else {}
    )

    fact_eval = (
        grade.get(
            "fact_anchor_evaluation"
        )
        if isinstance(
            grade.get(
                "fact_anchor_evaluation"
            ),
            dict,
        )
        else {}
    )

    model_ref = (
        grade.get(
            "model_answer_reference"
        )
        if isinstance(
            grade.get(
                "model_answer_reference"
            ),
            dict,
        )
        else {}
    )

    logic_eval = (
        grade.get(
            "logic_check_evaluation"
        )
        if isinstance(
            grade.get(
                "logic_check_evaluation"
            ),
            dict,
        )
        else {}
    )

    semantic_eval = (
        grade.get(
            "gemini_semantic_evaluation"
        )
        if isinstance(
            grade.get(
                "gemini_semantic_evaluation"
            ),
            dict,
        )
        else {}
    )

    originality_eval = (
        grade.get(
            "originality_evaluation"
        )
        if isinstance(
            grade.get(
                "originality_evaluation"
            ),
            dict,
        )
        else {}
    )

    cap_eval = (
        grade.get(
            "llm_cap_adjudication"
        )
        if isinstance(
            grade.get(
                "llm_cap_adjudication"
            ),
            dict,
        )
        else {}
    )

    question_type_value = first_value(
        question_type_eval,
        [
            "question_type",
            "type",
            "lens",
            "primary_type",
        ],
        grade.get(
            "question_type",
            "",
        ),
    )

    if isinstance(
        question_type_value,
        dict,
    ):
        question_type_value = first_value(
            question_type_value,
            [
                "id",
                "question_type",
                "type",
            ],
            "",
        )

    question_type = str(
        question_type_value or ""
    )

    question_type_status = str(
        first_value(
            question_type_eval,
            [
                "status",
                "classification_status",
            ],
            "",
        )
        or ""
    )

    question_type_locked = bool(
        first_value(
            question_type_eval,
            [
                "question_type_locked",
                "locked",
                "is_locked",
            ],
            False,
        )
    )

    topic_id = str(
        first_value(
            grade,
            [
                "logic_check_topic_id",
                "topic_id",
                "inferred_topic_id",
            ],
            "",
        )
        or first_value(
            model_ref,
            [
                "topic_id",
                "selected_topic_id",
                "matched_topic_id",
            ],
            "",
        )
        or first_value(
            fact_eval,
            [
                "topic_id",
                "selected_topic_id",
                "matched_topic_id",
            ],
            "",
        )
        or ""
    )

    anchor_ids = sorted(
        collect_anchor_ids(fact_eval)
    )

    logic_finding_ids = sorted(
        collect_logic_finding_ids(
            logic_eval
        )
    )

    logic_verdict = str(
        first_value(
            logic_eval,
            [
                "verdict",
                "status",
                "result",
                "mode",
            ],
            "",
        )
        or ""
    )

    semantic_request = request_summary(
        semantic_eval
    )
    originality_request = request_summary(
        originality_eval
    )
    cap_request = request_summary(
        cap_eval
    )

    contract_payload = {
        "normalization_version": (
            identity.get(
                "normalization_version"
            )
        ),
        "question_hash": identity.get(
            "question_hash"
        ),
        "submission_hash": identity.get(
            "submission_hash"
        ),
        "question_type": question_type,
        "question_type_status": (
            question_type_status
        ),
        "question_type_locked": (
            question_type_locked
        ),
        "topic_id": topic_id,
        "anchor_ids": anchor_ids,
        "semantic_provider": (
            semantic_request["provider"]
        ),
        "semantic_model": (
            semantic_request["model"]
        ),
        "semantic_sampling": (
            semantic_request[
                "applied_sampling"
            ]
        ),
        "semantic_prompt_hash": (
            semantic_request[
                "prompt_hash"
            ]
        ),
        "semantic_request_hash": (
            semantic_request[
                "request_hash"
            ]
        ),
        "originality_provider": (
            originality_request["provider"]
        ),
        "originality_model": (
            originality_request["model"]
        ),
        "originality_sampling": (
            originality_request[
                "applied_sampling"
            ]
        ),
    }

    layer_scores = extract_layer_scores(
        grade
    )

    total_score = numeric_value(
        grade.get("total_score")
    )

    errors: list[str] = []

    if (
        identity.get("question_hash")
        != EXPECTED_QUESTION_HASH
    ):
        errors.append(
            "question_hash mismatch"
        )

    if (
        identity.get("submission_hash")
        != EXPECTED_SUBMISSION_HASH
    ):
        errors.append(
            "submission_hash mismatch"
        )

    if not question_type:
        errors.append(
            "question_type missing"
        )

    if not topic_id:
        errors.append(
            "topic_id missing"
        )

    if total_score is None:
        errors.append(
            "total_score missing"
        )

    if not raw_result.strip():
        errors.append(
            "base Ollama result empty"
        )

    if semantic_eval.get("ok") is not True:
        errors.append(
            "Gemini semantic evaluation failed"
        )

    if originality_eval.get("ok") is not True:
        errors.append(
            "Gemini originality evaluation failed"
        )

    if not semantic_request.get(
        "request_hash"
    ):
        errors.append(
            "semantic request_hash missing"
        )

    if not originality_request.get(
        "request_hash"
    ):
        errors.append(
            "originality request_hash missing"
        )

    if cap_eval and not cap_request.get(
        "request_hash"
    ):
        errors.append(
            "cap adjudication request_hash missing"
        )

    return {
        "run": run_index,
        "duration_seconds": round(
            duration_seconds,
            3,
        ),
        "question_hash": identity.get(
            "question_hash"
        ),
        "submission_hash": identity.get(
            "submission_hash"
        ),
        "normalization_version": (
            identity.get(
                "normalization_version"
            )
        ),
        "question_type": question_type,
        "question_type_confidence": (
            first_value(
                question_type_eval,
                ["confidence"],
                None,
            )
        ),
        "question_type_status": (
            question_type_status
        ),
        "question_type_locked": (
            question_type_locked
        ),
        "question_type_source": (
            first_value(
                question_type_eval,
                ["source"],
                None,
            )
        ),
        "topic_id": topic_id,
        "anchor_ids": anchor_ids,
        "logic_verdict": logic_verdict,
        "logic_fatal": bool(
            logic_eval.get(
                "fatal_error_detected"
            )
        ),
        "logic_finding_ids": (
            logic_finding_ids
        ),
        "semantic_ok": (
            semantic_eval.get("ok")
        ),
        "semantic_request": (
            semantic_request
        ),
        "originality_ok": (
            originality_eval.get("ok")
        ),
        "originality_request": (
            originality_request
        ),
        "cap_adjudication_used": bool(
            cap_eval
        ),
        "cap_request": cap_request,
        "layer_scores": layer_scores,
        "total_score": total_score,
        "contract_payload": (
            contract_payload
        ),
        "contract_signature": sha256_json(
            contract_payload
        ),
        "errors": errors,
    }


def markdown_report(
    report: dict[str, Any],
) -> str:
    criteria = report["criteria"]

    lines = [
        "# P0 Grading Reproducibility Gate",
        "",
        f"- Version: `{report['version']}`",
        (
            "- Generated: "
            f"`{report['generated_at_utc']}`"
        ),
        (
            "- Incident session: "
            f"`{report['source_session']}`"
        ),
        (
            "- Cache bypass: "
            f"`{str(report['cache_bypass']).lower()}`"
        ),
        (
            "- Score averaging: "
            f"`{str(report['score_averaging']).lower()}`"
        ),
        (
            "- Ensemble scoring: "
            f"`{str(report['ensemble_scoring']).lower()}`"
        ),
        "",
        "## Result",
        "",
        (
            f"**{'PASS' if report['pass'] else 'FAIL'}**"
        ),
        "",
        "| Criterion | Result | Required | Pass |",
        "|---|---:|---:|:---:|",
        (
            "| Completed runs | "
            f"{criteria['completed_runs']['actual']} | "
            f"{criteria['completed_runs']['required']} | "
            f"{'PASS' if criteria['completed_runs']['pass'] else 'FAIL'} |"
        ),
        (
            "| Question type distinct | "
            f"{criteria['question_type_distinct']['actual']} | "
            f"{criteria['question_type_distinct']['required']} | "
            f"{'PASS' if criteria['question_type_distinct']['pass'] else 'FAIL'} |"
        ),
        (
            "| Contract signature distinct | "
            f"{criteria['contract_signature_distinct']['actual']} | "
            f"{criteria['contract_signature_distinct']['required']} | "
            f"{'PASS' if criteria['contract_signature_distinct']['pass'] else 'FAIL'} |"
        ),
        (
            "| Semantic request hash distinct | "
            f"{criteria['semantic_request_hash_distinct']['actual']} | "
            f"{criteria['semantic_request_hash_distinct']['required']} | "
            f"{'PASS' if criteria['semantic_request_hash_distinct']['pass'] else 'FAIL'} |"
        ),
        (
            "| Total score stddev | "
            f"{criteria['total_score_stddev']['actual']} | "
            f"≤ {criteria['total_score_stddev']['maximum']} | "
            f"{'PASS' if criteria['total_score_stddev']['pass'] else 'FAIL'} |"
        ),
        (
            "| Run errors | "
            f"{criteria['run_errors']['actual']} | "
            f"{criteria['run_errors']['required']} | "
            f"{'PASS' if criteria['run_errors']['pass'] else 'FAIL'} |"
        ),
        "",
        "## Runs",
        "",
        (
            "| Run | Score | A | B | C | D | E | "
            "Question type | Status | Topic | "
            "Logic | Semantic hash | Originality hash | Errors |"
        ),
        (
            "|---:|---:|---:|---:|---:|---:|---:|"
            "---|---|---|---|---|---|---|"
        ),
    ]

    for run in report["runs"]:
        layer = run["layer_scores"]
        errors = "; ".join(
            run["errors"]
        )

        semantic_hash = str(
            run["semantic_request"].get(
                "request_hash"
            )
            or ""
        )[:12]

        originality_hash = str(
            run["originality_request"].get(
                "request_hash"
            )
            or ""
        )[:12]

        lines.append(
            "| "
            f"{run['run']} | "
            f"{run['total_score']} | "
            f"{layer.get('A')} | "
            f"{layer.get('B')} | "
            f"{layer.get('C')} | "
            f"{layer.get('D')} | "
            f"{layer.get('E')} | "
            f"{run['question_type']} | "
            f"{run['question_type_status']} | "
            f"{run['topic_id']} | "
            f"{run['logic_verdict']} | "
            f"{semantic_hash} | "
            f"{originality_hash} | "
            f"{errors} |"
        )

    lines.extend(
        [
            "",
            "## Score statistics",
            "",
            (
                "- Scores: "
                f"`{report['score_statistics']['scores']}`"
            ),
            (
                "- Minimum: "
                f"`{report['score_statistics']['minimum']}`"
            ),
            (
                "- Maximum: "
                f"`{report['score_statistics']['maximum']}`"
            ),
            (
                "- Mean: "
                f"`{report['score_statistics']['mean']}`"
            ),
            (
                "- Population standard deviation: "
                f"`{report['score_statistics']['pstdev']}`"
            ),
            "",
            "## Notes",
            "",
            (
                "- Each run used a new temporary "
                "session directory."
            ),
            (
                "- Existing grade/session cache "
                "results were not reused."
            ),
            (
                "- Scores were recorded individually. "
                "No averaging or ensemble result was "
                "used as a final score."
            ),
            (
                "- The production scoring pipeline and "
                "post-pipeline cap reconciliation were "
                "both executed."
            ),
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--runs",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    if args.runs != 10:
        raise RuntimeError(
            "P0 Gate requires exactly 10 runs"
        )

    source_session, raw_text, identity = (
        locate_incident_session(
            Path("data/sessions")
        )
    )

    meta_path = source_session / "meta.json"
    image_count = 0

    if meta_path.exists():
        try:
            meta = json.loads(
                meta_path.read_text(
                    encoding="utf-8"
                )
            )

            images = meta.get("images")

            if isinstance(images, list):
                image_count = len(images)
        except Exception:
            image_count = 0

    rubric = bot.load_rubric()

    temp_root = Path(
        tempfile.mkdtemp(
            prefix=(
                "prof_eng_answer_"
                "p0_repro_gate_"
            )
        )
    )

    print(
        f"source_session={source_session}",
        flush=True,
    )
    print(
        f"question_hash="
        f"{identity['question_hash']}",
        flush=True,
    )
    print(
        f"submission_hash="
        f"{identity['submission_hash']}",
        flush=True,
    )
    print(
        f"image_count={image_count}",
        flush=True,
    )
    print(
        f"temporary_root={temp_root}",
        flush=True,
    )
    print(
        "cache_bypass=true",
        flush=True,
    )

    runs: list[dict[str, Any]] = []

    for run_index in range(
        1,
        args.runs + 1,
    ):
        started = time.monotonic()

        print(
            f"\n===== FULL GRADE "
            f"{run_index}/{args.runs} =====",
            flush=True,
        )

        try:
            grade, raw_result = run_full_grade(
                run_index=run_index,
                raw_text=raw_text,
                rubric=rubric,
                image_count=image_count,
                temp_root=temp_root,
            )

            summary = summarize_run(
                run_index=run_index,
                grade=grade,
                raw_result=raw_result,
                duration_seconds=(
                    time.monotonic()
                    - started
                ),
            )

        except Exception as error:
            summary = {
                "run": run_index,
                "duration_seconds": round(
                    time.monotonic() - started,
                    3,
                ),
                "question_hash": None,
                "submission_hash": None,
                "normalization_version": None,
                "question_type": "",
                "question_type_confidence": None,
                "question_type_status": "",
                "question_type_locked": False,
                "question_type_source": None,
                "topic_id": "",
                "anchor_ids": [],
                "logic_verdict": "",
                "logic_fatal": False,
                "logic_finding_ids": [],
                "semantic_ok": False,
                "semantic_request": {},
                "originality_ok": False,
                "originality_request": {},
                "cap_adjudication_used": False,
                "cap_request": {},
                "layer_scores": {
                    layer: None
                    for layer in "ABCDE"
                },
                "total_score": None,
                "contract_payload": {},
                "contract_signature": None,
                "errors": [
                    repr(error)
                ],
            }

        runs.append(summary)

        print(
            json.dumps(
                {
                    "run": summary["run"],
                    "total_score": (
                        summary["total_score"]
                    ),
                    "question_type": (
                        summary["question_type"]
                    ),
                    "question_type_status": (
                        summary[
                            "question_type_status"
                        ]
                    ),
                    "topic_id": (
                        summary["topic_id"]
                    ),
                    "contract_signature": (
                        summary[
                            "contract_signature"
                        ]
                    ),
                    "semantic_request_hash": (
                        summary.get(
                            "semantic_request",
                            {},
                        ).get("request_hash")
                    ),
                    "originality_request_hash": (
                        summary.get(
                            "originality_request",
                            {},
                        ).get("request_hash")
                    ),
                    "errors": summary["errors"],
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
            flush=True,
        )

    valid_scores = [
        float(run["total_score"])
        for run in runs
        if run["total_score"] is not None
    ]

    question_types = {
        str(
            run.get("question_type")
            or "<missing>"
        )
        for run in runs
    }

    contract_signatures = {
        str(
            run.get("contract_signature")
            or "<missing>"
        )
        for run in runs
    }

    semantic_request_hashes = {
        str(
            (
                run.get(
                    "semantic_request"
                )
                or {}
            ).get("request_hash")
            or "<missing>"
        )
        for run in runs
    }

    originality_request_hashes = {
        str(
            (
                run.get(
                    "originality_request"
                )
                or {}
            ).get("request_hash")
            or "<missing>"
        )
        for run in runs
    }

    run_error_count = sum(
        1
        for run in runs
        if run["errors"]
    )

    completed_runs = len(
        valid_scores
    )

    if valid_scores:
        minimum = min(valid_scores)
        maximum = max(valid_scores)
        mean = statistics.fmean(
            valid_scores
        )
    else:
        minimum = None
        maximum = None
        mean = None

    if len(valid_scores) >= 2:
        pstdev = statistics.pstdev(
            valid_scores
        )
    elif len(valid_scores) == 1:
        pstdev = 0.0
    else:
        pstdev = None

    completed_pass = (
        completed_runs == args.runs
    )
    question_type_pass = (
        len(question_types) == 1
    )
    contract_pass = (
        len(contract_signatures) == 1
    )
    semantic_request_pass = (
        len(semantic_request_hashes) == 1
        and "<missing>"
        not in semantic_request_hashes
    )
    stddev_pass = (
        pstdev is not None
        and pstdev <= 0.5
    )
    errors_pass = (
        run_error_count == 0
    )

    gate_pass = all(
        [
            completed_pass,
            question_type_pass,
            contract_pass,
            semantic_request_pass,
            stddev_pass,
            errors_pass,
        ]
    )

    report = {
        "version": VERSION,
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "source_session": str(
            source_session
        ),
        "source_identity": identity,
        "runs_requested": args.runs,
        "runs_completed": completed_runs,
        "cache_bypass": True,
        "temporary_session_root": str(
            temp_root
        ),
        "score_averaging": False,
        "ensemble_scoring": False,
        "pass": gate_pass,
        "criteria": {
            "completed_runs": {
                "actual": completed_runs,
                "required": args.runs,
                "pass": completed_pass,
            },
            "question_type_distinct": {
                "actual": len(
                    question_types
                ),
                "required": 1,
                "values": sorted(
                    question_types
                ),
                "pass": question_type_pass,
            },
            "contract_signature_distinct": {
                "actual": len(
                    contract_signatures
                ),
                "required": 1,
                "values": sorted(
                    contract_signatures
                ),
                "pass": contract_pass,
            },
            "semantic_request_hash_distinct": {
                "actual": len(
                    semantic_request_hashes
                ),
                "required": 1,
                "values": sorted(
                    semantic_request_hashes
                ),
                "pass": semantic_request_pass,
            },
            "total_score_stddev": {
                "actual": (
                    round(pstdev, 6)
                    if pstdev is not None
                    else None
                ),
                "maximum": 0.5,
                "pass": stddev_pass,
            },
            "run_errors": {
                "actual": run_error_count,
                "required": 0,
                "pass": errors_pass,
            },
        },
        "score_statistics": {
            "scores": valid_scores,
            "minimum": minimum,
            "maximum": maximum,
            "mean": (
                round(mean, 6)
                if mean is not None
                else None
            ),
            "pstdev": (
                round(pstdev, 6)
                if pstdev is not None
                else None
            ),
        },
        "request_hash_diagnostics": {
            "semantic_request_hash_distinct": (
                len(semantic_request_hashes)
            ),
            "semantic_request_hashes": sorted(
                semantic_request_hashes
            ),
            "originality_request_hash_distinct": (
                len(originality_request_hashes)
            ),
            "originality_request_hashes": sorted(
                originality_request_hashes
            ),
            "originality_hash_policy": (
                "diagnostic_only_when_downstream_"
                "prompt_changes_from_upstream_"
                "semantic_output_variance"
            ),
        },
        "runs": runs,
    }

    args.output_json.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.output_md.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output_json.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    args.output_md.write_text(
        markdown_report(report),
        encoding="utf-8",
    )

    print(
        "\n===== P0 GATE RESULT =====",
        flush=True,
    )
    print(
        json.dumps(
            {
                "pass": gate_pass,
                "runs_completed": (
                    completed_runs
                ),
                "question_type_distinct": (
                    len(question_types)
                ),
                "contract_signature_distinct": (
                    len(contract_signatures)
                ),
                "semantic_request_hash_distinct": (
                    len(semantic_request_hashes)
                ),
                "originality_request_hash_distinct": (
                    len(originality_request_hashes)
                ),
                "total_score_pstdev": (
                    round(pstdev, 6)
                    if pstdev is not None
                    else None
                ),
                "run_errors": run_error_count,
                "scores": valid_scores,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        flush=True,
    )

    if not gate_pass:
        raise AssertionError(
            "P0 reproducibility Gate failed"
        )


if __name__ == "__main__":
    main()
