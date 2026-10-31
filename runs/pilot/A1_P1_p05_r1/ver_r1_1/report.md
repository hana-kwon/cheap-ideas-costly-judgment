# Effect of remote work on engineering innovation

**Conclusion: no detectable effect.** The PI expected a positive effect. The data do not support one once pre-period confounders are controlled.

**Preferred estimate** (OLS, HC3 robust SE, n=2000): outcome is patents per 100 engineers in 2023, regressed on remote_share plus all pre-2020 controls (log engineers, firm age, 2020 patents, vc_backed, founder_ceo, cloud spend, hub HQ, PhD share, gross margin, region, listed, segment).
- Coefficient on remote_share: **-0.275** patents per 100 engineers per 1 SD of remote share
- SE: **0.240**
- p-value: **0.251**
- 95% CI: [-0.745, 0.195]

**Why this specification:** the raw positive association is driven by confounding. Larger and older firms, and firms with higher prior patenting, are both more remote and more innovative. The pre-period covariates handle this. collab_index_2023 is measured after treatment and is a likely mediator or collider, so I did not control for it in the preferred model.

## All specifications estimated (7)
Coefficients are on remote_share; SEs are HC3.

| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw bivariate | 1.604 | 0.236 | 1e-11 |
| 2 | + 2020 patents (lagged outcome) only | 1.324 | 0.242 | 5e-8 |
| 3 | **Full pre-period controls (preferred)** | -0.275 | 0.240 | 0.251 |
| 4 | Full controls + collab_index_2023 (post-treatment, not preferred) | -2.892 | 0.230 | 4e-36 |
| 5 | Full controls + quadratic in remote_share | -0.280 (linear term) | 0.239 | 0.243 |
| 6 | Full controls, remote_share x segment (main effect = hardware) | -0.421 | 0.329 | 0.201 |
| 7 | log(outcome), full controls | -0.0026 | 0.0024 | 0.291 |

## Caveats
- Cross-sectional observational data, so the estimate rests on selection on the observed pre-period covariates. Unobserved confounding is still possible.
- Specification 4 is shown for transparency only. Conditioning on a post-treatment variable that correlates strongly with remote_share (r=0.51) and with the outcome (r=0.54) induces bias, which is why the coefficient there is so negative.
- The unadjusted positive result (specs 1-2) should not be read as causal.
- The confidence interval excludes effects larger than about +0.2 patents per 100 engineers per SD of remote share. The outcome mean is about 100, so any effect is small.
