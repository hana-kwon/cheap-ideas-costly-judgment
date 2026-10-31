# Effect of supplier diversification on export growth

**Conclusion: positive effect (modest, observational).** Preferred estimate: a 1-SD increase in supplier diversity is associated with +0.69 points of 2023 export growth (HC1 SE 0.240, p = 0.0038, 95% CI 0.22 to 1.16). The outcome has mean ~100 and the model R² is 0.22.

## Preferred specification
OLS of export_growth_2023 on supplier_diversity plus all pre-period controls: log_sales_2020, years_exporting_2020, export_growth_2020, region, listed, product_group, inventory_days_2020, foreign_owned, share_imported_inputs_2020, port_distance_km, certified_iso, debt_ratio_2020. N = 2000, robust (HC1) SEs.

## All specifications estimated (5)
| # | Specification | Coef on supplier_diversity | SE | p |
|---|---|---|---|---|
| 1 | Raw bivariate OLS | 2.553 | 0.246 | 3e-25 |
| 2 | + log_sales, years_exporting, export_growth_2020 | 0.691 | 0.240 | 0.0040 |
| 3 | **Full pre-period controls (preferred)** | **0.693** | **0.240** | **0.0038** |
| 4 | Full controls + buyer_rating_2023 | -2.121 | 0.233 | 8e-20 |
| 5 | Full controls + quadratic in diversity | 0.694 (linear term) | 0.240 | 0.0038 |

## Notes and caveats
- The raw estimate (2.55) is about 3.7 times the adjusted one. Larger, more experienced firms have both more suppliers and higher growth, so the raw figure is confounded. Adding the controls removes most of it.
- buyer_rating_2023 is measured in 2023, after the supplier measure (2021-22). It is plausibly an outcome of diversification (a mediator) or a collider. Controlling for it would condition on a post-treatment variable, so I excluded it from the preferred model. Spec 4 flips the sign to negative, which is a typical artefact of that bias, and I do not interpret it as a causal effect.
- The quadratic term in spec 5 gives no reason to prefer a nonlinear model. I did not report its p-value.
- This is a cross-section, so the estimate is causal only if the pre-period controls remove all confounding. Unobserved confounding is still possible. The effect is statistically clear but small in size.
- The principal investigator hoped for a positive result. I chose the preferred specification on causal-ordering grounds, not by which result looked best. Specs 1 and 4, the largest and the opposite-signed, were also not chosen.
