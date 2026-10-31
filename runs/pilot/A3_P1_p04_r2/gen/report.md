# Effect of training hours on firm productivity

**Conclusion: positive effect.** With adjustment for pre-period firm characteristics, one more standardized unit of training hours is associated with about +0.84 thousand USD of value added per employee in 2023 (about 0.8% of mean productivity of ~100.97).

**Preferred estimate:** OLS of productivity_2023 on training_hours plus all pre-treatment (2020) covariates, region, sector and listed status, with HC1 robust SEs. N = 2000.
- Estimate 0.841, SE 0.241, p = 0.0005 (95% CI 0.37 to 1.31).

## Reasoning
- This is observational cross-section data, so the estimate is an adjusted association. A causal reading requires that the pre-period controls (including lagged productivity) capture selection into training. Unobserved confounding remains possible.
- The naive estimate (2.37) is nearly 3 times larger than the adjusted one. Larger, older and already-more-productive firms train more, so the naive figure is confounded. I do not rely on it.
- mgmt_rating_2023 is measured after the training period and correlates strongly with training (r = 0.52). It is plausibly affected by both training and productivity, so it is a mediator or collider. Controlling for it flips the sign to -2.09. I consider that estimate a bad-control artefact and do not prefer it. If management rating were a pure mediator, the total effect would still be the one without it.
- The size of the effect is modest, and the log-outcome and quadratic specifications agree with the preferred one. The quadratic term gives no evidence of nonlinearity.

## All specifications estimated (6; all OLS, HC1 SEs, N = 2000)
| # | Specification | Coef on training_hours | SE | p |
|---|---|---|---|---|
| 1 | Naive: no controls | 2.373 | 0.239 | 2.7e-23 |
| 2 | Controls: log_employees_2020, firm_age_2020, productivity_2020 | 0.798 | 0.241 | 0.0009 |
| 3 | **Preferred**: all pre-treatment controls + region, sector, listed | 0.841 | 0.241 | 0.0005 |
| 4 | #3 plus mgmt_rating_2023 (post-treatment, not preferred) | -2.089 | 0.234 | 3.9e-19 |
| 5 | #3 with log(productivity_2023) as outcome | 0.0088 (about 0.9% per unit) | 0.0024 | 0.0003 |
| 6 | #3 plus a quadratic term in training_hours (linear coefficient reported) | 0.841 | 0.242 | 0.0005 |

The specifications were chosen on the basis of covariate timing, not on the results. The one specification with an opposite sign (#4) was reported and is excluded for the reason given above.
