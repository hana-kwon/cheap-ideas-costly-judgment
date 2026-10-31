# Effect of training hours on productivity

**Conclusion: positive effect, modest in size.** The preferred estimate is +0.58 thousand USD of value added per employee in 2023, per 1-unit increase in training hours. Training hours are standardized, with mean 0 and SD about 1, so this is per 1 SD. The standard error is 0.233 (HC1 robust) and p = 0.013. The 95% CI is about [0.12, 1.04]. The mean of productivity is 100.6 and its SD is 11.4, so the effect is about 0.05 SD of productivity.

**Preferred specification:** OLS of productivity_2023 on training_hours plus all pre-period (2020) controls. These are log employees, firm age, 2020 productivity, region, listed, sector, export share, foreign-owned, family-owned, R&D intensity, union share and credit score. Standard errors are HC1 robust.

## Why this specification
- Training is not randomly assigned. It correlates with firm size (0.30), age (0.20) and prior productivity (0.21), so the raw association (2.49) is mostly confounding. Adding the pre-period controls cuts the estimate by about 77%.
- mgmt_rating_2023 was measured in 2023, after the training period. It is correlated 0.54 with training, so it is plausibly affected by training (a mediator or collider). Controlling for it flips the sign to -2.35. I treat that as a bad-control artifact and did not prefer it.
- This is a cross-section, so the estimate is causal only if the selection-on-observables assumption holds. Unobserved confounders could remain, and the estimate is best read as an upper-bound-ish conditional association.

## All specifications estimated (coefficient on training_hours, HC1 SE, n=2000)
1. Raw bivariate OLS: 2.488 (SE 0.241), p<0.001
2. Plus productivity_2020: 2.069 (SE 0.243), p<0.001
3. **Plus all pre-period controls (preferred): 0.579 (SE 0.233), p=0.0128**
4. Pre-period controls plus mgmt_rating_2023 (post-treatment, not preferred): -2.347 (SE 0.229), p<0.001
5. log(productivity_2023) as the outcome, pre-period controls: 0.0061 (SE 0.0023), p=0.0095, about +0.6% per SD
6. Pre-period controls plus a quadratic in training: linear term 0.580 (SE 0.233), p=0.0127. The quadratic term was not examined separately, so there is no clear evidence of nonlinearity.
7. Pre-period controls plus training x sector interaction: training main effect (manufacturing) 0.781 (SE 0.321), p=0.015. The services effect was not separately reported.

7 specifications were estimated. The preferred model was also re-run to print its full summary, which is not counted as a separate specification.
