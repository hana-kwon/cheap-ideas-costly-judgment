# Effect of training hours on productivity

**Conclusion: positive effect, modest in size.** Preferred estimate: +0.58 thousand USD of 2023 value added per employee for each additional unit of training_hours (training_hours is standardized, mean 0). The robust (HC1) standard error is 0.233 and p = 0.013. The 95% CI is about [0.12, 1.04].

## Preferred specification
OLS of productivity_2023 on training_hours, controlling for all pre-treatment (2020) covariates: lagged productivity, log employees, firm age, region, sector, listed, export share, foreign owned, family owned, R&D intensity, union share and credit score.

I did not control for mgmt_rating_2023. It is measured in 2023, after training, so it is likely a mediator or a collider. It correlates 0.54 with training and 0.57 with productivity. Adding it flips the training coefficient to -2.35, which I take to be a bad-control artefact and not a real negative effect.

## Caveats
- This is observational data. Training is strongly predicted by firm size, age and prior productivity, which is selection on observables.
- The naive estimate (2.49) is about four times the adjusted one. Controlling for observables removes most of the association, so unobserved confounding could plausibly remove more.
- The result is causal only if there is no remaining confounding.

## All specifications estimated (outcome productivity_2023 unless noted; HC1 SEs)
1. Naive, training only: 2.488 (SE 0.241), p < 0.001.
2. Plus productivity_2020: 2.069 (SE 0.243), p < 0.001.
3. Plus size, age, region, sector, listed, and lagged productivity: 0.567 (SE 0.232), p = 0.015.
4. **Full pre-treatment controls (preferred): 0.579 (SE 0.233), p = 0.013.**
5. Full pre-treatment controls plus mgmt_rating_2023 (rejected as a bad control): -2.347 (SE 0.229), p < 0.001.
6. Full controls plus a quadratic term in training: linear coefficient 0.580 (SE 0.233), p = 0.013. I did not look at the quadratic term itself.
7. Log outcome, full controls: 0.0061 (SE 0.0023), p = 0.0095. This is about 0.6% per unit of training.
8. Full controls without lagged productivity: 0.709 (SE 0.233), p = 0.002.

I also ran a descriptive regression of training on the controls and a correlation table. These are not effect estimates. In total, 8 effect specifications.
