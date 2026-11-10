#!/usr/bin/env python3
"""V44 exploratory extensions: neighbour heat connections, community reduction percentages and noise.

This is an engineering *sensitivity*, not an addition to the core, validated community ledger.
The existing 8,884 households already have heat-pump-enabled district hot-water/space heat.
Additional household scenarios refer to separate, hypothetical neighbouring households
*outside* that counted population. Their real locations, thermal loads, network costs,
additional electricity, permits and subscriptions have not been verified. Their reductions
must not be added to percentages computed over the original catchment denominator.

Noise is a transparent free-field point-source bounds check, NOT a BS 4142 assessment:
L_pA(r) = L_wA,combined - 20 log10(r/m) - 8, without screening/reflections,
spectral/tonal penalties, attenuation, plant-cycle profiles, survey background or receptors.
"""
from pathlib import Path
import json, math, csv
import numpy as np
import params as P
from data_io import load_communities
import heat_community as HC

ROOT=Path(__file__).resolve().parent


def heat_extension_fraction(T, comm, frac, grid_g):
    """Fraction of current catchment household count, IN ADDITION, as potential nearby users."""
    h=HC.run(T,comm,return_unused_profiles=True)
    demands,_=HC.node_demands(T,comm)
    n_years=next(iter(T.values())).shape[0]
    source_mwh=0.0; hp_electric_mwh=0.0; fossil_counterfactual_t=0.0
    electricity_counterfactual_t=0.0; washing_counterfactual_t=0.0
    population_extra=0.0
    node_details=[]
    H=P.HEAT; fuel=P.FUEL_EF
    for node in P.NODES:
        d=demands[node]
        available=h['unused_source_heat_profiles_mwh'][node]
        requested=np.maximum(d['home_loop']*frac,0)
        matched=np.minimum(requested,available)
        service=np.divide(matched,requested,out=np.zeros_like(matched),where=requested>0)
        space=(d['space']*frac*service).sum()/n_years
        hot=(d['hot']*frac*service).sum()/n_years
        hp=(d['home_el']*frac*service).sum()/n_years
        conn_homes=d['connected_households']*frac
        washing_hh_profile = conn_homes*H['washing_mwh_hh']/8760
        washing=(washing_hh_profile*service).sum()/n_years
        # Fossil heat displaced, allowing for existing electrical off-gas mix.
        off=H['off_gas_share'][node]; mix=H['off_gas_fuel']
        fossil_factor=(1-off)*fuel['gas']+off*(mix['heating_oil']*fuel['heating_oil']+mix['lpg']*fuel['lpg'])
        fuel_avoided=(space+hot-washing)/H['boiler_eff']*fossil_factor
        grid_avoided=(space+hot-washing)*off*mix['electric']*grid_g/1e3
        wash_avoided=washing*grid_g/1e3
        source_mwh+=matched.sum()/n_years
        hp_electric_mwh+=hp
        fossil_counterfactual_t+=fuel_avoided
        electricity_counterfactual_t+=grid_avoided
        washing_counterfactual_t+=wash_avoided
        population_extra+=conn_homes
        node_details.append(dict(node=P.NODE_LABEL[node],potential_additional_households=round(conn_homes,1),
                                 matched_heat_gwh=round(matched.sum()/n_years/1e3,4),
                                 requested_heat_gwh=round(requested.sum()/n_years/1e3,4),
                                 matched_fraction=round(float(matched.sum()/max(requested.sum(),1e-9)),4)))
    pump_emissions_t=hp_electric_mwh*grid_g/1e3
    extra_avoided=fossil_counterfactual_t+electricity_counterfactual_t+washing_counterfactual_t-pump_emissions_t
    return dict(additional_household_fraction=frac, hypothetical_additional_households=round(population_extra,1),
                hourly_matched_source_heat_gwh=round(source_mwh/1e3,3),
                additional_hp_electricity_gwh=round(hp_electric_mwh/1e3,3),
                potential_avoided_t_co2e_y=round(extra_avoided,1),
                potential_avoided_kt_co2e_y=round(extra_avoided/1000,3),
                conditional_no_storage=True,requires_new_customers=True,
                baseline_increase_is_not_additive=True, details=node_details)


def noise_examples():
    rows=[]
    for lwa in (95,105,115):
        for dist in (100,250,500):
            lp=lwa-20*math.log10(dist)-8
            for mitigation in (0,3,6,10):
                for correction in (0,6):
                    for bg in (35,40):
                        rating=lp-mitigation+correction
                        rows.append(dict(aggregate_sound_power_dba=lwa,distance_m=dist,
                            propagation_only_lp_dba=round(lp,1),illustrative_source_mitigation_db=mitigation,
                            acoustic_energy_reduction_pct=round(100*(1-10**(-mitigation/10)),1),
                            illustrative_character_penalty_db=correction,
                            assumed_background_la90_dba=bg,rating_minus_background_db=round(rating-bg,1),
                            bs4142_compliance='not assessed'))
    return rows


def main():
    with (ROOT/'heat_community.json').open() as f: old=json.load(f)
    lfull=old['ledger_full']; lw=old['ledger_weighted']
    den=lfull['baselines']['residents_plus_cattle_t']
    extfull=lfull['rows']; extw=lw['rows']
    keys_heat=[k for k in extfull if 'Home heating' in k or 'washing and cleaning' in k or 'Drying contracts' in k]
    keys_biogas=[k for k in extfull if 'Biomethane' in k or 'storage methane' in k or 'leak detection' in k]
    sum_full=lambda keys:sum(extfull[k] for k in keys)
    sum_weight=lambda keys:sum(extw[k] for k in keys)
    unapproved=[k for k in extfull if 'Asparagopsis' in k]
    emissions=dict(denominator_description="Existing 20,966 residents' UK-average territorial emissions plus the modelled catchment cattle's emissions",
       denominator_t_co2e_y=den,
       full=dict(kt_co2e_y=lfull['total_t']/1000,pct=100*lfull['total_t']/den),
       tier_weighted=dict(kt_co2e_y=lw['total_t']/1000,pct=100*lw['total_t']/den),
       full_without_unapproved_seaweed=dict(kt_co2e_y=(lfull['total_t']-sum_full(unapproved))/1000,pct=100*(lfull['total_t']-sum_full(unapproved))/den),
       weighted_without_unapproved_seaweed=dict(kt_co2e_y=(lw['total_t']-sum_weight(unapproved))/1000,pct=100*(lw['total_t']-sum_weight(unapproved))/den),
       heat_linked_full=dict(kt_co2e_y=sum_full(keys_heat)/1000,pct_of_community_baseline=100*sum_full(keys_heat)/den,
                             pct_of_full_savings=100*sum_full(keys_heat)/lfull['total_t']),
       heat_linked_weighted=dict(kt_co2e_y=sum_weight(keys_heat)/1000,pct_of_community_baseline=100*sum_weight(keys_heat)/den,
                                 pct_of_weighted_savings=100*sum_weight(keys_heat)/lw['total_t']),
       biogas_and_manure_full=dict(kt_co2e_y=sum_full(keys_biogas)/1000,pct_of_community_baseline=100*sum_full(keys_biogas)/den),
       biogas_and_manure_weighted=dict(kt_co2e_y=sum_weight(keys_biogas)/1000,pct_of_community_baseline=100*sum_weight(keys_biogas)/den))
    assert abs(emissions['full']['pct']-55.4955)<0.02
    assert abs(emissions['tier_weighted']['pct']-28.8324)<0.02
    # Optional future adjacent-household scenarios: no uplift claimed in original catchment.
    T=HC.temps(); comm=load_communities()
    h10=heat_extension_fraction(T,comm,0.10,old['grid_mean_g_kwh'])
    h20=heat_extension_fraction(T,comm,0.20,old['grid_mean_g_kwh'])
    out=dict(method='V44 transparent emissions percentages and exploratory heat/noise sensitivities',emissions=emissions,
             neighbouring_household_sensitivities={'plus_10_percent':h10,'plus_20_percent':h20},
             noise_method='Hemispherical ground-level illustrative point source, not measured Lw, receptor distance, background or BS 4142 conclusion',
             noise_examples=noise_examples(),
             caveats=['No extension benefit is included in original 109.1/56.7 kt totals or 55/29% values.',
                      'Additional household connections require a larger population boundary, verified nearby customers, pipes, cost, thermal stores and planning.',
                      'Biomethane cooking/heating reallocates the same existing 7.03 kt gas-substitution credit: it is not an extra saving.',
                      'No sound level or plant data for a site-specific BS 4142:2014+A1:2019 assessment.'])
    (ROOT/'V44_COMMUNITY_EXTENSION_SCREEN.json').write_text(json.dumps(out,indent=2)+'\n')
    with (ROOT/'V44_NOISE_SCREEN.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(out['noise_examples'][0]));writer.writeheader();writer.writerows(out['noise_examples'])
    print(json.dumps({"emissions":emissions,"potential_ext":{k: {z:v[z] for z in ['hypothetical_additional_households','hourly_matched_source_heat_gwh','potential_avoided_kt_co2e_y']} for k,v in out['neighbouring_household_sensitivities'].items()}},indent=2))

if __name__=='__main__': main()
