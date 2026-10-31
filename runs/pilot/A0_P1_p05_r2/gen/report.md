# Effect of remote work on engineering innovation

Outcome: patents per 100 engineers in 2023 (mean 100.5, SD 10.9). Treatment: `remote_share` (standardized, mean 0, per 1 unit). N = 2000 firms, cross-section, no missing data. All standard errors are HC1 robust.

## Conclusion
The data do not support the hypothesis that more remote work raises innovation. The raw correlation is strongly positive (+1.60, p<1e-10). It disappears once I control for pre-period firm characteristics, mainly firm size, age and prior patenting. Remote share is correlated with those variables: firms that are larger, older and more patent-intensive in 2020 have higher remote share. Those same variables predict 2023 patenting. Adjusted for them, the estimate is -0.28 patents per 100 engineers per SD of remote share (SE 0.239, p = 0.249). The 95% CI is about [-0.74, +0.19], so any effect is small, under about 0.2 patents per 100 engineers (under 2% of an outcome SD) on the positive side. I read this as **no effect**. This is observational data, so a causal reading also relies on the assumption that the controls capture all confounding.

## Preferred specification
OLS of 2023 patents on remote_share plus all pre-period controls: log engineers 2020, firm age, 2020 patents, region, listed, segment, VC-backed, founder CEO, cloud spend, HQ in hub city, PhD share and gross margin.
Estimate -0.275, SE 0.239, p = 0.249.

I did not control for `collab_index_2023`. It is measured after treatment and is plausibly a mediator or collider, so conditioning on it would bias the estimate. The specification below that does include it is shown only for transparency.

## All specifications estimated (coefficient on remote_share)
1. Raw bivariate OLS: +1.604, SE 0.236, p = 1.1e-11. Confounded and not preferred.
2. Plus the three core pre-period controls (log engineers, age, 2020 patents): -0.280, SE 0.238, p = 0.240.
3. Full pre-period controls (preferred): -0.275, SE 0.239, p = 0.249.
4. Full controls plus `collab_index_2023`: -2.892, SE 0.229, p = 1.8e-36. Not preferred, because it conditions on a post-treatment variable and the result is likely an artifact.
5. Full controls with a remote_share × segment interaction: main effect (hardware) -0.421, SE 0.327, p = 0.198.
6. Log outcome, full controls: -0.0026 (about -0.26%), SE 0.0024, p = 0.289.
7. Quadratic in remote_share, full controls: linear term -0.280 (p = 0.240), squared term -0.167 (p = 0.276). There is no evidence of nonlinearity.

Total: 7 specifications estimated. I also ran a diagnostic regression of remote_share on the covariates, which I don't count as an effect specification.
