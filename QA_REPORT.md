# Final QA Report

**Release status: PASS.**

## Source verification
- source page verified as the NBER-hosted Dehejia–Wahba NSW data page;
- sample correctly identified as the **RE74-available subset**, not the entire LaLonde NSW experiment;
- 260 randomized controls verified;
- 185 treated observations verified;
- 10 fields per source row verified;
- treatment indicators validated for every row;
- RE78 used as the outcome;
- historical earnings unit documented as **1982 U.S. dollars** from the published source literature.

## Pinned provenance
- control SHA-256: `a1364cea459d953dc691a667d99194b4ad335d6d550354fe23a5d2dc58d729b5`;
- treated SHA-256: `e7b742fe0ff07a0f45e129b4ff108bb9611cd83d53604732c48a8a0a3e20eda3`;
- source hashes, row counts, column counts, URLs, and treatment flags are stored in `data/source_manifest.json`;
- raw participant records are not redistributed.

## Corrected empirical release
- control mean RE78: **4,554.80**;
- treated mean RE78: **6,349.14**;
- treated-minus-control difference: **1,794.34**;
- Welch standard error: **671.00**;
- large-sample normal 95% interval: **479.19 to 3,109.50**;
- seeded bootstrap percentile 95% interval: **519.04 to 3,117.80**;
- bootstrap positive fraction: **0.9978**;
- bootstrap exceedance above 2,000: **0.3818**;
- two-sided treatment-label permutation diagnostic: **p = 0.005899**.

All monetary values are interpreted as historical 1982 U.S. dollars, not current dollars.

## Decision-threshold correction
The earlier six-point curve was replaced with a complete **41-point frontier from 0 to 4,000 in increments of 100**.

Every row now reports:
- illustrative minimum-gain threshold;
- observed point-estimate headroom;
- bootstrap exceedance fraction.

Released frontier diagnostics:
- exceedance ≥ 0.95 through **700**;
- exceedance ≥ 0.80 through **1,200**;
- exceedance ≥ 0.50 through **1,700**;
- exceedance ≥ 0.20 through **2,300**;
- exceedance ≥ 0.05 through **2,900**.

These are resampling diagnostics. They are not posterior probabilities, adoption probabilities, or validated economic break-even thresholds.

## Economic-interpretation correction
The repository no longer presents 500–3,000 dollar values as empirically established “economically meaningful” thresholds.

The released documentation explicitly states that:
- no NSW program cost per participant is estimated here;
- no current-dollar conversion is performed;
- no modern corporate L&D implementation cost is available;
- no validated ROI or utility threshold is claimed;
- the threshold grid is an illustrative sensitivity device.

## Robustness
- 5,000 seeded within-group nonparametric bootstrap resamples;
- explicit linear-interpolation percentile definition;
- 10,000 seeded treatment-label permutations;
- permutation result described as an exchangeability diagnostic, not exact reconstruction of the original assignment mechanism;
- point estimate, large-sample interval, bootstrap interval, and permutation diagnostic all packaged separately.

## Evidence completeness
- `primary_results.csv`: complete 41-point decision frontier;
- `secondary_results.csv`: core sample, effect, interval, bootstrap, and permutation results;
- `robustness_results.csv`: seeds, resample counts, and frontier crossing diagnostics;
- `empirical_summary.json`: synchronized machine-readable release;
- all four SVG figures regenerated directly from the released pipeline.

## Software and reproducibility QA
- analysis functions consolidated in `research/model.py`;
- exact source hashes and headline metrics are release invariants;
- tests cover statistics, deterministic resampling, source provenance, sample/effect values, complete frontier structure, monotonicity, headroom reconciliation, summary/table consistency, robustness configuration, and full bundle validation;
- CI passes Python **3.10, 3.11, and 3.12**;
- strict empirical rebuild downloads the pinned sources, regenerates every evidence artifact, runs tests, and requires **zero git diff**;
- strict empirical rebuild completed successfully.

## Licensing
- complete MIT text restored for repository code and original documentation;
- GitHub recognizes the repository license as **MIT**;
- `THIRD_PARTY_DATA.md` separates the repository license from the NBER-hosted data conditions;
- the source page's attributable non-commercial use requirement (CC BY-NC as stated there) is documented.

## Claim boundary
The historical randomized comparison supports a causal treated-control contrast for this experimental setting and reduced RE74-available subset, subject to the original study design. The repository does not claim transport to modern corporate L&D, current-dollar ROI, implementation profitability, or Bayesian probability of success.

## GitHub metadata
Recommended About text and final Topics are stored in `GITHUB_METADATA.md`. The live GitHub About and Topics remain UI metadata because the connected GitHub interface used for this repair does not expose repository-description/topic mutation.
