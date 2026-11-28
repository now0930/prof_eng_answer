"""Validate and compile V6 plans without contacting an AI provider."""

import ast
import json
import os

from edit_contract import exact_patch


def compile_inkling_task(task, source, valid_file):
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


def preflight_v6(plan, repo, valid_file, stop):
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
                    repo / target
                ).read_bytes().decode("utf-8")

            item = compile_inkling_task(task, source, valid_file)

            virtual[target] = item["expected"]
            compiled.append(item)

        except Exception as exc:
            stop(f"V6 task {task.get('id')}: {exc}")

    return compiled


def compile_plan(plan_path, repo, git, stop):
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
        p = repo / name
        return (
            name in tracked
            and not name.startswith("-")
            and p.is_file()
            and not p.is_symlink()
            and p.resolve().is_relative_to(repo.resolve())
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

    return plan, tasks, preflight_v6(plan, repo, valid_file, stop)
