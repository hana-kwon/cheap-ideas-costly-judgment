# Effect of remote work on engineering innovation

**Conclusion: no detectable effect.** Once firm size and age are controlled for, the association between remote share and 2023 patents per 100 engineers is small, negative and not statistically distinguishable from zero.

**Preferred estimate:** OLS of patents_per_100_eng_2023 on remote_share plus all pre-treatment (2020) covariates: log engineers, age, lagged patents, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd, gross_margin, listed, region and segment. HC3 robust SEs.
- Coefficient: -0.275 patents per 100 engineers per 1 SD of remote share
- SE: 0.240
- p-value: 0.251
- 95% CI: about [-0.75, +0.19]

## Reasoning
- The raw correlation is positive (+1.60, p<1e-10). It is confounded: larger and older firms patent more, and the adjusted estimates show this. Adding firm size and age (with or without lagged patents) moves the estimate to about -0.28.
- `collab_index_2023` is measured after treatment, so it is a potential mediator or collider. Controlling for it gives a strongly negative estimate (-2.89), which I regard as post-treatment bias and do not use. The assumption is that the estimate is causal only if the pre-treatment controls remove all confounding. This is observational cross-section data, so unobserved confounding remains possible.

## All specifications estimated (outcome = patents_per_100_eng_2023; HC3 SEs)
1. Raw bivariate: 1.604 (SE 0.236), p=1e-11
2. + lagged patents 2020: 1.324 (0.242), p=5e-8
3. + lagged patents, log engineers, age: -0.280 (0.239), p=0.241
4. **Full pre-treatment controls (preferred): -0.275 (0.240), p=0.251**
5. Full controls + collab_index_2023 (post-treatment, not preferred): -2.892 (0.230), p=4e-36
6. remote_share + collab_index_2023 only (not preferred): -1.918 (0.230), p=7e-17
7. Full controls + quadratic in remote_share (linear term): -0.280 (0.239), p=0.243
8. Full controls + interactions with lagged patents and segment: main-effect coefficient -0.422 (0.329), p=0.200. Both interactions are insignificant (lagged-patents interaction 0.090, p=0.67; segment interaction 0.292, p=0.51).
9. Full controls, trimmed to |remote_share|<3: -0.263 (0.244), p=0.281
10. Auxiliary: collab_index_2023 regressed on remote_share with full controls: coefficient 0.597. This is not an effect on the outcome, so I did not use it in the headline estimate and gave it no SE here.

Total: 10 regressions.
