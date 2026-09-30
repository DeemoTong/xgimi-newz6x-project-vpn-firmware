#!/usr/bin/env python3
"""Verify the XGIMI USB firmware package footer and optional SHA-256."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import struct
import zlib

HEADER_SIZE = 16 * 1024
FOOTER_SIZE = 32
MAGIC = b"12345678"
CHUNK_SIZE = 8 * 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("firmware", type=Path)
    parser.add_argument("--sha256", help="expected SHA-256, optional")
    args = parser.parse_args()
    size = args.firmware.stat().st_size
    if size < HEADER_SIZE + FOOTER_SIZE:
        parser.error("file is too small to be an XGIMI firmware package")
    digest = hashlib.sha256()
    crc2 = 0
    with args.firmware.open("rb") as stream:
        header = stream.read(HEADER_SIZE)
        crc1 = zlib.crc32(header) & 0xFFFFFFFF
        stream.seek(0)
        remaining = size - 24
        while remaining:
            block = stream.read(min(CHUNK_SIZE, remaining))
            if not block:
                raise EOFError("unexpected end of firmware")
            digest.update(block)
            crc2 = zlib.crc32(block, crc2)
            remaining -= len(block)
        crc2 = zlib.crc32(struct.pack("<I", crc1), crc2) & 0xFFFFFFFF
        stream.seek(size - 24)
        digest.update(stream.read(24))
        stream.seek(size - FOOTER_SIZE)
        footer = stream.read(FOOTER_SIZE)
    stored1, stored2 = struct.unpack("<II", footer[8:16])
    if footer[:8] != MAGIC or footer[16:] != header[:16]:
        parser.error("XGIMI footer magic/header reference does not match")
    if (stored1, stored2) != (crc1, crc2):
        parser.error(f"CRC mismatch: stored={stored1:08x}/{stored2:08x}, computed={crc1:08x}/{crc2:08x}")
    actual_sha = digest.hexdigest()
    if args.sha256 and actual_sha.lower() != args.sha256.lower():
        parser.error(f"SHA-256 mismatch: got {actual_sha}")
    print(f"OK: {args.firmware}")
    print(f"size: {size}")
    print(f"CRC1: {crc1:08x}; CRC2: {crc2:08x}")
    print(f"SHA-256: {actual_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
