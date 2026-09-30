#!/usr/bin/env python3
"""Join the two published XH25L V12.15.180 VPN firmware parts and verify them."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import sys

EXPECTED_SIZE = 2_672_910_368
EXPECTED_SHA256 = "7da2d9d03eb0514b4385968b720aecd84351a27d0616504cd377aea13b388750"
CHUNK_SIZE = 8 * 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("part1", type=Path)
    parser.add_argument("part2", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    temp = args.output.with_name(args.output.name + ".partial")
    if args.output.exists() or temp.exists():
        parser.error("output or temporary output already exists; move it first")
    digest = hashlib.sha256()
    size = 0
    try:
        with temp.open("xb") as dst:
            for part in (args.part1, args.part2):
                with part.open("rb") as src:
                    while True:
                        block = src.read(CHUNK_SIZE)
                        if not block:
                            break
                        dst.write(block)
                        digest.update(block)
                        size += len(block)
        actual_hash = digest.hexdigest()
        if size != EXPECTED_SIZE or actual_hash != EXPECTED_SHA256:
            raise ValueError(
                f"verification failed: size={size}, sha256={actual_hash}; "
                f"expected size={EXPECTED_SIZE}, sha256={EXPECTED_SHA256}"
            )
        temp.replace(args.output)
    except Exception as exc:
        temp.unlink(missing_ok=True)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {args.output}")
    print(f"size: {size}")
    print(f"sha256: {actual_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
