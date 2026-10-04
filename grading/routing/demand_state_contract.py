"""Single canonical contract for requirement-fulfilment states.

Public benchmark values are uppercase.  Runtime ledger values remain
lowercase for backward compatibility, but both use this module's aliases and
precedence.  ``PRESENT`` means correct under the provider contract; callers
must still enforce identity and evidence before accepting provider output.
"""

from __future__ import annotations

from typing import Any


CANONICAL_STATES = ("CORRECT", "PARTIAL", "WRONG", "MISSING")
PREDICTION_STATES = CANONICAL_STATES + ("UNKNOWN",)
STATE_ALIASES = {
    "PRESENT": "CORRECT",
    "INCORRECT": "WRONG",
    "CONTRADICTED": "WRONG",
    "ABSENT": "MISSING",
}

# Conservative conflict resolution: verified correctness defects dominate,
# then explicit absence, partial evidence, and finally positive coverage.
STATE_PRECEDENCE = {
    "UNKNOWN": 0,
    "CORRECT": 1,
    "PARTIAL": 2,
    "MISSING": 3,
    "WRONG": 4,
}


def normalize_state(value: Any, *, allow_unknown: bool = False) -> str:
    state = str(value or "").strip().upper()
    state = STATE_ALIASES.get(state, state)
    allowed = PREDICTION_STATES if allow_unknown else CANONICAL_STATES
    if state not in allowed:
        raise ValueError(f"unsupported demand state: {value!r}")
    return state


def normalize_internal_state(value: Any) -> str:
    try:
        return normalize_state(value, allow_unknown=True).lower().replace("wrong", "incorrect")
    except ValueError:
        return "unknown"


def precedence(value: Any) -> int:
    try:
        state = normalize_state(value, allow_unknown=True)
    except ValueError:
        state = "UNKNOWN"
    return STATE_PRECEDENCE[state]


def resolve_states(values: list[Any]) -> str:
    states = [normalize_state(value, allow_unknown=True) for value in values]
    return max(states, key=STATE_PRECEDENCE.__getitem__) if states else "UNKNOWN"
