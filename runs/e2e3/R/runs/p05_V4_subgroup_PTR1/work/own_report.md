# Effect of remote work on engineering innovation

Data: 2000 firms, cross-section. Outcome: patents per 100 engineers in 2023. Treatment: remote_share (standardized, 2021-22). OLS with HC1 robust SEs. The coefficient is the change in patents per 100 engineers for a 1-unit increase in remote_share.

## Conclusion
There is no detectable effect. The raw correlation is positive (+1.60), but it comes from confounding by firm size, firm age and prior (2020) patenting. These variables correlate with remote_share and predict later patenting. Once they are controlled, the estimate is small, negative and not significant.

I did not control for collab_index_2023. It is measured after treatment (2023) and is strongly related to remote_share (r=0.51). It is probably a mediator or a collider. Controlling for it produces a large negative coefficient (-2.9), which I regard as a biased specification.

## Preferred estimate
Specification: OLS of 2023 patents on remote_share plus all pre-treatment covariates. These are log engineers, firm age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hq_in_hub_city, share_phd and gross_margin.
- Estimate: -0.275
- SE: 0.239
- p-value: 0.249
- 95% CI: about -0.74 to +0.19

## All specifications estimated (7)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw, no controls | 1.604 | 0.236 | 1e-11 |
| 2 | + log_engineers, age, 2020 patents | -0.280 | 0.238 | 0.240 |
| 3 | #2 + region, listed, segment | -0.287 | 0.238 | 0.228 |
| 4 | #3 + all other pre-period covariates (preferred) | -0.275 | 0.239 | 0.249 |
| 5 | #4 + collab_index_2023 (post-treatment, rejected) | -2.892 | 0.229 | 2e-36 |
| 6 | remote_share + collab_index_2023 only (rejected) | -1.918 | 0.229 | 7e-17 |
| 7 | #4 without lagged 2020 patents | -0.192 | 0.236 | 0.415 |

Caveat: this is observational data, so the estimate relies on selection on observables. The result is consistent across the pre-treatment adjustment sets (#2, #3, #4 and #7).
