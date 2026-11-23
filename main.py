#!/usr/bin/env python3
"""Submitted program for the news-image-20261123 make.fun entry.

The deliverable is the front-page picture bundled in this
repository as entry.png.  This program publishes it: it copies
entry.png to /output/entry.png, falling back to ./output/entry.png
beside this file when /output does not exist.  It uses only the
standard library, touches no network, and reads no clock, so every
run writes exactly the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PREFERRED_DIR = "/output"


def pick_output_dir():
    """Return /output when present, else a local output folder."""
    if os.path.isdir(PREFERRED_DIR):
        return PREFERRED_DIR
    return os.path.join(HERE, "output")


def publish():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png is missing beside main.py")
    out_dir = pick_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    return target


if __name__ == "__main__":
    written = publish()
    print("wrote {} ({} bytes)".format(written, os.path.getsize(written)))
