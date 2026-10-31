# Effect of training hours on firm productivity

## Conclusion
Training hours are positively associated with 2023 productivity, even after adjusting for all pre-treatment firm characteristics. The preferred estimate is about +0.58 thousand USD of value added per employee for each additional (standardized-scale) training hour (SE 0.233, p = 0.013). The raw association (2.49) is about four times larger. Most of that gap is confounding: larger, older, and previously more productive firms train more. The data are a cross-section and the estimate is observational. Residual confounding by unobserved factors is possible, so the effect is not definitively causal and is probably modest.

## Preferred specification
OLS of productivity_2023 on training_hours, controlling for all pre-treatment (2020) covariates: log employees, firm age, 2020 productivity, region, listed, sector, export share, foreign-owned, family-owned, R&D intensity, union share, and credit score. HC1 robust SEs, N = 2000.
- Estimate: 0.579
- SE: 0.233
- p-value: 0.0128

I deliberately did **not** control for mgmt_rating_2023 in the preferred model. It is measured in 2023, after the training period. It is strongly correlated with training (r = 0.54), so it is plausibly a mediator or a collider. Conditioning on it flips the sign (-2.35), which I judge to be a bias artifact and not a real negative effect. I report it below for transparency.

## All specifications estimated (coefficient on training_hours, HC1 SEs, N = 2000)
| # | Specification | Estimate | SE | p |
|---|---|---|---|---|
| 1 | Raw, no controls | 2.488 | 0.241 | 4.8e-25 |
| 2 | + productivity_2020 only | 2.069 | 0.243 | 1.7e-17 |
| 3 | + size, age, region, listed, sector | 0.698 | 0.232 | 0.0026 |
| 4 | **Full pre-treatment controls (preferred)** | **0.579** | **0.233** | **0.0128** |
| 5 | Full controls + mgmt_rating_2023 (post-treatment; not preferred) | -2.347 | 0.229 | 1.0e-24 |
| 6 | Full pre-treatment controls + quadratic in training | 0.580 (linear term) | 0.233 | 0.0127 |
| 7 | log(productivity_2023) outcome, full controls | 0.0061 (about 0.6% per unit) | 0.0023 | 0.0095 |
| 8 | Full controls, training x sector interaction | 0.781 (manufacturing baseline) | 0.321 | 0.0149 |

I also ran a diagnostic regression of training on the covariates. It is not an effect estimate. It shows that size, age, and prior productivity predict training, which confirms the selection into training.

Total effect specifications estimated: 8.

## Caveats
- The effect is identified only under selection on observables. No instrument, panel, or experimental variation is available.
- The estimate is sensitive to the control set. It falls from 2.49 to 0.58 as pre-treatment controls are added, and further unobserved confounders could reduce it more.
- The sign reversal when mgmt_rating_2023 is added shows how fragile the estimate is to post-treatment conditioning.
- Training units are standardized (mean 0), so the estimate is per unit of the variable as coded.
