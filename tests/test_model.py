from research.model import mean_difference,bootstrap_differences,exceedance_fraction,validate_bundle
def test_mean_difference(): assert mean_difference([3,5],[1,1])==3
def test_seeded_bootstrap_and_threshold_monotonicity():
    b=bootstrap_differences([3,4,5],[1,2,2],n=200,seed=7); assert b==bootstrap_differences([3,4,5],[1,2,2],n=200,seed=7); assert exceedance_fraction(b,1)>=exceedance_fraction(b,3)
def test_packaged_curve(): assert validate_bundle()
