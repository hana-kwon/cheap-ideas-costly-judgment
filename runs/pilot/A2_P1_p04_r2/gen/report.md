# Effect of training hours on productivity

**Conclusion: positive effect.** Preferred estimate (spec 2: OLS of productivity_2023 on training_hours plus all pre-period controls, HC1 robust SE): **0.841 thousand USD of value added per employee per additional unit of training_hours** (training_hours is standardized, so this is per 1 SD). SE 0.241, p = 0.0005, N = 2000, 95% CI [0.37, 1.31].

Caveat: this is a cross-section with no experimental or quasi-experimental variation. The estimate is causal only if the 2020 controls capture all confounding. Controlling for productivity_2020 is a strong check, because it removes the persistent firm-quality component. The naive estimate is almost 3 times larger than the adjusted one, so selection is substantial and unmeasured confounding could remain.

## Variable choice
mgmt_rating_2023 was measured in 2023, after the training period. It is strongly correlated with training (r = 0.52), and training raises it (coefficient about 0.63 on mgmt_rating_2023). It is therefore a mediator or collider, not a confounder. Controlling for it flips the sign (spec 3), so I treat that result as biased and do not prefer it. I report it for completeness.

## All specifications estimated (7; coefficient on training_hours, HC1 SE)
1. Naive, no controls: 2.373 (SE 0.239), p = 2.7e-23. Confounded by firm characteristics.
2. **Preferred.** All pre-period (2020) controls, region, sector and listed: 0.841 (0.241), p = 0.0005.
3. Spec 2 plus mgmt_rating_2023 (post-treatment, not valid): -2.089 (0.234), p = 3.9e-19.
4. Minimal controls (size, age, productivity_2020): 0.798 (0.241), p = 0.0009.
5. log(productivity_2023) as outcome, spec 2 controls: 0.0088 (0.0024), p = 0.0003, about 0.9% per SD.
6. Spec 2 plus quadratic training term: linear coefficient 0.841 (0.242), p = 0.0005. The nonlinearity is negligible.
7. Spec 2 with a training x sector interaction: training coefficient for manufacturing only is 1.349 (0.313), p = 1.6e-5. This is the baseline-sector effect, not the average effect, so it is not comparable with the others.

Among the valid specifications (all except 3), the estimate is positive and significant.
The adjusted estimates are 0.80–0.84 in the pooled linear models, so they are stable across controls.
