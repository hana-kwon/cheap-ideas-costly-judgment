# Effect of remote work on engineering innovation

**Conclusion: positive effect.** Preferred estimate: a 1-unit increase in remote_share (the variable is centred, roughly SD scale) is associated with +0.750 patents per 100 engineers in 2023 (HC1 SE 0.231, p = 0.0012, n = 2000). The outcome has a mean of about 100.

**Preferred specification:** OLS of patents_per_100_eng_2023 on remote_share, controlling for all pre-period covariates (log engineers, age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd, gross_margin). Robust (HC1) standard errors.

Caveats:
- This is a cross-section with no random assignment. The estimate is causal only if the 2020 controls capture the confounding. Unobserved confounding remains possible.
- The effect is modest. The naive estimate (2.32) is about three times the adjusted one, so confounding by firm size, age and prior patenting is large.
- I did not choose the specification to favour the PI's expected result. I chose it on identification grounds, and it happens to agree in sign with that expectation.

## Why collab_index_2023 is not a control
collab_index_2023 is measured in 2023, after the remote-work period. Remote share strongly predicts it (coef 0.68, p < 1e-100). It is therefore a mediator or collider, not a pre-treatment confounder. Controlling for it gives -2.13, which is a biased "direct effect" that mixes in selection. I report it but do not use it.

## All specifications estimated (outcome = patents_per_100_eng_2023, coefficient on remote_share)
1. Naive bivariate OLS: 2.320, SE 0.242, p = 1e-21
2. Basic controls (size, age, 2020 patents): 0.753, SE 0.233, p = 0.0012
3. **Full pre-period controls (preferred): 0.750, SE 0.231, p = 0.0012**
4. Full pre-period controls without lagged 2020 patents: 0.826, SE 0.231, p = 0.0003
5. Full pre-period controls plus collab_index_2023 (post-treatment, not preferred): -2.126, SE 0.232, p = 4e-20
6. Full controls with remote_share x segment interaction: remote_share main effect (hardware) 0.706, SE 0.304, p = 0.020. Interaction with software 0.093, p = 0.83, so there is no heterogeneity by segment.
7. Auxiliary model, collab_index_2023 on remote_share with full controls: 0.682, p = 3e-130. This is a mechanism check, not an effect on innovation.

Seven models were estimated in total.
