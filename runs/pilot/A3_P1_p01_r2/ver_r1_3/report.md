# Effect of training hours on productivity

## Conclusion
After adjusting for pre-treatment firm characteristics, more training is associated with higher 2023 productivity. The estimate is modest in size and statistically significant. It is positive, but it is much smaller than the naive estimate. It rests on a selection-on-observables assumption, so it is not a guaranteed causal effect.

**Preferred estimate:** OLS of productivity_2023 on training_hours, controlling for all pre-period covariates (2020 productivity, log employees, age, region, sector, listed, export share, foreign, family, R&D, union, credit score). HC1 robust standard errors.
- Coefficient: 0.579 thousand USD of value added per employee per one-unit increase in training_hours. The variable is centered with an SD of about 1, so this is roughly per SD.
- SE = 0.233, p = 0.0128, 95% CI [0.12, 1.04].

## Why this specification
- Training is not randomly assigned. Larger, older and previously more productive firms train more. The naive estimate (2.49) is therefore inflated by confounding, and adjusting for pre-period covariates cuts it by about 77%.
- **mgmt_rating_2023 is excluded.** It is measured in 2023, after the training period. It correlates strongly with training (0.54) and with productivity (0.57), so it is plausibly a mediator or a consequence of both. Controlling for it flips the sign to -2.35. That is a bad-control or collider artefact and should not be interpreted as a negative effect.
- The remaining caveat is unobserved confounding, such as management quality or firm strategy. The positive result could still be biased in either direction.

## All specifications estimated (8; HC1 SEs; coefficient on training_hours)
| # | Spec | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive: no controls | 2.488 | 0.241 | 4.8e-25 |
| 2 | **All pre-period controls (preferred)** | 0.579 | 0.233 | 0.0128 |
| 3 | Basic controls (log emp, age, sector, region) | 0.692 | 0.231 | 0.0028 |
| 4 | Lagged productivity only | 2.069 | 0.243 | 1.7e-17 |
| 5 | Pre controls + mgmt_rating_2023 (post-treatment; rejected) | -2.347 | 0.229 | 1.0e-24 |
| 6 | log(productivity) with pre controls | 0.0061 (about 0.6%) | 0.0023 | 0.0095 |
| 7 | Pre controls + quadratic in training (linear term) | 0.580 | 0.233 | 0.0127 |
| 8 | Pre controls + training x sector (training main effect, manufacturing) | 0.781 | 0.321 | 0.0149 |

Specs 2, 3 and 6 to 8 agree on a small positive effect. Spec 5 is the only negative one, and I reject it on design grounds. No other specifications were run.
