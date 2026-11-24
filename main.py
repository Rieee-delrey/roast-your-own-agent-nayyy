#!/usr/bin/env python3
"""Roast Your Own Agent (u-nayyy-roast-your-own-agent-4c3d413c).
Writes one line roasting my own AI agent to /output/entry.txt, then reads
it back and verifies the gate (UTF-8, exactly one line, 1-200 chars) and
that the bytes are exactly the line, exiting non-zero on any failure."""
import hashlib
import os
import sys

LINE = "My agent is fully autonomous, as long as I approve every step, answer every question, and do the last step myself."


def main():
    if not 1 <= len(LINE) <= 200:
        print(f"gate fail: line is {len(LINE)} chars, must be 1-200", file=sys.stderr)
        sys.exit(1)
    if "\n" in LINE or LINE.strip() != LINE:
        print("gate fail: line must be a single line with no surrounding whitespace", file=sys.stderr)
        sys.exit(1)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(LINE)
    # Read-back verification: the file must be byte-identical to the line.
    with open("/output/entry.txt", "rb") as f:
        data = f.read()
    if data != LINE.encode("utf-8"):
        print("verification fail: /output/entry.txt does not match LINE", file=sys.stderr)
        sys.exit(1)
    text = data.decode("utf-8")
    if text.count("\n") != 0 or not 1 <= len(text) <= 200:
        print("verification fail: gate check on read-back text", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
