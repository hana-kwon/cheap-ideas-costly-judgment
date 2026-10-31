# Effect of remote work on engineering innovation

**Conclusion: positive effect.** Preferred estimate: +0.75 patents per 100 engineers per 1-unit (about 1 SD) increase in remote_share. SE 0.2315 (HC1 robust), p = 0.0012, n = 2000.

This is observational cross-section data. The estimate is causal only if the pre-2021 controls capture all confounding. Raw and thinly controlled estimates are 2–3 times larger, so selection into remote work looks positive. Larger, older firms with higher past patenting are more remote. The estimate may still be biased by unobserved confounders.

## Preferred specification
OLS of patents_per_100_eng_2023 on remote_share plus all pre-period covariates, with HC1 standard errors. The covariates are log_engineers_2020, firm_age_2020, patents_per_100_eng_2020, region, listed, segment, vc_backed, founder_ceo, cloud_spend_2020, hq_in_hub_city, share_phd_2020 and gross_margin_2020.

I excluded collab_index_2023 as a control. It is measured in 2023, after the treatment, and is plausibly a mediator or a collider. Remote share strongly predicts it (coefficient 0.68, p<1e-100). Controlling for it flips the remote coefficient to -2.13. That reflects post-treatment conditioning bias, not a real negative effect. I report it for transparency only.

## All specifications estimated (outcome = patents_per_100_eng_2023, coefficient on remote_share, HC1 SE)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw, no controls | 2.320 | 0.242 | 1e-21 |
| 2 | + log_engineers, firm_age | 0.829 | 0.232 | 0.00035 |
| 3 | + lagged patents only | 2.024 | 0.242 | 6e-17 |
| 4 | + size, age, lag, region, segment, listed | 0.749 | 0.231 | 0.0012 |
| 5 | **Full pre-period controls (preferred)** | **0.750** | **0.2315** | **0.0012** |
| 6 | Full pre-period controls + collab_index_2023 (post-treatment, not preferred) | -2.126 | 0.232 | 4e-20 |
| 7 | Full controls without lagged patents | 0.826 | 0.231 | 0.00034 |

Two auxiliary regressions were also run. The first was collab_index_2023 on remote_share plus controls (coefficient 0.68). The second was remote_share on the pre-period covariates, as a diagnostic of selection. That makes 9 regressions in total.

Every specification that excludes the post-treatment variable gives a positive, significant coefficient. The range is 0.75 to 2.3, and the better-controlled ones are about 0.75–0.83.
