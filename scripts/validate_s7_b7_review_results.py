#!/usr/bin/env python3
"""Validate local-only S7 B7 review inputs and report sanitized counts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from grading.evidence.s7_b7_review_validation import ReviewValidationError, validate_review_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-packet", default="calibration/s7_b7_expert_review_packet_v1.json")
    parser.add_argument("--blind-packet", default="tmp/s7_b7_blind_review/blinded_packet.json")
    parser.add_argument("--results", default="tmp/s7_b7_blind_review/review_results.json")
    parser.add_argument("--audit", default="tmp/s7_b7_blind_review/author_audit_and_key.json")
    parser.add_argument("--repository-root", default=str(REPOSITORY_ROOT))
    args = parser.parse_args()
    try:
        summary = validate_review_bundle(
            args.source_packet,
            args.blind_packet,
            args.results,
            args.audit,
            args.repository_root,
        )
    except ReviewValidationError as exc:
        # Error identifiers are static; never print private answer or reviewer data.
        print(json.dumps({"status": "REJECTED", "reason_code": str(exc)}, sort_keys=True))
        return 1
    except Exception:
        print(json.dumps({"status": "REJECTED", "reason_code": "VALIDATION_INTERNAL_ERROR"}, sort_keys=True))
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
