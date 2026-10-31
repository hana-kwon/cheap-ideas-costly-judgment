# Effect of supplier diversification on export growth

**Conclusion: positive effect.** Preferred estimate: OLS of export_growth_2023 on supplier_diversity, controlling for all pre-period (2020) firm characteristics, region and sector, with HC1 robust SEs (n=2000).
Coefficient = 0.693 index points per 1 SD of supplier diversity, SE = 0.240, p = 0.0038 (95% CI 0.22 to 1.16).

Specifications estimated (7 regressions in total; the last two are auxiliary):
1. Raw bivariate: 2.553 (SE 0.246, p<1e-24). Not preferred, because it is confounded by firm size and experience.
2. Plus log_sales, years_exporting and export_growth_2020: 0.691 (SE 0.240, p=0.004).
3. **Preferred.** Plus all pre-period covariates, region, sector and listed: 0.693 (SE 0.240, p=0.0038).
4. Preferred plus a quadratic term in diversity: linear coefficient 0.694 (SE 0.240, p=0.0038). The quadratic term adds nothing material.
5. Preferred plus buyer_rating_2023: -2.121 (SE 0.233). Rejected. buyer_rating is measured post-treatment and is affected by diversity (diversity coefficient on rating is 0.66). Controlling for it is a bad control and biases the estimate, so I did not use it.
6. Auxiliary: buyer_rating_2023 regressed on diversity with controls, coefficient 0.664. This was used only to diagnose the post-treatment problem.
7. Auxiliary: a repeat of the preferred model with the full summary printed. It is the same model as 3.

Caveat: this is a cross-section, so the causal reading relies on selection on observables. The naive estimate is about 3.7 times larger than the adjusted one, which shows that confounding matters. Unobserved confounding may remain.
