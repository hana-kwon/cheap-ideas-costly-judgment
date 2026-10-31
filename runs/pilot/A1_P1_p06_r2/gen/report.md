# Effect of supplier diversification on export growth

**Conclusion: no detectable effect.** Preferred estimate (OLS, HC1 robust SEs, n=2000, outcome export_growth_2023, adjusted for all pre-period covariates: log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign-owned, imported input share, port distance, ISO, debt ratio): coefficient on supplier_diversity = **0.051, SE 0.247, p = 0.836**. A 95% CI is roughly [-0.43, 0.54] index points per SD of diversity.

The PI hoped for a positive effect. The data do not support one once pre-period confounders are controlled.

## All specifications estimated (coef on supplier_diversity / SE / p)
1. Raw bivariate OLS: 1.782 / 0.255 / 2.7e-12. This is confounded and not preferred. The coefficient disappears once pre-period firm characteristics are added.
2. Core controls (log sales, years exporting, 2020 export growth): 0.057 / 0.246 / 0.817
3. **Full pre-period controls (preferred):** 0.051 / 0.247 / 0.836
4. Full pre-period controls plus buyer_rating_2023: -2.412 / 0.228 / 3.3e-26. Not valid. buyer_rating_2023 is measured after the treatment and is itself affected by diversity (see spec 5). Conditioning on it is a bad control or collider and induces bias.
5. Auxiliary regression of buyer_rating_2023 on diversity plus pre-period controls: 0.570 / 0.028 / 8e-92. This was a diagnostic and not an estimate of the effect of interest.
6. Full pre-period controls plus a quadratic term in diversity: linear coefficient 0.056 / 0.246 / 0.819. No evidence of nonlinearity worth reporting.

Total specifications estimated: 6 (5 for the effect on export growth, 1 diagnostic).

Caveats: this is a cross-section, so the result relies on selection on observables. Diversity is measured in 2021-2022 and the controls in 2020, so reverse causality is limited but unobserved confounding is possible.
