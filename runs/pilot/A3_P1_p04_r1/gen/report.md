# Effect of training hours on productivity

**Conclusion: positive effect.** Preferred estimate: +0.841 thousand USD of 2023 value added per employee for each 1-unit increase in training_hours. SE 0.241 (HC1 robust), p = 0.0005, 95% CI about [0.37, 1.31]. N = 2000.

training_hours is standardized (mean 0). I assume 1 unit is about 1 SD, but the codebook does not say. The effect is small: roughly 0.07 SD of productivity_2023 (SD 11.4).

**Preferred specification:** OLS of productivity_2023 on training_hours plus all pre-period covariates, with HC1 SEs. The covariates are log_employees_2020, firm_age_2020, productivity_2020, region, listed, sector, export_share_2020, foreign_owned, family_owned, rd_intensity_2020, union_share_2020 and credit_score_2020.

Training is not randomized. The estimate is causal only if the pre-period controls remove all confounding. Unobserved confounders could still bias it. The raw association (2.37) is about three times the adjusted one, so confounding by pre-period characteristics was substantial. Some may remain.

**Excluded control:** mgmt_rating_2023 was measured in 2023, after training. It is a possible mediator or collider. Controlling for it turns the estimate sharply negative (-2.09), which is the pattern that bad-control bias would produce. I do not treat that specification as valid.

## All specifications estimated (7; all OLS with HC1 SEs, N = 2000)
| # | Specification | Coef on training_hours | SE | p |
|---|---|---|---|---|
| 1 | Raw bivariate | 2.373 | 0.239 | 2.7e-23 |
| 2 | + log_employees, firm_age, productivity_2020 | 0.798 | 0.241 | 0.0009 |
| 3 | **Full pre-period controls (preferred)** | **0.841** | **0.241** | **0.0005** |
| 4 | Full pre-period controls + mgmt_rating_2023 (bad control, rejected) | -2.089 | 0.234 | 3.9e-19 |
| 5 | log(productivity_2023), full pre-period controls | 0.0088 (about 0.9%) | 0.0024 | 0.0003 |
| 6 | Full pre-period controls + quadratic term | linear 0.841 (quadratic 0.004, p = 0.98, so no curvature) | 0.242 | 0.0005 |
| 7 | Full pre-period controls without productivity_2020 | 0.905 | 0.240 | 0.0002 |

Every specification that uses only pre-treatment controls (2, 3, 5, 6, 7) gives a positive, significant effect of similar size. Only the raw estimate (1) is larger, and only the post-treatment control (4) reverses the sign.
