#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bot


class BotLoggingTest(unittest.TestCase):
    def test_log_writes_once_to_stdout(self) -> None:
        # LOG_FILE.open 같은 PosixPath 인스턴스 메서드는 read-only라
        # 직접 patch하지 않고 bot 모듈의 LOG_FILE 변수를 mock으로 교체한다.
        with (
            patch.object(bot, "ensure_dirs"),
            patch("builtins.print") as mocked_print,
            patch.object(bot, "LOG_FILE") as mocked_log_file,
        ):
            bot.log("single-sink-test")

        mocked_print.assert_called_once()

        args, kwargs = mocked_print.call_args

        self.assertIn("single-sink-test", args[0])
        self.assertTrue(kwargs.get("flush"))
        mocked_log_file.open.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
