# Effect of training hours on productivity

**Conclusion: positive effect.** Preferred estimate: +0.841 thousand USD value added per employee for each additional unit of training_hours (SE 0.241, p = 0.0005, HC1 robust SEs, N = 2000). This is a regression-adjusted association from cross-sectional observational data. I read it as an effect only if the pre-2021 controls remove all confounding, which I can't verify.

## Preferred specification
OLS of productivity_2023 on training_hours, controlling for all pre-period (2020) covariates: log employees, firm age, productivity_2020, region, listed, sector, export share, foreign ownership, family ownership, R&D intensity, union share and credit score.

I chose it because training was not randomly assigned. The naive estimate is about 2.8 times larger than the adjusted one, so confounding is clearly present. Training (2021-22) is correlated with 2020 productivity (r = 0.14) and with other firm characteristics.

I deliberately did **not** control for mgmt_rating_2023. It is measured in 2023, after the training, and is strongly related to training (r = 0.52). It is therefore a post-treatment variable, either a mediator or a collider. Adjusting for it flips the sign to -2.09, which is a bias artifact and not a credible effect. This differs from what the PI hoped for only in that the preferred estimate is much smaller than the naive one. It is still positive and significant.

## All specifications estimated (7; OLS, HC1 SEs, coefficient on training_hours)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive: training only | 2.373 | 0.239 | <0.001 |
| 2 | + log employees, age, region, sector, listed | 0.900 | 0.240 | 0.0002 |
| 3 | + productivity_2020 only | 2.090 | 0.238 | <0.001 |
| 4 | **Full pre-period controls (preferred)** | **0.841** | **0.241** | **0.0005** |
| 5 | Full pre-period controls + mgmt_rating_2023 (post-treatment, rejected) | -2.089 | 0.234 | <0.001 |
| 6 | Full pre-period controls + training² | 0.841 | 0.242 | 0.0005 |
| 7 | log(productivity_2023), full pre-period controls | 0.0088 (about 0.9% per unit) | 0.0024 | 0.0003 |

Specification 6 reports the linear term. The quadratic term was included only as a nonlinearity check.

## Caveats
- Selection on unobservables is possible, so the estimate is not guaranteed to be causal.
- The training_hours variable appears standardized (mean about 0), so "one unit" is about one standard deviation, not one hour. The codebook does not say this.
- The estimate shrinks sharply as controls are added (2.37 to 0.84). Residual confounding could shrink it further.
- I made no multiple-testing correction. Specifications 2, 4, 6 and 7 agree on a positive effect of roughly 0.8-0.9.
