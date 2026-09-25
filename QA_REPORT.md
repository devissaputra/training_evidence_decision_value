# Final QA Report

**Release status: PASS after correction.**

## Checks completed
- provenance and source identity reviewed;
- licensing/reuse note recorded;
- derived CSV structure checked against the stated sample and estimand;
- `results/empirical_summary.json` reconciled with packaged evidence;
- README/report language reconciled with the numerical results;
- study-specific methods moved into `research/model.py`;
- tests exercise scientific logic and invariants;
- internet rebuild script has no synthetic fallback;
- four SVG assets regenerated as study-specific figures and XML-validated;
- local Markdown links checked;
- citation metadata points to the final repository slug;
- no preregistration claim is made.

## Final empirical finding
The observed randomized difference in 1978 earnings is $1,794.34. The seeded bootstrap 95% resampling interval is about $501–$3,097. The bootstrap exceedance fraction is 0.36 at a $2,000 threshold and falls to 0.035 at $3,000, illustrating the dependence of evidence interpretation on the decision threshold.

## Required interpretation boundary
This is a historical job-training experiment in a specific population and period. Randomization supports a causal effect for that experimental setting, but transport to modern corporate L&D requires separate justification. Bootstrap exceedance fractions are not Bayesian posterior probabilities.
