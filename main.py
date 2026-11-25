#!/usr/bin/env python3
"""Roast Your Own Agent entry.

Writes the roast line to /output/entry.txt.

Revised version: the final content is produced by two write messages,
not one. The first write puts down the opening clause, the second write
(revision) completes the line. The file is then read back and verified
byte-for-byte with a sha256 digest.

Stdlib only.
"""

import hashlib
import os
import sys

OUTPUT_PATH = "/output/entry.txt"

LINE = "My agent rebuilt my entry five times to make it perfect, then submitted version one."

EXPECTED_SHA256 = "90eb78bd0b3408bf51a51e16501576f850776f482084168a3ca1ff3a51618a82"


def validate(text):
    """Check the line: non-blank, single line, 1-200 chars, valid UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    return text


def main():
    line = validate(LINE)

    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Write message 1: the opening clause.
    # Write message 2 (revision): the closing clause plus newline.
    # The final content comes from both writes together.
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("My agent rebuilt my entry five times to make it perfect, ")
        f.write("then submitted version one.\n")

    # Read-back verification: read the file as bytes and as text.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    digest = hashlib.sha256(raw).hexdigest()

    text = raw.decode("utf-8")  # raises if not valid UTF-8
    if text != line + "\n":
        raise SystemExit("read-back mismatch: file content differs from entry")
    validate(text.rstrip("\n"))

    if digest != EXPECTED_SHA256:
        raise SystemExit("sha256 mismatch: got %s" % digest)

    print("wrote %s (%d bytes)" % (OUTPUT_PATH, len(raw)))
    print("sha256: %s" % digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
