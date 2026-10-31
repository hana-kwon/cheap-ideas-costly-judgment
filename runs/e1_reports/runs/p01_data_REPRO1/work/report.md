# Effect of training hours on productivity

**Conclusion: positive effect (modest).** The data are a cross-section of 2000 firms, and training_hours is standardized (mean 0). The preferred estimate comes from OLS of productivity_2023 on training_hours. It controls for all pre-period covariates: log size, age, 2020 productivity, region, sector, listed, export share, foreign-owned, family-owned, R&D intensity, union share and credit score. It uses HC1 robust standard errors.

**Preferred estimate: 0.579 thousand USD of value added per employee per one-unit increase in training_hours. SE = 0.233, p = 0.0128, 95% CI [0.12, 1.04].** The same model with log productivity gives about +0.6% per unit (SE 0.0023, p = 0.0095).

Why this specification: training is not randomly assigned. Pre-period firm characteristics (size, age, lagged productivity) correlate with both training and later productivity. The naive estimate (2.49) is therefore about four times larger than the adjusted one, and most of it is confounding. I excluded mgmt_rating_2023 because it is measured after treatment. It is likely a mediator or a collider, and conditioning on it flips the sign to -2.35. I regard that estimate as biased and did not use it.

Caveat: the result rests on selection-on-observables. Unobserved confounders (for example, management quality) could still bias it, so the estimate is not clearly causal. The effect is small and only moderately significant.

## All specifications estimated (8; training_hours coefficient, robust SE, p)
1. Naive bivariate: 2.488 (0.241), p<1e-24. Confounded.
2. Controls for size, age and 2020 productivity: 0.589 (0.234), p=0.012.
3. **Full pre-period controls (preferred): 0.579 (0.233), p=0.0128.**
4. Full pre-period controls plus mgmt_rating_2023 (post-treatment, rejected): -2.347 (0.229), p<1e-23.
5. Log productivity as outcome, full controls: 0.0061 (0.0023), p=0.0095.
6. Full controls without lagged productivity: 0.709 (0.233), p=0.0023.
7. Full controls plus a quadratic term in training: linear term 0.579 (0.233), p=0.013. The quadratic term was not examined further.
8. Interaction of training with sector, full controls: the training coefficient for manufacturing is 0.781 (p=0.015). The services interaction is -0.383 (p=0.38), which is not significant.
