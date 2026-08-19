# Conservative normalization for grading input.
#
# This module removes transport metadata and nested /grade wrappers while
# preserving technical answer content. It is topic-neutral and idempotent.

from __future__ import annotations

import copy
import hashlib
import inspect
import re
import unicodedata
from typing import Any, Callable

SUBMISSION_NORMALIZATION_VERSION = (
    "grade_submission_normalizer_v1"
)
SUBMISSION_NORMALIZATION_MARKER = (
    "GRADE_SUBMISSION_NORMALIZED_V1"
)

_TIMESTAMP_PREFIX = re.compile(
    r"^\s*\[\d{4}-\d{2}-\d{2}\s+"
    r"(?:(?:오전|오후)\s*)?\d{1,2}:\d{2}\]\s*(.*)$"
)
_SPEAKER_PREFIX = re.compile(
    r"^([^:\n]{1,80}):\s*(.*)$"
)
_GRADE_COMMAND = re.compile(
    r"^\s*/grade(?:\s+.*)?$",
    re.IGNORECASE,
)
_CANCEL_COMMAND = re.compile(
    r"^\s*/cancel\s*$",
    re.IGNORECASE,
)
_END_MARKER = re.compile(r"^\s*끝[.]?\s*$")
_ZERO_WIDTH = re.compile(
    r"[\u200b-\u200d\u2060\ufeff]"
)
_PROTECTED_LABELS = {
    "문제",
    "[문제]",
    "답안",
    "[답안]",
    "배점",
    "주제",
}


def _hash_text(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def _clean_transport_lines(
    raw_text: str,
) -> tuple[list[str], list[str]]:
    events: list[str] = []
    cleaned: list[str] = []
    skip_bot_block = False

    for original_line in raw_text.splitlines():
        line = original_line.rstrip()
        timestamp_match = _TIMESTAMP_PREFIX.match(line)

        if timestamp_match:
            line = timestamp_match.group(1).strip()
            skip_bot_block = False
            events.append("timestamp_prefix_removed")

            if line.casefold().startswith("bot name:"):
                skip_bot_block = True
                events.append("bot_message_removed")
                continue

            speaker_match = _SPEAKER_PREFIX.match(line)
            if speaker_match:
                label = speaker_match.group(1).strip()
                body = speaker_match.group(2)

                if label not in _PROTECTED_LABELS:
                    line = body
                    events.append(
                        "speaker_prefix_removed"
                    )

        elif line.strip().casefold().startswith(
            "bot name:"
        ):
            skip_bot_block = True
            events.append("bot_message_removed")
            continue
        elif skip_bot_block:
            continue

        cleaned.append(line)

    return cleaned, events


def _select_last_grade_segment(
    lines: list[str],
    events: list[str],
) -> list[str]:
    marker_indexes = [
        index
        for index, line in enumerate(lines)
        if _GRADE_COMMAND.match(line)
    ]

    if not marker_indexes:
        return lines

    if len(marker_indexes) > 1:
        events.append(
            "nested_grade_segments_removed"
        )
    else:
        events.append("grade_command_removed")

    return lines[marker_indexes[-1] + 1 :]


def _remove_commands_and_end_markers(
    lines: list[str],
    events: list[str],
) -> list[str]:
    result: list[str] = []

    for line in lines:
        if _GRADE_COMMAND.match(line):
            events.append("grade_command_removed")
            continue
        if _CANCEL_COMMAND.match(line):
            events.append("cancel_command_removed")
            continue
        if _END_MARKER.match(line):
            events.append("end_marker_removed")
            continue
        result.append(line)

    while result and not result[0].strip():
        result.pop(0)

    while result and not result[-1].strip():
        result.pop()

    compact: list[str] = []
    blank_count = 0

    for line in result:
        if not line.strip():
            blank_count += 1
            if blank_count > 2:
                continue
        else:
            blank_count = 0

        compact.append(line.rstrip())

    return compact


def _extract_question_and_answer(
    normalized_text: str,
) -> tuple[str, str]:
    lines = normalized_text.splitlines()
    question_start = None

    for index, line in enumerate(lines):
        if re.match(
            r"^\s*(?:\[문제\]|문제\s*:)",
            line,
        ):
            question_start = index
            break

    if question_start is None:
        return "", normalized_text

    question_line = lines[question_start].strip()
    answer_lines = lines[question_start + 1 :]

    return (
        question_line,
        "\n".join(answer_lines).strip(),
    )


def normalize_grade_submission(
    value: Any,
) -> dict[str, Any]:
    raw_text = "" if value is None else str(value)
    normalized_unicode = unicodedata.normalize(
        "NFKC",
        raw_text,
    )
    normalized_unicode = _ZERO_WIDTH.sub(
        "",
        normalized_unicode,
    )

    lines, events = _clean_transport_lines(
        normalized_unicode
    )
    lines = _select_last_grade_segment(
        lines,
        events,
    )
    lines = _remove_commands_and_end_markers(
        lines,
        events,
    )

    normalized_text = "\n".join(lines).strip()
    question_text, answer_text = (
        _extract_question_and_answer(
            normalized_text
        )
    )
    unique_events = list(dict.fromkeys(events))

    return {
        "schema_version": "1.0",
        "version": SUBMISSION_NORMALIZATION_VERSION,
        "marker": SUBMISSION_NORMALIZATION_MARKER,
        "changed": (
            normalized_text != raw_text.strip()
        ),
        "events": unique_events,
        "raw_sha256": _hash_text(raw_text),
        "normalized_sha256": _hash_text(
            normalized_text
        ),
        "raw_length": len(raw_text),
        "normalized_length": len(normalized_text),
        "question_text": question_text,
        "answer_text": answer_text,
        "normalized_text": normalized_text,
    }


def _evidence_from_result(
    result: dict[str, Any],
) -> dict[str, Any]:
    evidence = {
        key: copy.deepcopy(item)
        for key, item in result.items()
        if key not in {
            "normalized_text",
            "answer_text",
        }
    }
    return evidence


def normalize_pipeline_call(
    target: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> tuple[
    tuple[Any, ...],
    dict[str, Any],
    dict[str, Any],
]:
    next_args = list(args)
    next_kwargs = dict(kwargs)
    selected_name = ""

    for candidate in ("raw_text", "input_text"):
        if candidate in next_kwargs:
            selected_name = candidate
            result = normalize_grade_submission(
                next_kwargs[candidate]
            )
            next_kwargs[candidate] = (
                result["normalized_text"]
            )
            evidence = _evidence_from_result(
                result
            )
            evidence["argument_name"] = candidate

            return (
                tuple(next_args),
                next_kwargs,
                evidence,
            )

    try:
        signature = inspect.signature(target)
        bound = signature.bind_partial(
            *next_args,
            **next_kwargs,
        )
    except (TypeError, ValueError):
        bound = None

    if bound is not None:
        for candidate in ("raw_text", "input_text"):
            if candidate in bound.arguments:
                selected_name = candidate
                result = normalize_grade_submission(
                    bound.arguments[candidate]
                )
                bound.arguments[candidate] = (
                    result["normalized_text"]
                )
                evidence = _evidence_from_result(
                    result
                )
                evidence[
                    "argument_name"
                ] = candidate

                return (
                    tuple(bound.args),
                    dict(bound.kwargs),
                    evidence,
                )

    if next_args and isinstance(next_args[0], str):
        result = normalize_grade_submission(
            next_args[0]
        )
        next_args[0] = result["normalized_text"]
        evidence = _evidence_from_result(result)
        evidence["argument_name"] = (
            "positional_0"
        )

        return (
            tuple(next_args),
            next_kwargs,
            evidence,
        )

    return (
        tuple(next_args),
        next_kwargs,
        {
            "schema_version": "1.0",
            "version": (
                SUBMISSION_NORMALIZATION_VERSION
            ),
            "marker": (
                SUBMISSION_NORMALIZATION_MARKER
            ),
            "changed": False,
            "events": ["text_argument_not_found"],
            "argument_name": "",
        },
    )


def attach_submission_normalization(
    grade: Any,
    evidence: dict[str, Any],
) -> Any:
    if not isinstance(grade, dict):
        return grade

    updated = copy.deepcopy(grade)
    updated["submission_normalization"] = (
        copy.deepcopy(evidence)
    )
    return updated
