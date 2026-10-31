# Effect of supplier diversification on export growth

**Conclusion: no effect** (after adjusting for pre-period confounders). The preferred estimate is +0.051 points of 2023 export growth (percent index) per 1 SD of supplier diversity. The SE is 0.247 (HC1 robust) and p = 0.84. The 95% CI is roughly [-0.43, +0.54].

## Preferred specification
OLS of export_growth_2023 on supplier_diversity plus all 2020 pre-period covariates: log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign ownership, share of imported inputs, port distance, ISO certification and debt ratio. SEs are HC1.

The unadjusted association is positive and significant (1.78, SE 0.25). It disappears once firm size, export tenure and prior growth are controlled. Those variables drive both diversification and growth. This indicates the raw correlation is confounding.

buyer_rating_2023 is measured after the treatment and is plausibly a mediator or collider. I do not control for it. Including it gives a negative coefficient (-2.41), which I regard as bias.

## All specifications estimated (7)
Coefficients are on supplier_diversity.

1. Raw bivariate OLS: 1.782 (SE 0.255, p<0.001)
2. Core controls (log sales, tenure, past growth): 0.057 (SE 0.246, p=0.82)
3. **Full pre-period controls (preferred): 0.051 (SE 0.247, p=0.84)**
4. Full controls plus buyer_rating_2023 (post-treatment, not preferred): -2.412 (SE 0.228, p<0.001)
5. Bivariate plus buyer_rating_2023 (not preferred): -1.577 (SE 0.231, p<0.001)
6. Full controls plus a quadratic term in diversity: linear term 0.056 (SE 0.246, p=0.82)
7. Full controls plus a diversity x product-group interaction: durables effect 0.273 (SE 0.337, p=0.42). The interaction term is -0.459 (SE 0.462, p=0.32).

## Caveats
This is cross-sectional observational data. Only observed pre-period confounders are adjusted for. The null is conditional on those controls being sufficient.
