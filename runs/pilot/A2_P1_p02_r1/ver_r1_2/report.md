# Remote work and engineering innovation

**Conclusion: positive effect (modest).** Preferred estimate: +0.75 patents per 100 engineers (2023) per 1-unit increase in remote_share. remote_share is on a standardized scale, so 1 unit is about 1 SD. The robust (HC1) SE is 0.23 and p = 0.0012 (95% CI 0.30 to 1.20). The outcome has mean about 100.

This is an observational cross-section. The estimate is causal only if the observed pre-period controls capture all confounding. I did not tune specifications to reach the PI's hoped-for result. The PI's prior played no role in choosing the preferred specification.

## Preferred specification
OLS of patents_per_100_eng_2023 on remote_share. Controls are all pre-period (2020) covariates: log engineers, firm age, lagged patents, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd, gross_margin, listed, region and segment. SEs are HC1.

Why these controls:
- remote_share is strongly related to firm size, age and prior patenting (t about 10, 8 and 4). The naive estimate is therefore confounded and about 3 times too large.
- collab_index_2023 is measured after treatment. It is plausibly a mediator or collider, so I did not control for it in the preferred model.

## All specifications estimated (coefficient on remote_share; HC1 SE; p)
1. Naive, no controls: 2.32 (0.242); p = 1e-21. Confounded.
2. Controls for size and age: 0.83 (0.232); p = 0.0004.
3. Controls for lagged patents only: 2.02 (0.242); p = 6e-17.
4. **Full pre-period controls (preferred): 0.75 (0.2315); p = 0.0012.**
5. Full pre-period controls plus collab_index_2023: -2.13 (0.232); p = 4e-20. I do not trust this one. Conditioning on a post-treatment variable gives a sign reversal and is not a valid total effect.
6. remote_share plus collab_index_2023 only: -1.41 (0.243); p = 7e-9. Same problem as 5.
7. Preferred model with the top and bottom 1% of remote_share trimmed: 0.82 (0.251); p = 0.0010.
8. Preferred model plus a quadratic term in remote_share: linear term 0.74 (p = 0.0013); quadratic term 0.093 (p = 0.52). There is no evidence of nonlinearity.
9. Auxiliary regression of collab_index_2023 on remote_share plus full controls: coefficient 0.68. Remote work is associated with higher collaboration scores, so collaboration is a plausible mediator.

Total: 9 regressions estimated.

## Caveats
- Specifications 5 and 6 point the other way. I judge them invalid, but they show the result depends on that modelling choice.
- Unobserved confounding is still possible. Remote share was not randomly assigned, and the estimate fell sharply once controls were added, which suggests selection matters.
- The effect is small relative to the outcome's mean of about 100.
