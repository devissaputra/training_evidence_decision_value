# Paper Blueprint

## Working title
Decision Value of Training Evidence: Reanalysis of the National Supported Work Experiment

## Motivation
A statistically positive training effect does not automatically answer whether the effect is large enough to justify implementation. Reanalyzing a randomized training experiment across explicit minimum-gain thresholds makes the distinction between effect estimation and decision sufficiency visible.

## Research question
How does the decision interpretation of randomized training evidence change as the minimum economically meaningful earnings gain changes?

## Data and method
Compute the randomized treated-minus-control difference in 1978 earnings, a transparent large-sample normal interval, and a seeded 5,000-resample nonparametric bootstrap. For thresholds from $500 to $3,000, report the fraction of bootstrap resamples whose difference exceeds each threshold. Those fractions are resampling diagnostics, not posterior probabilities.

## Results to report
The observed randomized difference in 1978 earnings is $1,794.34. The seeded bootstrap 95% resampling interval is about $501–$3,097. The bootstrap exceedance fraction is 0.36 at a $2,000 threshold and falls to 0.035 at $3,000, illustrating the dependence of evidence interpretation on the decision threshold. Report the packaged headline metrics and the full relevant derived table; do not cherry-pick only the strongest contrast.

## Robustness / sensitivity
The release reports the raw randomized mean difference, a large-sample normal interval, a seeded 5,000-resample nonparametric bootstrap interval, and the full threshold-exceedance curve from $500 to $3,000. Agreement between the normal and bootstrap intervals is informative, while the threshold curve shows how the decision conclusion changes without re-fitting the treatment effect.

## Limitations
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.

## Publication integrity
Do not describe this repository as peer reviewed, preregistered, or externally validated unless those events actually occur. Distinguish analysis of public data from original data collection.
