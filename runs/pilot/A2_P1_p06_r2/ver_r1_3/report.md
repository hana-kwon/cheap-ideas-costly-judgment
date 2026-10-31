# Effect of supplier diversification on export growth

## Conclusion
No credible evidence of an effect. The raw association is positive (+1.78, p<0.001). It vanishes once pre-period controls are added, mainly firm size (log sales), export tenure and past export growth. With these controls the estimate is +0.05 (SE 0.25, p=0.84). The 95% CI is about [-0.43, +0.54] export-growth index points per 1 SD of supplier diversity. This does not support the PI's hypothesis. The data are consistent with no effect, and effects larger than about 0.5 points per SD are unlikely.

## Preferred specification
OLS of export_growth_2023 on supplier_diversity plus all pre-period covariates (log_sales_2020, years_exporting_2020, export_growth_2020, region, listed, product_group, inventory_days_2020, foreign_owned, share_imported_inputs_2020, port_distance_km, certified_iso, debt_ratio_2020). HC1 robust SEs, N=2000.
Estimate 0.051, SE 0.247, p=0.836.

## All specifications estimated (5)
1. Raw bivariate OLS: 1.782, SE 0.255, p=2.7e-12. Confounded, not preferred.
2. Core controls (log sales, years exporting, past export growth): 0.057, SE 0.246, p=0.817.
3. Full pre-period controls (preferred): 0.051, SE 0.247, p=0.836.
4. Full controls plus buyer_rating_2023: -2.41, SE 0.228, p<1e-25. Not preferred. buyer_rating_2023 is measured after treatment and is likely a mediator or collider, so conditioning on it induces bias. The negative sign is likely an artifact.
5. Diagnostic only: buyer_rating_2023 regressed on supplier_diversity plus full controls: 0.570, SE 0.028. This shows diversity is strongly related to the post-treatment rating, which supports excluding it from the main model.

## Caveats
This is a cross-section with no experimental or instrumental variation. Unobserved confounding is possible. Supplier diversity was measured in 2021-2022, after the 2020 controls and before the 2023 outcome, so the timing is sensible. The linear specification was not tested against non-linear forms.
