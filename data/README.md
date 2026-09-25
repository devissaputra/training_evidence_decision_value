# Data

## Source
National Supported Work Demonstration — Dehejia–Wahba RE74 experimental subset.

Source page:
https://users.nber.org/~rdehejia/nswdata2.html

The source page documents:
- 260 controls;
- 185 treated observations;
- 10 variables per row;
- RE78 as the outcome.

## Pinned files
Exact source URLs, row counts, column counts, treatment indicators, and SHA-256 fingerprints are in `source_manifest.json`.

## Raw data
Raw participant-level data are not redistributed in this repository.

## Derived evidence
- `derived/primary_results.csv`: 41-point threshold frontier;
- `derived/secondary_results.csv`: core treatment-effect and uncertainty metrics;
- `derived/robustness_results.csv`: resampling configuration and frontier diagnostics.

## Monetary unit
RE78 and the threshold grid are treated as **historical 1982 U.S. dollars** according to the published source documentation. No modern-dollar conversion is performed.

## Licensing
The source page states attributable non-commercial use (CC BY-NC). See `../THIRD_PARTY_DATA.md`.

## Construct boundary
This is an experimental-evidence threshold-sensitivity study, not an ROI calculator or modern corporate training cost-benefit analysis.
