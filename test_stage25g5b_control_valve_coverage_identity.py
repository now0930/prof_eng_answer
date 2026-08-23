from __future__ import annotations

import copy

import verified_defect_reconciliation as owner


SYNC = (
    owner
    ._stage25g5b_sync_parsed_coverage_identity
)


def _reconciled_grade() -> dict:
    return {
        "score": 15.25,
        "total_score": 15.25,
        "question_type_coverage": {
            "question_type": "PRINCIPLE_INTERPRETATION",
            "name_ko": "원리·해석형",
            "coverage_counts": {
                "present": 1,
                "incorrect": 2,
                "total": 3,
            },
        },
        "parsed": {
            "question_type_coverage": {
                "question_type": "PRINCIPLE_INTERPRETATION",
                "coverage_counts": {
                    "present": 1,
                    "incorrect": 2,
                    "total": 3,
                },
            },
        },
        "verified_defect_reconciliation": {
            "marker": (
                "VERIFIED_DEFECT_RECONCILIATION_V1"
            ),
            "score_effect": "none",
        },
    }


def test_stage25g5b_syncs_root_metadata_to_parsed_coverage():
    grade = _reconciled_grade()
    result = SYNC(grade)

    assert (
        result["parsed"]["question_type_coverage"]
        == result["question_type_coverage"]
    )
    assert (
        result["parsed"]["question_type_coverage"][
            "name_ko"
        ]
        == "원리·해석형"
    )


def test_stage25g5b_uses_deep_copy_not_shared_object():
    grade = _reconciled_grade()
    result = SYNC(grade)

    root = result["question_type_coverage"]
    nested = result["parsed"][
        "question_type_coverage"
    ]
    assert root is not nested

    nested["name_ko"] = "변경"
    assert root["name_ko"] == "원리·해석형"


def test_stage25g5b_scope_guard_skips_nonreconciled_grade():
    grade = _reconciled_grade()
    grade.pop(
        "verified_defect_reconciliation"
    )
    original_nested = copy.deepcopy(
        grade["parsed"][
            "question_type_coverage"
        ]
    )

    result = SYNC(grade)
    assert (
        result["parsed"][
            "question_type_coverage"
        ]
        == original_nested
    )
    assert (
        "name_ko"
        not in result["parsed"][
            "question_type_coverage"
        ]
    )


def test_stage25g5b_full_wrapper_preserves_score_and_identity():
    grade = _reconciled_grade()
    before_score = (
        grade["score"],
        grade["total_score"],
    )

    result = (
        owner
        ._stage25g5b_sync_parsed_coverage_identity(
            copy.deepcopy(grade)
        )
    )
    assert (
        result["score"],
        result["total_score"],
    ) == before_score
    assert (
        result["parsed"]["question_type_coverage"]
        == result["question_type_coverage"]
    )
