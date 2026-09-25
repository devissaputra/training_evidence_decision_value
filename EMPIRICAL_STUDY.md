# Empirical Study Protocol

## Study
Decision Value of Training Evidence: Reanalysis of the National Supported Work Experiment

## Research question
How does the decision interpretation of randomized training evidence change as the minimum economically meaningful earnings gain changes?

## Design and source
Secondary analysis of the randomized National Supported Work experimental sample. Source: National Supported Work Demonstration — Dehejia-Wahba experimental sample. Analysis/retrieval date: 2026-09-25.

## Hypotheses
1. H1: the randomized treated group has higher mean 1978 earnings than the randomized control group in this sample.
2. H2: uncertainty around the mean difference is material relative to plausible implementation thresholds.
3. H3: bootstrap exceedance fractions fall as the minimum-gain threshold rises, so statistical evidence and decision sufficiency are not the same question.

## Operationalization and method
Compute the randomized treated-minus-control difference in 1978 earnings, a transparent large-sample normal interval, and a seeded 5,000-resample nonparametric bootstrap. For thresholds from $500 to $3,000, report the fraction of bootstrap resamples whose difference exceeds each threshold. Those fractions are resampling diagnostics, not posterior probabilities.

## Primary empirical result
The observed randomized difference in 1978 earnings is $1,794.34. The seeded bootstrap 95% resampling interval is about $501–$3,097. The bootstrap exceedance fraction is 0.36 at a $2,000 threshold and falls to 0.035 at $3,000, illustrating the dependence of evidence interpretation on the decision threshold.

## Validity and claim boundary
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.

## Reproducibility status
The repository packages derived results, study-specific analysis functions, deterministic or seeded procedures where relevant, an internet-enabled source rebuild script, and tests for both computations and critical scientific invariants. The released analysis was documented after dataset selection and should not be represented as preregistered.
