from __future__ import annotations

import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
FACT_AUDITOR_PATH = (
    ROOT
    / "scripts"
    / "rubric_audit"
    / "audit_fact_anchor_quality.py"
)
WORK_PACK_PATH = (
    ROOT
    / "scripts"
    / "rubric_audit"
    / "build_rubric_work_pack.py"
)


def load_module(
    name: str,
    path: Path,
) -> ModuleType:
    if not path.exists():
        raise AssertionError(
            f"module is missing: {path}"
        )

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise AssertionError(
            f"cannot create import spec: {path}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RestoredRubricAuditToolsTest(unittest.TestCase):
    def test_sources_are_nonempty_and_use_repo_root(
        self,
    ) -> None:
        fact = load_module(
            "restored_fact_auditor_source_test",
            FACT_AUDITOR_PATH,
        )
        work_pack = load_module(
            "restored_work_pack_source_test",
            WORK_PACK_PATH,
        )

        self.assertGreater(
            FACT_AUDITOR_PATH.stat().st_size,
            1000,
        )
        self.assertGreater(
            WORK_PACK_PATH.stat().st_size,
            1000,
        )

        self.assertEqual(fact.ROOT, ROOT)
        self.assertEqual(work_pack.ROOT, ROOT)

        self.assertTrue(
            str(fact.FACT_PATH).startswith(str(ROOT))
        )
        self.assertTrue(
            str(work_pack.DEFAULT_SRC).startswith(
                str(ROOT)
            )
        )

    def test_fact_auditor_detects_major_fixture(
        self,
    ) -> None:
        fact = load_module(
            "restored_fact_auditor_fixture_test",
            FACT_AUDITOR_PATH,
        )

        fixture = {
            "topics": [
                {
                    "topic_id": "fixture_topic",
                    "anchors": [
                        {
                            "id": "F1",
                            "expected": (
                                "검증용 expected 문장으로 "
                                "충분한 길이를 확보한다."
                            ),
                            "core_terms": [
                                "모범 답안",
                                "정상 용어",
                                "추가 용어",
                            ],
                            "support_terms": [],
                        }
                    ],
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fact_path = tmp_path / "fact.json"
            csv_path = tmp_path / "audit.csv"
            md_path = tmp_path / "audit.md"

            fact_path.write_text(
                json.dumps(
                    fixture,
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            fact.FACT_PATH = fact_path
            fact.OUT_CSV = csv_path
            fact.OUT_MD = md_path

            rc = fact.main()

            self.assertEqual(rc, 0)
            self.assertTrue(csv_path.exists())
            self.assertTrue(md_path.exists())

            with csv_path.open(
                encoding="utf-8-sig",
                newline="",
            ) as handle:
                rows = list(csv.DictReader(handle))

            self.assertTrue(
                any(
                    row.get("severity") == "MAJOR"
                    for row in rows
                )
            )
            self.assertTrue(
                any(
                    "오염 패턴" in row.get(
                        "message",
                        "",
                    )
                    for row in rows
                )
            )

    def test_work_pack_helpers_generate_clean_pack(
        self,
    ) -> None:
        work_pack = load_module(
            "restored_work_pack_helper_test",
            WORK_PACK_PATH,
        )

        self.assertEqual(
            work_pack.parse_nos("3, 6,10"),
            {3, 6, 10},
        )

        cleaned = work_pack.clean_text(
            "<p>첫 문장<br>둘째 문장</p>"
        )

        self.assertNotIn("<p>", cleaned)
        self.assertNotIn("<br>", cleaned)
        self.assertIn("첫 문장", cleaned)
        self.assertIn("둘째 문장", cleaned)

        rows = [
            {
                "no": "3",
                "post_id": "101",
                "title": "검증 항목",
                "suggested_topic_id": (
                    "temperature_measurement_"
                    "error_heat_transfer"
                ),
                "final_class": "KEEP",
                "reason": "검증 이유",
                "needed_action": "fact 보강",
            }
        ]
        posts = {
            "101": {
                "id": 101,
                "content_raw": (
                    "<p>온도 측정오차의 "
                    "열전달 원인을 설명한다.</p>"
                ),
            }
        }

        result = work_pack.make_pack(
            rows,
            posts,
            7000,
        )

        self.assertIn(
            "## Item 3 - 검증 항목",
            result,
        )
        self.assertIn(
            "question_type: CAUSE_ACTION",
            result,
        )
        self.assertNotIn("<p>", result)

    def test_work_pack_main_writes_requested_file(
        self,
    ) -> None:
        work_pack = load_module(
            "restored_work_pack_main_test",
            WORK_PACK_PATH,
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            posts_path = tmp_path / "posts.json"
            decisions_path = tmp_path / "decisions.tsv"
            output_path = tmp_path / "pack.md"

            posts_path.write_text(
                json.dumps(
                    [
                        {
                            "id": 101,
                            "content_text": (
                                "검증용 원문 내용"
                            ),
                        }
                    ],
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            decisions_path.write_text(
                "\t".join(
                    [
                        "no",
                        "post_id",
                        "title",
                        "suggested_topic_id",
                        "final_class",
                        "reason",
                        "needed_action",
                    ]
                )
                + "\n"
                + "\t".join(
                    [
                        "3",
                        "101",
                        "검증 항목",
                        "fixture_topic",
                        "KEEP",
                        "검증 이유",
                        "검증 조치",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            argv = [
                str(WORK_PACK_PATH),
                "--src",
                str(posts_path),
                "--decisions",
                str(decisions_path),
                "--nos",
                "3",
                "--out",
                str(output_path),
            ]

            with patch.object(sys, "argv", argv):
                rc = work_pack.main()

            self.assertEqual(rc, 0)
            self.assertTrue(output_path.exists())
            self.assertIn(
                "## Item 3 - 검증 항목",
                output_path.read_text(
                    encoding="utf-8"
                ),
            )


if __name__ == "__main__":
    unittest.main()
