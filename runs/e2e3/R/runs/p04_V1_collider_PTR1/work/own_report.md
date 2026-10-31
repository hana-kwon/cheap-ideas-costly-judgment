# Effect of training hours on firm productivity

**Conclusion: positive effect.** An extra standard-deviation-scale unit of training hours is associated with about +0.84 thousand USD of 2023 value added per employee (about 0.8% of mean productivity of ~101). The estimate is causal only if controlling for the pre-period covariates removes confounding.

**Preferred estimate:** OLS of productivity_2023 on training_hours, controlling for all pre-treatment (2020) covariates. These are log employees, firm age, 2020 productivity, region, listed, sector, export share, foreign-owned, family-owned, R&D intensity, union share and credit score. Standard errors are HC1 robust.
- Estimate = 0.841 (thousand USD per unit of training_hours)
- SE = 0.241
- p = 0.0005
- 95% CI about [0.37, 1.31]
- N = 2000

Larger firms, older firms and firms with higher 2020 productivity all train more. The raw correlation (2.37) is therefore inflated by confounding, and adjusting cuts it by about 65%.

**mgmt_rating_2023 is deliberately excluded.** It is measured in 2023, after training, so it is plausibly a mediator or collider. Controlling for it would be bad control. Adding it flips the sign to -2.09, which is the signature of that bias, so I do not interpret it.

**Caveat:** this is observational cross-section data. Unobserved confounders such as management quality could remain, so the estimate may still be biased. Because the raw and adjusted estimates differ so much, residual confounding is a real concern.

## All specifications estimated (outcome regressions on training_hours, HC1 SEs)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw bivariate | 2.373 | 0.239 | 2.7e-23 |
| 2 | + log_employees, age, productivity_2020 | 0.798 | 0.241 | 0.0009 |
| 3 | **All pre-period covariates (preferred)** | 0.841 | 0.241 | 0.0005 |
| 4 | #3 + mgmt_rating_2023 (post-treatment; not preferred) | -2.089 | 0.234 | 3.9e-19 |
| 5 | log(productivity_2023), all pre covariates | 0.0088 (about 0.9%) | 0.0024 | 0.0003 |
| 6 | #3 + quadratic in training (linear term shown) | 0.841 | 0.242 | 0.0005 |

I also ran a descriptive regression of training_hours on the covariates. It is not an effect estimate and is not counted above.
