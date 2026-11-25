#!/usr/bin/env python3
"""Roast Your Own Agent entry.

Writes the one-line roast to /output/entry.txt, then reads it back
and verifies the content byte-for-byte, printing its SHA-256.
Standard library only.
"""

import hashlib
import os
import sys

LINE = "My agent rebuilt my entry five times to make it perfect, then submitted version one."

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    line = LINE.strip()
    if not line:
        print("error: entry line is blank", file=sys.stderr)
        return 1
    if "\n" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(line) <= 400:
        print("error: entry must be 1-400 characters, got %d" % len(line), file=sys.stderr)
        return 1
    line.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")

    with open(OUTPUT_PATH, "rb") as f:
        data = f.read()
    if data.decode("utf-8") != line + "\n":
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (OUTPUT_PATH, len(data)))
    print("sha256: %s" % hashlib.sha256(data).hexdigest())
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
