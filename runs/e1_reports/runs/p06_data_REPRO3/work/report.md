# Effect of supplier diversification on export growth

**Conclusion: no effect.** After adjusting for pre-period firm characteristics, supplier_diversity has no detectable association with export_growth_2023.

**Preferred estimate:** OLS of export_growth_2023 on supplier_diversity, controlling for the 2020 pre-period covariates (log sales, years exporting, 2020 export growth, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio), region, listed status and product group. Robust HC1 standard errors, N=2000.
- Coefficient: 0.051 per 1 SD of supplier diversity
- SE: 0.247
- p-value: 0.836
- 95% CI: about [-0.43, 0.54]

The outcome has mean about 100 and the CI is narrow, so large effects are ruled out.

## Specifications estimated (7; SE is HC1; the first six are all OLS on N=2000)
1. Raw bivariate: 1.782 (SE 0.255), p<0.001. This is confounded: diversity correlates with firm size, experience and past growth.
2. + pre-period controls (log sales, years exporting, 2020 export growth): 0.057 (SE 0.246), p=0.82.
3. + region, listed, product group: 0.038 (SE 0.246), p=0.88.
4. Full pre-treatment controls (preferred): 0.051 (SE 0.247), p=0.84.
5. Full controls + buyer_rating_2023: -2.412 (SE 0.228), p<0.001. **Not preferred.** buyer_rating_2023 is measured after treatment and is highly correlated with diversity (r=0.49). It is likely a mediator or collider, so conditioning on it induces bias.
6. Full controls + squares of log sales and 2020 export growth: 0.051 (SE 0.247), p=0.84.
7. Preferred model with the outcome winsorized at 1% and 99%: 0.035 (SE 0.242), p=0.88.

I also ran the preferred model with standard errors clustered on region, which has only 3 clusters. I did not record or count that result because it is unreliable.

## Caveats
This is a cross-section, so the estimate is causal only under selection on observables. The raw positive association comes entirely from confounding by the 2020 covariates. Unobserved confounders could still matter.
