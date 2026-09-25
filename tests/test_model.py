import pytest

from research.model import (
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    EXPECTED_SOURCE_ROWS,
    PERMUTATION_RESAMPLES,
    PERMUTATION_SEED,
    bootstrap_differences,
    exceedance_fraction,
    large_sample_normal_interval,
    load_core_results,
    load_frontier,
    load_manifest,
    load_robustness,
    load_summary,
    mean_difference,
    permutation_differences,
    quantile_linear,
    two_sided_permutation_pvalue,
    validate_bundle,
    welch_standard_error,
)


def test_mean_difference_and_se():
    treated = [3, 5, 7]
    control = [1, 2, 3, 4]
    assert mean_difference(treated, control) == pytest.approx(2.5)
    assert welch_standard_error(treated, control) > 0


def test_large_sample_interval_contains_effect():
    treated = [3, 5, 7]
    control = [1, 2, 3, 4]
    effect = mean_difference(treated, control)
    low, high = large_sample_normal_interval(treated, control)
    assert low < effect < high


def test_linear_quantile():
    values = [0, 1, 2, 3, 4]
    assert quantile_linear(values, 0.25) == 1
    assert quantile_linear(values, 0.50) == 2
    assert quantile_linear(values, 0.90) == pytest.approx(3.6)


def test_seeded_bootstrap_is_reproducible():
    treated = [3, 4, 5]
    control = [1, 2, 2]
    first = bootstrap_differences(treated, control, n=200, seed=7)
    second = bootstrap_differences(treated, control, n=200, seed=7)
    assert first == second
    assert exceedance_fraction(first, 1) >= exceedance_fraction(first, 3)


def test_seeded_permutation_is_reproducible():
    treated = [3, 4, 5]
    control = [1, 2, 2]
    first = permutation_differences(treated, control, n=200, seed=11)
    second = permutation_differences(treated, control, n=200, seed=11)
    assert first == second
    p = two_sided_permutation_pvalue(mean_difference(treated, control), first)
    assert 0 < p <= 1


def test_source_manifest_is_pinned():
    manifest = load_manifest()
    for key, expected_rows in EXPECTED_SOURCE_ROWS.items():
        item = manifest["source_files"][key]
        assert item["rows"] == expected_rows
        assert item["columns"] == 10
        assert len(item["sha256"]) == 64
    assert manifest["source_files"]["control"]["treatment_indicator"] == 0
    assert manifest["source_files"]["treated"]["treatment_indicator"] == 1
    assert manifest["raw_data_redistributed"] is False


def test_released_sample_and_effect():
    metrics = load_summary()["headline_metrics"]
    assert metrics["n_control"] == 260
    assert metrics["n_treated"] == 185
    assert metrics["control_mean_re78_1982_usd"] == pytest.approx(4554.8, abs=0.01)
    assert metrics["treated_mean_re78_1982_usd"] == pytest.approx(6349.14, abs=0.01)
    assert metrics["difference_re78_1982_usd"] == pytest.approx(1794.34, abs=0.01)
    assert metrics["welch_standard_error_1982_usd"] > 0
    assert 0 < metrics["permutation_two_sided_p"] <= 1


def test_dense_frontier_and_monotonicity():
    rows = load_frontier()
    assert len(rows) == 41
    assert [int(r["minimum_gain_threshold_1982_usd"]) for r in rows] == list(range(0, 4001, 100))
    fractions = [float(r["bootstrap_exceedance_fraction"]) for r in rows]
    assert all(a >= b for a, b in zip(fractions, fractions[1:]))


def test_threshold_headroom_reconciles():
    effect = load_summary()["headline_metrics"]["difference_re78_1982_usd"]
    for row in load_frontier():
        threshold = float(row["minimum_gain_threshold_1982_usd"])
        assert float(row["point_estimate_headroom_1982_usd"]) == pytest.approx(effect - threshold, abs=0.02)


def test_core_table_matches_summary():
    summary = load_summary()["headline_metrics"]
    core = {r["metric"]: float(r["value"]) for r in load_core_results()}
    for key in [
        "n_control", "n_treated", "control_mean_re78_1982_usd", "treated_mean_re78_1982_usd",
        "difference_re78_1982_usd", "welch_standard_error_1982_usd", "normal95_low_1982_usd",
        "normal95_high_1982_usd", "bootstrap95_low_1982_usd", "bootstrap95_high_1982_usd",
        "permutation_two_sided_p",
    ]:
        assert core[key] == pytest.approx(summary[key], abs=5e-5)


def test_robustness_configuration_and_frontier_diagnostics():
    robust = {r["metric"]: float(r["value"]) for r in load_robustness()}
    assert robust["bootstrap_resamples"] == BOOTSTRAP_RESAMPLES
    assert robust["bootstrap_seed"] == BOOTSTRAP_SEED
    assert robust["permutation_resamples"] == PERMUTATION_RESAMPLES
    assert robust["permutation_seed"] == PERMUTATION_SEED
    for key, value in load_summary()["decision_frontier_diagnostics"].items():
        assert robust[f"max_threshold_with_bootstrap_exceedance_at_least_{key}"] == value


def test_bundle_validation():
    assert validate_bundle()
