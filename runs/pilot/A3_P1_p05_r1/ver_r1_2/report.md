# Effect of remote work on engineering innovation

**Conclusion: no detectable effect.** This does not support the PI's hypothesis that more remote work raises innovation.

Preferred estimate: OLS of 2023 patents per 100 engineers on remote_share, controlling for all pre-period covariates. Robust (HC3) standard errors, N=2000.
- Coefficient on remote_share: **-0.275** patents per 100 engineers per 1 unit of remote_share (remote_share is standardized, mean 0).
- Standard error: **0.240**
- p-value: **0.251**
- 95% CI: [-0.745, 0.195]

## Reasoning
- The naive correlation is positive and strongly significant (+1.60, p<1e-10). It is confounded: larger and older firms, and firms with higher past patenting, have both more remote work and more patents.
- Adding firm size and age alone moves the coefficient to -0.20 (p=0.40). The full set of pre-period controls gives -0.275 (p=0.25).
- I treated collab_index_2023 as a post-treatment variable, a possible mediator or collider. Remote work is correlated with it, and it was measured in 2023 alongside the outcome. Controlling for it gives -2.89 (p<1e-35). That is a biased, over-controlled estimate, so I do not use it for the causal effect.
- This is cross-sectional observational data. Unobserved confounding cannot be ruled out, so the estimate is not a proven causal effect. Within the observed controls, the data are consistent with zero and with modest effects of either sign.

## All specifications estimated (9 in total; the outcome is patents_per_100_eng_2023 unless noted; all use HC3 SEs)
1. Naive, remote_share only: 1.604 (SE 0.236, p=1e-11)
2. + lagged patents 2020 only: 1.324 (SE 0.242, p=5e-8)
3. + log engineers and firm age: -0.197 (SE 0.236, p=0.405)
4. **Full pre-period controls (preferred)**: -0.275 (SE 0.240, p=0.251). Controls are size, age, lagged patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hub HQ, PhD share, gross margin.
5. Full controls + collab_index_2023 (post-treatment, not preferred): -2.892 (SE 0.230, p=4e-36)
6. collab_index_2023 only (not preferred): -1.918 (SE 0.230, p=7e-17)
7. Log outcome, full controls: -0.0026 (SE 0.0024, p=0.291)
8. Full controls + remote_share x segment interaction: main effect (hardware) -0.421 (SE 0.329, p=0.201); software interaction +0.291 (p=0.512)
9. Full controls + quadratic in remote_share: linear term -0.280 (p=0.243); quadratic term p=0.281

An auxiliary regression of remote_share on collab_index_2023 and the controls was run to check association. It is not counted as an effect specification.
