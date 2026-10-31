# Effect of remote work on engineering innovation

**Conclusion: positive effect (modest).** Outcome: patents per 100 engineers in 2023. Treatment: remote_share (standardized, SD≈1). Data are a cross-section of 2000 firms, with no missing values. Remote share was not randomized, so the estimate rests on selection-on-observables.

**Preferred estimate:** OLS of 2023 patents per 100 engineers on remote_share, controlling for all pre-period covariates: log engineers, firm age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd and gross_margin. Standard errors are HC1 robust.
- Coefficient: **0.750 patents per 100 engineers per 1 SD of remote share** (about 0.07 SD of the outcome).
- SE: 0.231
- p-value: 0.0012
- 95% CI: 0.30 to 1.20

**Why this specification.** Remote share is correlated with firm size, age and prior patenting, which also predict the outcome. The naive estimate is therefore inflated (2.32), and adjustment cuts it by about two thirds. I did not control for collab_index_2023. It is measured in 2023, after treatment, so it is a likely mediator or collider. Controlling for it flips the sign to -2.13, which is not a valid total effect.

## All specifications estimated (9)
All are OLS with HC1 standard errors. Coefficients are on remote_share.

| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive, no controls | 2.320 | 0.242 | 1e-21 |
| 2 | Controls: size, age, region, listed, segment | 0.824 | 0.230 | 0.0003 |
| 3 | Control for 2020 patents only | 2.024 | 0.242 | 6e-17 |
| 4 | **Full pre-period controls (preferred)** | **0.750** | **0.231** | **0.0012** |
| 5 | Full controls + collab_index_2023 (post-treatment, rejected) | -2.126 | 0.232 | 4e-20 |
| 6 | Full controls without the 2020 patents lag | 0.826 | 0.231 | 0.0003 |
| 7 | Full controls + remote_share squared | linear term 0.745 (p=0.0013); quadratic 0.093 (p=0.52) | | |
| 8 | Full controls + remote_share×segment | 0.706 for hardware (p=0.020); interaction 0.093 (p=0.83) | | |
| 9 | Full controls, trimming remote_share outside the 1st–99th percentile | 0.825 | 0.251 | 0.0010 |

The adjusted estimates in specifications 2, 4, 6 and 9 are stable at about 0.7–0.8. There is no evidence of nonlinearity or of heterogeneity by segment.

**Caveats.** Unobserved confounding could still bias the estimate. The estimate is small relative to the outcome's SD of 11.3.
