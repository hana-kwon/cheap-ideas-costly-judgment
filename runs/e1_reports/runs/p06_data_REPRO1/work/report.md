# Effect of supplier diversification on export growth

**Conclusion: no detectable effect.** Preferred estimate: OLS of export_growth_2023 on supplier_diversity (standardized), controlling for all pre-period covariates (log sales, years exporting, 2020 export growth, region, listed, sector, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio), HC1 robust SEs, N=2000.
Coefficient = 0.051 (SE 0.247, p = 0.836; 95% CI about -0.43 to 0.54 index points per 1 SD of supplier diversity).

Reasoning: the naive association is positive (1.78, SE 0.25), but it vanishes once the pre-treatment confounders are controlled. Firm size, in particular, drives both variables. buyer_rating_2023 is measured after treatment and probably downstream of both treatment and outcome, so it is not a valid control. Adding it produces a spurious -2.41 (collider/post-treatment bias), and I do not use it. This is observational cross-section data, so the estimate remains conditional on no unobserved confounding.

## Specifications estimated (7)
1. Naive bivariate: 1.782 (SE 0.255), p<0.001
2. + log_sales, years_exporting, export_growth_2020: 0.057 (0.246), p=0.817
3. **Full pre-period controls (preferred)**: 0.051 (0.247), p=0.836
4. Full controls + buyer_rating_2023 (rejected, post-treatment): -2.412 (0.228), p<0.001
5. Full controls + squared supplier_diversity (linear term): 0.056 (0.246), p=0.819
6. Full controls + diversity x sector interaction (main effect for durables): 0.273 (0.337), p=0.419
7. Full controls, trimmed to |supplier_diversity|<3: 0.134 (0.241), p=0.576
