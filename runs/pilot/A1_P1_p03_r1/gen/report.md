# Supplier diversification and export growth

**Conclusion: positive effect.** Preferred estimate: +0.69 percentage-index points of 2023 export growth per 1 SD increase in supplier diversity (HC1 SE 0.240, p = 0.0038, n = 2000). This is an association adjusted for pre-period covariates. It reads as causal only if those covariates capture all confounding.

## Specifications estimated (4 in total, OLS, HC1 robust SEs)
| # | Specification | Coef | SE | p |
|---|---|---|---|---|
| 1 | Raw: growth2023 ~ diversity | 2.553 | 0.246 | 3e-25 |
| 2 | + log_sales_2020, years_exporting_2020, export_growth_2020 | 0.691 | 0.240 | 0.0040 |
| 3 (preferred) | + all the other 2020 pre-period controls (region, listed, product group, inventory days, foreign-owned, import share, port distance, ISO, debt ratio) | 0.693 | 0.240 | 0.0038 |
| 4 | Spec 3 + buyer_rating_2023 | -2.121 | 0.233 | 8e-20 |

## Notes
- The raw estimate (2.55) is inflated by confounding. Controlling for firm size and the other pre-period characteristics cuts it by about 73%. Specs 2 and 3 agree closely.
- I did not prefer spec 4. `buyer_rating_2023` is measured after the treatment (2021-22 diversity) and is itself strongly driven by diversity (coefficient 0.66, t = 23). It is a post-treatment variable, so it may be a mediator or a collider. Conditioning on it flips the sign to -2.12, and I attribute that to the conditioning, not to a real negative effect. I report the spec for transparency only.
- Spec 3 includes only variables measured in 2020 or earlier, before the treatment window, so it avoids that problem. Unobserved confounding remains possible. I did not run nonlinearity, heterogeneity, or instrument checks.
- The PI hoped for a positive result. The positive result in spec 3 comes from the pre-specified, covariate-adjusted model, not from a search over specifications. The effect is much smaller than the raw association suggests.
