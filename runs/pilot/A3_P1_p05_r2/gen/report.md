# Effect of remote work on engineering innovation

**Conclusion:** No detectable effect. This does not support the PI's hypothesis that remote work raises innovation.

**Preferred estimate:** OLS of patents per 100 engineers (2023) on remote_share. It controls for all pre-period (2020) covariates: log engineers, age, lagged patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd, gross_margin. Standard errors are HC1 robust, N=2000.
- Coefficient: -0.275 patents per 100 engineers per 1 unit of remote_share. The variable is standardized, so a unit is about 1 SD.
- SE: 0.239
- p-value: 0.249
- 95% CI: about [-0.74, 0.19]

## Why the raw association is misleading
- The raw association is positive and significant (1.60, SE 0.236, p≈1e-11).
- Larger and older firms are both more remote (remote_share regressed on the covariates: log_engineers 0.33, age 0.17) and more innovative. This is confounding.
- Adding size and age alone removes the effect (-0.20, p=0.40).
- Adding lagged patents alone leaves 1.32. Lagged patents are only weakly related to remote_share, so they do not remove the size and age confounding.
- collab_index_2023 is measured after treatment, and remote_share strongly predicts it (0.60, p<1e-90). It is a mediator or collider, so I did not use it as a control. Including it gives -2.89, which is biased and not interpretable as the total effect.
- Remote_share was not randomized, so the estimate rests on selection-on-observables. Unobserved confounding remains possible.

## All specifications estimated (10)
Outcome is patents_per_100_eng_2023 unless stated. All use HC1 robust standard errors.

| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw, no controls | 1.604 | 0.236 | 1e-11 |
| 2 | + log_engineers, age | -0.197 | 0.236 | 0.404 |
| 3 | + lagged patents only | 1.324 | 0.242 | 4e-8 |
| 4 | **Full pre-period controls (preferred)** | **-0.275** | **0.239** | **0.249** |
| 5 | Full controls + collab_index_2023 (post-treatment, biased) | -2.892 | 0.229 | 2e-36 |
| 6 | collab_index_2023 only (post-treatment, biased) | -1.918 | 0.229 | 7e-17 |
| 7 | Full controls + remote_share² | linear term -0.280, p=0.240; quadratic term -0.167, p=0.276 | | |
| 8 | Full controls + remote_share × segment | remote_share main effect -0.421, p=0.198; software interaction 0.291, p=0.509 | | |
| 9 | Log outcome, full controls | -0.0026 | 0.0024 | 0.289 |
| 10 | Mediator check: collab_index_2023 as outcome, full controls | 0.597 | n/a | <1e-90 |

I also ran a diagnostic regression of remote_share on the covariates. I did not count it as an effect specification.
