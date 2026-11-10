#!/usr/bin/env python3
"""Regenerate a release snapshot SHA-256 inventory in the flat repository root.

Run only when preparing a new release; it cannot substitute for model validation.
"""
from pathlib import Path
import csv
import hashlib

root = Path(__file__).resolve().parent
manifest = root / 'SHA256_MANIFEST.csv'
files = sorted(p for p in root.iterdir() if p.is_file() and p.name != manifest.name and not p.name.endswith('.pyc'))
with manifest.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['path', 'sha256'])
    for path in files:
        with path.open('rb') as inp:
            writer.writerow([path.name, hashlib.file_digest(inp, 'sha256').hexdigest()])
print(f'SHA256_MANIFEST.csv updated for {len(files)} flat files. Run verify_manifest.py.')
