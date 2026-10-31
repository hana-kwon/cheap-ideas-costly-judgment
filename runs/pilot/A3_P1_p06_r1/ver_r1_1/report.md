# Effect of supplier diversification on export growth

**Conclusion: no detectable effect.** This does not support the PI's hypothesis.

**Preferred estimate:** OLS of export_growth_2023 on supplier_diversity, controlling for all pre-period covariates (log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign-owned, imported input share, port distance, ISO certification, debt ratio). HC1 robust standard errors, n=2000.
- Coefficient: 0.051 (SE 0.247), p = 0.836. The 95% CI is roughly [-0.43, 0.54] index points per SD of diversity.

## All specifications estimated (5)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw bivariate | 1.782 | 0.255 | 2.7e-12 |
| 2 | + log sales, years exporting, 2020 export growth | 0.057 | 0.246 | 0.817 |
| 3 | Full pre-period controls (preferred) | 0.051 | 0.247 | 0.836 |
| 4 | Full controls + buyer_rating_2023 | -2.412 | 0.228 | 3e-26 |
| 5 | Full controls + quadratic in diversity (linear term) | 0.056 | 0.246 | 0.819 |

## Notes
- The raw positive association (spec 1) is confounding. Larger, more experienced firms with higher past export growth have more suppliers and also grow more. Once these pre-period variables are controlled, the effect is about 0.
- buyer_rating_2023 is measured after the treatment (2023). It is plausibly an outcome of diversity or a collider, so it is a bad control. Spec 4's significant negative coefficient is a conditioning artifact, and I do not interpret it as causal. I excluded it from the preferred model.
- The design is cross-sectional and observational. Unobserved confounding is still possible, so the estimate is not proven causal. The data give no support for a positive effect.
- I did not tabulate the quadratic term in spec 5, so I can't say whether it is significant.
