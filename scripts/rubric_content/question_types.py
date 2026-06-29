from __future__ import annotations

import argparse
from typing import Any

from rubric_registry import load_question_type_profile


def _coerce_question_type_row(key: Any, item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        row = dict(item)
        if key is not None:
            row.setdefault("id", str(key))
        qid = str(row.get("id") or row.get("question_type") or key or "")
        row["id"] = qid
        row["name"] = row.get("name") or row.get("name_ko") or row.get("title") or ""
        c_lens = (
            row.get("c_lens")
            or row.get("c_fact_focus")
            or row.get("description")
            or row.get("note")
            or ""
        )
        if isinstance(c_lens, list):
            c_lens = ", ".join(str(x) for x in c_lens)
        row["c_lens"] = str(c_lens)
        return row

    qid = str(key if key is not None else item)
    row = {"id": qid, "name": "", "c_lens": ""}
    try:
        from question_type_taxonomy import get_question_type_profile

        profile = get_question_type_profile(qid) or {}
        row["name"] = profile.get("name") or profile.get("name_ko") or profile.get("title") or ""
        c_lens = profile.get("c_lens") or profile.get("c_fact_focus") or profile.get("description") or ""
        if isinstance(c_lens, list):
            c_lens = ", ".join(str(x) for x in c_lens)
        row["c_lens"] = str(c_lens)
    except Exception:
        pass
    return row


def _iter_question_type_rows(profile: dict[str, Any]):
    types = profile.get("types", [])
    if isinstance(types, dict):
        for key in sorted(types):
            yield _coerce_question_type_row(key, types[key])
        return
    if isinstance(types, list):
        for item in types:
            yield _coerce_question_type_row(None, item)
        return


def cmd_list_types(_args: argparse.Namespace) -> int:
    profile = load_question_type_profile()
    rows = list(_iter_question_type_rows(profile))
    if not rows:
        print("NO QUESTION TYPES")
        return 0

    for item in rows:
        qid = str(item.get("id") or "")
        name = str(item.get("name") or "")
        c_lens = str(item.get("c_lens") or "")
        print(f"{qid:32} | {name} | {c_lens}")
    return 0


def add_parser(sub) -> None:
    p = sub.add_parser("list-types", help="List question types")
    p.set_defaults(func=cmd_list_types)
