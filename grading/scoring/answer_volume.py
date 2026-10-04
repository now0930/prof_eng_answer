from __future__ import annotations

import re
from typing import Any

ASCII_UNITS_PER_PAGE = 600
ASCII_HALF_PAGE_THRESHOLD = 300
ASCII_ONE_PAGE_THRESHOLD = 600
ASCII_ONE_TO_TWO_PAGE_BOUNDARY = 900
ASCII_TWO_TO_THREE_PAGE_BOUNDARY = 1500
ASCII_THREE_TO_FOUR_PAGE_BOUNDARY = 2100

VOLUME_METHOD = "ascii_equivalent_only_v1"


_PROBLEM_PREFIXES = ("[문제]", "문제:", "문제 :")
_INLINE_ANSWER_MARKERS = ("[답안]", "답안:", "답안 :")
_INLINE_SECTION_SEPARATOR_RE = re.compile(r"={20,}")


def _inline_answer_remainder_from_problem_line(
    line: str,
) -> str | None:
    'Return only an explicit inline answer remainder on a problem line.'
    prefix = next(
        (
            candidate
            for candidate in _PROBLEM_PREFIXES
            if line.startswith(candidate)
        ),
        None,
    )
    if prefix is None:
        return None

    body = line[len(prefix):].strip()
    candidates: list[tuple[int, str]] = []

    for marker in _INLINE_ANSWER_MARKERS:
        index = body.find(marker)
        if index >= 0:
            candidates.append(
                (index, body[index + len(marker):].strip())
            )

    separator = _INLINE_SECTION_SEPARATOR_RE.search(body)
    if separator is not None:
        candidates.append(
            (separator.start(), body[separator.end():].strip())
        )

    if not candidates:
        return ""

    _, remainder = min(candidates, key=lambda item: item[0])
    return remainder


def normalize_volume_text(text: str | None) -> str:
    """Remove transport/problem-control lines while preserving answer content."""
    kept: list[str] = []

    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        folded = line.casefold()

        if folded == "/grade":
            continue

        if folded in {"끝", "끝.", "end", "end."}:
            continue

        inline_answer = _inline_answer_remainder_from_problem_line(
            line
        )
        if inline_answer is not None:
            if inline_answer:
                kept.append(inline_answer)
            continue

        if line.startswith("[답안]"):
            remainder = line[len("[답안]"):].strip()
            if remainder:
                kept.append(remainder)
            continue

        if line.startswith("답안:") or line.startswith("답안 :"):
            _, _, remainder = line.partition(":")
            remainder = remainder.strip()
            if remainder:
                kept.append(remainder)
            continue

        kept.append(line)

    return "\n".join(kept).strip()


def ascii_equivalent_count(text: str | None) -> int:
    """Count visible ASCII as 1 unit and non-ASCII as 2 units."""
    total = 0

    for char in str(text or ""):
        if char.isspace():
            continue
        total += 1 if ord(char) < 128 else 2

    return total


def _estimated_pages(ascii_count: int) -> int:
    if ascii_count < ASCII_HALF_PAGE_THRESHOLD:
        return 0

    rounded = (
        ascii_count + ASCII_UNITS_PER_PAGE // 2
    ) // ASCII_UNITS_PER_PAGE

    return max(1, min(4, int(rounded)))


def estimate_ascii_answer_volume(
    text: str | None,
) -> dict[str, Any]:
    normalized = normalize_volume_text(text)
    ascii_count = ascii_equivalent_count(normalized)
    page_equivalent = round(
        ascii_count / ASCII_UNITS_PER_PAGE,
        2,
    )
    estimated_pages = _estimated_pages(ascii_count)

    common: dict[str, Any] = {
        "measurement_method": VOLUME_METHOD,
        "primary_signal": "ascii_equivalent_count",
        "ascii_equivalent_count": ascii_count,
        "ascii_units_per_page": ASCII_UNITS_PER_PAGE,
        "page_equivalent": page_equivalent,
        "estimated_answer_sheet_pages": estimated_pages,
        "estimated_answer_pages": estimated_pages,
        "image_count_used": False,
        "pdf_page_count_used": False,
        "line_count_used": False,
        "normalized_text_char_count": len(normalized),
    }

    if ascii_count < ASCII_HALF_PAGE_THRESHOLD:
        return {
            **common,
            "level": "text_only_short_answer",
            "cap": 9.0,
            "reason": (
                f"ASCII 환산 {ascii_count}자로 0.5쪽 미만의 "
                "요약 답안으로 판단되어 9.0점 상한을 적용한다."
            ),
        }

    if ascii_count < ASCII_ONE_PAGE_THRESHOLD:
        return {
            **common,
            "level": "less_than_one_page_text",
            "cap": 10.5,
            "reason": (
                f"ASCII 환산 {ascii_count}자로 1쪽 미만 수준으로 "
                "판단되어 10.5점 상한을 적용한다."
            ),
        }

    if ascii_count < ASCII_ONE_TO_TWO_PAGE_BOUNDARY:
        return {
            **common,
            "level": "one_page_text",
            "cap": 13.0,
            "reason": (
                f"ASCII 환산 {ascii_count}자, 약 "
                f"{page_equivalent}쪽으로 1쪽 수준의 부분 답안 "
                "상한 13.0점을 적용한다."
            ),
        }

    if ascii_count < ASCII_TWO_TO_THREE_PAGE_BOUNDARY:
        return {
            **common,
            "level": "two_page_text",
            "cap": 19.0,
            "reason": (
                f"ASCII 환산 {ascii_count}자, 약 "
                f"{page_equivalent}쪽으로 2쪽 수준의 축약 답안 "
                "상한 19.0점을 적용한다."
            ),
        }

    if ascii_count < ASCII_THREE_TO_FOUR_PAGE_BOUNDARY:
        return {
            **common,
            "level": "three_page_text",
            "cap": None,
            "reason": (
                f"ASCII 환산 {ascii_count}자, 약 "
                f"{page_equivalent}쪽으로 3쪽 표준 답안 "
                "분량이므로 분량 상한을 적용하지 않는다."
            ),
        }

    return {
        **common,
        "level": "four_page_text",
        "cap": None,
        "reason": (
            f"ASCII 환산 {ascii_count}자, 약 "
            f"{page_equivalent}쪽으로 4쪽 이상 충분한 답안 "
            "분량이므로 분량 상한을 적용하지 않는다."
        ),
    }
