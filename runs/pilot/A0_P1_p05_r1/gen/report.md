# Effect of remote work on engineering innovation

**Data:** 2000 firms, cross-section. Outcome is patents per 100 engineers in 2023. Treatment is `remote_share` (standardized, mean 0). Standard errors are HC1 robust.

## Conclusion
After adjusting for pre-period firm characteristics, I find no evidence that remote work affects innovation. The preferred estimate is **-0.275 patents per 100 engineers per 1 unit of remote_share (SE 0.239, p = 0.249, 95% CI about -0.74 to +0.19)**. This does not support the hypothesis that more remote work raises innovation.

The raw association is positive (+1.60, SE 0.24, p < 1e-10). It is almost entirely confounding. Once 2020 firm size, age and baseline patenting are controlled, it disappears and turns slightly negative.

## Preferred specification
OLS of 2023 patents per 100 engineers on remote_share. Controls are all pre-period covariates: log engineers, age, 2020 patents, VC-backed, founder CEO, cloud spend, HQ in hub city, PhD share, gross margin, listed, region and segment.

I excluded `collab_index_2023`. It is measured in 2023, after treatment, so it is a likely mediator or collider. Controlling for it would bias the estimate. Spec 4 shows this: it gives -2.89, a spurious large negative effect.

This is observational data, so a causal reading relies on selection on observables.

## All specifications estimated (10)
Estimates are for remote_share unless noted.

| # | Specification | Estimate | SE | p |
|---|---|---|---|---|
| 1 | Raw, no controls | 1.604 | 0.236 | 1e-11 |
| 2 | + log engineers, age, 2020 patents | -0.280 | 0.238 | 0.240 |
| 3 | **+ all pre-period covariates, region, segment (preferred)** | **-0.275** | **0.239** | **0.249** |
| 4 | Spec 3 + collab_index_2023 (post-treatment; not preferred) | -2.892 | 0.229 | 2e-36 |
| 5 | Spec 3 without lagged patents | -0.192 | 0.236 | 0.415 |
| 6 | Spec 3 + remote_share² | -0.280 (linear term) | 0.238 | 0.240 |
| 7 | Spec 3 with remote_share × segment interaction | -0.423 (hardware); interaction +0.299, SE 0.443, p = 0.50 | 0.327 | 0.196 |
| 8 | Outcome = collab_index_2023, with spec 3 controls (diagnostic only) | 0.597 | 0.029 | – |
| 9 | Spec 3 with the top and bottom 1% of the outcome trimmed | -0.292 | 0.226 | 0.196 |
| 10 | Spec 3 with log outcome | -0.0026 | 0.0024 | 0.289 |

Spec 8 shows remote work is associated with higher collaboration scores. That is not an innovation outcome.
