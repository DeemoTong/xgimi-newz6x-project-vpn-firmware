#!/usr/bin/env python3
"""Split a firmware file into GitHub Release-sized parts and write SHA256SUMS."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

PART_SIZE = 1_500_000_000  # GitHub requires each release asset to be under 2 GiB.
CHUNK_SIZE = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(CHUNK_SIZE):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("firmware", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--stem", default="xgimi-newz6x-vpn-v12.15.180")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    size = args.firmware.stat().st_size
    part_count = (size + PART_SIZE - 1) // PART_SIZE
    part_paths = [args.output_dir / f"{args.stem}.part{i:02d}.bin" for i in range(1, part_count + 1)]
    sums_path = args.output_dir / "SHA256SUMS.txt"
    if sums_path.exists() or any(path.exists() for path in part_paths):
        parser.error("output files already exist; use an empty output directory")
    original_hash = hashlib.sha256()
    try:
        with args.firmware.open("rb") as source:
            for part_path in part_paths:
                part_hash = hashlib.sha256()
                remaining = PART_SIZE
                with part_path.open("xb") as target:
                    while remaining:
                        block = source.read(min(CHUNK_SIZE, remaining))
                        if not block:
                            break
                        target.write(block)
                        part_hash.update(block)
                        original_hash.update(block)
                        remaining -= len(block)
                print(f"{part_hash.hexdigest()}  {part_path.name}")
        actual = sum(path.stat().st_size for path in part_paths)
        if actual != size:
            raise IOError(f"split size mismatch: {actual} != {size}")
        with sums_path.open("x", encoding="utf-8", newline="\n") as sums:
            for path in part_paths:
                sums.write(f"{sha256_file(path)}  {path.name}\n")
            sums.write(
                f"{original_hash.hexdigest()}  "
                "XGIMI_IRONMAN_XH25L_V12.15.180_VPN-EXPERIMENTAL-CRC-FIXED.bin\n"
            )
    except Exception:
        for path in part_paths:
            path.unlink(missing_ok=True)
        sums_path.unlink(missing_ok=True)
        raise
    print(f"Wrote {part_count} parts and {sums_path}; original SHA-256: {original_hash.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
