# Digital Gardens of North Tyne Valley — V39 computational research release

Energy & Environmental Science (Royal Society of Chemistry), Analysis article; 10 November 2026.

This is the **separate research release**, not part of the journal submission. All modelled operating results are scenario estimates, not measured operator performance. The article and supplementary information were editorially corrected separately; `build_manuscript.py` is a historical helper, not a reproducible generator of the final author-edited Word documents.

## Directory structure

- `DATA/`: prepared historical ERA5 records (2010–2025), GB grid and market data, communities and provenance records.
- `OUTPUT/`: expected numerical JSON/CSV/NPZ output, including the corrected `REVISED_SENSITIVITY.json` and the symmetrical accounting screens.
- Root `*.py` scripts: computational pipeline, sensitivity screens and local validation.
- `SHA256_MANIFEST.csv`: SHA-256 digests of every distributed research-release file other than the manifest itself.
- `verify_manifest.py`: standard-library checksum verifier, run after obtaining/extracting this release.

## Python and clean-directory reproduction

Requires Python 3.11+ and `numpy`, `pandas`, `scipy`, `matplotlib`; run commands from the **repository root**. To verify the delivered archive *before* recomputation:

```bash
python verify_manifest.py
```

To regenerate the outputs from the prepared input data, run in this order. The first two model searches can be the slowest steps; allow them to finish before the dependent scripts.

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

The `revised_sensitivities.py` step is required: it regenerates `OUTPUT/REVISED_SENSITIVITY.json` **and** `.csv` after the updated community ledger. The constant-baseline 25-year gross avoidance is approximately 2,727 kt, not the obsolete 2,800.8 kt. The directional 10%- and 2%-annual-decline sensitivities give approximately 1.01 and 2.16 Mt, respectively. Other optional analyses may depend on measurement inputs not distributed here. `figures.py` regenerates exploratory figures for the historical helper, **not** the curated article figures.

`validate.py` executes 149 internal checks. The regional screen performs seven checks and the symmetrical carbon screen performs five. All 161 checks passed on the **local archive** on 10 November 2026. Re-running scripts can change file timestamps or formats; regenerate the SHA-256 inventory for a newly issued release after finalising the outputs.

## Carbon, heat and attribution boundaries

All electricity use associated with community household heat pumps and EV charging is attributed the historical *location-based* grid factor. Contractual procurement factors are reported separately and not treated as physical community-grid displacement. The conditional gross annual community ledger gives 109.1 kt CO2e (full delivery), 95.2 kt (no seaweed approval), 47.6 kt (half uptake) and 56.7 kt (tier-weighted uptake), all before incremental vehicle manufacturing.

Campus recoverable heat is a technical estimate, not measured waste or proven useful heat offtake. The illustrative TNUoS flat proxy is not a verified site tariff; the `REVISED_SENSITIVITY` fixed-charge figures vary Digital Gardens alone and **must not** be interpreted as a fair twin comparison. Regional scaling must use North East-wide baselines (61% of activities addressed; 55% of resident-plus-cattle baseline), not catchment denominators.

## PUBLICATION AND DOI RELEASE GATE — NOT YET CLEARED

Public GitHub repository: https://github.com/bcjohnjr/UK---Digital-Gardens-versus-Mega-Data-Centres

The live public repository was checked on 10 November 2026 and still uses an older flat root layout, with files missing from this V39 hierarchy. The public version is therefore **not** asserted to reproduce the numerical analyses from a fresh clone. Do not use 'published and reproducible from a clean clone' or claim a UK-specific Zenodo DOI until the repository is updated and independently checked. The archive supplied in the V39 package is the candidate upload source.

Recommended public release procedure:

1. Back up the public repository and put the V39 release on a separate branch or update it with a reviewed commit; do not overwrite newer work without checking conflicts.
2. Place the exact `DATA/`, `OUTPUT/`, source Python and README hierarchy from this release in the repository root; remove or reconcile duplicate legacy flat files.
3. Clone the public release into a clean working directory and run `python verify_manifest.py` before regenerating anything.
4. Run the complete regeneration sequence above. Compare the resulting outputs with the package using appropriate numerical/byte-for-byte checks (compressed/NumPy byte representations can vary by platform).
5. Archive the verified GitHub release in Zenodo and add its DOI to the final journal submission only after the DOI resolves.

Raw third-party data redistribution rights and original licence terms need independent verification before public deposit. The author is responsible for confirming repository status, patent/COI disclosure and any separately submitted Joule manuscript's editorial status.
