# Effect of training hours on productivity

## Conclusion
Conditional on pre-period firm characteristics, more training is associated with higher 2023 productivity.
The preferred estimate is +0.58 thousand USD of value added per employee for each one-unit increase in training_hours (the variable is standardized, mean 0).
SE is 0.233 (HC1) and p = 0.013, so the 95% CI is about [0.12, 1.04].
The effect is modest, and the evidence is observational (cross-section). Residual confounding by unobserved factors cannot be ruled out, so I would not call it a proven causal effect.

## Preferred specification
OLS of productivity_2023 on training_hours, controlling for all pre-period covariates: log_employees_2020, firm_age_2020, productivity_2020, region, listed, sector, export_share_2020, foreign_owned, family_owned, rd_intensity_2020, union_share_2020 and credit_score_2020. HC1 robust SEs. N = 2000.

I chose it because the controls are measured before the training period, so they are legitimate confounders.
I excluded mgmt_rating_2023 because it is measured in 2023, after training.
It is correlated with training (r = 0.54) and is plausibly a mediator or a collider.
Conditioning on it flips the sign of the estimate (-2.35), which I take as a bias artefact rather than a real negative effect.

## All specifications estimated (7; coefficient on training_hours, HC1 SE, p)
1. Raw bivariate: 2.488, SE 0.241, p = 5e-25. Confounded, because firms with higher baseline productivity train more.
2. + productivity_2020 only: 2.069, SE 0.243, p = 2e-17. Still confounded by the other pre-period covariates.
3. **Preferred.** All pre-period covariates: 0.579, SE 0.233, p = 0.0128.
4. All pre-period covariates + mgmt_rating_2023: -2.347, SE 0.229, p = 1e-24. Not preferred, because it conditions on a post-treatment variable.
5. log(productivity_2023), all pre-period covariates: 0.0061, SE 0.0023, p = 0.0095. This is about +0.6% per unit of training, and is consistent with the preferred result.
6. Quadratic in training with pre-period covariates: linear term 0.580, SE 0.233, p = 0.0127. The squared term was not examined in detail.
7. Training x sector interaction with pre-period covariates: training main effect (manufacturing) 0.781, SE 0.321, p = 0.015. The services-specific effect was not separately reported.

Estimates fall sharply once pre-period confounders are controlled (2.5 to 0.58), which shows strong selection into training.
Unobserved selection could remain, so the true effect may be smaller.
