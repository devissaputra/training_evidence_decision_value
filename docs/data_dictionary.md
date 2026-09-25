# Data Dictionary

## Source schema
Each published source row contains 10 fields:
1. treatment
2. age
3. education
4. Black
5. Hispanic
6. married
7. nodegree
8. RE74
9. RE75
10. RE78

RE78 is the outcome used in this repository.

## `data/derived/primary_results.csv`
Complete 41-point decision-threshold frontier.

Columns:
- `minimum_gain_threshold_1982_usd`: illustrative threshold from 0 to 4,000;
- `point_estimate_headroom_1982_usd`: observed 1,794.34 effect minus threshold;
- `bootstrap_exceedance_fraction`: fraction of 5,000 bootstrap treatment-effect resamples above the threshold.

## `data/derived/secondary_results.csv`
Core experimental and uncertainty results:
- sample sizes;
- control and treated means;
- mean difference;
- Welch standard error;
- large-sample normal interval;
- bootstrap percentile interval;
- bootstrap exceedance diagnostics;
- permutation diagnostic p-value.

## `data/derived/robustness_results.csv`
Reproducibility configuration and threshold-frontier summary:
- bootstrap resample count and seed;
- permutation resample count and seed;
- maximum thresholds retaining exceedance fractions of at least 0.95, 0.80, 0.50, 0.20, and 0.05.

## `results/empirical_summary.json`
Machine-readable release summary containing source/sample definition, historical-dollar outcome definition, headline results, decision-frontier diagnostics, and interpretation boundaries.

## Construct boundary
The threshold frontier is a sensitivity analysis over hypothetical minimum benefits. It is not a cost-benefit study, ROI model, posterior decision probability, or current-dollar valuation.
