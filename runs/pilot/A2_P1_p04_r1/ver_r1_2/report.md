# Effect of training hours on productivity

**Conclusion: positive effect.** Preferred estimate: +0.84 thousand USD of value added per employee (2023) per one-unit increase in training_hours. The standard error is 0.241 (HC1 robust) and p = 0.0005. training_hours is standardized (mean 0, SD about 1), so this is roughly one SD of training.

Preferred specification: OLS of productivity_2023 on training_hours plus all pre-period (2020) controls, with HC1 standard errors. The controls are log employees, firm age, productivity_2020, region, sector, listed, export share, foreign-owned, family-owned, R&D intensity, union share and credit score. N = 2000.

## Why this specification
- The naive estimate (2.37) is confounded. Larger and older firms train more and are also more productive. Adding the pre-period controls cuts the estimate to about 0.84.
- mgmt_rating_2023 is measured in 2023, after training. It is plausibly a mediator or a consequence of training and productivity. Conditioning on it flips the sign to -2.09, and I treat that as bias from a post-treatment control, so I do not prefer it. The 2023 rating correlates 0.52 with training and 0.58 with productivity.
- The result is causal only if the pre-period controls remove all confounding. Unobserved confounders are still possible, so the estimate may not be purely causal.

## All specifications estimated (8; all OLS, HC1 SE, N = 2000)
Outcome is productivity_2023 unless noted.

| # | Specification | Coefficient | SE | p |
|---|---|---|---|---|
| 1 | training only | 2.373 | 0.239 | 2.7e-23 |
| 2 | + productivity_2020 | 2.090 | 0.238 | 1.9e-18 |
| 3 | + productivity_2020, size, age, region, sector, listed | 0.837 | 0.241 | 5.1e-4 |
| 4 | **Full pre-period controls (preferred)** | **0.841** | **0.241** | **4.9e-4** |
| 5 | Full pre-period controls + mgmt_rating_2023 (post-treatment, not preferred) | -2.089 | 0.234 | 3.9e-19 |
| 6 | training + mgmt_rating_2023 only (not preferred) | -1.394 | 0.238 | 4.5e-9 |
| 7 | Full pre-period controls + quadratic term in training (linear term shown) | 0.841 | 0.242 | 5.0e-4 |
| 8 | log(productivity_2023), full pre-period controls | 0.0088 (about 0.9% per unit) | 0.0024 | 2.8e-4 |

Specifications 3, 4, 7 and 8 agree on a positive effect. The sign of the effect depends on whether the post-treatment management rating is included (specifications 5 and 6).
