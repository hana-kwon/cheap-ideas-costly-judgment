# Effect of training hours on productivity

**Conclusion: positive effect, modest in size.** The preferred estimate is that one more unit of training_hours raises 2023 productivity by 0.58 thousand USD per employee (SE 0.233, p = 0.013, n = 2000). training_hours is centred at 0, so a unit is probably one standard deviation, but I did not check the SD. Productivity averages about 100, so the effect is about 0.6%.

Preferred specification: OLS of productivity_2023 on training_hours plus all 2020 pre-period controls, with HC1 robust standard errors. The controls are log employees, firm age, lagged productivity, region, listed, sector, export share, foreign-owned, family-owned, R&D intensity, union share and credit score.

## Why this one
- The naive estimate (2.49) is about four times larger. Firms with more training also differ in their pre-period characteristics, and 15% of the variation in training is explained by those characteristics. Controlling for them, especially lagged productivity, removes most of the apparent effect.
- mgmt_rating_2023 is measured in 2023, after the training. It is probably affected by training, so controlling for it is a bad control. Training raises it by about 0.66 per unit in a regression on the pre-period controls. Adding it flips the training estimate to -2.35, which I take to be an artefact, so I do not prefer it.
- This is observational data. Selection on unobservables is still possible, so the estimate may not be causal. The effect is also sensitive to the control set: it ranges from 0.58 to 0.71 across the reasonable specifications, with the lagged-productivity control mattering most.

## All specifications estimated (training_hours coefficient, HC1 SE)
| # | Specification | Estimate | SE | p |
|---|---|---|---|---|
| 1 | Naive, no controls | 2.488 | 0.241 | <0.001 |
| 2 | + log employees, age, lagged productivity | 0.589 | 0.234 | 0.012 |
| 3 | **All pre-period controls (preferred)** | **0.579** | **0.233** | **0.013** |
| 4 | Spec 3 + mgmt_rating_2023 (bad control) | -2.347 | 0.229 | <0.001 |
| 5 | Spec 3 + training_hours squared | 0.580 (linear term) | 0.233 | 0.013 |
| 6 | Spec 3 with log(productivity) as the outcome | 0.0061 (about 0.6%) | 0.0023 | 0.0095 |
| 7 | Spec 3 without lagged productivity | 0.709 | 0.233 | 0.0023 |

In spec 5 the squared term is 0.043 (p = 0.77), so there is no evidence of nonlinearity.

Two auxiliary regressions were run as diagnostics and are not counted as effect specifications: training on the pre-period controls (R² = 0.15), and mgmt_rating_2023 on training with controls (coefficient 0.66).
