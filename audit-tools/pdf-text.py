#!/usr/bin/env python3
"""Best-effort PDF text extraction using only the Python standard library."""

from __future__ import annotations

import re
import sys
import zlib
from pathlib import Path


LITERAL = re.compile(rb"\((?:\\.|[^\\()])*\)")


def decode_literal(value: bytes) -> str:
    value = value[1:-1]
    value = re.sub(
        rb"\\([0-7]{1,3})", lambda match: bytes([int(match.group(1), 8)]), value
    )
    replacements = {
        rb"\n": b"\n",
        rb"\r": b"\r",
        rb"\t": b"\t",
        rb"\b": b"\b",
        rb"\f": b"\f",
        rb"\(": b"(",
        rb"\)": b")",
        rb"\\": b"\\",
    }
    for escaped, plain in replacements.items():
        value = value.replace(escaped, plain)
    try:
        decoded = value.decode("utf-8")
    except UnicodeDecodeError:
        # PDF literal strings without a Unicode marker are byte strings. Using
        # Latin-1 preserves every byte instead of inserting replacement glyphs,
        # which keeps the resulting audit index grep-friendly.
        decoded = value.decode("latin-1")
    return "".join(character for character in decoded if character >= " " or character in "\t\n")


def streams(document: bytes):
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", document, re.DOTALL):
        payload = match.group(1)
        try:
            yield zlib.decompress(payload)
        except zlib.error:
            # Content streams need not be compressed.
            yield payload


def extract(path: Path):
    seen: set[str] = set()
    for stream in streams(path.read_bytes()):
        for text_object in re.finditer(rb"BT(.*?)ET", stream, re.DOTALL):
            line = "".join(
                decode_literal(item) for item in LITERAL.findall(text_object.group(1))
            ).strip()
            if line and line not in seen:
                seen.add(line)
                yield line


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} REPORT.pdf", file=sys.stderr)
        return 2
    for line in extract(Path(sys.argv[1])):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
