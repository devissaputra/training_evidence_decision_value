# Third-Party Data Attribution

Repository code and original documentation are licensed under the MIT License.

The empirical data are the **Dehejia–Wahba RE74 subset of the National Supported Work Demonstration** hosted on Rajeev Dehejia's NBER page.

The source page states that these data are distributed for **attributable non-commercial use (CC BY-NC)** and asks users to cite the associated Dehejia–Wahba and LaLonde papers.

Source page: https://users.nber.org/~rdehejia/nswdata2.html

This repository does **not** redistribute participant-level source files. During a reproducibility run it downloads the two published experimental files and stores only derived statistics, tables, and figures.

Repository transformations include source-layout validation, treatment-indicator checks, treated-minus-control RE78 estimation, a Welch-standard-error large-sample interval, seeded nonparametric bootstrap resampling, a seeded treatment-label permutation diagnostic, threshold-frontier calculations, and derived visualizations.

The repository does not claim endorsement by NBER, Dehejia, Wahba, LaLonde, or the original National Supported Work investigators.
