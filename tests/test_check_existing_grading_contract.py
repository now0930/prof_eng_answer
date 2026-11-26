from scripts.check_existing_grading_contract import classify_changes


def test_existing_contract_and_golden_cannot_be_rewritten_in_normal_change():
    protected = [
        "GRADING_DIRECTION_CONTRACT.md", "calibration/pytest_quarantine.json",
        "calibration/deterministic_authority_policy.json",
        "calibration/grading_integrity_drift_baseline.json",
        "calibration/qtype_golden/cases/compare_selection.json",
        "grading/evidence/fact_anchor_independent_revision_holds_20261101.json",
        "tests/test_deterministic_score_engine.py",
    ]
    blocked, review, topic = classify_changes([("M", path) for path in protected])
    assert blocked == sorted(protected)
    assert not review
    assert not topic


def test_delete_existing_regression_is_blocked_and_other_edit_reported():
    blocked, review, _ = classify_changes([
        ("D", "tests/test_old.py"),
        ("D", "scripts/test_old.py"),
        ("M", "tests/test_other.py"),
        ("A", "tests/test_new.py"),
    ])
    assert blocked == ["scripts/test_old.py", "tests/test_old.py"]
    assert review == ["tests/test_other.py"]


def test_additive_topic_changes_reuse_existing_validators_without_freezing_inventory():
    blocked, review, topic = classify_changes([
        ("A", "rubrics/topic_packs/new/fact_anchor.json"),
        ("M", "rubrics/generated/fact_anchor.json"),
        ("A", "tests/test_new_topic.py"),
        ("A", "calibration/risk_golden/new.json"),
    ])
    assert not blocked
    assert not review
    assert topic


def test_normal_grader_fix_can_run_existing_regressions():
    assert classify_changes([("M", "grading/scoring/deterministic_score_engine.py")]) == ([], [], False)


def test_registry_and_builder_changes_trigger_topic_validators():
    for path in ("grading/evidence/approved_fact_registry.json",
                 "scripts/build_generated_rubrics.py",
                 "master_topic_packs/new.json"):
        assert classify_changes([("M", path)]) == ([], [], True)


def test_rename_as_delete_add_does_not_bypass_old_test_protection():
    blocked, _, _ = classify_changes([
        ("D", "tests/test_old.py"), ("A", "tests/test_renamed.py"),
    ])
    assert blocked == ["tests/test_old.py"]
