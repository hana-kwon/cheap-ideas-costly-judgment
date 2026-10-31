# Effect of supplier diversification on export growth

**Conclusion: positive effect (modest).** Preferred estimate: a 1 SD increase in supplier_diversity is associated with +0.693 points of export growth (the outcome has SD 11.3). The robust (HC1) SE is 0.240, and p = 0.0038. The 95% CI is about [0.22, 1.16].

Preferred specification: OLS of export_growth_2023 on supplier_diversity plus all pre-period controls: log sales, years exporting, 2020 export growth, inventory days, foreign ownership, imported-input share, port distance, ISO certification, debt ratio, listed, region and product group. Standard errors are HC1.

The estimate is causal only if these controls remove all confounding. This is a cross-section, so unobserved confounding is possible.

## Why controls matter
Firm size, export experience and prior export growth are all correlated with supplier diversity (r of about 0.2 to 0.3) and also predict export growth. The naive estimate is therefore inflated, at about 2.55, and shrinks to about 0.69 once they are controlled for.

## Variable excluded
buyer_rating_2023 is measured in 2023, after the treatment. It is correlated with diversity at 0.54. It is probably a mediator or a collider, so conditioning on it is bad control. Adding it flips the sign to -2.1, which is a bias artefact rather than a real effect. I did not use it.

## All specifications estimated (6; coefficient on supplier_diversity, HC1 SE)
1. Raw bivariate OLS: 2.553 (SE 0.246), p < 1e-24. Confounded, not preferred.
2. Controls for log sales, years exporting and 2020 export growth: 0.691 (SE 0.240), p = 0.004.
3. **Full pre-period controls (preferred)**: 0.693 (SE 0.240), p = 0.0038.
4. Full controls plus buyer_rating_2023: -2.121 (SE 0.233), p < 1e-19. Bad control, rejected.
5. Raw plus buyer_rating_2023 only: -1.141 (SE 0.241), p < 1e-5. Bad control, rejected.
6. Full controls with a diversity x product_group interaction: the effect is 0.819 for durables (p = 0.017). The interaction for nondurables is -0.246 (p = 0.58), so there is no significant heterogeneity.

I report all six, including those I rejected, to avoid selective reporting. Specifications 2, 3 and 6 agree that the effect is positive and small.
