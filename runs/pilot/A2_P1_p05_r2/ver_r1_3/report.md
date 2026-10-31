# Effect of remote work on engineering innovation

## Conclusion
The data do not support the hypothesis that more remote work raises innovation. The raw positive association is explained by pre-2021 firm characteristics. After adjusting for them, the estimated effect is small, negative and statistically indistinguishable from zero.

**Preferred estimate:** a 1 SD increase in remote_share changes patents per 100 engineers (2023) by **-0.275** (HC1 SE 0.239, p = 0.249; 95% CI about -0.74 to +0.19). The outcome has SD 10.9, so the CI rules out effects larger than about 0.07 SD in either direction.

Preferred specification: OLS of 2023 patents per 100 engineers on remote_share. Controls are all pre-period covariates: log engineers, firm age, 2020 patents, vc_backed, founder_ceo, cloud spend, hub-city HQ, PhD share, gross margin, region, listed and segment. N = 2000.

I did not adjust for collab_index_2023 in the preferred model. It is measured in 2023, after the treatment period, and remote_share strongly predicts it (coef 0.60, p < 1e-90). That makes it a post-treatment variable (a mediator or collider), and controlling for it would bias the estimate. Specification 5 shows this: the coefficient becomes -2.89, an artifact of conditioning on it.

## All specifications estimated
The coefficient on remote_share is reported with HC1 robust SEs, outcome = patents_per_100_eng_2023.

| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive, no controls | 1.604 | 0.236 | 1e-11 |
| 2 | + log engineers, firm age | -0.197 | 0.236 | 0.404 |
| 3 | + 2020 patents only | 1.324 | 0.242 | 4e-8 |
| 4 | **Full pre-period controls (preferred)** | **-0.275** | **0.239** | **0.249** |
| 5 | Full controls + collab_index_2023 (post-treatment, not preferred) | -2.892 | 0.229 | 2e-36 |
| 6 | remote_share + collab_index_2023 only (not preferred) | -1.918 | 0.230 | 7e-17 |
| 7 | Full controls, remote × segment interaction | main effect (hardware) -0.421, p = 0.198; interaction (software) +0.291, p = 0.509 | | |
| 8 | Full controls, quadratic in remote_share | linear -0.280 (p = 0.240); squared -0.167 (p = 0.276) | | |
| 9 | Mediator check: collab_index_2023 on remote_share with full controls | 0.597 | | <1e-90 |

Specification 9 is not an effect on innovation. It was run only to diagnose collab_index_2023. That makes 9 regressions in total.

## Caveats
- This is a cross-section, so the estimate is causal only if the observed pre-period controls capture all confounding. Unobserved confounding could remain.
- The naive positive result (spec 1) was the one most favorable to the prior hypothesis. It is not robust: it disappears once firm size and age are controlled.
- Spec 3 stays positive because 2020 patents alone leaves size and age uncontrolled. Specs 2 and 4 show that size and age drive the raw association.
