# Effect of supplier diversification on export growth

**Conclusion: no detectable effect once pre-period confounders are controlled.** The PI's hypothesis of a positive effect is not supported.

Preferred estimate: OLS of export_growth_2023 on supplier_diversity, controlling for all 2020 pre-period covariates (log sales, years exporting, 2020 export growth, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio, listed) plus region and product-group fixed effects. HC1 robust SEs, N=2000.

- Coefficient: 0.051 (per 1 SD of supplier diversity, in export-growth index points)
- SE: 0.247, p = 0.836, 95% CI [-0.43, 0.54]

The naive bivariate slope is 1.78 (p<1e-11). It collapses to about 0.05 after adjusting for pre-period firm characteristics, mainly size (log sales), firm age, and prior export growth. That means the raw association is confounded. This is consistent with larger and more established firms having both more suppliers and higher growth.

buyer_rating_2023 is measured after the treatment and is plausibly an outcome or mediator of diversity. I treat it as a bad control and did not include it in the preferred model. Including it gives -2.41 (p<1e-25), which is a collider/mediator-induced artifact and should not be interpreted causally.

## All specifications estimated (6; all OLS, HC1 SEs, N=2000)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Naive: bivariate | 1.782 | 0.255 | 2.7e-12 |
| 2 | + pre-period covariates | 0.070 | 0.248 | 0.776 |
| 3 | + pre-period covariates + region and product-group FE (preferred) | 0.051 | 0.247 | 0.836 |
| 4 | Spec 3 + buyer_rating_2023 (post-treatment bad control; not preferred) | -2.412 | 0.228 | 3e-26 |
| 5 | Minimal: log_sales, export_growth_2020 only | 0.422 | 0.244 | 0.084 |
| 6 | Spec 3 + quadratic term in diversity (linear term shown) | 0.056 | 0.246 | 0.819 |

Caveats: this is a cross-section, so unobserved confounding remains possible. The CI rules out effects larger than about 0.5 index points per SD.
