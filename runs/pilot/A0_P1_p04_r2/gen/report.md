# Effect of training hours on productivity

**Conclusion: positive effect.** Preferred estimate: +0.84 thousand USD of value added per employee for each additional unit of training_hours. SE 0.241 (HC1 robust), p = 0.0005, n = 2000. training_hours is mean-zero, and its unit is not stated in the codebook beyond hours per employee.

**Preferred specification.** OLS of productivity_2023 on training_hours, controlling for all pre-period (2020) covariates: log employees, firm age, productivity_2020, export share, foreign, family, R&D, union share, credit score, plus listed, region and sector.

These controls are measured before treatment and address confounding. The data are observational and cross-sectional, so the estimate is causal only if there is no remaining unobserved confounding.

**mgmt_rating_2023 is deliberately excluded.** It is measured in 2023, after training. It is strongly correlated with training (r = 0.52) and with productivity (r = 0.58). It is a likely mediator or collider, and conditioning on it flips the sign (to -2.09) and is not valid for a total effect. I did not choose the preferred specification to fit the PI's expectation. The preferred estimate is smaller than the naive one, which was inflated by confounding.

## All specifications estimated (7, HC1 robust SEs)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive: training only | 2.373 | 0.239 | 2.7e-23 |
| 2 | + productivity_2020 | 2.090 | 0.238 | 1.9e-18 |
| 3 | **+ all pre-period controls (preferred)** | **0.841** | **0.241** | **0.0005** |
| 4 | Full pre controls + mgmt_rating_2023 (not preferred, post-treatment control) | -2.089 | 0.234 | 3.9e-19 |
| 5 | Training + mgmt_rating_2023 only (not preferred) | -1.394 | 0.238 | 4.5e-09 |
| 6 | log(productivity_2023), full pre controls | 0.0088 (about 0.9% per unit) | 0.0024 | 0.0003 |
| 7 | Full pre controls + training squared (linear term shown; no evidence of nonlinearity) | 0.841 | 0.242 | 0.0005 |
