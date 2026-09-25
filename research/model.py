from __future__ import annotations
import csv, json, math, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mean(xs):return sum(xs)/len(xs)
def mean_difference(treated,control):return mean(treated)-mean(control)
def bootstrap_differences(treated,control,n=5000,seed=20260925):
    rng=random.Random(seed); return [mean([rng.choice(treated) for _ in treated])-mean([rng.choice(control) for _ in control]) for _ in range(n)]
def exceedance_fraction(samples,threshold):return sum(x>threshold for x in samples)/len(samples)
def percentile(sorted_samples,p):return sorted_samples[int(p*(len(sorted_samples)-1))]
def load_curve():
    with (ROOT/'data/derived/primary_results.csv').open() as f:return list(csv.DictReader(f))
def load_summary():return json.loads((ROOT/'results/empirical_summary.json').read_text())
def validate_bundle():
    rows=load_curve(); vals=[float(r['bootstrap_exceedance_fraction']) for r in rows]
    return len(rows)==6 and all(a>=b for a,b in zip(vals,vals[1:])) and abs(float(rows[3]['bootstrap_exceedance_fraction'])-.36)<1e-9
