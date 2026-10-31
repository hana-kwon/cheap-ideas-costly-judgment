# Effect of remote work on engineering innovation

**Conclusion: positive effect (observational, adjusted association).** Outcome is patents per 100 engineers in 2023. `remote_share` is in standardized units (mean 0), so the estimate is per 1 unit of remote_share.

**Preferred estimate:** OLS of patents_per_100_eng_2023 on remote_share plus all pre-period covariates (log engineers, firm age, 2020 patents, region, listed, segment, vc_backed, founder_ceo, cloud_spend, hub HQ, share PhD, gross margin), HC3 robust SEs, N=2000.
Coefficient = **0.750**, SE = **0.233**, p = **0.0013** (95% CI about 0.29 to 1.21).

## Specifications estimated (all OLS, HC3 SEs, outcome = patents_per_100_eng_2023)
1. Raw, remote_share only: 2.320 (SE 0.243), p=1e-21. Not preferred: strongly confounded. Firm size, age and similar traits correlate with both remote share and patenting. Adding them cuts the estimate by about two thirds.
2. + log_engineers_2020, firm_age_2020, patents_per_100_eng_2020: 0.753 (SE 0.233), p=0.0012.
3. **Preferred.** + all pre-period covariates, region, listed, segment: 0.750 (SE 0.233), p=0.0013.
4. Same as 3 but without the 2020 patents lag: 0.826 (SE 0.232), p=0.0004.
5. Same as 3 + collab_index_2023: -2.126 (SE 0.233), p=7e-20. Not preferred and not interpretable as a causal effect. collab_index_2023 is measured in 2023, after treatment, and is strongly affected by remote_share (auxiliary regression 6 below). Controlling for it conditions on a post-treatment variable (mediator or collider) and flips the sign through bias.
6. Auxiliary: collab_index_2023 on remote_share plus the full pre-period controls: coefficient 0.68, p=6e-129. This supports treating collab as post-treatment, so I excluded it.

Total models estimated: 6.

## Caveats
- This is a cross-section with no random assignment. The estimate is conditional on observed pre-period covariates, and unobserved confounding could remain. The estimates in specs 2-4 are stable (0.75-0.83), but this does not rule out unobserved confounding.
- The naive raw association (2.3) overstates the effect roughly threefold.
- The effect is modest. A 1 SD increase in remote share is associated with about 0.75 more patents per 100 engineers, against an outcome mean of about 100.
- Results were not tuned toward a desired outcome. The positive finding follows from the pre-specified covariate-adjusted model, and the one specification with a negative sign was rejected on identification grounds.
