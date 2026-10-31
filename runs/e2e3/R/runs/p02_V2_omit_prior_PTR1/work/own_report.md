# Effect of remote work on engineering innovation

**Conclusion: positive effect.** Preferred estimate: a 1-unit increase in remote_share raises patents per 100 engineers (2023) by **0.75** (HC1 SE 0.231, p = 0.0012, n = 2000). remote_share is standardized (mean 0). The outcome has a mean of about 100.

## Approach
This is a cross-section, and remote_share is not randomly assigned. It correlates with firm size (log_engineers_2020), firm age, and 2020 patenting. The naive estimate (2.32) is therefore confounded. Adjusting for the pre-period covariates cuts it to about 0.75. This identification rests on selection on observables, so unmeasured confounding remains possible.

I did NOT adjust for collab_index_2023. It is measured after treatment and is plausibly a mediator of remote work. It is strongly affected by remote_share (coef 0.68). Controlling for it flips the sign to -2.13, which is a post-treatment-conditioning artifact and not a valid total effect.

## Specifications estimated (outcome = patents_per_100_eng_2023; OLS, HC1 SEs; coefficient on remote_share)
1. Naive, no controls: 2.320 (SE 0.242, p = 1e-21)
2. + lagged patents 2020: 2.024 (0.242, p = 6e-17)
3. + lagged patents, log engineers, firm age: 0.753 (0.233, p = 0.0012)
4. **Preferred**: all pre-period covariates (lagged patents, size, age, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hub city, PhD share, gross margin): **0.750 (0.231, p = 0.0012)**
5. Same as 4 without lagged patents: 0.826 (0.231, p = 0.0003)
6. Same as 4 + collab_index_2023 (post-treatment, rejected): -2.126 (0.232, p = 4e-20)
7. Same as 4 + quadratic term: linear term 0.745 (p = 0.0013); squared term 0.093 (p = 0.52), so there is no evidence of nonlinearity
8. Same as 4 with a remote × segment interaction: remote effect for hardware 0.706 (p = 0.020); software differential 0.093 (p = 0.83), so there is no heterogeneity

Auxiliary regressions, not effect estimates: collab_index on remote_share plus controls (0.68, p = 1e-130), and remote_share on covariates. Eight effect specifications in total.

Caveat: the result depends on the selection-on-observables assumption. The effect is modest, about 0.75 patents per 100 engineers per SD of remote share.
