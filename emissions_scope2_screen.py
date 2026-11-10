#!/usr/bin/env python3
"""Symmetrical carbon boundaries for proposed North Tyne AI and matched grid campus.
These attributional ledgers are NOT causal emissions avoidance or audited inventories.
No equivalent hourly certificate ownership is demonstrated for competitors.
"""
from pathlib import Path
import csv
DG_GWH=887.6193307204849
TWIN_GWH=884.663892288
GRID_G_PER_KWH=177.32660887557077
DG_CONDITIONAL_HOURLY_KT=37.0
DG_LOCATION_KT=DG_GWH*GRID_G_PER_KWH/1000
TWIN_LOCATION_KT=TWIN_GWH*GRID_G_PER_KWH/1000
TWIN_EQUAL_HOURLY_KT=DG_CONDITIONAL_HOURLY_KT*TWIN_GWH/DG_GWH
SCENARIOS=[
 ('Location based: all grid-served electricity',DG_LOCATION_KT,TWIN_LOCATION_KT,'Symmetrical historical GB average applied to facility consumption'),
 ('Hourly market attributes: only DG has verified matching (conditional)',DG_CONDITIONAL_HOURLY_KT,TWIN_LOCATION_KT,'Unequal conditional contracts; NOT an observed atmospheric reduction'),
 ('Hourly market attributes: both have equivalent matching (hypothetical)',DG_CONDITIONAL_HOURLY_KT,TWIN_EQUAL_HOURLY_KT,'Illustrative hourly matching; full residual mix and certificate evidence missing'),
 ('Consequential A: no proven additional renewable capacity',DG_LOCATION_KT,TWIN_LOCATION_KT,'Do not attribute avoided CO2 to contracts alone'),
 ('Consequential B: verified additional capacity and marginal displacement',None,None,'Unquantifiable without hourly marginal emissions, curtailment and CfD counterfactual'),
]
def main():
    assert abs(DG_LOCATION_KT-157.39852588906732)<1e-7
    assert abs(TWIN_LOCATION_KT-156.87444801409427)<1e-7
    assert abs((DG_LOCATION_KT-TWIN_LOCATION_KT)-.52407787497304)<1e-5
    assert abs(TWIN_EQUAL_HOURLY_KT-36.876803920084555)<1e-7
    assert abs(DG_GWH-TWIN_GWH-2.9554384324849)<1e-5
    out=Path(__file__).resolve().parent
    with (out/'CARBON_ACCOUNTING_SCREEN.csv').open('w',newline='',encoding='utf-8') as f:
       w=csv.writer(f);w.writerow(['accounting_scenario','digital_gardens_kt_co2_year','grid_twin_kt_co2_year','qualification'])
       for name,dg,twin,q in SCENARIOS:w.writerow([name,'' if dg is None else f'{dg:.6f}','' if twin is None else f'{twin:.6f}',q])
    print('5 symmetrical-accounting checks passed; no quantified consequential reduction.')
if __name__=='__main__':main()
