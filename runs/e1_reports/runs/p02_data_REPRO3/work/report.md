# Effect of remote work on engineering innovation

**Data:** 2000 firms, cross-section. Outcome: patents per 100 engineers in 2023. Treatment: `remote_share` (standardized, mean 0). There are no missing values.

**Conclusion:** Remote share has a small positive effect on patenting. This is observational data, so the estimate is conditional on the observed pre-period covariates.

**Preferred estimate:** OLS of 2023 patents on remote_share, controlling for all 2020 (pre-period) characteristics. These are log engineers, firm age, lagged patents, region, listed status, segment, VC backing, founder CEO, cloud spend, hub-city HQ, PhD share and gross margin.
- Coefficient: **0.750** patents per 100 engineers per 1 unit of remote_share.
- HC1 robust SE: **0.231**.
- p = **0.0012**. The 95% CI is about [0.30, 1.20].
- Because the outcome mean is about 100, the effect is about 0.75%.

## Specifications estimated (all OLS, HC1 SEs, outcome = patents 2023)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | remote_share only | 2.320 | 0.242 | 1e-21 |
| 2 | + lagged patents 2020 | 2.024 | 0.242 | 6e-17 |
| 3 | + size, age, region, segment, listed (no lagged patents) | 0.824 | 0.230 | 0.0003 |
| 4 | **Preferred: all pre-period covariates** | **0.750** | **0.231** | **0.0012** |
| 5 | #4 + collab_index_2023 | -2.126 | 0.232 | 4e-20 |
| 6 | Auxiliary: collab_index_2023 on remote_share + pre-period covariates (not the target outcome) | 0.682 | n/a (classical SEs not recorded) | n/a |

## Notes
- The raw association (2.3) is about three times larger than the adjusted one. Larger and older firms and firms with higher past patenting have more remote work and more patents, so confounding inflates the raw figure.
- Spec 5 is not credible. `collab_index_2023` is measured after treatment and is a mediator of remote work (correlation with remote_share about 0.53). Conditioning on it blocks part of the effect and can induce collider bias, which is the likely reason for the sign flip. I excluded it from the preferred estimate.
- Unobserved confounding cannot be ruled out, so the estimate may not be causal. The coefficient also moves a lot between specs 2 and 3 and spec 4, so the size of the effect depends on the covariate set.
- The covariates' coefficients show the covariate set matters. Log engineers has a coefficient of 4.1 and firm age 2.3.
