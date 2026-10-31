# Effect of remote work on engineering innovation

**Conclusion: positive effect (observational data, so this is causal only under selection-on-observables).**
Preferred estimate: +0.750 patents per 100 engineers in 2023 per 1-unit increase in remote_share (remote_share is standardized, SD ~1), SE 0.2315 (HC1 robust), p = 0.0012, N = 2000.

Preferred specification: OLS of patents_per_100_eng_2023 on remote_share plus all pre-period covariates (log engineers, age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hq_in_hub, share_phd, gross_margin). I did not control for collab_index_2023. It is measured after the treatment, and remote_share strongly raises it (coef 0.68), so it is a mediator or collider. Adjusting for it flips the sign, which would be a bias artifact.

## Specifications estimated (9 in total; coefficient on remote_share, HC1 SE)
1. Raw bivariate: 2.320 (SE 0.242), p<1e-20. Confounded: larger, more remote firms are also more innovative.
2. + lagged patents 2020: 2.024 (0.242), p<1e-16.
3. + lagged patents, size, age: 0.753 (0.233), p=0.0012.
4. **Full pre-treatment controls (preferred): 0.750 (0.2315), p=0.0012.**
5. Full controls + collab_index_2023 (post-treatment, rejected): -2.126 (0.232), p<1e-19. Biased.
6. remote_share + collab_index_2023 only (rejected): -1.407 (0.243), p<1e-8. Biased.
7. Full controls with remote_share x segment interaction: main effect 0.706 (0.304), p=0.020. Interaction 0.093 (p=0.83), so no heterogeneity by segment.
8. Full controls with quadratic term: linear 0.745 (p=0.0013), squared 0.093 (p=0.52). No evidence of nonlinearity.
9. Auxiliary regression of collab_index_2023 on remote_share with full controls: 0.682, p<1e-100. This is not an outcome model for the effect, but it supports the mediator diagnosis.

## Caveats
- Cross-sectional observational data. Unobserved confounding is possible. The estimate fell sharply once size, age and lagged patents were added (from 2.3 to 0.75), so residual confounding could remain.
- The result reflects the specifications I chose. The positive sign is robust across all specifications that use only pre-treatment controls. The negative estimates come only from conditioning on the post-treatment collaboration index, which I consider invalid.
- The effect is modest: about 0.75 patents per 100 engineers, against an outcome mean of about 100.
