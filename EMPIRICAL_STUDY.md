# Empirical Study Protocol

## Study
Decision Value of Training Evidence: Reanalysis of the National Supported Work Experiment

## Research question
How does the interpretation of randomized training evidence change as an illustrative minimum earnings-gain threshold becomes more demanding?

## Design
Secondary reanalysis of the **Dehejia–Wahba RE74 subset** of the randomized National Supported Work experimental sample.

The source page identifies 185 treated observations and 260 randomized controls. This is a reduced subset of the larger LaLonde experimental sample, selected because RE74 information is available.

## Outcome
RE78 is the outcome. Published Dehejia–Wahba documentation describes it as real 1978 earnings measured in **1982 U.S. dollars**.

No claim is made that these dollar values are current dollars or directly comparable with contemporary corporate training budgets.

## Hypotheses
1. H1: treated participants have higher mean RE78 than randomized controls in this subset.
2. H2: uncertainty around the mean difference is material relative to increasingly demanding illustrative thresholds.
3. H3: the bootstrap exceedance fraction declines monotonically as the threshold rises.

## Primary estimate
The observed treated-minus-control RE78 difference is **1,794.34** historical 1982 U.S. dollars.

## Uncertainty
- Welch standard error: **671.00**
- large-sample normal 95% interval: **479.19 to 3,109.50**
- seeded bootstrap percentile 95% interval: **519.04 to 3,117.80**
- bootstrap fraction above zero: **0.9978**
- seeded two-sided treatment-label permutation diagnostic: **p = 0.005899**

The permutation statistic is a robustness diagnostic under label exchangeability and is not claimed to recreate the exact original NSW assignment mechanism.

## Decision-threshold analysis
A dense grid from 0 to 4,000 in increments of 100 is evaluated. Each row reports:
- threshold;
- point-estimate headroom;
- bootstrap exceedance fraction.

Frontier diagnostics:
- ≥0.95 through 700
- ≥0.80 through 1,200
- ≥0.50 through 1,700
- ≥0.20 through 2,300
- ≥0.05 through 2,900

These values are resampling diagnostics for hypothetical historical-dollar thresholds. They are not posterior probabilities, program-adoption probabilities, or validated economic decision rules.

## Validity boundary
The randomized design supports a causal experimental contrast for the historical setting, but external validity remains limited. The Dehejia–Wahba subset is not the entire NSW experimental sample. Transport to modern L&D requires separate evidence on population, intervention, labor market, implementation cost, and current-dollar valuation.

## Reproducibility
Both source files are pinned by SHA-256, row count, column count, and expected treatment indicator. The full frontier, core-estimate table, robustness table, JSON summary, figures, tests, multi-version CI, and strict online zero-diff rebuild are synchronized.

The released analysis was documented after dataset selection and must not be represented as preregistered.
