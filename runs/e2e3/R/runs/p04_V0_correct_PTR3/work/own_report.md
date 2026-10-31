# Effect of training hours on firm productivity

**Conclusion: positive effect.** Preferred estimate: one more average annual training hour per employee is associated with +0.84 thousand USD of 2023 value added per employee. The standard error is 0.241 (HC1 robust), p = 0.0005, and N = 2000. Training hours are standardized (mean 0), so the unit is one unit of the variable's scale (not necessarily one standard deviation). The effect is about 0.8% of mean productivity (mean about 101).

## Preferred specification
OLS of productivity_2023 on training_hours. Controls are all pre-period covariates: productivity_2020, log_employees_2020, firm_age_2020, region, listed, sector, export_share_2020, foreign_owned, family_owned, rd_intensity_2020, union_share_2020 and credit_score_2020. Standard errors are HC1.

I deliberately did **not** control for mgmt_rating_2023. It is measured in 2023, after training, and it is strongly related to training (corr 0.52). It is therefore a likely mediator or collider. Conditioning on it flips the estimate to -2.09, which I take to be a post-treatment-bias artifact.

## All specifications estimated
The training coefficient and HC1 SE for each of the seven outcome regressions:

| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive: no controls | 2.373 | 0.239 | <0.001 |
| 2 | Core controls: productivity_2020, size, age, region, listed, sector | 0.837 | 0.241 | 0.0005 |
| 3 | **Preferred**: all pre-period controls | 0.841 | 0.241 | 0.0005 |
| 4 | All pre-period controls plus mgmt_rating_2023 (post-treatment, not preferred) | -2.089 | 0.234 | <0.001 |
| 5 | log(productivity_2023), all pre-period controls | 0.0088 (about 0.9%) | 0.0024 | 0.0003 |
| 6 | Quadratic in training, all pre-period controls (linear term) | 0.841 | 0.242 | 0.0005 |
| 7 | Training × sector interaction (the training coefficient is the manufacturing effect) | 1.349 | 0.313 | <0.001 |

I also ran one auxiliary regression of training_hours on the covariates and mgmt_rating_2023, to check how the rating relates to training. It is not an effect estimate, so I left it out of the count.

## Caveats
- This is a cross-section with non-random training, so the estimate is causal only if the pre-period controls remove all confounding. The naive estimate is almost three times larger than the adjusted one, which shows that selection is substantial.
- Adjusting for lagged productivity and the other pre-period covariates cuts the estimate sharply. The specifications with pre-period controls agree closely (0.84), but unobserved confounding remains possible.
- The sector interaction suggests the effect differs by sector. I did not estimate the services effect directly, so the sector heterogeneity is not characterised.
