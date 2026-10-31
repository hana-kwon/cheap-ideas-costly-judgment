# Effect of remote work on engineering innovation

**Data**: 2000 firms, cross-section. Outcome: patents per 100 engineers in 2023. Treatment: remote_share (2021-22, mean 0, standardized-looking). Estimates use OLS with HC1 robust SEs.

## Preferred estimate
OLS of patents_per_100_eng_2023 on remote_share, controlling for all pre-period covariates: log engineers, firm age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud spend, HQ in hub city, PhD share, gross margin.

- Estimate: **0.750** patents per 100 engineers per 1-unit increase in remote_share
- SE: 0.231 (HC1), p = 0.0012

The conclusion is a positive effect. It rests on selection-on-observables only. Remote share is related to firm size, age and prior patenting, so unobserved confounding cannot be excluded. The raw estimate (2.32) is about three times larger because of that confounding.

## Why I did not control for collab_index_2023
The 2023 collaboration index is measured after treatment. Remote share raises it by 0.68 (p<1e-100), so it is plausibly a mediator or collider. Adding it flips the remote coefficient to -2.13. That coefficient is not a total effect, and I do not use it. The result is sensitive to this choice, which is the main caveat.

## All specifications estimated (remote_share coefficient on 2023 patents unless noted)
1. Raw bivariate: 2.320, SE 0.242, p=1e-21
2. Basic controls (size, age, 2020 patents): 0.753, SE 0.233, p=0.0012
3. **Full pre-period controls (preferred)**: 0.750, SE 0.231, p=0.0012
4. Full controls + collab_index_2023 (post-treatment, not preferred): -2.126, SE 0.232, p=4e-20
5. Full controls + remote x region interactions (main-effect coefficient for the baseline region only): 0.869, SE 0.385, p=0.024
6. Full controls + quadratic term in remote_share (linear coefficient): 0.745, SE 0.231, p=0.0013
7. Full controls, trimmed at the 1st/99th percentile of remote_share: 0.825, SE 0.251, p=0.0010
8. Mediator check: collab_index_2023 on remote_share with full controls: 0.682, p=3e-130

Also run, as a diagnostic and not an effect estimate: a regression of remote_share on the covariates.
The PI hoped for a positive result. The preferred specification gives one, but I chose it on the grounds above and not because of the sign.
