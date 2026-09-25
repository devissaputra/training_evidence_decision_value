# Paper Blueprint

## Working title
Decision Thresholds for Training Evidence: A Reanalysis of the National Supported Work Experimental Benchmark

## Motivation
Training evaluation often stops at asking whether an estimated effect is positive. Organizational decisions require an additional question: *how large would the effect need to be before the evidence remains compelling under a chosen minimum-benefit rule?*

This repository separates effect estimation from that threshold-sensitivity question.

## Data
Dehejia–Wahba RE74 subset of the National Supported Work experiment:
- 185 treated
- 260 randomized controls
- RE78 outcome in historical 1982 U.S. dollars

## Methods
- unadjusted randomized treated-minus-control difference;
- Welch standard error;
- large-sample normal interval;
- seeded percentile bootstrap;
- seeded treatment-label permutation diagnostic;
- 41-point threshold frontier from 0 to 4,000.

## Results
- effect: **1,794.34**
- Welch SE: **671.00**
- normal 95% interval: **479.19–3,109.50**
- bootstrap 95% interval: **519.04–3,117.80**
- bootstrap positive fraction: **0.9978**
- permutation diagnostic p: **0.005899**
- 50% exceedance frontier: **1,700**
- 20% exceedance frontier: **2,300**
- 5% exceedance frontier: **2,900**

All monetary values are historical 1982 U.S. dollars unless otherwise stated.

## Contribution
The contribution is not a new causal estimator. It is a transparent decision-threshold layer built on a well-known experimental benchmark, with explicit separation between:
1. estimated treatment effect;
2. uncertainty;
3. hypothetical minimum-benefit scenarios;
4. external-validity and economic-calibration limits.

## Limitations
No modern cost data or current-dollar conversion is introduced. The Dehejia–Wahba sample is a reduced historical experimental subset. The permutation analysis is a label-exchangeability diagnostic, not exact reconstruction of the original assignment mechanism.

## Publication integrity
Do not describe this repository as preregistered, peer reviewed as a new study, a modern corporate ROI study, or a validated adoption model.
