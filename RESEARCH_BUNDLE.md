# Research Bundle Definition

This repository is treated as a research bundle because it links one explicit research question to a named empirical source, a documented operationalization, executable analysis code, derived evidence, reproducibility checks, visual evidence, validity boundaries, and a paper-ready interpretation path.

## Question
How does the decision interpretation of randomized training evidence change as the minimum economically meaningful earnings gain changes?

## Empirical core
Randomized mean contrast, uncertainty interval, and threshold exceedance analysis.

## Main result
The observed randomized difference in 1978 earnings is $1,794.34. The seeded bootstrap 95% resampling interval is about $501–$3,097. The bootstrap exceedance fraction is 0.36 at a $2,000 threshold and falls to 0.035 at $3,000, illustrating the dependence of evidence interpretation on the decision threshold.

## Boundary
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.

## Release criterion
A release passes only if source provenance, code, derived tables, JSON summary, README claims, figures, and tests agree numerically and semantically.
