#!/usr/bin/env python3
"""Write one funny epitaph to the make.fun output file.

The epitaph is a single line of famous last words, at most 150
characters. The program writes it to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt), then reads the file back and checks the
bytes match, so a bad write fails loudly instead of silently.
"""

import os
import sys

EPITAPH = "I finally reached inbox zero. It only took dying."

MAX_CHARS = 150


def main() -> int:
    text = EPITAPH.strip()
    if not text:
        print("error: epitaph is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "error: epitaph is %d characters, over the %d limit"
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if "\n" in text or "\r" in text:
        print("error: epitaph must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    data = text.encode("utf-8")
    with open(out_path, "wb") as handle:
        handle.write(data)

    with open(out_path, "rb") as handle:
        written = handle.read()
    if written != data:
        print("error: written bytes do not match the epitaph", file=sys.stderr)
        return 1

    print("wrote %d bytes to %s" % (len(data), out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
