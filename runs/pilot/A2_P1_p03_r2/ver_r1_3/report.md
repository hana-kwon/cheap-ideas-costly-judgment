# Effect of supplier diversification on export growth

**Conclusion: positive effect (modest).** Preferred estimate (OLS, HC1 robust SEs, n=2000, controls for all pre-period characteristics): a 1 SD increase in supplier diversity is associated with **+0.69 points** of 2023 export growth (SE 0.240, p = 0.0038, 95% CI 0.22 to 1.16). Export growth has mean about 100.

This is observational cross-section data, so the estimate is causal only if the 2020 controls remove all confounding. Unobserved confounders could still bias it.

## Choices that matter
- The naive raw estimate (2.55) is about 3.7 times larger than the adjusted one. Most of it comes from confounding by firm size, export experience and past export growth. I do not rely on it.
- `buyer_rating_2023` is measured in 2023, after the treatment period (2021-22), and correlates strongly with both diversity and growth. It is a likely mediator or collider. Controlling for it flips the sign to -2.12. That estimate is a post-treatment-conditioning artefact, so I excluded it from the preferred model. I report it below for transparency.
- The PI hoped for a positive result. The positive result here comes from the pre-specified adjustment set (pre-period covariates only), not from picking among specifications. The one specification that would show a different result is the one I consider invalid.

## All specifications estimated (coefficient on supplier_diversity; 5 in total)
| # | Specification | Coef | SE (HC1) | p |
|---|---|---|---|---|
| 1 | Raw bivariate | 2.553 | 0.246 | 3e-25 |
| 2 | + log_sales, years_exporting, export_growth_2020 | 0.691 | 0.240 | 0.0040 |
| 3 (preferred) | + all pre-period controls (region, listed, product group, inventory, foreign-owned, import share, port distance, ISO, debt) | 0.693 | 0.240 | 0.0038 |
| 4 | #3 + buyer_rating_2023 (post-treatment; not valid) | -2.121 | 0.233 | 8e-20 |
| 5 | #3 + diversity × log_sales interaction (main-effect coefficient at mean sales) | 0.690 | 0.239 | 0.0039 |
