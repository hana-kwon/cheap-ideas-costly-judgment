# Effect of supplier diversification on export growth

**Conclusion: positive effect (modest).** Preferred estimate: a 1-SD increase in supplier_diversity is associated with +0.69 points of the 2023 export-growth index (SE 0.240, HC1-robust; p = 0.0038; 95% CI 0.22 to 1.16). The outcome mean is about 100.5.

## Preferred specification
OLS of export_growth_2023 on supplier_diversity plus all pre-period covariates: log sales, years exporting, 2020 export growth, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio, listed, region, and product group. N = 2000. The causal reading rests on selection on observables. This is a cross-section, so unobserved confounding cannot be ruled out.

I deliberately excluded buyer_rating_2023. It is measured after the exposure and is plausibly a mediator or a collider. Controlling for it flips the sign (see below) and I judged that estimate biased.

## All specifications estimated (6, all OLS with HC1 SEs, coefficient on supplier_diversity)
1. Naive, no controls: 2.553 (SE 0.246, p < 1e-24). Confounded: larger firms and more experienced exporters have both more suppliers and higher growth. I do not prefer it.
2. **Pre-period controls (preferred): 0.693 (SE 0.240, p = 0.0038).**
3. Pre-period controls plus buyer_rating_2023: -2.121 (SE 0.233, p < 1e-19). Not preferred because it conditions on a post-treatment variable. The correlation of buyer_rating with diversity is 0.54.
4. Minimal controls (log sales, years exporting, 2020 growth): 0.691 (SE 0.240, p = 0.0040).
5. Preferred model plus a quadratic term in diversity: linear coefficient 0.694 (SE 0.240, p = 0.0038). There is no evidence of nonlinearity.
6. Preferred model with a diversity × product_group interaction: main (durables) effect 0.819 (SE 0.342, p = 0.017). The interaction was not examined further.

## Caveats
- The naive association (2.55) overstates the effect by roughly 3.7 times relative to the adjusted estimate.
- The adjusted effect is small and survives plausible pre-period control sets. It is not robust to conditioning on the post-treatment buyer rating, which I consider inappropriate.
- Residual confounding is possible.
