# Effect of remote work on engineering innovation

**Conclusion: positive effect (observational; a causal reading depends on selection on observables).**

Preferred specification: OLS of patents per 100 engineers (2023) on remote_share, controlling for all pre-period covariates (log engineers, firm age, 2020 patents per 100 engineers, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd, gross_margin). HC1 robust SEs, N=2000.

**Estimate: 0.750 patents per 100 engineers per 1-unit increase in remote_share (remote_share is standardized, so this is per SD). SE 0.231, p = 0.0012.** The 95% CI is about 0.30 to 1.20. The outcome has mean about 100.

## Specifications estimated (outcome patents_per_100_eng_2023, remote_share coefficient)
1. Raw, no controls: 2.32 (SE 0.242, p≈1e-21). This is confounded: larger, older and more innovative firms have more remote work.
2. Controls: log engineers, age, 2020 patents: 0.753 (SE 0.233, p=0.0012).
3. **Preferred.** All pre-period controls: 0.750 (SE 0.231, p=0.0012).
4. All pre-period controls plus collab_index_2023: -2.13 (SE 0.232, p≈4e-20). Not preferred. Collaboration is measured in 2023, after treatment, and is strongly affected by remote_share (coefficient 0.68). It is a post-treatment variable, so conditioning on it biases the estimate. The sign flip is an artifact of this.
5. All pre-period controls without the 2020 patents lag: 0.826 (SE 0.231, p=0.0003).
6. Quadratic in remote_share, all pre-period controls: linear term 0.745 (SE 0.231, p=0.0013).
7. Interaction with segment, all pre-period controls: hardware effect 0.706 (SE 0.304, p=0.020). The software interaction is 0.093 (p=0.83), so there is no evidence of heterogeneity.
8. Auxiliary: collab_index_2023 on remote_share with controls: 0.68 (p≈1e-130). This is a mediator check, not an effect estimate.
9. Auxiliary: remote_share on covariates (balance check). Remote share is related to size, age and prior patenting, which supports adjusting for them.

Total regressions estimated: 9.

## Caveats
The data are a cross-section, and treatment is not randomized. Unobserved confounders could remain. The raw correlation overstates the effect by roughly 3x. The adjusted effect is modest (about 0.75 patents per 100 engineers per SD of remote share, against a mean of about 100) but is statistically robust across the reasonable pre-period specifications (0.75–0.83). The conclusion does not rest on the PI's expectation. The positive result is what the data gave under the sound specifications. The one specification that gives a negative estimate conditions on a post-treatment variable and is rejected for that reason.
