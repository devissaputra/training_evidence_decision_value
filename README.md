# Decision Value of Training Evidence: Reanalysis of the National Supported Work Experiment

[![CI](https://github.com/devissaputra/training_evidence_decision_value/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/training_evidence_decision_value/actions/workflows/ci.yml)
[![Empirical rebuild](https://github.com/devissaputra/training_evidence_decision_value/actions/workflows/empirical-rebuild.yml/badge.svg)](https://github.com/devissaputra/training_evidence_decision_value/actions/workflows/empirical-rebuild.yml)

> **Empirical Research Bundle** · **Learning & Development Research** · Training Evaluation / Decision Analysis / Experimental Evidence

Secondary reanalysis of the **Dehejia–Wahba RE74 subset** of the randomized National Supported Work experiment. The study asks how the interpretation of a fixed experimental earnings effect changes when a decision maker imposes increasingly demanding **illustrative minimum-benefit thresholds**.

![Empirical workflow](assets/architecture.svg)

## Research question

> How does the interpretation of randomized training evidence change as an illustrative minimum economically meaningful earnings gain becomes more demanding?

## Source and sample

The source page identifies this as a further subset of LaLonde's National Supported Work experimental sample containing RE74 information:

- **185 treated observations**
- **260 randomized controls**
- 10 columns in each row
- variables: treatment, age, education, Black, Hispanic, married, nodegree, RE74, RE75, RE78
- **RE78 is the outcome**

Published Dehejia–Wahba documentation describes RE78 as **real 1978 earnings expressed in 1982 U.S. dollars**.

This repository therefore does **not** treat the dollar values as current purchasing power or as modern corporate L&D benefit values.

## Pinned source files

| File | Rows | SHA-256 |
|---|---:|---|
| control | 260 | `a1364cea459d953dc691a667d99194b4ad335d6d550354fe23a5d2dc58d729b5` |
| treated | 185 | `e7b742fe0ff07a0f45e129b4ff108bb9611cd83d53604732c48a8a0a3e20eda3` |

The raw participant files are downloaded only during reproducibility runs and are **not redistributed** in this repository.

## Hypotheses

1. **H1:** the treated group has higher mean RE78 than the randomized control group in this experimental subset.
2. **H2:** uncertainty around the treated-minus-control difference is material relative to increasingly demanding minimum-benefit scenarios.
3. **H3:** bootstrap exceedance fractions decline monotonically as the illustrative threshold rises.

These hypotheses concern this historical experimental subset and the repository's decision-threshold operationalization. They do not establish modern corporate training ROI.

## Method

The analysis reports four layers:

1. **Observed experimental contrast:** treated minus control mean RE78.
2. **Large-sample uncertainty:** Welch standard error and a 95% normal interval.
3. **Resampling uncertainty:** seeded 5,000-resample nonparametric bootstrap and percentile interval.
4. **Experimental-design robustness diagnostic:** seeded 10,000 treatment-label permutations under exchangeability.

The permutation result is a robustness diagnostic. It is **not** presented as exact reconstruction of the original NSW randomization procedure.

![Method](assets/method.svg)

## Main empirical results

| Metric | Result |
|---|---:|
| Control mean RE78 | 4,554.80 |
| Treated mean RE78 | 6,349.14 |
| Treated − control | **1,794.34** |
| Welch standard error | 671.00 |
| Large-sample 95% interval | 479.19 to 3,109.50 |
| Bootstrap 95% percentile interval | 519.04 to 3,117.80 |
| Bootstrap fraction above zero | 0.9978 |
| Bootstrap fraction above 2,000 | 0.3818 |
| Two-sided label-permutation diagnostic p | 0.005899 |

All monetary values in the table are **historical 1982 U.S. dollars** as defined in the source literature.

## Dense decision-threshold frontier

The released frontier spans **0 to 4,000 in 100-dollar increments**. For every threshold it reports:

- the observed point-estimate headroom: effect minus threshold;
- the fraction of bootstrap resamples whose treatment difference exceeds that threshold.

Selected diagnostics:

- bootstrap exceedance remains at least **0.95** through a threshold of **700**
- at least **0.80** through **1,200**
- at least **0.50** through **1,700**
- at least **0.20** through **2,300**
- at least **0.05** through **2,900**

These are **resampling frontier diagnostics**, not posterior probabilities of implementation success.

![Decision frontier](assets/research_design.svg)

## Why the thresholds are illustrative

The repository does **not** contain:

- observed NSW program delivery cost per participant;
- a corporate L&D implementation budget;
- a validated modern break-even rule;
- an inflation-adjusted conversion to current dollars;
- a utility function converting earnings into organizational value.

Therefore the threshold grid is a sensitivity device: it asks, *“How much of the resampled treatment-effect distribution clears a hypothetical minimum gain?”* It does not claim that 500, 2,000, or any other threshold is an economically correct adoption rule.

## What the study can claim

The historical randomized comparison supports a causal treatment contrast for this experimental setting, subject to the original study design and this reduced RE74-available subset. The repository can also show how that estimated effect looks under alternative illustrative minimum-benefit thresholds.

## What the study cannot claim

The repository does not establish that the same effect would occur in contemporary corporate L&D, another population, another labor market, or current dollars. The threshold curve does not estimate ROI, expected profit, implementation probability, or a Bayesian posterior probability.

![Evidence boundary](assets/evaluation.svg)

## Reproduce

Offline verification:

```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
```

Verify pinned source files and recompute:

```bash
python scripts/fetch_and_analyze.py
```

Regenerate the full released evidence:

```bash
python scripts/fetch_and_analyze.py --write
```

The empirical rebuild workflow downloads both pinned source files, regenerates all derived tables and figures, runs the tests, and passes only when the working tree has **zero evidence diff**.

## Evidence files

- `data/derived/primary_results.csv` — complete 41-point threshold frontier
- `data/derived/secondary_results.csv` — core estimates and uncertainty metrics
- `data/derived/robustness_results.csv` — resampling configuration and frontier-crossing diagnostics
- `results/empirical_summary.json` — machine-readable release summary
- `data/source_manifest.json` — source definitions, row counts, treatment flags, and SHA-256 fingerprints
- `scripts/fetch_and_analyze.py` — complete source-to-output pipeline
- `research/model.py` — reusable statistical functions and release validation
- `tests/` — numerical, provenance, reproducibility, and consistency tests

## Licensing and attribution

Repository code and original documentation are MIT licensed. The NBER-hosted data page states that the data are distributed for **attributable non-commercial use (CC BY-NC)**. See [THIRD_PARTY_DATA.md](THIRD_PARTY_DATA.md).

## Research integrity

This is a secondary reanalysis of historical public experimental data. It is **not preregistered, peer reviewed as a new study, a modern ROI study, or a replication of the original assignment mechanism**. The repository separates source evidence, statistical uncertainty, resampling diagnostics, threshold scenarios, and interpretation.
