# Effect of remote work on engineering innovation

**Conclusion: positive effect.** This is observational cross-section data, so the estimate is causal only under selection on observables.

Preferred estimate: OLS of patents per 100 engineers (2023) on remote_share. Controls are all pre-period covariates: log engineers, firm age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud spend, hub HQ, PhD share and gross margin. Standard errors are HC1 robust.
- Coefficient: **0.750 patents per 100 engineers per 1-unit increase in remote_share**. remote_share has mean 0 and SD of about 1.
- SE 0.231, p = 0.0012, N = 2000.

## Specifications estimated (8 outcome regressions)
1. Raw, no controls: 2.320 (SE 0.242, p<1e-20). This is heavily confounded: remote_share is correlated with firm size, age and prior patenting.
2. Basic controls (log engineers, age, 2020 patents): 0.753 (SE 0.233, p=0.0012).
3. Basic controls plus region, listed and segment: 0.749 (SE 0.231, p=0.0012).
4. Full pre-period controls (**preferred**): 0.750 (SE 0.231, p=0.0012).
5. Full controls without lagged 2020 patents: 0.826 (SE 0.231, p=0.0003).
6. Full controls plus collab_index_2023: -2.126 (SE 0.232, p<1e-19). **Not used.** The collaboration index is measured in 2023, after treatment. It is a mediator or collider, so conditioning on it is bad control, and it flips the sign. I don't interpret this as a negative effect.
7. Full controls plus remote_share × segment interaction: the remote_share main effect (hardware) is 0.706 (p=0.020). The software difference is 0.093 (p=0.83), so there is no evidence of heterogeneity.
8. Full controls plus a quadratic term: linear 0.745 (p=0.001), squared 0.093 (p=0.52), so no evidence of non-linearity.

I also ran an auxiliary regression of remote_share on the covariates, to check selection. It is not counted above. Remote share is higher in larger and older firms and in firms with higher past patenting.

## Caveats
- The data are a cross-section. Adjustment is only for observed pre-period covariates, and unobserved confounding is possible.
- The raw association (2.3) is about three times the adjusted one (0.75), which shows substantial selection on observables. Residual confounding could remain.
- The estimate supports the PI's hypothesis. The adjusted estimates in specifications 2 to 5 and 7 to 8 are consistent with each other. The one contrary specification (6) is excluded for the methodological reason given above. The analysis was not tuned to reach a particular result.
