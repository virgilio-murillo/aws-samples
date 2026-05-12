#!/usr/bin/env python3
"""Validate all Jupyter notebooks have valid JSON and nbformat schema."""
import sys
import glob
import nbformat

EXCLUDE = {".ipynb_checkpoints", "investigation", "kiro-test", "kiro-notes"}

notebooks = [
    n for n in glob.glob("**/*.ipynb", recursive=True)
    if not any(ex in n for ex in EXCLUDE)
]

errors = []
for path in sorted(notebooks):
    try:
        with open(path) as f:
            nb = nbformat.read(f, as_version=4)
        nbformat.validate(nb)
    except Exception as e:
        errors.append(f"{path}: {e}")

if errors:
    for e in errors:
        print(f"FAIL: {e}", file=sys.stderr)
    sys.exit(1)
print(f"OK: {len(notebooks)} notebooks valid")
