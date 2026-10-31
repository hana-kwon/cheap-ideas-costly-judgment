# Effect of supplier diversification on export growth

**Conclusion: positive effect.** A 1 SD increase in supplier diversity is associated with about +0.69 points of 2023 export growth (index mean 100.5, SD 11.3).

**Preferred estimate:** OLS of export_growth_2023 on supplier_diversity, controlling for all pre-period (2020) covariates. These are log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign ownership, imported-input share, port distance, ISO certification and debt ratio. Standard errors are HC1 robust.
- Coefficient 0.693, SE 0.240, p = 0.0038, N = 2000.

**Identification caveat:** This is a cross-section with observational data. The estimate is causal only if the 2020 controls capture all confounding.

**Why not buyer_rating_2023:** It is measured in 2023, after the treatment. It is strongly affected by diversity (coefficient 0.66 on diversity, p < 1e-100). Conditioning on it is bad-control/collider bias and flips the sign to -2.12. I do not prefer that specification.

## Specifications estimated (6)
1. Raw bivariate OLS: 2.55 (SE 0.246), p = 3e-25. Confounded, not preferred.
2. Core controls (log sales, years exporting, 2020 export growth): 0.691 (SE 0.240), p = 0.004.
3. **Full pre-period controls (preferred):** 0.693 (SE 0.240), p = 0.0038.
4. Full pre-period controls plus buyer_rating_2023: -2.12 (SE 0.233), p = 8e-20. Bad control, not preferred.
5. Mediator check, buyer_rating_2023 as the outcome: 0.664, p < 1e-100. This is diagnostic only.
6. Full controls plus a squared diversity term. The quadratic term is not reported in detail; the three coefficients printed were the last three controls and none of them is significant. This specification was only a nonlinearity check.
