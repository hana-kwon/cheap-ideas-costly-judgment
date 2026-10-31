# Effect of remote work on engineering innovation

**Conclusion: no detectable effect.** The raw positive association is confounded by firm size and age. Once pre-period characteristics are controlled, the estimate is small, negative and not significant.

**Preferred estimate:** OLS of patents per 100 engineers (2023) on remote_share. It controls for all pre-period covariates: log engineers, firm age, 2020 patents, vc_backed, founder_ceo, cloud spend, hub HQ, PhD share, gross margin, listed, region and segment. Standard errors are HC1 robust.
- Coefficient: -0.275 patents per 100 engineers per 1 SD of remote share.
- Standard error: 0.239.
- p-value: 0.249.
- 95% CI: about [-0.74, 0.19].
- N = 2000.

The outcome has mean about 100. The CI excludes the raw +1.6 association.

The PI hoped for a positive effect. The data do not support one once confounding is handled.

## Specifications estimated (all OLS, HC1 SEs, outcome = patents_per_100_eng_2023)
1. Raw, remote_share only: +1.604 (SE 0.236), p=1e-11. Confounded and not preferred.
2. Plus log engineers and firm age: -0.197 (SE 0.236), p=0.404.
3. Plus 2020 patents only: +1.324 (SE 0.242), p=4e-8. Omits size and age.
4. **Full pre-period controls (preferred):** -0.275 (SE 0.239), p=0.249.
5. Full controls plus collab_index_2023: -2.89 (SE 0.229), p=2e-36. Not valid. collab_index_2023 is a post-treatment variable, probably a mediator or collider (remote_share raises it with coefficient 0.60, p<1e-90). Conditioning on it induces bias, so I discard this spec.
6. Full controls plus a quadratic in remote_share: linear term -0.280 (SE 0.238), p=0.240. No evidence of non-linearity.
7. Full controls with a remote_share x segment interaction: remote_share main effect (hardware) -0.421 (SE 0.327), p=0.198. Interaction +0.291 (SE 0.440), p=0.509. No heterogeneity.
8. Auxiliary: collab_index_2023 on remote_share with full controls: +0.597, p<1e-90. This is not an effect on innovation.

Total models estimated: 8.

## Caveats
This is a cross-section with observational variation in remote_share. Unobserved confounding is possible. The adjusted estimate is imprecise enough to rule out only effects larger than about +0.2 patents per 100 engineers per SD.
