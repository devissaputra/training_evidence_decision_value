# Research Bundle Definition

This repository qualifies as an empirical L&D Research Bundle because it links a specific decision question to a historical randomized benchmark, pinned public source files, complete derived evidence, multiple uncertainty views, robustness diagnostics, executable regeneration, tests, CI, and explicit claim boundaries.

## Empirical core
- 185 treated observations;
- 260 randomized controls;
- historical RE78 outcome;
- observed treated-minus-control difference of 1,794.34;
- 41-point threshold frontier;
- bootstrap and treatment-label permutation diagnostics.

## Reproducibility
- both sources pinned by SHA-256;
- source rows and treatment indicators validated;
- complete source-to-output script;
- Python 3.10/3.11/3.12 CI;
- read-only online empirical rebuild;
- zero-diff release verification.

## Decision contribution
The bundle explicitly separates:
1. causal experimental contrast in the historical subset;
2. sampling/resampling uncertainty;
3. threshold-sensitivity scenarios;
4. economic and external-validity limitations.

## Release criterion
PASS requires:
- exact source fingerprints;
- correct historical-dollar labeling;
- explicit RE74-subset description;
- full 41-point frontier;
- core estimate table;
- robustness table;
- permutation diagnostic;
- no posterior-probability language;
- no claim that thresholds are observed costs or validated corporate break-even values;
- synchronized tests, figures, JSON, CSVs, and documentation.
