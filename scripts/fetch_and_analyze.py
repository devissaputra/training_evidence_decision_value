#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.model import (
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    EXPECTED_COLUMNS,
    PERMUTATION_RESAMPLES,
    PERMUTATION_SEED,
    bootstrap_differences,
    exceedance_fraction,
    large_sample_normal_interval,
    mean,
    mean_difference,
    permutation_differences,
    quantile_linear,
    two_sided_permutation_pvalue,
    welch_standard_error,
)

MANIFEST_PATH = ROOT / "data/source_manifest.json"
PRIMARY_PATH = ROOT / "data/derived/primary_results.csv"
SECONDARY_PATH = ROOT / "data/derived/secondary_results.csv"
ROBUSTNESS_PATH = ROOT / "data/derived/robustness_results.csv"
SUMMARY_PATH = ROOT / "results/empirical_summary.json"

SOURCE_CONFIG = {
    "control": {
        "url": "https://users.nber.org/~rdehejia/data/nswre74_control.txt",
        "expected_rows": 260,
        "expected_treatment": 0,
    },
    "treated": {
        "url": "https://users.nber.org/~rdehejia/data/nswre74_treated.txt",
        "expected_rows": 185,
        "expected_treatment": 1,
    },
}


def download(url):
    last_error = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "training-evidence-decision-value/2.0"},
            )
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def parse_source(payload, key, expected_treatment):
    rows = []
    for line_number, line in enumerate(payload.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != EXPECTED_COLUMNS:
            raise RuntimeError(
                f"{key}: line {line_number} has {len(fields)} columns; expected {EXPECTED_COLUMNS}"
            )
        values = [float(value) for value in fields]
        if values[0] != expected_treatment:
            raise RuntimeError(
                f"{key}: line {line_number} treatment={values[0]}; expected {expected_treatment}"
            )
        rows.append(values)
    return rows


def fetch_sources(manifest, refresh_fingerprints=False):
    source_files = manifest.setdefault("source_files", {})
    sources = {}
    for key, config in SOURCE_CONFIG.items():
        payload = download(config["url"])
        digest = hashlib.sha256(payload).hexdigest()
        rows = parse_source(payload, key, config["expected_treatment"])
        if len(rows) != config["expected_rows"]:
            raise RuntimeError(
                f"{key}: expected {config['expected_rows']} rows, got {len(rows)}"
            )

        previous = source_files.get(key, {})
        if not refresh_fingerprints:
            if not previous.get("sha256"):
                raise RuntimeError(
                    f"{key}: no pinned SHA-256. Use --refresh-fingerprints only for an intentional source release."
                )
            if previous["sha256"] != digest:
                raise RuntimeError(
                    f"{key}: fingerprint changed; expected {previous['sha256']}, got {digest}"
                )
            if int(previous.get("rows", -1)) != len(rows):
                raise RuntimeError(
                    f"{key}: row count changed; expected {previous.get('rows')}, got {len(rows)}"
                )

        source_files[key] = {
            "url": config["url"],
            "rows": len(rows),
            "columns": EXPECTED_COLUMNS,
            "sha256": digest,
            "treatment_indicator": config["expected_treatment"],
        }
        sources[key] = rows
    return sources


def frontier_crossing(frontier, level):
    eligible = [
        row["minimum_gain_threshold_1982_usd"]
        for row in frontier
        if row["bootstrap_exceedance_fraction"] >= level
    ]
    return max(eligible) if eligible else 0


def analyze(sources):
    control = [row[9] for row in sources["control"]]
    treated = [row[9] for row in sources["treated"]]

    observed = mean_difference(treated, control)
    se = welch_standard_error(treated, control)
    normal_low, normal_high = large_sample_normal_interval(treated, control)

    bootstrap = sorted(
        bootstrap_differences(treated, control, BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED)
    )
    bootstrap_low = quantile_linear(bootstrap, 0.025)
    bootstrap_high = quantile_linear(bootstrap, 0.975)

    permutation = permutation_differences(
        treated, control, PERMUTATION_RESAMPLES, PERMUTATION_SEED
    )
    permutation_p = two_sided_permutation_pvalue(observed, permutation)

    frontier = []
    for threshold in range(0, 4001, 100):
        frontier.append(
            {
                "minimum_gain_threshold_1982_usd": threshold,
                "point_estimate_headroom_1982_usd": round(observed - threshold, 2),
                "bootstrap_exceedance_fraction": round(
                    exceedance_fraction(bootstrap, threshold), 4
                ),
            }
        )

    decision_levels = {
        "0_95": frontier_crossing(frontier, 0.95),
        "0_80": frontier_crossing(frontier, 0.80),
        "0_50": frontier_crossing(frontier, 0.50),
        "0_20": frontier_crossing(frontier, 0.20),
        "0_05": frontier_crossing(frontier, 0.05),
    }

    core = [
        ("n_control", len(control)),
        ("n_treated", len(treated)),
        ("control_mean_re78_1982_usd", round(mean(control), 2)),
        ("treated_mean_re78_1982_usd", round(mean(treated), 2)),
        ("difference_re78_1982_usd", round(observed, 2)),
        ("welch_standard_error_1982_usd", round(se, 2)),
        ("normal95_low_1982_usd", round(normal_low, 2)),
        ("normal95_high_1982_usd", round(normal_high, 2)),
        ("bootstrap95_low_1982_usd", round(bootstrap_low, 2)),
        ("bootstrap95_high_1982_usd", round(bootstrap_high, 2)),
        ("bootstrap_positive_fraction", round(exceedance_fraction(bootstrap, 0), 4)),
        ("bootstrap_exceedance_gt_2000", round(exceedance_fraction(bootstrap, 2000), 4)),
        ("permutation_two_sided_p", round(permutation_p, 6)),
    ]

    robustness = [
        ("bootstrap_resamples", BOOTSTRAP_RESAMPLES),
        ("bootstrap_seed", BOOTSTRAP_SEED),
        ("permutation_resamples", PERMUTATION_RESAMPLES),
        ("permutation_seed", PERMUTATION_SEED),
    ]
    for key, value in decision_levels.items():
        robustness.append(
            (f"max_threshold_with_bootstrap_exceedance_at_least_{key}", value)
        )

    summary = {
        "study": "Decision Value of Training Evidence: Reanalysis of the National Supported Work Experiment",
        "sample_definition": "Dehejia-Wahba RE74 subset of the National Supported Work experimental sample",
        "outcome_definition": "RE78: real earnings in 1978, expressed in 1982 U.S. dollars in the published source documentation",
        "headline_metrics": {
            "n_control": len(control),
            "n_treated": len(treated),
            "control_mean_re78_1982_usd": round(mean(control), 2),
            "treated_mean_re78_1982_usd": round(mean(treated), 2),
            "difference_re78_1982_usd": round(observed, 2),
            "welch_standard_error_1982_usd": round(se, 2),
            "normal95_low_1982_usd": round(normal_low, 2),
            "normal95_high_1982_usd": round(normal_high, 2),
            "bootstrap95_low_1982_usd": round(bootstrap_low, 2),
            "bootstrap95_high_1982_usd": round(bootstrap_high, 2),
            "bootstrap_positive_fraction": round(exceedance_fraction(bootstrap, 0), 4),
            "bootstrap_exceedance_gt_2000": round(exceedance_fraction(bootstrap, 2000), 4),
            "permutation_two_sided_p": round(permutation_p, 6),
        },
        "decision_frontier_diagnostics": decision_levels,
        "threshold_interpretation": (
            "Thresholds are illustrative minimum-benefit scenarios in historical 1982 U.S. dollars. "
            "They are not observed program costs, modern corporate L&D break-even values, or validated economic thresholds."
        ),
        "inference_boundary": (
            "The permutation result is a treatment-label exchangeability diagnostic for the experimental subset; "
            "it is not presented as exact randomization inference for the original NSW assignment mechanism."
        ),
        "finding": (
            f"The observed treated-minus-control difference in RE78 is {observed:,.2f} historical 1982 U.S. dollars. "
            f"The large-sample 95% interval is {normal_low:,.2f} to {normal_high:,.2f}, "
            f"and the seeded bootstrap percentile interval is {bootstrap_low:,.2f} to {bootstrap_high:,.2f}. "
            "The dense threshold frontier maps the fixed treatment-effect estimate to increasingly demanding "
            "illustrative minimum-benefit scenarios; bootstrap exceedance fractions are resampling diagnostics, not posterior probabilities."
        ),
        "source": "National Supported Work Demonstration — Dehejia-Wahba RE74 experimental subset",
        "retrieved": "2026-09-25",
    }
    return frontier, core, robustness, summary


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_figures(frontier, summary):
    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    metrics = summary["headline_metrics"]
    diagnostics = summary["decision_frontier_diagnostics"]

    architecture = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430">
<rect width="1200" height="430" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Training Evidence Decision Value</text>
<text x="50" y="88" font-family="Arial" font-size="16">Pinned experimental subset → effect estimate → uncertainty → threshold frontier → bounded interpretation</text>
<g font-family="Arial" text-anchor="middle">
<rect x="35" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="130" y="185" font-size="16" font-weight="700">Pinned NSW data</text><text x="130" y="215" font-size="14">185 treated + 260 control</text>
<rect x="270" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="365" y="185" font-size="16" font-weight="700">Effect estimate</text><text x="365" y="215" font-size="14">RE78 mean difference</text>
<rect x="505" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="600" y="185" font-size="16" font-weight="700">Uncertainty</text><text x="600" y="215" font-size="14">normal + bootstrap + permutation</text>
<rect x="740" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="835" y="185" font-size="16" font-weight="700">Frontier</text><text x="835" y="215" font-size="14">0–4,000 by 100</text>
<rect x="975" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="1070" y="185" font-size="16" font-weight="700">Interpret</text><text x="1070" y="215" font-size="14">illustrative thresholds only</text>
</g>
<g stroke="#222" stroke-width="2"><line x1="225" y1="212" x2="270" y2="212"/><line x1="460" y1="212" x2="505" y2="212"/><line x1="695" y1="212" x2="740" y2="212"/><line x1="930" y1="212" x2="975" y2="212"/></g>
</svg>"""

    method = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="550" viewBox="0 0 1200 550">
<rect width="1200" height="550" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Training Evidence Decision Value — Method</text>
<g font-family="Arial">
<text x="70" y="125" font-size="20" font-weight="700">1. Historical experimental benchmark</text>
<text x="90" y="155" font-size="16">Use the Dehejia–Wahba RE74 subset: 185 randomized treated observations and 260 randomized controls.</text>
<text x="70" y="215" font-size="20" font-weight="700">2. Estimate RE78 difference</text>
<text x="90" y="245" font-size="16">RE78 is real 1978 earnings measured in 1982 U.S. dollars in the source documentation.</text>
<text x="70" y="305" font-size="20" font-weight="700">3. Characterize uncertainty</text>
<text x="90" y="335" font-size="16">Welch standard error + large-sample normal interval + seeded percentile bootstrap + label-permutation diagnostic.</text>
<text x="70" y="395" font-size="20" font-weight="700">4. Map evidence to illustrative thresholds</text>
<text x="90" y="425" font-size="16">Generate a 0–4,000 frontier in 100-dollar increments; report point-estimate headroom and bootstrap exceedance.</text>
<text x="90" y="465" font-size="14">Thresholds are scenarios, not observed training costs or validated modern corporate L&amp;D break-even values.</text>
</g>
</svg>"""

    points = []
    for row in frontier:
        x = 100 + (row["minimum_gain_threshold_1982_usd"] / 4000) * 1000
        y = 100 + (1 - row["bootstrap_exceedance_fraction"]) * 300
        points.append(f"{x:.1f},{y:.1f}")
    research_design = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500">
<rect width="1200" height="500" fill="white"/>
<text x="50" y="50" font-family="Arial" font-size="29" font-weight="700">Bootstrap Threshold Frontier</text>
<text x="50" y="78" font-family="Arial" font-size="15">Illustrative minimum RE78 gain thresholds in historical 1982 U.S. dollars</text>
<line x1="100" y1="400" x2="1100" y2="400" stroke="#222"/><line x1="100" y1="100" x2="100" y2="400" stroke="#222"/>
<polyline points="{' '.join(points)}" fill="none" stroke="#333" stroke-width="3"/>
<text x="600" y="455" text-anchor="middle" font-family="Arial" font-size="15">Minimum-gain threshold (1982 U.S. dollars)</text>
<text x="28" y="250" transform="rotate(-90 28 250)" text-anchor="middle" font-family="Arial" font-size="15">Bootstrap exceedance fraction</text>
<text x="100" y="420" font-family="Arial" font-size="12">0</text><text x="1060" y="420" font-family="Arial" font-size="12">4,000</text>
<text x="65" y="405" font-family="Arial" font-size="12">0.0</text><text x="65" y="105" font-family="Arial" font-size="12">1.0</text>
</svg>"""

    evaluation = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="590" viewBox="0 0 1200 590">
<rect width="1200" height="590" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Training Evidence Decision Value — Evidence Boundary</text>
<g font-family="Arial">
<rect x="55" y="95" width="1090" height="220" rx="18" fill="#f6f6f6" stroke="#333"/>
<text x="85" y="135" font-size="20" font-weight="700">Released evidence</text>
<text x="85" y="170" font-size="16">Observed RE78 difference: {metrics["difference_re78_1982_usd"]:,.2f} historical 1982 U.S. dollars.</text>
<text x="85" y="198" font-size="16">Large-sample 95% interval: {metrics["normal95_low_1982_usd"]:,.2f} to {metrics["normal95_high_1982_usd"]:,.2f}.</text>
<text x="85" y="226" font-size="16">Bootstrap 95% percentile interval: {metrics["bootstrap95_low_1982_usd"]:,.2f} to {metrics["bootstrap95_high_1982_usd"]:,.2f}.</text>
<text x="85" y="254" font-size="16">Two-sided treatment-label permutation diagnostic p = {metrics["permutation_two_sided_p"]:.6f}.</text>
<text x="85" y="282" font-size="16">Dense frontier: 0–4,000 by 100; 50% exceedance frontier reaches {diagnostics["0_50"]:,}.</text>
<rect x="55" y="350" width="1090" height="160" rx="18" fill="#f6f6f6" stroke="#333"/>
<text x="85" y="390" font-size="20" font-weight="700">Claim boundary</text>
<text x="85" y="425" font-size="16">Thresholds are illustrative scenarios, not observed program costs or modern L&amp;D break-even values.</text>
<text x="85" y="453" font-size="16">Bootstrap exceedance fractions are not posterior probabilities; the label permutation is a diagnostic, not exact design reconstruction.</text>
<text x="85" y="481" font-size="16">Transport from this historical program and population to modern corporate training requires separate evidence.</text>
</g>
</svg>"""

    (assets / "architecture.svg").write_text(architecture)
    (assets / "method.svg").write_text(method)
    (assets / "research_design.svg").write_text(research_design)
    (assets / "evaluation.svg").write_text(evaluation)


def write_outputs(frontier, core, robustness, summary, manifest):
    write_csv(
        PRIMARY_PATH,
        frontier,
        ["minimum_gain_threshold_1982_usd", "point_estimate_headroom_1982_usd", "bootstrap_exceedance_fraction"],
    )
    write_csv(
        SECONDARY_PATH,
        [{"metric": key, "value": value} for key, value in core],
        ["metric", "value"],
    )
    write_csv(
        ROBUSTNESS_PATH,
        [{"metric": key, "value": value} for key, value in robustness],
        ["metric", "value"],
    )
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    write_figures(frontier, summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--refresh-fingerprints", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text())
    sources = fetch_sources(manifest, refresh_fingerprints=args.refresh_fingerprints)
    frontier, core, robustness, summary = analyze(sources)
    if args.write:
        write_outputs(frontier, core, robustness, summary, manifest)

    print(json.dumps({
        "source_files": manifest["source_files"],
        "summary": summary,
        "frontier_rows": len(frontier),
        "core_results": dict(core),
        "robustness": dict(robustness),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
