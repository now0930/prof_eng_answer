from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import asdict, dataclass
from typing import Any


NORMALIZATION_VERSION = (
    "grading_text_normalization_v1"
)

_SUBMISSION_SEPARATOR = (
    "\n---ANSWER---\n"
)


@dataclass(frozen=True)
class GradingIdentity:
    normalized_question: str
    normalized_answer: str
    question_hash: str
    submission_hash: str
    normalization_version: str = (
        NORMALIZATION_VERSION
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_grading_text(
    text: str | None,
) -> str:
    """
    Normalize representation-only differences for grading identity.

    This function is used only for identity generation. It does not alter the
    question or answer passed to the grading pipeline.
    """
    value = unicodedata.normalize(
        "NFKC",
        str(text or ""),
    )

    value = value.replace(
        "\ufe0f",
        "",
    )
    value = value.replace(
        "\u200d",
        "",
    )

    value = value.replace(
        "\r\n",
        "\n",
    )
    value = value.replace(
        "\r",
        "\n",
    )

    value = re.sub(
        r"[ \t]+",
        " ",
        value,
    )
    value = re.sub(
        r" *\n *",
        "\n",
        value,
    )
    value = re.sub(
        r"\n{3,}",
        "\n\n",
        value,
    )

    return value.strip()


def _sha256_text(
    value: str,
) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def build_grading_identity(
    question_text: str | None,
    answer_text: str | None,
) -> GradingIdentity:
    normalized_question = (
        normalize_grading_text(
            question_text
        )
    )
    normalized_answer = (
        normalize_grading_text(
            answer_text
        )
    )

    question_hash = _sha256_text(
        normalized_question
    )

    submission_hash = _sha256_text(
        normalized_question
        + _SUBMISSION_SEPARATOR
        + normalized_answer
    )

    return GradingIdentity(
        normalized_question=(
            normalized_question
        ),
        normalized_answer=(
            normalized_answer
        ),
        question_hash=question_hash,
        submission_hash=submission_hash,
    )
