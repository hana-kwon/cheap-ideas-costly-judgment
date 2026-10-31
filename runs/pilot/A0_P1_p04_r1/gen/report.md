# Effect of training hours on firm productivity

## Conclusion
Training hours are positively associated with 2023 productivity after adjusting for pre-period firm characteristics. The preferred estimate is +0.84 thousand USD of value added per employee for each 1-unit increase in training_hours (SE 0.241, p = 0.0005). training_hours is centred at 0 and appears standardized, so one unit is probably about 1 SD. The mean productivity level is about 101. The data are cross-sectional and observational, so this is an adjusted association. It supports a causal reading only if the 2020 controls capture all confounding.

## Preferred specification
OLS of productivity_2023 on training_hours. Controls: log_employees_2020, firm_age_2020, productivity_2020, region, listed, sector, export_share_2020, foreign_owned, family_owned, rd_intensity_2020, union_share_2020 and credit_score_2020. HC1 robust SEs, N = 2000.

- Estimate: 0.841
- SE: 0.241
- p-value: 0.00049

The controls are all pre-treatment (2020). Larger, older, higher-productivity firms train more, so the unadjusted estimate is inflated by confounding. The adjusted estimate is about 65% smaller than the naive one.

I excluded mgmt_rating_2023 from the preferred model. It is measured in 2023, after training, and is strongly correlated with training (r = 0.52). That makes it a likely mediator or collider, and conditioning on it is bad control. Adding it flips the training coefficient to -2.09. I do not interpret that as a real negative effect. It is a post-treatment conditioning artifact.

## All specifications estimated (7 in total; all OLS, HC1 SEs, N = 2000)
| # | Specification | Coef on training_hours | SE | p |
|---|---|---|---|---|
| 1 | Naive: productivity_2023 ~ training | 2.373 | 0.239 | 2.7e-23 |
| 2 | + productivity_2020 | 2.090 | 0.238 | 1.9e-18 |
| 3 | **Preferred**: all pre-period controls, including productivity_2020 | **0.841** | **0.241** | **0.00049** |
| 4 | Same as 3 but without productivity_2020 | 0.905 | 0.240 | 0.00016 |
| 5 | Same as 3 + mgmt_rating_2023 (post-treatment, not recommended) | -2.089 | 0.234 | 3.9e-19 |
| 6 | log(productivity_2023) with the controls from 3 | 0.0088 (about 0.9% per unit) | 0.0024 | 0.00028 |
| 7 | Same as 3 + training_hours squared (linear term shown) | 0.841 | 0.242 | 0.0005 |

The estimate is positive and significant in every specification except #5. The size depends heavily on the controls, so the unadjusted figures of 2.1 to 2.4 should not be used. Unmeasured confounding could remain.
