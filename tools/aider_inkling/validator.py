"""Validate edits, deterministic grading, scope, and regression tests."""

import hashlib
import json
import re
import subprocess
import sys


def compiler_diagnostics(root, repo):
    import ast

    os.chdir(repo)
    sys.path.insert(0, str(repo))

    from grading.routing.deterministic_topic_router import (
        route_question_topics,
    )
    from grading.evidence.fact_anchor_evidence_adapter import (
        _required_anchor_ids,
        _question_similarity,
        evaluate_fact_anchor_requirements,
    )
    from grading.scoring.grade_submission_normalizer import (
        normalize_grade_submission,
    )

    config = json.loads(
        (root / "test_answers/compiler_case.json").read_text()
    )

    topic = config["topic_id"]
    topic_path = repo / "rubrics/topic_packs" / topic
    model_path = topic_path / "model_answer.json"

    if not model_path.is_file():
        sys.exit(f"Topic Pack not found: {topic}")

    payload = json.loads(model_path.read_text())

    answer_path = root / config["input"]
    raw = answer_path.read_text()
    lines = raw.splitlines()

    if lines and lines[0].strip() == "/grade":
        lines = lines[1:]

    normalized = normalize_grade_submission("\n".join(lines))

    question = normalized["question_text"]
    answer = normalized["answer_text"]

    if normalized["question_answer_boundary"]["manual_review_required"]:
        sys.exit("Question-answer boundary unresolved")

    def inspect_case(name, q, a):
        route = route_question_topics(q)

        required, scope = _required_anchor_ids(
            topic_path, q
        )

        evidence = evaluate_fact_anchor_requirements(
            question_text=q,
            answer_text=a,
            topic_ids=[topic],
        )

        patterns = []

        for row in payload.get("expected_question_patterns", []):
            if not isinstance(row, dict):
                continue

            pattern = str(
                row.get("pattern") or row.get("question") or ""
            )

            patterns.append({
                "pattern": pattern,
                "similarity": round(
                    _question_similarity(q, pattern), 6
                ),
                "required_anchor_ids":
                    row.get("required_anchor_ids", []),
                "pass_required_anchor_ids":
                    row.get("pass_required_anchor_ids", []),
            })

        patterns.sort(
            key=lambda row: row["similarity"],
            reverse=True,
        )

        return {
            "case": name,
            "route_keys": sorted(route.keys()),
            "routing": {
                key: route[key]
                for key in (
                    "status",
                    "primary_topic_id",
                    "topic_ids",
                    "selected_topic_ids",
                    "secondary_topic_ids",
                    "answer_text_used",
                    "provider_calls",
                )
                if key in route
            },
            "selected_scope": scope,
            "required_anchor_ids":
                sorted(required) if required is not None else None,
            "candidate_patterns": patterns,
            "evidence_keys": sorted(evidence.keys()),
            "provider_calls": evidence.get("provider_calls"),
            "requirements": [
                {
                    key: row[key]
                    for key in (
                        "requirement_id",
                        "anchor_id",
                        "status",
                        "verdict",
                        "reason_code",
                    )
                    if key in row
                }
                for row in evidence.get("requirements", [])
                if isinstance(row, dict)
            ],
        }

    report = {
        "compiler_version": "5.0-diagnostics",
        "input_sha256": hashlib.sha256(
            answer_path.read_bytes()
        ).hexdigest(),
        "topic_id": topic,
        "topic_checks": {
            candidate: (
                repo / "rubrics/topic_packs" / candidate
            ).is_dir()
            for candidate in config["check_topic_ids"]
        },
        "cases": [
            inspect_case("actual_answer", question, answer)
        ],
    }

    for case in config["synthetic_cases"]:
        report["cases"].append(
            inspect_case(
                case["name"],
                case["question"],
                case["answer"],
            )
        )

    report["symbols"] = {}

    for name in config["source_files"]:
        source = (repo / name).read_text()
        tree = ast.parse(source)

        report["symbols"][name] = {
            node.name: ast.unparse(node.args)
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }

    destination = root / "compiler_diagnostics_v5.json"

    output = json.dumps(
        report, ensure_ascii=False, indent=2
    )

    destination.write_text(output, encoding="utf-8")
    destination.chmod(0o600)

    print(output)
    print("\nV5 diagnostic report:", destination)


def scope_gate(report, rules):
    cases = {row["case"]: row for row in report["cases"]}
    errors = []

    for name, rule in rules.items():
        case = cases[name]
        actual = set(case["required_anchor_ids"] or [])
        required = set(rule.get("include", []))
        forbidden = set(rule.get("exclude", []))

        missing = required - actual
        unexpected = forbidden & actual

        if missing:
            errors.append(f"{name}: 누락 {sorted(missing)}")

        if unexpected:
            errors.append(f"{name}: 혼입 {sorted(unexpected)}")

        if "exact" in rule and actual != set(rule["exact"]):
            errors.append(f"{name}: 기존 요구 범위 불일치")

        if case["routing"]["primary_topic_id"] != rule["topic"]:
            errors.append(f"{name}: 라우팅 변경")

        if case["provider_calls"] != 0:
            errors.append(f"{name}: provider 호출 발생")

        if rule.get("check_evidence"):
            evaluated = {
                row["requirement_id"]
                for row in case["requirements"]
            }
            expected_ids = required | set(rule.get("exact", []))

            if expected_ids - evaluated:
                errors.append(
                    f"{name}: evidence scope 누락 "
                    f"{sorted(expected_ids - evaluated)}"
                )

            if forbidden & evaluated:
                errors.append(f"{name}: 무관 evidence 혼입")

        print(f"{name}: {sorted(actual)}")

    return errors


def validate_edit(ctx, files, target, item, log, before, original_head, original_index):
    REPO = ctx.repo
    git, snapshot, stop = ctx.git, ctx.snapshot, ctx.stop
    if git("rev-parse", "HEAD") != original_head:
        stop("예상하지 않은 Git 커밋이 발견되었습니다.")

    if git("diff", "--cached", "--binary") != original_index:
        stop("Git staging 영역이 변경되었습니다.")

    after = snapshot()

    changed = {
        name for name in before.keys() | after.keys()
        if before.get(name) != after.get(name)
    }

    unexpected = changed - set(files)
    if unexpected:
        stop(f"지정 범위 외 파일 변경: {sorted(unexpected)}")


    if changed != set(files):
        stop("V6: expected target not modified")

    if target.read_bytes().decode("utf-8") != item["expected"]:
        stop("V6: output differs from approved exact edit")

    output = log.read_text(errors="replace").lower()

    if any(x in output for x in [
        "has hit a token limit",
        "failed to apply edit",
        "search/replace block failed",
        "unable to apply",
    ]):
        stop("Aider 코드 적용 오류가 발견되었습니다.")

    print("수정 파일:", sorted(changed))

    if subprocess.call(
        ["git", "diff", "HEAD", "--check"], cwd=REPO
    ) != 0:
        stop("Git diff 검사 실패")


class Validation:
    def __init__(self, ctx, plan):
        self.ctx = ctx
        self.plan = plan
        ROOT, stop = ctx.root, ctx.stop
        ANSWER = ROOT / "test_answers/feedback_control.txt"
        VALIDATOR = ROOT / "validate_answer.sh"

        if not ANSWER.is_file() or not VALIDATOR.is_file():
            stop("실제 답안 또는 재채점 스크립트 없음")

        self.answer, self.validator = ANSWER, VALIDATOR
        self.answer_hash = hashlib.sha256(ANSWER.read_bytes()).hexdigest()

    def before(self):
        self.before_grade = self.grade_snapshot("before")
        if self.plan.get("scope_checks"):
            self.scope_probe("before")

    def grade_snapshot(self, label):
        RUN, ANSWER, VALIDATOR = self.ctx.run_dir, self.answer, self.validator
        answer_hash = self.answer_hash
        stop, run, git = self.ctx.stop, self.ctx.run, self.ctx.git
        if hashlib.sha256(ANSWER.read_bytes()).hexdigest() != answer_hash:
            stop("기준 답안이 변경되었습니다.")

        log = RUN / f"grade_{label}.log"

        print(f"\n[실제 답안 재채점: {label}]")

        code = run(
            ["bash", VALIDATOR, ANSWER],
            log,
        )

        if code != 0:
            stop(f"실제 답안 재채점 실패: {label}")

        output = log.read_text(encoding="utf-8")

        scores = re.findall(
            r"채점 완료:\s*(\d+(?:\.\d+)?)\s*/\s*25",
            output,
        )

        if not scores:
            stop("채점 점수를 찾을 수 없습니다.")

        result = {"total": float(scores[-1])}

        for name, score, maximum in re.findall(
            r"^- ([A-E]_[a-z_]+):\s*([\d.]+)/([\d.]+)",
            output,
            flags=re.M,
        ):
            result[name] = float(score)

        result["input_sha256"] = answer_hash
        result["dirty_diff_sha256"] = hashlib.sha256(
            git("diff", "HEAD", "--binary")
        ).hexdigest()

        (RUN / f"grade_{label}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return result

    def scope_probe(self, label):
        ROOT, RUN, PYTHON = self.ctx.root, self.ctx.run_dir, self.ctx.python
        ENV, stop = self.ctx.env, self.ctx.stop
        output = RUN / f"compiler_{label}.log"

        with output.open("w") as log:
            result = subprocess.run(
                [
                    str(PYTHON), "-B", str(ROOT / "develop.py"),
                    "--diagnose-worker"
                ],
                cwd=ROOT,
                env=ENV,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=300,
            )

        if result.returncode:
            stop(f"V5 진단 실패: {output}")

        report = json.loads(
            (ROOT / "compiler_diagnostics_v5.json").read_text()
        )

        (RUN / f"compiler_{label}.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2)
        )

        return report

    def after(self):
        RUN, REPO, PYTHON = self.ctx.run_dir, self.ctx.repo, self.ctx.python
        run, backup, stop = self.ctx.run, self.ctx.backup, self.ctx.stop
        plan, before_grade = self.plan, self.before_grade
        grade_snapshot, scope_probe = self.grade_snapshot, self.scope_probe
        after_grade = grade_snapshot("after")

        print("\n===== 수정 전후 채점 비교 =====")
        for key in before_grade:
            if key in after_grade:
                print(
                    f"{key}: "
                    f"{before_grade[key]} -> {after_grade[key]}"
                )

        (RUN / "grade_comparison.json").write_text(
            json.dumps(
                {"before": before_grade, "after": after_grade},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


        if plan.get("scope_checks"):
            print("\n===== V5 요구사항 범위 검증 =====")
            errors = scope_gate(scope_probe("after"), plan["scope_checks"])

            if errors:
                stop("범위 검증 실패: " + "; ".join(errors))

            print("V5 요구사항 범위 검증 통과")

        # 5. 전체 멀티코어 회귀시험
        print("\n[최종] 전체 프로젝트 회귀시험")

        code = run(
            [PYTHON, "-m", "pytest", "-n", "6", "--dist", "loadfile", "-q"],
            RUN / "pytest_full.log",
            cwd=REPO,
        )

        backup("final")

        if code != 0:
            stop("전체 회귀시험 실패")
