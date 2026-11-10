#!/usr/bin/env python3
"""Verify the complete flat V41 research release against SHA-256 checksums.

Use before recomputation; reproducing outputs may change bytes and invalidate
this *release snapshot* inventory without implying a scientific failure.
"""
from pathlib import Path
import csv
import hashlib
import sys

root = Path(__file__).resolve().parent
manifest = root / 'SHA256_MANIFEST.csv'
if not manifest.exists():
    raise SystemExit('SHA256_MANIFEST.csv missing from repository root')
with manifest.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
expected = {r['path']: r['sha256'] for r in rows}
if len(rows) != len(expected):
    raise SystemExit('Duplicate filenames in SHA256_MANIFEST.csv')
errors = []
for rel, digest in expected.items():
    path = root / rel
    if '/' in rel or '\\' in rel or not path.is_file():
        errors.append(f'MISSING OR NON-FLAT {rel}')
        continue
    with path.open('rb') as f:
        actual = hashlib.file_digest(f, 'sha256').hexdigest()
    if actual != digest:
        errors.append(f'MISMATCH {rel}')
ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache', '.mypy_cache'}
actual = {
    p.name for p in root.iterdir()
    if p.is_file() and p.name != manifest.name and not p.name.endswith('.pyc')
}
for extra in sorted(actual - set(expected)):
    errors.append(f'UNLISTED {extra}')
for folder in root.iterdir():
    if folder.is_dir() and folder.name not in ignore_dirs:
        errors.append(f'NON-FLAT DIRECTORY {folder.name}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(rows)} files match flat V41 SHA-256 inventory.')
