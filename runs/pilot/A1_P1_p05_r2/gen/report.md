# Effect of remote work on engineering innovation

## Conclusion
No detectable effect. The raw positive association (+1.60 patents per 100 engineers per 1 SD of remote share) is confounding. Larger and older firms do more remote work and also patent more. Once pre-period (2020) firm characteristics are controlled, the estimate is small, negative and statistically insignificant. This does not support the PI's hypothesis that more remote work raises innovation.

## Preferred estimate
OLS of patents_per_100_eng_2023 on remote_share, controlling for all 2020 pre-period covariates: log engineers, age, lagged patents, VC-backed, founder CEO, cloud spend, HQ in hub city, PhD share, gross margin, listed, region and segment. HC1 robust SEs, N=2000.
- Coefficient on remote_share: **-0.275**
- SE: **0.239**
- p-value: **0.249**
- 95% CI: about [-0.74, 0.19]. The CI excludes the naive +1.6.

Caveat: this is a cross-section with observational data. It identifies a causal effect only if the 2020 covariates capture all confounding.

## Why collab_index_2023 is not controlled
collab_index_2023 is measured in 2023, after the remote-work period. It is plausibly an outcome of remote work (remote_share predicts it strongly, coefficient 0.60, p<1e-80) and a correlate of innovation. Conditioning on it is a post-treatment adjustment and gives a spuriously large negative coefficient (-2.89). I report those specifications but do not prefer them.

## All specifications estimated (remote_share coefficient, HC1 SE, p)
1. Naive, no controls: 1.604, SE 0.236, p=1e-11
2. + log engineers, firm age: -0.197, SE 0.236, p=0.404
3. + lagged patents only: 1.324, SE 0.242, p=4e-8
4. **Full pre-period controls (preferred): -0.275, SE 0.239, p=0.249**
5. Full pre-period controls + collab_index_2023 (post-treatment, rejected): -2.892, SE 0.229, p=2e-36
6. remote_share + collab_index_2023 only (rejected): -1.918, SE 0.229, p=7e-17
7. Full pre-period controls + quadratic term in remote_share: linear term -0.280, SE 0.238, p=0.240
8. Full pre-period controls with remote_share x segment interaction: remote_share (hardware) -0.421, p=0.198; interaction with software +0.291, p=0.509
9. Mediator/diagnostic regression of collab_index_2023 on remote_share and pre-period controls: 0.597, p<1e-80. This is not an effect on innovation.

Also run as a diagnostic (not an effect estimate): remote_share regressed on the covariates, which showed that size, age and lagged patents predict it.

Total: 8 specifications for the effect on innovation, plus 1 diagnostic regression, so 9 estimated in all.
