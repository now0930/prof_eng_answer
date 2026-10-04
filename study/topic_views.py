"""Public Master -> grading/training/feedback read interfaces.

Feedback retains the diagnosis-projection-v1 wire contract. Each view loads
independently: unavailable learning material must never block grading.
Legacy projection functions remain supported for existing consumers.
"""

from pathlib import Path
from typing import Any

from .master_topic_pack import project_diagnosis, project_grading, project_training


def grading_view(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Read existing grading authority; do not calculate a score."""
    return project_grading(repository_root, master)


def training_view(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Read study content, source text and unresolved annotations."""
    return project_training(repository_root, master)


def feedback_view(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Read score-neutral guidance to pair with an already finalized grade."""
    return project_diagnosis(repository_root, master)
