#!/usr/bin/env python3
import sys
from pathlib import Path
from glob import glob

bad = [chr(0x00C3), chr(0x00C2), chr(0xFFFD)]
hits = []

for arg in sys.argv[1:]:
    paths = glob(arg) or [arg]
    for name in paths:
        p = Path(name)
        if not p.is_file():
            continue
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            if any(x in line for x in bad):
                hits.append((str(p), i, line))

for path, line_no, line in hits:
    print(f"{path}:{line_no}:{line}")

raise SystemExit(1 if hits else 0)
