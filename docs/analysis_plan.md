# Analysis Plan

## Status
This document describes the released analysis. It is **not a preregistration**.

## Research question
How does the interpretation of randomized training evidence change across increasingly demanding illustrative minimum earnings-gain thresholds?

## Sample
Dehejia–Wahba RE74 subset:
- 185 treated
- 260 randomized controls

## Outcome
RE78: real 1978 earnings, expressed in 1982 U.S. dollars in the published source documentation.

## Primary estimate
Unadjusted treated-minus-control difference in mean RE78.

## Uncertainty analyses
1. Welch standard error.
2. Large-sample 95% normal interval using 1.96 × SE.
3. Seeded 5,000-resample within-group nonparametric bootstrap.
4. Seeded 10,000 treatment-label permutation diagnostic.

The permutation diagnostic assumes label exchangeability within this subset and is not described as exact randomization inference for the original NSW assignment process.

## Threshold frontier
Evaluate hypothetical thresholds from 0 through 4,000 in 100-dollar increments.

For each threshold report:
- point-estimate headroom = observed effect − threshold;
- bootstrap exceedance fraction.

## Diagnostic frontier summaries
Record the largest grid threshold at which the exceedance fraction remains at least:
- 0.95
- 0.80
- 0.50
- 0.20
- 0.05

## Interpretation rule
Thresholds are illustrative sensitivity scenarios in historical 1982 U.S. dollars. They are not observed costs, current-dollar equivalents, modern corporate L&D break-even values, or empirically validated utility thresholds.

## Missingness and exclusions
The source files are used as published. Each row must have exactly 10 fields and the expected treatment indicator. No observations are imputed or covariate-adjusted.

## External validity
The RE74-available subset is not the entire LaLonde NSW experiment. Modern L&D application requires independent justification for population, intervention, setting, cost, and monetary conversion.
