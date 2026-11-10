#!/usr/bin/env python3
"""Explicit named-campus engineering screens, not operator emissions inventories.
Standard library only; Python 3.10+; output located under OUTPUT/.
"""
import csv
from pathlib import Path
from dataclasses import dataclass
HOURS=8760
UTIL=0.90
PUE=1.20
RECOVERABLE=0.85*0.85
GB_G_PER_KWH=177.32660887557077
GPU_KW_IT=2.06
@dataclass(frozen=True)
class Scenario:
    site: str
    rated_mw:float
    basis: str
    jobs: int|None=None
SITES=[
 Scenario('QTS Cambois full build, 720 MW IT',720,'IT',400),
 Scenario('Stellium 1, 15 MW facility-power allocation',15,'facility power'),
 Scenario('Stellium campus, 80 MW available facility power',80,'facility power'),
 Scenario('Stargate UK, proposed 8,000 GPUs, UK-wide',8_000*GPU_KW_IT/1000,'IT'),
 Scenario('Stargate UK, proposed 31,000 GPUs, UK-wide',31_000*GPU_KW_IT/1000,'IT'),
]
def estimate(site):
    it=site.rated_mw if site.basis=='IT' else site.rated_mw/PUE
    it_gwh=it*UTIL*HOURS/1000
    facility_gwh=it_gwh*PUE
    return dict(site=site.site,published_capacity_mw=site.rated_mw,capacity_basis=site.basis,
        hypothetical_it_mw=round(it,6),hypothetical_facility_gwh_year=round(facility_gwh,6),
        potential_recoverable_it_heat_gwh_year=round(it_gwh*RECOVERABLE,6),
        location_based_screen_kt_co2_year=round(facility_gwh*GB_G_PER_KWH/1000,6),
        published_operational_jobs=site.jobs if site.jobs is not None else '',
        announced_jobs_per_it_mw=round(site.jobs/it,6) if site.jobs is not None else '')
def main():
    rows=[estimate(site) for site in SITES]
    qts,st15,st80,sg8,sg31=rows
    assert abs(qts['potential_recoverable_it_heat_gwh_year']-4101.2568)<1e-5
    assert abs(st15['potential_recoverable_it_heat_gwh_year']-71.202375)<1e-5
    assert abs(st80['potential_recoverable_it_heat_gwh_year']-379.746)<.003
    assert 93<sg8['potential_recoverable_it_heat_gwh_year']<95
    assert 363<sg31['potential_recoverable_it_heat_gwh_year']<365
    assert abs(qts['announced_jobs_per_it_mw']-400/720)<1e-5
    assert len(rows)==5
    out=Path('OUTPUT');out.mkdir(exist_ok=True)
    with (out/'REGIONAL_SITE_SCREEN.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print('Regional campus: 7 checks passed. Technical heat potential is NOT actual wasted heat.')
if __name__=='__main__':main()
