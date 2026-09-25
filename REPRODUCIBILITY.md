# Reproducibility

## Offline validation

```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
```

The offline suite checks:
- statistical helper functions;
- deterministic bootstrap and permutation procedures;
- exact 260/185 sample sizes;
- 10-column source schema;
- pinned SHA-256 fingerprints;
- released means and treatment effect;
- complete 41-point frontier;
- monotonic exceedance behavior;
- point-estimate headroom;
- summary/core-table agreement;
- robustness configuration;
- full bundle validation.

## Pinned source files

| Source | Rows | SHA-256 |
|---|---:|---|
| control | 260 | `a1364cea459d953dc691a667d99194b4ad335d6d550354fe23a5d2dc58d729b5` |
| treated | 185 | `e7b742fe0ff07a0f45e129b4ff108bb9611cd83d53604732c48a8a0a3e20eda3` |

## Verify live published bytes

```bash
python scripts/fetch_and_analyze.py
```

This fails if either source fingerprint or row count changes.

## Regenerate the release

```bash
python scripts/fetch_and_analyze.py --write
```

This regenerates:
- `data/derived/primary_results.csv`
- `data/derived/secondary_results.csv`
- `data/derived/robustness_results.csv`
- `results/empirical_summary.json`
- all four SVG figures

## GitHub Actions

`.github/workflows/ci.yml` tests Python 3.10, 3.11, and 3.12.

`.github/workflows/empirical-rebuild.yml` downloads the pinned NBER-hosted files, regenerates the full evidence package, runs tests, and requires zero diff. It has read-only repository permissions and cannot silently update source fingerprints.

## Intentional source updates

`--refresh-fingerprints` exists only for an intentional versioned source refresh. It should not be used in normal CI.
