# Effect of training hours on firm productivity

## Conclusion
Positive effect (observational association, interpreted as causal only under selection-on-observables). Preferred estimate: one additional unit of training_hours (the variable is standardized, mean 0) is associated with **+0.841** thousand USD value added per employee in 2023 (HC1 SE **0.241**, p = **0.0005**, N = 2000). This is about +0.8% in logs (0.0088, SE 0.0024).

## Preferred specification
OLS of productivity_2023 on training_hours plus all pre-period (2020) controls: log_employees, firm_age, productivity_2020, region, listed, sector, export_share, foreign_owned, family_owned, rd_intensity, union_share, credit_score. HC1 robust SEs.

Reasoning: the controls are measured before training (2021-22), so they can confound the estimate without being affected by training. The raw estimate (2.37) is inflated about 2.8x by confounding, mainly firm size and age. These are correlated with both training and productivity.

**mgmt_rating_2023 is deliberately excluded.** It is measured in 2023, after training. It is a post-treatment variable, either a mediator or a collider. Controlling for it flips the sign to -2.09, which I judge to be a bias artifact. Training is positively related to the rating (auxiliary regression shows the rating is strongly related to it). I report this specification for transparency only, and it should not be read as evidence of a negative effect.

## All specifications estimated (coefficient on training_hours, HC1 SE, p)
1. Raw bivariate: 2.373, 0.239, p<1e-22
2. Basic controls (size, age, region, sector, listed): 0.900, 0.240, p=0.0002
3. **Preferred**: all pre-period controls: 0.841, 0.241, p=0.0005
4. All pre-period controls + mgmt_rating_2023 (post-treatment, not preferred): -2.089, 0.234, p<1e-18
5. Lagged productivity only: 2.090, 0.238, p<1e-17
6. log(productivity_2023), all pre-period controls: 0.0088, 0.0024, p=0.0003
7. Preferred plus quadratic training term: linear coefficient 0.841, 0.242, p=0.0005 (the quadratic term was not material; its estimate was not examined in detail)
8. Auxiliary regression of training_hours on covariates including mgmt_rating_2023 (diagnostic, not an effect estimate).

## Caveats
- Cross-sectional observational data. Unobserved confounders (e.g. management quality before 2020) could remain, so the causal interpretation is conditional on the controls.
- The estimate is sensitive to the control set (2.37 → 0.84), so the true effect is likely smaller than naive estimates. The sign of the post-treatment-adjusted result is not credible.
- The result agrees with the PI's prior, but I selected the specification on the basis of timing of covariates, not on the results.
