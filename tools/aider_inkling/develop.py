import os
import sys
import json
import socket
import hashlib
import fcntl
import subprocess
from pathlib import Path
from datetime import datetime

from ai_backends import EditBackend, PlanBackend
from edit_contract import exact_patch

ROOT = Path(__file__).resolve().parent
REPO = ROOT / "repo"
PYTHON = Path.home() / "hermes/validation/.venv-xdist/bin/python"

ENV = os.environ.copy()
ENV["CURRENT_UID"] = str(os.getuid())
ENV["CURRENT_GID"] = str(os.getgid())


# INKLING_COMPILER_V5_DIAGNOSTICS

def compiler_diagnostics():
    import ast

    os.chdir(REPO)
    sys.path.insert(0, str(REPO))

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
        (ROOT / "test_answers/compiler_case.json").read_text()
    )

    topic = config["topic_id"]
    topic_path = REPO / "rubrics/topic_packs" / topic
    model_path = topic_path / "model_answer.json"

    if not model_path.is_file():
        sys.exit(f"Topic Pack not found: {topic}")

    payload = json.loads(model_path.read_text())

    answer_path = ROOT / config["input"]
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
                REPO / "rubrics/topic_packs" / candidate
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
        source = (REPO / name).read_text()
        tree = ast.parse(source)

        report["symbols"][name] = {
            node.name: ast.unparse(node.args)
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }

    destination = ROOT / "compiler_diagnostics_v5.json"

    output = json.dumps(
        report, ensure_ascii=False, indent=2
    )

    destination.write_text(output, encoding="utf-8")
    destination.chmod(0o600)

    print(output)
    print("\nV5 diagnostic report:", destination)


if len(sys.argv) > 1 and sys.argv[1] == "--diagnose":
    os.execv(
        str(PYTHON),
        [
            str(PYTHON), "-B", str(Path(__file__).resolve()),
            "--diagnose-worker"
        ],
    )

if len(sys.argv) > 1 and sys.argv[1] == "--diagnose-worker":
    compiler_diagnostics()
    sys.exit(0)


RUN = ROOT / "runs" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
RUN.mkdir(parents=True)

LOCK = open(ROOT / ".develop.lock", "w")

def stop(message):
    print(f"\n[중단] {message}", flush=True)
    print(f"로그 위치: {RUN}", flush=True)
    sys.exit(1)

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args]
    )

def run(cmd, log, cwd=ROOT, env=None):
    print("\n실행:", " ".join(map(str, cmd)), flush=True)
    with open(log, "w") as out:
        proc = subprocess.Popen(
            list(map(str, cmd)),
            cwd=cwd,
            env=ENV if env is None else env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
        for line in proc.stdout:
            print(line, end="", flush=True)
            out.write(line)
            out.flush()
        return proc.wait()

def snapshot():
    result = {}
    rows = git(
        "status", "--porcelain=v1", "-z",
        "--untracked-files=all", "--no-renames"
    ).split(b"\0")

    for row in rows:
        if not row:
            continue

        name = os.fsdecode(row[3:])
        path = REPO / name

        if path.is_symlink():
            content = os.readlink(path).encode()
        elif path.is_file():
            content = path.read_bytes()
        else:
            content = b""

        result[name] = (
            row[:2],
            hashlib.sha256(content).hexdigest()
        )

    return result

def backup(prefix):
    (RUN / f"{prefix}.patch").write_bytes(
        git("diff", "HEAD", "--binary")
    )
    (RUN / f"{prefix}_staged.patch").write_bytes(
        git("diff", "--cached", "--binary")
    )
    (RUN / f"{prefix}_status.txt").write_bytes(
        git("status", "--short")
    )

try:
    fcntl.flock(LOCK, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    stop("다른 develop 작업이 실행 중입니다.")

if len(sys.argv) < 2:
    stop('사용법: ./develop.sh "개발 의도" 또는 --plan')

if not PYTHON.is_file():
    stop("기존 pytest 가상환경을 찾을 수 없습니다.")

try:
    executor = EditBackend.from_env(ENV) if "--compile-only" not in sys.argv else None
    if executor is not None:
        executor.preflight()
except (OSError, ValueError, subprocess.SubprocessError) as exc:
    stop(f"Editor setup failed: {exc}")

backup("before")
original_head = git("rev-parse", "HEAD")
original_index = git("diff", "--cached", "--binary")

plan_path = RUN / "plan.json"

# 1. 작업 지시서 생성 또는 재사용
if sys.argv[1] == "--plan":
    source = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "plan.json"
    plan_path.write_bytes(source.read_bytes())
    print("[1] 기존 plan.json 재사용: Copilot 호출 없음")

else:
    import tempfile
    import shutil

    try:
        planner = PlanBackend.from_env(ENV)
    except (OSError, ValueError) as exc:
        stop(f"Planner setup failed: {exc}")

    intent = " ".join(
        x for x in sys.argv[1:]
        if x != "--compile-only"
    )

    prompt = """
    You are a read-only development planner.

    User objective:
    """ + intent + """

    Inspect relevant repository files.
    Identify the root cause.
    Design the implementation.
    Select files and execution order.

    Never modify files or run shell commands.
    Use existing tracked Python or JSON files only.
    One writable file per task.
    Use exact existing function names or JSON keys.
    SEARCH must match exactly once.
    Both SEARCH and REPLACE must end with a newline.
    Maximum 8 edits per task.
    Do not include read_files or allow_no_change.
    Preserve scoring weights and Fact approval policy.
    Do not weaken existing tests.
    Do not hardcode individual answers.
    Return JSON only, without Markdown.

    Required schema:
    {
      "schema_version": "inkling_plan_v6",
      "objective": "objective",
      "analysis": {
        "root_cause": "verified cause",
        "inspected_files": ["relative path"]
      },
      "tasks": [
        {
          "id": 1,
          "files": ["existing file"],
          "target_symbols": ["existing symbol"],
          "instruction": "implementation",
          "edits": [
            {
              "search": "exact old source",
              "replace": "exact new source"
            }
          ],
          "acceptance": ["acceptance condition"],
          "test_files": ["tests/existing_test.py"]
        }
      ]
    }
    """

    before_planner = snapshot()

    print("[1] AI 관련 파일 분석 및 계획 작성", flush=True)

    with tempfile.TemporaryDirectory(
        prefix="planner_v6_"
    ) as directory:

        workspace = Path(directory)

        roots = {
            "grading", "rubrics", "master_topic_packs",
            "tests", "scripts", "tools",
            "calibration", "schemas"
        }

        copied = 0

        for raw in git("ls-files", "-z").split(b"\0"):
            if not raw:
                continue

            relative = Path(os.fsdecode(raw))
            src = REPO / relative

            if relative.parts[0] not in roots:
                continue

            if src.suffix not in {
                ".py", ".json", ".yaml", ".yml", ".md", ".toml"
            }:
                continue

            if not src.is_file() or src.is_symlink():
                continue

            if not src.resolve().is_relative_to(REPO.resolve()):
                continue

            dst = workspace / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1

        print(f"AI 분석 대상: {copied}개", flush=True)

        try:
            result = planner.run(prompt, workspace, RUN, ENV)
        except subprocess.TimeoutExpired:
            stop("AI 계획 실행 시간 제한 초과")
        except OSError as exc:
            stop(f"AI 계획 실행 실패: {exc}")

        if result.returncode != 0:
            stop(f"AI 계획 실행 실패: {planner.stderr_name} 확인")

    if snapshot() != before_planner:
        stop("AI 분석 중 원본 변경 감지")

    if git("rev-parse", "HEAD") != original_head:
        stop("HEAD 변경 감지")

    if git("diff", "--cached", "--binary") != original_index:
        stop("index 변경 감지")

    try:
        generated = json.loads(
            (RUN / planner.stdout_name).read_text()
        )
        assert generated["schema_version"] == "inkling_plan_v6"
        assert isinstance(generated["tasks"], list)
        assert generated["tasks"]

        plan_path.write_text(
            json.dumps(generated, ensure_ascii=False, indent=2)
        )

    except Exception as exc:
        stop(f"AI 계획 형식 오류: {exc}")

    print("AI 개발 계획 생성 완료", flush=True)

# 2. JSON 및 파일 경로 검증
try:
    plan = json.loads(plan_path.read_text())
    tasks = plan["tasks"]
    assert isinstance(tasks, list) and tasks
except Exception as exc:
    stop(f"잘못된 작업 지시서: {exc}")

tracked = {
    os.fsdecode(x)
    for x in git("ls-files", "-z").split(b"\0")
    if x
}

def valid_file(name):
    if not isinstance(name, str) or not name:
        return False
    p = REPO / name
    return (
        name in tracked
        and not name.startswith("-")
        and p.is_file()
        and not p.is_symlink()
        and p.resolve().is_relative_to(REPO.resolve())
    )

for task in tasks:
    try:
        assert isinstance(task["files"], list) and task["files"]
        assert isinstance(task["instruction"], str)
        assert task["instruction"].strip()
        assert isinstance(task["acceptance"], list)
        assert all(isinstance(x, str) for x in task["acceptance"])
        assert isinstance(task["test_files"], list)
        assert task["test_files"]
        assert all(valid_file(x) for x in task["files"])
        assert all(
            valid_file(x) and x.startswith("tests/")
            and x.endswith(".py")
            for x in task["test_files"]
        )
    except Exception:
        stop(f"작업 형식 또는 파일 경로 오류: {task}")


# INKLING_COMMAND_COMPILER_V6
import ast


def compile_inkling_task(task, source):
    target, = task["files"]

    if not valid_file(target) or not target.endswith((".py", ".json")):
        raise ValueError("invalid Python target")

    if task.get("read_files") or task.get("allow_no_change"):
        raise ValueError(
            "V6 exact mode forbids references/no-change"
        )


    # V6_STRUCTURED_DATA_SUPPORT
    if target.endswith(".json"):
        original = json.loads(source)

        if not isinstance(original, dict):
            raise ValueError("JSON object required")


        # V6_NESTED_ANCHOR_SUPPORT
        def anchor_records(payload):
            records = {}

            for row in payload.get("anchors", []):
                if not isinstance(row, dict):
                    raise ValueError("invalid anchor record")

                rid = row.get("anchor_id") or row.get("id")

                if not isinstance(rid, str) or not rid:
                    raise ValueError("invalid anchor ID")

                if rid in records:
                    raise ValueError("duplicate anchor ID")

                records[rid] = row

            return records

        original_records = anchor_records(original)

        if set(original) & set(original_records):
            raise ValueError("ambiguous JSON symbol")

        available = set(original) | set(original_records)
    else:
        tree = ast.parse(source)
        available = {
            node.name
            for node in ast.walk(tree)
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            )
        }

    symbols = task["target_symbols"]

    if (
        not isinstance(symbols, list)
        or not symbols
        or not set(symbols) <= available
    ):
        raise ValueError("unknown target symbol")

    expected = exact_patch(source, task["edits"])

    if target.endswith(".json"):
        result = json.loads(expected)

        if not isinstance(result, dict):
            raise ValueError("JSON object required")

        if result.get("topic_id") != original.get("topic_id"):
            raise ValueError("unexpected topic ID change")

        nested = set(symbols) & set(original_records)

        if nested:
            if set(symbols) != nested:
                raise ValueError("mixed JSON symbol scope")

            result_records = anchor_records(result)

            if list(original_records) != list(result_records):
                raise ValueError("anchor identity/order changed")

            before_metadata = {
                k: v for k, v in original.items()
                if k != "anchors"
            }

            after_metadata = {
                k: v for k, v in result.items()
                if k != "anchors"
            }

            if before_metadata != after_metadata:
                raise ValueError("metadata changed outside scope")

            changed = {
                rid for rid in original_records
                if original_records[rid] != result_records[rid]
            }

            if changed != nested:
                raise ValueError(
                    f"unexpected anchor changes: {sorted(changed)}"
                )

            print(
                "Nested Anchor scope PASS:",
                sorted(changed),
                flush=True
            )
    else:
        compile(expected, target, "exec")

    parts = [
        "EXACT EDIT TASK. Apply the supplied edits verbatim.",
        "Only writable file: " + target,
        "Existing symbols: " + ", ".join(symbols),
        "Do not design, refactor or request more context.",
        "Use the exact SEARCH/REPLACE blocks below.",
        "Do not make any additional edits."
    ]

    for edit in task["edits"]:
        parts.append(
            target
            + "\n<<<<<<< SEARCH\n"
            + edit["search"].rstrip("\n")
            + "\n=======\n"
            + edit["replace"].rstrip("\n")
            + "\n>>>>>>> REPLACE"
        )

    prompt = "\n\n".join(parts)

    if len(source.encode()) + len(prompt.encode()) > 100_000:
        raise ValueError("context byte budget exceeded")

    return {
        "target": target,
        "before": source,
        "expected": expected,
        "prompt": prompt,
    }


def preflight_v6(plan):
    if plan.get("schema_version") != "inkling_plan_v6":
        stop("V6: exact-edit plan required")

    virtual = {}
    compiled = []

    for task in plan["tasks"]:
        try:
            target, = task["files"]

            if not valid_file(target):
                raise ValueError("invalid target")

            source = virtual.get(target)

            if source is None:
                source = (
                    REPO / target
                ).read_bytes().decode("utf-8")

            item = compile_inkling_task(task, source)

            virtual[target] = item["expected"]
            compiled.append(item)

        except Exception as exc:
            stop(f"V6 task {task.get('id')}: {exc}")

    return compiled


compiled = preflight_v6(plan)

print("V6 exact-edit preflight PASS")

if "--compile-only" in sys.argv:
    for number, item in enumerate(compiled, 1):
        (RUN / f"compiled_{number}.md").write_text(
            item["prompt"], encoding="utf-8"
        )

    print("Compile-only: no code edit, no grade, no pytest")
    print(f"로그 위치: {RUN}")
    sys.exit(0)

print("\n[2] 작업 계획")
print(json.dumps(plan, ensure_ascii=False, indent=2))

if any(len(t["files"]) > 1 for t in tasks):
    print("\n주의: 여러 파일을 수정하는 작업이 포함되어 있습니다.")

if input("\nAI 코드 수정을 시작할까요? [y/N]: ").strip().lower() != "y":
    stop("사용자가 실행을 취소했습니다.")


# REAL_ANSWER_VALIDATION_V2
import re

ANSWER = ROOT / "test_answers/feedback_control.txt"
VALIDATOR = ROOT / "validate_answer.sh"

if not ANSWER.is_file() or not VALIDATOR.is_file():
    stop("실제 답안 또는 재채점 스크립트 없음")

answer_hash = hashlib.sha256(ANSWER.read_bytes()).hexdigest()

def grade_snapshot(label):
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

before_grade = grade_snapshot("before")


def scope_probe(label):
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


def scope_gate(report):
    cases = {row["case"]: row for row in report["cases"]}
    errors = []

    for name, rule in plan.get("scope_checks", {}).items():
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


if plan.get("scope_checks"):
    scope_probe("before")




# 3. 작업별 Aider 실행
for number, task in enumerate(tasks, 1):
    print(f"\n[작업 {number}/{len(tasks)}]", flush=True)

    files = task["files"]
    before = snapshot()
    backup(f"task_{number}_before")


    item = compiled[number - 1]
    target = REPO / item["target"]

    if target.read_bytes().decode("utf-8") != item["before"]:
        stop("V6: source changed since preflight")

    instruction = item["prompt"]

    task_file = RUN / f"task_{number}.md"
    task_file.write_text(instruction, encoding="utf-8")
    log = RUN / f"aider_{number}.log"

    try:
        cmd, cwd = executor.command(task_file, files, ROOT, REPO)
        editor_env = ENV.copy()
        editor_env["V6_APPROVED_EDITS"] = json.dumps(task["edits"])
        editor_env["V6_EXPECTED_SHA256"] = hashlib.sha256(
            item["expected"].encode("utf-8")
        ).hexdigest()
        code = run(cmd, log, cwd=cwd, env=editor_env)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        stop(f"AI 코드 수정 실행 실패: {exc}")
    backup(f"task_{number}_after")

    if code != 0:
        stop(f"AI 코드 수정 종료 코드: {code}")

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


    print(f"[작업 {number}] 코드 수정 및 변경 범위 검사 통과")

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
    errors = scope_gate(scope_probe("after"))

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

print("\n========================================")
print("전체 계획 실행 및 pytest 검증 통과")
print("자동 커밋 및 Push 없음")
print(f"실행 기록: {RUN}")
print("========================================")

print(git("diff", "--stat").decode(errors="replace"))
