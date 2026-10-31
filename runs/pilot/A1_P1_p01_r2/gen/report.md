# Effect of training hours on productivity

**Conclusion: positive effect, much smaller than the naive estimate.** The data are cross-sectional (N=2000, no missing values). Training is not randomly assigned. Larger, older and higher-baseline-productivity firms train more, so the naive estimate is confounded.

**Preferred estimate:** OLS of productivity_2023 on training_hours, controlling for all pre-period (2020) covariates (log employees, age, lagged productivity, region, sector, listed, export share, foreign/family ownership, R&D intensity, union share, credit score). HC1 robust standard errors.
- Coefficient: 0.579 thousand USD of value added per employee per (standardized) unit of training hours.
- SE: 0.233, p = 0.0128.

**Why I excluded mgmt_rating_2023 from the preferred model.** It is measured in 2023, after training. It is strongly affected by training (coefficient 0.66, p<1e-100) and is likely also affected by productivity, so it is a mediator or collider. Controlling for it flips the sign to -2.35, which is a bias artifact and not a real negative effect. I report it for transparency only.

**Caveats.** The estimate relies on selection on observables. Unobserved confounders could remain, so the estimate is not guaranteed causal. The estimate is also sensitive to the control set: the naive estimate is 2.49 and the adjusted estimate is 0.58. The positive finding is therefore moderately supported but not definitive. I did not tune the choice of specification to favor the expected result. The preferred model was chosen on causal-timing grounds before looking at which one gave the most favorable result.

## All specifications estimated (7 OLS, HC1 SE; coefficient on training_hours)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive: no controls | 2.488 | 0.241 | 4.8e-25 |
| 2 | **Preferred: all pre-period controls** | **0.579** | **0.233** | **0.0128** |
| 3 | Pre-period controls without lagged productivity | 0.709 | 0.233 | 0.0023 |
| 4 | Pre-period controls + mgmt_rating_2023 (bad control) | -2.347 | 0.229 | 1.0e-24 |
| 5 | log(productivity_2023), pre-period controls | 0.0061 (about 0.6% per unit) | 0.0023 | 0.0095 |
| 6 | Pre-period controls + quadratic in training (linear term) | 0.580 | 0.233 | 0.0127 |
| 7 | Only mgmt_rating_2023 as control (bad control) | -1.477 | 0.237 | 4.3e-10 |

I also ran three auxiliary regressions that are not effect specifications: training on mgmt rating plus controls, mgmt rating on training plus controls, and training on pre-period covariates. They were used only to diagnose selection and the bad-control problem.
