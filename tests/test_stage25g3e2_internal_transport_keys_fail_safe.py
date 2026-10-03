from __future__ import annotations

import ast
import inspect
from pathlib import Path

import logic_check_evaluator as evaluator


COMPACT_KEY = (
    evaluator
    ._STAGE25G3E_INTERNAL_COMPACT_SECONDARY_KEY
)
REPLAY_KEY = "_logic_check_secondary_replay"
HELPER = (
    evaluator
    ._stage25g3e2_read_internal_transport_value
)


class ExplodingGetDict(dict):
    def get(self, *args, **kwargs):
        raise RuntimeError(
            "simulated public routing get failure"
        )


class ExplodingString:
    def __str__(self):
        raise RuntimeError(
            "simulated internal value string failure"
        )


def test_stage25g3e2_base_dict_read_bypasses_overridden_get_for_both_keys():
    grade = ExplodingGetDict(
        {
            COMPACT_KEY: " secondary_topic ",
            REPLAY_KEY: True,
        }
    )
    assert HELPER(
        grade,
        COMPACT_KEY,
        "",
        normalize_string=True,
    ) == "secondary_topic"
    assert HELPER(
        grade,
        REPLAY_KEY,
        False,
    ) is True


def test_stage25g3e2_missing_and_non_dict_values_return_defaults():
    assert HELPER({}, REPLAY_KEY, False) is False
    assert HELPER(None, REPLAY_KEY, False) is False
    assert HELPER([], COMPACT_KEY, "") == ""


def test_stage25g3e2_string_normalization_failure_returns_default():
    grade = {
        COMPACT_KEY: ExplodingString(),
    }
    assert HELPER(
        grade,
        COMPACT_KEY,
        "",
        normalize_string=True,
    ) == ""


def test_stage25g3e2_evaluate_has_no_direct_internal_grade_get_calls():
    source = Path(
        evaluator.__file__
    ).read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    evaluate_node = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "evaluate_logic_checks"
    )
    evaluate_source = (
        ast.get_source_segment(
            source,
            evaluate_node,
        )
        or ""
    )
    helper_source = inspect.getsource(
        HELPER
    )

    assert evaluate_source.count(
        "_stage25g3e2_read_internal_transport_value"
    ) == 2
    assert (
        'grade.get("_logic_check_secondary_replay")'
        not in evaluate_source
    )
    assert (
        "grade.get(\\n"
        "                "
        "_STAGE25G3E_INTERNAL_COMPACT_SECONDARY_KEY"
        not in evaluate_source
    )
    assert "grade.get(" in evaluate_source
    assert "dict.get(" in helper_source
    assert (
        "STAGE25G3E2_INTERNAL_TRANSPORT_KEYS_"
        "FAIL_SAFE_V1"
        in source
    )


def test_stage25g3e2_replay_value_preserves_boolean_semantics():
    assert HELPER(
        {REPLAY_KEY: 0},
        REPLAY_KEY,
        False,
    ) == 0
    assert HELPER(
        {REPLAY_KEY: 1},
        REPLAY_KEY,
        False,
    ) == 1
    assert HELPER(
        {REPLAY_KEY: "yes"},
        REPLAY_KEY,
        False,
    ) == "yes"
