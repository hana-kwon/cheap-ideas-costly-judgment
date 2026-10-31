# Effect of supplier diversification on export growth

**Conclusion: positive effect (observational, conditional on observed pre-period confounders).**

Preferred estimate: OLS of export_growth_2023 on supplier_diversity, controlling for all 2020 pre-period covariates
(log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign owned, share imported inputs,
port distance, ISO certification, debt ratio). HC1 robust SE.
Coefficient = 0.693 index points per 1 SD of supplier diversity, SE = 0.240, p = 0.0038. N = 2000.

## Specifications estimated (5)
1. Naive, no controls: 2.553 (SE 0.246, p<1e-24). Not preferred: confounded by firm size, experience and past growth (these correlate with both diversity and the outcome).
2. Core controls (log sales, years exporting, 2020 export growth): 0.691 (SE 0.240, p=0.004).
3. **Full pre-period controls (preferred)**: 0.693 (SE 0.240, p=0.0038).
4. Full pre-period controls + buyer_rating_2023: -2.121 (SE 0.233, p<1e-19). Not preferred and not valid: buyer rating is measured in 2023, after the treatment (2021-22). It is a post-treatment variable (strongly affected by both diversity and export growth), so conditioning on it induces bias and flips the sign. Reported for transparency only.
5. Full pre-period controls + quadratic term in diversity: linear coefficient 0.694 (SE 0.240, p=0.0038); no sign of material nonlinearity.

## Caveats
Cross-sectional observational data, so unobserved confounding is possible. The naive association (2.55) is about 3.7 times the adjusted one (0.69), so the effect is modest and sensitive to controls. The estimate is stable across specifications once pre-period controls are included. The result agrees with the PI's expectation, but the specification was not chosen for that reason. It follows from excluding a post-treatment variable. The significantly negative estimate in spec 4 comes from that bad control.
