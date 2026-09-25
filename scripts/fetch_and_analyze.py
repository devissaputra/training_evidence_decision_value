#!/usr/bin/env python3
import json, math, statistics, urllib.request
from research.model import mean,mean_difference,bootstrap_differences,exceedance_fraction,percentile
URLS=['https://www.nber.org/~rdehejia/data/nswre74_control.txt','https://www.nber.org/~rdehejia/data/nswre74_treated.txt']
def get(u):return [[float(x) for x in line.split()] for line in urllib.request.urlopen(u).read().decode().splitlines() if line.strip()]
control,treated=map(get,URLS); yc=[x[9] for x in control]; yt=[x[9] for x in treated]
diff=mean_difference(yt,yc); se=math.sqrt(statistics.variance(yt)/len(yt)+statistics.variance(yc)/len(yc)); normal=(diff-1.96*se,diff+1.96*se)
boot=sorted(bootstrap_differences(yt,yc,5000,20260925)); thresholds=[500,1000,1500,2000,2500,3000]
curve={str(h):exceedance_fraction(boot,h) for h in thresholds}
summary={'study':'Decision Value of Training Evidence: Reanalysis of the National Supported Work Experiment','headline_metrics':{'n_control':len(yc),'n_treated':len(yt),'control_mean_re78':round(mean(yc),2),'treated_mean_re78':round(mean(yt),2),'difference_re78':round(diff,2),'normal_ci_low':round(normal[0],2),'normal_ci_high':round(normal[1],2),'bootstrap_ci_low':round(percentile(boot,.025),2),'bootstrap_ci_high':round(percentile(boot,.975),2),'bootstrap_positive_exceedance_fraction':round(exceedance_fraction(boot,0),3),'bootstrap_exceedance_fraction_gt_2000':round(curve['2000'],3)},'finding':'The observed randomized difference in 1978 earnings is $1,794.34. A seeded nonparametric bootstrap gives a 95% resampling interval of about $501–$3,097. Only 36% of bootstrap resamples exceed a $2,000 minimum-gain threshold; this is a bootstrap exceedance fraction, not a Bayesian posterior probability.','source':'National Supported Work Demonstration — Dehejia-Wahba experimental sample','retrieved':'2026-09-25'}
print(json.dumps({'summary':summary,'threshold_curve':curve},indent=2))
