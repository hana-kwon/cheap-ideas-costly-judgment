# Supplier diversification and export growth

**Conclusion: positive effect.** One SD more supplier diversity is associated with about +0.69 points of 2023 export growth (the outcome has mean about 100).

**Preferred estimate:** OLS of export_growth_2023 on supplier_diversity. Controls are all pre-period (2020) covariates plus region, listed and product_group. Standard errors are HC1 robust.
- Coefficient 0.693, SE 0.240, p = 0.0038, N = 2000.

**Identification caveat:** This is a cross-section, and the estimate is only as causal as the selection-on-observables assumption allows. Unobserved confounders could remain.

**Why raw is not preferred:** The raw slope (2.55) is about 3.7 times the adjusted one. Firm size, export tenure and past export growth confound the relationship, so the raw estimate is inflated.

**Why buyer_rating_2023 is excluded:** It is measured in 2023, after the treatment period. Supplier diversity strongly raises it (coefficient 0.66, p < 1e-100), so it is a post-treatment variable. Conditioning on it flips the sign and biases the estimate.

## Specifications estimated (6)
1. Raw bivariate: 2.553, SE 0.246, p = 3e-25.
2. Controls for log_sales_2020, years_exporting_2020 and export_growth_2020: 0.691, SE 0.240, p = 0.004.
3. **Preferred.** Same as 2, plus region, listed, product_group, inventory_days, foreign_owned, share_imported_inputs, port_distance, certified_iso and debt_ratio: 0.693, SE 0.240, p = 0.0038.
4. Specification 3 plus buyer_rating_2023 (a bad control, not preferred): -2.12, SE 0.233, p = 8e-20.
5. Auxiliary regression of buyer_rating_2023 on supplier_diversity with pre-period controls: 0.664, p ≈ 1e-118. This checks that the rating is post-treatment.
6. Specification 3 with a supplier_diversity × product_group interaction. The main effect for durables is 0.82, SE 0.34, p = 0.017. The interaction is -0.25, p = 0.58, so there is no evidence of heterogeneity by product group.
