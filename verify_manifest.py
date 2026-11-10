#!/usr/bin/env python3
"""Verify distributed V39 research archive against its SHA-256 manifest."""
from pathlib import Path
import csv
import hashlib
import sys
root=Path(__file__).resolve().parent
manifest=root/'SHA256_MANIFEST.csv'
with manifest.open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f))
expected={r['path']:r['sha256'] for r in rows}
errors=[]
for rel,hashval in expected.items():
    target=root/rel
    if not target.is_file():
        errors.append(f'MISSING {rel}');continue
    actual=hashlib.file_digest(target.open('rb'),'sha256').hexdigest()
    if actual != hashval:errors.append(f'MISMATCH {rel}')
actual_files={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST.csv' and '__pycache__' not in p.parts}
for extra in sorted(actual_files-set(expected)):
    errors.append(f'UNLISTED {extra}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(rows)} files match V39 SHA-256 inventory; no unlisted release files.')
