# Analysis Plan

## Status
This file documents the analysis released in this repository. It is **not a preregistration** and should not be described as one.

## Primary estimand / descriptive target
How does the decision interpretation of randomized training evidence change as the minimum economically meaningful earnings gain changes?

## Analysis
Compute the randomized treated-minus-control difference in 1978 earnings, a transparent large-sample normal interval, and a seeded 5,000-resample nonparametric bootstrap. For thresholds from $500 to $3,000, report the fraction of bootstrap resamples whose difference exceeds each threshold. Those fractions are resampling diagnostics, not posterior probabilities.

## Specified outputs for this release
1. source/sample size and provenance;
2. primary derived metric(s);
3. comparator, cross-group, cross-time, or frontier contrast where applicable;
4. uncertainty, sensitivity, or error information supported by the source;
5. explicit construct and external-validity limitations.

## Missingness / exclusions

All 185 randomized treated observations and 260 randomized controls in the Dehejia-Wahba NSW experimental sample are included. The outcome is 1978 earnings. No covariate adjustment or missing-value imputation is introduced in this reanalysis.

## Interpretation boundary
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.
