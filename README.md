# Digital Gardens of North Tyne Valley — V41 flat GitHub research release

*Energy & Environmental Science* (Royal Society of Chemistry); Analysis manuscript, 10 November 2026.

This is the numerical research release and is not itself the journal manuscript. Modelled outcomes are scenarios, **not measured operator performance**. The `build_manuscript.py` file is a legacy draft helper, and must **not** be used to overwrite the separately curated RSC submission documents.

## Flat layout: no folders needed

All 2010–2025 ERA5 `.csv.gz` files, 2018–2025 grid records, `.py` scripts, prepared `.json` / `.csv` / `.npz` outputs, metadata and verification tools are located **directly in the repository root**. There are **no DATA/ or OUTPUT/ folders**. All model scripts use the root of the script directory; they can be invoked from any current working directory.

Public repository: https://github.com/bcjohnjr/Digital-Gardens-of-North-Tyne

## Set up and verify from a new clone

Requires Python 3.11+ and `numpy`, `pandas`, `scipy`, and `matplotlib` for the model (optional legacy Word helper requires `python-docx`). Clone or download the exact release, and from the repository directory run:

```bash
python verify_manifest.py
python reorganise_repository.py   # optional non-destructive flat-layout check; never moves files
python validate.py
```

`verify_manifest.py` tests the distributed **byte-for-byte release snapshot**. Run it **before** regenerating any output. A Git clone has a hidden `.git` directory, which the verifier intentionally ignores. Any extra untracked files in root should be removed or accounted for before release verification.

## Regenerate numerical results

Run these in order, from the repository root; there are no directory-renaming or extraction steps:

```bash
python power_247.py
python power_247.py design
python trajectory.py
python design_trajectory.py
python heat_community.py
python island_network.py
python export_scenarios.py
python compare_econ.py
python design_econ.py
python regional_site_screen.py
python emissions_scope2_screen.py
python pv_lca_screen.py
python spectrum_xgs_screen.py
python turbine_trip_screen.py
python revised_sensitivities.py
python validate.py
```

`validate.py` contains **149 model assertions**. `regional_site_screen.py` adds **seven** checks, and `emissions_scope2_screen.py` adds **five** checks (161 total, when all pass). The power-design search can be computationally intensive. The `figures.py` helper creates exploratory figures in the **root** and is **not** the generator of the final curated journal figures. The two historical data-download scripts can create working cache folders and ZIPs for new raw data downloads; they are optional and not necessary for reproducing the prepared input release. Their own download archives are not the canonical model input paths.

The included `REVISED_SENSITIVITY` output incorporates the corrected community ledger; the constant-baseline 25-year gross avoidance is approximately **2,727 kt** (not 2,800.8 kt). Directional 10%- and 2%-annual-decline sensitivities yield approximately 1.01 and 2.16 Mt. The other existing assumptions and scenario qualifications are preserved.

## Re-issuing a snapshot manifest

Recomputing output files may alter byte representations (especially compressed and NumPy files) or output ordering without changing rounded scientific results. After validating numerical reproducibility, use `python make_manifest.py` to create a new **release snapshot** inventory and then rerun `python verify_manifest.py`. Do **not** regenerate the checksums to conceal a failed independent validation.

## Attribution and limitations

The community electricity loads from household heat pumps and EVs receive historical location-based grid emissions. The gross conditional annual community ledger is 109.1 kt CO2e (full delivery), 95.2 kt (no seaweed approval), 47.6 kt (half uptake), and 56.7 kt (tier-weighted uptake), excluding incremental vehicle manufacturing. Recoverable campus heat is a technical estimate, not documented useful heat offtake. The £25.7/MWh TNUoS proxy is not a verified site tariff; `REVISED_SENSITIVITY` fixed-charge results vary Digital Gardens alone, **not** a matched grid twin. North East-wide scaling uses 61% and 55% of the appropriate regional baselines.

Prepared historical data preserve attribution and provenance records. Upstream data licensing, actual site engineering, and an independent fresh-clone rerun remain separate checks. **This README does not claim that the live GitHub branch has been independently validated or assigned a Zenodo DOI.**
