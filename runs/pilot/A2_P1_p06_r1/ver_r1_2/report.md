# Supplier diversification and export growth

**Conclusion: no detectable effect once pre-treatment confounders are controlled.** The PI hoped for a positive effect. The data do not support one.

Preferred estimate (OLS, HC1 robust SE, N=2000): outcome export_growth_2023 regressed on supplier_diversity plus all pre-period controls. The controls are log_sales_2020, years_exporting_2020, export_growth_2020, region, listed, product_group, inventory_days, foreign_owned, share_imported_inputs, port_distance, certified_iso and debt_ratio.
- Coefficient per 1 SD of diversity: **0.051**, SE **0.247**, p = **0.836**. The 95% CI is about [-0.43, 0.54] index points.

## Specifications estimated (5)
1. Naive: growth ~ diversity. Coef 1.782, SE 0.255, p = 2.7e-12. This is confounded: firm size, tenure and past growth correlate with both diversity and growth.
2. Core controls (log sales, years exporting, past export growth). Coef 0.057, SE 0.246, p = 0.82.
3. Full pre-period controls (**preferred**). Coef 0.051, SE 0.247, p = 0.84.
4. Full controls plus buyer_rating_2023. Coef -2.41, SE 0.228, p = 3e-26. I rejected this. The rating is measured in 2023, after diversity, so it is a post-treatment variable (a mediator or collider). Conditioning on it biases the estimate.
5. Full controls plus a quadratic in diversity. Linear term 0.056, SE 0.246, p = 0.82. I did not examine the quadratic term in detail, and it was not needed for the conclusion.

The naive positive association (spec 1) disappears after adjusting for pre-period covariates. The estimates in specs 2, 3 and 5 are stable. This is a cross-section, so the result rests on selection on observables. The point estimate is near zero and the confidence interval is fairly tight, so any causal effect is small.
