# Data Dictionary

## Provenance
See `data/source_manifest.json`. Raw source observations are not silently republished.

## `data/derived/primary_results.csv`
Complete six-threshold bootstrap exceedance curve used in the reported decision analysis.

## `data/derived/secondary_results.csv`
When present and non-empty, this contains a second derived table needed to reproduce a reported comparison. If empty, no second packaged table is required.

## `results/empirical_summary.json`
Machine-readable headline sample sizes, estimates, and the release finding. Values must agree with README text and the derived CSVs.

## Construct boundary
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.
