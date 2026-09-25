# Research Design

## Question
How does decision interpretation change as the required minimum earnings gain rises?

## Design
Secondary analysis of a historical randomized training-program benchmark.

## Sample
The analysis uses the Dehejia–Wahba RE74 subset of the NSW experiment: 185 treated and 260 randomized controls.

## Outcome
RE78, documented in the source literature as real 1978 earnings in 1982 U.S. dollars.

## Estimand
Unadjusted average difference in RE78 between randomized treated and control observations in the subset.

## Uncertainty
- Welch standard error;
- large-sample normal interval;
- within-group nonparametric bootstrap;
- treatment-label permutation robustness diagnostic.

## Decision layer
A dense grid of hypothetical minimum-benefit thresholds is applied after estimating the effect. The observed estimate is not re-fitted for each threshold.

The bootstrap exceedance curve summarizes how often resampled differences clear each threshold. It is a frequentist resampling diagnostic and not a posterior probability.

## Validity boundary
Randomization supports the historical experimental comparison, but the subset, period, intervention, labor market, monetary units, and implementation economics differ from modern corporate L&D. Generalization requires separate evidence.
