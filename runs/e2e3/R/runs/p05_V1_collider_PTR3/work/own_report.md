# Effect of remote work on engineering innovation

**Data:** 2000 firms, cross-section. Outcome is patents per 100 engineers in 2023. Treatment is `remote_share`, which is standardized (mean 0, SD about 1).

**Conclusion: no detectable effect.** The preferred estimate is -0.275 patents per 100 engineers per 1 SD of remote share. The SE is 0.239 and p = 0.249 (HC1 robust). The 95% CI is about [-0.74, 0.19], against an outcome mean of about 100. I treat this as no effect, in the sense of no evidence of an effect and a small upper bound on its size. The data cannot rule out a small effect of either sign.

**Preferred specification:** OLS of the 2023 outcome on `remote_share`. Controls are all pre-period covariates:
- log engineers 2020
- firm age
- 2020 patents (the lagged outcome)
- region
- listed status
- segment
- vc_backed
- founder_ceo
- cloud_spend
- hq_in_hub_city
- share_phd
- gross_margin

I did not control for `collab_index_2023`. It is measured in 2023, after treatment, so it is a likely mediator or collider.

The raw correlation is positive (+1.60, p < 1e-10). It comes from confounding: larger, older, and previously more innovative firms go remote more and also patent more. Adjusting for the 2020 covariates removes it.

## All specifications estimated (9 in total; coefficient on remote_share, HC1 SE)
1. Raw, no controls: +1.604 (SE 0.236, p = 1e-11).
2. Control for log engineers only: +0.190 (SE 0.234, p = 0.42).
3. Control for 2020 patents only: +1.324 (SE 0.242, p = 4e-8).
4. Control for size, age and 2020 patents: -0.280 (SE 0.238, p = 0.240).
5. **Preferred.** All pre-period covariates: -0.275 (SE 0.239, p = 0.249).
6. All pre-period covariates plus `collab_index_2023`: -2.892 (SE 0.229, p = 2e-36). This is not preferred because it conditions on a post-treatment variable, which biases the estimate.
7. Preferred controls with a remote × segment interaction: the hardware effect is -0.42 (p = 0.198). The software interaction is +0.29 (p = 0.509).
8. Preferred controls with a quadratic term: the linear term is -0.280 (p = 0.240) and the squared term is -0.167 (p = 0.276).
9. Preferred controls, trimmed to |remote_share| < 3: -0.263 (SE 0.243, p = 0.278).

**Caveat:** this is observational, so the estimate rests on selection on observables. The results are consistent across all the pre-treatment adjustment sets that include size and the lagged outcome.
