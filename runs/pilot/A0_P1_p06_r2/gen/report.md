# Effect of supplier diversification on export growth

**Conclusion: no effect.** After adjusting for pre-period (2020) firm characteristics, supplier diversity has no detectable association with 2023 export growth. This does not support the PI's hypothesis.

**Preferred specification:** OLS of export_growth_2023 on supplier_diversity plus all 2020 pre-period controls (log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio). HC1 robust SEs, N=2000.
- Estimate: 0.051 (index points per 1 SD of supplier diversity)
- SE: 0.247
- p = 0.836
- 95% CI is roughly [-0.43, 0.54]. This rules out effects larger than about half a point, compared with an outcome mean of about 100.8.

## Why this specification
- The naive raw regression gives +1.78 (p<1e-11), but it is confounded. Adding just log sales, years exporting and 2020 export growth cuts the coefficient to 0.06. Larger and more established firms have both more suppliers and higher export growth.
- buyer_rating_2023 is measured after the treatment and is plausibly affected by it (supplier diversity raises ratings, coefficient 0.57, p<1e-80). It is a post-treatment variable, so controlling for it is bad practice (it gives -2.41, a collider/mediator-type bias). I excluded it from the preferred model.

## All specifications estimated (8)
Coefficients are on supplier_diversity unless noted.
1. Raw bivariate OLS: 1.782, SE 0.255, p=2.7e-12 (confounded; not preferred)
2. Core controls (log sales, years exporting, 2020 export growth): 0.057, SE 0.246, p=0.817
3. **Full pre-period controls (preferred): 0.051, SE 0.247, p=0.836**
4. Full controls plus buyer_rating_2023 (post-treatment): -2.412, SE 0.228, p=3e-26 (biased; not preferred)
5. Supplier diversity plus buyer_rating_2023 only: -1.577, SE 0.231, p=1e-11 (biased; not preferred)
6. Auxiliary: buyer_rating_2023 regressed on supplier diversity with full controls: 0.570, p=4e-83 (shows rating is post-treatment; not an effect on exports)
7. Interaction with product group (full controls): main effect 0.273 (SE 0.337, p=0.42), interaction with nondurables -0.459 (SE 0.462, p=0.32). No heterogeneity detected.
8. Quadratic term (full controls): linear 0.056 (p=0.82), squared -0.184 (p=0.30). No nonlinearity detected.

## Caveats
This is a cross-section, and the analysis relies on selection on the observed 2020 covariates. Unobserved confounding is possible. Results are robust across the sensible pre-period-adjusted models.
