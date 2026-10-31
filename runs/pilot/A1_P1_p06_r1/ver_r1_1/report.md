# Effect of supplier diversification on export growth

**Conclusion: no detectable effect.** The PI hoped for a positive effect. The data do not support one once firm size and other pre-period confounders are controlled.

## Preferred estimate
OLS of export_growth_2023 on supplier_diversity, controlling for all pre-period (2020) covariates, region, sector and listing status, with HC1 robust standard errors (N=2000):
- Coefficient: **0.051** per 1 SD of supplier diversity (percentage-point index)
- SE: **0.247**
- p-value: **0.836**
- 95% CI: about [-0.43, 0.54]

## Why this specification
- The raw association is positive (1.78, SE 0.25). It is driven by confounding. Larger, longer-exporting firms with higher past export growth have both more suppliers (correlations 0.30, 0.18 and 0.15) and higher 2023 export growth. Adjusting for them removes the effect.
- buyer_rating_2023 is measured after the treatment (2023). It is plausibly a consequence of both diversity and export outcomes, i.e. a mediator or collider. I excluded it from the preferred model. Including it gives a spurious, strongly negative coefficient (-2.41), which is a collider-bias artefact and not a causal effect.
- The design is cross-sectional and observational. Even the adjusted estimate relies on no unmeasured confounding. The CI rules out effects larger than about 0.5 points per SD.

## All specifications estimated (4, all OLS with HC1 SEs)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw bivariate | 1.782 | 0.255 | 2.7e-12 |
| 2 | + log_sales_2020, years_exporting_2020, export_growth_2020 | 0.057 | 0.246 | 0.817 |
| 3 | **Preferred**: all pre-period covariates + region, product_group, listed | 0.051 | 0.247 | 0.836 |
| 4 | #3 + buyer_rating_2023 (post-treatment; not preferred) | -2.412 | 0.228 | 3e-26 |
