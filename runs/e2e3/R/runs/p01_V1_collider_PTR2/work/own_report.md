# Effect of training hours on productivity

**Conclusion: positive effect (modest).** Preferred estimate: OLS of productivity_2023 (thousand USD per employee) on training_hours, controlling for all pre-period (2020) covariates, region, sector and listed status, with HC1 robust SEs. N=2000.
Estimate = **0.579** (SE 0.233, p = 0.0128; 95% CI 0.12 to 1.04) thousand USD per 1 unit of training_hours. training_hours is standardized, so the unit is one SD.

Reasoning: training is not randomly assigned. Larger, older and previously more productive firms train more, so the naive estimate (2.49) is inflated about 4x by confounding. Adjusting for the 2020 covariates gives 0.58. mgmt_rating_2023 was measured after training (2023). It is a post-treatment variable, either a mediator or a collider. I therefore did not control for it in the preferred model. Including it flips the sign to -2.35, which I think is a bias artifact, not a real effect. The result relies on selection on observables, so unobserved confounding could remain. The estimate is modest, and its significance is not strong across all choices.

## Specifications estimated (all OLS, HC1 SEs, outcome productivity_2023 unless noted; coefficient on training_hours)
1. Naive, no controls: 2.488 (SE 0.241, p<1e-24)
2. + log_employees_2020, firm_age_2020: 0.721 (SE 0.233, p=0.002)
3. + productivity_2020 only: 2.069 (SE 0.243, p<1e-16)
4. **Preferred**: all pre-period controls + region + listed + sector: 0.579 (SE 0.233, p=0.0128)
5. Spec 4 + mgmt_rating_2023 (post-treatment, not preferred): -2.347 (SE 0.229, p<1e-23)
6. Spec 4 with log(productivity_2023) as outcome: 0.0061 (SE 0.0023, p=0.0095), roughly 0.6% per SD
7. Spec 4 + quadratic training term: linear coefficient 0.5795 (SE 0.233, p=0.0127); the quadratic term was not material

Total: 7 specifications.
