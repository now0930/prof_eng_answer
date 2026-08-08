from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from coverage_feedback_event import (
    build_coverage_feedback_event,
)


COVERAGE_FEEDBACK_EVENT_FILENAME = (
    "coverage_feedback_event.json"
)

_LOG = logging.getLogger(__name__)


def persist_session_coverage_feedback_event(
    session_dir: Any,
    semantic_result: Any,
    question_demand_result: Any,
) -> Optional[Dict[str, Any]]:
    """
    Persist one downstream-only coverage event in the current session.

    Persistence is deliberately best-effort. A filesystem failure must not
    change routing or grading behavior.
    """
    event = build_coverage_feedback_event(
        semantic_result,
        question_demand_result,
    )
    if event is None:
        return None

    try:
        path = Path(session_dir)
        path.mkdir(parents=True, exist_ok=True)
        target = path / COVERAGE_FEEDBACK_EVENT_FILENAME
        tmp = path / (
            COVERAGE_FEEDBACK_EVENT_FILENAME + ".tmp"
        )
        tmp.write_text(
            json.dumps(
                event,
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        tmp.replace(target)
    except Exception as exc:
        # Operational observability only. Never log question/answer text,
        # session path, routing payload, score, or Topic content here.
        _LOG.warning(
            "coverage_feedback_persistence_failed exception_type=%s",
            type(exc).__name__,
        )
        return None

    return event
