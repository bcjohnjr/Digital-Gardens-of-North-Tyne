#!/usr/bin/env python3
"""Move legacy files from a flat GitHub upload to expected DATA/ and OUTPUT/ paths.
Run in the root of the cloned repository. No third-party modules required.
Leaves any conflicting file in place; never silently overwrites.
"""
from pathlib import Path
import shutil
r=Path(__file__).resolve().parent
historical_suffix='_hourly_era5.csv.gz'
grid={'gb_market_index_price.csv.gz','gb_national_intensity.csv.gz','north_east_england_intensity_mix.csv.gz','provenance.json'}
outputs={'PV_LCA_SCREEN.csv','PV_LCA_SCREEN.json','REVISED_SENSITIVITY.csv','REVISED_SENSITIVITY.json','SPECTRUM_XGS_LOWER_BOUNDS.csv','SPECTRUM_XGS_LOWER_BOUNDS.json','TURBINE_N1_POWER_LIMIT.csv','compare_econ.json','design.json','design_econ.json','design_grid.npz','design_trajectory.json','export_scenarios.json','heat_community.json','island_network.json','power_247.json','power_247_grid.npz','trajectory.json'}
def dest(name):
 if name.endswith(historical_suffix) or name in ('locations.json','provenance_manifest.json'):return r/'DATA'/'Digital_Gardens_UK_ERA5_historical'/name
 if name in grid:return r/'DATA'/'Digital_Gardens_UK_GRID'/name
 if name in {'communities.csv','digital_gardens_uk_era5.py','digital_gardens_uk_grid.py'}:return r/'DATA'/name
 if name in outputs:return r/'OUTPUT'/name
 if name.startswith('Figure_9_'):return r/'FIGURES'/name
 return None
moved=0;duplicates=0;conflicts=[]
for f in r.iterdir():
 if not f.is_file():continue
 d=dest(f.name)
 if d is None:continue
 d.parent.mkdir(exist_ok=True,parents=True)
 if d.exists():
   if f.read_bytes()==d.read_bytes():f.unlink();duplicates+=1
   else:conflicts.append(str(f.name))
 else:
   shutil.move(str(f),str(d));moved+=1
print(f'Reorganised {moved}; deleted {duplicates} byte-identical flat duplicates; conflicts {conflicts}')
if conflicts:raise SystemExit('Resolve conflicting source files manually before committing.')
