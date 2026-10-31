# Effect of supplier diversification on export growth

**Conclusion: positive effect (modest).** Preferred estimate: +0.693 export-growth index points per 1 SD of supplier_diversity, HC1 SE 0.240, p = 0.0038 (95% CI 0.22 to 1.16). The mean of the outcome is about 100.5.

Preferred specification: OLS of export_growth_2023 on supplier_diversity plus all pre-period controls: log sales, years exporting, 2020 export growth, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio, listed, region and product group. Standard errors are HC1 robust, N = 2000.

## Why this specification
The naive estimate is confounded: larger, more experienced firms have more suppliers and also grow faster. Adjusting for pre-period covariates cuts the estimate to about a quarter of the naive value. The estimate is identical across the adjusted specifications that exclude buyer_rating_2023 (0.69). buyer_rating_2023 is measured in 2023, the same period as the outcome. It correlates 0.54 with supplier diversity, so it is probably affected by diversity and is a post-treatment variable. Controlling for it would bias the estimate, so I excluded it. Including it flips the sign, which I judge to be a bad-control artifact.

The data are a cross-section, so the effect is identified only under selection on observables. Unmeasured confounding is possible, and the estimate should be read as an adjusted association with a causal interpretation conditional on that assumption.

## All specifications estimated (5)
| # | Specification | Coef | SE (HC1) | p |
|---|---|---|---|---|
| 1 | Naive: diversity only | 2.553 | 0.246 | 3e-25 |
| 2 | **Preferred: + all pre-period controls, region, product group** | **0.693** | **0.240** | **0.0038** |
| 3 | Preferred controls + buyer_rating_2023 (bad control, not preferred) | -2.121 | 0.233 | 8e-20 |
| 4 | Basic controls: log sales, years exporting, 2020 export growth | 0.691 | 0.240 | 0.0040 |
| 5 | Preferred controls + squared diversity term (linear coef shown) | 0.694 | 0.240 | 0.0038 |
