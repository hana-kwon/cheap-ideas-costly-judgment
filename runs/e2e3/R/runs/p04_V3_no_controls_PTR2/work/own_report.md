# Effect of training hours on firm productivity

**Conclusion: positive effect.** Preferred estimate: +0.84 thousand USD of value added per employee (2023) per one-unit increase in training_hours. Training_hours is standardized, so one unit is about one SD. HC1 robust SE = 0.241, p = 0.0005, 95% CI [0.37, 1.31].

Preferred specification: OLS of productivity_2023 on training_hours, controlling for all pre-period (2020) covariates. These are log employees, firm age, productivity_2020, export share, foreign-owned, family-owned, R&D intensity, union share, credit score, region, listed and sector.

The data are cross-sectional and observational. The estimate is causal only under selection on observables. Controlling for pre-period variables roughly cuts the raw association by 65%, so selection into training is strong. Larger, older and more productive firms train more. Unobserved confounding may remain.

I did not control for mgmt_rating_2023. It is measured after the training period and is strongly related to training (a regression of it on training gives a coefficient of 0.63). It is therefore a likely mediator or collider. Conditioning on it flips the sign of the training coefficient to -2.09, which I take to be a bias artifact and not a real effect.

## All specifications estimated (training_hours coefficient, HC1 SE)
1. Raw bivariate: 2.373 (0.239), p<0.001
2. Plus productivity_2020 only: 2.090 (0.238), p<0.001
3. **Plus all pre-period controls (preferred): 0.841 (0.241), p=0.0005**
4. All pre-period controls plus mgmt_rating_2023 (post-treatment, rejected): -2.089 (0.234), p<0.001
5. log(productivity_2023), all pre-period controls: 0.0088 (0.0024), p=0.0003 (about 0.9% per SD)
6. Pre-period controls plus a quadratic term in training: linear coefficient 0.841 (0.242), p=0.0005
7. Training plus mgmt_rating_2023 only (rejected): -1.394 (0.238), p<0.001
8. Training × sector interaction with pre-period controls: training main effect (manufacturing) 1.349 (0.313), p<0.001. The services effect differs. I did not report its separate estimate.
9. Auxiliary regression, mgmt_rating_2023 on training with pre-period controls: 0.628. This is a diagnostic and not an effect estimate.
