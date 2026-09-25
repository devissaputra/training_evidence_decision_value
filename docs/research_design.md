# Research Design

## Research question
How does the decision interpretation of randomized training evidence change as the minimum economically meaningful earnings gain changes?

## Design
Secondary analysis of the randomized National Supported Work experimental sample.

## Source and unit of analysis
Source: National Supported Work Demonstration — Dehejia-Wahba experimental sample. The operational unit follows the public dataset and is documented in `data/source_manifest.json` and `docs/data_dictionary.md`.

## Hypotheses
1. H1: the randomized treated group has higher mean 1978 earnings than the randomized control group in this sample.
2. H2: uncertainty around the mean difference is material relative to plausible implementation thresholds.
3. H3: bootstrap exceedance fractions fall as the minimum-gain threshold rises, so statistical evidence and decision sufficiency are not the same question.

## Method
Compute the randomized treated-minus-control difference in 1978 earnings, a transparent large-sample normal interval, and a seeded 5,000-resample nonparametric bootstrap. For thresholds from $500 to $3,000, report the fraction of bootstrap resamples whose difference exceeds each threshold. Those fractions are resampling diagnostics, not posterior probabilities.

## Validity boundary
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.
