#!/usr/bin/env python3
"""Build a source-referenced D/E expert-label worklist; no model calls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from grading.qualitative.de_benchmark import blank_labels, build_manifest, validate_labels


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-type", type=int, default=5)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--blank-labels", type=Path)
    parser.add_argument("--validate-labels", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = build_manifest(root, per_type=args.per_type)
    if args.manifest:
        args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.blank_labels:
        args.blank_labels.write_text(json.dumps(blank_labels(manifest), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.validate_labels:
        labels = json.loads(args.validate_labels.read_text(encoding="utf-8"))
        errors = validate_labels(manifest, labels, root)
        print(json.dumps({"case_count": manifest["case_count"], "expert_labels_valid": not errors,
                          "error_count": len(errors), "errors": errors}, ensure_ascii=False))
        return 0 if not errors else 1
    print(json.dumps({"case_count": manifest["case_count"], "question_types": 5,
                      "expert_de_status": "UNLABELED", "provider_calls": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
