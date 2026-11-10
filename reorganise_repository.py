#!/usr/bin/env python3
"""Deprecated V39 migration utility; flat V41 layout requires NO reorganisation.

This name is retained so an old instruction cannot inadvertently move data into
folders and break the working flat release. It does not alter any files.
"""
from pathlib import Path
root = Path(__file__).resolve().parent
required = ['params.py', 'power_247.py', 'communities.csv', 'design.json',
            'gb_national_intensity.csv.gz', 'falstone_hourly_era5.csv.gz']
missing = [name for name in required if not (root / name).is_file()]
if missing:
    raise SystemExit('Missing required flat-layout files: ' + ', '.join(missing))
print('Flat-layout check passed; no files moved. Run python verify_manifest.py next.')
