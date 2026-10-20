"""Quality checklist is private and cannot take grading authority."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile

import pytest

from grading.quality.operational_checksheet import (
    add_manual_issue, advance_issue, build_quality_checksheet,
    load_quality_checksheet, reclassify_issue,
)
from grading.scoring.deterministic_primary_grader import (
    grade_deterministically, persist_deterministic_grade,
)
from scripts.quality_checksheet import main as cli_main


QUESTION = "SIL 결정 방법을 설명하시오."
ANSWER = "lambda_SIS 비율이 PFD 비율보다 작도록 설계한다."


def make_grade():
    return grade_deterministically(question_text=QUESTION, answer_text=ANSWER)


def test_production_persistence_writes_private_score_neutral_sheet():
    grade = make_grade()
    original = deepcopy(grade)
    with tempfile.TemporaryDirectory() as directory:
        raw = persist_deterministic_grade(directory, grade)
        sheet_path = Path(directory) / "quality_checksheet.json"
        sheet = load_quality_checksheet(directory)
        assert sheet_path.stat().st_mode & 0o777 == 0o600
        assert sheet["score_effect"] == "none"
        assert "lambda_SIS" not in sheet_path.read_text()
        assert "SIL 결정 방법" not in sheet_path.read_text()
        assert json.loads(raw) == original == grade
        assert (Path(directory) / "deterministic_grade.json").is_file()
        assert len(sheet["checks"]) == 5
        assert all(row["result"] == "pass" for row in sheet["checks"])


def test_contract_defect_and_fatal_pass_contradiction_are_recorded_not_scored():
    grade = make_grade()
    grade["total_score"] = 25.0
    grade["official_pass_met"] = True
    sheet = build_quality_checksheet(grade, created_at="2026-10-13T00:00:00+00:00")
    by_id = {row["check_id"]: row for row in sheet["checks"]}
    assert by_id["score_authority"]["result"] == "fail"
    assert by_id["fatal_verdict_consistency"]["result"] == "fail"
    assert sheet["score_effect"] == "none"


def test_score_neutral_cross_topic_llm_suggestion_is_not_a_false_authority_defect():
    question = "열전대와 RTD의 원리, 특성 비교, 정확도 요인과 개선 방안을 설명하시오."
    answer = "열전대는 제벡 효과로 온도차를 잰다."
    grade = grade_deterministically(
        question_text=question, answer_text=answer,
        llm_evidence_fn=lambda _: json.dumps({"judgments": [{
            "requirement_id": "tc_seebeck_temperature_difference",
            "status": "SATISFIED", "quote": answer,
        }]}, ensure_ascii=False),
    )
    assert grade["provider_calls"] == 1
    assert grade["cross_topic_evidence"]["llm_evidence_audit"]["score_effect"] == "none"
    sheet = build_quality_checksheet(grade)
    by_id = {row["check_id"]: row for row in sheet["checks"]}
    assert by_id["score_authority"]["result"] == "pass"


def test_manual_issue_requires_triage_fix_and_distinct_passing_retest():
    grade = make_grade()
    sheet = build_quality_checksheet(grade, created_at="2026-10-13T00:00:00+00:00")
    add_manual_issue(sheet, category="false_high", priority="P1", note="reviewed example")
    issue_id = sheet["issues"][-1]["issue_id"]
    with pytest.raises(ValueError, match="transition"):
        advance_issue(sheet, issue_id=issue_id, status="closed", note="skip")
    advance_issue(sheet, issue_id=issue_id, status="triaged", note="confirmed")
    with pytest.raises(ValueError, match="fix reference"):
        advance_issue(sheet, issue_id=issue_id, status="fix_pending_retest", note="changed")
    advance_issue(sheet, issue_id=issue_id, status="fix_pending_retest",
                  note="updated", fix_reference="topic-pack-change-001")
    with pytest.raises(ValueError, match="new grade snapshot"):
        advance_issue(sheet, issue_id=issue_id, status="retested", note="rerun",
                      retest_sheet=deepcopy(sheet))
    retest = deepcopy(sheet)
    retest["grade_sha256"] = "a" * 64
    advance_issue(sheet, issue_id=issue_id, status="retested", note="checked",
                  retest_sheet=retest)
    advance_issue(sheet, issue_id=issue_id, status="closed", note="accepted")
    assert sheet["issues"][-1]["status"] == "closed"
    assert sheet["issues"][-1]["retest_sheet_sha256"]


def test_range_mismatch_can_be_neutrally_reclassified_with_audit():
    sheet = build_quality_checksheet(make_grade())
    add_manual_issue(sheet, category="false_low", priority="P2", note="initial suspicion")
    issue_id = sheet["issues"][-1]["issue_id"]
    reclassify_issue(sheet, issue_id=issue_id, category="benchmark_conflict",
                     note="answer or benchmark may be wrong")
    assert sheet["issues"][-1]["category"] == "benchmark_conflict"
    assert sheet["audit"][-1]["from_category"] == "false_low"
    with pytest.raises(ValueError, match="unchanged"):
        reclassify_issue(sheet, issue_id=issue_id, category="benchmark_conflict", note="same")


def test_auto_issue_cannot_be_retested_while_same_check_still_fails():
    grade = make_grade()
    grade["question_scope_evaluation"]["exact"] = False
    sheet = build_quality_checksheet(grade)
    issue = next(row for row in sheet["issues"] if row["check_id"] == "question_scope")
    advance_issue(sheet, issue_id=issue["issue_id"], status="triaged", note="scope gap")
    advance_issue(sheet, issue_id=issue["issue_id"], status="fix_pending_retest",
                  note="candidate fix", fix_reference="commit-123")
    retest = deepcopy(sheet)
    retest["grade_sha256"] = "b" * 64
    with pytest.raises(ValueError, match="has not passed"):
        advance_issue(sheet, issue_id=issue["issue_id"], status="retested",
                      note="still failing", retest_sheet=retest)


def test_cli_lists_and_records_without_changing_grade(capsys):
    grade = make_grade()
    with tempfile.TemporaryDirectory() as root:
        session = Path(root) / "session_1"
        persist_deterministic_grade(session, grade)
        before = (session / "deterministic_grade.json").read_bytes()
        assert cli_main(["list", "--sessions-root", root]) == 0
        listed = json.loads(capsys.readouterr().out)
        assert listed["sessions"] == 1
        assert cli_main(["add", "--session", str(session), "--category", "false_low",
                         "--priority", "P1", "--note", "missed valid paraphrase"]) == 0
        added = json.loads(capsys.readouterr().out)
        assert added["issue_id"].startswith("manual_")
        assert cli_main(["show", "--session", str(session)]) == 0
        shown = json.loads(capsys.readouterr().out)
        assert any(x["issue_id"] == added["issue_id"] for x in shown["issues"])
        export = Path(root) / "issues.csv"
        assert cli_main(["export", "--sessions-root", root,
                         "--output", str(export)]) == 0
        exported = json.loads(capsys.readouterr().out)
        assert exported["exported_issues"] >= 1
        assert export.stat().st_mode & 0o777 == 0o600
        assert "false_low" in export.read_text(encoding="utf-8")
        assert (session / "deterministic_grade.json").read_bytes() == before


def test_checksheet_write_failure_does_not_change_authoritative_grade(monkeypatch, capsys):
    grade = make_grade()
    def fail(*args, **kwargs):
        raise OSError("private response text must not be logged")
    monkeypatch.setattr(
        "grading.quality.operational_checksheet.save_quality_checksheet", fail,
    )
    with tempfile.TemporaryDirectory() as directory:
        raw = persist_deterministic_grade(directory, grade)
        assert json.loads(raw)["total_score"] == grade["total_score"]
        assert (Path(directory) / "deterministic_grade.json").is_file()
        assert not (Path(directory) / "quality_checksheet.json").exists()
    output = capsys.readouterr().out
    assert "checksheet_persistence_failed" in output
    assert "private response text" not in output


def test_checksheet_rejects_changed_grade_snapshot():
    grade = make_grade()
    with tempfile.TemporaryDirectory() as directory:
        persist_deterministic_grade(directory, grade)
        grade_path = Path(directory) / "deterministic_grade.json"
        tampered = json.loads(grade_path.read_text(encoding="utf-8"))
        tampered["total_score"] = 25.0
        grade_path.write_text(json.dumps(tampered), encoding="utf-8")
        with pytest.raises(ValueError, match="snapshot mismatch"):
            load_quality_checksheet(directory)
