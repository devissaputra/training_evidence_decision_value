from __future__ import annotations

import csv
import json
import math
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SOURCE_ROWS = {"control": 260, "treated": 185}
EXPECTED_SOURCE_SHA256 = {
    "control": "a1364cea459d953dc691a667d99194b4ad335d6d550354fe23a5d2dc58d729b5",
    "treated": "e7b742fe0ff07a0f45e129b4ff108bb9611cd83d53604732c48a8a0a3e20eda3",
}
EXPECTED_HEADLINE = {
    "n_control": 260,
    "n_treated": 185,
    "control_mean_re78_1982_usd": 4554.8,
    "treated_mean_re78_1982_usd": 6349.14,
    "difference_re78_1982_usd": 1794.34,
    "welch_standard_error_1982_usd": 671.0,
    "normal95_low_1982_usd": 479.19,
    "normal95_high_1982_usd": 3109.5,
    "bootstrap95_low_1982_usd": 519.04,
    "bootstrap95_high_1982_usd": 3117.8,
    "bootstrap_positive_fraction": 0.9978,
    "bootstrap_exceedance_gt_2000": 0.3818,
    "permutation_two_sided_p": 0.005899,
}
EXPECTED_COLUMNS = 10
BOOTSTRAP_SEED = 20260925
BOOTSTRAP_RESAMPLES = 5000
PERMUTATION_SEED = 20260926
PERMUTATION_RESAMPLES = 10000


def mean(values):
    values = list(values)
    if not values:
        raise ValueError("mean requires observations")
    return statistics.fmean(values)


def mean_difference(treated, control):
    return mean(treated) - mean(control)


def welch_standard_error(treated, control):
    return math.sqrt(
        statistics.variance(treated) / len(treated)
        + statistics.variance(control) / len(control)
    )


def large_sample_normal_interval(treated, control, z=1.96):
    effect = mean_difference(treated, control)
    se = welch_standard_error(treated, control)
    return effect - z * se, effect + z * se


def quantile_linear(sorted_values, p):
    values = list(sorted_values)
    if not values:
        raise ValueError("quantile requires observations")
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0, 1]")
    if len(values) == 1:
        return float(values[0])
    position = (len(values) - 1) * p
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return float(values[low])
    fraction = position - low
    return float(values[low]) + fraction * (float(values[high]) - float(values[low]))


def bootstrap_differences(treated, control, n=BOOTSTRAP_RESAMPLES, seed=BOOTSTRAP_SEED):
    treated = list(treated)
    control = list(control)
    rng = random.Random(seed)
    return [
        mean(rng.choices(treated, k=len(treated)))
        - mean(rng.choices(control, k=len(control)))
        for _ in range(n)
    ]


def exceedance_fraction(samples, threshold):
    samples = list(samples)
    if not samples:
        raise ValueError("exceedance_fraction requires samples")
    return sum(value > threshold for value in samples) / len(samples)


def permutation_differences(treated, control, n=PERMUTATION_RESAMPLES, seed=PERMUTATION_SEED):
    treated = list(treated)
    control = list(control)
    combined = treated + control
    n_treated = len(treated)
    rng = random.Random(seed)
    results = []
    for _ in range(n):
        shuffled = combined[:]
        rng.shuffle(shuffled)
        results.append(mean(shuffled[:n_treated]) - mean(shuffled[n_treated:]))
    return results


def two_sided_permutation_pvalue(observed, null_differences):
    null_differences = list(null_differences)
    extreme = sum(abs(value) >= abs(observed) for value in null_differences)
    return (extreme + 1) / (len(null_differences) + 1)


def load_csv(path):
    with (ROOT / path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def load_frontier():
    return load_csv("data/derived/primary_results.csv")


def load_core_results():
    return load_csv("data/derived/secondary_results.csv")


def load_robustness():
    return load_csv("data/derived/robustness_results.csv")


def load_summary():
    return json.loads((ROOT / "results/empirical_summary.json").read_text())


def load_manifest():
    return json.loads((ROOT / "data/source_manifest.json").read_text())


def validate_bundle():
    manifest = load_manifest()
    summary = load_summary()
    frontier = load_frontier()
    core = {row["metric"]: row["value"] for row in load_core_results()}
    robustness = {row["metric"]: row["value"] for row in load_robustness()}
    metrics = summary["headline_metrics"]

    if len(frontier) != 41:
        return False
    thresholds = [int(row["minimum_gain_threshold_1982_usd"]) for row in frontier]
    if thresholds != list(range(0, 4001, 100)):
        return False

    exceedance = [float(row["bootstrap_exceedance_fraction"]) for row in frontier]
    if not all(a >= b for a, b in zip(exceedance, exceedance[1:])):
        return False

    effect = float(metrics["difference_re78_1982_usd"])
    for row in frontier:
        threshold = float(row["minimum_gain_threshold_1982_usd"])
        if abs(float(row["point_estimate_headroom_1982_usd"]) - (effect - threshold)) > 0.02:
            return False

    if int(metrics["n_control"]) != EXPECTED_SOURCE_ROWS["control"]:
        return False
    if int(metrics["n_treated"]) != EXPECTED_SOURCE_ROWS["treated"]:
        return False

    source_files = manifest.get("source_files", {})
    for key, expected_rows in EXPECTED_SOURCE_ROWS.items():
        item = source_files.get(key, {})
        if int(item.get("rows", -1)) != expected_rows:
            return False
        if int(item.get("columns", -1)) != EXPECTED_COLUMNS:
            return False
        sha = str(item.get("sha256", ""))
        if len(sha) != 64 or any(ch not in "0123456789abcdef" for ch in sha):
            return False
        if sha != EXPECTED_SOURCE_SHA256[key]:
            return False

    for key, expected in EXPECTED_HEADLINE.items():
        actual = metrics.get(key)
        if isinstance(expected, float):
            if actual is None or abs(float(actual) - expected) > 5e-5:
                return False
        elif actual != expected:
            return False

    expected_core = {
        "n_control": metrics["n_control"],
        "n_treated": metrics["n_treated"],
        "control_mean_re78_1982_usd": metrics["control_mean_re78_1982_usd"],
        "treated_mean_re78_1982_usd": metrics["treated_mean_re78_1982_usd"],
        "difference_re78_1982_usd": metrics["difference_re78_1982_usd"],
        "welch_standard_error_1982_usd": metrics["welch_standard_error_1982_usd"],
        "normal95_low_1982_usd": metrics["normal95_low_1982_usd"],
        "normal95_high_1982_usd": metrics["normal95_high_1982_usd"],
        "bootstrap95_low_1982_usd": metrics["bootstrap95_low_1982_usd"],
        "bootstrap95_high_1982_usd": metrics["bootstrap95_high_1982_usd"],
        "permutation_two_sided_p": metrics["permutation_two_sided_p"],
    }
    for key, expected in expected_core.items():
        if key not in core or abs(float(core[key]) - float(expected)) > 5e-5:
            return False

    levels = summary["decision_frontier_diagnostics"]
    for level_key, value in levels.items():
        robustness_key = f"max_threshold_with_bootstrap_exceedance_at_least_{level_key}"
        if robustness_key not in robustness:
            return False
        if abs(float(robustness[robustness_key]) - float(value)) > 1e-9:
            return False

    return manifest.get("raw_data_redistributed") is False
